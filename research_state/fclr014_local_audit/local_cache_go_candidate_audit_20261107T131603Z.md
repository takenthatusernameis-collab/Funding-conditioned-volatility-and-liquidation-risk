# Local Cache GO-Candidate Audit (deterministic, local only) — 2026-11-07T13:16:03Z

**Scope:** `research_state/data_cache/` inventory only. **No network/fetch/credentials/paid/manual/API keys/auth bypass. No claim run. No outcome inspection.**

## Consumed/sealed windows (must not contaminate confirmatory claims)
- FCLR-002: 2024-01-01..2024-09-30 (consumed)
- FCLR-003: 2024-01-01..2024-12-31 (consumed)
- FCLR-013: 2026 Q3 (2026-07/08/09) consumed in test/context — **EXCLUDE from any new confirmatory reuse unless fully preregistered on a non-confounded boundary with explicit isolation**
- v3 manifest exists but CI spans 0 (NOT claim-worthy); treat its data handling as separate from new confirmatory claims.

## Inventory summary
- **19 months** with 5 symbols (BNBUSDT,BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT) and both `1h` + `fundingRate` zips: **2025-01..2025-12, 2026-01..2026-06, 2026-10** → `GO_CANDIDATE_LOCAL` (local presence only).
- 2024-01..2024-12: present but **CONSUMED/EXCLUDED** (overlaps FCLR-002/003).
- 2026-07..2026-09: present but **EXCLUDED** (FCLR-013/Q3 context).
- 2026-11: partial (1h only, no fundingRate).

Machine-readable: `research_state/fclr014_cache_candidate_inventory_20261107T131603Z.json`.

## Schema spot-checks (local zip inspection)
- `BTCUSDT-1h-2025-06-01.zip` → `open_time,open,high,low,close,volume,...` (Binance-Vision-style).
- `BTCUSDT-fundingRate-2026-04.zip` → `calc_time,funding_interval_hours,last_funding_rate` (Binance-Vision-style).

## Admissibility status
**NOT CONFIRMED ADMISSIBLE FOR CONFIRMATORY CLAIMS.** Local presence ≠ GO. Required before any confirmatory run:
1. **Provenance/licensing/unauthenticated origin** documented (source, retrieval path, terms/license, no credentials/paid/manual/bypass). *Unverified this session.*
2. **Coverage/completeness/census** verified (no gaps, symbol coverage, funding alignment; liquidation labels irrelevant for Track C volatility but document scope).
3. **Leakage/sealed-window isolation**: exclude 2024 consumed windows and 2026 Q3 FCLR-013 context; frozen splits; purge/embargo ≥ max horizon; train-only normalization; missing!=0.
4. **PREREG before outcomes** on a non-consumed/non-confounded boundary (hashes, boundaries, primary/secondary, negative-result handling). **Do not inspect outcomes before prereg is frozen/committed.**

## Proposed heavy next step (P0)
Draft and freeze **FCLR-014** pre-registration for Track C Gate 4 on a **non-consumed** candidate panel (e.g., 2025 full year or a pre-specified 2025 train/val/test with ≥3 non-overlapping 30-day test blocks) **only after** provenance/licensing verification is documented. If provenance cannot be verified from admissible unauthenticated evidence, treat cache as **NO-GO for confirmatory claims** and pursue §16 discovery (no network in claim runs; discovery must follow RESEARCH_PROMPT constraints).
