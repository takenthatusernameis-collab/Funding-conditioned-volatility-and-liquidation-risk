# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-13T10:11:51Z
**Status:** `NEXT_CELL_READY_TO_EXECUTE` — Five volatility/liquidation cells are now terminal with gates PASS. One frozen, pre-outcomes, never-executed cell was unblocked and executed this session (`FCLR-FWD-VOL-2024Q4-CROSS` → `NOT_REPLICATED`), and **one further fully-executable cached window (2025-07..2025-10) is identified and ready to execute with no new data needed.**

Terminal ledger (all `GATE: PASS`):

| Cell | Verdict | Headline |
|---|---|---|
| FCLR-FWD-VOL-011-CONFIRM | `NOT_REPLICATED` | forward C2 rel −5.55%, CI favours B1, repro Δ0.044pp |
| FCLR-LIQ-010-CONFIRM | `NOT_REPLICATED` | rel 0.501% < 2% floor, LOIO 0/17, placebo fail |
| FCLR-EXP-ROBUST-REDO | `FRAGILE` | LOIO 4/8, placebo fail |
| FCLR-FWD-VOL-2025-CROSS | `NOT_REPLICATED` | rel 0.29%, CI crosses zero, LOIO 0/5 |
| **FCLR-FWD-VOL-2024Q4-CROSS** | **`NOT_REPLICATED`** | **rel −20.77% (C2 worse), CI crosses zero, LOIO 0/5, placebo fail** |

Sealed FCLR-011 PASS (4.94%) remains unrefuted but does not generalize forward, to 2024 H2, or to 2025 H1. `H1_primary` is `NOT_SUPPORTED`.

**This file is the ONLY durable handoff.** Supersedes earlier handoffs/checkpoints. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. Do not create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file. Update in place by appending a dated `## SESSION LOG` entry.

---

## READ THIS FIRST — THE TWO BOTTLENECKS THAT CAUSED PAST SESSIONS TO WASTE CYCLES

1. **"No frozen prereg remains" was FALSE.** A valid, genuinely pre-outcomes prereg
   (`research_state/prereg_fclr_fwd_vol_2024q4_cross_20261113T091500Z.json`, 2026-11-13T09:15:00Z) had been
   frozen but **never executed**, because the executor and gate hardcoded the filename stem
   `2024_cross` while the prereg was written as `2024q4_cross`. The result: every session concluded
   "nothing executable" and stopped. **Always check for frozen preregs whose experiment id has no
   matching evaluation artifact before declaring a campaign closed.** Use:
   ```bash
   python3 scripts/next_campaign_status.py     # prints frozen-but-unexecuted preregs and ready windows
   ```
2. **A stale test asserted the old rank-0 campaign** and failed after the campaign advanced
   (`'COMPLETED_CAMPAIGN_NEXT_PREREG_REQUIRED' != 'ACTIVE_HEAVY_CAMPAIGN'`). The contract is now
   campaign-agnostic: rank 0 must be `ACTIVE_HEAVY_CAMPAIGN`; superseded campaigns must be demoted to
   rank 1, never deleted.

---

## IMMEDIATE TASK (mandatory, heavy-first, in this order)

**Priority = repo name:** advance *funding-conditioned volatility and liquidation risk* by producing **new terminal evidence**. Re-running terminal cells, identical no-op probes, Gate 4 polling, or monitor-only closure is forbidden.

### Cell 6 (execute this session — no new data, no new prereg needed beyond one freeze): `FCLR-FWD-VOL-2025H2-CROSS`
This is the highest expected information gain per unit of free compute. A 2025-07-23..2025-10-15 window over the
cached Binance archive is **disjoint from every tested window** (2024 H2, 2025-02..2025-05, 2026-05..2026-08,
2026-08..2026-10) and is fully materialized on disk:

- Data verified present: 5 symbols × complete hourly mark/premium/index klines for 2025-04..2025-10,
  funding files for all 12 months of 2025. Per-symbol finite rows for a 2025-04-01..2025-11-30 build:
  BTC/ETH/BNB/SOL 5,832 `target_24h` rows each, XRP 5,784.
- Proposed pre-registered blocks (rolling-origin, 7-day embargo, train start 2025-04-01):
  `0: train_end 2025-07-16, test 2025-07-23..2025-08-21`;
  `1: train_end 2025-08-13, test 2025-08-20..2025-09-18`;
  `2: train_end 2025-09-09, test 2025-09-16..2025-10-15`.
