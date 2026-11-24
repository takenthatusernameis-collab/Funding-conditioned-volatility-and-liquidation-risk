# AGENT HANDOFF — 2026-11-24T21:28:00Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: HALF 1 (FUNDING-CONDITIONED VOLATILITY) CLOSED AT BROAD SCALE ON BOTH ARMS (mean QLIKE NOT_SUPPORTED; correction-time NOT_SUPPORTED). HALF 1 REMAINING FRONTIER = VOLATILITY-STRESS (TAIL-EXCEEDANCE) CLASSIFICATION, OPEN. HALF 2 (LIQUIDATION RISK) CONFIRMATORY-EXHAUSTED.**
> Active rank-0 campaign: `FCLR-VOL-STRESS-01-20261124T213000Z` (READY_EXECUTE).
> **REPO-NAME PRIORITY → `Funding-conditioned-volatility-and-liquidation-risk`**: the repository name leads with the volatility half. Both prior repo-name volatility arms are now closed at 342+ coin scale with valid negative results: (a) the broad RV-forecast (FCLR-VOL-BROAD-01, closed NOT_SUPPORTED, 1.93% relative QLIKE improvement < 2% floor), and (b) the Shek (2026) funding-extreme CORRECTION-TIME / correction-hazard pattern (FCLR-VOL-CORR-01, closed NOT_SUPPORTED this session, session_20261124T204500Z: high-RV median correction 9.00h vs low-RV 10.00h, contrast -10.0% relative — NOT slower in high-RV; materiality floor not met). The remaining repo-name frontier is the PRIMARY research question's volatility-STRESS sub-target (RESEARCH_PROMPT.md §3.1 "future realized volatility or volatility stress"; §7 target 1): a DISTINCT outcome family (realized-variance tail-exceedance classification, not mean QLIKE and not correction-time) that has never been tested confirmatory at broad scale.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-24T21:28:00Z**
>
> **READINESS VERIFIED THIS REFRESH (2026-11-24T21:28:00Z):** the heavy-work gate is `pass=true`/`reason_code=OK` (no `HANDOFF_STALE_LATEST_SESSION`; latest on-disk session `session_20261124T204500Z` is now recorded here). The frozen `ironflow_bulk` panel is byte-verified (54/54 parquet `.sha256` sidecars recomputed and matched, `bad=0`, months 2025-05..2026-10). The next session starts from a VERIFIED-READY state — the only remaining job is to execute the heavy study below, not to re-probe feasibility.
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is `Funding-conditioned-volatility-and-liquidation-risk`. Half 1 (funding-conditioned volatility) has TWO closed broad-scale arms: (a) the mean log-RV QLIKE forecast (FCLR-VOL-BROAD-01, closed NOT_SUPPORTED), and (b) the funding-extreme correction-time / correction-hazard pattern (FCLR-VOL-CORR-01, closed NOT_SUPPORTED this session). Half 2 (liquidation risk) is confirmatory-exhausted on the frozen `ironflow_bulk` panel. The next session's single, non-deferrable job is the **broad-universe funding-conditioned volatility-STRESS (tail-exceedance) forecast** — a DISTINCT outcome family (next-24h realized-variance tail exceedance, a classification target) that has never been run confirmatory at broad scale and directly addresses the §3.1 primary question's "volatility stress" sub-target.
>
> **THE NEXT FOCUS CAMPAIGN (rank-0, mandatory heavy work): `FCLR-VOL-STRESS-01-20261124T213000Z`**
>
> Execute a HEAVY, confirmatory, broad-panel study. This is real computation — not a status memo, not a source probe, not a trigger-check-only session, not a verify-and-stop session, and **not another timestamp-only refresh of this handoff** (see NON-AVOIDANCE below).
>
> **Question:** On the full frozen `ironflow_bulk` panel (18 monthly parquet, 2025-05..2026-10; `candles_1h`, `funding`, `open_interest`), does the funding + price-dislocation feature set improve out-of-sample forecasts of a realized-volatility STRESS event — next-24h realized variance exceeding an expanding, TRAIN-ONLY high quantile per coin — beyond a realized-volatility-only baseline, judged on Brier / log-loss / calibration with a frozen materiality floor and Holm-adjusted uncertainty?
>
> **Frozen inputs (do NOT re-derive, do NOT substitute):**
> - `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}/` (18 monthly parquet, 2025-05..2026-10). `candles_1h` columns: `timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades`. `funding`: `timestamp, market, coin, dex, funding_rate, premium`. Assert every `.sha256` sidecar before reading; caches are read-only and unmodified.
> - Stress-event definition (freeze in prereg): a volatility-stress event at forecast origin t is `RV_{t+1..t+24} > q_t` where `q_t` is an EXPANDING, TRAIN-ONLY quantile of trailing 24h realized variance per coin (no future information). Baseline = RV-only (persistence / HAR-style). Candidate = RV + signed/absolute funding + mark/index premium + mark/EMA24 distance. Feature standardization and thresholds are train-only.
> - Design: chronological walk-forward / expanding train-only thresholds; `PURGE_EMBARGO_H=48` (>= max 24h forward horizon); no random split; no overlapping forward targets across the purge boundary.
> - Inference: cluster-robust (CR1) by coin AND Driscoll-Kraay HAC; Holm correction over the declared family (baseline vs candidate × metric). Materiality floor (frozen, NOT relaxed): the candidate's relative Brier (or log-loss) improvement over the RV-only baseline must exceed a pre-declared relative floor; verdict is symmetric (`PROMOTED` / `NOT_SUPPORTED`); a null is a valid, publishable negative result that closes the volatility-stress arm.
>
> **Next agent's single job:** Produce the complete artifact set under one fresh `research_state/session_<UTC>/` (UTC strictly > `20261124T213000Z`), prefix `fclr_volstress01_`, all non-empty, no zero-byte placeholders:
> 1. `fclr_volstress01_source_registry_{json,md}` — sha256-asserted `ironflow_bulk` inventory (paths, rows, coins, month span, schemas) with a TOP-LEVEL `datasets` map containing `candles_1h`, `funding`, `open_interest`. The JSON MUST carry `input_integrity.sha256_all_match=true`, `input_integrity.sha256_verified_bad=0`, and a `files` list of >=54 entries each with a 64-hex `sha256` and `sha_match` not false.
> 2. `fclr_volstress01_prereg_{json,md}` — outcome-blind frozen prereg (`outcome_data_inspected_before_freeze:false`, `frozen_before_outcomes:true`, `design.kind` containing one of `forecast`/`classification`/`stress`/`tail`/`exceedance`/`walk_forward`, a `materiality_floor_rel` or `materiality_floor` > 0, `source_registry_sha256` == sha256 of the source-registry JSON). The closed mean-QLIKE and correction-time designs must NOT be relabeled as the stress design.
> 3. `fclr_volstress01_eval_{py,json,md}` — the heavy stress-forecast evaluation triad (`status` in {CONFIRMATORY_COMPLETE, NOT_SUPPORTED, PROMOTED, INCONCLUSIVE}, `holdout_opened:true`, integer `n_events>=1`, `metrics.{baseline,candidate}.brier` numeric, boolean `materiality_met`, `verdict`).
> 4. `fclr_volstress01_recompute_{py,json}` — independent stdlib recompute from stored input hashes/config (`all_checks_match:true`, integer `n_checks`).
> 5. `fclr_volstress01_evidence_audit_{json,md}` — evidence audit (`audit_pass:true`, `unresolved_blockers:[]`, `verdict` == eval verdict).
> 6. `evidence_audit_{UTC}.json` — gate-critical alias (`audit_pass:true`, `verdict` == eval verdict).
> 7. `trigger_check_{UTC}.json` — non-empty trigger check (`external_trigger_required:false`, `trigger_source:"FROZEN_IRONFLOW_BULK"`, `fired:false`; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data).
>
> Every JSON must carry `experiment_id:"FCLR-VOL-STRESS-01"` and `session_id:"session_<UTC>"` matching the directory. Record the real session id in `research_state/experiment_frontier.json` (promote rank-0 `READY_EXECUTE` → `COMPLETED_VALIDATED` only after artifacts exist) and update this handoff after the artifacts exist. Do NOT write a future/non-existent session id into this handoff before its artifacts exist.
>
> **DO NOT:** re-run the broad RV-forecast (FCLR-VOL-BROAD-01, closed NOT_SUPPORTED) or the correction-time campaign (FCLR-VOL-CORR-01, closed NOT_SUPPORTED) or the temporal-stability campaign; build a risk overlay (§9 forecast gate not passed); claim a forecast-gate pass from a cross-sectional association; wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; add root-level research-state files (root `*.md|*.json` at the 500 cap — all new artifacts MUST go under `session_<UTC>/`); relabel exploratory as confirmatory; threshold-shop or relax the frozen floor after outcomes.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **A timestamp-only rewrite of this file is NOT progress and is explicitly forbidden as the next session's deliverable.** The prior program loop refreshed this handoff many times without producing a post-start heavy session; that loop is the failure mode this section exists to end.
- **How the gate's grandfathering works, and why it does NOT excuse idling:** `_vol_stress_state` (scripts/check_handoff_heavywork_gate.py) sets `required=true` only once the latest session *recorded in this handoff* is later than the campaign start `20261124T213000Z`. As long as this file points at `session_20261124T204500Z` (which predates the campaign start), `vol_stress.required=false` (grandfathered) and the gate stays green. **That green is a property of pointing at an older session, not evidence that the work is done.** The moment you create any `session_<UTC>` newer than `20261124T213000Z`, the binder flips `required=true` and the full `fclr_volstress01_*` set (plus `evidence_audit_` alias and non-empty `trigger_check_`) is mandatory; a trigger-only, prose-only, audit-only, prereg-only, verify-and-stop, empty, or arbitrary `recompute_*` session FAILS CLOSED.
- **Do not create a partial/empty session directory and leave it unrecorded.** That produces `HANDOFF_STALE_LATEST_SESSION:<dir>` and fails the gate closed for every later session (this exact failure occurred with the prior partial `session_20261124T204500Z`, now completed and recorded). If you create `session_<UTC>/`, populate it fully and record it in this handoff in the same session.
- Do not re-run any terminal campaign. Do not wait for an external trigger. Do not build a risk overlay. Do not track-adulterate. Do not ship a verdict from a non-reconciled eval (emit a verdict only after the independent recompute reports `all_checks_match:true`; preserve fail-closed behavior).
- **DO NOT treat `python3 scripts/next_campaign_status.py` output as a feasibility verdict.** That script only tests the OLD 3-contiguous-30-day-block framing and prints `no feasible 3-block design in ANY domain`. It does NOT assess the broad-panel volatility-stress design, which IS feasible today on the full 18-month `ironflow_bulk` panel. Misreading this output as "no feasible heavy work exists" and idling is a non-avoidance failure.
- Root `research_state/*.md|*.json` is at the 500 cap. All new artifacts MUST go under `session_<UTC>/`.

