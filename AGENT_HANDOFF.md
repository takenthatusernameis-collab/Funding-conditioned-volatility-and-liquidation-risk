# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T12:34:20Z
**This file is the ONLY durable handoff.** It supersedes `HANDOFF_NEXT_SESSION.md` @ 2026-11-12T11:38:00Z, the 2026-11-12T09:51:12Z "clean stop", and every earlier checkpoint.
**Update this file in place** (append a dated `## SESSION LOG` entry). Do **not** create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are now short redirects to this file.

---

## 0. IMMEDIATE FIRST ACTION (do this now, in order)

1. Read only this file. Do not re-derive the prior "clean stop"; it was wrong.
2. Run the preflight in §5.0. If a dependency is missing, install it; if data is missing, fetch it. Do not declare a clean stop from a missing local cache.
3. Execute campaign **`FCLR-EARLY4H-2025H1-HEAVY v2`**, Steps 1–4, in §4. Then continue to Step 5 if the primary is negative.

The work is admissible, unclaimed, disjoint from every sealed window, and requires **no** Gate 4, **no** new source, and **no** post-2026-10-31 data. The only reason it has not been done is that prior sessions kept rewriting the handoff instead of executing it.

---

## 1. WHY THIS IS THE HIGHEST-PRIORITY WORK (inferred from the repository name)

`Funding-conditioned-volatility-and-liquidation-risk` →
- **P1 — funding-conditioned volatility forecasting** (primary).
- **P2 — observed liquidation risk** (co-primary on the same panel).
- **P3 — modeled boundary breaches** (only after P1/P2 are exhausted).

A session is successful only if it produces **heavy, claim-advancing evidence** or a **timestamped, evidenced terminal stop** with the exact failing minima. Status-only output, re-probing already-assessed sources, cosmetic edits, and handoff churn are banned.

---

## 2. VERIFIED EVIDENCE (re-verified live 2026-11-12T12:34Z, no outcomes inspected)

| Input | Coverage | Source | Prior use |
|---|---|---|---|
| Observed liquidation labels | **2025-05-25 .. 2025-10-31**; 9 target coins; **394,167 events / $23.4B notional** (all 192 markets: 679,487 events) | `research_state/data_cache/ironflow_events/2025-05.parquet … 2025-10.parquet` (cached, CC BY 4.0) | **NONE** — never a target of any experiment |
| 4h candles (RV/features) | **2025-05-01 .. 2025-10-31, 1104 bars/coin, 0 internal gaps**, all 9 coins | live `candleSnapshot` `interval=4h`, unauthenticated, ~0.34 s/call | never fetched for this window |
| Funding history (hourly) | **2025-05-01 .. 2025-10-31, ~4416 rows/coin**, paginated at 500 (9 pages); filter `endTime` client-side | live `fundingHistory`, unauthenticated | cached funding starts 2025-11 only |

**Per-coin label counts (target 9):** BTC 141,632 ($11.32B), ETH 109,681 ($8.42B), SOL 83,021 ($2.49B), XRP 27,318 ($0.64B), DOGE 9,569 ($0.32B), SUI 9,346 ($0.12B), LINK 6,144 ($0.12B), AVAX 4,361 ($0.12B), BNB 4,095 ($0.04B).

**Critical correction to the 11:38Z handoff:** the figures "1.13M events / $32.3B / 6 blocks" were wrong. The real target-coin totals are **394,167 events / $23.4B**, and labels **start 2025-05-25**, so the powered window is **2025-05-25..2025-10-31 = 5 complete 30-day blocks (Jun–Oct) + a 7-day May ramp**. Do not reuse the 11:38Z numbers.

**Concentration hazard:** BTC+ETH are **~63% of events and ~84% of notional**. The evaluation must report per-coin results and must reject any PASS that is driven by a single coin or block.

**Why earlier work missed this window:** prior probes used **1h** candles, which Hyperliquid serves only from **2026-04-18**. The `4h` interval serves back to **2024-08-01**. The `4h` window 2025-05..2025-10 was never fetched or tested. The 2025-11..2026-04 `4h` pilot was `INCONCLUSIVE_PILOT_SHORTFALL` (only 2 complete blocks); its negative C2 result is **not** evidence against the new, powered window.

