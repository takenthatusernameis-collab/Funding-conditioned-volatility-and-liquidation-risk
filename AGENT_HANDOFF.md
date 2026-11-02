# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T03:21:57Z
**INITIAL TASK (NEXT SESSION):** NO FURTHER CONFIRMATORY WORK IS POSSIBLE WITHOUT NEW ADMISSIBLE UNAUTHENTICATED DATA. The repository is at a stable closeout point. If a new admissible liquidation/funding source appears (or SSRN H002 becomes accessible), the next session must: (1) probe it against the GO rubric in research_state/next_data_discovery_plan.md, (2) if GO, pre-register a new experiment ID BEFORE any outcome inspection, (3) freeze splits with frozen_before_outcomes=true, (4) execute, (5) update AGENT_HANDOFF.md and experiment_frontier.json. Otherwise, STOP — do not reopen closed tracks, do not re-run sealed experiments, do not write blocker memos and wait.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk (name is directive). All admissible work is now exhausted. Priority order was: Track A (observed liquidations, FCLR-010 PASSED + overlay executed) > Track C (volatility, NOT_SUPPORTED) > Track B (modeled boundary breaches, CLOSED_NEGATIVE). H002 permanently blocked.
**BRANCH/HEAD:** main @ a03d9a63ea2b828f1c0c30c76ca3ff83ef6e4c87
**HANDOFF ID:** FCLR-HANDOFF-082-20261102T032157Z
**SUPERSEDES:** FCLR-HANDOFF-081-20261102T031359Z

## BOTTLENECKS REMOVED (this session)
- **CAMPAIGN FCLR-HEAVY-001 COMPLETED:** All 6 steps executed with artifacts. Steps 1-5 were already done at handoff entry; Step 6 (integrity lock-in) was genuinely incomplete and has now been finished.
- **Integrity defect repaired:** All six FCLR-HEAVY-001 markdown files contained a literal unexpanded `$(date -u +%Y-%m-%dT%H:%M:%SZ)` placeholder instead of a real UTC timestamp. Substituted with 2026-11-02T03:21:57Z. Analytical content unaffected.
- **Sealed artifacts verified untouched:** All five FCLR-010 sealed files share identical mtime 2026-11-01T23:02:50Z. SHA-256 digests recorded in research_state/fclr_heavy001_integrity.md and experiment_frontier.json.
- **Tests:** 27/27 PASS at HEAD a03d9a63.
- **No dead-ends left open:** Track A deepening exhausted. Track B/C closed. H002 blocked. FCLR-NEXT-002 COMPLETE_NO-GO. No parallel discovery loops remain.

## STATUS (CURRENT — FINAL CLOSEOUT)
- Track A (FCLR-010): GATE PASSED on Hyperliquid ironflow census (199 perps, Nov 2025–Oct 2026, 12 blocks). C2 vs B1 Brier rel -2.21%, CI [-0.004892,-0.001263] excludes zero. Overlay FCLR-OVERLAY-001 executed (HYPOTHETICAL ONLY). Splits frozen 2026-11-01T05:39:07Z.
- FCLR-HEAVY-001: ALL 6 STEPS COMPLETE. Funding-liquidity coupling, regime stratification, lead/lag & censoring, funding ablation, cross-symbol concentration, integrity lock-in. All outputs hypothetical-only.
- Track C (H001): NOT_SUPPORTED — CONFIRMATORY CLOSED.
- Track B (H003): CLOSED_NEGATIVE (extended grid no robust skill).
- H002: PERMANENT BLOCK (SSRN HTTP 403).
- FCLR-LIQMICRO-002/003 COMPLETE. FCLR-NEXT-002 COMPLETE_NO-GO. No new admissible unauthenticated liquidation source found.

## FINAL STATE
All confirmatory gates resolved. Stable closeout point. No further confirmatory work is possible without NEW admissible unauthenticated data meeting the GO rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK) or SSRN H002 methodology access.

## HARD CONSTRAINTS (PERSIST)
- NO Binance merge. NO reopening H001/FCLR-003/FCLR-008/FCLR-010 without trigger + pre-registration + split freeze.
- ALL 27 tests MUST PASS. NO changes to `.github/workflows/`.
- Only admissible: ironflow Hyperliquid liquidations + Hyperliquid fundingHistory API.
- Never silently zero missing funding — drop/flag with justification.
- Sealed artifacts unchanged. Track A/B/C never merged; modeled != observed.
- No risk-overlay promotion beyond hypothetical.
- Do not write another blocker memo and wait if there is no new admissible data route.

## SINGLE HIGHEST-VALUE NEXT TASK
**NONE — repository at stable closeout.** The only materially different route is a NEW admissible unauthenticated liquidation/funding source (or SSRN H002 access). If one appears: probe → pre-register before outcome inspection → freeze splits → execute → handoff. Otherwise stop.