- Steps: (1) write a **coverage-only** audit `research_state/coverage_audit_fwd_vol_2025h2_cross_<UTC>.{json,md}`
  (finite-row counts only, no outcome statistic) — reuse `scripts/fclr_fwd_vol_2024_cross_coverage.py` as the template;
  (2) freeze `research_state/prereg_fclr_fwd_vol_2025h2_cross_<UTC>.{json,md}` with
  `status=FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`, copying the gate block verbatim
  from the 2024q4 prereg (materiality ≥2%, CI excludes zero, ≥5 instruments, ≥3 blocks, Holm, LOIO ≥4/5,
  placebo 200 perms, 7-day embargo, 2000-replicate bootstrap, seed 20261113);
  (3) extend `scripts/fclr_fwd_vol_2024_cross.py` (or copy it to `scripts/fclr_fwd_vol_2025h2_cross.py`) with the new
  prereg path, the new blocks, and the new `tracka_fwd_vol_2025h2_cross_*` / `evaluation_summary_FCLR-FWD-VOL-2025H2-CROSS-*` stems;
  (4) run it (full, not `--smoke`; it takes ~4 min) and create `scripts/fclr_fwd_vol_2025h2_cross_gate.py`
  that prints `GATE: PASS`;
  (5) update `hypothesis_registry.json` (`H_fclr_fwd_vol_2025h2_cross`) and `experiment_frontier.json`.
- **Do not** reuse an already-tested window, and do not tune features/horizons after seeing outcomes.

### Cell 7 (only if Cell 6 is completed and a further untested window remains)
The only other complete, untested, materially different cached window is **2024-01..2024-03** (complete
mark/premium/index; funding from 2024-04 does not cover it, so `signed_funding`/`abs_fund_pct` would be
absent — that makes it a **volatility-only B0/B1-only design, not a funding-conditioned test**). Do not
force it: only freeze it as a *baseline-only RV-diagnostic* cell with the funding hypotheses explicitly out of scope.
Prefer Cell 6 and Track A over this.

### Cell 8 (Track A, liquidation) — only if a *specific new* candidate emerges
Bounded discovery is allowed only against a concrete candidate not already falsified in
`research_state/alt_source_scan_latest.json` + `research_state/alt_source_deep_review_latest.md`
(2026-11-13T09:01Z). If found: admissibility audit → freeze prereg → execute → terminal verdict → gate.
If nothing new: record **new** concrete evidence (source, URL, observed fields, exact failing minimum) — do not
restate prior negatives.

### Blocked (external only) — Gate 4 Branch 1
Act only if `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` appears with `status=RESOLVED_VERIFIED`,
`fabricated=false`, and human/legal attestation. Currently absent; do not wait/poll.

### Completion (session is DONE only if one holds)
1. **Heavy execution complete:** coverage audit (if required) + frozen pre-outcomes prereg + timestamped terminal
   evaluation + registry/frontier updated + new fail-closed gate `GATE: PASS` + targeted tests green.
2. **Evidence-advancing discovery only:** timestamped audit/probe artifact showing a **previously-unrecorded**
   concrete failing minimum or newly discovered candidate (with exact fields/coverage), state updated.

Always run and report:
```bash
python3 scripts/fclr_heavy_confirm_gate.py
python3 scripts/fclr_liq_010_confirm_gate.py
python3 scripts/fclr_exp_robust_redo_gate.py
python3 scripts/fclr_fwd_vol_2025_cross_gate.py
python3 scripts/fclr_fwd_vol_2024_cross_gate.py
python3 scripts/next_campaign_status.py
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_next_campaign_status
```
No sealed mutation; no raw cache commits; no `.github/workflows/*` changes.

---

## HARD BANS (enforced)

- **No status-only sessions.** Do not re-verify gates and stop; that is not progress.
- **No "nothing executable" closure without running `python3 scripts/next_campaign_status.py`** and recording its output. This exact failure mode wasted ≥3 sessions.
- No threshold shopping, post-hoc feature/model/universe changes, or reuse of an inspected window as fresh confirmation.
- No zero-fill/forward-fill to force comparability (legacy reproduction zero-fill for non-core features is documented).
- No mutation of sealed FCLR-011/012-V/013/014 artifacts; no re-labelling a PASS as NOT_SUPPORTED.
- No agent-set Gate 4 `RESOLVED_VERIFIED`; no paid/manual/credentialed data; no `.github/workflows/*` patches.
- Do not commit raw cache or `data_cache/` contents.

---

## BOTTLENECKS REMOVED THIS SESSION

