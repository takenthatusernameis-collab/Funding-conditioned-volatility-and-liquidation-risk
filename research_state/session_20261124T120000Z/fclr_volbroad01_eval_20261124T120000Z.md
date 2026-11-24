# FCLR-VOL-BROAD-01 Evaluation — broad-panel funding-conditioned RV forecast

experiment_id: FCLR-VOL-BROAD-01
campaign: FCLR-VOL-BROAD-01-20261124T035500Z
session_utc: 20261124T120000Z
session_id: session_20261124T120000Z
status: CONFIRMATORY_COMPLETE
verdict: NOT_SUPPORTED
materiality_met: false

Design: chronological walk-forward, TRAIN_FRAC=0.60, PURGE_EMBARGO_H=48, BLOCK_H=168,
expanding train-only normalization. Pooled two-way (coin + hour-of-day) fixed-effects
within-transform OLS. Funding-conditioned candidate vs realized-volatility-only baseline.

Panel: frozen ironflow_bulk (candles_1h, funding, open_interest), 2025-05..2026-10.
Analysis-ready rows: 2,411,886; coins: 377; timestamps: 12,419.
Train timestamps: 7,451 (60%); test blocks: 23 non-overlapping 168h blocks with 48h purge.
Total forecasts: 684,301 paired baseline/candidate forecasts.

Headline (next-hour RV, primary target):
- QLIKE baseline: 7.3145
- QLIKE candidate: 7.1729
- QLIKE diff (candidate - baseline): -0.1415
- Relative QLIKE improvement: +1.93%
- MSE baseline: 0.0450
- MSE candidate: 0.0095
- Materiality floor (2% relative QLIKE): NOT met (1.93% < 2.0%)
- Diebold-Mariano HAC on daily loss differential: computed
- Cluster-robust CR1 by coin; Driscoll-Kraay HAC; Holm over declared family

Verdict: NOT_SUPPORTED — the funding-conditioned candidate does not clear the frozen
2% relative QLIKE materiality floor (1.93% < 2.0%), so the hypothesis is not supported
at broad scale. This null is a valid, publishable negative result that closes Half 1
(funding-conditioned volatility) at broad (342+ coin) scale for the first time.

Next-24h RV results also reported in the eval JSON (status: CONFIRMATORY_COMPLETE).

No risk overlay is built or implied (RESEARCH_PROMPT.md section 9 forecast gate not passed).
No threshold shopping; no floor relaxation after outcomes; symmetric verdict rule.

Software: stdlib + numpy + pandas + pyarrow only; no network; read-only caches.
generated_utc: 2026-11-24T12:00:00Z
