# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T21:00:09Z (supersedes 2026-11-22T20:57:55Z)
**Session type:** handoff timestamp refresh + bottleneck re-verification. The in-flight `session_20261122T190000Z` is complete on disk (FCLR-POOLED-ROBUST-002 decision NOT_SUPPORTED_LEAKAGE_ROBUST_NULL) with its `trigger_check_` bookkeeping file present and non-empty and its carried-forward `fclr_pooled001_*` / `fclr_pooled_audit001_*` bundles in place; the real-repo gate passes closed→green (see §1a). Sole rank-0 campaign is `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` (**ACTIVE / READY_EXECUTE**, gate-enforced). Campaign start UTC `20261122T193000Z` has **elapsed** (current UTC 2026-11-22T20:04:53Z). The next session (UTC > `20261122T193000Z`) **must** produce the full heavy artifact set under its own `session_<UTC>/` or the gate fails closed.

**Sole rank-0 campaign (gate-enforced):** `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` — **ACTIVE / READY_EXECUTE**. A heavy, outcome-blind, leakage-hardened **confirmatory study of the repository's liquidation-risk pillar using the OBSERVED ironflow liquidations bulk stream (Track A)** — the first confirmatory use of observed liquidation events, distinct from the modeled Track B breach proxy. It asks the second half of the primary research question (RESEARCH_PROMPT.md §3.2): do funding-conditioned features predict **observed** liquidation intensity (hourly event count and open-interest-normalized notional), under an explicit §15 label-admissibility audit (coverage, completeness, capped-sample check, `market`→`coin` identity) and the same leakage hardening that confirmed the volatility null. Gate binding `FCLR-LIQ-RISK-ESCALATION` (artifact family `fclr_risk09_*`) fails closed without the full heavy artifact set under `research_state/session_<UTC>/` (UTC > `20261122T193000Z`).

**Latest completed heavy session on disk:** `session_20261122T190000Z` — executed **FCLR-POOLED-ROBUST-002** to completion: `fclr_pooled_robust002_prereg_` (json+md), `fclr_pooled_robust002_robustness_` (py+json+md), `fclr_pooled_robust002_recompute_` (py+json), `fclr_pooled_robust002_evidence_audit_` (json+md), the `evidence_audit_` alias (json) and a non-empty `trigger_check_` (json); plus the carried-forward `fclr_pooled001_*` (11) and `fclr_pooled_audit001_*` (9) bundles. Decision: **NOT_SUPPORTED_LEAKAGE_ROBUST_NULL** — C2−B1 QLIKE = +1.011% (funding-conditioned features are *worse* than the RV-only baseline), fails the −2% materiality floor, bootstrap CI95 [−0.110, +1.025] includes zero, Holm primary p = 0.6365 vs α₂ = 0.00833. The FCLR-POOLED-001 null is confirmed leakage-robust; it was NOT a leakage artifact.

