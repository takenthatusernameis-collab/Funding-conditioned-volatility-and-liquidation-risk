# AGENT HANDOFF — 2026-11-24T00:20:14Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: NOT CONCLUDED — ACTIVE HEAVY WORK OPEN.**
> Active rank-0 campaign: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`.
> The frozen temporal-stability prereg exists, but BROAD-01 fidelity is NOT yet established.
> Verify-and-stop, prereg-only, prose-only, trigger-only, audit-only, and non-reconciled verdicts are
> forbidden completion modes.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-24T00:20:14Z**
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is
> `Funding-conditioned-volatility-and-liquidation-risk`. RESEARCH_PROMPT.md §3.2 has two halves:
> - **Half 1 (Volatility / Track C):** CLOSED — leakage-robust null across every claim-worthy panel
>   (H1_primary NOT_SUPPORTED; FCLR-011 PASS does not generalize forward; FCLR-FWD-VOL-011-CONFIRM
>   NOT_REPLICATED). No further volatility heavy work is admissible.
> - **Half 2 (Liquidation-risk):**
>   - **Track A (observed liquidations):** `TRACK_A_STRUCTURALLY_BLOCKED` as a complete-census claim;
>     the available ironflow_bulk liquidation feed is a capped sample and cannot establish absence.
>   - **Track B (modeled boundary breach):** NOT_SUPPORTED across all campaigns.
>   - **Track C (volatility-as-liquidation-proxy):** NOT_SUPPORTED.
>   - The only liquidation-risk results marked SUPPORTED are the regime-conditioned cross-sectional
>     funding → next-hour observed-liquidation-intensity findings on the narrow 15-coin panel:
>     FCLR-XSEC-004, FCLR-XSEC-005, and FCLR-XSEC-006, all EXPLORATORY_ONLY / `promotable:false`.
>   - **FCLR-LIQ-XSEC-BROAD-01 (COMPLETED, `session_20261123T085507Z`):** generalized those findings
>     to the full ironflow_bulk universe (2025-05..2026-10; 2,849,452 liquidation rows). Verdict:
>     **SUPPORTED_GENERALIZATION on cross-sectional rank ordering**. Exact headline: **long-arm mean
>     rank-IC = 0.155133**, block-bootstrap **CI95 = [0.142081, 0.168895]**; **short-arm mean
>     rank-IC = -0.002054**. The Poisson-deviance materiality floor (2%) was NOT met on either arm.
>     This is an association, not a time-series forecast or a complete liquidation census.
>
> **THE ACTIVE HEAVY QUESTION:** BROAD-01 never tested whether its per-block rank-IC series is stable
> over time. RESEARCH_PROMPT.md §17 promotion condition #4 requires that skill not be dominated by one
> coin, venue, crisis, or time block. The frozen campaign
> `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` tests exactly that gap.
>
> **STATE OF THE WORK (read before doing anything):**
> - The outcome-blind prereg is frozen under `research_state/broad_ts_scaffold/`:
>   `fclr_liqxsecbroad01_ts_prereg_20261123T164423Z.json` + `.md`
>   (`FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes:true`,
>   `outcome_data_inspected_before_freeze:false`). Copy it verbatim into the new session; do not
>   re-freeze it and do not edit sealed artifacts.
> - The runnable eval scaffold is
>   `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py`.
>   It now fails closed unless input hashes verify and the long-arm BROAD-01 headline reconciles.
> - A prior 23:56 UTC run produced `NOT_STABLE` from the non-reconciled scaffold. It is scientifically
>   invalid and has been archived under
>   `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/`. **DO NOT ship or cite its
>   verdict.** Do not recreate a partial top-level session directory.
> - The contradictory terminal-closure handoff was moved to
>   `research_state/handoff_archive/AGENT_HANDOFF_20261123T163509Z.md`. This file is the only root
>   durable handoff.
>
> **FIDELITY STATUS — THE REMAINING BLOCKER IS REAL, NOT COSMETIC:**
> The scaffold now reproduces BROAD-01's coverage and design counts: 12,586 hours, 799 markets,
> 1,715,710 test rows, 9,508 training rows, 30 valid 168h blocks, and 72/72 input hashes.
> It **does not** reproduce the sealed headline:
> - Scaffold long-arm mean rank-IC: **0.149461001148287** (BROAD-01: **0.1551333434568285**).
> - Scaffold long-arm Poisson deviance B1: **14896.850709403465** (BROAD-01: **14895.300476998453**).
> - Required tolerance remains **1e-3**. The scaffold raises `RuntimeError` before stability inference.
>
> A fit-input capture before either model's test-outcome calculation showed:
> - BROAD-01 and scaffold training shapes both `(9508, 3)`.
> - **9,506/9,508 feature rows are bit-identical**; two `log(RV168)` values differ by at most
>   **4.440892098500626e-16**.
> - **9,504/9,508 targets are bit-identical**; maximum target difference is
>   **1.7763568394002505e-15**.
> These machine-epsilon differences are amplified by the ill-conditioned unscaled RV regression and
> move the sealed headline materially. Therefore neither a `STABLE` nor a `NOT_STABLE` verdict is
> admissible until bit-level fidelity is established or the reference is formally downgraded.
>
> **YOU MUST EXECUTE: BIT-LEVEL FIDELITY AUDIT, THEN THE FROZEN STABILITY BATTERY.**
> Do not relax the 1e-3 tolerance and do not relabel the campaign.
>
> 1. Create a fresh `research_state/session_<UTC>/` with UTC strictly after
>    `20261123T135825Z`. Copy the frozen prereg JSON+MD from `broad_ts_scaffold/`.
> 2. Capture fit inputs without inspecting test outcomes. In a temporary directory outside Git, import
>    each module and monkeypatch its first OLS call:
>    - BROAD-01 reference:
>      `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.py`, patch
>      `ols(X, y)`.
>    - TS scaffold: patch `ols_fit(X, y)`.
>    In each wrapper, use `inspect.currentframe().f_back.f_locals["rows_in"]` to save the training
>    `coin`, `hk`, feature values, and target alongside `X` and `y`; then stop before outcome code.
>    Compare row keys first, then `numpy.array_equal` on feature/target values.
> 3. Reconcile the two differing `log(RV168)` rows and four differing target values to the sealed
>    scalar path. Audit in this order:
>    (a) direct pyarrow `to_pylist()` candle closes and per-market cumulative sums versus any pandas
>    conversion/filter path;
>    (b) direct scalar liquidation accumulation versus pandas groupby sum order, especially notional;
>    (c) funding/OI scalar lookup versus pandas dictionary conversion;
>    (d) coin-major test/train row order. The scaffold now sorts the test panel by `coin,hk`, uses
>    BROAD-01's 1-based `TRAIN_SUBSAMPLE=200` rule, uses `mean(funds <= target)` percentiles, and
>    uses scalar-style OLS/RV arithmetic; preserve these fixes.
>    Prefer a bit-identical `(9508,3)` design matrix and target vector. At minimum, require the
>    BROAD-01 long-arm mean rank-IC and B1 deviance to reproduce within 1e-3.
> 4. Only after fidelity passes, audit the scaffold's descriptive regime code against the frozen
>    prereg. Current weaknesses to fix before shipping a verdict:
>    - the RV-tercile loop records only the overall block IC and does not compute RV terciles;
>    - the UTC loop uses only each block's start hour instead of Asian `[0,8)`, European `[8,16)`,
>      and US `[16,24)` session buckets over eligible origins;
>    - several Holm family entries reuse the primary bootstrap p-value instead of a test-specific p.
>    Implement the prereg's regime definitions without changing its thresholds or verdict rule.
> 5. Run the complete frozen battery on the LONG arm (primary; SHORT is descriptive only):
>    sign-reproduction fraction (threshold 0.80), 6-block rolling mean min/median/max and CI95,
>    ordered-block trend test at frozen alpha_k, first/second-half gap with block-bootstrap CI95,
>    leave-one-block-out range, per-regime sign stability, and Holm across the declared 6-arm family.
>    Preserve all four per-block series: `ic_C2_l`, `ic_B1_l`, `ic_C2_s`, `ic_B1_s`, with block
>    start hours.
> 6. Frozen symmetric verdict: `STABLE` iff long-arm sign reproduction is at least 0.80 AND the
>    first/second-half gap CI95 excludes a sign reversal AND the trend test does not reject
>    stationarity at frozen alpha_k; otherwise `NOT_STABLE`. Preserve a genuine null honestly.
> 7. If bit-identical reconciliation is impossible after the documented audit, do not fabricate a
>    verdict. Record `BROAD01_FIDELITY_BLOCKED` with the exact row-level evidence, preserve BROAD-01
>    as unreconciled, and create a materially different numerically stable prereg only as a new
>    experiment ID. Do not call an inspected holdout fresh confirmation.
>
> **Do NOT:** declare the program concluded; verify-and-stop; re-run BROAD-01 as a terminal campaign;
> ship the archived `NOT_STABLE`; relax the 1e-3 tolerance; threshold-shop the 2% materiality floor;
> build a risk overlay (§9 gate not passed); claim a time-series forecast gate pass from a
> cross-sectional association; wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen
> data; §16, §19); create an empty partial session; or add root-level research-state files.

### Single, non-deferrable job (FIDELITY-AND-EXECUTE BROAD-TS)

Produce the complete `FCLR-LIQ-XSEC-BROAD-TS-01` artifact set under a fresh
`research_state/session_<UTC>/` (UTC strictly after `20261123T135825Z`), using the frozen prereg and
reconciled scaffold as inputs. Record that session id in this handoff only after its required files
exist. If any required artifact is missing or empty, the heavy-work gate fails closed.

---

## FOCUS CAMPAIGN — FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z (ACTIVE, rank-0)

**Question:** Is the SUPPORTED broad-universe cross-sectional funding → next-hour observed
liquidation-intensity association temporally stable (not dominated by one time block)?

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/{liquidations,funding,open_interest,candles_1h}/`
  (18 monthly parquet, 2025-05..2026-10). Liquidations: 2,849,452 rows; instrument key is
  `market`, with coin derived by `coin_from_market()`. Assert every `.sha256` sidecar before reading;
  caches are read-only. Verified: 72/72 hashes match.