---

## FOCUS CAMPAIGN — FCLR-VOL-STRESS-01-20261124T213000Z (rank-0, READY_EXECUTE)

**Question (OPEN):** Does the funding + price-dislocation feature set improve out-of-sample forecasts of a realized-volatility STRESS event (next-24h realized variance above a train-only high quantile) beyond an RV-only baseline on the broad 342+ coin `ironflow_bulk` panel, clearing a frozen materiality floor with Holm-adjusted uncertainty?

**Why this is the highest-value next task:**
- Repo name leads with **Funding-conditioned-volatility**; both prior broad-scale volatility arms (mean QLIKE and correction-time) are now closed NOT_SUPPORTED, so the volatility-STRESS classification estimand is the remaining repo-name volatility question.
- It is a DISTINCT outcome family (tail-exceedance classification, not mean QLIKE, not correction-time) — not a re-run of a terminal endpoint (RESEARCH_PROMPT.md §16).
- It directly addresses the §3.1 primary research question's "volatility stress" sub-target, which has never been tested confirmatory at broad scale.
- A null is a strong, publishable negative result; a pass would be the first broad-scale funding-conditioned volatility-stress skill and would still face the §17 promotion conditions in full.

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/candles_1h/` — 18 monthly parquet, hourly OHLC.
- `research_state/data_cache/ironflow_bulk/funding/` — 18 monthly parquet, `funding_rate`, `premium`.
- `research_state/data_cache/ironflow_bulk/open_interest/` — 18 monthly parquet, `mark_price`, `oracle_price`, `open_interest`.
- Assert every `.sha256` sidecar before reading; caches are read-only.

**Produced artifacts (target — ALL under one fresh `session_<UTC>/`; non-empty):**
- `fclr_volstress01_source_registry_<UTC>.{json,md}`
- `fclr_volstress01_prereg_<UTC>.{json,md}`
- `fclr_volstress01_eval_<UTC>.{py,json,md}`
- `fclr_volstress01_recompute_<UTC>.{py,json}` (`all_checks_match:true`)
- `fclr_volstress01_evidence_audit_<UTC>.{json,md}`
- `evidence_audit_<UTC>.json` (gate-critical alias)
- `trigger_check_<UTC>.json`

---

## STATE OF THE WORK (read before doing anything)

- **Half 1 (volatility) — broad RV forecast (mean QLIKE):** CLOSED. FCLR-VOL-BROAD-01 (session_20261124T120000Z) NOT_SUPPORTED: broad-panel (342+ coin, 18-month `ironflow_bulk`) funding-conditioned RV forecast improved QLIKE 1.93% relative over the RV-only baseline, below the frozen 2% floor; 23 test blocks, 684,301 forecasts; independent stdlib recompute `all_checks_match=true`.
- **Half 1 (volatility) — 5-coin null:** leakage-robust null (FCLR-011; panel FE study session_20261121T130159Z).
- **Half 1 (volatility) — correction-time frontier:** CLOSED. FCLR-VOL-CORR-01 (session_20261124T204500Z) NOT_SUPPORTED this session: 227,023 funding-extreme events; high-RV median correction 9.00h vs low-RV 10.00h (contrast -10.0% relative, NOT slower in high-RV); frozen >=10% relative slower-correction materiality floor NOT met; independent stdlib recompute `all_checks_match=true`, `n_checks=29`.
- **Half 1 (volatility) — stress / tail-exceedance frontier:** OPEN — this campaign (FCLR-VOL-STRESS-01).
- **Half 2 (liquidation risk):** confirmatory-exhausted on the frozen `ironflow_bulk` panel. Track A STRUCTURALLY_BLOCKED (capped-sample feed, not a census); Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; broad cross-sectional rank ordering SUPPORTED_GENERALIZATION but NOT_STABLE (§17 condition #4) and 2% Poisson-deviance materiality floor NOT MET.
- **Heavy-work gate:** the prior FCLR-VOL-CORR-01 binder is now dormant (this handoff refers to that campaign by name only, no timestamped id, so it will not re-fire). The new FCLR-VOL-STRESS-01 binder is active but grandfathered (latest on-disk session `session_20261124T204500Z` predates the campaign start `20261124T213000Z`) — green today ONLY via grandfathering, NOT because the work is done.
- **Forecast gate (§9):** NOT PASSED — no broad-scale volatility skill demonstrated; materiality floor not met on any prior arm. Risk overlay INELIGIBLE.
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
- **Do NOT include any other `FCLR-…-<8digit>T<6digit>Z` campaign id in this file** (refer to closed campaigns by name only, e.g. "FCLR-VOL-BROAD-01 (closed)"). A stray timestamped id would activate that campaign's binder on every future session and fail it closed. The ONLY timestamped campaign id permitted in this file is the active `FCLR-VOL-STRESS-01-20261124T213000Z`.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 2025-05..2026-10; hourly OHLC. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; `funding_rate`, `premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; `mark_price`, `oracle_price`, `open_interest`. |
| `research_state/session_20261124T204500Z/` | Latest complete heavy session (FCLR-VOL-CORR-01; NOT_SUPPORTED; correction-time binder satisfied; 13 non-empty artifacts). |
| `research_state/session_20261124T120000Z/` | Prior complete heavy session (FCLR-VOL-BROAD-01; NOT_SUPPORTED; mean QLIKE). |
| `research_state/session_20261121T130159Z/` | 5-coin panel fixed-effects volatility study (prior null). |
| `research_state/experiment_frontier.json` | rank-0 is `FCLR-VOL-STRESS-01-20261124T213000Z` (READY_EXECUTE); FCLR-VOL-CORR-01 and FCLR-VOL-BROAD-01 are COMPLETED_VALIDATED (NOT_SUPPORTED). |
| `research_state/negative_results_report.md` | Null/failed/inconclusive outcomes preserved. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3 (primary + secondary research question), §7 (targets), §9 (overlay gate), §16 (adaptive feasibility), §17 (promotion), §19 (definition of done), §20 (status contract).
- `scripts/check_handoff_heavywork_gate.py` — `VOL_STRESS_CAMPAIGN_RE` / `_vol_stress_state` / `VOL_STRESS_REQUIRED` binder (active, grandfathered); `VOL_CORR_CAMPAIGN_RE` / `_vol_corr_state` (dormant — no timestamped id in this file); `VOL_BROAD_CAMPAIGN_RE` / `_vol_broad_state` (dormant).
- `tests/test_vol_stress_campaign_gate.py` — regression pinning the new stress binder (11 tests).
- `tests/test_vol_corr_campaign_gate.py` — regression pinning the (now dormant) correction binder.
- `research_state/experiment_frontier.json` — rank-0 campaign registry.
- `research_state/data_cache/ironflow_bulk/` — frozen broad panel.
- `research_state/negative_results_report.md` — preserved nulls/negatives.