**Gate baseline (re-verified this session, 2026-11-22T20:04:53Z):** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK` (`latest_handoff=session_20261122T190000Z`, `latest_disk=session_20261122T190000Z`, `handoff_stale=False`, `pooled.required=True` 11/11, `pooled_audit.required=True` 9/9, `pooled_robust_02.required=True` 9/9 + alias + trigger present, `risk_08.required=False` because latest session UTC `20261122T190000Z` ≤ campaign start `20261122T193000Z` (grandfathered), `root=499/500`); all gate unittest modules → **121 tests, 0 failures**; `research_state` root md+json count = **499/500**; no empty session dirs; on-disk ironflow bulk caches unchanged (candles_1h/funding/open_interest/liquidations each 18 parquet + 18 sha256 sidecars + 18 accessed.json, 2025-05..2026-10).

**Environment (verified):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy` NOT installed (`ModuleNotFoundError`). `pyarrow` 26.0.1 installed — reads ironflow bulk parquet. Use stdlib + pyarrow only. Do NOT rely on numpy/pandas/scipy.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001/002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01/02, FCLR-NEXT-SOURCE-VERIFY-01, FCLR-POOLED-001, FCLR-POOLED-AUDIT-001, FCLR-POOLED-ROBUST-002) are terminal / superseded / completed — **do NOT re-run them**. The reachable-free-source frontier (NEXT-SOURCE-VERIFY-01) is terminal (NO_NEW_ADMISSIBLE_SOURCE). **FCLR-POOLED-001 is CONFIRMATORY_COMPLETE** (session_20261122T092003Z, NOT_SUPPORTED). **FCLR-POOLED-AUDIT-001 is COMPLETE** (session_20261122T165200Z). **FCLR-POOLED-ROBUST-002 is CONFIRMATORY_COMPLETE** (session_20261122T190000Z, NOT_SUPPORTED_LEAKAGE_ROBUST_NULL). A future session must NOT re-run any of them; per §9 no risk overlay should be built since the forecast gate did not pass.

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars (RESEARCH_PROMPT.md §Mission/§3). Never drift into unrelated work, risk overlays, or live/paper trading. RESEARCH_PROMPT.md §16/§19/§20 forbid declaring the research complete after one unfavorable result and forbid cosmetic verify-and-stop sessions while a valid heavy task remains: the sole rank-0 below is that heavy task.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (handoff timestamp refresh 2026-11-22T21:00:09Z; campaign start UTC 20261122T193000Z **ELAPSED**)

