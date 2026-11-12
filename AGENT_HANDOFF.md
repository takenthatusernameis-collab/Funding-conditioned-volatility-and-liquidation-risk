# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T16:52:59Z
**This file is the ONLY durable handoff.** It supersedes every earlier handoff, the 2026-11-12T15:47:45Z version, the 15:44:36Z/15:38:39Z "verification" sessions, the 14:56:44Z pipeline repair, the 14:37:52Z consolidation, and all earlier checkpoints. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are short redirects to this file.

**Update this file in place** (append a dated `## SESSION LOG` entry). Do **not** create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file.

**START HERE (next agent):** execute `FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1` (§4). The prereg is **already frozen** at `research_state/tracka_prereg_early2025h1_liq_glm_robust_20261112T165234Z.json` (SHA-256 `f06060c7…`). Implement `scripts/early4h_liq_glm_robust.py`, evaluate on the existing corrected panel, adjudicate. Do **not** re-diagnose the parent GLM: its instability is localized to test block 3 and is already root-caused in the Step 5 audit (`research_state/tracka_liq_glm_step5_power_coverage_20261112T165210Z.md`). If the robust estimator also returns `INCONCLUSIVE_NUMERICAL_INSTABILITY`, emit a single timestamped evidenced structural-blocker document with the exact failing minima and stop. Do not create a second campaign doc.

---

## 0. IMMEDIATE FIRST ACTION (do this now, in order)

1. Read only this file. The previous campaign was **executed** this session; do not re-run it and do not re-diagnose it.
2. Preflight is GREEN as of 2026-11-12T16:50Z (this session re-ran it): `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 103 tests OK`; panel SHA-256 `08c60803…` matches; robust prereg SHA-256 `f06060c7…`. **Do not re-run preflight from scratch to "verify" — go straight to §4 Step 2.** Only re-run if an artifact hash/coverage check fails.
3. **Execute the next heavy campaign (§4): `FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1`.** Its prereg is frozen; implement the bounded-feature estimator, evaluate, adjudicate.
4. Do **not** re-fetch candles/funding/labels, do **not** re-window, do **not** alter the sealed `134503Z` prereg or its artifacts.

Campaign is admissible, Hyperliquid-only, observed labels only, disjoint from sealed windows, and requires **no** Gate 4, **no** new source, and **no** post-2026-10-31 data.

---

## 1. WHY THIS IS THE HIGHEST-PRIORITY WORK (inferred from the repository name)

`Funding-conditioned-volatility-and-liquidation-risk` →
- **P1 — funding-conditioned volatility forecasting** (primary). **Answered:** `rv` is `NOT_MET` under the corrected sealed eval (`...145537Z`). Do not re-litigate.
- **P2 — observed liquidation risk** (co-primary). **Open.** The parent `liq` GLM returned `INCONCLUSIVE_NUMERICAL_INSTABILITY`; the root cause is diagnosed and the next estimator is pre-frozen. This is the remaining claim-advancing work.
- **P3 — modeled boundary breaches** (only after P1/P2 are exhausted).

A session is successful only if it produces **heavy, claim-advancing evidence** or a **timestamped, evidenced terminal stop** with the exact failing minima. Status-only output, re-probing already-assessed sources, cosmetic edits, and handoff churn are banned.

---

## 2. VERIFIED EVIDENCE (re-verified live 2026-11-12T16:50Z)

| Input | Coverage | Source | Prior use |
|---|---|---|---|
| Observed liquidation labels | **2025-05-25 .. 2025-10-31**; 9 target coins; **394,167 events / ~$23.38B notional** (all 192 markets: 679,487 events) | `research_state/data_cache/ironflow_events/2025-05.parquet … 2025-10.parquet` (cached, CC BY 4.0) | used in parent campaigns |
| 4h candles (RV/features) | **2025-05-01 .. 2025-10-31, 1104 bars/coin, 0 internal gaps**, all 9 coins | live `candleSnapshot` `interval=4h` | cached and used |
| Funding history (hourly) | **2025-05-01 .. 2025-10-31**, ~4416 rows/coin | live `fundingHistory` | cached and used |

