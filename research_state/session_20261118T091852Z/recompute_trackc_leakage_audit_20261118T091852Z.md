# Recompute — Track C Design A Leakage Audit (session_20261118T091852Z)

- **Timestamp (UTC):** 2026-11-18T09:18:52Z
- **Script:** `recompute_trackc_leakage_audit_20261118T091852Z.py` (stdlib-only: `csv`, `json`, `datetime`, `calendar`, `pathlib`; no numpy/pandas/scipy)
- **Input:** cached ZIP/CSV/dir under `research_state/data_cache/{BTC,ETH,SOL,XRP,BNB}USDT_2024_0{4..9}` (read-only)
- **Network used:** none

## Summary

| Field | Value |
|-------|-------|
| instruments | 5 (BTC/ETH/SOL/XRP/BNB USDT) |
| months_checked | 6 (2024-04..09) |
| funding_files_found | 30 / 30 |
| splits_feasible | true |
| tests_disjoint | true |
| sealed_conflict_months | [] |
| leakage_flags | [] |
| **verdict** | **PASS** |

## Checks
1. Funding-rate CSV presence + monotonic timestamps + interval regularity (8h) — PASS for all 30 symbol-months.
2. 1h kline (plain/mark/index/premium) daily coverage — 24 rows/day, zero missing days across all 5×6 — PASS.
3. 3 chronological non-overlapping 30d test splits, 7d purge/embargo, expanding train — last test ends day 111 of 183-day window — PASS.
4. Tested-window non-conflict vs sealed/holdout (2024-10..12, 2025+) — zero conflict — PASS.

## Reproduce
```bash
python3 research_state/session_20261118T091852Z/recompute_trackc_leakage_audit_20261118T091852Z.py
```
Emits `evidence_audit_20261118T091852Z.json` + `recompute_trackc_leakage_audit_20261118T091852Z.json` in this session dir.