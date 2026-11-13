# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-13T01:20:00Z
**This file is the ONLY durable handoff.** It supersedes every earlier handoff version, checkpoint, and frontier entry. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are short redirects to this file.

**Update this file in place** (append a dated `## SESSION LOG` entry). Do **not** create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file.

**START HERE (next agent, execute in this exact order):**

`FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` — **Complete Arm A evaluation (Arm B is DONE).** The campaign `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` has two frozen preregs:
- **Arm B (P2 exploratory): `TRACKA-LIQ-XSEC-20261112T201536Z` — COMPLETED 2026-11-13T00:33:08Z** with verdict `EXPLORATORY_NULL` (mean IC=0.0145 < 0.05 materiality floor, spread sign 2/3 blocks). Artifacts exist: `evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.{md,json}`, panel, build report.
- **Arm A (P1 primary): `TRACKA-VOL-FULLHIST-20261112T201536Z` — PANEL BUILT 2026-11-12T23:49:33Z, EVALUATION PENDING.** Panel `tracka_vol_fullhist_panel_2026-11-12T23:49:33Z.parquet` exists. No evaluation artifact yet. The script `scripts/fclr_build_tracka_vol_fullhist.py` does panel build + evaluation in one run; it was started but timed out (heavy: 2000-rep bootstrap × 10 coins × 4 horizons × 5 models + LOIO/per-block/placebo/permutation). **Next session must complete Arm A evaluation and persist final state.**

1. **Gate 4 (bounded, no polling):** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → expect `NO_VALID_GATE4_TRIGGER` (verified 2026-11-13T01:15Z). Absent = proceed; do not wait. Gate 4 is not a blocker.
2. **Confirm Arm B done, Arm A panel exists, no Arm A evaluation artifact:**
   - `python3 -c "import json; p=json.load(open('research_state/prereg_tracka_vol_fullhist_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['outcome_data_inspected_before_freeze'])"`
   - `python3 -c "import json; p=json.load(open('research_state/prereg_tracka_liq_xsec_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['promotable'])"`
   - `ls research_state/evaluation_summary_TRACKA-VOL-FULLHIST-*.json 2>/dev/null || echo 'ARM_A_EVAL_MISSING'`
   - `ls research_state/evaluation_summary_TRACKA-LIQ-XSEC-*.json 2>/dev/null && echo 'ARM_B_EVAL_EXISTS'`
3. **Complete Arm A evaluation.** The panel is already built. Run the evaluation to completion:
   - `python3 scripts/fclr_build_tracka_vol_fullhist.py` (allow 20+ minutes; 2000-rep circular block bootstrap 168h, 10 coins, 4 horizons, 5 models, LOIO, per-block, placebo/permutation, 7 §17 checks)
   - If it fails/times out, debug and re-run. Do **not** re-fetch bulk cache (already OK for Arm A datasets).
4. **Adjudicate and persist (after Arm A eval artifact exists):**
   - Update `research_state/hypothesis_registry.json`: set `H_tracka_hl_funding_conditioned_volatility_fullhistory` to `terminal=true`, `terminal_class="NOT_MET"` (or actual verdict), `last_verdict="forecast_gate_NOT_MET"` (or actual), `experiment_id="TRACKA-VOL-FULLHIST-20261112T201536Z"`.
   - Update `research_state/experiment_frontier.json`: rank-0 campaign `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` → `status="COMPLETED"`, `program_status="COMPLETED"`.
   - Append the six §6 answers as a dated `## SESSION LOG` entry here.
   - Commit code/state/tests only. **Never** commit raw parquet/caches or patch `.github/workflows/*`.
