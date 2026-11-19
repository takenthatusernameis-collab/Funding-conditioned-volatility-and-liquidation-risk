# AGENT HANDOFF — 2026-11-19T03:45:00Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file under `research_state/` is tombstoned/historical and has no campaign authority.
> No duplicate `AGENT_HANDOFF*` exists anywhere in the repo.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-19T03:45:00Z)

**Execute `FCLR-LIQ-TRACKA-CONFIRMATORY-01-20261119T034500Z` now.** The 12-month Track A extension is **COMPLETE** in `session_20261119T033443Z`: alignment ADMISSIBLE over `2025-11 … 2026-10` (13 Hyperliquid perps, 113,880 coin-hours, 1.0 yield, 0.0 max gap, g1..g7 PASS), descriptive layer produced (1,128,446 observed liquidation events; 21,557 hours with ≥1 event), carry-forward packages copied verbatim, stdlib recompute `n_discrepancies=0`, confirmatory design registered outcome-blind, all verification commands PASS. The campaign is **fully unblocked and fully offline**: the Ironflow/Hyperliquid bulk cache for all 12 months is local and hash-verified (48/48 objects OK).

**This is not a descriptive or audit session. Run the registered three-block confirmatory forecast evaluation.** The frozen prereg is `research_state/session_20261119T022824Z/fclr_tracka_confirmatory01_prereg_20261119T022824Z.json`. Do not re-freeze it, do not add metrics, do not re-split the months.

**Remaining mandatory work for the next session:**
1. **Power/MDE audit first** — compute the minimum detectable Brier/log-loss effect implied by the frozen block sizes (block_1 61d, block_2 89d, block_3 92d) and the observed event base rate. If MDE exceeds the plausible effect, write the evaluation artifacts with `status=UNDERPOWERED` and `models_run=false`; do not run a fake evaluation.
2. **Independent stdlib recompute** — reproduce panel aggregates, block membership, and label counts with `json/csv/statistics/random/hashlib/datetime` only; emit `n_discrepancies`.
3. **Confirmatory evaluation** — implement the frozen design exactly: intercept-only, funding-only, RV-only, and funding×RV logistic baselines; outcome `liq_count ≥ 1` per coin-hour (absence from the feed is **not** zero-probability of liquidation); predictors lagged ≥1h; headline metric **Brier score**; also report log-loss, AUC, calibration slope, and calibration intercept; label-hour permutation placebo null; Holm correction over the declared family; raw and adjusted results.
4. **Evidence audit + trigger check** — per `RESEARCH_PROMPT.md` §19, with `honest_status`, `prohibitions_respected`, `network_used` (expected `false`), and the explicit statement that the frozen prereg was not mutated. Re-evaluate all four registry triggers.
5. **Run all verification commands** (must PASS before touching this handoff):
   ```bash
   python3 scripts/check_handoff_heavywork_gate.py --json
   python3 scripts/check_tracka_scope_registry_drift.py --json
   python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10
   python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v
   python3 -m unittest discover -s tests -p 'test_tracka_*.py'
   ```
6. **Refresh this handoff** — set Latest executed session to the new session dir, record the confirmatory verdict (`SUPPORT` / `NOT_MET` / `UNDERPOWERED`), and select the next campaign from the remaining ranked frontier below.

Do not idle. Do not run a descriptive-only or trigger-check-only session: the heavywork gate now requires the power/MDE audit, independent recompute, evaluation triad, and trigger check in any post-start session. Do not evaluate the sealed Binance months. Do not re-run RISK-05/06/07, ROBUST-05, or Track C QLIKE.

---

