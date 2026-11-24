# AGENT HANDOFF — 2026-11-24T02:52:46Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: CONFIRMATORY PROGRAM CONCLUDED — NEGATIVE RESULTS SYNTHESIS PENDING.**
> Active rank-0 campaign: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z` (COMPLETED, artifacts produced, verdict NOT_STABLE).
> **BROAD_TS MATERIALIZATION COMPLETE.** The full artifact set has been produced under `session_20261124T015114Z/`. The reconciled scaffold emitted `NOT_STABLE` (bit-exact fidelity, abs error 0.0). The heavy-work gate is now satisfied for this campaign.
> **REPO-NAME PRIORITY → `Funding-conditioned-volatility-and-liquidation-risk`**: Per RESEARCH_PROMPT.md §3.2, Half 1 (Volatility/Track C) is CLOSED — leakage-robust null across every claim-worthy panel (H1_primary NOT_SUPPORTED; FCLR-011 PASS does not generalize forward; FCLR-FWD-VOL-011-CONFIRM NOT_REPLICATED). Half 2 (Liquidation-risk) is the unfinished frontier: all confirmatory liquidation-risk tracks exhausted on the frozen ironflow_bulk panel.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-24T02:52:46Z**
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is `Funding-conditioned-volatility-and-liquidation-risk`. The liquidation-risk half (RESEARCH_PROMPT.md §3.2 half 2) is unfinished but all confirmatory paths are exhausted on the frozen panel. The next session's single, non-deferrable job is the **FORMAL PROGRAM CLOSURE + NEGATIVE RESULTS SYNTHESIS** campaign per RESEARCH_PROMPT.md §13, §19, §20.
>
> **THE NEXT FOCUS CAMPAIGN (rank-0, mandatory heavy work): `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01-20261124T025246Z`**
>
> Execute a formal confirmatory-program closure with a complete negative-results synthesis. This is HEAVY WORK — not a status memo, not a probe, not a trigger-check-only session. The confirmatory liquidation-risk program has exhausted all feasible paths on the frozen ironflow_bulk panel (2025-05..2026-10, 2,849,452 liquidation rows, 342 coins, 799 test markets):
> - **Track A (observed liquidations):** STRUCTURALLY_BLOCKED — ironflow_bulk is a capped-sample feed, not a complete census; cannot establish absence.
> - **Track B (modeled boundary breach):** NOT_SUPPORTED across all campaigns (FCLR-TRACKB-MODELED-BREACH-01, trackb_TB1, trackb_TB2).
> - **Track C (volatility/stress):** NOT_SUPPORTED across every claim-worthy panel (FCLR-001, 002, 003, 008, 009, 011, 012-V, 013, GATE4 v3).
> - **Cross-sectional rank ordering:** SUPPORTED_GENERALIZATION (BROAD-01, rank-IC +0.155, CI95 excludes null) but NOT_STABLE (BROAD-TS, temporal stability fails §17 condition #4) and Poisson-deviance materiality floor (2%) NOT MET on either arm.
> - **Shek 2026 replication (H002):** PARTIAL_REPLICATION, non-confirmatory (p=0.079, magnitudes differ).
>
> **Next agent's single job:** Produce the complete closure artifact set under a fresh `research_state/session_<UTC>/` (UTC strictly > 20261124T02:52:46Z), prefix `fclr_liq_risk_program_closure_`, all non-empty, no zero-byte placeholders:
> 1. `fclr_liq_risk_program_closure_protocol_freeze.{json,md}` — outcome-blind closure protocol freeze (hash-bound to RESEARCH_PROMPT.md §13/§19/§20), `outcome_data_inspected_before_freeze:false`, input sha256 assertions.
> 2. `fclr_liq_risk_program_closure_synthesis_report.{json,md}` — complete negative-results synthesis across all tracks/hypotheses/experiments with exact verdicts, CIs, artifact paths, and evidence.
> 3. `fclr_liq_risk_program_closure_frontier_exhaustion_audit.{json,md}` — audit proving no feasible confirmatory design remains on admissible frozen data (per RESEARCH_PROMPT.md §16 three-blocked-routes rule spanning two+ source families/methods).
> 4. `fclr_liq_risk_program_closure_negative_results_preservation.{json,md}` — all nulls/failed/inconclusive outcomes preserved with explanations, per RESEARCH_PROMPT.md §19.
> 5. `fclr_liq_risk_program_closure_meta_analysis.{py,json,md}` — quantitative meta-analysis triad (family-wide multiplicity, Holm-adjusted outcomes, per-track verdict table).
> 6. `fclr_liq_risk_program_closure_recompute.{py,json}` — independent stdlib recompute reproducing headline verdicts from stored input hashes/configuration (all_checks_match:true).
> 7. `evidence_audit_{UTC}.json` + `.md` — gate-critical evidence audit alias.
> 8. `trigger_check_{UTC}.json` — non-empty trigger check (no external trigger required; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data).
>
> Record the real session id in `experiment_frontier.json` (promote as rank-0, status READY_EXECUTE → COMPLETED_VALIDATED upon artifact completion) and update this handoff after artifacts exist. Do NOT write a future/non-existent session id into this handoff before artifacts exist.
>
> **DO NOT:** re-run BROAD-TS; re-run BROAD-01; build a risk overlay (§9 gate not passed); claim forecast gate pass from cross-sectional association; wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; add root-level research-state files (at 499/500 cap); relabel exploratory as confirmatory; threshold-shop after outcomes.

---

## FOCUS CAMPAIGN — FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z (COMPLETED ARTIFACTS; rank-0 RETIRED)

**Question (RESOLVED):** Is the SUPPORTED broad-universe cross-sectional funding → next-hour observed liquidation-intensity association temporally stable (not dominated by one time block)?

**ANSWER: NOT_STABLE** — the association is time-block dominated (first/second-half gap CI95 = [-0.0265, 0.0268] includes 0), failing RESEARCH_PROMPT.md §17 condition #4. Sign reproduction = 1.00 (30/30), ordered-block trend p = 0.04895 ≥ alpha_k (PASS), but gap CI fails → NOT_STABLE. Fidelity: bit-exact (abs error 0.0 on rank-IC and B1 deviance).

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/{liquidations,funding,open_interest,candles_1h}/` (18 monthly parquet, 2025-05..2026-10). Liquidations: 2,849,452 rows; instrument key is `market`, with coin derived by `coin_from_market()`. Assert every `.sha256` sidecar before reading; caches are read-only. Verified: 72/72 hashes match.
- BROAD-01 constants: `MONTHS=2025-05..2026-10`, `TRAIN_FRAC=0.60`, `PURGE_EMBARGO_H=48`, `BLOCK_H=168`, `HORIZON_H=1`, `N_BOOT=2000`, `N_PERM=1000`, `N_LOIO=8`, `LOIO_PASS_THRESHOLD=6`, `SEED=20261123`, `ALPHA_K=0.05/(2*3)`, `MATERIALITY_PCT=2.0`.
- Sign convention: `relative_improvement = (baseline - candidate) / baseline`; positive means the candidate is better.

