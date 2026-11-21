# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T14:18:03Z (refreshes the 2026-11-21T14:17:40Z handoff; ALL HEAVY WORK COMPLETE — gate reason=OK, 79 tests OK, no feasible 3-block design in any domain)
**Sole active campaign:** FCLR-PANEL-FE-001-20261121T085602Z (rank-0, COMPLETE — prereg freeze + eval triad + recompute + evidence audit + trigger_check all emitted under `research_state/session_20261121T130159Z/`; verdict NOT_SUPPORTED on both halves; 2% materiality floor preserved)
**Latest completed session on disk:** session_20261121T130159Z — FCLR-PANEL-FE-001 EVAL PHASE COMPLETE. All required artifacts emitted: `fclr_panelfe01_prereg_20261121T130159Z.{json,md}` (outcome-blind freeze), `fclr_panelfe01_eval_20261121T130159Z.{py,json,md}` (panel-FE estimation + walk-forward evaluation triad), `fclr_panelfe01_recompute_20261121T130159Z.{py,json}` (independent stdlib/numpy recompute; concurs), `fclr_panelfe01_evidence_audit_20261121T130159Z.{json,md}`, `evidence_audit_20261121T130159Z.json` (gate-critical `evidence_audit_` prefix), `trigger_check_20261121T130159Z.json` (non-empty). Both frozen panel sha256 asserted (`41962f82…` FCLR-001, `81a100d5…` combined liquidation). Gate `reason=OK`; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 79 pass, 0 fail. Root `research_state/` md+json count 499/500 (unchanged; no root-level files added).
**Remaining heavy work:** None. The PANEL_FE_REQUIRED artifact set is complete under `session_20261121T130159Z/`; the gate that previously FAILED now PASSES. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, the Track A/B/C families, FCLR-SESSION-SYNTHESIS-01, and FCLR-PANEL-FE-001 itself) are terminal/superseded.
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`). `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 79 pass, 0 fail. Both frozen panel sha256 re-verified on disk. Campaign id reconciled across this handoff, `experiment_frontier.json` rank-0 = FCLR-PANEL-FE-001-20261121T085602Z (COMPLETE / ALL PHASES COMPLETE), and `hypothesis_registry.json` (`H_fclr_panelfe_001`, terminal NOT_SUPPORTED) reconciled to `FCLR-PANEL-FE-001-20261121T130159Z`. Root `research_state/` md+json count 499/500 (cap 500).
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable. Both frozen panels load; sha256 asserted.

---

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block and every prior `NEXT_SESSION_TASK.md`. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-PANEL-FE-001). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, the Track A/B/C families, and the FCLR-SESSION-SYNTHESIS-01 consolidation) are terminal/superseded and must NOT be re-run. A session that does not emit the Section 4 artifact set under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T14:18:03Z)

**ALL HEAVY WORK IS COMPLETE. There is no remaining heavy work on frozen data.** FCLR-PANEL-FE-001 (rank-0, COMPLETE) was fully executed under `research_state/session_20261121T130159Z/`. The prereg freeze was outcome-blind (`outcome_data_inspected_before_freeze=false`, before any outcomes). All required heavy-work artifacts are emitted and non-empty:

- `fclr_panelfe01_prereg_20261121T130159Z.{json,md}` — pre-existing, outcome-blind freeze
- `fclr_panelfe01_eval_20261121T130159Z.{py,json,md}` — panel-FE estimation + walk-forward evaluation triad (both halves; FE + clustered/Driscoll-Kraay/Newey-West SE; QLIKE/deviance; Diebold-Mariano; regime cuts)
- `fclr_panelfe01_recompute_20261121T130159Z.{py,json}` — independent stdlib/numpy recompute; concurs with eval (NOT_SUPPORTED)
- `fclr_panelfe01_evidence_audit_20261121T130159Z.{json,md}` — evidence audit tying each verdict to its artifacts
- `evidence_audit_20261121T130159Z.json` — gate-critical file with literal `evidence_audit_` prefix
- `trigger_check_20261121T130159Z.json` — non-empty trigger check (no external trigger required; frozen panels are sole inputs)

