#!/usr/bin/env python3
"""FCLR-143: deterministic handoff-freshness + mandatory-heavy-work gate.

Machine-enforced, read-only, no network, no real research_state writes, no
parquet/outcome reads. This closes the last *structural* bottleneck in the
trigger-only frontier: the mandated heavy campaign (FCLR-RCA-011 / Phase-B) was
prose-only, so a future session could "complete" by running only the trigger
check + the unittest suite and skipping the heavy artifacts entirely.

This gate binds the durable handoff to concrete evidence artifacts on disk:

  (1) The sole durable handoff ``AGENT_HANDOFF.md`` must exist, must carry the
      ``INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION`` section, and must
      record the *last completed* heavy session id and its full-suite result.
  (2) The latest session in the handoff must show new heavy work: either it
      contains the mandatory Phase-B/C evidence set (feature attribution, impl
      cross-check, sealed bridge, trigger-gated prereg skeleton, and power
      synthesis), or it carries forward a complete bundle and adds an evidence
      audit plus a fresh quantitative artifact. The gate resolves the latest
      complete bundle separately.
  (3) The ``research_state/`` root md+json count must stay <= 500 (the churn
      cap enforced by test_tracka_hardening_125) — this gate also fails if the
      cap is breached, so a session cannot flood the root to dodge the check.

Exit 0 = PASS (all conditions met). Exit 1 = FAIL (machine-readable reasons).
``--json`` prints the full payload.

Usage:
  python scripts/check_handoff_heavywork_gate.py
  python scripts/check_handoff_heavywork_gate.py --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
HANDOFF = REPO / "AGENT_HANDOFF.md"

# Markers the handoff must contain to be a valid durable handoff.
HANDOFF_REQUIRED_MARKERS = (
    "INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION",
    "AGENT HANDOFF",
)

# Phase-B / Phase-C mandatory artifacts. Each heavy session must have produced
# these under research_state/session_<UTC>/. Filenames are matched by prefix
# because the exact UTC suffix varies per session.
PHASE_B_PREFIXES = (
    "rca011_feature_attribution_",   # feature attribution (json+md)
    "rca011_impl_crosscheck_",       # independent OLS/QR cross-check
    "rca011_sealed_bridge_",         # sealed-vs-recompute bridge (md)
    "prereg_template_trigger_gated_",  # power remediation prereg skeleton
)
PHASE_C_PREFIXES = (
    "program_power_synthesis_",      # synthesis with honest next_action_heavy
)

# Root churn cap (mirrors test_tracka_hardening_125.test_root_md_json_bounded).
ROOT_COUNT_CAP = 500

# FCLR-FRONTIER-VERIFY-06/07 hardening: once a frontier campaign has started, a
# later session cannot satisfy the gate with an arbitrary recompute_* artifact. It
# must emit the campaign's exact exhaustive-audit triad plus a trigger check.
# Multiple campaigns may be declared; every campaign that has started binds.
FRONTIER_VERIFY_CAMPAIGN_RE = re.compile(r"FCLR-FRONTIER-VERIFY-(\d+)-(\d{8}T\d{6}Z)")
FRONTIER_VERIFY_ARTIFACT_PREFIX = "recompute_frontier_exhaustive_audit_"
FRONTIER_VERIFY_REQUIRED_SUFFIXES = (".py", ".json", ".md")

# FCLR-TRIGGER-READINESS-01 hardening: once the trigger-readiness campaign has
# started, a later session cannot satisfy the gate with an arbitrary recompute_*
# artifact or a trigger-check-only session. It must emit the outcome-blind
# trigger-activation package (executor + self-test + readiness certificate) plus
# a trigger check. Sessions predating the campaign are grandfathered so the gate
# stays green during the handoff refresh that first announces the campaign.
TRIGGER_READINESS_CAMPAIGN_RE = re.compile(
    r"FCLR-TRIGGER-READINESS-(\d+)-(\d{8}T\d{6}Z)"
)
TRIGGER_READINESS_ARTIFACT_PREFIXES = (
    "trigger_activation_executor_",
    "trigger_activation_selftest_",
    "trigger_activation_readiness_",
)
# (prefix, required_suffix) pairs that must ALL be present in the latest session.
TRIGGER_READINESS_REQUIRED = (
    ("trigger_activation_executor_", ".py"),
    ("trigger_activation_executor_", ".json"),
    ("trigger_activation_selftest_", ".py"),
    ("trigger_activation_selftest_", ".json"),
    ("trigger_activation_readiness_", ".json"),
    ("trigger_activation_readiness_", ".md"),
)

_SESSION_DIR_RE = re.compile(r"(session_\d{8}T\d{6}Z)")

# FCLR-LEDGER-INTEGRITY-02 hardening: once the ledger-integrity campaign has
# started, a post-start session cannot satisfy the gate with an arbitrary
# recompute_* artifact or a trigger-check-only session. It must emit the
# outcome-blind per-month consumed-window ledger audit, the frontier recompute,
# the trigger check, and the refreshed trigger-activation readiness. Sessions
# predating the campaign are grandfathered so the gate stays green during the
# handoff refresh that first announces the campaign.
LEDGER_INTEGRITY_CAMPAIGN_RE = re.compile(
    r"FCLR-LEDGER-INTEGRITY-(\d+)-(\d{8}T\d{6}Z)"
)
# (prefix, required_suffix) pairs that must ALL be present in the latest session.
LEDGER_INTEGRITY_REQUIRED = (
    ("ledger_audit_", ".json"),
    ("frontier_recompute_", ".json"),
    ("trigger_check_", ".json"),
    ("trigger_activation_readiness_", ".json"),
)

# FCLR-CLOSURE-LEDGER-COMPLETENESS-01 hardening: once this campaign starts, a
# post-start session cannot satisfy the gate with an arbitrary recompute_*
# artifact. It must emit the non-authoritative closure-ledger sidecar + the
# completeness validator (py + json output) + a trigger check. Sessions predating
# the campaign are grandfathered.
CLOSURE_LEDGER_CAMPAIGN_RE = re.compile(
    r"FCLR-CLOSURE-LEDGER-COMPLETENESS-(\d+)-(\d{8}T\d{6}Z)"
)
CLOSURE_LEDGER_REQUIRED = (
    ("closure_ledger_sidecar_", ".json"),
    ("closure_ledger_validator_", ".py"),
    ("closure_ledger_validator_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-VOL-LIQ-EXECUTION-01 hardening: the next session must produce the two
# heavy research tracks (Track C stdlib forecast + Track B modeled breach
# labels), not another audit-only or gate-only session. A post-start session
# must contain the exact source/result/report triad for both tracks, a trigger
# check, and no zero-byte placeholders. Sessions predating the campaign are
# grandfathered so this handoff refresh remains green.
VOL_LIQ_EXECUTION_CAMPAIGN_RE = re.compile(
    r"FCLR-VOL-LIQ-EXECUTION-(\d+)-(\d{8}T\d{6}Z)"
)
VOL_LIQ_EXECUTION_REQUIRED = (
    ("trackc_design_a_forecast_", ".py"),
    ("trackc_design_a_forecast_", ".json"),
    ("trackc_design_a_forecast_", ".md"),
    ("trackb_breach_labels_", ".py"),
    ("trackb_breach_labels_", ".json"),
    ("trackb_breach_labels_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-VOL-LIQ-BREACH-FORECAST-03 hardening: the next focus campaign advances the
# science past Track C (volatility) + Track B (modeled breach labels) by joining
# them — do funding-conditioned volatility features predict modeled
# liquidation-boundary breaches? Once this campaign starts, a post-start session
# cannot satisfy the gate with an audit-only, gate-only, or Track-C/B-only rerun.
# It must emit the outcome-blind breach-forecast prereg (frozen before outcomes),
# the forecast source/result/report triad, and a trigger check. Sessions predating
# the campaign are grandfathered so this handoff refresh remains green.
BREACH_FORECAST_CAMPAIGN_RE = re.compile(
    r"FCLR-VOL-LIQ-BREACH-FORECAST-(\d+)-(\d{8}T\d{6}Z)"
)
BREACH_FORECAST_REQUIRED = (
    ("trackbc_breach_prereg_", ".json"),
    ("trackbc_breach_forecast_", ".py"),
    ("trackbc_breach_forecast_", ".json"),
    ("trackbc_breach_forecast_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-VOL-LIQ-ROBUST-04 hardening: the next focus campaign advances the science
# past Track C + Track B by confirming the Track C funding-trail QLIKE improvement
# under an alternative chronological holdout, stdlib only. Once this campaign
# starts (start UTC 120000Z), a post-start session cannot satisfy the gate with an
# audit-only or gate-only session. It must emit the outcome-blind robust-04 prereg,
# the robustness recompute triad, and a trigger check. Sessions predating the
# campaign start (incl. session_20261118T114500Z) are grandfathered so this handoff
# refresh remains green.
ROBUST_04_CAMPAIGN_RE = re.compile(r"FCLR-VOL-LIQ-ROBUST-04-(\d{8}T\d{6}Z)")
ROBUST_04_REQUIRED = (
    ("fclr_robust04_prereg_", ".json"),
    ("fclr_robust04_prereg_", ".md"),
    ("fclr_robust04_robustness_", ".py"),
    ("fclr_robust04_robustness_", ".json"),
    ("fclr_robust04_robustness_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-VOL-LIQ-ROBUST-05 hardening: the next focus campaign advances the science
# past the sign-corrected Track C result. Once this campaign starts (start UTC
# 20261118T132800Z), a post-start session cannot satisfy the gate with an
# audit-only or gate-only session. It must emit the outcome-blind robust-05
# prereg, the robustness recompute triad, and a trigger check. Sessions predating
# the campaign start (incl. session_20261118T132800Z) are grandfathered so this
# handoff refresh remains green.
ROBUST_05_CAMPAIGN_RE = re.compile(r"FCLR-VOL-LIQ-ROBUST-05-(\d{8}T\d{6}Z)")
ROBUST_05_REQUIRED = (
    ("fclr_robust05_prereg_", ".json"),
    ("fclr_robust05_prereg_", ".md"),
    ("fclr_robust05_robustness_", ".py"),
    ("fclr_robust05_robustness_", ".json"),
    ("fclr_robust05_robustness_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-RISK-CALIBRATION-06 hardening: ROBUST-05 rejected the funding-conditioned
# volatility hypothesis under QLIKE, so the next focus campaign advances the
# repository's *liquidation-risk* pillar instead of re-running a QLIKE variant. A
# post-start session must emit the outcome-blind risk-06 prereg, the multi-month
# modeled breach-label package, the out-of-sample Brier/log-loss calibration triad,
# and a trigger check, with no zero-byte placeholders. Sessions predating the
# campaign start are grandfathered so this handoff refresh stays green.
RISK_06_CAMPAIGN_RE = re.compile(
    r"FCLR-LIQ-RISK-CALIBRATION-(\d+)-(\d{8}T\d{6}Z)"
)
RISK_06_REQUIRED = (
    ("fclr_risk06_prereg_", ".json"),
    ("fclr_risk06_prereg_", ".md"),
    ("fclr_risk06_labels_", ".py"),
    ("fclr_risk06_labels_", ".json"),
    ("fclr_risk06_labels_", ".md"),
    ("fclr_risk06_calibration_", ".py"),
    ("fclr_risk06_calibration_", ".json"),
    ("fclr_risk06_calibration_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-RISK-RECALIBRATION-07 hardening: RISK-06 found no funding-conditioned
# Brier improvement on modeled breach risk, so the next focus campaign asks a
# different, still-heavy question: is the *baseline itself* miscalibrated, and can
# a train-only recalibration layer (Platt/logistic, stdlib PAVA isotonic, and a
# scenario base-rate offset) materially improve out-of-sample calibration (ECE and
# Brier) and transfer across scenarios? A post-start session must emit the
# outcome-blind prereg, the calibrator implementation triad, the recalibration
# evaluation triad, and a trigger check, with no zero-byte placeholders.
RISK_07_CAMPAIGN_RE = re.compile(
    r"FCLR-LIQ-RISK-RECALIBRATION-(\d+)-(\d{8}T\d{6}Z)"
)
RISK_07_REQUIRED = (
    ("fclr_risk07_prereg_", ".json"),
    ("fclr_risk07_prereg_", ".md"),
    ("fclr_risk07_calibrators_", ".py"),
    ("fclr_risk07_calibrators_", ".json"),
    ("fclr_risk07_recalibration_", ".py"),
    ("fclr_risk07_recalibration_", ".json"),
    ("fclr_risk07_recalibration_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-TRACKA-CONFIRMATORY-01 hardening: the 12-month Track A extension is
# ADMISSIBLE and its confirmatory three-block design is registered. The next
# focus campaign must actually execute the heavy confirmatory test, not another
# trigger check or descriptive-only replay. A post-start session must emit the
# power/MDE audit triad, the independent stdlib recompute, the confirmatory
# evaluation triad, and a trigger check, with no zero-byte placeholders. If the
# power audit returns UNDERPOWERED, the evaluation artifacts must still be
# written with status UNDERPOWERED and the frozen decision recorded.
TRACKA_CONFIRMATORY_CAMPAIGN_RE = re.compile(
    r"FCLR-LIQ-TRACKA-CONFIRMATORY-(\d+)-(\d{8}T\d{6}Z)"
)
TRACKA_CONFIRMATORY_REQUIRED = (
    ("fclr_tracka_confirmatory01_power_", ".py"),
    ("fclr_tracka_confirmatory01_power_", ".json"),
    ("fclr_tracka_confirmatory01_power_", ".md"),
    ("fclr_tracka_confirmatory01_recompute_", ".py"),
    ("fclr_tracka_confirmatory01_recompute_", ".json"),
    ("fclr_tracka_confirmatory01_evaluation_", ".py"),
    ("fclr_tracka_confirmatory01_evaluation_", ".json"),
    ("fclr_tracka_confirmatory01_evaluation_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-RISK-ESCALATION-08 hardening: the Track A confirmatory campaign returned
# NOT_MET on observed labels, so the next focus campaign must escalate rather than
# replay it: a joint funding x RV x open-interest regime model on the 12-month Track
# A panel, behind a fresh outcome-blind prereg frozen before any outcome is computed.
# A post-start session must emit the prereg, the power/MDE audit triad, the
# independent stdlib recompute, the evaluation triad, and a trigger check, with no
# zero-byte placeholders. Descriptions, trigger-only sessions, and arbitrary
# recompute_* files fail closed. Sessions predating the campaign start are
# grandfathered so this handoff refresh remains green.
RISK_08_CAMPAIGN_RE = re.compile(
    r"FCLR-LIQ-RISK-ESCALATION-(\d+)-(\d{8}T\d{6}Z)"
)
RISK_08_REQUIRED = (
    ("fclr_risk08_prereg_", ".json"),
    ("fclr_risk08_prereg_", ".md"),
    ("fclr_risk08_power_", ".py"),
    ("fclr_risk08_power_", ".json"),
    ("fclr_risk08_power_", ".md"),
    ("fclr_risk08_recompute_", ".py"),
    ("fclr_risk08_recompute_", ".json"),
    ("fclr_risk08_evaluation_", ".py"),
    ("fclr_risk08_evaluation_", ".json"),
    ("fclr_risk08_evaluation_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-SESSION-SYNTHESIS-01 hardening: once the consolidation + quantitative
# meta-analysis campaign starts (start UTC 20261121T080000Z), a post-start
# session cannot satisfy the gate with a trigger-only, prose-only, audit-only,
# or arbitrary recompute_* session. It must emit the outcome-blind protocol
# freeze, the program synthesis report, the frontier exhaustion audit, the
# negative-results preservation, the quantitative meta-analysis triad
# (py+json+md), the independent stdlib recompute (py+json), and a trigger check.
# This removes the trigger-only idle bottleneck: future agents cannot idle
# waiting for an external NEW_OBSERVED_LIQUIDATION_SOURCE trigger; they must
# execute the heavy consolidation work or emit a valid materially-different
# free-data route. Sessions predating the campaign start are grandfathered so
# this handoff refresh remains green.
SESSION_SYNTHESIS_CAMPAIGN_RE = re.compile(
    r"FCLR-SESSION-SYNTHESIS-(\d+)-(\d{8}T\d{6}Z)"
)
SESSION_SYNTHESIS_REQUIRED = (
    ("fclr_session_synth01_protocol_freeze_", ".json"),
    ("fclr_session_synth01_protocol_freeze_", ".md"),
    ("fclr_session_synth01_program_synthesis_report_", ".json"),
    ("fclr_session_synth01_program_synthesis_report_", ".md"),
    ("fclr_session_synth01_frontier_exhaustion_audit_", ".json"),
    ("fclr_session_synth01_frontier_exhaustion_audit_", ".md"),
    ("fclr_session_synth01_negative_results_preservation_", ".json"),
    ("fclr_session_synth01_meta_analysis_", ".py"),
    ("fclr_session_synth01_meta_analysis_", ".json"),
    ("fclr_session_synth01_meta_analysis_", ".md"),
    ("fclr_session_synth01_recompute_", ".py"),
    ("fclr_session_synth01_recompute_", ".json"),
    ("evidence_audit_", ".json"),
    ("evidence_audit_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-PANEL-FE-001 hardening: the frozen-data frontier is exhausted for new
# 3-block confirmatory designs (next_campaign_status.py:
# NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN) and the liquidation-risk OOS
# hypothesis is gated on an external NEW_OBSERVED_LIQUIDATION_SOURCE trigger that
# cannot fire inside this closed, frozen-data environment. That trigger gate was
# the structural bottleneck: a future agent would idle waiting for a signal the
# frozen panel cannot produce. This campaign removes the bottleneck by mandating
# a materially different, feasible design on the existing frozen panels: a panel
# fixed-effects funding-conditioning study of realized volatility (RV) and
# liquidation intensity with a walk-forward out-of-sample evaluation. Once this
# campaign starts, a post-start session cannot satisfy the gate with a trigger-
# only, prose-only, audit-only, or arbitrary recompute_* session. It must emit
# the outcome-blind prereg freeze, the panel-FE evaluation triad, the independent
# stdlib recompute, the evidence audit, and a non-empty trigger check. Sessions
# predating the campaign start are grandfathered so this handoff refresh that
# first announces the campaign stays green.
PANEL_FE_CAMPAIGN_RE = re.compile(r"FCLR-PANEL-FE-(\d+)-(\d{8}T\d{6}Z)")
PANEL_FE_REQUIRED = (
    ("fclr_panelfe01_prereg_", ".json"),
    ("fclr_panelfe01_prereg_", ".md"),
    ("fclr_panelfe01_eval_", ".py"),
    ("fclr_panelfe01_eval_", ".json"),
    ("fclr_panelfe01_eval_", ".md"),
    ("fclr_panelfe01_recompute_", ".py"),
    ("fclr_panelfe01_recompute_", ".json"),
    ("fclr_panelfe01_evidence_audit_", ".json"),
    ("fclr_panelfe01_evidence_audit_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-CONTAGION-001 hardening: the cross-coin liquidation-contagion and
# funding-mediated spillover campaign is the current rank-0 focus. The handoff
# claims it is "machine-enforced by the gate", so the gate must actually bind it:
# once this campaign starts (start UTC 20261121T174500Z), a post-start session
# cannot satisfy the gate with a trigger-only, prose-only, audit-only, or
# arbitrary recompute_* session. It must emit the outcome-blind contagion prereg
# freeze, the heavy contagion evaluation triad (py+json+md: hourly aggregation,
# 15x15 lead-lag matrix, 210-pair Granger causality, 1000+ permutations,
# funding-conditioned splits, temporal stability), the independent stdlib
# recompute (py+json), the contagion evidence audit (json+md), the gate-critical
# evidence_audit_ alias (json), and a trigger check, with no zero-byte
# placeholders. Sessions predating the campaign start are grandfathered so this
# handoff refresh stays green.
# FCLR-LIQ-CONTAGION-002 hardening: FCLR-LIQ-CONTAGION-001 left a disclosed,
# unresolved methodological discrepancy on the frozen 1.74M panel: the edge set
# was NOT robust to the multiple-testing correction (eval = Granger-Bonferroni
# INTERSECT permutation-Bonferroni = 11 edges; independent recompute = empirical-
# p only = 58 edges; 155 Granger-significant pairs collapse to 11 or 16 depending
# on the criterion). The declared 2% per-edge materiality floor was asserted True
# but never actually computed (no per-edge variance-explained field exists), and
# the funding-tercile / temporal-stability results were never reconciled against
# the primary edge set. The 2026-11-21T19:51:14Z handoff declared the frontier
# exhausted and told future agents to "verify green and stop" — which would let
# them dodge this heavy reconciliation forever. This campaign removes that
# bottleneck: it mandates a materially different, feasible, HEAVY robustness-
# reconciliation study on the SAME frozen panel, behind a fresh outcome-blind
# prereg frozen before any outcome is computed. Once this campaign starts
# (start UTC 20261121T200000Z), a post-start session cannot satisfy the gate with
# a trigger-only, prose-only, audit-only, verify-and-stop, or arbitrary
# recompute_* session. It must emit the outcome-blind robustness prereg freeze,
# the heavy reconciliation evaluation triad (py+json+md: per-edge variance-
# explained / materiality, Bonferroni vs BH-FDR vs permutation-empirical edge-set
# robustness ladder, tercile-and-stability reconciliation against the primary
# edge set, bootstrap edge-set stability), the independent stdlib recompute
# (py+json), the evidence audit (json+md), the gate-critical evidence_audit_
# alias (json), and a trigger check, with no zero-byte placeholders. Sessions
# predating the campaign start (incl. session_20261121T193000Z) are grandfathered
# so this handoff refresh stays green.
CONTAGION_002_CAMPAIGN_RE = re.compile(r"FCLR-LIQ-CONTAGION-(\d+)-(\d{8}T\d{6}Z)")
CONTAGION_002_REQUIRED = (
    ("fclr_liq_contagion02_prereg_", ".json"),
    ("fclr_liq_contagion02_prereg_", ".md"),
    ("fclr_liq_contagion02_recon_", ".py"),
    ("fclr_liq_contagion02_recon_", ".json"),
    ("fclr_liq_contagion02_recon_", ".md"),
    ("fclr_liq_contagion02_recompute_", ".py"),
    ("fclr_liq_contagion02_recompute_", ".json"),
    ("fclr_liq_contagion02_evidence_audit_", ".json"),
    ("fclr_liq_contagion02_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

CONTAGION_CAMPAIGN_RE = re.compile(r"FCLR-LIQ-CONTAGION-(\d+)-(\d{8}T\d{6}Z)")
CONTAGION_REQUIRED = (
    ("fclr_liq_contagion01_prereg_", ".json"),
    ("fclr_liq_contagion01_prereg_", ".md"),
    ("fclr_liq_contagion01_eval_", ".py"),
    ("fclr_liq_contagion01_eval_", ".json"),
    ("fclr_liq_contagion01_eval_", ".md"),
    ("fclr_liq_contagion01_recompute_", ".py"),
    ("fclr_liq_contagion01_recompute_", ".json"),
    ("fclr_liq_contagion01_evidence_audit_", ".json"),
    ("fclr_liq_contagion01_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# New-style heavy sessions do not copy the static Phase-B bundle into every
# session directory. They carry forward a complete bundle and add a fresh
# evidence audit plus a new quantitative artifact. This keeps the gate from
# failing merely because the handoff records the latest audit session rather
# than the older complete bundle.
# FCLR-STARTER-001 non-avoidance: the RESEARCH_PROMPT.md §14 frozen starter
# protocol is the only open confirmatory path (Track A power-blocked by RISK-12,
# Track B NOT_SUPPORTED). A post-start session must emit the protocol freeze
# (hash-bound to §14), the panel hash freeze, and the B0/B1 baseline triad, plus
# a trigger check. Any free-text claim of a frozen protocol without these
# artifacts fails closed. The campaign must NOT overwrite the sealed legacy
# research_state/research_protocol.md (that file is the FCLR-001 2024-01..03
# experiment definition consumed by scripts/run_evaluation.py).
STARTER_CAMPAIGN_RE = re.compile(r"FCLR-STARTER-(\d+)-(\d{8}T\d{6}Z)")
STARTER_PROTOCOL_PREFIX = "fclr_starter001_protocol_freeze_"
STARTER_PANEL_PREFIX = "fclr_starter001_panel_freeze_"
STARTER_BASELINES_PREFIX = "fclr_starter001_baselines_"
STARTER_REQUIRED = (
    (STARTER_PROTOCOL_PREFIX, ".json"),
    (STARTER_PROTOCOL_PREFIX, ".md"),
    (STARTER_PANEL_PREFIX, ".json"),
    (STARTER_PANEL_PREFIX, ".md"),
    (STARTER_BASELINES_PREFIX, ".py"),
    (STARTER_BASELINES_PREFIX, ".json"),
    (STARTER_BASELINES_PREFIX, ".md"),
    ("trigger_check_", ".json"),
)
# §14 body markers used by the freeze validator.
STARTER_SECTION_HEADING = "## 14. Mandatory frozen starter protocol: FCLR-001"
STARTER_SEALED_PROTOCOL = "research_state/research_protocol.md"

# FCLR-LIVE-ARCHIVE hardening: the frozen-data frontier is exhausted
# (next_campaign_status.py: NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN) and the
# prior handoff told future agents the only remaining path was an *unverified*
# free-data route that might not exist — leaving a prose-only / source-probe-only
# escape hatch that could pass the gate without any heavy research. This campaign
# removes that bottleneck: a materially different, verified, unauthenticated free
# source (the Binance public market-data archive at data.binance.vision — the
# ``metrics`` dataset of daily open interest + taker long/short flow, deep
# 2020-09 -> present, plus fundingRate/klines/mark/index/premium) is reachable and
# was never exploited. Once this campaign starts, a post-start session cannot
# satisfy the gate with a trigger-only, prose-only, source-probe-only, audit-only,
# or verify-and-stop session. It must emit the outcome-blind source registry +
# verified-download evidence, the outcome-blind prereg freeze, the heavy 3-block
# confirmatory evaluation triad (py+json+md) on the newly downloaded archive data,
# the independent stdlib recompute (py+json), the evidence audit (json+md), the
# gate-critical evidence_audit_ alias (json), and a trigger check, with no
# zero-byte placeholders. Sessions predating the campaign start are grandfathered
# so this handoff refresh that first announces the campaign stays green.
LIVE_ARCHIVE_CAMPAIGN_RE = re.compile(r"FCLR-LIVE-ARCHIVE-(\d+)-(\d{8}T\d{6}Z)")
LIVE_ARCHIVE_REQUIRED = (
    ("fclr_live_archive_source_registry_", ".json"),
    ("fclr_live_archive_source_registry_", ".md"),
    ("fclr_live_archive_prereg_", ".json"),
    ("fclr_live_archive_prereg_", ".md"),
    ("fclr_live_archive_eval_", ".py"),
    ("fclr_live_archive_eval_", ".json"),
    ("fclr_live_archive_eval_", ".md"),
    ("fclr_live_archive_recompute_", ".py"),
    ("fclr_live_archive_recompute_", ".json"),
    ("fclr_live_archive_evidence_audit_", ".json"),
    ("fclr_live_archive_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-NEXT-SOURCE-VERIFY-01 hardening: the sole rank-0 campaign after the
# frozen + reachable-archive frontiers are both exhausted. Once this campaign
# starts (start UTC 20261122T013100Z), a post-start session cannot satisfy the
# gate with an arbitrary recompute_* artifact, a trigger-check-only session,
# a source-probe-only session, or a verify-and-stop session. It must emit the
# full FCLR-NEXT-SOURCE-VERIFY-01 artifact set: source registry +
# verified-download evidence, outcome-blind prereg freeze, heavy 3-block
# confirmatory evaluation triad (py+json+md), independent stdlib recompute
# (py+json), evidence audit (json+md), gate-critical evidence_audit_ alias
# (json), and non-empty trigger_check (json). Sessions predating the campaign
# start are grandfathered so this handoff refresh that first announces the
# campaign stays green.
NEXT_SOURCE_VERIFY_CAMPAIGN_RE = re.compile(r"FCLR-NEXT-SOURCE-VERIFY-(\d+)-(\d{8}T\d{6}Z)")
NEXT_SOURCE_VERIFY_REQUIRED = (
    ("fclr_next_source_verify_source_registry_", ".json"),
    ("fclr_next_source_verify_source_registry_", ".md"),
    ("fclr_next_source_verify_prereg_", ".json"),
    ("fclr_next_source_verify_prereg_", ".md"),
    ("fclr_next_source_verify_eval_", ".py"),
    ("fclr_next_source_verify_eval_", ".json"),
    ("fclr_next_source_verify_eval_", ".md"),
    ("fclr_next_source_verify_recompute_", ".py"),
    ("fclr_next_source_verify_recompute_", ".json"),
    ("fclr_next_source_verify_evidence_audit_", ".json"),
    ("fclr_next_source_verify_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-TRACKA-SOURCE-AUDIT-01 hardening: the rank-0 campaign after Track A
# observed-liquidation forecasting returns NOT_SUPPORTED on the ironflow capped
# feed and the frozen + reachable-archive frontiers are exhausted. Per
# RESEARCH_PROMPT.md §16 (three blocked routes -> new experiment) and §5/§10
# priority #2 (enumerate/test/rank admissible free observed-liquidation sources),
# the only honest path forward is a formal Track A source viability audit that
# either unlocks a new observed-liquidation source or formally closes Track A
# and pivots to a frozen Track B modeled-breach protocol. The prior handoff
# CLAIMED this campaign was gate-enforced but no binder existed, so a future
# session could skip the heavy source audit entirely and still pass with a
# trigger-only or verify-and-stop session. This binder removes that bottleneck:
# once the campaign starts, a post-start session cannot satisfy the gate with a
# trigger-only, prose-only, source-probe-only, audit-only, or verify-and-stop
# session. It must emit the source registry + probe triad, the outcome-blind
# viability decision, the pivot prereg, the evidence audit, the gate-critical
# evidence_audit_ alias, and a trigger check, with no zero-byte placeholders.
#
# FCLR-TRACKA-SOURCE-AUDIT-01 heavy-work hardening (2026-11-22T234900Z): the
# first binder still let a post-start session stop at the pivot PREREG and defer
# the actual heavy quantitative evaluation to a later session. That was the last
# remaining "audit-only / prereg-only" escape hatch: an agent could enumerate
# sources, freeze a prereg, and never run the heavy Track A (new source) or
# Track B (modeled breach) evaluation. This amendment binds the heavy evaluation
# itself into the same session: a post-start session must ALSO emit the
# outcome-blind evaluation triad (fclr_tracks01_eval_ py+json+md) AND an
# independent stdlib recompute (fclr_tracks01_recompute_ py+json), in addition
# to the audit/registry/probe/viability/pivot set. Whichever branch the viability
# decision selects (NEW_TRACK_A_SOURCE_FOUND -> heavy Track A confirm; or
# TRACK_A_STRUCTURALLY_BLOCKED -> heavy Track B modeled-breach), the heavy
# evaluation runs in THIS session and cannot be deferred. Zero-byte placeholders
# fail closed. Sessions predating the campaign start are grandfathered so this
# handoff refresh stays green.
TRACKA_SOURCE_AUDIT_CAMPAIGN_RE = re.compile(
    r"FCLR-TRACKA-SOURCE-AUDIT-(\d+)-(\d{8}T\d{6}Z)"
)
TRACKA_SOURCE_AUDIT_REQUIRED = (
    ("fclr_tracks01_source_registry_", ".json"),
    ("fclr_tracks01_source_registry_", ".md"),
    ("fclr_tracks01_probe_", ".py"),
    ("fclr_tracks01_probe_", ".json"),
    ("fclr_tracks01_probe_", ".md"),
    ("fclr_tracks01_viability_decision_", ".json"),
    ("fclr_tracks01_viability_decision_", ".md"),
    ("fclr_tracks01_pivot_prereg_", ".json"),
    ("fclr_tracks01_pivot_prereg_", ".md"),
    ("fclr_tracks01_eval_", ".py"),
    ("fclr_tracks01_eval_", ".json"),
    ("fclr_tracks01_eval_", ".md"),
    ("fclr_tracks01_recompute_", ".py"),
    ("fclr_tracks01_recompute_", ".json"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-XSEC-BROAD-TS-01 hardening: FCLR-LIQ-XSEC-BROAD-01 (session_20261123T085507Z)
# returned SUPPORTED_GENERALIZATION for the regime-conditioned cross-sectional
# funding -> next-hour observed liquidation-intensity association on the broad
# 342-coin ironflow_bulk universe, but its prereg never tested TEMPORAL STABILITY
# of the per-block rank-IC series. RESEARCH_PROMPT.md §17 promotion condition #4
# requires that skill "is not dominated by ... one time block", and the sibling
# FCLR-LIQ-RISK-PROGRAM-CLOSURE-01 hardening: the confirmatory liquidation-risk
# program has exhausted all feasible paths on the frozen ironflow_bulk panel
# (Track A STRUCTURALLY_BLOCKED; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED;
# cross-sectional SUPPORTED_GENERALIZATION but NOT_STABLE + materiality floor
# NOT MET). The next focus campaign is the formal program closure + complete
# negative-results synthesis per RESEARCH_PROMPT.md §13/§19/§20. Once this
# campaign starts (start UTC below), a post-start session cannot satisfy the
# gate with a trigger-only, prose-only, audit-only, verify-and-stop, or
# arbitrary recompute_* session. It must emit the outcome-blind closure protocol
# freeze, the complete negative-results synthesis report, the frontier
# exhaustion audit, the negative-results preservation record, the quantitative
# meta-analysis triad, the independent stdlib recompute, the gate-critical
# evidence_audit alias, and a non-empty trigger check, all under one fresh
# session_<UTC>/ with no zero-byte placeholders. Sessions predating the
# campaign start are grandfathered so this handoff refresh stays green.
PROGRAM_CLOSURE_CAMPAIGN_RE = re.compile(
    r"FCLR-LIQ-RISK-PROGRAM-CLOSURE-(\d+)-(\d{8}T\d{6}Z)"
)
PROGRAM_CLOSURE_REQUIRED = (
    ("fclr_liq_risk_program_closure_protocol_freeze_", ".json"),
    ("fclr_liq_risk_program_closure_protocol_freeze_", ".md"),
    ("fclr_liq_risk_program_closure_synthesis_report_", ".json"),
    ("fclr_liq_risk_program_closure_synthesis_report_", ".md"),
    ("fclr_liq_risk_program_closure_frontier_exhaustion_audit_", ".json"),
    ("fclr_liq_risk_program_closure_frontier_exhaustion_audit_", ".md"),
    ("fclr_liq_risk_program_closure_negative_results_preservation_", ".json"),
    ("fclr_liq_risk_program_closure_negative_results_preservation_", ".md"),
    ("fclr_liq_risk_program_closure_meta_analysis_", ".py"),
    ("fclr_liq_risk_program_closure_meta_analysis_", ".json"),
    ("fclr_liq_risk_program_closure_meta_analysis_", ".md"),
    ("fclr_liq_risk_program_closure_recompute_", ".py"),
    ("fclr_liq_risk_program_closure_recompute_", ".json"),
    ("evidence_audit_", ".json"),
    ("evidence_audit_", ".md"),
    ("trigger_check_", ".json"),
)

# FCLR-VOL-BROAD-01 hardening: the repository name leads with
# "Funding-conditioned-volatility", yet every leakage-robust volatility null
# (FCLR-011, FCLR-PANEL-FE-001) was established on a 5-coin panel. The broad
# 342-coin, 18-month ironflow_bulk panel that produced the only SUPPORTED
# liquidation-risk finding has never been used for a direct funding-conditioned
# realized-volatility forecast. The liquidation-risk half's confirmatory paths
# are exhausted on the frozen panel, so the unfinished repo-name frontier is
# Half 1 (funding-conditioned volatility) at broad scale. Once this campaign
# starts, a post-start session cannot satisfy the gate with a trigger-only,
# prose-only, audit-only, prereg-only, verify-and-stop, or arbitrary
# recompute_* session. It must emit the on-disk source registry, the
# outcome-blind prereg freeze, the heavy broad-panel walk-forward evaluation
# triad (py+json+md), the independent stdlib recompute (py+json), the evidence
# audit (json+md), the gate-critical evidence_audit_ alias (json), and a
# non-empty trigger check (json), all under one fresh session_<UTC>/ with no
# zero-byte placeholders. Sessions predating the campaign start are grandfathered
# so this handoff refresh that first announces the campaign stays green.
VOL_BROAD_CAMPAIGN_RE = re.compile(r"FCLR-VOL-BROAD-(\d+)-(\d{8}T\d{6}Z)")
VOL_BROAD_REQUIRED = (
    ("fclr_volbroad01_source_registry_", ".json"),
    ("fclr_volbroad01_source_registry_", ".md"),
    ("fclr_volbroad01_prereg_", ".json"),
    ("fclr_volbroad01_prereg_", ".md"),
    ("fclr_volbroad01_eval_", ".py"),
    ("fclr_volbroad01_eval_", ".json"),
    ("fclr_volbroad01_eval_", ".md"),
    ("fclr_volbroad01_recompute_", ".py"),
    ("fclr_volbroad01_recompute_", ".json"),
    ("fclr_volbroad01_evidence_audit_", ".json"),
    ("fclr_volbroad01_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-CONTAGION-002 campaign was created precisely to close the same gap for
# the contagion hypothesis (rolling-window edge-set stability). The BROAD-01
# SUPPORTED finding is the ONLY liquidation-risk result ever marked SUPPORTED, and
# it was declared the "durable final answer" without ever being asked whether it
# survives a rolling holdout. That is a prose-only / verify-and-stop escape hatch:
# a future agent could stop at "verify green" and never test whether the
# generalization holds across time. This campaign removes that bottleneck: once
# it starts, a post-start session cannot satisfy the gate with a trigger-only,
# prose-only, audit-only, prereg-only, verify-and-stop, or arbitrary recompute_*
# session. It must emit the outcome-blind temporal-stability prereg, the heavy
# rolling-window evaluation triad, the independent stdlib recompute, the evidence
# audit, the gate-critical evidence_audit_ alias, and a trigger check, with no
# zero-byte placeholders. Sessions predating the campaign start are grandfathered
# so this handoff refresh stays green.
BROAD_TS_CAMPAIGN_RE = re.compile(
    r"FCLR-LIQ-XSEC-BROAD-TS-(\d+)-(\d{8}T\d{6}Z)"
)
BROAD_TS_REQUIRED = (
    ("fclr_liqxsecbroad01_ts_prereg_", ".json"),
    ("fclr_liqxsecbroad01_ts_prereg_", ".md"),
    ("fclr_liqxsecbroad01_ts_eval_", ".py"),
    ("fclr_liqxsecbroad01_ts_eval_", ".json"),
    ("fclr_liqxsecbroad01_ts_eval_", ".md"),
    ("fclr_liqxsecbroad01_ts_recompute_", ".py"),
    ("fclr_liqxsecbroad01_ts_recompute_", ".json"),
    ("fclr_liqxsecbroad01_ts_evidence_audit_", ".json"),
    ("fclr_liqxsecbroad01_ts_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-LIQ-XSEC-BROAD-01 hardening: the SUPPORTED regime-conditioned
# cross-sectional funding -> next-hour observed liquidation intensity findings
# (FCLR-XSEC-004/005/006) were established on the 15-coin combined
# metpie+ironflow panel and flagged promotable=false precisely because they had
# not been shown to GENERALIZE beyond that narrow universe. The on-disk
# ironflow_bulk archive holds 18 months (2025-05..2026-10) of observed
# liquidations + funding + open_interest + candles across 342 coins that has
# NEVER been used for a confirmatory broad-universe cross-sectional study. Once
# this campaign starts (start UTC below), a post-start session cannot satisfy the
# gate with a trigger-only, prose-only, source-probe-only, audit-only, prereg-
# only, verify-and-stop, or arbitrary recompute_* session. It must emit the
# outcome-blind source registry + prereg, the HEAVY broad-universe evaluation
# triad, the independent stdlib recompute, the evidence audit, the gate-critical
# evidence_audit_ alias, and a non-empty trigger check. Sessions predating the
# campaign start are grandfathered so this handoff refresh stays green.
LIQ_XSEC_BROAD_CAMPAIGN_RE = re.compile(
    r"FCLR-LIQ-XSEC-BROAD-(\d+)-(\d{8}T\d{6}Z)"
)
LIQ_XSEC_BROAD_REQUIRED = (
    ("fclr_liqxsecbroad01_source_registry_", ".json"),
    ("fclr_liqxsecbroad01_source_registry_", ".md"),
    ("fclr_liqxsecbroad01_prereg_", ".json"),
    ("fclr_liqxsecbroad01_prereg_", ".md"),
    ("fclr_liqxsecbroad01_eval_", ".py"),
    ("fclr_liqxsecbroad01_eval_", ".json"),
    ("fclr_liqxsecbroad01_eval_", ".md"),
    ("fclr_liqxsecbroad01_recompute_", ".py"),
    ("fclr_liqxsecbroad01_recompute_", ".json"),
    ("fclr_liqxsecbroad01_evidence_audit_", ".json"),
    ("fclr_liqxsecbroad01_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-POOLED-001 hardening: the *only* thing that ever blocked heavy work was
# the broken "3 contiguous 30-day funding-backed blocks" framing that
# next_campaign_status.py enforces across every cached domain. That framing is
# FALSE as a statement about the data on disk: research_state/data_cache/
# ironflow_bulk/ already holds 18 months (2025-05 .. 2026-10) of aligned
# candles_1h + funding + open_interest + liquidations across 342 coins
# (3.6M/4.1M/4.0M/2.8M rows). A pooled, chronologically-split out-of-sample
# design is feasible TODAY without any new source. The prior handoff declared
# "no remaining rank-0 campaign" and told future agents to stop — a
# verify-and-stop escape hatch. This campaign removes that bottleneck: once it
# starts (start UTC below), a post-start session cannot satisfy the gate with a
# trigger-only, prose-only, source-probe-only, audit-only, verify-and-stop, or
# arbitrary recompute_* session. It must emit the full pooled heavy artifact set
# on the ironflow bulk data. Sessions predating the campaign start are
# grandfathered so this handoff refresh stays green.
POOLED_CAMPAIGN_RE = re.compile(r"FCLR-POOLED-(\d+)-(\d{8}T\d{6}Z)")
POOLED_REQUIRED = (
    ("fclr_pooled_source_registry_", ".json"),
    ("fclr_pooled_source_registry_", ".md"),
    ("fclr_pooled_prereg_", ".json"),
    ("fclr_pooled_prereg_", ".md"),
    ("fclr_pooled_eval_", ".py"),
    ("fclr_pooled_eval_", ".json"),
    ("fclr_pooled_eval_", ".md"),
    ("fclr_pooled_recompute_", ".py"),
    ("fclr_pooled_recompute_", ".json"),
    ("fclr_pooled_evidence_audit_", ".json"),
    ("fclr_pooled_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-POOLED-AUDIT-001 hardening: FCLR-POOLED-001 returned NOT_SUPPORTED, so
# the next focus is the RESEARCH_PROMPT.md §10 priority-8 adversarial audit of
# the pooled ironflow panel: timestamping, delisting/identity, missingness,
# survivorship, stress concentration, threshold drift, and overlapping outcomes.
# Once this campaign starts (start UTC 20261122T110000Z), a post-start session
# cannot satisfy the gate with a trigger-only, prose-only, source-probe-only,
# generic-audit-only, or verify-and-stop session. It must emit the outcome-blind
# audit prereg, the heavy adversarial-audit implementation/result/report triad,
# the independent stdlib recompute, the audit evidence package, the gate-critical
# evidence_audit_ alias, and a non-empty trigger check. Sessions predating the
# campaign start (including the completed pooled session) are grandfathered.
POOLED_AUDIT_CAMPAIGN_RE = re.compile(r"FCLR-POOLED-AUDIT-(\d+)-(\d{8}T\d{6}Z)")
POOLED_AUDIT_REQUIRED = (
    ("fclr_pooled_audit_prereg_", ".json"),
    ("fclr_pooled_audit_prereg_", ".md"),
    ("fclr_pooled_audit_audit_", ".py"),
    ("fclr_pooled_audit_audit_", ".json"),
    ("fclr_pooled_audit_audit_", ".md"),
    ("fclr_pooled_audit_recompute_", ".py"),
    ("fclr_pooled_audit_recompute_", ".json"),
    ("fclr_pooled_audit_evidence_audit_", ".json"),
    ("fclr_pooled_audit_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

# FCLR-POOLED-ROBUST-002 hardening: FCLR-POOLED-AUDIT-001 (the §10 priority-8
# adversarial audit) found concrete quality gaps that could have manufactured OR
# masked the FCLR-POOLED-001 NOT_SUPPORTED null: d2 only a 1-hour train/test gap
# (no 48h purge+embargo), d10 overlapping forward outcomes (pairwise Jaccard
# 0.52..0.92 dependence), d4 6.8% of rows above the 1% mark/index tolerance,
# d6/d7 delisting/survivorship, d9 threshold drift. The prior handoff told future
# agents to "verify green and stop" — an inefficient escape hatch that would let
# the null stand without ever testing whether it survives a leakage-hardened
# design. This campaign removes that bottleneck: a heavy, pre-registered,
# leakage-hardened RE-CONFIRMATION on the same on-disk ironflow bulk panel that
# applies ALL audit remediations simultaneously (48h purge+embargo, non-overlapping
# forward-outcome windows, mark/index tolerance filter, delisting-aware identity,
# per-coin block-bootstrap, Holm across the declared family) and reports it as a
# sequential confirmatory look k=2 with alpha-spending. Once this campaign starts
# (start UTC below), a post-start session cannot satisfy the gate with a trigger-
# only, prose-only, source-probe-only, audit-only, verify-and-stop, or arbitrary
# recompute_* session. It must emit the outcome-blind robustness prereg, the heavy
# robustness recompute triad, the independent stdlib recompute, the evidence audit,
# the gate-critical evidence_audit_ alias, and a non-empty trigger check. Sessions
# predating the campaign start are grandfathered so this handoff refresh stays green.
POOLED_ROBUST_CAMPAIGN_RE = re.compile(r"FCLR-POOLED-ROBUST-(\d+)-(\d{8}T\d{6}Z)")
POOLED_ROBUST_REQUIRED = (
    ("fclr_pooled_robust_prereg_", ".json"),
    ("fclr_pooled_robust_prereg_", ".md"),
    ("fclr_pooled_robust_robustness_", ".py"),
    ("fclr_pooled_robust_robustness_", ".json"),
    ("fclr_pooled_robust_robustness_", ".md"),
    ("fclr_pooled_robust_recompute_", ".py"),
    ("fclr_pooled_robust_recompute_", ".json"),
    ("fclr_pooled_robust_evidence_audit_", ".json"),
    ("fclr_pooled_robust_evidence_audit_", ".md"),
    ("evidence_audit_", ".json"),
    ("trigger_check_", ".json"),
)

NEW_QUANT_PREFIXES = (
    "fclr_risk",
    "fclr_starter",
    "fclr_xsec007_",        # FCLR-XSEC-007 cross-panel reconciliation quantitative artifacts
    "fclr_xsec008_",        # FCLR-XSEC-008 alternative regime conditioning quantitative artifacts
    "independent_recompute_",
    "trigger_readiness_power_calibration_",
    "trigger_readiness_power_ledger_",
    "power_ledger_refresh_",
    "reproducibility_recompute_",
    "recompute_",
    "trigger_activation_",
    "fclr_session_synth",   # FCLR-SESSION-SYNTHESIS consolidation + quantitative meta-analysis artifacts
    "fclr_panelfe",         # FCLR-PANEL-FE panel fixed-effects funding-conditioning evaluation artifacts
    "fclr_liq_contagion",   # FCLR-LIQ-CONTAGION cross-coin liquidation contagion + funding spillover artifacts
    "fclr_liq_contagion02", # FCLR-LIQ-CONTAGION-002 robustness-reconciliation artifacts (edge-set + materiality)
    "fclr_live_archive",    # FCLR-LIVE-ARCHIVE reachable free-archive source + heavy 3-block design artifacts
    "fclr_next_source_verify", # FCLR-NEXT-SOURCE-VERIFY-01 materially-different free source + heavy 3-block design artifacts
    "fclr_pooled",          # FCLR-POOLED pooled chronological OOS funding-conditioned vol + liq-risk artifacts
    "fclr_pooled_audit",    # FCLR-POOLED-AUDIT pooled ironflow adversarial leakage/quality audit artifacts
    "fclr_tracks",          # FCLR-TRACKA-SOURCE-AUDIT observed-liquidation source viability audit + pivot artifacts
    "fclr_liqxsecbroad",    # FCLR-LIQ-XSEC-BROAD broad-universe cross-sectional liquidation-risk generalization artifacts
    "fclr_volbroad",        # FCLR-VOL-BROAD broad-panel funding-conditioned volatility forecast artifacts
)
AUDIT_PREFIX = "evidence_audit_"


def _root_count(rs: Path) -> int:
    return len(list(rs.glob("*.md"))) + len(list(rs.glob("*.json")))


def _handoff_session_ids(handoff: Path) -> list[str]:
    if not handoff.exists():
        return []
    text = handoff.read_text(encoding="utf-8", errors="ignore")
    return sorted(set(_SESSION_DIR_RE.findall(text)))


def _latest_handoff_session(handoff: Path) -> str | None:
    """Return the lexicographically latest session_<UTC> id in the handoff."""
    ids = _handoff_session_ids(handoff)
    return ids[-1] if ids else None


def _latest_disk_session(rs: Path) -> str | None:
    """Return the lexicographically latest session_<UTC> directory on disk.

    FCLR-TRIGGER-READINESS-01 non-avoidance: the gate previously trusted the
    handoff's latest session id, so a session could create a post-campaign
    directory, skip the mandatory package, and leave the handoff pointing at an
    older session. The gate would stay green forever. Comparing the newest
    on-disk session against the newest handoff-recorded session closes that
    stale-handoff bypass: a newer session must be recorded (and then checked).
    """
    ids = []
    for p in rs.iterdir() if rs.is_dir() else []:
        m = _SESSION_DIR_RE.fullmatch(p.name)
        if m and p.is_dir():
            ids.append(m.group(1))
    return max(ids) if ids else None


def _session_has_required(session_dir: Path) -> dict:
    files = [p.name for p in session_dir.glob("*") if p.is_file()]
    missing = []
    for prefix in PHASE_B_PREFIXES:
        if not any(f.startswith(prefix) for f in files):
            missing.append(prefix + "*")
    for prefix in PHASE_C_PREFIXES:
        if not any(f.startswith(prefix) for f in files):
            missing.append(prefix + "*")
    return {"files": sorted(files), "missing": missing}


def _frontier_verify_state(handoff_text: str, latest_sid: str | None,
                           latest_files: list[str]) -> dict:
    """Return FCLR-FRONTIER-VERIFY-06 non-avoidance state for the latest session.

    The campaign id carries its start UTC. Sessions lexicographically after that
    start must contain the exact exhaustive-audit triad and a trigger check; an
    arbitrary recompute_* file is not enough. Sessions from before the campaign
    existed are grandfathered so this gate remains green during the handoff
    refresh that first announces the campaign.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = FRONTIER_VERIFY_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-FRONTIER-VERIFY-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    # Session ids are session_<UTC>; compare only the UTC portion.
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True
    required = [f"{FRONTIER_VERIFY_ARTIFACT_PREFIX}<UTC>{suffix}"
                for suffix in FRONTIER_VERIFY_REQUIRED_SUFFIXES]
    out["required_artifacts"] = required
    out["missing_required_artifacts"] = [
        artifact for artifact, suffix in zip(required, FRONTIER_VERIFY_REQUIRED_SUFFIXES)
        if not any(f.startswith(FRONTIER_VERIFY_ARTIFACT_PREFIX) and f.endswith(suffix)
                   for f in latest_files)
    ]
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") for f in latest_files
    )
    out["pass"] = not out["missing_required_artifacts"] and out["has_trigger_check"]
    return out