- BROAD-01 constants: `MONTHS=2025-05..2026-10`, `TRAIN_FRAC=0.60`, `PURGE_EMBARGO_H=48`,
  `BLOCK_H=168`, `HORIZON_H=1`, `N_BOOT=2000`, `N_PERM=1000`, `N_LOIO=8`,
  `LOIO_PASS_THRESHOLD=6`, `SEED=20261123`, `ALPHA_K=0.05/(2*3)`, `MATERIALITY_PCT=2.0`.
- Sign convention: `relative_improvement = (baseline - candidate) / baseline`; positive means the
  candidate is better. Do not reverse the sign to manufacture agreement.
- The BROAD-01 prereg JSON is hand-authored pseudo-JSON and is not strict `json.load`-parseable. Use
  its `.md` plus the constants in the sealed eval script. Do not rewrite the sealed artifact.

**Current scaffold repairs already made:**
- Test panel is coin-major (`coin,hk`), matching BROAD-01 tie ordering; hour-major ordering had
  flipped the long-arm rank-IC sign.
- Train subsample is coin-major and selects BROAD-01's 1-based every-200th row, yielding 9,508 rows.
- Absolute-funding percentile uses BROAD-01's `count(values <= target) / n`, not midpoint
  interpolation.
- RV, OLS normal equations, smearing, rank-IC, and Poisson deviance follow BROAD-01 scalar arithmetic.
- Short-arm prediction retains BROAD-01's own long-target implementation; deviance is aligned to the
  declared short actual. Do not silently alter this reference behavior during fidelity work.
