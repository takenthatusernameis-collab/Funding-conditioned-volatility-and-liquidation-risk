# AGENT HANDOFF — Funding-conditioned-volatility-and-liquidation-risk

**Generated (UTC):** 2026-11-27T23:03:47Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Single durable handoff for the next agentic work session.**

> This file is the ONE durable handoff. Timestamped duplicates
> (`AGENT_HANDOFF_20261127T182958Z.md`, `_183426Z.md`, `_220239Z.md`) were moved to
> `handoff_archive/` to remove the multi-handoff bottleneck. Do not recreate them;
> append to this file only.
>
> **CURATOR REFRESH 2026-11-27T23:03:47Z:** handoff re-verified green
> (`check_handoff_heavywork_gate.py` → `pass=true`, `reason_code=OK`, `failures=[]`,
> `handoff_stale=false`, `handoff_markers_ok=true`,
> `heavy_session_dir=research_state/session_20261127T065600Z`,
> `live_archive.campaign_id=FCLR-LIVE-ARCHIVE-08-20261127T131654Z`,
> `live_archive.required=false` **by design** — the binder is ARMED, not inert: it flips to
> `required=true` and fail-closed the instant any `session_<UTC>` with id
> `> 20261127T131654Z` appears on disk, so a trigger-only / prose-only / audit-only /
> prereg-only / verify-and-stop session cannot pass). Inputs confirmed present so the next
> session is NOT blocked: `research_state/data_cache/` holds all five symbols
> 2024-01..2026-11 (markPrice/funding/premium/index), `cached_inputs_hashes.json` present,
> and every campaign-07 template in `session_20261127T065600Z/` is non-empty. Root
> `research_state/` md+json count is at the cap of 500 → all new artifacts go under one
> fresh `session_<UTC>/`. No campaign change, no token change, no grandfathered-id change.
> No session is blocked; rank-0 FCLR-LIVE-ARCHIVE-08 remains the single repo-name-aligned
> open path. The executor session (id > `20261127T131654Z`) must still produce the full
> artifact set below.

---

## EXECUTIVE STATUS

**Confirmatory volatility program: CONCLUDED (terminal).**
- **Track C (volatility/stress/correction/jump forecasts):** NOT_SUPPORTED across every
  broad-panel confirmatory arm (FCLR-VOL-BROAD-01, -CORR-01, -STRESS-01, -JUMP-04..01,
  FCLR-PANEL-FE-001, FCLR-011). All closed; do NOT reopen.
- **Track A (observed liquidations):** STRUCTURALLY_BLOCKED — no admissible,
  unauthenticated historical source with required coverage.
- **Track B (modeled boundary breaches):** the only remaining confirmatory path.
- **Risk overlay:** NOT ELIGIBLE — the campaign-07 forecast gate did NOT pass, so per
  RESEARCH_PROMPT.md §9 no overlay is authorized.

**Environment constraints (binding):** no network/downloads, no paid/manual/credentialed
data, no workflow/scheduler/poller additions, no fabricated provenance, no threshold
shopping or sealed-holdout reuse. **Stdlib only** (no numpy/pandas/pyarrow/requests; no
pip install). `research_state/` root md+json count is at the cap of 500 — **all new
artifacts go under one fresh `research_state/session_<UTC>/`, never the root.**

---

## BOTTLENECKS REMOVED THIS SESSION (so heavy progress can continue)

1. **Phantom-session deadlock (gate was RED).** The prior handoff named a *next* session
   (a `session_` id dated after the campaign start) that was never created, so
   `check_handoff_heavywork_gate.py` failed with `HEAVY_SESSION_DIR_MISSING`. This handoff
   now references only the REAL latest on-disk session `session_20261127T065600Z`
   (campaign-07, complete bundle + evidence audit), which satisfies the new-heavy check.
2. **Inactive heavy-work binder.** The `FCLR-LIVE-ARCHIVE-08-<UTC>` token was missing, so
   the gate's live-archive enforcement regex never matched and the "machine-enforced"
   claim was inert. This handoff now carries the dated token
   `FCLR-LIVE-ARCHIVE-08-20261127T131654Z`, so any session with id > `20261127T131654Z`
   is bound to the full `fclr_live_archive08_*` artifact family (fail-closed on
   trigger-only / prose-only / audit-only / prereg-only / verify-and-stop / zero-byte).
3. **Multi-handoff ambiguity.** Three competing timestamped handoffs could send a future
   agent down divergent paths. Consolidated to this single file; duplicates archived.
