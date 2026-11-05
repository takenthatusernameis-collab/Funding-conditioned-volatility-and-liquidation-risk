# Track A Campaign Sweep — FCLR-NEXT-097 (Strict-Manifest Defaults, Resume Gate, Network Isolation)

**Timestamp (UTC):** 20261105T122444Z
**HEAD (baseline):** c1a6cbf3 (working tree modified by 097 hardening; not committed)
**Task:** FCLR-NEXT-097-TRACK-A-NO-COAST-STRICT-MANIFEST-DEFAULTS-RESUME-GATE-COVERAGE
**Objective:** Measurable hardening delta while Track A blocked (Hyperliquid data_through 2026-10). Volatility (Track C) SEALED/LOCKED; Liquidation Risk (Track A) only active objective. No coasting/status-only.

## Entry verification (exact)
- `python -m unittest discover tests` → **244 tests, OK** (097 adds 18: `test_tracka_adversarial_rubric_097` 12, `test_monitor_network_isolation_097` 6; 096 baseline 226).
- `python scripts/tracka_resume_check.py` → JSON `pass:true, elapsed_s:0.000769, network:false, writes_real_research_state:false`, checks include `rubric_strict_rejects_minimal_go_shaped`, `rubric_minimal_fixture_compat_preserved`, `rubric_strict_accepts_full_manifest` + legacy checks.
- `python scripts/monitor_ironflow_liquidations.py --quick` (20261105T121645Z) → **No resume trigger**. `data_through=2026-10`, probed `2026-11,2026-12,2027-01,2027-02`, head_probes=8, cached_hits=0, probe_diff added=0/changed=0/removed=0, baseline_drift intact (state_only_tree_unchanged), kaggle_mirror unchanged/triggered false.
- `python scripts/deep_review_alt_sources.py` / `hunt_alternative_liquidation_sources.py` → canonical latest refreshed; **no rubric-GO admissible unauthenticated Hyperliquid observed-liquidation source**.

## Before/after metrics (measured)
| Metric | 096 baseline | 097 after | Delta / evidence |
|---|---:|---:|---|
| `research_state` root `*.md+*.json` | 157 | **159** | +2 required evidence only (`campaign_sweep_tracka_20261105T122444Z.md`, `liquidation_forward_validate_017_blocker_20261105T122444Z.md`) |
| Ironflow probes | 2 | **2** | canonical digest + 1 live (`ironflow_probe_20261105T121645Z.json`, `ironflow_probe_digest_latest.json`) |
| Full tests | 226 OK | **244 OK** | +18 additive; 093-097 rubric + 097 network-isolation green |
| Rubric adversarial (093-097) | 67 | **79** | +12 strict-manifest/compat cases (`test_tracka_adversarial_rubric_097.py`) |
| Resume script | PASS <5s, 5 checks | **PASS <5s, 8 checks** incl. strict/compat/full-manifest | machine-readable; offline/no-network/no-real-writes |
| Monitor network-isolation proofs | verify/drift tmp isolation (096) | **+6 tests** covering `verify_state`, `check_baseline_drift`, `evaluate_resume_decision`, `simulate_resume`, `main --verify/--decision` tmp-isolated CLI paths with patched network functions asserting not called + real `research_state` snapshot unchanged | `tests/test_monitor_network_isolation_097.py` |
| Watch `trigger_harden_*` live (all) | 1 | **1** | `trigger_harden_20261104T113550Z.json`; **non-20261104T live residue = 0** |
| Watch consolidation | 096 consolidated 20261104T family safely | **audit complete, no unsafe moves** | generator refs in `scripts/write_trigger_harden_successor.py` and `scripts/track_c_inventory_harden.py` use `research_state/watch/trigger_harden_*.json` (non-recursive root glob); archive excluded. Read-only compatibility proof: root glob resolves to kept live file only; prev=`trigger_harden_20261104T113550Z.json`; archive contains 1 manifest + 27 archived 20261104T files. No non-20261104T residue to consolidate. |
| New recurring timestamped probe/scan families | 0 | **0** | canonical outputs only |

## Strict-manifest defaults + compat proof (097, measurable)
- `scripts/tracka_rubric.py` adds `assess_candidate(..., strict_tracka_manifest=False, minimal_fixture_compat=False)`, `assess_strict_manifest`, `assess_minimal_fixture`. **Backward-compatible default preserved** (093-096 suites green: 67 tests).
- **Strict full-manifest path**: for GO-shaped observed Hyperliquid claims, fail-closes by default on missing machine-verifiable access/dataset provenance + label definition (`observed_access_provenance_missing`, `label_definition_missing`), and applies strict evidence requirements for claimed months/blocks/symbol proof/raw-epoch normalization when present in that path.
- **Compat path**: `minimal_fixture_compat=True` preserves legacy minimal fixture behavior (093-096 minimal GO-shaped candidate remains GO only in compat/default-legacy calls as appropriate; strict rejects minimal-only).
- **Proof (deterministic):** minimal GO-shaped candidate lacking provenance/label/coverage evidence is **NO-GO in strict mode** and **GO in compat/legacy path**; full manifest with machine-verifiable evidence is **GO in strict mode**. Enforced by `test_tracka_adversarial_rubric_097.py` and `tracka_resume_check.py`.

## Network-isolation proof (097)
- Deterministic tmp-dir/mock tests assert network primitives (`http_get`, `head_probe`, `resolve_get`, `check_resume_condition`, `check_baseline_drift_probe` where applicable) are **not called** in state-only/decision/simulate/`--verify`/`--decision` isolated CLI paths.
- Real `research_state` snapshot (probe filenames/mtimes + root md+json count) **unchanged** by isolated CLI verification tests.
- Note: `--quick` and `--scan` are network probes by design; 097 proves state-only/decision/verify cached branches used for state-only decisions are non-network in tested isolation.

## Watch residue consolidation/audit (safe, generator-compatible)
- **Before (096 end):** `trigger_harden_*` live in watch root = 1 (`20261104T113550Z.json`); non-20261104T live residue = 0. Archive present with 096 provenance manifest + 27 archived 20261104T files.
- **After (097 audit):** unchanged live count = 1, non-20261104T live = 0. No moves performed (no safe removable residue beyond compatibility constraint; 096 removed the removable 20261104T set). **Measured delta:** tested incompatibility/safety proof added (generator non-recursive glob, archive exclusion, prev resolution) — prevents future unsafe consolidation. No generators broken.

## Trigger probe evidence (irrefutable, no resume)
- Ironflow `--quick` (20261105T121645Z): `data_through=2026-10`; 2026-11..2027-02 absent (events+fills). No 200. Baseline drift intact. Kaggle mirror unchanged/triggered false.
- Deep review/hunt: canonical latest only; **no rubric-GO source**. **No prereg created. No outcome inspection.**

## Constraints honored
No credentials/manual files/.github/workflows changes. Track C SEALED/LOCKED; Track B NOT_SUPPORTED. Raw data/caches out of git. Canonical outputs only. No new recurring timestamped probe/scan families. No schedulers/pollers/status files/repeated wrappers/agent-controllers. Leakage-safe; preregister before outcomes if triggered.