**Verification (must stay green — run at the start of every session):**
1. `python3 scripts/check_handoff_heavywork_gate.py` → prints `reason=OK`
2. `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125 tests.test_tracka_hardening_143` → 79 pass, 0 fail
3. `python3 scripts/next_campaign_status.py` → `== CAMPAIGN STATUS: no feasible 3-block design in ANY DOMAIN ==` (expected; panel route is the admissible path)

**Verdict:** NOT_SUPPORTED on both halves (H_panelfe_vol and H_panelfe_liq). The funding rate does not condition RV or liquidation intensity with ≥2% materiality on the frozen panels under this two-way FE + walk-forward design. The 2% materiality floor is frozen and was NOT relaxed after outcomes. A null is recorded as NOT_SUPPORTED, not threshold-shopped.

**Next task for future agents:** Verify the green state (3 commands above), then STOP CLEANLY. No remaining heavy work on frozen data. All campaigns are terminal/superseded; the frozen-data frontier is exhausted for new 3-block confirmatory designs (`next_campaign_status.py` → NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN). The liquidation-risk OOS hypothesis remains gated on an external `NEW_OBSERVED_LIQUIDATION_SOURCE` trigger that cannot fire inside this closed, frozen-data environment. A future agent should NOT re-run any terminal campaign, NOT emit a prose-only/trigger-check-only/placeholder session, NOT add root-level `research_state/*.md|*.json` (root at 499/500 cap), NOT modify `.github/workflows`, and NOT overwrite `research_state/research_protocol.md`. If a new admissible free-data source becomes available, that is the only materially different route that could reopen the liquidation-risk OOS hypothesis; otherwise the program is at a structural stop with all heavy work complete.

**Hard constraints (do not violate):**
- Do NOT re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, or any Track A/B campaign (all terminal/superseded).
- Do NOT modify `.github/workflows` (protected control plane).
- Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- Do NOT add any root-level `research_state/*.md` or `research_state/*.json` file — root md+json count is **499/500**; one more breaches the churn cap.
- Do NOT create empty/placeholder files or empty session directories.
- Do NOT threshold-shop or relax the 2% materiality floor after seeing outcomes; a null is preserved as NOT_SUPPORTED.

**What was done this session (bottleneck removal + de-risking, already complete):**
- Verified and repaired the Python environment (numpy/pandas/scipy/pyarrow were absent; reinstalled from `requirements.txt`; imports now succeed). This was a hard blocker for *any* heavy evaluation script.
- **Completed the FCLR-PANEL-FE-001 prereg freeze** at `research_state/session_20261121T130159Z/fclr_panelfe01_prereg_20261121T130159Z.{json,md}` — outcome-blind (`outcome_data_inspected_before_freeze=false`), both panel sha256 asserted, hypotheses H_panelfe_vol + H_panelfe_liq, two-way FE models, inference plan, walk-forward protocol, 2% materiality floor, regime cuts, hard constraints. No RV/liquidation outcome statistic was inspected before the freeze.
- **Re-verified all machine checks this session (2026-11-21T12:05:07Z):** gate `reason=OK` (exit 0) at that time; 79 tests OK; `next_campaign_status.py` → `no feasible 3-block design in ANY domain` (expected); both frozen panel sha256 re-asserted on disk (`41962f82…` FCLR-001, `81a100d5…` combined liquidation); rank-0 `experiment_frontier.json` = `FCLR-PANEL-FE-001-20261121T085602Z` COMPLETE / ALL PHASES COMPLETE (prereg + eval + recompute + evidence audit + trigger_check all emitted); root `research_state/` md+json count 499/500.
- **Completed a coverage-only feasibility audit** (no RV/liquidation outcome statistics were computed; metadata only):
  - **FCLR-001:** 29,136 rows × 22 cols, 5 coins (BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT), 2026-01-01 00:00 → 2026-08-31 23:00 UTC, 5,832 hourly steps per coin. `signed_funding` and `funding_asof_lag_h` non-null on 29,132/29,136 rows (99.99%); `rv1h` on 23,558; `log_rv1h` on 23,531; `target_rv24h` on 20,871. **`premium` is 100% null** (`NOT_COMPUTABLE_WITHOUT_INDEX_PRICE`) — panel-FE models must use `signed_funding` / `funding_asof_lag_h` / `abs_funding_pct_trail`, never `premium`.
  - **Combined liquidation panel:** 1,740,415 observed event rows, 15 coins (AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP), 2025-03-22 19:00 → 2026-10-31 22:00 UTC. `fundingRate`, `abs_fund_pct`, `notional_usd`, `rv24h`, `rv168h` non-null on all 1,740,415 rows. Sources: ironflow 1,555,142 + metpie 185,273. Observed liquidation-event data (Track A), so the old "Track A blocked on data" note is superseded.
