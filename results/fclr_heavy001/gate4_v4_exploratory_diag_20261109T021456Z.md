# Gate 4 v4 EXPLORATORY diagnostic — 20261109T021456Z

**Label:** `EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE` (v4 prereg `confirmatory_claim_go=NO_GO`, `frozen_before_outcomes=true`, sealed-anchor conflict with FCLR002/003/013 domain family; 2024-04..09 exploratory-only).

**Scope:** Diagnose B/D split-3 instability from `GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D-EXPLORATORY-20261109T004003Z` (git SHA `2f21b1dd4`); run prereg-scoped exploratory robustness (E vs A instrument LOO) and alignment checks. No prereg A–E contrasts changed; no confirmatory claim.

## Commands
```bash
git rev-parse --short=9 HEAD  # 2f21b1dd4 (repo state at diag)
python -m unittest tests.test_gate4_v4_exploratory_diag -v  # 3/3 OK
python scripts/run_gate4_v4_exploratory_diag.py --out-suffix 20261109T021456Z --git-sha 2f21b1dd4
python -m unittest discover tests
python scripts/tracka_resume_check.py
python scripts/tracka_resume_gate.py --json
```

## Inputs
- Prior exec: `research_state/gate4_v4_exploratory_exec/run_manifest_funding_v4_exploratory_exec_20261109T004003Z.json` (SHA256 `3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c` for FCLR-015 manifest ref in v4 prereg).
- v4 prereg: `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` (FROZEN_BEFORE_OUTCOMES).
- Local cache: `research_state/data_cache` (FCLR-015 identity-verified 2024-04..09), symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT, horizon 24h, `--include-cache`, `v3_30d` splits.

## Primary contrast (EXPLORATORY, reproduced deterministically)
| Contrast | ΔQLIKE (alt−base; negative=better) | 95% block CI (24h UTC, 2000 reps, seed 12345) | n_obs | n_blocks | Verdict |
|---|---:|---:|---:|---:|---|
| E vs A | +0.487902 | [-0.042161, 1.197338] | 12969 | 120 | **INCONCLUSIVE** (CI spans 0); no improvement claim |
| B vs A | +11.110523 | [0.480523, 32.312583] | 13620 | 120 | worse / unstable (exploratory) |
| C vs A | -0.024710 | [-0.371595, 0.270799] | 13985 | 120 | inconclusive |
| D vs A | +2.421918 | [-0.253960, 7.512203] | 13269 | 120 | inconclusive / unstable |

## B/D split-3 instability diagnosis (deterministic, 2024-08-13..2024-09-11 test)
Primary fit: direct-variance OLS HAR (target = forward realized variance), train-only normalization per split, ridge `1e-10*I`, predictions floored at `max(p,0)`; paired QLIKE uses valid rows where `y>0 & p_base>0 & p_alt>0` (`src/volatility/eval.py`).

| Ablation | Split-3 aggregate QLIKE | n_valid | neg/floored pred | Key mechanism |
|---|---:|---:|---:|---|
| A (RV only) | 0.974693 | 3579 | 21 | baseline stable |
| B (RV+signed funding) | 45.000373 | 3288 | 312 | **BTC blowup**: raw preds include very negative values (BTC raw_min -0.000527, 89/720 raw<0; SOL raw_min -0.001226, 125/720) and near-zero positives after floor; BTC per-instrument QLIKE mean 225.80 drives aggregate. Funding coefficient magnitude becomes comparable in normalized space while variance scale is ~1e-6–1e-3, so linear extrapolation crosses zero. |
| D (RV+signed+abs) | 11.285366 | 3024 | 576 | **SOL/BTC blowups**: SOL QLIKE mean 56.34, BTC 1.68; larger `coef_l2` (BTC 0.00418, ETH 0.00557, SOL 0.00552, XRP 0.00409) and many raw negatives (BTC 275/720, SOL 142/720, ETH 90/720, XRP 69/720). Added collinear-ish funding magnitude/level features amplify ill-conditioned extrapolation under tiny ridge. |
| E (RV+signed+abs+trails) | 1.502044 | 2978 | 622 | Worse than A but **no catastrophic single-instrument blowup** (BTC 3.86, SOL 2.46); trails absorb some variation but still produce many raw negatives (622) and near-zero positives — QLIKE remains sensitive (`y/p - log(y/p) - 1`) to small positive forecasts. |

