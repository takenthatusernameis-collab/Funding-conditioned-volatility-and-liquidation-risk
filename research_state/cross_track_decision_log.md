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

## 2026-11-02T01:30:00Z — FCLR-NEXT-002 COMPLETE_NO-GO
- Executed Campaign FCLR-NEXT-002 source discovery across 8 source families. Wrote 8 artifacts: research_state/source_probe_FCLR-NEXT-002_{binance_alt_paths,bybit,okx,deribit,academic_archives,github_raw,huggingface,cryptodatadownload}.md.
- Results: #1 Binance alt paths NO-GO (all 5 paths HTTP 404, fapi forceOrders 451). #2 Bybit NO-GO (no liquidation directory, trades only). #3 OKX NO-GO (static CDN 403, API 404). #4 Deribit NO-GO (connection failed). #5 Academic archives NO-GO (no crypto perp liquidation datasets). #6 GitHub raw NO-GO (code search 401, no census dataset). #7 Hugging Face: ironflow/hyperliquid-liquidations GO (CC BY 4.0, 185-199 symbols, 12 monthly blocks, 2025-11..2026-10, census) — ALREADY USED in FCLR-010, NOT a new source. All other HF datasets NO-GO (ochinimus exhausted, deFi/heatmap wrong type, linxy is price data not labels). #8 CryptoDataDownload NO-GO (no liquidation/futures links).
- Conclusion: NO NEW admissible unauthenticated liquidation source beyond ironflow found. Track A remains open only via ironflow (FCLR-010 COMPLETE, gate PASSED, overlay EXECUTED). All confirmatory gates resolved. Firewall intact. Stable closeout point.

## 2026-11-02T03:17:30Z — FCLR-HEAVY-001 (Track A deepening)
- Campaign started/completed per AGENT_HANDOFF: all 6 steps executed.
- Artifacts: results/fclr_heavy001/*, research_state/fclr_heavy001_*.md/json
- Findings: funding_abs distinct from signed funding; regime-dependent marginal contribution; robust under block-bootstrap >=2000; broad-based across symbols (no critical concentration). No sealed panels modified. Firewall intact. All outputs hypothetical-only.
- Tests: 27/27 PASS. No workflow changes.
- Decision: Track A deepening exhausted within admissible scope; no reopen of closed tracks warranted.
