# Liquidation Forward Validate 018 — Blocker (FCLR-NEXT-098)
**Timestamp (UTC):** 20261105T131205Z
**Track:** A (FCLR-010, liquidation risk / observed liquidations) — **BLOCKED / NO RESUME**
**Repo-name priority:** Volatility (Track C) SEALED/LOCKED. **Liquidation Risk = ONLY ACTIVE OBJECTIVE.** Track B NOT_SUPPORTED.

## Blocker (current, verified 20261105T130449Z)
- Ironflow Hyperliquid liquidation archive: `data_through=2026-10`. Forward months probed `2026-11,2026-12,2027-01,2027-02` — **events+fills absent (no HTTP 200)**. Head probes=8, cached_hits=0, probe_diff added/changed/removed=0, baseline drift intact (state_only_tree_unchanged, content hash complete, 18 pairs). Kaggle mirror unchanged/triggered false (last 2026-11-01T06:18:48.21Z).
- Alternative sources (deep_review/hunt canonical latest): **no rubric-GO admissible unauthenticated Hyperliquid observed-liquidation source** passing strict full-manifest gate.
- **No prereg created. No outcome inspection.** Prereg-before-outcomes remains mandatory on trigger.

## 098 measurable hardening delta (concrete)
| Area | Before (097) | After (098) | Proof |
|---|---|---|---|
| Tests | 244 OK | **261 OK** | `python -m unittest discover tests` |
| Harness manifest gate | rubric strict path existed; harness `evaluate_forward` not integrated | **`fclr010_harness.evaluate_source_manifest` + `evaluate_forward` strict gate by default when manifest provided** | minimal-only GO-shaped rejected in strict/default; full machine-verifiable manifest accepted; compat explicit (`strict_manifest_gate=False`) preserved; legacy no-manifest prereg/data behavior preserved (`test_fclr010_harness`, 091/092/094 green) |
| Prereg-before-outcomes trigger simulation | not present | **4 offline deterministic branches, tmp-only, no network, real `research_state` unchanged** | minimal NO-GO blocks despite mocked 2026-11+ data+prereg; strict-GO+no-prereg blocks (`outcomes_inspected=False`); strict-GO+missing-prereg blocks; strict-GO+prereg+mocked data => `READY_FROZEN`/no inspect |
| Alt/cache churn safety | audit context | **tmp-isolated deterministic proofs** | deep_review/hunt produce canonical latest only; no recurring timestamped families; no real `url_probe_cache.json` mutation (mtime/size snapshot unchanged) |
| Handoff drift | observed single | **audited/tested single durable root handoff** | only `AGENT_HANDOFF.md`; no copies in research_state/scripts/tests/src |
| Root `research_state` md+json | 159 | **161** (`<=161`) | +2 required evidence artifacts only |
| Ironflow probes | 2 | **2** | `ironflow_probe_20261105T130449Z.json` + `ironflow_probe_digest_latest.json` |
| Watch trigger_harden live root | 1 | **1** | no unsafe moves |
| New recurring probe/scan families | 0 | **0** | canonical only |

## Resume condition (only, unchanged)
Resume Track A forward validation **only** when: `ironflow data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated **OR** an admissible unauthenticated Hyperliquid observed-liquidation source passes the **strict full-manifest GO gate** (`assess_strict_manifest` / harness default strict manifest path) with machine-verifiable access/provenance, label definition, coverage/block/symbol evidence, and UTC-normalized timestamp proof. **Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.** No conflation of observed/modeled liquidations. No threshold shopping.

## Exact next concrete commands (on trigger)
1. `python -m unittest discover tests` (expect >=261 green)
2. `python scripts/tracka_resume_check.py` (expect pass:true, strict/compat/full-manifest checks, <5s, no network, no real research_state writes)
3. `python scripts/monitor_ironflow_liquidations.py --quick` and `--verify`/decision as needed (capture evidence)
4. **PREREG FIRST:** `python -c "from scripts.fclr010_harness import FCLR010Harness; from pathlib import Path; h=FCLR010Harness(); print(h.pre_register_forward_experiment(Path('research_state/readiness')))"` — write frozen prereg **before** inspecting outcomes
5. Build/obtain strict full manifest (machine-verifiable provenance, label, months/blocks/symbol/timestamp evidence) and run gate: `python -c "import json; from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); m=json.load(open('research_state/readiness/tracka_strict_manifest.json')); print(h.evaluate_source_manifest(m, strict=True))"` (must be GO)
6. Only with strict GO manifest + prereg present: `h.evaluate_forward(data_path=..., output_dir=..., pre_reg_path=..., source_manifest=m)` (default strict). **Do not inspect outcomes before prereg.**
7. Run frozen FCLR-010 harness/forward path only after prereg+strict-GO gate; record artifacts under `research_state/` with leakage/firewall evidence; update frontier/handoff.

## Evidence pointers
- `research_state/campaign_sweep_tracka_20261105T131205Z.md`
- `research_state/ironflow_probe_20261105T130449Z.json`, `research_state/ironflow_probe_digest_latest.json`
- `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`
- `research_state/experiment_frontier.json` (098 update)
- `tests/test_tracka_hardening_098.py`, `scripts/fclr010_harness.py` (strict gate integration)
