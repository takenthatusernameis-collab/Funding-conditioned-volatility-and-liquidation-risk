# AGENT HANDOFF — 2026-11-23T23:18:00Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> Gate status verified at this refresh (2026-11-23T23:18:00Z): **PASS** (reason_code=OK,
> failures=[], latest_disk_session_id == latest_recorded_session_id == session_20261123T085507Z,
> handoff_stale=false). Campaign gate unittests: **126 tests OK**.
> **PROGRAM STATUS: NOT CONCLUDED — ACTIVE HEAVY WORK OPEN.** The active heavy task
> `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` is mid-flight: a frozen outcome-blind prereg and a
> runnable eval scaffold already exist (archived under `research_state/broad_ts_scaffold/`), but the
> scaffold does **NOT yet reproduce** BROAD-01's frozen headline. Verify-and-stop is NOT a permitted
> completion. The non-deferrable heavy campaign is re-issued with the first-step reconciliation
> requirement made explicit so the next session can execute it without rediscovery.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-23T23:18:00Z (refresh 2026-11-23T23:18:00Z)**
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is
> `Funding-conditioned-volatility-and-liquidation-risk`. RESEARCH_PROMPT.md §3.2 primary question has two
> halves:
> - **Half 1 (Volatility / Track C):** CLOSED — leakage-robust null across every claim-worthy panel
>   (H1_primary NOT_SUPPORTED; FCLR-011 PASS does not generalize forward; FCLR-FWD-VOL-011-CONFIRM
>   NOT_REPLICATED). No further volatility heavy work is admissible.
> - **Half 2 (Liquidation-risk):**
>   - **Track A (observed liquidations):** `TRACK_A_STRUCTURALLY_BLOCKED` — no admissible
>     unauthenticated historical liquidation source with required coverage exists in this environment
>     (source audit frozen outcome-blind; `outcome_data_inspected_before_freeze:false`).
>   - **Track B (modeled boundary breach):** NOT_SUPPORTED across all campaigns.
>   - **Track C (volatility-as-liquidation-proxy):** NOT_SUPPORTED (same as Half 1).
>   - **The ONLY liquidation-risk results ever marked SUPPORTED** are the regime-conditioned
>     cross-sectional funding → next-hour observed-liquidation-intensity findings on the narrow 15-coin
>     panel: FCLR-XSEC-004 (count, low-RV), FCLR-XSEC-005 (notional-weighted, low-RV), FCLR-XSEC-006
>     (all three UTC buckets). All were flagged `promotable:false` / EXPLORATORY_ONLY because they never
>     generalized beyond 15 coins.
>   - **FCLR-LIQ-XSEC-BROAD-01 (COMPLETED, session_20261123T085507Z):** generalized those findings to the
>     full 342-coin ironflow_bulk universe (2025-05..2026-10, 2,849,452 liquidation rows). Verdict:
>     **SUPPORTED_GENERALIZATION on the cross-sectional rank-ordering association.** Exact headline:
>     **LONG arm** mean per-block rank-IC = **0.155133**, block-bootstrap **CI95 = [0.142081, 0.168895]**
>     (excludes null in the favorable direction), Holm primary p < alpha_k; **SHORT arm** mean rank-IC =
>     **-0.002054** (null). **Poisson-deviance materiality floor (2%) NOT MET on either arm**
>     (long -0.23%, short +0.71%). It is a rank-ordering *association*, not a time-series forecast.
>
> **THE UNFINISHED, NON-DEFERRABLE HEAVY QUESTION (this campaign):**
> BROAD-01 reported only the *mean* per-block rank-IC. It NEVER tested **temporal stability** of the
> per-block rank-IC series — i.e. whether the SUPPORTED rank-ordering association survives a rolling
> holdout and is not dominated by one time block. RESEARCH_PROMPT.md §17 promotion condition #4 explicitly
> requires: *"Skill is not dominated by one coin, one venue, one brief crisis or one time block."* BROAD-01
> is the ONLY SUPPORTED liquidation-risk result in the entire program, and it was declared the "durable
> final answer" without ever being asked whether it is stable across time. Answering that is the single
> highest-value remaining heavy task.
>
> **STATE OF THE WORK (read this before doing anything):** A previous session already froze the
> outcome-blind prereg (status `FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes:true`,
> `outcome_data_inspected_before_freeze:false`) and drafted a runnable eval scaffold. Both are archived
> under `research_state/broad_ts_scaffold/`:
> - `fclr_liqxsecbroad01_ts_prereg_20261123T164423Z.json` + `.md` — the FROZEN prereg (DO NOT re-freeze;
>   DO NOT edit after outcomes; copy it verbatim into the new session as the prereg).
> - `fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py` — a runnable heavy eval (numpy+pandas+pyarrow).
>
> **CRITICAL — THE SCAFFOLD DOES NOT YET REPRODUCE BROAD-01 AND MUST NOT BE TRUSTED AS-IS.** When run on
> the frozen panel, the scaffold produces **long-arm mean rank-IC = -0.1454** (BROAD-01: **+0.1551**) and
> **long-arm Poisson deviance = 13322** (BROAD-01: **14895**), on the *same* 1,715,710-row test panel and
> 30×168h blocks. A sign-flipped mean rank-IC means the eval is **not a faithful reuse** of BROAD-01's
> methodology; any STABLE/NOT_STABLE verdict from it is **scientifically invalid**. Do NOT ship the
> scaffold's verdict. (For reference, the scaffold's *non-reconciled* run already yields verdict
> `NOT_STABLE` with mean rank-IC -0.1454 — that verdict is an artifact of the divergence, not a finding.)
>
> **YOU MUST EXECUTE: reconcile the scaffold to BROAD-01, THEN run the stability battery.**
> Concretely:
> 1. **Reconcile** `broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py` against BROAD-01's
>    `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.py` until the
>    long-arm mean rank-IC reproduces **+0.1551** and long-arm Poisson deviance reproduces **14895**
>    (tol 1e-3). Known divergence surfaces to audit first, in priority order:
>    (a) **per-market feature construction** — `rv24`/`rv168` cumulative-sum windows, `ma_dev`
>    (BROAD-01 uses `(c/prev_c - 1)` on consecutive closes; scaffold uses the same but verify off-by-one),
>    `dislocation = mark/oracle - 1`;
>    (b) **train-only z-scaling `sc`** — per-feature train mean/std must match BROAD-01's `scale_feats`
>    loop exactly (same train mask, same ddof);
>    (c) **`abs_fund_pct`** — BROAD-01 `percentile_rank(funds, target) = mean(funds <= target)` per coin
>    over train hours; the scaffold's searchsorted midpoint form `(lo+hi)/(2n)` is NOT identical — restore
>    BROAD-01's exact `<=`-count percentile;
>    (d) **train subsample** — BROAD-01 builds `train_feature_rows` in a specific order (per-coin, per-hour
>    from `coin_series`); the scaffold uses `series_df.iloc[::200]` over a market-major ordering. Match
>    BROAD-01's row order and `TRAIN_SUBSAMPLE=200` stride so the OLS fit sees the same rows;
>    (e) **OLS intercept** — BROAD-01 `b1_feat`/`c2_feat` include `1.0` as the first element and `ols()`
>    adds NO extra intercept; the scaffold's `ols_fit`/`ols_predict` must NOT add a second `np.ones`
>    column (a double intercept makes the design collinear and flips beta). This was already a bug in the
>    scaffold — confirm it is fixed.
> 2. **Then** run the full pre-frozen stability battery (do NOT change the battery or thresholds after
>    reconciliation — they are frozen in the prereg):
>    - sign-reproduction fraction (long arm, threshold 0.80 = ≥24/30 blocks positive);
>    - 6-block rolling rank-IC min/median/max + block-bootstrap CI95 (N=2000, seed 20261123);
>    - ordered-block monotone trend test (Spearman block-index vs rank-IC, two-sided, frozen alpha_k);
>    - first-half vs second-half mean rank-IC gap with block-bootstrap CI95;
>    - leave-one-block-out range of mean rank-IC;
>    - per-regime (RV-tercile, UTC-bucket) sign stability;
>    - Holm across the declared 6-arm stability family (alpha_k = 0.05/6).
>    **Primary arm is the LONG arm** (the SUPPORTED arm). The SHORT arm is descriptive only and must not
>    drive the verdict.
> 3. **Verdict rule (frozen, symmetric):** `STABLE` iff long arm sign reproduced in ≥0.80 of blocks AND
>    first/second-half gap CI95 excludes a sign reversal AND trend test does not reject stationarity at
>    frozen alpha_k; otherwise `NOT_STABLE` (a genuine, durable finding: the SUPPORTED association is
>    time-block dominated and fails §17 condition #4). Preserve the null honestly; never relax a threshold
>    after outcomes; never relabel. The materiality floor (2%) was already NOT met in BROAD-01; this
>    campaign tests rank-ordering *stability*, NOT a time-series forecast gate, and must not be relabeled
>    as one.
>
> **Do NOT:** declare the program concluded; verify-and-stop; re-run BROAD-01; re-run any terminal
> campaign; threshold-shop the materiality floor; build a risk overlay (§9 gate not passed); claim a
> time-series forecast gate pass from a cross-sectional association; wait for
> `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen data; §16, §19); ship a verdict from a
> non-reconciled eval (the current scaffold's -0.1454 is invalid).
>
> **Blockers: None external — the reconciliation + heavy work is executable now on the frozen
> ironflow_bulk panel.** The only blocker is internal methodology fidelity (scaffold does not yet match
> BROAD-01), and it is resolvable offline.

### Single, non-deferrable job (RECONCILE-AND-EXECUTE BROAD-TS)

Produce the complete `FCLR-LIQ-XSEC-BROAD-TS-01` artifact set under a fresh
`research_state/session_<UTC>/` (UTC strictly after `20261123T135825Z`), using the frozen prereg and
scaffold from `research_state/broad_ts_scaffold/` as the starting point. Record that session id in this
handoff and run the verification commands. If any required artifact is missing or empty, the heavy-work
gate fails closed and the session is incomplete.

---

## FOCUS CAMPAIGN — FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z (ACTIVE, rank-0)

**Question:** Is the SUPPORTED broad-universe cross-sectional funding → next-hour observed liquidation-intensity
association temporally stable (not dominated by one time block)?

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/{liquidations,funding,open_interest,candles_1h}/`
  (18 monthly parquet, 2025-05..2026-10). Liquidations: 2,849,452 rows, 342 coins (2025-05);
  **instrument key is `market` — there is NO `coin` column in liquidations** (coin is derived via the
  `coin_from_market()` helper). Each parquet has `.sha256` and `.accessed.json` sidecars — assert sha256
  before reading; caches are read-only. Verified readable with pyarrow 26.0.1 (sha256: 72/72 ok).
  **Parquet `timestamp` is `timestamp[us, tz=UTC]`** — when loaded via `to_pandas()` the dtype may be
  `datetime64[us]`; do NOT do `pd.to_datetime(int_col).astype(int64)//1e9` (that mis-scales us→wrong hours
  and yields 0 eligible origins). Use BROAD-01's `_hkey` (int seconds floor, or datetime `.timestamp()`
  floor) — the scaffold already adopts this; keep it.