---

## SESSION CLOSE-OUT (THIS SESSION — 2026-11-24T21:28:00Z)

**What changed and why (real actions, not a timestamp bump):**
- **Completed the FCLR-VOL-CORR-01 heavy study that a prior session had left half-done.** A prior agent created `session_20261124T204500Z/` containing only `fclr_volcorr01_eval_20261124T204500Z.py` and never recorded it, so the heavy-work gate failed closed with `HANDOFF_STALE_LATEST_SESSION:session_20261124T204500Z` for every later session. This session finished the study: fixed a `Timedelta.astype` bug in the eval, froze an outcome-blind source registry + prereg (bound to the registry sha256) BEFORE computing outcomes, ran the heavy 227,023-event correction-time / hazard evaluation, produced an independent stdlib recompute (`all_checks_match=true`, `n_checks=29`), the evidence audit (json+md), the gate-critical alias, and the trigger check — 13 non-empty artifacts, no zero-byte placeholders.
- **Recorded `session_20261124T204500Z` as the latest session** in this handoff, clearing the stale-session failure; the gate is now `pass=true`/`reason_code=OK`.
- **Closed the correction-time arm and promoted the next repo-name frontier.** FCLR-VOL-CORR-01 returned NOT_SUPPORTED; `experiment_frontier.json` marks it COMPLETED_VALIDATED and promotes the new rank-0 `FCLR-VOL-STRESS-01-20261124T213000Z`.
- **Built the next binding campaign so future agents cannot idle.** Added the `VOL_STRESS_CAMPAIGN_RE` / `_vol_stress_state` / `VOL_STRESS_REQUIRED` binder to the gate (mirroring the vol_corr binder, with stress-forecast content checks), wired it into `check()`, added `fclr_volcorr`/`fclr_volstress` to `NEW_QUANT_PREFIXES`, and added `tests/test_vol_stress_campaign_gate.py` (11 tests). A post-start session cannot pass with a trigger-only/prose-only/audit-only/prereg-only/verify-and-stop session or a closed-endpoint design relabeled as stress.

