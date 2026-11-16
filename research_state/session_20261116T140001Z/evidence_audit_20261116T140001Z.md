# Evidence Audit — 2026-11-16T14:06:00Z (session_20261116T140001Z)

## Trigger check (performed once, no network/polling)
- Read: `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`.
- Timestamp: 2026-11-16T13:58:36Z.
- Triggers: `GATE4_BRANCH_1=OPEN`, `NEW_OBSERVED_LIQUIDATION_SOURCE=OPEN`, `HL_LABEL_EXTENSION=OPEN`, `EXPANSION_ROBUSTNESS_REDO=OPEN` (all OPEN).
- Ironflow: `data_through=2026-10`; 2026-11, 2026-12, 2027-01 `CONFIRMED_ABSENT`.
- No HuggingFace/network probe performed; no repeat check in this session.

## Carried-forward bundle verification
- Complete Phase-B/C bundle: `research_state/session_20261116T100533Z/` present and unmodified in role.
  - `rca011_feature_attribution_20261116T035833Z.{json,md}` ✓
  - `rca011_impl_crosscheck_20261116T035833Z.json` ✓
  - `rca011_sealed_bridge_20261116T035833Z.md` (+ `_ext`) ✓
  - `prereg_template_trigger_gated_20261116T035833Z.json` ✓
  - `program_power_synthesis_20261116T035833Z.{json,md}` ✓
- Latest prior heavy recompute: `research_state/session_20261116T125624Z/` contains `recompute_fclr009_20261116T125624Z.{py,json,md}` + `evidence_audit_20261116T125624Z.md` (4 files; `all_within_tolerance=true`). FCLR-009 DONE; not repeated.

## New quantitative artifact (this session; queue item 2 — FCLR-006)
- `recompute_fclr006_20261116T140001Z.py` / `.json` / `.md` (this directory).
- Independent numpy/pandas recompute from cached 2026 CSVs (`research_state/data_cache/*_2026_{04..08}`), hardcoded frozen splits per `research_state/research_protocol_fclr006.md` (train 2026-04-01..04-24, 7d embargo, val 2026-05-02..05-15, 7d embargo, test 2026-05-23..08-06). No network, no `run_manifest` (LFS pointer), no `scripts/run_evaluation.py`, no sealed artifacts mutated. Mark data restricted to <= 2026-08-06T23:00:00Z to mirror canonical loader boundary.
- Recomputed: B0 QLIKE 0.514065 (n=9120), B1 0.522388 (n=9107), C1 0.694728 (n=9107), C2 1.038821 (n=9107). C2-vs-B1 mean diff 0.516434, relative -98.86%, 95% CI [0.246822, 0.863561] (excludes zero, favors B1), n_pairs 9107. C1-vs-B1 mean 0.172340 rel -32.99%; C2-vs-C1 mean 0.344093 rel -49.53%.
- Published (for audit): B0 0.518169 (n=9000), B1 0.527290 (n=8987), C1 0.620158, C2 0.882279; C2-vs-B1 mean 0.354989, rel -67.32%, errata-corrected CI [0.173748, 0.615614], n_pairs 8987.
- **Tolerance result: `all_within_tolerance=false`.** QLIKE abs diffs exceed 1e-6 and row counts differ (9120/9107 vs 9000/8987) despite mark end-cut; likely residual eligibility/alignment difference vs canonical pipeline (e.g. per-model common-row handling/feature availability at boundaries). The recompute is **directionally consistent** with the terminal headline: C2 is substantially worse than B1 on the frozen test window (large positive diff, CI excludes zero, large negative relative reduction), corroborating NOT_MET / FCLR-H001 NOT_SUPPORTED. Gate remains NOT_MET by design (2 blocks < 3). Discrepancy recorded; no sealed artifact mutated.

## Integrity conclusion
- RCA-011 complete (not rerun): FCLR-011 fragile/non-reproducible/promotable; sealed +4.94% not reproduced by clean recomputes.
- FCLR-009 independently reproduced (`all_within_tolerance=true`, session_20261116T125624Z).
- FCLR-006 (this session): independent recompute produced; headline direction (C2 harm, CI excludes zero, gate NOT_MET) corroborated but exact published values/counts not reproduced within tolerance — recorded as a reproducibility discrepancy requiring follow-up if a tighter canonical-path reproduction is attempted.
- All cached-data confirmatory estimands remain terminal; `next_action_heavy=null` on cached confirmatory work absent trigger. Triggers all OPEN.
- `session_20261116T104644Z/`, `session_20261116T105341Z/` remain incomplete trigger-only and not resumed.

## Gates/tests
- Captured in this session directory: `heavywork_gate.json`, `scope_drift.json`, `targeted_tests.txt`, `unittest_discover.txt` (as produced).
