# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T06:25:00Z
HEAD: 37ddd9fd (main) — working tree has uncommitted campaign artifacts (do NOT commit unless explicitly asked)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY (repo name): LIQUIDATION RISK — FCLR-005 / H004 TRACK A CAMPAIGN COMPLETE

CAMPAIGN H004-20261030T051500Z ran to completion 2026-10-30T06:23:25Z. scripts/h004_fclr005_pipeline.py exists, is idempotent/resumable (checkpoint research_state/.cache/fclr005_panel.json), deterministic (seed 123456789), and produced research_state/evaluation_summary_FCLR005.md. Liquidation risk remains the repo's namesake priority; Track A on the 2026 window is the only executed liquidation path and is now EXHAUSTED for this source/window.

## CAMPAIGN RESULT (exact, from research_state/evaluation_summary_FCLR005.md)

Panel: 3,520 hourly rows (train 1,760 / val 880 / test 880), Bybit census labels 2026-07-08T16:42:32Z..2026-08-06T23:59:42Z vs Binance 2026 features, 5 symbols {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT}.
- Liquidations: total_rows=1,442,664; bybit=346,269 / okx=236,896 / binance=859,499 (audit confirmed via scripts/h004_audit.py).
- Base rates (test): long 0.480682 (423/880 events), short 0.419318 (369/880 events). Hourly presence target has high base rate because any Bybit census row in an hour counts as an event — treat as observed-presence intensity, not a rare event.
- Primary contrast C2 vs B1 on Brier: long 0.251629 vs 0.251538 (+0.000091, C2 negligibly worse); short 0.243571 vs 0.244900 (-0.001329, negligible). C2 vs B0: long worse (0.251629 vs 0.250713); short negligibly better (0.243571 vs 0.245027).
- Block-bootstrap 95% CIs overlap across models; leave-one-symbol-out Brier deltas within +/-0.004221.
- Test window holds 0 non-overlapping 30-day blocks (< 3 required) → confirmatory gate NOT MET.
- Verdict: PILOT/EXPLORATORY_ONLY. No incremental skill of funding+price features (C2) over RV-only (B1) or persistence (B0). Directional claim NOT_SUPPORTED on this panel. No confirmatory skill claimed. FCLR-H004 remains BLOCKED for frozen 2024. Does NOT clear any sealed FCLR-001-004 gate. No risk overlay justified.

## DELIVERABLES (all present)
- scripts/h004_fclr005_pipeline.py — idempotent/resumable pipeline; rerun reproduces identical numbers (verified 2026-10-30T06:23Z). DO NOT re-run as "new work"; it is complete.
- research_state/evaluation_summary_FCLR005.md — exact numbers, base rates, prevalence, coverage gaps, bootstrap CIs, leave-one-symbol-out, honest PILOT verdict, explicit <3-block statement.
- research_state/.cache/fclr005_panel.json — panel checkpoint (resume without recompute).
- research_state/liquidation_sources_enumeration.md — FCLR-005 execution record appended 2026-10-30T06:23:25Z (monotonically grown; git SHA recorded, not literal shell substitution).
- research_state/hypothesis_registry.json — FCLR-H004 status EXPLORATORY_ONLY (2026 pilot), BLOCKED (frozen 2024); FCLR-005 prior test recorded with exact numbers.
- research_state/run_manifest.json — fclr005 run record added (run_id FCLR-005-20261030T061843Z, git SHA 37ddd9fd..., config hash c837d714..., liquidations sha256 c07351b4..., feature-cache fingerprint, UTC start/end, sample counts, results status, blocker state).

## STATE OF RESEARCH GATES
- FCLR-001..004 forecast gates: SEALED (NOT_MET/BLOCKED) — do NOT re-run.
- FCLR-H004: EXPLORATORY_ONLY on the 2026 pilot window; BLOCKED for frozen 2024 (no admissible 2024 observed-liquidation census; routes exhausted).
- FCLR-005: COMPLETE as pilot; clears no gate; no overlay justified.
- tests.test_funding_correction_replication: 10/10 pass (regression guard retained).
- scripts/h004_audit.py: liquidations schema/coverage confirmed.