**Exact test outcomes with paths (this session):**
- Heavy-work gate: `python3 scripts/check_handoff_heavywork_gate.py --json` → `pass=true`, `reason_code=OK`, `failures=[]`, `handoff_stale=false`, `vol_stress.required=false`/`vol_stress.pass=true` (grandfathered: latest session `session_20261124T204500Z` predates campaign start `20261124T213000Z`), `vol_corr.required=false` (dormant).
- Gate binder compile: `python3 -m py_compile scripts/check_handoff_heavywork_gate.py` → OK.
- Campaign-gate regression suite: `python3 -m unittest tests.test_vol_stress_campaign_gate tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate tests.test_tracka_hardening_143 tests.test_active_campaign_gate` → all pass.
- FCLR-VOL-CORR-01 eval: `python3 research_state/session_20261124T204500Z/fclr_volcorr01_eval_20261124T204500Z.py` → `status=CONFIRMATORY_COMPLETE`, `verdict=NOT_SUPPORTED`, `n_events=227023`, high median 9.00h, low median 10.00h, `materiality_met=false`.
- FCLR-VOL-CORR-01 recompute: `all_checks_match=true`, `n_checks=29`, `verdict_recompute=NOT_SUPPORTED` == eval.
- Frozen cache integrity: 54/54 parquet `.sha256` sidecars recomputed and matched (`bad=0`) via the source-registry build.

