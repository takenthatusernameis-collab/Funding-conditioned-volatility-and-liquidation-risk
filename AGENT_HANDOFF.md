# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Timestamp:** 2026-11-20T18:07:07Z
**Session:** FCLR-STARTER-001 COMPLETE (NOT_SUPPORTED); FCLR-XSEC-001 COMPLETE (NOT_SUPPORTED, session_20261120T175300Z); all prior campaigns SUPERSEDED; root research_state/ md+json count 499/500 — churn cap enforced by test_tracka_hardening_125 (ONE root-level md/json file remaining before cap breach fails heavy-work gate); heavy-work gate: scripts/check_handoff_heavywork_gate.py must be re-verified after any session writes; tests/test_active_campaign_gate.py invariant: exactly one rank-0 ACTIVE/READY_EXECUTE, all others SUPERSEDED (full suite run timed out at >120s — run targeted tests only).
**Campaign declared:** FCLR-XSEC-002-20261120T180707Z (start UTC 20261120T180707Z) — UTC-hour / market-wide-RV conditioning of funding effect (contingency ladder mechanism 1).
**Latest heavy session:** session_20261120T175300Z (FCLR-XSEC-001 Steps 1/2/3 COMPLETE: protocol freeze, within-hour baselines, cross-sectional evaluation + block bootstrap + Holm + independent recompute + evidence audit; verdict NOT_SUPPORTED).
**Status:** FCLR-STARTER-001 COMPLETE — Track C 24h forward RV forecast, verdict NOT_SUPPORTED, holdout inspected/sealed. FCLR-XSEC-001 COMPLETE — within-hour cross-sectional funding contrast, verdict NOT_SUPPORTED (funding contrast CI [−0.390010, +0.157598] includes zero, Holm adj_p=0.388, n=5,334 hours, 5 coins); RV persistence baseline also NOT_SUPPORTED (CI [−0.121076, +0.487735], Holm adj_p=0.514). FCLR-XSEC-002 is the distinct-regime exploratory successor; all phases NOT_STARTED.

---

# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-20T18:07:07Z)

FCLR-STARTER-001 and FCLR-XSEC-001 are both COMPLETE with verdict **NOT_SUPPORTED**. No funding-conditioned feature set has improved volatility forecasting on the frozen panel across two distinct identification strategies (time-series 24h forward RV; within-hour cross-sectional funding contrast).

**Summary of completed campaigns:**
- **FCLR-STARTER-001** (session_20261120T052201Z/): C2 vs B1 diff +0.0094, 95% CI [+0.0024, +0.0164], rel +2.62% (worse), Holm adj_p=0.075, verdict NOT_SUPPORTED. Holdout opened=true, sealed.
- **FCLR-XSEC-001** (session_20261120T175300Z/): funding contrast mean diff −0.125751, 95% CI [−0.390010, +0.157598], p=0.388, Holm adj_p=0.388; RV persistence baseline mean diff +0.176794, 95% CI [−0.121076, +0.487735], p=0.257, Holm adj_p=0.514; verdict NOT_SUPPORTED. Holdout NOT opened. Panel hash 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4 verified.

**Required artifacts emitted under research_state/session_20261120T175300Z/:**
1. `fclr_xsec001_protocol_freeze_20261120T175300Z.json` + `.md` — preregistered protocol, outcome_data_inspected_before_freeze=false
2. `fclr_xsec001_baselines_20261120T175300Z.py` + `.json` + `.md` — within-hour RV persistence baseline
3. `fclr_xsec001_evaluation_20261120T175300Z.py` + `.json` + `.md` — cross-sectional evaluation, verdict NOT_SUPPORTED
4. `trigger_check_20261120T175300Z.json` — non-empty, 9 checks all PASS
5. `evidence_audit_20261120T175300Z.md` — evidence audit
6. `independent_recompute_fclr_xsec001_20261120T175300Z.py` + `.json` — independent numpy-only recompute

**Do NOT:** Re-run FCLR-STARTER-001 (protocol frozen, holdout inspected). Re-run FCLR-XSEC-001 (verdict emitted, artifacts complete). Overwrite `research_state/research_protocol.md` (sealed legacy). Modify `.github/workflows` (protected control plane). Add any root-level `research_state/*.md` or `research_state/*.json` file (root churn cap 499/500 — one remaining slot). Create empty placeholder files.

