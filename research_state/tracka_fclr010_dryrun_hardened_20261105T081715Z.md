# Track A FCLR-010 Offline Dry-Run Hardened (091)
TIMESTAMP (UTC): 20261105T081715Z

## Components Verified
| Component | Command | Result | Time |
|---|---|---|---|
| Trigger probe (cached) | `python scripts/monitor_ironflow_liquidations.py --quick` | NO RESUME TRIGGER; data_through=2026-10 | ~0.46s |
| Alt source hunt | `python scripts/hunt_alternative_liquidation_sources.py` | 11 candidates, source=cache | cached |
| Deep review | `python scripts/deep_review_alt_sources.py` | cache_hits=13 cache_misses=1 | cached |
| Fixture generation | `python scripts/generate_tracka_fixtures.py` | train/val/test written, 6 symbols | ~0.40s |
| Harness config load | `python scripts/fclr010_harness.py` | frozen config JSON, FCLR-010 | <0.05s |
| Prereg gate | `FCLR010Harness.evaluate_forward(..., pre_reg_path=None)` | BLOCKED | instant |
| Prereg write | `pre_register_forward_experiment()` | frozen record, no_holdout_reuse, no_retuning | instant |
| Tests | `python -m unittest discover tests` | 146 OK | ~13s |

## Fixtures
- Path: `tests/fixtures/tracka/` (`panel_train.jsonl`, `panel_validation.jsonl`, `panel_test.jsonl`, `manifest.json`)
- Manifest: `frozen_before_outcomes=true`, embargo_days=7, symbols `[BTC-PERP,ETH-PERP,SOL-PERP,AVAX-PERP,ARB-PERP,DOGE-PERP]`.
- Contract: `tests/fixtures/tracka/README.md`.

## Resume Path (<10s cold to decision)
1. `python scripts/monitor_ironflow_liquidations.py --quick` — if NO TRIGGER, stop (no outcomes inspected).
2. IF trigger (HTTP 200 >=2026-11): **HALT outcome inspection**, write `research_state/fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json` via harness with frozen splits/features/targets/metrics/stop rule/data hashes.
3. Run ONLY frozen FCLR-010 harness path on preregistered data; record results; update frontier/handoff.

## Gaps Closed
- Added adversarial tests for rubric strictness, prereg enforcement, no-scheduler invariant, fixture manifest, zero-latency harness load.
- Probe artifacts remain stable at 2 files (canonical digest + latest probe).
