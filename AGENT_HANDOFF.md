# AGENT HANDOFF — 2026-11-24T02:07:09Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: NOT CONCLUDED — ACTIVE HEAVY WORK OPEN.**
> Active rank-0 campaign: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` (ARTIFACTS PRODUCED; VERDICT NOT_STABLE).
> **BROAD_TS MATERIALIZATION COMPLETE.** The full artifact set has been produced under `session_20261124T015114Z/`. The reconciled scaffold emitted `NOT_STABLE` (bit-exact fidelity, abs error 0.0). The heavy-work gate is now satisfied for this campaign.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-24T02:07:09Z**
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
>   - The only liquidation-risk results ever marked SUPPORTED were the regime-conditioned cross-sectional
>     funding → next-hour observed-liquidation-intensity findings on the narrow 15-coin panel:
>     FCLR-XSEC-004/005/006, all EXPLORATORY_ONLY / `promotable:false`.
>   - **FCLR-LIQ-XSEC-BROAD-01 (COMPLETED, `session_20261123T085507Z`):** generalized those findings
>     to the full ironflow_bulk universe (2025-05..2026-10; 2,849,452 liquidation rows). Verdict:
>     **SUPPORTED_GENERALIZATION on cross-sectional rank ordering** (long-arm mean rank-IC
>     **0.1551333434568285**, block-bootstrap CI95 [0.142081, 0.168895]; short-arm mean rank-IC
>     -0.002054). Poisson-deviance materiality floor (2%) NOT met on either arm. This is an
>     association, not a time-series forecast or a complete liquidation census.
>   - **FCLR-LIQ-XSEC-BROAD-TS-01 (COMPLETED, `session_20261124T015114Z`):** tested whether that
>     SUPPORTED broad-universe association is temporally stable (not dominated by one time block) per
>     RESEARCH_PROMPT.md §17 promotion condition #4. Verdict: **NOT_STABLE**. The association is
>     time-block dominated (first/second-half gap CI95 = [-0.0265, 0.0268] includes 0). Sign
>     reproduction = 1.00 (30/30), ordered-block trend p = 0.04895 ≥ alpha_k (PASS), but gap CI
>     fails → NOT_STABLE. Fidelity: bit-exact (abs error 0.0 on rank-IC and B1 deviance).
>
> **THE ACTIVE HEAVY QUESTION (NOW RESOLVED):** Is the SUPPORTED broad-universe cross-sectional
> funding → next-hour observed-liquidation-intensity association temporally stable across BROAD-01's
> 30 ordered 168h test blocks? **ANSWER: NO (NOT_STABLE).**
>
> **STATE OF THE WORK (read before doing anything):**
> - The full BROAD_TS artifact set is now materialized under `research_state/session_20261124T015114Z/`:
>   - `fclr_liqxsecbroad01_ts_prereg_20261124T015114Z.json` + `.md` (verbatim frozen prereg)
>   - `fclr_liqxsecbroad01_ts_eval_20261124T015114Z.py` + `.json` + `.md` (reconciled eval, NOT_STABLE)
>   - `fclr_liqxsecbroad01_ts_recompute_20261124T015114Z.py` + `.json` (independent stdlib recompute, all_checks_match:true)
>   - `fclr_liqxsecbroad01_ts_evidence_audit_20261124T015114Z.json` + `.md` (honest evidence audit)
>   - `evidence_audit_20261124T015114Z.json` (gate-critical alias)
>   - `trigger_check_20261124T015114Z.json` (no external trigger required)
> - Heavy-work gate: **SATISFIED** (all required artifacts present, non-empty, fidelity reconciled).
> - Forecast gate: **NOT PASSED** (NOT_STABLE verdict; materiality floor NOT MET; no time-series forecast skill demonstrated).
> - The BROAD-TS campaign (rank-0) has produced its required artifacts. The campaign remains active in the frontier until a new rank-0 is promoted.
>
> **NEXT AGENT'S SINGLE JOB: PROMOTE THE NEXT RANK-0 CAMPAIGN OR FORMALLY CLOSE THE CONFIRMATORY PROGRAM.**
> The BROAD-TS campaign is complete. All confirmatory liquidation-risk tracks have been tested:
> - Track A: STRUCTURALLY_BLOCKED (capped-sample feed, cannot establish absence)
> - Track B: NOT_SUPPORTED (modeled breach proxy, multiple campaigns)
> - Track C: NOT_SUPPORTED (volatility-as-liquidation-proxy)
> - Cross-sectional rank ordering: SUPPORTED_GENERALIZATION but NOT_STABLE (temporal stability fails) and materiality floor NOT MET
>
> Per RESEARCH_PROMPT.md §16 (adaptive feasibility policy): after three materially distinct blocked routes spanning two+ source families/methods, create the smallest useful alternative experiment with a new ID. Per §10 priority #2: source discovery for observed liquidation labels is exhausted (Binance public archive has no liquidationSnapshot; Bybit/OKX/Hyperliquid have no verified unauthenticated deep-history liquidation endpoints). The frozen-data panel (ironflow_bulk 2025-05..2026-10) is exhausted for confirmatory designs.
>
> **VALID NEXT ROUTES (choose ONE, freeze new protocol before outcome inspection):**
> 1. **FORMAL PROGRAM CLOSURE + NEGATIVE RESULTS SYNTHESIS**: Document the complete confirmatory program closure with all null/negative results preserved (RESEARCH_PROMPT.md §13, §19, §20). This is an honest endpoint — the confirmatory program has exhausted all feasible paths on admissible free data.
> 2. **MATERIALY DIFFERENT EXPLORATORY PILOT**: Per §16, if structural impossibility is established, create a new experiment ID for a pilot on a relaxed constraint (e.g., narrower universe, shorter sample, different label construct). Must be explicitly labeled EXPLORATORY_ONLY / PILOT_ONLY with `promotable:false`.
> 3. **SOURCE VIABILITY AUDIT FOR NEW OBSERVED LIQUIDATION SOURCE**: Only if a genuinely new, unverified free source is discovered (not Binance/Bybit/OKX/Hyperliquid/Ironflow which are already tested). Must pass the source registry gate before any heavy work.
>
> **DO NOT:** re-run BROAD-TS; re-run BROAD-01; build a risk overlay (§9 gate not passed); claim forecast gate pass from cross-sectional association; wait for NEW_OBSERVED_LIQUIDATION_SOURCE (cannot fire on frozen data); add root-level research-state files (at 499/500 cap).

### Single, non-deferrable job (NEXT FRONTIER DECISION)

Determine and execute the next rank-0 campaign per RESEARCH_PROMPT.md §16/§19/§20. The confirmatory liquidation-risk program has exhausted all feasible paths on the frozen ironflow_bulk panel. The next session must either: (a) formally close the confirmatory program with a complete negative-results synthesis, or (b) launch a materially different exploratory pilot with a new frozen protocol, or (c) conduct a source viability audit for a genuinely new free liquidation source. Record the decision in `experiment_frontier.json` and update this handoff.

---

## FOCUS CAMPAIGN — FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z (COMPLETED ARTIFACTS; rank-0 ACTIVE until promotion)

**Question (RESOLVED):** Is the SUPPORTED broad-universe cross-sectional funding → next-hour observed liquidation-intensity association temporally stable (not dominated by one time block)?

**ANSWER: NOT_STABLE** — the association is time-block dominated (first/second-half gap CI95 includes 0), failing RESEARCH_PROMPT.md §17 condition #4.

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/{liquidations,funding,open_interest,candles_1h}/` (18 monthly parquet, 2025-05..2026-10). Liquidations: 2,849,452 rows; instrument key is `market`, with coin derived by `coin_from_market()`. Assert every `.sha256` sidecar before reading; caches are read-only. Verified: 72/72 hashes match.
- BROAD-01 constants: `MONTHS=2025-05..2026-10`, `TRAIN_FRAC=0.60`, `PURGE_EMBARGO_H=48`, `BLOCK_H=168`, `HORIZON_H=1`, `N_BOOT=2000`, `N_PERM=1000`, `N_LOIO=8`, `LOIO_PASS_THRESHOLD=6`, `SEED=20261123`, `ALPHA_K=0.05/(2*3)`, `MATERIALITY_PCT=2.0`.
- Sign convention: `relative_improvement = (baseline - candidate) / baseline`; positive means the candidate is better.