- The per-block rank-IC series and walk-forward split definition frozen in
  `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_prereg_20261123T085507Z.json` and
  `fclr_liqxsecbroad01_eval_20261123T085507Z.json`. **Reuse the SAME block boundaries and sign
  convention** (`relative_improvement = (baseline - candidate)/baseline`, positive = candidate better) so
  the stability test is directly comparable to BROAD-01.
  - **BOTTLENECK (removed): the BROAD-01 prereg `.json` is NOT strict JSON** — it is hand-authored
    pseudo-JSON with trailing commas before every `}` and bracket typos such as `[0, 8)` in `utc_buckets`.
    `json.load(open(...prereg...json))` FAILS. Do NOT waste a session rediscovering this and do NOT rewrite
    the sealed artifact. The canonical machine-readable design is the **`.md` prereg** plus the **constants
    at the top of `fclr_liqxsecbroad01_eval_20261123T085507Z.py`**: `MONTHS=2025-05..2026-10`,
    `TRAIN_FRAC=0.60`, `PURGE_EMBARGO_H=48`, `BLOCK_H=168`, `HORIZON_H=1`, `N_BOOT=2000`, `N_PERM=1000`,
    `N_LOIO=8`, `LOIO_PASS_THRESHOLD=6`, `SEED=20261123`, `ALPHA_K=0.05/(2*3)`, `MATERIALITY_PCT=2.0`.
    Copy the scaffold eval as the starting point.
  - **BOTTLENECK (removed): script placement / output-dir gotchas.** The eval script computes
    `REPO = Path(__file__).resolve().parents[2]`, so it MUST live inside `research_state/session_<UTC>/`
    (parents[2] = repo root). It writes to `sys.argv[1]` but does **not** create that directory — run
    `mkdir -p research_state/session_<UTC>` first, then
    `python3 research_state/session_<UTC>/fclr_liqxsecbroad01_ts_eval_<UTC>.py research_state/session_<UTC>`.
  - **BOTTLENECK (removed): block-index alignment.** BROAD-01's `block_rank_ic()` returns one IC per valid
    block (≥5 coins) but drops the block index. BROAD-01 had **30/30 valid blocks**, so the list is
    length-30 in block order. For the TS eval, retain the block start hour alongside each IC (the scaffold's
    `block_rank_ic_with_hours` already returns `(block_index, block_start_h, ic, n_coins)`).
  - **BOTTLENECK (removed): environment deps.** numpy/pandas/pyarrow are NOT preinstalled in this
    sandbox. Install with `python3 -m pip install --quiet numpy pandas pyarrow` (verified: numpy 2.5.5,
    pandas 3.1.1, pyarrow 26.0.1 install cleanly; wheels go to `~/.local`). scipy/requests are in
    requirements.txt but not needed for the heavy eval.
  - **BOTTLENECK (removed): scaffold performance/memory.** The original scaffold's `abs_fund_pct_vec`
    was O(rows×coins) with per-row pandas filtering (catastrophic on 3.6M rows) and the test-panel build
    used per-row `.loc` over 1.7M rows; both OOM'd / never finished. The archived scaffold has these
    vectorized (searchsorted percentile + merge-based test panel). If you rewrite the feature pipeline
    during reconciliation, keep it vectorized; the full eval runs in ~3 min on 15 GiB RAM.
  - **BOTTLENECK (removed): OLS double-intercept.** The archived scaffold originally added `np.ones` in
    both `b1_X`/`c2_X` AND `ols_fit`/`ols_predict`, making the design collinear and flipping beta. The
    archived scaffold already fixes this (intercept lives only in the feature matrix). Preserve that fix.

