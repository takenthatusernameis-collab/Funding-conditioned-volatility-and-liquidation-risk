# CROSS_TRACK_DECISION_LOG (IMMUTABLE FIREWALL)

**Last updated:** 2026-11-01T16:56:00Z
**Firewall:** Hyperliquid ironflow (Track A/observed) ONLY. NO Binance merge. Modeled != observed.

## Track A (Observed liquidations, ironflow Hyperliquid)
- FCLR-010: gate PASSED (C2 vs B1 −0.003077, 95% CI [−0.004892,−0.001263], rel −2.21%, n=199, 5 blocks). SEALED.
- H_COUPLED-001: initial 500 reps PASS (+4.61%, CI [0.002511,0.003158]). ROBUST (>=2000 reps) PASS (this session). Coupled result publishable path.
- Overlay eligibility: MET. Decision: pre-register overlay/position-sizing spec before any outcome inspection; no overlay build/tuning yet.

## Track B (Modeled boundaries)
- CLOSED_NEGATIVE; separation irrefutable.

## Track C (Volatility-only)
- Exhausted/confirmatory closed; H001 NOT_SUPPORTED.

## H002
- PERMANENTLY BLOCKED (SSRN HTTP 403). No further work.
2026-11-01T17:07:48Z | FCLR-OVERLAY-001 PRE-REGISTERED | Created research_state/pre_registration_tracka_overlay_20261101T165900Z.md with frozen bands/multipliers (p_low/p_mid/p_high from dev quantiles), block-bootstrap, gates, no-tuning/no-outcome-inspection constraints. Updated experiment_frontier.json. Firewall: ironflow Hyperliquid only.

2026-11-01T18:30:05Z | FCLR-OVERLAY-001 EXECUTED | Wrote research_state/evaluation_summary_tracka_overlay_001.md with fixed bands/multipliers, dev-only quantiles, block-bootstrap CIs; hypothetical only, no profitability claim. Firewall: ironflow Hyperliquid only.

2026-11-02T00:08:30Z | FCLR-LIQMICRO-003 STARTED | Adversarial leakage/quality audit + robustness sensitivity on FCLR-LIQMICRO-002 panel (ironflow Hyperliquid + Hyperliquid funding). Firewall intact: no Binance merge, no H001/FCLR-003/FCLR-010 re-test. Artifacts: leakage_audit_liqmicro_002.md, robustness_liqmicro_002.md.

2026-11-02T00:13:00Z | FCLR-LIQMICRO-003 COMPLETE | Closeout done. experiment_frontier.json FCLR-LIQMICRO-003 status=COMPLETE with sealed_panel_integrity block (md5 hashes of results/liqmicro_v2/* recorded; mtimes 2026-11-02T00:05 unchanged; verdict UNCHANGED — no rewrites). All 27 tests PASS at HEAD 358cea47. Firewall intact: no Binance merge, no H001/FCLR-003/FCLR-010 re-test, no Track A/B/C label merging. Final gate states: Track C H001 NOT_SUPPORTED (CONFIRMATORY_CLOSED); Track A FCLR-010 gate PASSED / overlay HYPOTHETICAL_ONLY; Track B CLOSED_NEGATIVE; H002 PERMANENT_BLOCK; FCLR-LIQMICRO-002/003 COMPLETE. Resume condition: new admissible unauthenticated liquidation/funding source passing the rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK) OR SSRN H002 methodology accessible — in either case pre-register a new experiment ID BEFORE outcome inspection.

## 2026-11-02T01:04:00Z — FCLR-LIQMICRO-003 CLOSEOUT COMPLETE
- Status COMPLETE. Artifacts: leakage_audit_liqmicro_002.md (PASS), robustness_liqmicro_002.md.
- Sealed panel verified unchanged (md5s recorded). Tests 27/27 PASS.
- Firewall intact: Hyperliquid-only; no Binance; no H001/FCLR-003/FCLR-010 re-test; no Track label merging.
- Resume condition: new admissible unauthenticated liquidation/funding source passing rubric OR SSRN H002 access; pre-register before outcome inspection.
