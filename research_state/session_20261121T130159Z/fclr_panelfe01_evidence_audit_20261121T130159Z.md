# FCLR-PANEL-FE-001 — Evidence Audit

**Session:** session_20261121T130159Z
**Experiment ID:** FCLR-PANEL-FE-001-20261121T130159Z
**Campaign:** FCLR-PANEL-FE-001
**Verdict:** NOT_SUPPORTED (overall)

## What this audit ties together

Each verdict below is tied to its concrete artifact on disk under `research_state/session_20261121T130159Z/`:

| Verdict | Artifact | Role |
|---|---|---|
| Prereg freeze (outcome-blind) | `fclr_panelfe01_prereg_20261121T130159Z.json` + `.md` | Froze hypotheses, models, inference, walk-forward protocol, 2% materiality floor, panel sha256, `outcome_data_inspected_before_freeze=false` |
| Panel-FE estimation + walk-forward OOS | `fclr_panelfe01_eval_20261121T130159Z.py` + `.json` + `.md` | Two-way (coin + hour) FE; cluster-robust + Driscoll-Kraay + Newey-West SE; QLIKE + Diebold-Mariano; regime cuts |
| Independent recompute | `fclr_panelfe01_recompute_20261121T130159Z.py` + `.json` | Pure numpy recompute from raw parquet; concurs with eval (NOT_SUPPORTED) |
| This evidence audit | `fclr_panelfe01_evidence_audit_20261121T130159Z.json` + `.md` | Ties each verdict to its artifacts (this document) |
| Gate-critical audit (literal prefix) | `evidence_audit_20261121T130159Z.json` | Satisfies gate `AUDIT_PREFIX="evidence_audit_"` new-style heavy-session check |
| Trigger check | `trigger_check_20261121T130159Z.json` | Non-empty; records no external trigger required (frozen panels are sole inputs) |

## Half A — volatility (H_panelfe_vol): NOT_SUPPORTED

- Coefficient on `signed_funding` in `next_log_rv1h ~ coin_FE + hour_FE + signed_funding` is not HAC-significant (Driscoll-Kraay 95% CI includes zero).
- Implied effect from +1 SD funding shock is below the 2% materiality floor (frozen, not relaxed).
- Walk-forward QLIKE relative reduction is not positive; Diebold-Mariano does not reject equal predictive accuracy.
- Robustness contrasts (A2 `target_rv24h_log`, A3 `abs_funding_pct_trail`) likewise do not clear the joint gate (HAC significance + materiality + Holm).

## Half B — liquidation intensity (H_panelfe_liq): NOT_SUPPORTED

- Coefficient on `funding_rate_mean` in `log1p(liq_count) ~ coin_FE + hour_FE + funding_rate_mean` is HAC-significant but the implied 1-SD effect is below the 2% materiality floor.
- Holm-adjusted p-value does not pass the familywise threshold.
- Walk-forward QLIKE relative reduction = -2.96% (funding worse than baseline); DM p = 0.71 (equal accuracy not rejected).
- Robustness contrasts (B2 `log1p(liq_notional)`, B3 `abs_fund_pct_mean`) likewise do not clear the joint gate.

## Cross-references (kept distinct)

- FCLR-XSEC-002 (RV tercile, SUPPORTED) and FCLR-XSEC-004/005/006 (liquidation intensity, SUPPORTED) are **pooled cross-sectional regime contrasts** — a different estimand from this within-(coin, hour) two-way FE design. Their SUPPORTED verdicts do not carry over; this campaign's NOT_SUPPORTED is an honest null for the panel-FE estimand.
- Observed liquidations (Track A) kept distinct from modeled boundary breaches (Track B) and from RV forecasts.

## Hard constraints honored (all verified)

- `outcome_data_inspected_before_freeze=false` — prereg frozen before any outcome statistic.
- Both frozen panel sha256 asserted in script headers before any read.
- `premium` never used (100% null, `NOT_COMPUTABLE_WITHOUT_INDEX_PRICE`).
- `funding_asof_lag_h` (hours-since-funding) never used as a rate.
- No random train/test split; strictly chronological expanding-window walk-forward.
- Materiality floor 0.02 frozen; a null is recorded as NOT_SUPPORTED, not threshold-shopped.
- No sealed protocol overwritten (`research_state/research_protocol.md` untouched).
- No root-level `research_state/*.md` or `*.json` added (root count stays 499/500).
- No `.github/workflows` modified.
- No network calls, no credentials, no paid data; frozen panels are the sole inputs.
- No terminal/superseded campaigns re-run.

## Artifact completeness (machine-enforced gate set)

All FCLR-PANEL-FE-001 required artifacts present and non-empty under `session_20261121T130159Z/`:
- `fclr_panelfe01_prereg_*.json` + `.md` (complete, pre-existing)
- `fclr_panelfe01_eval_*.py` + `.json` + `.md` (complete, this session)
- `fclr_panelfe01_recompute_*.py` + `.json` (complete, this session)
- `fclr_panelfe01_evidence_audit_*.json` + `.md` (complete, this session)
- `evidence_audit_*.json` (complete, this session — gate-critical literal prefix)
- `trigger_check_*.json` (complete, this session, non-empty)
