# AGENT HANDOFF — 2026-11-23T11:26:45Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> Gate status as of this refresh (2026-11-23T11:26:45Z): **PASS** (reason_code=OK, root=499/500).
> The prior heavy session `session_20261123T085507Z` COMPLETED the full `FCLR-LIQ-XSEC-BROAD-01`
> heavy set (broad-universe generalization of narrow 15-coin cross-sectional findings).
> Verdict: **SUPPORTED_GENERALIZATION on cross-sectional rank-ordering association** (rank-IC
> positive on both long/short arms, CI95 excludes null, Holm primary p < alpha_k);
> **Poisson-deviance materiality floor (2%) NOT MET on either arm** (long -0.23%, short +0.71%).
> This is a cross-sectional *association* generalization test, NOT a time-series forecast gate pass.
> The binder is regression-pinned by `tests/test_tracka_hardening_143.py::TestLiqXsecBroadCampaignGate`.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-23T11:26:45Z (refresh time)**
>
> **REPO-NAME PRIORITY → FINAL STATE:** The repository is `Funding-conditioned-volatility-and-liquidation-risk`.
> RESEARCH_PROMPT.md §3.2 primary question two halves:
> - **Half 1 (Volatility / Track C):** CLOSED — leakage-robust null across every claim-worthy panel
>   (H1_primary NOT_SUPPORTED; FCLR-011 PASS does not generalize forward; FCLR-FWD-VOL-011-CONFIRM NOT_REPLICATED).
> - **Half 2 (Liquidation-risk):**
>   - **Track A (observed liquidations):** `TRACK_A_STRUCTURALLY_BLOCKED` (source audit complete, frozen
>     outcome-blind; `outcome_data_inspected_before_freeze:false`). No admissible unauthenticated
>     historical liquidation source with required coverage exists in this environment.
>   - **Track B (modeled boundary breach):** NOT_SUPPORTED across all campaigns (pooled, robust,
>     live-archive, tracks01 modeled-breach pivot).
>   - **Track C (volatility-as-liquidation-proxy):** NOT_SUPPORTED (same as Half 1).
>   - **The ONLY liquidation-risk results ever marked SUPPORTED** were the *regime-conditioned
>     cross-sectional* funding → next-hour observed-liquidation-intensity findings on the narrow
>     15-coin panel: FCLR-XSEC-004 (count, low-RV), FCLR-XSEC-005 (notional-weighted, low-RV),
>     FCLR-XSEC-006 (all three UTC buckets). All flagged `promotable:false` / EXPLORATORY_ONLY
>     because they never generalized beyond 15 coins.
>   - **FCLR-LIQ-XSEC-BROAD-01 (just completed, session_20261123T085507Z):** Tested generalization
>     to the full 342-coin ironflow_bulk universe (2025-05..2026-10, 2.85M liquidation rows).
>     **Verdict: SUPPORTED_GENERALIZATION for the cross-sectional rank-ordering association** (rank-IC
>     reproduced, CI95 excludes null favorable, Holm primary p < alpha_k).
>     **HOWEVER: Poisson-deviance materiality floor (2%) NOT MET on either arm** (long -0.23%,
>     short +0.71%). This is a rank-ordering association, not a calibrated-magnitude improvement.
>     Per RESEARCH_PROMPT.md §9 (gate before overlay) and §17 (promotion conditions), a cross-sectional
>     association that does not meet the materiality floor on the primary metric does NOT pass the
>     forecast gate. No risk overlay is eligible.
>
> **Program status: CONCLUDED.** All feasible confirmatory paths under current constraints are exhausted.
> The final_synthesis_report.md (2026-11-10) declared the confirmatory program complete with no
> promotable forecast skill. The FCLR-LIQ-XSEC-BROAD-01 campaign was the final remaining test of the
> only SUPPORTED liquidation-risk findings. Its result — generalization of a rank-ordering association
> without meeting the materiality floor — is the durable final answer: the narrow-universe findings
> were a small-universe artifact for calibrated magnitude, though the directional rank association
> does survive at breadth.
>
> **There is NO remaining heavy campaign to execute.** The next session should:
> 1. Verify the gate passes (it will, with this handoff update and the recorded session_20261123T085507Z).
> 2. Confirm no new feasible heavy work exists (next_campaign_status.py shows NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN).
> 3. Stop cleanly — the research program is complete under current constraints.
>
> **Do NOT:** invent a new campaign; re-run any terminal campaign; threshold-shop the materiality floor;
> build a risk overlay (§9 gate not passed); claim a time-series forecast gate pass from a cross-sectional
> association; wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen data; §16, §19).
>
> **Blockers: None — the program is complete, not blocked.**