**Fidelity resolution (bit-exact):**
The scaffold reproduces BROAD-01's sealed headline BIT-EXACTLY (long mean rank-IC 0.1551333434568285 and long B1 Poisson deviance 14895.300476998453, both abs error 0.0). Methodological fixes applied: (a) `ma_dev` uses last-close reference quirk; (b) Duan smearing residual applies None→1.0 only; (c) liquidation notional uses sequential Python `+=`; (d) train-only mean/std uses sequential Python sum/pstd; (e) feature logs use scalar `math.log`.

**Produced artifacts (ALL under `session_20261124T015114Z/`; non-empty):**
- `fclr_liqxsecbroad01_ts_prereg_20261124T015114Z.json` + `.md`
- `fclr_liqxsecbroad01_ts_eval_20261124T015114Z.py` + `.json` + `.md`
- `fclr_liqxsecbroad01_ts_recompute_20261124T015114Z.py` + `.json` (all_checks_match:true)
- `fclr_liqxsecbroad01_ts_evidence_audit_20261124T015114Z.json` + `.md`
- `evidence_audit_20261124T015114Z.json` (gate-critical alias)
- `trigger_check_20261124T015114Z.json`

---

## STATE OF THE WORK (read before doing anything)

- **BROAD-TS campaign (rank-0):** COMPLETE. Verdict NOT_STABLE. Heavy-work gate SATISFIED. Forecast gate NOT PASSED.
- **All confirmatory liquidation-risk tracks exhausted:** Track A STRUCTURALLY_BLOCKED; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; cross-sectional SUPPORTED_GENERALIZATION but NOT_STABLE + materiality floor NOT MET.
- **Heavy-work gate:** SATISFIED (all required BROAD_TS artifacts present, non-empty, fidelity reconciled).
- **Forecast gate (§9):** NOT PASSED — NOT_STABLE verdict; materiality floor NOT MET; no time-series forecast skill demonstrated. Risk overlay INELIGIBLE.
- **Root `research_state/*.md|*.json` count:** 499/500 — at cap. All new artifacts MUST go under `session_<UTC>/` or another nested directory.
- **Next frontier decision REQUIRED:** Per RESEARCH_PROMPT.md §16/§19/§20, the confirmatory program must either formally close with a complete negative-results synthesis, or launch a materially different exploratory pilot (EXPLORATORY_ONLY / promotable:false), or conduct a source viability audit for a genuinely new free liquidation source. The chosen route is **FORMAL PROGRAM CLOSURE + NEGATIVE RESULTS SYNTHESIS** (campaign `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01`).

