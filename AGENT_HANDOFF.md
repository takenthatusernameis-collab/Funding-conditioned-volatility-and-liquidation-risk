# AGENT HANDOFF — 2026-11-14T03:20:41Z (authoritative, single durable handoff)

## INITIAL TASK FOR NEXT SESSION — `FCLR-VOL-FORWARD-AUDIT-20261114T032041Z`

**Execute heavy work now. Do not rewrite this handoff, do not re-run the old evaluator unchanged, and do not emit a status-only report.**

The previous handoff claimed P1 `FCLR-VOL-FORWARD-2026Q1Q2` was closed as `INADMISSIBLE` with no remaining heavy work. That claim is **stale and wrong**. A later checkpoint fixed an open-interest schema mismatch and produced a 165-coin / 1,485-row panel, but the resulting `EXPLORATORY_NULL` evaluation is **numerically invalid**. The next session must audit, correct, re-run, and harden the evaluation.

### Step 0 — Remove the dependency bottleneck first (mandatory)

Workflow diagnostics repeatedly show `ModuleNotFoundError: numpy/pandas/pyarrow` after dependency-free starts. Do not treat that as a research blocker. Create an isolated environment and use it for every command:

```bash
python3 -m venv /tmp/fclr-venv
/tmp/fclr-venv/bin/pip install -r requirements.txt
```

Use `/tmp/fclr-venv/bin/python` for all verification and research commands. Do not edit `requirements.txt` or `.github/workflows/*`.

### Step 1 — Verify the frozen state before changing anything

This handoff was written at commit `aeda997a4`; the relevant artifacts are:

- Frozen prereg: `research_state/prereg_tracka_vol_forward_2026q1q2_20261114T015222Z.json` (sha256 `9ec5186616553c76db7ee58645a8f5c824bba9e401a0025191b6ac7738a108dd`).
- Invalid latest evaluation: `research_state/evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T02:45:26Z.json` (sha256 `ec2b6f956859b0fb02c6e39f005b1525b4c93289f8f596415641dbc4f6425ddb`).
- Invalid build report: `research_state/tracka_vol_forward_panel_build_report_2026-11-14T02:45:26Z.json` (sha256 `1a17e58f1c17e1bce971b6f89321a270f5541bea2a90446e0b7ca54121936c8a`).
- Panel: `research_state/tracka_vol_forward_panel_2026-11-14T02:45:26Z.parquet` (sha256 `dd4258363ef7aebb0504af9d17b48b98221b8e3e67d49f8944d622294d027b56`).

Confirm the prereg hash is unchanged, then treat the 02:45 evaluation as `EXECUTION_INVALID`. Preserve all prior artifacts; do not delete or overwrite them.

### Step 2 — Confirm the evidence-backed defects

The 02:45 run produced 165 coins, 1,485 rows, and 3/3 test blocks, but its evaluation has four concrete defects:

1. **Test leakage / wrong fit target:** `fit_predict_qlike()` fits OLS on the test rows, despite the prereg requiring causal, train-only scaling and train-fit coefficients.
2. **Unscaled features cause numerical collapse:** raw `rv1h/rv24h/rv168h` values are tiny and unscaled. B1 and C2 predictions collapse to the `1e-12` clip floor, producing absurd QLIKE values around `1e8`–`3e8`, while C1 is near `1`. This is implementation failure, not evidence of a funding signal.
3. **Bootstrap CI is structurally impossible:** `block_bootstrap_ci()` is called on only 9 daily means while `block_h=168`, so it immediately returns `(nan, nan)`.
4. **Holm is fake:** `holm_flags` are computed from a hard-coded `0.5` placeholder p-value, not a real multiplicity-adjusted test.

Therefore `EXPLORATORY_NULL` at 02:45 is **not a valid null**. Do not cite it as a research result, do not promote it, and do not reopen sealed verdicts.

### Step 3 — Implement the minimal prereg-compliant correction

Edit only `scripts/fclr_build_tracka_vol_forward.py` and focused tests. Keep the frozen family definitions, target definitions, windows, horizons, contrasts, and materiality floor unchanged.

- Fit scaling statistics (mean/std) and OLS coefficients on the **train split only** (`2026-01-18` through `2026-03-18 23:00`), then apply them to each test block. Do not fit on test rows.
- Keep features causal and missing values missing; do not forward-fill targets or invent synthetic values.
- Compute the primary bootstrap CI on the **paired per-row QLIKE difference series over the 1,485 test rows**, with `block_h=168` rows and `reps=2000`; report finite `lo`/`hi` and the actual number of observations used.
- Replace the placeholder Holm input with a deterministic paired permutation or bootstrap p-value per primary-family cell, then apply `holm_reject()` across the 12 cells. Do not tune the p-value method to obtain a verdict.
- Emit explicit audit fields in the evaluation JSON/MD: `execution_status`, `train_rows`, `test_rows`, `scaling`, `fit_split`, `bootstrap_n`, `bootstrap_block_h`, and `holm_method`.
- If the corrected run still fails, produce a bounded NO_GO/INCONCLUSIVE with the exact failing minimum. Do not retune thresholds or features.

