# RCA011 Feature Attribution & Impl Crosscheck 20261116T035833Z

Panel: `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet`
Design: OLS on log(RV+1e-12), train-only z-scaling for funding/ema24_dist, Duan smearing, 7d purge before test, paired 24h block bootstrap (2000, seed={RNG_SEED}).
C2 premium slot not computable from cached 2026 archive; joint spec uses ema24_dist as the C2 structural slot (matches recompute).

Train rows=152 (after purge/dropna), Test rows=10905.

## Models
|model|SM QLIKE|lstsq QLIKE|max|pred_sm-pred_ls||SM R2|smear|
|---|---:|---:|---:|---:|---:|
|B1|0.563193|0.563193|2.776e-17|0.876444|4.204126|
|B1_plus_funding|2.493112|2.493112|7.461e-14|0.903282|3.357050|
|B1_plus_ema24|0.508304|0.508304|3.296e-17|0.893274|4.270370|
|B1_plus_funding_plus_ema24|2.219020|2.219020|1.488e-14|0.916299|2.849826|

## Contrasts (statsmodels path, block bootstrap)
|contrast|label|rel%|CI95 lo|CI95 hi|ci_cross0|
|---|---|---:|---:|---:|:---:|
|B1_plus_funding_vs_B1|funding_increment|-342.6749|-497.4808|-221.2735|False|
|B1_plus_ema24_vs_B1|ema24_increment|9.7459|7.0092|12.7429|False|
|B1_plus_funding_plus_ema24_vs_B1|joint_increment|-294.0072|-429.6168|-186.5569|False|
|B1_plus_funding_plus_ema24_vs_B1_plus_funding|ema24_over_funding|10.9940|9.4330|12.4379|False|
|B1_plus_funding_plus_ema24_vs_B1_plus_ema24|funding_over_ema24|-336.5535|-495.8134|-210.3323|False|

## Implementation cross-check (SM vs numpy.linalg.lstsq)
|contrast|SM rel%|lstsq rel%|abs diff pp|
|---|---:|---:|---:|
|B1_plus_funding_vs_B1|-342.674861|-342.674861|5.059064e-12|
|B1_plus_ema24_vs_B1|9.745936|9.745936|1.456613e-13|
|B1_plus_funding_plus_ema24_vs_B1|-294.007232|-294.007232|1.875833e-12|
|B1_plus_funding_plus_ema24_vs_B1_plus_funding|10.993990|10.993990|5.915268e-13|
|B1_plus_funding_plus_ema24_vs_B1_plus_ema24|-336.553453|-336.553453|2.842171e-12|

## Attribution read
- **funding_increment** = B1_plus_funding vs B1 (signed_funding + trailing |funding| percentile, z-scored).
- **ema24_increment** = B1_plus_ema24 vs B1 (ema24_dist, z-scored).
- **joint_increment** = B1_plus_funding_plus_ema24 vs B1 (cached-archive analogue of C2 vs B1 without premium).
- Marginals over the other: ema24_over_funding, funding_over_ema24.
- Negative rel% means the augmented model is worse (higher QLIKE) than baseline.

Elapsed 4.54s
