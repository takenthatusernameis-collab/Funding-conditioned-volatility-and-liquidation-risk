# Evidence Audit — FCLR-002/FCLR-003 Recompute — 20261117T000400Z

## Scope
- Session: `session_20261117T000400Z`.
- Heavy work completed: independent raw-cache recomputation for both FCLR-002 and FCLR-003, not a trigger-only or copied-bundle session.
- Evidence verified present: `session_20261116T100533Z` (five RCA-011 families and power bundle), `session_20261116T125624Z` (FCLR-009), `session_20261116T185811Z` (FCLR-006), and `session_20261116T230140Z` (FCLR-008).

## Trigger check (once, offline)
- `GATE4_BRANCH_1`: OPEN.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: OPEN.
- `HL_LABEL_EXTENSION`: OPEN.
- `EXPANSION_ROBUSTNESS_REDO`: OPEN.
- Ironflow monitor state: `data_through=2026-10`; no new observed post-2026-10 evidence was available. No network request, HuggingFace probe, or LFS fetch was made.

## Method and data integrity
- Inputs: local `research_state/data_cache/{BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT}_2024_01..12/` CSVs and ZIP archives.
- The cache is mixed-format: Apr-Jun mark/premium/index files are ZIP archives, while Jan-Mar and Jul-Nov are decompressed CSVs. The recompute explicitly reads both. This is a material bottleneck: readers that search only `*.csv` silently drop Apr-Jun and make FCLR-002 falsely unevaluable.
- Splits are hardcoded from the frozen summaries in `evaluation_summary_FCLR002.md` and `evaluation_summary_FCLR003.md`; no `run_manifest` or LFS object was read.
- Features: trailing RV1h/RV24h/RV168h, latest signed funding, past-only 90-day absolute-funding percentile, premium, and EMA24 distance. OLS is on `log(y + 1e-12)` with intercept and `1e-12` ridge. QLIKE is canonical `y/yhat - log(y/yhat) - 1`. Bootstrap is deterministic by UTC day with seed 12345.
- This is an independent path from `scripts/run_evaluation.py`; the handoff requires a fresh quantitative artifact, not rerun sealed outputs.

## FCLR-002 result
- `all_within_tolerance`: **false**.
- QLIKE: B0 `0.539499` vs published `0.543471`; B1 `0.484735` vs `0.487438`; C1 `0.485223` vs `0.487455`; C2 `0.443053` vs `0.442223`.
- Counts match the published deterministic row counts: B0 n=8280; B1/C1/C2 n=8274.
- C2 vs B1 recomputed mean diff `-0.041683`, relative reduction `8.60%`, CI `[-0.093389, -0.005759]`, n=8274. Published: `-0.045215`, `9.28%`, CI `[-0.097648, -0.008788]`.
- Interpretation: the qualitative result is directionally corroborated (C2 improves over B1 and the CI excludes zero), but the exact headline is not reproduced within the handoff tolerance. The discrepancy is a finding, not a tuning target. The original gate remains **NOT_MET** because the 70-day test window has only two 30-day blocks.

## FCLR-003 result
- `all_within_tolerance`: **false**.
- QLIKE: B0 `0.486931` vs `0.486931`; B1 `0.400689` vs `0.400689`; C1 `0.392092` vs `0.389589`; C2 `0.448156` vs `0.444702`.
- Counts match: B0 n=10800; B1/C1/C2 n=10796.
- C2 vs B1 recomputed mean diff `0.047467`, relative change `-11.85%`, CI `[0.004045, 0.097614]`, n=10796. Published: `0.044013`, `-10.98%`, CI `[0.001487, 0.093225]`.
- Interpretation: the independent path confirms the terminal qualitative verdict: C2 is worse than B1 and the primary contrast does **NOT_MEET** the 2% improvement gate. Exact C1/C2 values diverge beyond tolerance, so the sealed headline should not be represented as exactly reproduced.

## Gate results captured in this session
- `python3 scripts/check_handoff_heavywork_gate.py --json`: PASS; `latest_session=session_20261116T230140Z` at the time of capture, root 500/500.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: PASS; 196 scripts in registry and scope.
- Targeted suite: 52 tests, OK, EXIT 0.
- Full discovery: 1340 tests, 4 errors, 18 skipped, EXIT 1. All four errors are the documented pre-existing `pyarrow` missing-engine errors in `tests.test_fclr_liq_combined_admissibility_audit`; no new failures were observed.
- A timestamp-only modification to tracked `research_state/ironflow_fastpath_cache.json` was reverted.

## Bottlenecks removed for future sessions
- The previous handoff said raw 2024 CSVs were present, but Apr-Jun files are ZIPs. Future agents must use a ZIP-aware reader or they will reproduce the false `test_n=0` / `None` failure.
- The old handoff made FCLR-003 secondary. This session completed both, so the next session should not repeat either recompute; it should proceed to the next queue item (FCLR-010/013/014) or an admissible trigger.
- The FCLR-002/003 mismatches are now documented as quantitative findings rather than hidden by a copied artifact.

## Current scientific conclusion
All four reopen triggers remain OPEN. No cached-data confirmatory estimand should be rerun. The only productive next work is the remaining independent reproducibility queue or a genuinely new admissible source/design.