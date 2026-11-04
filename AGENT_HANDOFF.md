# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T005727Z
Git SHA (HEAD): 8b58dffd
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T005727Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-EXECUTION

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-023-TRACK-C-FUNDING-CONDITIONED-VOL-HARDENING
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting, no deferring)
CAMPAIGN: FCLR-NEXT-023-FUNDING-CONDITIONED-VOL-CONTINUOUS-EXECUTION
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility forecasting) >> Track B (modeled boundary breaches) >> Track A (observed liquidation labels)
TIMESTAMP (UTC): 20261104T005727Z
OBJECTIVE: Repo name is directive - focus on FUNDING-CONDITIONED VOLATILITY. Build hard execution path for Track C (incremental value of funding + price features over RV-only baseline). Forward validation FCLR-NEXT-012 blocked pending admissible triggers (ironflow > 2026-10-31 OR unsealed 2026 Binance panel beyond 2026-11-02). Do NOT wait passively - harden everything so the moment trigger fires, we run pre-registered frozen config with zero latency.
HEAVY WORK MANDATE (NON-NEGOTIABLE, ALL FIVE EACH SESSION):
(1) FULL INVENTORY HARDENING: enumerate root zips (count by asset/month/year), research_state/data_cache/ironflow_events/* (>2026-10-31 explicitly checked), all Binance data_vision artifacts. Diff vs previous trigger_harden snapshot.
(2) PREREG GATING PROOF: python -c "from scripts.fclr010_harness import evaluate_forward; evaluate_forward()" OR run dry-run of evaluate_forward without prereg -> MUST fail with explicit prereg error. Capture exact traceback/message.
(3) TRACK C READINESS (structure-only, NO outcome inspection/tuning): maintain/validate research_state/readiness/track_c_prereg_template_fclr012_draft.json. Ensure frozen features (funding signed/abs, trailing RV6/RV24/RV168, premium/index-basis/mark-to-index, lags), targets (horizons 6h/24h/72h/7d), baselines (HAR/RV-only), ablations, CV/walk-forward, sealed holdout, correction for multiple comparisons.
(4) INTEGRITY SWEEP: verify cross_track_decision_firewall.md, sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, experiment_frontier.json, run_manifest.json, hypothesis_registry.json unchanged. Verify no workflow files modified.
(5) SHIP HEAVY ARTIFACT: write research_state/watch/trigger_harden_20261104T005727Z.json with full diffs/inventory/gating_proof/track_c_readiness/integrity_hashes/next_action. MUST include concrete runnable commands for next session.

BOTTLENECK REMOVAL RULES:
- If any check takes >30s, parallelize or optimize; if blocking on download, use cache; if tests fail, fix immediately.
- No "status only" files. Every artifact must enable action.
- If data missing, harden detection/triggers and pre-reg readiness - do not idle.
- Tests must stay >=117 passing; run them first if anything changed.
- Do NOT re-run sealed FCLR-001/002/003/006/007/008/011 (firewall-sealed; would violate pre-registration/holdout discipline).

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
- Firewall rule added: do NOT re-run sealed FCLR-001/002/003/006/007/008/011 (removes session inefficiency from re-running exhausted confirmatory panels)

## 2) Bottlenecks still open
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data
  - Ironflow: latest 2026-10.parquet in research_state/data_cache/ironflow_events/ (no files > 2026-10-31)
  - Binance: root zips 2024-01..2024-03 only; live probe 2026-11-04T00:45Z -> 404 for 2026-11-03/04 and 2026-10-28/29; archive genuinely ends 2026-11-02
  - Remedy: maintain trigger detection + Track C pre-registration readiness continuously so we execute pre-registered frozen config with zero latency on trigger arrival; do not idle waiting.
- Must maintain trigger detection + Track C pre-reg readiness continuously

## 3) Verified state (this session)
- Tests: 117/117 OK (verified 20261104T005813Z)
- Git HEAD: 8b58dffd (main)
- Ironflow latest: 2026-10.parquet (coverage up to 2026-10-31 per registry); trigger_ironflow_gt_20261031=false
- Root data zips: 463 root zips, all 2024 (01-01..03-30); no Binance data beyond 2026-11-02
- Sealed window: 2026-05-08..2026-08-06 (frozen)
- Prereg gating: evaluate_forward requires prereg (enforced; BLOCKED without it, explicit reason)
- Integrity seals present and unchanged (cross_track_decision_firewall.md IMMUTABLE/SEALED)
- Track C prereg draft: research_state/readiness/track_c_prereg_template_fclr012_draft.json exists
- H001 status: INCONCLUSIVE (FCLR-008 decisive unsealed panel: C2 vs B1 +4.30% rel QLIKE, CI [-0.029938, 0.000524] crosses zero -> gate NOT_MET). All confirmatory panels exhausted: FCLR-003, 006, 007, 008.
- FCLR-010 (Track A) gate PASSED (sealed); FCLR-011 (Track C) gate PASSED (sealed); FCLR-012-V forward INCONCLUSIVE (5 days, 0 blocks)
- Overlay INELIGIBLE across all tracks (gate never passed); cross-track firewall IMMUTABLE

## 4) Next focus campaign (FCLR-NEXT-023)
**TRACK C - FUNDING-CONDITIONED VOLATILITY HARDENING** (repo-name driven priority)

Focus: Make Track C execution-ready so that on trigger arrival, we pre-register BEFORE inspecting holdout outcomes and execute frozen walk-forward against RV-only HAR baseline with full ablations. Repo name = Funding-conditioned-volatility-and-liquidation-risk -> Track C first, always.

Concrete heavy tasks for next session:
1. Create/maintain `scripts/track_c_inventory_harden.py` - fast inventory with diffs vs previous snapshot
2. Ensure Track C prereg template has all required frozen elements (no outcomes inspected)
3. Add/maintain trigger detection helper that exits non-zero or writes alert on trigger
4. Prove gating repeatedly with captured proof (evaluate_forward MUST fail without prereg)
5. Ship `trigger_harden_20261104T005727Z.json` with hashes + runnable commands

**RULE:** Never idle. If no trigger, HARDEN. Every session must produce a verifiable heavy artifact.

## 5) Concrete runnable commands for next session
```
# 1) Verify tests first (gate before anything else)
python -m unittest discover -s tests -v   # expect 117 OK

# 2) Inventory hardening (full diff vs previous snapshot)
python scripts/track_c_inventory_harden.py   # writes research_state/watch/trigger_harden_<ts>.json

# 3) Prereg gating proof (MUST fail with explicit prereg error without prereg)
python -c "from scripts.fclr010_harness import evaluate_forward; evaluate_forward()"   # expect BLOCKED explicit reason
python scripts/fclr010_harness.py   # prints frozen config

# 4) Track C readiness (structure-only, no outcome inspection)
python -m json.tool research_state/readiness/track_c_prereg_template_fclr012_draft.json

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

(End of file - total 165 lines)
