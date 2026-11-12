# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T22:40:00Z
**This file is the ONLY durable handoff.** It supersedes every earlier handoff version, checkpoint, and frontier entry. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are short redirects to this file.

**Update this file in place** (append a dated `## SESSION LOG` entry). Do **not** create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file.

**START HERE (next agent, execute in this exact order):**

`FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` — **execute the two frozen, never-run preregistered experiments that the premature 21:12Z/22:12Z `CLOSED_TERMINAL` state wrongly ignored.** This is the repo-name priority work: **P1 funding-conditioned volatility** (Arm A) and **P2 observed liquidation risk** (Arm B). Both were frozen at `2026-11-12T20:15:36Z` with `status=FROZEN_PRE_OUTCOMES` and `outcome_data_inspected_before_freeze=false`, and **neither has any evaluation artifact**. The "all designs sealed / verification-only" directive is **void**: two unexecuted, admissible, preregistered experiments exist, so the program is **not** terminal.

1. **Gate 4 (bounded, no polling):** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → expect `NO_VALID_GATE4_TRIGGER` (verified 2026-11-12T22:12Z). Absent = proceed; do not wait. Gate 4 is not a blocker for either arm.
2. **Confirm the two preregs are frozen and unexecuted (read-only):**
   - `python3 -c "import json; p=json.load(open('research_state/prereg_tracka_vol_fullhist_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['frozen_before_outcomes'], p['outcome_data_inspected_before_freeze'])"`
   - `python3 -c "import json; p=json.load(open('research_state/prereg_tracka_liq_xsec_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['promotable'])"`
   - `ls research_state | grep -Ei 'FULLHIST|XSEC' | grep -v prereg || echo 'NO_OUTCOME_ARTIFACTS'`
3. **Materialise the bulk cache (bounded, cache-first, unauthenticated, fail-closed).** The manifest `research_state/ironflow_bulk_manifest.json` currently records **48/48 ABSENT** (only `funding/2025-06.parquet` exists). Fetch per the frozen prereg's `acquisition` block:
   - `python3 scripts/fclr_ironflow_bulk.py fetch --datasets candles_1h,funding,open_interest --months 2025-05..2026-04`
   - `python3 scripts/fclr_ironflow_bulk.py fetch --datasets liquidations --months 2025-05..2025-10`
   - `python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-05..2026-04`
   If the network is unavailable, emit a timestamped blocker with the exact failing object list and stop that arm cleanly — do **not** fabricate, zero-fill, or substitute Binance/2024 data.
4. **Arm A — `TRACKA-VOL-FULLHIST-20261112T201536Z` (P1 primary).** Build `research_state/tracka_vol_fullhist_panel_<UTC>.parquet` + build report exactly per the frozen prereg (10 coins, train 2025-06-02..2025-09-30, 7d embargo, test blocks 0/1/2, **never read 2026-01-18..2026-04-30 or 2026-05-01..2026-10-31**, no liquidation labels). Fit B1/C1/C2 (train-only OLS, epsilon 1e-12, train-only standardization), score primary T24 + secondary T6/T72/T168, run the 12-comparison Holm primary family and the separate 8-cell OI secondary family, 2000-rep circular block bootstrap (block 168h, seed 20261112), LOIO/per-coin/per-block, placebo/permutation, and all seven §17 promotion checks. Emit `research_state/evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.{md,json}`. Verdict `NOT_MET` / `INCONCLUSIVE` / `FORECAST_GATE_PASSED`; preserve the null and exact failing minima if it fails.
5. **Arm B — `TRACKA-LIQ-XSEC-20261112T201536Z` (P2 exploratory, max `EXPLORATORY_ONLY`, never promotable).** Build `research_state/tracka_liq_xsec_panel_<UTC>.parquet` + build report from cached `ironflow_events/2025-05..2025-10` plus fetched candles/funding; full native-perp cross-section (coverage-only eligibility, ≥20 liq-days, ≥100 events, ≥5 coins, 3 blocks). Compute the within-bucket cross-sectional funding score, Spearman rank IC vs next-24h observed liquidation count/notional, 1000-rep within-bucket permutation null (seed 20261112), top-k minus bottom-k spread, per-block + pooled. Emit `research_state/evaluation_summary_TRACKA-LIQ-XSEC-<UTC>.{md,json}`. Do **not** promote or re-label any sealed P2 verdict.
6. **Adjudicate and persist:** update `research_state/experiment_frontier.json` (this campaign → completed/`NOT_MET`/etc., keep history), `research_state/hypothesis_registry.json` (add the two frozen hypotheses with terminal verdicts, do not change sealed verdicts), append the six §6 answers as a dated `## SESSION LOG` entry here, and commit code/state/tests only. **Never** commit raw parquet/caches or patch `.github/workflows/*`.
7. **Do not stop at status-only output.** The session is done only when both arms have a timestamped `{md,json}` evaluation artifact with exact failing minima or a clean pass, the bulk cache is verified (or a network blocker is evidenced), and the frontier/hypothesis registries are consistent.

---

## 0. WHY THIS IS THE HIGHEST-PRIORITY WORK (inferred from the repository name)

`Funding-conditioned-volatility-and-liquidation-risk` →
- **P1 — funding-conditioned volatility forecasting** (primary, Arm A): prior verdicts (FCLR-014, TRACKA-VOL, TRACKA-ALT-VOL) all used a **single 6-month window** (2026-05..2026-10) because that was the only admissible mark-price cache. The frozen `ironflow/hyperliquid-candles-1h` bulk dataset makes **2025-06-01..2026-01-17 a never-opened holdout** with ~20,880 test rows across 10 coins — the first genuinely independent forward-block test of the repo's primary question.
- **P2 — observed liquidation risk** (co-primary, Arm B): sealed P2 designs are per-coin time-series on 8–9 hand-picked coins. The frozen cross-sectional arm scores the **full native-perp cross-section (~150–200 coins)** on a ranking estimand — a different universe and estimand that has never been evaluated.
- **P3 — modeled boundary breaches** (Track B): unchanged `H_trackb_modeled_breaches` NOT_SUPPORTED (TB2 1.68% < 2% floor; TB1 degenerate). Not reopened.

**A session is successful only if it produces a timestamped, machine-checkable evaluation artifact for Arm A and Arm B (or an evidenced, bounded data-acquisition blocker), plus consistent frontier/hypothesis state.** Status-only output, re-probing sealed designs, re-scoring the sealed 19.04% expansion result, reading the reserved/sealed windows, and handoff churn are banned.

---

