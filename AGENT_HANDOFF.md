# AGENT HANDOFF — 2026-11-19T02:36:00Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file under `research_state/` is tombstoned/historical and has no campaign authority.
> No duplicate `AGENT_HANDOFF*` exists anywhere in the repo.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-19T02:36:00Z)

**Execute `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z` now.** This is the single highest-value campaign. Session `session_20261119T022824Z` is IN PROGRESS: step 1 (generalize alignment script with `--months` CLI defaulting to 2025-11..2026-10) DONE; step 2 (outcome-blind prereg frozen) DONE; step 3 (12-month alignment ran) DONE -> ADMISSIBLE, gates g1..g7 PASS, panel 113,880 coin-hours, alignment yield 1.0, max gap 0.0; stdlib recompute `n_discrepancies=0`; confirmatory prereg (registration only) registered; evidence audit + trigger check written.

The campaign is **fully unblocked and fully offline**: the entire Ironflow/Hyperliquid bulk cache `2025-11 … 2026-10` (candles_1h, funding, open_interest, liquidations) is materialised and hash-verified (24/24 objects OK, `fclr_ironflow_bulk.py verify` exit 0). No download is needed.

Remaining work this session: (a) descriptive layer (item 5) — per-coin event totals/notional, share of hours with >=1 event, top-10 liquidation hours, weekday/hour-of-day profile, incidence vs funding & RV decile with counts + CIs, explicit statement these are descriptive associations on observed labels not predictive evidence; (b) mandatory carry-forward (item 9) copied verbatim (RISK-07 package + recompute_fclr_risk07_recalibration_*, RISK-06 package, ROBUST-05 package, Track A exploratory package from session_20261118T201919Z); (c) run all verification commands below; (d) refresh this handoff (latest session, active next campaign = `FCLR-LIQ-TRACKA-CONFIRMATORY-01-<UTC>`, trigger state from trigger_check_<UTC>.json).

Do not idle, do not re-audit RISK-05/06/07, do not run gate-only or handoff-refresh-only work, do not evaluate the confirmatory design (registration only), do not read sealed Binance months for outcomes.

---