5. **Verify:** `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → all OK.

**Do not stop at status-only output.** The session is done only when Arm A has a timestamped `{md,json}` evaluation artifact with exact failing minima or a clean pass, and the frontier/hypothesis registries are consistent (tests pass).

---

## 0. WHY THIS IS THE HIGHEST-PRIORITY WORK (inferred from the repository name)

`Funding-conditioned-volatility-and-liquidation-risk` →
- **P1 — funding-conditioned volatility forecasting** (primary, Arm A): prior verdicts (FCLR-014, TRACKA-VOL, TRACKA-ALT-VOL) all used a **single 6-month window** (2026-05..2026-10) because that was the only admissible mark-price cache. The frozen `ironflow/hyperliquid-candles-1h` bulk dataset makes **2025-06-01..2026-01-17 a never-opened holdout** with ~20,880 test rows across 10 coins — the first genuinely independent forward-block test of the repo's primary question.
- **P2 — observed liquidation risk** (co-primary, Arm B): sealed P2 designs are per-coin time-series on 8–9 hand-picked coins. The frozen cross-sectional arm scores the **full native-perp cross-section (~150–200 coins)** on a ranking estimand — a different universe and estimand that has never been evaluated. **COMPLETED: EXPLORATORY_NULL.**
- **P3 — modeled boundary breaches** (Track B): unchanged `H_trackb_modeled_breaches` NOT_SUPPORTED (TB2 1.68% < 2% floor; TB1 degenerate). Not reopened.

**A session is successful only if it produces a timestamped, machine-checkable evaluation artifact for Arm A (Arm B already done), plus consistent frontier/hypothesis state.** Status-only output, re-probing sealed designs, re-scoring the sealed 19.04% expansion result, reading the reserved/sealed windows, and handoff churn are banned.

---

## 1. VERIFIED STATE (as of 2026-11-13T01:20:00Z)

| Item | State |
|---|---|
| Gate 4 Branch 1 trigger | **ABSENT** (`NO_VALID_GATE4_TRIGGER`, re-verified 2026-11-13T01:15Z). Do not poll/wait. |
| Alternative liquidation-source discovery | **EXECUTED, NO ADMISSIBLE SOURCE** — `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` (22 candidates via `alt_source_scan_latest.json` @ 20261112T191347Z; 14 deep-review probes; live HF metadata probes). All NO-GO with exact failing minima. Do **not** repeat identical probes. |
| Robust `liq` campaign | **COMPLETE, NOT_MET.** `scripts/early4h_liq_glm_robust.py` (sha `33f917b2…`), eval `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` (sha `7f1f7edb…`), terminal stop `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` (sha `f5105524…`). Numerically stable (max row QLIKE 319 ≪ 1e6); gate fails. |
| Sealed panels/preregs | Panel `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` sha `08c60803…`; sealed `rv`/parent prereg `134503Z` sha `fdd96bd1…`; robust prereg sha `f06060c7…`. All sealed — do not alter. |
| `H_tracka_hl_symbol_expansion_liquidation_forecast` | **SUPPORTED_PASS_PRIMARY_GATE (19.04%)** but **NOT PROMOTABLE**: fails §17 conditions 4/5/7 — LOIO 4/8 < 6 required, placebo/permutation null (true 19.04% ≤ 95th pct 21.10%), instrument-concentration sensitive. Keep as exploratory; `H_tracka_hl_expansion_robustness` = FRAGILE. |
| Label ceiling (hard) | Ironflow observed liquidation labels **2025-05-25 .. 2026-10-31** only (9 target coins). No labels before 2025-05-25; no verified post-2026-10-31 extension. |
| **Frozen prereg — Arm A (P1)** | **`TRACKA-VOL-FULLHIST-20261112T201536Z`** — `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}`, frozen `2026-11-12T20:15:36Z`, `status=FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`. **Panel built 2026-11-12T23:49:33Z. NO evaluation artifact yet.** Never-opened holdout 2025-06-01..2026-01-17, 10 coins, 4 horizons, B1/C1/C2 + OI secondary family. **COMPLETE EVALUATION.** |
| **Frozen prereg — Arm B (P2)** | **`TRACKA-LIQ-XSEC-20261112T201536Z`** — `research_state/prereg_tracka_liq_xsec_20261112T201536Z.{json,md}`, frozen `2026-11-12T20:15:36Z`, `status=FROZEN_PRE_OUTCOMES`, `promotable=false` (max `EXPLORATORY_ONLY`). **COMPLETED 2026-11-13T00:33:08Z.** Verdict `EXPLORATORY_NULL` (mean IC=0.0145 < 0.05 floor, spread sign 2/3). Artifacts: `evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.{md,json}`, panel, build report. |
| Bulk data cache | `research_state/ironflow_bulk_manifest.json`: **Arm A datasets (candles_1h, funding, open_interest) 2025-05..2026-04 all OK (36/36).** Liquidations 2025-05..2025-10 OK (6/6); 2025-11..2026-04 ABSENT (6/6) — **not needed for Arm A.** Arm B used cached `ironflow_events/2025-05..2025-10` (18 files, 2,848,413 rows). No further fetch needed. |
| Frontier state | Rank-0 is `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` with `status=ACTIVE_HEAVY_CAMPAIGN`, `program_status=ACTIVE`. Must be updated to `COMPLETED`/`COMPLETED` after Arm A eval. |
| Dependencies/tests | `deps OK` (numpy,pandas,scipy,pyarrow,requests). `tests.test_active_campaign_gate` **FAILS** (2 failures): rank-0 status not COMPLETED; Arm A hypothesis not terminal. Other tests OK. **Must pass after Arm A completion.** |
| LFS pointer hazard | `run_manifest.json` is an unresolved Git LFS pointer in CI — do **not** read as JSON or depend on it. |
| Known unrelated test failures (do not chase) | `tests.test_tracka_hardening_099` drift-bound; CLI resume-gate test. |

---

## 2. BOTTLENECKS — REMOVED / REMAINING

| Bottleneck | Status / resolution |
|---|---|
| **False `CLOSED_TERMINAL` while two frozen preregs were unexecuted** | **REMOVED:** Frontier rank-0 now points to `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z`; premature closure entry demoted to `SUPERSEDED_TERMINAL`. |
| **"Do not fetch / do not run estimators" deadlock** | **REMOVED:** Arm B executed; Arm A panel built; bulk cache ready for Arm A. |
| **Bulk ironflow cache absent (48/48)** | **RESOLVED FOR ARM A:** 36/36 required objects OK. Liquidations 2025-11..2026-04 absent but not needed for Arm A. |
| **Arm A evaluation not complete** | **OPEN — ONLY REMAINING HEAVY WORK:** 2000-rep bootstrap + full inference suite. Run `scripts/fclr_build_tracka_vol_fullhist.py` to completion. |
| Repeated alternative-source discovery sessions with no new evidence angle | **Removed:** discovery executed once with timestamped probe audit; reopen requires a registry-keyed artifact. |
| Stale/competing next-task pointers (frontier duplicates, root redirect docs) | **Removed:** this file is sole authority; frontier normalized; redirect files unchanged. |
| `liq` estimator-form instability / re-diagnosis churn | **Removed:** root-caused and closed by robust eval + terminal structural stop. |
| HL 2025H1 observed-label exhaustion | **Structural (terminal for that design):** documented in terminal stop; Arm B changes estimand/universe and is explicitly exploratory. |
| Gate 4 external/legal evidence | **External blocker (unchanged):** absent valid `RESOLVED_VERIFIED` trigger; do not wait/poll. Not a blocker for Arm A/B. |
| Verifiably admissible new liquidation-label source | **Open, external reopen path:** requires §16 audit artifact; none exists now. |
| Program-level status coherence (registry vs frontier vs verdicts) | **Open — this session's deliverable:** after Arm A eval, update hypothesis registry + frontier to COMPLETED/terminal. |

---

## 3. VERIFIED EXPERIMENT / HYPOTHESIS LEDGER (from `research_state/hypothesis_registry.json`, updated 2026-11-13T01:20Z)

| ID | Status | Verdict | Notes |
|---|---|---|---|
| `H1_primary` | NOT_SUPPORTED | forecast_gate_NOT_MET | FCLR-014: C2 vs B1 rel QLIKE 1.14% < 2% floor, CI [−0.016361, 0.007728] crosses 0, 17d test window = 0 blocks. Also FCLR-003/008/012-V/013. |
| `H2_shek_replication` | EXPLORATORY_ONLY | PARTIAL | 88 events, 5 Binance perps, 2024Q1; high-RV median 16.0h vs 8.0h, log-rank p=0.0792; SSRN 403 blocks full replication. Never exact/confirmatory. |
| `H_trackb_modeled_breaches` | NOT_SUPPORTED | forecast_gate_NOT_MET | TB2 2024-01..09, 5 symbols, 619/5040 pos; gate 1.68% < 2% floor. Modeled, not observed. |
| `H_tracka_hl_liquidation_forecast` | NOT_MET | forecast_gate_NOT_MET | TRACKA-HL-S-20261111T133430Z, HL candleSnapshot 2026-05..10, 9 symbols, 1434 labeled buckets. |
| `H_tracka_hl_early_liquidation_forecast` | INCONCLUSIVE_PILOT_SHORTFALL | inconclusive_pilot_shortfall | 4h cadence, 2025-11..2026-04, 9 symbols; pilot shortfall, not a claim. |
| `H_tracka_hl_symbol_expansion_liquidation_forecast` | SUPPORTED_PASS_PRIMARY_GATE | forecast_gate_PASS | **Exploratory only:** LOIO 4/8, placebo null 21.10% ≥ 19.04%. Fails §17 promotion. |
| `H_tracka_hl_funding_conditioned_volatility_forecast` | NOT_MET | forecast_gate_NOT_MET | TRACKA-VOL-FAMILY-20261112T005111Z, 12-comparison Holm, no horizon passes. |
| `H_tracka_hl_expansion_robustness` | FRAGILE | robustness_gate_FRAGILE | LOIO 4/8, placebo/permutation fail, bootstrap 3/3 pass. |
| `H_tracka_hl_alt_volatility_forecast` | NOT_MET | forecast_gate_NOT_MET | TRACKA-ALT-VOL-20261112T020322Z, rel 5.77% pass but CI [−0.121, 0.034] crosses 0. |
| **`H_tracka_hl_funding_conditioned_volatility_fullhistory`** | **FROZEN_PRE_OUTCOMES** | **PENDING** | **Arm A — COMPLETE EVALUATION.** `TRACKA-VOL-FULLHIST-20261112T201536Z`, panel built 2026-11-12T23:49:33Z. Never-opened holdout 2025-06-01..2026-01-17, 10 coins, 4 horizons, 12-comparison Holm + 8-cell OI secondary family. |
| **`H_tracka_hl_liquidation_cross_sectional_funding`** | **FROZEN_PRE_OUTCOMES** | **EXPLORATORY_NULL** | **Arm B — COMPLETED 2026-11-13T00:33:08Z.** `TRACKA-LIQ-XSEC-20261112T201536Z`, full native-perp cross-section (158 coins), Spearman rank IC + 1000-rep permutation null. Mean IC=0.0145 < 0.05 floor. |

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z`

