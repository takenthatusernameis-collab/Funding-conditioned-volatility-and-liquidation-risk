# AGENT HANDOFF — Funding-conditioned-volatility-and-liquidation-risk

**Generated (UTC):** 2026-11-27T22:06:41Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Durable handoff for next agentic work session**

---

## EXECUTIVE STATUS

**Confirmatory program: CONCLUDED** (final_synthesis_report.md, 2026-11-10)
- **Track C (volatility/stress forecasts):** NOT_SUPPORTED — all 8+ confirmatory panels/experiments (FCLR-001, 003, 008, 009, 011, 012-V, 013, GATE4 v3 30d) null; best C2 vs B1 = -0.43% QLIKE (CI crosses zero, below 2% floor)
- **Track B (modeled boundary breaches):** NOT_SUPPORTED — 32 tests (FCLR-H003-EXT-001), no cells survive Holm correction
- **Track A (observed liquidations):** STRUCTURALLY_BLOCKED — no admissible unauthenticated historical source with required coverage
- **Risk overlay:** NOT ELIGIBLE (no passed OOS forecasting gate)

**Environment constraints (verified 2026-11-10, still binding):**
- No network/downloads, no paid/manual/credentialed data
- No workflow/scheduler/poller additions
- No fabricated provenance or outcomes
- No threshold shopping or sealed-holdout reuse
- Stdlib only (numpy, pandas, scipy, pyarrow, requests allowed but no pip install)

---

## ACTIVE RANK-0 CAMPAIGN: FCLR-LIVE-ARCHIVE-08

**Status:** `READY_EXECUTE` | **Program:** `ACTIVE` | **Rank:** 0
**Experiment ID:** `FCLR-LIVE-ARCHIVE-08` (generated 20261127T080708Z)
**Campaign start (gate anchor):** `20261127T131654Z`

### Task Definition (from experiment_frontier.json rank-0)
> **Track-B modeled boundary-breach forecast (NOT an overlay):**
> Pre-registered hypothetical long/short liquidation boundaries from disclosed constant margin/leverage scenarios; target = whether the future mark-price path breaches the boundary within a fixed horizon; separate long/short labels; compare a funding-conditioned model vs a mark-price-only baseline by out-of-sample AUC / log-loss / Brier with >=2000 block-bootstrap and leave-one-symbol-out; independent stdlib recompute all_checks_match=true. Stdlib only, read-only cache, no network.

### Frozen Design (MUST REUSE EXACTLY)
- **Data domain:** Binance 5-symbol (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) monthly futures archive (markPriceKlines, fundingRate, premiumIndexKlines, indexPriceKlines) 2024-04..2026-10
- **Common support S:** Balanced mark-price hourly intersection, `|S| = 22608` timestamps (all five symbols present, close>0). XRPUSDT 2025-10-19 has 24 corrupt closes (quarantined, not zero-filled); other four symbols 22608 each. Split: 60/20/20 + 168h embargo (train=13550, val=4517, test=4517 per symbol; test rows across 5 symbols = 22585)
- **Estimands:** Long-breach / short-breach AUC, log-loss, Brier. Baseline = mark-price-only (RV + lagged returns). Candidate = funding-conditioned (adds funding rate, premium, dislocation/smoothing features). Materiality floor: >=2% relative improvement with 95% block-bootstrap CI lower bound > 0.
- **Multiplicity:** Leave-one-symbol-out + >=2000 block-bootstrap. Symmetric verdict (NOT_SUPPORTED / SUPPORTED / INCONCLUSIVE) frozen before outcomes.

### Required Artifact Set (enforced by `scripts/check_handoff_heavywork_gate.py` — LIVE_ARCHIVE_REQUIRED)
All artifacts must be non-empty and placed under **one fresh** `research_state/session_<UTC>/` directory with session ID **> 20261127T131654Z** (NOT merely > 20261127T065600Z — the interval (20261127T065600Z, 20261127T131654Z] is GRANDFATHERED and FORBIDDEN).

| Artifact Prefix | Suffixes | Description |
|-----------------|----------|-------------|
| `fclr_live_archive_source_registry_` | `.json`, `.md` | Outcome-blind source registry: verified cache read (paths, sha256, coverage, layouts), hash-bound to `cached_inputs_hashes.json` |
| `fclr_live_archive_prereg_` | `.json`, `.md` | Outcome-blind prereg freeze: margin/leverage scenarios, horizon, long/short labels, estimands, floor, alpha, bootstrap, split sizes on S — `outcome_data_inspected_before_freeze: false` |
| `fclr_live_archive_eval_` | `.py`, `.json`, `.md` | Heavy 3-block evaluation on common support S: funding-conditioned vs mark-price-only, AUC/log-loss/Brier, >=2000 block bootstrap + leave-one-symbol-out |
| `fclr_live_archive_recompute_` | `.py`, `.json` | **Independent stdlib recompute** that rebuilds S and confirms all_checks_match=true, all five symbols in every block/fold, n_test>=500 |
| `fclr_live_archive_evidence_audit_` | `.json`, `.md` | Evidence audit: artifact hashes, config reproduction, verdict traceability |
| `evidence_audit_` | `.json` | Gate-critical alias (must exist alongside the named audit) |
| `trigger_check_` | `.json` | Gate trigger check (non-empty) |

