# FCLR-SESSION-SYNTHESIS-01 — Protocol Freeze (PREREGISTERED, PRE-OUTCOMES)

- **Experiment ID:** FCLR-SESSION-SYNTHESIS-01-20261121T080000Z
- **Frozen at (UTC):** 2026-11-21T08:00:00Z
- **Outcome data inspected before freeze:** `false`
- **Campaign rank:** 0 (CONSOLIDATION_CAMPAIGN)

## 1. Why this campaign exists (bottleneck removal)

The repository is named **Funding-conditioned-volatility-and-liquidation-risk** — two scientific
halves reconciled by funding conditioning:

- **(a) Funding → volatility (RV).** Terminal on the frozen FCLR-001 panel
  (`41962f82...`). Funding → next-hour RV is SUPPORTED cross-sectionally only in the HIGH-RV
  regime (FCLR-XSEC-002), but every out-of-sample forward confirmation FAILED to replicate
  (FCLR-FWD-VOL-011-CONFIRM family). Hypothesis H1_primary is terminal NOT_SUPPORTED.
- **(b) Funding → liquidation risk.** Terminal on the frozen combined liquidation panel
  (`81a100d5...`). Funding → next-hour liquidation intensity is SUPPORTED cross-sectionally in the
  LOW-RV regime (FCLR-XSEC-004 count-based, FCLR-XSEC-005 notional-weighted) and across all three
  UTC session buckets (FCLR-XSEC-006), but NO out-of-sample forecast gate passed
  (FCLR-LIQ-OOS-FORECAST-001 terminal NOT_SUPPORTED: QLIKE FAIL; Brier/LogLoss PASS but joint gate
  requires ALL three).

The prior rank-0 campaign (`FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE-20261121T071500Z`) is
**TRIGGER_ONLY/BOUNDED_TRIGGER_ONLY** — it is gated on an external
`NEW_OBSERVED_LIQUIDATION_SOURCE` trigger that cannot fire inside this closed, frozen-data research
environment. That trigger gate is the structural bottleneck: future agents would idle waiting for a
signal the frozen panel cannot produce.

**This campaign removes that bottleneck** by executing a heavy, non-deferrable
evidence-consolidation + quantitative meta-analysis campaign NOW on the verified frozen panels and
the complete terminal artifact record, so significant progress continues without an external
trigger.

## 2. Design (outcome-blind)

- **Type:** evidence-consolidation and quantitative meta-analysis.
- **Data source:** existing terminal `research_state/session_*` artifacts + the two frozen panels.
  **No new outcomes are generated.** No network, no paid data, no credentials.
- **Panel audit (asserted in the synthesis script header):**
  - FCLR-001 panel: `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`,
    sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`
  - Combined liquidation panel: `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`,
    sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`

## 3. Meta-analysis protocol (frozen before any consolidation)

- **Effect size:** standardized funding-conditioning effect = `mean_diff / mean_abs_outcome`
  (per terminal test), aggregated across terminal campaigns.
- **Aggregation:** inverse-variance weighted fixed-effect synthesis, with a DerSimonian-Laird
  random-effects sensitivity check.
- **Heterogeneity:** Cochran's Q and I² reported.
- **Regime stratification:** separate synthesis for (a) RV outcome and (b) liquidation-intensity
  outcome, plus a joint cross-pillar synthesis.
- **Materiality floor preserved:** 0.02. **No post-hoc floor relaxation.**
- **Verdict rule:** the synthesis verdict is DESCRIPTIVE/CONSOLIDATORY only. It does NOT promote any
  terminal hypothesis. It states whether the consolidated evidence is directionally coherent and
  carries forward every honest terminal verdict unchanged.

## 4. Acceptance checks

Enumerated in `fclr_session_synth01_protocol_freeze_20261121T080000Z.json` →
`acceptance_checks` (20 checks). The machine-enforced gate binds the exact artifact triad:
protocol freeze (json+md), program synthesis report (json+md), frontier exhaustion audit (json+md),
negative-results preservation (json), meta-analysis (py+json+md), independent recompute (json),
evidence audit (json+md), and non-empty trigger_check (json).

## 5. Non-avoidance

Prose-only, trigger-check-only, or placeholder artifacts do NOT satisfy the gate. Re-running any
terminal campaign (STARTER-001 / XSEC-001..008) does NOT satisfy this task. The synthesis must
include a quantitative meta-analysis that reads both frozen panels and aggregates exact effect
sizes across ≥7 terminal campaigns.