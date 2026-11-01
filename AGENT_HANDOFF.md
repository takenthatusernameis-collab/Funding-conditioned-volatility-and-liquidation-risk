# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T22:25:00Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility and liquidation risk. Primary volatility hypothesis H001 NOT_SUPPORTED (FCLR-003 gate NOT_MET). Track A liquidation forecast (FCLR-010) PASSED on Hyperliquid ironflow data; overlay executed hypothetically. Current liqmicro campaign (FCLR-LIQMICRO-001) ran but funding features are zeroed (no Hyperliquid funding integrated). Bottleneck: funding data not wired for Hyperliquid perps despite repo focus on "funding-conditioned".
**BRANCH/HEAD:** main @ 5cf38b32
**HANDOFF ID:** FCLR-HANDOFF-064-20261101T222500Z
**SUPERSEDES:** FCLR-HANDOFF-063-20261101T221637Z

**STATUS:** Tests 27/27 PASS. Sealed artifacts intact. Working tree has modified __pycache__ and src/analysis/liqmicro/__pycache__ (harmless). Heavy funding-conditioned work required.

## BOTTLENECKS IDENTIFIED (REMOVE THEM)
- **Funding data missing for Hyperliquid**: liqmicro features set funding_rate/sign/abs/zscore to 0.0 because no funding_df passed. Hyperliquid has funding history; need to fetch/integrate public funding data for the same symbols/time range as ironflow liquidations (or use existing cached funding files mapped to symbols). This is blocking proper "funding-conditioned" analysis.
- **Cross-track clarity**: Need to properly test D1-D3 with actual funding variation, not zeros. Current results may be invalid/degenerate.
- **Heavy work needed**: Integration + re-analysis with real funding is compute-heavy and directly matches repo name.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T22:25:00Z
**PRIORITY: P0 | TYPE: HEAVY FUNDING-CONDITIONED RESEARCH | CAMPAIGN: FCLR-LIQMICRO-002 | FIREWALLS ENFORCED**

**MANDATE:** Integrate Hyperliquid funding data properly and re-run funding-conditioned liquidation microstructure with REAL funding variation. Do NOT re-open sealed H001/FCLR-003. Do NOT merge Binance. Use ONLY admissible data.

### CAMPAIGN FCLR-LIQMICRO-002 — EXECUTE IN STRICT ORDER
1. **Sanity** (5 min)
   - `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → must stay 27/27 PASS

2. **Funding data discovery for Hyperliquid** (HEAVY)
   - Find Hyperliquid funding data. Check public sources: Hyperliquid API (unauthenticated), or any cached funding files that can be mapped to Hyperliquid symbols. Hyperliquid perpetual symbols in ironflow are like `BTC-PERP` (native perps).
   - Look in research_state/data_cache for any hyperliquid funding, or check if we need to fetch from api.hyperliquid.xyz (info endpoint for funding history) - but must be unauthenticated and follow constraints.
   - If no existing cached funding matches Hyperliquid symbols, document and try to construct from available sources. Do NOT fabricate.
   - Write audit to `research_state/liqmicro_funding_audit_002.md` with coverage.

3. **Wire funding into pipeline** (IMPLEMENT)
   - Extend `src/analysis/liqmicro/ingest.py` or add `funding_ingest.py` to load Hyperliquid funding aligned to symbol/hour.
   - Fix `features.py::add_funding_features` to actually use funding_df with proper alignment (handle symbol mapping BTC-PERP vs BTCUSDT, timestamps).
   - Ensure no look-ahead, proper timezone handling.

4. **Re-run with real funding** (HEAVY COMPUTATION)
   - Rebuild panel with real funding features (funding_rate, funding_sign, funding_abs, funding_zscore).
   - Re-test D1-D3 with proper funding variation. Regenerate results in `results/liqmicro_v2/` or overwrite with versioned artifacts.
   - Update pre-registration if needed? Or create new one `pre_registration_FCLR-LIQMICRO-002.md` noting it's a fix to funding integration while keeping hypotheses same.
   - Write `research_state/evaluation_summary_FCLR-LIQMICRO-002.md`.

5. **Validate & report**
   - Confirm funding features have variation (std > 0). If still zero after trying all routes, document blocker with evidence and try alternative approaches.
   - All tests must remain 27/27.
   - Explicitly state relation to H001 (no reversal, no re-test).

### MANDATORY VERIFY COMMANDS
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1 && \
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk status --short && \
python -m unittest discover -s tests -v 2>&1 | tail -2
```

## HARD CONSTRAINTS
- NO Binance merge, NO FCLR-003/H001 re-opening
- All 27 tests must PASS
- No .github/workflows changes
- Use only admissible free data
- Do not fabricate data
- Sealed artifacts unchanged except new ones

## REQUIRED END-OF-SESSION OUTPUT
1. Tests + tree status
2. Funding audit path + coverage (symbols with funding, % overlap)
3. Code changes to wire funding
4. New results with funding variation confirmed
5. Updated evaluation summary with D1-D3 verdict
6. Explicit statement re: H001

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** FCLR-LIQMICRO-002 - Integrate real Hyperliquid funding data and re-analyze funding-conditioned liquidations. This is heavy, directly matches repo name, fixes the critical bottleneck.