### Single, non-deferrable job (VERIFY AND STOP)

Run the verification commands below. If all pass, the session is complete — no further work exists.

**Verification commands (run before declaring done):**

```bash
# 1. Heavy-work gate must return reason=OK (not VERIFY_AND_STOP, not BLOCKED)
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Campaign gate unittests must pass
python3 -m unittest \
  tests.test_active_campaign_gate \
  tests.test_fclr_starter_001_campaign_gate \
  tests.test_fclr_campaign_gate \
  tests.test_fclr_heavy_confirm_gate \
  tests.test_pooled_robust_002_campaign_gate \
  tests.test_tracka_hardening_143

# 3. Frozen 3-block domains exhausted (expected; confirms no further feasible heavy design)
python3 scripts/next_campaign_status.py
```

---

## FOCUS CAMPAIGN (COMPLETED — no further heavy work)

**FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z** — executed to completion in `session_20261123T085507Z/`:

1. **SOURCE REGISTRY** — `fclr_liqxsecbroad01_source_registry_*` (json+md) recorded ironflow_bulk
   parquet files: 18 months × 4 datasets, 72/72 sha256 verified, 342 coins (2025-05), 2.85M liq rows.
2. **PREREG FREEZE** — `fclr_liqxsecbroad01_prereg_*` (json+md) froze outcome-blind design:
   broad-universe cross-sectional generalization, RV-tercile + UTC-session regime (expanding thresholds),
   next-hour observed liquidation intensity (count + notional, long/short separate), chronological
   walk-forward (60% train, 48h purge, 168h test blocks), per-coin block bootstrap (2000 reps),
   placebo/permutation, leave-one-instrument-out (8/8 pass), Holm (6-arm family), 2% materiality floor,
   symmetric verdict rule.
3. **HEAVY EVALUATION + INDEPENDENT RECOMPUTE** — `fclr_liqxsecbroad01_eval_*` (py+json+md) and
   `fclr_liqxsecbroad01_recompute_*` (py+json). Identical sign convention, `all_checks_match:true`.

**Results:**
- **Long arm:** mean rank-IC C2=0.155, B1=-0.017; Poisson deviance rel improvement -0.23% (floor 2% NOT MET)
- **Short arm:** mean rank-IC C2=-0.002, B1=-0.073; Poisson deviance rel improvement +0.71% (floor 2% NOT MET)
- **Uncertainty:** bootstrap CI95 [0.142, 0.169] excludes null favorable; placebo 95th pct 0.0013, true effect exceeds; LOIO 8/8 sign reproduced
- **Multiplicity:** Holm across 6-arm family, all raw p=0.0, adjusted p=0.0 < alpha_k=0.00833
- **Verdict:** `SUPPORTED_GENERALIZATION` (rank-ordering association generalizes; materiality floor NOT MET)
- **Evidence audit:** Consistent eval/recompute; honest caveats recorded (not a forecast gate pass, not a census).

---

## ROOT CONSTRAINTS (hard)

- Root md+json count: **499/500** — at cap. ALL new artifacts MUST go under `session_<UTC>/`. Do NOT add
  any root-level `research_state/*.md|*.json`.
- No empty files, no zero-byte placeholders.
- Do NOT threshold-shop or relax the materiality floor after outcomes.
- Preserve nulls honestly: verdict may be `SUPPORTED_GENERALIZATION` or `NOT_SUPPORTED` (with evidence).
- Do NOT re-run any terminal campaign (see list above).
- Do NOT build a risk overlay (§9: forecast gate did not pass on ANY primary target).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md` (sealed FCLR-001 definition consumed by
  `scripts/run_evaluation.py`).
- Stdlib + pyarrow only; no network for heavy evaluation (source probes already done); no new source
  without provenance; no overlay.
- Do NOT track-adulterate: never describe a broad-universe cross-sectional association, Track B
  (modeled breach), or Track C (volatility) as proof of an observed-liquidation forecast gate pass;
  never claim a complete observed-liquidation census from a capped feed.
- **Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`** — cannot fire on frozen data; not a valid excuse
  to idle (§16, §19). The program is complete.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **No** prose-only / trigger-only / source-probe-only / audit-only / **prereg-only** / verify-and-stop /
  placeholder sessions — **EXCEPT: this final verification session is explicitly permitted to
  verify-and-stop because the program is concluded.**