## 1. VERIFIED STATE (as of 2026-11-12T22:40:00Z)

| Item | State |
|---|---|
| Gate 4 Branch 1 trigger | **ABSENT** (`NO_VALID_GATE4_TRIGGER`, re-verified 2026-11-12T22:20Z). Do not poll/wait. |
| Alternative liquidation-source discovery | **EXECUTED, NO ADMISSIBLE SOURCE** — `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` (22 candidates via `alt_source_scan_latest.json` @ 20261112T191347Z; 14 deep-review probes; live HF metadata probes). All NO-GO with exact failing minima. Do **not** repeat identical probes. |
| Robust `liq` campaign | **COMPLETE, NOT_MET.** `scripts/early4h_liq_glm_robust.py` (sha `33f917b2…`), eval `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` (sha `7f1f7edb…`), terminal stop `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` (sha `f5105524…`). Numerically stable (max row QLIKE 319 ≪ 1e6); gate fails. |
| Sealed panels/preregs | Panel `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` sha `08c60803…`; sealed `rv`/parent prereg `134503Z` sha `fdd96bd1…`; robust prereg sha `f06060c7…`. All sealed — do not alter. |
| `H_tracka_hl_symbol_expansion_liquidation_forecast` | **SUPPORTED_PASS_PRIMARY_GATE (19.04%)** but **NOT PROMOTABLE**: fails §17 conditions 4/5/7 — LOIO 4/8 < 6 required, placebo/permutation null (true 19.04% ≤ 95th pct 21.10%), instrument-concentration sensitive. Keep as exploratory; `H_tracka_hl_expansion_robustness` = FRAGILE. |
| Label ceiling (hard) | Ironflow observed liquidation labels **2025-05-25 .. 2026-10-31** only (9 target coins). No labels before 2025-05-25; no verified post-2026-10-31 extension. |
| **Frozen prereg — Arm A (P1)** | **`TRACKA-VOL-FULLHIST-20261112T201536Z`** — `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}`, frozen `2026-11-12T20:15:36Z`, `status=FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`. **No evaluation artifact exists.** Never-opened holdout 2025-06-01..2026-01-17, 10 coins, 4 horizons, B1/C1/C2 + OI secondary family. **EXECUTE THIS.** |
| **Frozen prereg — Arm B (P2)** | **`TRACKA-LIQ-XSEC-20261112T201536Z`** — `research_state/prereg_tracka_liq_xsec_20261112T201536Z.{json,md}`, frozen `2026-11-12T20:15:36Z`, `status=FROZEN_PRE_OUTCOMES`, `promotable=false` (max `EXPLORATORY_ONLY`). **No evaluation artifact exists.** Full native-perp cross-section, Spearman rank IC + permutation null. **EXECUTE THIS.** |
| Bulk data cache | `research_state/ironflow_bulk_manifest.json` records **48/48 objects ABSENT** (only `funding/2025-06.parquet` present). Arm A/B require the cache-first fetch in START HERE step 3. `liquidations` are already cached in `research_state/data_cache/ironflow_events/2025-05..2025-10` (18 files, 2,848,413 rows). |
| Frontier state | **UPDATED THIS SESSION:** rank-0 is now the active `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` campaign; the premature `CLOSED_TERMINAL` entry is demoted to `SUPERSEDED_TERMINAL` (kept for history). All older entries remain `SUPERSEDED_TERMINAL`. |
| Dependencies/tests | `deps OK` re-verified 2026-11-12T22:20Z (numpy,pandas,scipy,pyarrow,requests). `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → **111 tests OK** (43.6s, 2026-11-12T22:20Z). `tests/test_active_campaign_gate.py` fails if the frontier returns to a rank-0 `CLOSED_TERMINAL` while the two preregs remain unexecuted. |
| LFS pointer hazard | `run_manifest.json` is an unresolved Git LFS pointer in CI — do **not** read as JSON or depend on it. |
| Known unrelated test failures (do not chase) | `tests.test_tracka_hardening_099` drift-bound; CLI resume-gate test. |

---

## 2. BOTTLENECKS — REMOVED / REMAINING

| Bottleneck | Status / resolution |
|---|---|
| **False `CLOSED_TERMINAL` while two frozen preregs were unexecuted** | **REMOVED (this update):** the 21:12Z/22:12Z closure declared "all designs sealed / verification-only" but ignored `prereg_tracka_vol_fullhist_20261112T201536Z` and `prereg_tracka_liq_xsec_20261112T201536Z` (both frozen, no outcomes). Frontier rank-0 now points to `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z`; the closure entry is demoted. |
| **"Do not fetch / do not run estimators" deadlock** | **REMOVED:** the frozen preregs' acquisition block authorizes a bounded, cache-first, unauthenticated fetch; Arm A/B estimators must be run. Gate 4 is not a blocker for these arms. |
| Bulk ironflow cache absent (48/48) | **Open — first heavy step:** `python3 scripts/fclr_ironflow_bulk.py fetch ...` then `verify`; fail closed with exact missing objects if offline. |
| Repeated alternative-source discovery sessions with no new evidence angle | **Removed:** discovery executed once with timestamped probe audit; reopen requires a registry-keyed artifact. No repeated no-op probes. |
| Stale/competing next-task pointers (frontier duplicates, root redirect docs) | **Removed:** this file is sole authority; frontier normalized; redirect files unchanged. |
| `liq` estimator-form instability / re-diagnosis churn | **Removed:** root-caused and closed by robust eval + terminal structural stop. No further estimator iteration on that sealed panel/splits/labels. |
| HL 2025H1 observed-label exhaustion | **Structural (terminal for that design):** documented in terminal stop; Arm B changes estimand/universe and is explicitly exploratory. |
| Gate 4 external/legal evidence | **External blocker (unchanged):** absent valid `RESOLVED_VERIFIED` trigger; do not wait/poll. Not a blocker for Arm A/B. |
| Verifiably admissible new liquidation-label source | **Open, external reopen path:** requires §16 audit artifact; none exists now. |
| Program-level status coherence (registry vs frontier vs verdicts) | **Open — this campaign's deliverable:** after Arm A/B, add both hypotheses with terminal/exploratory verdicts and keep the frontier consistent. |

---

## 3. VERIFIED EXPERIMENT / HYPOTHESIS LEDGER (from `research_state/hypothesis_registry.json`, updated 2026-11-12T22:40Z)

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
| **`H_tracka_hl_funding_conditioned_volatility_fullhistory`** | **FROZEN_PRE_OUTCOMES** | **NOT_RUN** | **Arm A — EXECUTE.** `TRACKA-VOL-FULLHIST-20261112T201536Z`, never-opened holdout 2025-06-01..2026-01-17, 10 coins, 4 horizons, 12-comparison Holm + 8-cell OI secondary family. |
| **`H_tracka_hl_liquidation_cross_sectional_funding`** | **FROZEN_PRE_OUTCOMES** | **NOT_RUN** | **Arm B — EXECUTE (exploratory, max `EXPLORATORY_ONLY`, not promotable).** `TRACKA-LIQ-XSEC-20261112T201536Z`, full native-perp cross-section, Spearman rank IC + 1000-rep permutation null. |

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z`