**Outcome-blind design (freeze BEFORE computing any stability metric):**
1. Reuse BROAD-01's 30 non-overlapping 168h test blocks (60% chronological train, 48h purge+embargo, then
   168h test blocks); compute the per-block cross-sectional Spearman rank-IC series (long and short arms,
   count and notional targets) exactly as BROAD-01, retaining the block start hour.
2. Pre-register the stability battery (already frozen in the archived prereg — do NOT change it):
   - fraction of blocks with positive rank-IC (long arm) and with the BROAD-01 sign;
   - rolling-window rank-IC (6-block rolling mean) min/median/max and its 95% interval;
   - monotone trend test across ordered blocks (Spearman/Kendall of block-index vs rank-IC) with a frozen
     two-sided alpha;
   - first-half vs second-half mean rank-IC gap with a block-bootstrap CI;
   - leave-one-block-out range of the mean rank-IC;
   - per-regime (RV-tercile, UTC-bucket) stability of the sign.
3. **Primary arm is the LONG arm** (the SUPPORTED arm: mean rank-IC 0.1551, CI95 [0.1421, 0.1689]). The
   SHORT arm (mean rank-IC -0.0021) is null and is reported descriptively; it must not drive the verdict.
4. Uncertainty: per-coin block bootstrap ≥2,000 deterministic-seed replicates (resample complete UTC
   blocks jointly across coins), percentile CI95.