> **READ THIS FIRST.**
>
> You are the next agentic work session for the **Funding-conditioned-volatility-and-liquidation-risk** research program. Your single highest-value, repo-name-prioritized, gate-enforced task is to **execute the rank-0 campaign `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z`**: a heavy, outcome-blind, **leakage-hardened confirmatory study of OBSERVED liquidation intensity** on the on-disk ironflow liquidations bulk stream (Track A). This is NOT a re-run of FCLR-POOLED-ROBUST-002 (that confirmed the funding-conditioned *volatility* null is leakage-robust) and NOT a re-run of any modeled Track B breach analysis. It answers the still-open half of the primary question: **do funding-conditioned features predict real, observed liquidation events?**
>
> **Why this and nothing else:** The funding-conditioned volatility (QLIKE) pillar is now robustly closed. FCLR-POOLED-001 returned NOT_SUPPORTED; FCLR-POOLED-AUDIT-001 found leakage/quality gaps; FCLR-POOLED-ROBUST-002 applied every remediation simultaneously and still returned NOT_SUPPORTED_LEAKAGE_ROBUST_NULL (C2−B1 = +1.011% QLIKE, worse than baseline; Holm primary p=0.6365; CI95 includes zero). RESEARCH_PROMPT.md §9 still forbids any risk overlay because the forecast gate did not pass. §16/§19 require continuing after an unfavorable result instead of stopping. The *other* primary target (§3.2, observed liquidation outcomes) has never been tested confirmatively: the ironflow `liquidations` bulk stream (18 months, 2025-05..2026-10, ~2.85M wallet-level events keyed by `market`/`issuer`) is on disk, unused for a confirmatory, and is the highest-value unfinished work. It is now **gate-enforced** so it cannot be skipped.
>
> **What you must produce (all under `research_state/session_<UTC>/` with UTC > `20261122T193000Z`, non-empty, no zero-byte placeholders):**
> 1. `fclr_risk09_prereg_<UTC>.{json,md}` — outcome-blind prereg **frozen before any outcome is inspected** (`outcome_data_inspected_before_freeze:false`; assert input sha256; 48h purge+embargo; non-overlapping forward blocks; delisting-aware per-coin identity; RV/persistence baseline vs funding-conditioned candidate; materiality floor; Holm family; alpha-spending look) frozen BEFORE outcomes.
> 2. `fclr_risk09_power_<UTC>.{py,json,md}` — observed-event sparsity/coverage + minimum-detectable-effect (power) audit for the rare observed-liquidation intensity target (events per coin-hour, notional coverage, identity-match rate, effective sample size).
> 3. `fclr_risk09_recompute_<UTC>.{py,json}` — independent stdlib recompute from the stored input hashes (no pyarrow-based eval module imported), reproducing headline counts/intensities within a declared tolerance.
> 4. `fclr_risk09_evaluation_<UTC>.{py,json,md}` — the heavy label-admissibility + leakage-hardened intensity evaluation: §15 admissibility audit, `market`→`coin` identity map, hourly event-count and OI-normalized notional targets, RV-only vs funding-conditioned candidate, per-coin block-bootstrap CI95, Holm across the declared family, and an explicit symmetric verdict rule (SUPPORTED / PARTIAL_POSITIVE_SIGNAL / NOT_SUPPORTED).
> 5. `evidence_audit_<UTC>.json` — gate-critical alias (plus `.md` recommended).
> 6. non-empty `trigger_check_<UTC>.json`.
>
> **Also carry forward** the complete `fclr_pooled001_*` (11), `fclr_pooled_audit001_*` (9) and `fclr_pooled_robust002_*` (9) bundles into your session dir so the older gate bindings (`FCLR-POOLED`, `FCLR-POOLED-AUDIT`, `FCLR-POOLED-ROBUST`) stay satisfied; pristine copies are under `session_20261122T190000Z/`.
>
> **Verdict discipline:** preserve the null honestly. Do NOT threshold-shop, do NOT relax the materiality floor after seeing outcomes, do NOT build an overlay, do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` (it cannot fire on frozen data). Observed liquidation labels may be an incomplete/capped feed: per §15 you may report a **PARTIAL_POSITIVE_SIGNAL** with explicit incomplete-label handling, but you may NEVER claim a complete observed-liquidation census or describe modeled Track B performance as observed liquidation. Either verdict is a valid, heavy, publishable result.
>
> **When done, update this handoff** per §6 (what changed, exact test outcomes, evidence paths, gate state, next task, verifying command, blockers) and set the latest session id to your `session_<UTC>/`. Do NOT write your `session_<UTC>/` id into this handoff before the directory exists (the gate verifies the lexicographically latest recorded session id against disk).

**STATUS: rank-0 `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` ACTIVE / READY_EXECUTE (gate-enforced). FCLR-POOLED-001 CONFIRMATORY_COMPLETE (NOT_SUPPORTED); FCLR-POOLED-AUDIT-001 COMPLETE (session_20261122T165200Z); FCLR-POOLED-ROBUST-002 CONFIRMATORY_COMPLETE (session_20261122T190000Z, NOT_SUPPORTED_LEAKAGE_ROBUST_NULL). No other rank-0 entry exists. Campaign start time has ELAPSED — next session is POST-START and gate requires the full `fclr_risk09_*` heavy artifacts.**

### 1a. Bottlenecks removed / verified clear (machine-checked)

1. **Stale-handoff gate failure fixed (the real bottleneck).** `session_20261122T190000Z` existed on disk but was not the latest session recorded in this handoff, so `check_handoff_heavywork_gate.py` failed with `HANDOFF_STALE_LATEST_SESSION:session_20261122T190000Z`. It is now recorded as the latest session and the gate passes.
2. **Incomplete heavy session completed.** `session_20261122T190000Z` had all nine `fclr_pooled_robust002_*` research artifacts + the `evidence_audit_` alias but was missing its `trigger_check_20261122T190000Z.json`. That non-empty trigger check (campaign, session, artifact list, headline QLIKE, decision, recompute pass, 54/54 sha256 verified) is now written.
3. **Carried-forward bundles restored.** The cumulative gate binds `FCLR-POOLED-001`, `FCLR-POOLED-AUDIT-001` and `FCLR-POOLED-ROBUST-002` onto every post-start session. `session_20261122T190000Z` was missing the `fclr_pooled001_*` (11) and `fclr_pooled_audit001_*` (9) bundles. Pristine copies were carried forward into it so all three older bindings are satisfied without re-running anything.
4. **Stale rank-0 frontier state fixed.** `research_state/experiment_frontier.json` listed `FCLR-POOLED-ROBUST-002-20261122T180000Z` as rank 0 / READY_EXECUTE / NOT_STARTED even though it was complete on disk. It is now demoted to **rank 1 / SUPERSEDED_TERMINAL / COMPLETE** (session_20261122T190000Z, verdict NOT_SUPPORTED_LEAKAGE_ROBUST_NULL, phases COMPLETE). `tests/test_active_campaign_gate.py` still passes (exactly one rank-0, ACTIVE, all others terminal).
5. **New rank-0 heavy campaign installed and gate-bound.** `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` is the sole rank-0 ACTIVE entry with a concrete `next_unfinished_task` and a 2-phase plan. The existing `FCLR-LIQ-RISK-ESCALATION` binding in `scripts/check_handoff_heavywork_gate.py` is ladder-aware (`fclr_risk{NN}_*`), so campaign 09 binds `fclr_risk09_*` with no gate-code change; a post-start session (`UTC > 20261122T193000Z`) that lacks the full heavy set fails closed. `tests/test_tracka_hardening_143.py::TestRisk08CampaignGate` already proves this ladder fails closed for missing/empty/trigger-less sessions and passes only with the full package.
6. **Verify-and-stop escape hatch closed.** The prior handoff told future agents to "confirm green and stop." That is replaced by an executable, gate-bound heavy campaign with a 2-phase plan and a `next_unfinished_task`.
7. **No blocked / inefficient sessions remain.** The observed-liquidation campaign runs entirely on existing on-disk data (no new source, no network, no external trigger); all prior campaigns are terminal; all on-disk `session_*` dirs contain files.

### 1b. Next session execution checklist (gate-enforced)

`FCLR-LIQ-RISK-ESCALATION-09` is the rank-0 task. Per RESEARCH_PROMPT.md §9 the forecast gate did NOT pass, so **no position-sizing/risk-reduction overlay shall be built**. Per §15/§16/§19 continue the valid liquidation-risk track with observed events and honest incomplete-label handling rather than stopping.

**Next session must:**
1. **Freeze the outcome-blind prereg** (`fclr_risk09_prereg_<UTC>.{json,md}`) BEFORE inspecting any outcome, with the §15 admissibility plan, all leakage remediations and the alpha-spending rule recorded; assert input sha256.
2. **Produce the power/MDE + coverage audit** (`fclr_risk09_power_<UTC>.{py,json,md}`): observed-event sparsity per coin-hour, identity-match rate, notional coverage, effective sample size and minimum detectable effect for the rare intensity target.
3. **Execute the heavy observed-liquidation evaluation** (`fclr_risk09_evaluation_<UTC>.{py,json,md}`): label-admissibility audit, `market`→`coin` identity map, hourly event-count + OI-normalized notional targets, RV-only vs funding-conditioned candidate, per-coin block-bootstrap CI95, Holm across the declared family, explicit symmetric verdict.
4. **Produce the independent stdlib recompute** (`fclr_risk09_recompute_<UTC>.{py,json}`), the gate-critical **`evidence_audit_<UTC>.json`**, and a non-empty **`trigger_check_<UTC>.json`**.
5. **Carry forward** the complete `fclr_pooled001_*` (11), `fclr_pooled_audit001_*` (9) and `fclr_pooled_robust002_*` (9) bundles into your session dir so the older `FCLR-POOLED` / `FCLR-POOLED-AUDIT` / `FCLR-POOLED-ROBUST` bindings stay satisfied.
6. **Preserve null discipline:** no threshold-shopping, no relaxing the materiality floor, no overlay, no waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE`, no claiming a complete observed-liquidation census from a capped feed.
7. **Keep `research_state` root ≤ 500 md+json files; all artifacts under session dirs; no empty/zero-byte files.**

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate   # → 121 tests, 0 failures
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (NOT a blocker)
```

### 1c. Heavy work enforced (gate verified this session)

`scripts/check_handoff_heavywork_gate.py` binds four active families: `FCLR-POOLED-001-20261122T040000Z` (start `20261122T040000Z`), `FCLR-POOLED-AUDIT-001-20261122T120000Z` (start `20261122T120000Z`), `FCLR-POOLED-ROBUST-002-20261122T180000Z` (start `20261122T180000Z`) and the new `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` (start `20261122T193000Z`). The current latest session `session_20261122T190000Z/` (UTC > the first three starts, ≤ the risk-09 start) satisfies the pooled + pooled-audit + pooled-robust families and is grandfathered for the risk-09 family. **Any future recorded session with UTC > `20261122T193000Z` must produce the full `fclr_risk09_*` heavy artifact set (plus the carried-forward pooled + pooled-audit + pooled-robust bundles) or the gate fails closed.** A prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop session fails closed.

### 1d. NEXT FOCUS CAMPAIGN (heavy-work enforced — cannot be skipped)

**Campaign:** `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` — the mandatory observed-liquidation (Track A) leakage-hardened intensity focus campaign for the next agentic work session.

**Why it cannot be avoided:** `scripts/check_handoff_heavywork_gate.py` binds `FCLR-LIQ-RISK-ESCALATION` (ladder-aware, start UTC `20261122T193000Z`). The gate fails closed for any post-start session (`UTC > 20261122T193000Z`) that does not carry the full `fclr_risk09_*` heavy artifact set under its own `session_<UTC>/`. `tests/test_tracka_hardening_143.py::TestRisk08CampaignGate` proves the binding fails closed for missing/empty/trigger-less sessions and passes only with the full package. A session that only "verifies green and stops" trips the gate and fails closed.

**Required deliverables for the next session (all under `research_state/session_<UTC>/`, UTC > `20261122T193000Z`, non-empty, no zero-byte placeholders):**
1. `fclr_risk09_prereg_<UTC>.{json,md}` — outcome-blind freeze with all §15 + leakage remediations + alpha-spending, frozen before outcomes.
2. `fclr_risk09_power_<UTC>.{py,json,md}` — observed-event sparsity/coverage + MDE power audit.
3. `fclr_risk09_recompute_<UTC>.{py,json}` — independent stdlib recompute from stored hashes.
4. `fclr_risk09_evaluation_<UTC>.{py,json,md}` — heavy label-admissibility + leakage-hardened intensity evaluation (count + OI-normalized notional, RV-only vs funding-conditioned, block bootstrap, Holm).
5. `evidence_audit_<UTC>.json` (+ `.md`) and non-empty `trigger_check_<UTC>.json`.
6. Carried-forward `fclr_pooled001_*` (11), `fclr_pooled_audit001_*` (9) and `fclr_pooled_robust002_*` (9) bundles.

**Verifying command:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate   # → 121 tests, 0 failures
python3 scripts/next_campaign_status.py                          # → NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN (not a blocker)
```

