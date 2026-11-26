# FCLR-LIVE-ARCHIVE-05 Preregistration (20261126T082429Z)
**Experiment:** FCLR-LIVE-ARCHIVE-05
**Outcome-data inspected before freeze:** False
**Target:** next-24h realized-semivariance asymmetry log((RV_plus+1e-09)/(RV_minus+1e-09)).
**Models:** B1 = OLS signed-component HAR (7 feats); C2 = B1 + funding + price features (11 feats).
**Primary contrast:** C2 vs B1 paired test-set out-of-sample MSE. Materiality floor: 2% relative reduction.
**Decision rule:** PROMOTED iff relative MSE reduction >=2% and bootstrap 95% CI lower bound > 0; else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.
**Source registry sha256:** f824cbb3ebc21fde2e7cf81fa19072c9bed22029aceb2406d54746786b94289c
