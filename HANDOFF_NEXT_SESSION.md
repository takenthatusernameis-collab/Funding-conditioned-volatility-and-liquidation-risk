# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T11:38:00Z (supersedes ALL prior handoffs/checkpoints; this file is the sole durable handoff)
**Supersedes:** `HANDOFF_NEXT_SESSION.md` @ 2026-11-12T09:51:12Z and every earlier checkpoint.
**Prior handoff verdict:** "timestamped evidenced clean stop" — **OVERTURNED this session.** That stop was arithmetically wrong. A previously unnoticed admissible window exists and was never claimed by any experiment. Evidence below.

---

## 0. THE FINDING THAT REOPENS THE PROGRAM (read this first)

**A powered, never-used, fully-admissible Hyperliquid panel exists: 2025-05-01 .. 2025-10-31.**

Verified this session (2026-11-12, live, unauthenticated, no outcomes inspected):

| Input | Coverage | Source | Prior use |
|---|---|---|---|
| Observed liquidation labels | **2025-05..2025-10, 9 coins, 1.13M events, $32.3B notional** | `research_state/data_cache/ironflow_events/2025-05.parquet … 2025-10.parquet` (cached, CC BY 4.0) | **NONE — never a target of any experiment** |
| 4h candles (RV/features) | **2025-05-01 .. 2025-10-31, 1104 bars/coin, 0 internal gaps, 180-186 bars/month** | live `candleSnapshot` interval=`4h` (fetchable, ~0.34 s/call) | never fetched for this window |
| Funding history (hourly) | **2025-05-01 .. 2025-10-31, 4416 rows/coin (9 pages)** | live `fundingHistory`, paginates at 500 rows (9 pages) | cached funding starts 2025-11 only |

**Why every earlier conclusion missed it:** all prior work probed **1h** candles, which Hyperliquid serves only from **2026-04-18** onward. The `4h` interval serves back to **2024-08-01**. The prior "candles absent before 2026-04" conclusion is true only for `1h`. The `4h` interval was used once (early-4h campaign) but only on 2025-11..2026-04 — **2025-05..2025-10 was never examined.**

**This window is ~6 months = 6 non-overlapping 30-day blocks** (3 required), 9 instruments (5 required), with observed labels + computable RV + funding. It is disjoint from every sealed window (2026-05..2026-10, 2025-11..2026-04, 2024 Binance). It requires **no** Gate 4, **no** new external source, **no** post-2026-10-31 data.

Repo priority P1 (funding-conditioned volatility) and P2 (observed liquidation risk) are both actionable on it. **This is the heavy work. Execute it.**

---

## 1. REPO-PRIORITY P0 (inferred from repository name)
`Funding-conditioned-volatility-and-liquidation-risk` → **(1) funding-conditioned volatility forecasting, (2) observed liquidation risk, (3) modeled boundary breaches.** Every session produces **heavy, claim-advancing work** or a **timestamped evidenced clean stop**. Status-only output, polling, re-probes of already-assessed sources, and cosmetic edits are banned.

---

## 2. VERIFIED STATE (single source of truth; re-verified 2026-11-12T11:38Z)

- **Gate 4 Branch 1 trigger: ABSENT.** `research_state/fclr016_local_audit/` holds only `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` and `..._UNRESOLVED_20261108T204000Z.json`. No `*RESOLVED*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. Agent cannot create/attest/fabricate/bypass. **Do not wait or poll.**
- **Ironflow labels:** 18 monthly parquets cached, 2025-05..2026-10; **no post-2026-10-31 labels** (HF `lastModified` 2026-11-07T10:18:25Z). Do not re-probe without new evidence.
- **HL 2026-11 forward edge:** ~12 d — far below the 100 d reprobe threshold and the 90 d needed for 3×30d blocks. **Not eligible. Do not poll.**
- **Alt-source discovery:** complete. `research_state/alt_source_scan_latest.json` (22 candidates) + `alt_source_deep_review_latest.md` (14 probes) → **no new GO**. `ironflow/hyperliquid-liquidations` (CC BY 4.0) is the only admissible Track A source and it is exhausted for *post-2026-10* work. **Do not rerun** `hunt_alternative_liquidation_sources.py` / `deep_review_alt_sources.py` without a materially new unassessed candidate.
- **Sealed / do not reopen, relitigate, or retune:** Track C ALL NOT_SUPPORTED (FCLR-001/002/003/006/007; dossier `track_c_consolidated_dossier.md`), H001 NOT_SUPPORTED, risk overlay INELIGIBLE. Track A: 9-symbol 2026-05..2026-10 NOT_MET; early 2025-11..2026-04 INADMISSIBLE (1h) then `INCONCLUSIVE_PILOT_SHORTFALL` (4h, only 2 blocks); expansion PASS but robustness FRAGILE (LOIO 4/8 need ≥6; placebo/permutation FAIL). Track B ALL NOT_SUPPORTED/NOT_SUPPORTED_DEGENERATE. H2 `H2_shek_replication` EXPLORATORY_ONLY/PARTIAL.
- **Frontier:** `research_state/experiment_frontier.json` — this campaign supersedes the stale rank-0 entry.
- **Tests:** `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → 103 tests OK (2026-11-12T11:36Z).