---

## ROOT CONSTRAINTS (hard)

- Root `research_state/*.md|*.json` count: **499/500** — at cap. All new artifacts MUST go under `session_<UTC>/` or another nested directory. Do not add root-level research-state files.
- No empty files and no zero-byte placeholders.
- Do not threshold-shop or relax a frozen floor/threshold after outcomes.
- Preserve nulls honestly: valid outcomes are `STABLE`, `NOT_STABLE`, `NOT_SUPPORTED`, `STRUCTURALLY_BLOCKED`, or an evidence-backed fidelity blocker; never a fabricated pass.
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
- The closure campaign `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01` must emit ALL eight artifact categories listed above in the SAME session; a prereg-only or audit-only session fails closed.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. Capped-sample feed, not a census. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; funding and premium features. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; OI, mark, and oracle prices. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet; hourly close and instrument identity. |
| `research_state/broad_ts_scaffold/` | Frozen prereg, fidelity-reconciled eval, verified run, invalid run. |
| `research_state/session_20261123T085507Z/` | Sealed BROAD-01 reference and headline. |
| `research_state/session_20261124T015114Z/` | Complete BROAD_TS artifact set. |
| `research_state/experiment_frontier.json` | rank-0 is BROAD-TS (COMPLETED, NOT_STABLE); retire and promote closure campaign. |
| `research_state/final_synthesis_report.md` | Historical synthesis (2026-11-10), superseded by active closure campaign. |
| `research_state/negative_results_report.md` | Null/failed/inconclusive outcomes preserved (FCLR-001/002/003/009/014, Track B, Track C). |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3.2, §9, §13, §15, §16, §17, §19, §20.
- `scripts/check_handoff_heavywork_gate.py` — BROAD_TS binder and required artifact set.
- `research_state/experiment_frontier.json` — rank-0 campaign registry; retire BROAD-TS, promote closure campaign.
- `research_state/broad_ts_scaffold/` — frozen prereg, fidelity-reconciled eval, verified run.
- `research_state/session_20261123T085507Z/` — sealed BROAD-01 reference.
- `research_state/session_20261124T015114Z/` — complete BROAD_TS artifact set.
- `research_state/final_synthesis_report.md` — historical synthesis.
- `research_state/negative_results_report.md` — preserved nulls/negatives.

