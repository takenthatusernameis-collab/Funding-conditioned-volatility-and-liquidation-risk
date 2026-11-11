# HANDOFF — Funding-conditioned-volatility-and-liquidation-risk
**Single durable handoff / initial task message for next agentic work session**
**Timestamp (UTC):** 2026-11-11T09:10:11Z
**Repo:** /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk

## Repo-priority state (evidence-backed, do not relitigate)
- **Repo priority:** Funding-conditioned volatility + liquidation risk → Track A (observed liquidation labels) is the claim-worthy track; Tracks B/C concluded NOT_SUPPORTED.
- **Track A — Observed liquidations: UNBLOCKED_GO_SOURCE.** `ironflow/hyperliquid-liquidations` adjudicated GO per Phase 3 rubric (CC BY 4.0, unauthenticated HF bulk parquet, no requester-pays, complete months 2025-06..2026-10 with 164–353 `*-PERP` markets/month, schema mappable to FCLR-010/H004, provenance in-repo). Local labels: `research_state/data_cache/ironflow_events/` — 18 monthly parquet, 2025-05..2026-10, 2,848,413 rows, 468 markets incl. `BTC-PERP`..`SUI-PERP`. Experiment `TRACKA-HL-20261111T073000Z` preregistered pre-outcomes at `research_state/tracka_prereg_hyperliquid_2026.json`. Hyperliquid-native only; no Binance/2024 conflation; no sealed-hout reuse.
- **Track B — Modeled breach proxy:** CONFIRMATORY_COMPLETE, NOT_SUPPORTED. No further Track B work.
- **Track C/H1 — Funding-conditioned volatility:** NOT_SUPPORTED on all claim-worthy local panels. No further Track C work.
- **Program:** `ACTIVE` (Track A unblocked by ironflow GO). Bottleneck: Track A alignment market/price context is INSUFFICIENT for the full prereg window — documented in `research_state/tracka_hl_alignment_blocker.md`.

## Bottleneck status (resolved to a documented decision point)
The alignment gap has been characterized against admissible unauthenticated Hyperliquid-native sources (https://api.hyperliquid.xyz/info):
- `ironflow` labels: COMPLETE 2025-05..2026-10 (not the bottleneck).
- `fundingHistory`: WORKS, cached 9 symbols, but only 2025-11..2026-10 (missing 2025-06..2025-10).
- `candleSnapshot` (mark-price 1h OHLCV, payload `{"type":"candleSnapshot","req":{"coin","interval":"1h","startTime","endTime"}}`): WORKS but ~6–7 month lookback — only ~2026-05..2026-10 for BTC/ETH/SOL/XRP (2025-11→0 rows, 2026-05→169). No separate historical index-price/premium-index endpoint.
- **Conclusion:** the full 2025-06..2026-10 prereg panel (mark price + funding + liquidations on frozen splits train 2025-06..2025-11 / val 2025-12..2026-01 / test 2026-02..2026-10) CANNOT be built from admissible sources. See `research_state/tracka_hl_alignment_blocker.md` for full evidence.

## Singular next task — TRACKA-HL Phase 4 (heavy, execute immediately)
Objective: resolve the Track A alignment blocker and, if coverage can be extended to the full prereg window, build the aligned panel + run the pre-registered evaluation + verdict artifact; otherwise document the closure path per the blocker doc.

### Immediate steps (in order)
1. **Verify prereg freeze is intact** — confirm `research_state/tracka_prereg_hyperliquid_2026.json` (`status: PREREGISTERED_FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes: true`) and split boundaries are unchanged. Do NOT inspect outcomes before this check.
2. **Decide the alignment path** (record the choice in `research_state/tracka_hl_alignment_blocker.md` or a successor):
   - (a) Extend coverage: find an additional admissible unauthenticated Hyperliquid-native source serving mark/index/premium/klines back to 2025-06 for the overlapping symbols; prove provenance (URL, access date, hash/ETag, license, terms) + coverage; then proceed to step 3.
   - (b) Scope-down: build panel only on the overlap where all three exist (~2026-05..2026-10 candles / 2025-11..2026-10 funding). This deviates from the frozen prereg → requires RE-PREREG before any outcome computation; do not compute outcomes on the old frozen prereg with a deviated panel.
   - (c) Close Track A panel as NOT_SUPPORTED due to missing/inadmissible alignment context; this blocker doc is the terminal evidence.
3. **If (a) succeeds: build aligned analysis panel** — merge ironflow observed liquidation events (2025-06..2026-10) + compatible Hyperliquid market/funding/price context with full provenance. Label: notional_usd-weighted liquidation event count per symbol per 24h UTC bucket (observed only). Hyperliquid-native only; no Binance/2024 conflation; no sealed-holdout reuse.
4. **Run pre-registered evaluation** — leakage/split/integrity checks per prereg; QLIKE on observed liquidation intensity; primary contrast C2 vs B1; materiality gate: ≥2% relative reduction, 95% CI excludes zero, ≥5 paired instruments, ≥3 non-overlapping 30-day test blocks (per frozen split boundaries).
5. **Atomically update state** — `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_liquidation_forecast), `research_state/run_manifest.json` (TRACKA-HL entry). Write verdict artifact `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md` (or the documented closure per path (b)/(c)).

### Forbidden (hard constraints — violation = failed handoff)
- No threshold-shopping on test set.
- No sealed-holdout reuse (FCLR-002/FCLR-003/Track B/C test sets sealed).
- No Binance/2024 conflation (Hyperliquid only, 2025-06..2026-10 panel).
- No modeled/proxy/synthetic liquidation labels (observed ironflow events only).
- No outcome inspection before prereg freeze verification.
- No risk overlay before forecast gate met.
- No network polling or redundant GETs beyond cached provenance.
- No `.github/workflows` edits.
- No status-only output — must produce auditable verdict artifact, documented closure path, or documented blocker.

### Canonical artifacts (read/write)
`HANDOFF_NEXT_SESSION.md` (this file), `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/ironflow_probe_20261111T015524Z.json`, `research_state/ironflow_probe_digest_latest.json`, `research_state/ironflow_monitor_state.json`, `research_state/tracka_hl_alignment_blocker.md`.

### Verification checklist (run before/after substantive changes)
- `python scripts/check_tracka_scope_registry_drift.py --json` (pass True)
- Provenance check: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`

## Handoff acceptance criteria (next agent must satisfy)
- **Either** auditable verdict artifact `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md` written with full evaluation trace (QLIKE scores, CIs, paired instrument counts, test block counts, gate pass/fail) **or** documented closure path / blocker in `research_state/tracka_hl_alignment_blocker.md` with evidence.
- Prereg freeze verified intact before any outcome computation; any panel-scope deviation requires re-prereg first.
- All canonical state files atomically updated (experiment_frontier.json, hypothesis_registry.json, run_manifest.json).
- Zero forbidden actions taken.
- Output is heavy execution artifact, not status report.