### Known hazard: the `RESOLVED_VERIFIED` string is a false positive
`research_state/fclr020_local_audit/fclr020_gate4_readiness_action_matrix_latest.json` **contains the literal string `RESOLVED_VERIFIED`**. It is a readiness/planning matrix, **not** a Gate 4 trigger. Gate 4 triggers **only** on a file matching `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all 8 fields, `fabricated=false`, and human/legal attestation. Do not grep the whole tree and conclude Gate 4 fired.

---

## 3. BOTTLENECKS AND THEIR REMOVAL

| Bottleneck | Agent-removable? | Resolution / trigger |
|---|---|---|
| **Prior handoff declared a clean stop while admissible data existed** | **YES — REMOVED** | This finding (§0) supersedes it. 2025-05..2025-10 is admissible and unclaimed. |
| **Ambiguous/wrong window from "1h only" probing** | **YES — REMOVED** | 4h candles reach 2024-08-01; documented in §0. Never probe 1h to conclude "no early data." |
| **Three redundant redirect docs + stale checkpoint churn** | **YES — REMOVED** | `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md` are now **stale pointers to the 09:51 handoff** — superseded by this file. Do not follow them. |
| **CI worker lacks `pandas`/`pyarrow`/`scipy`** | **YES — fixed** | `requirements.txt` now includes `pyarrow`. Worker bootstrap installs `requirements.txt`. 22 `pandas` + 6 `pyarrow` ModuleNotFoundErrors in the diagnostics ledger were caused by this; see §6. |
| **Gate 4 Branch 1 (Binance terms)** | No (external/legal) | Valid RESOLVED trigger → execute Branch 1 immediately. Otherwise irrelevant to this campaign. |
| **HL post-2026-10-31 forward depth** | No (time) | HL ≥100 d AND verified post-2026-10-31 observed labels → bounded probe. Until then, not applicable. |

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR-EARLY4H-2025H1-HEAVY` (execute in strict order)

**Objective:** the first powered, pre-registered test of funding-conditioned features vs RV-only baseline on the untouched 2025-05..2025-10 Hyperliquid panel — for **both** Track A (observed liquidation intensity) and Track C-style volatility target (repo priority P1).

**Do NOT** inspect any outcome before the prereg is frozen. **Do NOT** reuse any sealed holdout. **Do NOT** tune, threshold-shop, or expand the feature grid post-freeze.

### Step 1 — Bounded acquisition + provenance (no outcomes)
- Fetch `4h` `candleSnapshot` for the 9 coins (`AVAX BNB BTC DOGE ETH LINK SOL SUI XRP`) over **2025-05-01 .. 2025-11-01**, monthly, unauthenticated (~102 calls; one call returns the whole window at ~0.34 s, so per-month calls are for provenance granularity). Expect 1104 in-window bars/coin (the endpoint also returns a terminal bar at exactly `endTime`; drop bars `>= endTime`).
- Fetch `fundingHistory` for the same coins over the same window (paginate at 500; 9 pages/coin, 4416 in-window rows).
- Cache under `research_state/data_cache/hyperliquid_candles_4h_early/<COIN>/<YYYY-MM>.json` with `.sha256` + `.accessed.json` sidecars (match existing layout).
- Emit `research_state/tracka_hl_early2025h1_acquisition_report_<UTC>.json`: endpoint, params, HTTP status, rows, first/last ms, per-month bar counts, gaps, unauthenticated/no-key/no-requester-pays/signature status, per-file SHA-256.
- Reuse `scripts/tracka_hl_fetch_candles_early_4h.py` and `scripts/tracka_hl_expansion_funding_paginate.py` as templates; do not duplicate them.

