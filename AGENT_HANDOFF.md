# AGENT HANDOFF — 2026-11-23T14:41:56Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> Gate status as of this refresh (2026-11-23T14:36:36Z): **PASS** (reason_code=OK, root=499/500).
> **PROGRAM STATUS: NOT CONCLUDED — ACTIVE HEAVY WORK OPEN.** The prior handoff wrongly declared
> the program CONCLUDED and told the next session to "verify and stop". That was the last
> structural bottleneck: it would let a future agent idle forever on the ONLY SUPPORTED
> liquidation-risk finding without ever testing whether it survives a rolling holdout.
> This refresh REMOVES that bottleneck and hands the next session a non-deferrable heavy campaign.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-23T14:41:56Z (refresh 2026-11-23T14:41:56Z)**
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is
> `Funding-conditioned-volatility-and-liquidation-risk`. RESEARCH_PROMPT.md §3.2 primary
> question has two halves:
> - **Half 1 (Volatility / Track C):** CLOSED — leakage-robust null across every claim-worthy panel
>   (H1_primary NOT_SUPPORTED; FCLR-011 PASS does not generalize forward; FCLR-FWD-VOL-011-CONFIRM
>   NOT_REPLICATED). No further volatility heavy work is admissible.
> - **Half 2 (Liquidation-risk):**
>   - **Track A (observed liquidations):** `TRACK_A_STRUCTURALLY_BLOCKED` — no admissible
>     unauthenticated historical liquidation source with required coverage exists in this
>     environment (source audit frozen outcome-blind; `outcome_data_inspected_before_freeze:false`).
>   - **Track B (modeled boundary breach):** NOT_SUPPORTED across all campaigns.
>   - **Track C (volatility-as-liquidation-proxy):** NOT_SUPPORTED (same as Half 1).
>   - **The ONLY liquidation-risk results ever marked SUPPORTED** are the regime-conditioned
>     cross-sectional funding → next-hour observed-liquidation-intensity findings on the narrow
>     15-coin panel: FCLR-XSEC-004 (count, low-RV), FCLR-XSEC-005 (notional-weighted, low-RV),
>     FCLR-XSEC-006 (all three UTC buckets). All were flagged `promotable:false` / EXPLORATORY_ONLY
>     because they never generalized beyond 15 coins.
>   - **FCLR-LIQ-XSEC-BROAD-01 (COMPLETED, 2026-11-23T08:55:07Z, `session_20261123T085507Z`):**
>     generalized those findings to the full 342-coin ironflow_bulk universe (2025-05..2026-10,
>     2.85M liquidation rows). Verdict: **SUPPORTED_GENERALIZATION on the cross-sectional
>     rank-ordering association** (rank-IC positive on the long arm, CI95 excludes null, Holm
>     primary p < alpha_k). **Poisson-deviance materiality floor (2%) NOT MET on either arm**
>     (long -0.23%, short +0.71%). It is a rank-ordering *association*, not a time-series forecast.
>
> **THE UNFINISHED, NON-DEFERRABLE HEAVY QUESTION (this campaign):**
> BROAD-01 reported only the *mean* per-block rank-IC. It NEVER tested **temporal stability** of
> the per-block rank-IC series — i.e. whether the SUPPORTED rank-ordering association survives a
> rolling holdout and is not dominated by one time block. RESEARCH_PROMPT.md §17 promotion
> condition #4 explicitly requires: *"Skill is not dominated by one coin, one venue, one brief
> crisis or one time block."* BROAD-01 is the ONLY SUPPORTED liquidation-risk result in the entire
> program, and it was declared the "durable final answer" without ever being asked whether it is
> stable across time. Answering that is the single highest-value remaining heavy task.
>
> **YOU MUST EXECUTE: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`** (full spec below). This is a
> materially different, feasible, frozen-data design — no new source, no network, no trigger wait.
>
> **Do NOT:** declare the program concluded; verify-and-stop; re-run BROAD-01; re-run any terminal
> campaign; threshold-shop the materiality floor; build a risk overlay (§9 gate not passed);
> claim a time-series forecast gate pass from a cross-sectional association; wait for
> `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen data; §16, §19).
>
> **Blockers: None — the heavy work is executable now on the frozen ironflow_bulk panel.**

