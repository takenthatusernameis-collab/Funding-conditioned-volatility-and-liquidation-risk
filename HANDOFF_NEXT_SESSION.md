# HANDOFF — Funding-conditioned-volatility-and-liquidation-risk
**Single durable handoff / initial task message for next agentic work session**
**Timestamp (UTC):** 2026-11-11T08:44:03Z
**Repo:** /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk

## Repo-priority state (evidence-backed, do not relitigate)
- **Repo priority:** Funding-conditioned volatility + liquidation risk → Track A (observed liquidation labels) is the claim-worthy track; Tracks B/C concluded NOT_SUPPORTED.
- **Track A — Observed liquidations: UNBLOCKED_GO_SOURCE.** `ironflow/hyperliquid-liquidations` adjudicated GO per Phase 3 rubric (CC BY 4.0, unauthenticated HF bulk parquet, no requester-pays, complete months 2025-06..2026-10 with 164–353 `*-PERP` markets/month, schema mappable to FCLR-010/H004, provenance in-repo). Experiment `TRACKA-HL-20261111T073000Z` preregistered pre-outcomes at `research_state/tracka_prereg_hyperliquid_2026.json`. Split boundaries frozen in `research_state/run_manifest.json`. Hyperliquid-native only; no Binance/2024 conflation; no sealed-holdout reuse.
- **Track B — Modeled breach proxy:** CONFIRMATORY_COMPLETE, NOT_SUPPORTED (TB1 degenerate/zero test breaches; TB2 gate NOT_MET: LogLoss B1=0.292447→C2=0.287540 +1.68% <2%, 95% CI crosses zero, Holm fails, 2 test blocks <3). Not observed liquidations. No active blocker; no further Track B work.
- **Track C/H1 — Funding-conditioned volatility:** NOT_SUPPORTED on all claim-worthy local panels (FCLR-003/008/009/012-V/013/014). No active blocker; no further Track C work.
- **Program:** `ACTIVE` (Track A unblocked by ironflow GO). Bottlenecks cleared: Tracks B/C concluded (NOT_SUPPORTED); Track A unblocked (ironflow GO).
- **Latent precondition:** Track A alignment market/funding/price context requires an admissible unauthenticated Hyperliquid source — prove admissible provenance/coverage or document blocker in `research_state/tracka_hl_alignment_blocker.md`; Binance 2024 zips are inadmissible for Track A (no Binance/2024 conflation).

## Local data inventory (evidence-backed)
- **Ironflow liquidation events** (observed, unauthenticated HF parquet): `research_state/data_cache/ironflow_events/` — 18 monthly parquet files 2025-05.parquet through 2026-10.parquet (2025-05 partial, 2025-06..2026-10 complete). Schema: timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash.
- **Hyperliquid fundingHistory** (unauthenticated API): `research_state/data_cache/hyperliquid_funding/` — 9 symbols (BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI) JSON files from `https://api.hyperliquid.xyz/info` (type=fundingHistory).
- **Gap:** Hyperliquid market data (mark price, index price, premium index, OHLCV klines) for the same 2025-06..2026-10 window and overlapping symbols — must be sourced from admissible unauthenticated Hyperliquid-native sources only. Binance Vision data is inadmissible for Track A.

## Singular next task — TRACKA-HL Phase 4 (heavy, execute immediately)
Objective: build aligned Hyperliquid liquidation + market/funding/price panel from admissible unauthenticated sources, run pre-registered evaluation per `research_state/tracka_prereg_hyperliquid_2026.json`, produce auditable verdict artifact.

### Immediate steps (in order)
1. **Verify prereg freeze is intact** — confirm `research_state/tracka_prereg_hyperliquid_2026.json` and `research_state/run_manifest.json#TRACKA-HL-20261111T073000Z` split boundaries are unchanged and `frozen_before_outcomes: true`. Do NOT inspect outcomes before this check.
2. **Source and validate alignment data** — identify admissible unauthenticated Hyperliquid-native market/funding/price sources (mark price, index price, premium index, OHLCV klines) covering 2025-06..2026-10 for symbols overlapping ironflow events. Prove provenance (URL, access date, hash/ETag, license, terms) and coverage. If alignment data is inadmissible or unavailable, document the blocker in `research_state/tracka_hl_alignment_blocker.md` with evidence and stop cleanly — do not fabricate, do not fall back to Binance/2024.
3. **Build aligned analysis panel** — merge ironflow observed liquidation events (2025-06..2026-10) + compatible Hyperliquid market/funding/price context from Step 2, with full provenance (URL, access date, hash/ETag, terms). Label: notional_usd-weighted liquidation event count per symbol per 24h UTC bucket (observed, not modeled/proxy/synthetic). Ensure Hyperliquid-native only; no Binance/2024 conflation; no sealed-holdout reuse.
4. **Run pre-registered evaluation** — leakage/split/integrity checks per prereg; QLIKE on observed liquidation intensity; primary contrast C2 vs B1; materiality gate: ≥2% relative reduction, 95% CI excludes zero, ≥5 paired instruments, ≥3 non-overlapping 30-day test blocks (per split boundaries: train 2025-06-01..2025-11-30, val 2025-12-08..2026-01-31, test 2026-02-08..2026-10-31 with 7-day embargo).
5. **Atomically update state** — `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_liquidation_forecast), `research_state/run_manifest.json` (TRACKA-HL entry). Write verdict artifact `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md`.

### Forbidden (hard constraints — violation = failed handoff)
- No threshold-shopping on test set.
- No sealed-holdout reuse (FCLR-002/FCLR-003/Track B/C test sets sealed).
- No Binance/2024 conflation (Hyperliquid only, 2025-06..2026-10 panel).
- No modeled/proxy/synthetic liquidation labels (observed ironflow events only).
- No outcome inspection before prereg freeze verification.
- No risk overlay before forecast gate met.
- No network polling or redundant GETs beyond cached provenance.
- No `.github/workflows` edits.
- No status-only output — must produce auditable verdict artifact or documented blocker.

### Canonical artifacts (read/write)
`HANDOFF_NEXT_SESSION.md` (this file), `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/ironflow_probe_20261111T015524Z.json`, `research_state/ironflow_probe_digest_latest.json`, `research_state/ironflow_monitor_state.json`.

### Verification checklist (run before/after substantive changes)
- `python scripts/check_tracka_scope_registry_drift.py --json` (pass True)
- Provenance check: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`

## Handoff acceptance criteria (next agent must satisfy)
- **Either** auditable verdict artifact `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md` written with full evaluation trace (QLIKE scores, CIs, paired instrument counts, test block counts, gate pass/fail) **or** documented blocker `research_state/tracka_hl_alignment_blocker.md` with evidence that no admissible unauthenticated Hyperliquid market/price source exists for the required window/symbols.
- All canonical state files atomically updated (experiment_frontier.json, hypothesis_registry.json, run_manifest.json).
- Prereg freeze verified intact before any outcome computation.
- Zero forbidden actions taken.
- Output is heavy execution artifact, not status report.

(End of file)