| Bottleneck | Resolution |
|---|---|
| **Frozen 2024q4 prereg never executed** because executor/gate hardcoded stem `2024_cross` vs actual `2024q4_cross` | Aligned `scripts/fclr_fwd_vol_2024_cross.py` and `..._gate.py` to the `2024q4` / `2024Q4` stems; derived artifact paths from the prereg. Cell executed → `NOT_REPLICATED`, `GATE: PASS`. |
| **"No frozen prereg remains executable" false closure claim** | Corrected in this handoff; added `scripts/next_campaign_status.py` to list frozen-but-unexecuted preregs and ready windows. |
| **Stale test hardcoded old rank-0 campaign** | `tests/test_active_campaign_gate.py` now asserts rank 0 is an `ACTIVE_HEAVY_CAMPAIGN` from `{FCLR-HEAVY-CONFIRM…, FCLR-NEXT-CAMPAIGN…}`; superseded campaign demoted to rank 1. |
| Frontier rank-0 left at a completed campaign | Rank 0 = `FCLR-NEXT-CAMPAIGN-20261113T091500Z` (`ACTIVE_HEAVY_CAMPAIGN`); `FCLR-HEAVY-CONFIRM-20261113T041200Z` demoted to rank 1. |
| Obsolete "Execute Cell 1 FCLR-LIQ-010-CONFIRM" instruction (already terminal) | Removed; superseded. |
| 2024 H2 window declared "not tested anywhere" but unexecuted | Executed; 2024 H2 now terminal `NOT_REPLICATED`. |
| 2025 H2 window never evaluated despite complete cache | Identified as executable (5,832 target rows/symbol); documented as Cell 6 with exact blocks. |

---

## EXACT START COMMANDS

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk

# Preflight
python3 -c "import numpy,pandas,scipy,pyarrow; print('deps OK')"

# What is actually left? (frozen-but-unexecuted preregs + ready cached windows)
python3 scripts/next_campaign_status.py

# Gate 4 external trigger (expected absent; do not poll)
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"

# Confirm all five terminal cells are green
python3 scripts/fclr_heavy_confirm_gate.py
python3 scripts/fclr_liq_010_confirm_gate.py
python3 scripts/fclr_exp_robust_redo_gate.py
python3 scripts/fclr_fwd_vol_2025_cross_gate.py
python3 scripts/fclr_fwd_vol_2024_cross_gate.py

# Targeted suite
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_next_campaign_status

