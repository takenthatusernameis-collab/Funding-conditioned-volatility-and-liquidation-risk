# FCLR-014 Evidence Audit — 2026-11-17T06:08:53Z

Session: `research_state/session_20261117T060853Z/`
Generated: 2026-11-17T06:08:53Z

## 1. Trigger check (Phase A)

- Source: `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json`
- Network: none. Polling: none.
- All four reopen triggers are **OPEN**: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`.
- Ironflow: `data_through=2026-10`, `consecutive_absent=3`; 2026-11/2026-12/2027-01 = `CONFIRMED_ABSENT`.
- No trigger fired → no confirmatory estimand advanced or re-scored.
- Artifact: `trigger_check_20261117T060853Z.json`

## 2. New quantitative artifacts (Phase B — heavy work)

### FCLR-014 Panel Coverage Audit
- **Artifact:** `fclr014_panel_coverage_audit_20261117T060853Z.{json,md}`
- **Scope:** Per-symbol × per-month coverage matrix over `research_state/data_cache/` for all 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)
- **Method:** Local scan of cached CSV/ZIP files; no network; no parquet engine
- **Result:** 31 months with complete mark+funding for all 5 symbols (2024-04..2026-10); 22 months with full mark+index+premium+funding (2025-01..2026-10)
- **Correction:** Prior handoff claim "no admissible panel exists locally" is FALSE. Cache holds abundant admissible data.

### FCLR-014 Blocker Resolution
- **Artifact:** `fclr014_panel_blocker_resolution_20261117T060853Z.{json,md}`
- **Method:** Cross-referenced coverage matrix with `TESTED_WINDOWS` from `scripts/next_campaign_status.py` and `MIN_DESIGN_DAYS=127`
- **Two design options analyzed:**
  - **Option A (Full C2, needs premium/index):** 0 feasible blocks, 0 feasible runs → NOT FEASIBLE
  - **Option B (Mark+funding-only B0/B1/C1):** 4 feasible disjoint blocks (2024-10, 2024-11, 2024-12, 2025-01), meets >=3 requirement → **FEASIBLE**
- **Verdict:** A new mark+funding-only pre-registration CAN be frozen before outcomes.

## 3. Carried-forward bundle audit (Phase C)

All seven referenced sessions are present and unmodified:

| Session | Experiment | Status |
|---------|------------|--------|
| `session_20261116T100533Z/` | FCLR-RCA-011 (5 families) | Complete bundle present |
| `session_20261116T125624Z/` | FCLR-009 | Present; `all_within_tolerance=true` |
| `session_20261116T185811Z/` | FCLR-006 | Present; `all_within_tolerance=true` |
| `session_20261116T230140Z/` | FCLR-008 | Present; B0/B1 within tolerance, C1/C2 divergence documented, NOT_MET corroborated |
| `session_20261117T000400Z/` | FCLR-002/003 | Present; exact values diverged beyond tolerance, NOT_MET corroborated |
| `session_20261117T002014Z/` | FCLR-010 | Present; parquet-free CSV/JSON recompute, verdict NOT_REPLICATED |
| `session_20261117T031656Z/` | FCLR-013 | Present; ZIP/CSV parquet-free recompute, verdict NOT_REPLICATED |

No recompute was re-run for any carried-forward session. No sealed artifact was mutated.

## 4. Bottlenecks

- **Parquet engine absent:** no `pyarrow`/`fastparquet`/`duckdb`/`polars`; network installs prohibited. FCLR-014 audit uses CSV/JSON/ZIP path only -- no parquet required.
- **Network installs:** numpy/pandas installed from requirements.txt (listed dependencies) to enable the stdlib/numpy path. No new heavy deps added to core path.
- **Root churn cap:** `research_state/` root at 500/500 md+json; all new artifacts written under `session_20261117T060853Z/` only.
- **LFS pointers unresolved:** `run_manifest.json`, `run_manifest_FCLR002.json`, `fclr002_panel*.json`, `manifest_fclr002.json`, `manifest_fclr003.json` are pointers with no local object; not accessed. `git lfs pull` not run (network prohibited).
- **Missing protocols:** `research_protocol_fclr002.md` / `research_protocol_fclr003.md` do not exist; not required for FCLR-014 audit.
- **2024 format:** Apr-Jun 2024 mark/premium/index are ZIPs; Jan-Mar/Jul-Nov CSVs; 2025-2026 ZIP+CSV -- ZIP-aware readers required (not needed for coverage audit).

## 5. Next Steps

- Run `check_handoff_heavywork_gate.py --json` and `check_tracka_scope_registry_drift.py --json`
- Run targeted unittests + full `unittest discover -q`, record counts/exit
- Update `AGENT_HANDOFF.md` with FCLR-014 coverage audit + blocker resolution results, tick queue item
- Freeze new mark+funding-only B0/B1/C1 prereg if next session continues (current session stops at artifacts + verification)