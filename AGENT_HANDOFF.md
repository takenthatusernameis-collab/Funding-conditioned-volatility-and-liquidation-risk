# AGENT HANDOFF — 2026-11-14T07:33:46Z (single durable handoff)

## INITIAL TASK FOR NEXT AGENTIC WORK SESSION (MANDATORY, HEAVY, OFFLINE, UNBLOCKED)

**Do this first. Do not produce a status-only, inventory-only, or planning-only response.**

1. **PRIMARY (must complete in this session unless a hard local error is hit): Phase B — implement and run `TRACKA-LIQ-EXPANSION-RECOMPUTE`.**
   - `scripts/fclr_liq_expansion_recompute.py` does **not** exist. Create it.
   - Freeze `research_state/prereg_tracka_liq_expansion_recompute_20261114T073346Z.{json,md}` **before any outcome computation** (`FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `pre_registered_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`, `promotable=false`, `max_status=EXPLORATORY_ONLY`).
   - Rebuild the panel from caches (**not** from the sealed parquet): `research_state/data_cache/ironflow_events/2026-05..2026-10.parquet` + `research_state/data_cache/hyperliquid_funding/{ZEC,NEAR,UNI,AAVE,CRV,ADA,LTC,BCH}.json` + `research_state/data_cache/hyperliquid_candles/{SYM}/2026-05..2026-10.json`. **Do not use `ironflow_bulk` (stops at 2026-04).**
   - Recompute B0/B1/C1/C2 with train-only fit/scaling/smearing on the frozen sealed design/splits; run paired 24h/circular block bootstrap (2000 deterministic reps), Holm over `C2_vs_B1/C1_vs_B1/C2_vs_C1`, LOIO, funding-permutation placebo, per-symbol/per-block stability, leakage audit.
   - Emit `research_state/tracka_liq_expansion_recompute_panel_<UTC>.parquet`, `..._panel_build_report_<UTC>.json`, `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-<UTC>.{json,md}` with verdict `REPRODUCED|NOT_REPRODUCED|INCONCLUSIVE|INADMISSIBLE` and an explicit statement of whether sealed **19.04%** C2-vs-B1, **LOIO 4/8**, and the **placebo failure** replicate. Preserve all sealed artifacts.
   - Add targeted `unittest` tests for prereg frozen fields, panel-hash consistency, non-empty contrasts, and sealed-artifact immutability.
2. **SECONDARY (only after Phase B artifacts/tests/gates are done, or if Phase B hits a provable hard stop with exact failing minima): Phase A — fix and rerun FCLR-011 recompute.** Phase A is capped `INCONCLUSIVE/EXPLORATORY`; see diagnosis below. Do **not** let Phase A displace Phase B.
3. **AFTER EACH PHASE (atomically):** update `research_state/experiment_frontier.json` and `research_state/hypothesis_registry.json` (audit-only; do not alter sealed statuses), append to `research_state/negative_results_report.md` and `research_state/leakage_audit.md`, append a dated session log here, and verify `/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all` (expect 19/19) plus targeted gate tests.

This handoff **supersedes all prior handoffs**, including 2026-11-14T06:35:00Z and 06:25:08Z.
Prior handoff claimed Phase A `READY_EXECUTE` and Phase B pending on `ironflow_bulk` — **both false**.
Phase A is a design/implementation dead-end as written (empty contrasts, double-assemble bug); Phase B
has no implementation but **all required inputs are present**. This file removes those bottlenecks.

### What I verified myself (do not re-verify, do not re-litigate)
| Claim | Verified result | Evidence |
|---|---|---|
| Campaign gate | **19/19 PASS** | `/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all` |
| Deps | `pyarrow 26.0.1, pandas 3.1.1, numpy 2.5.4, scipy 1.18.1` present **only** in `/tmp/fclr-venv` | system `python3` lacks `pyarrow` |
| Gate tests | 34 tests OK (`tests.test_active_campaign_gate`, `tests.test_fclr_campaign_gate`) | `/tmp/fclr-venv/bin/python -m unittest ...` |
| Artifact guard | `research_state` root = 419 md/json, 419 tracked, 0 untracked — consistent | `scripts/tracka_resume_check.py` `root_md_json_bounded` |
| Phase A prereg freeze | works, exits 0 | `fclr011_recompute_audit.py --write-prereg --out-utc <UTC>` |
| **Phase A full run** | **exits 0 but verdict `INCONCLUSIVE`, empty contrasts** | `inconclusive_reason: "model C1 not fittable on train rows"` |
| **Phase A root cause** | **structural, not data-missing** | see diagnosis below |
| **Phase B script** | **DOES NOT EXIST** | `ls scripts/*recompute*` → only `fclr011_recompute_audit.py` |
| Phase B inputs | **all present and sufficient** | see Phase B section |

### PHASE A DIAGNOSIS — why "just run it" fails (do not repeat the failed command)
`scripts/fclr011_recompute_audit.py` computes the frozen `CORE_FEATURES` list, which requires
`log_rv168h` (7-day rolling RV). Because the target is 24h-ahead RV, the first **168 + 24 = 192**
hourly rows of every symbol have no `log_rv168h`. Measured on the real panel I built:

```
train rows 9096 → complete (with 168h) = 152  → B1 fits on only {BNBUSDT, BTCUSDT}
                              complete (no 168h) = 1218
per-symbol train log_rv168h non-null: BTC 72, BNB 145, ETH 0, SOL 0, XRP 0
validation: 2798 with / 3541 without;  test: 10905 with / 10905 without
```

`run_audit()` then requires **all** of B0/B1/C1/C2 to fit on `train_core`, and C1/C2 need the
complete-case rows — only 152 exist, so it returns `INCONCLUSIVE` before any contrast is computed.
**The prereg is frozen and correct. The panel is correct. The failure is the 168h feature in the
train window, not missing data and not a broken prereg.**

**There is also a real code bug you must fix or the run reports the wrong thing:**
`main()` calls `assemble_panel(MONTHS)` (all 8 months) and writes the parquet, then
`run_audit(prereg, out_utc, smoke)` calls `assemble_panel(months)` **again** with
`months = ["2026_05","2026_06"] if smoke else MONTHS`. So `--smoke` and a full run produce an
**identical panel SHA-256** (`41962f82...`), and the emitted `build`/`coverage` block describes a
*second* panel that does not match the parquet on disk. Fix: pass the already-built `panel`/`build`
into `run_audit` instead of rebuilding, or gate `--smoke` on the month list.

### PHASE A — APPROVED EXECUTION PATH (do this, in order)
1. **Do not** re-run the bare full command from the old handoff; it is already known to return
   `INCONCLUSIVE`. That result is *correct* given the current code, but it is not a research finding —
   it is a design bug.
2. **Fix the double-assemble bug** in `scripts/fclr011_recompute_audit.py` (see above). Add a test in
   `tests/` asserting that a `--smoke` run and a full run produce **different** panel hashes, and that
   `build.rows_total` equals `len(panel)` for the parquet that was written. This is a real,
   heavy, verifiable code change — not status churn.
3. **Decide the 168h design with a frozen decision, before touching outcomes.** Two admissible options;
   pick one and record it in the prereg delta, do not tune after seeing results:
   - **(A1, preferred) Warm-up exclusion with an honest split:** drop `log_rv168h` from
     `CORE_FEATURES`/B1 for the **train** fit only, keep the 168h feature out of the frozen design
     entirely, and re-freeze B1 as `HAR-RV` = `log_rv1h + log_rv24h`. This raises train complete rows
     from 152 → **1218** and is a clean, defensible, fully-specified model. All four models stay
     nested (B0 ⊂ B1 ⊂ C1 ⊂ C2).
   - **(A2) Extend the train window backwards** into 2025 so 168h is warm by 2026-01-01. This needs
     `BTCUSDT_2025_11`/`2025_12` (and the other four symbols) in
     `research_state/data_cache/`; check before choosing — if absent, A2 is data-blocked and you must
     use A1.
4. Freeze `research_state/prereg_fclr011_recompute_20261114T042139Z.json` + `.md` again **only if**
   the frozen design genuinely changes (A1 changes B1, so yes). Keep `status=FROZEN_PRE_OUTCOMES`,
   `frozen_before_outcomes=true`, `pre_registered_before_outcomes=true`,
   `outcome_data_inspected_before_freeze=false`, `promotable=false`, `max_status=EXPLORATORY_ONLY`,
   `audit_only=true`, `does_not_reopen_sealed_verdict=true`.
5. Run the fixed script end-to-end with an explicit `--out-utc`. Assert the emitted verdict is one of
   `REPRODUCED|NOT_REPRODUCED|INCONCLUSIVE|INADMISSIBLE`, that `contrasts` is **non-empty**, and that
   the panel SHA-256 in the JSON matches the parquet on disk. Emit
   `research_state/evaluation_summary_FCLR-011-RECOMPUTE-<UTC>.{json,md}`.
6. **Stop rule (do not relax after outcomes):** instruments < 5, test blocks < 3, or core coverage
   < 0.80 ⇒ bounded `INADMISSIBLE/INCONCLUSIVE` NO_GO with the exact failing minima.

---

## PHASE B — NOW THE PRIMARY HEAVY TASK (Phase A is capped at INCONCLUSIVE/EXPLORATORY)

Phase B is **not** blocked and **not** waiting on Phase A. It has a bigger budget and real data.
**You must implement it from scratch — no script exists.** Do not look for one; write it.

**Target:** independently recompute the sealed Track A liquidation expansion PASS
`TRACKA-HL-EXPANSION-20261111T195500Z`, on the frozen 2026-05..2026-10 window, and its FRAGILE
robustness result. **Sealed reference (do not re-score, do not overwrite):**
`research_state/tracka_hl_expansion_eval_result_20261111T202344Z.json` —
`C2_vs_B1 rel_reduction_pct = 19.0371`, `mean_diff = -2.70974`, `ci = [-5.088102, -0.477660]`,
`n_pairs = 593`, `n_blocks = 3`, `paired_symbols = [AAVE, ADA, BCH, CRV, LTC, NEAR, UNI, ZEC]`;
`C1_vs_B1 = 9.6794%`; `C2_vs_C1 = 10.3605%`. Robustness: LOIO 4/8, placebo null p95 21.10%.
Sealed panel `tracka_hl_expansion_panel_20261111T202344Z.parquet`,
sha256 `39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699` (1472 buckets, 1203 with
label, 1168 complete label+funding+rv). **Do not modify it.**

**Inputs — verified present and sufficient (this is why Phase B is unblocked):**
- Labels: `research_state/data_cache/ironflow_events/2026-05..2026-10.parquet` — 1,264,105 rows total,
  columns `timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills,
  block, tx_hash`. **Observed Hyperliquid liquidation labels only.** No modeled/proxy/synthetic, no
  venue mixing.
- Funding: `research_state/data_cache/hyperliquid_funding/{ZEC,NEAR,UNI,AAVE,CRV,ADA,LTC,BCH}.json` —
  **all 8 symbols, 4,416 funding rows each, coverage 1777593600045..1793487600044**, unauthenticated,
  no API key, `fundingRate` + `premium` per row.
- 1h candles: `research_state/data_cache/hyperliquid_candles/{SYM}/2026-05..2026-10.json` — all 8
  symbols, all 6 months, `.accessed.json` + `.sha256` provenance present.
- `ironflow_bulk/{liquidations,candles_1h,funding,open_interest}` covers **2025-05..2026-04 only** —
  it does **not** reach 2026-05..2026-10. **Do not plan on it for Phase B.** Use `ironflow_events` +
  `hyperliquid_*` caches above.

**Implementation requirements (these are the whole point of the task):**
1. **Write** `scripts/fclr_liq_expansion_recompute.py` (new file, ~600-900 lines is fine; mirror the
   structure and rigor of `fclr011_recompute_audit.py`).
2. **Freeze a prereg BEFORE computing any outcome**: `research_state/
   prereg_tracka_liq_expansion_recompute_20261114T042139Z.{json,md}` with the same
   `FROZEN_PRE_OUTCOMES` field set as Phase A. Include the frozen splits, the 3 registered contrasts
   (`C2_vs_B1`, `C1_vs_B1`, `C2_vs_C1`), the 24h/UTC-day circular block bootstrap, Holm, LOIO,
   funding-permutation placebo, and the stop rule.
3. **Rebuild the panel from the caches** (not from the sealed parquet — that would be circular).
   Emit `research_state/tracka_liq_expansion_recompute_panel_<UTC>.parquet` +
   `..._panel_build_report_<UTC>.json` with per-coin row counts, coverage, label/funding/rv
   completeness, and input SHA-256s.
4. **Recompute** B0/B1/C1/C2 with train-only fit/scaling/smearing, evaluate on the frozen test window,
   report QLIKE/MAE/RMSE, paired block bootstrap (2000 deterministic reps), Holm over the 3 contrasts,
   LOIO, funding-permutation placebo, per-symbol/per-block stability, and a leakage audit.
5. Emit `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-<UTC>.{json,md}` with verdict
   `REPRODUCED|NOT_REPRODUCED|INCONCLUSIVE|INADMISSIBLE`, all `EXPLORATORY_ONLY`, `promotable=false`.
   **State explicitly whether the 19.04% survives and whether LOIO 4/8 and the placebo failure
   replicate.** Do not promote, do not reopen the sealed verdict.
6. **Stop rule:** instruments < 5, test blocks < 3, or insufficient core coverage ⇒ bounded
   `INADMISSIBLE/INCONCLUSIVE` NO_GO with exact failing minima. No threshold relaxation post-outcomes.
7. **Add tests** under `tests/` (unittest style, matching the repo) covering: prereg frozen-field
   assertion, panel-hash consistency, non-empty contrasts, and that sealed artifacts are unchanged.

**Sequencing:** Phase B first if you want guaranteed heavy, decisive output. Phase A is optional and
capped. Do **both** if time allows, but never emit a report that only describes Phase A.

---

## AFTER EACH PHASE (atomically, non-optional)
- Update `research_state/experiment_frontier.json` (advance/record phase status; keep rank 0 truthful).
- Add an audit hypothesis to `research_state/hypothesis_registry.json` (do not alter sealed statuses).
- Append to `research_state/negative_results_report.md` and `research_state/leakage_audit.md`.
- Append a dated session log entry below with commands, key results/hashes, verdicts, blockers.
- Re-run `/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all` (expect 19/19) and targeted gate tests:
  `/tmp/fclr-venv/bin/python -m unittest tests.test_active_campaign_gate tests.test_fclr_campaign_gate`.
  **Note:** `pytest` is not installed and full `unittest discover` exceeds a 2-minute shell timeout — run targeted modules.
- **Definition of done for this session:** Phase B implementation + frozen prereg + rebuilt panel + evaluation summary + tests + gate verification committed as artifacts in working tree (or a documented hard stop with exact failing minima and no false NO_GO). Any other outcome is insufficient progress.

## ENVIRONMENT FACTS (do not rediscover)
- Use **`/tmp/fclr-venv/bin/python`** for everything needing `pyarrow`/`pandas`/`numpy`/`scipy`.
  System `python3` fails with `ModuleNotFoundError: pyarrow`.
- `pytest` is not installed; tests are `unittest`. Target specific modules.
- No network. No `.github/workflows/*` edits. No raw parquet/cache commits. No sealed-artifact
  overwrites. No fabricated artifacts/thresholds/p-values/verdicts.
- Unresolved Git-LFS pointer: `research_state/data_cache/fclr011_panel.json`. **Do not wait for LFS** —
  Phase A rebuilds from cache by design.
- Invariants: preregister before outcome inspection; observed ≠ modeled labels; no venue mixing; no
  forward-fill/synthetic; no May 2026/sealed holdout scoring; no terminal verdict reopening.

---

## Session log

### 2026-11-14T07:33:46Z — Handoff refreshed as single durable, execution-forcing focus campaign
- Reconfirmed `AGENT_HANDOFF.md` as the only authoritative handoff; kept redirect stubs in `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md`.
- Elevated **Phase B (`TRACKA-LIQ-EXPANSION-RECOMPUTE`) as mandatory primary work** with explicit definition of done (implementation, frozen prereg, rebuilt panel, eval, tests, gates). Phase A remains secondary/capped to prevent another session from stalling on its known design dead-end.
- Preserved all verified bottleneck fixes from 06:35:00Z: Phase A `INCONCLUSIVE` due to 168h train-window design + double-assemble bug; Phase B unblocked via `ironflow_events`+`hyperliquid_funding`+`hyperliquid_candles` caches (not `ironflow_bulk`); sealed reference numbers and stop rules unchanged.
- No sealed artifacts modified; no outcome computation performed in this session.

### 2026-11-14T06:35:00Z — Durable handoff rewritten from executed evidence (bottlenecks removed)
Executed the prior handoff's Phase A commands instead of re-asserting them, and found its premise
false. Changes made:
- **Removed the bottleneck** that would have burned the next session: the old handoff said Phase A was
  `READY_EXECUTE` and Phase B was "pending, use cached ironflow bulk". In reality Phase A returns
  `INCONCLUSIVE` with empty contrasts (train complete-case rows = 152 because `log_rv168h` is absent
  for the first 192h of every symbol, so C1/C2 cannot fit), and Phase B has **no script at all** —
  and its named input `ironflow_bulk` stops at 2026-04, so a future agent following the old text would
  have hit a missing-data wall and possibly declared a false NO_GO.
- Verified the real Phase B inputs: `ironflow_events` 2026-05..10 (1.26M observed liquidation rows),
  `hyperliquid_funding` all 8 symbols × 4,416 rows with full 2026-05..10 coverage, `hyperliquid_candles`
  all 8 symbols × 6 months. Phase B is therefore fully executable offline.
- Documented and specified a fix for a real bug: `fclr011_recompute_audit.py` assembles the panel twice
  (`main()` over `MONTHS`, then `run_audit()` over smoke-narrowed months), so `--smoke` and full runs
  share one panel SHA-256 and the reported `build`/`coverage` does not describe the emitted parquet.
- Promoted Phase B to the primary heavy task with an exact spec, sealed reference numbers, and a
  requirement to write `scripts/fclr_liq_expansion_recompute.py` plus tests.
- Removed all diagnostic artifacts I created (prereg, panel, build report, evaluation summary for
  `20261114T063000Z`) and reverted an incidental `ironflow_fastpath_cache.json` timestamp touch, so the
  working tree is clean at HEAD. No sealed artifact modified.

### 2026-11-14T06:25:08Z — (superseded) execution-explicit handoff
Claimed Phase A ready and Phase B pending on ironflow bulk. Phase A premise disproven above; Phase B
input claim corrected above.

### 2026-11-14T04:21:39Z
Installed `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z` as rank 0 with Phase A/B; repaired the
artifact-count guard; removed the hardcoded active-campaign test.

### 2026-11-14T03:30:40Z
Executed FCLR-VOL-FORWARD-AUDIT-20261114T032041Z: corrected evaluator (train-only fit/scaling, paired
per-row block bootstrap n=1485/block_h=168/reps=2000, paired-permutation Holm), verdict
EXPLORATORY_NULL, gate 19/19 PASS.

### 2026-11-14T02:35:42Z
Prior 02:33 INADMISSIBLE claim superseded by 02:43/02:45 checkpoint; preserved as history.