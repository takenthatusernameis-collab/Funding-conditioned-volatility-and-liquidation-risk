# FCLR-LIVE-ARCHIVE-07 Preregistration (20261126T153717Z)
**Experiment:** FCLR-LIVE-ARCHIVE-07
**Outcome-data inspected before freeze:** False
**Target:** next-24h mean log realized variance log(RV_24h_next + 1e-09).
**Models:** B1 = OLS signed-component HAR (7 feats); C2 = B1 + funding + price features (11 feats).
**Primary contrast:** C2 vs B1 paired test-set out-of-sample QLIKE. Materiality floor: 2% relative reduction.
**Decision rule:** PROMOTED iff relative QLIKE reduction >=2% and bootstrap 95% CI lower bound > 0; else NOT_SUPPORTED; INCONCLUSIVE if insufficient data.
**Source registry sha256:** 371e7db58c0c3ddd56471eb06b76e17ff8172f585e3f8950648b6d339a43a49c
**Sequential look:** k=2, alpha_2 = 0.008333.
