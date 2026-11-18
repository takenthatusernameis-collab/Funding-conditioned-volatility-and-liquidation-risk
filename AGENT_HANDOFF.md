# AGENT HANDOFF — 2026-11-18T01:50:38Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T01:50:38Z)

**At a glance — repository `Funding-conditioned-volatility-and-liquidation-risk` → priority is Track C funding-conditioned volatility (repo-name rule).** The program's confirmatory science is genuinely terminal: H001 NOT_SUPPORTED (FCLR-003 sealed negative, FCLR-006 negative, FCLR-011 sealed PASS does NOT replicate forward), Track A externally blocked (no admissible post-2026-10 observed liquidation labels), Track B modeled-boundary inconclusive. **That part is settled and must not be relitigated.** What WAS broken is the *bookkeeping*: the "closed frontier" rested on a tested-window ledger that omitted FCLR-003's sealed test window, so the frontier tool mislabeled 2024-10/11/12 as fresh and invited re-scoring sealed negative data. **That bottleneck has now been fixed in `scripts/next_campaign_status.py` (FCLR-LEDGER-INTEGRITY-01, previous session).** The next session's mandatory heavy campaign is to **independently verify the fix, produce the durable per-month ledger audit, and refresh the outcome-blind trigger-activation package** — not to re-fix, and not to wait idle.

**Rank-0 state (unchanged, do not relitigate):**
- Program: `CLOSED_TERMINAL` — `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; 0/58 rows §17-promotable.
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`).
- **Do not start or re-run any sealed cached-data confirmatory estimand.** Do not re-run FCLR-014, the replication synthesis, the design-frontier certificate, FCLR-013/010/002/003/009/006/008, or any frontier verify-06/07/08+ re-audit.

---

## WHAT WAS FIXED — `FCLR-LEDGER-INTEGRITY-01-20261117T234500Z` (code applied, verified)

**The bottleneck (evidence-backed):** `scripts/next_campaign_status.py` `TESTED_WINDOWS` omitted FCLR-003's sealed NEGATIVE test window (2024-10-02..2024-12-31). Consequences:
- `markfund_frontier()` reported `individually_feasible_months = ['2024-10','2024-11','2024-12','2025-01']` and `n_individually_feasible=4` — treating FCLR-003's *test* months as fresh.
- `ready_windows()` labeled 2024-04/05/2025-01 as `inside_tested_window=False`.
- A future agent reading `--json` could re-score sealed FCLR-003 test data — a §17 violation.

**Fix applied (tracked code + tests):**
- `scripts/next_campaign_status.py` — added `("2024-10-02", "2024-12-31", "FCLR-003 sealed NEGATIVE test window (NOT_SUPPORTED)")` to `TESTED_WINDOWS` with an explanatory comment.
- `tests/test_next_campaign_status.py` — updated `test_markfund_frontier_reproduces_certified_closed_verdict` and `test_markfund_frontier_in_json_output` to the corrected verdict, and added `test_fclr003_sealed_test_months_not_reproposed` as a regression guard.
- **Corrected frontier (verified):** `n_individually_feasible=1` (`2025-01` only), `max_mutually_non_overlapping=1`, `n_overlapping_pairs=0`, `campaign_feasible_non_overlapping=False`. The only individually-feasible month is 2025-01 (its 30-day train is FCLR-003 test, allowed as pre-test history), a single block < 3. **Frontier remains closed, now for the honest reason.**
- **Tests:** `tests.test_next_campaign_status` 22/22 OK; all 77 frontier-dependent tests (`test_fclr014_anchor_integrity`, `test_fclr_design_feasibility`, `test_fclr_final_structural_closure`, `test_tracka_hardening_143`, `test_fclr018_gate4_prereg_readiness_matrix`) OK. Full discovery 1129/62/9/14 — same environment-dependent baseline (all errors are `ModuleNotFoundError: numpy`), +3 tests from this change.
- **Gates:** `check_handoff_heavywork_gate.py --json` PASS (`handoff_stale=false`); `check_tracka_scope_registry_drift.py --json` PASS (196/196). Timestamp-only cache side effect reverted.

