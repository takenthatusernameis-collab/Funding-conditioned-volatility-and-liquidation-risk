# Evaluation Summary — FCLR-LIQ-010-CONFIRM-20261113T063000Z

Generated: 2026-11-13T06:59:53Z
Verdict: **NOT_REPLICATED**

## Primary (C2 vs B1, Brier, pooled test)

- mean diff (C2 - B1): -0.000690 (negative = C2 better)
- 95% CI: [-0.001106, -0.000316]
- relative reduction: 0.50%
- n: 64056
- days: 157

## Checks

- materiality_ge_2pct: False
- ci_excludes_zero_improving: True
- instruments_ge_5: True
- blocks_ge_3: True
- loio_ge_4_of_5: False
- placebo_pass: False
- leakage_audit_pass: True

## Universe: 17 symbols with cached funding

The sealed FCLR-010 used 199 instruments with live access; only 17 retain cached funding offline. This is an honest narrower recompute, not a re-score.