# Then execute Cell 6 (FCLR-FWD-VOL-2025H2-CROSS) per the IMMEDIATE TASK
```

---

## DEFINITION OF DONE (answer in the handoff)

- What did the evidence support, contradict, or leave unknown?
- Strongest alternative explanation?
- Which data/label/inference limitation dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- Exact artifact and command/test demonstrating progress.

---

## KEY REFERENCES

- `research_state/prereg_fclr_fwd_vol_2024q4_cross_20261113T091500Z.{json,md}` — frozen prereg, executed this session.
- `research_state/coverage_audit_fwd_vol_2024q4_cross_20261113T091427Z.json` — coverage-only audit template (5 symbols, 3 blocks).
- `scripts/fclr_fwd_vol_2024_cross.py` — the executor to copy for Cell 6.
- `scripts/fclr_fwd_vol_2024_cross_coverage.py` — the coverage-audit template for Cell 6.
- `scripts/fclr_fwd_vol_2024_cross_gate.py` — the gate template for Cell 6.
- `research_state/evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.{md,json}` — this session's result.
- `scripts/fclr_fwd_vol_confirm.py` — shared models/features/`bootstrap_diff`/`holm` machinery.
- `scripts/next_campaign_status.py` — campaign truth: frozen-but-unexecuted preregs and ready windows.
- `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json` — updated this session.
- `research_state/evaluation_summary_FCLR-011.md` — the sealed PASS (4.94%).
- `RESEARCH_PROMPT.md` §16, §17, §18, §19, §20.

---

## SESSION LOG (append-only; newest first)

## 2026-11-13T10:11:51Z — Kilo session: unblocked and executed the never-run 2024q4 cell (NOT_REPLICATED, GATE: PASS); removed the false "nothing executable" closure; identified the next executable window (2025 H2)

- **State verified (no sealed/raw/cache/workflow mutations):** `fclr_heavy_confirm_gate.py` PASS (FCLR-FWD-VOL-011-CONFIRM NOT_REPLICATED, 7/7, repro Δ0.044pp); `fclr_liq_010_confirm_gate.py` PASS; `fclr_exp_robust_redo_gate.py` PASS (FRAGILE); `fclr_fwd_vol_2025_cross_gate.py` PASS (NOT_REPLICATED); `fclr_fwd_vol_2024_cross_gate.py` PASS (NOT_REPLICATED). Targeted suite `tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate` → **119/119 OK**.
- **Heavy execution (new terminal evidence):** discovered `research_state/prereg_fclr_fwd_vol_2024q4_cross_20261113T091500Z.json` (status `FROZEN_PRE_OUTCOMES`, `outcome_data_inspected_before_freeze=false`, frozen 2026-11-13T09:15:00Z) had **never been executed** — the executor/gate hardcoded the stem `2024_cross` while the prereg/coverage used `2024q4_cross`. Fixed the stem alignment, executed the cell on cached Binance 2024 H2 (5 symbols, 3 non-overlapping blocks 2024-07-23..2024-09-30, 7-day embargo, train from 2024-04-01, n_valid=10080, test n=8880 over 69 days): **verdict `NOT_REPLICATED`**. Pooled C2 vs B1 24h QLIKE mean diff **+0.091136**, 95% CI **[−0.012223, 0.256785]** (crosses zero, favours B1), rel reduction **−20.77%**, p_boot 0.185. `materiality_ge_2pct` FAIL; `ci_excludes_zero_improving` FAIL; `loio_ge_4_of_5` FAIL (0/5; only XRPUSDT positive at 7.56%); `placebo_pass` FAIL (null p95 −19.72% vs true −20.77%, 200 perms); `holm_pass` FAIL; `leakage_audit_pass` PASS; `instruments_ge_5` PASS; `blocks_ge_3` PASS. Horizon family: h168 C2_vs_B1 rel **+12.46%** (CI excludes zero) — the only horizon where C2 helped — but it is not the pre-registered primary (24h), not material, and not robust to LOIO/placebo. Artifacts: `research_state/evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.{md,json}`; panel `tracka_fwd_vol_2024q4_cross_panel_20261113T100451Z.parquet` (sha 5349fc34…); build report `tracka_fwd_vol_2024q4_cross_build_report_20261113T100451Z.json`. Gate `scripts/fclr_fwd_vol_2024_cross_gate.py` → `GATE: PASS` (13/13 checks).
- **Bottlenecks removed:** (1) the frozen-2024q4-prereg naming mismatch that made every prior session declare "nothing executable"; (2) the stale rank-0 campaign assertion in `tests/test_active_campaign_gate.py` (was failing on the committed HEAD); (3) frontier left at a completed campaign (now rank 0 = `FCLR-NEXT-CAMPAIGN-20261113T091500Z` `ACTIVE_HEAVY_CAMPAIGN`; `FCLR-HEAVY-CONFIRM-20261113T041200Z` demoted to rank 1); (4) obsolete "Execute Cell 1 FCLR-LIQ-010-CONFIRM" block removed.
- **Registry/frontier:** added `H_fclr_fwd_vol_2024q4_cross` = `NOT_REPLICATED` terminal (artifact 7122075e…, panel 5349fc34…, prereg e1a26ca5…); registry now 16 hypotheses; `updated_utc` 2026-11-13T10:04:51Z.
- **Evidence supported:** the FCLR-011 funding-conditioned volatility PASS does **not** generalize to 2024 H2 (the C2 degradation is a genuine period effect, not a pipeline defect — the same pipeline reproduces FCLR-011 at Δ0.044pp). **Contradicted:** the claim that no executable cached design remained. **Unknown:** whether any funding-conditioned volatility edge exists outside 2026-05..2026-08, and whether external unauthenticated observed-liquidation data will appear. **Dominant limitation:** only one genuinely favourable period (2026-05..2026-08) has ever been observed; every disjoint test has failed.
- **Strongest alternative explanation:** funding-conditioned volatility features (premium/ema_dist/abs_fund_pct) carry no stable out-of-sample signal for 24h RV; the sealed FCLR-011 PASS is a single-regime artifact.
- **Falsifying next test (highest IG/unit free compute):** execute Cell 6 `FCLR-FWD-VOL-2025H2-CROSS` — the complete, disjoint, never-tested 2025-07-23..2025-10-15 cached window with 5 instruments and 3 pre-registered 30-day blocks. A material, CI-excluding-zero, LOIO-robust, placebo-passing improvement would falsify the "single-regime artifact" conclusion.
- **Artifacts/commands:** `python3 scripts/fclr_fwd_vol_2024_cross.py`; `python3 scripts/fclr_fwd_vol_2024_cross_gate.py` → `GATE: PASS`; `python3 scripts/next_campaign_status.py`; the five gates above; the targeted suite → 119 OK; `research_state/evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.{md,json}`.