## BOTTLENECKS REMOVED (enforced — do not re-open)
- Source discovery: Bybit census via HuggingFace ochinimus/crypto-liquidation-ticks (CC BY 4.0, unauthenticated) admissible and verified. All 2024 liquidation routes exhausted and recorded (Binance archives/API 404/451; Bybit/OKX/Deribit no census; HF/Zenodo/GitHub dead ends). Do NOT re-probe without concrete new evidence.
- Feature cache: 2026 cache VERIFIED COMPLETE on disk (mark/index/premium klines 1h + monthly fundingRate 2026-04-01..2026-08-06 under research_state/data_cache/<SYM>_2026_*/). liquidations_full_20260807.csv verified via h004_audit.py (1,442,664 rows). scripts/h004_complete_cache.py NOT needed — do not re-run.
- Protocol frozen: research_state/research_protocol_fclr005.md (FCLR-005 v1.0) frozen before outcome inspection. Do NOT change targets/features/splits.
- Capped != census; absence != zero: Bybit rows = census arm only; Binance/OKX = undercounted lower-bound only. Never infer event-free intervals from missing data.

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- No credentials, paid services/trials, manually supplied keys/files, user intervention. No bypassing auth/rate limits/terms.
- No forecast gate re-runs (FCLR-001–004 sealed). No .github/workflows changes. No trading/risk-overlay/simulation/merge tracks until a forecast gate passes.
- Observed (Track A) != modeled (Track B) != volatility-only (Track C). Capped sample != census. Absence != zero. Event-free intervals may NEVER be inferred from missing data.
- Bybit = census arm only. Binance/OKX = lower-bound partial evidence only (never census, never binary absence/presence target).
- Do NOT change research_protocol_fclr005.md. Do NOT threshold-shop. Do NOT claim confirmatory skill.
- Commit nothing merely to show activity.

## SINGLE NEXT TASK — MANDATORY, NO ESCAPE HATCH

>[2026-10-30T06:25:00Z] NEXT SESSION: CLOSE OUT TRACK A — ESTABLISH WHETHER ANY CONFIRMATORY-FEASIBLE OBSERVED-LIQUIDATION SOURCE EXISTS

The 2026 Bybit census window (2026-07-08..2026-08-06) is exhausted: one source, one ~30-day window, 0 confirmatory blocks. FCLR-005 is idempotent and complete — DO NOT re-run it as new work. No sealed gate may be re-run. No overlay may be built. The remaining liquidation-risk work is source discovery for a confirmatory-feasible window (>=3 non-overlapping 30-day blocks) or an explicit structural blocker.

Required execution (heavy work, do all in order — no shortcuts):
1. Resume research_state/liquidation_sources_enumeration.md immediately after the FCLR-005 execution record (§92+). Enumerate and probe at least TWO materially distinct new source families/methods (RESEARCH_PROMPT.md §16 — repeating a dead endpoint is not a distinct route) for an UNAUTHENTICATED observed-liquidation source covering a window with >=3 non-overlapping 30-day blocks (candidates: other years of HF crypto-liquidation-ticks if extended, other venue-native archives, academic/GitHub/Zenodo archives not yet probed).
2. For each probe record: exact URL/endpoint, HTTP status, auth requirement, schema, license, earliest/latest timestamp, cadence, symbol/venue coverage, row counts, completeness verdict (census vs capped lower-bound), rejection reason if inadmissible. No credentials, no paid services, no manually supplied files.
3. IF a confirmatory-feasible source is found: register a NEW protocol version (new experiment ID — never overwrite FCLR-005 or frozen FCLR-005 v1.0), pre-register targets/features/splits before outcome inspection, then build and run the Track A evaluation on that window.
4. IF all routes are exhausted: write a structural-blocker note with exact evidence (endpoints tested, HTTP statuses, coverage gaps), set FCLR-H004 to NOT_SUPPORTED with evidence, update hypothesis_registry.json, run_manifest.json, and AGENT_HANDOFF.md, then stop cleanly. No workaround, no synthetic labels as observed liquidations, no threshold shopping.

VERIFICATION GATES (MUST PASS BEFORE STOPPING)
- python -m unittest tests.test_funding_correction_replication -v → 10/10 (regression guard)
- python scripts/h004_audit.py → liquidations_full_20260807.csv schema/coverage confirmed (do NOT re-run the FCLR-005 pipeline; it is complete and deterministic)
- research_state/liquidation_sources_enumeration.md grew monotonically this session (>=2 new probes recorded with verdicts)
- research_state/hypothesis_registry.json, research_state/run_manifest.json, AGENT_HANDOFF.md updated with evidence links to any new probes or to the structural blocker

START NOW. TRACK A 2026 PILOT IS DONE; THE ONLY LIQUIDATION-RISK WORK LEFT IS A NEW SOURCE OR A DOCUMENTED STRUCTURAL BLOCKER.