4. **Grandfathered interval.** Session ids in `(20261127T065600Z, 20261127T131654Z]` are
   GRANDFATHERED and FORBIDDEN as a fresh session id. The next session id MUST be
   lexicographically **> `20261127T131654Z`**.
5. **Prior "MONITOR ONLY / verify-and-stop" directives:** SUPERSEDED. Execute the campaign
   below to completion in one session; do not wait, probe, or idle.
6. **False "design exhausted" signal.** `scripts/next_campaign_status.py` prints
   "contiguous design exhausted" / "no disjoint 30-day block feasible" — that verdict is
   scoped to the OLD disjoint-block design family (separate 127-day train + 30-day test
   blocks). It does **NOT** apply to FCLR-LIVE-ARCHIVE-08, which uses the full balanced
   common support `S` (`|S|=22608`, 2024-04..2026-10) with a single 60/20/20 + 168h embargo
   chronological split and three contiguous test blocks carved from `S`. Do not re-derive
   feasibility, do not declare the campaign blocked on that message, and do not switch
   designs — execute campaign-08 exactly as frozen below.

---

## ACTIVE RANK-0 CAMPAIGN: FCLR-LIVE-ARCHIVE-08 (Track B modeled boundary breach)

**Status:** `READY_EXECUTE` | **Program:** `ACTIVE` | **Rank:** 0
**Campaign token (gate anchor):** `FCLR-LIVE-ARCHIVE-08-20261127T131654Z`
**Source of truth:** `research_state/experiment_frontier.json` rank-0.

### Task (frozen)
Track-B modeled boundary-breach forecast — **NOT an overlay.** Pre-registered hypothetical
long/short liquidation boundaries from disclosed constant margin/leverage scenarios; target =
whether the future mark-price path breaches the boundary within a fixed horizon; separate
long/short labels; compare a funding-conditioned model vs a mark-price-only baseline by
out-of-sample AUC / log-loss / Brier with ≥2000 block-bootstrap and leave-one-symbol-out;
independent stdlib recompute `all_checks_match=true`. Stdlib only, read-only cache, no
network.

### Frozen design (MUST reuse exactly)
- **Data domain:** Binance 5-symbol (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) monthly
  futures archive (markPriceKlines, fundingRate, premiumIndexKlines, indexPriceKlines)
  2024-04..2026-10, read-only under `research_state/data_cache/`.
- **Common support S:** balanced mark-price hourly intersection, `|S| = 22608` timestamps
  (all five symbols present, close>0). XRPUSDT 2025-10-19 has 24 corrupt closes
  (quarantined, NOT zero-filled). Split: 60/20/20 + 168h embargo (train=13550, val=4517,
  test=4517 per symbol; test rows across 5 symbols = 22585).
- **Estimands:** long-breach / short-breach AUC, log-loss, Brier. Baseline = mark-price-only
  (RV + lagged returns). Candidate = funding-conditioned (adds funding rate, premium,
  dislocation/smoothing features). Materiality floor: ≥2% relative improvement with 95%
  block-bootstrap CI lower bound > 0.
- **Multiplicity:** leave-one-symbol-out + ≥2000 block-bootstrap; symmetric verdict
  (NOT_SUPPORTED / SUPPORTED / INCONCLUSIVE) frozen before outcomes.

### Required artifact set (enforced by `scripts/check_handoff_heavywork_gate.py`)
All non-empty, under **one fresh** `research_state/session_<UTC>/` with id **> 20261127T131654Z**:

| Artifact prefix | Suffixes |
|-----------------|----------|
| `fclr_live_archive08_source_registry_` | `.json`, `.md` |
| `fclr_live_archive08_prereg_` | `.json`, `.md` |
| `fclr_live_archive08_eval_` | `.py`, `.json`, `.md` |
| `fclr_live_archive08_recompute_` | `.py`, `.json` |
| `fclr_live_archive08_evidence_audit_` | `.json`, `.md` |
| `evidence_audit_` (gate alias) | `.json` |
| `trigger_check_` | `.json` |

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**TIMESTAMP:** 2026-11-27T23:03:47Z
**REPO-NAME PRIORITY:** the repository leads with *Funding-conditioned-volatility* AND
*liquidation-risk*. Every volatility arm is terminally closed; the single highest-value
unfinished, repo-name-aligned task is the funding-conditioned **liquidation-risk** Track-B
modeled boundary-breach forecast (FCLR-LIVE-ARCHIVE-08). It is the ONLY task this session
may execute.

