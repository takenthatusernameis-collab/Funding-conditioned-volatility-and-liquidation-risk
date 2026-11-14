# NEXT SESSION TASK — 2026-11-14T08:23:40Z (durable, execution-forcing)

## PRIMARY TASK (MANDATORY, HEAVY, OFFLINE, UNBLOCKED)

**Implement and run `TRACKA-LIQ-EXPANSION-RECOMPUTE` (Phase B of FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z).**

### What to do (exact sequence)
1. **Create** `scripts/fclr_liq_expansion_recompute.py` (NEW FILE, ~600-900 lines). Model after `scripts/fclr011_recompute_audit.py` but for the 8-symbol Hyperliquid liquidation panel.
2. **Freeze prereg** `research_state/prereg_tracka_liq_expansion_recompute_20261114T073346Z.{json,md}` **before any outcome computation** with `status=FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `pre_registered_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`, `promotable=false`, `max_status=EXPLORATORY_ONLY`.
3. **Rebuild panel from caches** (NOT from sealed parquet — that would be circular):
   - Labels: `research_state/data_cache/ironflow_events/2026-05..2026-10.parquet` (1,264,105 rows, observed HL liquidations only)
   - Funding: `research_state/data_cache/hyperliquid_funding/{ZEC,NEAR,UNI,AAVE,CRV,ADA,LTC,BCH}.json` (all 8, 4,416 rows each, 1777593600045..1793487600044)
   - 1h candles: `research_state/data_cache/hyperliquid_candles/{SYM}/2026-05..2026-10.json` (all 8, all 6 months, .accessed.json + .sha256 present)
   - **DO NOT USE** `ironflow_bulk` (stops at 2026-04)
4. **Recompute** B0/B1/C1/C2 with train-only fit/scaling/smearing; evaluate on frozen test window; paired 24h circular block bootstrap (2000 reps, deterministic); Holm over C2_vs_B1, C1_vs_B1, C2_vs_C1; LOIO; funding-permutation placebo; per-symbol/per-block stability; leakage audit.
5. **Emit**:
   - `research_state/tracka_liq_expansion_recompute_panel_<UTC>.parquet`
   - `research_state/tracka_liq_expansion_recompute_panel_build_report_<UTC>.json` (per-coin counts, coverage, label/funding/rv completeness, input SHA-256s)
   - `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-<UTC>.{json,md}` with verdict **REPRODUCED|NOT_REPRODUCED|INCONCLUSIVE|INADMISSIBLE** (all EXPLORATORY_ONLY, promotable=false)
   - **Explicitly state** whether the sealed **19.04% C2-vs-B1**, **LOIO 4/8**, and **placebo failure** (null p95 21.10%) replicate.
6. **Stop rule**: instruments < 5, test blocks < 3, core coverage < 0.80 → bounded INADMISSIBLE/INCONCLUSIVE NO_GO with exact failing minima. **No relaxation after outcomes.**
7. **Add tests** under `tests/` (unittest): prereg frozen-field assertion, panel-hash consistency, non-empty contrasts, sealed-artifact immutability.

### Sealed reference (read-only, do not re-score, do not overwrite)
`research_state/tracka_hl_expansion_eval_result_20261111T202344Z.json`:
- C2_vs_B1: `rel_reduction_pct = 19.0371`, `mean_diff = -2.70974`, `ci = [-5.088102, -0.477660]`, `n_pairs = 593`, `n_blocks = 3`, paired_symbols = `[AAVE, ADA, BCH, CRV, LTC, NEAR, UNI, ZEC]`
- C1_vs_B1: `9.6794%`; C2_vs_C1: `10.3605%`
- Robustness: LOIO 4/8, placebo null p95 `21.10%`
- Sealed panel SHA-256: `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699` (1472 buckets, 1203 with label, 1168 complete)

### Verification (atomically after Phase B completes)
- `/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all` → expect **19/19 PASS**
- `/tmp/fclr-venv/bin/python -m unittest tests.test_active_campaign_gate tests.test_fclr_campaign_gate tests.test_next_campaign_status tests.test_fclr_liq_expansion_recompute_*` (targeted; pytest not installed; full discover exceeds timeout)
- Update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/negative_results_report.md`, `research_state/leakage_audit.md`, append session log to `AGENT_HANDOFF.md`

### Environment (do not rediscover)
- **Use `/tmp/fclr-venv/bin/python`** (only env with pyarrow/pandas/numpy/scipy; system python lacks pyarrow)
- **No network**, **no raw parquet/cache commits**, **no sealed artifact overwrites**, **no fabricated verdicts/thresholds**
- Tests are **unittest** style (see `test_active_campaign_gate.py`)

---

## SECONDARY TASK (ONLY AFTER PHASE B ARTIFACTS/TESTS/GATES ARE DONE, OR IF PHASE B HITS HARD STOP)

**Fix and rerun FCLR-011 recompute (Phase A)** — capped **INCONCLUSIVE/EXPLORATORY**, not promotable.
- **Double-assemble bug**: `fclr011_recompute_audit.py` assembles panel twice (main: MONTHS; run_audit: smoke-narrowed months). Fix: pass built panel/build into `run_audit` or gate `--smoke` on month list.
- **168h design dead-end**: train complete-case rows = 152 (BTC/BNB only) because `log_rv168h` requires 192h warm-up; C1/C2 cannot fit. Two options (pick one, freeze decision before outcomes): **(A1, preferred) Warm-up exclusion** — drop `log_rv168h` from B1 train fit only, re-freeze B1 as `log_rv1h + log_rv24h` (raises train core 152→1218); **(A2) Extend train window** into 2025 (needs BTCUSDT_2025_11/12 + others in cache; verify first).
- Prereg: `prereg_fclr011_recompute_20261114T042139Z.json` (already exists, must re-freeze if design changes with `audit_only=true`, `does_not_reopen_sealed_verdict=true`).

---

## DEFINITION OF DONE FOR THIS SESSION
Phase B implementation + frozen prereg + rebuilt panel + evaluation summary + tests + gate verification committed as artifacts in working tree (or a documented hard stop with exact failing minima and **no false NO_GO**). Any other outcome is **insufficient progress**.

---
*Authoritative handoff: AGENT_HANDOFF.md (2026-11-14T07:33:46Z). This file is a redirect; do not edit — update the handoff instead.*