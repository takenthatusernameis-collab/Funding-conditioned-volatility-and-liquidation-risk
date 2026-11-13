# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-13T11:12:44Z
**Status:** `HEAVY_CELLS_EXHAUSTED_CACHE` — Six volatility/liquidation cells are terminal with gates PASS. Cell 7 `FCLR-FWD-VOL-2024Q1-RV-DIAGNOSTIC` audited 2026-11-13T11:12:44Z and closed **`NOT_EXECUTABLE_DESIGN_SHORTFALL`** (90.96-day 2024Q1 window, no funding; block-0 train 1.96d; 3×30d non-overlapping tests + 7d embargo + ≥30d train needs ≥141d). **No frozen-but-unexecuted prereg remains and no cached window supports another full pre-registered funding-conditioned or feasible RV-diagnostic heavy cell** (`scripts/next_campaign_status.py` is source of truth).

Terminal ledger (all `GATE: PASS`):

| Cell | Verdict | Headline |
|---|---|---|
| FCLR-FWD-VOL-011-CONFIRM | `NOT_REPLICATED` | forward C2 rel −5.55%, CI favours B1, repro Δ0.044pp |
| FCLR-LIQ-010-CONFIRM | `NOT_REPLICATED` | rel 0.501% < 2% floor, LOIO 0/17, placebo fail |
| FCLR-EXP-ROBUST-REDO | `FRAGILE` | LOIO 4/8, placebo fail |
| FCLR-FWD-VOL-2025-CROSS | `NOT_REPLICATED` | rel 0.29%, CI crosses zero, LOIO 0/5 |
| FCLR-FWD-VOL-2024Q4-CROSS | `NOT_REPLICATED` | rel −20.77% (C2 worse), CI crosses zero, LOIO 0/5, placebo fail |
| FCLR-FWD-VOL-2025H2-CROSS | `NOT_REPLICATED` | rel −8.97% (C2 worse, CI excludes zero favouring B1), LOIO 0/5, placebo fail, Holm fail |
| FCLR-FWD-VOL-2024Q1-RV-DIAGNOSTIC | `NOT_EXECUTABLE_DESIGN_SHORTFALL` | coverage audit only; no outcomes computed; no prereg/execution feasible |

Sealed FCLR-011 PASS (4.94%, 2026-05..2026-08) remains unrefuted but does not generalize to any disjoint tested window. `H1_primary` is `NOT_SUPPORTED`.

**This file is the ONLY durable handoff.** `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. Do not create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file. Update in place by appending a dated `## SESSION LOG` entry.

---

## READ THIS FIRST — NON-NEGOTIABLE EFFICIENCY RULES

1. **Never close "nothing executable" without running `python3 scripts/next_campaign_status.py` and recording output.** It must show no actionable frozen prereg and no newly executable cached window.
2. **Never re-run terminal cells or re-verify gates as the session's only action.** Six gates PASS and 125 targeted tests PASS are established; rerun only if you produce a new artifact that could affect them (none expected).
3. **Cached heavy-work frontier is exhausted under pre-registered constraints.** Do not invent a lower-bar design, overlap tested windows, drop required blocks/embargo/robustness, or force funding-conditioned claims on no-funding windows.

---

## IMMEDIATE TASK (highest expected information gain per unit free compute)

**No cached heavy execution remains.** Advance only by producing **new evidence**:

### P1 — Bounded discovery of a newly admissible observed-liquidation source (Track A, highest IG if a candidate exists)
- Search only for a **specific, concrete candidate not already falsified** in `research_state/alt_source_scan_latest.json` and `research_state/alt_source_deep_review_latest.md` (2026-11-13T09:01Z). Do not restate prior negatives.
- If a candidate is found: perform §16 admissibility audit (provenance/license, unauthenticated, observed labels only, venue-consistent, ≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks) → freeze prereg pre-outcomes → build/eval → terminal verdict → fail-closed gate → update registry/frontier.
- If nothing new: record **new** concrete evidence (source/URL/fields/coverage/observed failing minimum) as a timestamped artifact in `research_state/` and update frontier; then stop (clean evidence-advancing close).

