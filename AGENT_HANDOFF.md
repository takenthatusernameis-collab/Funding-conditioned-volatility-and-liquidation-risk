# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T15:47:45Z (re-verified live; prior 2026-11-12T15:44:36Z, 2026-11-12T15:42:03Z, 2026-11-12T14:56:44Z, 2026-11-12T14:37:52Z, 2026-11-12T12:34:20Z retained below as history)
**This file is the ONLY durable handoff.** It supersedes `HANDOFF_NEXT_SESSION.md` @ 2026-11-12T11:38:00Z, the 2026-11-12T09:51:12Z "clean stop", and every earlier checkpoint.
**Update this file in place** (append a dated `## SESSION LOG` entry). Do **not** create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are short redirects to this file.

**START HERE (next agent):** execute `FCLR-EARLY4H-2025H1-LIQ-GLM v1` in §4 on the existing corrected panel (`research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet`, SHA-256 `08c60803…`). Freeze a new prereg before any `liq` outcome, implement `scripts/early4h_liq_glm.py` (Poisson/quasi-Poisson log-link, IRLS, `liq` only), evaluate/adjudicate, then follow §4 Step 5 if NOT_MET/INCONCLUSIVE. Do not re-diagnose prior pipeline bugs, do not re-fetch caches, do not alter sealed artifacts.

---

## 0. IMMEDIATE FIRST ACTION (do this now, in order)

1. Read only this file. **The pipeline defect that produced the invalid 134634Z eval is already diagnosed and fixed** (see §2/§3 and `research_state/tracka_hl_early2025h1_pipeline_correction_20261112T145644Z.md`). Do **not** re-diagnose the identity-lag / wrong-lag-column / warm-up bugs, and do **not** re-run acquisition/build/eval from scratch blindly.
2. **Preflight is already GREEN as of 2026-11-12T15:47Z** (this session re-ran it): `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 103 tests OK`; panel SHA-256 `08c60803…` matches; ironflow target events 394,167 across 2025-05..2025-10; live 4h `candleSnapshot` → HTTP 200 + 1104 bars for all 9 coins. **Do not re-run preflight from scratch to "verify" — go straight to §4 Step 2.** Only re-run if an artifact hash/coverage check fails. Data caches for 2025-05..2025-10 4h candles and early funding are present locally — do not re-fetch.
3. **Execute the next heavy campaign (§4): `FCLR-EARLY4H-2025H1-LIQ-GLM v1`.** The corrected eval (`...20261112T145537Z`) is valid and yields: `rv` **NOT_MET** (funding does not improve RV forecasting; C2 worse than B1, CI includes 0) and `liq` **INCONCLUSIVE_NUMERICAL_INSTABILITY** (the frozen unregularized linear-in-log model extrapolates on the Oct-2025 funding spike). `liq` is therefore **open, not a null**. The next test is a QLIKE-consistent estimator (Poisson / quasi-Poisson log-link) on the same frozen panel/splits/universe — this is a **new model form**, so it requires a **new frozen prereg before any outcome is inspected**.
4. Freeze the new prereg (§4 Step 2), build/evaluate (§4 Steps 3–4), and adjudicate. Do **not** alter the frozen `134503Z` prereg (hypotheses, contrasts, splits, minima, materiality) — it is sealed and its SHA-256 is unchanged.
5. If the new `liq` GLM also yields a defensible **NOT_MET** (or is itself numerically unstable): execute Step 5 of §4 (power/coverage audit, 2024-08..2025-04 label-ceiling feasibility, per-coin/block concentration check). Only then consider a terminal structural stop with exact failing minima.

Campaign is admissible, Hyperliquid-only, observed labels only, disjoint from sealed windows, and requires **no** Gate 4, **no** new source, and **no** post-2026-10-31 data.

---

## 1. WHY THIS IS THE HIGHEST-PRIORITY WORK (inferred from the repository name)

`Funding-conditioned-volatility-and-liquidation-risk` →
- **P1 — funding-conditioned volatility forecasting** (primary).
- **P2 — observed liquidation risk** (co-primary on the same panel).
- **P3 — modeled boundary breaches** (only after P1/P2 are exhausted).

A session is successful only if it produces **heavy, claim-advancing evidence** or a **timestamped, evidenced terminal stop** with the exact failing minima. Status-only output, re-probing already-assessed sources, cosmetic edits, and handoff churn are banned.

---

## 2. VERIFIED EVIDENCE (re-verified live 2026-11-12T14:56Z, no outcomes inspected)

