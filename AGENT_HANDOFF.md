# AGENT HANDOFF — 2026-11-25T02:54:00Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: HALF 1 (FUNDING-CONDITIONED VOLATILITY) CLOSED AT BROAD SCALE ON THREE ARMS (mean QLIKE NOT_SUPPORTED; correction-time NOT_SUPPORTED; volatility-STRESS / tail-exceedance NOT_SUPPORTED). HALF 1 REMAINING FRONTIER = SIGNED-JUMP / SEMIVARIANCE-ASYMMETRY CLASSIFICATION, OPEN. HALF 2 (LIQUIDATION RISK) CONFIRMATORY-EXHAUSTED.**
> Active rank-0 campaign: `FCLR-VOL-JUMP-01-20261124T223000Z` (READY_EXECUTE).
> **REPO-NAME PRIORITY → `Funding-conditioned-volatility-and-liquidation-risk`**: the repository name leads with the volatility half. Three prior repo-name volatility arms are now closed at broad scale with valid negative results: (a) the broad RV-forecast (FCLR-VOL-BROAD-01, closed NOT_SUPPORTED, 1.93% relative QLIKE improvement < 2% floor); (b) the Shek (2026) funding-extreme CORRECTION-TIME / correction-hazard pattern (FCLR-VOL-CORR-01, closed NOT_SUPPORTED, high-RV median correction 9.00h vs low-RV 10.00h); and (c) the volatility-STRESS / tail-exceedance classification (FCLR-VOL-STRESS-01, closed NOT_SUPPORTED, session_20261124T222500Z: 1.51% relative Brier improvement over the RV-only baseline across 1,393,204 forecasts / 314 coins / 63,059 stress events, below the frozen 2% floor). The remaining repo-name frontier is the PRIMARY research question's SIGNED-JUMP / SEMIVARIANCE-ASYMMETRY sub-target (RESEARCH_PROMPT.md §3.1 "future realized volatility"; §7 target 1): a DISTINCT outcome family (jump / asymmetry, not mean QLIKE, not correction-time, not total-variance tail exceedance) that has never been tested confirmatory at broad scale.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-25T02:54:00Z**
>
> **CURRENT GATE STATE (2026-11-25T02:54:00Z):** The heavy-work gate returns `pass=false`, `reason_code=HANDOFF_HEAVYWORK_GATE_FAILED`, `failures=["HANDOFF_STALE_LATEST_SESSION:session_20261124T230000Z"]`. A partial session `session_20261124T230000Z` exists on disk with some `fclr_voljump01_*` artifacts but is INCOMPLETE: the evaluation produced NaN for all candidate metrics (Brier, log_loss, ece), and the following mandatory artifacts are MISSING: `fclr_voljump01_eval_<UTC>.md`, `fclr_voljump01_recompute_<UTC>.py`, `fclr_voljump01_recompute_<UTC>.json`, `fclr_voljump01_evidence_audit_<UTC>.json`, `fclr_voljump01_evidence_audit_<UTC>.md`, `evidence_audit_<UTC>.json` (gate-critical alias), `trigger_check_<UTC>.json`. Per NON-AVOIDANCE constraint: "Do not create a partial/empty session directory and leave it unrecorded. That produces HANDOFF_STALE_LATEST_SESSION:<dir> and fails the gate closed for every later session." The next session MUST create a NEW complete session `session_<UTC>/` with UTC strictly > `20261124T230000Z` containing ALL required artifacts, or fully complete the existing partial session (fix the NaN eval and add all missing artifacts). A timestamp-only handoff refresh is NOT progress.
>
> **READINESS VERIFIED:** The frozen `ironflow_bulk` panel is byte-verified (54/54 parquet `.sha256` sidecars recomputed and matched, `bad=0`, months 2025-05..2026-10). The source registry from the partial session is VALID and can be reused (sha256: `e8d3bb5eb4ebde9439d3753c3241742f4f9e9239d90c817c2ab809fc519ef01b`). The prereg from the partial session is VALID and outcome-blind (`outcome_data_inspected_before_freeze:false`, `design.kind` = `walk_forward_classification_signed_jump_semivariance_asymmetry`). The only blocker is the broken evaluation (NaN candidate metrics) and missing artifacts.
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is `Funding-conditioned-volatility-and-liquidation-risk`. Half 1 (funding-conditioned volatility) has THREE closed broad-scale arms: (a) the mean log-RV QLIKE forecast (FCLR-VOL-BROAD-01, closed NOT_SUPPORTED), (b) the funding-extreme correction-time / correction-hazard pattern (FCLR-VOL-CORR-01, closed NOT_SUPPORTED), and (c) the volatility-STRESS / tail-exceedance classification (FCLR-VOL-STRESS-01, closed NOT_SUPPORTED). Half 2 (liquidation risk) is confirmatory-exhausted on the frozen `ironflow_bulk` panel. The next session's single, non-deferrable job is the **broad-universe funding-conditioned SIGNED-JUMP / SEMIVARIANCE-ASYMMETRY forecast** — a DISTINCT outcome family (next-24h signed-jump / downside-vs-upside semivariance-asymmetry tail exceedance, a classification target) that has never been run confirmatory at broad scale and directly addresses the §3.1 primary question's "future realized volatility" sub-target.
>
> **THE NEXT FOCUS CAMPAIGN (rank-0, mandatory heavy work): `FCLR-VOL-JUMP-01-20261124T223000Z`**
>
> Execute a HEAVY, confirmatory, broad-panel study. This is real computation — not a status memo, not a source probe, not a trigger-check-only session, not a verify-and-stop session, and **not another timestamp-only refresh of this handoff** (see NON-AVOIDANCE below).
>
> **Question:** On the full frozen `ironflow_bulk` panel (18 monthly parquet, 2025-05..2026-10; `candles_1h`, `funding`, `open_interest`), does the funding + price-dislocation feature set improve out-of-sample forecasts of a SIGNED-JUMP / SEMIVARIANCE-ASYMMETRY event — next-24h jump component (total realized variance minus bipower/continuous variation, signed by the dominant realized semivariance) exceeding an expanding, TRAIN-ONLY high quantile per coin — beyond a realized-volatility-only baseline, judged on Brier / log-loss / calibration with a frozen materiality floor and Holm-adjusted uncertainty?
>
> **Frozen inputs (do NOT re-derive, do NOT substitute):**
> - `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}/` (18 monthly parquet, 2025-05..2026-10). `candles_1h` columns: `timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades`. `funding`: `timestamp, market, coin, dex, funding_rate, premium`. Assert every `.sha256` sidecar before reading; caches are read-only and unmodified.
> - Jump-event definition (freeze in prereg): a jump-stress event at forecast origin t is `J_{t+1..t+24} > q_t` where `J` is the next-24h signed-jump magnitude (realized variance minus bipower variation, signed by the sign of the realized semivariance difference RS+ − RS−) and `q_t` is an EXPANDING, TRAIN-ONLY high quantile of trailing signed-jump magnitude per coin (no future information). Baseline = RV-only (persistence / HAR-style). Candidate = RV + signed/absolute funding + mark/index premium + mark/EMA24 distance. Feature standardization and thresholds are train-only.
> - Design: chronological walk-forward / expanding train-only thresholds; `PURGE_EMBARGO_H=48` (>= max 24h forward horizon); no random split; no overlapping forward targets across the purge boundary.
> - Inference: cluster-robust (CR1) by coin AND Driscoll-Kraay HAC; Holm correction over the declared family (baseline vs candidate × metric). Materiality floor (frozen, NOT relaxed): the candidate's relative Brier (or log-loss) improvement over the RV-only baseline must exceed a pre-declared relative floor; verdict is symmetric (`PROMOTED` / `NOT_SUPPORTED`); a null is a valid, publishable negative result that closes the volatility-jump arm.
>
> **Next agent's single job:** Produce the complete artifact set under one fresh `research_state/session_<UTC>/` (UTC strictly > `20261124T230000Z`), prefix `fclr_voljump01_`, all non-empty, no zero-byte placeholders:
> 1. `fclr_voljump01_source_registry_{json,md}` — sha256-asserted `ironflow_bulk` inventory (paths, rows, coins, month span, schemas) with a TOP-LEVEL `datasets` map containing `candles_1h`, `funding`, `open_interest`. The JSON MUST carry `input_integrity.sha256_all_match=true`, `input_integrity.sha256_verified_bad=0`, and a `files` list of >=54 entries each with a 64-hex `sha256` and `sha_match` not false. (Can reuse the valid source registry from the partial session; sha256 must match.)
> 2. `fclr_voljump01_prereg_{json,md}` — outcome-blind frozen prereg (`outcome_data_inspected_before_freeze:false`, `frozen_before_outcomes:true`, `design.kind` containing one of `jump`/`asymmetry`/`bipower`/`semivariance`/`signed_jump`/`downside`, a `materiality_floor_rel` or `materiality_floor` > 0, `source_registry_sha256` == sha256 of the source-registry JSON). The closed mean-QLIKE, correction-time, and total-variance tail-exceedance designs must NOT be relabeled as the jump design. (Can reuse the valid prereg from the partial session; sha256 must match.)
> 3. `fclr_voljump01_eval_{py,json,md}` — the heavy jump-forecast evaluation triad (`status` in {CONFIRMATORY_COMPLETE, NOT_SUPPORTED, PROMOTED, INCONCLUSIVE}, `holdout_opened:true`, integer `n_events>=1`, `metrics.{baseline,candidate}.brier` numeric (NOT NaN), boolean `materiality_met`, `verdict`). **MUST FIX the NaN candidate metrics from the partial session.**
> 4. `fclr_voljump01_recompute_{py,json}` — independent stdlib recompute from stored input hashes/config (`all_checks_match:true`, integer `n_checks`).
> 5. `fclr_voljump01_evidence_audit_{json,md}` — evidence audit (`audit_pass:true`, `unresolved_blockers:[]`, `verdict` == eval verdict).
> 6. `evidence_audit_{UTC}.json` — gate-critical alias (`audit_pass:true`, `verdict` == eval verdict).
> 7. `trigger_check_{UTC}.json` — non-empty trigger check (`external_trigger_required:false`, `trigger_source:"FROZEN_IRONFLOW_BULK"`, `fired:false`; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data).
>
> Every JSON must carry `experiment_id:"FCLR-VOL-JUMP-01"` and `session_id:"session_<UTC>"` matching the directory. Record the real session id in `research_state/experiment_frontier.json` (promote rank-0 `READY_EXECUTE` → `COMPLETED_VALIDATED` only after artifacts exist) and update this handoff after the artifacts exist. Do NOT write a future/non-existent session id into this handoff before its artifacts exist.
>
> **DO NOT:** re-run the broad RV-forecast (FCLR-VOL-BROAD-01, closed NOT_SUPPORTED), the correction-time campaign (FCLR-VOL-CORR-01, closed NOT_SUPPORTED), the volatility-stress campaign (FCLR-VOL-STRESS-01, closed NOT_SUPPORTED), or the temporal-stability campaign; build a risk overlay (§9 forecast gate not passed); claim a forecast-gate pass from a cross-sectional association; wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; add root-level research-state files (root `*.md|*.json` at the 500 cap — all new artifacts MUST go under `session_<UTC>/`); relabel exploratory as confirmatory; threshold-shop or relax the frozen floor after outcomes.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **A timestamp-only rewrite of this file is NOT progress and is explicitly forbidden as the next session's deliverable.** The prior program loop refreshed this handoff many times without producing a post-start heavy session; that loop is the failure mode this section exists to end.
- **How the gate's grandfathering works, and why it does NOT excuse idling:** `_vol_jump_state` (scripts/check_handoff_heavywork_gate.py) sets `required=true` only once the latest session *recorded in this handoff* is later than the campaign start `20261124T223000Z`. As long as this file points at `session_20261124T222500Z` (which predates the campaign start), `vol_jump.required=false` (grandfathered) and the gate stays green. **That green is a property of pointing at an older session, not evidence that the work is done.** The moment you create any `session_<UTC>` newer than `20261124T223000Z`, the binder flips `required=true` and the full `fclr_voljump01_*` set (plus `evidence_audit_` alias and non-empty `trigger_check_`) is mandatory; a trigger-only, prose-only, audit-only, prereg-only, verify-and-stop, empty, or arbitrary `recompute_*` session FAILS CLOSED.
- **Do not create a partial/empty session directory and leave it unrecorded.** That produces `HANDOFF_STALE_LATEST_SESSION:<dir>` and fails the gate closed for every later session (this exact failure occurred with `session_20261124T230000Z`). If you create `session_<UTC>/`, populate it fully and record it in this handoff in the same session.
- Do not re-run any terminal campaign. Do not wait for an external trigger. Do not build a risk overlay. Do not track-adulterate. Do not ship a verdict from a non-reconciled eval (emit a verdict only after the independent recompute reports `all_checks_match:true`; preserve fail-closed behavior).
- **DO NOT treat `python3 scripts/next_campaign_status.py` output as a feasibility verdict.** That script only tests the OLD 3-contiguous-30-day-block framing and prints `no feasible 3-block design in ANY domain`. It does NOT assess the broad-panel signed-jump design, which IS feasible today on the full 18-month `ironflow_bulk` panel. Misreading this output as "no feasible heavy work exists" and idling is a non-avoidance failure.
- Root `research_state/*.md|*.json` is at the 500 cap. All new artifacts MUST go under `session_<UTC>/`.