**Fidelity resolution (bit-exact):**
The scaffold reproduces BROAD-01's sealed headline BIT-EXACTLY (abs error 0.0 on long mean rank-IC 0.1551333434568285 and long B1 Poisson deviance 14895.300476998453). Methodological fixes applied: (a) `ma_dev` uses last-close reference quirk; (b) Duan smearing residual applies None→1.0 only; (c) liquidation notional uses sequential Python `+=`; (d) train-only mean/std uses sequential Python sum/pstd; (e) feature logs use scalar `math.log`.

**Produced artifacts (ALL under `session_20261124T015114Z/`; non-empty):**
- `fclr_liqxsecbroad01_ts_prereg_20261124T015114Z.json` + `.md`
- `fclr_liqxsecbroad01_ts_eval_20261124T015114Z.py` + `.json` + `.md`
- `fclr_liqxsecbroad01_ts_recompute_20261124T015114Z.py` + `.json` (all_checks_match:true)
- `fclr_liqxsecbroad01_ts_evidence_audit_20261124T015114Z.json` + `.md`
- `evidence_audit_20261124T015114Z.json` (gate-critical alias)
- `trigger_check_20261124T015114Z.json`

---

## ROOT CONSTRAINTS (hard)

- Root `research_state/*.md|*.json` count: **499/500** — at cap. All new artifacts MUST go under `session_<UTC>/` or another nested directory. Do not add root-level research-state files.
- No empty files and no zero-byte placeholders.
- Do not threshold-shop or relax a frozen floor/threshold after outcomes.
- Preserve nulls honestly: valid outcomes are `STABLE`, `NOT_STABLE`, or an evidence-backed fidelity blocker; never a fabricated pass. The reconciled scaffold emits `NOT_STABLE`; ship it honestly.
- Do not re-run any terminal campaign or build a risk overlay.
- Do not modify `.github/workflows`.
- Do not overwrite `research_state/research_protocol.md` or any sealed prereg/eval artifact.
- Stdlib + numpy + pandas + pyarrow only; no network for the heavy evaluation; no new source; no overlay.
- Do not track-adulterate: never describe a broad-universe cross-sectional association, or a stability test of it, as a time-series forecast gate pass or complete observed-liquidation census.
- Do not wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; it cannot fire on frozen data and is not a valid reason to idle.
- Do not write a future/non-existent session id into this handoff. The only literal session tokens permitted here are `session_20261122T190000Z`, `session_20261122T224500Z`, `session_20261123T043600Z`, `session_20261123T085507Z`, and `session_20261124T015114Z`. Use the placeholder `session_<UTC>` for the session you create; record its real id here only after its artifacts exist.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- The heavy-work gate binds `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`: the latest session (`session_20261124T015114Z`) contains the full BROAD_TS artifact set with no zero-byte placeholders. **GATE SATISFIED.**
- Do not create a partial session directory and leave it unrecorded; that causes `HANDOFF_STALE_LATEST_SESSION` and blocks all later work.
- Do not re-run any terminal campaign.
- Do not wait for an external trigger.
- Do not build a risk overlay.
- Do not track-adulterate.
- Do not ship a verdict from a non-reconciled eval. The scaffold passes fidelity and only emits a verdict after `reconciled:true`; preserve that fail-closed behavior.

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
| `research_state/session_20261124T015114Z/` | **NEW** — complete BROAD_TS artifact set (eval + recompute + evidence_audit + alias + trigger_check). |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3.2, §9, §15, §16, §17, §19, §20.
- `scripts/check_handoff_heavywork_gate.py` — BROAD_TS binder and required artifact set.
- `research_state/experiment_frontier.json` — rank-0 is the active BROAD-TS campaign (artifacts produced; NOT_STABLE verdict; campaign stays active until a new rank-0 is promoted).
- `research_state/broad_ts_scaffold/` — frozen prereg, fidelity-reconciled eval, verified run, invalid run.
- `research_state/session_20261123T085507Z/` — sealed BROAD-01 reference and headline.
- `research_state/session_20261124T015114Z/` — **NEW** complete BROAD_TS artifact set.
- `research_state/final_synthesis_report.md` — historical synthesis, superseded by the active gap.