## CURRENT STATE (verified 2026-11-19T03:45:00Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; Track A exploratory **COMPLETE**; Track A 12-month extension **COMPLETE / ADMISSIBLE**; Track A confirmatory **REGISTERED, NOT EVALUATED**; next required campaign **READY**.
- **Latest EXECUTED session:** `session_20261119T033443Z` — `FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z` — **COMPLETE**: descriptive layer (`fclr_tracka_extension01_descriptive_20261119T033443Z.{py,json,md}`), carry-forward packages, evidence audit, trigger check.
- **Prior executed session:** `session_20261119T022824Z` — extension alignment + confirmatory prereg registration (steps 1-3).
- **Track A extension verdict:** `ADMISSIBLE` on `2025-11 … 2026-10` — 13 main-dex Hyperliquid perps, 1,128,446 observed liquidation events, 113,880 coin-hours, alignment yield 1.000, max coin-month candle gap 0.000, gates g1..g7 PASS.
- **Descriptive result (descriptive only, not predictive):** 18.93% of coin-hours have ≥1 observed event (Wilson 95% CI 18.70%..19.16%). Event incidence rises monotonically across trailing-24h RV deciles (6.33% → 36.02%). Funding deciles are U-shaped (decile 4 16.36%, decile 10 22.90%). These are same-panel associations, not lead-lag evidence.
- **Rank-0 triggers:** `NEW_OBSERVED_LIQUIDATION_SOURCE` = **FIRED** (`confirmed_on_extension=true` → extension admissibility JSON); `GATE4_BRANCH_1`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` remain **OPEN**.
- **Root `research_state/` md+json count:** **498 / 500** (unchanged; new artifacts live under `session_20261119T033443Z/`, not root). Write every new artifact under the new session subdir.
- **Frozen evidence is immutable:** `session_20261118T201919Z/*`, `session_20261118T132800Z/*`, and `session_20261119T022824Z/*` must not be edited. New work goes in a new session dir.
- **Empty-session bottleneck removed:** `session_20261119T024457Z/` was empty and made the heavywork gate stale; it has been deleted.

### Bottlenecks already removed (do not redo)
1. **Data bottleneck gone.** Ironflow/Hyperliquid bulk cache `candles_1h,funding,open_interest,liquidations` covers `2025-11 … 2026-10`; `verify` = 48/48 OK.
2. **Events bottleneck gone.** `research_state/data_cache/ironflow_events/<YYYY-MM>.parquet` covers `2025-05 … 2026-10`.
3. **Admissibility/extension bottleneck gone.** The 12-month panel and ADMISSIBLE verdict are frozen; do not recompute the alignment.
4. **Confirmatory-registration bottleneck gone.** The three-block design, label contract, feature lags, models, metrics, placebo, multiplicity, and headline metric are frozen in `fclr_tracka_confirmatory01_prereg_20261119T022824Z.json`.
5. **Empty-session/stale-handoff bottleneck gone.** `session_20261119T024457Z/` deleted; this handoff points at the complete extension session.
6. **Non-avoidance gate installed.** `scripts/check_handoff_heavywork_gate.py` now requires `fclr_tracka_confirmatory01_power_*`, `fclr_tracka_confirmatory01_recompute_*`, `fclr_tracka_confirmatory01_evaluation_*`, and `trigger_check_*` in any post-start confirmatory session.

### Known structural traps (avoid them)
- `fclr_tracka_exploratory01_alignment_20261118T201919Z.py` hardcodes a 6-month window. **Do not edit it** (frozen evidence). Copy it into a new session dir if reuse is needed.
- `scripts/check_tracka_scope_registry_drift.py` compares `scripts/*.py` against `research_state/tracka_script_scope_registry.json` (196/196). If you add or rename anything under `scripts/`, add the registry entry in the same commit.
- `pandas`/`pyarrow` are allowed **only** for parquet reads in ingest/alignment. Core statistics stay stdlib (`json/csv/statistics/random/hashlib/datetime`). No `statsmodels`, no `numpy` in the core path.
- Never emit a zero-byte artifact. Never write sealed Binance months (`2024-10 … 2026-11`) for outcomes.
- A zero `liq_count` hour means no observed event in the feed, not a confirmed no-liquidation hour. State this in every outcome artifact.

---

## NEXT FOCUS CAMPAIGN — REQUIRED HEAVY WORK (machine-enforced)

**`FCLR-LIQ-TRACKA-CONFIRMATORY-01-20261119T034500Z` — confirmatory three-block test of funding-conditioned observed-liquidation incidence on the 12-month Track A panel**

### Research question
In the frozen `2025-11 … 2026-10` Hyperliquid main-dex panel, do funding-rate-conditioned features improve out-of-sample **observed liquidation incidence** forecasts (Brier score) over an RV-only logistic baseline across the three preregistered blocks — after a mandatory power/MDE audit and a label-hour placebo null?

### Required session directory
Create a new UTC session dir `research_state/session_<UTC>/` (UTC at session start) and populate **all** of the following, non-empty, with the campaign id `FCLR-LIQ-TRACKA-CONFIRMATORY-01-20261119T034500Z` embedded in every JSON:

1. **`fclr_tracka_confirmatory01_power_<UTC>.{py,json,md}`**
   - Minimum detectable effect from the frozen block sizes, observed event base rate, and declared multiplicity.
   - Explicit `status`: `POWERED` or `UNDERPOWERED`.
   - If `UNDERPOWERED`, the evaluation artifacts below must record `models_run=false` and the campaign verdict must be `UNDERPOWERED`, not a fabricated result.

2. **`fclr_tracka_confirmatory01_recompute_<UTC>.{py,json}`**
   - Independent stdlib recomputation of panel row counts, block membership, event counts, and hourly label counts.
   - Emit `n_discrepancies`; must be `0` for the frozen panel.

3. **`fclr_tracka_confirmatory01_evaluation_<UTC>.{py,json,md}`**
   - Implement the frozen prereg exactly: blocks `2025-11-01..2025-12-31`, `2026-02-01..2026-04-30`, `2026-06-01..2026-08-31`; purges `2026-01` and `2026-05`; reserve `2026-09..2026-10` untouched.
   - Models: intercept-only, funding-only, RV-only, funding×RV interaction; no booster, no NN.
   - Predictors strictly lagged ≥1h; training history only from earlier time.
   - Metrics: Brier (headline), log-loss, AUC, calibration slope, calibration intercept.
   - Label-hour permutation placebo null; Holm correction over the declared family; report raw and adjusted results.
   - Honest verdict: `SUPPORT`, `NOT_MET`, or `UNDERPOWERED`. No post-hoc metric addition.

4. **`evidence_audit_<UTC>.{json,md}`** — per `RESEARCH_PROMPT.md` §19, with `honest_status`, `prohibitions_respected`, `network_used` (expected `false`), and an explicit statement that the frozen prereg was not mutated and no sealed Binance outcome was read.

5. **`trigger_check_<UTC>.json`** — re-evaluate the 4 registry triggers:
   - `NEW_OBSERVED_LIQUIDATION_SOURCE`: remains **FIRED**; keep `confirmed_on_extension=true` pointing at the extension admissibility JSON.
   - `HL_LABEL_EXTENSION`: still **OPEN** unless labels after 2026-10-31 with ≥100-day depth exist.
   - `GATE4_BRANCH_1`, `EXPANSION_ROBUSTNESS_REDO`: unchanged **OPEN** unless their exact evidence artifacts appear.

6. **Mandatory carry-forward (copied verbatim, non-empty):**
   - `fclr_tracka_confirmatory01_prereg_20261119T022824Z.{json,md}` (frozen prereg)
   - `fclr_tracka_extension01_admissibility_session_20261119T022824Z.{json,md}` (ADMISSIBLE verdict)
   - `fclr_tracka_extension01_descriptive_20261119T033443Z.{json,md}` (descriptive baseline)
   - `fclr_tracka_extension01_panel_session_20261119T022824Z.csv` (or a new session-local copy; never edit the frozen source)

### Execution recipe
1. Create new session dir `research_state/session_<UTC>/`.
2. Copy the frozen prereg, extension admissibility, descriptive baseline, and panel into it.
3. Run the power/MDE audit; write `fclr_tracka_confirmatory01_power_*`.
4. Run the independent stdlib recompute; require `n_discrepancies=0`.
5. If powered, run the frozen three-block evaluation; otherwise write the honest `UNDERPOWERED` evaluation artifacts.
6. Write evidence audit and trigger check.
7. Run all verification commands; all must PASS.
8. Update this handoff (only after verification passes).

### Verification commands (all must PASS before touching this handoff)
```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 scripts/check_tracka_scope_registry_drift.py --json
python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v
python3 -m unittest discover -s tests -p 'test_tracka_*.py'
```
Baseline recorded now: heavywork gate **PASS**, drift **PASS 196/196**, bulk verify **48/48 OK**, `tests.test_tracka_hardening_143 + 125` **PASS 64/64**, root `research_state/` md+json = **498**.

### Prohibitions (enforced by gate/review)
- Do not re-run RISK-05/06/07, ROBUST-05, or Track C QLIKE.
- Do not read sealed Binance months for outcomes.
- Do not add or swap metrics after inspecting outcomes.
- Do not mutate the frozen prereg, extension admissibility, panel, or carry-forward artifacts.
- Do not conflate observed liquidation labels with modeled boundary breaches.
- Do not write to `.github/workflows`, do not install heavyweight stats packages.
- Do not spend the session on handoff refresh, gate-only work, descriptive-only replays, or re-auditing already-certified results.
- Do not emit a zero-byte artifact.

### Ranked remaining frontier after this campaign (choose only after recording a verdict)
1. **`FCLR-LIQ-TRACKA-CONFIRMATORY-02-<UTC>`** — only if the confirmatory verdict is `UNDERPOWERED`/`INCONCLUSIVE` and a materially different preregistered estimand is justified (new design, new freeze, no re-scoring).
2. **`FCLR-LIQ-RISK-ESCALATION-08-<UTC>`** — extend the observed-label risk pillar to a joint funding × RV × OI regime model on the 12-month panel, with a fresh outcome-blind prereg and block design.
3. **`FCLR-LIQ-TRACKA-DATA-EXTENSION-02-<UTC>`** — only if new post-`2026-10-31` observed labels with ≥100-day depth become available; then refresh `HL_LABEL_EXTENSION`.
4. `GATE4_BRANCH_1` / `EXPANSION_ROBUSTNESS_REDO` remain external-trigger-only; do not manufacture evidence.

---

## READ FIRST (exact files)
1. `RESEARCH_PROMPT.md` §1–§6, §9–§10, §13–§16, §18–§20
2. `research_state/session_20261119T022824Z/fclr_tracka_confirmatory01_prereg_20261119T022824Z.json` — frozen confirmatory design
3. `research_state/session_20261119T022824Z/fclr_tracka_extension01_admissibility_session_20261119T022824Z.json` — ADMISSIBLE verdict
4. `research_state/session_20261119T033443Z/fclr_tracka_extension01_descriptive_20261119T033443Z.md` — descriptive baseline
5. `research_state/session_20261119T033443Z/trigger_check_20261119T033443Z.json` — trigger definitions/status
6. `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` — frozen 12-month panel
7. `scripts/check_handoff_heavywork_gate.py`, `scripts/check_tracka_scope_registry_drift.py`, `scripts/fclr_ironflow_bulk.py`
8. `research_state/resume_trigger_registry.json`, `research_state/data_source_registry.json`
9. `tests/test_tracka_hardening_143.py` — non-avoidance gate contract, including `TestTrackaConfirmatoryCampaignGate`

## REOPEN TRIGGERS (machine-checkable)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`) — **OPEN**
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: extension admissibility `status=ADMISSIBLE`, `observed_labels=true`, 13 instruments, 12 complete months — **FIRED**
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` post-2026-10-31 observed labels, ≥100-day depth — **OPEN**
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null) — **OPEN**

## VERIFICATION RECORD — 2026-11-19T03:45:00Z
- Track A exploratory: COMPLETE, `ADMISSIBLE`, 6/6 gates, `n_discrepancies=0` (frozen, immutable).
- Track A extension (`session_20261119T022824Z`): alignment **ADMISSIBLE** over `2025-11 .. 2026-10` (g1..g7 PASS; 113,880 coin-hours; yield 1.0; max gap 0.0; 1,128,446 observed events); stdlib recompute `n_discrepancies=0`; confirmatory prereg registered (not evaluated).
- Track A extension completion (`session_20261119T033443Z`): descriptive layer produced (18.93% of coin-hours with ≥1 event; RV decile incidence 6.33% → 36.02%; funding decile incidence 16.36% → 22.90%); full carry-forward copied verbatim; evidence audit + trigger check written.
- Empty `session_20261119T024457Z/` deleted; stale-session gate bottleneck removed.
- `check_handoff_heavywork_gate.py --json`: **PASS** (latest complete session `session_20261119T033443Z`; confirmatory campaign gate installed and grandfathered for the announcing session).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (196/196, no network, read-only).
- `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125`: **PASS 64/64**.
- `python3 -m unittest discover -s tests -p 'test_tracka_*.py'`: **PASS** (0 failures).
- Bulk cache verify: **48 objects, 0 failure(s)**.
- Root `research_state/` md+json unchanged at **498** (cap 500); no sealed artifact or workflow modified.

(End of file)