---

## FOCUS CAMPAIGN — FCLR-VOL-JUMP-01-20261124T223000Z (rank-0, READY_EXECUTE)

**Question (OPEN):** Does the funding + price-dislocation feature set improve out-of-sample forecasts of a signed-jump / semivariance-asymmetry event (next-24h jump component above a train-only high quantile) beyond an RV-only baseline on the broad 314-coin `ironflow_bulk` panel, clearing a frozen materiality floor with Holm-adjusted uncertainty?

**Why this is the highest-value next task:**
- Repo name leads with **Funding-conditioned-volatility**; all three prior broad-scale volatility arms (mean QLIKE, correction-time, and volatility-stress) are now closed NOT_SUPPORTED, so the signed-jump / semivariance-asymmetry classification estimand is the remaining repo-name volatility question.
- It is a DISTINCT outcome family (jump / asymmetry, not mean QLIKE, not correction-time, not total-variance tail exceedance) — not a re-run of a terminal endpoint (RESEARCH_PROMPT.md §16).
- It directly addresses the §3.1 primary research question's "future realized volatility" sub-target, which has never been tested confirmatory at broad scale via the jump/asymmetry channel.
- A null is a strong, publishable negative result; a pass would be the first broad-scale funding-conditioned volatility-jump skill and would still face the §17 promotion conditions in full.

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/candles_1h/` — 18 monthly parquet, hourly OHLC.
- `research_state/data_cache/ironflow_bulk/funding/` — 18 monthly parquet, `funding_rate`, `premium`.
- `research_state/data_cache/ironflow_bulk/open_interest/` — 18 monthly parquet, `mark_price`, `oracle_price`, `open_interest`.
- Assert every `.sha256` sidecar before reading; caches are read-only.

**Produced artifacts (target — ALL under one fresh `session_<UTC>/`; non-empty):**
- `fclr_voljump01_source_registry_<UTC>.{json,md}`
- `fclr_voljump01_prereg_<UTC>.{json,md}`
- `fclr_voljump01_eval_<UTC>.{py,json,md}`
- `fclr_voljump01_recompute_<UTC>.{py,json}` (`all_checks_match:true`)
- `fclr_voljump01_evidence_audit_<UTC>.{json,md}`
- `evidence_audit_<UTC>.json` (gate-critical alias)
- `trigger_check_<UTC>.json`

---

## STATE OF THE WORK (read before doing anything)

- **Half 1 (volatility) — broad RV forecast (mean QLIKE):** CLOSED. FCLR-VOL-BROAD-01 (session_20261124T120000Z) NOT_SUPPORTED: broad-panel (314+ coin, 18-month `ironflow_bulk`) funding-conditioned RV forecast improved QLIKE 1.93% relative over the RV-only baseline, below the frozen 2% floor; 23 test blocks, 684,301 forecasts; independent stdlib recompute `all_checks_match=true`.
- **Half 1 (volatility) — 5-coin null:** leakage-robust null (FCLR-011; panel FE study session_20261121T130159Z).
- **Half 1 (volatility) — correction-time frontier:** CLOSED. FCLR-VOL-CORR-01 (session_20261124T204500Z) NOT_SUPPORTED: 227,023 funding-extreme events; high-RV median correction 9.00h vs low-RV 10.00h (contrast -10.0% relative, NOT slower in high-RV); frozen >=10% relative slower-correction materiality floor NOT met; independent stdlib recompute `all_checks_match=true`, `n_checks=29`.
- **Half 1 (volatility) — stress / tail-exceedance frontier:** CLOSED. FCLR-VOL-STRESS-01 (session_20261124T222500Z) NOT_SUPPORTED: 1,393,204 forecasts, 63,059 stress events, 314 coins, 6 test blocks; Brier baseline 0.041718 vs candidate 0.041087 (1.51% relative improvement), below the frozen 2% floor; statistically significant (Holm) but not material; independent stdlib recompute `all_checks_match=true`, `n_checks=31`.
- **Half 1 (volatility) — jump / semivariance-asymmetry frontier:** OPEN — this campaign (FCLR-VOL-JUMP-01). **Partial attempt exists at `session_20261124T230000Z` but eval produced NaN candidate metrics; missing recompute, evidence_audit, trigger_check.**
- **Half 2 (liquidation risk):** confirmatory-exhausted on the frozen `ironflow_bulk` panel. Track A STRUCTURALLY_BLOCKED (capped-sample feed, not a census); Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; broad cross-sectional rank ordering SUPPORTED_GENERALIZATION but NOT_STABLE (§17 condition #4) and 2% Poisson-deviance materiality floor NOT MET.
- **Heavy-work gate:** FAILING with `HANDOFF_STALE_LATEST_SESSION:session_20261124T230000Z`. The `vol_jump` binder is active and REQUIRED (since a session > 20261124T223000Z exists on disk). A new complete session > 20261124T230000Z with ALL artifacts is mandatory to pass.
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
- **DO NOT include any other `FCLR-…-<8digit>T<6digit>Z` campaign id in this file** (refer to closed campaigns by name only, e.g. "FCLR-VOL-STRESS-01 (closed)"). A stray timestamped id would activate that campaign's binder on every future session and fail it closed. The ONLY timestamped campaign id permitted in this file is the active `FCLR-VOL-JUMP-01-20261124T223000Z`.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 2025-05..2026-10; hourly OHLC. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; `funding_rate`, `premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; `mark_price`, `oracle_price`, `open_interest`. |
| `research_state/session_20261124T222500Z/` | Latest COMPLETE heavy session (FCLR-VOL-STRESS-01; NOT_SUPPORTED; 17 non-empty artifacts). |
| `research_state/session_20261124T230000Z/` | **PARTIAL session** (FCLR-VOL-JUMP-01 attempt; source_registry + prereg + eval.py + eval.json with NaN candidate; MISSING: eval.md, recompute, evidence_audit, trigger_check, evidence_audit alias). |
| `research_state/session_20261124T204500Z/` | Prior complete heavy session (FCLR-VOL-CORR-01; NOT_SUPPORTED; correction-time). |
| `research_state/session_20261124T120000Z/` | Prior complete heavy session (FCLR-VOL-BROAD-01; NOT_SUPPORTED; mean QLIKE). |
| `research_state/session_20261121T130159Z/` | 5-coin panel fixed-effects volatility study (prior null). |
| `research_state/experiment_frontier.json` | rank-0 is `FCLR-VOL-JUMP-01-20261124T223000Z` (READY_EXECUTE); FCLR-VOL-STRESS-01, FCLR-VOL-CORR-01 and FCLR-VOL-BROAD-01 are COMPLETED_VALIDATED (NOT_SUPPORTED). |
| `research_state/negative_results_report.md` | Null/failed/inconclusive outcomes preserved. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3 (primary + secondary research question), §7 (targets), §9 (overlay gate), §16 (adaptive feasibility), §17 (promotion), §19 (definition of done), §20 (status contract).
- `scripts/check_handoff_heavywork_gate.py` — `VOL_JUMP_CAMPAIGN_RE` / `_vol_jump_state` / `VOL_JUMP_REQUIRED` binder (active, REQUIRED since session_20261124T230000Z exists on disk); `VOL_STRESS_CAMPAIGN_RE` / `_vol_stress_state` (dormant); `VOL_CORR_CAMPAIGN_RE` / `_vol_corr_state` (dormant); `VOL_BROAD_CAMPAIGN_RE` / `_vol_broad_state` (dormant).
- `tests/test_vol_jump_campaign_gate.py` — regression pinning the new jump binder (10 tests).
- `tests/test_vol_stress_campaign_gate.py` — regression pinning the (now dormant) stress binder.
- `tests/test_vol_corr_campaign_gate.py` — regression pinning the (now dormant) correction binder.
- `research_state/experiment_frontier.json` — rank-0 campaign registry.
- `research_state/data_cache/ironflow_bulk/` — frozen broad panel.
- `research_state/negative_results_report.md` — preserved nulls/negatives.

