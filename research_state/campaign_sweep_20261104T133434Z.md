# CAMPAIGN SWEEP (Block 1 of 4 - MANDATORY)
Timestamp (UTC): 20261104T133434Z
Git SHA (HEAD): f53daa1e
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 - TRACK C (funding-conditioned volatility) matches repo name

## 1) AGENT_HANDOFF.md vs run_manifest.json reconciliation
- AGENT_HANDOFF.md (current): States Track C "NOT_SUPPORTED" was STALE, superseded; FCLR-011 COMPLETE FORECAST_GATE_PASSED (C2 vs B1 -4.94% rel QLIKE, CI [-0.032546,-0.001418] excl zero). Forward FCLR-012-V INCONCLUSIVE (Binance archive ends 2026-11-02, 0 blocks). Track A COMPLETE_SEALED FCLR-010 PASS, blocked on ironflow >=2026-11. Track B NOT_SUPPORTED.
- research_state/run_manifest.json: Confirms FCLR-011 status COMPLETE/gate FORECAST_GATE_PASSED with same numbers (rel_reduction 0.0494, ci [-0.032546,-0.001418]), instruments 5, test_blocks 3. FCLR-012-V INCONCLUSIVE/gate NOT_MET (rel_reduction 15.19 but ci [-0.360564,0.059434], 0 blocks). FCLR-010 COMPLETE_SEALED/gate FORECAST_GATE_PASSED (Brier -2.21%, ci [-0.004892,-0.001263], 199 instruments, 5 blocks).
- CONTRADICTION RESOLVED: Earlier stale claim "Track C NOT_SUPPORTED" citing FCLR-003 sealed is incorrect; current authoritative state is FCLR-011 PASS. Handoff now corrected.

## 2) Frozen gates/sealed sets (from run_manifest + artifacts)
Sealed/complete (do NOT re-run/re-tune):
- FCLR-001, FCLR-002 structure references exist in artifacts; FCLR-011 uses frozen splits from prereg pre_registration_fclr011_20261103T111501Z.md
- FCLR-010: COMPLETE_SEALED, FORECAST_GATE_PASSED (Track A). Overlay HYPOTHETICAL_ONLY (FCLR-OVERLAY-001). Hyperliquid-only firewall.
- FCLR-011: COMPLETE, FORECAST_GATE_PASSED (Track C). Panel BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT.
- FCLR-003: mentioned as sealed (Track B NOT_SUPPORTED) - do not re-run.
- FCLR-006,007,008 referenced in constraints - do not re-run sealed outcomes.

Frozen splits (must not change):
- FCLR-011: train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06 (7d purge/embargo). Frozen before outcomes.
- FCLR-012-V: train 2026-08-07..2026-09-16, val 2026-09-24..2026-10-21, test 2026-10-29..2026-11-02 (0 blocks) - INCONCLUSIVE, data blocked.
- FCLR-010: 60/20/20 chronological with 7d purge/embargo, test 2026-05-28..2026-10-31 (5 blocks).

## 3) Current blockers
- Track C forward (FCLR-012-V): Binance archive probe shows ends 2026-11-02 (live probe 2026-11-04T00:45Z -> 404 for 2026-11-03/04). Only 5 days test window = 0 non-overlapping 30-day blocks. CI spans zero. Blocked on data, NOT methodology.
- Track A (FCLR-010): Blocked on new ironflow parquet >=2026-11 (ironflow/liquidations data through 2026-10). Last probe showed tree unchanged (304). No admissible unauthenticated source with >=2026-11 events found.
- Bottlenecks to remove if they block heavy work: ensure tests fast/reliable, clean caches, fix broken imports/paths. No new schedulers/controllers/status-only files.

## 4) Available heavy work NOW (matches repo priority)
Since repo is "Funding-conditioned-volatility-and-liquidation-risk" and Track C gate PASSED on FCLR-011, highest value is deeper funding-conditioned validation on FROZEN FCLR-011/FCLR-002 splits only:
- Regime-stratified QLIKE by funding quartiles per symbol/time
- Funding x RV interaction refinements
- Mark/index premium and mark/EMA24 sensitivity ablations
- Block-bootstrap >=2000 (deterministic), Holm correction
- Must not touch sealed outcomes, must not threshold-shop, must not merge Binance/Hyperliquid

## 5) Evidence from recent commits/tests
- HEAD: f128b157 (chore(kilo): checkpoint agent session x10)
- Tests: 164/164 pass (per handoff). Will verify.