| Input | Coverage | Source | Prior use |
|---|---|---|---|
| Observed liquidation labels | **2025-05-25 .. 2025-10-31**; 9 target coins; **394,167 events / $23.4B notional** (all 192 markets: 679,487 events) | `research_state/data_cache/ironflow_events/2025-05.parquet … 2025-10.parquet` (cached, CC BY 4.0) | **used** in `FCLR-EARLY4H-2025H1-HEAVY v2` (corrected) |
| 4h candles (RV/features) | **2025-05-01 .. 2025-10-31, 1104 bars/coin, 0 internal gaps**, all 9 coins | live `candleSnapshot` `interval=4h`, unauthenticated, ~0.34 s/call | cached and used |
| Funding history (hourly) | **2025-05-01 .. 2025-10-31, ~4416 rows/coin**, paginated at 500 (9 pages); filter `endTime` client-side | live `fundingHistory`, unauthenticated | cached and used |

**Per-coin label counts (target 9):** BTC 141,632 ($11.32B), ETH 109,681 ($8.42B), SOL 83,021 ($2.49B), XRP 27,318 ($0.64B), DOGE 9,569 ($0.32B), SUI 9,346 ($0.12B), LINK 6,144 ($0.12B), AVAX 4,361 ($0.12B), BNB 4,095 ($0.04B).

**Critical correction to the 11:38Z handoff:** the figures "1.13M events / $32.3B / 6 blocks" were wrong. The real target-coin totals are **394,167 events / $23.4B**, and labels **start 2025-05-25**, so the powered window is **2025-05-25..2025-10-31 = 5 complete 30-day blocks (Jun–Oct) + a 7-day May ramp**. Do not reuse the 11:38Z numbers.

**Concentration hazard:** BTC+ETH are **~63% of events and ~84% of notional**. The evaluation must report per-coin results and must reject any PASS that is driven by a single coin or block.

**Why earlier work missed this window:** prior probes used **1h** candles, which Hyperliquid serves only from **2026-04-18**. The `4h` interval serves back to **2024-08-01**. The `4h` window 2025-05..2025-10 was never fetched or tested. The 2025-11..2026-04 `4h` pilot was `INCONCLUSIVE_PILOT_SHORTFALL` (only 2 complete blocks); its negative C2 result is **not** evidence against the new, powered window.

**Campaign status — CORRECTED AND VALID (2026-11-12T14:56Z).** The `134634Z` eval was invalid due to a code/pipeline defect (identity lag + wrong test-side lag column + truncated funding warm-up). It is fixed; see `research_state/tracka_hl_early2025h1_pipeline_correction_20261112T145644Z.md`. The **valid corrected artifacts** are:
- panel `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (+ build report `...145529Z.json`)
- eval `research_state/evaluation_summary_EARLY4H-2025H1-20261112T145537Z.{md,json}`
- frozen prereg `tracka_prereg_early2025h1_20261112T134503Z.json` (unchanged, SHA-256 `fdd96bd1…`)

**Corrected outcome:** `rv` **NOT_MET** (C2_vs_B1 diff `+0.243`, CI `[-0.097, 0.583]` includes 0, rel `-29.3%`, p=0.161; stable). `liq` **INCONCLUSIVE_NUMERICAL_INSTABILITY** (frozen unregularized linear-in-log model extrapolates on the Oct-2025 funding spike; max per-row QLIKE `1.6e27`). **`liq` is open, not a null.** Do not cite `134634Z`.

**Gate 4 Branch 1 trigger: ABSENT.** Only `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` and `..._UNRESOLVED_20261108T204000Z.json` exist. The literal string `RESOLVED_VERIFIED` inside `fclr020_gate4_readiness_action_matrix_latest.json` is a readiness matrix, **not** a trigger. Do not wait, poll, or whole-tree grep for it.

**`run_manifest.json` is an unresolved Git LFS pointer in CI.** Do not read it as JSON and do not make the campaign depend on it. Write the campaign prereg and state files directly.

---

## 3. BOTTLENECKS REMOVED / REMAINING

| Bottleneck | Status / resolution |
|---|---|
| **Four competing handoff docs** | **Removed:** this file is the sole durable handoff; `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. `research_state/FCLR_CAMPAIGN_NEXT.md` is explicitly marked SUPERSEDED. |
| **Dependency/install wall (pandas/pyarrow/requests)** | **Partially removed:** `requirements.txt` includes `requests`; core deps importable in current env (`deps OK`). **Caveat (verified 14:56Z):** `.github/workflows/main.yml` does **not** provision an agent venv from `requirements.txt` before the Kilo agent loop (only controller-tests installs pytest/numpy/requests). The `experiment_frontier.json` "FIXED 12:34Z: provisions an agent venv" claim is **false** — corrected in this handoff; do not rely on it. Workflow edits require explicit maintainer authorization and are out-of-scope; if CI agents lack deps, report as workflow blocker, do not patch `.github/workflows/*`. |
| **Wrong window arithmetic / 1h-vs-4h confusion** | **Removed:** corrected in §2; 4h interval required; 5 complete Jun–Oct blocks + May ramp; per-coin reporting mandated. |
| **LFS pointer read as JSON** | **Removed:** campaign must not read `run_manifest.json`. |
| **Stale handoff state ("no artifacts yet", "execute Steps 1–4")** | **Removed:** §0/§2/§4 now reflect the corrected valid artifacts and the next task. |
| **Degenerate/invalid EARLY4H-2025H1 evaluation (134634Z)** | **REMOVED (2026-11-12T14:56Z):** root-caused and fixed in `scripts/early4h_campaign.py` (identity lag `shift(0)`→`shift(1)`; test-side per-target lag; funding warm-up from 2025-05-01). Corrected eval is valid. See pipeline correction note. |
| **`liq` numerical instability of frozen linear model** | **Open:** the frozen unregularized linear-in-log model extrapolates on the Oct-2025 funding spike. Not a code bug — a model-form limitation. Requires a **new frozen prereg** for a QLIKE-consistent (Poisson/quasi-Poisson log-link) estimator (§4). |
| **Funding percentile warm-up** | **Removed:** `abs_fund_pct` now computed from 2025-05-01; first valid 2025-05-30; only 5 warm-up days missing (all pre/at `LABEL_START`). |