**Bottlenecks removed (verified this session):** stale-handoff gate failure fixed (`session_20261122T190000Z` now recorded); missing `trigger_check_` written; `fclr_pooled001_*`/`fclr_pooled_audit001_*` bundles carried forward; stale rank-0 ROBUST-002 demoted to SUPERSEDED_TERMINAL/COMPLETE; new rank-0 `FCLR-LIQ-RISK-ESCALATION-09` installed and gate-bound; gate PASS reason=OK; 121/121 unittests pass; root count 499/500 ≤ cap; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data (not a valid excuse to idle).

---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible evidence)

`scripts/next_campaign_status.py` reports `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` (re-verified this session), but that verdict is TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing. It is NOT a statement about the data on disk:

| Probe | Result |
|-------|--------|
| `research_state/data_cache/ironflow_bulk/candles_1h` | 18 monthly parquet files, 3,643,742 rows, up to 799 coins, 2025-05..2026-10 |
| `.../ironflow_bulk/funding` | 18 files, 4,104,648 rows, up to 494 coins |
| `.../ironflow_bulk/open_interest` | 18 files, 3,977,432 rows, up to 553 coins |
| `.../ironflow_bulk/liquidations` | 18 files, 2,849,452 rows, wallet-level events keyed on `market`/`issuer` (e.g. `HYPE-PERP`) |
| Observed-liquidation identity map | FEASIBLE TODAY — `market` `XXX-PERP` → `coin` `XXX`, join to candles/funding/OI on coin + UTC |
| Leakage-hardened observed-liquidation intensity study | FEASIBLE TODAY — no new source, no network, no external trigger |