- SHA mismatch or headline mismatch raises before any stability verdict is written.
- `per_block_series` now contains `ic_C2_l`, `ic_B1_l`, `ic_C2_s`, and `ic_B1_s`.

**Required artifacts (ALL under the new session directory; no zero-byte placeholders):**
- `fclr_liqxsecbroad01_ts_prereg_<UTC>.json` + `.md` — verbatim frozen prereg copy.
- `fclr_liqxsecbroad01_ts_fidelity_audit_<UTC>.json` + `.md` — row-level BROAD-01 reconciliation
  evidence, including fit-input comparison and final headline errors.
- `fclr_liqxsecbroad01_ts_eval_<UTC>.py` + `.json` + `.md` — reconciled heavy stability evaluation.
  The JSON must report `fidelity_reconciliation.reconciled:true`, the long-arm mean rank-IC near
  +0.1551, long-arm Poisson deviance near 14895, and all four per-block series.
- `fclr_liqxsecbroad01_ts_recompute_<UTC>.py` + `.json` — independent stdlib recompute asserting
  `all_checks_match:true`.
- `fclr_liqxsecbroad01_ts_evidence_audit_<UTC>.json` + `.md` — honest evidence audit.
- `evidence_audit_<UTC>.json` — gate-critical non-empty alias.
- `trigger_check_<UTC>.json` — non-empty record that no external trigger is required.

