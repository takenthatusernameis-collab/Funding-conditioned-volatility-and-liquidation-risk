# FCLR-014 Local Cache Provenance Decision (2026-11-07T13:31:02Z)

**Scope:** GO-candidate months in `research_state/data_cache/` — 19 months `2025-01..2025-12, 2026-01..2026-06, 2026-10`, 5 symbols (BNBUSDT,BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT), `1h` + `fundingRate` zips (2970 files; inventory `fclr014_cache_inventory_20261107T133102Z.json`, `manifest_entries_sha256=f37ccfccc628e6c647eed291f4a8de3cf3fdf77044ffa8a73371a3dfa326b0f7`). **Deterministic local audit only; no network/fetch/credentials/paid/manual/API keys/auth bypass. No outcome inspection.**

## Admissible evidence reviewed
- `research_state/binance_source_probe.md` (2026-10-25): verifies **unauthenticated HTTP 200** + SHA256/schema for **2024-01** Binance Vision UM futures (`fundingRate` monthly, `markPriceKlines/indexPriceKlines/premiumIndexKlines/klines` daily). **Does not document 2025+ months.** No liquidation labels; forced-liquidation endpoint restricted (451) in that environment.
- Local zip schema spot-checks (Binance-Vision-style): `BTCUSDT-fundingRate-2025-06.zip` → `calc_time,funding_interval_hours,last_funding_rate`; `BTCUSDT-1h-2025-06-14.zip` → kline header `open_time,open,high,low,close,...`; `ETHUSDT-fundingRate-2026-04.zip` / `ETHUSDT-1h-2026-04-01.zip` consistent. Schema consistency is **necessary but not sufficient** evidence of provenance/license.
- No admissible local artifact found tying 2025-01..2026-10 cached files to an unauthenticated retrieval log, source URL manifest per file/month, license/terms acceptance record, or ETag/revision provenance for those months.

## Exclusions preserved (confirmatory contamination guard)
- **CONSUMED/EXCLUDED:** 2024-01..2024-12 (FCLR-002/003).
- **EXCLUDED:** 2026-07..2026-09 (FCLR-013/Q3 context).
- **PARTIAL/EXCLUDED:** 2026-11 (1h only, no fundingRate for panel completeness). Track A blocked/no trigger; Track B closed/inconclusive.

## Decision
**NO-GO FOR CONFIRMATORY CLAIMS on cached 2025+ GO-candidate months (provenance UNVERIFIED).** Local presence ≠ admissible GO. The cache cannot support frozen confirmatory Gate 4 claims until:
1. Provenance/licensing/unauthenticated origin is documented from **admissible evidence** for the specific 2025-01..2026-10 files/months (source, exact unauthenticated retrieval path, terms/license, no credentials/paid/manual/bypass, checksums/hashes or equivalent provenance).
2. Coverage/completeness/census/leakage isolation verified; **FCLR-014 prereg frozen before outcomes** on a non-consumed/non-confounded boundary (≥3 non-overlapping 30-day test blocks), committed input manifest/hashes, frozen splits, purge/embargo≥max horizon, train-only normalization, missing!=0, `frozen_before_outcomes=true`.
3. Only then: bounded deterministic outcome evaluation + leakage audit; preserve negatives/inconclusive. **Do not overwrite FCLR-013/FCLR-003/v3 anchors.**

## Heavy-work fallback (mandatory when NO-GO; no stalling)
Future sessions MUST NOT re-probe Track A and MUST NOT run claim outcomes on unprovenanced cache. Each session executes provenance verification and, on continued NO-GO, ships **≥1 substantive hardening/test/guardrail with green gates** (e.g., guardrails blocking consumed/confounded windows 2024-01..12, 2026-07..09 and unprovenanced manifests in FCLR-014 tooling; canonical integrity; fail-closed CLIs) and records evidence in `AGENT_HANDOFF.md`, then stops cleanly.