### Blocker Resolution (from experiment_frontier.json)
- **None external.** No aborted session on disk; newest complete session is `20261127T065600Z` (FCLR-LIVE-ARCHIVE-07, NOT_SUPPORTED).
- **Forecast gate (campaign-07) did NOT pass** → per RESEARCH_PROMPT §9 NO risk overlay is authorized; campaign-08 is forecast validation of a modeled boundary-breach target, which is permitted.
- **Reuse the campaign-07 mark-price cache read-only; do NOT re-download.**

---

## GATE ENFORCEMENT

The handoff gate (`scripts/check_handoff_heavywork_gate.py`) is **machine-enforced**. A session passes only if:
1. `AGENT_HANDOFF.md` exists with `INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SECTION` and records the last completed heavy session ID + full-suite result.
2. The latest session contains the **exact LIVE_ARCHIVE_REQUIRED artifact set** (all 10 files, non-empty) under a fresh `session_<UTC>/` with ID > 20261127T131654Z.
3. `research_state/` root md+json count ≤ 500 (churn cap).
4. Independent recompute achieves `all_checks_match=true`.

**Failure modes to avoid:**
- Trigger-only, prose-only, audit-only, verify-and-stop sessions → **FAIL**
- Arbitrary `recompute_*` without the full triad → **FAIL**
- Session ID ≤ 20261127T131654Z → **FAIL** (grandfathered interval forbidden)
- Zero-byte placeholders → **FAIL**
- Root churn cap breach → **FAIL**

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**TIMESTAMP:** 2026-11-27T22:06:41Z
**SESSION CONSTRAINT:** New session ID must be **> 20261127T131654Z** (e.g., `session_20261127T220641Z` or later)

### MANDATORY WORKPLAN (execute in order, single session)

#### Phase 1: Source Registry & Prereg Freeze (outcome-blind)
1. **Verify cache** — Read `research_state/data_cache/{BNBUSDT,BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT}_2024_04..2026_10/` mark-price klines + funding. Assert every `.sha256` sidecar against `research_state/cached_inputs_hashes.json` (20694 entries). Record coverage, layouts, shortfalls.
2. **Rebuild common support S** — All-five-symbol hourly intersection (mark-price close>0, dedup by open_time) restricted to 2024-04-01..2026-10-31 UTC. Freeze `|S|=22608` and split sizes (train=13550, val=4517, test=4517 per symbol; test rows across 5 symbols = 22585).
3. **Emit source registry** — `fclr_live_archive08_source_registry_<UTC>.{json,md}` under the new session dir.
4. **Freeze prereg** — Outcome-blind: margin/leverage scenarios (disclosed constant), breach horizon, long/short labels, estimands (AUC/log-loss/Brier), baseline (mark-price-only RV+lagged returns), candidate (funding-conditioned), materiality floor (2% relative, CI lower bound > 0), alpha (Holm across declared family), bootstrap (>=2000 block + leave-one-symbol-out), split on S. Hash-bound to source registry. `outcome_data_inspected_before_freeze: false`. Emit `fclr_live_archive08_prereg_<UTC>.{json,md}`.

#### Phase 2: Heavy Boundary-Breach Evaluation
5. **Implement evaluation** — Stdlib only (no sklearn, no external ML libs). Rolling-origin 3-block on S: for each block, train on prior train+val, embargo 168h, test on block. Generate hypothetical long/short liquidation boundaries from margin/leverage scenarios. Compute breach labels (future mark-price path breaches boundary within horizon). Fit baseline (mark-price-only) and candidate (funding-conditioned) models. Score AUC, log-loss, Brier. Block bootstrap (>=2000) + leave-one-symbol-out for CIs and multiplicity.
6. **Emit evaluation triad** — `fclr_live_archive08_eval_<UTC>.{py,json,md}` (code, results, report).

#### Phase 3: Independent Recompute & Evidence Audit
7. **Independent recompute** — Separate code path (stdlib only) that rebuilds S from cache, re-runs the full evaluation, asserts `all_checks_match=true`, confirms all five symbols in every block/fold, n_test>=500. Emit `fclr_live_archive08_recompute_<UTC>.{py,json}`.
8. **Evidence audit** — Artifact hashes, config reproduction, verdict traceability. Emit `fclr_live_archive08_evidence_audit_<UTC>.{json,md}` + alias `evidence_audit_<UTC>.json`.
9. **Trigger check** — Non-empty `trigger_check_<UTC>.json` with gate status.

