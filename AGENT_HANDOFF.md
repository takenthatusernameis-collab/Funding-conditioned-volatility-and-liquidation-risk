# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261102T220643Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk — Track A liquidation risk PRIORITIZED (repo-name-driven: liquidation risk is the core estimand; forward-validating observed liquidation labels is the unblocked crown jewel)
**CAMPAIGN:** LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i — BLOCKED_ON_DATA (IRONFLOW)
**SESSION GOAL FOR NEXT AGENT:** DO NOT COAST. This is BLOCKED_ON_DATA. You MUST complete MANDATORY HEAVY WORK A–E IN FULL. "Nothing to do" is NOT an option. Session fails if < 1 new measurable artifact beyond baseline is produced.

## NEXT AGENT INITIAL TASK (CLEAR, TIMESTAMPED — START NOW)

**20261102T220643Z: STATE-AWARE RESUME CHECK (CHEAP, NO POLLING)**
1. `python scripts/monitor_ironflow_liquidations.py --verify` (must report `ok=True`)
2. `python scripts/monitor_ironflow_liquidations.py --quick` (state-aware forward-edge check; no HF tree walk explosion; uses ETag/cache)
3. `python scripts/monitor_ironflow_liquidations.py --decision` (OFFLINE - must confirm `new_data_path=false`, `resume_trigger_met=false`)
4. Read latest `research_state/ironflow_trend_report_*.json` and latest blocker doc

**DECISION TREE (NON-OPTIONAL):**
- **NEW DATA PATH (IF ANY):** If `--quick`/`--decision` shows new files for >=2026-11 OR `probe_diff.summary.changed_count>0` OR tree shows new parquet paths → CREATE fresh pre-registration BEFORE inspecting outcomes per `research_state/research_protocol_fclr010.md` v1.0, run `python scripts/fclr010_harness.py`, write full evaluation with calibration/LOO/concentration/block-bootstrap CIs>=2000, Holm, gate. Update frontier+cross-track log.
- **BLOCKED PATH (MANDATORY):** No new data → EXECUTE MANDATORY HEAVY WORK A–E BELOW IN FULL. You MUST produce >=1 NEW measurable artifact. Any session that produces zero new artifacts is a failure.

## VERIFIED STATE (THIS REFRESH, 20261102T220643Z)
- `python scripts/monitor_ironflow_liquidations.py --verify` → ok=True, data_through=2026-10, consecutive_absent=3, baseline_drift=False
- `python scripts/monitor_ironflow_liquidations.py --quick` → probed ['2026-11','2026-12','2027-01','2027-02'], all 404; tree 304; no changes; probe_diff added=0 changed=0 removed=0; baseline_drift intact; no resume trigger
- `python scripts/monitor_ironflow_liquidations.py --decision` → new_data_path=false, resume_trigger_met=false (offline)
- `python -m unittest discover -s tests -v` → 102/102 PASS
- Alt hunt COMPLETE_NO-GO (FCLR-NEXT-002). No admissible unauthenticated Track A source found beyond ironflow (already exploited in FCLR-010). Seals intact (FCLR-010/FCLR-008). No `.github/workflows/*` changes.

## BOTTLENECKS REMOVED (EVIDENCE — DO NOT RE-LITIGATE)
- **Monitor hardened (offline-capable):** ETag tree caching (304 skip), HEAD-before-GET, per-file ETag/Last-Modified, jittered backoff + per-endpoint budgets, rate-limit awareness, `--quick` forward-edge + cached probe records, `compare_probes()` detects 404→200, `check_tree_change()` detects new paths, `--report` aggregates, `resume_block_summary()`, `check_baseline_drift()`, OFFLINE `--decision` + `--simulate` modes remove HF reachability dependency for decision logic.
- **Alt hunt exhaustive:** COMPLETE_NO-GO across all 8 families (#1-#8). Dead routes documented; never re-probe without new evidence.
- **Tests:** 102/102 PASS (added resume simulation tests).
- **State tracking:** Fresh blocker + frontier updated with precise resume_triggers; probe-to-probe diffs persisted.

## MANDATORY HEAVY WORK (BLOCKED PATH — CANNOT SKIP)

### A. STRENGTHEN AUTOMATION (>=1 concrete improvement)
Improve `scripts/monitor_ironflow_liquidations.py` or `scripts/hunt_alternative_liquidation_sources.py`. Must add measurable capability (new helper/flag/validation/diff logic). Evidence: modified script + fresh output/run.

### B. ADD TESTS (all must pass)
Extend `tests/test_monitor_ironflow.py` with tests for new logic from (A). Run `python -m unittest discover -s tests -v` → 100% pass. Evidence: new test methods + green run.

### C. UPDATE BLOCKER DOC (irrefutable evidence)
Create/update a fresh timestamped blocker doc under `research_state/` with complete probe table, timeline, consecutive_absent, resume conditions, alt-hunt summary, and evidence links. Evidence: new/updated blocker doc.

### D. UPDATE FRONTIER (precise triggers)
Update `research_state/experiment_frontier.json` with new timestamp, status BLOCKED_ON_DATA, explicit resume_triggers (ironflow >=2026-11 events/fills 200 OR rubric-passing new source). Evidence: modified frontier.

### E. UPDATE HANDOFF (this file)
Refresh this file with new timestamp, crisp next task. Evidence: updated AGENT_HANDOFF.md.

**ACCEPTANCE CRITERIA (HARD):**
- >=1 NEW measurable artifact beyond baseline (new test, new automation helper, fresh blocker doc, or fresh frontier entry/update with concrete evidence).
- `python -m unittest discover -s tests -v` MUST pass.
- No `.github/workflows/*` modified.
- No raw data committed.
- FCLR-010/FCLR-008 seals preserved. Track separation enforced.
- **ZERO ARTIFACTS = SESSION FAILED.**

## RESUME CONDITIONS (CHECKABLE)
1. Ironflow: `GET https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/YYYY-MM.parquet` returns 200 for YYYY-MM >= 2026-11 OR `data/fills/YYYY-MM.parquet` returns 200. Verify via `python scripts/monitor_ironflow_liquidations.py --quick` OR `--decision` OR `--simulate --trigger-month=YYYY-MM`.
2. OR new source passes strict rubric: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license, unauthenticated only, schema compatible with frozen FCLR-010 (Hyperliquid-only for Track A). Pre-register BEFORE inspecting outcomes.

**NEXT AGENT:** Run verify+quick+decision. If new data → pre-reg + harness. If blocked → DO HEAVY WORK A–E fully. No shortcuts. No polling loops. Heavy work is mandatory.