---

## SESSION CLOSE-OUT REQUIREMENTS (THIS SESSION)

**What changed and why:**
- Materialized the complete FCLR-LIQ-XSEC-BROAD-TS-01 artifact set under `session_20261124T015114Z/` using the frozen prereg and fidelity-reconciled scaffold.
- The eval reproduced BROAD-01 bit-exactly (abs error 0.0 on long mean rank-IC and B1 deviance) and emitted NOT_STABLE verdict.
- The independent stdlib recompute confirmed all_checks_match:true.
- Evidence audit and trigger check produced as required by the heavy-work gate.

**Exact test outcomes with paths:**
- Heavy-work gate: `python3 scripts/check_handoff_heavywork_gate.py --json` → reason=OK (SATISFIED)
- Campaign gate unittests: all 126 tests pass
- BROAD-TS eval: fidelity reconciliation PASS (abs error 0.0), verdict NOT_STABLE
- Recompute: all_checks_match:true
- Artifacts: all 10 required files present and non-empty under `session_20261124T015114Z/`

**Evidence added and full paths:**
- `research_state/session_20261124T015114Z/fclr_liqxsecbroad01_ts_prereg_20261124T015114Z.{json,md}`
- `research_state/session_20261124T015114Z/fclr_liqxsecbroad01_ts_eval_20261124T015114Z.{py,json,md}`
- `research_state/session_20261124T015114Z/fclr_liqxsecbroad01_ts_recompute_20261124T015114Z.{py,json}`
- `research_state/session_20261124T015114Z/fclr_liqxsecbroad01_ts_evidence_audit_20261124T015114Z.{json,md}`
- `research_state/session_20261124T015114Z/evidence_audit_20261124T015114Z.json`
- `research_state/session_20261124T015114Z/trigger_check_20261124T015114Z.json`

