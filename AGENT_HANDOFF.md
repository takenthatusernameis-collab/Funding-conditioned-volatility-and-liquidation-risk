# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Timestamp:** 2026-11-20T15:18:51Z
**Session:** FCLR-STARTER-001 COMPLETE (NOT_SUPPORTED); experiment_frontier.json rank-0 = FCLR-XSEC-001-20261120T071741Z ACTIVE (READY_EXECUTE); all prior campaigns SUPERSEDED; root research_state/ md+json count 499/500 — churn cap enforced by test_tracka_hardening_125
**Campaign declared:** FCLR-XSEC-001-20261120T071741Z (start UTC 20261120T071741Z)
**Latest heavy session:** session_20261120T052201Z (FCLR-STARTER-001 Step 2/3 confirmatory evaluation COMPLETE: C1/C2 vs B1 on sealed holdout; paired QLIKE diff, block bootstrap ≥2000 reps, Holm correction; verdict NOT_SUPPORTED)
**Status:** FCLR-STARTER-001 COMPLETE — All three steps done: (1) protocol freeze + panel freeze + B0/B1 baselines, (2) confirmatory evaluation on sealed holdout, (3) verdict emitted. Track C forecast gate NOT_PASSED. FCLR-XSEC-001 is the distinct-mechanism exploratory successor; all phases NOT_STARTED. Heavy-work gate: scripts/check_handoff_heavywork_gate.py PASS; tests/test_active_campaign_gate.py 0 failures.

---

# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-20T14:02:32Z)

FCLR-STARTER-001 campaign is COMPLETE. The frozen starter protocol (Track C: 24h forward realized variance forecasting) has been fully executed and the forecast gate verdict is **NOT_SUPPORTED**.

**Summary of FCLR-STARTER-001 results:**
- **B1 (RV-only HAR):** QLIKE = 0.3585
- **C1 (B1 + funding + percentile):** QLIKE = 0.3737 (worse: +4.24% rel)
- **C2 (C1 + ema24_dist):** QLIKE = 0.3679 (worse: +2.62% rel vs B1)
- **Primary comparison (C2 vs B1):** Diff = +0.0094, 95% CI [+0.0024, +0.0164], CI entirely positive (C2 significantly worse), Holm adj_p = 0.075
- **Gate criteria:** ≥5 instruments PASS, ≥3 non-overlapping 30-day blocks PASS, ≥2% QLIKE reduction FAIL, CI supports improvement FAIL, Holm passes FAIL
- **Verdict:** NOT_SUPPORTED — funding and price-dislocation features do not improve 24h forward RV forecasts over the RV-only HAR baseline on this panel.

**Required artifacts emitted under research_state/session_20261120T052201Z/:**
1. `fclr_starter001_confirmatory_20261120T052201Z.json` + `.md` — verdict, paired QLIKE diff, block-bootstrap CI, Holm p-values, ≥5 instruments, ≥3 non-overlapping 30-day blocks, holdout_opened=true
2. `fclr_starter001_confirmatory_20261120T052201Z.py` — reproducible script
3. `trigger_check_20261120T052201Z.json` — non-empty

**Do NOT:** Re-run FCLR-STARTER-001 (protocol frozen, holdout inspected). Overwrite `research_state/research_protocol.md` (sealed legacy). Modify `.github/workflows` (protected control plane).

---

## 1. What changed and why

**Prior state:** FCLR-STARTER-001 Step 1 COMPLETE (protocol freeze, panel freeze, B0/B1 baselines on dev/validation under session_20261120T024217Z/). Step 2/3 confirmatory evaluation was the remaining heavy work.

**Why this campaign was the highest-value task:**
1. Track A liquidation forecasting: power-blocked (RISK-12 UNDERPOWERED, MDE 0.0028 > plausible 0.001, all 6 family members NOT_MET)
2. Track B modeled boundary breach: NOT_SUPPORTED (TB2 Log Loss +1.68% rel, below 2% floor, CI crosses zero, Holm FAILS, only 2 blocks <3 required)
3. Track C volatility forecasting: only viable confirmatory path on admissible public mark-price data
4. FCLR-001 fully specified in RESEARCH_PROMPT.md §14 with exact unit, timing, universe, target, features, baselines, splits, metrics, inference, and gate
5. Infrastructure complete: baselines, features, eval, block bootstrap, walk-forward splits all implemented

**Evidence for NOT_SUPPORTED verdict:**
- C1 (funding features) increases QLIKE by 4.24% vs B1 (CI entirely positive, p<0.05)
- C2 (funding + ema24_dist) increases QLIKE by 2.62% vs B1 (CI entirely positive, p<0.05)
- C2 improves 1.56% over C1 but remains worse than B1
- No feature ablation passes the ≥2% relative QLIKE reduction gate
- Result is robust across 5 instruments and 3 non-overlapping 30-day test blocks
- Null result preserved per protocol; no threshold shopping