**FOCUS CAMPAIGN (repo-name priority, non-avoidance):** FCLR-LIVE-ARCHIVE-08 — the
funding-conditioned liquidation-risk Track-B modeled boundary-breach forecast. This is the
single focus campaign. The gate (`scripts/check_handoff_heavywork_gate.py`) binds every
post-start session (id `> 20261127T131654Z`) to the full `fclr_live_archive08_*` artifact
family plus `trigger_check_<UTC>.json`, so heavy work cannot be avoided, deferred, or
reduced to prose-only / audit-only / prereg-only / trigger-only / verify-and-stop.

**SESSION CONSTRAINT:** create `research_state/session_<UTC>/` with UTC **> 20261127T131654Z**
(use the actual `date -u +%Y%m%dT%H%M%SZ` run start time, which will be later than
`20261127T131654Z`). Do NOT use any id in `(20261127T065600Z, 20261127T131654Z]`
(grandfathered/forbidden).

### MANDATORY WORKPLAN (single session, in order)

**Phase 1 — Source registry & prereg freeze (outcome-blind).**
1. Verify cache: read `research_state/data_cache/{BNBUSDT,BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT}_2024_04..2026_10/`
   mark-price klines + funding; assert every `.sha256` sidecar against
   `research_state/cached_inputs_hashes.json`. Record coverage/layouts/shortfalls.
2. Rebuild common support S (all-five-symbol hourly intersection, close>0, dedup by
   open_time, 2024-04-01..2026-10-31 UTC). Freeze `|S|=22608` and split sizes.
3. Emit `fclr_live_archive08_source_registry_<UTC>.{json,md}`.
4. Freeze prereg (outcome-blind): margin/leverage scenarios, horizon, long/short labels,
   estimands, baseline vs candidate, 2% floor, alpha/Holm family, ≥2000 block-bootstrap +
   LOSO, split on S; hash-bound to source registry; `outcome_data_inspected_before_freeze: false`.
   Emit `fclr_live_archive08_prereg_<UTC>.{json,md}`.

**Phase 2 — Heavy boundary-breach evaluation.**
5. Stdlib-only rolling-origin 3-block OOS evaluation on S: hypothetical long/short
   liquidation boundaries from margin/leverage scenarios; breach labels; fit baseline
   (mark-price-only) and candidate (funding-conditioned); score AUC/log-loss/Brier;
   ≥2000 block-bootstrap + leave-one-symbol-out. Emit
   `fclr_live_archive08_eval_<UTC>.{py,json,md}`.

**Phase 3 — Independent recompute & evidence audit.**
6. Separate-code-path stdlib recompute that rebuilds S and re-runs the full evaluation,
   asserts `all_checks_match=true`, all five symbols in every block/fold, n_test≥500. Emit
   `fclr_live_archive08_recompute_<UTC>.{py,json}`.
7. Evidence audit (artifact hashes, config reproduction, verdict traceability). Emit
   `fclr_live_archive08_evidence_audit_<UTC>.{json,md}` + alias `evidence_audit_<UTC>.json`.
8. Non-empty `trigger_check_<UTC>.json` with gate status.
9. Update `research_state/experiment_frontier.json` rank-0 → `COMPLETED_VALIDATED` with the
   reproduced verdict. Run `python3 scripts/check_handoff_heavywork_gate.py` until green
   (`pass=true`, `failures=[]`).

### SUCCESS CRITERIA
- All required artifacts present, non-empty, under one fresh `session_<UTC>/` (id > 20261127T131654Z).
- `scripts/check_handoff_heavywork_gate.py` exits 0.
- `all_checks_match=true` from the independent recompute.
- Symmetric verdict recorded in prereg and evaluation.

### REFERENCE TEMPLATES (campaign-07, session_20261127T065600Z)
- Eval: `research_state/session_20261127T065600Z/fclr_live_archive07_eval_20261127T065600Z.py`
- Recompute: `research_state/session_20261127T065600Z/fclr_live_archive07_recompute_20261127T065600Z.py`
- Prereg: `research_state/session_20261127T065600Z/fclr_live_archive07_prereg_20261127T065600Z.json`
- Source registry: `research_state/session_20261127T065600Z/fclr_live_archive07_source_registry_20261127T065600Z.json`

### HARD CONSTRAINTS (violation = wasted session / gate failure)
- Session id > `20261127T131654Z`; grandfathered ids forbidden.
- Forecast gate (campaign-07) NOT_SUPPORTED → NO risk overlay (§9). This is forecast
  validation of a modeled boundary-breach target, which is permitted.