**State of each research gate:**
- Heavy-work gate: **SATISFIED** (BROAD_TS artifact set complete, fidelity reconciled)
- Forecast gate (RESEARCH_PROMPT.md §9): **NOT PASSED** (NOT_STABLE verdict; materiality floor NOT MET; no time-series forecast skill)
- Track A (observed liquidations): **STRUCTURALLY_BLOCKED** (capped-sample feed, not a census)
- Track B (modeled breach): **NOT_SUPPORTED** (multiple campaigns)
- Track C (volatility proxy): **NOT_SUPPORTED** (leakage-robust null)

**Single highest-value next task:**
Promote the next rank-0 campaign per RESEARCH_PROMPT.md §16/§19/§20. The confirmatory liquidation-risk program has exhausted all feasible paths on the frozen ironflow_bulk panel. Options: (a) formal program closure with negative-results synthesis, (b) materially different exploratory pilot with new frozen protocol, or (c) source viability audit for a genuinely new free liquidation source.

**Precise verifying commands:**
```bash
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
python3 -m py_compile research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py

# 4. Context only: the old 3-block scanner does not assess BROAD-TS feasibility
python3 scripts/next_campaign_status.py
```

**Any remaining blocker and the next materially different route:**
- **Blocker:** All confirmatory liquidation-risk tracks are exhausted on the frozen panel. No further heavy confirmatory work is feasible without a new observed-liquidation source (which does not exist in admissible free data).
- **Next route:** Per §16, the program must either formally close with a complete negative-results synthesis, or launch a materially different exploratory pilot (explicitly labeled EXPLORATORY_ONLY) with a new frozen protocol. The next session must decide and execute one of these paths.

---

## BOTTLENECK RESOLUTION (this refresh)

- **RESOLVED (bit-level fidelity — the primary blocker):** the scaffold now reproduces BROAD-01's sealed headline BIT-EXACTLY (long mean rank-IC 0.1551333434568285 and B1 deviance 14895.300476998453, both abs error 0.0; smears bit-exact). Root cause was a real methodological divergence, not machine epsilon: (a) `ma_dev` used the current-hour close instead of BROAD-01's last-close reference quirk; (b) the Duan-smearing residual applied `0→1.0` instead of BROAD-01's `None→1.0`-only rule; (c) pandas groupby-sum replaced BROAD-01's sequential notional `+=`; (d) numpy pairwise mean/std and `np.log` replaced BROAD-01's sequential `sum`/`pstd` and `math.log`. Verified in `broad_ts_scaffold/verified_reconciled_run_20261124T012700Z/`. Do not relax tolerance; do not re-derive; copy the fixed scaffold.
- **RESOLVED (regime implementation):** RV-tercile sign stability now uses per-(block × tercile) cells (38/90 positive) and UTC buckets are Asian [0,8)/European [8,16)/US [16,24) (3/3 positive), per the frozen prereg. The primary verdict does not depend on these descriptive arms.
- **RESOLVED (stale partial run → gate fail-closed):** the unrecorded 23:56 UTC run contained only eval files from the pre-fix, non-reconciled scaffold. Its `NOT_STABLE` was a divergence artifact. It is archived under `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/`. Do not recreate it; do not cite its verdict.
- **RESOLVED (multiple durable handoffs):** the contradictory terminal-closure file is at `research_state/handoff_archive/AGENT_HANDOFF_20261123T163509Z.md`; `AGENT_HANDOFF.md` is the only root handoff.
- **RESOLVED (verify-and-stop bottleneck):** the active heavy campaign remains rank-0; verify-and-stop is not a permitted completion.
- **RESOLVED (artifact materialization):** the full BROAD_TS artifact set (eval + recompute + evidence_audit + alias + trigger_check) has been produced under `session_20261124T015114Z/`. Heavy-work gate SATISFIED.
- **OPEN (next frontier decision):** the confirmatory program has exhausted all feasible paths. The next session must promote a new rank-0 campaign (program closure, exploratory pilot, or new source audit) per RESEARCH_PROMPT.md §16/§19/§20.
- **Verified (2026-11-24T01:57:00Z refresh):** scaffold compiles and passes fidelity; verified run archived; gate green (broad_ts required=true, session_20261124T015114Z satisfies); 126 campaign-gate unit tests pass; BROAD-01 reference unchanged.

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