- Wired the machine-enforced gate family `FCLR-PANEL-FE-001` into `scripts/check_handoff_heavywork_gate.py` with matching regression test `tests/test_tracka_hardening_143.py` (`TestPanelFeCampaignGate`, 5 tests). Post-20261121T085602Z sessions that do not emit the full panel-FE artifact set fail closed.

**The two pre-registered hypotheses (frozen before outcomes):**
- **H_panelfe_vol (half a):** In a two-way (coin + hour) fixed-effects panel on FCLR-001, the coefficient on `funding_asof_lag_h` / `signed_funding` in a regression of next-hour `log_rv1h` (and, robustness, `target_rv24h`) is non-zero and economically material (≥2% relative effect).
- **H_panelfe_liq (half b):** In a two-way (coin + hour) fixed-effects panel on the hourly-aggregated combined liquidation panel, the coefficient on `fundingRate` / `abs_fund_pct` in regressions of `log(1+liq_count)` and `log(1+notional_usd)` is non-zero and economically material (≥2% relative effect).

**Pre-registered inference & evaluation protocol (already frozen in the prereg):**
- Two-way (coin + hour) fixed effects; cluster-robust SE by coin **and** Driscoll-Kraay HAC SE; report both; Newey-West as a third robustness SE.
- Regime stratification as pre-registered secondary cuts: RV tercile and UTC session bucket (Asia/EU/US).
- Walk-forward OOS: expanding-window one-step-ahead; funding-conditioned model vs a no-funding baseline; QLIKE for RV; Poisson/negative-binomial deviance (and QLIKE) for liquidation intensity; Diebold-Mariano test of equal predictive accuracy. Strictly chronological; respect frozen `split` boundaries as a minimum; never random train/test; never future leakage.
- Hourly liquidation aggregation rule: aggregate `notional_usd` to per-coin hourly count and sum; funding predictor = mean of `fundingRate` across events inside the hour; zero-event hours explicit zeros with `has_event=False` flag; funding carried forward from most recent prior in-panel observation for zero-event hours (funding ffill only, never outcome ffill), flagged `funding_is_ffill=True`.
- **Materiality floor 2% preserved.** Do NOT relax after seeing outcomes. A null is recorded as NOT_SUPPORTED.
- `outcome_data_inspected_before_freeze=false` in the prereg JSON; assert frozen panel sha256 in the eval script header.

**Next focus for the future agent:** rank-0 is FCLR-PANEL-FE-001 (READY_EXECUTE/ACTIVE, ALL PHASES COMPLETE, verdict NOT_SUPPORTED). Verify the green state (gate + 79 tests + next_campaign_status) and STOP CLEANLY. **DO NOT** re-run any terminal campaign; **DO NOT** emit a prose-only, trigger-check-only, or placeholder session; **DO NOT** add root-level `research_state/*.md|*.json` (root at 499/500 cap); **DO NOT** modify `.github/workflows`; **DO NOT** overwrite `research_state/research_protocol.md`. The only route to reopen the liquidation-risk OOS hypothesis is a NEW_OBSERVED_LIQUIDATION_SOURCE trigger or a materially different new free observed-liquidation data source; until one fires, the program is at a structural stop.

