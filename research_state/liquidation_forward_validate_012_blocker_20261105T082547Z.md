# LIQUIDATION_FORWARD_VALIDATE_012_BLOCKER
Timestamp (UTC): 20261105T082547Z
Git SHA (HEAD): 69d08ad5 (working tree modified by FCLR-NEXT-092 hardening; pycache churn uncommitted)
Branch: main
Campaign: FCLR-NEXT-092-TRACK-A-HEAVY-WHILE-BLOCKED-ZERO-CHURN-RESUME
Repo priority: Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE.

## Objective (inferred)
Complete liquidation-risk half of `Funding-conditioned-volatility-and-liquidation-risk`. No admissible unauthenticated liquidation data beyond 2026-10; create unavoidable heavy progress while blocked.

## Entry Metrics (irrefutable)
- research_state md+json (root): 183
- ironflow probe artifacts: 2 (1 live `ironflow_probe_20261105T082334Z.json` + `ironflow_probe_digest_latest.json`) — stable
- tests: 146 OK baseline
- monitor --quick: ~0.499s cached
- harness cold: ~0.036s
- churn sources identified: timestamped alt-source deep_review/scan families regenerated each run; monitor test side-effects create probe files (tests tolerate/prune via monitor behavior).

## Trigger Probe (exhaustive, Hyperliquid-only)
- `python scripts/monitor_ironflow_liquidations.py --quick`: NO RESUME TRIGGER. data_through=2026-10; probed 2026-11,2026-12,2027-01,2027-02; head_probes=8; baseline_drift intact (state_only_tree_unchanged); kaggle_mirror unchanged. Evidence: `research_state/ironflow_probe_20261105T082334Z.json`.
- `python scripts/deep_review_alt_sources.py`: cache_hits=13, cache_misses=1 (ETag/cached). Canonical output `research_state/alt_source_deep_review_latest.md`.
- `python scripts/hunt_alternative_liquidation_sources.py`: candidates=11, source=cache. Canonical output `research_state/alt_source_scan_latest.json`.
- Decision: **NO NEW DATA - ON HOLD**. No prereg created; no harness outcome inspection.

## Bottleneck Demolition (092)
- Eliminated recurring timestamped families for alt-source probes: `scripts/hunt_alternative_liquidation_sources.py` now writes `research_state/alt_source_scan_latest.json`; `scripts/deep_review_alt_sources.py` now writes `research_state/alt_source_deep_review_latest.md`. No `alt_source_*_{ts}` outputs.
- Removed session-created timestamped alt-source artifacts (consolidated into canonical latest files). Enforced ironflow probe artifacts == 2 after runs.
- No schedulers/pollers/status-only files/repeated wrappers/agent-controllers. No workflow changes. Track C locked; Track B unsupported.

## Rubric/Source Hardening (adversarial)
- Rubric remains maximally strict and aligned (hunt/deep_review): `unauthenticated_only`, `no_requester_pays`, `min_symbols>=5`, `completeness_doc_required`, `license_ok`, `schema_compatible_fclr010`. Hyperliquid-only Track A firewall preserved.
- Added `tests/test_tracka_hardening_092.py` (9 tests): adversarial edge fixtures (reject auth/key/requester-pays/incomplete coverage/non-Hyperliquid-merge/modeled-as-observed via schema+constraints), rubric alignment, canonical alt-output enforcement (no timestamped scan/deep-review families), harness dry-run <10s, prereg gate blocks evaluation without prereg, fixtures present/frozen with >=5 symbols.
- Existing `tests/test_tracka_hardening_091.py` (8 tests) still green.

## Harness Hardening + Offline Dry-run
- `python scripts/fclr010_harness.py`: config loads; splits `frozen_before_outcomes=true`; cold <0.05s. `pre_register_forward_experiment` writes frozen prereg; `evaluate_forward` BLOCKS without prereg/data. Tests enforce <10s bound and prereg-block behavior.
- Fixtures: `tests/fixtures/tracka/manifest.json` frozen, 6 symbols, train/val/test present.

## Tests / Exit Metrics
- `python -m unittest discover tests`: **155 tests OK** (+9 vs 146 baseline). Green.
- research_state md+json (root): 184 (this blocker + canonical alt latest files may exist; net stable/small delta; recurring timestamped families eliminated for alt probes).
- ironflow probe artifacts: **2** (enforced).
- monitor --quick: cached <0.6s. harness: <0.1s.

## Resume Condition (only)
- ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated, OR
- admissible unauthenticated Hyperliquid-only source passes strict GO rubric (>=5 symbols, completeness documented, schema compatible with frozen FCLR-010, no auth/keys/requester-pays, not modeled-as-observed).
- **PREREGISTER BEFORE INSPECTING OUTCOMES** (`research_state/fclr010_prereg_<UTC>.json` or harness prereg path). Hyperliquid-only. No holdout reuse/retuning/threshold-shopping/track merge.

## Concrete Resume Instructions
1. `python scripts/monitor_ironflow_liquidations.py --quick` (and verify if needed). If trigger: STOP outcome inspection.
2. Write frozen prereg with hypothesis/splits/features/targets/metrics/gates/stop rule/data hashes before reading outcomes.
3. Run only frozen FCLR-010 harness/evaluation path on admissible Hyperliquid data; keep observed vs modeled separated.
4. Update `experiment_frontier.json`, write evaluation/blocker artifact, update `AGENT_HANDOFF.md` stricter. Tests green.

## State Left Stricter
- Alt-source probes no longer create timestamped families (canonical latest outputs).
- Adversarial rubric + dry-run bounds enforced by tests (155 total).
- Track C/B locked/unsupported; no conflation; no workflow/scheduler/poller/controller changes.