**Objective:** Complete Arm A evaluation and persist final consistent state (Arm B already done).

### Arm A — `TRACKA-VOL-FULLHIST-20261112T201536Z` (P1, primary) — **ONLY REMAINING WORK**
- Prereg: `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}` (frozen 2026-11-12T20:15:36Z).
- Panel: `research_state/tracka_vol_fullhist_panel_2026-11-12T23:49:33Z.parquet` (already built, 10 coins, train 2025-06-02..2025-09-30, 7d embargo, test blocks 0/1/2 = 2025-10-08..2026-01-17).
- Models: B1/C1/C2 (+ B2/C3 OI secondary family, never promotable).
- Inference: 12-comparison Holm primary family (4 horizons × 3 contrasts); 8-cell OI secondary family (separate Holm); 2000-rep circular block bootstrap (168h block, seed 20261112); LOIO/per-coin/per-block; placebo/permutation (500 reps); all seven §17 promotion checks.
- **Emit:** `research_state/evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.{md,json}` + panel build report.
- **Verdict** expected: `NOT_MET` / `INCONCLUSIVE` / `FORECAST_GATE_PASSED`; preserve null and exact failing minima if it fails.

### Arm B — `TRACKA-LIQ-XSEC-20261112T201536Z` (P2, exploratory, max `EXPLORATORY_ONLY`) — **DONE**
- Verdict: `EXPLORATORY_NULL` (mean IC=0.0145 < 0.05 materiality floor, spread sign 2/3 blocks).
- Artifacts exist: `evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.{md,json}`, panel, build report.
- Do **not** promote or re-label.

