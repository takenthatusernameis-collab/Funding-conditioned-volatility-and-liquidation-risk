# Protocol FCLR-H003-EXT-001 — Track B boundary-breach (unsealed 2026) extended horizons/tiers/intensity

- Experiment ID: FCLR-H003-EXT-001
- Status: PROTOCOL_FROZEN
- Frozen at: 2026-10-30T17:49:18Z
- Git SHA: (to be recorded)
- Hypothesis (H003 extended): Do funding extremes + realized volatility + pre-specified price dislocation/smoothing features improve out-of-sample forecast skill for modeled perpetual boundary breaches (Track B) on the unsealed 2026 panel?
- Track: B (modeled boundary breaches). Distinct from observed liquidations (Track A). Never conflate.
- Panel: Unsealed 2026 data only from research_state/data_cache/ for markPriceKlines/indexPriceKlines/fundingRate (and related) across BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT. Do not touch sealed panels.
- Time range (to be confirmed by coverage audit): use common timestamps present across required series; record exact boundaries in run manifest.
- Targets (pre-registered):
  - Binary breach (long/short separate) over 72h and 168h horizons (extended vs original 24h)
  - Event-intensity (notional-normalized) over 72h and 168h where denominators (OI/volume) exist; if missing, report partial coverage with explicit limits (secondary)
- Margin scenarios (pre-registered):
  - MMR tier S1: maintenance margin ratio = 0.005 (0.5%) — legacy/illustrative
  - MMR tier S2: maintenance margin ratio = 0.004 (0.4%) — lower MMR (adverse-move / more sensitive) tier
  Assumptions: use mark price as reference per scenario; funding/fees treated as documented assumptions (state in eval). If historical maintenance margin cannot be verified for venue, label as illustrative adverse-move proxy only.
- Splits/leakage: Chronological train/val/test on unsealed panel. Purge/embargo >= max horizon (>=168h). Feature normalization/training params only from train. No look-ahead, no forward-fill, no zero-fill of missing features.
- Baselines: B0 (persistence), B1 (HAR-style RV-only). Ablations: C1 (RV + funding), C2 (RV + funding + price-dislocation/smoothing). Paired sample across all comparisons.
- Features (causal): funding extremeness (past-only 90-day percentile, require >=30 obs), signed/abs funding, trailing RV (6h/24h/168h), RV ratio, mark/index premium, mark/EMA24 distance. Missingness tracked.
- Metrics (primary): Brier score, log loss, calibration (slope/intercept). Precision/recall at pre-specified alert budget. For intensity (secondary), define scale normalization explicitly.
- Inference: Block bootstrap (resample complete UTC time blocks across symbols), >=2000 replicates if feasible. Leave-one-symbol-out and time-block stability. Holm correction for declared family. Minimum practical improvement >=2% relative reduction where applicable.
- Decision gates: incremental skill over B1 required; uncertainty must not cross zero in the direction of improvement; track separation enforced.
