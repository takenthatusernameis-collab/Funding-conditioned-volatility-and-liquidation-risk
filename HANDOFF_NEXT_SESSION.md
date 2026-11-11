# HANDOFF — Funding-conditioned-volatility-and-liquidation-risk
**Single durable handoff / initial task message for next agentic work session**
**Timestamp (UTC):** 2026-11-11T09:17:11Z
**Repo:** /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk

## Non-negotiable state (do not relitigate)
- **Priority:** Funding-conditioned volatility + liquidation risk. **Track A** (observed Hyperliquid liquidations) is the only claim-worthy active track. **Track B** (modeled breach proxy) and **Track C/H1** (funding-conditioned volatility) are concluded **NOT_SUPPORTED** — no further work on B/C.
- **Track A source:** `ironflow/hyperliquid-liquidations` adjudicated **GO** (CC BY 4.0, unauthenticated HF bulk parquet, observed-only). Local labels: `research_state/data_cache/ironflow_events/*.parquet` (2025-05..2026-10, 2,848,413 rows, 468 markets incl. `*-PERP` for BTC/ETH/BNB/SOL/XRP/AVAX/DOGE/LINK/SUI). Prereg (frozen pre-outcomes): `research_state/tracka_prereg_hyperliquid_2026.json` (`TRACKA-HL-20261111T073000Z`, `status: PREREGISTERED_FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes: true`).
- **Program blocker (documented, not resolved):** full 2025-06..2026-10 aligned panel **cannot** be built from currently evidenced admissible unauthenticated Hyperliquid-native sources. Evidence in `research_state/tracka_hl_alignment_blocker.md`: HL `fundingHistory` cached 2025-11..2026-10 only; `candleSnapshot` (mark 1h) ~6–7mo lookback (~2026-05..2026-10); no admissible historical index/premium endpoint identified. Frozen prereg splits (train 2025-06..2025-11 / val 2025-12..2026-01 / test 2026-02..2026-10, 7d embargo) are therefore not executable on a full aligned panel with current sources.

## Bottleneck-removal campaign (HEAVY, inescapable — complete this session)
Objective: close the Track A alignment gap to a **terminal, auditable** outcome. No status-only output; produce a verdict/closure artifact and update canonical state.

### Step 1 — Prereg freeze gate (MANDATORY, before any outcome computation)
- Verify `research_state/tracka_prereg_hyperliquid_2026.json` remains frozen (`frozen_before_outcomes: true`, splits/label/metric unchanged). Record verification in your work log/artifact. **Do not inspect outcomes** before this passes.

### Step 2 — Exhaust path (a): admissible coverage extension (time-boxed, evidence-first)
- Search **in-repo/local cache** for overlooked Hyperliquid-native, unauthenticated, provenance-able market/price/funding data covering 2025-06..2026-10 (inspect `data/`, `research_state/data_cache/`, existing HL scripts: `scripts/hl_coverage_probe.py`, `scripts/hyperliquid_funding_fetch.py`). Note: Binance `*USDT*` / markPriceKlines caches are **not** Hyperliquid-native and cannot be conflated with HL labels.
- If and only if a concrete, admissible unauthenticated HL-native historical source is identified (mark/index/premium/klines/funding back to 2025-06 for overlapping symbols), fetch minimally with full provenance (URL, access UTC, hash/ETag, license/terms) and prove coverage. If no such source is evidenced, **declare path (a) exhausted** citing `research_state/tracka_hl_alignment_blocker.md` + any new probe evidence.

### Step 3 — Force a terminal path (choose one; execute fully)
- **(b) Scope-down with RE-PREREG (preferred if a viable overlap exists):** quantify the maximal overlap where observed HL labels + admissible HL mark/price + admissible HL funding all coexist (current evidence suggests funding 2025-11..2026-10, mark candles ~2026-05..2026-10 → intersection ~2026-05..2026-10; confirm precisely from local artifacts). This **deviates** from frozen prereg → **write a new successor prereg** `research_state/tracka_prereg_hyperliquid_2026_scoped.json` (new experiment_id, frozen pre-outcomes, explicit split boundaries/embargo, symbols, label, baselines B0/B1, models C1/C2, primary contrast C2 vs B1, QLIKE metric, materiality gate ≥2% rel reduction & 95% CI excludes zero & ≥5 paired instruments & ≥3 non-overlapping 30-day test blocks — or explicitly document infeasibility of any gate element given the narrowed window) **before any outcome computation**. If the overlap cannot satisfy minimum prereg power/blocks, path (b) is infeasible → take (c).
- **(c) Terminal closure (if (a) exhausted and (b) infeasible):** produce a conclusive, auditable Track A closure verdict **NOT_SUPPORTED / INCONCLUSIVE_CLOSED_DUE_TO_ALIGNMENT_DATA_INADMISSIBILITY** in `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md`, explicitly tying the closure to prereg constraints and evidenced coverage gaps (no fabricated results). Update `research_state/final_confirmatory_verdict.md` (Track A section), `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_liquidation_forecast), and `research_state/run_manifest.json` to reflect the terminal state.

### Step 4 — If (b) yields a feasible, newly-preregistered panel (heavy execution)
- Build aligned Hyperliquid-native panel (ironflow observed events + admissible HL context) with full provenance; enforce 7d embargo, no leakage, UTC normalization.
- Run pre-registered evaluation (QLIKE, C2 vs B1, materiality gate per successor prereg). Compute outcomes **only after** successor prereg is written/frozen.
- Write `research_state/evaluation_summary_<SUCCESSOR_EXPERIMENT_ID>.md` with full trace (scores, CIs, paired instruments, test blocks, gate pass/fail) and atomically update frontier/registry/manifest/final verdict.

## Hard constraints (violation = failed handoff)
- **No** threshold-shopping on test set. **No** sealed-holdout reuse. **No** Binance/2024 conflation with HL labels. **No** modeled/proxy/synthetic liquidation labels. **No** outcome inspection before prereg/successor-prereg freeze verification. **No** risk overlay before forecast gate met. **No** `.github/workflows` edits. **No** redundant network polling.
- Any panel/split deviation from the frozen prereg **requires re-preregistration before outcomes**.

## Required deliverables (end-of-session, auditable)
1. Path decision recorded: `(a) exhausted` evidence and chosen `(b)` or `(c)` documented (append to `research_state/tracka_hl_alignment_blocker.md` or successor note).
2. **Either** `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md` (closure, path c) **or** successor prereg + `research_state/evaluation_summary_<SUCCESSOR_ID>.md` (path b executed).
3. Canonical state updated atomically: `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, and `final_confirmatory_verdict.md` as applicable.
4. Keep `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md` consistent if further work remains (else mark terminal).

## Canonical artifacts
`HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/ironflow_probe_digest_latest.json`.

## Verification checklist
- `python scripts/check_tracka_scope_registry_drift.py --json`
- `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
