# Agent Handoff — 2026-11-14T19:16:15Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

## Current State: COMPLETED_VALIDATED (exploratory) — no agent-removable heavy work
- Rank 0: `FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z` — **COMPLETED_VALIDATED**
- Verdict: **EXPLORATORY_NULL** (`promotable=false`, `max_status=EXPLORATORY_ONLY`, Gate 4 Binance v5 terms `EXTERNAL_BLOCKED`; no RESOLVED_VERIFIED trigger). Do **not** claim confirmatory/promotion for H1.

## This session (executed, heavy)
- Verified no `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` trigger.
- Implemented `scripts/fclr_fwd_vol_2025_disjoint_cross.py` (per-block train windows from frozen prereg, FCLR-011 model set/QLIKE/contrasts, 2000-rep day-block bootstrap, Holm family, LOIO, funding-permutation placebo, leakage audit; exploratory verdicts only).
- Ran `--smoke` (1 symbol, block 0) and full 3-block evaluation (5 symbols, 3 blocks, 10,800 paired rows, 90 days).
- Emitted:
  - `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet`
  - `research_state/tracka_fwd_vol_2025_disjoint_cross_build_report_20261114T191615Z.json` (sha256 `de0ca73e7d092a20...`)
  - `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json`
  - `research_state/evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.md`
- `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`: **PASS** (17 checks).
- Updated `research_state/experiment_frontier.json` rank 0 -> COMPLETED_VALIDATED; updated `tests/test_next_campaign_status.py` to reflect executed campaign.

## Result summary (primary C2 vs B1, 24h QLIKE, pooled 3 blocks)
- mean diff (C2-B1): **+0.006923** (C2 worse), 95% CI **[-0.012604, 0.028030]** crosses 0
- relative reduction: **-1.963%**, p_boot **0.535**, Holm p (primary) **1.0**, n=10800, days=90
- Checks: materiality_ge_2pct **false**, ci_excludes_zero_improving **false**, instruments_ge_5 **true**, blocks_ge_3 **true**, loio_ge_4_of_5 **false**, placebo_pass **true**, holm_pass **false**, leakage_audit_pass **true**
- Per-block train/test rows: b0 2760/3600 (2025-04-25..05-24 -> 2025-06), b1 3432/3600 (2025-09-25..10-24 -> 2025-11), b2 3552/3600 (2025-10-25..11-23 -> 2025-12)
- Interpretation: sealed FCLR-011 does **not** transport to these three disjoint 2025 blocks (exploratory null; no promotion).

## Initial Task for Next Agentic Session (2026-11-14T19:16:15Z) — durable handoff
**Status: TRIGGER-ONLY / NO agent-removable heavy work on cached admissible Binance data.** Do not poll. Do not produce status-only output. Do not re-run tested/exhausted windows (incl. 2024-06/2025-06/2025-11/2025-12 disjoint blocks now tested, 2024-07-23..2024-09-30, 2025-02-01..2025-05-31, 2025-07-23..2025-10-15, 2026-01-01..2026-04-01, 2026-05-01..2026-08-31, 2026-08-03..2026-10-31, 2026-01-18..2026-04-30). Do not re-open sealed FCLR-011/012-V/013/014 artifacts.

### Deterministic check (<30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py | tail -20
ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"
python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
```
If still `NO_VALID_GATE4_TRIGGER` and no new admissible trigger, **do not loop**: record bounded NO_GO only if you must touch state; otherwise preserve evidence.

### Resume triggers (act only on a material trigger, with NEW experiment ID / frozen prereg pre-outcomes as required)
1. **GATE4_BRANCH_1** — valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation -> follow Gate 4 confirmatory flow (do not treat disjoint cross as confirmatory).
2. **NEW_OBSERVED_LIQUIDATION_SOURCE** — materially new candidate -> §16 admissibility audit artifact BEFORE prereg/outcomes -> if ADMISSIBLE freeze prereg pre-outcomes -> build/eval/verdict -> atomic registry/frontier updates under NEW experiment ID.
3. **HL_LABEL_EXTENSION** — Hyperliquid >=100d depth AND verified post-2026-10-31 observed labels -> bounded reprobe only.
4. **EXPANSION_ROBUSTNESS_REDO** — cached-panel robustness with NEW frozen prereg pre-outcomes (no sealed verdict mutation).

## Hard stops
- No polling for Gate 4. No network discovery without a materially new angle and admissibility audit. No raw cache commits. No `.github/workflows/*` edits.
- Every session ends with committed/state-updated work OR a bounded NO_GO + exact evidence.