---

## 1. What changed and why

**Prior state:** FCLR-XSEC-001 was the rank-0 READY_EXECUTE campaign per the previous handoff (timestamped 2026-11-20T18:06:40Z). It has since been fully executed in session_20261120T175300Z/. Both the funding contrast and the RV persistence baseline fail the gate (CI includes zero, Holm fails). Null result preserved; no threshold shopping.

**Why the next campaign is the highest-value task:**
1. Track A liquidation forecasting: power-blocked (RISK-12 UNDERPOWERED, MDE 0.0028 > plausible 0.001, all 6 family members NOT_MET)
2. Track B modeled boundary breach: NOT_SUPPORTED (TB2 Log Loss +1.68% rel, below 2% floor, CI crosses zero, Holm FAILS, only 2 blocks <3 required)
3. Track C time-series 24h RV forecast: NOT_SUPPORTED (FCLR-STARTER-001)
4. Track C cross-sectional funding contrast: NOT_SUPPORTED (FCLR-XSEC-001, just completed)
5. Per RESEARCH_PROMPT.md §16 contingency ladder, mechanism 1 (UTC-hour / market-wide-RV conditioning) is the next distinct-mechanism exploratory route on the same frozen panel — same data, different identification (regime conditioning rather than within-hour contrast).
6. Infrastructure complete: baselines, features, eval, block bootstrap, walk-forward splits all implemented in src/ and scripts/.

**Evidence for NOT_SUPPORTED verdicts:**
- FCLR-STARTER-001: C1 +4.24% rel QLIKE vs B1, C2 +2.62% rel vs B1 (CI entirely positive, p<0.05); no feature ablation passes ≥2% relative QLIKE reduction
- FCLR-XSEC-001: funding contrast CI [−0.390010, +0.157598] includes zero (p=0.388, Holm adj_p=0.388); RV persistence baseline CI [−0.121076, +0.487735] includes zero (p=0.257, Holm adj_p=0.514); robust across 5 coins and 5,334+ hours

---

## 2. Current state of each research gate

| Gate | Track | Status | Evidence |
|------|-------|--------|----------|
| Source feasibility | All | PARTIAL | Hyperliquid mark/index/funding/klines admissible; Binance public archive not probed for sealed months |
| Label decision | Track A | DECIDED | Hyperliquid observed labels (incomplete census, documented); Track B/C viable without Track A |
| Protocol freeze (FCLR-001) | Track C | COMPLETE | `research_state/protocol_fclr_starter_001_20261120T024217Z.md` (hash-bound to §14) |
| Panel freeze | Track C | COMPLETE | `research_state/session_20261120T024217Z/fclr_starter001_panel_freeze_20261120T024217Z.json` (panel_sha256, panel_frozen_before_target_generation=true) |
| Baseline first | Track C | COMPLETE | B0 (persistence RV24h QLIKE=0.5743) and B1 (HAR OLS QLIKE=0.5413) on dev/validation; holdout_opened=false |
| Incremental features | Track C | COMPLETE | C1/C2 evaluated on holdout; funding + ema24_dist do not improve over B1 (NOT_SUPPORTED) |
| Cross-sectional funding contrast | Track C | COMPLETE | FCLR-XSEC-001 NOT_SUPPORTED (CI includes zero, Holm adj_p=0.388) |
| Forecast gate | Track C | NOT_PASSED | Both time-series and cross-sectional identification strategies failed |
| Overlay eligibility | — | BLOCKED | Requires forecast gate pass first |

---

## 3. Single highest-value next task — FCLR-XSEC-002 (heavy work, non-deferrable)

**Execute a distinct-regime exploratory campaign on the frozen FCLR-001 panel (research_state/fclr011_recompute_panel_20261115T234700Z.parquet).**

**Why:** FCLR-XSEC-001 is complete with verdict NOT_SUPPORTED. Per RESEARCH_PROMPT.md §16 (adaptive feasibility policy) and the contingency ladder in §6 of the prior handoff, the next step is mechanism 1: UTC-hour / market-wide-RV conditioning — test whether funding's predictive value is concentrated in specific regimes (high RV hours, specific UTC sessions). This is a distinct estimand from both FCLR-STARTER-001 (time-series 24h RV) and FCLR-XSEC-001 (within-hour cross-sectional funding contrast). It uses the same frozen panel but conditions on market-wide RV regime before testing the funding effect.