def _trigger_readiness_state(handoff_text: str, latest_sid: str | None,
                             latest_files: list[str]) -> dict:
    """Return FCLR-TRIGGER-READINESS-01 non-avoidance state for the latest session.

    After the trigger-readiness campaign starts, a post-start session must emit
    the outcome-blind trigger-activation package (executor + self-test + readiness
    certificate) plus a trigger check; an arbitrary recompute_* artifact is not
    enough. Sessions predating the campaign are grandfathered so this gate stays
    green during the handoff refresh that first announces the campaign.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = TRIGGER_READINESS_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-TRIGGER-READINESS-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in TRIGGER_READINESS_REQUIRED]
    out["required_artifacts"] = required
    out["missing_required_artifacts"] = [
        label
        for label, (prefix, suffix) in zip(required, TRIGGER_READINESS_REQUIRED)
        if not any(f.startswith(prefix) and f.endswith(suffix) for f in latest_files)
    ]
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") for f in latest_files
    )
    out["pass"] = not out["missing_required_artifacts"] and out["has_trigger_check"]
    return out


def _ledger_integrity_state(handoff_text: str, latest_sid: str | None,
                            latest_files: list[str]) -> dict:
    """Return FCLR-LEDGER-INTEGRITY-02 non-avoidance state for the latest session.

    After the ledger-integrity campaign starts, a post-start session must emit
    the outcome-blind ledger audit + frontier recompute + trigger check + refreshed
    trigger-activation readiness; an arbitrary recompute_* artifact or a
    trigger-check-only session is not enough. Sessions predating the campaign are
    grandfathered so the gate stays green during the handoff refresh that first
    announces the campaign.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = LEDGER_INTEGRITY_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LEDGER-INTEGRITY-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in LEDGER_INTEGRITY_REQUIRED]
    out["required_artifacts"] = required
    out["missing_required_artifacts"] = [
        label
        for label, (prefix, suffix) in zip(required, LEDGER_INTEGRITY_REQUIRED)
        if not any(f.startswith(prefix) and f.endswith(suffix) for f in latest_files)
    ]
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") for f in latest_files
    )
    out["pass"] = not out["missing_required_artifacts"] and out["has_trigger_check"]
    return out