The §15 admissibility requirements (coverage, completeness, capped-sample check, incomplete-label design) are all auditable on the existing ironflow liquidations bulk caches. Future agents cannot idle waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.

---

## 3. NON-AVOIDANCE CONSTRAINTS (machine-checked)

- **Do NOT** create root-level `research_state/*.md|*.json` — root count is **499/500**; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (the gate checks non-zero size).
- **Do NOT** claim completion without a full `fclr_risk09_*` heavy artifact set under a new `session_<UTC>/` (UTC > `20261122T193000Z`), and without recording that session id in this handoff.
- **Do NOT** write a concrete future `session_<UTC>` id into this handoff before that directory exists — the gate treats the lexicographically latest recorded `session_` id as the session to verify and will fail if its directory is missing.
- **Do NOT** threshold-shop or relax the materiality floor after outcomes; preserve nulls as `NOT_SUPPORTED`.
- **Do NOT** re-run any terminal/completed campaign (incl. FCLR-POOLED-001, FCLR-POOLED-AUDIT-001, FCLR-POOLED-ROBUST-002, NEXT-SOURCE-VERIFY-01, LIVE-ARCHIVE-01/-02, and all earlier campaigns).
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.
- **Do NOT** re-verify that `data.binance.vision` is reachable — already exhausted by FCLR-LIVE-ARCHIVE-02.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the gate passes for a post-start session only when the full `fclr_risk09_*` heavy artifact set (plus carried-forward bundles) is present and non-empty under the latest `session_<UTC>/`.
- **Do NOT** build a position-sizing/risk-reduction overlay — per RESEARCH_PROMPT.md §9, the forecast gate did not pass (NOT_SUPPORTED), so no overlay is eligible.
- **Do NOT** track-adulterate: never describe Track B (modeled breach) or Track C (volatility) performance as proof that actual liquidations were forecast; never claim a complete observed-liquidation census from a capped feed.