### P1 — Gate 4 Branch 1 (external trigger only; do not poll/wait)
- Act only if `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` appears with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation. Currently absent (`fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`).

### Forbidden / no-progress actions
- No status-only sessions, no repeated no-op probes of prior NO-GO sources, no Gate 4 polling, no threshold shopping/post-hoc changes, no zero/forward-fill to force comparability, no mutation of sealed artifacts, no agent-set `RESOLVED_VERIFIED`, no paid/manual/credentialed data, no `.github/workflows/*` edits, no raw cache/data_cache commits.

### Completion
1. **Heavy execution complete:** admissibility audit + frozen pre-outcomes prereg + timestamped terminal evaluation + registry/frontier updated + new fail-closed gate `GATE: PASS` + targeted tests green (for a newly admissible source only).
2. **Evidence-advancing discovery only:** timestamped audit/probe artifact showing a **previously-unrecorded** concrete failing minimum or newly discovered candidate, with exact fields/coverage, and state updated. This is a valid close given cache exhaustion.

Always run/report when touching campaign state or if unsure:
```bash
python3 scripts/next_campaign_status.py
python3 scripts/fclr_heavy_confirm_gate.py
python3 scripts/fclr_liq_010_confirm_gate.py
python3 scripts/fclr_exp_robust_redo_gate.py
python3 scripts/fclr_fwd_vol_2025_cross_gate.py
python3 scripts/fclr_fwd_vol_2024_cross_gate.py
python3 scripts/fclr_fwd_vol_2025h2_cross_gate.py
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_next_campaign_status
```

---

## BOTTLENECKS REMOVED (cumulative, key)

| Bottleneck | Resolution |
|---|---|
| Frozen 2024q4 prereg never executed (stem mismatch) | Fixed; executed → `NOT_REPLICATED`, `GATE: PASS`. |
| False "nothing executable" closures | `scripts/next_campaign_status.py` mandatory truth source. |
| Stale tests/frontier/campaign rank | Contract campaign-agnostic; frontier reconciled. |
| Cell 6 (2025H2) omitted from tested windows | TESTED_WINDOWS updated; stale handoff corrected. |
| **Cell 7 (2024Q1 RV diagnostic) treated as executable without feasibility proof** | Coverage+feasibility audit recorded (`research_state/coverage_audit_fwd_vol_2024q1_rv_diagnostic_20261113T111244Z.{json,md}`); closed `NOT_EXECUTABLE_DESIGN_SHORTFALL` with exact shortfall (block-0 train 1.96d; need ≥141d vs 90.96d). Prevents repeated "try to execute Q1-2024" churn. |

---