**Still open (this is the next campaign's job):** the durable per-month ledger audit artifact does not yet exist, and the closure JSON's enumerated ledger still lacks FCLR-002/003 window rows. The code fix is in; the *evidence artifact* and *closure-ledger backfill* are not.

---

## MANDATORY NEXT CAMPAIGN — `FCLR-LEDGER-INTEGRITY-02-20261118T015038Z` (outcome-blind, heavy, non-avoidable)

### Deliverables (ALL required; a trigger-check-only or handoff-only session does NOT count)

Create `research_state/session_<UTC>/` (real UTC; `research_state/` root is **500/500**, so **all new artifacts go in the session dir only**). Produce, in order:

1. **`ledger_audit_<UTC>.{py,json,md}`** — outcome-blind, read-only. For every month 2024-01..2026-10, compute the union of train/val/test months consumed by FCLR-001/002/003/006/007/008/009/011/013/014 and all `FCLR-FWD-VOL-*` / `FCLR-LIQ-*` cells, from the sealed `evaluation_summary_*` files and `TESTED_WINDOWS`/`BULK_TESTED_WINDOWS`. Emit a per-month table: `{month, consumed_by:[experiment_ids], phase:[train|val|test|embargo], frontier_says_tested:bool}`. **Headline assertion:** every month in the FCLR-002/003 train/val/test union is marked consumed (specifically 2024-04..2024-12).

2. **`frontier_recompute_<UTC>.{py,json,md}`** — independently re-run the corrected `next_campaign_status.py` logic and **confirm** the closed verdict: `n_individually_feasible=1` (2025-01), `max_mutually_non_overlapping=1`, `campaign_feasible_non_overlapping=False`. State the arithmetic that closes it. **Do NOT re-derive a different frontier; the fix is applied — verify, do not re-fix.** If you find the fix regressed, revert to `git show HEAD:scripts/next_campaign_status.py` and re-apply the single `TESTED_WINDOWS` row.

3. **`closure_ledger_backfill_<UTC>.{json,md}`** — the minimal plan to add FCLR-002/003 consumed windows to the closure JSON's enumerated ledger (`fclr_final_structural_closure_*.json` `rows`/reopen metadata) so the omission is caught. Record as a plan; do NOT mutate the sealed closure JSON.

4. **`trigger_check_<UTC>.json`** — one-shot, no network, no polling. Read `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json`. Record timestamp, each trigger status, `data_through`, post-2026-10 classifications. Current: all four triggers `OPEN`; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/12, 2027-01 `CONFIRMED_ABSENT`.

5. **`trigger_activation_readiness_<UTC>.{json,md}`** — refresh the outcome-blind trigger-activation certificate from `session_20261117T215904Z/trigger_activation_readiness_20261117T215904Z.{json,md}` (promotable=false, program_status=CLOSED_TERMINAL, four trigger contracts with power floors: Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`). Carry the four pre-sized contracts forward; add the corrected-frontier reference.

6. **`evidence_audit_<UTC>.md`** — confirm the carried-forward bundles are present and unmodified (FCLR-003 sealed negative; FCLR-011 recompute; frontier certificates `session_20261117T193323Z` + `session_20261117T194457Z`; trigger-readiness `session_20261117T215904Z`; the corrected `scripts/next_campaign_status.py`). Record exact files and command outputs.

7. **Gates + suite capture (in the session dir):** `check_handoff_heavywork_gate.py --json`, `check_tracka_scope_registry_drift.py --json`, targeted suite, and `python3 -m unittest discover -q` to completion. Record count/skip/error/EXIT. **Baseline is environment-dependent** (targeted 82/6/0; discovery 1129/62/9/14/EXIT 1). Never treat a missing-dependency error set as green. Revert timestamp-only side effects to tracked files.

### Definition of done (what makes this heavy work count)

- The session dir contains artifacts 1–7 above with real numeric content (not a copied bundle).
- `ledger_audit` **proves** 2024-04..2024-12 are consumed and cites the exact `next_campaign_status.py` `TESTED_WINDOWS` line and the exact `evaluation_summary_FCLR002/003.md` lines.
- `frontier_recompute` **reproduces** the corrected closed verdict (`n_individually_feasible=1`, `max_mutually_non_overlapping=1`, `campaign_feasible_non_overlapping=False`).
- Gates pass (`check_handoff_heavywork_gate.py --json` shows `handoff_stale=false` once this session id is recorded in this handoff before the final gate capture).
- **Do NOT re-fix the code.** The fix is applied and tested; re-fixing is a regression. If you believe the fix is wrong, revert to `HEAD` and re-apply only the single `TESTED_WINDOWS` row, then show red→green.

---

## Read first (in order)

1. `RESEARCH_PROMPT.md` §16 (adaptive feasibility / progress without weakening evidence) and §17 (promotion conditions).
2. `research_state/evaluation_summary_FCLR002.md`, `evaluation_summary_FCLR003.md` (the omitted train/val/test windows).
3. `scripts/next_campaign_status.py` — `TESTED_WINDOWS` (lines ~74–88), `BULK_TESTED_WINDOWS`, `markfund_frontier()`, `disjoint_block_frontier()`, `ready_windows()`, `MIN_DESIGN_DAYS=127`.
4. `tests/test_next_campaign_status.py` — the assertions that pin the current (wrong) frontier verdict; these must be updated by the follow-up.
5. `research_state/fclr_final_structural_closure_20261116T114626.{md,json}` (the closure ledger that omits FCLR-002/003).
6. `research_state/session_20261117T215904Z/trigger_activation_readiness_20261117T215904Z.{json,md}` + `trigger_activation_executor_20261117T215904Z.py`.
7. `research_state/session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (power floors) and `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` (prereg skeleton).

## Completed work — do not repeat

- **FCLR-003 — SEALED NEGATIVE (the only adequately powered confirmatory window):** C2 vs B1 +0.015205 QLIKE (worse), CI [-0.020240, 0.056734] crosses 0; 2024-10-02..2024-12-31, 91d, 3 blocks, 5 instruments, n=10796. `research_state/evaluation_summary_FCLR003.md`. Do not re-score.
- **FCLR-011 sealed PASS → forward NOT_REPLICATED:** 2026-05..08 rel -5.55% on 2026-08..10; independent clean OLS recompute does not reproduce (+4.94% expected vs -294% observed, NOT_REPRODUCED). `session_20261116T0040Z/`.
- **FCLR-REPRO-SYNTH-05 — DONE (`session_20261117T072040Z`):** design-frontier certificate `BLOCKED_ON_DESIGN` + replication robustness (7 studies, 2/7 within tolerance, 0 promotable).
- **FCLR-014 — BLOCKED_ON_DESIGN (`session_20261117T071110Z`):** the 4-block "freeze a prereg" claim (`session_20261117T051045Z`) is RETRACTED as leakage-prone.
- **Frontier verify-06/07 line CLOSED:** `session_20261117T193323Z` + `session_20261117T194457Z` both `all_exact_match=true`, `BLOCKED_ON_DESIGN`. Do not run verify-08+.
- **Trigger-readiness package v1 — DONE (`session_20261117T215904Z`):** executor (referee, REFUSE_ALL, exit 2, outcome_files_opened=[]), selftest (13 tests, EXIT 0), readiness certificate, trigger check. Inputs to artifact 5 above; do not rebuild from scratch, refresh it.
- **FCLR-LEDGER-INTEGRITY-01 code fix — DONE (2026-11-17T23:45:00Z):** `scripts/next_campaign_status.py` `TESTED_WINDOWS` now includes FCLR-003's sealed test window; frontier tests updated + regression guard added. Corrected frontier verified closed. See "What was fixed this session" above. Do not re-fix.

## Blocked-path warning (do not waste a session here)

- **No parquet engine is installed** (`pyarrow`, `fastparquet`, `duckdb`, `polars` absent; network installs prohibited). Any `.parquet`-only task is blocked unless a CSV/JSON/ZIP twin exists. Use the ZIP/CSV reader pattern from `session_20261117T031656Z` / `session_20261117T000400Z` and the `_read_zip_csvs` helper in `scripts/fclr011_recompute_audit.py`.
- **Unresolved Git-LFS pointers (no local object):** `research_state/run_manifest.json`, `run_manifest_FCLR002.json`, `data_cache/fclr002_panel*.json`, `data_cache/manifest_fclr002.json`, `data_cache/manifest_fclr003.json`. Do NOT run `git lfs pull` (network prohibited). Do not block on them.
- **`research_state/research_protocol_fclr002.md` / `research_protocol_fclr003.md` do not exist** — do not block on them. (Note: `research_protocol_fclr006.md` does exist and restates the FCLR-002/003 windows.)
- **2024 cache format:** 2024-04..06 mark/premium/index files are ZIPs wrapping per-day CSVs (nested `SYM-1h-DATE/SYM-1h-DATE.csv`); Jan–Mar and Jul–Nov 2024 are CSVs; 2025–2026 are ZIP+CSV. Use a ZIP-aware, recursive reader.
- Do NOT run `scripts/fclr_liq_010_confirm.py` (parquet-only; fails on import).
- **No outcome data may be inspected** while building this campaign's artifacts; the trigger-activation package is outcome-blind by construction. Never open an `evaluation_summary_*` outcome, `results/*`, sealed panel, or holdout.

## Bottlenecks removed / prevented by this handoff

- **Tested-window ledger omission (the real bottleneck) — FIXED:** FCLR-003's sealed test window (2024-10-02..12-31) was added to `TESTED_WINDOWS`; the frontier no longer mislabels 2024-10/11/12 as fresh. See "What was fixed this session" above.
- **Closure ledger omission — still open:** the structural closure JSON enumerates experiments but not the FCLR-002/003 consumed *windows*; artifact 3 records the backfill plan.
- **Idle "AWAITING_TRIGGER" equilibrium corrected:** the prior handoff's "no agent-removable heavy work remains" was used to justify trigger-check-only sessions. This handoff names concrete, verifiable heavy work (ledger audit + corrected-frontier verification + refreshed readiness) that must be executed before any idle hold.
- **Competing handoff authority:** none. `AGENT_HANDOFF.md` is the sole durable handoff.
- **Empty-session loop:** do not create a session dir until artifact 1 is ready; empty/phantom sessions are non-counting.

## Prohibitions

- Do not start or re-run any sealed cached-data confirmatory estimand; all sealed estimands are terminal.
- Do not re-run FCLR-014, the replication synthesis, the design-frontier certificate; do not run verify-08+.
- Do not mutate sealed artifacts, the closure JSON, or `.github/workflows/*`.
- Do not poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or add root-level `research_state/*.md|json` (root at 500/500 churn cap).
- Do not add `statsmodels` or unpinned heavy dependencies to the core path.
- Do not run `git lfs pull` or otherwise fetch network data.
- Do not run `scripts/fclr_liq_010_confirm.py` (parquet-only; will fail on import).
- Discovery suite is long-running; let it finish and record actual EXIT, not partial/timeout.
- **Do NOT re-fix `scripts/next_campaign_status.py` `TESTED_WINDOWS`.** The FCLR-003 fix is applied and tested; re-editing it is a regression. If you believe it is wrong, revert to `git show HEAD:scripts/next_campaign_status.py` and re-apply only the single FCLR-003 row, then show red→green.
- Do not mutate the sealed closure JSON; record the FCLR-002/003 backfill as a plan (artifact 3).

## Reopen triggers (machine-checkable — act ONLY when satisfied; all `OPEN`)

- `GATE4_BRANCH_1` — `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`). Human/legal attestation only.
- `NEW_OBSERVED_LIQUIDATION_SOURCE` — `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION` — `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO` — `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json` (LOIO≥6/8 AND placebo>95th null; re-scoring the sealed 19.04% forbidden).

## Verification record — 2026-11-18T01:50:38Z (ledger-integrity fix applied; campaign 02 opened)

- **Repo/rank-0:** `CLOSED_TERMINAL`; rank-0 `TRIGGER_ONLY`; 0/58 rows §17-promotable. No sealed estimand re-run.
- **Concrete inefficiency found and FIXED (outcome-blind, from sealed evaluations + tracked code):** `scripts/next_campaign_status.py` `TESTED_WINDOWS` omitted FCLR-003's sealed test window. `markfund_frontier()` listed 2024-10/11/12 as individually feasible and `ready_windows()` marked 2024-04/05 as untested, though FCLR-002/003 consumed 2024-04..2024-12. Evidence: `evaluation_summary_FCLR002.md` lines 8–10; `evaluation_summary_FCLR003.md` lines 7–10.
- **Fix applied:** added `("2024-10-02", "2024-12-31", "FCLR-003 sealed NEGATIVE test window (NOT_SUPPORTED)")` to `TESTED_WINDOWS` with an explanatory comment; updated the two frontier tests and added `test_fclr003_sealed_test_months_not_reproposed`.
- **Corrected frontier (verified):** `n_individually_feasible=1` (`2025-01`), `max_mutually_non_overlapping=1`, `n_overlapping_pairs=0`, `campaign_feasible_non_overlapping=False`, `disjoint n_feasible=0`. The only individually-feasible month is 2025-01 (its 30-day train is FCLR-003 test, allowed as pre-test history), a single block < 3. **Frontier remains closed, now for the honest reason.**
- **Arithmetic that closes the frontier:** the only complete untested contiguous run is 2025-01 = 31 days < `MIN_DESIGN_DAYS=127`; 2024-10..12 are FCLR-003 *test*; 2025-01's 30-day train window (2024-11-25..2024-12-24) is FCLR-003 *test*; so no ≥3 mutually-non-overlapping untested 30-day block set exists.
- **Tests:** `tests.test_next_campaign_status` 22/22 OK (was 21, +1 regression guard); all 77 frontier-dependent tests (`test_fclr014_anchor_integrity`, `test_fclr_design_feasibility`, `test_fclr_final_structural_closure`, `test_tracka_hardening_143`, `test_fclr018_gate4_prereg_readiness_matrix`) OK. Full discovery: 1129/62/9/14/EXIT 1 — same environment-dependent baseline (all errors are `ModuleNotFoundError: numpy`), +3 tests from this change.
- **Gates:** `check_handoff_heavywork_gate.py --json` **PASS** (`reason_code: OK`, `handoff_stale=false`, latest session `session_20261117T215904Z`, root 500/500, trigger_readiness.pass=true); `check_tracka_scope_registry_drift.py --json` **PASS** (196/196 scripts in registry). Timestamp-only cache side effect (`ironflow_fastpath_cache.json`) reverted.
- **No sealed artifacts, registries, or `.github/workflows/*` modified; no root-level `research_state/*.md|json` added; no competing handoff authority remains. Tracked code changed: `scripts/next_campaign_status.py` (+10 lines) and `tests/test_next_campaign_status.py` (updated 2 tests, +1 new test).**

## Staleness correction

Latest on-disk session `session_20261117T215904Z` is recorded in this handoff. When the next session creates `session_<UTC>/`, record its id here **before** the final gate capture so `handoff_stale` stays false and `HANDOFF_STALE_LATEST_SESSION` does not fire.

---

## NEXT AGENT: YOUR FIRST COMMAND SEQUENCE

```bash
# 1. Verify the fix is in place
python3 scripts/next_campaign_status.py --json | jq '.markfund_frontier | {n_individually_feasible, max_mutually_non_overlapping, campaign_feasible_non_overlapping, individually_feasible_months}'

# Expected: n_individually_feasible=1, max_mutually_non_overlapping=1, campaign_feasible_non_overlapping=false, individually_feasible_months=["2025-01"]

# 2. Create session dir (real UTC)
SESSION_DIR="research_state/session_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$SESSION_DIR"

# 3. Start artifact 1: ledger_audit (read-only, outcome-blind)
#    Write a Python script that enumerates all consumed months from evaluation summaries + TESTED_WINDOWS
#    Output: $SESSION_DIR/ledger_audit_$(date -u +%Y%m%dT%H%M%SZ).{py,json,md}

# 4. Continue with artifacts 2-7 in order. Do not skip. Do not stop at artifact 1.
```

**This handoff is the only authority. The campaign is mandatory. Heavy work is non-avoidable. Execute.**