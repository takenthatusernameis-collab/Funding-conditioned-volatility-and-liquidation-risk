# Forward Campaign Pre-registration — FCLR-012 (Consolidate Track A + Funding Incremental)

Generated: 2026-11-03T12:00:41Z
Repo: Funding-conditioned-volatility-and-liquidation-risk
Experiment ID: FCLR-012
Campaign: CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL
Status: PREREGISTERED (outcomes NOT inspected)

## 1) Purpose
Pre-register forward validation on (a) Track A observed liquidations (ironflow Hyperliquid census) extending beyond 2026-10-31 if new monthly parquet appears, AND (b) a separate funding-conditioned volatility forward test on new 2026 Binance panel data. Frozen splits/metrics/gates/embargoes/block-bootstrap; no holdout reuse; NO overlay changes. This is the single next focus campaign — future agents must not avoid this heavy work.

## 2) Frozen design (locked before any outcome inspection)

### Track A forward test (FCLR-012-A)
- Hypothesis: FCLR-H004 (observed liquidations)
- Contrast: C2 vs B1 on Brier score
- Model forms: FROZEN per FCLR-010 (fixed logistic, no regularization, no hyperparameter search)
- Features: signed funding + abs funding percentile (90d) + mark/index premium + mark/EMA24 distance (causal, available by forecast t)
- Primary metric: paired out-of-sample Brier difference; relative reduction
- Materiality floor: >=2% relative Brier reduction (frozen)
- CI requirement: two-sided 95% CI excludes zero on improving side (frozen)
- Structural: >=5 instruments, >=3 non-overlapping 30-day blocks, 7-day purge/embargo, block-bootstrap >=2000 reps deterministic seed
- Data: ironflow Hyperliquid liquidation events (observed, not modeled); Hyperliquid-only; NO Binance merge (firewall immutable)
- Trigger: new monthly ironflow parquet beyond 2026-10-31; otherwise NO new forward run
- Holdout: new post-2026-10-31 window only; sealed before outcomes; no reuse of 2026-05-28..2026-10-31 test

### Funding-conditioned volatility forward test (FCLR-012-V)
- Hypothesis: FCLR-H001 (incremental 24h volatility forecasting)
- Contrast: C2 vs B1 on QLIKE
- Model forms: FROZEN OLS log-linear (B0/B1/C1/C2 per FCLR-001 protocol), no regularization/tuning
- Features: RV1h/RV24h/RV168h + signed funding + abs funding percentile + mark/index premium + mark/EMA24 distance
- Primary metric: paired out-of-sample QLIKE difference; relative reduction
- Materiality floor: >=2% relative QLIKE reduction (frozen)
- CI requirement: two-sided 95% CI excludes zero on improving side (frozen)
- Structural: >=5 instruments, >=3 non-overlapping 30-day blocks, 7-day purge/embargo, block-bootstrap >=2000 reps deterministic seed
- Data: new 2026 Binance panel beyond FCLR-011 test (2026-05-08..2026-08-06); if none available, NO run (do not lower thresholds)
- Holdout: new unsealed 2026 window only; sealed before outcomes; no reuse of sealed FCLR-001/003/006/007/008/011 panels

## 3) Execution rules (immutable)
- Pre-register BEFORE inspecting outcomes (this file IS the pre-registration)
- Freeze splits/metrics/gates before outcome calculation
- Enforce embargoes (>=7 days) at all split boundaries
- Block-bootstrap for uncertainty (>=2000 deterministic-seed reps)
- No tuning on holdout/test; no threshold shopping; no holdout reuse
- Separate experiments; never reuse sealed holdouts
- Cross-track firewall enforced (Hyperliquid Track A never merged with Binance panels)
- NO risk-overlay changes; overlay remains HYPOTHETICAL_ONLY
- Heavy work only; no status-only files; no polling loops

## 4) Acceptance (verifiable)
- research_state/track_a_fclr010_consolidated.md exists
- research_state/funding_incremental_synthesis_20261103T115630Z.md exists
- research_state/experiment_frontier.json contains FCLR-012 entry
- python -m pytest tests/test_fclr010_harness.py passes
- scripts/fclr010_harness.py pre_register_forward_experiment() writes a locked prereg; evaluate_forward() BLOCKED without pre-reg

## 5) Next materially different free route if blocked
If no new ironflow parquet beyond 2026-10-31 and no new unsealed 2026 Binance panel exists: do NOT fabricate data, do NOT relax thresholds, do NOT re-run sealed panels. Log the blocker, preserve FCLR-010/FCLR-011 gate states, and wait for new admissible data; then pre-register a fresh experiment ID before outcome inspection.