**No campaign artifacts exist yet.** `find research_state -iname '*early2025h1*'` returns nothing. This is unclaimed work.

**Gate 4 Branch 1 trigger: ABSENT.** Only `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` and `..._UNRESOLVED_20261108T204000Z.json` exist. The literal string `RESOLVED_VERIFIED` inside `fclr020_gate4_readiness_action_matrix_latest.json` is a readiness matrix, **not** a trigger. Do not wait, poll, or whole-tree grep for it.

**`run_manifest.json` is an unresolved Git LFS pointer in CI.** Do not read it as JSON and do not make the campaign depend on it. Write the campaign prereg and state files directly.

---

## 3. BOTTLENECKS REMOVED THIS SESSION

| Bottleneck | Resolution |
|---|---|
| **Four competing handoff docs** (`AGENT_HANDOFF.md`, `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`) | Consolidated: **this file is the sole durable handoff**; the other three are short redirects. |
| **False "dependencies fixed" claim** — `requirements.txt` lacked `requests` and the workflow never installed `requirements.txt`; agents hit `ModuleNotFoundError: pandas/pyarrow` in 22+6+12+6 logged runs | **Actually fixed:** `requests` added to `requirements.txt`; `.github/workflows/main.yml` now provisions `$RUNNER_TEMP/agent-venv` from `requirements.txt` and prepends it to `PATH` before the Kilo agent loop. |
| **Wrong window arithmetic** (May labels start 05-25, not 05-01; BTC/ETH concentration) | Corrected in §2; campaign uses 5 complete Jun–Oct blocks + May ramp and mandates per-coin reporting. |
| **LFS pointer read as JSON** | Campaign must not read `run_manifest.json`; write its own prereg/state. |
| **No executable start** | §5 gives exact preflight, acquisition, prereg, build, and evaluation commands/artifacts. |