### Step 2 — Freeze prereg BEFORE any outcome computation
Write `research_state/tracka_prereg_early2025h1_<UTC>.json` + `.md` (use `scripts/create_forward_prereg.py`), declaring **ex ante**:
- **Window:** 2025-05-01T00:00:00Z .. 2025-10-31T23:59:59Z (6 non-overlapping 30-d blocks).
- **Universe:** the 9 named coins, selected by name rule *before* outcomes; no survivor substitution.
- **Unit:** coin × 24h UTC bucket.
- **Targets (declare both, distinct families):** (a) Track A — next-24h observed liquidation intensity, notional-weighted; (b) Track C-style — next-24h realized variance (4h-based RV24h/RV168h).
- **Models, frozen:** B0 persistence; B1 RV-only HAR(log RV1h, log RV24h, log RV168h); C1 = B1 + signed funding + 90-d trailing abs-funding percentile (≥30 obs); C2 = C1 + mark/index premium + mark/EMA24 distance. Epsilon 1e-12. Training-only standardization. **No regularization, no model search, no tuning.**
- **Primary contrast:** `C2_vs_B1`. Secondary: `C1_vs_B1`, `C2_vs_C1`.
- **Metric:** QLIKE (lower better) on paired OOS.
- **Splits:** train / val / ≥3 non-overlapping 30-d test blocks with ≥7-d embargo.
- **Inference:** block bootstrap over complete 30-d UTC blocks, ≥2000 reps, fixed seed. Holm correction across the **full declared family**.
- **Materiality floor:** ≥2% relative QLIKE reduction AND 95% CI upper bound < 0.
- **Minima:** ≥5 paired instruments; ≥3 test blocks.
- **Missingness:** missing stays missing; no forward fill; no synthetic labels.
- Set `pre_registered_before_outcomes: true`, `frozen_before_outcomes: true`. Record the JSON SHA-256.

### Step 3 — Build panel deterministically
- Emit `research_state/tracka_hl_early2025h1_panel_<UTC>.parquet` + `..._panel_build_report_<UTC>.json` with input hashes, per-coin coverage, missingness, row counts before/after every filter, reason-coded exclusions.
- Assert leakage guards: target never overlaps splits after purge/embargo; funding publication/settlement time and sign correct; mark/index alignment within pre-registered tolerance.

### Step 4 — Evaluate and adjudicate
- Emit `research_state/evaluation_summary_EARLY4H-2025H1-<UTC>.md` (+ `.json`): per-model QLIKE, paired C2_vs_B1 Δ with CI, relative reduction, per-block and per-coin breakdown (skill must not be dominated by one coin/venue/block), calibration if any probability forecast, Holm-adjusted p-values, and an explicit gate verdict **PASS / NOT_MET** with reasons.
- **If PASS:** update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically under the **new** experiment ID. Sealed records untouched.
- **If NOT_MET:** preserve the null honestly. Report it. Then continue to Step 5 — do not stop.

### Step 5 — If Step 4 is negative, immediately continue
Per `RESEARCH_PROMPT.md` §16, a negative primary does not end the program. Continue in the same session with the **next** unblocked task, in this order:
1. **Power/coverage audit** on the 2025-05..2025-10 panel: which coins/blocks carry the signal, event-adequacy per coin-month, and whether a pre-registered *sub-cohort* (e.g. top-5 by label activity, frozen ex ante) is powered for a secondary confirmatory.
2. **2024-08..2025-04 extension feasibility** (4h candles reach 2024-08-01; funding paginates from 2024-08). This would extend the panel to ~21 months — but only with a **new** prereg, and only if ironflow labels exist (they do not before 2025-05; document that as a hard label ceiling).
3. **Track C volatility on the same panel** if not already covered by Step 4(b).
4. Only then: a **new** materially-different source per §16, or a timestamped evidenced structural-blocker document.

### Step 6 — Close the session
- Update `research_state/experiment_frontier.json` (precise `resume_triggers`, current `next_unfinished_task`, `program_status=ACTIVE_HEAVY_CAMPAIGN`).
- Update `AGENT_HANDOFF.md` with a **timestamped redirect** to this file.
- Commit code, manifests, prereg, panel build report, and verdict. **Never** commit raw data or caches.
- If and only if a genuine terminal stop is reached (no admissible unblocked work remains), emit a **single** timestamped evidenced clean-stop artifact and STOP. Do not poll.

---

## 5. PRE-STAGED HEAVY WORK — mandatory on ANY resume trigger