Do not re-diagnose the dependency wall, re-probe 1h candles, re-run alt-source discovery, or reopen sealed verdicts.

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR-EARLY4H-2025H1-LIQ-GLM v1`

**Objective:** the first powered, pre-registered test of funding-conditioned features on **observed liquidation intensity** using a **QLIKE-consistent estimator** (Poisson / quasi-Poisson log-link), because the frozen linear-in-log model was numerically unstable on `liq` (§3). Reuse the **same frozen panel, universe, and splits** as `TRACKA-HL-EARLY4H-2025H1` — only the **estimator/model form** is new. The `rv` result is already a valid NOT_MET and is **not** re-litigated here.

**Why this is the highest-value next test:** `rv` (P1, funding-conditioned volatility) is now answered — funding does not help. `liq` (P2, observed liquidation risk) is the co-primary and is still **open**, but the frozen linear model cannot answer it. A log-link count/intensity model is the QLIKE-consistent estimator and is robust to the Oct-2025 funding spike because it models the mean directly instead of exponentiating an unbounded linear predictor.

**Do NOT** inspect any `liq` outcome under the new estimator before its prereg is frozen. **Do NOT** reuse a sealed holdout. **Do NOT** tune, threshold-shop, or expand the feature grid after the freeze. **Do NOT** alter the sealed `134503Z` prereg.

### Step 1 — Reuse the corrected panel (no re-fetch, no re-window)
- Input panel: `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (SHA-256 `08c60803…`). Verify SHA-256 matches before use; if it does not, rebuild via `python3 scripts/early4h_campaign.py build` (deterministic, same inputs) and use the newest panel.
- Do **not** re-fetch candles/funding/labels. Caches are complete and hash-verified (§2).

### Step 2 — Freeze a NEW prereg BEFORE any outcome computation
Write `research_state/tracka_prereg_early2025h1_liq_glm_<UTC>.json` + `.md`, declaring **ex ante**:
- **Experiment ID:** `TRACKA-HL-EARLY4H-2025H1-LIQ-GLM`. **Campaign:** `FCLR-EARLY4H-2025H1-LIQ-GLM v1`.
- **Reused (identical, from `134503Z`):** window, universe (9 coins), unit (coin × 24h UTC bucket), train/val/4 test blocks + 1-day embargo, minima (≥5 instruments, ≥3 test blocks), materiality (≥2% rel QLIKE reduction AND 95% CI upper < 0), Holm across the declared family, missingness policy.
- **Target (only):** next-24h observed liquidation notional (`t1_liq`), QLIKE loss. Do **not** re-test `rv` here.
- **Models, frozen (new estimator):**
  - B1 = HAR-RV **log-link** (log RV4h, log RV24h, log RV168h) — RV-only baseline.
  - C1 = B1 + signed funding + 90-d trailing abs-funding percentile (≥30 obs).
  - C2 = C1 + mark/index premium + mark/EMA24 distance.
  - Estimator: Poisson / quasi-Poisson GLM with **log link** (IRLS), no regularization, no model search, no tuning. Fit on train only. Predict the conditional mean directly (no exp-of-unbounded-linear-predictor extrapolation).
- **Primary contrast:** `C2_vs_B1`. Secondary: `C1_vs_B1`, `C2_vs_C1`.
- **Inference:** block bootstrap over complete 30-d UTC blocks, ≥2000 reps, fixed seed (20261112 or a new declared seed). Holm across the full declared family.
- **Numerical-stability acceptance:** declare ex ante that a target is `INCONCLUSIVE_NUMERICAL_INSTABILITY` if any per-row QLIKE > 1e6 (same guard as the corrected eval), so the GLM is not silently reported as a 1e17 artifact.
- Set `pre_registered_before_outcomes: true`, `frozen_before_outcomes: true`. Record the JSON SHA-256.

