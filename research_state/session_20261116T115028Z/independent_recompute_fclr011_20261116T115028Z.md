# Independent Numpy Recomputation — FCLR-011 Terminal Headline — 2026-11-16T11:50:28Z

**Session:** `research_state/session_20261116T115028Z/`
**Trigger verdict:** `NO_TRIGGER_FIRED` (see `trigger_check.md`) — no trigger satisfied; per handoff step 3b, this session performs an independent recomputation of a terminal headline from stored panel/config.

## What was recomputed

The sealed FCLR-011 feature-attribution contrasts were independently re-derived from the stored recompute panel (`research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet`, sha256 `41962f82…`) using a **third** implementation path: **numpy-only OLS** (`np.linalg.lstsq`), train-only z-scaling (ddof=0), Duan smearing, QLIKE on positive test targets. No statsmodels, no network, read-only.

- Train window: 2026-01-01 .. 2026-03-17 (152 rows after purge/dropna)
- Test window: 2026-05-08 .. 2026-08-06 (10,905 rows, positive-target)
- Purge: 7 days before test (enforced and asserted)
- Target: `target_rv24h`

## Result: `all_within_tolerance = true` (PASS)

| Contrast | Sealed QLIKE A | Recomputed QLIKE A | Δ QLIKE A | Sealed QLIKE B | Recomputed QLIKE B | Δ QLIKE B | Sealed rel% | Recomputed rel% | Δ rel% | Pass? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| B1_plus_funding_vs_B1 | 2.493112 | 2.493112 | 7.9e-9 | 0.563193 | 0.563193 | 8.2e-10 | -342.6749 | -342.6749 | <1e-4 | YES |
| B1_plus_ema24_vs_B1 | 0.508304 | 0.508304 | 9.7e-10 | 0.563193 | 0.563193 | 8.2e-10 | 9.7459 | 9.7459 | <1e-4 | YES |
| B1_plus_funding_plus_ema24_vs_B1 | 2.219020 | 2.219020 | 7.4e-9 | 0.563193 | 0.563193 | 8.2e-10 | -294.0072 | -294.0072 | <1e-4 | YES |
| joint_vs_B1_plus_funding | 2.219020 | 2.219020 | 7.4e-9 | 2.493112 | 2.493112 | 7.9e-9 | 10.9940 | 10.9940 | 1.4e-8 | YES |
| joint_vs_B1_plus_ema24 | 2.219020 | 2.219020 | 7.4e-9 | 0.508304 | 0.508304 | 9.7e-10 | -336.5535 | -336.5535 | 2.3e-6 | YES |

Tolerances: QLIKE abs ≤ 1e-6; rel% ≤ 1e-3 pct-points. All five contrasts pass.

## Interpretation

- The third independent implementation path (numpy-only, no statsmodels) reproduces the sealed RCA011 feature-attribution QLIKE values and contrasts to ~1e-8 (QLIKE) and ~1e-6 (rel%), far inside declared tolerance.
- This confirms the carried-forward terminal finding: **FCLR-011 is NOT_REPRODUCED vs sealed (+4.94%) and is fragile/non-promotable.** The recompute degradation (C2-vs-B1 −294.01%, funding increment −342.67%) is driven by **funding augmentation** (signed_funding + trailing |funding| percentile), not by ema24_dist (which helps, +9.75%) and not by numerical solver error (now triple-confirmed: statsmodels vs lstsq vs independent numpy).
- The attribution fit has only **152 complete training rows** after purge/dropna; funding coefficients are unstable. This supports an integrity/instability finding, not a general "true absence of skill" claim.

## Artifacts

- `independent_recompute_fclr011.py` — the recomputation script (numpy-only, read-only).
- `independent_recompute_fclr011_20261116T115028Z.json` — full results JSON with per-contrast comparison and tolerances.

## Prohibitions respected

- No new confirmatory estimand launched (no trigger fired).
- No network, no polling, no HuggingFace re-probe.
- No sealed-artifact, frontier, hypothesis-registry, or workflow mutation.
- All outputs written to this session subdirectory; no root-level additions (root remains 500/500).