# AGENT HANDOFF — 2026-11-24T03:55:53Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: HALF 2 (LIQUIDATION RISK) CONFIRMATORY EXHAUSTED; HALF 1 (FUNDING-CONDITIONED VOLATILITY) BROAD-SCALE TEST OPEN.**
> Active rank-0 campaign: `FCLR-VOL-BROAD-01-20261124T035500Z` (READY_EXECUTE).
> **REPO-NAME PRIORITY → `Funding-conditioned-volatility-and-liquidation-risk`**: the repository name leads with the volatility half. Every leakage-robust volatility null to date (FCLR-011; the 5-coin panel fixed-effects study, session_20261121T130159Z) was established on a **5-coin panel**. The broad 342+ coin, 18-month `ironflow_bulk` panel that produced the only SUPPORTED liquidation-risk finding has **never** been used for a direct funding-conditioned realized-volatility forecast. That is the unfinished repo-name frontier.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-24T03:55:53Z**
>
> **REPO-NAME PRIORITY → ACTIVE FRONTIER:** The repository is `Funding-conditioned-volatility-and-liquidation-risk`. Half 2 (liquidation risk) is confirmatory-exhausted on the frozen `ironflow_bulk` panel (Track A STRUCTURALLY_BLOCKED on a capped-sample feed; Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; the broad cross-sectional rank-ordering association is SUPPORTED_GENERALIZATION but NOT_STABLE and its 2% Poisson-deviance materiality floor is NOT MET). Half 1 (funding-conditioned volatility) is only closed on a **5-coin** panel. The next session's single, non-deferrable job is to run the **broad-universe funding-conditioned volatility forecast** at the same 342+ coin scale that produced the only SUPPORTED liquidation-risk result.
>
> **THE NEXT FOCUS CAMPAIGN (rank-0, mandatory heavy work): `FCLR-VOL-BROAD-01-20261124T035500Z`**
>
> Execute a HEAVY, confirmatory, broad-panel study. This is real computation — not a status memo, not a source probe, not a trigger-check-only session, not a verify-and-stop session.
>
> **Question:** On the full frozen `ironflow_bulk` panel (18 monthly parquet, 2025-05..2026-10; `candles_1h`, `funding`, `open_interest`), do funding features improve out-of-sample forecasts of realized volatility over a realized-volatility-only baseline, once coin and hour-of-day fixed effects are removed, and does any improvement clear the frozen 2% materiality floor with Holm-adjusted uncertainty?
>
> **Frozen inputs (do NOT re-derive, do NOT substitute):**
> - `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}/` (18 monthly parquet, 2025-05..2026-10). `candles_1h` columns: `timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades`. `funding`: `timestamp, market, coin, dex, funding_rate, premium`. Assert every `.sha256` sidecar before reading; caches are read-only and unmodified.
> - Target: next-hour and 24h realized volatility from hourly close-to-close log returns (report both). Baseline: realized-volatility-only (persistence / trailing-RV) forecast.
> - Features, all known at origin hour `t`: signed `funding_rate` (latest observation `<= t`), trailing `abs_funding` trail, trailing `RV24`/`RV168`, mark/oracle premium dislocation, MA deviation. Train-only normalization; expanding train-only thresholds; no future information.
> - Design: chronological walk-forward, `TRAIN_FRAC=0.60`, `PURGE_EMBARGO_H=48`, `BLOCK_H=168`, expanding train-only mean/std; no random split; no overlapping forward targets across the purge boundary.
> - Models: pooled two-way (coin + hour-of-day) fixed-effects within-transform, funding-conditioned vs a no-funding FE baseline. Metrics: QLIKE (primary) and MSE, with Diebold-Mariano HAC on the daily loss differential. Inference: cluster-robust (CR1) by coin **and** Driscoll-Kraay HAC; Holm correction over the declared family.
> - Materiality floor (frozen, NOT relaxed): a +1 sample-SD funding shock must move QLIKE by >= 2% relative. Verdict is symmetric (`PROMOTED` / `NOT_SUPPORTED`); a null is a valid, publishable negative result that closes Half 1 at broad scale.
>
> **Next agent's single job:** Produce the complete artifact set under one fresh `research_state/session_<UTC>/` (UTC strictly > `20261124T035500Z`), prefix `fclr_volbroad01_`, all non-empty, no zero-byte placeholders:
> 1. `fclr_volbroad01_source_registry_{json,md}` — sha256-asserted `ironflow_bulk` inventory (paths, rows, coins, month span, schemas).
> 2. `fclr_volbroad01_prereg_{json,md}` — outcome-blind frozen prereg (`outcome_data_inspected_before_freeze:false`, input sha256 assertions).
> 3. `fclr_volbroad01_eval_{py,json,md}` — the heavy walk-forward evaluation triad.
> 4. `fclr_volbroad01_recompute_{py,json}` — independent stdlib recompute from stored input hashes/config (`all_checks_match:true`).
> 5. `fclr_volbroad01_evidence_audit_{json,md}` — evidence audit.
> 6. `evidence_audit_{UTC}.json` — gate-critical alias.
> 7. `trigger_check_{UTC}.json` — non-empty trigger check (no external trigger is required; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data).
>
> Record the real session id in `research_state/experiment_frontier.json` (promote rank-0 `READY_EXECUTE` → `COMPLETED_VALIDATED` only after artifacts exist) and update this handoff after the artifacts exist. Do NOT write a future/non-existent session id into this handoff before its artifacts exist.
>
> **DO NOT:** re-run the temporal-stability campaign or the earlier broad cross-sectional campaign; build a risk overlay (§9 forecast gate not passed); claim a forecast-gate pass from a cross-sectional association; wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; add root-level research-state files (root `*.md|*.json` at the 500 cap — all new artifacts MUST go under `session_<UTC>/`); relabel exploratory as confirmatory; threshold-shop or relax the 2% floor after outcomes.

