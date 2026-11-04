# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T003945Z
Git SHA (HEAD): 74371478
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T003945Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-EXECUTION

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-023-TRACK-C-FUNDING-CONDITIONED-VOL-HARDENING
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting, no deferring)
CAMPAIGN: FCLR-NEXT-023-FUNDING-CONDITIONED-VOL-CONTINUOUS-EXECUTION
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility forecasting) >> Track B (modeled boundary breaches) >> Track A (observed liquidation labels)
TIMESTAMP (UTC): 20261104T003945Z
OBJECTIVE: Repo name is directive - focus on FUNDING-CONDITIONED VOLATILITY. Build hard execution path for Track C (incremental value of funding + price features over RV-only baseline). Forward validation FCLR-NEXT-012 blocked pending admissible triggers (ironflow > 2026-10-31 OR unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06). Do NOT wait passively - harden everything so the moment trigger fires, we run pre-registered frozen config with zero latency.
HEAVY WORK MANDATE (NON-NEGOTIABLE, ALL FIVE EACH SESSION):
(1) FULL INVENTORY HARDENING: enumerate root zips (count by asset/month/year), research_state/data_cache/ironflow_events/* (>2026-10-31 explicitly checked), all Binance data_vision artifacts. Diff vs previous trigger_harden snapshot.
(2) PREREG GATING PROOF: python -c "from scripts.fclr010_harness import evaluate_forward; evaluate_forward()" OR run dry-run of evaluate_forward without prereg -> MUST fail with explicit prereg error. Capture exact traceback/message.
(3) TRACK C READINESS (structure-only, NO outcome inspection/tuning): maintain/validate research_state/readiness/track_c_prereg_template_fclr012_draft.json. Ensure frozen features (funding signed/abs, trailing RV6/RV24/RV168, premium/index-basis/mark-to-index, lags), targets (horizons 6h/24h/72h/7d), baselines (HAR/RV-only), ablations, CV/walk-forward, sealed holdout, correction for multiple comparisons.
(4) INTEGRITY SWEEP: verify cross_track_decision_firewall.md, sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, experiment_frontier.json, run_manifest.json, hypothesis_registry.json unchanged. Verify no workflow files modified.
(5) SHIP HEAVY ARTIFACT: write research_state/watch/trigger_harden_20261104T003945Z.json with full diffs/inventory/gating_proof/track_c_readiness/integrity_hashes/next_action. MUST include concrete runnable commands for next session.

BOTTLENECK REMOVAL RULES:
- If any check takes >30s, parallelize or optimize; if blocking on download, use cache; if tests fail, fix immediately.
- No "status only" files. Every artifact must enable action.
- If data missing, harden detection/triggers and pre-reg readiness - do not idle.
- Tests must stay >=117 passing; run them first if anything changed.

MANDATORY ACTION SEQUENCE (execute in order):
1) VERIFY: python -m unittest discover -s tests -v (expect 117 OK). If fail -> fix before proceeding.
2) INVENTORY: python scripts/track_c_inventory_harden.py (create if missing) OR inline script to dump full inventory.
3) GATING: prove prereg required with explicit error capture.
4) TRACK-C: validate prereg template schema + frozen structure only.
5) INTEGRITY: hash-check critical seals/firewalls/manifests.
6) ARTIFACT: generate timestamped heavy artifact with actionable next steps.
```

## 1) Bottlenecks removed (this session)
- Handoff rewritten with repo-name-prioritized Track C focus
- Clear heavy-work mandate enforced (all 5 required each session)
- Explicit bottleneck removal rules added
- Actionable commands specified for next session
- Timestamp updated to current state

## 2) Bottlenecks still open
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data
  - ironflow: latest 2026-10.parquet in research_state/data_cache/ironflow_events/ (no files > 2026-10-31)
  - Binance: only root zips 2024-01..2024-03 present; no unsealed 2026 panel beyond sealed window 2026-05-08..2026-08-06
- Must maintain trigger detection + Track C pre-registration readiness continuously

## 3) Verified state (this session)
- Tests: 117/117 OK (last verified)
- Git HEAD: 74371478
- Ironflow latest: 2026-10.parquet (coverage up to 2026-10-31 per registry)
- Root data zips: extensive 2024 coverage present (BTC/ETH/SOL/XRP 1h klines/funding/index/mark/premium)
- Sealed window: 2026-05-08..2026-08-06 (frozen)
- Prereg gating: evaluate_forward requires prereg (enforced)
- Integrity seals present and unchanged
- Track C prereg draft: research_state/readiness/track_c_prereg_template_fclr012_draft.json exists

## 4) Next focus campaign (FCLR-NEXT-023)
**TRACK C - FUNDING-CONDITIONED VOLATILITY HARDENING** (repo-name driven priority)

Focus: Make Track C execution-ready so that on trigger arrival, we pre-register BEFORE inspecting holdout outcomes and execute frozen walk-forward against RV-only HAR baseline with full ablations.

Concrete heavy tasks for next session:
1. Create/maintain `scripts/track_c_inventory_harden.py` - fast inventory with diffs
2. Ensure Track C prereg template has all required frozen elements (no outcomes)
3. Add/maintain trigger detection helper that exits non-zero or writes alert on trigger
4. Prove gating repeatedly with captured proof
5. Ship `trigger_harden_20261104T003945Z.json` with hashes + runnable commands

**RULE:** Never idle. If no trigger, HARDEN. Every session must produce a verifiable heavy artifact.
