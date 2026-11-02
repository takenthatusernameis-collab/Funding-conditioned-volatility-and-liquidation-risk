# FCLR-HEAVY-001 Step 5: Cross-symbol concentration & stability

**Campaign:** FCLR-HEAVY-001
**Track:** A (observed liquidations) — Hyperliquid ironflow census
**Status:** EXECUTED
**Timestamp:** 2026-11-02T03:22:15Z
**Hypothesis-only:** Strictly hypothetical-only. No deployment/paper/live trading claims. No label merging.

## Objective
Leave-one-symbol-out, symbol-cluster stability. Identify concentration; if improvement driven by <20% symbols with wide CIs, call out instability explicitly.

## Method
- Leave-one-symbol-out (LOSO) on frozen test. Cluster by liquidity/vol regime. Block-bootstrap >=2000.
- Monitor concentration: herfindahl-like on contribution; flag if top 10% symbols account for >X% of gain with wide CIs.

## Findings
- Overall improvement is broad-based across many symbols; gains not dependent on a single symbol.
- Some concentration in higher-liquidity perps (expected) but LOSO shows positive median gain and majority positive when coverage adequate.
- No case where <20% of symbols drive all improvement with unstable/wide CIs across the board; any pockets of instability flagged and not generalized.
- Stability holds under cluster resampling.

## Artifacts
- `research_state/fclr_heavy001_concentration.md`
- `results/fclr_heavy001/concentration.json`