**State of each research gate:**
- Heavy-work gate: **SATISFIED / GREEN** (latest session recorded; vol_stress binder active but grandfathered because no post-start session exists yet — it flips to `required=true` the instant the next session creates `session_<UTC> > 20261124T213000Z`).
- Forecast gate (§9): **NOT PASSED** (no broad-scale volatility skill; 2% QLIKE materiality floor not met on any prior arm).
- Half 1 (volatility) — RV forecast (mean QLIKE): **CLOSED NOT_SUPPORTED at broad scale** (FCLR-VOL-BROAD-01; 1.93% < 2%).
- Half 1 (volatility) — correction-time: **CLOSED NOT_SUPPORTED at broad scale** (FCLR-VOL-CORR-01; this session).
- Half 1 (volatility) — stress / tail-exceedance: **OPEN** (this campaign closes it).
- Half 2 (liquidation risk): **CONFIRMATORY EXHAUSTED**.

**Single highest-value next task:**
Execute `FCLR-VOL-STRESS-01-20261124T213000Z` — a HEAVY, confirmatory, broad-panel funding-conditioned volatility-STRESS (tail-exceedance) forecast with a frozen outcome-blind prereg, event-study/classification evaluation, independent stdlib recompute, evidence audit, gate-critical alias, and trigger check, all under one fresh `session_<UTC>/` (UTC strictly > `20261124T213000Z`). This is the deliverable; a handoff refresh is not.

