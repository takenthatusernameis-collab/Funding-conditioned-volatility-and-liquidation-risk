# FCLR-VOL-BROAD-01 Preregistration — outcome-blind broad-panel funding-conditioned RV forecast

experiment_id: FCLR-VOL-BROAD-01
campaign: FCLR-VOL-BROAD-01-20261124T035500Z
session_utc: 20261124T120000Z
session_id: session_20261124T120000Z
phase: PREREG_FREEZE_ON_BROAD_UNIVERSE
source: fclr_volbroad01_prereg

outcome_data_inspected_before_freeze: false
decision_frozen_before_outcomes: true
frozen_before_outcomes: true

Estimand: out-of-sample, pooled two-way (coin + hour-of-day) fixed-effects within-transform forecast of next-hour and next-24-hour realized volatility on the broad frozen ironflow_bulk panel, testing whether funding features improve QLIKE over a realized-volatility-only baseline once coin and hour fixed effects are removed, and whether any improvement clears the frozen 2% relative QLIKE materiality floor with Holm-adjusted uncertainty. Outcome-blind: no outcome summaries inspected before this freeze.

Label construct: hourly close-to-close realized volatility.
- targets: next_hour_rv, next_24h_rv
- horizon_h: 1, 24
- next-hour RV = squared close-to-close log return over hour t+1; next-24h RV = sum of squared close-to-close log returns over hours t+1..t+24; per coin from candles_1h close.

Universe: broad ironflow_bulk intersection panel.
- months: 2025-05 .. 2026-10 (18 monthly parquet)
- n_coins_candles_1h: 342; n_coins_funding_oi: 198
- panel uses the intersection of coins present in candles_1h, funding, and open_interest; present-day survivors not substituted; no future information in coin selection.

Features (all known at origin hour t):
- signed funding rate: latest funding observation <= t, retaining sign separately
- abs_funding trail: trailing rolling mean of abs(funding_rate), train-only thresholds
- RV24: trailing 24-hour realized volatility ending at t
- RV168: trailing 168-hour realized volatility ending at t
- mark/oracle premium: mark_price / oracle_price - 1, contemporaneous alignment
- MA deviation: close_t / 24-hour trailing moving average of close - 1
- normalization: train-only means/stds; expanding train-only thresholds; no full-sample quantiles; no future information
- min_valid_funding_observations: 30

Baseline: realized-volatility-only persistence — pooled two-way FE within-transform of target RV on trailing RV24 (+RV168), no funding features.
Candidate: funding-conditioned FE — same pooled two-way FE within-transform plus signed funding rate, abs_funding trail, RV24/RV168, mark/oracle premium, MA deviation.

Design: walk_forward.
- train_frac: 0.60
- purge_embargo_h: 48
- block_h: 168
- chronological non-overlapping 168h test blocks over the post-train test span
- expanding train; train-only normalization per block; no random split; no overlapping forward targets across purge boundary.

Metrics: QLIKE (primary), MSE (secondary). Inference: Diebold-Mariano HAC on daily loss differential; cluster-robust CR1 by coin; Driscoll-Kraay HAC. Multiplicity: Holm step-down over declared family.

Verdict rule (symmetric, frozen):
- PROMOTED iff materiality floor met AND Holm-adjusted uncertainty supports improvement
- NOT_SUPPORTED iff floor not met OR uncertainty does not support improvement
- INCONCLUSIVE iff evaluation cannot be completed or fidelity blocker
- a null is a valid, publishable negative result that closes Half 1 at broad scale
- no threshold shopping; no floor relaxation after outcomes.

Materiality floor: 0.02 (2% relative QLIKE). A +1 sample-SD funding shock must move QLIKE by >= 2% relative to baseline. Frozen before outcomes; never relaxed after outcomes.

Sign convention: relative_improvement = (baseline - candidate) / baseline; positive means candidate better; used identically in eval and recompute.

Input hash assertions:
- source_registry_sha256: 2a085fb9de762b6080ee8f4fcf4b30906d8a0a98301fff4aa3e49a7d1b25dcc8
- source_registry_path: research_state/session_20261124T120000Z/fclr_volbroad01_source_registry_20261124T120000Z.json
- sha256_sidecars_asserted_before_every_read: true
- caches_read_only_not_mutated: true
- no_network_for_heavy_evaluation: true

Status vocabulary: PROMOTED / NOT_SUPPORTED / INCONCLUSIVE (symmetric, frozen).

generated_utc: 2026-11-24T12:00:00Z