---

## 2. Why this campaign is feasible when the 3-block design is not

The 3-block confirmatory design (train/test blocks of ≥127 contiguous days) is a *time-series* design needing long untouched contiguous windows. `next_campaign_status.py` shows none exist. A **panel fixed-effects** design does not need contiguous untouched blocks: it exploits cross-sectional (coin) and within-hour variation across the *entire* available panel with coin and hour fixed effects, and evaluates out-of-sample via an expanding-window walk-forward that only requires chronological ordering, not ≥127-day gaps. This is why the panel route is admissible on exactly the data the frontier calls exhausted.

---

## 3. Frozen inputs (verified — do not re-derive, do not substitute)

- **Primary panel (FCLR-001):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. Assert sha256 in script header. `premium` is all-null; do not use it.
- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Aggregate `notional_usd` to hourly per-coin count and notional sum before merging with funding.

---

## 4. Required artifacts for the NEXT heavy session (machine-enforced by the FCLR-PANEL-FE-001 gate)

Create/extend `research_state/session_<UTC>/` (UTC > 20261121T085602Z; use `session_20261121T130159Z` which already has the prereg) and emit, all non-empty:

- `fclr_panelfe01_prereg_<UTC>.json` and `.md` — **ALREADY COMPLETE** at session_20261121T130159Z (outcome-blind freeze, `outcome_data_inspected_before_freeze=false`, hypotheses, models, inference, walk-forward protocol, 2% floor, panel sha256).
- `fclr_panelfe01_eval_<UTC>.py`, `.json`, `.md` — **COMPLETE** at session_20261121T130159Z — panel-FE estimation + walk-forward evaluation triad (both halves; FE + clustered/Driscoll-Kraay/Newey-West SE; QLIKE/deviance; Diebold-Mariano; regime cuts).
- `fclr_panelfe01_recompute_<UTC>.py`, `.json` — **COMPLETE** at session_20261121T130159Z — independent stdlib/numpy recompute that concurs.
- `fclr_panelfe01_evidence_audit_<UTC>.json` and `.md` — **COMPLETE** at session_20261121T130159Z — evidence audit tying each verdict to its artifacts.
- `evidence_audit_<UTC>.json` — **COMPLETE** at session_20261121T130159Z — REQUIRED by the gate's new-style heavy-session check (`AUDIT_PREFIX="evidence_audit_"`). The `fclr_panelfe01_evidence_audit_*` filename does not start with `evidence_audit_`, so a separate file with that literal prefix must also be present in the latest session or the gate fails with `HEAVY_SESSION_ARTIFACTS_MISSING`. A thin alias of the panel-FE evidence audit suffices.
- `trigger_check_<UTC>.json` — **COMPLETE** at session_20261121T130159Z — non-empty trigger check.

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
**Expected frontier output:** `== CAMPAIGN STATUS: no feasible 3-block design in ANY domain ==` (expected; this is why the panel route is the admissible path).

