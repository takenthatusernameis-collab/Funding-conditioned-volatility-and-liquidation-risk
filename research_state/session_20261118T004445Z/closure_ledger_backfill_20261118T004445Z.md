# Closure-Ledger Backfill — PLAN (20261118T004445Z)

Campaign: `FCLR-LEDGER-INTEGRITY-02-20261118T000000Z`
Read-only. **Does not mutate the sealed closure JSON.**

## Problem

`research_state/fclr_final_structural_closure_20261116T114626.json`
(sha256 `f2d55756…c0d1`) enumerates 58 experiment rows (`id`, `source_artifact`,
`verdict`) but carries **no consumed train/val/test window metadata**. A reader
cannot tell from the closure JSON alone that 2024-04..2024-12 were consumed by
FCLR-002/003 — the omission FCLR-LEDGER-INTEGRITY-01 fixed in the frontier tool
but did not backfill into the closure record.

## Constraint

RESEARCH_PROMPT §13: never overwrite a sealed artifact. The closure JSON is
sealed. This is a plan only.

## Plan (for FCLR-CLOSURE-LEDGER-COMPLETENESS-01)

Emit a **new, non-authoritative sidecar** `closure_ledger_sidecar_<UTC>.json`
enumerating consumed windows per experiment (FCLR-002, FCLR-003,
FCLR-FWD-VOL-2024Q4-CROSS, FCLR-FWD-VOL-011-CONFIRM, …). Do **not** edit the
sealed closure JSON. Add a validator that cross-checks the sidecar against
`scripts/next_campaign_status.py` `TESTED_WINDOWS`/`BULK_TESTED_WINDOWS` and the
ledger audit, exiting nonzero on any consumed month not enumerated.

## Acceptance test

The FCLR-CLOSURE-LEDGER-COMPLETENESS session must emit
`closure_ledger_sidecar_<UTC>.json` (complete) + `closure_ledger_validator_<UTC>.{py,json}`
(exit 0 on complete sidecar) + `trigger_check_<UTC>.json`.

## Do not

- Do not edit the sealed closure JSON.
- Do not add root-level `research_state/*.md|json` (root at 500/500).
- Do not open any outcome metric, holdout, or `results/*`.