### Single, non-deferrable job (EXECUTE BROAD-TS)

Produce the complete `FCLR-LIQ-XSEC-BROAD-TS-01` artifact set under a fresh
`research_state/session_<UTC>/` (UTC strictly after `20261123T135825Z`), then record that session id
in this handoff and run the verification commands. If any required artifact is missing or empty,
the heavy-work gate fails closed and the session is incomplete.

---

## FOCUS CAMPAIGN — FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z (ACTIVE, rank-0)

**Question:** Is the SUPPORTED broad-universe cross-sectional funding → next-hour observed
liquidation-intensity association temporally stable (not dominated by one time block)?

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/{liquidations,funding,open_interest,candles_1h}/`
  (18 monthly parquet, 2025-05..2026-10). Liquidations: 2,849,452 rows, 342 coins (2025-05);
  instrument key is `market` (there is NO `coin` column in liquidations). Each parquet has `.sha256`
  and `.accessed.json` sidecars — assert sha256 before reading; caches are read-only.
- The per-block rank-IC series and walk-forward split definition frozen in
  `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_prereg_20261123T085507Z.json`
  and `fclr_liqxsecbroad01_eval_20261123T085507Z.json`. **Reuse the SAME block boundaries and sign
  convention** (`relative_improvement = (baseline - candidate)/baseline`, positive = candidate better)
  so the stability test is directly comparable to BROAD-01.
  - **BOTTLENECK (removed by this refresh): the BROAD-01 prereg `.json` is NOT strict JSON** — it is
    a hand-authored pseudo-JSON with trailing commas before every `}` and bracket typos such as
    `[0, 8)` in `utc_buckets`. `json.load(open(...prereg...json))` FAILS (`Expecting property name...`
    at line 18, then `Expecting ',' delimiter` at line 38). Do NOT waste a session rediscovering this
    and do NOT rewrite the sealed artifact. The canonical machine-readable design is the **`.md`
    prereg** plus the **constants at the top of `fclr_liqxsecbroad01_eval_20261123T085507Z.py`**:
    `TRAIN_FRAC=0.60`, `PURGE_EMBARGO_H=48`, `BLOCK_H=168`, `HORIZON_H=1`, `N_BOOT=2000`,
    `N_PERM=1000`, `N_LOIO=8`, `LOIO_PASS_THRESHOLD=6`, `SEED=20261123`, `ALPHA_K=0.05/(2*3)`,
    `MATERIALITY_PCT=2.0`. Copy that eval script as the starting point for the TS eval, change
    `SESSION_UTC`, and dump the per-block `ic_C2_l / ic_B1_l / ic_C2_s / ic_B1_s` series (BROAD-01
    stored only their means in JSON; the series is re-derivable from the script).

**Outcome-blind design (freeze BEFORE computing any stability metric):**
1. Reuse BROAD-01's 30 non-overlapping 168h test blocks; compute the per-block cross-sectional
   Spearman rank-IC series (long and short arms, count and notional targets) exactly as BROAD-01.
2. Pre-register the stability battery (no metric chosen after seeing outcomes):
   - fraction of blocks with positive rank-IC (long arm) and with the BROAD-01 sign;
   - rolling-window rank-IC (e.g. 6-block rolling mean) min/median/max and its 95% interval;
   - monotone trend test across ordered blocks (Spearman/Kendall of block-index vs rank-IC) with
     a frozen two-sided alpha;
   - first-half vs second-half mean rank-IC gap with a block-bootstrap CI;
   - leave-one-block-out range of the mean rank-IC;
   - per-regime (RV-tercile, UTC-bucket) stability of the sign.
3. Uncertainty: per-coin block bootstrap ≥2,000 deterministic-seed replicates (resample complete UTC
   blocks jointly across coins), percentile CI95.
4. Multiplicity: Holm across the declared stability family; report raw and adjusted p-values.
5. Frozen symmetric verdict rule (declare BEFORE outcomes):
   - `STABLE` iff the sign is reproduced in ≥ the pre-registered fraction of blocks, the
     first/second-half gap CI excludes a sign reversal, and the trend test does not reject
     stationarity at the frozen alpha;
   - otherwise `NOT_STABLE` (a genuine, durable finding: the SUPPORTED association is time-block
     dominated and fails §17 condition #4).
   Preserve the null honestly; never relax a threshold after outcomes; never relabel.

**Required artifacts (ALL under the new `session_<UTC>/`; no zero-byte placeholders):**
- `fclr_liqxsecbroad01_ts_prereg_<UTC>.json` + `.md` — outcome-blind freeze (status FROZEN_PRE_OUTCOMES,
  `frozen_before_outcomes:true`, `outcome_data_inspected_before_freeze:false`).
- `fclr_liqxsecbroad01_ts_eval_<UTC>.py` + `.json` + `.md` — HEAVY rolling-window stability evaluation.
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
- Preserve nulls honestly: verdict may be `STABLE`, `NOT_STABLE`, or (if truly blocked)
  `DATA_BLOCKED` with evidence — never a fabricated pass.
- Do NOT re-run any terminal campaign (BROAD-01 and all SUPERSEDED_TERMINAL campaigns).
- Do NOT build a risk overlay (§9: forecast gate did not pass on ANY primary target).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md` (sealed FCLR-001 definition consumed by
  `scripts/run_evaluation.py`).