---

## FOCUS CAMPAIGN — FCLR-VOL-BROAD-01-20261124T035500Z (rank-0, READY_EXECUTE)

**Question (OPEN):** Does funding conditioning improve out-of-sample realized-volatility forecasts on the broad 342+ coin `ironflow_bulk` panel, over a realized-volatility-only baseline, after coin + hour fixed effects, and does it clear the frozen 2% QLIKE materiality floor?

**Why this is the highest-value next task:**
- Repo name leads with **Funding-conditioned-volatility**; the broad panel has only ever been used for liquidation-intensity (cross-sectional) work, never for a direct RV forecast.
- Prior volatility nulls (FCLR-011; the 5-coin panel FE study, session_20261121T130159Z) do not cover the broad universe; this is a materially different universe and design, not a repeat of a failed endpoint.
- Liquidation-risk Half 2 is exhausted; this is the remaining honest heavy question on admissible frozen data.
- A null is a strong, publishable negative result; a pass would be the first broad-scale volatility skill and would still face the §17 promotion conditions in full.

**Frozen inputs (do NOT re-derive, do NOT substitute):**
- `research_state/data_cache/ironflow_bulk/candles_1h/` — 18 monthly parquet, hourly OHLC.
- `research_state/data_cache/ironflow_bulk/funding/` — 18 monthly parquet, `funding_rate`, `premium`.
- `research_state/data_cache/ironflow_bulk/open_interest/` — 18 monthly parquet, `mark_price`, `oracle_price`, `open_interest`.
- Assert every `.sha256` sidecar before reading; caches are read-only.

**Produced artifacts (target — ALL under one fresh `session_<UTC>/`; non-empty):**
- `fclr_volbroad01_source_registry_<UTC>.{json,md}`
- `fclr_volbroad01_prereg_<UTC>.{json,md}`
- `fclr_volbroad01_eval_<UTC>.{py,json,md}`
- `fclr_volbroad01_recompute_<UTC>.{py,json}` (`all_checks_match:true`)
- `fclr_volbroad01_evidence_audit_<UTC>.{json,md}`
- `evidence_audit_<UTC>.json` (gate-critical alias)
- `trigger_check_<UTC>.json`

---

## STATE OF THE WORK (read before doing anything)