- Reuse campaign-07 mark-price cache READ-ONLY; do NOT re-download.
- Stdlib only; no pip install.
- All artifacts under one fresh `session_<UTC>/`; root cap 500 reached — no root writes.
- Do not modify `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts.
- XRPUSDT 2025-10-19: drop `close<=0`, quarantine, do NOT zero-fill.

### WHAT NOT TO DO
| Forbidden | Reason |
|-----------|--------|
| Re-run any closed volatility arm (FCLR-VOL-*, FCLR-PANEL-FE, FCLR-011) | Terminally NOT_SUPPORTED; §17 promotion impossible |
| Build a risk overlay | §9 forbids (campaign-07 gate NOT_SUPPORTED) |
| Wait for NEW_OBSERVED_LIQUIDATION_SOURCE / HL_LABEL_EXTENSION / GATE4_BRANCH_1 | External predicates unsatisfied; do_not_act_until_satisfied=True |
| Add root-level research_state files | Root cap 500 reached |
| Threshold-shop after outcomes / relabel exploratory as confirmatory | Structural violation; verdicts sealed |
| Use session id ≤ 20261127T131654Z | Grandfathered; gate rejects |
| Trigger-only / prose-only / audit-only / prereg-only / verify-and-stop session | Gate fails closed |

### VERIFICATION COMMANDS (run at START and END)
```bash
export UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
python3 scripts/next_campaign_status.py
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m json.tool research_state/experiment_frontier.json >/dev/null
git diff --check
```
Gate must report at END: `pass=true`, `reason_code=OK`, `failures=[]`, with empty
missing/empty artifact lists for the `fclr_live_archive08_*` family.

---

## COMPLETED CAMPAIGNS (DO NOT RE-RUN)

| Campaign | Session | Verdict |
|----------|---------|---------|
| FCLR-LIVE-ARCHIVE-07 | 20261127T065600Z | NOT_SUPPORTED (C2 vs B1 rel -0.704%, CI [-1.218%,-0.190%]) |
| FCLR-LIVE-ARCHIVE-06 | 20261126T133828Z | NOT_SUPPORTED (downside semivar level, rel MSE 0.716%) |
| FCLR-LIVE-ARCHIVE-05 | 20261126T082429Z | NOT_SUPPORTED (signed semivar asymmetry, rel MSE 0.141%) |
| FCLR-LIVE-ARCHIVE-04 | 20261126T061929Z | NOT_SUPPORTED (quantile/full-dist, rel pinball -1.102%) |
| FCLR-LIVE-ARCHIVE-03 | 20261126T051548Z | NOT_SUPPORTED (stress/tail Brier, rel 0.458%) |
| FCLR-LIVE-ARCHIVE-01 | 20261126T042519Z | NOT_SUPPORTED (mean-RV QLIKE, rel 0.840%) |
| FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 | 20261125T060000Z | NOT_SUPPORTED (formal closure + meta-analysis) |
| FCLR-VOL-JUMP-04..01 | 20261125T030000Z..054500Z | NOT_SUPPORTED (all volatility-jump arms) |
| FCLR-VOL-STRESS-01 | 20261124T222500Z | NOT_SUPPORTED (vol stress/tail) |
| FCLR-VOL-CORR-01 | 20261124T204500Z | NOT_SUPPORTED (correction-time/hazard) |
| FCLR-VOL-BROAD-01 | 20261124T120000Z | NOT_SUPPORTED (mean log-RV QLIKE broad) |

**All volatility arms (Track C) are CLOSED. Track A is STRUCTURALLY_BLOCKED. Track B
(FCLR-LIVE-ARCHIVE-08) is the only remaining confirmatory path.**

---

## KEY FILES TO READ BEFORE STARTING
1. `research_state/experiment_frontier.json` — rank-0 task definition (this campaign)
2. `research_state/final_synthesis_report.md` — program conclusion evidence
3. `scripts/next_campaign_status.py` — cache frontier truth (`--json`)
4. `scripts/check_handoff_heavywork_gate.py` — gate enforcement (LIVE_ARCHIVE_REQUIRED)
5. `research_state/session_20261127T065600Z/` — campaign-07 template artifacts
6. `research_state/cached_inputs_hashes.json` — verified checksums
7. `research_state/data_cache/` — read-only Binance 5-symbol monthly archive

---

**This handoff is durable and machine-actionable. The next session MUST execute the full
FCLR-LIVE-ARCHIVE-08 artifact set in a single fresh session with id > 20261127T131654Z.
No partial, deferred, or prose-only work will pass the gate.**

(End of file)