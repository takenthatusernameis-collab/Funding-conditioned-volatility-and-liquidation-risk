# AGENT HANDOFF — 2026-11-25T06:00:00Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: CLOSED — FORMAL PROGRAM CLOSURE + NEGATIVE-RESULTS SYNTHESIS COMPLETE.**
> HALF 1 (FUNDING-CONDITIONED VOLATILITY) — ALL FIVE repo-name estimands CLOSED `NOT_SUPPORTED`:
> mean log-RV QLIKE (FCLR-VOL-BROAD-01), funding-extreme correction-time/hazard (FCLR-VOL-CORR-01),
> volatility-STRESS/tail-exceedance (FCLR-VOL-STRESS-01), signed-jump MAGNITUDE-exceedance
> (FCLR-VOL-JUMP-01/02/03), and signed-jump DIRECTION/SIGN (FCLR-VOL-JUMP-04).
> HALF 2 (LIQUIDATION RISK) — confirmatory-exhausted on the frozen `ironflow_bulk` panel
> (Track A STRUCTURALLY_BLOCKED; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; cross-sectional
> SUPPORTED_GENERALIZATION but NOT_STABLE + 2% materiality floor NOT MET).
> Rank-0 campaign `FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z` is now
> `COMPLETED_VALIDATED` under `session_20261125T060000Z`. All eight `fclr_liq_risk_program_closure_*`
> artifact categories produced, all non-empty, no zero-byte placeholders; independent stdlib
> recompute `all_checks_match=true`, `n_checks=63`; gate-critical `evidence_audit_` alias
> `audit_pass:true`; `trigger_check_` non-empty (`external_trigger_required:false`,
> `trigger_source:"FROZEN_IRONFLOW_BULK"`, `fired:false`).
> **REPO-NAME PRIORITY → `Funding-conditioned-volatility-and-liquidation-risk`**: the name leads with
> volatility; every funding-conditioned volatility estimand is now closed with valid negative results,
> and the liquidation-risk half is exhausted. There is no remaining un-run confirmatory estimand on
> the frozen panel. The honest endpoint — formal closure + negative-results preservation — is done.
> The only remaining duty for any future session is to verify the gate stays green and stop;
> no new heavy work remains.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — verified 2026-11-25T07:13:08Z**
>
> **CURRENT GATE STATE (2026-11-25T07:13:08Z):** The heavy-work gate is GREEN on the real repo. The
> latest on-disk AND handoff-recorded session is `session_20261125T060000Z`, which carries the
> COMPLETE `fclr_liq_risk_program_closure_*` artifact set (protocol_freeze json+md, synthesis_report
> json+md, frontier_exhaustion_audit json+md, negative_results_preservation json+md,
> meta_analysis py+json+md, recompute py+json with `all_checks_match=true` / `n_checks=63`,
> gate-critical `evidence_audit_` json+md alias with `audit_pass:true` / `unresolved_blockers:[]`,
> non-empty `trigger_check_` json). The `program_closure` binder for the campaign
> `FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z` is `required=true` and `pass=true` because the
> latest session `20261125T060000Z` is strictly newer than the campaign start `20261125T054500Z`.
> The gate stays green only because all required closure artifacts exist and are non-empty.
>
> **REPO-NAME PRIORITY → COMPLETE:** The repository is `Funding-conditioned-volatility-and-liquidation-risk`.
> Half 1 (funding-conditioned volatility) is closed at broad scale on ALL FIVE estimands: mean log-RV
> QLIKE (FCLR-VOL-BROAD-01, NOT_SUPPORTED, 1.93% < 2%), funding-extreme correction-time/hazard
> (FCLR-VOL-CORR-01, NOT_SUPPORTED), volatility-STRESS/tail-exceedance (FCLR-VOL-STRESS-01,
> NOT_SUPPORTED, 1.51% < 2%), signed-jump MAGNITUDE-exceedance (FCLR-VOL-JUMP-01/02/03 all
> NOT_SUPPORTED — jump03 aggregate 0.3025% < 2%), and signed-jump DIRECTION/SIGN (FCLR-VOL-JUMP-04,
> NOT_SUPPORTED — 110,914 non-overlapping forecasts, 57,354 downside-dominance events, 367 coins,
> aggregate 0.0474% / ≤0.1020% best-config relative Brier improvement, all below the 2% floor). Half 2
> (liquidation risk) is confirmatory-exhausted on the frozen `ironflow_bulk` panel. The program is
> CLOSED; the formal closure + negative-results synthesis + quantitative meta-analysis has been
> executed under `session_20261125T060000Z`.
>
> **NO HEAVY WORK REMAINS.** The next session's job is to VERIFY the gate stays green and STOP:
> `python3 scripts/check_handoff_heavywork_gate.py --json` → `reason=OK` with
> `program_closure.required=true` and `program_closure.pass=true`, plus the campaign-gate regression
> suite (122 tests OK). Do NOT re-run any closed volatility arm, do NOT re-run any terminal liquidation
> track, do NOT build a risk overlay (forecast gate not passed), do NOT wait for
> `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen data), do NOT add root-level
> `research_state/*.md|*.json` files (root at 500 cap), do NOT threshold-shop, do NOT relabel
> exploratory as confirmatory, and do NOT produce a timestamp-only refresh of this handoff as a
> substitute for verification. Verified at 2026-11-25T07:13:08Z: gate `pass=true`, `reason_code=OK`,
> `program_closure.required=true`, `program_closure.pass=true`, all 122 campaign-gate tests pass, root
> count 500/500 at cap.

---

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **A timestamp-only rewrite of this file is NOT progress and is explicitly forbidden as the next session's deliverable.** The prior program loop refreshed this handoff many times without producing a post-start heavy session; that loop is the failure mode this section exists to end. This refresh is backed by a REAL completed heavy session (`session_20261125T054500Z`, FCLR-VOL-JUMP-04, 110,914 non-overlapping directional/sign forecasts across 4 estimator×horizon configs, valid numeric candidate metrics, independent recompute `all_checks_match=true`, `n_checks=76`) executed in THIS session — not a timestamp bump.
- **How the gate's grandfathering works, and why the grace window is CLOSED:** `_program_closure_state` (scripts/check_handoff_heavywork_gate.py) sets `required=true` only once the latest session *recorded in this handoff / on disk* is strictly later than the campaign start. The campaign start is `20261125T054500Z` (this refresh time), NOT a future date. As long as the latest session is `session_20261125T054500Z` (which equals the campaign start), `program_closure.required=false` (grandfathered) and the gate stays green. **That green is a property of pointing at the campaign-start session, not evidence that the work is done.** Because the start is already in the past, ANY new `session_<UTC>` you create (UTC > `20261125T054500Z`) immediately flips `required=true`; the full `fclr_liq_risk_program_closure_*` set (plus `evidence_audit_` alias and non-empty `trigger_check_`) is mandatory and a trigger-only, prose-only, audit-only, prereg-only, verify-and-stop, empty, or arbitrary `recompute_*` session FAILS CLOSED. There is no future-dated window left in which to idle.
- **Do not create a partial/empty session directory and leave it unrecorded.** That produces `HANDOFF_STALE_LATEST_SESSION:<dir>` and fails the gate closed for every later session. If you create `session_<UTC>/`, populate it fully and record it in this handoff in the same session.
- Do not re-run any terminal campaign. Do not wait for an external trigger. Do not build a risk overlay. Do not track-adulterate. Do not ship a verdict from a non-reconciled eval (emit a verdict only after the independent recompute reports `all_checks_match:true`; preserve fail-closed behavior).
- **DO NOT treat `python3 scripts/next_campaign_status.py` output as a feasibility verdict.** That script only tests the OLD 3-contiguous-30-day-block framing and prints `no feasible 3-block design in ANY domain`. It does NOT assess the closure/meta-analysis design, which IS feasible today on the frozen on-disk artifacts. Misreading this output as "no feasible heavy work exists" and idling is a non-avoidance failure.
- Root `research_state/*.md|*.json` is at the 500 cap. All new artifacts MUST go under `session_<UTC>/`.

---

## FOCUS CAMPAIGN — FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z (rank-0, READY_EXECUTE)

**Question (OPEN):** Across both halves of the repository on the frozen `ironflow_bulk` panel, (a) do all confirmatory verdicts survive a family-wide multiplicity audit, and (b) is the confirmatory frontier formally exhausted on admissible frozen data such that the honest endpoint is closure + negative-results synthesis?

**Why this is the highest-value next task:**
- Repo name leads with **Funding-conditioned-volatility**; all five volatility arms (mean QLIKE, correction-time, stress, jump MAGNITUDE, jump DIRECTION/SIGN) are closed NOT_SUPPORTED, and the liquidation-risk half is exhausted. There is no remaining un-run confirmatory estimand on the frozen panel.
- The honest, publishable endpoint is a formal closure + complete negative-results synthesis with a quantitative meta-analysis — exactly the pattern that turns a large body of nulls into a rigorous, citable negative result.
- It is a DISTINCT, materially different design (meta-analysis / frontier-exhaustion audit over existing artifacts), not a re-run of any terminal endpoint.

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}/` — 18 monthly parquet; sha256-asserted; read-only.
- The frozen `research_state/session_*/` artifacts of the closed campaigns (synthesis inputs only).

**Produced artifacts (target — ALL under one fresh `session_<UTC>/`; non-empty):**
- `fclr_liq_risk_program_closure_protocol_freeze_<UTC>.{json,md}`
- `fclr_liq_risk_program_closure_synthesis_report_<UTC>.{json,md}`
- `fclr_liq_risk_program_closure_frontier_exhaustion_audit_<UTC>.{json,md}`
- `fclr_liq_risk_program_closure_negative_results_preservation_<UTC>.{json,md}`
- `fclr_liq_risk_program_closure_meta_analysis_<UTC>.{py,json,md}`
- `fclr_liq_risk_program_closure_recompute_<UTC>.{py,json}` (`all_checks_match:true`)
- `evidence_audit_<UTC>.{json,md}` (gate-critical alias)
- `trigger_check_<UTC>.json`

---

## STATE OF THE WORK (read before doing anything)

- **Half 1 (volatility) — broad RV forecast (mean QLIKE):** CLOSED. FCLR-VOL-BROAD-01 (session_20261124T120000Z) NOT_SUPPORTED: broad-panel (314+ coin, 18-month `ironflow_bulk`) funding-conditioned RV forecast improved QLIKE 1.93% relative over the RV-only baseline, below the frozen 2% floor.
- **Half 1 (volatility) — correction-time frontier:** CLOSED. FCLR-VOL-CORR-01 (session_20261124T204500Z) NOT_SUPPORTED: 227,023 funding-extreme events; high-RV median correction 9.00h vs low-RV 10.00h; frozen ≥10% relative slower-correction floor NOT met.
- **Half 1 (volatility) — stress / tail-exceedance frontier:** CLOSED. FCLR-VOL-STRESS-01 (session_20261124T222500Z) NOT_SUPPORTED: 1,393,204 forecasts, 63,059 stress events, 314 coins; Brier baseline 0.041718 vs candidate 0.041087 (1.51% relative), below the 2% floor.
- **Half 1 (volatility) — jump MAGNITUDE / semivariance-asymmetry frontier:** CLOSED. FCLR-VOL-JUMP-01 (session_20261125T030000Z) NOT_SUPPORTED: 1,136,222 forecasts, 39,116 jump events, 454 coins; Brier 0.033322 vs 0.033292 (0.0922% relative), far below the 2% floor.
- **Half 1 (volatility) — jump leakage-hardened re-confirmation:** CLOSED. FCLR-VOL-JUMP-02 (session_20261125T034400Z) NOT_SUPPORTED: 30,284 NON-overlapping forecasts, 1,388 jump events, 202 coins; Brier 0.043611 vs 0.043545 (0.1510% relative); null SURVIVES 48h purge+embargo, non-overlapping forward windows, mark/index tolerance filter, delisting-aware identity, per-coin cluster bootstrap and Holm; independent recompute `all_checks_match=true`, `n_checks=60`.
- **Half 1 (volatility) — jump multi-estimator / multi-horizon robustness:** CLOSED. FCLR-VOL-JUMP-03 (session_20261125T045000Z) NOT_SUPPORTED: 87,162 NON-overlapping forecasts, 4,235 jump events, 202 coins, 4 (estimator × horizon) configs; per-config relative Brier 0.0991%..0.5386% (bipower/24h reproduces jump02 at 0.1510%), aggregate 0.3025%, all below the 2% floor; null SURVIVES bipower vs threshold-bipower AND {24h,48h}; independent stdlib recompute `all_checks_match=true`, `n_checks=76`.
- **Half 1 (volatility) — jump DIRECTIONAL / sign frontier:** CLOSED. FCLR-VOL-JUMP-04 (session_20261125T054500Z) NOT_SUPPORTED: 110,914 NON-overlapping forecasts, 57,354 downside-dominance events (base rate ~51.7%), 367 coins, 4 (estimator × horizon) configs; per-config relative Brier -0.0785%..0.1020%, aggregate 0.0474%, all below the 2% floor; null SURVIVES bipower vs threshold-bipower AND {24h,48h} under full leakage remediation; independent stdlib recompute `all_checks_match=true`, `n_checks=76`. **This closes the funding-conditioned volatility-jump family (magnitude AND direction) for good.**
- **Half 2 (liquidation risk):** confirmatory-exhausted on the frozen `ironflow_bulk` panel. Track A STRUCTURALLY_BLOCKED; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; broad cross-sectional rank ordering SUPPORTED_GENERALIZATION but NOT_STABLE (§17 condition #4) and 2% Poisson-deviance materiality floor NOT MET.
- **Heavy-work gate:** PASSING (`reason=OK`). `program_closure.required=true` and `program_closure.pass=true` (latest session 20261125T060000Z is strictly newer than the campaign start 20261125T054500Z, and all required `fclr_liq_risk_program_closure_*` artifacts exist and are non-empty under `session_20261125T060000Z/`). Rank-0 campaign `FCLR-LIQ-RISK-PROGRAM-CLOSURE-02` promoted `READY_EXECUTE` → `COMPLETED_VALIDATED`. No heavy work remains; the next session verifies green and stops.
- **Forecast gate (§9):** NOT PASSED — no broad-scale volatility skill demonstrated; materiality floor not met on any arm. Risk overlay INELIGIBLE.
- **Root `research_state/*.md|*.json` count:** 500/500 — at cap. All new artifacts went under `session_20261125T060000Z/`; no root-level files added.

---

## ROOT CONSTRAINTS (hard)

- Root `research_state/*.md|*.json` count: **500/500** — at cap. All new artifacts MUST go under `session_<UTC>/` or another nested directory. Do not add root-level research-state files.
- No empty files and no zero-byte placeholders.
- Do not threshold-shop or relax any frozen floor/threshold after outcomes.
- Preserve nulls honestly: valid outcomes are `PROMOTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`, or an evidence-backed fidelity/structural blocker; never a fabricated pass.
- Do not re-run any terminal campaign or build a risk overlay.
- Do not modify `.github/workflows`.
- Do not overwrite `research_state/research_protocol.md` or any sealed prereg/eval artifact.
- Stdlib + numpy + pandas + pyarrow only; no network for the heavy evaluation; no new source; no overlay.
- Do not track-adulterate: never describe a broad-universe cross-sectional association, or a stability test of it, as a time-series forecast gate pass.
- Do not wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; it cannot fire on frozen data and is not a valid reason to idle.
- Do not write a future/non-existent session id into this handoff. Use the placeholder `session_<UTC>` for the session you create; record its real id here only after its artifacts exist.
- **DO NOT include any other `FCLR-…-<8digit>T<6digit>Z` campaign id in this file** (refer to closed campaigns by name only, e.g. "FCLR-VOL-JUMP-04 (closed)"). A stray timestamped id would activate that campaign's binder on every future session and fail it closed. The ONLY timestamped campaign id permitted in this file is the active `FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z`.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 2025-05..2026-10; hourly OHLC. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; `funding_rate`, `premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; `mark_price`, `oracle_price`, `open_interest`. |
| `research_state/session_20261125T060000Z/` | **LATEST COMPLETE closure session** (FCLR-LIQ-RISK-PROGRAM-CLOSURE-02; program closed; all eight `fclr_liq_risk_program_closure_*` artifact categories + `evidence_audit_` alias + `trigger_check_`, all non-empty; recompute `all_checks_match=true`, `n_checks=63`). |
| `research_state/session_20261125T054500Z/` | Prior complete heavy session (FCLR-VOL-JUMP-04; NOT_SUPPORTED; 13 non-empty artifacts + helper; recompute `all_checks_match=true`, `n_checks=76`). |
| `research_state/session_20261125T045000Z/` | Prior complete heavy session (FCLR-VOL-JUMP-03; NOT_SUPPORTED; multi-estimator × multi-horizon magnitude). |
| `research_state/session_20261125T034400Z/` | Prior complete heavy session (FCLR-VOL-JUMP-02; NOT_SUPPORTED; leakage-hardened). |
| `research_state/session_20261125T030000Z/` | Prior complete heavy session (FCLR-VOL-JUMP-01; NOT_SUPPORTED; signed-jump magnitude). |
| `research_state/session_20261124T222500Z/` | Prior complete heavy session (FCLR-VOL-STRESS-01; NOT_SUPPORTED; tail-exceedance). |
| `research_state/session_20261124T204500Z/` | Prior complete heavy session (FCLR-VOL-CORR-01; NOT_SUPPORTED; correction-time). |
| `research_state/session_20261124T120000Z/` | Prior complete heavy session (FCLR-VOL-BROAD-01; NOT_SUPPORTED; mean QLIKE). |
| `research_state/experiment_frontier.json` | rank-0 is `FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z` (COMPLETED_VALIDATED under session_20261125T060000Z); all FCLR-VOL-* arms are COMPLETED_VALIDATED (NOT_SUPPORTED). |
| `research_state/negative_results_report.md` | Null/failed/inconclusive outcomes preserved. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3 (primary + secondary research question), §7 (targets), §9 (overlay gate), §13/§16 (adaptive feasibility / three-blocked-routes), §17 (promotion), §19 (definition of done), §20 (status contract).
- `scripts/check_handoff_heavywork_gate.py` — `PROGRAM_CLOSURE_CAMPAIGN_RE` / `_program_closure_state` / `PROGRAM_CLOSURE_REQUIRED` binder (active for the FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 campaign; `required=true` and `pass=true` because the latest session 20261125T060000Z is strictly newer than the 20261125T054500Z start and all required closure artifacts exist and are non-empty).
- `tests/test_vol_jump_campaign_gate.py` and sibling campaign-gate tests — regression pinning the binders (hermetic; use fixtures, not this handoff).
- `research_state/experiment_frontier.json` — rank-0 campaign registry.
- `research_state/data_cache/ironflow_bulk/` — frozen broad panel.
- `research_state/negative_results_report.md` — preserved nulls/negatives.
- `research_state/session_20261125T054500Z/fclr_voljump04_eval_20261125T054500Z.py` — the working, terminating multi-estimator × multi-horizon DIRECTIONAL/sign jump evaluation just executed (reference for the leakage-hardened pipeline; do NOT re-run it).

---

## SESSION CLOSE-OUT (THIS SESSION — 2026-11-25T05:50:53Z)

**What changed and why (real actions, not a timestamp bump):**
- **Re-read the full durable state** (AGENT_HANDOFF.md, RESEARCH_PROMPT.md, research_state/experiment_frontier.json, scripts/check_handoff_heavywork_gate.py, scripts/next_campaign_status.py, tests/*, session_20261125T054500Z/ artifact set) and confirmed every prior claim against on-disk evidence.
- **Confirmed the previous session's heavy work is complete:** FCLR-VOL-JUMP-04 executed under `research_state/session_20261125T054500Z/` — the multi-estimator (bipower vs threshold-bipower) × multi-horizon ({24h, 48h}) DIRECTIONAL / SIGN signed-jump / semivariance-asymmetry study (target `J^{(H)} < 0`, downside-dominant) with ALL FCLR-POOLED-AUDIT-001 leakage remediations applied simultaneously. 110,914 non-overlapping forecasts, 57,354 downside-dominance events, 367 coins, 4 configs, ~146s. Per-config relative Brier -0.0785%..0.1020% (aggregate 0.0474%), all below the frozen 2% floor → NOT_SUPPORTED. Independent stdlib recompute `all_checks_match=true`, `n_checks=76`. This closes the funding-conditioned volatility-jump family (magnitude AND direction) for good.
- **Confirmed the complete 13-artifact set exists** under `session_20261125T054500Z/` — all non-empty, no zero-byte placeholders (source_registry json+md, prereg json+md, eval py+json+md, recompute py+json, evidence_audit json+md, gate-critical `evidence_audit_` alias, non-empty `trigger_check_`).
- **Confirmed the roll-forward to `FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z`** (formal closure + negative-results synthesis + quantitative meta-analysis; start = 20261125T054500Z, in the past) so the gate stays green only because the latest session equals the start, and ANY new session is immediately bound to the full `fclr_liq_risk_program_closure_*` set.
- **Verified the heavy-work gate is green on the real repo** (see commands below).

**Precise verifying commands:**
```bash
# 0. One-time environment setup if needed
python3 -m pip install --quiet numpy pandas pyarrow

# 1. Heavy-work gate must return reason=OK
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Gate binder must compile
python3 -m py_compile scripts/check_handoff_heavywork_gate.py

# 3. Campaign-gate regression suite must pass
python3 -m unittest \
  tests.test_vol_jump_campaign_gate \
  tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate \
  tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 \
  tests.test_active_campaign_gate

# 4. Context only: the old 3-block scanner does not assess closure/meta-analysis feasibility
python3 scripts/next_campaign_status.py
```

---

## SESSION CLOSE-OUT (THIS SESSION — 2026-11-25T06:00:00Z)

**What changed and why (real actions, not a timestamp bump):**
- **Executed FCLR-LIQ-RISK-PROGRAM-CLOSURE-02** (formal program closure + complete negative-results synthesis + quantitative meta-analysis) under `research_state/session_20261125T060000Z/` — UTC strictly > campaign start 20261125T054500Z, so the `program_closure` binder is `required=true` and `pass=true`.
- **Produced the complete eight-category closure artifact set**, all non-empty, no zero-byte placeholders:
  1. `fclr_liq_risk_program_closure_protocol_freeze_20261125T060000Z.{json,md}` — outcome-blind closure protocol freeze (`outcome_data_inspected_before_freeze:false`, all 54 input sha256 asserted, hash-bound to RESEARCH_PROMPT.md §13/§19/§20).
  2. `fclr_liq_risk_program_closure_synthesis_report_20261125T060000Z.{json,md}` — complete negative-results synthesis across all tracks/hypotheses with exact verdicts, CIs, artifact paths, evidence.
  3. `fclr_liq_risk_program_closure_frontier_exhaustion_audit_20261125T060000Z.{json,md}` — audit proving no feasible confirmatory design remains (§16 three-blocked-routes rule, two+ source families/methods).
  4. `fclr_liq_risk_program_closure_negative_results_preservation_20261125T060000Z.{json,md}` — all null/failed/inconclusive outcomes preserved with explanations (§19).
  5. `fclr_liq_risk_program_closure_meta_analysis_20261125T060000Z.{py,json,md}` — quantitative meta-analysis triad (family-wide multiplicity, Holm-adjusted outcomes, per-track verdict table; 0 Holm-surviving claims).
  6. `fclr_liq_risk_program_closure_recompute_20261125T060000Z.{py,json}` — independent stdlib recompute reproducing headline verdicts from stored input hashes/configuration (`all_checks_match=true`, `n_checks=63`, `n_mismatches=0`).
  7. `evidence_audit_20261125T060000Z.{json,md}` — gate-critical evidence audit alias (`audit_pass:true`, `unresolved_blockers:[]`, verdict consistent with synthesis).
  8. `trigger_check_20261125T060000Z.json` — non-empty trigger check (`external_trigger_required:false`, `trigger_source:"FROZEN_IRONFLOW_BULK"`, `fired:false`).
- **Every JSON carries** `experiment_id:"FCLR-LIQ-RISK-PROGRAM-CLOSURE-02"` and `session_id:"session_20261125T060000Z"` matching the directory.
- **Promoted rank-0** in `research_state/experiment_frontier.json`: `READY_EXECUTE` → `COMPLETED_VALIDATED`, program_status `ACTIVE` → `COMPLETE`, session/completed_session `session_20261125T060000Z`, completed_utc `20261125T06:00:00Z`.
- **Updated this handoff** to mark the program CLOSED; no heavy work remains. No root-level `research_state/*.md|*.json` files added (root at 500/500 cap); all artifacts under `session_20261125T060000Z/`.

**Precise verifying commands:**
```bash
# 0. One-time environment setup if needed
python3 -m pip install --quiet numpy pandas pyarrow

# 1. Heavy-work gate must return reason=OK with program_closure.required=true and pass=true
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Gate binder must compile
python3 -m py_compile scripts/check_handoff_heavywork_gate.py

# 3. Campaign-gate regression suite must pass
python3 -m unittest \
  tests.test_vol_jump_campaign_gate \
  tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate \
  tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 \
  tests.test_active_campaign_gate

# 4. Context only: the old 3-block scanner does not assess closure/meta-analysis feasibility
python3 scripts/next_campaign_status.py
```

---

## PRIOR SESSION CLOSE-OUT (2026-11-25T05:38:48Z — historical)

**What changed and why:** Refreshed the sole durable handoff to point at the then-active FCLR-VOL-JUMP-04 campaign; the underlying heavy work (FCLR-VOL-JUMP-03) was already completed in session_20261125T045000Z. That refresh did NOT create a new session; it updated the handoff timestamp and made the then-current gate state explicit. (Superseded by this session, which actually executed FCLR-VOL-JUMP-04.)

---

## BOTTLENECK RESOLUTION (this session — 2026-11-25T05:50:53Z)

- **RESOLVED (the core bottleneck — deferred heavy work):** the FCLR-VOL-JUMP-04 heavy evaluation had been announced but never executed; prior sessions only refreshed this handoff. RESOLVED by executing the full multi-estimator × multi-horizon DIRECTIONAL/sign jump04 evaluation in session_20261125T054500Z with the complete 13-artifact set and a passing independent recompute (`all_checks_match=true`, `n_checks=76`).
- **RESOLVED (future-dated grandfathering window):** the FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 start is `20261125T054500Z` (in the past), so there is no future grace window; any new session is immediately bound. The gate stays green only because the latest session equals the start.
- **RESOLVED (root churn cap):** root `research_state/*.md|*.json` is at 500; all new artifacts went under `session_20261125T054500Z/`.
- **OPEN (next frontier execution):** `FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z` must be executed properly — all required `fclr_liq_risk_program_closure_*` artifacts under one fresh `session_<UTC>/` (UTC > 20261125T054500Z), no zero-byte placeholders, in one session. This is the next agent's single, non-deferrable job. No remaining bottleneck blocks it: all inputs are frozen on disk, no network needed, no external trigger required, no closed campaign needs re-running.

---

## RESEARCH_PROMPT.md §19 ANSWERS (this session)

**What did the evidence support, contradict, or leave unknown?**
- Supported (prior, unchanged): the broad-universe cross-sectional funding → next-hour liquidation-intensity rank ordering generalizes but is NOT temporally stable.
- Contradicted/closed (this session): the funding-conditioned volatility-JUMP DIRECTIONAL/SIGN hypothesis at broad scale is NOT_SUPPORTED (FCLR-VOL-JUMP-04 — aggregate 0.0474% / ≤0.1020% best-config relative Brier improvement across bipower vs threshold-bipower × {24h,48h}). Together with the earlier mean-QLIKE / correction-time / stress / jump-magnitude nulls (jump01/02/03), the entire funding-conditioned volatility family is now closed at broad scale.
- Unknown (next campaign): whether any feasible confirmatory design remains on admissible frozen data, or whether the frontier is formally exhausted (the closure campaign's frontier-exhaustion audit answers this).

**What is the strongest alternative explanation?**
The volatility nulls (mean QLIKE 1.93%, correction-time, stress 1.51%, jump magnitude 0.0922%, leakage-hardened jump 0.1510%, estimator/horizon-robust jump 0.3025%, directional/sign jump 0.0474%) may all reflect that funding carries weak, regime-dependent information that is economically immaterial at broad scale across every repo-name volatility estimand — the leading explanation the closure synthesis must weigh.

**Which data/label/inference limitation currently dominates uncertainty?**
1. Estimand: all five broad-scale volatility endpoints plus the jump estimator/horizon/direction robustness are closed; the open question is now whether the frontier is formally exhausted.
2. Label: ironflow liquidations are a capped-sample feed (constrains Half 2, not the funding/volatility arm).
3. Materiality/inference: no arm has cleared its frozen floor; the closure meta-analysis must report family-wide Holm-adjusted outcomes.

**What concrete new test would falsify the current leading hypothesis?**
A family-wide multiplicity audit + frontier-exhaustion audit showing either (a) a surviving feasible confirmatory design that clears a frozen floor (would reopen the program), or (b) formal exhaustion with all nulls preserved (closes the program).

**What task has the highest expected information gain per unit of free compute?**
`FCLR-LIQ-RISK-PROGRAM-CLOSURE-02` — it converts the entire body of nulls into a rigorous, citable negative result using only frozen on-disk artifacts.

**What exact artifact and command/test demonstrate progress?**
- Artifact: one fresh `research_state/session_<UTC>/` (UTC > 20261125T054500Z) with the full `fclr_liq_risk_program_closure_*` set plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json`, all non-empty.
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` → `reason=OK` with `program_closure.required=true` and `program_closure.pass=true`.
- Test: `python3 -m unittest tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate tests.test_tracka_hardening_143 tests.test_active_campaign_gate` passes.

(End of file)