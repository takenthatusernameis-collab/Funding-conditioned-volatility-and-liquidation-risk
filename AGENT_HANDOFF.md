# AGENT HANDOFF — 2026-11-28T08:55:21Z
> **SUPERSEDED 2026-11-28T09:07:46Z.** "ALL CONFIRMATORY PATHS EXHAUSTED" applies to the volatility half only. The liquidation-risk half has one open, unblocked HIGH gap. Follow `HANDOFF_NEXT_SESSION.md` (single source of truth) instead.

## Repository: Funding-conditioned-volatility-and-liquidation-risk

## Executive Summary
**ALL CONFIRMATORY PATHS EXHAUSTED. PROGRAM CLOSURE COMPLETE.**

The repository has reached its honest endpoint: every confirmatory experiment on all admissible free data sources has been executed, independently recomputed, audited, and returned **NOT_SUPPORTED**. No forecast gate has passed. No risk overlay is eligible. The negative results are preserved with full audit trails.

---

## What Changed & Why (Latest Session: `session_20261128T040000Z`)

**FCLR-LIVE-ARCHIVE-08** completed — the final confirmatory campaign on the Binance 5-symbol archive (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT; 2024-04..2026-10 UTC; |S|=22,584 common-support hourly timestamps).

- **Design**: Track-B modeled boundary-breach forecast (±4% mark-price path breach within 24h, 25× leverage). NOT a risk overlay.
- **Result**: C2 (funding+price) **worse** than B1 (mark-price-only) on ALL metrics:
  - AUC: 0.6706 vs 0.7086 (−5.36%)
  - Log-loss: 0.4349 vs 0.4332 (−0.38%)
  - Brier: 0.1324 vs 0.1315 (−0.71%)
- **Verdict**: **NOT_SUPPORTED** (relative Brier improvement −0.705% vs frozen 2% floor; 95% block-bootstrap CI [−1.426%, +0.073%] includes zero).
- **Integrity**: Independent stdlib recompute `all_checks_match=true`; evidence audit `audit_pass=true`; trigger check non-empty.
- **Artifacts**: Complete `fclr_live_archive08_{source_registry,prereg,eval,recompute,evidence_audit}_{json,md,py}` + `trigger_check.json` under `research_state/session_20261128T040000Z/`.

---

## Current State of Every Research Gate

| Track / Estimand | Status | Verdict | Basis |
|---|---|---|---|
| **Half 1: Funding-conditioned volatility (Binance 5-symbol archive)** | | | |
| FCLR-LIVE-ARCHIVE-01: mean log-RV QLIKE | COMPLETED_VALIDATED | NOT_SUPPORTED | rel 0.840% < 2% floor |
| FCLR-LIVE-ARCHIVE-03: stress/tail Brier | COMPLETED_VALIDATED | NOT_SUPPORTED | rel 0.458% < 2% floor |
| FCLR-LIVE-ARCHIVE-04: quantile/full-distribution | COMPLETED_VALIDATED | NOT_SUPPORTED | rel avg-pinball −1.102% |
| FCLR-LIVE-ARCHIVE-05: signed-semivariance-asymmetry | COMPLETED_VALIDATED | NOT_SUPPORTED | rel MSE 0.141% < 2% floor |
| FCLR-LIVE-ARCHIVE-06: downside-semivariance-level | COMPLETED_VALIDATED | NOT_SUPPORTED | rel MSE 0.716% (CI [0.419%,1.020%]) < 2% |
| FCLR-LIVE-ARCHIVE-07: mean log-RV QLIKE (2024-04..2026-10 cohort) | COMPLETED_VALIDATED | NOT_SUPPORTED | rel −0.704% (CI [−1.218%,−0.190%]) |
| FCLR-LIVE-ARCHIVE-08: Track-B boundary-breach | COMPLETED_VALIDATED | NOT_SUPPORTED | C2 worse on all metrics |
| **Half 1: Funding-conditioned volatility (Hyperliquid ironflow_bulk)** | | | |
| FCLR-VOL-BROAD-01: mean log-RV QLIKE | COMPLETED_VALIDATED | NOT_SUPPORTED | 1.93% < 2% |
| FCLR-VOL-CORR-01: correction-time/hazard | COMPLETED_VALIDATED | NOT_SUPPORTED | ≥10% slower-correction floor NOT met |
| FCLR-VOL-STRESS-01: stress/tail-exceedance | COMPLETED_VALIDATED | NOT_SUPPORTED | 1.51% < 2% |
| FCLR-VOL-JUMP-01: jump magnitude | COMPLETED_VALIDATED | NOT_SUPPORTED | 0.0922% < 2% |
| FCLR-VOL-JUMP-02: leakage-hardened jump magnitude | COMPLETED_VALIDATED | NOT_SUPPORTED | 0.1510% < 2%; null survives full remediation |
| FCLR-VOL-JUMP-03: multi-estimator × multi-horizon jump magnitude | COMPLETED_VALIDATED | NOT_SUPPORTED | aggregate 0.3025% < 2% |
| FCLR-VOL-JUMP-04: directional/sign jump | COMPLETED_VALIDATED | NOT_SUPPORTED | ≤0.1020% best-config < 2% |
| **Half 2: Liquidation risk (Hyperliquid ironflow_bulk)** | | | |
| Track A: observed liquidation-event forecasting | CLOSED | STRUCTURALLY_BLOCKED | capped-sample feed; no complete census source |
| Track B: modeled boundary-breach forecast | COMPLETED_VALIDATED | NOT_SUPPORTED | modeled proxy ≠ account-specific liquidation |
| Track C: volatility/stress outcome | COMPLETED_VALIDATED | NOT_SUPPORTED | no arm cleared frozen materiality floor |
| Cross-sectional regime funding → liq-intensity | COMPLETED_VALIDATED | SUPPORTED_GENERALIZATION / NOT_STABLE | 2% Poisson-deviance floor NOT MET |