## CURRENT STATE (verified 2026-11-19T02:29:03Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; Track A exploratory **COMPLETE**; confirmatory Track A **REGISTERED** (registration only, not evaluated; awaits `FCLR-LIQ-TRACKA-CONFIRMATORY-01-<UTC>`).
- **Latest session (in progress):** `session_20261119T022824Z` — `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z` — steps 1-3 DONE: alignment generalized (`--months`, default 2025-11..2026-10), prereg frozen outcome-blind, 12-month alignment **ADMISSIBLE** (g1..g7 PASS; 113,880 coin-hours; yield 1.0; max gap 0.0), stdlib recompute `n_discrepancies=0`, confirmatory prereg registered, evidence audit + trigger check written.
- **Latest executed session:** `session_20261118T132800Z` — `FCLR-VOL-LIQ-ROBUST-04` — **COMPLETE** (negative result: funding-conditioned features do NOT improve volatility/breach forecasts over RV-only).
- **Track A extension verdict (from `session_20261119T022824Z`):** `ADMISSIBLE` on `2025-11 … 2026-10` — 13 main-dex Hyperliquid perps, ~1.13M observed liquidation events, 113,880 coin-hours, alignment yield 1.000, max coin-month candle gap 0.000, gates g1..g7 PASS.
- **Rank-0 triggers:** `NEW_OBSERVED_LIQUIDATION_SOURCE` = **FIRED** (confirmed_on_extension=true -> extension admissibility JSON); `GATE4_BRANCH_1`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` remain **OPEN**.
- **Root `research_state/` md+json count:** **498 / 500** (unchanged; session artifacts live under `session_20261119T022824Z/`, not root). Write every new artifact under the session subdir.
- **Frozen evidence is immutable:** `session_20261118T201919Z/*` and `session_20261118T132800Z/*` must not be edited. New work goes in a new session dir.

### Bottlenecks already removed (do not redo)
1. **Data bottleneck gone.** `scripts/fclr_ironflow_bulk.py fetch --datasets candles_1h,funding,open_interest,liquidations --months 2026-05..2026-10` executed 2026-11-19T01:49Z. All 24 objects for `2026-05..2026-10` verify OK.
2. **Events bottleneck gone.** `research_state/data_cache/ironflow_events/<YYYY-MM>.parquet` covers `2025-05 … 2026-10`.
3. **Ambiguity bottleneck gone.** The exact blocker ("register confirmatory only after extending candle/funding/OI cache to 2026-05..2026-10 and re-running this audit") is now a single deterministic job.
4. **Alignment-script bottleneck removed.** `session_20261119T022824Z/fclr_tracka_extension01_alignment_20261119T022824Z.py` was a broken copy of the exploratory script: it hardcoded the 6-month `2025-11..2026-04` window, the frozen exploratory campaign/session ids, and wrote into the frozen `session_20261118T201919Z/` directory. It has been generalized: `--months` CLI (default `2025-11..2026-10`), extension campaign id + new session dir, emits `window_months`, writes only to `session_20261119T022824Z/`. No longer a write-to-frozen-evidence violation.

### Known structural traps (avoid them)
- `fclr_tracka_exploratory01_alignment_20261118T201919Z.py` hardcodes `MONTHS = ["2025-11" … "2026-04"]`. **Do not edit it** (frozen evidence). Copy it into the new session dir and generalize: `MONTHS` must come from a CLI `--months 2025-11..2026-10` argument, and `window_months` must be emitted into the JSON.
- `scripts/check_tracka_scope_registry_drift.py` compares `scripts/*.py` against `research_state/tracka_script_scope_registry.json` (196/196). If you add or rename anything under `scripts/`, you must add the registry entry in the same commit, or the drift gate fails.
- `pandas`/`pyarrow` are allowed **only** for parquet reads in ingest/alignment. Core statistics stay stdlib (`json/csv/statistics/random/hashlib/datetime`). No `statsmodels`, no `numpy` in the core path.
- Never emit a zero-byte artifact. Never write sealed Binance months (`2024-10 … 2026-11`) for outcomes.

---

## NEXT FOCUS CAMPAIGN — REQUIRED HEAVY WORK (machine-enforced)

**`FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z` — 12-month Track A extension audit + confirmatory design registration**

### Research question
Does the observed Hyperliquid forced-liquidation label remain admissible and stable across the **full 12-month window `2025-11 … 2026-10`** (13 coins, both halves of the year), and if so, can a **confirmatory forecast test** be frozen now on that window?

### Required session directory
Create a new UTC session dir `research_state/session_<UTC>/` (UTC at session start) and populate **all** of the following, non-empty, with the campaign id `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z` embedded in every JSON:

1. **`fclr_tracka_extension01_prereg_<UTC>.{json,md}`** — outcome-blind, frozen before the extended alignment is computed.
   - Same source/licence/venue/coin definitions as the exploratory prereg (CC BY 4.0, unauthenticated, main-dex perps, `dex == ""`, `market_class == "perp"`).
   - Window `2025-11 … 2026-10`; 13 coins.
   - Frozen gates identical to exploratory: `g1` provenance hashed, `g2` ≥5 instruments with events, `g3` ≥3 complete months, `g4` max coin-month 1h candle gap ≤20%, `g5` observed-only labels, `g6` alignment yield ≥95%.
   - **New, pre-declared stability gate `g7_halfyear_stability`:** the per-half-year (2025-11…2026-04 vs 2026-05…2026-10) event prevalence ratio and per-coin event counts must be reported; `g7` PASS iff both halves independently satisfy `g2`/`g3`/`g6`. Declare this before computing it.
   - `outcome_target_inspected_before_freeze=false`.

2. **`fclr_tracka_extension01_alignment_<UTC>.{py,json,md,csv}`** — generalized copy of the exploratory alignment script.
   - Must accept `--months`, default `2025-11..2026-10`; emit panel CSV plus per-month and per-half-year aggregates.
   - Report: events joined/unjoined, hours with ≥1 liquidation, funding coverage, OI coverage, max gap rate, per-coin counts.

3. **`fclr_tracka_extension01_admissibility_<UTC>.{json,md}`** — gate-by-gate verdict for all 7 gates with numeric evidence, per-half-year table, and explicit `status ∈ {ADMISSIBLE, DATA_BLOCKED, NOT_STARTED}`.
   - If `ADMISSIBLE`: also emit `fclr_tracka_confirmatory01_prereg_<UTC>.{json,md}` (item 4).
   - If not: write the exact shortfall (month, coin, gate, observed vs threshold) and stop at `DATA_BLOCKED`.

4. **`fclr_tracka_confirmatory01_prereg_<UTC>.{json,md}`** — the frozen confirmatory design, registered only from an `ADMISSIBLE` verdict.
   - **Splits:** 3 non-overlapping chronological blocks over the 12 months (each ≥60 days, ≥20-day purge/embargo between blocks), frozen month boundaries, no reshuffling.
   - **Label:** observed liquidation incidence per `(coin, hour_utc)` (`liq_count`, `liq_notional_usd`, long/short split) and its normalized variant by contemporaneous OI; absence ≠ zero, state this in the label contract.
   - **Features:** funding rate, funding sign/level, premium, mark-price realized volatility, OI change — all lagged strictly ≥1h to avoid look-ahead.
   - **Models & baselines:** intercept-only, funding-only, RV-only, and funding×RV interaction. No booster/NN.
   - **Metrics:** Brier, log-loss, AUC, calibration slope/intercept; headline metric frozen before evaluation, placebo/null via label-hour permutation.
   - **Power:** minimum detectable effect from block sizes; if MDE exceeds the plausible effect, say so and mark the campaign `UNDERPOWERED` rather than running it.
   - **Gate:** what result would count as support vs honest negative; no post-hoc metric addition.

5. **`fclr_tracka_extension01_descriptive_<UTC>.{json,md}`** — mandatory heavy descriptive layer (this is *not* a forecast test and must not be reported as one):
   - Per coin: total events, notional, share of hours with ≥1 event, top-10 liquidation hours, weekday/hour-of-day profile.
   - Event incidence vs funding rate decile and vs RV decile within the descriptive panel, with counts and CIs.
   - Explicit statement that these are descriptive associations on observed labels, not predictive evidence.

6. **`recompute_tracka_extension01_<UTC>.{py,json}`** — independent stdlib recompute from the panel CSV; must report `n_discrepancies=0` (panel rows, event totals, notional totals, hours-with-liq, coins-with-events, max gap).

7. **`evidence_audit_<UTC>.{json,md}`** — per RESEARCH_PROMPT.md §19, with `honest_status`, `prohibitions_respected`, `network_used` (expected `false` — cache is local), and the statement that no confirmatory evaluation was run.

8. **`trigger_check_<UTC>.json`** — re-evaluate the 4 registry triggers plus the extension verdict:
   - `NEW_OBSERVED_LIQUIDATION_SOURCE`: remains FIRED for the exploratory artifact; add a `confirmed_on_extension=true|false` field pointing at the extension admissibility JSON.
   - `HL_LABEL_EXTENSION`: still OPEN unless labels after 2026-10-31 with ≥100-day depth exist.
   - `GATE4_BRANCH_1`, `EXPANSION_ROBUSTNESS_REDO`: unchanged OPEN.

9. **Mandatory carry-forward (copied verbatim, non-empty):** RISK-07 package + `recompute_fclr_risk07_recalibration_*`, RISK-06 package, ROBUST-05 package, and the Track A exploratory package from `session_20261118T201919Z`.

### Execution recipe
1. Copy `fclr_tracka_exploratory01_alignment_20261118T201919Z.py` → new session dir; replace the hardcoded `MONTHS` with `--months` parsing; keep all math identical.
2. Freeze the extension prereg **before** reading the 2026-05…2026-10 liquidation outcomes.
3. Run alignment over 12 months; emit panel CSV (expect ≈112k+ coin-hours), per-month table, per-half-year table.
4. Evaluate gates 1–7; write the admissibility verdict.
5. If ADMISSIBLE, write the confirmatory prereg (splits, MDE, metrics, gate) — freeze only, **no evaluation**.
6. Run the descriptive layer (item 5). This is required heavy output even if the verdict is DATA_BLOCKED; in that case restrict it to admissible months and label it as such.
7. Run the stdlib recompute; require `n_discrepancies=0`.
8. Write the evidence audit and trigger check, then run all verification commands below.

### Verification commands (all must PASS before touching this handoff)
```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 scripts/check_tracka_scope_registry_drift.py --json
python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v
python3 -m unittest discover -s tests -p 'test_tracka_*.py'
```
Baseline recorded now: heavywork gate **PASS**, drift **PASS 196/196**, bulk verify **24/24 OK**, `tests.test_tracka_hardening_143 + 125` → **61 tests OK**, root `research_state/` md+json = **498**.

### Prohibitions (enforced by gate/review)
- Do not re-run RISK-05/06/07, ROBUST-05, or Track C QLIKE.
- Do not read sealed Binance months for outcomes.
- Do not evaluate the confirmatory design in this campaign — registration only.
- Do not conflate observed liquidation labels with modeled boundary breaches.
- Do not write to `.github/workflows`, do not install heavyweight stats packages, do not modify frozen session artifacts.
- Do not spend the session on handoff refresh, gate-only work, or re-auditing already-certified results.

### Handoff update (only after verification)
1. Set **Latest executed session** to the new session dir and its campaign id.
2. Set **Active required next campaign** to `FCLR-LIQ-TRACKA-CONFIRMATORY-01-<UTC>` if the confirmatory prereg was registered; otherwise `BLOCKED` with the exact shortfall.
3. Update **Rank-0 trigger state** from the new `trigger_check_<UTC>.json`.
4. Keep this file the sole durable handoff; no duplicates; no new root-level `research_state/*.md|json`.

---

## READ FIRST (exact files)
1. `RESEARCH_PROMPT.md` §1–§6, §9–§10, §13–§16, §18–§20
2. `research_state/session_20261118T201919Z/fclr_tracka_exploratory01_prereg_20261118T201919Z.md` — frozen definitions/gates
3. `research_state/session_20261118T201919Z/fclr_tracka_exploratory01_alignment_20261118T201919Z.py` — the script to generalize
4. `research_state/session_20261118T201919Z/fclr_tracka_exploratory01_admissibility_20261118T201919Z.json` — 6-month verdict
5. `research_state/session_20261118T201919Z/trigger_check_20261118T201919Z.json` — trigger definitions/status
6. `scripts/fclr_ironflow_bulk.py` — cache fetch/verify/manifest (already run; read for schema and paths)
7. `scripts/next_campaign_status.py`, `scripts/check_handoff_heavywork_gate.py`, `scripts/check_tracka_scope_registry_drift.py`
8. `research_state/resume_trigger_registry.json`, `research_state/data_source_registry.json`, `research_state/evaluation_summary.md`

## REOPEN TRIGGERS (machine-checkable)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`) — **OPEN**
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: exploratory admissibility `status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 complete months — **FIRED (exploratory)**; extension re-check is this campaign's job
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` post-2026-10-31 observed labels, ≥100-day depth — **OPEN**
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null) — **OPEN**

## VERIFICATION RECORD — 2026-11-19T02:36:00Z
- Track A exploratory: COMPLETE, `ADMISSIBLE`, 6/6 gates, `n_discrepancies=0`; 13 coins, 6 months, 537,829 observed events (frozen, immutable).
- Track A extension (session_20261119T022824Z): steps 1-3 DONE; alignment **ADMISSIBLE** over `2025-11 .. 2026-10` (g1..g7 PASS; 113,880 coin-hours; yield 1.0; max gap 0.0; ~1.13M events); stdlib recompute `n_discrepancies=0`; confirmatory prereg registered (not evaluated); evidence audit + trigger check written.
- Bulk cache extended to `2026-10` and hash-verified: `candles_1h`, `funding`, `open_interest`, `liquidations` all present for `2026-05..2026-10` (18 + 6 objects, 0 failures, `verify` 24/24 OK).
- `check_handoff_heavywork_gate.py --json`: **PASS** (`risk_07` required true, pass true; no empty/missing required artifacts; session_20261119T022824Z carries evidence_audit + recompute quant).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (196/196, no network, read-only; session alignment script is under research_state/session_*/, not scripts/).
- `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125`: **61 tests OK**.
- Root `research_state/` md+json unchanged at **498** (cap 500); no sealed artifact or workflow modified.
- Bottleneck removed: alignment script generalized, no longer writes to frozen exploratory session dir; confirmatory path is no longer data-blocked — extension audit in progress, descriptive + carry-forward + verification remain.

(End of file)