- **Do NOT** write a future/non-existent `session_<UTC>` id into this handoff before that directory
  exists (the gate treats a non-existent recorded dir as a failure). The only literal `session_<digits>`
  tokens in this handoff are `session_20261122T190000Z`, `session_20261122T224500Z`,
  `session_20261123T043600Z`, and `session_20261123T085507Z`.
- **Do NOT** create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- **Do NOT** re-run any terminal campaign.
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`.
- **Do NOT** build a risk overlay.
- **Do NOT** track-adulterate.

---

## EVIDENCE NOTE (read before writing the recompute)

The prior `session_20261123T043600Z` tracks01 evidence contains a **sign-convention
discrepancy that was corrected in FCLR-LIQ-XSEC-BROAD-01**. In `fclr_tracks01_eval_20261123T043600Z.json`
the long arm stored `rel_brier_improvement_pct=-2.0` (improvement as `C2_minus_B1`), while
`fclr_tracks01_recompute_20261123T043600Z.json` computed `rel_brier_improvement_pct=+2.0`
(improvement as `B1_minus_C2`) and recorded `all_checks_match:false`. Both concluded **NOT_SUPPORTED**
(the bootstrap CI includes zero and Holm fails, so the verdict is robust to the sign error).
For FCLR-LIQ-XSEC-BROAD-01: one explicit sign convention was declared in the prereg
(`relative_improvement = (baseline - candidate) / baseline`, positive = candidate better), used
identically in the eval AND the recompute, and the recompute asserts `all_checks_match:true`.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. **Capped-sample feed — not a complete census (per §15).** Columns: `timestamp[ms],market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`. **Verified: 2,849,452 rows across 18 files, 342 distinct coins, span 2025-05-25..2026-10-31. There is NO `coin` column — the instrument key is `market`.** |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,funding_rate,premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,mark_price,oracle_price,open_interest,open_interest_usd`. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,market_class,open,high,low,close,volume,trades`. |
| `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` | Frozen 15-coin combined metpie+ironflow panel (sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`), 1,740,415 rows, 2025-03-22..2026-10-31. The NARROW universe whose SUPPORTED findings (XSEC-004/005/006) were tested for generalization. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate caches.

---

## KEY FILES TO READ (for verification only)

- `research_state/experiment_frontier.json` — rank-0 is now `FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z`
  with status **COMPLETE**, verdict **SUPPORTED_GENERALIZATION (materiality NOT MET)**, completed
  session `session_20261123T085507Z`. All other campaigns are SUPERSEDED_TERMINAL or COMPLETE.
- `scripts/check_handoff_heavywork_gate.py` — gate enforcement (should return PASS with this handoff).
- `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_eval_20261123T085507Z.json` — heavy evaluation.
- `research_state/session_20261123T085507Z/fclr_liqxsecbroad01_evidence_audit_20261123T085507Z.json` — evidence audit.
- `research_state/final_synthesis_report.md` — program-wide CONCLUDED verdict (no promotable skill).
- `RESEARCH_PROMPT.md` §3.2 (primary question two halves), §9 (overlay gate), §16 (adaptive feasibility), §17 (promotion conditions).

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why (handoff updated to record completion of FCLR-LIQ-XSEC-BROAD-01 and program conclusion)
2. Exact test outcomes with paths (gate PASS, all unittests PASS)
3. Evidence added and full paths (no new evidence — program complete)
4. State of each research gate (all gates satisfied; forecast gate NOT PASSED on any primary target)
5. Single highest-value next task (**NONE — program concluded**)
6. Precise verifying command (see above)
7. Any blocker with next materially different route (**None — program complete**)

---

## BOTTLENECK RESOLUTION (this handoff)

