# Track B Admissibility Lock — TB1 (modeled liquidation boundary-breach campaign)

**Timestamp (UTC):** 2026-11-10T13:00:00Z
**Campaign:** FOCUS_CAMPAIGN.md M5.1 (Track B modeled liquidation boundary breaches)
**Window:** 2025-01-01 .. 2026-10-31 (22 contiguous months, 5 instruments)
**Symbols:** BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT

## Selection rationale (no outcome inspection performed)
- Repo-name priority is liquidation risk. Track C (volatility) is concluded NOT_SUPPORTED
  and Track A (observed liquidations) is STRUCTURALLY_BLOCKED. Track B (modeled breach
  proxy on local mark/index/premium klines + funding) is the only untested heavy-work path.
- Window chosen to be **distinct from all previously inspected windows**:
  - NOT FCLR-009 (2025-01-01..2025-12-31 test 2025-06-08..2025-12-31) — holdout-reuse prohibited.
  - NOT FCLR-002 (test 2024-07-23..2024-09-30), NOT FCLR-008 (test 2026-05-08..2026-08-06),
    NOT FCLR-010 (test 2026-05-28..2026-10-31), NOT FCLR-014 (test 2025-05-22..2025-06-07).
  - TB1 test window = **2026-01-01..2026-10-31** (see frozen splits below) — no prior
    Track B/C outcome inspection on this window for a modeled-breach design.
- Full local coverage: mark/index/premium 1h klines + monthly fundingRate, all with
  adjacent sha256 sidecars, provenance machine-verified.

## Machine-verified evidence
- **Provenance:** `provenance_verified=true`, `unmapped_count=0`, `mismatch_count=0`,
  `verified_count=2757` across mark/index/premium klines + funding CSVs for 2024-01..2024-09
  and the full 2025-01..2026-10 cache window (source: adjacent_sidecar). No network.
- **Funding schema:** `all_funding_schema_ok=true`, no missing months for 2025-01..2026-10
  (5 symbols x 22 months).
- **Required series:** `all_required_series_complete=true` (markPriceKlines, indexPriceKlines,
  premiumIndexKlines), `series_gaps` empty for all three series.
- **Panel size:** `symbols_ok=5` (>=5 required), `min_complete_symbol_days=667`,
  `panel_non_overlapping_30d_blocks_estimate=22` (>=3 required).
- **Tooling:** `scripts/trackc_panel_deep_audit_orchestrator.py --window-hint 2025_01..2026_10`
  → `research_state/trackb_TB1_admissibility_2024q1q3.json` (note: filename retains the
  legacy 2024q1q3 token from the fast-candidate scan; the JSON `candidate_months` field is
  authoritative: 2025-01..2026-10).
- **Blockers at lock time:** only `CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES` and
  `CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS` — both procedural, resolved by M5.2.

## Admissibility verdict
**ADMISSIBLE.** All structural prerequisites met. Proceed to M5.2 prereg freeze BEFORE any
outcome/label inspection.