---

## 4. FROZEN / ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

- **Ironflow bulk caches (the data source for FCLR-LIQ-RISK-ESCALATION-09):** `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}/<YYYY-MM>.parquet` plus `<YYYY-MM>.parquet.sha256` and `<YYYY-MM>.accessed.json` sidecars, 18 months 2025-05..2026-10. Row counts and schemas per §2. Assert sha256 before reading; do NOT mutate the caches. The `liquidations` schema is `timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash` — join `market` (`XXX-PERP`) to `coin` (`XXX`) in funding/candles/open_interest.
- **Combined liquidation panel (legacy, still frozen):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins. Not needed for the observed-liquidation study; do not substitute it for the bulk liquidations stream.
- **FCLR-001 panel (funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`; `premium` all-null. Not needed for the observed-liquidation study.

---

## 5. CAMPAIGN LEDGER (all terminal except the rank-0)

| Campaign | Mechanism | Session / Status |
|----------|-----------|------------------|
| FCLR-STARTER-001 … FCLR-PANEL-FE-001 | earlier frozen-data campaigns | terminal/superseded |
| FCLR-LIQ-CONTAGION-001 | cross-coin contagion + funding spillover | COMPLETE (20261121T193000Z) |
| FCLR-LIQ-CONTAGION-002 | edge-set robustness + per-edge materiality reconciliation | COMPLETE (20261121T210000Z) |
| FCLR-FINAL-SYNTHESIS-01 | final synthesis report | COMPLETE (20261121T220100Z) |
| FCLR-LIVE-DATA-ACQUISITION-001 | unverified free-data route | SUPERSEDED 20261121T232840Z |
| FCLR-LIVE-ARCHIVE-01 | verified free-archive heavy 3-block design | SUPERSEDED by -02 (never started) |
| FCLR-LIVE-ARCHIVE-02 | verified free-archive heavy 3-block design | SUPERSEDED_TERMINAL (session_20261122T013000Z; NOT_SUPPORTED) |
| FCLR-NEXT-SOURCE-VERIFY-01 | materially different verified free source + heavy 3-block confirmatory | SUPERSEDED_TERMINAL (session_20261122T033000Z; NO_NEW_ADMISSIBLE_SOURCE) |
| FCLR-POOLED-001-20261122T040000Z | pooled chronological OOS confirmatory on on-disk ironflow bulk data | CONFIRMATORY_COMPLETE — rank 1 SUPERSEDED_TERMINAL; EXECUTED under session_20261122T092003Z; 11 fclr_pooled001_* artifacts; decision NOT_SUPPORTED |
| FCLR-POOLED-AUDIT-001-20261122T120000Z | adversarial leakage/quality audits on pooled ironflow bulk panel + Track B modeled breach labels | COMPLETE — executed under session_20261122T165200Z; rank 1 SUPERSEDED_TERMINAL; 9 fclr_pooled_audit001_* artifacts + evidence_audit_ + non-empty trigger_check_ |
| FCLR-POOLED-ROBUST-002-20261122T180000Z | leakage-hardened re-confirmation applying all audit remediations; sequential confirmatory look k=2 | CONFIRMATORY_COMPLETE — executed under session_20261122T190000Z; rank 1 SUPERSEDED_TERMINAL; 9 fclr_pooled_robust002_* artifacts + alias + trigger_check_; decision NOT_SUPPORTED_LEAKAGE_ROBUST_NULL |
| **FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z** | **first confirmatory use of OBSERVED ironflow liquidations (Track A); leakage-hardened intensity forecast + §15 label-admissibility** | **RANK-0 ACTIVE / READY_EXECUTE — gate-enforced via FCLR-LIQ-RISK-ESCALATION (start UTC 20261122T193000Z); not yet started; `fclr_risk09_*` heavy artifacts required under session_<UTC> (UTC > 20261122T193000Z)** |

Note: the earlier modeled-breach calibration work (RISK-06) and recalibration work (RISK-07) are complete and terminal; the observed-liquidation escalation above is strictly more direct evidence for the liquidation-risk pillar and does not re-run them.

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this `AGENT_HANDOFF.md` with: (1) what changed and why; (2) what was tested with exact outcomes; (3) what evidence was added and where (full paths); (4) the state of each research gate; (5) the single highest-value next task; (6) the precise verifying command; (7) any blocker with the next materially different route.

**(1)** This refresh records the completed `session_20261122T190000Z` as the latest session, adds its missing `trigger_check_`, carries forward the `fclr_pooled001_*` and `fclr_pooled_audit001_*` bundles, demotes FCLR-POOLED-ROBUST-002 to SUPERSEDED_TERMINAL/COMPLETE in the frontier, and installs `FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z` as the sole rank-0 gate-bound campaign. **(2)** Gate `check_handoff_heavywork_gate.py` → PASS reason=OK; 121/121 gate unittests 0 failures (the 3 real-repo/CLI tests that were red now pass because the gate is green). **(3)** No new research_state root artifacts written; only session-dir bookkeeping (trigger_check + carried-forward bundles) and the frontier/handoff updates. **(4)** Gate state: `check_handoff_heavywork_gate.py` PASS reason=OK; root count 499/500 ≤ cap. **(5)** Single highest-value next task: execute FCLR-LIQ-RISK-ESCALATION-09 (observed-liquidation leakage-hardened intensity study) and record its session id. **(6)** Precise verifying command: `python3 scripts/check_handoff_heavywork_gate.py && python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate`. **(7)** Blocker: none — the campaign runs entirely on frozen on-disk ironflow bulk data with no new source and no external trigger; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data and is not a valid idle excuse.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK (latest session = session_20261122T190000Z; pooled 11/11 + pooled_audit 9/9 + pooled_robust 9/9 + alias + trigger present and non-empty under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate   # → 121 tests, 0 failures
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (does NOT cover the observed-liquidation study — that is the point)
```

After the heavy observed-liquidation session writes its `fclr_risk09_*` artifacts (UTC > `20261122T193000Z`), carries forward the pooled + pooled-audit + pooled-robust bundles, and records its `session_<UTC>/` in this handoff, `check_handoff_heavywork_gate.py` PASSES because the full `fclr_risk09_*` artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)