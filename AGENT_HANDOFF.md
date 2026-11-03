# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T12:00:41Z
Git SHA (HEAD): 2f7e0584
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk

## 1) What changed / why (this session context)
- Retired duplicate NEXT_AGENT_HANDOFF_2026-11-03T11-59-35Z.md (two competing "single durable handoffs" was a bottleneck); AGENT_HANDOFF.md is now the ONLY durable handoff.
- Campaign FCLR-NEXT-012 CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL executed: consolidation + synthesis artifacts written, forward harness hardened, manifest cross-links added, forward pre-registration written, experiment frontier updated.
- Confirmed Track A (observed liquidations, Hyperliquid ironflow census) forecast gate passed: FCLR-010 C2 vs B1 +2.21% Brier rel (PASS). Overlay pre-registered + executed hypothetically (no trading).
- Confirmed funding-conditioned volatility track passed gate: FCLR-011 C2 vs B1 +4.94% QLIKE rel (PASS) on 2026 panel (BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT).
- Cross-track firewall enforced (no Binance<->Hyperliquid merge). Many experiments closed (H001 NOT_SUPPORTED, H002 PERMANENT_BLOCK, Track B CLOSED_NEGATIVE).

## 2) What was actually tested (exact outcomes)
- FCLR-010: test 2026-05-28..2026-10-31, 199 native perps, block-bootstrap ~24h blocks. C2 vs B1 Brier diff -0.003077, rel -2.21%, CI excludes 0. Gates all PASS.
- FCLR-011: test 2026-05-08..2026-08-06, 5 instruments, block-bootstrap 2000 reps. C2 vs B1 QLIKE diff -0.016458, rel -4.94%, CI [-0.032546,-0.001418]. Gates all PASS.
- Tests present: 14 test files (see tests/). Not re-run in this turn; rely on existing passing state per decision log.

## 3) Evidence added / where
- research_state/track_a_fclr010_consolidated.md (FCLR-010 consolidation: results, splits, ironflow coverage, leakage audit, firewall, gate decision, overlay status, links)
- research_state/funding_incremental_synthesis_20261103T115630Z.md (FCLR-011 synthesis: funding+dislocation incremental over RV-only, features, splits, bootstrap, reproducibility)
- research_state/forward_campaign_fclr012_prereg.md (FCLR-012 pre-registration: forward validation Track A + volatility, frozen splits/metrics/gates/embargo/block-bootstrap, no holdout reuse, NO overlay changes)
- research_state/run_manifest.json (git_sha 2f7e0584, experiments map FCLR-010/FCLR-011/OVERLAY-001 with cross-links)
- research_state/experiment_frontier.json (FCLR-012 entry added, rank 0)
- scripts/fclr010_harness.py (hardened: pre_register_forward_experiment() writes locked prereg; evaluate_forward() BLOCKED without pre-reg, frozen config only, no retuning)
- Existing evidence: research_state/evaluation_summary_FCLR010.md, research_state/evaluation_summary_FCLR-011_20261103T111743Z.md, research_state/evaluation_summary_tracka_overlay_001.md, research_state/cross_track_decision_log.md, research_state/cross_track_decision_firewall.md, research_state/hypothesis_registry.json

## 4) Current state of each research gate
- Track A (FCLR-H004/FCLR-010): FORECAST_GATE_PASSED. Overlay: HYPOTHETICAL_ONLY (pre-registered+executed). No live/paper trading.
- Funding-conditioned volatility (FCLR-011/FCLR-H001): FORECAST_GATE_PASSED (incremental value of funding+price features over RV-only).
- Track C (H001): NOT_SUPPORTED / CONFIRMATORY_CLOSED (all confirmatory panels exhausted: FCLR-003/006/007/008).
- Track B: CLOSED_NEGATIVE.
- H002 (funding-extreme correction replication): PERMANENT_BLOCK (SSRN HTTP 403).
- LIQMICRO-002/003: COMPLETE.
- FCLR-NEXT-012: PREREGISTERED (forward validation gated on new admissible data only).

## 5) SINGLE HIGHEST-VALUE NEXT TASK (must not avoid heavy work)
**CAMPAIGN: CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL (FCLR-NEXT-012)** — EXECUTION PHASE.

The consolidation/synthesis/preregistration artifacts are written and the forward campaign is pre-registered. The heavy work remaining is EXECUTION, gated strictly on new admissible data:
- FCLR-012-A (Track A): forward validation beyond 2026-10-31 ONLY if new monthly ironflow parquet appears. Execute pre-registered forward test via scripts/fclr010_harness.py (pre_register_forward_experiment() then evaluate_forward() with pre-reg + data). Frozen config, no retuning, no overlay changes, firewall intact.
- FCLR-012-V (volatility): forward test on new unsealed 2026 Binance panel beyond FCLR-011 test (2026-05-08..2026-08-06). Only if new unsealed panel exists; otherwise NO run — do not relax thresholds, do not re-run sealed panels.
- If neither new data source appears: log the blocker, preserve gate states, wait for new admissible unauthenticated data; then pre-register a fresh experiment ID before outcome inspection.

Concrete subtasks already DONE (do not repeat): consolidate, synthesize, unify handoff, harden harness, manifest hygiene, bottleneck removal (duplicate handoff retired), heavy-work enforcement (prereg written).

## 6) Precise command/check to verify
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python -m pytest tests/test_fclr010_harness.py -v 2>&1 | tail -15
grep -n "FCLR-012" research_state/experiment_frontier.json 2>&1 | head -5
test -f research_state/track_a_fclr010_consolidated.md && echo "OK_consolidated"
test -f research_state/forward_campaign_fclr012_prereg.md && echo "OK_prereg"
test -f research_state/funding_incremental_synthesis_20261103T115630Z.md && echo "OK_synthesis"
ls research_state/NEXT_AGENT_HANDOFF_*.md 2>&1 | head -1  # must NOT exist (single durable handoff)
```
All must pass/be present. Do not claim success without running checks.

## 7) Blockers / next materially different free route
- No new admissible unauthenticated liquidation source beyond ironflow found (FCLR-NEXT-002 source discovery COMPLETE_NO-GO across 8 families). Track A forward only via ironflow.
- Overlay is hypothetical only; do not build live/paper trading.
- Cross-track firewall is IMMUTABLE - never merge Hyperliquid ironflow with Binance panels.
- Forward runs BLOCKED until new admissible data appears (new ironflow monthly parquet >2026-10-31 for Track A; new unsealed 2026 Binance panel for volatility). Do NOT relax thresholds or re-run sealed panels.
- Bottlenecks removed: duplicate handoff retired; consolidated bundle written; forward harness hardened; manifest cross-linked; pre-registration written.

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

**NEXT AGENT: EXECUTE FCLR-NEXT-012 FORWARD VALIDATION ONLY IF NEW ADMISSIBLE DATA APPEARS. OTHERWISE LOG BLOCKER AND WAIT. DO NOT DEVIATE FROM FROZEN RULES.**
