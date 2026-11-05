# LIQUIDATION_FORWARD_VALIDATE_013_BLOCKER
Timestamp (UTC): 20261105T092616Z
Git SHA (HEAD): c628e94c (working tree modified by FCLR-NEXT-093 hardening; pycache churn pre-existing/uncommitted)
Branch: main
Campaign: FCLR-NEXT-093-TRACK-A-STEPS3-6-BOTTLENECK-DEMOLITION-HEAVY
Repo priority: Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE.

## Objective (inferred)
Complete liquidation-risk half of `Funding-conditioned-volatility-and-liquidation-risk`. No admissible unauthenticated liquidation data beyond 2026-10; while blocked, create unavoidable heavy progress (churn reduction, rubric hardening, dry-run/resume proof, stricter state).

## Entry Metrics (irrefutable)
- research_state md+json (root): 185 (entry snapshot context)
- ironflow probe artifacts: 2 (1 live + `ironflow_probe_digest_latest.json`)
- tests baseline: 155 OK (prior)
- monitor --quick: NO RESUME TRIGGER, data_through=2026-10, probed 2026-11..2027-02, head_probes=8, baseline drift intact, kaggle unchanged
- harness cold: ~0.015s
- Steps 1-2 already complete prior session (baseline + trigger probe NO NEW DATA). Not re-executed.

## Trigger Probe (verified 093)
- `python scripts/monitor_ironflow_liquidations.py --quick` => NO RESUME TRIGGER. Evidence live probe `research_state/ironflow_probe_20261105T091733Z.json` (canonical digest maintained).
- `deep_review_alt_sources.py` / `hunt_alternative_liquidation_sources.py` => canonical latest outputs; no GO.
- Decision: **NO NEW DATA - ON HOLD**. No prereg created; no outcome inspection.

## Bottleneck Demolition (093 Step 3)
- Consolidated unreferenced timestamped Track A families (072416/081715/033013 chain, 7 files) into `research_state/tracka_bottleneck_history_090.md` with SHA256+excerpts; removed files.
- Consolidated unreferenced root `ironflow_scan_20261102T*` (3) and `trigger_watch_20261103T*` (2) with hashes; removed.
- Consolidated 0616xx chain (`source_hardening`, 2x `bottleneck_demolition`, `alt_source_consolidated`) into history 093c with hashes/excerpts; repaired dangling history refs; removed files (no external refs outside history/internal).
- Removed 5 unreferenced `research_state/watch/trigger_harden_20261104T*.json`; hash/sample recorded. (28 remain; not referenced; generator scripts unchanged.)
- Ironflow probes enforced == 2 after probes/tests.
- No new recurring timestamped probe/scan families. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes.

## Rubric/Source Hardening (093 Step 4)
- Added `scripts/tracka_rubric.py`: deterministic fail-closed Hyperliquid-only/observed-only rubric; schema requires `timestamp,symbol,liquidation_notional`; rejects auth/key/signature/requester-pays, modeled/proxy, non-Hyperliquid merge, <5 symbols, missing completeness/license, schema mismatch.
- Added `tests/test_tracka_adversarial_rubric_093.py` (17 explicit adversarial edge fixtures) — all green.
- Existing strict/adversarial tests (`test_tracka_hardening_091.py`, `test_tracka_hardening_092.py`) green. Rubric core aligned; canonical alt outputs preserved.

## Harness Hardening + Offline Dry-run (093 Step 5)
- `FCLR010Harness` cold <0.05s; config frozen; `evaluate_forward` BLOCKED without prereg; fixtures present/frozen (6 symbols, train/val/test). Dry-run path <10s proven/enforced by existing tests.

## Tests / Exit Metrics
- `python -m unittest discover tests`: **173 tests OK** (green; >=155).
- research_state md+json (root): **169** (net -16 from 185 entry snapshot).
- ironflow probe artifacts: **2**.
- recurring alt timestamped families: **0** (canonical latest only).
- monitor quick: NO TRIGGER, cached. harness cold: ~0.015s.

## Before/After (093)
| Metric | Before | After |
|---|---:|---:|
| root md+json | 185 | 169 |
| ironflow probes | 2 | 2 |
| tests | 155 | 173 |
| unreferenced 20261105 Track A chain | 7 files | 0 (history) |
| 0616xx source/bottleneck/alt chain | 4 files (history refs only) | 0 (history 093c) |
| old root ironflow_scan/trigger_watch | 5 | 0 |
| watch trigger_harden 20261104 batch | 33 | 28 |

## Resume Condition (only)
- ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated, OR
- admissible unauthenticated Hyperliquid-only source passes strict GO rubric (`scripts/tracka_rubric.py` / hunt/deep_review constraints): >=5 symbols, completeness documented, schema compatible with frozen FCLR-010, observed (not modeled/proxy), no auth/keys/signature/requester-pays, Hyperliquid-only, no non-Hyperliquid merge.
- **PREREGISTER BEFORE INSPECTING OUTCOMES** (frozen prereg). No holdout reuse, no retuning, no threshold-shopping, no track merge.

## Concrete Resume Instructions
1. Run `python scripts/monitor_ironflow_liquidations.py --quick` (and verify if triggered). If trigger: STOP outcome inspection.
2. Run `python scripts/deep_review_alt_sources.py` and `python scripts/hunt_alternative_liquidation_sources.py`; require rubric GO from `scripts/tracka_rubric.py` criteria for any new candidate before use.
3. Write frozen prereg (hypothesis/splits/features/targets/metrics/gates/stop rule/data hashes) BEFORE reading outcomes.
4. Run only frozen FCLR-010 harness/evaluation on admissible Hyperliquid data; keep observed vs modeled separated.
5. Update `experiment_frontier.json`, write evaluation/blocker artifact, update `AGENT_HANDOFF.md` stricter. Keep tests >=173 green. Keep ironflow probes == 2; keep canonical alt outputs only.

## State Left Stricter
- Adversarial rubric module + 17 explicit edge-fail fixtures enforce modeled-as-observed/non-Hyperliquid/auth/schema/coverage rejection.
- Unreferenced timestamped churn families consolidated (history with hashes/excerpts); root md+json reduced 185->169.
- Track C/B locked/unsupported; Hyperliquid-only firewall; prereg-before-outcomes; no workflow/scheduler/poller/controller changes.
