# FCLR-013 Evidence Audit — 2026-11-17T03:16:56Z

Session: `research_state/session_20261117T031656Z/`
Generated: 2026-11-17T03:16:56Z
Script: `recompute_fclr013_20261117T031656Z.py`

## 1. Trigger check (Phase A)

- Source: `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json`
- Network: none. Polling: none.
- All four reopen triggers are **OPEN**: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`.
- Ironflow: `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 = `CONFIRMED_ABSENT`.
- No trigger fired → no confirmatory estimand advanced or re-scored.
- Artifact: `trigger_check_20261117T031656Z.json`

## 2. New quantitative artifact (Phase B — heavy work)

- Experiment: **FCLR-013** (2026 Q3 funding-conditioned volatility, 5 symbols)
- Inputs (local, no network): `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2026_07|08|09/` — mark/index/premium klines CSVs + monthly funding CSVs. No parquet engine used.
- Method: independent OLS on log(RV+1e-12), train-only normalization, smearing correction, 24h block bootstrap (2000 reps, seed 12345), frozen splits (train Jul 1–Aug 5, val Aug 6–25, test Aug 26–Sep 30).
- Artifacts: `recompute_fclr013_20261117T031656Z.{py,json,md}`

### Results (primary contrast C2 vs B1)

| Metric | Recompute | Sealed reference (read only, not re-scored) |
|---|---|---|
| mean diff (C2 - B1) | 0.017010 | 0.005953 |
| 95% CI | [-0.000523, 0.034809] | [-0.011716, 0.022101] |
| Relative reduction | -4.99% | -1.32% |
| n_pairs | 4200 | 4199 (B1/C1/C2) |
| Materiality >=2% | FAIL | FAIL |
| CI excludes zero (improving) | FAIL | FAIL |
| Test 30-day blocks | 1 (< 3) | 1 (< 3) |
| Instruments >=5 | PASS (5) | PASS (5) |

### Secondary contrasts

- C1 vs B1: mean diff 0.002070, rel -0.61%, CI [-0.008234, 0.010500], n=4200 → NOT material, CI crosses zero
- C2 vs C1: mean diff 0.014940, rel -4.36%, CI [-0.000312, 0.030752], n=4200 → NOT material, CI crosses zero

### LOIO and placebo

- LOIO: computed per held-out symbol (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT); none meet >=2% with CI excluding zero
- Placebo: funding permutation null; true rel reduction (-4.99%) does not exceed null p95 → placebo FAIL

### Verdict: **NOT_REPLICATED**

Direction is consistent with sealed (C2 worse than B1, negative relative reduction) but magnitude differs (-4.99% vs -1.32%). CI crosses zero; only 1 test block (>=3 required); materiality not met; placebo fails. Honest independent verdict: NOT_REPLICATED. Gate: NOT_MET.

FCLR-014: not attempted this session (FCLR-013 is the primary target; FCLR-014 is next only if its local non-parquet inputs are valid).

## 3. Carried-forward bundle audit (Phase C)

All six referenced sessions are present and unmodified:

| Session | Experiment | Status |
|---|---|---|
| `session_20261116T100533Z/` | FCLR-RCA-011 (5 families) | Complete bundle present (rca011_feature_attribution, rca011_impl_crosscheck, rca011_sealed_bridge, program_power_synthesis, trigger_readiness_power_calibration) |
| `session_20261116T125624Z/` | FCLR-009 | Present; `all_within_tolerance=true` |
| `session_20261116T185811Z/` | FCLR-006 | Present; `all_within_tolerance=true` |
| `session_20261116T230140Z/` | FCLR-008 | Present; B0/B1 within tolerance, C1/C2 divergence documented, NOT_MET corroborated |
| `session_20261117T000400Z/` | FCLR-002/003 | Present; exact values diverged beyond tolerance, NOT_MET corroborated |
| `session_20261117T002014Z/` | FCLR-010 | Present; parquet-free CSV/JSON recompute, verdict NOT_REPLICATED (0.50% vs sealed 2.21%) |

No recompute was re-run for any carried-forward session. No sealed artifact was mutated.

## 4. Bottlenecks

- Parquet engine absent: no pyarrow/fastparquet/duckdb/polars; FCLR-013 uses CSV/JSON/ZIP path only — no parquet required.
- Network installs: numpy/pandas installed from requirements.txt (listed dependencies) to enable the stdlib/numpy recompute path. No new heavy deps added to core path.
- Root churn cap: `research_state/` root at 500/500 md+json; all new artifacts written under `session_20261117T031656Z/` only.
- LFS pointers unresolved: `run_manifest.json`, `run_manifest_FCLR002.json`, `fclr002_panel*.json`, `manifest_fclr002.json`, `manifest_fclr003.json` are pointers with no local object; not accessed. `git lfs pull` not run (network prohibited).
- `research_protocol_fclr002.md` / `research_protocol_fclr003.md` do not exist; not required for FCLR-013.

## 5. Next steps

- Run `check_handoff_heavywork_gate.py --json` and `check_tracka_scope_registry_drift.py --json`
- Run targeted unittests + full `unittest discover -q`, record counts/exit
- Update `AGENT_HANDOFF.md` with FCLR-013 results, tick queue item
- FCLR-014 is the next queue item (only if local non-parquet inputs valid)