**Candidate mechanisms (from contingency ladder, prioritized by expected information gain):**
1. **FCLR-XSEC-002 — UTC-hour / market-wide-RV conditioning** — Split hours by market-wide RV tercile (or high/low RV session). Within each regime, test the within-hour funding contrast. If funding only matters in high-RV hours, the time-series and cross-sectional nulls may be regime-masked. **Recommended.**
2. **liq_count persistence family** — Use observed liquidation count at t-1 as predictor for t liquidation intensity (uses Track A labels already in panel if available)
3. **RISK-13** — Per RISK-12 evidence audit: advance only if MDE ≤ plausible effect via MDE-by-instrument redesign or larger panel (requires new data, lower priority)
4. **Track B modeled boundary-breach** — If contract specs and margin tiers verifiable from public sources

**Exact specification for next session:**
- **Unit:** Eligible linear perpetual contract × closed UTC hourly timestamp (same as FCLR-001 / FCLR-XSEC-001)
- **Panel:** Frozen FCLR-001 panel (panel_sha256: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4)
- **Target:** Next-hour realized variance (rv1h at t+1)
- **Predictor:** Within-hour cross-sectional funding rank (high vs low funding percentile within hour), computed separately within each market-wide RV regime
- **Regime variable:** Market-wide RV at hour t = cross-sectional mean of coin rv1h at t; split into high/low tercile (or Asian/European/US UTC session buckets)
- **Baseline:** Within-hour RV persistence within each regime
- **Evaluation:** Within-regime paired comparison, block bootstrap across hours within regime, Holm over family (regimes × contrasts)
- **Protocol:** New experiment ID (FCLR-XSEC-002-20261120T180707Z), preregistered before examining outcomes

**Do NOT:** Re-run FCLR-STARTER-001. Re-run FCLR-XSEC-001. Modify sealed protocol. Claim Track A/B results without new evidence. Add root-level md/json files (churn cap 499/500).

---

## 4. Precise command/check to verify completion — MACHINE-ENFORCED HEAVY-WORK GATE

**Next session must:**
1. Read this handoff + RESEARCH_PROMPT.md completely
2. Inspect working tree and latest artifacts (session_20261120T175300Z/, session_20261120T052201Z/)
3. Preregister a new exploratory protocol (FCLR-XSEC-002) for UTC-hour / market-wide-RV conditioning
4. Run the analysis on the frozen panel (panel_sha256 must match)
5. Emit protocol freeze, baselines, evaluation, and trigger_check artifacts under a new timestamped session directory

**Acceptance test for next session:**
- New `research_state/session_<UTC>/` with:
  - `fclr_xsec002_protocol_freeze_<UTC>.json` + `.md` — new protocol, hash-bound, distinct estimand from FCLR-001 and FCLR-XSEC-001
  - `fclr_xsec002_baselines_<UTC>.py` + `.json` + `.md` — within-regime baseline metrics
  - `fclr_xsec002_evaluation_<UTC>.py` + `.json` + `.md` — regime-conditioned evaluation results
  - `trigger_check_<UTC>.json` — non-empty
- `experiment_frontier.json` rank 0 = FCLR-XSEC-002, status READY_EXECUTE / ACTIVE, FCLR-XSEC-001 marked SUPERSEDED
- `python3 -m unittest tests/test_active_campaign_gate.py tests/test_tracka_hardening_125.py` returns 0 failures (full suite exceeds 120s timeout — run targeted tests only)
- No holdout outcomes inspected before protocol freeze
- Zero-byte placeholder files do NOT count — every artifact must contain meaningful content
- All new artifacts go under `research_state/session_<UTC>/` — the root research_state/ md+json count is 499/500; one root-level md/json file breaches the churn cap and fails the heavy-work gate

**Non-avoidance:** A future agent cannot satisfy the heavy-work gate with prose, trigger-check-only, or placeholder artifacts. The machine-enforced gate (scripts/check_handoff_heavywork_gate.py + tests/test_active_campaign_gate.py) requires the concrete artifact triad plus a non-empty trigger_check in the latest session directory.