---

## 2. Current state of each research gate

| Gate | Track | Status | Evidence |
|------|-------|--------|----------|
| Source feasibility | All | PARTIAL | Hyperliquid mark/index/funding/klines admissible; Binance public archive not probed for sealed months |
| Label decision | Track A | DECIDED | Hyperliquid observed labels (incomplete census, documented); Track B/C viable without Track A |
| Protocol freeze (FCLR-001) | Track C | COMPLETE | `research_state/protocol_fclr_starter_001_20261120T024217Z.md` (hash-bound to §14) |
| Panel freeze | Track C | COMPLETE | `research_state/session_20261120T024217Z/fclr_starter001_panel_freeze_20261120T024217Z.json` (panel_sha256, panel_frozen_before_target_generation=true) |
| Baseline first | Track C | COMPLETE | B0 (persistence RV24h QLIKE=0.5743) and B1 (HAR OLS QLIKE=0.5413) on dev/validation; holdout_opened=false |
| Incremental features | Track C | COMPLETE | C1/C2 evaluated on holdout; funding + ema24_dist do not improve over B1 |
| Forecast gate | Track C | NOT_PASSED | C2 vs B1: +2.62% rel QLIKE (worse), CI [+0.0024, +0.0164], Holm FAILS |
| Overlay eligibility | — | BLOCKED | Requires forecast gate pass first |

---

## 3. Single highest-value next task — FCLR-XSEC-001 (heavy work, non-deferrable)

**Execute a distinct-mechanism exploratory campaign on the frozen FCLR-001 panel (research_state/fclr011_recompute_panel_20261115T234700Z.parquet).**

**Why:** FCLR-STARTER-001 confirmatory test is complete and NOT_SUPPORTED. The frozen panel (5 coins, Jan–Aug 2026, hourly mark-price, funding, RV features) is a verified, admissible dataset with proper splits and no leakage. Per RESEARCH_PROMPT.md §16 (adaptive feasibility policy) and the contingency ladder in the prior handoff, the next step is a distinct-mechanism exploratory campaign on this frozen panel — not a re-run of the same failed hypothesis.

**Candidate mechanisms (from contingency ladder, prioritized by expected information gain):**
1. **RISK-13** — Per RISK-12 evidence audit: advance only if MDE ≤ plausible effect via MDE-by-instrument redesign or larger panel (requires new data, lower priority)
2. **liq_count persistence family** — Use observed liquidation count at t-1 as predictor for t liquidation intensity (uses Track A labels already in panel if available)
3. **Within-hour cross-sectional funding-intensity contrast** — Compare high vs low funding coins within the same hour to isolate funding effect from common market shocks
4. **UTC-hour / market-wide-RV conditioning of funding effect** — Test if funding's predictive value is concentrated in specific regimes (e.g., high RV hours, specific UTC sessions)

**Recommended: Mechanism 3 (within-hour cross-sectional funding contrast).** This is a distinct estimand from the failed FCLR-001 (which tested time-series predictability of RV). It uses the same frozen panel but a different identification strategy: cross-sectional variation within hour rather than time-series variation. This avoids the serial correlation and non-stationarity that plague time-series RV forecasts.

