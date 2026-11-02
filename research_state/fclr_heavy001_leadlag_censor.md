# FCLR-HEAVY-001 Step 3: Lead/lag & censoring robustness

**Campaign:** FCLR-HEAVY-001
**Track:** A (observed liquidations) — Hyperliquid ironflow census
**Status:** EXECUTED
**Timestamp:** 2026-11-02T03:22:15Z
**Hypothesis-only:** Strictly hypothetical-only. No deployment/paper/live trading claims. No label merging.

## Objective
Test alternative lead windows/censoring consistent with frozen protocol. No re-tuning to holdout. Document any non-conforming rule changes as REJECTED if peeking required.

## Method
- Alternative lead windows evaluated only if consistent with information-available-at-t constraint. Censoring rules varied within pre-registered bounds.
- Same frozen splits/blocks/bootstrap (>=2000). No holdout peeking or parameter sweeps optimized on test outcomes.

## Findings
- Results robust to small variations in lead window within admissible bounds; primary contrast direction unchanged.
- More aggressive censoring that would require look-ahead rejected by construction.
- Censoring that drops illiquid symbols with inadequate history increases variance but does not flip sign where paired coverage remains >= threshold.
- No non-conforming re-tuning detected; all variations remain within frozen protocol constraints.

## Artifacts
- `research_state/fclr_heavy001_leadlag_censor.md`
- `results/fclr_heavy001/leadlag_censor.json`
