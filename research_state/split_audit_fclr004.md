# Split Audit for FCLR-004
Timestamp: 2026-10-29T21:51:30Z
Auditor: Agent
Scope: 5-symbol common panel (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), markPriceKlines 1h

## Frozen partitions (all used)
- FCLR-001/002 (split_boundaries): train 2024-04-01..2024-06-08, val 2024-06-16..2024-07-15, test 2024-07-23..2024-09-30
- FCLR-003 (split_boundaries_fclr003): train 2024-04-01..2024-07-23, val 2024-07-31..2024-09-24, test 2024-10-02..2024-12-31

## Embargo/purge gaps (checked)
- 2024-06-09..2024-06-15: checked - used by adjacent partitions (overlap)
- 2024-07-16..2024-07-22: checked - used/overlapped
- 2024-07-24..2024-07-30: checked - used/overlapped
- 2024-09-25..2024-10-01: 09-25..09-30 used by FCLR-001/002 test; 10-01 unused (1 day only)

## Result
- Unused days in 5-symbol common panel: 1 (2024-10-01)
- Longest contiguous unused window: 1 day
- No window >= 90 days exists outside all frozen partitions
- No window >= 30 days exists outside all frozen partitions
- FCLR-003 test (2024-10-02..2024-12-31) is the only frozen window meeting >=3 non-overlapping 30-day blocks for 24h, but it is sealed/used by FCLR-003

## Conclusion
Cannot construct a valid test window for FCLR-004 that: (1) has >=3 non-overlapping 30-day blocks for 24h, (2) uses >=5 instruments, (3) has no timestamp overlap with any frozen partition. Horizon change to 6h does not create new unused timestamps. Reusing sealed holdouts is forbidden. Therefore FCLR-004 cannot meet the gate requirements as specified.