### Acceptance gate (Arm A completion)
1. Arm A evaluation artifact `evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.{md,json}` exists with exact failing minima or clean pass.
2. `experiment_frontier.json` rank-0 updated to `status="COMPLETED"`, `program_status="COMPLETED"`.
3. `hypothesis_registry.json`: `H_tracka_hl_funding_conditioned_volatility_fullhistory` → `terminal=true`, `terminal_class` set, `last_verdict` set, `experiment_id` set.
4. `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → all OK.
5. No reserved/sealed window read; no Binance/2024 substitution; no `.github/workflows/*` edits; no raw parquet/cache commits.

---

## 5. EXACT START COMMANDS

```bash
cd <repo>
# 1) Preflight (bounded)
python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"

# 2) Gate 4 trigger check (real RESOLVED file only, never matrix text)
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"

# 3) Confirm Arm B done, Arm A panel exists, no Arm A evaluation artifact
python3 -c "import json; p=json.load(open('research_state/prereg_tracka_vol_fullhist_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['outcome_data_inspected_before_freeze'])"
python3 -c "import json; p=json.load(open('research_state/prereg_tracka_liq_xsec_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['promotable'])"
ls research_state/evaluation_summary_TRACKA-VOL-FULLHIST-*.json 2>/dev/null || echo 'ARM_A_EVAL_MISSING'
ls research_state/evaluation_summary_TRACKA-LIQ-XSEC-*.json 2>/dev/null && echo 'ARM_B_EVAL_EXISTS'

# 4) Complete Arm A evaluation (allow 20+ minutes; heavy bootstrap + inference)
python3 scripts/fclr_build_tracka_vol_fullhist.py

# 5) After Arm A eval artifact exists, update registries and verify
# (Manual steps: edit hypothesis_registry.json, experiment_frontier.json, append SESSION LOG)
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit
```

Expected end-of-session artifacts: `research_state/evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.{md,json}`, `research_state/tracka_vol_fullhist_panel_build_report_<UTC>.json`, updated `hypothesis_registry.json` (Arm A terminal), updated `experiment_frontier.json` (COMPLETED), and a `## SESSION LOG` entry here.

---

## 6. SESSION DEFINITION OF DONE (answer in the handoff)

- What did the evidence support, contradict, or leave unknown?
- Strongest alternative explanation?
- Which data/label/inference limitation dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- Exact artifact and command/test demonstrating progress.

---

## 7. HARD BANS (no exceptions)

- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation with Hyperliquid windows; no venue mixing in one panel.
- No modeled/proxy/synthetic liquidation labels presented as observed.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass; no whole-tree grep for the trigger string.
- No reopening/relitigating/retuning sealed verdicts (Track B/C, FCLR-*, expansion/volatility campaigns, H2, early4h `rv`, early4h `liq` parent/robust).
- No estimator iteration on the sealed 2025H1 `liq` panel/splits/labels (terminal stop in force).
- No re-probing 1h candles to conclude "no early data" — use `4h`.
- No repeated alternative-source discovery without a new source family/file/verified label extension (see trigger `NEW_OBSERVED_LIQUIDATION_SOURCE`).
- No polling/waiting; no status-only sessions; no redundant controllers, schedulers, wrappers, or polling loops.
- **Authorized heavy work (not banned):** Arm A evaluation (2000-rep bootstrap + full inference) on the already-built panel. Does not touch sealed panels, reserved/sealed windows, or liquidation labels.
- No successor handoff or second campaign doc. Update this file.
- No raw data/cache commits; no `.github/workflows/*` patches.

---

## 8. KEY REFERENCES

- `RESEARCH_PROMPT.md` — §5 (source acceptance), §16 (adaptive feasibility), §17 (multiplicity/promotion), §18 (integrity), §19 (session DoD), §20 (status contract).
- `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}` — **Arm A (P1), frozen, panel built, evaluation pending.**
- `research_state/prereg_tracka_liq_xsec_20261112T201536Z.{json,md}` — **Arm B (P2 exploratory), frozen, COMPLETED (EXPLORATORY_NULL).**
- `scripts/fclr_build_tracka_vol_fullhist.py` — builds panel + runs full evaluation (run to completion).
- `research_state/evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.{md,json}` — Arm B completed artifact.
- `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` — Track A HL 2025H1 observed-label `liq` closed (do not relitigate).
- `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` — all alternative source families NO-GO with exact failing minima.
- `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` — state to update to COMPLETED/terminal after Arm A.
- `research_state/structural_closure_verdict_heavy.md` (2026-10-31) — earlier Track A/B/C closure; historical evidence only.

---

## 9. SESSION LOG (append-only; newest first)

<!-- Format: ## <UTC> — <agent/session id> — <one-line outcome> ... -->

## 2026-11-13T01:20:00Z — Session state captured: Arm B (LIQ-XSEC) COMPLETED EXPLORATORY_NULL; Arm A (VOL-FULLHIST) panel built, evaluation PENDING; bulk cache ready for Arm A; tests fail on incomplete state; next session must complete Arm A eval and persist COMPLETED

- **Evidence supported/contradicted/unknown:** Supported — Arm B evaluation artifact exists (`evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.{md,json}`) with verdict EXPLORATORY_NULL (mean IC=0.0145 < 0.05 floor, spread sign 2/3, permutation p=0.094). Arm A panel built 2026-11-12T23:49:33Z (10 coins, 2025-06-02..2026-01-17 holdout). Bulk cache: 36/36 Arm A objects OK (candles_1h, funding, open_interest 2025-05..2026-04). Gate 4 trigger ABSENT. Contradicted — test `test_active_campaign_gate` fails (2 failures): rank-0 campaign status is ACTIVE_HEAVY_CAMPAIGN not COMPLETED; Arm A hypothesis not terminal. Unknown — Arm A evaluation outcome (NOT_MET/INCONCLUSIVE/FORECAST_GATE_PASSED); exact failing minima.
- **Strongest alternative explanation:** The funding-conditioned volatility signal on the never-opened 2025-06..2026-01 holdout is either absent or too weak to clear the 2% materiality floor + Holm correction across 12 comparisons + bootstrap CI, consistent with all prior volatility campaigns (FCLR-014, TRACKA-VOL, TRACKA-ALT-VOL, TRACKA-VOL-FAMILY) which were NOT_MET.
- **Dominant limitation:** The 11-month holdout (2025-06-01..2026-01-17) is the first genuinely independent forward-block test for P1, but prior campaigns on different windows all failed. If Arm A also fails, the cumulative evidence across multiple independent windows strongly suggests no detectable funding-conditioned volatility forecast skill with admissible unauthenticated data under frozen protocols.
- **Falsifying next test:** Arm A evaluation clearing all gates (primary 24h QLIKE rel reduction ≥2%, Holm across 12 comparisons PASS, bootstrap CI excludes zero, ≥5 instruments, ≥3 blocks, LOIO ≥6/10, placebo/permutation PASS). If Arm A passes, it would be the first confirmatory P1 result.
- **Highest expected info gain per free compute:** Complete Arm A evaluation (2000-rep bootstrap + full inference on existing panel) and persist COMPLETED state. This is the last unexecuted frozen prereg; after this, all claim-worthy local admissible experiments are exhausted.
- **Artifacts/commands:** `ls research_state/evaluation_summary_TRACKA-LIQ-XSEC-*.json` → exists; `ls research_state/evaluation_summary_TRACKA-VOL-FULLHIST-*.json` → ARM_A_EVAL_MISSING; `python3 scripts/fclr_build_tracka_vol_fullhist.py` (started, heavy, allow 20+ min); `python -m unittest tests.test_active_campaign_gate` → 2 failures (rank-0 status, Arm A hypothesis not terminal). No sealed verdicts modified; no raw data committed; no workflow changes.

---

## 2026-11-12T22:40:00Z — Handoff rebuilt as single durable campaign for FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z; two frozen preregs identified as unexecuted; false CLOSED_TERMINAL demoted

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`NO_VALID_GATE4_TRIGGER`); deps importable; 111 tests OK (43.4s); alternative-source discovery already executed at 2026-11-12T19:14:00Z with complete probe audit finding **no** admissible source; all P1/P2/P3 experiments sealed (see §3). Frontier was stale: 8 entries, all `rank=0`/`ACTIVE_HEAVY_CAMPAIGN`, including duplicate and already-executed tasks. Contradicted — no valid Gate 4 trigger and no new admissible source. Unknown — whether any future external source or Gate 4 trigger can reopen a claim-worthy test.
- **Strongest alternative explanation:** The funding-conditioned signal for volatility/liquidation forecasting is either absent or too weak to detect with admissible unauthenticated data under frozen pre-registered protocols; the single symbol-expansion PASS (19.04%) is instrument-concentration-sensitive (LOIO 4/8) and indistinguishable from placebo (21.10%), so it fails §17 promotion.
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and ceiling on incremental forecast skill vs RV-only baseline (Tracks B/C) dominate; all local admissible panels consumed; no reopen path without new admissible source or valid Gate 4 trigger.
- **Falsifying next test:** A new admissible unauthenticated observed-liquidation source passing §16 audit (≥5 instruments, ≥3×30d blocks or ≥1 complete month, provenance/license, observed labels, venue-consistent) followed by a frozen prereg and out-of-sample evaluation; or a valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`, `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Neither exists now.
- **Highest expected info gain per free compute:** `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` — execute the two frozen preregs that the premature closure ignored. Arm A: never-opened 11-month holdout for P1. Arm B: full native-perp cross-section for P2 (exploratory).
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` → `deps OK`; `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 111 tests in 43.371s / OK` (at that time). No sealed verdicts modified; no raw data committed; no workflow changes.

---

## 2026-11-12T21:22:35Z — FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS executed; program closed CLOSED_TERMINAL; stale frontier bottleneck removed; machine-checkable reopen registry live

- **Evidence supported/contradicted/unknown:** Supported — structural closure artifact `research_state/fclr_final_structural_closure_20261112T212043.{md,json}` emitted with per-ID rows, `reopen_conditions`, input hashes. `resume_trigger_registry.json` created with 4 triggers. Frontier normalized to one terminal rank-0 + 8 superseded entries. Hypothesis registry updated with `terminal`/`terminal_class`/`reopen_requires`. Contradicted — the closure ignored two frozen preregs (`prereg_tracka_vol_fullhist_20261112T201536Z`, `prereg_tracka_liq_xsec_20261112T201536Z`) that were frozen pre-outcomes with no evaluation artifacts. This contradiction was identified and fixed in the 22:40Z handoff update. Unknown — whether any future trigger will satisfy the reopen registry.
- **Strongest alternative explanation:** Funding-conditioned signal for volatility/liquidation is absent or undetectable with admissible unauthenticated data under frozen preregistrations; symbol-expansion PASS (19.04%) fails §17 promotion (LOIO 4/8, placebo 21.10% ≥ true).
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and forecast-skill ceiling vs RV-only baseline (Tracks B/C); all local admissible panels consumed. The premature closure was a process error, not an evidence conclusion.
- **Falsifying next test:** (1) Valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation); (2) new unauthenticated observed-liquidation source passing §16 audit; (3) verified HL/ironflow labels after 2026-10-31 with ≥100d depth; (4) newly preregistered expansion robustness meeting LOIO≥6 and placebo/permutation criteria. None exist now.
- **Highest expected info gain per free compute:** The 22:40Z handoff correctly identified the two unexecuted frozen preregs as the next heavy campaign (`FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z`), superseding the premature closure.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print 'deps OK'"` → `deps OK`; read `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/alt_source_probe_audit_20261112T191400Z.md`. No sealed verdicts modified; no raw data committed; no workflow changes.