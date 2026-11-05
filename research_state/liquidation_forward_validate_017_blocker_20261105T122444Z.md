# Track A Forward Validation Blocker — 017 (FCLR-NEXT-097)

**Timestamp (UTC):** 20261105T122444Z
**Task:** FCLR-NEXT-097-TRACK-A-NO-COAST-STRICT-MANIFEST-DEFAULTS-RESUME-GATE-COVERAGE
**Status:** **BLOCKED (data-gated, no rubric-GO source)** — measurable hardening delta delivered; no resume trigger.
**HEAD (baseline):** c1a6cbf3

## Blocker (irrefutable)
- `monitor_ironflow_liquidations.py --quick` (20261105T121645Z): **No resume trigger**. `data_through=2026-10`. Probed `2026-11,2026-12,2027-01,2027-02` (events/fills) — **all absent**. head_probes=8, cached_hits=0, probe_diff 0/0/0. `baseline_drift(intact=True, method=state_only_tree_unchanged)`. kaggle_mirror unchanged/triggered false.
- `deep_review_alt_sources.py` / `hunt_alternative_liquidation_sources.py`: canonical latest refreshed; **no rubric-GO admissible unauthenticated Hyperliquid observed-liquidation source**.
- **No prereg created. No outcome inspection.**

## 097 hardening delta (concrete)
| Area | Before (096) | After (097) | Evidence |
|---|---:|---:|---|
| Root `research_state/*.md+*.json` | 157 | **159** (+2 required evidence) | this blocker + sweep |
| Ironflow probes | 2 | **2** | canonical digest + 1 live |
| Full tests | 226 OK | **244 OK** | `python -m unittest discover tests` |
| Rubric adversarial 093-097 | 67 | **79** (+12) | `tests/test_tracka_adversarial_rubric_097.py` |
| Resume script | PASS <5s, 5 checks | **PASS <5s, 8 checks** | strict rejects minimal GO-shaped; compat preserved; strict accepts full manifest; offline/no-network/no-real-writes |
| Monitor network isolation | 096 tmp isolation | **+6 tests** state-only/decision/simulate/`--verify`/`--decision` with patched network asserts-not-called + real `research_state` unchanged | `tests/test_monitor_network_isolation_097.py` |
| Watch `trigger_harden_*` live (all / non-20261104T) | 1 / 0 | **1 / 0** | generator-compatible; no unsafe moves; audit+compat proof recorded |

## Strict-manifest/compat proof
Minimal GO-shaped candidate (minimal fields only) is **NO-GO in strict manifest mode** (missing machine-verifiable provenance/label evidence) and **GO in compat/legacy path**. Full manifest with machine-verifiable provenance/label/month-block/symbol/normalization evidence is **GO in strict mode**. 093-096 suites remain green.

## Resume instructions
- **Condition:** Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` month>=2026-11 HTTP 200 unauthenticated **OR** admissible unauthenticated Hyperliquid source passes **strict GO** rubric (`assess_strict_manifest` path / full machine-verifiable manifest). Hyperliquid-only.
- **Before outcomes:** **PREREGISTER** (freeze splits/metrics/gates; no threshold-shopping; no sealed Track C/B changes). No outcome inspection before prereg.
- **On resume:** `python scripts/tracka_resume_check.py`; `monitor --quick`; `deep_review`; `hunt`; full tests; freeze prereg; execute FCLR-010 harness path; update frontier/handoff.

Track C SEALED/LOCKED. Track B NOT_SUPPORTED. No conflation. No workflow/scheduler/poller/status-only/repeated wrappers/agent-controllers/new recurring families.