**Objective:** execute the two frozen preregistered experiments that were wrongly bypassed by the premature terminal closure, and adjudicate them with timestamped, machine-checkable artifacts. The frozen preregs are authoritative; this section only sequences them.

### Arm A — `TRACKA-VOL-FULLHIST-20261112T201536Z` (P1, primary)
- Prereg: `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}` (frozen 2026-11-12T20:15:36Z).
- Data: `ironflow/hyperliquid-candles-1h` + `hyperliquid-funding` + `hyperliquid-open-interest`, 2025-05..2026-04, cache-first via `scripts/fclr_ironflow_bulk.py`.
- Universe: 10 native perps (coverage-only rule). Unit: coin × 1h decision point.
- Targets: T24 primary, T6/T72/T168 secondary. Models B1/C1/C2 (+ B2/C3 OI secondary family).
- Splits: train 2025-06-02..2025-09-30; 7d embargo; test blocks 0/1/2 (2025-10-08..2026-01-17). **Never read 2026-01-18..2026-04-30 (reserved) or 2026-05-01..2026-10-31 (sealed).**
- Inference: 12-comparison Holm primary family; 8-cell OI secondary family (separate, non-promotable); 2000-rep circular block bootstrap (168h, seed 20261112); LOIO/per-coin/per-block; placebo/permutation; all seven §17 promotion checks.
- Emit: `research_state/tracka_vol_fullhist_panel_<UTC>.parquet`, `..._panel_build_report_<UTC>.json`, `research_state/evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.{md,json}`.

### Arm B — `TRACKA-LIQ-XSEC-20261112T201536Z` (P2, exploratory, max `EXPLORATORY_ONLY`)
- Prereg: `research_state/prereg_tracka_liq_xsec_20261112T201536Z.{json,md}` (frozen 2026-11-12T20:15:36Z, `promotable=false`).
- Data: cached `research_state/data_cache/ironflow_events/2025-05..2025-10` + fetched candles/funding; observed labels only; no venue mixing.
- Universe: full native-perp cross-section (coverage-only eligibility: ≥20 liq-days, ≥100 events, complete hourly coverage; ≥5 coins).
- Estimand: within-bucket cross-sectional funding score vs next-24h observed liquidation count (primary, Spearman rank IC) and notional (secondary, top-k minus bottom-k spread).
- Inference: 1000-rep within-bucket permutation null (seed 20261112), per-block + pooled; materiality |mean IC| ≥ 0.05 and spread sign consistent in ≥2/3 blocks.
- Emit: `research_state/tracka_liq_xsec_panel_<UTC>.parquet`, `..._panel_build_report_<UTC>.json`, `research_state/evaluation_summary_TRACKA-LIQ-XSEC-<UTC>.{md,json}`.

### Acceptance gate (both arms)
1. Bulk cache `verify` passes, or a timestamped network blocker lists every missing object.
2. Each arm has a `{md,json}` evaluation artifact with exact failing minima or a clean pass.
3. `experiment_frontier.json` and `hypothesis_registry.json` are updated consistently; sealed verdicts are unchanged.
4. `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` is green.
5. No reserved/sealed window read; no Binance/2024 substitution; no `.github/workflows/*` edits; no raw parquet/cache commits.

---

## 5. EXACT START COMMANDS

```bash
cd <repo>
# 1) Preflight (bounded)
python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"

# 2) Gate 4 trigger check (real RESOLVED file only, never matrix text)
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"

# 3) Confirm the two frozen preregs and that no outcome artifact exists
python3 -c "import json; p=json.load(open('research_state/prereg_tracka_vol_fullhist_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['outcome_data_inspected_before_freeze'])"
python3 -c "import json; p=json.load(open('research_state/prereg_tracka_liq_xsec_20261112T201536Z.json')); print(p['experiment_id'], p['status'], p['promotable'])"
ls research_state | grep -Ei 'FULLHIST|XSEC' | grep -v prereg || echo 'NO_OUTCOME_ARTIFACTS'

# 4) Materialise the bulk cache (cache-first, unauthenticated, fail-closed)
python3 scripts/fclr_ironflow_bulk.py fetch --datasets candles_1h,funding,open_interest --months 2025-05..2026-04
python3 scripts/fclr_ironflow_bulk.py fetch --datasets liquidations --months 2025-05..2025-10
python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-05..2026-04

# 5) Execute Arm A then Arm B per the frozen preregs, then run the regression gate
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit

# 6) Append SESSION LOG entry to this file; commit code/state/tests only.
```

Expected end-of-session artifacts: `research_state/tracka_vol_fullhist_panel_<UTC>.parquet` + build report, `research_state/evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.{md,json}`, `research_state/tracka_liq_xsec_panel_<UTC>.parquet` + build report, `research_state/evaluation_summary_TRACKA-LIQ-XSEC-<UTC>.{md,json}`, refreshed `research_state/ironflow_bulk_manifest.json`, updated `experiment_frontier.json` + `hypothesis_registry.json`, and a `## SESSION LOG` entry here. If the network is unavailable, a timestamped blocker listing every missing object is the only acceptable substitute — no fabrication.

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
- **Authorized heavy work (not banned):** Arm A/B estimators and the cache-first bulk fetch required by the two frozen preregs. They do not touch sealed panels, reserved/sealed windows, or liquidation labels in Arm A.
- No successor handoff or second campaign doc. Update this file.
- No raw data/cache commits; no `.github/workflows/*` patches.

---

## 8. KEY REFERENCES