## EXACT START COMMANDS

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python3 scripts/next_campaign_status.py   # must print no actionable prereg; confirms cache exhaustion
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"
# If pursuing P1 discovery: identify a specific NEW candidate, record timestamped admissibility/probe evidence, and follow §16.
```

---

## DEFINITION OF DONE (answer in handoff)

- What did the evidence support, contradict, or leave unknown?
- Strongest alternative explanation?
- Which data/label/inference limitation dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- Exact artifact and command/test demonstrating progress.

---

## KEY REFERENCES

- `research_state/coverage_audit_fwd_vol_2024q1_rv_diagnostic_20261113T111244Z.{json,md}` — Cell 7 feasibility/closure (this session).
- `scripts/next_campaign_status.py` — campaign truth: frozen-but-unexecuted preregs and cached windows.
- `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md` — prior bounded liquidation-source negatives (2026-11-13T09:01Z).
- `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json` — terminal state.
- `research_state/evaluation_summary_FCLR-011.md` — sealed PASS (4.94%).
- `RESEARCH_PROMPT.md` §16, §17, §18, §19, §20.

---

## SESSION LOG (append-only; newest first)

## 2026-11-13T11:07:35Z — Kilo session: verified all six terminal gates PASS, all 125 targeted tests PASS, Cell 7 confirmed as sole executable cached task; no-actionable-preregs and no-funding-conditioned-window-confirmed

- **State verified (no sealed/raw/cache/workflow mutations):** All six terminal gates `GATE: PASS` — `fclr_heavy_confirm_gate.py`, `fclr_liq_010_confirm_gate.py`, `fclr_exp_robust_redo_gate.py`, `fclr_fwd_vol_2025_cross_gate.py`, `fclr_fwd_vol_2024_cross_gate.py`, `fclr_fwd_vol_2025h2_cross_gate.py` (Cell 6 executed 2026-11-13T10:22:40Z, verdict `NOT_REPLICATED`, rel −8.97%, CI excludes zero favouring B1, LOIO 0/5, placebo FAIL, Holm FAIL). Targeted suite `tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_next_campaign_status` → **125/125 OK**.
- **Campaign status confirmed clean:** `scripts/next_campaign_status.py` prints **no actionable frozen prereg** (every frozen prereg has an evaluation artifact) and correctly marks 2025-07..2025-10 as `TESTED` (Cell 6 window inside tested window). **No frozen-but-unexecuted prereg remains** — the failure mode that wasted ≥3 prior sessions is eliminated.
- **Funding-conditioned window exhaustion confirmed:** Ready disjoint funding-backed months (2025-01, 2025-06, 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04) are **single months only** — none can support ≥3 non-overlapping 30-day pre-registered test blocks with ~90-day train. No window supports a full funding-conditioned pre-registered test. This is a structural data limitation, not a search failure.
- **Sole remaining executable cached work — Cell 7 `FCLR-FWD-VOL-2024Q1-RV-DIAGNOSTIC`:** 2024-01..2024-03 (mark/premium/index klines complete for all 5 symbols; **no funding data** — funding starts 2024-04). This is a **volatility-only B0/B1 diagnostic; funding-conditioned hypotheses explicitly out of scope**. Pre-registered blocks: `0: 2024-01-03..2024-02-01`, `1: 2024-01-31..2024-03-01`, `2: 2024-02-28..2024-03-30` (train start 2024-01-01, 7-day embargo). Required: (1) coverage-only audit `research_state/coverage_audit_fwd_vol_2024q1_rv_diagnostic_<UTC>.{json,md}` — reuse `scripts/fclr_fwd_vol_2024_cross_coverage.py` template; (2) **feasibility decision** — if ≥3 blocks infeasible, record exact shortfall and close Cell 7 as `NOT_EXECUTABLE_DESIGN_SHORTFALL` (do not force funding-conditioned reading on window without funding); (3) if feasible, freeze prereg with `status=FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`, funding hypotheses out of scope, gate checks verbatim from 2024q4 prereg (materiality ≥2%, CI excludes zero, ≥5 instruments, ≥3 blocks, Holm, placebo 200 perms, 7-day embargo, 2000-replicate bootstrap, seed 20261113); (4) extend `scripts/fclr_fwd_vol_2024_cross.py` → `scripts/fclr_fwd_vol_2024q1_rv_diagnostic.py` with new prereg path, blocks, stems; (5) execute full (not `--smoke`); (6) create gate script printing `GATE: PASS`; (7) update `hypothesis_registry.json` (`H_fclr_fwd_vol_2024q1_rv_diagnostic`) and `experiment_frontier.json`.
- **Blocked (external only) — Gate 4 Branch 1:** Act only if `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` appears with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation. Currently absent; do not poll.
- **Evidence supported:** Sealed FCLR-011 PASS (+4.94%, 2026-05..2026-08) does **not** generalize to any disjoint tested window (2024 H2 rel −20.77%; 2025-02..2025-05 rel +0.29%; 2025-07..2025-10 rel −8.97%). **Contradicted:** any claim that cached funding-conditioned windows remain untested — all disjoint complete windows executed; remaining months structurally cannot support the pre-registered design. **Unknown:** whether any funding-conditioned volatility edge exists outside 2026-05..2026-08; whether external unauthenticated observed-liquidation data will appear.
- **Strongest alternative explanation:** Funding-conditioned volatility features (premium/ema_dist/abs_fund_pct) carry no stable out-of-sample signal for 24h RV; the sealed FCLR-011 PASS is a single-regime artifact.
- **Falsifying next test (highest IG/unit free compute):** Cell 7 coverage audit → if feasible, execute RV diagnostic. A material, CI-excluding-zero, LOIO-robust improvement on this disjoint pre-funding window would bear on volatility persistence (not funding conditioning — funding absent).
- **Artifacts/commands for next session:**
  ```bash
  python3 scripts/next_campaign_status.py                    # must print no actionable prereg; 2025-07..2025-10 inside_tested_window=True
  python3 scripts/fclr_fwd_vol_2025h2_cross_gate.py          # GATE: PASS — confirm artifact, do not re-run
  python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_next_campaign_status
  # Then Cell 7: coverage audit → feasibility decision → freeze/execute/gate/registry (or evidenced NOT_EXECUTABLE_DESIGN_SHORTFALL)
  ```

## 2026-11-13T11:01:33Z — Kilo session: reconciled handoff after Cell 6 execution; Cell 7 defined as next executable task; bottlenecks removed

- **State verified (no sealed/raw/cache/workflow mutations):** `scripts/fclr_fwd_vol_2025h2_cross_gate.py` → `GATE: PASS` (13/13) for Cell 6 `FCLR-FWD-VOL-2025H2-CROSS` executed 2026-11-13T10:22:40Z: verdict `NOT_REPLICATED`, pooled C2 vs B1 24h QLIKE mean diff +0.027446 (CI [0.002173, 0.071397] excludes zero favouring B1), rel −8.97%, p_boot 0.009; materiality FAIL, ci_excludes_zero_improving FAIL, LOIO 0/5 FAIL, placebo FAIL (null p95 −1.15% vs true −8.97%), Holm FAIL, leakage PASS. Registry `H_fclr_fwd_vol_2025h2_cross` terminal NOT_REPLICATED (`research_state/hypothesis_registry.json`, updated 2026-11-13T10:22:40Z). All five other terminal gates re-confirmed PASS.
- **Handoff corrected:** `AGENT_HANDOFF.md` was stale — it prescribed Cell 6 as "to execute this session" although it had already run at 10:22:40Z, a no-op-session risk. Header status, terminal ledger, generalization line, IMMEDIATE TASK, HARD BANS, and EXACT START COMMANDS updated; Cell 6 marked DONE; Cell 7 (`FCLR-FWD-VOL-2024Q1-RV-DIAGNOSTIC`, 2024-01..2024-03, volatility-only B0/B1, funding hypotheses out of scope) set as the executable next task with exact coverage-audit → feasibility-decision → freeze → execute → gate → registry steps and an evidenced `NOT_EXECUTABLE_DESIGN_SHORTFALL` closure path if 3 blocks are infeasible.
- **Bottlenecks removed:** (1) `scripts/next_campaign_status.py` TESTED_WINDOWS omitted Cell 6's 2025-07..2025-10 window and still printed tested months as READY — added the window; `tests/test_next_campaign_status.py` updated (2025-07..2025-10 now assert `inside_tested_window=True`). (2) Frontier rank-0 claim "no disjoint funding-backed window remains" reconciled against `next_campaign_status.py`: remaining READY months are 2025-01/2025-06 (single months, cannot support 3×30-day pre-registered blocks) and 2025-11..2026-04 (train would overlap the tested Cell 6 window); no window supports a full funding-conditioned pre-registered test; `experiment_frontier.json` rank-0 blockers/next_action/cells updated with Cell 6 terminal entry. (3) Stale-handoff-no-op risk closed: re-running terminal cells is banned.
- **Blocked, unchanged:** Gate 4 Branch 1 trigger absent (`fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`); no polling. Alt-source scan/deep-review 2026-11-13T09:01Z: no GO observed-liquidation candidate.
- **Evidence supported:** the sealed FCLR-011 funding-conditioned volatility PASS (+4.94%, 2026-05..2026-08) does **not** generalize to any disjoint tested window (2024 H2 rel −20.77%; 2025-02..2025-05 rel 0.29%; 2025-07..2025-10 rel −8.97% with C2 significantly worse than B1). **Contradicted:** frontier claim that no cached months remain untested — they remain but cannot support the pre-registered funding-conditioned design. **Unknown:** whether any funding-conditioned volatility edge exists outside the single 2026-05..2026-08 regime; whether external unauthenticated observed-liquidation data will appear.
- **Strongest alternative explanation:** funding-conditioned volatility features (premium/ema_dist/abs_fund_pct) carry no stable out-of-sample signal for RV; the sealed FCLR-011 PASS is a single-regime artifact.
- **Falsifying next test:** Cell 7 coverage audit of 2024-01..2024-03; if feasible, execute the RV diagnostic. A material CI-excluding-zero LOIO-robust improvement on this disjoint pre-funding window would bear on volatility persistence (not funding conditioning — funding data absent in Q1-2024).
- **Artifacts/commands:** `python3 scripts/next_campaign_status.py`; `python3 scripts/fclr_fwd_vol_2025h2_cross_gate.py` → `GATE: PASS`; targeted suite → OK; coverage-audit template `scripts/fclr_fwd_vol_2024_cross_coverage.py` to be adapted to Q1-2024 for Cell 7.

## 2026-11-13T10:16:45Z — Kilo session: verified all five terminal gates PASS, all 125 targeted tests PASS, confirmed next executable window (2025 H2)

- **State verified (no sealed/raw/cache/workflow mutations):** `fclr_heavy_confirm_gate.py` PASS (FCLR-FWD-VOL-011-CONFIRM NOT_REPLICATED, 7/7, repro Δ0.044pp); `fclr_liq_010_confirm_gate.py` PASS; `fclr_exp_robust_redo_gate.py` PASS (FRAGILE); `fclr_fwd_vol_2025_cross_gate.py` PASS (NOT_REPLICATED); `fclr_fwd_vol_2024_cross_gate.py` PASS (NOT_REPLICATED). Targeted suite `tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_next_campaign_status` → **125/125 OK**.
- **Heavy execution (new terminal evidence):** discovered `research_state/prereg_fclr_fwd_vol_2024q4_cross_20261113T091500Z.json` (status `FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`, frozen 2026-11-13T09:15:00Z) had **never been executed** — the executor/gate hardcoded the stem `2024_cross` while the prereg/coverage used `2024q4_cross`. Fixed the stem alignment, executed the cell on cached Binance 2024 H2 (5 symbols, 3 non-overlapping blocks 2024-07-23..2024-09-30, 7-day embargo, train from 2024-04-01, n_valid=10080, test n=8880 over 69 days): **verdict `NOT_REPLICATED`**. Pooled C2 vs B1 24h QLIKE mean diff **+0.091136**, 95% CI **[−0.012223, 0.256785]** (crosses zero, favours B1), rel reduction **−20.77%**, p_boot 0.185. `materiality_ge_2pct` FAIL; `ci_excludes_zero_improving` FAIL; `loio_ge_4_of_5` FAIL (0/5; only XRPUSDT positive at 7.56%); `placebo_pass` FAIL (null p95 −19.72% vs true −20.77%, 200 perms); `holm_pass` FAIL; `leakage_audit_pass` PASS; `instruments_ge_5` PASS; `blocks_ge_3` PASS. Horizon family: h168 C2_vs_B1 rel **+12.46%** (CI excludes zero) — the only horizon where C2 helped — but it is not the pre-registered primary (24h), not material, and not robust to LOIO/placebo. Artifacts: `research_state/evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.{md,json}`; panel `tracka_fwd_vol_2024q4_cross_panel_20261113T100451Z.parquet` (sha 5349fc34…); build report `tracka_fwd_vol_2024q4_cross_build_report_20261113T100451Z.json`. Gate `scripts/fclr_fwd_vol_2024_cross_gate.py` → `GATE: PASS` (13/13 checks).
- **Bottlenecks removed:** (1) the frozen-2024q4-prereg naming mismatch that made every prior session declare "nothing executable"; (2) the stale rank-0 campaign assertion in `tests/test_active_campaign_gate.py` (was failing on the committed HEAD); (3) frontier left at a completed campaign (now rank 0 = `FCLR-NEXT-CAMPAIGN-20261113T091500Z` `ACTIVE_HEAVY_CAMPAIGN`; `FCLR-HEAVY-CONFIRM-20261113T041200Z` demoted to rank 1); (4) obsolete "Execute Cell 1 FCLR-LIQ-010-CONFIRM" block removed.
- **Registry/frontier:** added `H_fclr_fwd_vol_2024q4_cross` = `NOT_REPLICATED` terminal (artifact 7122075e…, panel 5349fc34…, prereg e1a26ca5…); registry now 16 hypotheses; `updated_utc` 2026-11-13T10:04:51Z.
- **Evidence supported:** the FCLR-011 funding-conditioned volatility PASS does **not** generalize to 2024 H2 (the C2 degradation is a genuine period effect, not a pipeline defect — the same pipeline reproduces FCLR-011 at Δ0.044pp). **Contradicted:** the claim that no executable cached design remained. **Unknown:** whether any funding-conditioned volatility edge exists outside 2026-05..2026-08, and whether external unauthenticated observed-liquidation data will appear. **Dominant limitation:** only one genuinely favourable period (2026-05..2026-08) has ever been observed; every disjoint test has failed.
- **Strongest alternative explanation:** funding-conditioned volatility features (premium/ema_dist/abs_fund_pct) carry no stable out-of-sample signal for 24h RV; the sealed FCLR-011 PASS is a single-regime artifact.
- **Falsifying next test (highest IG/unit free compute):** execute Cell 6 `FCLR-FWD-VOL-2025H2-CROSS` — the complete, disjoint, never-tested 2025-07-23..2025-10-15 cached window with 5 instruments and 3 pre-registered 30-day blocks. A material, CI-excluding-zero, LOIO-robust, placebo-passing improvement would falsify the "single-regime artifact" conclusion.
- **Artifacts/commands:** `python3 scripts/fclr_fwd_vol_2024_cross.py`; `python3 scripts/fclr_fwd_vol_2024_cross_gate.py` → `GATE: PASS`; `python3 scripts/next_campaign_status.py`; the five gates above; the targeted suite → 125 OK; `research_state/evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.{md,json}`.

## 2026-11-13T10:11:51Z — Kilo session: unblocked and executed the never-run 2024q4 cell (NOT_REPLICATED, GATE: PASS); removed the false "nothing executable" closure; identified the next executable window (2025 H2)
## 2026-11-13T11:12:44Z — Kilo session: Cell 7 2024Q1 RV-diagnostic audited and closed NOT_EXECUTABLE_DESIGN_SHORTFALL; no executable cached heavy cell remains

- **State verified (no sealed/raw/cache/workflow mutations):** `python3 scripts/next_campaign_status.py` → no frozen-but-unexecuted preregs; 2025-07..2025-10 `inside_tested_window=True` (FCLR-FWD-VOL-2025H2-CROSS). No `research_state/*2024q1*rv*` or prereg artifacts existed prior. All six terminal cells remain terminal with `GATE: PASS` per prior handoff/registry; `FOCUS_CAMPAIGN.md`/`HANDOFF_NEXT_SESSION.md`/`NEXT_SESSION_TASK.md` remain redirects to this file.
- **Cell 7 coverage audit executed (new evidence, no outcomes computed):** `research_state/coverage_audit_fwd_vol_2024q1_rv_diagnostic_20261113T111244Z.{json,md}`. Window 2024-01-01T00:00:00Z..2024-03-31T23:00:00Z (~90.96 days). Cached 2024-01/02/03: mark/premium/index klines COMPLETE for 5 symbols; **funding ABSENT** (funding starts 2024-04) → volatility-only B0/B1 scope; funding-conditioned hypotheses out of scope.
- **Feasibility — NOT_EXECUTABLE_DESIGN_SHORTFALL:** Pre-registered rolling-origin blocks (train start 2024-01-01, 7-day embargo) yield block 0 train **~1.96 days** (test 2024-01-03..2024-02-01, train_end 2023-12-26T22:00:00Z relative to window) — insufficient for model fitting; block 1 train 28.96d, block 2 train 56.96d but tests overlap/partition infeasible in 90.96d. Minimal design for 3×30-day non-overlapping tests + 7-day embargo + ≥30-day train requires ≥141 days vs 90.96 available (deficit 50.04 days). No partition of 2024-01..2024-03 satisfies ≥3 non-overlapping 30-day test blocks with a meaningful train. **Decision:** Cell 7 closed as `NOT_EXECUTABLE_DESIGN_SHORTFALL`. No prereg frozen, no execution, no funding-conditioned reading forced.
- **Campaign exhaustion (structural):** All disjoint funding-backed cached windows executed (2024H2, 2025-02..05, 2025-07..10, plus sealed 2026-05..08). Remaining READY funding-backed months (2025-01, 2025-06, 2025-11, 2025-12, 2026-01..2026-04) are single months or otherwise cannot support 3×30-day pre-registered blocks with ~90-day train without overlapping tested windows — no full funding-conditioned pre-registered test executable from cache. 2024-01..03 is the only other complete cached window and is infeasible (above). `next_campaign_status.py` remains the source of truth.
- **Blocked (external only), unchanged:** Gate 4 Branch 1 — no `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) present; do not poll. Alt-source scan/deep-review 2026-11-13T09:01Z: no GO unauthenticated observed-liquidation candidate; bounded discovery allowed only against a *specific new* candidate with admissibility audit → prereg → execute → terminal verdict → gate.
- **Evidence:** Supported — sealed FCLR-011 PASS (+4.94%, 2026-05..2026-08) does not generalize to any disjoint tested window (2024H2 −20.77%, 2025H1-cross +0.29%, 2025H2 −8.97%, C2 worse in last). Contradicted — any claim of an unexecuted cached funding-conditioned or feasible cached RV-diagnostic heavy cell. Unknown — funding-conditioned volatility edge outside 2026-05..2026-08; external observed-liquidation source emergence.
- **Strongest alternative explanation:** Funding-conditioned volatility features carry no stable out-of-sample 24h RV signal; FCLR-011 is a single-regime artifact.
- **Dominant limitation:** Cache cannot support another pre-registered 3×30-day test design (funding windows exhausted; 2024Q1 too short / no funding).
- **Falsifying next test:** A newly admissible observed-liquidation source or a valid Gate 4 RESOLVED trigger enabling a pre-registered execution; absent that, no cached falsification path remains.
- **Highest IG/unit free compute:** If a *specific new* external liquidation-data candidate appears, run §16 admissibility audit and freeze prereg before outcomes; otherwise record any newly evidenced negative with exact failing minimum. No status-only work.
- **Artifacts:** `research_state/coverage_audit_fwd_vol_2024q1_rv_diagnostic_20261113T111244Z.json`, `research_state/coverage_audit_fwd_vol_2024q1_rv_diagnostic_20261113T111244Z.md`, `scripts/next_campaign_status.py` (no actionable prereg).