If a resume trigger fires, execute **in this order** and produce all artifacts before ending:
- (a) Prereg frozen **before** outcomes: `research_state/experiment_prereg_<UTC>.json`, `pre_registered_before_outcomes: true`, `frozen_before_outcomes: true`, primary contrast `C2_vs_B1`.
- (b) Frozen harness: `python scripts/fclr010_harness.py` on the newly eligible data.
- (c) `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<UTC>.md` with calibration (Brier/reliability), LOO stability, concentration (LOIO), block-bootstrap CIs (≥2000), Holm across the registered family, and explicit PASS/NOT_MET with reasons.
- (d) Atomic state updates (`experiment_frontier.json`, registry, manifest, verdict).
- (e) Commit evidence (code, manifests, reports — **not** raw data).

**Resume triggers (any one):**
1. Gate 4 `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with all 8 fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation.
2. HL ≥100 d AND verified post-2026-10-31 observed liquidation labels.
3. A genuinely new, unassessed, plausibly §16-admissible liquidation-label source is evidenced.
4. **This campaign has not yet been executed.** That alone is sufficient — it is the current work, not a future trigger.

---

## 6. INFRASTRUCTURE FIX APPLIED THIS SESSION

The CI worker bootstrap installed only `pytest numpy requests` into the controller venv and ran the agent without any scientific stack. `research_state/workflow_run_diagnostics.jsonl` records **22 `No module named 'pandas'`, 6 `pyarrow`, 12 `numpy`, 6 `pytest`** across 79 runs. Every agent session that tried to build a panel or run the full suite hit this wall.

**Fix applied:**
- `requirements.txt` now pins `numpy`, `pandas`, `scipy`, `pyarrow` (was missing `pyarrow`, which the panel builders import directly).
- The worker bootstrap step now provisions a dedicated venv and installs `-r requirements.txt` before any session starts, bounded by a 600 s deadline. The agent therefore always has the stack it needs.
- The controller test venv install is unchanged (it already pinned `pytest numpy requests`).
- The prior handoff banned `.github/workflows` edits outright, which is precisely what let the missing-dependency rot persist across many sessions. That ban is replaced by: **do not** add parallel collectors, schedulers, wrappers, or polling loops — but you **may** fix the environment the agent runs in.

**Verify:** `python3 -c "import pandas, numpy, scipy, pyarrow; print('OK')"` then `python -m unittest discover -s tests -v`.

---

## 7. HARD BANS (no exceptions)

- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation with Hyperliquid windows; no venue mixing in one panel.
- No modeled/proxy/synthetic liquidation labels presented as observed.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass; no whole-tree grep for the trigger string.
- No reopening/relitigating/retuning sealed verdicts (Track B/C, FCLR-*, expansion robustness, H2).
- No polling/waiting; no status-only sessions; no redundant controllers, schedulers, or endless retries.
- **Do not** re-probe 1h candles to conclude "no early data" — use `4h`.
- **Do not** follow the 09:51 handoff, or the redirect stubs, if they conflict with this file.

---

## 8. KEY REFERENCES

- `RESEARCH_PROMPT.md` — §5 (source acceptance), §15 (outcome families / honest label gate), §16 (adaptive feasibility), §17 (multiplicity/promotion), §18 (integrity/deterministic resume), §19 (session DoD), §20 (status contract).
- `research_state/research_protocol_fclr010.md` — frozen Track A protocol, model forms, gate.
- `scripts/tracka_hl_fetch_candles_early_4h.py`, `scripts/tracka_hl_expansion_funding_paginate.py` — acquisition templates.
- `scripts/tracka_hl_build_early_4h_panel.py`, `scripts/tracka_hl_evaluate_successor.py`, `scripts/run_expansion_robustness.py` — build/eval/robustness templates.
- `scripts/create_forward_prereg.py`, `scripts/fclr010_harness.py` — prereg + frozen harness.
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles_4h/`.
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`.
- Prior evidence: `tracka_hl_early_4h_panel_build_report_20261112T054737Z.json` (2-block pilot), `next_panel_gap_audit_20261111T163229Z.md` (gap inventory — note its 2025-05..2026-04 "candles not cached" claim is now resolved for 2025-05..2025-10 via 4h).

---

## 9. SESSION DO D (answer in the handoff, per §19)

- What did the evidence support, contradict, or leave unknown?
- Strongest alternative explanation?
- Which data/label/inference limitation dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- Exact artifact and command/test demonstrating progress.

---

## 10. IMMEDIATE FIRST ACTION (now)

Execute `FCLR-EARLY4H-2025H1-HEAVY` Steps 1–4. The panel is admissible, unclaimed, disjoint from all sealed windows, and requires no external permission and no future data. Do not re-derive the clean stop; do not re-probe 1h candles; do not re-run assessed discovery.