---

## SESSION CLOSE-OUT REQUIREMENTS (THIS SESSION)

**What changed and why:**
- Refreshed AGENT_HANDOFF.md as the sole durable handoff after BROAD-TS artifact materialization under `session_20261124T015114Z/`.
- BROAD-TS campaign complete: verdict NOT_STABLE, bit-exact fidelity (abs error 0.0), heavy-work gate SATISFIED.
- All confirmatory liquidation-risk tracks exhausted on frozen panel.
- Next focus campaign set: `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01-20261124T025246Z` — formal program closure + negative-results synthesis (mandatory heavy work, eight-artifact set).

**Exact test outcomes with paths:**
- Heavy-work gate: `python3 scripts/check_handoff_heavywork_gate.py --json` → reason=OK (SATISFIED)
- Campaign gate unittests: all 126 tests pass
- BROAD-TS eval: fidelity reconciliation PASS (abs error 0.0), verdict NOT_STABLE
- Recompute: all_checks_match:true

**State of each research gate:**
- Heavy-work gate: **SATISFIED** (BROAD_TS artifact set complete, fidelity reconciled)
- Forecast gate (§9): **NOT PASSED** (NOT_STABLE; materiality floor NOT MET; no forecast skill)
- Track A: **STRUCTURALLY_BLOCKED** (capped-sample feed, not a census)
- Track B: **NOT_SUPPORTED** (modeled breach, multiple campaigns)
- Track C: **NOT_SUPPORTED** (leakage-robust null across all panels)
- Cross-sectional rank ordering: **SUPPORTED_GENERALIZATION but NOT_STABLE, materiality floor NOT MET**

**Single highest-value next task:**
Execute `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01` — formal program closure + complete negative-results synthesis under a fresh `session_<UTC>/` with the eight mandatory artifact categories. This is the honest endpoint: the confirmatory program has exhausted all feasible paths on admissible frozen data.

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
python3 -m py_compile \
  research_state/broad_ts_scaffold/fclr_liqxsecbroad01_ts_eval_20261123T164423Z.py