### SUCCESS CRITERIA
- All 10 required artifacts present, non-empty, under one fresh `session_<UTC>/` (ID > 20261127T131654Z)
- `scripts/check_handoff_heavywork_gate.py` exits 0 (PASS)
- `all_checks_match=true` from independent recompute
- Symmetric verdict (NOT_SUPPORTED / SUPPORTED / INCONCLUSIVE) recorded in prereg and evaluation

### REFERENCE ARTIFACTS (from campaign-07, session_20261127T065600Z)
- Template eval: `research_state/session_20261127T065600Z/fclr_live_archive07_eval_20261127T065600Z.py`
- Template recompute: `research_state/session_20261127T065600Z/fclr_live_archive07_recompute_20261127T065600Z.py`
- Template prereg: `research_state/session_20261127T065600Z/fclr_live_archive07_prereg_20261127T065600Z.json`
- Source registry: `research_state/session_20261127T065600Z/fclr_live_archive07_source_registry_20261127T065600Z.json`

---

## CONTEXT: WHY THIS CAMPAIGN EXISTS

The repository name leads with **"Funding-conditioned-volatility"**, yet every leakage-robust volatility null was established on a 5-coin panel. The Binance public market-data archive at `data.binance.vision` (metrics dataset: daily open interest + taker long/short flow, deep 2020-09→present, plus fundingRate/klines/mark/index/premium) is a **verified, unauthenticated, free source that was never exploited**. The frozen-data frontier is exhausted (`next_campaign_status.py: NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN`). This campaign removes the "prose-only / source-probe-only / verify-and-stop" escape hatch by mandating a **materially different, verified, confirmatory design on newly downloaded archive data** — but for the **liquidation-risk** half (Track B modeled boundary breaches), which is permitted because the forecast gate (campaign-07) did NOT pass (no risk overlay authorized).

---

## COMPLETED CAMPAIGNS (DO NOT RE-RUN)

| Campaign | Session | Verdict | Status |
|----------|---------|---------|--------|
| FCLR-LIVE-ARCHIVE-07 | 20261127T065600Z | NOT_SUPPORTED (C2 vs B1 rel -0.704%, CI [-1.218%,-0.190%]) | COMPLETED_VALIDATED |
| FCLR-LIVE-ARCHIVE-06 | 20261126T133828Z | NOT_SUPPORTED (downside semivar level, rel MSE 0.716%, CI [0.419%,1.020%]) | COMPLETED_VALIDATED |
| FCLR-LIVE-ARCHIVE-05 | 20261126T082429Z | NOT_SUPPORTED (signed semivar asymmetry, rel MSE 0.141%) | COMPLETED_VALIDATED |
| FCLR-LIVE-ARCHIVE-04 | 20261126T061929Z | NOT_SUPPORTED (quantile/full-dist, rel pinball -1.102%) | COMPLETED_VALIDATED |
| FCLR-LIVE-ARCHIVE-03 | 20261126T051548Z | NOT_SUPPORTED (stress/tail Brier, rel 0.458%) | COMPLETED_VALIDATED |
| FCLR-LIVE-ARCHIVE-01 | 20261126T042519Z | NOT_SUPPORTED (mean-RV QLIKE, rel 0.840%) | COMPLETED_VALIDATED |
| FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 | 20261125T060000Z | NOT_SUPPORTED (formal closure + meta-analysis) | COMPLETED_VALIDATED |
| FCLR-VOL-JUMP-04..01 | 20261125T030000Z..054500Z | NOT_SUPPORTED (all volatility-jump arms) | COMPLETED_VALIDATED |
| FCLR-VOL-STRESS-01 | 20261124T222500Z | NOT_SUPPORTED (vol stress/tail) | COMPLETED_VALIDATED |
| FCLR-VOL-CORR-01 | 20261124T204500Z | NOT_SUPPORTED (correction-time/hazard) | COMPLETED_VALIDATED |
| FCLR-VOL-BROAD-01 | 20261124T120000Z | NOT_SUPPORTED (mean log-RV QLIKE broad) | COMPLETED_VALIDATED |

**All volatility arms (Track C) are CLOSED. Track A is STRUCTURALLY_BLOCKED. Track B (this campaign) is the only remaining confirmatory path.**

---

## KEY FILES TO READ BEFORE STARTING

1. `research_state/experiment_frontier.json` — rank-0 task definition (this campaign)
2. `research_state/final_synthesis_report.md` — program conclusion evidence
3. `scripts/next_campaign_status.py` — cache frontier truth (run with `--json`)
4. `scripts/check_handoff_heavywork_gate.py` — gate enforcement (LIVE_ARCHIVE_REQUIRED)
5. `research_state/session_20261127T065600Z/` — campaign-07 template artifacts
6. `research_state/cached_inputs_hashes.json` — 20694 verified checksums
7. `research_state/data_cache/` — read-only Binance 5-symbol monthly archive

---

**This handoff is durable and machine-actionable. The next session MUST execute the full FCLR-LIVE-ARCHIVE-08 artifact set in a single fresh session with ID > 20261127T131654Z. No partial, deferred, or prose-only work will pass the gate.**