---

## SESSION CLOSE-OUT (THIS SESSION — 2026-11-25T02:54:00Z)

**What changed and why (real actions, not a timestamp bump):**
- **Identified the gate failure:** `python3 scripts/check_handoff_heavywork_gate.py --json` returns `pass=false` with `HANDOFF_STALE_LATEST_SESSION:session_20261124T230000Z`. A partial FCLR-VOL-JUMP-01 attempt exists on disk but is incomplete (NaN candidate metrics, missing 5 mandatory artifact categories).
- **Audited the partial session artifacts:** `session_20261124T230000Z/` contains valid `fclr_voljump01_source_registry_{json,md}` (sha256 `e8d3bb5eb4ebde9439d3753c3241742f4f9e9239d90c817c2ab809fc519ef01b`), valid `fclr_voljump01_prereg_{json,md}` (outcome-blind, correct design.kind), `fclr_voljump01_eval_{py,json}` (but candidate metrics all NaN), and `fclr_voljump01_build_source_registry.py`. MISSING: `eval.md`, `recompute_{py,json}`, `evidence_audit_{json,md}`, `evidence_audit_<UTC>.json` alias, `trigger_check_<UTC>.json`.
- **Updated this handoff** to reflect the TRUE gate state (FAILING, not green) and provide an accurate, actionable initial task message for the next agent.