Run:

```bash
/tmp/fclr-venv/bin/python -m py_compile scripts/fclr_build_tracka_vol_forward.py
/tmp/fclr-venv/bin/python scripts/fclr_build_tracka_vol_forward.py
```

The corrected run must emit a new timestamped panel/build-report/evaluation family. It remains `EXPLORATORY_ONLY` and never promotable.

### Step 4 — Harden the gate so an invalid evaluation cannot pass again

Extend `scripts/fclr_campaign_gate.py` additively and fail-closed:

- Reject non-finite primary bootstrap CIs.
- Reject missing, placeholder, or non-numeric Holm p-values/flags.
- Require `execution_status=VALID_EXPLORATORY` (or the corrected equivalent) and the train/test fit metadata.
- Keep all existing A/B/F checks; do not weaken them.

Add deterministic fixture tests in `tests/test_fclr_campaign_gate.py` proving that NaN CI, placeholder Holm, and missing execution metadata fail the gate, while a valid corrected fixture passes.

### Step 5 — Verification and close-out

```bash
/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all
/tmp/fclr-venv/bin/python -m unittest -q tests.test_fclr_campaign_gate tests.test_active_campaign_gate
```

Then update `research_state/experiment_frontier.json` and this handoff with the **actual** corrected verdict, finite CI, Holm result, new artifact paths/hashes, and exact failing minima if any. Do not claim completion from prose alone.

## NEXT FOCUS CAMPAIGN (ordered, no skipping)

1. **`FCLR-VOL-FORWARD-AUDIT-20261114T032041Z` (P0, execute now):** fix the invalid vol-forward evaluator, re-run on the existing cached panel, and harden the gate. This is the only heavy work that is immediately unblocked.
2. **Gate 4 Branch 1 (P1, trigger-only):** execute only if a valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Do not wait or poll.
3. **New observed-liquidation source (P2, trigger-only):** run a §16 admissibility audit only if a materially new unauthenticated source appears with ≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, provenance/license, observed-only labels, venue consistency, and joinability. Freeze a new prereg before any outcome work.

## Invariants

- Preregister before any outcome inspection or evaluated-target build for a new cell.
- Observed labels and modeled/proxy labels are never conflated; no venue mixing; no forward fill or synthetic data.
- Do not read May 2026 or sealed holdouts for scoring/decisions; do not reopen terminal verdicts.
- No `.github/workflows/*` edits; do not commit raw parquet/caches.
- Do not fabricate artifacts, thresholds, p-values, or verdicts. If blocked, produce a bounded NO_GO with exact failing minima.

## Current state summary (verified 2026-11-14T03:20:41Z)

- The 02:35 handoff's `INADMISSIBLE` closure is **superseded**: the OI schema bug was fixed in checkpoint `51ca490c2`, yielding 165 coins and 1,485 rows.
- The 02:45 `EXPLORATORY_NULL` is **execution-invalid**, not a research null, for the four reasons above.
- Gate and tests currently pass only because the gate does not validate CI finiteness, Holm authenticity, or execution metadata. That is the next engineering gap.
- The strongest alternative explanation is that funding-conditioned volatility has no incremental QLIKE signal on this window; the corrected evaluation must distinguish that from numerical collapse.
- The dominant uncertainty is **evaluation implementation validity**, not data coverage. The new falsification test is the corrected train-only evaluation with finite CI and real Holm flags.
- Highest-information next action: implement Step 3 and Step 4, then re-run and record the corrected verdict.
- Pre-existing unrelated check: `tests.test_tracka_hardening_099.test_root_md_json_count_bounded` reports 416 > 406 at this commit. That is an artifact-count guard, not a research blocker; use the focused commands above and do not delete evidence to make it pass.

## Session log

### 2026-11-14T03:20:41Z
- Audited the post-handoff checkpoint `51ca490c2` and found the durable handoff/frontier stale. Confirmed the 02:45 vol-forward evaluation is invalid because of test-row OLS fitting, unscaled feature collapse, a 9-observation bootstrap with 168-hour blocks, and placeholder Holm p-values. Replaced the false "no heavy work" directive with the executable `FCLR-VOL-FORWARD-AUDIT-20261114T032041Z` campaign and exact acceptance commands.

### 2026-11-14T02:35:42Z
- Prior handoff declared P1 complete as a bounded structural NO_GO. That was based on the 02:33 run before the OI schema fix; it is superseded by the 02:43/02:45 checkpoint and must not be repeated.

### 2026-11-14T01:53:00Z
- Converted the P1 prose path into the runnable frozen-prereg scaffold. Builder was not yet executed at that point.