**Root-cause hypotheses (EXPLORATORY, evidence-backed):**
1. **Scale/conditioning under train-only standardization:** narrow funding distributions + direct-variance target (small absolute scale) produce standardized coefficients that extrapolate to negative/near-zero variance on split 3; floor-at-zero removes invalid negatives but leaves extreme small-positive ratios for QLIKE.
2. **Feature instability/collinearity for B/D:** B uses signed funding only; D adds abs funding (correlated with |signed| regimes). Split 3 appears to have funding/vol dynamics that make these linear combinations unstable.
3. **Valid-row selection interaction:** aggregate metrics are computed on `y>0 & p>0`; catastrophic rows are sometimes excluded when floored to 0 but remaining near-zero positives can dominate mean QLIKE (observed for BTC in B, SOL in D).

## Prereg-scoped exploratory robustness (E vs A only)
**Instrument leave-one-out (block bootstrap ΔQLIKE, same spec; EXPLORATORY):**
| Sample | ΔQLIKE E−A | 95% CI | n_obs | Interpretation (EXPLORATORY) |
|---|---:|---:|---:|---|
| all | +0.487902 | [-0.042161, 1.197338] | 12969 | inconclusive |
| drop BTCUSDT | +0.634232 | [0.136810, 1.436794] | 10579 | CI excludes 0 but worse than A |
| drop ETHUSDT | +0.504444 | [0.078897, 1.199251] | 10353 | CI excludes 0 but worse than A |
| drop SOLUSDT | +1.136493 | [0.273338, 2.371366] | 10415 | worse than A |
| drop XRPUSDT | +0.110879 | [-0.128657, 0.358264] | 10425 | inconclusive / attenuated |
| drop BNBUSDT | +1.938175 | [0.714012, 3.920391] | 10296 | worse than A |

**Finding (EXPLORATORY):** E vs A is sensitive to instrument composition; dropping XRPUSDT attenuates harm toward 0 (CI spans 0), while dropping BTC/ETH/SOL/BNB makes harm statistically clear. No LOO shows improvement. **Not confirmatory; not promotable.**

**Stabilized variant comparison (EXPLORATORY only; NOT a prereg contrast replacement):** stronger ridge + `pred_floor=1e-8` produced ΔQLIKE +9213.35 CI [5201.59,14629.06], n=13987 — catastrophic; indicates naive flooring/ridge scaling interacts badly with normalized feature scales and is **not** a candidate fix. Do not use.

## Alignment/leakage checks (code-level evidence)
- `wf.apply_train_only_normalization` applied per split before fit (`scripts/run_funding_ablations.py` `run_multisplit`).
- `src.features.funding.resample_funding_to_hourly` uses `reindex(method='ffill')` on sorted funding => last known at/before hour; no backward fill.
- Trailing funding stats (`trailing_funding_pct/zscore`) are past-only on aligned series.
- No test tuning, no outcome peeking; this session reads only prior versioned artifacts + local cache.

## Artifacts (versioned)
- `scripts/run_gate4_v4_exploratory_diag.py` (EXPLORATORY diagnostic runner)
- `tests/test_gate4_v4_exploratory_diag.py` (3 synthetic, no-network tests)
- `research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json`
- `results/fclr_heavy001/gate4_v4_exploratory_diag_20261109T021456Z.md` (this note)

## Verdict (EXPLORATORY)
**NOT CONFIRMATORY / NOT PROMOTABLE.** Primary E vs A remains inconclusive (CI spans 0) and instrument-sensitive with no LOO improvement. B/D split-3 instability is explained by funding-augmented linear extrapolation producing negative/near-zero variance forecasts under small target scale and tiny ridge, with QLIKE dominated by remaining near-zero positive predictions or concentrated instrument blowups (BTC for B; SOL/BTC for D). A naive stabilized floor+strong ridge made results catastrophically worse. Any future confirmatory work requires a separately preregistered, non-confounded design and must not reuse sealed-anchor outcomes.
