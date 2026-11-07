# Local Data Admissibility Audit (2026-11-07T13:05Z)

**Scope:** deterministic local scan only. **No network, no fetch, no credentials/paid/manual/API keys/auth bypass.** Not a claim run; not outcome inspection.

## Command context
- Repo: `Funding-conditioned-volatility-and-liquidation-risk` (git `fba0d21b` baseline at scan start).
- Integrity gates at audit time: `unittest discover` 732/732 OK; canonical 3/3 OK; `tracka_resume_check` pass/network:false/writes_real_research_state:false.

## Observed local market-data artifacts (root/repo-local)
| Asset | 1h kline daily zips (2024) | Funding dirs/zips (2024) | Date span observed | Schema spot-check |
|---|---:|---:|---|---|
| BTCUSDT | 90 | 2024-01,02,03 dirs+zips | 2024-01-01..2024-03-30 | `open_time,open,high,low,close,volume` (Binance-Vision-style) |
| ETHUSDT | 90 | 2024-01,02,03 | 2024-01-01..2024-03-30 | same |
| BNBUSDT | 90 | 2024-01,02,03 | 2024-01-01..2024-03-30 | same |
| SOLUSDT | 89 | 2024-01,02,03 | 2024-01-01..2024-03-29 | same |
| XRPUSDT | 89 | 2024-01,02,03 | 2024-01-01..2024-03-29 | same |

## Observed local liquidation artifacts
- `research_state/data_cache/liquidations_full_20260807.csv` — single-day context only. **Insufficient** for Track A confirmatory GO (needs ≥5 symbols, ≥3 non-overlapping 30-day blocks, verified provenance/license/schema/coverage/census semantics where required).

## Admissibility decision (GO/NO-GO)
- **2024 1h+funding roots (2024-01..03): NO-GO for confirmatory reopen as-is.**
  - Rationale: overlaps consumed/sealed FCLR-002/003 windows (`evaluation_summary_FCLR002.md`: 2024-01-01..2024-09-30; `evaluation_summary_FCLR003.md`: 2024-01-01..2024-12-31). Reuse without isolation risks contamination/sealed-holdout reuse.
  - **Only permissible path:** a new experiment fully **PREREGISTERED before any outcome inspection** on a **non-consumed/non-confounded boundary** with explicit provenance/licensing, frozen splits/boundaries/hashes, leakage controls (chronological, purge/embargo≥max horizon, train-only normalization, missing!=0). Absent that prereg, exclude from confirmatory claims.
- **Observed-liquidation single-day cache: NO-GO.**
- **Track A:** BLOCKED/NO TRIGGER (ironflow `data_through=2026-10`; 2026-11..2027-02 absent). **No reprobe.**

## Required next step
Acquire/identify **NEW admissible unauthenticated** data meeting `research_state/next_data_discovery_plan.md` GO checklist, or remain NO-GO and perform substantive non-claim hardening with green gates. No status-only churn.