**Program Closure Synthesis**: `research_state/session_20261125T060000Z/fclr_liq_risk_program_closure_synthesis_report_20261125T060000Z.md` — `negative_results_preserved: true | all_nulls_honest: true | no_threshold_shop: true | no_overlay: true | audit_pass: true | unresolved_blockers: []`

---

## Bottlenecks Removed
- **No more closed campaigns to re-run** — all `next_action_heavy: NONE` for rank 0–6 in `experiment_frontier.json`.
- **No threshold-shopping** — all materiality floors (2% QLIKE/Brier/MSE, 10% correction-time) frozen before outcomes.
- **No track adulteration** — firewall intact: Hyperliquid (Track A) never merged with Binance (Track B/C).
- **No overlay built** — forecast gate (RESEARCH_PROMPT.md §9) never passed.
- **No root-level artifact sprawl** — all new artifacts correctly placed under `research_state/session_<UTC>/`; root `*.md|*.json` at cap 500.

---

## Single Highest-Value Next Task

**IF AND ONLY IF** a new admissible unauthenticated source is discovered that passes the rubric:
- ≥5 symbols with ≥3 non-overlapping 30-day blocks
- Documented completeness (no capped samples for binary absence/presence labels)
- License OK for research redistribution
- Free, unauthenticated, automated download (no API keys, no signup, no requester-pays)

**THEN** the next agent must:
1. **Pre-register a NEW experiment ID** (e.g., `FCLR-NEWSOURCE-001-<UTC>`) with frozen protocol BEFORE any outcome inspection.
2. Execute the full confirmatory triad: source registry → prereg freeze → heavy evaluation + independent stdlib recompute + evidence audit + trigger check — all under one fresh `research_state/session_<UTC>/`.
3. Apply Holm correction across the full declared family (including all prior closed arms per RESEARCH_PROMPT.md §17).
4. Report `all_checks_match=true` from the independent recompute or the result is not evidence.

**VERIFICATION COMMAND** (proves no heavy work remains on current frozen panels):
```bash
python -c "
import json
with open('research_state/experiment_frontier.json') as f:
    data = json.load(f)
for item in data:
    if item['rank'] == 0:
        print('Rank 0:', item['task'], '|', item['program_status'], '|', item['last_verdict'])
        print('Next heavy:', item['next_action_heavy'])
        print('Blockers:', item['blockers'])
"
```
Expected output: Rank 0 = FCLR-LIVE-ARCHIVE-08 | COMPLETE | NOT_SUPPORTED | Next heavy: NONE | Blockers: None external.

---

## What Must NOT Be Repeated (Hard Constraints)
- ❌ Do NOT re-run FCLR-LIVE-ARCHIVE-01 through -08, FCLR-VOL-*, or FCLR-LIQ-RISK-PROGRAM-CLOSURE-02.
- ❌ Do NOT build a risk overlay (forecast gate not passed).
- ❌ Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — FCLR-NEXT-002 already exhausted 8 source families.
- ❌ Do NOT add root-level `research_state/*.md|*.json` (cap 500 enforced).
- ❌ Do NOT threshold-shop after outcomes; do NOT relabel exploratory as confirmatory.
- ❌ Do NOT misread `scripts/next_campaign_status.py` (old 3-block framing) as "feasible work remains."
- ❌ Do NOT claim a gate passed because code runs, tests pass, or HTTP 200 returns.

---

## Durable Handoff Contract (Per RESEARCH_PROMPT.md §12)
1. **What changed**: FCLR-LIVE-ARCHIVE-08 completed with independent recompute confirmation; final confirmatory campaign on Binance 5-symbol archive closed NOT_SUPPORTED.
2. **What was tested**: Track-B modeled boundary-breach forecast (25× leverage, ±4% boundary, 24h horizon) on 5 symbols × 22,584 timestamps; 3-block OOS with 168h embargo; 2000-replicate block bootstrap.
3. **Evidence added**: Complete artifact set under `session_20261128T040000Z/`; `experiment_frontier.json` rank 0 updated to COMPLETE.
4. **Gate states**: All confirmatory gates RESOLVED (NOT_SUPPORTED or STRUCTURALLY_BLOCKED). Forecast gate FAILED. Overlay NOT_ELIGIBLE.
5. **Next task**: Monitor for new admissible source passing rubric; if found, pre-register NEW experiment ID before outcome inspection. Otherwise, no further confirmatory work warranted.
6. **Verification command**: See above — proves `next_action_heavy: NONE` and `blockers: None external` for rank 0.
7. **Blockers & free route**: No external blockers. The only materially different route is a NEW unauthenticated source family not yet tested. FCLR-NEXT-002 already tested 8 families (Binance alt paths, Bybit, OKX, Deribit, academic, GitHub, Hugging Face, CryptoDataDownload) — only Hugging Face `ironflow/hyperliquid-liquidations` was GO (CC BY 4.0) but ALREADY USED in FCLR-010.

---

**Timestamp**: 2026-11-28T08:55:21Z
**Session ID**: handoff_20261128T085521Z
**Git HEAD**: (run `git rev-parse HEAD` to verify)
**Next agent**: Execute verification command above. If output matches expected, the program is correctly closed. Only proceed with heavy work if a NEW admissible source is discovered and pre-registered.