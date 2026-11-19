# AGENT HANDOFF — 2026-11-19T07:47:04Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file under `research_state/` is tombstoned/historical and has no campaign authority.
> No duplicate `AGENT_HANDOFF*` exists anywhere in the repo.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-19T07:47:04Z)

**Campaign `FCLR-LIQ-RISK-ESCALATION-08-20261119T044920Z` is now LIVE and machine-enforced.** The previous session (`session_20261119T043545Z`) executed `FCLR-LIQ-TRACKA-CONFIRMATORY-01` and returned **NOT_MET** (models_run=True, power=POWERED, n_discrepancies=0). Do not replay it.

Your job this session is the heavy escalation work, in this order:

1. Create `research_state/session_<UTC>/` (UTC at session start).
2. Write the **outcome-blind** prereg `fclr_risk08_prereg_<UTC>.{json,md}` and freeze it **before** touching any outcome. Universe = the frozen `2025-11 … 2026-10` Track A panel; features = lagged funding, RV, open interest, and their funding×RV interaction; blocks = the frozen chronological blocks with purges/reserve; headline = Brier; placebo = label-hour permutation; multiplicity = Holm.
3. Run `fclr_risk08_power_<UTC>.{py,json,md}` (power/MDE audit; explicit `status` POWERED/UNDERPOWERED).
4. Run `fclr_risk08_recompute_<UTC>.{py,json}` (independent stdlib recompute; require `n_discrepancies=0`).
5. Run `fclr_risk08_evaluation_<UTC>.{py,json,md}` (joint funding×RV×OI regime model vs RV-only baseline; Brier, log-loss, AUC, calibration slope/intercept; placebo; Holm; honest verdict SUPPORT/NOT_MET/UNDERPOWERED).
6. Write `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json`.
7. Run every verification command below; all must PASS. Only then update this handoff.

`scripts/check_handoff_heavywork_gate.py` now **fails closed** on any post-`20261119T044920Z` session that lacks the exact prereg/power/recompute/evaluation/trigger package. A descriptive-only, trigger-check-only, gate-only, or arbitrary-recompute session cannot pass. Zero-byte artifacts fail. **Do not idle. Do not re-audit already-certified results.**

**Do NOT start:** `FCLR-LIQ-TRACKA-CONFIRMATORY-02` (its precondition is an UNDERPOWERED/INCONCLUSIVE verdict; the current verdict is NOT_MET), `FCLR-LIQ-TRACKA-DATA-EXTENSION-02` (no post-`2026-10-31` observed labels with ≥100-day depth; `HL_LABEL_EXTENSION` remains OPEN), RISK-05/06/07, ROBUST-05, or Track C QLIKE. **Do NOT** read sealed Binance months (`2024-10 … 2026-11`) for outcomes.

---

