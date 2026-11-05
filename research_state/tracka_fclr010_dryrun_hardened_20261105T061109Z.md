TIMESTAMP (UTC): 20261105T061109Z
STEP: 5) HARNESS HARDENING + DRY-RUN

- Tests exist: tests/test_fclr010_harness.py
- Generated Track A fixtures via scripts/generate_tracka_fixtures.py (train/val/test present)
- fclr010_validate.py enforces preregistration-before-outcomes (correct). Without new data/triggers, no prereg created.
- Adversarial tests present (added previously). Dry-run offline: fixtures OK, harness structure validated.
- Zero-latency on resume: fixtures cached, scripts ready, rubric frozen.

Status: READY (offline). No execution without trigger+prereg.


## Consolidated from older dryrun hardened reports

### tracka_fclr010_dryrun_hardened_20261105T051428Z.md
# Track A FCLR-010 dryrun hardened
ts: 20261105T051428Z
---
## fixtures
Wrote fixtures to /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/tests/fixtures/tracka
  train: 18144 rows, 3024 hours, 6 symbols
  validation: 9792 rows, 1632 hours, 6 symbols
  test: 22608 rows, 3768 hours, 6 symbols

## harness import/test
FCLR-010