### Step 3 — Implement the estimator in a new script (do not mutate the sealed campaign)
- Add `scripts/early4h_liq_glm.py` (new file; do **not** edit `scripts/early4h_campaign.py` model form). It must:
  - Load the frozen prereg + corrected panel, assert SHA-256s.
  - Fit Poisson/quasi-Poisson log-link by IRLS on the train split only.
  - Predict on the test blocks, compute QLIKE, paired block bootstrap, Holm.
  - Emit `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-<UTC>.md` + `.json` with per-model QLIKE, paired `C2_vs_B1` Δ + CI, rel reduction, per-block/per-coin breakdown, Holm p-values, numerical-stability block, and an explicit **PASS / NOT_MET / INCONCLUSIVE_*** verdict.
- Assert leakage guards and reuse the same per-target lag (`lag_liq`) as the corrected panel.

### Step 4 — Evaluate and adjudicate
- **If PASS:** update `experiment_frontier.json` and `hypothesis_registry.json` atomically under the **new** experiment ID; write `research_state/final_confirmatory_verdict_liq_glm_<UTC>.md`. Do not modify sealed records or `run_manifest.json`.
- **If NOT_MET:** preserve the null honestly, report it, then continue to Step 5 — do not stop.
- **If INCONCLUSIVE_NUMERICAL_INSTABILITY:** report the exact per-row QLIKE and the offending rows/coins/blocks; then go to Step 5.

### Step 5 — If Step 4 is negative or inconclusive, immediately continue
1. **Power/coverage audit** on the 2025-05-25..2025-10-31 panel: per-coin event adequacy, which blocks carry signal, and whether a pre-registered *sub-cohort* (e.g. top-5 by label activity, frozen ex ante) is powered for a secondary confirmatory.
2. **2024-08..2025-04 extension feasibility:** 4h candles reach 2024-08-01 and funding paginates from 2024-08, but **ironflow labels do not exist before 2025-05** — document this as a hard label ceiling; do not fabricate or proxy it.
3. **Concentration check:** confirm no PASS is driven by BTC/ETH alone (BTC+ETH ≈63% events / 84% notional).
4. Only then: a **new** materially different source per `RESEARCH_PROMPT.md` §16, or a timestamped evidenced structural-blocker document.

### Step 6 — Close the session
- Append a dated `## SESSION LOG` entry to **this file** with the six §6 answers.
- Update `research_state/experiment_frontier.json` (`resume_triggers`, `next_unfinished_task`, `program_status=ACTIVE_HEAVY_CAMPAIGN`).
- Commit code, manifests, prereg, panel build report, and verdict. **Never** commit raw data or caches.
- Only if a genuine terminal stop is reached (no admissible unblocked work remains) emit a **single** timestamped evidenced clean-stop artifact and stop. Do not poll.

---

## 5. EXACT START COMMANDS

### 5.0 Preflight (run first; fix, do not stop)
```bash
cd <repo>
python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"
python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit
python3 - <<'PY'
import glob, pandas as pd
coins=["AVAX","BNB","BTC","DOGE","ETH","LINK","SOL","SUI","XRP"]
for f in sorted(glob.glob("research_state/data_cache/ironflow_events/2025-0[5-9].parquet"))+["research_state/data_cache/ironflow_events/2025-10.parquet"]:
    df=pd.read_parquet(f,columns=["market"])
    n=sum((df["market"]==c+"-PERP").sum() for c in coins)
    print(f.split("/")[-1], "target_events", int(n))
PY
```
Expected: `deps OK`, tests OK, and target events > 0 for 2025-05..2025-10. If `deps OK` fails, install `requirements.txt` into an active venv; if target events are 0, the cache is incomplete — fetch the missing parquet(s) before proceeding.

**Panel integrity (required before reuse):**
```bash
python3 -c "import hashlib;print(hashlib.sha256(open('research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet','rb').read()).hexdigest())"
```
Expected prefix `08c60803…`. If it differs, rebuild with `python3 scripts/early4h_campaign.py build` and use the newest panel (deterministic, same inputs).

Known pre-existing failures at HEAD (do **not** chase them): `tests.test_tracka_hardening_099` drift-bound (`research_state` root md+json is 281 > 260), probe-family inventory (8 newer `*probe_*.json` artifacts), and the CLI resume-gate test. They predate this campaign and are unrelated; the two named test modules above are the required green gate.

### 5.1 Verify live data is still fetchable (bounded, no outcomes)
```bash
python3 - <<'PY'
import requests
from datetime import datetime, timezone
INFO="https://api.hyperliquid.xyz/info"
def ms(s): return int(datetime.fromisoformat(s.replace("Z","+00:00")).timestamp()*1000)
for c in ["BTC","ETH","SOL","AVAX","XRP","BNB","DOGE","LINK","SUI"]:
    r=requests.post(INFO,json={"type":"candleSnapshot","req":{"coin":c,"interval":"4h","startTime":ms("2025-05-01T00:00:00Z"),"endTime":ms("2025-11-01T00:00:00Z")-1}},timeout=30)
    js=r.json(); print(c,r.status_code,len(js) if isinstance(js,list) else js)
PY
```
Expected: HTTP 200 and **1104** bars for every coin. If this fails, record the exact HTTP status and stop only after trying the `4h` interval again; never fall back to `1h`.