- Stdlib + pyarrow only; no network for heavy evaluation (source probes already done); no new source
  without provenance; no overlay.
- Do NOT track-adulterate: never describe a broad-universe cross-sectional association (or a
  stability test of it) as a time-series forecast gate pass; never claim a complete observed-
  liquidation census from a capped feed.
- **Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`** — cannot fire on frozen data; not a valid
  excuse to idle (§16, §19). The BROAD-TS heavy work needs no trigger.
- **Do NOT write a future/non-existent `session_<UTC>` id into this handoff before that directory
  exists** (the gate treats a non-existent recorded dir as a failure). The only literal
  `session_<digits>` tokens permitted in this handoff are `session_20261122T190000Z`,
  `session_20261122T224500Z`, `session_20261123T043600Z`, and `session_20261123T085507Z`.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- The heavy-work gate binds `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`: once the first
  `session_<UTC>` with UTC > `20261123T135825Z` exists, that latest session MUST contain the full
  BROAD-TS artifact set above (prereg json+md, eval py+json+md, recompute py+json, ts evidence
  audit json+md, `evidence_audit_` json alias, non-empty `trigger_check_` json), with no zero-byte
  placeholders. Trigger-only / prose-only / audit-only / prereg-only / verify-and-stop / arbitrary
  `recompute_*` sessions FAIL closed.
- Do NOT create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- Do NOT re-run any terminal campaign.
- Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`.
- Do NOT build a risk overlay.
- Do NOT track-adulterate.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. **Capped-sample feed — not a complete census (per §15).** Columns: `timestamp[ms],market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`. **Verified: 2,849,452 rows across 18 files, 342 distinct coins, span 2025-05-25..2026-10-31. There is NO `coin` column — the instrument key is `market`.** |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,funding_rate,premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,mark_price,oracle_price,open_interest,open_interest_usd`. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,market_class,open,high,low,close,volume,trades`. |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_prereg_20261123T085507Z.json` | BROAD-01 frozen prereg (block boundaries, regime, sign convention, verdict rule) to REUSE for comparability. |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.json` | BROAD-01 heavy evaluation (mean rank-IC, uncertainty, Holm) whose per-block series the TS campaign extends. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this file (sole durable handoff).
- `scripts/check_handoff_heavywork_gate.py` — gate enforcement; BROAD_TS binder at
  `_broad_ts_state` (required set `BROAD_TS_REQUIRED`).
