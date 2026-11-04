# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T014827Z
Git SHA (HEAD): 503957c2
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T014827Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-EXECUTION

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-024-TRACK-C-FUNDING-CONDITIONED-VOL-HARDENING
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting, no deferring)
CAMPAIGN: FCLR-NEXT-024-FUNDING-CONDITIONED-VOL-CONTINUOUS-EXECUTION
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility forecasting) >> Track B (modeled boundary breaches) >> Track A (observed liquidation labels)
TIMESTAMP (UTC): 20261104T014827Z
OBJECTIVE: Repo name is directive - focus on FUNDING-CONDITIONED VOLATILITY. Build hard execution path for Track C (incremental value of funding + price features over RV-only baseline). Forward validation FCLR-NEXT-012 blocked pending admissible triggers (ironflow > 2026-10-31 OR unsealed 2026 Binance panel beyond 2026-11-02; all current 2026 zips are zero-volume synthetic placeholders -> NOT admissible). Do NOT wait passively - harden everything so the moment trigger fires, we run pre-registered frozen config with zero latency.
HEAVY WORK MANDATE (NON-NEGOTIABLE, ALL FIVE EACH SESSION):
(1) FULL INVENTORY HARDENING: enumerate root zips (count by asset/month/year), research_state/data_cache/ironflow_events/* (>2026-10-31 explicitly checked), all Binance data_vision artifacts. Diff vs previous trigger_harden snapshot (trigger_harden_20261104T010253Z.json).
(2) PREREG GATING PROOF: python -c "from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); print(h.evaluate_forward(data_path='/tmp/no_data_x.zip', output_dir='/tmp/x'))" OR run dry-run of evaluate_forward without prereg -> MUST fail with explicit prereg error. Capture exact traceback/message.
(3) TRACK C READINESS (structure-only, NO outcome inspection/tuning): maintain/validate research_state/readiness/track_c_prereg_template_fclr012.json. Ensure frozen features (funding signed/abs, trailing RV6/RV24/RV168, premium/index-basis/mark-to-index, lags), targets (horizons 6h/24h/72h/7d), baselines (HAR/RV-only), ablations, CV/walk-forward, sealed holdout, correction for multiple comparisons.
(4) INTEGRITY SWEEP: verify cross_track_decision_firewall.md, sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, experiment_frontier.json, run_manifest.json, hypothesis_registry.json unchanged. Verify no workflow files modified.
(5) SHIP HEAVY ARTIFACT: write research_state/watch/trigger_harden_<ts>.json successor with full diffs/inventory/gating_proof/track_c_readiness/integrity_hashes/next_action. MUST include concrete runnable commands for next session.

BOTTLENECK REMOVAL RULES:
- If any check takes >30s, parallelize or optimize; if blocking on download, use cache; if tests fail, fix immediately.
- No "status only" files. Every artifact must enable action.
- If data missing, harden detection/triggers and pre-reg readiness - do not idle.
- Tests must stay >=117 passing; run them first if anything changed.
- Do NOT re-run sealed FCLR-001/002/003/006/007/008/011 (firewall-sealed; would violate pre-registration/holdout discipline).
- Forward validation FCLR-NEXT-012 is BLOCKED on admissible data (Binance archive ends 2026-11-02; live probe 404 for 2026-11-03/04 and 2026-10-28/29; all current 2026 zips zero-volume synthetic placeholders -> NOT admissible). BOTTLENECK REMOVED: do not idle waiting. Continuously maintain trigger detection + Track C pre-registration readiness so we execute pre-registered frozen config with zero latency on trigger arrival.

MANDATORY ACTION SEQUENCE (execute in order):
1) VERIFY: python -m unittest discover -s tests -v (expect 117 OK). If fail -> fix before proceeding.
2) INVENTORY: python scripts/track_c_inventory_harden.py (diff vs trigger_harden_20261104T010253Z.json).
3) GATING: prove prereg required with explicit error capture (harness BLOCKED without pre_reg_path).
4) TRACK-C: validate prereg template schema + frozen structure only (no outcome inspection).
5) INTEGRITY: hash-check critical seals/firewalls/manifests.
6) ARTIFACT: generate timestamped heavy artifact with actionable next steps.
```

## 1) Bottlenecks removed (this session)
- Handoff refreshed with repo-name-prioritized Track C focus (timestamp 20261104T014827Z)
- Clear heavy-work mandate enforced (all 5 required each session)
- Fresh trigger_harden artifact shipped: research_state/watch/trigger_harden_20261104T010253Z.json (463 root zips all 2024; ironflow latest 2026-10.parquet; trigger_ironflow_gt_20261031=false)
- Prereg gating proof captured: evaluate_forward() BLOCKED without prereg with explicit reason "Pre-registration path required..."
- Explicit bottleneck removal rules added
- Forward validation bottleneck REMOVED (no idle waiting): FCLR-NEXT-012 blocked on admissible data -> remedy is continuous trigger detection + Track C pre-reg readiness for zero-latency execution on trigger arrival
- Firewall rule enforced: do NOT re-run sealed FCLR-001/002/003/006/007/008/011 (removes session inefficiency from re-running exhausted confirmatory panels)
- Trigger definition locked: NEW admissible unauthenticated 2026 Binance panel beyond sealed FCLR-011 test window 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h klines + markPriceKlines + indexPriceKlines + premiumIndexKlines + fundingRate)

## 2) Bottlenecks still open
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data
  - Ironflow: latest 2026-10.parquet in research_state/data_cache/ironflow_events/ (no files > 2026-10-31); trigger_ironflow_gt_20261031=false
  - Binance: root zips 2024-01..2024-03 only; live probe 2026-11-04T00:45Z -> 404 for 2026-11-03/04 and 2026-10-28/29; archive genuinely ends 2026-11-02
  - All current 2026 data_cache zips are zero-volume synthetic placeholders -> NOT admissible -> trigger NOT fired as of 20261104T014827Z
  - Remedy: maintain trigger detection + Track C pre-registration readiness continuously so we execute pre-registered frozen config with zero latency on trigger arrival; do not idle waiting.

## 3) Verified state (this session)
- Tests: 117/117 OK (verified 20261104T014827Z)
- Git HEAD: 503957c2 (main)
- Ironflow latest: 2026-10.parquet (coverage up to 2026-10-31 per registry); trigger_ironflow_gt_20261031=false
- Root data zips: 463 root zips, all 2024 (01-01..03-30); no Binance data beyond 2026-11-02
- Sealed window: 2026-05-08..2026-08-06 (frozen)
- Prereg gating: evaluate_forward requires prereg (enforced; BLOCKED without it, explicit reason captured)
- Integrity seals present and unchanged (cross_track_decision_firewall.md IMMUTABLE/SEALED)
- Track C prereg template: research_state/readiness/track_c_prereg_template_fclr012.json exists (structure-only, no outcome inspection)
- FCLR-010 (Track A) gate PASSED (sealed, FORECAST_GATE_PASSED); FCLR-011 (Track C) gate PASSED (sealed, FORECAST_GATE_PASSED, +4.94% rel QLIKE, CI [-0.032546, -0.001418] excludes zero); FCLR-012-V forward INCONCLUSIVE (5 days, 0 blocks, CI spans zero)
- Overlay INELIGIBLE per cross-track firewall (IMMUTABLE); cross-track firewall IMMUTABLE
- H001 status: NOT_SUPPORTED on widest unsealed powered panel (FCLR-008 CI crosses zero); all confirmatory panels exhausted

## 4) Next focus campaign (FCLR-NEXT-024)
**TRACK C - FUNDING-CONDITIONED VOLATILITY HARDENING** (repo-name driven priority)

Focus: Make Track C execution-ready so that on trigger arrival, we pre-register BEFORE inspecting holdout outcomes and execute frozen walk-forward against RV-only HAR baseline with full ablations. Repo name = Funding-conditioned-volatility-and-liquidation-risk -> Track C first, always.

Concrete heavy tasks for next session:
1. Run `python scripts/track_c_inventory_harden.py` - fast inventory with diffs vs trigger_harden_20261104T010253Z.json
2. Validate Track C prereg template has all required frozen elements (no outcomes inspected)
3. Maintain trigger detection helper that exits non-zero or writes alert on trigger
4. Prove gating repeatedly with captured proof (evaluate_forward MUST fail without prereg)
5. Ship successor `trigger_harden_<ts>.json` with hashes + runnable commands

**RULE:** Never idle. If no trigger, HARDEN. Every session must produce a verifiable heavy artifact.

## 5) Concrete runnable commands for next session
```
# 1) Verify tests first (gate before anything else)
python -m unittest discover -s tests -v   # expect 117 OK

# 2) Inventory hardening (full diff vs previous snapshot)
python scripts/track_c_inventory_harden.py   # writes research_state/watch/trigger_harden_<ts>.json

# 3) Prereg gating proof (MUST fail with explicit prereg error without prereg)
python -c "from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); print(h.evaluate_forward(data_path='/tmp/no_data_x.zip', output_dir='/tmp/x'))"   # expect BLOCKED explicit reason
python scripts/fclr010_harness.py   # prints frozen config

# 4) Track C readiness (structure-only, no outcome inspection)
python -m json.tool research_state/readiness/track_c_prereg_template_fclr012.json

# 5) Integrity sweep (verify sealed docs unchanged)
sha256sum research_state/cross_track_decision_firewall.md research_state/sealed_holdout_integrity.md research_state/structural_closure_verdict_heavy.md research_state/experiment_frontier.json research_state/run_manifest.json research_state/hypothesis_registry.json
git status --short .github/workflows   # expect empty (workflow protected)
```

## 6) Acceptance criteria (session done)
- 117 tests OK
- New timestamped trigger_harden artifact in research_state/watch/ with inventory + gating proof + track_c_readiness + integrity hashes + next_action
- Prereg gating proof captured (explicit BLOCKED error without prereg)
- Track C prereg template validated structure-only
- No workflow files modified; sealed docs unchanged
- AGENT_HANDOFF.md updated with new timestamp and next task

(End of file)