**Per-coin label counts (target 9):** BTC 141,632 ($11.32B), ETH 109,681 ($8.42B), SOL 83,021 ($2.49B), XRP 27,318 ($0.64B), DOGE 9,569 ($0.32B), SUI 9,346 ($0.12B), LINK 6,144 ($0.12B), AVAX 4,361 ($0.12B), BNB 4,095 ($0.04B). BTC+ETH ≈ **63.6% of events / 83.6% of notional**.

**Label ceiling (hard):** ironflow labels exist only 2025-05-25 .. 2026-10-31. There are **no labels before 2025-05-25**. The 2024-08..2025-04 4h extension is structurally impossible for an observed-label test; do not fabricate or proxy it.

**Sealed `rv` result (do not relitigate):** `rv` `NOT_MET` — C2_vs_B1 diff `+0.243`, CI `[-0.097, 0.583]` includes 0, rel `-29.3%`, p=0.161. Artifacts: panel `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (SHA-256 `08c60803…`), eval `evaluation_summary_EARLY4H-2025H1-20261112T145537Z.{md,json}`, prereg `tracka_prereg_early2025h1_20261112T134503Z.json` (SHA-256 `fdd96bd1…`, unchanged).

**Parent `liq` GLM (executed this session):** `TRACKA-HL-EARLY4H-2025H1-LIQ-GLM`, prereg `tracka_prereg_early2025h1_liq_glm_20261112T164838Z.json` (SHA-256 `d9ebb279…`), script `scripts/early4h_liq_glm.py`, eval `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-20261112T164926Z.{md,json}`. Verdict **`INCONCLUSIVE_NUMERICAL_INSTABILITY`**:
- B1 (RV-only) is stable: mean QLIKE 4.15, max row QLIKE 212.8, **0** rows > 1e6.
- C1: mean QLIKE 4,769; max row QLIKE 4.83e6; **1** row > 1e6 (block 3 / SOL).
- C2: mean QLIKE 3.43e6; max row QLIKE 3.48e9; **2** rows > 1e6 (block 3 / SOL, DOGE).
- The instability is **localized to test block 3 (2025-09-29..2025-10-28, the Oct-2025 funding spike)**: `fundingRate` 27.7×, `premium` 12.5×, `ema_dist` 4.5× outside the training range. Blocks 0-2 are stable. Power is **not** the constraint (246-261 positive days per block). This is a **bounded-feature problem**, not a sample-size/label problem.

**Step 5 audit (this session):** `research_state/tracka_liq_glm_step5_power_coverage_20261112T165210Z.{md,json}` — power adequate, label ceiling documented, concentration documented, next campaign specified.

**Gate 4 Branch 1 trigger: ABSENT.** Only `fclr016_v5_terms_evidence_BLOCKED_…`/`_UNRESOLVED_…` exist; the literal `RESOLVED_VERIFIED` inside `fclr020_gate4_readiness_action_matrix_latest.json` is a readiness matrix, not a trigger. Do not wait or poll.

**`run_manifest.json` is an unresolved Git LFS pointer in CI.** Do not read it as JSON and do not make the campaign depend on it.

---

## 3. BOTTLENECKS REMOVED / REMAINING

| Bottleneck | Status / resolution |
|---|---|
| **Four competing handoff docs** | **Removed:** this file is the sole durable handoff; the three root `*HANDOFF*`/`*NEXT*`/`*CAMPAIGN*`/`*TASK*` files are redirects; `research_state/FCLR_CAMPAIGN_NEXT.md` is SUPERSEDED. |
| **Status-only re-verification churn** | **Removed:** this session executed the parent `liq` GLM end-to-end (prereg → script → eval → Step 5) instead of re-verifying. The next agent's first action is execution, not verification. |
| **Dependency/install wall** | **Removed for the agent loop:** `deps OK`; core deps importable. Caveat: `.github/workflows/main.yml` does not provision an agent venv from `requirements.txt`; if CI agents lack deps, report as a workflow blocker, do not patch `.github/workflows/*`. |
| **Wrong window arithmetic / 1h-vs-4h confusion** | **Removed:** 4h interval required; 5 complete Jun–Oct blocks + May ramp; per-coin reporting mandated. |
| **LFS pointer read as JSON** | **Removed:** campaign must not read `run_manifest.json`. |
| **Degenerate/invalid EARLY4H-2025H1 evaluation (134634Z)** | **Removed:** root-caused and fixed; corrected eval is valid. |
| **`liq` estimator-form instability** | **Root-caused (2026-11-12T16:52Z):** the parent log-link GLM is stable except for 1-2 block-3 rows where raw funding/premium/ema_dist leave the training support. **Next step pre-frozen:** bounded-feature GLM (`FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1`). |
| **Funding percentile warm-up** | **Removed:** `abs_fund_pct` computed from 2025-05-01. |

Do not re-diagnose the dependency wall, re-probe 1h candles, re-run alt-source discovery, reopen sealed verdicts, or re-run the parent GLM.

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1`

**Objective:** the first stable, pre-registered test of funding-conditioned features on **observed liquidation intensity** using the **same Poisson/quasi-Poisson log-link GLM** with each continuous feature **bounded to the training range**, because the parent GLM's only failure is block-3 extrapolation (§2). Reuse the **same frozen panel, universe, and splits**. `rv` is already answered; do not re-test it.

**Status: PREREG ALREADY FROZEN — do not re-freeze, do not edit it.**
- Prereg: `research_state/tracka_prereg_early2025h1_liq_glm_robust_20261112T165234Z.json` (SHA-256 `f06060c7fccb5530629bdd7ff3d7278a22ad7480a12aa86d07c3868ba1b09123`) + `.md`.
- Experiment ID: `TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST`.
- Panel: `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (SHA-256 `08c60803…`).

### Step 1 — Verify inputs (bounded, no outcome)
- Confirm panel SHA-256 `08c60803…` and robust prereg SHA-256 `f06060c7…`.
- Do **not** re-fetch caches, re-window, or recompute the panel. If the panel hash differs, rebuild via `python3 scripts/early4h_campaign.py build` and use the newest panel (deterministic, same inputs).

### Step 2 — Implement the estimator (new script; do not mutate sealed scripts)
- Add `scripts/early4h_liq_glm_robust.py`. It must:
  - Load the frozen robust prereg + corrected panel; assert both SHA-256s.
  - For `fundingRate`, `abs_fund_pct`, `premium`, `ema_dist`: compute observed `[min, max]`, mean, std on the **train split** (positive `t1_liq` rows only); clip to `[min, max]`; standardize by train mean/std. RV log features unchanged.
  - Fit Poisson/quasi-Poisson log-link by IRLS on the train split only (no regularization, no model search, no tuning).
  - Predict on the test blocks, compute QLIKE on positive rows, paired block bootstrap (2000 reps, seed 20261112), Holm across the family.
  - Emit `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-<UTC>.md` + `.json` with per-model QLIKE, paired `C2_vs_B1` Δ + CI, rel reduction, per-block/per-coin breakdown, Holm p-values, numerical-stability block (max row QLIKE ≤ 1e6), and an explicit **PASS / NOT_MET / INCONCLUSIVE_*** verdict.
  - Reuse the exact `liq`-glm evaluation conventions (positive `t1_liq` rows only, same splits/universe) so results are comparable.

### Step 3 — Evaluate and adjudicate
- **If PASS:** update `experiment_frontier.json` and `hypothesis_registry.json` atomically under the **new** experiment ID; write `research_state/final_confirmatory_verdict_liq_glm_robust_<UTC>.md`. Do not modify sealed records or `run_manifest.json`.
- **If NOT_MET:** preserve the null honestly, report it, then continue to Step 4.
- **If INCONCLUSIVE_NUMERICAL_INSTABILITY again:** report the exact per-row QLIKE and the offending rows/coins/blocks, then go to Step 4.

### Step 4 — If Step 3 is negative or inconclusive, immediately continue
1. **Terminal structural stop** with a timestamped evidenced document stating the exact failing minima (panel, blocks, coins, features, rows, QLIKE) and why no admissible cached-data estimator can resolve it. Do **not** iterate estimator forms without a materially new source or a new preregistered design.
2. Only if a genuinely new admissible source exists per `RESEARCH_PROMPT.md` §16 may a new campaign be frozen. No polling, no status-only output.

### Step 5 — Close the session
- Append a dated `## SESSION LOG` entry to **this file** with the six §6 answers.
- Update `research_state/experiment_frontier.json` (`resume_triggers`, `next_unfinished_task`, `program_status`).
- Commit code, manifests, prereg, panel build report, and verdict. **Never** commit raw data or caches.
- Only if a genuine terminal stop is reached emit a single timestamped evidenced clean-stop artifact and stop.

---

## 5. EXACT START COMMANDS

### 5.0 Preflight (run once; fix, do not stop)
```bash
cd <repo>
python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"
python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit
python3 -c "import hashlib;print(hashlib.sha256(open('research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet','rb').read()).hexdigest())"
python3 -c "import hashlib;print(hashlib.sha256(open('research_state/tracka_prereg_early2025h1_liq_glm_robust_20261112T165234Z.json','rb').read()).hexdigest())"
```
Expected: `deps OK`; `Ran 103 tests OK`; panel `08c60803…`; prereg `f06060c7…`.

### 5.1 Run the campaign (after implementing `scripts/early4h_liq_glm_robust.py`)
```bash
python3 scripts/early4h_liq_glm_robust.py
```
Expected: an `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-<UTC>.{md,json}` with a single verdict. Do not re-run the parent `early4h_liq_glm.py`.

### 5.2 Artifacts that must exist at session end
- `scripts/early4h_liq_glm_robust.py`
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-<UTC>.md` + `.json`
- updated `research_state/experiment_frontier.json` and a `## SESSION LOG` entry here
- if a terminal stop: a single timestamped evidenced structural-blocker document

Known pre-existing failures at HEAD (do **not** chase them): `tests.test_tracka_hardening_099` drift-bound (`research_state` root md+json count), probe-family inventory (newer `*probe_*.json` artifacts), and the CLI resume-gate test. They predate this campaign and are unrelated; the two named test modules are the required green gate.

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
- No reopening/relitigating/retuning sealed verdicts (Track B/C, FCLR-*, expansion robustness, H2, `rv`).
- No polling/waiting; no status-only sessions; no redundant controllers, schedulers, wrappers, or polling loops.
- **Do not** re-probe 1h candles to conclude "no early data" — use `4h`.
- **Do not** re-run the parent `liq` GLM or re-diagnose its block-3 instability; it is already root-caused.
- **Do not** create a successor handoff or a second campaign doc. Update this file.
- **Do not** commit raw data or caches.

---

## 8. KEY REFERENCES

- `RESEARCH_PROMPT.md` — §5 (source acceptance), §15 (outcome families / honest label gate), §16 (adaptive feasibility), §17 (multiplicity/promotion), §18 (integrity/deterministic resume), §19 (session DoD), §20 (status contract).
- `research_state/research_protocol_fclr010.md` — frozen Track A protocol, model forms, gate.
- `scripts/early4h_campaign.py` — sealed campaign (build/eval); do not mutate its model form.
- `scripts/early4h_liq_glm.py` — parent GLM estimator (completed, `INCONCLUSIVE_NUMERICAL_INSTABILITY`).
- `research_state/tracka_liq_glm_step5_power_coverage_20261112T165210Z.md` — Step 5 audit and robust-campaign rationale.
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-20261112T164926Z.md` — parent GLM result.
- `research_state/evaluation_summary_EARLY4H-2025H1-20261112T145537Z.md` — corrected sealed eval (`rv` NOT_MET, parent `liq` inconclusive).
- `scripts/tracka_hl_fetch_candles_early_4h.py`, `scripts/tracka_hl_expansion_funding_paginate.py` — acquisition templates.
- `scripts/create_forward_prereg.py`, `scripts/fclr010_harness.py` — prereg/harness templates (prereg helper reads the LFS-pointer manifest; the robust prereg is already frozen).
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding_early/`, `research_state/data_cache/hyperliquid_candles_4h_early/`.
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`.

---

## 9. SESSION LOG (append-only; newest first)

<!-- Format: ## <UTC> — <agent/session id> — <one-line outcome> ... -->

## 2026-11-12T16:52:59Z — Executed `FCLR-EARLY4H-2025H1-LIQ-GLM v1`; parent `liq` GLM INCONCLUSIVE (block-3 extrapolation); froze `LIQ-GLM-ROBUST v1` as the next campaign

- **Evidence supported/contradicted/unknown:** Supported — the parent log-link GLM is stable except for 1-2 block-3 rows; B1 0/1016 rows > 1e6, C1 1/1016 (block 3/SOL), C2 2/1016 (block 3/SOL,DOGE); block-3 funding/premium/ema_dist are 27.7×/12.5×/4.5× outside train range; every test block has 246-261 positive days (power adequate); labels exist only 2025-05-25..2026-10-31 (no pre-2025-05 labels); BTC+ETH 63.6% events / 83.6% notional. Contradicted — the parent verdict is a global numerical failure: it is localized. Unknown — whether a bounded-feature log-link GLM resolves `liq`.
- **Strongest alternative explanation:** The parent instability is out-of-support extrapolation of raw funding/premium/ema_dist in the Oct-2025 block, not sample size or label availability. Bounding features to the training range should remove it.
- **Dominant limitation:** Out-of-range feature extrapolation in block 3 dominates `liq` uncertainty; secondary BTC/ETH concentration and the 2025-05-25 label ceiling. No dependency/data/source/pipeline blocker remains.
- **Falsifying next test:** `scripts/early4h_liq_glm_robust.py` under the already-frozen prereg on the same panel; a stable `C2_vs_B1` with 95% CI excluding 0 and ≥2% rel QLIKE reduction falsifies "funding does not inform liquidation intensity"; a stable null or a second instability closes `liq` with a terminal stop.
- **Highest expected info gain per free compute:** §4 Steps 2-3 — implement `scripts/early4h_liq_glm_robust.py` (bounded-feature IRLS) → evaluate → adjudicate. No re-fetch, no re-window, no Gate 4, no new source.
- **Artifacts/commands:** Prereg `research_state/tracka_prereg_early2025h1_liq_glm_20261112T164838Z.{json,md}` (sha `d9ebb279…`); script `scripts/early4h_liq_glm.py`; eval `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-20261112T164926Z.{md,json}`; Step 5 audit `research_state/tracka_liq_glm_step5_power_coverage_20261112T165210Z.{md,json}`; frozen robust prereg `research_state/tracka_prereg_early2025h1_liq_glm_robust_20261112T165234Z.{json,md}` (sha `f06060c7…`). Preflight green (deps OK; 103 tests OK; panel `08c60803…`). No sealed verdicts modified; no raw data committed; workflow not edited.

## 2026-11-12T15:54:27Z — Live state re-verified at session start — working tree clean; corrected panel `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` SHA-256 `08c608035d179be8…` matches; frozen prereg `134503Z` unchanged (`fdd96bd1…`); valid eval `…145537Z` (`rv` NOT_MET, `liq` INCONCLUSIVE_NUMERICAL_INSTABILITY); `scripts/early4h_liq_glm.py` and no `*liq_glm*` prereg exist → campaign UNEXECUTED. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T15:47:45Z — Handoff re-verification + bottleneck sweep — no research outcomes. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T15:38:39Z — Preflight verification session — all preflight checks pass. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T14:56:44Z — Pipeline repair session — root-caused and fixed the degenerate EARLY4H eval; produced valid `rv` NOT_MET + `liq` INCONCLUSIVE; set next GLM campaign. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T14:37:52Z — Handoff consolidation — clarified state, surfaced degenerate EARLY4H eval, set next heavy task. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)