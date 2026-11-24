# AGENT HANDOFF — 2026-11-24T01:28:23Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: NOT CONCLUDED — ACTIVE HEAVY WORK OPEN.**
> Active rank-0 campaign: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`.
> **FIDELITY IS NOW RESOLVED (bit-exact) and the reconciled scaffold emits a valid
> `NOT_STABLE` verdict.** The remaining work is to materialize the full BROAD_TS artifact set
> under a fresh `session_<UTC>/` and close the session. Verify-and-stop, prereg-only, prose-only,
> trigger-only, audit-only, and non-reconciled verdicts are forbidden completion modes.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-24T01:28:23Z**
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is
> `Funding-conditioned-volatility-and-liquidation-risk`. RESEARCH_PROMPT.md §3.2 has two halves:
> - **Half 1 (Volatility / Track C):** CLOSED — leakage-robust null across every claim-worthy panel
>   (H1_primary NOT_SUPPORTED; FCLR-011 PASS does not generalize forward; FCLR-FWD-VOL-011-CONFIRM
>   NOT_REPLICATED). No further volatility heavy work is admissible.
> - **Half 2 (Liquidation-risk):**
>   - **Track A (observed liquidations):** `TRACK_A_STRUCTURALLY_BLOCKED` as a complete-census claim;
>     the ironflow_bulk liquidation feed is a capped sample and cannot establish absence.
>   - **Track B (modeled boundary breach):** NOT_SUPPORTED across all campaigns.
>   - **Track C (volatility-as-liquidation-proxy):** NOT_SUPPORTED.
>   - The only liquidation-risk results marked SUPPORTED are the regime-conditioned cross-sectional
>     funding → next-hour observed-liquidation-intensity findings on the narrow 15-coin panel:
>     FCLR-XSEC-004/005/006, all EXPLORATORY_ONLY / `promotable:false`.
>   - **FCLR-LIQ-XSEC-BROAD-01 (COMPLETED, `session_20261123T085507Z`):** generalized those findings
>     to the full ironflow_bulk universe (2025-05..2026-10; 2,849,452 liquidation rows). Verdict:
>     **SUPPORTED_GENERALIZATION on cross-sectional rank ordering** (long-arm mean rank-IC
>     **0.1551333434568285**, block-bootstrap CI95 [0.142081, 0.168895]; short-arm mean rank-IC
>     -0.002054). Poisson-deviance materiality floor (2%) NOT met on either arm. This is an
>     association, not a time-series forecast or a complete liquidation census.
>   - **FCLR-LIQ-XSEC-BROAD-TS-01 (ACTIVE, `20261123T135825Z`):** tests whether that SUPPORTED
>     broad-universe association is temporally stable (not dominated by one time block) per
>     RESEARCH_PROMPT.md §17 promotion condition #4.
>
> **THE ACTIVE HEAVY QUESTION:** Is the SUPPORTED broad-universe cross-sectional funding → next-hour
> observed-liquidation-intensity association temporally stable across BROAD-01's 30 ordered 168h
> test blocks?
>
> **STATE OF THE WORK (read before doing anything):**
> - The outcome-blind prereg is frozen under `research_state/broad_ts_scaffold/`:
>   `fclr_liqxsecbroad01_ts_prereg_20261123T164423Z.json` + `.md`
>   (`FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes:true`,
>   `outcome_data_inspected_before_freeze:false`). Copy it verbatim into the new session; do not
>   re-freeze it and do not edit sealed artifacts.
> - The runnable eval scaffold is
>   `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py`.
> - **FIDELITY IS RESOLVED (this refresh):** the scaffold now reproduces BROAD-01's sealed headline
>   BIT-EXACTLY. Verified run (archived at
>   `research_state/broad_ts_scaffold/verified_reconciled_run_20261124T012700Z/`):
>   - long mean rank-IC = **0.1551333434568285** (abs error **0.0** vs BROAD-01),
>   - long B1 Poisson deviance = **14895.300476998453** (abs error **0.0**),
>   - long C2 deviance = 14929.610988, short B1 = 13423.736369, short C2 = 13328.791641 (all match),
>   - smear_B1 = 3361.8521903545097, smear_C2 = 3371.0200433164528 (bit-exact),
>   - `fidelity_reconciliation.reconciled: true`.
> - The reconciled scaffold runs the FULL frozen stability battery and emits **Verdict: NOT_STABLE**
>   (mean_IC_C2_long = 0.155133). The verdict is driven by the frozen symmetric rule: sign
>   reproduction 30/30 = 1.00 (≥ 0.80 PASS) AND ordered-block trend p = 0.048951 ≥ alpha_k
>   (stationarity not rejected PASS) **but** the first/second-half gap CI95 = [-0.026532, 0.026818]
>   INCLUDES 0 (does NOT exclude a sign reversal → FAIL) ⇒ **NOT_STABLE**. This is a genuine,
>   durable finding: the SUPPORTED association is time-block dominated and fails §17 condition #4.
>   It is a valid, honest outcome — preserve it; never relabel it as a forecast-gate pass or a census.
> - Regime code is now prereg-aligned: RV-tercile sign stability is computed per (block × tercile)
>   cell (38/90 positive, frac 0.4222) and UTC-session buckets are Asian [0,8) / European [8,16) /
>   US [16,24) (3/3 buckets positive). The primary verdict does NOT depend on these descriptive arms.
> - The contradictory terminal-closure handoff remains archived at
>   `research_state/handoff_archive/AGENT_HANDOFF_20261123T163509Z.md`. This file is the only root
>   durable handoff.
> - The invalid 23:56 UTC run is archived at
>   `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/`. **DO NOT ship or cite its
>   `NOT_STABLE`** — it came from a pre-fix, non-reconciled scaffold. The NOT_STABLE you may ship
>   is the one produced by the now-reconciled scaffold under a fresh session.
>
> **YOU MUST EXECUTE: MATERIALIZE THE FULL BROAD_TS ARTIFACT SET AND CLOSE THE SESSION.**
> The hard fidelity work is DONE. Do not re-derive it and do not edit the scaffold's numerics.
>
> 1. Create a fresh `research_state/session_<UTC>/` with UTC strictly after `20261123T135825Z`
>    (a new timestamped directory). Copy the frozen prereg JSON+MD verbatim from
>    `broad_ts_scaffold/`. Do NOT re-freeze and do NOT edit sealed artifacts.
> 2. Copy the fixed scaffold to the session as `fclr_liqxsecbroad01_ts_eval_<UTC>.py`. Update its
>    `SESSION_UTC` constant to the new session UTC (keep the campaign id
>    `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` unchanged). The script writes
>    `fclr_liqxsecbroad01_ts_eval_<SESSION_UTC>.{json,md}` and stamps `session_utc` from it. Keep
>    all numerics identical — it is bit-faithful to BROAD-01.
> 3. Run the eval to produce `fclr_liqxsecbroad01_ts_eval_<UTC>.{py,json,md}`. It MUST pass the
>    internal fidelity check (`reconciled:true`, long rank-IC 0.1551333434568285 within 1e-3, long
>    B1 deviance 14895 within 1e-3) and emit the full per-block series `ic_C2_l`, `ic_B1_l`,
>    `ic_C2_s`, `ic_B1_s` with `block_start_h`.
> 4. Produce `fclr_liqxsecbroad01_ts_recompute_<UTC>.{py,json}` — an INDEPENDENT stdlib recompute
>    that re-derives the long-arm mean rank-IC and B1 deviance (and the sign-reproduction fraction)
>    from the emitted per-block series / a fresh stdlib pass and asserts `all_checks_match:true`.
>    It must not import the eval module's numerics; it is a cross-check.
> 5. Produce `fclr_liqxsecbroad01_ts_evidence_audit_<UTC>.{json,md}`, the gate-critical non-empty
>    alias `evidence_audit_<UTC>.json`, and a non-empty `trigger_check_<UTC>.json` recording that no
>    external trigger is required (frozen data; §16/§19 — NEW_OBSERVED_LIQUIDATION_SOURCE cannot
>    fire on frozen data and is not a valid reason to idle).
> 6. Record the new session id in THIS handoff ONLY AFTER every required artifact exists and is
>    non-empty. Then run the verification commands below. If any required artifact is missing or
>    zero-byte, the heavy-work gate fails closed.
> 7. Close out per SESSION CLOSE-OUT REQUIREMENTS, answering RESEARCH_PROMPT.md §19.
>
> **Optional (non-verdict-critical) refinement:** the Holm 6-arm family currently reuses the primary
> bootstrap p for `loio_range`, `rolling_mean_min`, `per_regime_rv_tercile`, and
> `per_regime_utc_bucket`. The STABLE/NOT_STABLE verdict does NOT depend on Holm, so this does not
> block shipping; if you improve it, use test-specific permutation/binomial p-values and do not
> change the frozen verdict rule or thresholds.
>
> **Do NOT:** declare the program concluded; verify-and-stop; re-run BROAD-01 as a terminal campaign;
> ship the archived invalid `NOT_STABLE` without a reconciled eval; relax the 1e-3 tolerance; edit
> the frozen prereg; threshold-shop the 2% materiality floor; build a risk overlay (§9 gate not
> passed); claim a time-series forecast gate pass from a cross-sectional association; wait for
> `NEW_OBSERVED_LIQUIDATION_SOURCE`; create an empty partial session; or add root-level
> research-state files.

### Single, non-deferrable job (MATERIALIZE BROAD_TS)

Produce the complete `FCLR-LIQ-XSEC-BROAD-TS-01` artifact set under a fresh
`research_state/session_<UTC>/` (UTC strictly after `20261123T135825Z`), using the frozen prereg and
the now-fidelity-reconciled scaffold as inputs. The eval will emit **NOT_STABLE**; ship that verdict
honestly. Record that session id in this handoff only after its required files exist. If any required
artifact is missing or empty, the heavy-work gate fails closed.

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
  `BLOCK_H=168`, `HORIZON_H=1`, `N_BOOT=2000`, `N_PERM=1000`, `N_LOIO=8`, `LOIO_PASS_THRESHOLD=6`,
  `SEED=20261123`, `ALPHA_K=0.05/(2*3)`, `MATERIALITY_PCT=2.0`.
- Sign convention: `relative_improvement = (baseline - candidate) / baseline`; positive means the
  candidate is better. Do not reverse the sign to manufacture agreement.
- The BROAD-01 prereg JSON is hand-authored pseudo-JSON and is not strict `json.load`-parseable. Use
  its `.md` plus the constants in the sealed eval script. Do not rewrite the sealed artifact.

**Fidelity resolution (this refresh — the scaffold is now bit-faithful):**
The 0.00567 rank-IC gap was NOT machine-epsilon. It was a real methodological divergence, now fixed
by reproducing BROAD-01's exact reference behavior:
- **`ma_dev` numerator:** in BROAD-01's second per-hour loop the local `c` is never reassigned, so it
  equals the market's LAST close (left over from the returns loop). The scaffold previously used the
  current-hour close, which changed the funding-conditioned fit materially. Now uses `last_close`.
- **Duan smearing residual:** BROAD-01's fit loop maps `fi <= 0 → 1.0`, but its residual loop only
  maps `None → 1.0` (so `fi = 0.0` rows use `log(EPS)` in the residual). The scaffold previously
  applied `0 → 1.0` to both, inflating the smear. Now reproduces the split.
- **Liquidation notional accumulation:** replaced pandas `groupby().sum()` with BROAD-01's sequential
  Python `+=` in (month, row) order (eliminates machine-epsilon divergence on a few notional groups).
- **Train-only mean/std:** sequential Python `sum`/`pstd` in coin-major order (replaces numpy pairwise
  mean/std).
- **Feature logs:** scalar `math.log(max(v,0)+eps)` (replaces `np.log`, which can differ by 1 ULP).
After these fixes the long-arm mean rank-IC and B1 deviance reproduce BROAD-01 to **0.0** abs error.

**Frozen battery already implemented in the scaffold (do not re-derive):**
sign-reproduction fraction (threshold 0.80), 6-block rolling mean min/median/max and CI95, ordered-
block Spearman trend test at frozen alpha_k, first/second-half gap with block-bootstrap CI95,
leave-one-block-out range, leave-one-instrument-out (8 subsets, ≥6 pass), per-regime RV-tercile and
Asian/European/US UTC-bucket sign stability, Holm across the declared 6-arm family, and the symmetric
STABLE/NOT_STABLE verdict. All four per-block series (`ic_C2_l`, `ic_B1_l`, `ic_C2_s`, `ic_B1_s`)
with block start hours are preserved.

**Required artifacts (ALL under the new session directory; no zero-byte placeholders):**
- `fclr_liqxsecbroad01_ts_prereg_<UTC>.json` + `.md` — verbatim frozen prereg copy.
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
  blocker; never a fabricated pass. The reconciled scaffold emits `NOT_STABLE`; ship it honestly.
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
  `session_20261123T043600Z`, and `session_20261123T085507Z`. Use the placeholder `session_<UTC>`
  for the session you create; record its real id here only after its artifacts exist.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- The heavy-work gate binds `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`: once the first post-start
  session exists, that latest session MUST contain the full BROAD_TS artifact set above, with no
  zero-byte placeholders. Trigger-only, prose-only, audit-only, prereg-only, verify-and-stop,
  arbitrary `recompute_*`, and non-reconciled eval sessions FAIL closed.
- Do not create a partial session directory and leave it unrecorded; that causes
  `HANDOFF_STALE_LATEST_SESSION` and blocks all later work.
- Do not re-run any terminal campaign.
- Do not wait for an external trigger.
- Do not build a risk overlay.
- Do not track-adulterate.
- Do not ship a verdict from a non-reconciled eval. The scaffold now passes fidelity and only emits a
  verdict after `reconciled:true`; preserve that fail-closed behavior.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. Capped-sample feed, not a census. Columns include `timestamp[us,tz=UTC],market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; funding and premium features. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; OI, mark, and oracle prices. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet; hourly close and instrument identity. |