- **Resolved (stale handoff):** The prior handoff declared `FCLR-LIQ-XSEC-BROAD-01` as READY_EXECUTE
  but `session_20261123T085507Z` had already completed it. This refresh records the completed session
  (`session_20261123T085507Z`) and updates the campaign status to COMPLETE with the true verdict.
- **Resolved (frontier drift):** `experiment_frontier.json` rank-0 showed `READY_EXECUTE / NOT_STARTED`
  for `FCLR-LIQ-XSEC-BROAD-01` even though it completed. This refresh updates it to
  `COMPLETE / SUPPORTED_GENERALIZATION (materiality NOT MET)` with `completed_session:
  session_20261123T085507Z`.
- **Resolved (gate failures):** The gate was failing with `HANDOFF_STALE_LATEST_SESSION` because
  `session_20261123T085507Z` was not recorded in the handoff. This refresh adds it.
- **Verified (2026-11-23T11:26:45Z refresh):** `python3 scripts/check_handoff_heavywork_gate.py --json`
  → PASS reason_code=OK root=499/500. All campaign gate unittests pass. `next_campaign_status.py`
  confirms NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN.

---

## SESSION CLOSE-OUT — VERIFY-AND-STOP (this session, 2026-11-23T11:37:58Z)

This is the explicitly-permitted final verification session. No new research artifacts were created
(root md+json count unchanged at 499/500). Verified outcomes recorded below.

**1. What changed and why:**
- Refreshed AGENT_HANDOFF.md to record this verify-and-stop session's exact test outcomes.
- No campaign executed, no new heavy work, no new root-level research_state artifacts.

**2. Exact test outcomes with paths:**
- Heavy-work gate: `python3 scripts/check_handoff_heavywork_gate.py --json` → PASS, reason_code=OK,
  root=499/500, handoff_stale=false, latest session session_20261123T085507Z present on disk.
- Campaign gate unittests:
  `python3 -m unittest tests.test_active_campaign_gate tests.test_fclr_starter_001_campaign_gate
  tests.test_fclr_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_pooled_robust_002_campaign_gate
  tests.test_tracka_hardening_143` → Ran 126 tests, OK (skipped=5).
- Frozen 3-block domains exhausted:
  `python3 scripts/next_campaign_status.py` → CAMPAIGN STATUS: no feasible 3-block design in ANY domain
  (NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN).

**3. Evidence added and full paths:** none — program complete; no new evidence artifacts.

**4. State of each research gate:**
- Heavy-work gate: SATISFIED (PASS, reason_code=OK).
- All campaign gate binders (tracked in check_handoff_heavywork_gate.py): PASS / not required (no post-start
  campaign binds; latest session session_20261123T085507Z satisfies LIQ_XSEC_BROAD).
- Forecast gate: NOT PASSED on any primary target (no promotable forecast skill; materiality floor NOT MET).

**5. Single highest-value next task:** NONE — program concluded under current constraints.

**6. Precise verifying command:**
```
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m unittest tests.test_active_campaign_gate tests.test_fclr_starter_001_campaign_gate \
  tests.test_fclr_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_pooled_robust_002_campaign_gate \
  tests.test_tracka_hardening_143
python3 scripts/next_campaign_status.py
```

**7. Blocker / next materially different route:** None — program complete; no feasible route remains
(frozen data frontier exhausted; NEW_OBSERVED_LIQUIDATION_SOURCE cannot fire on frozen data).

---
## HANDOFF GENERATED: 2026-11-23T11:26:45Z (refresh) / SESSION CLOSE-OUT VERIFIED: 2026-11-23T11:37:58Z
**Latest handoff session: session_20261123T085507Z** (completed FCLR-LIQ-XSEC-BROAD-01 heavy set:
broad-universe generalization test of the regime-conditioned cross-sectional funding → next-hour
observed-liquidation-intensity findings; verdict SUPPORTED_GENERALIZATION for rank-ordering
association; Poisson-deviance materiality floor NOT MET on either arm; independent recompute
`all_checks_match:true`).
**Rank-0 campaign: FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z** (status COMPLETE, verdict
SUPPORTED_GENERALIZATION with materiality caveat, completed_session session_20261123T085507Z).
**Program status: CONCLUDED.** No further heavy campaigns feasible under current constraints.

(End of file - total 409 lines)