---

## ROOT CONSTRAINTS (hard)

- Root `research_state/*.md|*.json` count: **499/500** — at cap. All new artifacts MUST go under
  `session_<UTC>/` or another nested directory. Do not add root-level research-state files.
- No empty files and no zero-byte placeholders.
- Do not threshold-shop or relax a frozen floor/threshold after outcomes.
- Preserve nulls honestly: valid outcomes are `STABLE`, `NOT_STABLE`, or an evidence-backed fidelity
  blocker; never a fabricated pass.
- Do not re-run any terminal campaign or build a risk overlay.
- Do not modify `.github/workflows`.
- Do not overwrite `research_state/research_protocol.md` or any sealed prereg/eval artifact.
- Stdlib + numpy + pandas + pyarrow only; no network for the heavy evaluation; no new source; no
  overlay.
- Do not track-adulterate: never describe a broad-universe cross-sectional association, or a
  stability test of it, as a time-series forecast gate pass or complete observed-liquidation census.
- Do not wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; it cannot fire on frozen data and is not a valid
  reason to idle.
- Do not write a future/non-existent session id into this handoff. The only literal session tokens
  permitted here are `session_20261122T190000Z`, `session_20261122T224500Z`,
  `session_20261123T043600Z`, and `session_20261123T085507Z`.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- The heavy-work gate binds `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`: once the first
  post-start session exists, that latest session MUST contain the full BROAD_TS artifact set above,
  with no zero-byte placeholders. Trigger-only, prose-only, audit-only, prereg-only,
  verify-and-stop, arbitrary `recompute_*`, and non-reconciled eval sessions FAIL closed.
- Do not create a partial session directory and leave it unrecorded; that causes
  `HANDOFF_STALE_LATEST_SESSION` and blocks all later work.