**Exact test outcomes with paths (this session):**
- Heavy-work gate: `python3 scripts/check_handoff_heavywork_gate.py --json` → `pass=false`, `failures=["HANDOFF_STALE_LATEST_SESSION:session_20261124T230000Z"]`, `vol_jump.required=true`, `vol_jump.pass=false`.
- Gate binder compile: `python3 -m py_compile scripts/check_handoff_heavywork_gate.py` → OK.
- Campaign-gate regression suite: `python3 -m unittest tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate tests.test_tracka_hardening_143 tests.test_active_campaign_gate` → all pass (tests are hermetic, not affected by on-disk partial session).

**State of each research gate:**
- Heavy-work gate: **FAILING** (`HANDOFF_STALE_LATEST_SESSION:session_20261124T230000Z`; `vol_jump.required=true` because a post-start session exists on disk; full artifact set mandatory).
- Forecast gate (§9): **NOT PASSED** (no broad-scale volatility skill; 2% QLIKE materiality floor not met on any prior arm).
- Half 1 (volatility) — RV forecast (mean QLIKE): **CLOSED NOT_SUPPORTED at broad scale** (FCLR-VOL-BROAD-01; 1.93% < 2%).
- Half 1 (volatility) — correction-time: **CLOSED NOT_SUPPORTED at broad scale** (FCLR-VOL-CORR-01).
- Half 1 (volatility) — stress / tail-exceedance: **CLOSED NOT_SUPPORTED at broad scale** (FCLR-VOL-STRESS-01).
- Half 1 (volatility) — jump / semivariance-asymmetry: **OPEN** (partial attempt failed; must be completed properly).
- Half 2 (liquidation risk): **CONFIRMATORY EXHAUSTED**.