---

## 5. Source/engineering blockers and next free route

| Blocker | Evidence | Next materially different free route |
|---------|----------|--------------------------------------|
| No Binance liquidation labels | Binance public archive requires manual download or requester-pays; no unauthenticated historical liquidation feed | Use frozen Hyperliquid panel for regime-conditioned mechanism; register separate Binance-arm protocol if/when archive access verified |
| Track A power limit | RISK-12 MDE=0.0028 > plausible 0.001; 13 coins, 12 months insufficient | Regime-conditioned mechanism uses within-hour variation, different statistical power profile |
| Sealed Binance months unread | RESEARCH_PROMPT.md prohibits reading sealed months for outcomes | Frozen panel already available; no new data needed for exploratory mechanism |
| No historical market-cap ranks | Free point-in-time ranks unavailable | Venue-native universe — all discoverable perpetuals from public listing metadata |
| Root research_state/ md+json count | 499/500 — one new root-level md/json file breaches the churn cap enforced by test_tracka_hardening_125 and fails the heavy-work gate | All new artifacts go under a timestamped session_<UTC>/ directory; do NOT add root-level md/json files |
| FCLR-STARTER-001 forecast gate NOT_PASSED | C2 vs B1 +2.62% QLIKE, CI positive, Holm FAILS | Distinct-mechanism exploratory campaign (cross-sectional) — now also NOT_SUPPORTED |
| FCLR-XSEC-001 forecast gate NOT_PASSED | Funding contrast CI [−0.390010, +0.157598], Holm adj_p=0.388 | Regime-conditioned mechanism (UTC-hour / market-wide-RV conditioning) on same frozen panel |
| session_20261120T172000Z/ empty | Empty session directory, no artifacts, no purpose | Remove or repurpose; do not create new empty session directories |
| experiment_frontier.json stale | Rank 0 still shows FCLR-XSEC-001 READY_EXECUTE/ACTIVE with phases NOT_STARTED, but work is COMPLETE | Update frontier: rank 0 = FCLR-XSEC-002 READY_EXECUTE/ACTIVE, FCLR-XSEC-001 SUPERSEDED |
| hypothesis_registry.json stale | No FCLR-XSEC-001 or FCLR-XSEC-002 hypothesis entry | Register FCLR-XSEC-002 hypothesis with NOT_STARTED status |

**Do not:**
- Re-run FCLR-STARTER-001 (protocol frozen, holdout inspected, verdict emitted)
- Re-run FCLR-XSEC-001 (verdict emitted, artifacts complete under session_20261120T175300Z/)
- Re-run RISK-09/10/11/12 variants (explicitly prohibited in RISK-12 prereg)
- Attempt Track A liquidation forecasting without a materially larger panel
- Modify `.github/workflows` (protected control plane)
- Create placeholder artifacts — only create when contents are meaningful
- Overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03)
- Add root-level `research_state/*.md` or `research_state/*.json` files (churn cap 499/500)

---

## 6. Contingency ladder (if regime-conditioned mechanism blocked)

If the UTC-hour / market-wide-RV conditioning hits a structural blocker (e.g., insufficient regime variation, funding rank collinear with RV within regimes):

1. **liq_count persistence family** — If Track A labels have adequate coverage, test t-1 liquidation count as predictor
2. **RISK-13** — Per RISK-12 evidence audit: advance only if MDE ≤ plausible effect via MDE-by-instrument redesign or larger panel
3. **Track B modeled boundary-breach** — If contract specs and margin tiers verifiable from public sources

---

## 7. Next session must

Read this handoff + RESEARCH_PROMPT.md completely, inspect working tree and latest artifacts (session_20261120T175300Z/, session_20261120T052201Z/), then **preregister and execute a distinct-regime exploratory campaign (FCLR-XSEC-002: UTC-hour / market-wide-RV conditioning) on the frozen FCLR-001 panel**. No other task has higher expected information gain per unit of free compute. The FCLR-STARTER-001 and FCLR-XSEC-001 campaigns are complete with final NOT_SUPPORTED verdicts; the machine-enforced handoff heavy-work gate requires the concrete artifact triad for any new campaign — future agents cannot satisfy it with prose or placeholders.

(End of file)