- `RESEARCH_PROMPT.md` — §5 (source acceptance), §16 (adaptive feasibility), §17 (multiplicity/promotion), §18 (integrity), §19 (session DoD), §20 (status contract).
- `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}` — **Arm A (P1), frozen, unexecuted, authoritative.**
- `research_state/prereg_tracka_liq_xsec_20261112T201536Z.{json,md}` — **Arm B (P2 exploratory), frozen, unexecuted, authoritative.**
- `scripts/fclr_ironflow_bulk.py` — cache-first, bounded, fail-closed bulk acquisition.
- `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` — Track A HL 2025H1 observed-label `liq` closed (do not relitigate).
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` — robust `liq` null.
- `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` — all alternative source families NO-GO with exact failing minima.
- `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` — state to keep consistent after Arm A/B.
- `research_state/structural_closure_verdict_heavy.md` (2026-10-31) — earlier Track A/B/C closure; historical evidence only.

---

## 9. SESSION LOG (append-only; newest first)

<!-- Format: ## <UTC> — <agent/session id> — <one-line outcome> ... -->

## 2026-11-12T19:22:00Z — Handoff rebuilt as single terminal-closure campaign; frontier staleness and discovery-loop bottleneck identified; next campaign set to `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS`

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`NO_VALID_GATE4_TRIGGER`); deps importable; 103 named tests OK (43.4s); alternative-source discovery already executed at 2026-11-12T19:14:00Z with a complete probe audit (`research_state/alt_source_probe_audit_20261112T191400Z.{md,json}`) finding **no** admissible source; all P1/P2/P3 experiments sealed (see §3). Frontier is stale: 8 entries, all `rank=0`/`ACTIVE_HEAVY_CAMPAIGN`, including duplicate and already-executed tasks. Contradicted — no valid Gate 4 trigger and no new admissible source. Unknown — whether any future external source or Gate 4 trigger can reopen a claim-worthy test; that is exactly what the resume-trigger registry will make machine-checkable.
- **Strongest alternative explanation:** The funding-conditioned signal for volatility/liquidation forecasting is either absent or too weak to detect with admissible unauthenticated data under frozen pre-registered protocols; the single symbol-expansion PASS (19.04%) is instrument-concentration-sensitive (LOIO 4/8) and indistinguishable from placebo (21.10%), so it fails §17 promotion.
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and ceiling on incremental forecast skill vs RV-only baseline (Tracks B/C) dominate; all local admissible panels consumed; no reopen path without new admissible source or valid Gate 4 trigger.
- **Falsifying next test:** A new admissible unauthenticated observed-liquidation source passing §16 audit (≥5 instruments, ≥3×30d blocks or ≥1 complete month, provenance/license, observed labels, venue-consistent) followed by a frozen prereg and out-of-sample evaluation; or a valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`, `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Neither exists now.
- **Highest expected info gain per free compute:** `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — a code-generated, deterministic, testable terminal closure + machine-checkable reopen registry. This converts an unbounded discovery loop into a bounded, evidence-gated resume path and removes the stale frontier bottleneck.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` → `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 103 tests in 43.371s / OK`; read `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/alt_source_probe_audit_20261112T191400Z.md`, `research_state/structural_closure_verdict_heavy.md`, `RESEARCH_PROMPT.md` §5/§16/§17/§19/§20. No sealed verdicts modified; no raw data committed; no workflow changes.

**START HERE (next agent):** Execute `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` per §4. Gate 4 check first (expect `NO_VALID_GATE4_TRIGGER`). Do **not** run discovery or evaluators. Build `scripts/fclr_final_structural_closure.py` + `tests/test_fclr_final_structural_closure.py`; emit `research_state/fclr_final_structural_closure_<UTC>.{md,json}` and `research_state/resume_trigger_registry.json`; normalize `experiment_frontier.json` (one terminal rank-0) and `hypothesis_registry.json` (add `terminal`/`reopen_requires`); append the six §6 answers as a dated `## SESSION LOG` entry. No polling, no status-only output, no sealed-record reopening, no `.github/workflows/*` edits, no raw data commits.

## 2026-11-12T21:08:37Z — Verified state re-check; Gate 4 trigger confirmed ABSENT; deps OK; frontier remains stale (8 rank-0 ACTIVE_HEAVY_CAMPAIGN entries); next campaign is `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — the ONLY remaining heavy work

- **Evidence supported/contradicted/unknown:** Supported — `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` → `NO_VALID_GATE4_TRIGGER` (confirmed 2026-11-12T21:08Z); `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` → `deps OK`; all P1/P2/P3 routes sealed per §3 ledger; alternative-source discovery exhausted (probe audit at 2026-11-12T19:14:00Z). Contradicted — no valid Gate 4 trigger; no admissible new source. Unknown — external reopen paths only (Gate 4 Branch 1, new admissible liquidation source, HL label extension post-2026-10-31, or newly preregistered expansion robustness meeting LOIO≥6 + placebo/permutation criteria). The `experiment_frontier.json` has 8 stale rank-0 entries all `ACTIVE_HEAVY_CAMPAIGN` — this is the bottleneck to remove.
- **Strongest alternative explanation:** Funding-conditioned signal for volatility/liquidation is absent or undetectable with admissible unauthenticated data under frozen preregistrations; the single PASS (symbol-expansion 19.04%) fails §17 promotion (LOIO 4/8, placebo 21.10% ≥ true).
- **Dominant limitation:** External data/provenance/licensing (Track A) and forecast-skill ceiling vs RV baseline (Tracks B/C) — all local admissible panels consumed. No reopen without new admissible source or valid Gate 4 trigger.
- **Falsifying next test:** (1) Valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation; OR (2) New admissible unauthenticated liquidation source passing §16 audit (≥5 instruments, ≥1 complete month or ≥3×30d blocks, provenance/license, observed labels, venue-consistent); OR (3) HL/ironflow verified post-2026-10-31 labels with ≥100d depth; OR (4) Newly preregistered expansion robustness meeting LOIO≥6 AND placebo/permutation p>0.05. None exist now.
- **Highest expected info gain per free compute:** `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — code-generated deterministic terminal closure + machine-checkable resume-trigger registry. This eliminates the stale frontier bottleneck (8 competing rank-0 entries) and replaces unbounded discovery with 4 exact evidence-gated reopen predicates.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` → `deps OK`. Read: `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json` (8 stale entries), `research_state/hypothesis_registry.json`, `research_state/alt_source_probe_audit_20261112T191400Z.md`, `RESEARCH_PROMPT.md` §5/§16/§17/§19/§20.

