# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T11:56:30Z
Git SHA (HEAD): 2f7e0584
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk

## 1) What changed / why (this session context)
- Inspected full repo state: large set of scripts/tests, extensive research_state/ artifacts, cached data present (zips + extracted CSVs + ironflow parquet cache).
- Confirmed Track A (observed liquidations, Hyperliquid ironflow census) passed forecast gate: FCLR-010 C2 vs B1 +2.21% Brier (PASS). Overlay pre-registered and executed hypothetically (no trading).
- Confirmed funding-conditioned volatility track also passed gate: FCLR-011 C2 vs B1 +4.94% QLIKE (PASS) on 2026 panel (BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT).
- Cross-track firewall enforced (no Binance<->Hyperliquid merge). Many experiments closed (H001 NOT_SUPPORTED, H002 PERMANENT_BLOCK, Track B CLOSED_NEGATIVE).
- AGENT_HANDOFF.md did not exist as a single durable handoff; creating it now as requested.

## 2) What was actually tested (exact outcomes)
- FCLR-010: test 2026-05-28..2026-10-31, 199 native perps, block-bootstrap ~24h blocks. C2 vs B1 Brier diff -0.003077, rel -2.21%, CI excludes 0. Gates all PASS.
- FCLR-011: test 2026-05-08..2026-08-06, 5 instruments, block-bootstrap 2000 reps. C2 vs B1 QLIKE diff -0.016458, rel -4.94%, CI [-0.032546,-0.001418]. Gates all PASS.
- Tests present: 14 test files (see tests/). Not re-run in this turn; rely on existing passing state per decision log.

## 3) Evidence added / where
- This handoff: AGENT_HANDOFF.md
- Existing evidence: research_state/evaluation_summary_FCLR010.md, research_state/evaluation_summary_FCLR-011_20261103T111743Z.md, research_state/evaluation_summary_tracka_overlay_001.md, research_state/cross_track_decision_log.md, research_state/cross_track_decision_firewall.md, research_state/run_manifest.json, research_state/data_source_registry.json

## 4) Current state of each research gate
- Track A (FCLR-H004/FCLR-010): FORECAST_GATE_PASSED. Overlay: HYPOTHETICAL_ONLY (pre-registered+executed). No live/paper trading.
- Funding-conditioned volatility (FCLR-011): FORECAST_GATE_PASSED (incremental value of funding+price features over RV-only).
- Track C (H001): NOT_SUPPORTED / CONFIRMATORY_CLOSED
- Track B: CLOSED_NEGATIVE
- H002 (funding-extreme correction replication): PERMANENT_BLOCK
- LIQMICRO-002/003: COMPLETE

## 5) SINGLE HIGHEST-VALUE NEXT TASK (must not avoid heavy work)
**CAMPAIGN: CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL (FCLR-NEXT-012)**

Objective: Create a single auditable consolidated bundle that unifies Track A (FCLR-010, observed Hyperliquid liquidations) and the funding-conditioned volatility result (FCLR-011) without merging cross-tracks, freezes a forward-validation plan, and removes bottlenecks so future agents do heavy work automatically.

Concrete subtasks (do ALL, in order):
1. **Consolidate**: Write `research_state/track_a_fclr010_consolidated.md` merging FCLR-010 results, ironflow coverage, leakage audit, firewall compliance, gate decision, overlay status, and links to manifests/hashes.
2. **Synthesize**: Write `research_state/funding_incremental_synthesis_20261103T115630Z.md` summarizing FCLR-011 (funding+dislocation incremental over RV-only), feature definitions, splits, bootstrap, and reproducibility (link to evaluation_summary_FCLR-011_20261103T111743Z.md).
3. **Unify handoff**: Ensure `AGENT_HANDOFF.md` remains the single durable handoff (this file). Add a "FORWARD CAMPAIGN" section with frozen rules.
4. **Harden forward harness**: Validate `scripts/fclr010_harness.py` against frozen config; add/verify a forward validation entrypoint (pre-register before inspecting new outcomes). Ensure it cannot retune.
5. **Manifest hygiene**: Update `research_state/run_manifest.json` with entries for FCLR-011 (and cross-link FCLR-010/overlay) including git SHA, timestamps, data hashes where known, split boundaries, result status.
6. **Bottleneck removal**: Remove/retire redundant ad-hoc summary files that duplicate consolidated info (or document them as superseded). Ensure no polling/status-only loops added. Keep compute bounded.
7. **Heavy-work enforcement**: Create `research_state/forward_campaign_fclr012_prereg.md` pre-registering forward validation on Track A (ironflow) extending beyond 2026-10-31 if new monthly parquet appears, AND a separate funding-conditioned volatility forward test on new 2026 data - both with frozen splits/metrics/gates, embargoes, block-bootstrap, no holdout reuse. NO overlay changes.

**Acceptance test (verify this):**
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python -m pytest tests/test_fclr010_harness.py -v 2>&1 | tail -15
grep -n "FCLR-012" research_state/experiment_frontier.json 2>&1 | head -5
test -f research_state/track_a_fclr010_consolidated.md && echo "OK_consolidated"
test -f research_state/forward_campaign_fclr012_prereg.md && echo "OK_prereg"
```
All must pass/be present. Do not claim success without running checks.

## 6) Precise command/check to verify
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log --oneline -1
python scripts/fclr010_harness.py 2>&1 | head -40
ls -lh research_state/evaluation_summary_FCLR010.md research_state/evaluation_summary_FCLR-011_20261103T111743Z.md research_state/evaluation_summary_tracka_overlay_001.md
```

## 7) Blockers / next materially different free route
- No new admissible unauthenticated liquidation source found beyond ironflow (per decision log). Track A only via ironflow.
- Overlay is hypothetical only; do not build live/paper trading.
- Cross-track firewall is IMMUTABLE - never merge Hyperliquid ironflow with Binance panels.
- If ironflow releases new monthly parquet (>2026-10), can do forward validation ONLY via pre-registered FCLR-012 (item 7 above).
- Bottlenecks to remove: fragmented summaries, missing single consolidated bundle, forward harness needs hardening. These are engineering tasks that unblock heavy work - do them.

## FORWARD CAMPAIGN (FROZEN RULES)
- Pre-register BEFORE inspecting outcomes
- Freeze splits/metrics/gates
- Enforce embargoes (>=7d)
- Block-bootstrap for uncertainty
- No tuning on holdout/test
- Separate experiments, never reuse sealed holdouts
- Firewall enforced
- No risk-overlay until/unless separate pre-registration passes gates
- Heavy work only - no status-only files

**NEXT AGENT: START WITH CAMPAIGN FCLR-NEXT-012 ABOVE. DO NOT DEVIATE.**
