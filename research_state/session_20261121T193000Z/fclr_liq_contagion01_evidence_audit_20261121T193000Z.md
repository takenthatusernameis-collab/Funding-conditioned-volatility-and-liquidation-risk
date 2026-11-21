# FCLR-LIQ-CONTAGION-001 — Evidence Audit

**Session:** session_20261121T193000Z
**Experiment ID:** FCLR-LIQ-CONTAGION-001-20261121T193000Z
**Campaign:** FCLR-LIQ-CONTAGION-001 (rank-0)
**Verdict:** NOT_SUPPORTED (overall)

## What this audit ties together

Each verdict below is tied to its concrete artifact on disk under `research_state/session_20261121T193000Z/`:

| Verdict | Artifact | Role |
|---|---|---|
| Prereg freeze (outcome-blind) | `fclr_liq_contagion01_prereg_20261121T193000Z.json` + `.md` | Froze H_contagion_liq, H_contagion_funding, 15x15 directed network (Granger + lead-lag), 1000+ permutations, funding-tercile conditioning, 90-day rolling windows, 2% materiality floor, panel sha256, `outcome_data_inspected_before_freeze=false` |
| Contagion evaluation | `fclr_liq_contagion01_eval_20261121T193000Z.py` + `.json` + `.md` | Hourly aggregation (211,188 coin-observations), 15x15x24 lead-lag, Granger VAR(6) for 210 directed pairs, 1000x210 permutations, funding-tercile splits, volatility spillover, temporal stability |
| Independent recompute | `fclr_liq_contagion01_recompute_20261121T193000Z.py` + `.json` | Independent stdlib/numpy recompute; reports DISCREPANCY vs eval (58 edges density 0.2762 vs 11 edges density 0.0524; 300 permutations vs prereg 1000+). Discrepancy recorded, not suppressed. |
| This evidence audit | `fclr_liq_contagion01_evidence_audit_20261121T193000Z.json` + `.md` | Ties each verdict to its artifacts (this document) |
| Gate-critical audit (literal prefix) | `evidence_audit_20261121T193000Z.json` | Satisfies gate `AUDIT_PREFIX="evidence_audit_"` contagion new-style heavy-session check |
| Trigger check | `trigger_check_20261121T193000Z.json` | Non-empty; records no external trigger required (frozen panel is sole input) |

## Hypothesis verdicts

### H_contagion_liq — SUPPORTED

- 11/210 directed Granger edges significant at Bonferroni-adjusted p < 0.01 (alpha 4.8e-05).
- Final contagion network density 0.0524 >= 2% materiality floor.
- Permutation null rejected for top edges (empirical p = 0).
- Top edges: ETH->LINK (F=105.09), XRP->CRV (F=72.74), SOL->LINK (F=61.36), XRP->LINK (F=59.83), ETH->LTC (F=55.99). Not dominated by a single coin.

### H_contagion_funding — NOT_SUPPORTED

- Funding-tercile monotonicity 38/112 pairs (rate 0.339) below the 0.5 support threshold.
- No >= 2% relative difference between high- and low-funding-differential terciles established.
- Funding-mediated spillover not confirmed.

### Overall — NOT_SUPPORTED

H_contagion_funding fails, so the joint campaign verdict is NOT_SUPPORTED despite H_contagion_liq being SUPPORTED.

## Recompute discrepancy (recorded, not suppressed)

The independent recompute does NOT concur with the primary eval (`recompute_concurs_with_eval=false`, verdict DISCREPANCY). It finds 58 significant edges / density 0.2762 versus the eval's 11 / 0.0524, used 300 permutations (below the preregistered 1000+), and 211,740 hourly coin-observations (eval: 211,188). This methodological sensitivity is disclosed honestly; the primary eval remains the registered analysis.

## Hard constraints honored (all verified)

- `outcome_data_inspected_before_freeze=false` — prereg frozen before any contagion statistic.
- Combined liquidation panel sha256 asserted in eval/recompute headers before any read.
- Materiality floor 0.02 frozen; a null is recorded as NOT_SUPPORTED, not threshold-shopped.
- Observed liquidations only (Track A); kept distinct from modeled boundary breaches (Track B).
- No external trigger required; frozen panel is the sole input.
- No network calls, no credentials, no paid data.
- No root-level `research_state/*.md` or `*.json` added (root count stays 499/500).
- No `.github/workflows` modified.
- `research_state/research_protocol.md` not overwritten.
- No terminal/superseded campaigns re-run.

## Artifact completeness (machine-enforced gate set)

All FCLR-LIQ-CONTAGION-001 required artifacts present and non-empty under `session_20261121T193000Z/`:
- `fclr_liq_contagion01_prereg_*.json` + `.md` (complete)
- `fclr_liq_contagion01_eval_*.py` + `.json` + `.md` (complete)
- `fclr_liq_contagion01_recompute_*.py` + `.json` (complete)
- `fclr_liq_contagion01_evidence_audit_*.json` + `.md` (complete, this session)
- `evidence_audit_*.json` (complete, this session — gate-critical literal prefix)
- `trigger_check_*.json` (complete, this session, non-empty)