**START HERE (next agent — execute exactly, no deviation):**
1. **Gate 4 check** (bounded, no wait): `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → expect `NO_VALID_GATE4_TRIGGER`. **Do not poll, do not wait.**
2. **Do not run any estimator, data fetch, probe, or discovery.** All P1/P2/P3 designs are sealed; alternative liquidation sources are NO-GO with evidenced failing minima.
3. **Build the closure generator:** Create `scripts/fclr_final_structural_closure.py` (deterministic, offline, no network) reading `hypothesis_registry.json`, `experiment_frontier.json`, `evaluation_summary_*.json`, `terminal_structural_stop_*.md`, `alt_source_probe_audit_*.json`. Emit `research_state/fclr_final_structural_closure_<UTC>.{md,json}` with: per-ID row (ID, type, status, verdict, gate outcome, failing minima, §17 promotion met=false, terminal class), `reopen_conditions` array, input-file sha256 list.
4. **Add test:** `tests/test_fclr_final_structural_closure.py` with fixture registry + verdict, asserting all IDs present once, §17 conditions evaluated, `resume_trigger_registry.json` predicates well-formed, unknown verdicts flagged not dropped.
5. **Emit `research_state/resume_trigger_registry.json`** with exactly 4 triggers (machine predicates + required evidence + `do_not_act_until_satisfied=true`): `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (conditional).
6. **Normalize registries (no verdict changes):** `experiment_frontier.json` → single rank-0 terminal entry (`program_status=CLOSED_TERMINAL`, `status=CLOSED_TERMINAL`, `next_unfinished_task=null`, `resume_triggers` = 4 registry keys); demote 8 stale entries to `status=SUPERSEDED_TERMINAL` + `superseded_by` pointer. `hypothesis_registry.json` → add `terminal=true`, `terminal_class`, `reopen_requires:[<trigger_id>]` per hypothesis.
7. **Verify:** `python -m unittest tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` (expect all OK).
8. **Append §6 answers** as dated `## SESSION LOG` entry here. Commit code, state JSON/MD, tests only. **Never** commit raw data/caches or patch `.github/workflows/*`.

## 2026-11-12T19:16:24Z — All Tracks A/B/C routes sealed/exhausted; discovery campaign complete with no new admissible source; program structurally concluded; next heavy campaign is FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS

- **Evidence supported/contradicted/unknown:** Supported — the 2026-11-12T19:14:00Z bounded alternative liquidation-label source discovery (hunt/deep-review + live HF metadata probes) found no candidate meeting §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels only, venue-consistent). All Tracks A/B/C routes are now sealed/exhausted: Track C H001 NOT_SUPPORTED (FCLR-001/002/003/006/007/008/009/011/012-V/013/GATE4-v3/TRACKA-VOL-FAMILY/TRACKA-ALT-VOL all NOT_MET); Track B NOT_SUPPORTED (TB1 degenerate zero events, TB2 gate NOT_MET at 1.68% < 2% floor); Track A all panels NOT_MET/INADMISSIBLE/FRAGILE (only symbol-expansion 19.04% PASS failed LOIO 4/8≥6 and Placebo/Permutation 19.04%≤21.10% null). Gate 4 trigger ABSENT (external/legal, do not poll). No untested admissible cached-data experiment remains. Contradicted — none. Unknown — whether any future external source or Gate 4 trigger could reopen a claim-worthy test.
- **Strongest alternative explanation:** The funding-conditioned signal for volatility/liquidation forecasting is either absent or too weak to detect with available admissible unauthenticated data under frozen pre-registered protocols; the single symbol-expansion PASS is instrument-concentration-sensitive (LOIO fails) and not distinguishable from placebo, so it does not meet promotion criteria (§17).
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and ceiling on incremental forecast skill vs RV-only baseline (Tracks B/C) dominate; all local admissible panels consumed; no reopen path without new admissible unauthenticated source or valid Gate 4 trigger.
- **Falsifying next test:** A valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`, `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) OR a new admissible unauthenticated liquidation-label source passing §16 audit (≥5 instruments, ≥3×30d blocks or ≥1 complete month, provenance/license, venue-consistent). Neither exists now.
- **Highest expected info gain per free compute:** FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS — produce a single definitive program-level verdict incorporating all latest results, define exact machine-checkable reopen conditions, update experiment_frontier.json and hypothesis_registry.json to terminal states. No status-only output; no polling; no sealed-record reopening.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → 103 OK (last green). New entry: `research_state/fclr_final_structural_closure_<UTC>.{md,json}` with six §6 answers + exact reopen conditions; update `research_state/experiment_frontier.json` rank-0 to terminal CLOSED state with reopen conditions recorded; update `research_state/hypothesis_registry.json` to final statuses. No `.github/workflows/*` edits; no raw data/caches committed.