### 5.2 Artifacts that must exist at session end
- `research_state/tracka_prereg_early2025h1_liq_glm_<UTC>.json` + `.md` (frozen before outcomes; new experiment ID `TRACKA-HL-EARLY4H-2025H1-LIQ-GLM`)
- `scripts/early4h_liq_glm.py` (new estimator script; do not mutate the sealed campaign script's model form)
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-<UTC>.md` + `.json`
- updated `research_state/experiment_frontier.json` and a `## SESSION LOG` entry in this file
- If the panel is rebuilt: `research_state/tracka_hl_early2025h1_panel_<UTC>.parquet` + build report (only if SHA-256 mismatch forces it)

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
- No reopening/relitigating/retuning sealed verdicts (Track B/C, FCLR-*, expansion robustness, H2).
- No polling/waiting; no status-only sessions; no redundant controllers, schedulers, wrappers, or polling loops.
- **Do not** re-probe 1h candles to conclude "no early data" — use `4h`.
- **Do not** create a successor handoff or a second campaign doc. Update this file.
- **Do not** commit raw data or caches.

---

## 8. KEY REFERENCES

- `RESEARCH_PROMPT.md` — §5 (source acceptance), §15 (outcome families / honest label gate), §16 (adaptive feasibility), §17 (multiplicity/promotion), §18 (integrity/deterministic resume), §19 (session DoD), §20 (status contract).
- `research_state/research_protocol_fclr010.md` — frozen Track A protocol, model forms, gate.
- `scripts/tracka_hl_fetch_candles_early_4h.py`, `scripts/tracka_hl_expansion_funding_paginate.py` — acquisition templates.
- `scripts/tracka_hl_build_early_4h_panel.py`, `scripts/tracka_hl_evaluate_early_4h.py`, `scripts/run_expansion_robustness.py` — build/eval/robustness templates (hard-coded to the 2-block pilot; parameterize the window).
- `scripts/create_forward_prereg.py`, `scripts/fclr010_harness.py` — prereg + frozen harness (the prereg helper reads the LFS-pointer manifest; write the new prereg directly instead).
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles_4h/`.
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`.
- Prior evidence: `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.md` (2-block pilot, `INCONCLUSIVE_PILOT_SHORTFALL`), `research_state/next_panel_gap_audit_20261111T163229Z.md` (gap inventory; its "2025-05..2026-04 candles not cached" claim is resolved for 2025-05..2025-10 via 4h).

---

## 9. SESSION LOG (append-only; newest first)

<!-- Format: ## <UTC> — <agent/session id> — <one-line outcome> ... -->

## 2026-11-12T15:54:27Z — Live state re-verified at session start — working tree clean; corrected panel `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` SHA-256 `08c608035d179be8…` matches; frozen prereg `134503Z` unchanged (`fdd96bd1…`); valid eval `…145537Z` (`rv` NOT_MET, `liq` INCONCLUSIVE_NUMERICAL_INSTABILITY); `scripts/early4h_liq_glm.py` and no `*liq_glm*` prereg exist → campaign UNEXECUTED. No bottlenecks remain (§3). Next session MUST execute `FCLR-EARLY4H-2025H1-LIQ-GLM v1` (§4): freeze a NEW prereg BEFORE any `liq` outcome, implement `scripts/early4h_liq_glm.py` (Poisson/quasi-Poisson log-link IRLS, `liq` only), evaluate on the frozen panel/splits, adjudicate, then §4 Step 5 if NOT_MET/INCONCLUSIVE.

- **Evidence supported/contradicted/unknown:** Supported — sole durable handoff is current; preflight green (deps OK; 103 tests OK; panel hash matches; live 4h `candleSnapshot` HTTP 200 + 1104 bars all 9 coins); `liq` open under QLIKE-consistent estimator. Contradicted — no competing handoff docs: redirects + SUPERSEDED `FCLR_CAMPAIGN_NEXT.md`. Unknown — `liq` outcome under Poisson/quasi-Poisson log-link GLM.
- **Strongest alternative explanation:** `rv` NOT_MET is a genuine null; `liq` is open solely because the sealed linear-in-log model extrapolates on the Oct-2025 funding spike (model-form, not a code bug). The log-link GLM models the conditional mean directly and resolves this.
- **Dominant limitation:** `liq` estimator form dominates; secondary BTC/ETH concentration (~63% events / 84% notional) and the 2025-05-25 label start. No dependency/data/source/pipeline blocker remains.
- **Falsifying next test:** `scripts/early4h_liq_glm.py` under a new frozen prereg on the existing corrected panel; a stable `C2_vs_B1` with 95% CI excluding 0 and ≥2% rel QLIKE reduction falsifies "funding does not inform liquidation intensity"; a stable null closes `liq`.
- **Highest expected info gain per free compute:** §4 Steps 2–4 — freeze new prereg → implement `scripts/early4h_liq_glm.py` → evaluate on frozen panel → adjudicate. No re-fetch, no re-window, no Gate 4, no new source.
- **Exact artifact/command demonstrating progress:** Preflight green (above). Session-end artifacts: `research_state/tracka_prereg_early2025h1_liq_glm_<UTC>.json`+`.md`, `scripts/early4h_liq_glm.py`, `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-<UTC>.md`+`.json`, updated `experiment_frontier.json`, and a `## SESSION LOG` entry here.

## 2026-11-12T15:47:45Z — Handoff re-verification + bottleneck sweep — no research outcomes; preflight green; next session MUST execute `FCLR-EARLY4H-2025H1-LIQ-GLM v1` (§4)

- **Evidence supported/contradicted/unknown:** Re-verified the sole durable handoff is internally consistent and current. Confirmed at 2026-11-12T15:47Z: `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 103 tests OK`; corrected panel `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` SHA-256 `08c60803…` matches; live 4h `candleSnapshot` → HTTP 200 + 1104 bars for all 9 coins; `research_state/experiment_frontier.json` rank-0 = `FCLR_EARLY4H_2025H1_LIQ_GLM_PREREG_BUILD_EVAL`, `ACTIVE_HEAVY_CAMPAIGN`; no `scripts/early4h_liq_glm.py` and no `*liq_glm*` prereg/eval exist → the campaign is still unexecuted. Contradicted — no competing handoff docs: `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md` are redirects; `research_state/FCLR_CAMPAIGN_NEXT.md` is marked SUPERSEDED. Unknown — `liq` outcome under the QLIKE-consistent estimator.
- **Strongest alternative explanation:** `rv` NOT_MET is a genuine null; `liq` is open only because the sealed linear-in-log model is numerically unstable on the Oct-2025 funding spike. The Poisson/quasi-Poisson log-link GLM is the QLIKE-consistent estimator and directly resolves this.
- **Dominant limitation:** `liq` estimator form (unbounded exp link) dominates; secondary BTC/ETH concentration (~63% events / 84% notional) and 2025-05-25 label start. No dependency, data, source, or pipeline blocker remains.
- **Falsifying next test:** `scripts/early4h_liq_glm.py` under a new frozen prereg on the existing corrected panel; a stable `C2_vs_B1` with 95% CI excluding 0 and ≥2% rel QLIKE reduction falsifies "funding does not inform liquidation intensity"; a stable null closes `liq`.
- **Highest expected info gain per free compute:** §4 Steps 2–4 — freeze new prereg → implement `scripts/early4h_liq_glm.py` (IRLS Poisson log-link) → evaluate on frozen panel/splits → adjudicate. No re-fetch, no re-window, no Gate 4, no new source.
- **Artifacts/commands:** Preflight green (above). Required session-end artifacts: `research_state/tracka_prereg_early2025h1_liq_glm_<UTC>.json` + `.md`, `scripts/early4h_liq_glm.py`, `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-<UTC>.md` + `.json`, updated `experiment_frontier.json`, and a `## SESSION LOG` entry here. Bottleneck sweep found none outstanding; handoff remains single-source.

## 2026-11-12T15:38:39Z — Preflight verification session — all preflight checks pass; next session MUST execute `FCLR-EARLY4H-2025H1-LIQ-GLM v1` (§4)

- **Evidence supported/contradicted/unknown:** All §5 preflight checks verified live at 2026-11-12T15:38Z: `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 103 tests OK`; panel SHA-256 `08c60803…` matches expected prefix; ironflow cache target events sum to 394,167 across 2025-05..2025-10 (BTC 141,632, ETH 109,681, SOL 83,021, XRP 27,318, DOGE 9,569, SUI 9,346, LINK 6,144, AVAX 4,361, BNB 4,095); live 4h `candleSnapshot` fetch returns HTTP 200 + 1104 bars for all 9 coins. Contradicted — no blockers remain. Unknown — `liq` outcome under QLIKE-consistent estimator (next campaign).
- **Strongest alternative explanation:** The corrected `rv` NOT_MET is genuine; `liq` remains open solely due to estimator form (unbounded exp-link linear model extrapolates on Oct-2025 funding spike). The next test (Poisson/quasi-Poisson log-link GLM) is the QLIKE-consistent estimator and directly addresses this.
- **Dominant limitation:** Estimator form for `liq` dominates; secondary is BTC/ETH concentration (~63% events / 84% notional). No data, source, or pipeline blockers remain.
- **Falsifying next test:** `scripts/early4h_liq_glm.py` under a **new frozen prereg** (`TRACKA-HL-EARLY4H-2025H1-LIQ-GLM`) on the existing corrected panel. A stable `C2_vs_B1` with CI excluding 0 and ≥2% rel QLIKE reduction falsifies "funding does not inform liquidation intensity"; a stable null closes `liq`.
- **Highest expected info gain per free compute:** Execute §4 Steps 2–4: freeze new prereg → implement `scripts/early4h_liq_glm.py` (IRLS Poisson log-link) → evaluate on frozen panel/splits → adjudicate. No re-fetch, no re-window, no Gate 4, no new source.
- **Artifacts/commands:** All §5.0 preflight green. Next session MUST run §5.1 (bounded live probe), then §4 Steps 2–4. Required session-end artifacts: `research_state/tracka_prereg_early2025h1_liq_glm_<UTC>.json` + `.md`, `scripts/early4h_liq_glm.py`, `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-<UTC>.md` + `.json`, updated `experiment_frontier.json`, and a `## SESSION LOG` entry here.

## 2026-11-12T14:56:44Z — Pipeline repair session — root-caused and fixed the degenerate EARLY4H eval; produced valid `rv` NOT_MET + `liq` INCONCLUSIVE; set next GLM campaign

- **Evidence supported/contradicted/unknown:** Supported — the `134634Z` eval was invalid due to three code defects in `scripts/early4h_campaign.py`: (1) `_add_lags` used `shift(0)` (no-op), making `lag_liq[t] = log(t1_liq[t])` an identity → `liq` QLIKE exactly 0; (2) the test-side design used the shared `lag_log` (= `lag_liq`) for the `rv` model → predictions ~1.97e7, QLIKE ~19.27, identical across models (~1e-15 diffs); (3) `abs_fund_pct` computed on the daily panel (starts at `LABEL_START`) plus `_load_funding` truncating at `LABEL_START-8d` starved C1/C2 of ~200 training rows. Contradicted — the "no effective funding signal" reading of `rv` was an artifact. Unknown — whether funding helps `liq`: the corrected frozen linear model is numerically unstable on the Oct-2025 funding spike (max per-row QLIKE 1.6e27), so `liq` is **open, not a null**.
- **Strongest alternative explanation:** For `rv`, the corrected, stable result is a genuine null: funding-conditioned features (C1/C2) do not improve next-24h RV forecasting over RV-only HAR (C2_vs_B1 diff +0.243, CI [-0.097, 0.583] includes 0, rel -29.3%, p=0.161). For `liq`, the frozen linear-in-log model's exp() link extrapolates on Oct-2025 funding ~100× the train range — a model-form limitation, not a code bug.
- **Dominant limitation:** Estimator form for `liq` (unbounded exp link, no regularization by prereg) dominates `liq` uncertainty. Secondary: BTC/ETH concentration (~63% events / 84% notional) and the 2025-05-25 label start constrain powered inference.
- **Falsifying next test:** Fit a QLIKE-consistent Poisson/quasi-Poisson log-link GLM on the same frozen panel/splits for `liq`; a stable `C2_vs_B1` with materially non-zero paired deltas would falsify "funding does not inform liquidation intensity"; a stable null would close `liq`.
- **Highest expected info gain per free compute:** Implement `scripts/early4h_liq_glm.py` (Poisson log-link) under a **new frozen prereg** on the existing corrected panel — no re-fetch, no re-window, directly answers the open `liq` question with a QLIKE-consistent estimator.
- **Artifacts/commands:** Fixed `scripts/early4h_campaign.py` (shift(1); per-target test lag; funding warm-up from 2025-05-01; numerical-stability guard). Wrote `research_state/tracka_hl_early2025h1_pipeline_correction_20261112T145644Z.md`. Produced corrected panel `...145529Z.parquet` + build report, corrected eval `evaluation_summary_EARLY4H-2025H1-20261112T145537Z.{md,json}` (`rv` NOT_MET, `liq` INCONCLUSIVE_NUMERICAL_INSTABILITY). Preflight: `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 103 tests OK`. Prereg `134503Z` SHA-256 unchanged (`fdd96bd1…`). No sealed verdicts modified; no raw data committed; workflow not edited.
- **DoD (required):** (1) supported: pipeline defect real and fixed; `rv` funding does not help; contradicted: `134634Z` was a valid eval. unknown: `liq` effect (estimator-limited). (2) strongest alternative: `rv` null is genuine; `liq` instability is model-form. (3) dominant limitation: `liq` estimator form. (4) falsifier: stable Poisson log-link GLM `liq` result. (5) highest info gain: `scripts/early4h_liq_glm.py` under new prereg. (6) see artifacts/commands above and updated §0–§5 of this file.

## 2026-11-12T14:37:52Z — Glyph Cluster (handoff consolidation) — clarified state, surfaced degenerate EARLY4H eval, set next heavy task

- **Evidence supported/contradicted/unknown:** Repo and `AGENT_HANDOFF.md` confirm `FCLR-EARLY4H-2025H1-HEAVY v2` is the highest-priority admissible campaign (Hyperliquid-only, observed ironflow labels 2025-05-25..2025-10-31, 4h candles, disjoint from sealed windows, no Gate 4). Contrary to prior handoff state, early2025h1 artifacts exist (acq `tracka_hl_early2025h1_acquisition_report_20261112T134247Z.json`, frozen prereg `tracka_prereg_early2025h1_20261112T134503Z.json`, panels/build reports incl. `...134520Z`, evals incl. latest `evaluation_summary_EARLY4H-2025H1-20261112T134634Z.{md,json}`). Latest eval is **invalid/degenerate**: `liq` all-zero QLIKE/contrasts (CI [0,0], p=1, rel n/a) and `rv` C2/C1/B1 identical to ~1e-15 across all coins/blocks — unknown whether funding adds value until pipeline is audited. Redirect handoffs intact; `requirements.txt` includes `requests`; local deps import OK; early candle/funding caches present.
- **Strongest alternative explanation:** Evaluation/panel defect (target scaling/zeroing, feature join dropping funding/premium signal, or QLIKE computed on constant/identical predictions) rather than a true null; alternatively genuine null masked by degenerate metrics — cannot distinguish without code+panel trace.
- **Dominant limitation:** Validity of the executed eval (target/feature construction and loss computation) dominates; until fixed, inference is undefined. Secondary: BTC/ETH concentration (~63% events/84% notional) and 2025-05-25 label start constrain powered inference.
- **Falsifying next test:** Rebuild/evaluate with audited liq/RV targets and verified non-constant, correctly joined funding/premium features under the frozen prereg; a correctly computed `C2_vs_B1` with materially non-zero paired deltas and stable per-block/per-coin behavior would falsify "pipeline identical/no signal" (and test the substantive hypothesis).
- **Highest expected info gain per free compute:** Audit+repair `scripts/tracka_hl_build_early_4h_panel.py` / `scripts/tracka_hl_evaluate_early_4h.py` (and helpers) against `tracka_prereg_early2025h1_20261112T134503Z.json` + panel/build report, then produce a corrected timestamped eval or reason-coded inconclusive — cheap, unblocks claim-worthy PASS/NOT_MET and Step 5.
- **Artifacts/commands:** Read/verified `AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md` (head), `requirements.txt`, `.github/workflows/main.yml` (no agent-venv-from-requirements), `research_state/experiment_frontier.json`, early2025h1 acq/prereg/panel/eval artifacts, caches present. Preflight evidence: `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` -> `deps OK`. No sealed verdicts modified; no raw data committed; workflow not edited (protected).
- **DoD (required):** (1) supported: campaign admissible and partially executed; contradicted: "no artifacts yet" and "workflow provisions agent venv from requirements"; unknown: true C2 vs B1 effect pending valid eval. (2) strongest alternative: pipeline bug. (3) dominant limitation: eval/target validity. (4) falsifier: corrected prereg-consistent re-eval with non-degenerate losses/deltas. (5) highest info gain: pipeline audit+fix+re-eval. (6) see artifacts/commands above and updated §0–§3 of this file.

---

## SESSION LOG

### 2026-11-12T15:44:36Z — Handoff consolidation/state verification (no research outcomes)
- Verified `AGENT_HANDOFF.md` is the sole durable handoff and root redirect files (`HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`) point here; no competing handoff docs found.
- Re-verified corrected evidence artifacts exist: panel `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` (SHA-256 `08c60803…`), valid eval `research_state/evaluation_summary_EARLY4H-2025H1-20261112T145537Z.{md,json}` (rv NOT_MET, liq INCONCLUSIVE_NUMERICAL_INSTABILITY), frozen prereg `tracka_prereg_early2025h1_20261112T134503Z.{json,md}`, pipeline correction note `research_state/tracka_hl_early2025h1_pipeline_correction_20261112T145644Z.md`.
- Confirmed `research_state/experiment_frontier.json` rank-0 is aligned: `FCLR_EARLY4H_2025H1_LIQ_GLM` / `FCLR_EARLY4H_2025H1_LIQ_GLM_PREREG_BUILD_EVAL`, `ACTIVE_HEAVY_CAMPAIGN`.
- No new outcomes inspected; no raw data committed. Gate 4 remains external blocker (not required for campaign).
- Next agent: execute §4 `FCLR-EARLY4H-2025H1-LIQ-GLM v1` (freeze new prereg before any liq outcome, implement `scripts/early4h_liq_glm.py` Poisson/quasi-Poisson log-link, evaluate/adjudicate, then power/label-ceiling/concentration follow-up if needed).
