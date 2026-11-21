# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T11:58:45Z (refreshed and re-verified green this session; supersedes the 2026-11-21T11:56:27Z refresh)
**Sole active campaign:** FCLR-PANEL-FE-001-20261121T085602Z (rank-0, READY_EXECUTE/ACTIVE) — the heavy panel fixed-effects funding-conditioning study of realized volatility and liquidation intensity with walk-forward OOS
**Latest completed heavy session on disk:** session_20261121T080000Z (FCLR-SESSION-SYNTHESIS-01, verdict CONSOLIDATORY_ONLY — inverse-variance fixed-effect + DerSimonian-Laird random-effects meta-analysis over 17 terminal funding-conditioning contrasts; RV FE pooled d=1.237 CI incl. zero; liquidation FE pooled d=0.379 CI excl. zero BUT RE DL pooled d=0.228 CI incl. zero under I²=97.5%; independent stdlib recompute concurs; all terminal verdicts carried forward unchanged, no hypothesis promoted)
**Frontier status (machine-verified):** `python3 scripts/next_campaign_status.py` → `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN`. The 3-block confirmatory route is exhausted on every domain (Binance 5-symbol contiguous + disjoint + mark+funding-only; Hyperliquid bulk + extended). **This handoff does NOT ask the next session to wait for that route.** It redirects to a *materially different, feasible* design that uses the full frozen panels (panel fixed effects + walk-forward), which the 3-block frontier check does not and cannot certify as exhausted.
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → exit 0 (`reason=OK`); `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 79 tests pass (OK); both frozen panel sha256 values re-verified on disk (`41962f82…` FCLR-001, `81a100d5…` combined liquidation); campaign id reconciled across this handoff, `experiment_frontier.json` rank-0, and `hypothesis_registry.json` (`H_fclr_panelfe_001`, FROZEN_PENDING_EVALUATION) to the single canonical `FCLR-PANEL-FE-001-20261121T085602Z`; root `research_state/` md+json count 499/500 (cap 500). The `FCLR-PANEL-FE-001` gate family in `scripts/check_handoff_heavywork_gate.py` binds the exact panel-FE artifact set for any post-20261121T085602Z session, so future agents cannot idle on the external trigger.
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable this session (re-run `python3 -m pip install -r requirements.txt` if a fresh checkout lacks them). Both frozen panels load; sha256 asserted.

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block and every prior `NEXT_SESSION_TASK.md`. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-PANEL-FE-001). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, the Track A/B/C families, and the FCLR-SESSION-SYNTHESIS-01 consolidation) are terminal/superseded and must NOT be re-run. A session that does not emit the Section 4 artifact set under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T11:58:45Z)

**Execute FCLR-PANEL-FE-001 — a panel fixed-effects study of whether the funding rate conditions (a) realized volatility and (b) liquidation intensity, with a walk-forward out-of-sample evaluation — behind a fresh outcome-blind prereg frozen before any outcome is inspected.**

**First action (do this before anything else, in this order — no shortcuts):**
1. `cd` to repo root; run `python3 scripts/check_handoff_heavywork_gate.py` (must print `reason=OK`) and `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` (must be all OK). If either fails, fix the environment first — nothing else counts as progress until both are green.
2. Create `research_state/session_<UTC>/` with `UTC > 20261121T085602Z`.
3. Freeze the outcome-blind prereg FIRST (`fclr_panelfe01_prereg_<UTC>.json` + `.md`, `outcome_data_inspected_before_freeze=false`, both panel sha256 asserted). Do NOT read any RV/liquidation outcome statistics before this file exists.
4. Only then run the panel-FE evaluation triad, the independent stdlib/numpy recompute, the evidence audit, and the non-empty `trigger_check_<UTC>.json`.
5. Re-run the gate and the 79-test suite; both must stay green before you stop.

**This is non-avoidable heavy work.** A prose-only session, a trigger-check-only session, an audit-only session, a placeholder file, or an empty session directory does NOT satisfy the `FCLR-PANEL-FE-001` gate family and is a failed session. The bottleneck that blocked the prior session (awaiting an external `NEW_OBSERVED_LIQUIDATION_SOURCE` trigger, or hunting a non-existent new free-data route) is removed: the frozen panels are sufficient and verified, so the only remaining input is the agent's own execution of the study.

**Why this is the focus (repository-name priority):** The repository is named *Funding-conditioned-volatility-and-liquidation-risk* — two scientific halves reconciled by funding conditioning. Half (a): does the funding rate *condition volatility (RV)*? Half (b): does it *condition liquidation risk*? Every prior campaign answered these with **pooled cross-sectional regime contrasts** or a **3-block time-series confirmation**. Both routes are now exhausted or underpowered on the frozen panels (see Section 5). This campaign attacks the same two halves with a **materially different and feasible design**: a two-way (coin + hour) fixed-effects panel regression on the full frozen panels, which uses within-coin, within-hour variation and therefore does **not** require the 3 mutually non-overlapping ≥127-day contiguous blocks that the frontier check reports as unavailable.

**Why this removes the bottleneck (explicit):** The prior rank-0 campaign (`FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE-20261121T071500Z`, then the consolidation) left the next session with only two options: *await an external `NEW_OBSERVED_LIQUIDATION_SOURCE` trigger* (which cannot fire inside this closed, frozen-data environment) or *find a new free-data route* (which `next_campaign_status.py` confirms does not exist). That is a blocked frontier: a future agent would emit blocker evidence and stop, making no progress. **This handoff removes that bottleneck** by naming a concrete, executable, heavy campaign on data that is already frozen and verified. The only thing the next session must supply is the outcome-blind prereg and the evaluation triad.

**What was done this session (bottleneck removal + de-risking, already complete):**
- Verified and repaired the Python environment (numpy/pandas/scipy/pyarrow were absent; reinstalled from `requirements.txt`; imports now succeed). This was a hard blocker for *any* heavy evaluation script.
- Re-verified the machine checks on a clean tree: gate `reason=OK` (exit 0); 79 tests OK; `next_campaign_status.py` → `no feasible 3-block design in ANY domain` (expected); both frozen panel sha256 re-verified on disk (`41962f82…` FCLR-001, `81a100d5…` combined liquidation); root `research_state/` md+json count 499/500; rank-0 `experiment_frontier.json` = `FCLR-PANEL-FE-001-20261121T085602Z` READY_EXECUTE/ACTIVE; `hypothesis_registry.json` holds `H_fclr_panelfe_001` FROZEN_PENDING_EVALUATION (terminal=false).
- Completed a **coverage-only feasibility audit** (no RV/liquidation outcome statistics were computed; this is metadata needed to make the campaign executable, not a peek at results):
  - **FCLR-001:** 29,136 rows × 22 cols, 5 coins (BNBUSDT/BTCUSDT/ETHUSDT/XRPUSDT/SOLUSDT), 2026-01-01 00:00 → 2026-08-31 23:00 UTC, 5,832 hourly steps per coin. `signed_funding` and `funding_asof_lag_h` are non-null on 29,132/29,136 rows (99.99%); `rv1h` on 23,558; `log_rv1h` on 23,531; `target_rv24h` on 20,871. **`premium` is 100% null** (`premium_status=NOT_COMPUTABLE_WITHOUT_INDEX_PRICE`) — the panel-FE models must use `signed_funding` / `funding_asof_lag_h` / `abs_funding_pct_trail`, never `premium`.
  - **Combined liquidation panel:** 1,740,415 observed event rows, 15 coins (AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP), 2025-03-22 19:00 → 2026-10-31 22:00 UTC. `fundingRate`, `abs_fund_pct`, `notional_usd`, `rv24h`, `rv168h` are non-null on all 1,740,415 rows. Sources: ironflow 1,555,142 + metpie 185,273. This is **observed** liquidation-event data (Track A), so the old "Track A blocked on data" note is superseded for this design.
- Wired a new machine-enforced gate family `FCLR-PANEL-FE-001` into `scripts/check_handoff_heavywork_gate.py` with a matching regression test in `tests/test_tracka_hardening_143.py` (`TestPanelFeCampaignGate`, 5 tests). Post-20261121T085602Z sessions that do not emit the full panel-FE artifact set fail closed.
- **No bottleneck remains to remove**; the FCLR-PANEL-FE-001 gate family binds the full Section 4 artifact set so the next session cannot idle.

**The two pre-registered hypotheses (frozen before outcomes):**
- **H_panelfe_vol (half a):** In a two-way (coin + hour) fixed-effects panel on FCLR-001, the coefficient on `funding_asof_lag_h` / `signed_funding` in a regression of next-hour `log_rv1h` (and, robustness, `target_rv24h`) is non-zero and economically material (≥2% relative effect).
- **H_panelfe_liq (half b):** In a two-way (coin + hour) fixed-effects panel on the hourly-aggregated combined liquidation panel, the coefficient on `fundingRate` / `abs_fund_pct` in regressions of `log(1+liq_count)` and `log(1+notional_usd)` is non-zero and economically material (≥2% relative effect).

**Pre-registered inference & evaluation protocol (freeze these before touching outcomes):**
- Two-way (coin + hour) fixed effects; cluster-robust SE by coin **and** Driscoll-Kraay HAC SE; report both; Newey-West as a third robustness SE.
- Regime stratification as pre-registered secondary cuts: RV tercile and UTC session bucket (Asia/EU/US).
- Walk-forward OOS: expanding-window one-step-ahead; funding-conditioned model vs a no-funding baseline; QLIKE for RV; Poisson/negative-binomial deviance (and QLIKE) for liquidation intensity; Diebold-Mariano test of equal predictive accuracy. The walk-forward must be strictly chronological and respect the frozen `split` boundaries as a minimum; never use a random train/test split and never let future information enter a forecast origin.
- Hourly liquidation aggregation rule: aggregate `notional_usd` to per-coin hourly count and sum; use the funding rate observed at/inside the hour (state the exact rule — last event funding rate or hourly mean — in the prereg) and never fabricate a missing liquidation hour as zero without flagging it.
- **Materiality floor 2% preserved.** Do NOT relax it after seeing outcomes. A null is recorded as NOT_SUPPORTED.
- `outcome_data_inspected_before_freeze=false` in the prereg JSON; assert the frozen panel sha256 in the eval script header.

**Next focus for the future agent:** rank-0 is FCLR-PANEL-FE-001 (READY_EXECUTE). Execute it end-to-end under a new `research_state/session_<UTC>/` and emit the Section 4 artifact set. **DO NOT** re-run any terminal campaign; **DO NOT** emit a prose-only, trigger-check-only, or placeholder session; **DO NOT** add root-level `research_state/*.md|*.json` (root at 499/500 cap); **DO NOT** modify `.github/workflows`; **DO NOT** overwrite the sealed `research_state/research_protocol.md`.

---

## 2. Why this campaign is feasible when the 3-block design is not

The 3-block confirmatory design (train/test blocks of ≥127 contiguous days) is a *time-series* design that needs long untouched contiguous windows. `next_campaign_status.py` shows none exist (Binance contiguous 2024-04..05 = 61d; Hyperliquid untouched = 24d; mark+funding-only has 1 feasible month, need 3). A **panel fixed-effects** design does not need contiguous untouched blocks: it exploits cross-sectional (coin) and within-hour variation across the *entire* available panel with coin and hour fixed effects, and evaluates out-of-sample via an expanding-window walk-forward that only requires chronological ordering, not ≥127-day gaps. This is why the panel route is admissible on exactly the data the frontier calls exhausted.

---

## 3. Frozen inputs (verified — do not re-derive, do not substitute)

- **Primary panel (FCLR-001):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. Assert the sha256 in the script header. `premium` is all-null; do not use it.
- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 19:00 → 2026-10-31 22:00 UTC. Aggregate `notional_usd` to hourly per-coin count and notional sum before merging with funding.

---

## 4. Required artifacts for the NEXT heavy session (machine-enforced by the FCLR-PANEL-FE-001 gate)

Create a new `research_state/session_<UTC>/` (UTC > 20261121T085602Z) and emit, all non-empty:

- `fclr_panelfe01_prereg_<UTC>.json` and `.md` — outcome-blind prereg freeze (`outcome_data_inspected_before_freeze=false`, hypotheses, models, inference, walk-forward protocol, 2% floor, panel sha256).
- `fclr_panelfe01_eval_<UTC>.py`, `.json`, `.md` — the panel-FE estimation + walk-forward evaluation triad (both halves; FE + clustered/Driscoll-Kraay SE; QLIKE / deviance; Diebold-Mariano; regime cuts).
- `fclr_panelfe01_recompute_<UTC>.py`, `.json` — an **independent stdlib/numpy** recompute that re-derives the headline coefficients and OOS metrics from the raw parquet and concurs.
- `fclr_panelfe01_evidence_audit_<UTC>.json` and `.md` — evidence audit tying each verdict to its artifacts.
- `trigger_check_<UTC>.json` — non-empty trigger check (records that no external trigger is required for this campaign and that the frozen panels are the sole inputs).

### Acceptance Tests (run these — they are the gate)

```bash
# Gate must pass (exit 0)
python3 scripts/check_handoff_heavywork_gate.py

# Unit tests must pass (0 failures)
python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143

# Frontier must show the 3-block design exhausted (machine-verified context)
python3 scripts/next_campaign_status.py
```

**Expected gate output:** `[PASS] handoff-heavywork gate: ... reason=OK`
**Expected frontier output:** `== CAMPAIGN STATUS: no feasible 3-block design in ANY domain ==` (this is expected and is *why* the panel route is the admissible path).

**State verification:**
- `experiment_frontier.json` rank 0 = FCLR-PANEL-FE-001-20261121T085602Z READY_EXECUTE/ACTIVE; all others SUPERSEDED.
- `hypothesis_registry.json` records `H_fclr_panelfe_001` with status `FROZEN_PENDING_EVALUATION` (prereg frozen, evaluation pending; `terminal=false`).
- No liquidation/RV outcomes inspected before the prereg freeze.
- Root `research_state/` md+json count stays ≤ 500 (currently 499/500).

---

## 5. Bottlenecks removed / stale paths (do not re-open)

- **Trigger-only dead end removed.** Awaiting `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire inside this closed, frozen-data environment. The panel-FE design needs no external trigger; `trigger_check_<UTC>.json` records that explicitly.
- **Track A data blocker superseded.** The combined liquidation panel is observed liquidation-event data (ironflow + metpie, 1.74M events, 15 coins). The old "Track A blocked / no admissible liquidation data" notes predate this panel and must not be used to justify idling.
- **Stale branch, do not merge.** `origin/docs/fclr006-interval-flag-errata-20261030` is 2,158 commits behind `main` and only 2 ahead; it carries an old AGENT_HANDOFF.md plus accidental zip files. It is not a valid handoff and must not be merged over `main`. The sole durable handoff is `AGENT_HANDOFF.md` on `main`.
- **Root churn cap.** Root `research_state/` is at 499/500 md+json files. Do not add any root-level `research_state/*.md` or `research_state/*.json`; all new artifacts go under `research_state/session_<UTC>/`.

---

## 6. Completed campaigns (terminal — record only, do NOT re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | session_20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | Pooled within-hour cross-sectional funding contrast (RV) | session_20261120T175300Z | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0 |
| FCLR-XSEC-002 | Regime-conditioned funding contrast (next-hour RV, RV tercile) | session_20261120T210000Z | **SUPPORTED** | high-RV funding CI [0.0046, 0.2348], p=0.019; OOS forwards all NOT_REPLICATED |
| FCLR-XSEC-004 | Regime-conditioned funding contrast (next-hour liq INTENSITY, count) | session_20261120T230000Z | **SUPPORTED** | low-RV funding CI [448605.26, 841155.73], p=0.0, Holm 0.0, materiality 0.80 |
| FCLR-XSEC-005 | Regime-conditioned funding contrast (next-hour liq INTENSITY, notional) | session_20261121T001225Z | **SUPPORTED** | low-RV notional funding CI [452972.90, 850198.89], p=0.0, materiality 0.80 |
| FCLR-XSEC-006 | Regime-conditioned funding contrast (next-hour notional liq, UTC bucket) | session_20261121T010934Z | **SUPPORTED** | significant across all three UTC session buckets |
| FCLR-XSEC-007 | Cross-panel reconciliation (RV tercile vs UTC session) | session_20261121T021041Z | NOT_SUPPORTED | Primary A CI [−0.0004, 2.005] incl. 0 (p=0.272) |
| FCLR-XSEC-008 | Alternative regime conditioning (rv168/rv24 vol-of-vol terciles) | session_20261121T054721Z | NOT_SUPPORTED | sign reversal vs XSEC-002; XSEC program terminal |
| FCLR-LIQ-OOS-FORECAST-001 | OOS forecast of next-24h observed notional liq intensity (C2 vs B1) | session_20261121T055825Z | NOT_SUPPORTED | QLIKE FAIL rel −5.88% CI incl. zero; Brier/LogLoss PASS; joint needs ALL |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity C2 vs B1 | FCLR-LIQ-COMBINED-20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING / -QLIKE | Cross-sectional ordering / QLIKE of daily liq intensity | 2026-11-15 | NOT_MET | daily ordering/QLIKE, not regime-conditioned hourly paired contrast |
| Track A / Track B / FCLR-011 family | observed-liq forecast / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |
| FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE | Trigger-only sentinel (external trigger) | 20261121T071500Z | SUPERSEDED | was the structural bottleneck; replaced by SESSION-SYNTHESIS-01 then PANEL-FE-001 |
| FCLR-SESSION-SYNTHESIS-01 | Outcome-blind consolidation + quantitative meta-analysis | session_20261121T080000Z | **CONSOLIDATORY_ONLY** | 17 contrasts; RV FE d=1.237 CI incl. 0; liq FE d=0.379 CI excl. 0 BUT RE DL d=0.228 CI incl. 0 under I²=97.5%; no promotable skill |

---

## 7. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, or any Track A/B campaign (all terminal/superseded).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — root md+json count is **499/500**; one more breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate). All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null is preserved as NOT_SUPPORTED.
- **Do NOT** conflate observed liquidations with modeled boundary breaches (Track B) or with RV forecasts — keep the track separation explicit in every artifact.
- The `FCLR-PANEL-FE-001` gate family binds the exact artifact set for any post-20261121T085602Z session that claims this campaign family. Prose-only, trigger-check-only, audit-only, or placeholder artifacts do NOT satisfy the gate.

---

## 8. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. The active rank-0 campaign is FCLR-PANEL-FE-001 (READY_EXECUTE). The next session must execute it end-to-end behind a fresh outcome-blind prereg and emit the Section 4 artifact set. **No prose-only, no trigger-check-only, no placeholder sessions.** Commit nothing merely to show activity; if no meaningful progress is possible, record the evidence for the blocker and stop cleanly with the next valid independent task executed.

(End of handoff)