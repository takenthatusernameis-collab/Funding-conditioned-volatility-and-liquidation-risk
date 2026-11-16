# Evidence Audit — 2026-11-16T11:50:28Z

**Session:** `research_state/session_20261116T115028Z/`
**Trigger verdict:** `NO_TRIGGER_FIRED` (see `trigger_check.json`) — all four triggers `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`. Read once; no network, no polling.

## Carried-forward heavy bundle audited

- **Upstream (authoritative):** `research_state/session_20261116T035833Z/`
- **Prior self-contained bundle:** `research_state/session_20261116T100533Z/`

Required artifact families and presence (prefix match):

| family | upstream 035833Z | prior bundle 100533Z | this session 115028Z |
|---|---|---|---|
| `rca011_feature_attribution_` (json+md) | present | present (copied, unmodified) | referenced + independently reproduced |
| `rca011_impl_crosscheck_` (json) | present | present (copied, unmodified) | referenced (triple-path confirmed) |
| `rca011_sealed_bridge_` (md + _ext) | present | present (copied, unmodified) | referenced |
| `prereg_template_trigger_gated_` (json) | present | present (copied, unmodified) | referenced (still adequate) |
| `program_power_synthesis_` (json+md) | present | present (copied, unmodified) | referenced |

## Integrity conclusion

- FCLR-RCA-011 is **COMPLETE**. FCLR-011 sealed PASS is **not independently reproduced** (clean recompute C2 vs B1 **-294.01%** vs sealed **+4.94%**) and is **fragile / non-promotable**.
- Attribution fit has only **152 complete training rows** after purge/dropna; funding coefficients are unstable, so this supports an integrity/instability finding, not a general "true absence of skill" claim.
- `next_action_heavy=null` on cached data. Do not rerun FCLR-RCA-011 merely because an old note calls it pending.

## New heavy artifact this session

- `independent_recompute_fclr011_20261116T115028Z.{json,md}` + `independent_recompute_fclr011.py` (offline, numpy-only, read-only).
- Method: third independent implementation path — numpy-only OLS (`np.linalg.lstsq`), train-only z-scaling (ddof=0), Duan smearing, QLIKE on positive test targets. No statsmodels, no network.
- Result: `all_within_tolerance = true`. All five attribution contrasts reproduce the sealed RCA011 QLIKE values to ~1e-8 (QLIKE) and ~1e-6 (rel%), far inside declared tolerance (QLIKE abs ≤ 1e-6; rel% ≤ 1e-3 pct-points).
- This triple-confirms (statsmodels vs lstsq vs independent numpy) that the FCLR-011 degradation is **not** a numerical solver artifact and that the sealed +4.94% PASS is not reproducible; funding augmentation drives the recompute harm.

## Prohibitions respected

- No new confirmatory estimand launched (no trigger fired).
- No network probe, no polling, no sealed-artifact/frontier/registry mutation.
- All new artifacts written to this session subdirectory; no root-level additions (root remains 500/500 md/json).
- `statsmodels` not added to the core path; the independent path is numpy-only per handoff dependency policy.