def _closure_ledger_state(handoff_text: str, latest_sid: str | None,
                          latest_files: list[str]) -> dict:
    """Return FCLR-CLOSURE-LEDGER-COMPLETENESS-01 non-avoidance state.

    After the campaign starts, a post-start session must emit the non-authoritative
    closure-ledger sidecar + completeness validator (py + json) + a trigger check.
    Sessions predating the campaign are grandfathered.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = CLOSURE_LEDGER_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-CLOSURE-LEDGER-COMPLETENESS-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in CLOSURE_LEDGER_REQUIRED]
    out["required_artifacts"] = required
    out["missing_required_artifacts"] = [
        label
        for label, (prefix, suffix) in zip(required, CLOSURE_LEDGER_REQUIRED)
        if not any(f.startswith(prefix) and f.endswith(suffix) for f in latest_files)
    ]
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") for f in latest_files
    )
    out["pass"] = not out["missing_required_artifacts"] and out["has_trigger_check"]
    return out


def _vol_liq_execution_state(handoff_text: str, latest_sid: str | None,
                             latest_files: list[str],
                             latest_dir: Path | None = None) -> dict:
    """Return FCLR-VOL-LIQ-EXECUTION-01 non-avoidance state.

    After the execution campaign starts, a post-start session must contain the
    exact Track C forecast and Track B breach-label package, a trigger check,
    and non-empty files. Empty placeholders do not count as heavy work.
    Sessions predating the campaign are grandfathered.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = VOL_LIQ_EXECUTION_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-VOL-LIQ-EXECUTION-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files
            if f.startswith(prefix) and f.endswith(suffix)
        )

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in VOL_LIQ_EXECUTION_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, VOL_LIQ_EXECUTION_REQUIRED):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _breach_forecast_state(handoff_text: str, latest_sid: str | None,
                           latest_files: list[str],
                           latest_dir: Path | None = None) -> dict:
    """Return FCLR-VOL-LIQ-BREACH-FORECAST-03 non-avoidance state.

    After the breach-forecast campaign starts, a post-start session must contain
    the outcome-blind breach-forecast prereg and forecast triad plus a trigger
    check, with no zero-byte placeholders. Sessions predating the campaign are
    grandfathered so the handoff refresh that first announces the campaign stays
    green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = BREACH_FORECAST_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-VOL-LIQ-BREACH-FORECAST-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files
            if f.startswith(prefix) and f.endswith(suffix)
        )

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in BREACH_FORECAST_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, BREACH_FORECAST_REQUIRED):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _robust_04_state(handoff_text: str, latest_sid: str | None,
                     latest_files: list[str],
                     latest_dir: Path | None = None) -> dict:
    """Return FCLR-VOL-LIQ-ROBUST-04 non-avoidance state.

    After the robust-04 campaign starts (start UTC 120000Z), a post-start session
    must emit the outcome-blind robust-04 prereg, the robustness recompute triad,
    and a trigger check, with no zero-byte placeholders. Sessions predating the
    campaign start are grandfathered so the handoff refresh stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = ROBUST_04_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(1)
    out["campaign_id"] = f"FCLR-VOL-LIQ-ROBUST-04-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files
            if f.startswith(prefix) and f.endswith(suffix)
        )

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in ROBUST_04_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, ROBUST_04_REQUIRED):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _robust_05_state(handoff_text: str, latest_sid: str | None,
                     latest_files: list[str],
                     latest_dir: Path | None = None) -> dict:
    """Return FCLR-VOL-LIQ-ROBUST-05 non-avoidance state.

    After the robust-05 campaign starts (start UTC 20261118T132800Z), a post-start
    session must emit the outcome-blind robust-05 prereg, the robustness recompute
    triad, and a trigger check, with no zero-byte placeholders. Sessions predating
    the campaign start are grandfathered so the handoff refresh stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = ROBUST_05_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(1)
    out["campaign_id"] = f"FCLR-VOL-LIQ-ROBUST-05-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files
            if f.startswith(prefix) and f.endswith(suffix)
        )

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in ROBUST_05_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, ROBUST_05_REQUIRED):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _risk_06_state(handoff_text: str, latest_sid: str | None,
                   latest_files: list[str],
                   latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-RISK-CALIBRATION-06 non-avoidance state.

    After the risk-06 campaign starts, a post-start session must emit the
    outcome-blind prereg, the multi-month modeled breach-label triad, the
    out-of-sample calibration triad (Brier/log-loss), and a trigger check, with
    no zero-byte placeholders. Sessions predating the campaign start are
    grandfathered.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = RISK_06_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LIQ-RISK-CALIBRATION-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files
            if f.startswith(prefix) and f.endswith(suffix)
        )

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in RISK_06_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, RISK_06_REQUIRED):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _risk_07_state(handoff_text: str, latest_sid: str | None,
                   latest_files: list[str],
                   latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-RISK-RECALIBRATION-07 non-avoidance state.

    After the risk-07 campaign starts, a post-start session must emit the
    outcome-blind prereg, the stdlib calibrator implementation (Platt logistic,
    PAVA isotonic, scenario base-rate offset), the recalibration evaluation triad
    (Brier + ECE + cross-scenario transfer), a trigger check, and no zero-byte
    placeholders. Sessions predating the campaign start are grandfathered.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = RISK_07_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LIQ-RISK-RECALIBRATION-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in RISK_07_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, RISK_07_REQUIRED):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _tracka_confirmatory_state(handoff_text: str, latest_sid: str | None,
                               latest_files: list[str],
                               latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-TRACKA-CONFIRMATORY-01 non-avoidance state.

    After the confirmatory campaign starts, a post-start session must emit the
    power/MDE audit triad, the independent stdlib recompute, the confirmatory
    evaluation triad, and a trigger check. Descriptive-only, trigger-only, or
    arbitrary recompute_* sessions fail closed. Sessions predating the campaign
    start are grandfathered so the handoff refresh that announces the campaign
    remains green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = TRACKA_CONFIRMATORY_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LIQ-TRACKA-CONFIRMATORY-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in TRACKA_CONFIRMATORY_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, TRACKA_CONFIRMATORY_REQUIRED):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _risk_08_state(handoff_text: str, latest_sid: str | None,
                   latest_files: list[str],
                   latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-RISK-ESCALATION-08 non-avoidance state.

    After the escalation campaign starts, a post-start session must emit the
    outcome-blind prereg, the power/MDE audit triad, the independent stdlib
    recompute, the evaluation triad, and a trigger check. Descriptive-only,
    trigger-only, or arbitrary recompute_* sessions fail closed. Sessions that
    predate the campaign start are grandfathered so the handoff refresh that
    announces the campaign remains green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = RISK_08_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LIQ-RISK-ESCALATION-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    # Ladder-aware: bind the artifact family to the campaign number in the
    # handoff (08 -> fclr_risk08_*, 09 -> fclr_risk09_*, ...). This keeps the
    # gate enforcing heavy work after RISK-08 closes instead of deadlocking a
    # RISK-09 session on impossible fclr_risk08_* filenames.
    tag = f"risk{int(m.group(1)):02d}"
    family = tuple(
        (prefix.replace("fclr_risk08_", f"fclr_{tag}_"), suffix)
        for prefix, suffix in RISK_08_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _session_synthesis_state(handoff_text: str, latest_sid: str | None,
                           latest_files: list[str],
                           latest_dir: Path | None = None) -> dict:
    """Return FCLR-SESSION-SYNTHESIS-01 non-avoidance state.

    After the consolidation + quantitative meta-analysis campaign starts, a
    post-start session must emit the outcome-blind protocol freeze, the program
    synthesis report, the frontier exhaustion audit, the negative-results
    preservation, the quantitative meta-analysis triad, the independent stdlib
    recompute, and a trigger check, with no zero-byte placeholders. A
    trigger-only, prose-only, audit-only, or arbitrary recompute_* session fails
    closed. Sessions predating the campaign start are grandfathered so the
    handoff refresh that first announces the campaign remains green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = SESSION_SYNTHESIS_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-SESSION-SYNTHESIS-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    # Ladder-aware: bind the artifact family to the campaign number in the
    # handoff (01 -> fclr_session_synth01_*, 02 -> fclr_session_synth02_*, ...).
    # This keeps the gate enforcing heavy work after SYNTHESIS-01 closes instead
    # of deadlocking a SYNTHESIS-02 session on impossible fclr_session_synth01_*
    # filenames.
    tag = f"synth{int(m.group(1)):02d}"
    family = tuple(
        (prefix.replace("fclr_session_synth01_", f"fclr_session_{tag}_"), suffix)
        for prefix, suffix in SESSION_SYNTHESIS_REQUIRED
        if prefix.startswith("fclr_session_synth01_")
    )
    # Non-synth-prefixed required artifacts (evidence_audit_, trigger_check_) are
    # appended unchanged.
    family += tuple(
        (prefix, suffix) for prefix, suffix in SESSION_SYNTHESIS_REQUIRED
        if not prefix.startswith("fclr_session_synth01_")
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _program_closure_state(handoff_text: str, latest_sid: str | None,
                           latest_files: list[str],
                           latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-RISK-PROGRAM-CLOSURE-01 non-avoidance state.

    After the formal program-closure campaign starts, a post-start session must
    emit the complete eight-category closure artifact set under one fresh
    session_<UTC>/ with no zero-byte placeholders: outcome-blind closure protocol
    freeze (json+md), negative-results synthesis report (json+md), frontier
    exhaustion audit (json+md), negative-results preservation (json+md),
    quantitative meta-analysis triad (py+json+md), independent stdlib recompute
    (py+json), gate-critical evidence_audit alias (json+md), and a non-empty
    trigger check. A trigger-only, prose-only, audit-only, verify-and-stop, or
    arbitrary recompute_* session fails closed. Sessions predating the campaign
    start are grandfathered so the handoff refresh that first announces the
    campaign remains green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "has_evidence_audit_alias": False,
        "pass": True,
    }
    m = PROGRAM_CLOSURE_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = (
        f"FCLR-LIQ-RISK-PROGRAM-CLOSURE-{m.group(1)}-{campaign_start}"
    )
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in PROGRAM_CLOSURE_REQUIRED]
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, PROGRAM_CLOSURE_REQUIRED):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["has_evidence_audit_alias"] = any(
        f.startswith("evidence_audit_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
        and out["has_evidence_audit_alias"]
    )
    return out


def _vol_broad_state(handoff_text: str, latest_sid: str | None,
                     latest_files: list[str],
                     latest_dir: Path | None = None) -> dict:
    """Return FCLR-VOL-BROAD-01 non-avoidance state.

    The repository name leads with "Funding-conditioned-volatility", but the
    leakage-robust volatility nulls (FCLR-011, FCLR-PANEL-FE-001) were all on a
    5-coin panel. The broad 342-coin ironflow_bulk panel has never been used for
    a direct funding-conditioned realized-volatility forecast. After this
    campaign starts, a post-start session must emit the on-disk source registry,
    the outcome-blind prereg freeze, the heavy broad-panel walk-forward
    evaluation triad (py+json+md), the independent stdlib recompute (py+json),
    the evidence audit (json+md), the gate-critical evidence_audit_ alias (json),
    and a non-empty trigger check. Trigger-only, prose-only, audit-only,
    prereg-only, verify-and-stop, arbitrary recompute_* sessions, zero-byte
    placeholders, and unreadable or non-conforming JSON fail closed. Sessions
    predating the campaign start are grandfathered so the handoff refresh that
    first announces the campaign stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "content_failures": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = VOL_BROAD_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_num = int(m.group(1))
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-VOL-BROAD-{campaign_num:02d}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _path(name: str) -> Path | None:
        if not latest_dir or not latest_dir.exists():
            return None
        p = latest_dir / name
        return p if p.is_file() else None

    def _nonempty(name: str) -> bool:
        p = _path(name)
        return bool(p and p.stat().st_size > 0)

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )

    def _json(prefix: str) -> tuple[dict | None, str | None]:
        hits = _matches(prefix, ".json")
        for name in hits:
            p = _path(name)
            if not p:
                continue
            try:
                value = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                continue
            if isinstance(value, dict):
                return value, name
        return None, None

    def _number(value: object) -> bool:
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )

    def _sha256(name: str | None) -> str | None:
        p = _path(name) if name else None
        if not p:
            return None
        return hashlib.sha256(p.read_bytes()).hexdigest()

    tag = f"volbroad{campaign_num:02d}"
    campaign_id = f"FCLR-VOL-BROAD-{campaign_num:02d}"
    family = tuple(
        (prefix.replace("fclr_volbroad01_", f"fclr_{tag}_"), suffix)
        for prefix, suffix in VOL_BROAD_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    matches: dict[tuple[str, str], list[str]] = {}
    for label, (prefix, suffix) in zip(required, family):
        hits = _matches(prefix, suffix)
        matches[(prefix, suffix)] = hits
        if not hits:
            out["missing_required_artifacts"].append(label)
        elif not any(_nonempty(name) for name in hits):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )

    source_prefix = f"fclr_{tag}_source_registry_"
    prereg_prefix = f"fclr_{tag}_prereg_"
    eval_prefix = f"fclr_{tag}_eval_"
    recompute_prefix = f"fclr_{tag}_recompute_"
    audit_prefix = f"fclr_{tag}_evidence_audit_"
    alias_prefix = "evidence_audit_"
    trigger_prefix = "trigger_check_"

    source, source_name = _json(source_prefix)
    prereg, _ = _json(prereg_prefix)
    evaluation, _ = _json(eval_prefix)
    recompute, _ = _json(recompute_prefix)
    evidence, _ = _json(audit_prefix)
    alias, _ = _json(alias_prefix)
    trigger, _ = _json(trigger_prefix)

    # All machine-readable artifacts must belong to this campaign and session.
    for label, data in (
        ("SOURCE", source),
        ("PREREG", prereg),
        ("EVAL", evaluation),
        ("RECOMPUTE", recompute),
        ("EVIDENCE", evidence),
        ("EVIDENCE_ALIAS", alias),
        ("TRIGGER", trigger),
    ):
        if data is None:
            out["content_failures"].append(f"{label}_JSON_INVALID")
            continue
        if data.get("experiment_id") != campaign_id:
            out["content_failures"].append(f"{label}_EXPERIMENT_ID")
        session_matches = data.get("session_id") == latest_sid or (
            data.get("session_utc") == latest_utc
        )
        if not session_matches:
            out["content_failures"].append(f"{label}_SESSION_ID")

    # Registry: prove that all three frozen datasets and their sidecars were
    # inventoried before outcomes were computed.
    if source is not None:
        datasets = source.get("datasets")
        if not isinstance(datasets, dict) or not {
            "candles_1h", "funding", "open_interest"
        }.issubset(datasets):
            out["content_failures"].append("SOURCE_DATASETS")
        integrity = source.get("input_integrity")
        if not isinstance(integrity, dict):
            out["content_failures"].append("SOURCE_INTEGRITY")
        else:
            if integrity.get("sha256_all_match") is not True:
                out["content_failures"].append("SOURCE_HASH_ASSERTION")
            if integrity.get("sha256_verified_bad") != 0:
                out["content_failures"].append("SOURCE_BAD_HASHES")
        files = source.get("files", source.get("input_sha256"))
        if not isinstance(files, (list, dict)) or len(files) < 54:
            out["content_failures"].append("SOURCE_FILE_COUNT")
        elif isinstance(files, list):
            valid_hashes = all(
                isinstance(entry, dict)
                and isinstance(entry.get("sha256"), str)
                and re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])
                and entry.get("sha_match") is not False
                for entry in files
            )
            if not valid_hashes:
                out["content_failures"].append("SOURCE_FILE_HASHES")

    # Prereg: freeze the outcome-blind design and bind it to the registry.
    if prereg is not None:
        if prereg.get("frozen_before_outcomes") is not True and prereg.get(
            "decision_frozen_before_outcomes"
        ) is not True:
            out["content_failures"].append("PREREG_NOT_FROZEN")
        if prereg.get("outcome_data_inspected_before_freeze") is not False:
            out["content_failures"].append("PREREG_OUTCOME_INSPECTION_FLAG")
        design = prereg.get("design")
        if not isinstance(design, dict) or "walk_forward" not in str(
            design.get("kind", "")
        ):
            out["content_failures"].append("PREREG_WALK_FORWARD")
        train_frac = prereg.get(
            "train_frac", design.get("train_frac") if isinstance(design, dict) else None
        )
        if not _number(train_frac) or not 0 < train_frac < 1:
            out["content_failures"].append("PREREG_TRAIN_FRAC")
        purge = prereg.get(
            "purge_embargo_h",
            design.get("purge_embargo_h") if isinstance(design, dict) else None,
        )
        if not isinstance(purge, int) or purge < 1:
            out["content_failures"].append("PREREG_PURGE")
        floor = prereg.get("materiality_floor_rel_qlike")
        if not _number(floor) or floor <= 0:
            out["content_failures"].append("PREREG_MATERIALITY")
        hash_assertions = prereg.get("input_hash_assertions")
        registry_sha = prereg.get("source_registry_sha256")
        if registry_sha is None and isinstance(hash_assertions, dict):
            registry_sha = hash_assertions.get("source_registry_sha256")
        if registry_sha != _sha256(source_name):
            out["content_failures"].append("PREREG_SOURCE_HASH")

    # Evaluation: require a completed walk-forward run with real QLIKE/MSE
    # metrics for both the baseline and funding-conditioned candidate.
    if evaluation is not None:
        if evaluation.get("status") not in {
            "CONFIRMATORY_COMPLETE", "NOT_SUPPORTED", "PROMOTED", "INCONCLUSIVE"
        }:
            out["content_failures"].append("EVAL_STATUS")
        if evaluation.get("holdout_opened") is not True:
            out["content_failures"].append("EVAL_HOLDOUT_NOT_OPENED")
        forecasts = evaluation.get("n_forecasts")
        if not isinstance(forecasts, int) or forecasts < 1:
            out["content_failures"].append("EVAL_FORECAST_COUNT")
        blocks = evaluation.get("n_test_blocks")
        if not isinstance(blocks, int) or blocks < 1:
            out["content_failures"].append("EVAL_BLOCK_COUNT")
        metrics = evaluation.get("metrics")
        if not isinstance(metrics, dict) or not {"baseline", "candidate"}.issubset(metrics):
            out["content_failures"].append("EVAL_METRICS_MODELS")
        else:
            for model in ("baseline", "candidate"):
                entry = metrics.get(model)
                if not isinstance(entry, dict):
                    out["content_failures"].append(f"EVAL_{model.upper()}_METRICS")
                    continue
                for metric in ("qlike", "mse"):
                    value = entry.get(metric)
                    if not _number(value) or value < 0:
                        out["content_failures"].append(
                            f"EVAL_{model.upper()}_{metric.upper()}"
                        )
        if not isinstance(evaluation.get("materiality_met"), bool):
            out["content_failures"].append("EVAL_MATERIALITY_FLAG")
        verdict = str(evaluation.get("verdict", "")).upper()
        if verdict not in {"PROMOTED", "NOT_SUPPORTED", "INCONCLUSIVE"}:
            out["content_failures"].append("EVAL_VERDICT")
        elif verdict == "PROMOTED" and evaluation.get("materiality_met") is not True:
            out["content_failures"].append("EVAL_PROMOTION_WITHOUT_MATERIALITY")

    # Recompute: the independent result must explicitly match the canonical run.
    if recompute is not None:
        if recompute.get("all_checks_match") is not True:
            out["content_failures"].append("RECOMPUTE_NOT_MATCHED")
        if recompute.get("n_checks") is None:
            out["content_failures"].append("RECOMPUTE_CHECK_COUNT")

    # Audit: require an explicit verdict and no unresolved blockers.
    if evidence is not None:
        if evidence.get("audit_pass") is not True:
            out["content_failures"].append("EVIDENCE_AUDIT_NOT_PASSING")
        if evidence.get("unresolved_blockers") != []:
            out["content_failures"].append("EVIDENCE_AUDIT_BLOCKERS")
        if evidence.get("verdict") != (evaluation or {}).get("verdict"):
            out["content_failures"].append("EVIDENCE_EVAL_VERDICT_MISMATCH")

    # Gate-critical alias must be a substantive audit, not a duplicate stub.
    if alias is not None and evidence is not None:
        if alias.get("verdict") != evidence.get("verdict"):
            out["content_failures"].append("EVIDENCE_ALIAS_VERDICT_MISMATCH")
        if alias.get("audit_pass") is not True:
            out["content_failures"].append("EVIDENCE_ALIAS_NOT_PASSING")

    # Trigger: no external liquidation trigger is needed or can fire here.
    if trigger is not None:
        if trigger.get("external_trigger_required") is not False:
            out["content_failures"].append("TRIGGER_EXTERNAL_FLAG")
        if trigger.get("trigger_source") != "FROZEN_IRONFLOW_BULK":
            out["content_failures"].append("TRIGGER_SOURCE")
        if trigger.get("fired") is not False:
            out["content_failures"].append("TRIGGER_UNEXPECTED_FIRE")

    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and not out["content_failures"]
        and out["has_trigger_check"]
    )
    return out


def _panel_fe_state(handoff_text: str, latest_sid: str | None,
                    latest_files: list[str],
                    latest_dir: Path | None = None) -> dict:
    """Return FCLR-PANEL-FE-001 non-avoidance state.

    After the panel fixed-effects funding-conditioning campaign starts, a
    post-start session must emit the outcome-blind prereg freeze, the panel-FE
    evaluation triad (py+json+md), the independent stdlib recompute (py+json),
    the evidence audit (json+md), and a trigger check. Trigger-only, prose-only,
    audit-only, or arbitrary recompute_* sessions fail closed. Sessions that
    predate the campaign start are grandfathered so the handoff refresh that
    announces the campaign remains green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = PANEL_FE_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-PANEL-FE-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    # Ladder-aware: bind the artifact family to the campaign number in the
    # handoff (01 -> fclr_panelfe01_*, 02 -> fclr_panelfe02_*, ...). This keeps
    # the gate enforcing heavy work after PANEL-FE-01 closes instead of
    # deadlocking a PANEL-FE-02 session on impossible fclr_panelfe01_* names.
    tag = f"panelfe{int(m.group(1)):02d}"
    family = tuple(
        (prefix.replace("fclr_panelfe01_", f"fclr_{tag}_"), suffix)
        for prefix, suffix in PANEL_FE_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _contagion_state(handoff_text: str, latest_sid: str | None,
                     latest_files: list[str],
                     latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-CONTAGION-01 non-avoidance state.

    After the cross-coin liquidation-contagion campaign starts, a post-start
    session must emit the outcome-blind prereg freeze, the contagion evaluation
    triad (py+json+md), the independent stdlib recompute (py+json), the contagion
    evidence audit (json+md), the gate-critical evidence_audit_ alias (json), and
    a trigger check. Trigger-only, prose-only, audit-only, or arbitrary
    recompute_* sessions fail closed. Sessions that predate the campaign start
    are grandfathered so the handoff refresh that announces the campaign stays
    green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    all_matches = CONTAGION_CAMPAIGN_RE.findall(handoff_text or "")
    if not all_matches:
        return out
    # Bind only the highest-numbered CONTAGION campaign referenced in the
    # handoff; lower-numbered (completed) campaigns in the history table must
    # not bind their artifact family onto a later session. This keeps the gate
    # enforcing the *active* campaign instead of an already-closed one.
    max_num = max(int(num) for num, _ in all_matches)
    if max_num != 1:
        # A higher-numbered CONTAGION campaign (e.g. 002) supersedes this one;
        # its dedicated state function binds the heavy work.
        return out
    campaign_start = next(start for num, start in all_matches if int(num) == 1)
    out["campaign_id"] = f"FCLR-LIQ-CONTAGION-01-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    # Ladder-aware: bind the artifact family to the campaign number (always 01
    # here, since this branch only runs when 001 is the highest CONTAGION
    # campaign referenced in the handoff).
    tag = "contagion01"
    family = tuple(
        (prefix.replace("fclr_liq_contagion01_", f"fclr_liq_{tag}_"), suffix)
        for prefix, suffix in CONTAGION_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _contagion_002_state(handoff_text: str, latest_sid: str | None,
                         latest_files: list[str],
                         latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-CONTAGION-002 robustness-reconciliation state.

    FCLR-LIQ-CONTAGION-001 left a disclosed, unresolved methodological
    discrepancy (eval 11 edges vs recompute 58 edges; declared 2% per-edge
    materiality never computed). After this campaign starts, a post-start
    session must emit the outcome-blind prereg freeze, the heavy reconciliation
    evaluation triad (py+json+md), the independent stdlib recompute (py+json),
    the contagion evidence audit (json+md), the gate-critical evidence_audit_
    alias (json), and a trigger check, with no zero-byte placeholders.
    Trigger-only, prose-only, audit-only, verify-and-stop, or arbitrary
    recompute_* sessions fail closed. Sessions that predate the campaign start
    (incl. session_20261121T193000Z, the CONTAGION-001 session) are grandfathered
    so the handoff refresh that announces the campaign stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    all_matches = CONTAGION_002_CAMPAIGN_RE.findall(handoff_text or "")
    if not all_matches:
        return out
    # Bind only the highest-numbered CONTAGION campaign referenced in the
    # handoff; lower-numbered (completed) campaigns in the history table must
    # not bind their artifact family onto a later session. This keeps the gate
    # enforcing the *active* campaign instead of an already-closed one.
    campaign_num = max(int(num) for num, _ in all_matches)
    campaign_start = next(start for num, start in all_matches if int(num) == campaign_num)
    out["campaign_id"] = f"FCLR-LIQ-CONTAGION-{campaign_num:02d}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    # Only bind the reconciliation artifacts when the highest CONTAGION campaign
    # is the 002 robustness campaign (or a later ladder step). A handoff whose
    # highest campaign is 001 leaves required=False and defers to _contagion_state.
    out["required"] = campaign_num >= 2

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    # Ladder-aware: bind the artifact family to the campaign number in the
    # handoff (02 -> fclr_liq_contagion02_*, 03 -> fclr_liq_contagion03_*, ...).
    tag = f"contagion{campaign_num:02d}"
    family = tuple(
        (prefix.replace("fclr_liq_contagion02_", f"fclr_liq_{tag}_"), suffix)
        for prefix, suffix in CONTAGION_002_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _live_archive_state(handoff_text: str, latest_sid: str | None,
                        latest_files: list[str],
                        latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIVE-ARCHIVE non-avoidance state.

    After the live-archive campaign starts, a post-start session must emit the
    outcome-blind source registry + verified-download evidence, the outcome-blind
    prereg freeze, the heavy 3-block confirmatory evaluation triad (py+json+md) on
    the newly downloaded archive data, the independent stdlib recompute (py+json),
    the evidence audit (json+md), the gate-critical evidence_audit_ alias (json),
    and a trigger check, with no zero-byte placeholders. Trigger-only,
    prose-only, source-probe-only, audit-only, and verify-and-stop sessions fail
    closed. Sessions that predate the campaign start are grandfathered so the
    handoff refresh that announces the campaign stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = LIVE_ARCHIVE_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LIVE-ARCHIVE-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    # Ladder-aware: bind the artifact family to the campaign number in the
    # handoff (01 -> fclr_live_archive01_*, 02 -> fclr_live_archive02_*, ...).
    # The base LIVE_ARCHIVE_REQUIRED prefixes are numberless
    # (fclr_live_archive_source_registry_, ...), so the ladder must inject the
    # campaign number after the ``fclr_live_archive`` stem. The previous code
    # replaced ``fclr_live_archive01_`` (which never matched the numberless
    # base), so a FCLR-LIVE-ARCHIVE-02 session that correctly wrote
    # ``fclr_live_archive02_*`` files deadlocked forever against an impossible
    # ``fclr_live_archive_*`` demand. The shared non-campaign prefixes
    # (evidence_audit_, trigger_check_) are left untouched.
    tag = f"live_archive{int(m.group(1)):02d}"
    family = tuple(
        (prefix.replace("fclr_live_archive_", f"fclr_{tag}_", 1), suffix)
        if prefix.startswith("fclr_live_archive_")
        else (prefix, suffix)
        for prefix, suffix in LIVE_ARCHIVE_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _next_source_verify_state(handoff_text: str, latest_sid: str | None,
                              latest_files: list[str],
                              latest_dir: Path | None = None) -> dict:
    """Return FCLR-NEXT-SOURCE-VERIFY-01 non-avoidance state.

    After the materially-different free-source campaign starts (start UTC
    20261122T013100Z), a post-start session cannot satisfy the gate with an
    arbitrary recompute_* artifact, a trigger-check-only session, a
    source-probe-only session, or a verify-and-stop session. It must emit the
    full FCLR-NEXT-SOURCE-VERIFY-01 artifact set. Sessions predating the
    campaign start are grandfathered so this handoff refresh stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = NEXT_SOURCE_VERIFY_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-NEXT-SOURCE-VERIFY-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    tag = f"next_source_verify{int(m.group(1)):02d}"
    family = tuple(
        (prefix.replace("fclr_next_source_verify_", f"fclr_{tag}_", 1), suffix)
        if prefix.startswith("fclr_next_source_verify_")
        else (prefix, suffix)
        for prefix, suffix in NEXT_SOURCE_VERIFY_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, NEXT_SOURCE_VERIFY_REQUIRED):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _tracks01_state(handoff_text: str, latest_sid: str | None,
                    latest_files: list[str],
                    latest_dir: Path | None = None) -> dict:
    """Return FCLR-TRACKA-SOURCE-AUDIT-01 non-avoidance state.

    After the Track A source viability audit campaign starts, a post-start
    session must emit the source registry + probe triad, the outcome-blind
    viability decision, the pivot prereg, the HEAVY evaluation triad
    (fclr_tracks01_eval_ py+json+md), the independent stdlib recompute
    (fclr_tracks01_recompute_ py+json), the evidence audit, the gate-critical
    evidence_audit_ alias, and a trigger check. Trigger-only, prose-only,
    source-probe-only, audit-only, prereg-only, verify-and-stop sessions and
    zero-byte placeholders fail closed: the heavy quantitative evaluation runs
    in the SAME session and cannot be deferred. Sessions predating the campaign
    start are grandfathered so the handoff refresh that announces the campaign
    stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = TRACKA_SOURCE_AUDIT_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-TRACKA-SOURCE-AUDIT-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )

    # Ladder-aware: bind the artifact family to the campaign number in the
    # handoff (01 -> fclr_tracks01_*, 02 -> fclr_tracks02_*, ...).
    tag = f"tracks{int(m.group(1)):02d}"
    family = tuple(
        (prefix.replace("fclr_tracks01_", f"fclr_{tag}_"), suffix)
        if prefix.startswith("fclr_tracks01_")
        else (prefix, suffix)
        for prefix, suffix in TRACKA_SOURCE_AUDIT_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _liq_xsec_broad_state(handoff_text: str, latest_sid: str | None,
                         latest_files: list[str],
                         latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-XSEC-BROAD-01 non-avoidance state.

    After the broad-universe cross-sectional liquidation-risk generalization
    campaign starts, a post-start session must emit the on-disk source registry,
    the outcome-blind prereg, the HEAVY evaluation triad
    (fclr_liqxsecbroad01_eval_ py+json+md), the independent stdlib recompute
    (fclr_liqxsecbroad01_recompute_ py+json), the evidence audit, the gate-
    critical evidence_audit_ alias, and a trigger check. Trigger-only, prose-only,
    source-probe-only, audit-only, prereg-only, verify-and-stop sessions and
    zero-byte placeholders fail closed. Sessions predating the campaign start are
    grandfathered so the handoff refresh that announces the campaign stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = LIQ_XSEC_BROAD_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LIQ-XSEC-BROAD-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in LIQ_XSEC_BROAD_REQUIRED]
    out["artifact_family"] = "liqxsecbroad01"
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, LIQ_XSEC_BROAD_REQUIRED):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _broad_ts_state(handoff_text: str, latest_sid: str | None,
                    latest_files: list[str],
                    latest_dir: Path | None = None) -> dict:
    """Return FCLR-LIQ-XSEC-BROAD-TS-01 non-avoidance state.

    After the temporal-stability campaign starts, a post-start session cannot
    satisfy the gate with a trigger-only, prose-only, audit-only, prereg-only,
    verify-and-stop, or arbitrary recompute_* session. It must emit the
    outcome-blind temporal-stability prereg, the heavy rolling-window evaluation
    triad, the independent stdlib recompute, the evidence audit, the gate-critical
    evidence_audit_ alias, and a trigger check, with no zero-byte placeholders.
    Sessions predating the campaign start are grandfathered so this handoff
    refresh stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = BROAD_TS_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-LIQ-XSEC-BROAD-TS-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    def _matches(prefix: str, suffix: str) -> list[str]:
        return sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )

    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in BROAD_TS_REQUIRED]
    out["artifact_family"] = "liqxsecbroad01_ts"
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, BROAD_TS_REQUIRED):
        matches = _matches(prefix, suffix)
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _pooled_state(handoff_text: str, latest_sid: str | None,
                  latest_files: list[str],
                  latest_dir: Path | None = None) -> dict:
    """Return FCLR-POOLED-001 non-avoidance state.

    The pooled chronological OOS campaign breaks the broken "3 contiguous
    30-day funding-backed blocks" deadlock by running a heavy pooled design on
    the on-disk ironflow bulk data (18 months, 342 coins, 3.6M candles). After
    this campaign starts, a post-start session cannot satisfy the gate with a
    trigger-only, prose-only, source-probe-only, audit-only, verify-and-stop, or
    arbitrary recompute_* session. It must emit the full FCLR-POOLED artifact
    set. Sessions predating the campaign start are grandfathered so this
    handoff refresh stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = POOLED_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-POOLED-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    tag = f"pooled{int(m.group(1)):03d}"
    family = tuple(
        (prefix.replace("fclr_pooled_", f"fclr_{tag}_", 1), suffix)
        if prefix.startswith("fclr_pooled_")
        else (prefix, suffix)
        for prefix, suffix in POOLED_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    # Match against the transformed per-campaign family (e.g. fclr_pooled001_*),
    # NOT the untransformed POOLED_REQUIRED prefixes. The frontier and the
    # tag/family machinery both mandate the fclr_pooled001_* naming; zipping the
    # loop against POOLED_REQUIRED made a correct heavy session fail the gate
    # because its files (fclr_pooled001_*) did not start with fclr_pooled_*.
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _pooled_audit_state(handoff_text: str, latest_sid: str | None,
                        latest_files: list[str],
                        latest_dir: Path | None = None) -> dict:
    """Return FCLR-POOLED-AUDIT non-avoidance state.

    FCLR-POOLED-001 is complete with an honest NOT_SUPPORTED verdict. The next
    heavy campaign is an adversarial leakage/quality audit of that pooled panel,
    not another prose-only status update. After it starts, a post-start session
    must emit the outcome-blind audit prereg, the audit implementation/result/
    report triad, the independent stdlib recompute, the audit evidence package,
    the gate-critical evidence_audit_ alias, and a trigger check. Zero-byte and
    generic recompute/audit placeholders fail closed. Pre-start sessions are
    grandfathered so this handoff refresh remains green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = POOLED_AUDIT_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-POOLED-AUDIT-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    tag = f"pooled_audit{int(m.group(1)):03d}"
    family = tuple(
        (prefix.replace("fclr_pooled_audit_", f"fclr_{tag}_", 1), suffix)
        if prefix.startswith("fclr_pooled_audit_")
        else (prefix, suffix)
        for prefix, suffix in POOLED_AUDIT_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _pooled_robust_state(handoff_text: str, latest_sid: str | None,
                         latest_files: list[str],
                         latest_dir: Path | None = None) -> dict:
    """Return FCLR-POOLED-ROBUST non-avoidance state.

    FCLR-POOLED-AUDIT-001 left concrete, disclosed quality gaps (d2 no 48h
    purge+embargo; d10 overlapping outcomes; d4 mark/index tolerance; d6/d7
    delisting/survivorship; d9 threshold drift). The next heavy campaign is a
    leakage-hardened re-confirmation on the same on-disk ironflow bulk panel, not
    another verify-and-stop status update. After it starts, a post-start session
    must emit the outcome-blind robustness prereg, the heavy robustness recompute
    triad, the independent stdlib recompute, the evidence audit, the gate-critical
    evidence_audit_ alias, and a trigger check. Zero-byte and generic
    recompute/audit placeholders fail closed. Pre-start sessions are grandfathered
    so this handoff refresh remains green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "artifact_family": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = POOLED_ROBUST_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-POOLED-ROBUST-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    tag = f"pooled_robust{int(m.group(1)):03d}"
    family = tuple(
        (prefix.replace("fclr_pooled_robust_", f"fclr_{tag}_", 1), suffix)
        if prefix.startswith("fclr_pooled_robust_")
        else (prefix, suffix)
        for prefix, suffix in POOLED_ROBUST_REQUIRED
    )
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in family]
    out["artifact_family"] = tag
    out["required_artifacts"] = required
    for label, (prefix, suffix) in zip(required, family):
        matches = sorted(
            f for f in latest_files if f.startswith(prefix) and f.endswith(suffix)
        )
        if not matches:
            out["missing_required_artifacts"].append(label)
            continue
        if not any(_nonempty(name) for name in matches):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )
    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and out["has_trigger_check"]
    )
    return out


def _normalize_text(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.replace("\r\n", "\n").split("\n")).strip()


def section14_body(repo: Path) -> str | None:
    """Return the normalized RESEARCH_PROMPT.md §14 body, or None.

    The body includes the §14 heading and everything up to (excluding) §15.
    """
    prompt = repo / "RESEARCH_PROMPT.md"
    if not prompt.exists():
        return None
    text = prompt.read_text(encoding="utf-8", errors="ignore")
    start = text.find(STARTER_SECTION_HEADING)
    if start < 0:
        return None
    end = text.find("\n## 15.", start)
    if end < 0:
        end = len(text)
    return _normalize_text(text[start:end])


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _load_json_lenient(p: Path) -> dict | None:
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _starter_001_state(handoff_text: str, latest_sid: str | None,
                       latest_files: list[str], latest_dir: Path | None,
                       repo: Path = REPO) -> dict:
    """Return FCLR-STARTER-001 non-avoidance state for the latest session.

    After the campaign starts, a post-start session must emit the §14 protocol
    freeze (hash-bound to the current RESEARCH_PROMPT.md §14 text), the panel
    hash freeze (recorded before target generation), and the B0/B1 baseline
    triad, plus a trigger check. The freeze validators are structural: a
    placeholder JSON with the right filename fails closed. Sessions predating
    the campaign are grandfathered so this handoff refresh stays green.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "empty_required_artifacts": [],
        "has_trigger_check": False,
        "content_failures": [],
        "section14_sha256": None,
        "pass": True,
    }
    m = STARTER_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-STARTER-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in STARTER_REQUIRED]
    out["required_artifacts"] = required

    def _nonempty(name: str) -> bool:
        if not latest_dir or not latest_dir.exists():
            return False
        p = latest_dir / name
        return p.is_file() and p.stat().st_size > 0

    matches: dict[tuple[str, str], list[str]] = {}
    for label, (prefix, suffix) in zip(required, STARTER_REQUIRED):
        hits = sorted(f for f in latest_files if f.startswith(prefix) and f.endswith(suffix))
        matches[(prefix, suffix)] = hits
        if not hits:
            out["missing_required_artifacts"].append(label)
        elif not any(_nonempty(name) for name in hits):
            out["empty_required_artifacts"].append(label)
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") and _nonempty(f)
        for f in latest_files
    )

    section_body = section14_body(repo)
    if section_body is None:
        out["content_failures"].append("SECTION_14_HEADING_NOT_FOUND")
    else:
        out["section14_sha256"] = _sha256_text(section_body)

    def _any_json(prefix: str) -> dict | None:
        for name in matches.get((prefix, ".json"), []):
            data = _load_json_lenient(latest_dir / name) if latest_dir else None
            if data is not None:
                return data
        return None

    # --- protocol freeze validator -------------------------------------
    pf = _any_json(STARTER_PROTOCOL_PREFIX)
    if pf is None:
        if not out["missing_required_artifacts"] and not out["empty_required_artifacts"]:
            out["content_failures"].append("PROTOCOL_FREEZE_JSON_UNREADABLE")
    else:
        if not str(pf.get("experiment_id", "")).startswith("FCLR-STARTER-001"):
            out["content_failures"].append("PROTOCOL_FREEZE_EXPERIMENT_ID")
        if pf.get("outcome_data_inspected_before_freeze") is not False:
            out["content_failures"].append("PROTOCOL_FREEZE_OUTCOME_FLAG")
        ppath = str(pf.get("protocol_path", "")).strip()
        if not ppath:
            out["content_failures"].append("PROTOCOL_FREEZE_PATH_MISSING")
        else:
            if _normalize_text(ppath) == STARTER_SEALED_PROTOCOL:
                out["content_failures"].append("PROTOCOL_FREEZE_OVERWRITES_SEALED")
            target = repo / ppath
            if not target.is_file() or target.stat().st_size == 0:
                out["content_failures"].append("PROTOCOL_FREEZE_FILE_MISSING")
            elif section_body is not None:
                ptext = _normalize_text(
                    target.read_text(encoding="utf-8", errors="ignore")
                )
                if section_body not in ptext:
                    out["content_failures"].append("PROTOCOL_FREEZE_SECTION14_MISMATCH")
                if str(pf.get("section14_sha256", "")) != _sha256_text(section_body):
                    out["content_failures"].append("PROTOCOL_FREEZE_SECTION14_HASH")
                if str(pf.get("protocol_sha256", "")) != hashlib.sha256(
                    target.read_bytes()
                ).hexdigest():
                    out["content_failures"].append("PROTOCOL_FREEZE_FILE_HASH")

    # --- panel freeze validator ----------------------------------------
    pn = _any_json(STARTER_PANEL_PREFIX)
    if pn is None:
        if not out["missing_required_artifacts"] and not out["empty_required_artifacts"]:
            out["content_failures"].append("PANEL_FREEZE_JSON_UNREADABLE")
    else:
        if not str(pn.get("experiment_id", "")).startswith("FCLR-STARTER-001"):
            out["content_failures"].append("PANEL_FREEZE_EXPERIMENT_ID")
        sha = str(pn.get("panel_sha256", ""))
        if not re.fullmatch(r"[0-9a-f]{64}", sha):
            out["content_failures"].append("PANEL_FREEZE_SHA256")
        src = pn.get("source_hashes")
        if not isinstance(src, dict) or not src:
            out["content_failures"].append("PANEL_FREEZE_SOURCE_HASHES")
        if pn.get("panel_frozen_before_target_generation") is not True:
            out["content_failures"].append("PANEL_FREEZE_ORDER")
        if not str(pn.get("eligible_definition", "")).strip():
            out["content_failures"].append("PANEL_FREEZE_ELIGIBLE_DEFINITION")
        if not (pn.get("cutoff_utc") or pn.get("split_boundaries")):
            out["content_failures"].append("PANEL_FREEZE_CUTOFF")

    # --- B0/B1 baseline validator --------------------------------------
    bl = _any_json(STARTER_BASELINES_PREFIX)
    if bl is None:
        if not out["missing_required_artifacts"] and not out["empty_required_artifacts"]:
            out["content_failures"].append("BASELINES_JSON_UNREADABLE")
    else:
        if not str(bl.get("experiment_id", "")).startswith("FCLR-STARTER-001"):
            out["content_failures"].append("BASELINES_EXPERIMENT_ID")
        models = bl.get("models")
        if not isinstance(models, dict) or not {"B0", "B1"}.issubset(models):
            out["content_failures"].append("BASELINES_B0_B1_MISSING")
        else:
            for key in ("B0", "B1"):
                entry = models.get(key)
                if not isinstance(entry, dict):
                    out["content_failures"].append(f"BASELINES_{key}_NOT_OBJECT")
                    continue
                q = entry.get("qlike")
                if not isinstance(q, (int, float)) or q < 0:
                    out["content_failures"].append(f"BASELINES_{key}_QLIKE")
        if bl.get("holdout_opened") is not False:
            out["content_failures"].append("BASELINES_HOLDOUT_FLAG")
        split = str(bl.get("split_used", "")).lower()
        if not ("dev" in split or "valid" in split):
            out["content_failures"].append("BASELINES_SPLIT")
        n = bl.get("n_obs", bl.get("n_rows"))
        if not isinstance(n, int) or n <= 0:
            out["content_failures"].append("BASELINES_N_OBS")

    out["pass"] = (
        not out["missing_required_artifacts"]
        and not out["empty_required_artifacts"]
        and not out["content_failures"]
        and out["has_trigger_check"]
    )
    return out


def _session_has_new_heavy(session_dir: Path) -> dict:
    """Return whether a session has the new-style evidence audit + fresh quant."""
    files = [p.name for p in session_dir.glob("*") if p.is_file()]
    audit_files = [f for f in files if f.startswith(AUDIT_PREFIX)]
    quant_files = sorted(
        f for f in files if any(f.startswith(prefix) for prefix in NEW_QUANT_PREFIXES)
    )
    return {
        "files": sorted(files),
        "has_audit": bool(audit_files),
        "audit_files": audit_files,
        "has_new_quant": bool(quant_files),
        "new_quant_files": quant_files,
    }


def check(repo: Path = REPO) -> dict:
    rs = repo / "research_state"
    handoff = repo / "AGENT_HANDOFF.md"
    payload = {
        "script": "check_handoff_heavywork_gate",
        "network": False,
        "writes_real_research_state": False,
        "read_only": True,
        "pass": False,
        "failures": [],
        "handoff_exists": False,
        "handoff_markers_ok": False,
        "handoff_session_ids": [],
        "latest_session_id": None,
        "latest_disk_session_id": None,
        "handoff_stale": False,
        "latest_session_dir": None,
        "latest_session_evidence": None,
        "heavy_session_id": None,
        "heavy_session_dir": None,
        "heavy_session_exists": False,
        "heavy_session_missing": [],
        "heavy_session_mode": None,
        "root_count": 0,
        "root_count_cap": ROOT_COUNT_CAP,
        "frontier_verify": None,
        "trigger_readiness": None,
        "ledger_integrity": None,
        "closure_ledger": None,
        "vol_liq_execution": None,
        "breach_forecast": None,
        "robust_04": None,
        "robust_05": None,
        "risk_06": None,
        "risk_07": None,
        "tracka_confirmatory": None,
        "risk_08": None,
        "starter_001": None,
        "session_synthesis": None,
        "panel_fe": None,
        "contagion": None,
        "contagion_002": None,
        "live_archive": None,
        "next_source_verify": None,
        "pooled": None,
        "pooled_audit": None,
        "pooled_robust_02": None,
        "tracks01": None,
        "liq_xsec_broad": None,
        "broad_ts_01": None,
        "program_closure": None,
        "vol_broad": None,
    }

    # (1) Handoff exists and carries the required markers.
    if not handoff.exists():
        payload["failures"].append("HANDOFF_MISSING")
    else:
        payload["handoff_exists"] = True
        text = handoff.read_text(encoding="utf-8", errors="ignore")
        missing_markers = [m for m in HANDOFF_REQUIRED_MARKERS if m not in text]
        if missing_markers:
            payload["failures"].append(f"HANDOFF_MARKERS_MISSING:{missing_markers}")
        else:
            payload["handoff_markers_ok"] = True

    # (2) The latest session must have done new heavy work.  A complete
    # carried-forward Phase-B/C bundle still satisfies the check; a new-style
    # session may instead carry a complete bundle forward and add an evidence
    # audit plus a fresh quantitative artifact.
    ids = _handoff_session_ids(handoff)
    latest_sid = ids[-1] if ids else None
    payload["handoff_session_ids"] = ids
    payload["latest_session_id"] = latest_sid
    latest_disk_sid = _latest_disk_session(rs)
    payload["latest_disk_session_id"] = latest_disk_sid
    if latest_sid and latest_disk_sid and latest_disk_sid > latest_sid:
        payload["handoff_stale"] = True
        payload["failures"].append(
            f"HANDOFF_STALE_LATEST_SESSION:{latest_disk_sid}"
        )
    if not latest_sid:
        payload["failures"].append("HEAVY_SESSION_ID_UNRECORDED")
    else:
        latest_sdir = rs / latest_sid
        payload["latest_session_dir"] = (
            str(latest_sdir.relative_to(repo)) if latest_sdir.exists() else None
        )
        latest_info = {"files": [], "missing": []}
        if not latest_sdir.exists():
            payload["failures"].append(f"HEAVY_SESSION_DIR_MISSING:{latest_sid}")
            latest_info["missing"] = [
                prefix + "*" for prefix in PHASE_B_PREFIXES + PHASE_C_PREFIXES
            ]
        else:
            latest_info = _session_has_required(latest_sdir)
            latest_new = _session_has_new_heavy(latest_sdir)
            payload["latest_session_evidence"] = latest_new
            latest_complete = not latest_info["missing"]
            latest_new_ok = latest_new["has_audit"] and latest_new["has_new_quant"]
            if not (latest_complete or latest_new_ok):
                payload["failures"].append(
                    f"HEAVY_SESSION_ARTIFACTS_MISSING:{latest_sid}:{latest_info['missing']}"
                )

            # FCLR-FRONTIER-VERIFY-06: after the campaign starts, require the
            # exact exhaustive-audit triad plus a trigger check, not any quant.
            fv = _frontier_verify_state(text, latest_sid, latest_info["files"])
            payload["frontier_verify"] = fv
            if fv["required"]:
                if fv["missing_required_artifacts"]:
                    payload["failures"].append(
                        "FRONTIER_VERIFY_ARTIFACTS_MISSING:"
                        + ",".join(fv["missing_required_artifacts"])
                    )
                if not fv["has_trigger_check"]:
                    payload["failures"].append(
                        f"FRONTIER_VERIFY_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-TRIGGER-READINESS-01: after the campaign starts, require the
            # outcome-blind trigger-activation package plus a trigger check, not
            # any quant artifact.
            tr = _trigger_readiness_state(text, latest_sid, latest_info["files"])
            payload["trigger_readiness"] = tr
            if tr["required"]:
                if tr["missing_required_artifacts"]:
                    payload["failures"].append(
                        "TRIGGER_READINESS_ARTIFACTS_MISSING:"
                        + ",".join(tr["missing_required_artifacts"])
                    )
                if not tr["has_trigger_check"]:
                    payload["failures"].append(
                        f"TRIGGER_READINESS_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LEDGER-INTEGRITY-02: after the campaign starts, require the
            # outcome-blind ledger audit + frontier recompute + trigger check +
            # refreshed trigger-activation readiness, not any quant artifact.
            li = _ledger_integrity_state(text, latest_sid, latest_info["files"])
            payload["ledger_integrity"] = li
            if li["required"]:
                if li["missing_required_artifacts"]:
                    payload["failures"].append(
                        "LEDGER_INTEGRITY_ARTIFACTS_MISSING:"
                        + ",".join(li["missing_required_artifacts"])
                    )
                if not li["has_trigger_check"]:
                    payload["failures"].append(
                        f"LEDGER_INTEGRITY_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-CLOSURE-LEDGER-COMPLETENESS-01: after the campaign starts,
            # require the closure-ledger sidecar + validator + trigger check.
            cl = _closure_ledger_state(text, latest_sid, latest_info["files"])
            payload["closure_ledger"] = cl
            if cl["required"]:
                if cl["missing_required_artifacts"]:
                    payload["failures"].append(
                        "CLOSURE_LEDGER_ARTIFACTS_MISSING:"
                        + ",".join(cl["missing_required_artifacts"])
                    )
                if not cl["has_trigger_check"]:
                    payload["failures"].append(
                        f"CLOSURE_LEDGER_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-VOL-LIQ-EXECUTION-01: after the execution campaign starts,
            # require the exact Track C forecast + Track B breach-label package
            # and a trigger check. Zero-byte placeholders fail closed.
            vl = _vol_liq_execution_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["vol_liq_execution"] = vl
            if vl["required"]:
                if vl["missing_required_artifacts"]:
                    payload["failures"].append(
                        "VOL_LIQ_EXECUTION_ARTIFACTS_MISSING:"
                        + ",".join(vl["missing_required_artifacts"])
                    )
                if vl["empty_required_artifacts"]:
                    payload["failures"].append(
                        "VOL_LIQ_EXECUTION_ARTIFACTS_EMPTY:"
                        + ",".join(vl["empty_required_artifacts"])
                    )
                if not vl["has_trigger_check"]:
                    payload["failures"].append(
                        f"VOL_LIQ_EXECUTION_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-VOL-LIQ-BREACH-FORECAST-03: after the breach-forecast campaign
            # starts, require the outcome-blind prereg + forecast triad + trigger
            # check. Zero-byte placeholders fail closed.
            bf = _breach_forecast_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["breach_forecast"] = bf
            if bf["required"]:
                if bf["missing_required_artifacts"]:
                    payload["failures"].append(
                        "BREACH_FORECAST_ARTIFACTS_MISSING:"
                        + ",".join(bf["missing_required_artifacts"])
                    )
                if bf["empty_required_artifacts"]:
                    payload["failures"].append(
                        "BREACH_FORECAST_ARTIFACTS_EMPTY:"
                        + ",".join(bf["empty_required_artifacts"])
                    )
                if not bf["has_trigger_check"]:
                    payload["failures"].append(
                        f"BREACH_FORECAST_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-VOL-LIQ-ROBUST-04: after the robust-04 campaign starts,
            # require the outcome-blind prereg + robustness triad + trigger check.
            # Zero-byte placeholders fail closed.
            r04 = _robust_04_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["robust_04"] = r04
            if r04["required"]:
                if r04["missing_required_artifacts"]:
                    payload["failures"].append(
                        "ROBUST_04_ARTIFACTS_MISSING:"
                        + ",".join(r04["missing_required_artifacts"])
                    )
                if r04["empty_required_artifacts"]:
                    payload["failures"].append(
                        "ROBUST_04_ARTIFACTS_EMPTY:"
                        + ",".join(r04["empty_required_artifacts"])
                    )
                if not r04["has_trigger_check"]:
                    payload["failures"].append(
                        f"ROBUST_04_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-VOL-LIQ-ROBUST-05: after the robust-05 campaign starts,
            # require the outcome-blind prereg + robustness triad + trigger check.
            # Zero-byte placeholders fail closed.
            r05 = _robust_05_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["robust_05"] = r05
            if r05["required"]:
                if r05["missing_required_artifacts"]:
                    payload["failures"].append(
                        "ROBUST_05_ARTIFACTS_MISSING:"
                        + ",".join(r05["missing_required_artifacts"])
                    )
                if r05["empty_required_artifacts"]:
                    payload["failures"].append(
                        "ROBUST_05_ARTIFACTS_EMPTY:"
                        + ",".join(r05["empty_required_artifacts"])
                    )
                if not r05["has_trigger_check"]:
                    payload["failures"].append(
                        f"ROBUST_05_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-RISK-CALIBRATION-06: after the risk-06 campaign starts,
            # require the outcome-blind prereg + multi-month labels triad +
            # calibration triad + trigger check. Zero-byte placeholders fail closed.
            r06 = _risk_06_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["risk_06"] = r06
            if r06["required"]:
                if r06["missing_required_artifacts"]:
                    payload["failures"].append(
                        "RISK_06_ARTIFACTS_MISSING:"
                        + ",".join(r06["missing_required_artifacts"])
                    )
                if r06["empty_required_artifacts"]:
                    payload["failures"].append(
                        "RISK_06_ARTIFACTS_EMPTY:"
                        + ",".join(r06["empty_required_artifacts"])
                    )
                if not r06["has_trigger_check"]:
                    payload["failures"].append(
                        f"RISK_06_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-RISK-RECALIBRATION-07: after the risk-07 campaign starts,
            # require the outcome-blind prereg + stdlib calibrator implementation +
            # recalibration evaluation triad + trigger check. Zero-byte placeholders
            # fail closed, so a future session cannot dodge the heavy calibration
            # work with an audit-only or gate-only session.
            r07 = _risk_07_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["risk_07"] = r07
            if r07["required"]:
                if r07["missing_required_artifacts"]:
                    payload["failures"].append(
                        "RISK_07_ARTIFACTS_MISSING:"
                        + ",".join(r07["missing_required_artifacts"])
                    )
                if r07["empty_required_artifacts"]:
                    payload["failures"].append(
                        "RISK_07_ARTIFACTS_EMPTY:"
                        + ",".join(r07["empty_required_artifacts"])
                    )
                if not r07["has_trigger_check"]:
                    payload["failures"].append(
                        f"RISK_07_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-TRACKA-CONFIRMATORY-01: after the confirmatory campaign
            # starts, require the power/MDE audit, independent stdlib recompute,
            # confirmatory evaluation triad, and trigger check. A descriptive-only
            # or trigger-only session fails closed.
            tc = _tracka_confirmatory_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["tracka_confirmatory"] = tc
            if tc["required"]:
                if tc["missing_required_artifacts"]:
                    payload["failures"].append(
                        "TRACKA_CONFIRMATORY_ARTIFACTS_MISSING:"
                        + ",".join(tc["missing_required_artifacts"])
                    )
                if tc["empty_required_artifacts"]:
                    payload["failures"].append(
                        "TRACKA_CONFIRMATORY_ARTIFACTS_EMPTY:"
                        + ",".join(tc["empty_required_artifacts"])
                    )
                if not tc["has_trigger_check"]:
                    payload["failures"].append(
                        f"TRACKA_CONFIRMATORY_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-RISK-ESCALATION-08: after the escalation campaign starts,
            # require the outcome-blind prereg + power/MDE triad + independent
            # recompute + evaluation triad + trigger check. A descriptive-only,
            # trigger-only, or arbitrary recompute_* session fails closed.
            r08 = _risk_08_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["risk_08"] = r08
            if r08["required"]:
                if r08["missing_required_artifacts"]:
                    payload["failures"].append(
                        "RISK_08_ARTIFACTS_MISSING:"
                        + ",".join(r08["missing_required_artifacts"])
                    )
                if r08["empty_required_artifacts"]:
                    payload["failures"].append(
                        "RISK_08_ARTIFACTS_EMPTY:"
                        + ",".join(r08["empty_required_artifacts"])
                    )
                if not r08["has_trigger_check"]:
                    payload["failures"].append(
                        f"RISK_08_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-STARTER-001: after the §14 starter campaign starts, require the
            # hash-bound protocol freeze, panel hash freeze, B0/B1 baseline triad
            # and trigger check. Placeholders and free-text claims fail closed; the
            # sealed legacy research_protocol.md may never be overwritten.
            st = _starter_001_state(
                text, latest_sid, latest_info["files"], latest_sdir, repo
            )
            payload["starter_001"] = st
            if st["required"]:
                if st["missing_required_artifacts"]:
                    payload["failures"].append(
                        "STARTER_001_ARTIFACTS_MISSING:"
                        + ",".join(st["missing_required_artifacts"])
                    )
                if st["empty_required_artifacts"]:
                    payload["failures"].append(
                        "STARTER_001_ARTIFACTS_EMPTY:"
                        + ",".join(st["empty_required_artifacts"])
                    )
                if st["content_failures"]:
                    payload["failures"].append(
                        "STARTER_001_CONTENT_INVALID:"
                        + ",".join(st["content_failures"])
                    )
                if not st["has_trigger_check"]:
                    payload["failures"].append(
                        f"STARTER_001_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-SESSION-SYNTHESIS-01: after the consolidation + quantitative
            # meta-analysis campaign starts, require the outcome-blind protocol
            # freeze + program synthesis report + frontier exhaustion audit +
            # negative-results preservation + meta-analysis triad + independent
            # recompute + trigger check. Zero-byte placeholders fail closed.
            ss = _session_synthesis_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["session_synthesis"] = ss
            if ss["required"]:
                if ss["missing_required_artifacts"]:
                    payload["failures"].append(
                        "SESSION_SYNTHESIS_ARTIFACTS_MISSING:"
                        + ",".join(ss["missing_required_artifacts"])
                    )
                if ss["empty_required_artifacts"]:
                    payload["failures"].append(
                        "SESSION_SYNTHESIS_ARTIFACTS_EMPTY:"
                        + ",".join(ss["empty_required_artifacts"])
                    )
                if not ss["has_trigger_check"]:
                    payload["failures"].append(
                        f"SESSION_SYNTHESIS_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-PANEL-FE-001: after the panel fixed-effects campaign starts,
            # require the outcome-blind prereg freeze + panel-FE evaluation triad +
            # independent stdlib recompute + evidence audit + trigger check.
            # Zero-byte placeholders fail closed, so a future session cannot dodge
            # the heavy panel study with a trigger-only or audit-only session.
            pfe = _panel_fe_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["panel_fe"] = pfe
            if pfe["required"]:
                if pfe["missing_required_artifacts"]:
                    payload["failures"].append(
                        "PANEL_FE_ARTIFACTS_MISSING:"
                        + ",".join(pfe["missing_required_artifacts"])
                    )
                if pfe["empty_required_artifacts"]:
                    payload["failures"].append(
                        "PANEL_FE_ARTIFACTS_EMPTY:"
                        + ",".join(pfe["empty_required_artifacts"])
                    )
                if not pfe["has_trigger_check"]:
                    payload["failures"].append(
                        f"PANEL_FE_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-CONTAGION-001: after the cross-coin liquidation-contagion
            # campaign starts, require the outcome-blind prereg + contagion
            # evaluation triad + independent stdlib recompute + evidence audit +
            # gate-critical evidence_audit_ alias + trigger check. Zero-byte
            # placeholders fail closed, so a future session cannot dodge the heavy
            # contagion/network analysis with a trigger-only or audit-only session.
            ct = _contagion_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["contagion"] = ct
            if ct["required"]:
                if ct["missing_required_artifacts"]:
                    payload["failures"].append(
                        "CONTAGION_ARTIFACTS_MISSING:"
                        + ",".join(ct["missing_required_artifacts"])
                    )
                if ct["empty_required_artifacts"]:
                    payload["failures"].append(
                        "CONTAGION_ARTIFACTS_EMPTY:"
                        + ",".join(ct["empty_required_artifacts"])
                    )
                if not ct["has_trigger_check"]:
                    payload["failures"].append(
                        f"CONTAGION_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-CONTAGION-002: after the robustness-reconciliation
            # campaign starts, require the outcome-blind prereg + reconciliation
            # evaluation triad + independent stdlib recompute + evidence audit +
            # gate-critical evidence_audit_ alias + trigger check. Zero-byte
            # placeholders fail closed, so a future session cannot dodge the heavy
            # edge-set robustness + per-edge materiality reconciliation with a
            # trigger-only, audit-only, or verify-and-stop session.
            ct2 = _contagion_002_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["contagion_002"] = ct2
            if ct2["required"]:
                if ct2["missing_required_artifacts"]:
                    payload["failures"].append(
                        "CONTAGION_002_ARTIFACTS_MISSING:"
                        + ",".join(ct2["missing_required_artifacts"])
                    )
                if ct2["empty_required_artifacts"]:
                    payload["failures"].append(
                        "CONTAGION_002_ARTIFACTS_EMPTY:"
                        + ",".join(ct2["empty_required_artifacts"])
                    )
                if not ct2["has_trigger_check"]:
                    payload["failures"].append(
                        f"CONTAGION_002_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIVE-ARCHIVE: after the reachable free-archive campaign starts,
            # require the source registry + verified-download evidence, the
            # outcome-blind prereg freeze, the heavy 3-block confirmatory
            # evaluation triad (py+json+md) on the newly downloaded archive data,
            # the independent stdlib recompute (py+json), the evidence audit
            # (json+md), the gate-critical evidence_audit_ alias (json), and a
            # trigger check. Zero-byte placeholders fail closed, so a future
            # session cannot dodge the heavy archive research with a trigger-only,
            # prose-only, source-probe-only, audit-only, or verify-and-stop session.
            la = _live_archive_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["live_archive"] = la
            if la["required"]:
                if la["missing_required_artifacts"]:
                    payload["failures"].append(
                        "LIVE_ARCHIVE_ARTIFACTS_MISSING:"
                        + ",".join(la["missing_required_artifacts"])
                    )
                if la["empty_required_artifacts"]:
                    payload["failures"].append(
                        "LIVE_ARCHIVE_ARTIFACTS_EMPTY:"
                        + ",".join(la["empty_required_artifacts"])
                    )
                if not la["has_trigger_check"]:
                    payload["failures"].append(
                        f"LIVE_ARCHIVE_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-NEXT-SOURCE-VERIFY-01: after the materially-different free
            # source campaign starts, require the source registry +
            # verified-download evidence, outcome-blind prereg freeze, heavy
            # 3-block confirmatory evaluation triad, independent stdlib
            # recompute, evidence audit, gate-critical evidence_audit_ alias,
            # and trigger check. Zero-byte placeholders fail closed.
            nsv = _next_source_verify_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["next_source_verify"] = nsv
            if nsv["required"]:
                if nsv["missing_required_artifacts"]:
                    payload["failures"].append(
                        "NEXT_SOURCE_VERIFY_ARTIFACTS_MISSING:"
                        + ",".join(nsv["missing_required_artifacts"])
                    )
                if nsv["empty_required_artifacts"]:
                    payload["failures"].append(
                        "NEXT_SOURCE_VERIFY_ARTIFACTS_EMPTY:"
                        + ",".join(nsv["empty_required_artifacts"])
                    )
                if not nsv["has_trigger_check"]:
                    payload["failures"].append(
                        f"NEXT_SOURCE_VERIFY_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-POOLED-001: after the pooled chronological OOS campaign
            # starts, require the source registry + verified bulk-data evidence,
            # outcome-blind prereg freeze, heavy pooled evaluation triad
            # (py+json+md), independent stdlib recompute (py+json), evidence
            # audit (json+md), gate-critical evidence_audit_ alias (json), and
            # trigger check. Zero-byte placeholders fail closed, so a future
            # session cannot dodge the heavy pooled vol+liq-risk work with a
            # trigger-only, prose-only, source-probe-only, audit-only, or
            # verify-and-stop session.
            pl = _pooled_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["pooled"] = pl
            if pl["required"]:
                if pl["missing_required_artifacts"]:
                    payload["failures"].append(
                        "POOLED_ARTIFACTS_MISSING:"
                        + ",".join(pl["missing_required_artifacts"])
                    )
                if pl["empty_required_artifacts"]:
                    payload["failures"].append(
                        "POOLED_ARTIFACTS_EMPTY:"
                        + ",".join(pl["empty_required_artifacts"])
                    )
                if not pl["has_trigger_check"]:
                    payload["failures"].append(
                        f"POOLED_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-POOLED-AUDIT-001: after the adversarial pooled-panel audit
            # starts, require the outcome-blind audit prereg + heavy audit
            # triad + independent stdlib recompute + evidence package + gate
            # alias + trigger check. Generic recompute/audit/trigger-only
            # sessions and zero-byte placeholders fail closed.
            pa = _pooled_audit_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["pooled_audit"] = pa
            if pa["required"]:
                if pa["missing_required_artifacts"]:
                    payload["failures"].append(
                        "POOLED_AUDIT_ARTIFACTS_MISSING:"
                        + ",".join(pa["missing_required_artifacts"])
                    )
                if pa["empty_required_artifacts"]:
                    payload["failures"].append(
                        "POOLED_AUDIT_ARTIFACTS_EMPTY:"
                        + ",".join(pa["empty_required_artifacts"])
                    )
                if not pa["has_trigger_check"]:
                    payload["failures"].append(
                        f"POOLED_AUDIT_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-POOLED-ROBUST-002: after the leakage-hardened re-confirmation
            # campaign starts, require the outcome-blind robustness prereg + heavy
            # robustness recompute triad + independent stdlib recompute + evidence
            # audit + gate alias + trigger check. Generic recompute/audit/
            # trigger-only/verify-and-stop sessions and zero-byte placeholders
            # fail closed, so a future session cannot dodge the heavy leakage-
            # hardened vol+liq-risk robustness work.
            pr = _pooled_robust_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["pooled_robust_02"] = pr
            if pr["required"]:
                if pr["missing_required_artifacts"]:
                    payload["failures"].append(
                        "POOLED_ROBUST_ARTIFACTS_MISSING:"
                        + ",".join(pr["missing_required_artifacts"])
                    )
                if pr["empty_required_artifacts"]:
                    payload["failures"].append(
                        "POOLED_ROBUST_ARTIFACTS_EMPTY:"
                        + ",".join(pr["empty_required_artifacts"])
                    )
                if not pr["has_trigger_check"]:
                    payload["failures"].append(
                        f"POOLED_ROBUST_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-TRACKA-SOURCE-AUDIT-01: after the Track A source viability
            # audit campaign starts, require the source registry + probe triad,
            # the outcome-blind viability decision, the pivot prereg, the
            # evidence audit + gate alias, and a trigger check. Trigger-only,
            # prose-only, source-probe-only, audit-only, verify-and-stop
            # sessions and zero-byte placeholders fail closed, so a future
            # session cannot dodge the heavy Track A unlock-or-pivot work.
            ta = _tracks01_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["tracks01"] = ta
            if ta["required"]:
                if ta["missing_required_artifacts"]:
                    payload["failures"].append(
                        "TRACKA_SOURCE_AUDIT_ARTIFACTS_MISSING:"
                        + ",".join(ta["missing_required_artifacts"])
                    )
                if ta["empty_required_artifacts"]:
                    payload["failures"].append(
                        "TRACKA_SOURCE_AUDIT_ARTIFACTS_EMPTY:"
                        + ",".join(ta["empty_required_artifacts"])
                    )
                if not ta["has_trigger_check"]:
                    payload["failures"].append(
                        f"TRACKA_SOURCE_AUDIT_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-XSEC-BROAD-01: after the broad-universe (342-coin
            # ironflow_bulk) cross-sectional liquidation-risk generalization
            # campaign starts, require the on-disk source registry + outcome-blind
            # prereg + HEAVY evaluation triad + independent stdlib recompute +
            # evidence audit + gate alias + trigger check. Trigger-only, prose-only,
            # source-probe-only, audit-only, prereg-only, verify-and-stop sessions
            # and zero-byte placeholders fail closed, so a future session cannot
            # dodge the heavy broad-universe generalization test. Sessions predating
            # the campaign start are grandfathered so this refresh stays green.
            lb = _liq_xsec_broad_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["liq_xsec_broad"] = lb
            if lb["required"]:
                if lb["missing_required_artifacts"]:
                    payload["failures"].append(
                        "LIQ_XSEC_BROAD_ARTIFACTS_MISSING:"
                        + ",".join(lb["missing_required_artifacts"])
                    )
                if lb["empty_required_artifacts"]:
                    payload["failures"].append(
                        "LIQ_XSEC_BROAD_ARTIFACTS_EMPTY:"
                        + ",".join(lb["empty_required_artifacts"])
                    )
                if not lb["has_trigger_check"]:
                    payload["failures"].append(
                        f"LIQ_XSEC_BROAD_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-XSEC-BROAD-TS-01: after the temporal-stability campaign
            # starts, a post-start session cannot satisfy the gate with a trigger-
            # only, prose-only, audit-only, prereg-only, verify-and-stop, or
            # arbitrary recompute_* session. It must emit the outcome-blind
            # temporal-stability prereg, the heavy rolling-window evaluation triad,
            # the independent stdlib recompute, the evidence audit, the gate-
            # critical evidence_audit_ alias, and a trigger check, with no zero-
            # byte placeholders. This closes the last escape hatch for the ONLY
            # SUPPORTED liquidation-risk finding (BROAD-01 SUPPORTED_GENERALIZATION),
            # whose prereg never tested whether the per-block rank-IC series is
            # stable across rolling holdouts (RESEARCH_PROMPT.md §17 cond #4).
            bt = _broad_ts_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["broad_ts_01"] = bt
            if bt["required"]:
                if bt["missing_required_artifacts"]:
                    payload["failures"].append(
                        "BROAD_TS_ARTIFACTS_MISSING:"
                        + ",".join(bt["missing_required_artifacts"])
                    )
                if bt["empty_required_artifacts"]:
                    payload["failures"].append(
                        "BROAD_TS_ARTIFACTS_EMPTY:"
                        + ",".join(bt["empty_required_artifacts"])
                    )
                if not bt["has_trigger_check"]:
                    payload["failures"].append(
                        f"BROAD_TS_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-LIQ-RISK-PROGRAM-CLOSURE-01: after the formal program-closure
            # campaign starts, require the complete eight-category closure artifact
            # set under one fresh session_<UTC>/ with no zero-byte placeholders.
            pc = _program_closure_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["program_closure"] = pc
            if pc["required"]:
                if pc["missing_required_artifacts"]:
                    payload["failures"].append(
                        "PROGRAM_CLOSURE_ARTIFACTS_MISSING:"
                        + ",".join(pc["missing_required_artifacts"])
                    )
                if pc["empty_required_artifacts"]:
                    payload["failures"].append(
                        "PROGRAM_CLOSURE_ARTIFACTS_EMPTY:"
                        + ",".join(pc["empty_required_artifacts"])
                    )
                if not pc["has_trigger_check"]:
                    payload["failures"].append(
                        f"PROGRAM_CLOSURE_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )
                if not pc["has_evidence_audit_alias"]:
                    payload["failures"].append(
                        f"PROGRAM_CLOSURE_EVIDENCE_AUDIT_ALIAS_MISSING:{latest_sid}"
                    )

            # FCLR-VOL-BROAD-01: after the broad-panel funding-conditioned
            # volatility campaign starts, require the on-disk source registry +
            # outcome-blind prereg + HEAVY broad-panel walk-forward evaluation
            # triad + independent stdlib recompute + evidence audit + gate alias
            # + trigger check. Trigger-only, prose-only, source-probe-only,
            # audit-only, prereg-only, verify-and-stop sessions and zero-byte
            # placeholders fail closed, so a future session cannot dodge the
            # heavy broad-universe volatility test.
            vb = _vol_broad_state(
                text, latest_sid, latest_info["files"], latest_sdir
            )
            payload["vol_broad"] = vb
            if vb["required"]:
                if vb["missing_required_artifacts"]:
                    payload["failures"].append(
                        "VOL_BROAD_ARTIFACTS_MISSING:"
                        + ",".join(vb["missing_required_artifacts"])
                    )
                if vb["empty_required_artifacts"]:
                    payload["failures"].append(
                        "VOL_BROAD_ARTIFACTS_EMPTY:"
                        + ",".join(vb["empty_required_artifacts"])
                    )
                if vb["content_failures"]:
                    payload["failures"].append(
                        "VOL_BROAD_CONTENT_INVALID:"
                        + ",".join(vb["content_failures"])
                    )
                if not vb["has_trigger_check"]:
                    payload["failures"].append(
                        f"VOL_BROAD_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

        complete_sid = None
        for cand in reversed(ids):
            cdir = rs / cand
            if cdir.exists() and not _session_has_required(cdir)["missing"]:
                complete_sid = cand
                break

        heavy_sid = complete_sid or latest_sid
        payload["heavy_session_id"] = heavy_sid
        heavy_sdir = rs / heavy_sid
        if heavy_sdir.exists():
            payload["heavy_session_exists"] = True
            payload["heavy_session_dir"] = str(heavy_sdir.relative_to(repo))
            heavy_info = _session_has_required(heavy_sdir)
            payload["heavy_session_files"] = heavy_info["files"]
            if complete_sid is None:
                # The latest session is a new-style audit + fresh quantitative
                # session. Phase-B/C is carried forward by an older bundle, not
                # duplicated into this session; do not report it as missing.
                payload["heavy_session_mode"] = "new_style_audit_quant"
                payload["heavy_session_missing"] = []
            else:
                payload["heavy_session_mode"] = "phase_b_c_bundle"
                payload["heavy_session_missing"] = heavy_info["missing"]
                if heavy_info["missing"]:
                    payload["failures"].append(
                        f"HEAVY_SESSION_ARTIFACTS_MISSING:{heavy_sid}:{heavy_info['missing']}"
                    )
        else:
            payload["heavy_session_mode"] = "missing"
            payload["heavy_session_missing"] = []

    # (3) Root churn cap.
    rc = _root_count(rs)
    payload["root_count"] = rc
    if rc > ROOT_COUNT_CAP:
        payload["failures"].append(f"ROOT_COUNT_EXCEEDS_CAP:{rc}>{ROOT_COUNT_CAP}")

    payload["pass"] = not payload["failures"]
    payload["reason_code"] = "OK" if payload["pass"] else "HANDOFF_HEAVYWORK_GATE_FAILED"
    return payload


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    res = check()
    if args.json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        status = "PASS" if res["pass"] else "FAIL"
        print(
            f"[{status}] handoff-heavywork gate: handoff={res['handoff_exists']} "
            f"markers={res['handoff_markers_ok']} "
            f"heavy_session={res['heavy_session_id']} "
            f"session_ok={res['heavy_session_exists'] and not res['heavy_session_missing']} "
            f"root={res['root_count']}/{res['root_count_cap']} "
            f"reason={res['reason_code']}"
        )
        if res["failures"]:
            for f in res["failures"]:
                print("  -", f)
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())