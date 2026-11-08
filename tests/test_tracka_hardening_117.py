"""FCLR-NEXT-117: fclr010_execute manifest-context-behind-guard + h004 historical-pilot execution guard/marker + full scripts eval/canonical-mutation registry sweep + run_liqmicro READY frontier-writer auditability.

Deterministic, tmp-isolated, no network, no real parquet/outcome reads, no real research_state writes.

Closes exact gaps left by FCLR-NEXT-116:
  (G1) scripts/fclr010_execute.py defers manifest/split context behind guard via
       _load_outcomes_guarded/_frozen_split_context invoked ONLY by explicit outcome
       loader (post-READY). Blocked main must not pre-read manifest/splits.
  (G2) scripts/h004_fclr005_pipeline.py is out-of-scope historical Track A pilot
       (Bybit 2026 liquidation census, fixed local path, NOT Hyperliquid ironflow/
       FCLR010 guarded seam). Default execution refused with
       H004_OUT_OF_SCOPE_HISTORICAL_TRACKA_PILOT; explicit allow flag/env required.
  (G3) Full scripts/* machine-readable sweep registry; diff test fails on
       missing/unclassified/needs-manual-review scripts.
  (G4) run_liqmicro frontier mutation extracted to explicit post-gate writer
       _write_experiment_frontier_ready(); blocked never reaches pipeline/writer.

Stable prior reason codes/order/fields preserved where applicable.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.fclr010_guarded_entry import refusal_payload

REAL = Path(__file__).resolve().parent.parent
SCRIPTS = REAL / "scripts"
RS = REAL / "research_state"

BLOCKED_PAYLOAD = {
    "status": "BLOCKED",
    "outcomes_inspected": False,
    "canonical_outputs_mutated": False,
    "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
}

SCRIPT_REGISTRY = {
  "check_tracka_scope_registry_drift.py": {
    "class": "resume_gate_infra",
    "reason": "Repo-local deterministic drift check for tracka_script_scope_registry.json; fails on scripts/*.py additions/removals or malformed entries. Read-only, no network, no real research_state writes."
  },
  "cache_panel.py": {
    "class": "repo_maintenance_utility",
    "reason": "cache_panel.py: panel cache helper; no Track A liquidation outcome claim production."
  },
  "campaign_resume.py": {
    "class": "repo_maintenance_utility",
    "reason": "campaign_resume.py: campaign resume/maintenance orchestration; no Track A liquidation outcome claims/canonical liquidation mutation."
  },
  "consolidate_source_probe_fclr_next_002_104.py": {
    "class": "repo_maintenance_utility",
    "reason": "consolidate_source_probe_fclr_next_002_104.py: repo/diagnostic/maintenance utility; no Track A liquidation outcome claims or guarded canonical liquidation mutation."
  },
  "controller_progress.py": {
    "class": "repo_maintenance_utility",
    "reason": "controller_progress.py: repo/diagnostic/maintenance utility; no Track A liquidation outcome claims or guarded canonical liquidation mutation."
  },
  "coupled_build_panel.py": {
    "class": "guarded_tracka",
    "reason": "G1 machine-refuse without loader; no unguarded parquet."
  },
  "coupled_robust_eval.py": {
    "class": "guarded_tracka_ready_writing",
    "reason": "Guarded + coupled loader; READY writes summary only; blocked refuses (G1/G4)."
  },
  "coverage_audit.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "coverage_audit.py: coverage/audit utility (Track C/FCLR or auxiliary); no Hyperliquid guarded liquidation outcome claim path unless separately wired."
  },
  "coverage_audit_fclr007.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "coverage_audit_fclr007.py: coverage/audit utility (Track C/FCLR or auxiliary); no Hyperliquid guarded liquidation outcome claim path unless separately wired."
  },
  "create_blocker_evidence.py": {
    "class": "prereg_utility",
    "reason": "Emits blocker/prereg-evidence artifacts; no liquidation outcome reads/claims."
  },
  "create_forward_prereg.py": {
    "class": "prereg_utility",
    "reason": "Writes prereg records only; no outcome reads."
  },
  "deep_review_alt_sources.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "Alt-source review/provenance; no guarded liquidation outcome claims."
  },
  "diagnostics_scanner.py": {
    "class": "repo_maintenance_utility",
    "reason": "diagnostics_scanner.py: repo/diagnostic/maintenance utility; no Track A liquidation outcome claims or guarded canonical liquidation mutation."
  },
  "download_extended.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "download_extended.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "download_fclr012v_premium_index.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "download_fclr012v_premium_index.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "exhaustive_binance_probe.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "exhaustive_binance_probe.py: bounded fetch/probe/provenance utility; no Track A liquidation outcome claim production."
  },
  "extract_cache.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "extract_cache.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "extract_fclr012v_klines.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "extract_fclr012v_klines.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr002_coverage_audit.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr002_coverage_audit.py: coverage/audit utility (Track C/FCLR or auxiliary); no Hyperliquid guarded liquidation outcome claim path unless separately wired."
  },
  "fclr002_download.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr002_download.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr002_gapfill.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr002_gapfill.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr003_download.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr003_download.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr003_extract.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr003_extract.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr004_download.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr004_download.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr006_block_audit.py": {
    "class": "unclassified_auxiliary",
    "reason": "fclr006_block_audit.py: auxiliary script with no detected Track A liquidation claim/eval/canonical mutation pattern; no guarded Hyperliquid liquidation outcome path detected."
  },
  "fclr007_download.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr007_download.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr008_coverage_audit.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr008_coverage_audit.py: coverage/audit utility (Track C/FCLR or auxiliary); no Hyperliquid guarded liquidation outcome claim path unless separately wired."
  },
  "fclr009_coverage_audit.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr009_coverage_audit.py: coverage/audit utility (Track C/FCLR or auxiliary); no Hyperliquid guarded liquidation outcome claim path unless separately wired."
  },
  "fclr010_coverage_audit.py": {
    "class": "guarded_tracka_audit_ready_writing",
    "reason": "Guarded coverage audit; blocked main refuses/no canonical JSON write (G2)."
  },
  "fclr010_execute.py": {
    "class": "guarded_tracka_ready_writing",
    "reason": "Guarded execute + READY-only canonical summary/manifest mutation; blocked refuses before writes (G1/G4)."
  },
  "fclr010_execute_fast.py": {
    "class": "guarded_tracka",
    "reason": "Fast refusal/no-op unless explicit READY_FROZEN+loader."
  },
  "fclr010_guarded_entry.py": {
    "class": "guarded_tracka",
    "reason": "Single guarded execution entry; refuses blocked before outcome load."
  },
  "fclr010_harness.py": {
    "class": "harness_core",
    "reason": "Defines FCLR010Harness/guarded execute_ready_data_load contract."
  },
  "fclr010_validate.py": {
    "class": "prereg_utility",
    "reason": "Validation/prereg helper; no guarded outcome claim reads."
  },
  "fclr012_download.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr012_download.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "fclr012v_coverage_audit.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr012v_coverage_audit.py: coverage/audit utility (Track C/FCLR or auxiliary); no Hyperliquid guarded liquidation outcome claim path unless separately wired."
  },
  "fclr013_coverage_audit.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr013_coverage_audit.py: coverage/audit utility (Track C/FCLR or auxiliary); no Hyperliquid guarded liquidation outcome claim path unless separately wired."
  },
  "fclr015_verify_cache_provenance_2024q2q3.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr015_verify_cache_provenance_2024q2q3.py: bounded unauthenticated Binance Vision provenance verification for cached 2024-04..09 files (sha256/ETag/Last-Modified GET); admissibility evidence only, no outcome reads/claims, no Track A guarded liquidation path."
  },
  "fclr016_repair_canonical_cache.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr016_repair_canonical_cache.py: bounded unauthenticated Binance Vision canonical cache repair for 2025+ (downloads missing canonical daily zips into kind-specific subdirs; no overwrites; sha256/ETag/Last-Modified recorded); admissibility evidence only, no outcome reads/claims, no Track A guarded liquidation path, no canonical eval/cross-track writes."
  },
  "fclr016_v5_admissibility_report.py": {
    "class": "prereg_utility",
    "reason": "fclr016_v5_admissibility_report.py: read-only Gate 4 v5 admissibility report; reads 4 package artifacts (provenance manifest, completeness/leakage audit, terms evidence, prereg draft) and emits a stable JSON refusal verdict; no outcome/data/network loading, no canonical eval/cross-track writes, no Track A liquidation outcome claims."
  },
  "fclr016_v5_preflight_summary.py": {
    "class": "prereg_utility",
    "reason": "fclr016_v5_preflight_summary.py: read-only Gate 4 v5 preflight summary; runs fail-closed admissibility package check and emits JSON + markdown refusal matrix; no outcome/data/network loading, no canonical eval/cross-track writes, no Track A liquidation outcome claims."
  },
  "fclr016_v5_promotion_dryrun.py": {
    "class": "prereg_utility",
    "reason": "fclr016_v5_promotion_dryrun.py: read-only Gate 4 v5 promotion dry-run harness; evaluates real blocked package plus synthetic-fixture-only GO matrix in tmp copies, never writes real terms evidence or canonical artifacts; no outcome/data/network loading, no canonical eval/cross-track writes, no Track A liquidation outcome claims."
  },
  "fclr017_gate4_cache_coverage_audit.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr017_gate4_cache_coverage_audit.py: deterministic read-only local cache coverage/integrity/planning audit for Gate 4 2024-04..09/12 5-symbol kline+funding data; planning evidence only, no outcome computation, no network, no freeze/promotion, no Track A claims, no canonical/sealed overwrite."
  },
  "fclr018_gate4_prereg_readiness_matrix.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr018_gate4_prereg_readiness_matrix.py: deterministic read-only Gate 4 prereg-readiness/draft design matrix from local evidence; enumerates candidate windows and emits DRAFT_NOT_FROZEN skeleton (no_confirmatory_outcomes/exploratory_only/no_network/not_go). Planning/draft only; no outcome computation, no freeze/promotion, no network, no Track A claims, no sealed overwrite."
  },
  "fclr019_gate4_evidence_bundle_index.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr019_gate4_evidence_bundle_index.py: deterministic read-only Gate 4 evidence-bundle index from fclr018+local provenance/admissibility refs; maps confirmatory prerequisites per candidate window to present_unverified/present_blocker/missing. Draft-only/no_confirmatory_outcomes/no_network/not_go; no freeze/promotion, no prerequisite satisfied, no Track A claims, no sealed overwrite."
  },
  "fclr020_gate4_readiness_action_matrix.py": {
    "class": "track_c_or_aux_audit_utility",
    "reason": "fclr020_gate4_readiness_action_matrix.py: deterministic read-only Gate 4 readiness/action matrix from fclr019; per-window actions/blockers/verification checks, authorizes_confirmatory_outcomes=false, no satisfaction inference. Draft-only/no_confirmatory_outcomes/no_network/not_go; no freeze/promotion, no prerequisite satisfied, no Track A claims, no sealed overwrite."
  },
  "fclr016_v5_terms_evidence_template.py": {
    "class": "prereg_utility",
    "reason": "fclr016_v5_terms_evidence_template.py: deterministic non-evidentiary terms-evidence TEMPLATE generator; writes only a clearly non-evidentiary template to an explicit user path, never creates RESOLVED_VERIFIED status, no outcome/data/network loading, no canonical eval/cross-track writes, no Track A liquidation outcome claims."
  },
  "fclr016_validate_v5_admissibility.py": {
    "class": "prereg_utility",
    "reason": "fclr016_validate_v5_admissibility.py: deterministic read-only Gate 4 v5 admissibility validator; fail-closed on the 4-artifact package, exits 0 for consistent blocked/non-GO package and 2 with --expect-go unless full confirmatory GO; no outcome/data/network loading, no canonical eval/cross-track writes, no Track A liquidation outcome claims."
  },
  "fclr016_verify_cache_provenance_2025plus.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr016_verify_cache_provenance_2025plus.py: bounded unauthenticated Binance Vision provenance verification for cached 2025+ files (sha256/ETag/Last-Modified GET vs local canonical zips, placeholder-duplicate hazard detection); admissibility evidence only, no outcome reads/claims, no Track A guarded liquidation path, no canonical eval/cross-track writes."
  },
  "forecast_pipeline.py": {
    "class": "track_c_sealed_volatility",
    "reason": "forecast_pipeline.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "freeze_fclr009_splits.py": {
    "class": "track_c_sealed_volatility",
    "reason": "freeze_fclr009_splits.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "funding_correction_replication.py": {
    "class": "track_c_sealed_volatility",
    "reason": "FCLR-H002 funding-correction replication (volatility/correction-time context); explicitly distinct from liquidation outcomes; no Track A guarded liquidation reads."
  },
  "funding_interaction_analysis.py": {
    "class": "track_c_sealed_volatility",
    "reason": "funding_interaction_analysis.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "funding_interaction_analysis_fast.py": {
    "class": "track_c_sealed_volatility",
    "reason": "funding_interaction_analysis_fast.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "generate_tracka_fixtures.py": {
    "class": "test_fixture_utility",
    "reason": "Generates synthetic Track A fixtures for tests; no real outcome reads/canonical claims."
  },
  "h002_download_2024_q1.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "h002_download_2024_q1.py: bounded fetch/probe/provenance utility; no Track A liquidation outcome claim production."
  },
  "h004_audit.py": {
    "class": "out_of_scope_historical_tracka_pilot",
    "reason": "Audit helper for historical h004/FCLR-005 pilot artifacts; not guarded fclr010 outcome path."
  },
  "h004_complete_cache.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "h004_complete_cache.py: data fetch/extract/provenance helper; not a liquidation-risk claim producer and not a guarded Track A outcome reader."
  },
  "h004_download_2026.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "Download/provenance helper for 2026 h004 data; not a liquidation-risk claim producer."
  },
  "h004_fclr005_pipeline.py": {
    "class": "out_of_scope_historical_tracka_pilot",
    "reason": "Historical Track A observed-label pilot using Bybit 2026 liquidation census (LIQ constant, fixed local path) + Binance features; NOT Hyperliquid ironflow and NOT routed through FCLR010Harness guarded outcome-loader seam. Produces pilot evaluation summary; out of guarded fclr010 outcome contract by design (distinct experiment/protocol). Must not be conflated with Hyperliquid observed-liquidation gate."
  },
  "hl_coverage_probe.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "Coverage probe/provenance; no guarded outcome claims."
  },
  "hunt_alternative_liquidation_sources.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "Source-hunt/provenance; no guarded outcome claims."
  },
  "hyperliquid_funding_fetch.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "Funding fetch/provenance utility; no liquidation outcome claim production."
  },
  "liqmicro_audit.py": {
    "class": "guarded_tracka_audit_ready_writing",
    "reason": "Guarded liqmicro audit; blocked main refuses/no canonical md write (G2)."
  },
  "merge_redundant_artifacts_090.py": {
    "class": "repo_maintenance_utility",
    "reason": "Artifact maintenance; no liquidation outcome reads/claims."
  },
  "migrate_digest_archive_090.py": {
    "class": "repo_maintenance_utility",
    "reason": "Digest/archive maintenance; no liquidation outcome reads/claims."
  },
  "monitor_ironflow_liquidations.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "HTTP probe/provenance ingestion; not liquidation-risk claim producer."
  },
  "nonfinite_serialization.py": {
    "class": "track_c_or_aux_utility",
    "reason": "nonfinite_serialization.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "overlay_quick.py": {
    "class": "guarded_tracka_ready_writing",
    "reason": "Guarded + coupled loader; READY writes summary/frontier/cross-track; blocked refuses (G1/G4)."
  },
  "overlay_tracka_execute.py": {
    "class": "guarded_tracka_ready_writing",
    "reason": "Guarded + coupled loader; READY writes summary/frontier/cross-track; blocked refuses (G1/G4)."
  },
  "probe_fclr012v_extend.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "probe_fclr012v_extend.py: bounded fetch/probe/provenance utility; no Track A liquidation outcome claim production."
  },
  "probe_fclr012v_extend2.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "probe_fclr012v_extend2.py: bounded fetch/probe/provenance utility (FCLR-012-V forward extension); no Track A liquidation outcome claim production."
  },
  "run_evaluation.py": {
    "class": "track_c_sealed_volatility",
    "reason": "Track C/FCLR volatility evaluation path (sealed); liquidation terms absent as claim target; no Track A guarded liquidation outcome reads."
  },
  "run_evaluation_fixed.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_evaluation_fixed.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "run_fi_quick.py": {
    "class": "track_c_or_aux_utility",
    "reason": "run_fi_quick.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "run_h003.py": {
    "class": "track_b_modeled_boundary",
    "reason": "Track B/FCLR-H003 modeled boundary-breach labels (synthetic); explicitly modeled != observed liquidations; out of Track A observed outcome contract."
  },
  "run_h003_ext.py": {
    "class": "track_b_modeled_boundary",
    "reason": "Track B modeled boundary extension; modeled != observed."
  },
  "run_h003_ext_fast.py": {
    "class": "track_b_modeled_boundary",
    "reason": "Track B modeled boundary extension (fast); modeled != observed."
  },
  "run_h003_ext_inference.py": {
    "class": "track_b_modeled_boundary",
    "reason": "Track B modeled boundary inference; modeled != observed."
  },
  "run_liqmicro.py": {
    "class": "guarded_tracka",
    "reason": "Guarded; blocked no loader/canonical/frontier mutation (115 G2)."
  },
  "run_liqmicro_v2.py": {
    "class": "guarded_tracka",
    "reason": "Guarded; blocked no loader/canonical/frontier mutation (115 G2)."
  },
  "run_stream_b_deep_analysis_001.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_stream_b_deep_analysis_001.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "run_stream_b_feature_extension.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_stream_b_feature_extension.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "run_stream_b_robustness_002.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_stream_b_robustness_002.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "run_trackc_deeper_validation_fclr011.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_trackc_deeper_validation_fclr011.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "run_trackc_robustness_fclr011.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_trackc_robustness_fclr011.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "run_volatility_funding_eval.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_volatility_funding_eval.py: Track C sealed volatility/forecast/robustness or supporting utility; no Track A Hyperliquid guarded liquidation outcome claims."
  },
  "synthetic_boundary_labels.py": {
    "class": "track_b_modeled_boundary",
    "reason": "Synthetic/modeled boundary label construction; modeled != observed, no observed liquidation claims."
  },
  "track_c_inventory_harden.py": {
    "class": "repo_maintenance_utility",
    "reason": "track_c_inventory_harden.py: repo/diagnostic/maintenance utility; no Track A liquidation outcome claims or guarded canonical liquidation mutation."
  },
  "tracka_operator_report.py": {
    "class": "resume_gate_infra",
    "reason": "Read-only operator report composition."
  },
  "tracka_resume_check.py": {
    "class": "resume_gate_infra",
    "reason": "Read-only checks; seam wiring only; no outcome reads/claims."
  },
  "tracka_resume_gate.py": {
    "class": "resume_gate_infra",
    "reason": "Read-only fail-closed gate; no outcome reads/canonical mutation."
  },
  "tracka_rubric.py": {
    "class": "resume_gate_infra",
    "reason": "Track A admissibility rubric/GO-NO-GO logic; pure assessment, no outcome parquet reads or canonical claim mutation."
  },
  "verify_heavy_work_004i.py": {
    "class": "repo_maintenance_utility",
    "reason": "Historical campaign checklist verifier; no liquidation outcome reads/claims."
  },
  "volatility_track_progress.py": {
    "class": "track_c_sealed_volatility",
    "reason": "Track C progress/report utility (volatility); no Track A guarded liquidation outcome reads."
  },
  "write_trigger_harden_successor.py": {
    "class": "prereg_utility",
    "reason": "Trigger-hardening artifacts; no outcome reads."
  }
,
  "_debug_abl.py": {
    "class": "unclassified_auxiliary",
    "reason": "_debug_abl.py: local debug/inspection utility for ablation pipeline magnitudes; no Track A liquidation outcome claims, no guarded Hyperliquid seam, no canonical eval/cross-track writes."
  },
  "_debug_ablations.py": {
    "class": "unclassified_auxiliary",
    "reason": "_debug_ablations.py: local debug utility for funding ablation pipeline; no Track A liquidation outcome claims, no guarded Hyperliquid seam, no canonical eval/cross-track writes."
  },
  "_debug_dup.py": {
    "class": "unclassified_auxiliary",
    "reason": "_debug_dup.py: local debug utility for duplicate-column checks; no Track A liquidation outcome claims, no guarded Hyperliquid seam, no canonical eval/cross-track writes."
  },
  "_debug_funding.py": {
    "class": "unclassified_auxiliary",
    "reason": "_debug_funding.py: local debug utility for funding ablation panel/prediction inspection; no Track A liquidation outcome claims, no guarded Hyperliquid seam, no canonical eval/cross-track writes."
  },
  "_debug_loghar.py": {
    "class": "unclassified_auxiliary",
    "reason": "_debug_loghar.py: local debug utility comparing log-HAR vs OLS; no Track A liquidation outcome claims, no guarded Hyperliquid seam, no canonical eval/cross-track writes."
  },
  "_debug_logridge.py": {
    "class": "unclassified_auxiliary",
    "reason": "_debug_logridge.py: local debug utility comparing log-ridge vs OLS HAR predictions; no Track A liquidation outcome claims, no guarded Hyperliquid seam, no canonical eval/cross-track writes."
  },
  "fclr_h001_extract.py": {
    "class": "raw_fetch_monitor_provenance",
    "reason": "fclr_h001_extract.py: local zip extraction/provenance helper for Binance public-archive data into data/raw; restartable/idempotent, no network required by design, no Track A liquidation outcome claim producer."
  },
  "run_funding_ablations.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_funding_ablations.py: Gate 4 funding-conditioned volatility ablations (Track C), leakage-resistant multi-split pilot, local admissible Binance data only; writes evaluation/manifest/leakage summaries as non-confirmatory pilot evidence; no Track A Hyperliquid guarded liquidation outcome reads/claims."
  },
  "run_rv_baseline.py": {
    "class": "track_c_sealed_volatility",
    "reason": "run_rv_baseline.py: RV-only OOS baseline (Gate 3, Track C), leakage-resistant walk-forward on local Binance data; writes evaluation/manifest summaries; no Track A Hyperliquid guarded liquidation outcome reads/claims."
  },
}

ALLOWED_CLASSES = {
    "guarded_tracka", "guarded_tracka_ready_writing", "guarded_tracka_audit_ready_writing",
    "harness_core", "resume_gate_infra", "prereg_utility", "raw_fetch_monitor_provenance",
    "track_b_modeled_boundary", "track_c_sealed_volatility", "track_c_or_aux_audit_utility",
    "track_c_or_aux_utility", "test_fixture_utility", "repo_maintenance_utility",
    "out_of_scope_historical_tracka_pilot", "unclassified_auxiliary",
}

LIQ_OUTCOME_PATTERNS = re.compile(
    r"read_parquet\s*\(|pyarrow\.parquet|pq\.read_table|pq\.read_|ironflow_events|"
    r"liquidat.*\.csv|liquidat.*\.parquet|pd\.read_csv\(.*liq|load_.*liquidat",
    re.I,
)
EVAL_SUMMARY_PATTERN = re.compile(r"evaluation_summary", re.I)
CANONICAL_RS_PATTERN = re.compile(r"experiment_frontier\.json|cross_track_decision|run_manifest\.json", re.I)
GUARDED_SEAM_PATTERN = re.compile(r"guarded_execute|fclr010_guarded_entry|FCLR010Harness")


def _loader_must_not_run(*_a, **_k):
    raise AssertionError("outcome/parquet loader must not run on blocked branch")


def _snapshot(paths):
    return {p: (p.read_bytes() if p.exists() else None) for p in paths}


class Test117G1Fclr010ExecuteManifestBehindGuard(unittest.TestCase):
    def test_main_blocked_no_pre_guard_manifest_read(self):
        from scripts import fclr010_execute
        canon = [RS / "evaluation_summary_FCLR010.md", RS / "run_manifest.json"]
        before = _snapshot(canon)
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch("scripts.fclr010_execute._load_outcomes", side_effect=_loader_must_not_run), \
             patch("scripts.fclr010_execute._frozen_split_context", side_effect=AssertionError("pre-guard split context read on blocked")), \
             patch("scripts.fclr010_execute.FCLR010Harness._load_json_lfs_aware", side_effect=AssertionError("pre-guard manifest read on blocked")):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = fclr010_execute.main()
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        self.assertIn("BLOCKED", out)
        self.assertNotIn("Splits:", out)
        for p, b in before.items():
            self.assertEqual(b, p.read_bytes() if p.exists() else None, p)

    def test_deferred_split_context_only_in_guarded_loader(self):
        src = (SCRIPTS / "fclr010_execute.py").read_text()
        self.assertIn("def _frozen_split_context", src)
        self.assertIn("def _load_outcomes_guarded", src)
        self.assertIn("outcome_loader=_load_outcomes_guarded", src)
        main_src = src[src.index("def main"):src.index("files = loaded")]
        before_guard = main_src.split("guarded_execute")[0]
        self.assertNotIn("_load_json_lfs_aware(RUN_MANIFEST)", before_guard)
        self.assertNotIn("split_boundaries_fclr010", before_guard)

    def test_guarded_loader_reads_splits_only_when_called(self):
        from scripts.fclr010_execute import _frozen_split_context
        import scripts.fclr010_execute as mod
        with tempfile.TemporaryDirectory() as td:
            m = Path(td) / "run_manifest.json"
            m.write_text(json.dumps({"split_boundaries_fclr010": {
                "frozen_before_outcomes": True,
                "train": {"start": "2026-01-01T00:00:00Z", "end": "2026-01-10T00:00:00Z"},
                "validation": {"start": "2026-01-11T00:00:00Z", "end": "2026-01-15T00:00:00Z"},
                "test": {"start": "2026-01-16T00:00:00Z", "end": "2026-01-20T00:00:00Z"},
            }}))
            old = mod.RUN_MANIFEST
            try:
                mod.RUN_MANIFEST = m
                ctx = _frozen_split_context()
                self.assertTrue(ctx["splits"]["frozen_before_outcomes"])
            finally:
                mod.RUN_MANIFEST = old

    def test_blocked_branch_never_mutates_manifest_or_summary(self):
        from scripts import fclr010_execute
        targets = [RS / "evaluation_summary_FCLR010.md", RS / "run_manifest.json"]
        before = _snapshot(targets)
        for payload in [dict(BLOCKED_PAYLOAD), {"status": "BLOCKED", "reason_code": "X", "outcomes_inspected": False, "canonical_outputs_mutated": False}]:
            with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=payload), \
                 patch("scripts.fclr010_execute._load_outcomes", side_effect=_loader_must_not_run), \
                 patch("scripts.fclr010_execute._frozen_split_context", side_effect=AssertionError("blocked")):
                with redirect_stdout(io.StringIO()):
                    fclr010_execute.main()
        for p, b in before.items():
            self.assertEqual(b, p.read_bytes() if p.exists() else None, p)


class Test117G2H004HistoricalPilotGuard(unittest.TestCase):
    def test_default_execution_refused_no_canonical_mutation(self):
        import importlib
        mod = importlib.import_module("scripts.h004_fclr005_pipeline")
        importlib.reload(mod)
        targets = [RS / "evaluation_summary_FCLR005.md", RS / "experiment_frontier.json",
                   RS / "hypothesis_registry.json", RS / "run_manifest.json", RS / "liqmicro_data_audit_001.md"]
        before = _snapshot(targets)
        old_argv = sys.argv[:]
        old_env = os.environ.get(mod.H004_ALLOW_ENV)
        try:
            sys.argv = ["h004_fclr005_pipeline.py"]
            os.environ.pop(mod.H004_ALLOW_ENV, None)
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = mod.main()
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "BLOCKED")
            self.assertEqual(payload["reason_code"], "H004_OUT_OF_SCOPE_HISTORICAL_TRACKA_PILOT")
            self.assertTrue(payload["out_of_scope_historical_tracka_pilot"])
            self.assertFalse(payload["hyperliquid_fclr010_guarded_seam"])
            self.assertFalse(payload["canonical_outputs_mutated"])
            self.assertFalse(payload["network"])
            self.assertFalse(payload["writes_real_research_state"])
        finally:
            sys.argv = old_argv
            if old_env is None:
                os.environ.pop(mod.H004_ALLOW_ENV, None)
            else:
                os.environ[mod.H004_ALLOW_ENV] = old_env
        for p, b in before.items():
            self.assertEqual(b, p.read_bytes() if p.exists() else None, p)

    def test_quarantine_markers_present(self):
        src = (SCRIPTS / "h004_fclr005_pipeline.py").read_text()
        mod = __import__("scripts.h004_fclr005_pipeline", fromlist=["x"])
        self.assertTrue(mod.H004_OUT_OF_SCOPE_HISTORICAL_TRACKA_PILOT)
        self.assertFalse(mod.H004_HYPERLIQUID_FCLR010_GUARDED_SEAM)
        self.assertNotIn("FCLR010Harness", src)
        self.assertNotIn("fclr010_guarded_entry", src)
        self.assertIn("Bybit 2026 liquidation census", src)

    def test_refusal_payload_shape_stable(self):
        from scripts.h004_fclr005_pipeline import _h004_refusal
        p = _h004_refusal()
        for k in ["status", "reason_code", "out_of_scope_historical_tracka_pilot",
                  "hyperliquid_fclr010_guarded_seam", "canonical_outputs_mutated",
                  "network", "writes_real_research_state", "script"]:
            self.assertIn(k, p)
        self.assertEqual(p["script"], "h004_fclr005_pipeline")


class Test117G3FullScriptsRegistrySweep(unittest.TestCase):
    def test_registry_covers_all_scripts(self):
        actual = sorted(p.name for p in SCRIPTS.glob("*.py"))
        missing = [n for n in actual if n not in SCRIPT_REGISTRY]
        extra = [n for n in SCRIPT_REGISTRY if n not in actual]
        self.assertEqual(missing, [], f"unregistered scripts: {missing}")
        self.assertEqual(extra, [], f"registry has removed scripts: {extra}")

    def test_registry_entries_valid(self):
        for name, meta in SCRIPT_REGISTRY.items():
            self.assertIn("class", meta, name)
            self.assertIn("reason", meta, name)
            self.assertIn(meta["class"], ALLOWED_CLASSES, f"{name}: {meta['class']}")
            self.assertNotIn("needs_manual", meta["class"], name)
            self.assertGreaterEqual(len(meta["reason"]), 15, name)

    def test_risk_scripts_have_explicit_guard_or_scope(self):
        for name, meta in SCRIPT_REGISTRY.items():
            cls = meta["class"]
            t = (SCRIPTS / name).read_text(errors="ignore")
            risk = EVAL_SUMMARY_PATTERN.search(t) or CANONICAL_RS_PATTERN.search(t) or LIQ_OUTCOME_PATTERNS.search(t)
            if not risk:
                continue
            self.assertIn(cls, ALLOWED_CLASSES, f"{name} risk flags but bad class")
            if cls.startswith("guarded_tracka"):
                self.assertTrue(GUARDED_SEAM_PATTERN.search(t) or "guard" in t.lower(), name)
            if name == "h004_fclr005_pipeline.py":
                self.assertEqual(cls, "out_of_scope_historical_tracka_pilot")
                self.assertNotIn("FCLR010Harness", t)
                self.assertNotIn("fclr010_guarded_entry", t)

    def test_no_new_unclassified_eval_summary_writers(self):
        for name, meta in SCRIPT_REGISTRY.items():
            t = (SCRIPTS / name).read_text(errors="ignore")
            if EVAL_SUMMARY_PATTERN.search(t):
                self.assertNotEqual(meta["class"], "unclassified_auxiliary", name)


class Test117G4RunLiqmicroFrontierWriterAuditability(unittest.TestCase):
    def _import_run_liqmicro(self):
        import importlib, types
        saved = {}
        def _ensure(mn, attrs=None):
            if mn in sys.modules:
                return
            m = types.ModuleType(mn)
            for k,v in (attrs or {}).items(): setattr(m,k,v)
            sys.modules[mn] = m
            saved[mn] = None
        class _R:
            def summary(self): return ''
            params = pvalues = bse = tvalues = {}
        class _OLS:
            def __init__(self,*a,**k): pass
            def fit(self,*a,**k): return _R()
        _ensure('statsmodels'); _ensure('statsmodels.api', {'OLS': _OLS, 'add_constant': lambda x:x})
        _ensure('statsmodels.formula.api')
        # liqmicro submodules: provide expected names
        for mn, name in [('analysis.liqmicro.features','LiqMicroFeatures'),
                         ('analysis.liqmicro.models','LiqMicroModels'),
                         ('analysis.liqmicro.stats','LiqMicroStats')]:
            if mn not in sys.modules:
                m = types.ModuleType(mn); setattr(m,name,type(name,(),{}))
                sys.modules[mn]=m; saved[mn]=None
        try:
            sys.modules.pop('scripts.run_liqmicro', None)
            mod = importlib.import_module('scripts.run_liqmicro')
            return mod
        finally:
            sys.modules.pop('scripts.run_liqmicro', None)
            for mn, prev in saved.items():
                if prev is None: sys.modules.pop(mn, None)
                else: sys.modules[mn]=prev

    def test_blocked_never_calls_pipeline_or_frontier_writer(self):
        mod = self._import_run_liqmicro()
        frontier = RS / "experiment_frontier.json"
        before = frontier.read_bytes() if frontier.exists() else None
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch.object(mod, "_run_pipeline", side_effect=AssertionError("pipeline on blocked")), \
             patch.object(mod, "_write_experiment_frontier_ready", side_effect=AssertionError("frontier writer on blocked")), \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: {**k, "status": "BLOCKED"}):
            with redirect_stdout(io.StringIO()):
                rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(before, frontier.read_bytes() if frontier.exists() else None)

    def test_explicit_frontier_writer_exists_and_is_pipeline_only(self):
        src = (SCRIPTS / "run_liqmicro.py").read_text()
        self.assertIn("def _write_experiment_frontier_ready", src)
        self.assertIn("_write_experiment_frontier_ready(any_sig, summary_path)", src)
        main_src = src[src.index("def main"):]
        self.assertNotIn("_write_experiment_frontier_ready", main_src.split("_run_pipeline")[0])

    def test_frontier_writer_isolated_tmp_no_real_rs_mutation(self):
        mod = self._import_run_liqmicro()
        real_frontier = RS / "experiment_frontier.json"
        before = real_frontier.read_bytes() if real_frontier.exists() else None
        with tempfile.TemporaryDirectory() as td:
            tfront = Path(td) / "experiment_frontier.json"
            tfront.write_text(json.dumps({"frontier": []}))
            tsum = Path(td) / "summary.md"; tsum.write_text("x")
            old = mod.RESEARCH_STATE
            try:
                mod.RESEARCH_STATE = Path(td)
                mod._write_experiment_frontier_ready(0, tsum)
                got = json.loads(tfront.read_text())
                self.assertIn("FCLR-LIQMICRO-001", got)
            finally:
                mod.RESEARCH_STATE = old
        self.assertEqual(before, real_frontier.read_bytes() if real_frontier.exists() else None)


class Test117StableContracts(unittest.TestCase):
    def test_refusal_payload_stable(self):
        p = refusal_payload(reason="x", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", script="s")
        self.assertEqual(p["status"], "BLOCKED")
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["network"])


if __name__ == "__main__":
    unittest.main()
