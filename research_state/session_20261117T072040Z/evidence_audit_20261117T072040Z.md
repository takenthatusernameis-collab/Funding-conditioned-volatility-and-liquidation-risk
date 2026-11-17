# FCLR Evidence Audit — 2026-11-17T07:22:30Z (FCLR-REPRO-SYNTH-05)

Session: `research_state/session_20261117T072040Z/`
Campaign: `FCLR-REPRO-SYNTH-05` (design-frontier certificate + replication robustness)

## 1. Trigger check (Phase A)
- Sources read once (no network/polling/HF re-probe): `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`.
- All reopen triggers **OPEN**: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`.
- Ironflow: `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 `CONFIRMED_ABSENT`.
- No trigger fired → no confirmatory estimand advanced/re-scored/re-run.
- Artifact: `trigger_check_20261117T072040Z.json`.

## 2. New quantitative artifacts (Phase B — heavy work)

### 2a. Design-frontier certificate
- Artifacts: `recompute_design_frontier_certificate_20261117T072040Z.{py,json,md}`.
- Method: stdlib-only, deterministic, read-only. Uses `scripts/next_campaign_status.py --json` for canonical full-C2 and computes a mark+funding-only block frontier (30d train + 7d embargo + 30d test per block) with **mutual non-overlap enforced on `[train_start, test_end]`** and test months excluded per `TESTED_WINDOWS`.
- Per-estimand certificate (with/without mutual non-overlap counts reported):
  - **Full-C2 (mark+index+premium+funding):** 0 disjoint feasible blocks; contiguous runs 2024-04..05 (61d), 2025-01 (31d), none >=127d; `campaign_feasible=false` → `BLOCKED_ON_DESIGN`.
  - **Mark+funding-only (B0/B1/C1):** 4 individually feasible test months without mutual non-overlap (2024-10, 2024-11, 2024-12, 2025-01); **2 mutually non-overlapping** (2024-10, 2025-01) < 3; 5 overlapping pairs; contiguous untested complete mark+funding months <127d → `BLOCKED_ON_DESIGN`.
- **FCLR-014 closed verdict reproduced:** `true` (full-C2 = 0 blocks / no >=127d run; mark+funding-only = 4 individually feasible but 2 mutually non-overlapping). Overall `BLOCKED_ON_DESIGN`, `promotable=false`. Retracted claim restated: 4-block confirmatory prereg freeze (041333Z corrected / 051045Z) is leakage-prone (cross-block train/test overlap).

### 2b. Replication robustness
- Artifacts: `replication_robustness_20261117T072040Z.{py,json,md}` (built on `session_20261117T071110Z/replication_synthesis_20261117T071110Z.json`, no rerun).
- Qualitative corroboration (recompute does not overturn sealed verdict into promotable positive): **7/7** overall (rate 1.000), Wilson95 [0.646, 1.000]. Leave-one-out: each drop leaves 6/6 (rate 1.000), LOO range 1.000–1.000, all-unity true.
- Sign consistency (C2-vs-B1 rel_reduction_pct): positive (C2 better) **3** (FCLR-002, FCLR-008, FCLR-010), negative (C2 worse) **4** (FCLR-003, FCLR-006, FCLR-009, FCLR-013); consistent in sign **false** (QLIKE/Brier mixed estimands).
- Estimand-heterogeneity caveat: pools QLIKE (FCLR-002/003/006/008/009/013) and Brier (FCLR-010) across different windows/blocks/designs; programme-level summary only. Stricter like-for-like within-tolerance reproduction remains **2/7** (FCLR-006, FCLR-009).
- Boundary certificate (minimal change to flip to promotable): programme `CLOSED_TERMINAL / NO_CLAIM_WORTHY_RESULT_PROMOTABLE`. Global minimal flip = one promotable positive result on a trigger-satisfied, pre-powered (paired_n floors), >=3-block, 7d-purge/embargo, pre-registered admissible design, or a new design-feasible (>=3 mutually non-overlapping blocks) cached-data estimand that passes confirmatory gates. Neither exists in current local frontier. Concrete: FCLR-014 needs >=1 more mutually non-overlapping feasible mark+funding-only block (total>=3) + frozen prereg + passing run; FCLR-013 needs >=3-block preregistered panel with favorable >=2% CI-excluding-0 and passing LOIO/placebo; FCLR-010 needs >=2% favorable effect with passing robustness (not re-scoring).

## 3. Carried-forward bundle audit (no reruns)

| Session | Experiment | Status |
|---------|------------|--------|
| `session_20261116T100533Z/` | FCLR-RCA-011 (5 families) | present |
| `session_20261116T125624Z/` | FCLR-009 | `all_within_tolerance=true` |
| `session_20261116T185811Z/` | FCLR-006 | `all_within_tolerance=true` |
| `session_20261116T230140Z/` | FCLR-008 | B0/B1 within tolerance; C1/C2 divergence documented; NOT_MET corroborated |
| `session_20261117T000400Z/` | FCLR-002/003 | diverged beyond tolerance; NOT_MET corroborated |
| `session_20261117T002014Z/` | FCLR-010 | parquet-free recompute; NOT_REPLICATED |
| `session_20261117T031656Z/` | FCLR-013 | ZIP/CSV parquet-free recompute; NOT_REPLICATED |
| `session_20261117T071110Z/` | FCLR-014 adjudication + replication synthesis | BLOCKED_ON_DESIGN baseline, 7/7 corroboration |

No carried-forward session recomputed; no sealed artifact mutated.

## 4. Tool-hardening note
- `scripts/next_campaign_status.py` not modified this session (certificate emitted as session artifact reproducing canonical full-C2 + mark+funding-only non-overlap frontier). No `scripts/*.py` added; scope registries unchanged.

## 5. Prohibitions respected
- No confirmatory estimand started/re-run/re-scored (FCLR-014, synthesis not repeated); no prereg frozen on retracted 4-block claim.
- No sealed/frontier/hypothesis-registry or `.github/workflows/*` mutation; no polling/network/HF re-probe; no LFS pull; no paid/credentialed/manual data; no root-level `research_state/*.md|json` added (root cap respected); no `statsmodels`/unpinned heavy deps added. No parquet reads.