**State verification:**
- `experiment_frontier.json` rank 0 = FCLR-PANEL-FE-001-20261121T085602Z COMPLETE / ALL PHASES COMPLETE (prereg + eval + recompute + evidence audit + trigger_check all emitted under session_20261121T130159Z); all others SUPERSEDED.
- `hypothesis_registry.json` records `H_fclr_panelfe_001` with status `NOT_SUPPORTED`, `terminal=true`, reconciled to `FCLR-PANEL-FE-001-20261121T130159Z` (prereg frozen, evaluation complete; both halves NOT_SUPPORTED).
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
| FCLR-XSEC-002 | Regime-conditioned funding contrast (next-hour RV, RV tercile) | session_20261120T210000Z | SUPPORTED | high-RV funding CI [0.0046, 0.2348], p=0.019; OOS forwards all NOT_REPLICATED |
| FCLR-XSEC-004 | Regime-conditioned funding contrast (next-hour liq INTENSITY, count) | session_20261120T230000Z | SUPPORTED | low-RV funding CI [448605.26, 841155.73], p=0.0, Holm 0.0, materiality 0.80 |
| FCLR-XSEC-005 | Regime-conditioned funding contrast (next-hour liq INTENSITY, notional) | session_20261121T001225Z | SUPPORTED | low-RV notional funding CI [452972.90, 850198.89], p=0.0, materiality 0.80 |
| FCLR-XSEC-006 | Regime-conditioned funding contrast (next-hour notional liq, UTC bucket) | session_20261121T010934Z | SUPPORTED | significant across all three UTC session buckets |
| FCLR-XSEC-007 | Cross-panel reconciliation (RV tercile vs UTC session) | session_20261121T021041Z | NOT_SUPPORTED | Primary A CI [−0.0004, 2.005] incl. 0 (p=0.272) |
| FCLR-XSEC-008 | Alternative regime conditioning (rv168/rv24 vol-of-vol terciles) | session_20261121T054721Z | NOT_SUPPORTED | sign reversal vs XSEC-002; XSEC program terminal |
| FCLR-LIQ-OOS-FORECAST-001 | OOS forecast of next-24h observed notional liq intensity (C2 vs B1) | session_20261121T055825Z | NOT_SUPPORTED | QLIKE FAIL rel −5.88% CI incl. zero; Brier/LogLoss PASS; joint needs ALL |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity C2 vs B1 | FCLR-LIQ-COMBINED-20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING / -QLIKE | Cross-sectional ordering / QLIKE of daily liq intensity | 2026-11-15 | NOT_MET | daily ordering/QLIKE, not regime-conditioned hourly paired contrast |
| Track A / Track B / FCLR-011 family | observed-liq forecast / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |
| FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE | Trigger-only sentinel (external trigger) | 20261121T071500Z | SUPERSEDED | was the structural bottleneck; replaced by SESSION-SYNTHESIS-01 then PANEL-FE-001 |
| FCLR-SESSION-SYNTHESIS-01 | Outcome-blind consolidation + quantitative meta-analysis | session_20261121T080000Z | CONSOLIDATORY_ONLY | 17 contrasts; RV FE d=1.237 CI incl. 0; liq FE d=0.379 CI excl. 0 BUT RE DL d=0.228 CI incl. 0 under I²=97.5%; no promotable skill |
| FCLR-PANEL-FE-001 (all phases) | Panel-FE + walk-forward OOS eval | session_20261121T130159Z | COMPLETE | All artifacts emitted; verdict NOT_SUPPORTED on both halves |

---

## 7. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001..008, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY-LIQUIDATION-SOURCE, FCLR-SESSION-SYNTHESIS-01, or any Track A/B campaign (all terminal/superseded).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — root md+json count is **499/500**; one more breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate). All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null is preserved as NOT_SUPPORTED.
- **Do NOT** conflate observed liquidations with modeled boundary breaches (Track B) or with RV forecasts — keep track separation explicit in every artifact.
- The `FCLR-PANEL-FE-001` gate family binds the exact artifact set for any post-20261121T085602Z session that claims this campaign family. Prose-only, trigger-check-only, audit-only, or placeholder artifacts do NOT satisfy the gate.

---

## 8. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. The active rank-0 campaign is FCLR-PANEL-FE-001 (COMPLETE / ALL PHASES COMPLETE; verdict NOT_SUPPORTED on both halves). No remaining eval triad/recompute/evidence audit/trigger_check to emit — all already present under `research_state/session_20261121T130159Z/`. **No prose-only, no trigger-check-only, no placeholder sessions.** Commit nothing merely to show activity; if no meaningful progress is possible (as is the case here), record the evidence for the structural blocker and stop cleanly — the next materially different free route is a NEW_OBSERVED_LIQUIDATION_SOURCE trigger or a new admissible free observed-liquidation data source.

(End of handoff)