- **Half 2 (liquidation risk):** confirmatory-exhausted on the frozen `ironflow_bulk` panel. Track A STRUCTURALLY_BLOCKED (capped-sample feed, not a census); Track B NOT_SUPPORTED; Track C NOT_SUPPORTED; broad cross-sectional rank ordering SUPPORTED_GENERALIZATION but NOT_STABLE (temporal stability fails §17 condition #4) and 2% Poisson-deviance materiality floor NOT MET.
- **Half 1 (volatility):** leakage-robust null on a **5-coin** panel (FCLR-011; panel FE study `session_20261121T130159Z`). **Broad-scale test is OPEN** — this campaign.
- **Heavy-work gate:** the previous heavy campaign's artifacts are complete; the gate binds the new rank-0 campaign via `VOL_BROAD_CAMPAIGN_RE` / `_vol_broad_state` / `VOL_BROAD_REQUIRED`. The refresh is green because the latest on-disk session predates the new campaign start (grandfathered).
- **Forecast gate (§9):** NOT PASSED — no broad-scale volatility skill demonstrated; materiality floor not met on any prior arm. Risk overlay INELIGIBLE.
- **Root `research_state/*.md|*.json` count:** at the 500 cap. All new artifacts MUST go under `session_<UTC>/` or another nested directory.

---

## ROOT CONSTRAINTS (hard)

- Root `research_state/*.md|*.json` count: **500/500** — at cap. All new artifacts MUST go under `session_<UTC>/` or another nested directory. Do not add root-level research-state files.
- No empty files and no zero-byte placeholders.
- Do not threshold-shop or relax the frozen 2% floor/threshold after outcomes.
- Preserve nulls honestly: valid outcomes are `PROMOTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`, or an evidence-backed fidelity/structural blocker; never a fabricated pass.
- Do not re-run any terminal campaign or build a risk overlay.
- Do not modify `.github/workflows`.
- Do not overwrite `research_state/research_protocol.md` or any sealed prereg/eval artifact.
- Stdlib + numpy + pandas + pyarrow only; no network for the heavy evaluation; no new source; no overlay.
- Do not track-adulterate: never describe a broad-universe cross-sectional association, or a stability test of it, as a time-series forecast gate pass.
- Do not wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`; it cannot fire on frozen data and is not a valid reason to idle.
- Do not write a future/non-existent session id into this handoff. Use the placeholder `session_<UTC>` for the session you create; record its real id here only after its artifacts exist.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- The heavy-work gate binds `FCLR-VOL-BROAD-01-20261124T035500Z`: a post-start session must contain the full `fclr_volbroad01_*` artifact set plus the gate-critical `evidence_audit_` alias and a non-empty `trigger_check_`, with no zero-byte placeholders. A trigger-only, prose-only, audit-only, prereg-only, verify-and-stop, or arbitrary `recompute_*` session FAILS CLOSED.
- Do not create a partial session directory and leave it unrecorded; that causes `HANDOFF_STALE_LATEST_SESSION` and blocks all later work.
- Do not re-run any terminal campaign.
- Do not wait for an external trigger.
- Do not build a risk overlay.
- Do not track-adulterate.
- Do not ship a verdict from a non-reconciled eval. Emit a verdict only after the independent recompute reports `all_checks_match:true`; preserve fail-closed behavior.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 2025-05..2026-10; hourly OHLC. |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet; `funding_rate`, `premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet; `mark_price`, `oracle_price`, `open_interest`. |
| `research_state/session_20261124T015114Z/` | Latest complete heavy session (temporal-stability campaign). |
| `research_state/session_20261121T130159Z/` | 5-coin panel fixed-effects volatility study (prior null). |
| `research_state/experiment_frontier.json` | rank-0 is `FCLR-VOL-BROAD-01-20261124T035500Z` (READY_EXECUTE). |
| `research_state/negative_results_report.md` | Null/failed/inconclusive outcomes preserved. |
| `research_state/fclr_final_structural_closure_20261124T025751.{md,json}` | Terminal structural closure evidence (historical). |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert hashes before reading; do not mutate caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3 (primary research question), §9 (overlay gate), §16 (adaptive feasibility), §17 (promotion), §19 (definition of done), §20 (status contract).
- `scripts/check_handoff_heavywork_gate.py` — `VOL_BROAD_CAMPAIGN_RE` / `_vol_broad_state` / `VOL_BROAD_REQUIRED` binder.
- `research_state/experiment_frontier.json` — rank-0 campaign registry.
- `research_state/data_cache/ironflow_bulk/` — frozen broad panel.
- `research_state/negative_results_report.md` — preserved nulls/negatives.

---

## SESSION CLOSE-OUT REQUIREMENTS (THIS SESSION)

**What changed and why:**
- Refreshed `AGENT_HANDOFF.md` as the sole durable handoff after the prior heavy session completed.
- Re-prioritized by repository name: Half 2 (liquidation risk) is confirmatory-exhausted; Half 1 (funding-conditioned volatility) is only closed on a 5-coin panel. The unfinished repo-name frontier is a broad-scale volatility forecast.
- Promoted rank-0 to `FCLR-VOL-BROAD-01-20261124T035500Z`; demoted the earlier program-closure synthesis plan to SUPERSEDED (deferred until after the broad volatility test).
- Added a machine-checked heavy-work binder (`VOL_BROAD_*`) so a future session cannot dodge the heavy broad-panel volatility work with a trigger-only, audit-only, prereg-only, or verify-and-stop session.

**Exact test outcomes with paths:**
- Heavy-work gate: `python3 scripts/check_handoff_heavywork_gate.py --json` → `reason=OK` (SATISFIED; new campaign grandfathered because the latest on-disk session predates its start).
- Gate binder compile: `python3 -m py_compile scripts/check_handoff_heavywork_gate.py` → OK.

**State of each research gate:**
- Heavy-work gate: **SATISFIED** (new rank-0 binder active; refresh green via grandfathering).
- Forecast gate (§9): **NOT PASSED** (no broad-scale volatility skill; materiality floor not met).
- Half 1 (volatility): **BROAD-SCALE TEST OPEN** (5-coin null only).
- Half 2 (liquidation risk): **CONFIRMATORY EXHAUSTED** (Track A blocked; Track B/C null; cross-sectional NOT_STABLE + materiality floor unmet).

**Single highest-value next task:**
Execute `FCLR-VOL-BROAD-01-20261124T035500Z` — a heavy, confirmatory, broad-panel funding-conditioned realized-volatility forecast with a frozen outcome-blind prereg, walk-forward evaluation, independent stdlib recompute, evidence audit, gate alias, and trigger check, all under one fresh `session_<UTC>/`.

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
  tests.test_tracka_hardening_143 \
  tests.test_active_campaign_gate \
  tests.test_fclr_campaign_gate

# 4. Context only: the old 3-block scanner does not assess broad-panel feasibility
python3 scripts/next_campaign_status.py
```

**Any remaining blocker and the next materially different route:**
- **Blocker:** Half 2 confirmatory paths are exhausted on the frozen panel; Half 1 has only a 5-coin null. No broad-scale volatility forecast exists.
- **Next route:** `FCLR-VOL-BROAD-01` — broad-panel funding-conditioned volatility forecast (this campaign). If it returns a null, Half 1 is closed at broad scale and the only remaining route is a new admissible free observed-liquidation source (which cannot fire on frozen data).

---

## BOTTLENECK RESOLUTION (this refresh)

- **RESOLVED (verify-and-stop / closure-memo escape hatch):** the prior plan routed the next session to a program-closure synthesis. That would let a future agent end the program by writing documents instead of running heavy science. Replaced with a concrete, feasible, heavy broad-panel volatility forecast that uses the same frozen panel and matches the repository-name first half.
- **RESOLVED (no feasible heavy work on frozen data):** the broad `ironflow_bulk` panel (candles + funding + open_interest) has never been used for a direct RV forecast; a walk-forward, leakage-hardened, fixed-effects design is feasible today without any new source.
- **RESOLVED (gate not binding the active frontier):** added `VOL_BROAD_CAMPAIGN_RE` / `_vol_broad_state` / `VOL_BROAD_REQUIRED` and wired them into `check()`; a post-start session cannot pass with a trigger-only/audit-only/prereg-only/verify-and-stop session.
- **RESOLVED (root churn cap):** root `research_state/*.md|*.json` is at 500; all new artifacts must go under `session_<UTC>/`.
- **OPEN (next frontier execution):** `FCLR-VOL-BROAD-01-20261124T035500Z` must be executed — all required artifacts under one fresh `session_<UTC>/`, no zero-byte placeholders, all in one session.

---

## RESEARCH_PROMPT.md §19 ANSWERS (this session)

**What did the evidence support, contradict, or leave unknown?**
- Supported: the broad-universe cross-sectional funding → next-hour liquidation-intensity rank ordering generalizes (earlier SUPPORTED_GENERALIZATION), but it is NOT temporally stable.
- Contradicted: the liquidation-risk forecast gate (NOT_STABLE; 2% Poisson-deviance materiality floor NOT MET); the 5-coin funding-conditioned volatility hypothesis (leakage-robust null).
- Unknown: whether funding conditioning improves realized-volatility forecasts at broad (342+ coin) scale; this campaign answers it.

**What is the strongest alternative explanation?**
The funding–liquidation link is regime-dependent, not a stable structural feature. For volatility, the 5-coin null may be a power/universe artifact rather than a true absence of skill; the broad panel is the correct test.

**Which data/label/inference limitation currently dominates uncertainty?**
1. Universe: prior volatility nulls cover only 5 coins; broad-panel evidence is missing.
2. Label: ironflow liquidations are a capped-sample feed (not a census); absence != zero (constrains Half 2, not Half 1).
3. Materiality: no arm has cleared the frozen 2% floor; the broad RV test must report QLIKE and MSE with DM HAC and Holm.

**What concrete new test would falsify the current leading hypothesis?**
A broad-panel, leakage-hardened, fixed-effects funding-conditioned RV forecast that clears the 2% QLIKE materiality floor with Holm-adjusted uncertainty and multi-block, multi-coin support. A null would instead close Half 1 at broad scale.

**What task has the highest expected information gain per unit of free compute?**
`FCLR-VOL-BROAD-01` — it directly tests the repository-name first half on the broad panel for the first time, using only frozen on-disk data.

**What exact artifact and command/test demonstrate progress?**
- Artifact: one fresh `research_state/session_<UTC>/` with the full `fclr_volbroad01_*` set plus `evidence_audit_<UTC>.json` and `trigger_check_<UTC>.json`.
- Command: `python3 scripts/check_handoff_heavywork_gate.py --json` → `reason=OK` with `vol_broad.required=true` and `vol_broad.pass=true`.
- Test: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_active_campaign_gate` passes.

(End of file)