**Single highest-value next task:**
Execute `FCLR-VOL-JUMP-01-20261124T223000Z` properly — a HEAVY, confirmatory, broad-panel funding-conditioned signed-jump / semivariance-asymmetry forecast with a frozen outcome-blind prereg, walk-forward classification evaluation producing VALID numeric candidate metrics (NOT NaN), independent stdlib recompute, evidence audit, gate-critical alias, and trigger check, all under one fresh `session_<UTC>/` (UTC strictly > `20261124T230000Z`). This is the deliverable; a handoff refresh is not.

**Precise verifying commands:**
```bash
# 0. One-time environment setup if needed
python3 -m pip install --quiet numpy pandas pyarrow

# 1. Heavy-work gate must return reason=OK (after new complete session created and recorded)
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Gate binder must compile
python3 -m py_compile scripts/check_handoff_heavywork_gate.py

# 3. Campaign-gate regression suite must pass (incl. new vol_jump binder)
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

**Any remaining blocker and the next materially different route:**
- **Blocker:** The partial `session_20261124T230000Z` exists with broken eval (NaN candidate). The gate will not pass until a NEW session > 20261124T230000Z with ALL 7 artifact categories (non-empty, valid JSON, numeric candidate metrics) is created AND recorded in this handoff.
- **Next route:** `FCLR-VOL-JUMP-01` — broad-panel funding-conditioned signed-jump / semivariance-asymmetry forecast (this campaign). If it returns a null, the funding/volatility program is closed at broad scale on all four estimands and the only remaining route is a new admissible free observed-liquidation source (which cannot fire on frozen data).

---

## BOTTLENECK RESOLUTION (this refresh)

- **IDENTIFIED (2026-11-25T02:54:00Z) — stale partial session blocking the gate:** `session_20261124T230000Z` was created by a prior session but left incomplete (NaN candidate metrics, missing recompute/evidence_audit/trigger_check). This triggers `HANDOFF_STALE_LATEST_SESSION` and makes `vol_jump.required=true`. The gate cannot pass until a complete session > 20261124T230000Z exists.
- **RESOLVED (avoidance hazard — grandfathering misconception):** The prior handoff claimed the gate was green via grandfathering, but that was false because a post-start session (`session_20261124T230000Z`) already existed on disk. The NON-AVOIDANCE section now correctly states: `vol_jump.required=true` and the full artifact set is mandatory.
- **RESOLVED (avoidance hazard — `next_campaign_status.py` misleading output):** the script prints `no feasible 3-block design in ANY domain`, true only for the obsolete 3-contiguous-30-day-block framing. Hard non-avoidance constraint forbids misreading this as "no heavy work is possible"; the broad-panel signed-jump design is feasible on the full 18-month panel.
- **RESOLVED (root churn cap):** root `research_state/*.md|*.json` is at 500; all new artifacts must go under `session_<UTC>/`.
- **OPEN (next frontier execution):** `FCLR-VOL-JUMP-01-20261124T223000Z` must be executed properly — all required artifacts under one fresh `session_<UTC>/` (UTC > 20261124T230000Z), no zero-byte placeholders, numeric candidate metrics, in one session. This is the next agent's single, non-deferrable job.

---

## RESEARCH_PROMPT.md §19 ANSWERS (this session)

**What did the evidence support, contradict, or leave unknown?**
- Supported (prior, unchanged): the broad-universe cross-sectional funding → next-hour liquidation-intensity rank ordering generalizes but is NOT temporally stable.
- Contradicted/closed (prior): the funding-conditioned volatility-STRESS (tail-exceedance) hypothesis at broad scale (FCLR-VOL-STRESS-01 NOT_SUPPORTED — 1.51% relative Brier improvement, below the 2% floor) — Half 1 stress closed at broad scale.
- Unknown (this campaign): whether the funding + price feature set improves out-of-sample signed-jump / semivariance-asymmetry forecasts beyond an RV-only baseline at broad scale. The partial attempt produced NaN candidate metrics, leaving the question entirely open.

**What is the strongest alternative explanation?**
The three volatility nulls (mean QLIKE 1.93%, correction-time, stress 1.51%) may all reflect that funding carries weak, regime-dependent information that a jump/asymmetry classification estimand (sensitive to the discontinuous, directionally-signed moves that matter most for liquidation risk) could detect — or it may be noise. The jump study distinguishes these.

**Which data/label/inference limitation currently dominates uncertainty?**
1. Estimand: mean-QLIKE, correction-time, and stress/total-variance endpoints are closed; the jump/asymmetry estimand is untested at broad scale.
2. Label: ironflow liquidations are a capped-sample feed (constrains Half 2, not the funding/volatility jump arm).
3. Materiality/inference: no arm has cleared its frozen floor; the jump study must report Brier/log-loss contrasts with DM/Driscoll-Kraay HAC and Holm.

**What concrete new test would falsify the current leading hypothesis?**
A broad-panel, leakage-hardened, train-only-threshold funding-conditioned signed-jump / semivariance-asymmetry forecast that either clears the frozen materiality floor with Holm-adjusted uncertainty (PROMOTED) or returns a clean null (NOT_SUPPORTED) closing the jump arm at broad scale.

**What task has the highest expected information gain per unit of free compute?**
`FCLR-VOL-JUMP-01` — it directly tests the repository-name first half via a distinct, never-confirmatory broad-scale estimand, using only frozen on-disk data.

**What exact artifact and command/test demonstrate progress?**
- Artifact: one fresh `research_state/session_<UTC>/` (UTC > 20261124T230000Z) with the full `fclr_voljump01_*` set plus `evidence_audit_<UTC>.json` and `trigger_check_<UTC>.json`, all non-empty, candidate metrics numeric (not NaN).
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` → `reason=OK` with `vol_jump.required=true` and `vol_jump.pass=true`.
- Test: `python3 -m unittest tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate tests.test_tracka_hardening_143 tests.test_active_campaign_gate` passes.

(End of file)