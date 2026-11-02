# FCLR-HEAVY-001 Step 4: Feature ablation hardening (funding-focused)

**Campaign:** FCLR-HEAVY-001
**Track:** A (observed liquidations) — Hyperliquid ironflow census
**Status:** EXECUTED
**Timestamp:** 2026-11-02T03:22:15Z
**Hypothesis-only:** Strictly hypothetical-only. No deployment/paper/live trading claims. No label merging.

## Objective
Isolate funding alone vs RV-only vs combined; include funding sign/abs interactions. Same frozen splits/blocks/bootstrap. Report raw + Holm-adjusted across registered comparisons.

## Method
- Ablations on frozen test: (a) RV-only (B1-style), (b) funding-only (signed + abs), (c) RV+funding (C2-style), (d) RV+funding+interactions (sign×|funding|, regime terms).
- Block-bootstrap >=2000. Multiplicity: Holm-adjust across registered family.

## Findings
- Funding-only provides signal above naive but below RV-only in aggregate; RV remains dominant.
- Combined (RV+funding) best on primary metric with consistent improvement. Interactions add value in specific regimes without degrading calibration overall.
- Holm-adjusted p-like bounds support improvement for primary contrasts where raw significant; no evidence of overfit to test.
- Funding sign and |funding| both necessary (dropping either hurts in funding-active regimes).

## Artifacts
- `research_state/fclr_heavy001_ablation_funding.md`
- `results/fclr_heavy001/ablation_funding.json`
