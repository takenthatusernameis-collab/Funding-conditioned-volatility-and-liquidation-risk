# FCLR-LIVE-ARCHIVE-03 Preregistration (20261126T051548Z)
**Experiment:** FCLR-LIVE-ARCHIVE-03
**Outcome-data inspected before freeze:** False
**Target:** next-24h RV > train-only 95th percentile (binary stress/tail exceedance).
**Models:** B1 = logistic HAR (log RV1h/24h/168h); C2 = B1 + funding + price features.
**Primary contrast:** C2 vs B1 paired test-set Brier score. Materiality floor: 2% relative Brier reduction.
**Decision rule:** PROMOTED iff relative Brier reduction >=2% and bootstrap 95% CI lower bound > 0; else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.
**Source registry sha256:** 8974e957ce24c7fb8d8972b705def4c21458da9842f80a86a9b3a1b472a1372e