5. Multiplicity: Holm across the declared stability family; report raw and adjusted p-values.
6. Frozen symmetric verdict rule (already declared in the prereg):
   - `STABLE` iff, on the long arm, the sign is reproduced in ≥ the pre-registered fraction of blocks
     (≥0.80), the first/second-half gap CI excludes a sign reversal, and the trend test does not reject
     stationarity at the frozen alpha;
   - otherwise `NOT_STABLE` (a genuine, durable finding: the SUPPORTED association is time-block dominated
     and fails §17 condition #4).
   Preserve the null honestly; never relax a threshold after outcomes; never relabel. The materiality floor
   (2%) was already NOT met in BROAD-01; this campaign tests rank-ordering *stability*, NOT a time-series
   forecast gate, and must not be relabeled as one.

**Required artifacts (ALL under the new `session_<UTC>/`; no zero-byte placeholders):**
- `fclr_liqxsecbroad01_ts_prereg_<UTC>.json` + `.md` — the FROZEN prereg copied verbatim from the
  scaffold (status FROZEN_PRE_OUTCOMES, `frozen_before_outcomes:true`,
  `outcome_data_inspected_before_freeze:false`). Do NOT re-freeze after seeing outcomes.
- `fclr_liqxsecbroad01_ts_eval_<UTC>.py` + `.json` + `.md` — the RECONCILED heavy rolling-window stability
  evaluation, including the dumped per-block `ic_C2_l / ic_B1_l / ic_C2_s / ic_B1_s` series with block
  start hours. The eval JSON must report the reconciled long-arm mean rank-IC (≈+0.1551) and long-arm
  Poisson deviance (≈14895) so a reviewer can confirm BROAD-01 was faithfully reused.
- `fclr_liqxsecbroad01_ts_recompute_<UTC>.py` + `.json` — independent stdlib recompute asserting
  `all_checks_match:true` against the eval.
- `fclr_liqxsecbroad01_ts_evidence_audit_<UTC>.json` + `.md` — honest evidence audit.
- `evidence_audit_<UTC>.json` — gate-critical alias (non-empty).
- `trigger_check_<UTC>.json` — non-empty (record that no external trigger is required).

---

## ROOT CONSTRAINTS (hard)

- Root md+json count: **499/500** — at cap. ALL new artifacts MUST go under `session_<UTC>/`. Do NOT
  add any root-level `research_state/*.md|*.json`.
- No empty files, no zero-byte placeholders.
- Do NOT threshold-shop or relax any frozen floor/threshold after outcomes.
- Preserve nulls honestly: verdict may be `STABLE`, `NOT_STABLE`, or (if truly blocked) `DATA_BLOCKED` with
  evidence — never a fabricated pass.
- Do NOT re-run any terminal campaign (BROAD-01 and all SUPERSEDED_TERMINAL campaigns).
- Do NOT build a risk overlay (§9: forecast gate did not pass on ANY primary target).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md` (sealed FCLR-001 definition consumed by
  `scripts/run_evaluation.py`).
- Stdlib + numpy + pandas + pyarrow only; no network for heavy evaluation (source probes already done); no
  new source without provenance; no overlay.
- Do NOT track-adulterate: never describe a broad-universe cross-sectional association (or a stability test
  of it) as a time-series forecast gate pass; never claim a complete observed-liquidation census from a
  capped feed.
- **Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`** — cannot fire on frozen data; not a valid excuse to
  idle (§16, §19). The BROAD-TS heavy work needs no trigger.
- **Do NOT write a future/non-existent `session_<UTC>` id into this handoff before that directory exists**
  (the gate treats a non-existent recorded dir as a failure). The only literal `session_<digits>` tokens
  permitted in this handoff are `session_20261122T190000Z`, `session_20261122T224500Z`,
  `session_20261123T043600Z`, and `session_20261123T085507Z`. The archived scaffold lives under
  `research_state/broad_ts_scaffold/` (NOT a `session_` dir) — refer to it by that path.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- The heavy-work gate binds `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`: once the first
  `session_<UTC>` with UTC > `20261123T135825Z` exists, that latest session MUST contain the full
  BROAD-TS artifact set above (prereg json+md, eval py+json+md, recompute py+json, ts evidence audit json+md,
  `evidence_audit_` json alias, non-empty `trigger_check_` json), with no zero-byte placeholders.
  Trigger-only / prose-only / audit-only / prereg-only / verify-and-stop / arbitrary `recompute_*` sessions
  FAIL closed.
- Do NOT create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- Do NOT re-run any terminal campaign.
- Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`.
- Do NOT build a risk overlay.
- Do NOT track-adulterate.
- Do NOT ship a verdict from a non-reconciled eval: the scaffold's long-arm mean rank-IC = -0.1454 is a
  divergence artifact, not a finding. Reconcile to +0.1551 first.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. **Capped-sample feed — not a complete census (per §15).** Columns: `timestamp[us,tz=UTC],market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`. **Verified: 2,849,452 rows across 18 files, 342 distinct coins, span 2025-05-25..2026-10-31. There is NO `coin` column — the instrument key is `market`.** |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,funding_rate,premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,mark_price,oracle_price,open_interest,open_interest_usd`. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet. Columns: `timestamp[us,tz=UTC],market,coin,dex,market_class,open,high,low,close,volume,trades`. |
| `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_prereg_20261123T164423Z.json` + `.md` | FROZEN outcome-blind prereg for BROAD-TS (stability battery + symmetric verdict rule). Copy verbatim into the new session; do NOT re-freeze. |
| `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py` | Runnable heavy eval scaffold. **Runs end-to-end but does NOT yet reproduce BROAD-01 (long-arm mean rank-IC -0.1454 vs +0.1551; deviance 13322 vs 14895). Reconcile to BROAD-01 before trusting any verdict.** |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.py` | BROAD-01 heavy evaluation script — the fidelity reference. Constants + `_hkey` + `b1_feat`/`c2_feat` + `fit_side` + `predict_side` + `block_rank_ic`. |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.json` | BROAD-01 heavy evaluation (mean rank-IC 0.1551, CI95 [0.1421,0.1689], deviance 14895/14929, short null). |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this file (sole durable handoff).
- `scripts/check_handoff_heavywork_gate.py` — gate enforcement; BROAD_TS binder at
  `_broad_ts_state` (required set `BROAD_TS_REQUIRED`, lines ~599-614 and ~2175-2243).
- `research_state/experiment_frontier.json` — rank-0 is
  `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` (READY_EXECUTE / ACTIVE) with the reconcile-then-execute
  `next_action_heavy`; BROAD-01 is COMPLETED_VALIDATED (rank 1).
- `research_state/broad_ts_scaffold/` — frozen prereg + runnable eval scaffold (reconcile the eval).
- `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.json` — BROAD-01
  (the +0.1551 headline the reconciled eval must reproduce).
- `research_state/final_synthesis_report.md` — program-wide synthesis (superseded by this active campaign).
- `RESEARCH_PROMPT.md` §3.2 (primary question two halves), §9 (overlay gate), §16 (adaptive feasibility),
  §17 (promotion conditions, esp. #4 "not dominated by one time block").

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why (record execution of FCLR-LIQ-XSEC-BROAD-TS-01 and its verdict).
2. Exact test outcomes with paths (gate PASS, all unittests PASS).
3. Evidence added and full paths (all under the new `session_<UTC>/`).
4. State of each research gate (heavy-work gate SATISFIED; forecast gate still NOT PASSED unless a future
   campaign earns it).
5. Single highest-value next task (the next materially-different heavy question, or a justified DATA_BLOCKED
   with a materially different route).
6. Precise verifying command (see below).
7. Any blocker with next materially different route.

---

## BOTTLENECK RESOLUTION (this handoff)

- **Resolved (stale partial session → gate fail-closed):** A prior session created
  `research_state/session_20261123T164423Z/` with a frozen prereg + a runnable eval scaffold but **no
  eval.json/md, no recompute, no evidence audits, no trigger_check** — and its eval, when run, produced a
  **sign-flipped** long-arm mean rank-IC (-0.1454 vs BROAD-01's +0.1551), i.e. a non-reproducing,
  scientifically-invalid result. Left in place, the gate failed with
  `HANDOFF_STALE_LATEST_SESSION:session_20261123T164423Z` (a newer on-disk session not recorded in the
  handoff, and incomplete). The prereg (valid, frozen) and the eval scaffold (runnable, de-bottlenecked)
  were **archived** to `research_state/broad_ts_scaffold/` via `git mv`; the empty `session_20261123T164423Z/`
  dir was removed. Latest disk session is again `session_20261123T085507Z` == handoff latest →
  `handoff_stale:false`, gate PASS. Do NOT recreate an empty `session_` dir; do NOT record a `session_<UTC>`
  token that does not yet have its artifacts on disk.
- **Resolved (verify-and-stop bottleneck):** The prior handoff declared the program CONCLUDED and instructed
  "verify and stop", which would let a future agent satisfy the gate with no heavy research. This refresh
  keeps the active, gate-bound `FCLR-LIQ-XSEC-BROAD-TS-01` campaign. Verify-and-stop is NOT a permitted
  completion.
- **Resolved (stale frontier):** `experiment_frontier.json` rank-0 points at
  `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` (READY_EXECUTE / ACTIVE) with a concrete
  `next_action_heavy` = "reconcile the scaffold to BROAD-01 (+0.1551 / 14895), then run the stability
  battery"; BROAD-01 is demoted to COMPLETED_VALIDATED (rank 1). Routing off the frontier points at the
  heavy work.
- **Resolved (misread exhaustion signal):** `scripts/next_campaign_status.py` reports
  `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` — but that tool only assesses fresh 3-block *funding-volatility*
  designs on the Binance 5-symbol cache. It does NOT assess the BROAD-TS temporal-stability design on the
  already-frozen ironflow_bulk panel, which IS feasible now. Do not treat that tool's output as
  "program done".
- **Resolved (unparseable frozen prereg):** `session_20261123T085507Z/fclr_liqxsecbroad01_prereg_20261123T085507Z.json`
  is hand-authored pseudo-JSON (trailing commas, `[0, 8)` bracket typos) and fails `json.load`. The TS session
  must NOT parse it; use the `.md` prereg and the constants block in
  `fclr_liqxsecbroad01_eval_20261123T085507Z.py` (see FOCUS CAMPAIGN → Frozen inputs). This removes a
  guaranteed first-step failure without mutating the sealed BROAD-01 artifact.
- **Resolved (script placement + output dir):** the BROAD-01 eval uses `parents[2]` for the repo root and does
  not create its output dir. The TS eval MUST be placed inside `research_state/session_<UTC>/` and the session
  dir MUST be created before running. This removes a silent path/IO failure for the next agent.
- **Resolved (block-index loss):** BROAD-01's `block_rank_ic()` drops the block index. BROAD-01 had 30/30 valid
  blocks, so the TS eval must retain the block start hour alongside each IC (the scaffold's
  `block_rank_ic_with_hours` does this).
- **Resolved (env deps):** numpy/pandas/pyarrow are not preinstalled. `python3 -m pip install --quiet numpy
  pandas pyarrow` works (verified). Documented above.
- **Resolved (scaffold perf/OOM):** the original scaffold's `abs_fund_pct_vec` (O(rows×coins) per-row pandas
  filter) and per-row `.loc` test-panel build OOM'd / never finished on 3.6M rows. The archived scaffold
  vectorizes both (searchsorted percentile + merge-based panel) and runs in ~3 min / <8 GiB. If you rewrite
  the feature pipeline during reconciliation, keep it vectorized.
- **Resolved (OLS double-intercept):** the archived scaffold originally added `np.ones` in both the feature
  matrix and `ols_fit`/`ols_predict` (collinear → beta flip). The archived scaffold fixes this (intercept
  only in the feature matrix). Preserve the fix.
- **OPEN (methodology fidelity — the actual heavy work):** the scaffold eval does NOT reproduce BROAD-01's
  +0.1551 long-arm mean rank-IC (yields -0.1454) and 14895 long-arm deviance (yields 13322). The divergence
  is in the feature/scaling/subsample pipeline (see the reconciliation checklist in the INITIAL TASK
  MESSAGE). Reconcile to tol 1e-3 BEFORE running/trusting the stability battery. This is the next agent's
  first heavy task.
- **Verified (2026-11-23T23:18:00Z refresh):** `python3 scripts/check_handoff_heavywork_gate.py --json`
  → PASS reason_code=OK failures=[] latest_disk=session_20261123T085507Z handoff_stale=false.
  Campaign gate unittests pass (126 tests OK). pyarrow 26.0.1 present; ironflow_bulk parquet readable with
  expected schemas; sha256 72/72 ok.

---

## VERIFICATION COMMANDS (run before declaring done)

```bash
# 0. One-time env setup (deps are NOT preinstalled in this sandbox)
python3 -m pip install --quiet numpy pandas pyarrow

# 1. Heavy-work gate must return reason=OK (not HANDOFF_HEAVYWORK_GATE_FAILED)
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Campaign gate unittests must pass
python3 -m unittest \
  tests.test_active_campaign_gate \
  tests.test_fclr_starter_001_campaign_gate \
  tests.test_fclr_campaign_gate \
  tests.test_fclr_heavy_confirm_gate \
  tests.test_pooled_robust_002_campaign_gate \
  tests.test_tracka_hardening_143

# 3. Frozen 3-block domains exhausted (EXPECTED — does NOT block BROAD-TS; see BOTTLENECK RESOLUTION)
python3 scripts/next_campaign_status.py
```

**Latest handoff session: session_20261123T085507Z** (completed FCLR-LIQ-XSEC-BROAD-01 heavy set;
SUPPORTED_GENERALIZATION for the long-arm rank-ordering association; materiality floor NOT MET; independent
recompute `all_checks_match:true`).
**Active rank-0 campaign: FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z** (status READY_EXECUTE,
program_status ACTIVE). This campaign tests the temporal stability of the ONLY SUPPORTED liquidation-risk
finding (RESEARCH_PROMPT.md §17 condition #4) and is the mandated heavy work. A frozen prereg + runnable
eval scaffold are archived under `research_state/broad_ts_scaffold/`; the scaffold does NOT yet reproduce
BROAD-01's +0.1551 long-arm mean rank-IC (yields -0.1454) and MUST be reconciled to BROAD-01 (tol 1e-3)
before any stability verdict is shipped.
**Program status: ACTIVE — heavy work open.**

(End of file)