- Do not re-run any terminal campaign.
- Do not wait for an external trigger.
- Do not build a risk overlay.
- Do not track-adulterate.
- Do not ship a verdict from a non-reconciled eval. The current scaffold intentionally raises before
  writing an eval JSON/MD unless BROAD-01 reconciliation passes.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. Capped-sample feed, not a census. Columns include `timestamp[us,tz=UTC],market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; funding and premium features. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; OI, mark, and oracle prices. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet; hourly close and instrument identity. |
| `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_prereg_20261123T164423Z.json` + `.md` | Frozen outcome-blind TS prereg. |
| `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py` | Fail-closed heavy eval scaffold; exact headline reconciliation required. |
| `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/` | Archived non-reconciled output; evidentiary only, never a verdict source. |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.py` | Sealed BROAD-01 fidelity reference. |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.json` | Sealed BROAD-01 headline: +0.1551333434568285 long mean rank-IC; 14895.300476998453 B1 deviance. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate
caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3.2, §9, §15, §16, §17, and §19.
- `scripts/check_handoff_heavywork_gate.py` — BROAD_TS binder and required artifact set.
- `research_state/experiment_frontier.json` — rank-0 is the active BROAD-TS campaign.
- `research_state/broad_ts_scaffold/` — frozen prereg and fail-closed eval.
- `research_state/session_20261123T085507Z/` — sealed BROAD-01 reference and headline.
- `research_state/final_synthesis_report.md` — historical synthesis, superseded by the active gap.

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why, including the BROAD-01 fidelity result.
2. Exact test outcomes with paths (heavy-work gate and campaign unit tests).
3. Evidence added and full paths under the new session directory.
4. State of each research gate (heavy-work gate SATISFIED; forecast gate still NOT PASSED).
5. Single highest-value next task (or an evidence-backed DATA_BLOCKED with a materially different route).
6. Precise verifying commands.
7. Any remaining blocker and the next materially different route.

Also answer RESEARCH_PROMPT.md §19: what the evidence supports or contradicts, the strongest
alternative explanation, the dominant data/label/inference limitation, the next falsifying test, and
the highest-information next action.

---

## BOTTLENECK RESOLUTION (this refresh)

- **Resolved (stale partial run → gate fail-closed):** the unrecorded 23:56 UTC run contained only
  eval files from the non-reconciled scaffold. Its `NOT_STABLE` verdict was a divergence artifact.
  The files were archived under `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/`;
  the empty top-level session directory was removed. Do not recreate it.
- **Resolved (multiple durable handoffs):** the contradictory terminal-closure file was moved to
  `research_state/handoff_archive/`; `AGENT_HANDOFF.md` is now the only root handoff.
- **Resolved (verify-and-stop bottleneck):** the active heavy campaign remains rank-0; verify-and-stop
  is not a permitted completion.
- **Resolved (hour-major tie ordering):** the scaffold now uses coin-major test rows, eliminating the
  original sign-flip caused by ordinal tie ranks under a different row order.
- **Resolved (train subsample mismatch):** the scaffold uses BROAD-01's coin-major, 1-based every-200th
  selection and reproduces the 9,508-row training count.
- **Resolved (percentile mismatch):** absolute-funding percentile now uses the exact `<=` count.
- **Resolved (silent invalid verdict):** the scaffold now fails on bad hashes or headline mismatch and
  emits detailed reconciliation errors.
- **OPEN (bit-level fidelity):** two log-RV168 fit values differ by 4.44e-16 and four targets differ
  by at most 1.78e-15; the ill-conditioned fit amplifies these to a 0.00567 rank-IC gap and 1.55
  deviance gap. This is the next agent's first heavy task. Do not relax tolerance.
- **OPEN (regime implementation audit):** the scaffold's descriptive RV-tercile/UTC sections and some
  Holm p-values must be aligned with the frozen prereg before any final verdict.
- **Verified (2026-11-24T00:20:14Z refresh):** invalid run archived; sole-handoff archive complete;
  scaffold compiles and fails closed at fidelity; BROAD-01 reference remains unchanged.

---

## VERIFICATION COMMANDS (run before declaring done)

```bash
# 0. One-time environment setup if needed
python3 -m pip install --quiet numpy pandas pyarrow

# 1. Heavy-work gate must return reason=OK
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Campaign gate unittests must pass
python3 -m unittest \
  tests.test_active_campaign_gate \
  tests.test_fclr_starter_001_campaign_gate \
  tests.test_fclr_campaign_gate \
  tests.test_fclr_heavy_confirm_gate \
  tests.test_pooled_robust_002_campaign_gate \
  tests.test_tracka_hardening_143

# 3. Compile the heavy scaffold
python3 -m py_compile \
  research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py

# 4. Context only: the old 3-block scanner does not assess BROAD-TS feasibility
python3 scripts/next_campaign_status.py
```

**Latest handoff session: `session_20261123T085507Z`** — completed FCLR-LIQ-XSEC-BROAD-01; supported
the cross-sectional rank-ordering association but did not meet the 2% materiality floor.
**Active rank-0 campaign: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`** — temporal stability of
that association. **Program status: ACTIVE — fidelity audit and heavy stability work remain open.**

(End of file)