Do not re-diagnose the dependency wall, re-probe 1h candles, re-run alt-source discovery, or reopen sealed verdicts.

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR-EARLY4H-2025H1-HEAVY v2`

**Objective:** the first powered, pre-registered test of funding-conditioned features vs an RV-only baseline on the untouched 2025-05-25..2025-10-31 Hyperliquid panel, for **both** Track A (observed liquidation intensity) and Track C-style volatility.

**Do NOT** inspect any outcome before the prereg is frozen. **Do NOT** reuse a sealed holdout. **Do NOT** tune, threshold-shop, or expand the feature grid after the freeze.

### Step 1 — Bounded acquisition + provenance (no outcomes)
- Fetch `4h` `candleSnapshot` for `AVAX BNB BTC DOGE ETH LINK SOL SUI XRP` over **2025-05-01 .. 2025-11-01**, monthly, unauthenticated. Expect **1104 in-window bars/coin** (drop any bar with `t >= endTime`).
- Fetch `fundingHistory` for the same coins/window, paginate at 500, filter to `2025-05-01T00:00:00Z .. 2025-10-31T23:59:59Z` client-side (~4416 rows/coin).
- Cache under `research_state/data_cache/hyperliquid_candles_4h_early/<COIN>/<YYYY-MM>.json` and `research_state/data_cache/hyperliquid_funding_early/<COIN>.json` with `.sha256` + `.accessed.json` sidecars.
- Emit `research_state/tracka_hl_early2025h1_acquisition_report_<UTC>.json`: endpoint, params, HTTP status, rows, first/last ms, per-month bar counts, gaps, unauthenticated/no-key/no-requester-pays status, per-file SHA-256.
- Use `scripts/tracka_hl_fetch_candles_early_4h.py` and `scripts/tracka_hl_expansion_funding_paginate.py` as **templates**; parameterize the window (their `MONTHS`/`END_MS` are hard-coded to 2025-11..2026-04). Do not duplicate them.

### Step 2 — Freeze prereg BEFORE any outcome computation
Write `research_state/tracka_prereg_early2025h1_<UTC>.json` + `.md`, declaring **ex ante**:
- **Window:** labels 2025-05-25T00:00:00Z .. 2025-10-31T23:59:59Z; **5 complete non-overlapping 30-day blocks with boundaries frozen in the prereg inside 2025-06-01..2025-10-31**, plus May 25–31 as a ramp/partial block (not a test block).
- **Universe:** the 9 named coins, selected by name rule before outcomes; no survivor substitution.
- **Unit:** coin × 24h UTC bucket.
- **Targets (declare both, distinct families):** (a) Track A — next-24h observed liquidation intensity, notional-weighted; (b) Track C-style — next-24h realized variance (4h-based RV24h/RV168h).
- **Models, frozen:** B0 persistence; B1 RV-only HAR(log RV4h, log RV24h, log RV168h); C1 = B1 + signed funding + 90-d trailing abs-funding percentile (≥30 obs); C2 = C1 + mark/index premium + mark/EMA24 distance. Epsilon 1e-12. Training-only standardization. **No regularization, no model search, no tuning.**
- **Primary contrast:** `C2_vs_B1`. Secondary: `C1_vs_B1`, `C2_vs_C1`.
- **Metric:** QLIKE (lower better) on paired OOS.
- **Splits:** train / val / ≥3 complete non-overlapping 30-d test blocks with ≥7-d embargo.
- **Inference:** block bootstrap over complete 30-d UTC blocks, ≥2000 reps, fixed seed. Holm correction across the **full declared family**.
- **Materiality floor:** ≥2% relative QLIKE reduction AND 95% CI upper bound < 0.
- **Minima:** ≥5 paired instruments; ≥3 test blocks.
- **Missingness:** missing stays missing; no forward fill; no synthetic labels.
- Set `pre_registered_before_outcomes: true`, `frozen_before_outcomes: true`. Record the JSON SHA-256.

### Step 3 — Build panel deterministically
- Emit `research_state/tracka_hl_early2025h1_panel_<UTC>.parquet` + `..._panel_build_report_<UTC>.json` with input hashes, per-coin coverage, missingness, row counts before/after every filter, reason-coded exclusions.
- Assert leakage guards: target never overlaps splits after purge/embargo; funding publication/settlement time and sign correct; mark/index alignment within the pre-registered tolerance.

### Step 4 — Evaluate and adjudicate
- Emit `research_state/evaluation_summary_EARLY4H-2025H1-<UTC>.md` (+ `.json`): per-model QLIKE, paired `C2_vs_B1` Δ with CI, relative reduction, per-block and per-coin breakdown, calibration, Holm-adjusted p-values, and an explicit **PASS / NOT_MET** verdict with reasons.
- **If PASS:** update `experiment_frontier.json` and `hypothesis_registry.json` atomically under the **new** experiment ID; write `research_state/final_confirmatory_verdict_early2025h1_<UTC>.md`. Do not modify sealed records or `run_manifest.json`.
- **If NOT_MET:** preserve the null honestly, report it, then continue to Step 5 — do not stop.

### Step 5 — If Step 4 is negative, immediately continue
1. **Power/coverage audit** on the 2025-05-25..2025-10-31 panel: per-coin event adequacy, which blocks carry signal, and whether a pre-registered *sub-cohort* (e.g. top-5 by label activity, frozen ex ante) is powered for a secondary confirmatory.
2. **2024-08..2025-04 extension feasibility:** 4h candles reach 2024-08-01 and funding paginates from 2024-08, but **ironflow labels do not exist before 2025-05** — document this as a hard label ceiling; do not fabricate or proxy it.
3. **Track C volatility on the same panel** if not already covered by Step 4(b).
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
- `research_state/tracka_hl_early2025h1_acquisition_report_<UTC>.json`
- `research_state/tracka_prereg_early2025h1_<UTC>.json` + `.md` (frozen before outcomes)
- `research_state/tracka_hl_early2025h1_panel_<UTC>.parquet` + `..._panel_build_report_<UTC>.json`
- `research_state/evaluation_summary_EARLY4H-2025H1-<UTC>.md` + `.json`
- updated `research_state/experiment_frontier.json` and a `## SESSION LOG` entry in this file

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