## CURRENT STATE (verified 2026-11-19T07:47:04Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; Track A exploratory **COMPLETE**; Track A 12-month extension **COMPLETE / ADMISSIBLE**; Track A confirmatory **CONFIRMATORY_COMPLETE, verdict NOT_MET**; escalation campaign `FCLR-LIQ-RISK-ESCALATION-08-20261119T044920Z` **READY and gate-enforced**.
- **Latest EXECUTED session:** `session_20261119T043545Z` — confirmatory power/MDE audit (POWERED), independent stdlib recompute (`n_discrepancies=0`), three-block evaluation (verdict NOT_MET), evidence audit, trigger check.
- **Prior executed sessions:** `session_20261119T033443Z` (extension descriptive layer, carry-forwards, audit, trigger check); `session_20261119T022824Z` (extension alignment ADMISSIBLE + confirmatory prereg registration).
- **Track A extension verdict:** `ADMISSIBLE` on `2025-11 … 2026-10` — 13 main-dex Hyperliquid perps, 1,128,446 observed liquidation events, 113,880 coin-hours, alignment yield 1.000, max coin-month candle gap 0.000, gates g1..g7 PASS.
- **Track A confirmatory verdict:** `NOT_MET` — no contrast survived Holm correction (family=4, alpha=0.05); block_3 funding×RV vs RV-only raw Brier diff -0.000522 (p_raw=0.005, p_holm=1.0). Honest negative preserved; block_1 is a cold-start anchor and contributes to power only.
- **Descriptive result (associational only, not predictive):** 18.93% of coin-hours have ≥1 observed event (Wilson 95% CI 18.70%..19.16%); incidence rises monotonically across trailing-24h RV deciles (6.33% → 36.02%); funding deciles are U-shaped (decile 4 16.36%, decile 10 22.90%).
- **Rank-0 triggers:** `NEW_OBSERVED_LIQUIDATION_SOURCE` = **FIRED**; `GATE4_BRANCH_1`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` remain **OPEN**.
- **Root `research_state/` md+json count:** **498 / 500** (cap enforced by `test_tracka_hardening_125`). Write every new artifact under the new session subdir, never at root.
- **Frozen evidence is immutable:** `session_20261118T201919Z/*`, `session_20261118T132800Z/*`, `session_20261119T022824Z/*`, and the confirmatory prereg must not be edited. New work goes in a new session dir.

### Bottlenecks already removed (do not redo)
1. **Data bottleneck gone.** Ironflow/Hyperliquid bulk cache `candles_1h,funding,open_interest,liquidations` covers `2025-11 … 2026-10`; `verify` = 48/48 OK.
2. **Events bottleneck gone.** `research_state/data_cache/ironflow_events/<YYYY-MM>.parquet` covers `2025-05 … 2026-10`.
3. **Admissibility/extension bottleneck gone.** 12-month panel + ADMISSIBLE verdict are frozen; do not recompute alignment.
4. **Confirmatory-registration bottleneck gone.** Three-block design, label contract, lags, models, metrics, placebo, multiplicity frozen in `fclr_tracka_confirmatory01_prereg_20261119T022824Z.json`.
5. **Empty-session/stale-handoff bottleneck gone.** `session_20261119T024457Z/` deleted; gate compares newest on-disk session to handoff.
6. **Confirmatory non-avoidance gate installed and satisfied** by `session_20261119T043545Z`.
7. **Escalation non-avoidance gate installed (new this refresh).** `scripts/check_handoff_heavywork_gate.py` now defines `RISK_08_CAMPAIGN_RE`/`RISK_08_REQUIRED`/`_risk_08_state`, with a `risk_08` verdict in `--json` and a regression suite in `TestRisk08CampaignGate`. The campaign start UTC is concrete (`20261119T044920Z`), so the obligation can no longer be dodged by an unspecified `<UTC>` placeholder.

### Known structural traps (avoid them)
- `fclr_tracka_exploratory01_alignment_20261118T201919Z.py` hardcodes a 6-month window. **Do not edit it** (frozen evidence). Copy it into a new session dir if reuse is needed.
- `scripts/check_tracka_scope_registry_drift.py` compares `scripts/*.py` against `research_state/tracka_script_scope_registry.json` (196/196). If you add or rename anything under `scripts/`, add the registry entry in the same commit.
- `pandas`/`pyarrow` are allowed **only** for parquet reads in ingest/alignment. Core statistics stay stdlib (`json/csv/statistics/random/hashlib/datetime`). No `statsmodels`, no `numpy` in the core path.
- Never emit a zero-byte artifact. Never write sealed Binance months for outcomes.
- A zero `liq_count` hour means no observed event in the feed, not a confirmed no-liquidation hour. State this in every outcome artifact.

---

## NEXT FOCUS CAMPAIGN — REQUIRED HEAVY WORK (machine-enforced)

**Campaign id (concrete, gate-bound): `FCLR-LIQ-RISK-ESCALATION-08-20261119T044920Z`**

### Research question
On the frozen `2025-11 … 2026-10` Hyperliquid main-dex panel, does a **joint funding × RV × open-interest regime model** improve out-of-sample observed liquidation incidence (Brier score) over an RV-only baseline, across preregistered chronological blocks, after a power/MDE audit and a label-hour placebo null?

### Required session directory
Create `research_state/session_<UTC>/` and populate **all** of the following, non-empty, with the campaign id embedded in every JSON:

1. **`fclr_risk08_prereg_<UTC>.{json,md}`** — outcome-blind prereg (universe, window, blocks/purges/reserve, label contract, lagged features incl. funding×RV and OI, models, metrics, headline, placebo, multiplicity, Holm family, gate, prohibitions). Frozen before any outcome is inspected.
2. **`fclr_risk08_power_<UTC>.{py,json,md}`** — power/MDE audit from frozen block sizes and base rate; explicit `status` POWERED/UNDERPOWERED.
3. **`fclr_risk08_recompute_<UTC>.{py,json}`** — independent stdlib recompute; `n_discrepancies=0`.
4. **`fclr_risk08_evaluation_<UTC>.{py,json,md}`** — joint model vs RV-only baseline; Brier headline; log-loss, AUC, calibration slope/intercept; label-hour permutation placebo; Holm correction; honest verdict SUPPORT/NOT_MET/UNDERPOWERED.
5. **`evidence_audit_<UTC>.{json,md}`** — per `RESEARCH_PROMPT.md` §19.
6. **`trigger_check_<UTC>.json`** — re-evaluate the 4 registry triggers.

### Execution recipe
1. Create new session dir `research_state/session_<UTC>/`.
2. Register the outcome-blind prereg; freeze before outcomes.
3. Run the power/MDE audit; require `status=POWERED` (else honest UNDERPOWERED, `models_run=false`).
4. Run the independent stdlib recompute; require `n_discrepancies=0`.
5. If powered, run the frozen evaluation; else write honest UNDERPOWERED artifacts.
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
Baseline recorded now: heavywork gate **PASS** (risk_08 enforced for sessions after `20261119T044920Z`; latest session `session_20261119T043545Z` grandfathered), drift **PASS 196/196**, bulk verify **48/48 OK**, `tests.test_tracka_hardening_143 + 125` **PASS 69/69**, root `research_state/` md+json = **498**.

### Prohibitions (enforced by gate/review)
- Do not re-run RISK-05/06/07, ROBUST-05, or Track C QLIKE.
- Do not start `FCLR-LIQ-TRACKA-CONFIRMATORY-02` (precondition unmet: verdict is NOT_MET).
- Do not start `FCLR-LIQ-TRACKA-DATA-EXTENSION-02` (no post-`2026-10-31` observed labels with ≥100-day depth; `HL_LABEL_EXTENSION` remains OPEN).
- Do not read sealed Binance months for outcomes.
- Do not add or swap metrics after inspecting outcomes.
- Do not mutate the frozen prereg, extension admissibility, panel, or carry-forward artifacts.
- Do not conflate observed liquidation labels with modeled boundary breaches.
- Do not write to `.github/workflows`, do not install heavyweight stats packages.
- Do not spend the session on handoff refresh, gate-only work, descriptive-only replays, or re-auditing already-certified results.
- Do not emit a zero-byte artifact.

### Ranked remaining frontier after RISK-ESCALATION-08
1. `GATE4_BRANCH_1` / `EXPANSION_ROBUSTNESS_REDO` remain external-trigger-only; do not manufacture evidence.
2. `FCLR-LIQ-TRACKA-DATA-EXTENSION-02-<UTC>` — only if new post-`2026-10-31` observed labels with ≥100-day depth become available; then refresh `HL_LABEL_EXTENSION`.

---

## READ FIRST (exact files)
1. `RESEARCH_PROMPT.md` §1–§6, §9–§10, §13–§16, §18–§20
2. `research_state/session_20261119T022824Z/fclr_tracka_confirmatory01_prereg_20261119T022824Z.json` — frozen confirmatory design (label contract, lags, blocks)
3. `research_state/session_20261119T022824Z/fclr_tracka_extension01_admissibility_session_20261119T022824Z.json` — ADMISSIBLE verdict
4. `research_state/session_20261119T043545Z/fclr_tracka_confirmatory01_evaluation_20261119T043545Z.{py,json,md}` — executed confirmatory pattern to mirror for RISK-08
5. `research_state/session_20261119T043545Z/trigger_check_20261119T043545Z.json` — trigger definitions/status
6. `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` — frozen 12-month panel
7. `scripts/check_handoff_heavywork_gate.py`, `scripts/check_tracka_scope_registry_drift.py`, `scripts/fclr_ironflow_bulk.py`
8. `research_state/resume_trigger_registry.json`, `research_state/data_source_registry.json`
9. `tests/test_tracka_hardening_143.py` — non-avoidance gate contracts, incl. `TestRisk08CampaignGate`

## REOPEN TRIGGERS (machine-checkable)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`) — **OPEN**
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: extension admissibility `status=ADMISSIBLE`, `observed_labels=true`, 13 instruments, 12 complete months — **FIRED**
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` post-2026-10-31 observed labels, ≥100-day depth — **OPEN**
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null) — **OPEN**

## VERIFICATION RECORD — 2026-11-19T07:47:04Z
- Track A exploratory: COMPLETE, `ADMISSIBLE`, 6/6 gates, `n_discrepancies=0` (frozen, immutable).
- Track A extension (`session_20261119T022824Z`): alignment **ADMISSIBLE** over `2025-11 .. 2026-10`; stdlib recompute `n_discrepancies=0`; confirmatory prereg registered.
- Track A extension completion (`session_20261119T033443Z`): descriptive layer + verbatim carry-forwards + evidence audit + trigger check.
- Track A confirmatory execution (`session_20261119T043545Z`): verdict `NOT_MET`; power/MDE audit + independent recompute + three-block evaluation + evidence audit + trigger check, all non-empty.
- **Escalation gate installed:** `RISK_08_CAMPAIGN_RE`/`RISK_08_REQUIRED`/`_risk_08_state` wired into `check_handoff_heavywork_gate.py`; `TestRisk08CampaignGate` added (5 tests: missing package, empty files, missing trigger, full package, pre-start grandfather).
- `check_handoff_heavywork_gate.py --json`: **PASS** (`risk_08` enforced for sessions after `20261119T044920Z`; latest session `session_20261119T043545Z` grandfathered).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (196/196).
- `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125`: **PASS 69/69**.
- `python3 -m unittest discover -s tests -p 'test_tracka_*.py'`: **PASS** (0 failures).
- Bulk cache verify: **48 objects, 0 failure(s)**.
- Root `research_state/` md+json unchanged at **498** (cap 500); no sealed artifact or workflow modified.

(End of file)