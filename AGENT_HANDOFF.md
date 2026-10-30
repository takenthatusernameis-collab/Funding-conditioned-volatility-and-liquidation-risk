# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T12:05:15Z
HEAD: c151dfad (main) — clean working tree (ignore __pycache__)
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH

## INITIAL TASK MESSAGE (TIMESTAMPED) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY: CAMPAIGN FCLR-NEXT-001 — DISCOVER A PATH FORWARD (NO SEAL VIOLATIONS)**

### CURRENT GROUND TRUTH (DECISIVE)
- **FCLR-003 (confirmatory):** COMPLETE & NEGATIVE. C2 (funding+price-dislocation/smoothing) vs B1 (RV-only HAR): mean diff +0.015205 QLIKE, rel -3.78% (worse), 95% CI [-0.020240,0.056734] crosses zero. **FCLR-H001: NOT_SUPPORTED.** Risk-overlay INELIGIBLE.
- **FCLR-002:** Underpowered (2 blocks), not claim-worthy (SEALED).
- **FCLR-001:** Coverage defect, PILOT/INCONCLUSIVE (SEALED).
- **H002:** PARTIAL_REPLICATION (Shek SSRN HTTP 403 blocks full methodology). Event stats known from Jan-Mar 2024 (88 events, median 8.0h). RV-regime contrast impossible without Jan-Mar 2024 mark prices.
- **H003:** INCONCLUSIVE on both panels; no incremental skill for 24h boundary-breach forecasting. Extensions untested.
- **H004:** BLOCKED for 2024 (no admissible liquidation census). FCLR-005 (2026 pilot) used HF ochinimus/crypto-liquidation-ticks (Bybit census) but <3 blocks, high base rate (~0.48), no incremental skill of funding+price over RV-only. Still EXPLORATORY_ONLY.
- **Data exhaustion:** 2024-04..12 fully consumed (FCLR-002/003). 2025 has mark price only BTC/ETH (2 symbols). 2026 partial. **No unsealed >=5-symbol, >=3-block confirmatory window remains on current admissible data without NEW source.**

### BOTTLENECKS TO REMOVE
1. **Liquidation source gap (Track A/H004):** Enumeration shows Binance archives 404, forceOrders 451; Bybit trades exist but not liquidation census. HF dataset (2026 only) found but undercounted/excludes 2024. Need systematic discovery of other unauthenticated sources.
2. **H002 methodology lock:** SSRN blocked. Need to document exactly what's reconstructible vs missing without guessing.
3. **H003 extension feasibility:** Long horizons/lower MMR/event-intensity - untested but require pre-registration + events.
4. **No concrete discovery plan:** Need actionable GO/NO-GO with probe commands.

### HEAVY EXECUTION PLAN
Execute in order, produce durable artifacts.

#### STEP 1: LIQUIDATION SOURCE CAMPAIGN (HIGHEST LEVERAGE)
Read: `research_state/liquidation_sources_enumeration.md`, `research_state/binance_source_probe.md`, `research_state/research_protocol_fclr005.md`, `research_state/evaluation_summary_FCLR005.md`

Create `research_state/liquidation_source_campaign.md` with:
- Ranked candidates (unauthenticated): check public archives, GitHub raw files, HF mirrors, academic repos, other exchanges
- Probe commands (curl) for each - test without credentials
- For promising: minimal dataset to get >=3 non-overlapping 30-day blocks across >=5 symbols with provenance/license
- DEAD/UNKNOWN/BLOCKED classification with evidence
- If ANY viable found → pre-register micro-experiment BEFORE bulk download

#### STEP 2: H002 METHODOLOGY DOSSIER
Read: `scripts/funding_correction_replication.py`, `tests/test_funding_correction_replication.py`, `research_state/h002_replication_report.md`, `research_state/shek_methodology_availability.md`

Create `research_state/h002_methodology_dossier.md`: reconstructible elements, missing (RV regime split, thresholds, contract set), blockers, feasibility of RV-regime contrast with available data.

#### STEP 3: H003 EXTENSION FEASIBILITY
Read: `scripts/synthetic_boundary_labels.py`, `scripts/run_h003.py`, `research_state/fclr_h003_pre_registration.md`, `research_state/evaluation_summary_h003*.md`

Create `research_state/h003_extension_feasibility.md`: event rates, feasible horizons/scenarios, pre-reg requirements if pursued.

#### STEP 4: DISCOVERY PLAN
Create `research_state/next_data_discovery_plan.md`: targets, candidate sources/methods, validation checklist, GO/NO-GO criteria, concrete probe commands.

#### STEP 5: VERIFY & UPDATE
- `python -m unittest discover -s tests -v` (must pass)
- Update this handoff with campaign status
- Commit artifacts if sensible (research_state/*.md)

### VERIFICATION
```bash
python -m unittest discover -s tests -v
git log --oneline -2
```

### HARD CONSTRAINTS
- **NO SEAL VIOLATIONS:** No tuning/threshold-shopping on FCLR-002/003. No re-opening sealed holds.
- **NO FABRICATION:** No invented liquidation labels; don't conflate modeled breaches with observed.
- **NO WORKFLOW CHANGES:** No `.github/workflows/*` changes without explicit authorization.
- **PRE-REGISTER FIRST:** New experiment on unsealed data must be pre-registered before outcome inspection.
- **EVIDENCE-BASED:** If methodology unreachable, document blockers. No guessing.
- **DATA EXHAUSTION REAL:** Assume no path on current data until concrete new admissible source found.

### NEXT AGENT DIRECTIVE
**START WITH STEP 1.** Build liquidation_source_campaign.md - systematic discovery of unauthenticated sources that could cover 2024 or provide confirmatory-feasible window. Be exhaustive, produce GO/NO-GO. No busywork.