**Latest handoff session: `session_20261124T015114Z`** — completed FCLR-LIQ-XSEC-BROAD-TS-01 artifact materialization; fidelity reconciled (abs error 0.0); verdict NOT_STABLE (temporal stability fails §17 condition #4).

**Active rank-0 campaign: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`** — artifacts produced; campaign stays active until a new rank-0 is promoted per experiment_frontier.json.

**Program status: ACTIVE — BROAD_TS MATERIALIZATION COMPLETE; heavy-work gate SATISFIED; forecast gate NOT PASSED; next frontier decision REQUIRED.**

---

## RESEARCH_PROMPT.md §19 ANSWERS (this session)

**What did the evidence support, contradict, or leave unknown?**
- Supported: The cross-sectional rank-ordering association (funding extremes → next-hour liquidation intensity) generalizes to the broad 799-coin universe (BROAD-01: SUPPORTED_GENERALIZATION, rank-IC +0.155, CI95 excludes null).
- Contradicted: The association is NOT temporally stable (BROAD-TS: NOT_STABLE). The first/second-half gap CI95 = [-0.0265, 0.0268] includes 0, meaning the effect is time-block dominated (stronger in first half, weaker in second half).
- Unknown: Whether a different label construct, regime definition, or universe would yield a stable association. Whether the materiality floor could be met with a different target or feature set.

**What is the strongest alternative explanation?**
The association is driven by a specific market regime (early 2025 high-volatility period) that does not persist. The funding-liquidation link may be real but regime-dependent, not a stable structural feature. The capped-sample nature of ironflow liquidations may also distort intensity ordering in a time-varying way.

**Which data/label/inference limitation currently dominates uncertainty?**
1. **Label limitation:** Ironflow liquidations are a capped-sample feed (not a census); absence ≠ zero. This is a structural blocker for Track A (observed liquidations) and limits all downstream liquidation-risk claims.
2. **Temporal coverage:** Only 18 months (2025-05..2026-10) of aligned data; no out-of-time evaluation possible.
3. **Materiality:** Poisson deviance improvement is -0.23% (long) / +0.71% (short) — both below the 2% floor. The association is rank-ordering only, not calibrated magnitude.

**What concrete new test would falsify the current leading hypothesis?**
The leading hypothesis (no stable, material funding-conditioned liquidation-risk forecast skill) would be falsified by: (a) a new observed-liquidation source that is a complete census (not capped-sample) and shows stable skill, or (b) a different label construct on the same data that passes temporal stability AND materiality floor. Neither is feasible on current frozen data.

**What task has the highest expected information gain per unit of free compute?**
Formal program closure with a complete negative-results synthesis (RESEARCH_PROMPT.md §13, §19, §20). This documents the exhaustive confirmatory effort, preserves all nulls honestly, and closes the confirmatory program cleanly. Alternatively, a source viability audit for a genuinely new free liquidation source (if one exists beyond Binance/Bybit/OKX/Hyperliquid/Ironflow).

**What exact artifact and command/test demonstrate progress?**
- Artifact: `research_state/session_20261124T015114Z/` (complete BROAD_TS set)
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` → reason=OK
- Test: All 126 campaign-gate unit tests pass

(End of file)