| `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_prereg_20261123T164423Z.json` + `.md` | Frozen outcome-blind TS prereg. |
| `research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py` | **Fidelity-reconciled** heavy eval scaffold (bit-exact to BROAD-01; emits NOT_STABLE). |
| `research_state/broad_ts_scaffold/verified_reconciled_run_20261124T012700Z/` | Verified reconciled run: eval json+md + console log (evidence fidelity passes and NOT_STABLE). |
| `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/` | Archived pre-fix non-reconciled output; evidentiary only, never a verdict source. |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.py` | Sealed BROAD-01 fidelity reference. |
| `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.json` | Sealed BROAD-01 headline: +0.1551333434568285 long mean rank-IC; 14895.300476998453 B1 deviance. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate
caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3.2, §9, §15, §16, §17, and §19.
- `scripts/check_handoff_heavywork_gate.py` — BROAD_TS binder and required artifact set.
- `research_state/experiment_frontier.json` — rank-0 is the active BROAD-TS campaign (kept
  READY_EXECUTE/ACTIVE; `NOT_STABLE` is not an allowed rank-0 COMPLETE verdict, so the campaign stays
  active until the session artifact set is produced and a new rank-0 is promoted).
- `research_state/broad_ts_scaffold/` — frozen prereg, fidelity-reconciled eval, verified run, invalid run.
- `research_state/session_20261123T085507Z/` — sealed BROAD-01 reference and headline.
- `research_state/final_synthesis_report.md` — historical synthesis, superseded by the active gap.

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why, including the BROAD-01 fidelity result (now reconciled, abs error 0.0).
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

- **RESOLVED (bit-level fidelity — the primary blocker):** the scaffold now reproduces BROAD-01's
  sealed headline BIT-EXACTLY (long mean rank-IC 0.1551333434568285 and B1 deviance
  14895.300476998453, both abs error 0.0; smears bit-exact). Root cause was a real methodological
  divergence, not machine epsilon: (a) `ma_dev` used the current-hour close instead of BROAD-01's
  last-close reference quirk; (b) the Duan-smearing residual applied `0→1.0` instead of BROAD-01's
  `None→1.0`-only rule; (c) pandas groupby-sum replaced BROAD-01's sequential notional `+=`; (d)
  numpy pairwise mean/std and `np.log` replaced BROAD-01's sequential `sum`/`pstd` and `math.log`.
  Verified in `broad_ts_scaffold/verified_reconciled_run_20261124T012700Z/`. Do not relax tolerance;
  do not re-derive; copy the fixed scaffold.
- **RESOLVED (regime implementation):** RV-tercile sign stability now uses per-(block × tercile)
  cells (38/90 positive) and UTC buckets are Asian [0,8)/European [8,16)/US [16,24) (3/3 positive),
  per the frozen prereg. The primary verdict does not depend on these descriptive arms.
- **RESOLVED (stale partial run → gate fail-closed):** the unrecorded 23:56 UTC run contained only
  eval files from the pre-fix, non-reconciled scaffold. Its `NOT_STABLE` was a divergence artifact.
  It is archived under `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/`. Do not
  recreate it; do not cite its verdict.
- **RESOLVED (multiple durable handoffs):** the contradictory terminal-closure file is at
  `research_state/handoff_archive/AGENT_HANDOFF_20261123T163509Z.md`; `AGENT_HANDOFF.md` is the only
  root handoff.
- **RESOLVED (verify-and-stop bottleneck):** the active heavy campaign remains rank-0; verify-and-stop
  is not a permitted completion.
- **OPEN (artifact materialization):** the full BROAD_TS artifact set (eval + recompute +
  evidence_audit + alias + trigger_check) must be produced under a fresh `session_<UTC>/`. The eval
  is ready (bit-exact, NOT_STABLE); the recompute, evidence audit, and trigger check remain to be
  written. This is the next agent's single job.
- **OPEN (non-verdict-critical):** Holm 6-arm family reuses the primary bootstrap p for four arms.
  Does not affect the STABLE/NOT_STABLE verdict; optional refinement only.
- **Verified (2026-11-24T01:28:23Z refresh):** scaffold compiles and passes fidelity; verified run
  archived; gate green (broad_ts required=false, grandfathered until a post-start session exists);
  126 campaign-gate unit tests pass; BROAD-01 reference unchanged.

---

## VERIFICATION COMMANDS (run before declaring done)

```bash
# 0. One-time environment setup if needed
python3 -m pip install --quiet numpy pandas pyarrow

# 1. Heavy-work gate must return reason=OK (required=true once a post-start session exists)
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
that association. **Program status: ACTIVE — fidelity RESOLVED (bit-exact); reconciled NOT_STABLE
verdict produced; remaining work is to materialize the full BROAD_TS artifact set under a fresh
session and close out.**

(End of file)