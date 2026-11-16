# Evidence Audit — 2026-11-16T100533Z

**Session:** `research_state/session_20261116T100533Z/`
**Trigger verdict:** `NO_TRIGGER_FIRED` (see `trigger_check.json`) — all four triggers `OPEN`; Ironflow `data_through=2026-10`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`. Read once; no network, no polling.

## Heavy bundle audited

- **Upstream (authoritative):** `research_state/session_20261116T035833Z/`
- **This session (self-contained carry-forward):** `research_state/session_20261116T100533Z/`

Required artifact families and presence (prefix match):

| family | upstream 035833Z | this session 100533Z |
|---|---|---|
| `rca011_feature_attribution_` (json+md) | present | present (copied, unmodified) |
| `rca011_impl_crosscheck_` (json) | present | present (copied, unmodified) |
| `rca011_sealed_bridge_` (md + _ext) | present | present (copied, unmodified) |
| `prereg_template_trigger_gated_` (json) | present | present (copied, unmodified) |
| `program_power_synthesis_` (json+md) | present | present (copied, unmodified) |

## Integrity conclusion

- FCLR-RCA-011 is **COMPLETE**. FCLR-011 sealed PASS is **not independently reproduced** (clean recompute C2 vs B1 **-294.01%** vs sealed **+4.94%**) and is **fragile / non-promotable**.
- Attribution fit has only **152 complete training rows** after purge/dropna; funding coefficients are unstable, so this supports an integrity/instability finding, not a general "true absence of skill" claim.
- `next_action_heavy=null` on cached data. Do not rerun FCLR-RCA-011 merely because an old note calls it pending.

## New heavy artifact this session

- `trigger_readiness_power_calibration_20261116T100533Z.{json,md}` (offline, stdlib-only; no parquet/outcome reads).
- Key finding: most historical windows were **underpowered** for the 2% materiality floor; only FCLR-009 (n=24,495, 6 blocks, MDE 1.95%) was adequately powered; the Track A liquidation recompute (n=593, MDE 8.88%) needs **~11,689 paired observations** for a 2% MDE. Per-trigger sample floors are now fixed before any outcome data exists.

## Gate results (captured under this session directory)

- `heavywork_gate.json`: PASS — heavy session `session_20261116T100533Z`, no missing artifacts, root `498/500`, reason `OK`.
- `scope_drift.json`: PASS — `scripts=196`, `registry=196`, reason `OK`.
- `targeted_tests.txt`: PASS — 51 tests OK (test_active_campaign_gate, test_tracka_hardening_117/118/143).
- `unittest_discover.txt`: completed — **1354 tests**, `OK (skipped=1)`, 343.113s, final EXIT 0.

## Side effects

- The discovery suite touched `research_state/ironflow_fastpath_cache.json` (timestamp-only); reverted.
- No network probe, no polling, no sealed-artifact/frontier/registry mutation, no new confirmatory estimand.
- Root md/json count unchanged at 498/500.