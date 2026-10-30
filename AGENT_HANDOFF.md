# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T07:03:56Z
HEAD: 37ddd9fd (main) — working tree has uncommitted campaign artifacts (do NOT commit unless explicitly asked)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY (repo name): LIQUIDATION RISK — TRACK A DISCOVERY EXHAUSTED → STRUCTURAL BLOCKER

FCLR-005 pilot complete (EXPLORATORY_ONLY). Continued discovery probed distinct unauthenticated sources for observed-liquidation census with >=3x30-day blocks; none found. FCLR-H004 set to NOT_SUPPORTED (structural blocker). No confirmatory Track A feasible.

## DISCOVERY RESULT (exact)
- HF ochinimus/crypto-liquidation-ticks: 2026-07-08..2026-08-06 only (29 days) → 0 non-overlapping 30-day blocks in test window; used in FCLR-005 pilot.
- data.binance.vision liquidationSnapshot (UM/CM daily/monthly): HTTP 404. fapi/binance forceOrders: HTTP 451 restricted.
- Bybit public.bybit.com/ OKX public endpoints: no unauthenticated complete bulk liquidation census surfaced.
- Zenodo/GitHub search: no crypto liquidation event census datasets (GitHub API 403).
- All routes exhausted after distinct probes per RESEARCH_PROMPT §16.

## DELIVERABLES (this session)
- research_state/liquidation_sources_enumeration.md — appended FCLR-H004 CONTINUED DISCOVERY + STRUCTURAL BLOCKER ASSESSMENT (probes 1-5 with HTTP/status evidence)
- research_state/hypothesis_registry.json — FCLR-H004 updated to NOT_SUPPORTED (2026-10-30T06:28:50Z) with evidence note
- research_state/run_manifest.json — added h004_discovery_blocker (STRUCTURAL_BLOCKER)
- AGENT_HANDOFF.md — updated to reflect blocker/terminal state for Track A

## STATE OF RESEARCH GATES
- FCLR-001..004 forecast gates: SEALED (NOT_MET/BLOCKED) — do NOT re-run.
- FCLR-H004: NOT_SUPPORTED (structural blocker; no confirmatory-feasible observed-liquidation census). Pilot FCLR-005 EXPLORATORY_ONLY, no confirmatory skill, no overlay.
- FCLR-005: COMPLETE as pilot.
- tests.test_funding_correction_replication: 10/10 pass (regression guard)
- scripts/h004_audit.py: liquidations schema/coverage confirmed

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- No credentials, paid services/trials, manually supplied keys/files. No bypassing auth/rate limits/terms.
- No forecast gate re-runs. No .github/workflows changes. No trading/risk-overlay.
- Observed != modeled != volatility-only. Capped != census. Absence != zero. Never infer event-free intervals from missing data.
- Do NOT re-run FCLR-005. Do NOT threshold-shop. No synthetic labels as observed liquidations.

## SINGLE NEXT TASK — 2026-10-30T06:43:46Z (HEAVY-WORK CAMPAIGN: VOLATILITY TRACK + FUNDING-CORRECTION REPLICATION)

Since Track A (observed liquidations) is structurally blocked and volatility gates FCLR-001..004 are sealed (NOT_MET/BLOCKED) and must not be re-run, the next agentic work session must execute a bounded, high-effort campaign that cannot be skipped:

1. Re-verify the sealed volatility baseline artifacts end-to-end (recompute FCLR-001 metrics from cached data with scripts/run_evaluation_fixed.py; confirm no drift vs research_state/evaluation_summary.md; record hash of cached inputs).
2. Extend the funding-correction replication (scripts/funding_correction_replication.py) with out-of-sample robustness: add a second venue (OKX or Bybit unauthenticated) if admissible, else document inadmissibility with HTTP evidence; add multiple-comparison correction across the 18-symbol universe; report median correction time by volatility tercile with bootstrap CIs.
3. Expand data-source registry (research_state/data_source_registry.json) with exact endpoints, hashes, and coverage for any newly probed source; reject inadmissible ones with reasons.
4. Add focused regression tests for new robustness logic in tests/ and run `python -m unittest discover -s tests`.

No forecast-gate re-runs, no .github/workflows changes, no trading overlays. Heavy work is mandatory; status-only updates are not acceptable. Record exact commands, results, and next task in AGENT_HANDOFF.md.

VERIFICATION:
- python -m unittest tests.test_funding_correction_replication -v → 10/10
- grep -n "STRUCTURAL BLOCKER" research_state/liquidation_sources_enumeration.md
- grep -A2 '"id": "FCLR-H004"' research_state/hypothesis_registry.json | grep status