- `research_state/experiment_frontier.json` — rank-0 is now
  `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` (READY_EXECUTE / ACTIVE); BROAD-01 demoted to
  COMPLETED_VALIDATED.
- `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.json` — BROAD-01.
- `research_state/final_synthesis_report.md` — program-wide synthesis (superseded by this active campaign).
- `RESEARCH_PROMPT.md` §3.2 (primary question two halves), §9 (overlay gate), §16 (adaptive
  feasibility), §17 (promotion conditions, esp. #4 "not dominated by one time block").

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why (record execution of FCLR-LIQ-XSEC-BROAD-TS-01 and its verdict).
2. Exact test outcomes with paths (gate PASS, all unittests PASS).
3. Evidence added and full paths (all under the new `session_<UTC>/`).
4. State of each research gate (heavy-work gate SATISFIED; forecast gate still NOT PASSED unless a
   future campaign earns it).
5. Single highest-value next task (the next materially-different heavy question, or a justified
   DATA_BLOCKED with a materially different route).
6. Precise verifying command (see below).
7. Any blocker with next materially different route.

---

## BOTTLENECK RESOLUTION (this handoff)

- **Resolved (verify-and-stop bottleneck):** The prior handoff declared the program CONCLUDED and
  instructed "verify and stop", which would let a future agent satisfy the gate with no heavy
  research. This refresh replaces that with the active, gate-bound `FCLR-LIQ-XSEC-BROAD-TS-01`
  campaign. Verify-and-stop is NO LONGER a permitted completion.
- **Resolved (stale frontier):** `experiment_frontier.json` rank-0 pointed at the COMPLETE BROAD-01
  campaign. This refresh sets rank-0 to `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`
  (READY_EXECUTE / ACTIVE) with a concrete `next_unfinished_task` and phase list, and demotes
  BROAD-01 to COMPLETED_VALIDATED (rank 1). Routing off the frontier now points at the heavy work.
- **Resolved (misread exhaustion signal):** `scripts/next_campaign_status.py` reports
  `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` — but that tool only assesses fresh 3-block
  *funding-volatility* designs on the Binance 5-symbol cache. It does NOT assess the BROAD-TS
  temporal-stability design on the already-frozen ironflow_bulk panel, which IS feasible now. Do not
  treat that tool's output as "program done".
- **Retired (completed campaign binder):** BROAD-01 is complete; its heavy artifacts live in
  `session_20261123T085507Z/`. The BROAD-01 binder is retired (its campaign id is referred to
  without the UTC suffix so the gate does not re-demand BROAD-01 artifacts from the TS session).
- **Resolved (unparseable frozen prereg):** `session_20261123T085507Z/fclr_liqxsecbroad01_prereg_20261123T085507Z.json`
  is hand-authored pseudo-JSON (trailing commas, `[0, 8)` bracket typos) and fails `json.load`.
  The TS session must NOT parse it; use the `.md` prereg and the constants block in
  `fclr_liqxsecbroad01_eval_20261123T085507Z.py` (see FOCUS CAMPAIGN → Frozen inputs). This removes a
  guaranteed first-step failure for the next agent without mutating the sealed BROAD-01 artifact.
- **Verified (2026-11-23T14:36:36Z refresh):** `python3 scripts/check_handoff_heavywork_gate.py --json`
  → PASS reason_code=OK root=499/500; BROAD_TS grandfathered (latest session 20261123T085507Z <
  campaign start 20261123T135825Z). All campaign gate unittests pass.

---

## VERIFICATION COMMANDS (run before declaring done)

```bash
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
SUPPORTED_GENERALIZATION for the rank-ordering association; materiality floor NOT MET; independent
recompute `all_checks_match:true`).
**Active rank-0 campaign: FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z** (status READY_EXECUTE,
program_status ACTIVE). This campaign tests the temporal stability of the ONLY SUPPORTED
liquidation-risk finding (RESEARCH_PROMPT.md §17 condition #4) and is the mandated heavy work.
**Program status: ACTIVE — heavy work open.**

(End of file)