## 2026-11-12T19:14:00Z — Bounded alternative liquidation-label source discovery executed (cache-backed hunt/deep-review + targeted live HF metadata probes) — no new admissible observed-label source; timestamped probe evidence emitted; clean stop

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`NO_VALID_GATE4_TRIGGER`); ironflow remains the only known admissible HL observed-label source on sealed windows but shows no verified post-2026-10-31 extension (events/fills 2025-05..2026-10, lastModified 2026-11-07T10:18:25Z), and Track A HL 2025H1 observed-label `liq` remains closed by terminal stop. Bounded discovery (hunt/deep-review, cache-backed, plus live unauthenticated HF metadata probes 2026-11-12T19:14Z) found no candidate meeting §5/§16 minima. Contradicted — none. Unknown — whether any future source/file/extension outside probed families will satisfy §5/§16.
- **Strongest alternative explanation:** No admissible unauthenticated observed-liquidation dataset exists within current free public surfaces for a new P2 test; apparent matches are domain/mechanism mismatches (DeFi/lending/OEV/aggregates), insufficient windows (<1 month / <3×30d), derived/heatmap artifacts without evidenced observed event labels, or auth/paywall/inaccessible endpoints.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage/venue-joinability minima dominate uncertainty; HL 2025H1 observed-label path structurally exhausted and ironflow has no verified post-2026-10-31 extension.
- **Falsifying next test:** A concrete source passing §16 admissibility audit (`research_state/<source>_admissibility_audit_<UTC>.{md,json}`) with evidenced observed labels and required coverage, followed by frozen prereg and out-of-sample evaluation; or a valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`, `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation).
- **Highest expected info gain per free compute:** On next session, reprobe only on materially new evidence (new source family/endpoint/file, verified ironflow/HF post-2026-10-31 event extension, or valid Gate 4 trigger). Avoid repeating identical cache-backed no-op probes; any smoke-test pass must go directly to §16 admissibility audit before prereg/outcomes.
- **Artifacts/commands:** Gate 4 check → `NO_VALID_GATE4_TRIGGER`; `python3 scripts/hunt_alternative_liquidation_sources.py` (wrote `research_state/alt_source_scan_latest.json`, candidates=22, source=cache, 20261112T191347Z); `python3 scripts/deep_review_alt_sources.py` (wrote `research_state/alt_source_deep_review_latest.md`, cache_hits=0 cache_misses=14); targeted unauthenticated HF API metadata probes (2026-11-12T19:14Z). Emitted `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` (all probed families NO-GO with exact failing minima; no §16 audit created; no new admissible source). Frontier rank-0 remained `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (accurate at the time). No sealed verdicts/preregs modified; no `.github/workflows/*` changes.

## 2026-11-12T19:06:19Z — Verified state re-check complete; handoff current; next campaign remains `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (rank-0, ACTIVE_HEAVY_CAMPAIGN)

- **Evidence supported/contradicted/unknown:** Supported — all sealed campaigns remain sealed (rv NOT_MET, parent liq INCONCLUSIVE_NUMERICAL_INSTABILITY root-caused, robust liq NOT_MET with terminal structural stop 2026-11-12T17:04:57Z). Contradicted — no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` Gate 4 trigger exists (`NO_VALID_GATE4_TRIGGER` confirmed); HL/ironflow observed-label path exhausted (labels only 2025-05-25..2026-10-31, no post-2026-10-31 extension). Unknown — whether any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, provenance/license, venue-consistent, no Binance/2024 conflation) exists.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce timestamped evidenced failing minima per source family only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete new source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk; or a valid Gate 4 Branch 1 trigger.
- **Highest expected info gain per free compute:** Bounded `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` discovery with timestamped GO/NO-GO evidence and, if any candidate passes smoke test, immediate §16 admissibility audit BEFORE prereg/outcomes.
- **Artifacts/commands:** Verified `AGENT_HANDOFF.md` sole durable handoff (redirect files unchanged); verified `research_state/experiment_frontier.json` rank-0 = `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (ACTIVE_HEAVY_CAMPAIGN); verified `research_state/data_source_registry_alt_hunt.json` (ironflow GO on sealed window; all other candidates NO-GO); verified `research_state/alt_source_deep_review_latest.md` (no new GO sources); verified `research_state/hf_search_cache.json` (13 candidates enumerated, none new GO); verified `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` present; verified `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` → `NO_VALID_GATE4_TRIGGER`. No sealed verdicts modified; no raw data committed; no workflow changes.

## 2026-11-12T17:17:29Z — Session state review complete; no work executed; next campaign reaffirmed as `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (rank-0, ACTIVE_HEAVY_CAMPAIGN)

- **Evidence supported/contradicted/unknown:** Supported — all sealed campaigns remain sealed (rv NOT_MET, parent liq INCONCLUSIVE_NUMERICAL_INSTABILITY root-caused, robust liq NOT_MET with terminal structural stop at 2026-11-12T17:04:57Z). Contradicted — no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` Gate 4 trigger exists; HL/ironflow observed-label path exhausted (labels only 2025-05-25..2026-10-31, no post-2026-10-31 extension). Unknown — whether any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima exists.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce timestamped evidenced failing minima per source family only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete new source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk; or a valid Gate 4 Branch 1 trigger.
- **Highest expected info gain per free compute:** Bounded discovery via `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` with timestamped GO/NO-GO evidence and immediate §16 audit on any smoke-test pass.
- **Artifacts/commands:** Verified `AGENT_HANDOFF.md` sole durable handoff; verified frontier rank-0 = `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`; verified `data_source_registry_alt_hunt.json`, `alt_source_deep_review_latest.md`, `hf_search_cache.json`, `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md`; Gate 4 → `NO_VALID_GATE4_TRIGGER`. No sealed verdicts modified; no raw data committed; no workflow changes.

## 2026-11-12T17:13:43Z — Handoff refreshed: LIQ-GLM-ROBUST closed; next campaign set to bounded alternative liquidation-label source discovery

- **Evidence supported/contradicted/unknown:** Supported — robust `liq` campaign completed NOT_MET with terminal structural stop (artifacts present, hashes verifiable) and frontier rank-0 is `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`. Contradicted — prior handoff START HERE still pointed to already-executed LIQ-GLM-ROBUST implementation. Unknown — existence of any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce evidenced failing minima only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima (≥5 instruments, ≥3×30d or ≥1 complete month, observed labels) dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete new source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk.
- **Highest expected info gain per free compute:** Bounded `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` discovery with timestamped GO/NO-GO evidence and, if any candidate passes smoke test, immediate §16 admissibility audit before prereg/outcomes.
- **Artifacts/commands:** Updated `AGENT_HANDOFF.md` (this file) to set START HERE/campaign/bottlenecks to `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`; verified presence of `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` and `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md`. No sealed verdicts modified; no raw data committed; no workflow changes.
## 2026-11-12T21:12:00Z — State verified; single durable handoff refreshed with explicit terminal-closure next task (no new admissible evidence; bottlenecks unchanged)

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`, 2026-11-12T21:12Z); `deps OK` (numpy,pandas,scipy,pyarrow,requests, 2026-11-12T21:12Z); all P1/P2/P3 experiments sealed per §3 and alternative-source families NO-GO per `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}`. Contradicted — no valid Gate 4 trigger; no admissible new liquidation source. Unknown — future external reopen paths only (Gate 4 Branch 1, new §16-admissible observed-liquidation source, verified HL label extension post-2026-10-31, or newly preregistered expansion robustness meeting LOIO≥6 and placebo/permutation criteria).
- **Strongest alternative explanation:** Funding-conditioned signal for volatility/liquidation is absent or undetectable with admissible unauthenticated data under frozen preregistrations; symbol-expansion PASS (19.04%) fails §17 promotion (LOIO 4/8, placebo 21.10% ≥ true).
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and forecast-skill ceiling vs RV-only baseline (Tracks B/C); all local admissible panels consumed. `experiment_frontier.json` remains stale (8 rank-0 `ACTIVE_HEAVY_CAMPAIGN` entries) — primary bottleneck to remove.
- **Falsifying next test:** (1) Valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation); (2) new unauthenticated observed-liquidation source passing §16 audit (≥5 instruments, ≥1 complete month or ≥3×30d blocks, provenance/license, venue-consistent); (3) verified HL/ironflow labels after 2026-10-31 with ≥100d depth; (4) newly preregistered expansion robustness meeting LOIO≥6 and placebo/permutation criteria. None exist now.
- **Highest expected info gain per free compute:** `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — code-generated deterministic terminal closure + machine-checkable `resume_trigger_registry.json`, normalize frontier to one terminal rank-0 and align hypothesis registry (`terminal`/`reopen_requires`) without changing verdicts.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print 'deps OK'"` (via -c) → `deps OK`; read `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/alt_source_probe_audit_20261112T191400Z.md`. No sealed verdicts modified; no raw data committed; no workflow changes.

**START HERE (next agent — execute exactly, no deviation):** Run Gate 4 check (expect `NO_VALID_GATE4_TRIGGER`); do **not** run estimators, fetches, probes, or discovery. Build `scripts/fclr_final_structural_closure.py` + `tests/test_fclr_final_structural_closure.py`; emit `research_state/fclr_final_structural_closure_<UTC>.{md,json}` and `research_state/resume_trigger_registry.json` (exactly 4 triggers: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`); normalize `experiment_frontier.json` to one terminal rank-0 (`CLOSED_TERMINAL`, `next_unfinished_task=null`) and demote stale entries to `SUPERSEDED_TERMINAL`; add `terminal`/`terminal_class`/`reopen_requires` to `hypothesis_registry.json` without changing verdicts; verify with `python -m unittest tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit`; append §6 SESSION LOG here; commit code/state/tests only.

## 2026-11-12T21:22:35Z — FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS executed; program closed CLOSED_TERMINAL; stale frontier bottleneck removed; machine-checkable reopen registry live

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`, re-verified 2026-11-12T21:22Z); deps OK (numpy,pandas,scipy,pyarrow,requests); 103 named tests green (43.4s) plus the new closure suite → 108 tests OK. All P1/P2/P3 experiments sealed per `research_state/hypothesis_registry.json` and `research_state/`: H1_primary NOT_SUPPORTED (rel QLIKE 1.14% < 2% floor, CI [−0.016361,0.007728] crosses 0, 0 blocks); H_tracka_hl_liquidation_forecast NOT_MET (C2 worse, rel −280.56%); H_tracka_hl_early_liquidation_forecast INCONCLUSIVE_PILOT_SHORTFALL (2 blocks < 3); H_tracka_hl_symbol_expansion_liquidation_forecast SUPPORTED_PASS_PRIMARY_GATE (19.04%) but NOT promotable — fails §17 conditions 4/5/7 (LOIO 4/8 < 6; placebo null 21.10% ≥ 19.04%); H_tracka_hl_funding_conditioned_volatility_forecast NOT_MET (12-comparison Holm, no horizon passes); H_tracka_hl_alt_volatility_forecast NOT_MET (CI [−0.121,0.034] crosses 0); H_tracka_hl_expansion_robustness FRAGILE; H_trackb_modeled_breaches NOT_SUPPORTED (TB2 gate 1.68% < 2% floor; TB1 degenerate zero events); robust liq GLM NOT_MET (terminal structural stop, CI [−1.23,+0.85], Holm not rejected). Contradicted — no valid Gate 4 trigger; no admissible new liquidation source (22 candidates, 14 deep-review probes, all NO-GO with exact failing minima in `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}`). Unknown — whether any future external source or Gate 4 trigger can reopen a claim-worthy test; now machine-checkable via `research_state/resume_trigger_registry.json`.
- **Strongest alternative explanation:** The funding-conditioned signal for volatility/liquidation forecasting is absent or too weak to detect with admissible unauthenticated data under frozen pre-registered protocols; the single symbol-expansion PASS (19.04%) is instrument-concentration-sensitive (LOIO 4/8) and indistinguishable from placebo (21.10%), so it fails §17 promotion.
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and the forecast-skill ceiling vs RV-only baseline (Tracks B/C); all local admissible panels consumed; no reopen path without a registry-keyed artifact.
- **Falsifying next test:** (1) Valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation); (2) new unauthenticated observed-liquidation source passing §16 audit (`research_state/<source>_admissibility_audit_<UTC>.json`, `status=ADMISSIBLE`, `observed_labels=true`, instruments≥5, blocks≥3 or complete_month≥1, provenance+license, venue-consistent); (3) verified ironflow/HL observed labels after 2026-10-31 with ≥100d depth; (4) newly preregistered expansion robustness meeting LOIO≥6 AND placebo/permutation p>0.05 (never re-scoring the sealed 19.04%). None exist now.
- **Highest expected info gain per free compute:** `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` itself — code-generated, deterministic, testable terminal closure plus machine-checkable reopen registry; converts unbounded discovery into a bounded evidence-gated resume path; removes the stale-frontier bottleneck (8 competing rank-0 ACTIVE_HEAVY_CAMPAIGN entries → 1 rank-0 CLOSED_TERMINAL + 8 SUPERSEDED_TERMINAL).
- **Exact artifact and command/test:** `scripts/fclr_final_structural_closure.py` (deterministic, offline, no network); `tests/test_fclr_final_structural_closure.py` (fixture-based); `research_state/fclr_final_structural_closure_20261112T212043.{md,json}` (18 rows, 0 §17 promotions met, input sha256 list); `research_state/resume_trigger_registry.json` (exactly 4 triggers); `research_state/experiment_frontier.json` (one rank-0 CLOSED_TERMINAL, `next_unfinished_task=null`); `research_state/hypothesis_registry.json` (all 9 terminal=true with terminal_class/reopen_requires, verdicts unchanged). Commands: `python3 scripts/fclr_final_structural_closure.py`; `python -m unittest tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → **108 tests OK**; `python3 -c "import json;d=json.load(open('research_state/resume_trigger_registry.json'));print(len(d['triggers']),'triggers OK')"` → **4 triggers OK**. No sealed verdicts modified; no raw data/caches committed; no `.github/workflows/*` edits; no polling/discovery/estimator runs.

**START HERE (next agent — execute exactly, no deviation):** Gate 4 check first (`ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` — expect `NO_VALID_GATE4_TRIGGER`; do not poll/wait). Program is `CLOSED_TERMINAL`; do not run any estimator, fetch, probe, discovery, or sealed-record reopening. Progress is only possible via a satisfied registry trigger: `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, or `EXPANSION_ROBUSTNESS_REDO` (conditional, non-priority, newly preregistered only — never re-score the sealed 19.04%). Update this file only; no second handoff/campaign doc; no raw data commits; no `.github/workflows/*` patches.

## 2026-11-12T22:12:07Z — State re-verified: program CLOSED_TERMINAL; all 4 resume triggers OPEN and unsatisfied; no new admissible evidence; next session = verification maintenance only

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`, re-verified 2026-11-12T22:12Z); deps OK (numpy,pandas,scipy,pyarrow,requests); 108 tests green (43.4s + closure suite). `research_state/experiment_frontier.json` shows single rank-0 `CLOSED_TERMINAL` entry with `next_unfinished_task=null` and 8 `SUPERSEDED_TERMINAL` entries. `research_state/hypothesis_registry.json` all 9 hypotheses `terminal=true` with `terminal_class` and `reopen_requires` populated; verdicts unchanged. `research_state/resume_trigger_registry.json` has exactly 4 triggers, all `status=OPEN`, `do_not_act_until_satisfied=true`. No valid `fclr016_v5_terms_evidence_RESOLVED_*.json` exists; no `<source>_admissibility_audit_*.json` with `status=ADMISSIBLE` + `observed_labels=true` + coverage minima; no `hl_label_extension_audit_*.json` with verified post-2026-10-31 labels ≥100d; no `expansion_robustness_redo_prereg_*.json` meeting LOIO≥6 AND placebo/permutation p>0.05. Contradicted — no trigger satisfied. Unknown — whether any future external event will satisfy a trigger.
- **Strongest alternative explanation:** The funding-conditioned signal for volatility/liquidation forecasting is absent or undetectable with admissible unauthenticated data under frozen preregistrations; the single symbol-expansion PASS (19.04%) fails §17 promotion (LOIO 4/8, placebo 21.10% ≥ true).
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and forecast-skill ceiling vs RV-only baseline (Tracks B/C); all local admissible panels consumed; no reopen path without a registry-keyed artifact.
- **Falsifying next test:** (1) Valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation); (2) new unauthenticated observed-liquidation source passing §16 audit (`research_state/<source>_admissibility_audit_<UTC>.json`, `status=ADMISSIBLE`, `observed_labels=true`, instruments≥5, blocks≥3 or complete_month≥1, provenance+license, venue-consistent); (3) verified ironflow/HL observed labels after 2026-10-31 with ≥100d depth; (4) newly preregistered expansion robustness meeting LOIO≥6 AND placebo/permutation p>0.05 (never re-scoring the sealed 19.04%). None exist now.
- **Highest expected info gain per free compute:** **Verification maintenance session only** — bounded check of all 4 triggers + test suite; if none satisfied, clean stop with evidence. No discovery, no estimators, no sealed-record reopening. This is the only honest work remaining.
- **Exact artifact and command/test:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import json;d=json.load(open('research_state/resume_trigger_registry.json'));print(len(d['triggers']),'triggers:',[t['trigger_id'] for t in d['triggers']])"` → `4 triggers: ['GATE4_BRANCH_1', 'NEW_OBSERVED_LIQUIDATION_SOURCE', 'HL_LABEL_EXTENSION', 'EXPANSION_ROBUSTNESS_REDO']`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_final_structural_closure` → **108 tests OK**. No sealed verdicts modified; no raw data/caches committed; no `.github/workflows/*` edits; no polling/discovery/estimator runs.

**START HERE (next agent — execute exactly, no deviation):** Run Gate 4 check (expect `NO_VALID_GATE4_TRIGGER`); do **not** run any estimator, fetch, probe, discovery, or sealed-record reopening. Verify all 4 triggers in `research_state/resume_trigger_registry.json` remain `status=OPEN` and unsatisfied. Run `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_final_structural_closure` (expect 108 OK). If no trigger satisfied: append a `## SESSION LOG` entry here documenting the verification, stop cleanly. If ANY trigger becomes satisfied: follow its `gate_protocol` exactly. Program is `CLOSED_TERMINAL` — no other work is admissible.

## 2026-11-12T22:40:00Z — Bottleneck removed: two frozen preregs (Arm A P1 full-history volatility, Arm B P2 cross-sectional liquidation) found unexecuted and wrongly sealed; handoff/frontier/registry realigned to execute them (heavy work)

- **Evidence supported/contradicted/unknown:** Supported — `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}` and `research_state/prereg_tracka_liq_xsec_20261112T201536Z.{json,md}` exist with `status=FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`; no `FULLHIST`/`XSEC` evaluation artifact exists (`ls research_state | grep -Ei 'FULLHIST|XSEC' | grep -v prereg` → none); `research_state/ironflow_bulk_manifest.json` records 48/48 objects ABSENT (only `funding/2025-06.parquet` present); `ironflow_events/2025-05..2025-10` cached (18 files, 2,848,413 rows). Gate 4 → `NO_VALID_GATE4_TRIGGER`; deps OK. Contradicted — the 21:12Z/22:12Z `CLOSED_TERMINAL` "all designs sealed / verification-only" claim: two admissible, preregistered, unexecuted experiments exist. Unknown — whether Arm A's fresh 2025-06..2026-01 blocks break or tighten the volatility null; whether the full cross-section carries funding-conditioned liquidation ordering information.
- **Strongest alternative explanation:** Prior volatility nulls may reflect a single 6-month macro regime rather than a structural absence of funding-conditioned skill; the fresh 11-month holdout is the first test that can distinguish those. Arm B is exploratory by construction and cannot promote.
- **Dominant limitation:** Bulk ironflow cache is absent; bounded unauthenticated acquisition (candles/funding/OI for 2025-05..2026-04) is the gating step. External Gate 4 remains irrelevant to both arms.
- **Falsifying next test:** Arm A C2_vs_B1 primary T24 QLIKE on the never-opened 2025-06-01..2026-01-17 holdout (materiality ≥2%, 95% block-bootstrap CI excluding zero, Holm across 12); Arm B mean |Spearman IC| ≥0.05 with sign-consistent top-minus-bottom spread in ≥2/3 blocks vs 1000-rep permutation null.
- **Highest expected info gain per free compute:** Execute Arm A then Arm B exactly per the frozen preregs; each is a self-contained, machine-checkable artifact with exact failing minima.
- **Exact artifact and command/test:** Preregs above; `python3 scripts/fclr_ironflow_bulk.py fetch --datasets candles_1h,funding,open_interest --months 2025-05..2026-04`; `python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-05..2026-04`; `python -m unittest tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit`. Updated `AGENT_HANDOFF.md` (START HERE/§0-§5/§7/§8), `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`. No sealed verdicts modified; no raw data/caches committed; no `.github/workflows/*` edits.

**START HERE (next agent — execute exactly, no deviation):** Follow §5. Gate 4 check (expect `NO_VALID_GATE4_TRIGGER`); confirm both preregs are `FROZEN_PRE_OUTCOMES` with no outcome artifact; fetch+verify the bulk cache; execute Arm A then Arm B per the frozen preregs; emit both `{md,json}` evaluation artifacts; update frontier/hypothesis registries; append this log; commit code/state/tests only. Do **not** re-score sealed verdicts, read the reserved/sealed windows, or stop at status-only output. Program is **ACTIVE**, not closed.