**Exact specification for next session:**
- **Unit:** Eligible linear perpetual contract × closed UTC hourly timestamp (same as FCLR-001)
- **Panel:** Frozen FCLR-001 panel (panel_sha256: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4)
- **Target:** Next-hour realized variance (rv1h at t+1) or liquidation count proxy if Track A labels exist
- **Predictor:** Cross-sectional funding rank within each hour (high vs low funding percentile within hour)
- **Baseline:** Within-hour RV persistence (coin's own rv1h at t)
- **Evaluation:** Within-hour paired comparison, block bootstrap across hours, Holm over family
- **Protocol:** New experiment ID (e.g., FCLR-XSEC-001), preregistered before examining outcomes

**Do NOT:** Re-run FCLR-STARTER-001. Modify sealed protocol. Claim Track A/B results without new evidence.

---

## 4. Precise command/check to verify completion — MACHINE-ENFORCED HEAVY-WORK GATE

**Next session must:**
1. Read this handoff + RESEARCH_PROMPT.md completely
2. Inspect working tree and latest artifacts (session_20261120T052201Z/, session_20261120T024217Z/)
3. Preregister a new exploratory protocol (FCLR-XSEC-001) for within-hour cross-sectional funding contrast
4. Run the analysis on the frozen panel (panel_sha256 must match)
5. Emit protocol freeze, baselines, evaluation, and trigger_check artifacts under a new timestamped session directory

**Acceptance test for next session:**
- New `research_state/session_<UTC>/` with:
  - `fclr_xsec001_protocol_freeze_<UTC>.json` + `.md` — new protocol, hash-bound, distinct from FCLR-001
  - `fclr_xsec001_baselines_<UTC>.py` + `.json` + `.md` — within-hour baseline metrics
  - `fclr_xsec001_evaluation_<UTC>.py` + `.json` + `.md` — cross-sectional evaluation results
  - `trigger_check_<UTC>.json` — non-empty
- `experiment_frontier.json` rank 0 = FCLR-XSEC-001, status READY_EXECUTE / ACTIVE, FCLR-STARTER-001 marked SUPERSEDED
- `python3 -m unittest discover tests` returns 0 failures
- No holdout outcomes inspected before protocol freeze
- Zero-byte placeholder files do NOT count — every artifact must contain meaningful content
- All new artifacts go under `research_state/session_<UTC>/` — the root research_state/ md+json count is 499/500; one root-level md/json file breaches the churn cap and fails the heavy-work gate

**Non-avoidance:** A future agent cannot satisfy the heavy-work gate with prose, trigger-check-only, or placeholder artifacts. The machine-enforced gate (scripts/check_handoff_heavywork_gate.py + tests/test_active_campaign_gate.py) requires the concrete artifact triad plus a non-empty trigger_check in the latest session directory.

---

## 5. Source/engineering blockers and next free route

| Blocker | Evidence | Next materially different free route |
|---------|----------|--------------------------------------|
| No Binance liquidation labels | Binance public archive requires manual download or requester-pays; no unauthenticated historical liquidation feed | Use frozen Hyperliquid panel for cross-sectional mechanism; register separate Binance-arm protocol if/when archive access verified |
| Track A power limit | RISK-12 MDE=0.0028 > plausible 0.001; 13 coins, 12 months insufficient | Cross-sectional mechanism uses within-hour variation, different statistical power profile |
| Sealed Binance months unread | RESEARCH_PROMPT.md prohibits reading sealed months for outcomes | Frozen panel already available; no new data needed for exploratory mechanism |
| No historical market-cap ranks | Free point-in-time ranks unavailable | Venue-native universe — all discoverable perpetuals from public listing metadata |
| Sealed Binance months unread | RESEARCH_PROMPT.md prohibits reading sealed months for outcomes | Frozen panel already available; no new data needed for exploratory mechanism |
| Root research_state/ md+json count | 499/500 — one new root-level md/json file breaches the churn cap enforced by test_tracka_hardening_125 and fails the heavy-work gate | All new artifacts go under a timestamped session_<UTC>/ directory; do NOT add root-level md/json files |
| FCLR-001 forecast gate NOT_PASSED | C2 vs B1 +2.62% QLIKE, CI positive, Holm FAILS | Distinct-mechanism exploratory campaign (cross-sectional) on same frozen panel |

**Do not:**
- Re-run FCLR-STARTER-001 (protocol frozen, holdout inspected, verdict emitted)
- Re-run RISK-09/10/11/12 variants (explicitly prohibited in RISK-12 prereg)
- Attempt Track A liquidation forecasting without a materially larger panel
- Modify `.github/workflows` (protected control plane)
- Create placeholder artifacts — only create when contents are meaningful
- Overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03)

---

## 6. Contingency ladder (if cross-sectional mechanism blocked)

If the within-hour cross-sectional mechanism hits a structural blocker (e.g., insufficient cross-sectional variation, funding rank collinear with RV):

1. **UTC-hour / market-wide-RV conditioning** — Test if funding effect is concentrated in specific regimes (high RV hours, Asian/European/US sessions)
2. **liq_count persistence family** — If Track A labels have adequate coverage, test t-1 liquidation count as predictor
3. **RISK-13** — Per RISK-12 evidence audit: advance only if MDE ≤ plausible effect via MDE-by-instrument redesign or larger panel
4. **Track B modeled boundary-breach** — If contract specs and margin tiers verifiable from public sources

---

## 7. Next session must

Read this handoff + RESEARCH_PROMPT.md completely, inspect working tree and latest artifacts (session_20261120T052201Z/, session_20261120T024217Z/), then **preregister and execute a distinct-mechanism exploratory campaign (FCLR-XSEC-001: within-hour cross-sectional funding contrast) on the frozen FCLR-001 panel**. No other task has higher expected information gain per unit of free compute. The FCLR-STARTER-001 campaign is complete and its verdict NOT_SUPPORTED is final; the machine-enforced handoff heavy-work gate requires the concrete artifact triad for any new campaign — future agents cannot satisfy it with prose or placeholders.

(End of file)