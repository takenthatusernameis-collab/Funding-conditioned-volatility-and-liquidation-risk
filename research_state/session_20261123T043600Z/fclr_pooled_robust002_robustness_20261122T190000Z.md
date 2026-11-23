# FCLR-POOLED-ROBUST-002 Robustness Report (20261122T190000Z)

**Decision:** NOT_SUPPORTED_LEAKAGE_ROBUST_NULL
**Verdict:** The earlier NOT_SUPPORTED null survives the leakage-hardened design; funding-conditioned features add no material QLIKE improvement over the RV-only baseline.

## Design
- 48h purge+embargo (audit found 1h)
- non-overlapping 168h forward blocks; forward horizon 24h; eligible test origins 1091728 (audit found Jaccard 0.52..0.92)
- 1% mark-oracle premium tolerance filter (audit found 6.8% rows above tol; excluded 13787)
- delisting-aware per-coin identity (637 survivors, 160 exited)
- survivors-vs-exited sensitivity arm
- per-month funding-tercile threshold drift reported (max 1.076e-06)
- per-coin block bootstrap CI95 (2000 reps, seed 20261122)
- Holm across declared family; alpha-spending look k=2, alpha_k=0.00833

## Primary (QLIKE, forward 24h RV)
- B1 (HAR-RV baseline): 4033.416882
- C2 (funding+prem+OI):  4074.201549
- diff C2-B1: 40.784667  rel 1.011%
- materiality floor 2.0%: NOT MET
- bootstrap CI95 rel%: [-0.110, 1.025]
- Holm-adjusted primary p=0.6365 vs alpha_2=0.00833: NOT SIGNIFICANT

## Track B modeled breach (secondary, modeled proxy, NEVER observed liquidation)
- base rate: 0.003056
- Brier model: 0.965990  climatology: 0.003046
- Brier skill: -316.095668

## Sensitivity
- survivors arm: n=1051387 rel%=1.0138825224273318
- exited arm:    n=40341 rel%=-0.08082700316597666

## Sample
- markets: 797, train rows: 2337867, test eligible non-overlap rows: 1091728, test blocks: 23