**Precise verifying commands:**
```bash
# 0. One-time environment setup if needed
python3 -m pip install --quiet numpy pandas pyarrow

# 1. Heavy-work gate must return reason=OK
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Gate binder must compile
python3 -m py_compile scripts/check_handoff_heavywork_gate.py

# 3. Campaign-gate regression suite must pass (incl. new vol_stress binder)
python3 -m unittest \
  tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate \
  tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 \
  tests.test_active_campaign_gate

# 4. Context only: the old 3-block scanner does not assess broad-panel feasibility
python3 scripts/next_campaign_status.py
```

**Any remaining blocker and the next materially different route:**
- **Blocker:** None. The gate is green (`reason=OK`), the frozen `ironflow_bulk` panel is byte-verified (54/54 sidecars matched, `bad=0`), and no session is stale or partial. Half 1 mean-QLIKE and correction-time arms are closed at broad scale; Half 2 confirmatory paths are exhausted. The volatility-stress arm is the open frontier, not a blocker.
- **Next route:** `FCLR-VOL-STRESS-01` — broad-panel funding-conditioned volatility-stress (tail-exceedance) forecast (this campaign). If it returns a null, the funding/volatility program is closed at broad scale on all three estimands and the only remaining route is a new admissible free observed-liquidation source (which cannot fire on frozen data).

---

## BOTTLENECK RESOLUTION (this refresh)

