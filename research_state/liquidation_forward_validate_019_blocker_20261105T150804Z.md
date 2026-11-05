# Liquidation Forward Validate 019 — Blocker (FCLR-NEXT-100 / HEAVY-099 ROOT-CAUSE FIX)
**Timestamp (UTC):** 20261105T150804Z
**Track:** A (FCLR-010, liquidation risk / observed liquidations) — **BLOCKED / NO RESUME**
**Repo-name priority:** Volatility (Track C) SEALED/LOCKED. **Liquidation Risk = ONLY ACTIVE OBJECTIVE.** Track B NOT_SUPPORTED.

## Blocker (current, verified 20261105T150804Z)
- Ironflow Hyperliquid liquidation archive: `data_through=2026-10`. Forward months probed `2026-11,2026-12,2027-01,2027-02` — **events+fills absent (no HTTP 200)**. Head probes=8, cached_hits=0, probe_diff added/changed/removed=0, baseline drift intact (state_only_tree_unchanged, content hash complete, 18 pairs). Kaggle mirror unchanged/triggered false (last 2026-11-01T06:18:48.21Z).
- Alternative sources (deep_review/hunt canonical latest): **no rubric-GO admissible unauthenticated Hyperliquid observed-liquidation source** passing strict full-manifest gate.
- **No prereg created. No outcome inspection.** Prereg-before-outcomes remains mandatory on trigger.

## 100 measurable hardening delta (concrete) — ROOT-CAUSE FIX
| Area | Before (099, broken invariant) | After (100, fixed) | Proof |
|---|---|---|---|
| `ironflow_probe_*` files | **3** (2 live + 1 digest) | **2** (1 live + 1 digest) | `ls research_state/ironflow_probe_*.json` |
| Consolidation `removed` | 0 (dedup skipped unlink) | **1** | `ironflow_probe_20261105T150753Z.json` churn `3 -> 2` |
| Idempotency | re-archived every run | second pass `removed=0`, count stays 2 | `test_conolidation_idempotent_probe_count_stays_two` |
| Tests | 274 OK | **276 OK** (+2) | `python -m unittest discover tests` |
| Root `research_state` md+json | 161 | **161** (`<=163`) | unchanged |
| Canonical alt outputs | 2 | 2 | `alt_source_deep_review_latest.md`, `alt_source_scan_latest.json` |
| `tracka_resume_check.py` | pass | pass (`pass:true`, `<5s`, `network:false`, `writes_real_research_state:false`) | unchanged |
| Trigger | NO DATA | NO DATA | `monitor --quick` |

**Root cause:** `_consolidate_ironflow_probes` dedup `if pid in seen: continue` skipped the `old.unlink()`, so a probe already archived in the canonical digest was re-archived on every `--quick` while its file was never deleted (verified 3 files / `removed 0`). Churn was also measured and written *after* consolidation, re-creating the file consolidation had removed. Fixed by splitting dedup (skip append, always unlink) and moving churn to a single pre-consolidation write.

## Resume condition (only, unchanged)
Resume Track A forward validation **only** when: `ironflow data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated **OR** an admissible unauthenticated Hyperliquid observed-liquidation source passes the **strict full-manifest GO gate** with machine-verifiable access/provenance, label definition, coverage/block/symbol evidence, and UTC-normalized timestamp proof. **Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.** No conflation of observed/modeled liquidations. No threshold shopping.

## Exact next concrete commands (on trigger)
1. `python -m unittest discover tests` (expect >=276 green)
2. `python scripts/tracka_resume_check.py` (expect pass:true, strict/compat/full-manifest checks, <5s, no network, no real research_state writes)
3. `python scripts/monitor_ironflow_liquidations.py --quick` and `--verify`/decision as needed (capture evidence)
4. **PREREG FIRST:** `python -c "from scripts.fclr010_harness import FCLR010Harness; from pathlib import Path; h=FCLR010Harness(); print(h.pre_register_forward_experiment(Path('research_state/readiness')))"` — write frozen prereg **before** inspecting outcomes
5. Build/obtain strict full manifest and run gate: `python -c "import json; from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); m=json.load(open('research_state/readiness/tracka_strict_manifest.json')); print(h.evaluate_source_manifest(m, strict=True))"` (must be GO)
6. Only with strict GO manifest + prereg present: `h.evaluate_forward(data_path=..., output_dir=..., pre_reg_path=..., source_manifest=m)` (default strict). **Do not inspect outcomes before prereg.**
7. Run frozen FCLR-010 harness/forward path only after prereg+strict-GO gate; record artifacts under `research_state/` with leakage/firewall evidence; update frontier/handoff.

## Evidence pointers
- `research_state/campaign_sweep_tracka_20261105T150804Z.md`
- `research_state/ironflow_probe_20261105T150804Z.json`, `research_state/ironflow_probe_digest_latest.json`
- `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`
- `research_state/experiment_frontier.json` (100 update)
- `tests/test_monitor_ironflow.py` (TestConsolidation, +2 new tests), `scripts/monitor_ironflow_liquidations.py` (`_consolidate_ironflow_probes`)