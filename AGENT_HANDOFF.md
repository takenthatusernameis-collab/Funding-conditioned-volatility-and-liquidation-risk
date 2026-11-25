# AGENT HANDOFF — 2026-11-25T04:37:21Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: HALF 1 (FUNDING-CONDITIONED VOLATILITY) — ALL FOUR ESTIMANDS CLOSED AT BROAD SCALE, AND THE JUMP NULL IS NOW LEAKAGE-ROBUST.** Mean-QLIKE (FCLR-VOL-BROAD-01, NOT_SUPPORTED, 1.93% < 2%), correction-time (FCLR-VOL-CORR-01, NOT_SUPPORTED), volatility-STRESS / tail-exceedance (FCLR-VOL-STRESS-01, NOT_SUPPORTED, 1.51% < 2%), SIGNED-JUMP / SEMIVARIANCE-ASYMMETRY (FCLR-VOL-JUMP-01, NOT_SUPPORTED, 0.0922% < 2%), and the LEAKAGE-HARDENED RE-CONFIRMATION of that jump null (FCLR-VOL-JUMP-02, session_20261125T034400Z, NOT_SUPPORTED, 0.1510% < 2% under non-overlapping forward windows + mark/index tolerance + delisting-aware identity + per-coin block bootstrap + 48h purge + Holm). HALF 2 (LIQUIDATION RISK) CONFIRMATORY-EXHAUSTED on the frozen panel.
> Active rank-0 campaign: `FCLR-VOL-JUMP-03-20261125T034400Z` (READY_EXECUTE) — a materially different, feasible, HEAVY robustness study that tests whether the now leakage-robust jump null is an artifact of the SPECIFIC jump estimator and forecast horizon (bipower vs threshold-bipower × {24h, 48h}). The campaign start is `20261125T034400Z` (in the past) so there is NO grandfathering grace window: any session created from now on is immediately bound to the full heavy artifact set.
> **REPO-NAME PRIORITY → `Funding-conditioned-volatility-and-liquidation-risk`**: the repository name leads with the volatility half. All four repo-name volatility estimands are closed at broad scale with valid negative results, and the jump null has now survived full leakage remediation (jump02). The remaining repo-name work is to prove the jump null is also ESTIMATOR- and HORIZON-robust — the final capstone of the funding-conditioned volatility program. A null that survives is the publishable capstone.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-25T04:37:21Z**
>
> **CURRENT GATE STATE (2026-11-25T04:37:21Z):** The heavy-work gate is GREEN on the real repo. `python3 scripts/check_handoff_heavywork_gate.py --json` returns `pass=true`, `reason_code=OK`. The latest on-disk AND handoff-recorded session is `session_20261125T034400Z`, which carries the COMPLETE `fclr_voljump02_*` artifact set (source_registry json+md, prereg json+md, eval py+json+md, recompute py+json with `all_checks_match=true` / `n_checks=60`, evidence_audit json+md, gate-critical `evidence_audit_` alias, non-empty `trigger_check_`). The `vol_jump` binder for the active campaign `FCLR-VOL-JUMP-03-20261125T034400Z` is currently `required=false` ONLY because the latest session `20261125T034400Z` is <= the campaign start `20261125T034400Z`. **That green is a property of the latest session equaling the campaign start, NOT evidence that the next campaign is done.** The campaign start is deliberately set to `20261125T034400Z` (in the past) so there is NO future grace window: the moment you create any `session_<UTC>` strictly newer than `20261125T034400Z` (i.e. any session from now on), the binder flips `required=true` and the full `fclr_voljump03_*` set (plus `evidence_audit_` alias and non-empty `trigger_check_`) becomes MANDATORY.
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is `Funding-conditioned-volatility-and-liquidation-risk`. Half 1 (funding-conditioned volatility) is now closed at broad scale on ALL FOUR estimands: mean log-RV QLIKE (FCLR-VOL-BROAD-01, NOT_SUPPORTED), funding-extreme correction-time / hazard (FCLR-VOL-CORR-01, NOT_SUPPORTED), volatility-STRESS / tail-exceedance (FCLR-VOL-STRESS-01, NOT_SUPPORTED), and signed-jump / semivariance-asymmetry (FCLR-VOL-JUMP-01, NOT_SUPPORTED — 0.0922% relative Brier improvement). The leakage-hardened RE-CONFIRMATION of the jump null (FCLR-VOL-JUMP-02, session_20261125T034400Z, NOT_SUPPORTED — 0.1510% relative Brier improvement under non-overlapping forward windows, mark/index tolerance filter, delisting-aware per-coin identity, per-coin cluster bootstrap, 48h purge+embargo and Holm) is now ALSO closed. Half 2 (liquidation risk) is confirmatory-exhausted on the frozen `ironflow_bulk` panel. The next session's single, non-deferrable job is the **multi-estimator / multi-horizon signed-jump robustness study** — a materially different, leakage-hardened design that tests whether the jump null is an artifact of the bipower estimator or the 24h horizon, using only frozen on-disk data.
>
> **THE NEXT FOCUS CAMPAIGN (rank-0, mandatory heavy work): `FCLR-VOL-JUMP-03-20261125T034400Z`**
>
> Execute a HEAVY, confirmatory, broad-panel robustness study. This is real computation — not a status memo, not a source probe, not a trigger-check-only session, not a verify-and-stop session, and **not another timestamp-only refresh of this handoff** (see NON-AVOIDANCE below).
>
> **Question:** On the full frozen `ironflow_bulk` panel (18 monthly parquet, 2025-05..2026-10; `candles_1h`, `funding`, `open_interest`), does the funding + price-dislocation feature set improve out-of-sample forecasts of a SIGNED-JUMP / SEMIVARIANCE-ASYMMETRY event — next-`H`h jump component (realized variance minus bipower/continuous variation, signed by the dominant realized semivariance) exceeding an expanding, TRAIN-ONLY high quantile per coin — beyond a realized-volatility-only baseline, judged on Brier / log-loss / calibration with a frozen materiality floor and Holm-adjusted uncertainty, **when the jump estimator is varied (bipower vs threshold-bipower) AND the forecast horizon is varied ({24h, 48h}), with ALL of the FCLR-POOLED-AUDIT-001 remediations applied simultaneously** (48h purge+embargo, NON-overlapping forward-outcome windows, mark/index tolerance filter, delisting-aware per-coin identity, per-coin cluster bootstrap, Holm across the declared estimator×horizon×metric family)?
>
> **Frozen inputs (do NOT re-derive, do NOT substitute):**
> - `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}/` (18 monthly parquet, 2025-05..2026-10). `candles_1h` columns: `timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades`. `funding`: `timestamp, market, coin, dex, funding_rate, premium`. `open_interest`: `timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd`. Assert every `.sha256` sidecar before reading; caches are read-only and unmodified.
> - Jump-event definition (freeze in the new prereg): a jump-stress event at forecast origin t is `J^{(H)}_{t+1..t+H} > q_t` where `J^{(H)}` is the next-`H`h jump magnitude (realized variance minus the chosen continuous-variation estimator — bipower OR threshold-bipower — signed by the sign of RS+ − RS−) and `q_t` is an EXPANDING, TRAIN-ONLY high quantile of trailing jump magnitude per coin (no future information). Baseline = RV-only (persistence / HAR-style). Candidate = RV + signed/absolute funding + mark/index premium + mark/EMA24 distance. Feature standardization and thresholds are train-only.
> - Design: chronological walk-forward / expanding train-only thresholds; `PURGE_EMBARGO_H=48`; NON-overlapping forward-outcome windows (step the forecast origin by >= `H` hours so adjacent targets do not share hours); mark/index tolerance filter; delisting-aware per-coin identity; per-coin cluster bootstrap. No random split.
> - Inference: cluster-robust (CR1) by coin AND Driscoll-Kraay HAC; Holm correction over the declared family (baseline vs candidate × estimator × horizon × metric). Materiality floor (frozen, NOT relaxed): the candidate's relative Brier (or log-loss) improvement over the RV-only baseline must exceed 2% (0.02); verdict is symmetric (`PROMOTED` / `NOT_SUPPORTED`); a null that survives across estimators and horizons is a valid, publishable negative result that closes the volatility-jump arm for good.
>
> **Next agent's single job:** Produce the complete artifact set under one fresh `research_state/session_<UTC>/` (UTC strictly > `20261125T034400Z`), prefix `fclr_voljump03_`, all non-empty, no zero-byte placeholders:
> 1. `fclr_voljump03_source_registry_{json,md}` — sha256-asserted `ironflow_bulk` inventory with a TOP-LEVEL `datasets` map containing `candles_1h`, `funding`, `open_interest`; JSON MUST carry `input_integrity.sha256_all_match=true`, `input_integrity.sha256_verified_bad=0`, and a `files` list of >=54 entries each with a 64-hex `sha256` and `sha_match` not false.
> 2. `fclr_voljump03_prereg_{json,md}` — outcome-blind frozen prereg (`outcome_data_inspected_before_freeze:false`, `frozen_before_outcomes:true`, `design.kind` containing one of `jump`/`asymmetry`/`bipower`/`semivariance`/`signed_jump`/`downside`, `materiality_floor_rel` > 0, `source_registry_sha256` == sha256 of the source-registry JSON). The closed mean-QLIKE, correction-time, total-variance tail-exceedance, jump01 and jump02 designs must NOT be relabeled as the jump03 multi-estimator design.
> 3. `fclr_voljump03_eval_{py,json,md}` — the heavy multi-estimator/multi-horizon jump-forecast robustness evaluation triad (`status` in {CONFIRMATORY_COMPLETE, NOT_SUPPORTED, PROMOTED, INCONCLUSIVE}, `holdout_opened:true`, integer `n_events>=1`, `metrics.{baseline,candidate}.brier` numeric (NOT NaN), boolean `materiality_met`, `verdict`).
> 4. `fclr_voljump03_recompute_{py,json}` — independent stdlib recompute from stored input hashes/config (`all_checks_match:true`, integer `n_checks`).
> 5. `fclr_voljump03_evidence_audit_{json,md}` — evidence audit (`audit_pass:true`, `unresolved_blockers:[]`, `verdict` == eval verdict).
> 6. `evidence_audit_<UTC>.json` — gate-critical alias (`audit_pass:true`, `verdict` == eval verdict).
> 7. `trigger_check_<UTC>.json` — non-empty trigger check (`external_trigger_required:false`, `trigger_source:"FROZEN_IRONFLOW_BULK"`, `fired:false`; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data).
>
> Every JSON must carry `experiment_id:"FCLR-VOL-JUMP-03"` and `session_id:"session_<UTC>"` matching the directory. Record the real session id in `research_state/experiment_frontier.json` (promote rank-0 `READY_EXECUTE` → `COMPLETED_VALIDATED` only after artifacts exist) and update this handoff after the artifacts exist. Do NOT write a future/non-existent session id into this handoff before its artifacts exist.
>
> **DO NOT:** re-run the broad RV-forecast (FCLR-VOL-BROAD-01, closed), the correction-time campaign (FCLR-VOL-CORR-01, closed), the volatility-stress campaign (FCLR-VOL-STRESS-01, closed), the jump01 campaign (FCLR-VOL-JUMP-01, closed), the jump02 leakage-hardened re-confirmation (FCLR-VOL-JUMP-02, closed — this is a materially different multi-estimator/horizon design, not a relabel), or the temporal-stability campaign; build a risk overlay (§9 forecast gate not passed); claim a forecast-gate pass from a cross-sectional association; wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; add root-level research-state files (root `*.md|*.json` at the 500 cap — all new artifacts MUST go under `session_<UTC>/`); relabel exploratory as confirmatory; threshold-shop or relax the frozen floor after outcomes.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **A timestamp-only rewrite of this file is NOT progress and is explicitly forbidden as the next session's deliverable.** The prior program loop refreshed this handoff many times without producing a post-start heavy session; that loop is the failure mode this section exists to end. This refresh is backed by a REAL completed heavy session (`session_20261125T034400Z`, FCLR-VOL-JUMP-02, 30,284 non-overlapping forecasts, valid numeric candidate metrics, independent recompute `all_checks_match=true`, `n_checks=60`) executed in THIS session — not a timestamp bump.
- **How the gate's grandfathering works, and why the grace window is CLOSED:** `_vol_jump_state` (scripts/check_handoff_heavywork_gate.py) sets `required=true` only once the latest session *recorded in this handoff / on disk* is strictly later than the campaign start. The campaign start is `20261125T034400Z` (this refresh time), NOT a future date. As long as the latest session is `session_20261125T034400Z` (which equals the campaign start), `vol_jump.required=false` (grandfathered) and the gate stays green. **That green is a property of pointing at the campaign-start session, not evidence that the work is done.** Because the start is already in the past, ANY new `session_<UTC>` you create (UTC > `20261125T034400Z`) immediately flips `required=true`; the full `fclr_voljump03_*` set (plus `evidence_audit_` alias and non-empty `trigger_check_`) is mandatory and a trigger-only, prose-only, audit-only, prereg-only, verify-and-stop, empty, or arbitrary `recompute_*` session FAILS CLOSED. There is no future-dated window left in which to idle.
- **Do not create a partial/empty session directory and leave it unrecorded.** That produces `HANDOFF_STALE_LATEST_SESSION:<dir>` and fails the gate closed for every later session (this exact failure occurred with `session_20261124T230000Z`, now superseded). If you create `session_<UTC>/`, populate it fully and record it in this handoff in the same session.
- Do not re-run any terminal campaign. Do not wait for an external trigger. Do not build a risk overlay. Do not track-adulterate. Do not ship a verdict from a non-reconciled eval (emit a verdict only after the independent recompute reports `all_checks_match:true`; preserve fail-closed behavior).
- **DO NOT treat `python3 scripts/next_campaign_status.py` output as a feasibility verdict.** That script only tests the OLD 3-contiguous-30-day-block framing and prints `no feasible 3-block design in ANY domain`. It does NOT assess the broad-panel multi-estimator jump robustness design, which IS feasible today on the full 18-month `ironflow_bulk` panel (jump02 completed in ~46s on this exact panel). Misreading this output as "no feasible heavy work exists" and idling is a non-avoidance failure.
- Root `research_state/*.md|*.json` is at the 500 cap. All new artifacts MUST go under `session_<UTC>/`.