- **RESOLVED THIS REFRESH (2026-11-24T21:28:00Z) — stale partial session blocking the gate:** `session_20261124T204500Z/` held only an unrun `fclr_volcorr01_eval_*.py` and was unrecorded, so the gate failed closed (`HANDOFF_STALE_LATEST_SESSION`). The study was completed in full (13 non-empty artifacts), the session was recorded here, and the gate now returns `pass=true`/`reason_code=OK`. The next session inherits a green, byte-verified state.
- **RESOLVED THIS REFRESH (2026-11-24T21:28:00Z) — frontier exhausted / idle escape hatch:** with both prior repo-name volatility arms closed, a future agent could have declared the program done and idled. The new rank-0 `FCLR-VOL-STRESS-01` campaign (a distinct, feasible, heavy tail-exceedance study on the same frozen panel) plus its gate binder removes that escape hatch: a post-start session cannot pass without the full heavy artifact set.
- **RESOLVED (avoidance hazard — refresh loop / grandfathering):** the handoff had been refreshed repeatedly without producing a post-start session; `vol_stress.required` stays false because the file points at pre-start `session_20261124T204500Z`. The NON-AVOIDANCE section names this mechanism and forbids a timestamp-only refresh as the next deliverable.
- **RESOLVED (avoidance hazard — `next_campaign_status.py` misleading output):** the script prints `no feasible 3-block design in ANY domain`, true only for the obsolete 3-contiguous-30-day-block framing. A future agent could misread this as "no heavy work is possible" and idle. Hard non-avoidance constraint forbids that misread; the broad-panel volatility-stress design is feasible on the full 18-month panel and is the mandated heavy work.
- **RESOLVED (root churn cap):** root `research_state/*.md|*.json` is at 500; all new artifacts must go under `session_<UTC>/`.
- **OPEN (next frontier execution):** `FCLR-VOL-STRESS-01-20261124T213000Z` must be executed — all required artifacts under one fresh `session_<UTC>/`, no zero-byte placeholders, in one session. This is the next agent's single, non-deferrable job.

---

## RESEARCH_PROMPT.md §19 ANSWERS (this session)

**What did the evidence support, contradict, or leave unknown?**
- Supported (prior, unchanged): the broad-universe cross-sectional funding → next-hour liquidation-intensity rank ordering generalizes but is NOT temporally stable.
- Contradicted/closed this session: the Shek (2026) funding-extreme correction-time / correction-hazard hypothesis at broad scale (FCLR-VOL-CORR-01 NOT_SUPPORTED — high-RV correction not slower than low-RV; materiality floor not met) — Half 1 correction-time closed at broad scale.
- Unknown (this campaign): whether the funding + price feature set improves out-of-sample realized-volatility STRESS (tail-exceedance) forecasts beyond an RV-only baseline at broad scale.

**What is the strongest alternative explanation?**
The broad RV-forecast near-miss (1.93%) and the correction-time null may both reflect that funding carries weak, regime-dependent information that a tail/stress classification estimand (more sensitive to the tails that matter for risk) could detect — or it may be noise. The stress study distinguishes these.

**Which data/label/inference limitation currently dominates uncertainty?**
1. Estimand: mean-QLIKE and correction-time endpoints are closed; the stress/tail classification estimand is untested at broad scale.
2. Label: ironflow liquidations are a capped-sample feed (constrains Half 2, not the funding/volatility stress arm).
3. Materiality/inference: no arm has cleared its frozen floor; the stress study must report Brier/log-loss contrasts with DM/Driscoll-Kraay HAC and Holm.

**What concrete new test would falsify the current leading hypothesis?**
A broad-panel, leakage-hardened, train-only-threshold funding-conditioned volatility-stress forecast that either clears the frozen materiality floor with Holm-adjusted uncertainty (PROMOTED) or returns a clean null (NOT_SUPPORTED) closing the stress arm at broad scale.

**What task has the highest expected information gain per unit of free compute?**
`FCLR-VOL-STRESS-01` — it directly tests the repository-name first half via a distinct, never-confirmatory broad-scale estimand, using only frozen on-disk data.

**What exact artifact and command/test demonstrate progress?**
- Artifact: one fresh `research_state/session_<UTC>/` with the full `fclr_volstress01_*` set plus `evidence_audit_<UTC>.json` and `trigger_check_<UTC>.json`.
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` → `reason=OK` with `vol_stress.required=true` and `vol_stress.pass=true`.
- Test: `python3 -m unittest tests.test_vol_stress_campaign_gate tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate tests.test_tracka_hardening_143 tests.test_active_campaign_gate` passes.

(End of file)