# 4. Context only: the old 3-block scanner does not assess BROAD-TS feasibility
python3 scripts/next_campaign_status.py
```

**Any remaining blocker and the next materially different route:**
- **Blocker:** All confirmatory liquidation-risk tracks are exhausted on the frozen panel. No further heavy confirmatory work is feasible without a new observed-liquidation source (which does not exist in admissible free data).
- **Next route:** Formal program closure with complete negative-results synthesis (campaign `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01`). If the environment later changes (new admissible unauthenticated source with verifiable provenance and coverage), a new experiment may be pre-registered before examining outcomes.

---

## BOTTLENECK RESOLUTION (this refresh)

- **RESOLVED (bit-level fidelity):** scaffold reproduces BROAD-01 sealed headline BIT-EXACTLY (long mean rank-IC 0.1551333434568285 and B1 deviance 14895.300476998453, abs error 0.0). Do not relax tolerance; do not re-derive.
- **RESOLVED (stale partial run → gate fail-closed):** unrecorded 23:56 UTC run archived under `research_state/broad_ts_scaffold/invalid_run_20261123T235600Z/`. Do not recreate; do not cite its verdict.
- **RESOLVED (multiple durable handoffs):** contradictory terminal-closure file at `research_state/handoff_archive/AGENT_HANDOFF_20261123T163509Z.md`; `AGENT_HANDOFF.md` is the only root handoff.
- **RESOLVED (artifact materialization):** full BROAD_TS artifact set produced under `session_20261124T015114Z/`. Heavy-work gate SATISFIED.
- **RESOLVED (verify-and-stop bottleneck):** the active heavy campaign is rank-0 COMPLETE; verify-and-stop is not a permitted completion. The next agent must execute the closure campaign or formally justify a materially different route.
- **OPEN (next frontier decision):** closure campaign `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01` must be executed — eight mandatory artifacts under a fresh `session_<UTC>/`, no zero-byte placeholders, all in one session.

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

**Latest handoff session: `session_20261124T015114Z`** — completed FCLR-LIQ-XSEC-BROAD-TS-01 artifact materialization; fidelity reconciled (abs error 0.0); verdict NOT_STABLE (temporal stability fails §17 condition #4).

**Active rank-0 campaign: `FCLR-LIQ-XSEC-BROAD-TS-01-20261123T135825Z`** — COMPLETED, artifacts produced, NOT_STABLE verdict. Retire upon closure campaign promotion.

**Next focus campaign: `FCLR-LIQ-RISK-PROGRAM-CLOSURE-01-20261124T025246Z`** — formal program closure + negative-results synthesis; mandatory heavy work; eight-artifact set under fresh `session_<UTC>/`.

**Program status: CONFIRMATORY PROGRAM CONCLUDED — NEGATIVE RESULTS SYNTHESIS PENDING.** All confirmatory liquidation-risk tracks exhausted; forecast gate NOT PASSED; risk overlay INELIGIBLE; closure campaign REQUIRED.

---

## RESEARCH_PROMPT.md §19 ANSWERS (this session)

**What did the evidence support, contradict, or leave unknown?**
- Supported: The cross-sectional rank-ordering association (funding extremes → next-hour liquidation intensity) generalizes to the broad 799-coin universe (BROAD-01: SUPPORTED_GENERALIZATION, rank-IC +0.155, CI95 excludes null).
- Contradicted: The association is NOT temporally stable (BROAD-TS: NOT_STABLE). The first/second-half gap CI95 = [-0.0265, 0.0268] includes 0, meaning the effect is time-block dominated.
- Unknown: Whether a different label construct, regime definition, or universe would yield a stable association. Whether the materiality floor could be met with a different target or feature set.

**What is the strongest alternative explanation?**
The association is driven by a specific market regime (early 2025 high-volatility period) that does not persist. The funding-liquidation link may be real but regime-dependent, not a stable structural feature. The capped-sample nature of ironflow liquidations may also distort intensity ordering in a time-varying way.

**Which data/label/inference limitation currently dominates uncertainty?**
1. **Label limitation:** Ironflow liquidations are a capped-sample feed (not a census); absence ≠ zero. Structural blocker for Track A.
2. **Temporal coverage:** Only 18 months (2025-05..2026-10) of aligned data; no out-of-time evaluation possible.
3. **Materiality:** Poisson deviance improvement is -0.23% (long) / +0.71% (short) — both below the 2% floor. The association is rank-ordering only, not calibrated magnitude.

**What concrete new test would falsify the current leading hypothesis?**
The leading hypothesis (no stable, material funding-conditioned liquidation-risk forecast skill) would be falsified by: (a) a new observed-liquidation source that is a complete census and shows stable skill, or (b) a different label construct on the same data that passes temporal stability AND materiality floor. Neither is feasible on current frozen data.

**What task has the highest expected information gain per unit of free compute?**
Formal program closure with a complete negative-results synthesis (RESEARCH_PROMPT.md §13, §19, §20). This documents the exhaustive confirmatory effort, preserves all nulls honestly, and closes the confirmatory program cleanly.

**What exact artifact and command/test demonstrate progress?**
- Artifact: `research_state/session_20261124T015114Z/` (complete BROAD_TS set)
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` → reason=OK
- Test: All 126 campaign-gate unit tests pass

(End of file)