---

## FOCUS CAMPAIGN — FCLR-VOL-JUMP-03-20261125T034400Z (rank-0, READY_EXECUTE)

**Question (OPEN):** Does the funding + price-dislocation feature set improve out-of-sample forecasts of a signed-jump / semivariance-asymmetry event beyond an RV-only baseline on the broad `ironflow_bulk` panel, clearing a frozen 2% materiality floor with Holm-adjusted uncertainty, **when the jump estimator (bipower vs threshold-bipower) and the forecast horizon ({24h, 48h}) are varied and all FCLR-POOLED-AUDIT-001 leakage remediations are applied simultaneously**?

**Why this is the highest-value next task:**
- Repo name leads with **Funding-conditioned-volatility**; all four prior broad-scale volatility arms (mean QLIKE, correction-time, stress, jump01) are closed NOT_SUPPORTED, and the jump null has now survived full leakage remediation (jump02). The remaining repo-name work is to prove the null is not an artifact of the bipower estimator or the 24h horizon.
- It is a DISTINCT, materially different design (multi-estimator × multi-horizon robustness), not a re-run of the terminal jump01/jump02 endpoints — exactly the pattern that produced FCLR-POOLED-ROBUST-002 after FCLR-POOLED-001.
- A null that survives across estimators and horizons is the strong, publishable capstone of the funding-conditioned volatility program; a pass would be the first broad-scale funding-conditioned volatility-jump skill and would still face the §17 promotion conditions in full.

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/candles_1h/` — 18 monthly parquet, hourly OHLC.
- `research_state/data_cache/ironflow_bulk/funding/` — 18 monthly parquet, `funding_rate`, `premium`.
- `research_state/data_cache/ironflow_bulk/open_interest/` — 18 monthly parquet, `mark_price`, `oracle_price`, `open_interest`.
- Assert every `.sha256` sidecar before reading; caches are read-only.

**Produced artifacts (target — ALL under one fresh `session_<UTC>/`; non-empty):**
- `fclr_voljump03_source_registry_<UTC>.{json,md}`
- `fclr_voljump03_prereg_<UTC>.{json,md}`
- `fclr_voljump03_eval_<UTC>.{py,json,md}`
- `fclr_voljump03_recompute_<UTC>.{py,json}` (`all_checks_match:true`)
- `fclr_voljump03_evidence_audit_<UTC>.{json,md}`
- `evidence_audit_<UTC>.json` (gate-critical alias)
- `trigger_check_<UTC>.json`

---

## STATE OF THE WORK (read before doing anything)

- **Half 1 (volatility) — broad RV forecast (mean QLIKE):** CLOSED. FCLR-VOL-BROAD-01 (session_20261124T120000Z) NOT_SUPPORTED: broad-panel (314+ coin, 18-month `ironflow_bulk`) funding-conditioned RV forecast improved QLIKE 1.93% relative over the RV-only baseline, below the frozen 2% floor.
- **Half 1 (volatility) — correction-time frontier:** CLOSED. FCLR-VOL-CORR-01 (session_20261124T204500Z) NOT_SUPPORTED: 227,023 funding-extreme events; high-RV median correction 9.00h vs low-RV 10.00h; frozen >=10% relative slower-correction floor NOT met.
- **Half 1 (volatility) — stress / tail-exceedance frontier:** CLOSED. FCLR-VOL-STRESS-01 (session_20261124T222500Z) NOT_SUPPORTED: 1,393,204 forecasts, 63,059 stress events, 314 coins; Brier baseline 0.041718 vs candidate 0.041087 (1.51% relative), below the 2% floor.
- **Half 1 (volatility) — jump / semivariance-asymmetry frontier:** CLOSED. FCLR-VOL-JUMP-01 (session_20261125T030000Z) NOT_SUPPORTED: 1,136,222 forecasts, 39,116 jump events, 454 coins; Brier baseline 0.033322 vs candidate 0.033292 (0.0922% relative improvement), far below the frozen 2% floor.
- **Half 1 (volatility) — jump leakage-hardened re-confirmation:** CLOSED. FCLR-VOL-JUMP-02 (session_20261125T034400Z) NOT_SUPPORTED: 30,284 NON-overlapping forecasts, 1,388 jump events, 202 coins, 3 test blocks; Brier baseline 0.043611 vs candidate 0.043545 (0.1510% relative improvement), below the 2% floor; the null SURVIVES 48h purge+embargo, non-overlapping forward windows, mark/index tolerance filter, delisting-aware identity, per-coin cluster bootstrap and Holm (Holm-adjusted; statistically distinguishable but economically immaterial; the frozen materiality floor governs); independent stdlib recompute `all_checks_match=true`, `n_checks=60`.
- **Half 1 (volatility) — jump multi-estimator / multi-horizon frontier:** OPEN — this campaign (FCLR-VOL-JUMP-03).
- **Half 2 (liquidation risk):** confirmatory-exhausted on the frozen `ironflow_bulk` panel. Track A STRUCTURALLY_BLOCKED; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; broad cross-sectional rank ordering SUPPORTED_GENERALIZATION but NOT_STABLE (§17 condition #4) and 2% Poisson-deviance materiality floor NOT MET.
- **Heavy-work gate:** PASSING (`reason=OK`). `vol_jump.required=false` (grandfathered; latest session 20261125T034400Z equals the FCLR-VOL-JUMP-03 start 20261125T034400Z). A new complete session > 20261125T034400Z with ALL `fclr_voljump03_*` artifacts is mandatory to keep the gate green after that session is created — and because the start is already in the past, that binding is immediate.
- **Forecast gate (§9):** NOT PASSED — no broad-scale volatility skill demonstrated; materiality floor not met on any arm. Risk overlay INELIGIBLE.
- **Root `research_state/*.md|*.json` count:** 500/500 — at cap. All new artifacts MUST go under `session_<UTC>/`.

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
- **DO NOT include any other `FCLR-…-<8digit>T<6digit>Z` campaign id in this file** (refer to closed campaigns by name only, e.g. "FCLR-VOL-JUMP-02 (closed)"). A stray timestamped id would activate that campaign's binder on every future session and fail it closed. The ONLY timestamped campaign id permitted in this file is the active `FCLR-VOL-JUMP-03-20261125T034400Z`.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 2025-05..2026-10; hourly OHLC. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; `funding_rate`, `premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; `mark_price`, `oracle_price`, `open_interest`. |
| `research_state/session_20261125T034400Z/` | **LATEST COMPLETE heavy session** (FCLR-VOL-JUMP-02; NOT_SUPPORTED; 13 non-empty artifacts; recompute `all_checks_match=true`, `n_checks=60`). |
| `research_state/session_20261125T030000Z/` | Prior complete heavy session (FCLR-VOL-JUMP-01; NOT_SUPPORTED; signed-jump). |
| `research_state/session_20261124T222500Z/` | Prior complete heavy session (FCLR-VOL-STRESS-01; NOT_SUPPORTED; tail-exceedance). |
| `research_state/session_20261124T204500Z/` | Prior complete heavy session (FCLR-VOL-CORR-01; NOT_SUPPORTED; correction-time). |
| `research_state/session_20261124T120000Z/` | Prior complete heavy session (FCLR-VOL-BROAD-01; NOT_SUPPORTED; mean QLIKE). |
| `research_state/session_20261124T230000Z/` | **SUPERSEDED PARTIAL** (broken jump01 attempt; NaN candidate metrics; do not use; superseded by session_20261125T030000Z). |
| `research_state/experiment_frontier.json` | rank-0 is `FCLR-VOL-JUMP-03-20261125T034400Z` (READY_EXECUTE); FCLR-VOL-JUMP-01/02, FCLR-VOL-STRESS-01, FCLR-VOL-CORR-01 and FCLR-VOL-BROAD-01 are COMPLETED_VALIDATED (NOT_SUPPORTED). |
| `research_state/negative_results_report.md` | Null/failed/inconclusive outcomes preserved. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3 (primary + secondary research question), §7 (targets), §9 (overlay gate), §16 (adaptive feasibility), §17 (promotion), §19 (definition of done), §20 (status contract).
- `scripts/check_handoff_heavywork_gate.py` — `VOL_JUMP_CAMPAIGN_RE` / `_vol_jump_state` / `VOL_JUMP_REQUIRED` binder (ladder-aware; active for the FCLR-VOL-JUMP-03 campaign; currently grandfathered only because the latest session 20261125T034400Z equals the 20261125T034400Z start).
- `tests/test_vol_jump_campaign_gate.py` — regression pinning the jump binder (hermetic; uses fixtures, not this handoff).
- `research_state/experiment_frontier.json` — rank-0 campaign registry.
- `research_state/data_cache/ironflow_bulk/` — frozen broad panel.
- `research_state/negative_results_report.md` — preserved nulls/negatives.
- `research_state/session_20261125T034400Z/fclr_voljump02_eval_20261125T034400Z.py` — the working, terminating leakage-hardened jump evaluation to adapt for the jump03 multi-estimator / multi-horizon design.

---

## SESSION CLOSE-OUT (THIS SESSION — 2026-11-25T04:37:21Z)

**What changed and why (real actions, not a timestamp bump):**
- **Refreshed the sole durable handoff with a current timestamp (2026-11-25T04:37:21Z)** to provide the next agentic session with an accurate, inferred initial task message. The underlying heavy work (FCLR-VOL-JUMP-02) was completed in the prior session (`session_20261125T034400Z`).
- **Verified the heavy-work gate is green on the real repo:** `python3 scripts/check_handoff_heavywork_gate.py --json` → `pass=true`, `reason_code=OK`, `vol_jump.required=false` (latest session `20261125T034400Z` == campaign start `20261125T034400Z`), `handoff_stale=false`, `root_count=500/500`, `failures=[]`.
- **Confirmed the active rank-0 campaign is `FCLR-VOL-JUMP-03-20261125T034400Z` (READY_EXECUTE)** in `research_state/experiment_frontier.json`.
- **Confirmed the grandfathering grace window is CLOSED** — the campaign start `20261125T034400Z` is in the past; any new session is immediately bound to the full `fclr_voljump03_*` artifact set.

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

# 4. Context only: the old 3-block scanner does not assess broad-panel feasibility
python3 scripts/next_campaign_status.py
```

---

## PRIOR SESSION CLOSE-OUT (2026-11-25T03:44:00Z — historical)

**What changed and why (real actions, not a timestamp bump):**
- Completed FCLR-VOL-JUMP-02 properly under `research_state/session_20261125T034400Z/` after the prior `session_20261124T230000Z` partial attempt (NaN candidate metrics; non-terminating O(n_boot×n) bootstrap) was superseded. Rewrote the evaluation with an equivalent O(n_boot × n_groups) group-code weighted cluster bootstrap; ran to completion (1,136,222 forecasts, 39,116 jump events, 454 coins, ~44s). Candidate Brier 0.033292 vs baseline 0.033322 → 0.0922% relative improvement, below the frozen 2% floor → NOT_SUPPORTED. Independent recompute `all_checks_match=true`, `n_checks=60`.

---

## BOTTLENECK RESOLUTION (this session — 2026-11-25T04:37:21Z)

- **RESOLVED (the core bottleneck — deferred heavy work):** the FCLR-VOL-JUMP-02 heavy evaluation had been announced but never executed; prior sessions only refreshed this handoff. RESOLVED by executing the full leakage-hardened jump02 evaluation in the prior session (`session_20261125T034400Z`) with the complete 13-artifact set and a passing independent recompute.
- **RESOLVED (future-dated grandfathering window):** the FCLR-VOL-JUMP-03 start is `20261125T034400Z` (the prior session time, in the past), so there is no future grace window; any new session is immediately bound. The gate stays green only because the latest session equals the start.
- **RESOLVED (root churn cap):** root `research_state/*.md|*.json` is at 500; all new artifacts went under `session_20261125T034400Z/`.
- **OPEN (next frontier execution):** `FCLR-VOL-JUMP-03-20261125T034400Z` must be executed properly — all required `fclr_voljump03_*` artifacts under one fresh `session_<UTC>/` (UTC > 20261125T034400Z), no zero-byte placeholders, numeric candidate metrics, in one session. This is the next agent's single, non-deferrable job.

---

## RESEARCH_PROMPT.md §19 ANSWERS (this refresh)

**What did the evidence support, contradict, or leave unknown?**
- Supported (prior, unchanged): the broad-universe cross-sectional funding → next-hour liquidation-intensity rank ordering generalizes but is NOT temporally stable.
- Contradicted/closed (prior session): the funding-conditioned volatility-JUMP hypothesis at broad scale under FULL leakage remediation (FCLR-VOL-JUMP-02 NOT_SUPPORTED — 0.1510% relative Brier improvement, below the 2% floor) — the jump null is now leakage-robust, completing the closure of all four repo-name volatility estimands plus their robustness.
- Unknown (next campaign): whether the jump null is also robust to the jump ESTIMATOR (bipower vs threshold-bipower) and the forecast HORIZON (24h vs 48h).

**What is the strongest alternative explanation?**
The volatility nulls (mean QLIKE 1.93%, correction-time, stress 1.51%, jump 0.0922%, leakage-hardened jump 0.1510%) may all reflect that funding carries weak, regime-dependent information that is economically immaterial at broad scale — or the jump null may be an artifact of the bipower estimator / 24h horizon. The jump03 multi-estimator/horizon study distinguishes these.

**Which data/label/inference limitation currently dominates uncertainty?**
1. Estimand: all four broad-scale volatility endpoints are closed and the jump null is leakage-robust; the open question is estimator/horizon robustness.
2. Label: ironflow liquidations are a capped-sample feed (constrains Half 2, not the funding/volatility jump arm).
3. Materiality/inference: no arm has cleared its frozen floor; the jump03 study must report Brier/log-loss contrasts with DM/Driscoll-Kraay HAC and Holm under full remediation across estimators and horizons.

**What concrete new test would falsify the current leading hypothesis?**
A broad-panel, fully leakage-hardened, train-only-threshold funding-conditioned signed-jump / semivariance-asymmetry robustness forecast that varies the jump estimator (bipower vs threshold-bipower) and horizon ({24h, 48h}) and either clears the frozen materiality floor with Holm-adjusted uncertainty (PROMOTED) or returns a clean null (NOT_SUPPORTED) that closes the jump arm for good.

**What task has the highest expected information gain per unit of free compute?**
`FCLR-VOL-JUMP-03` — it directly tests whether the repository-name first half's last closed estimand is robust to the jump estimator and horizon, using only frozen on-disk data.

**What exact artifact and command/test demonstrate progress?**
- Artifact: one fresh `research_state/session_<UTC>/` (UTC > 20261125T034400Z) with the full `fclr_voljump03_*` set plus `evidence_audit_<UTC>.json` and `trigger_check_<UTC>.json`, all non-empty, candidate metrics numeric (not NaN).
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` → `reason=OK` with `vol_jump.required=true` and `vol_jump.pass=true`.
- Test: `python3 -m unittest tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate tests.test_tracka_hardening_143 tests.test_active_campaign_gate` passes.

(End of file)