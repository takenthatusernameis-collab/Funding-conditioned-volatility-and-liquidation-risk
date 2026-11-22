# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T18:56:38Z (supersedes 2026-11-22T17:56:12Z)
**Session type:** handoff refresh + timestamp update + next focus campaign lock. Sole rank-0 campaign is `FCLR-POOLED-ROBUST-002-20261122T180000Z` (**ACTIVE / READY_EXECUTE**, gate-enforced). Campaign start UTC `20261122T180000Z` has **elapsed** (current UTC 2026-11-22T18:56:38Z). The next session (UTC > 180000Z) **must** produce the full heavy artifact set or the gate fails closed.

**Sole rank-0 campaign (gate-enforced):** `FCLR-POOLED-ROBUST-002-20261122T180000Z` — **ACTIVE / READY_EXECUTE**. A heavy, outcome-blind, leakage-hardened RE-CONFIRMATION of the funding-conditioned volatility + liquidation-risk hypothesis on the same on-disk ironflow bulk panel, applying all `FCLR-POOLED-AUDIT-001` remediations simultaneously (48h purge+embargo, non-overlapping forward windows, mark/index tolerance, delisting-aware identity, survivors-vs-exited arm, per-month threshold-drift reporting, per-coin block-bootstrap, Holm across the declared family) and reported as sequential confirmatory look k=2 with alpha-spending. Gate binding `FCLR-POOLED-ROBUST` fails closed without the full heavy artifact set under `research_state/session_<UTC>/` (UTC > `20261122T180000Z`).

**Latest completed heavy session on disk:** `session_20261122T165200Z` — executed FCLR-POOLED-AUDIT-001 to completion: the 11 `fclr_pooled_audit001_*` artifacts (prereg json+md, audit py+json+md, recompute py+json, evidence audit json+md), plus `evidence_audit_` (json) and non-empty `trigger_check_` (json); carried forward the complete `fclr_pooled001_*` bundle (13 artifacts) from `session_20261122T092003Z/`. Decision basis preserved: FCLR-POOLED-001 NOT_SUPPORTED (funding-conditioned features add no QLIKE improvement over RV-only baseline).

**Gate baseline (verified this session, 2026-11-22T18:56:38Z):** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK` (`latest_handoff=session_20261122T165200Z`, `latest_disk=session_20261122T165200Z`, `handoff_stale=False`, `pooled.required=True` 13/13 artifacts present under latest session, `pooled_audit.required=True` 11/11 artifacts present, `pooled_robust_02.required=False` because latest session UTC `20261122T165200Z` ≤ campaign start `20261122T180000Z` (grandfathered), `root=499/500`); all gate unittest modules (`test_tracka_hardening_143`, `test_tracka_hardening_144`, `test_active_campaign_gate`, `test_fclr_heavy_confirm_gate`, `test_fclr_campaign_gate`, `test_fclr_starter_001_campaign_gate`, `test_pooled_robust_002_campaign_gate`) → **121 tests, 0 failures**; `research_state` root md+json count = **499/500**; latest on-disk session = latest recorded in this handoff (`session_20261122T165200Z`); no empty session directories (61 session dirs scanned); no `fclr_pooled_audit*` artifacts missing. On-disk ironflow bulk caches unchanged: candles_1h/funding/open_interest/liquidations each **18 parquet files + 18 sha256 sidecars + 18 accessed.json** (2025-05..2026-10).

**Environment (verified):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy` NOT installed (`ModuleNotFoundError`). `pyarrow` 26.0.1 installed — reads ironflow bulk parquet. Use stdlib + pyarrow only. Do NOT rely on numpy/pandas/scipy.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001/002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01/02, FCLR-NEXT-SOURCE-VERIFY-01, FCLR-POOLED-001, FCLR-POOLED-AUDIT-001) are terminal / superseded / completed — **do NOT re-run them**. The reachable-free-source frontier (NEXT-SOURCE-VERIFY-01) is executed and terminal (NO_NEW_ADMISSIBLE_SOURCE). **FCLR-POOLED-001 is CONFIRMATORY_COMPLETE** — executed under `session_20261122T092003Z` with all 13 `fclr_pooled_*` artifacts; decision NOT_SUPPORTED. **FCLR-POOLED-AUDIT-001 is COMPLETE** — executed under `session_20261122T165200Z` with all 11 `fclr_pooled_audit001_*` artifacts + `evidence_audit_` + `trigger_check_`. A future session must NOT re-run either completed campaign; per §9 no risk overlay should be built since the forecast gate did not pass.

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars (RESEARCH_PROMPT.md §Mission/§3). Never drift into unrelated work, risk overlays, or live/paper trading. RESEARCH_PROMPT.md §16/§19/§20 forbid declaring the research complete after one unfavorable result and forbid cosmetic verify-and-stop sessions while a valid heavy task remains: the sole rank-0 below is that heavy task.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (handoff refresh 2026-11-22T18:56:38Z; campaign start UTC 20261122T180000Z **ELAPSED**)

> **READ THIS FIRST.**
>
> You are the next agentic work session for the **Funding-conditioned-volatility-and-liquidation-risk** research program. Your single highest-value, repo-name-prioritized, gate-enforced task is to **execute the rank-0 campaign `FCLR-POOLED-ROBUST-002-20261122T180000Z`**: a heavy, outcome-blind, **leakage-hardened re-confirmation** of the funding-conditioned volatility + liquidation-risk hypothesis on the same on-disk ironflow bulk panel. This is NOT a re-run of FCLR-POOLED-001 and NOT a re-run of the FCLR-POOLED-AUDIT-001 audit. It applies the audit's own remediations simultaneously and asks whether the NOT_SUPPORTED verdict survives a leakage-hardened design.
>
> **Why this and nothing else:** FCLR-POOLED-001 came back **NOT_SUPPORTED** (funding-conditioned features add ~0.0% QLIKE vs the RV-only baseline, below the −2% materiality floor; bootstrap CI95 includes zero). FCLR-POOLED-AUDIT-001 then found concrete quality gaps that could have *manufactured or masked* that null: (d2) only a 1-hour train/test gap — the 48h purge+embargo was NOT applied; (d10) overlapping forward outcomes (pairwise Jaccard 0.52..0.92 dependence); (d4) 6.8% of rows above the 1% mark/index tolerance; (d6/d7) delisting/survivorship (344 coins new, 44 exited, survivor share 38%); (d9) monthly threshold drift. RESEARCH_PROMPT.md §10 priority 8 (adversarial audits) is done; §16/§19 require continuing after an unfavorable result instead of stopping; §9 still forbids any risk overlay because the forecast gate did not pass. The leakage-hardened re-confirmation is therefore the highest-value unfinished task, and it is now **gate-enforced** so it cannot be skipped.
>
> **What you must produce (all under `research_state/session_<UTC>/` with UTC > `20261122T180000Z`, non-empty, no zero-byte placeholders):**
> 1. `fclr_pooled_robust002_prereg_<UTC>.{json,md}` — outcome-blind prereg **frozen before any outcome is inspected** (`outcome_data_inspected_before_freeze:false`; assert input sha256; 48h purge+embargo; non-overlapping 6h/24h/72h/168h forward windows; 1% mark-oracle premium tolerance filter; delisting-aware per-coin identity; RV-only baseline; 2% materiality floor; Holm family; alpha-spending k=2, α₂ = 0.05/(2·3) = 0.00833).
> 2. `fclr_pooled_robust002_robustness_<UTC>.{py,json,md}` — heavy stdlib+pyarrow robustness recompute implementing every remediation, producing QLIKE (primary) and Brier/log-loss on the clearly-labeled Track B modeled breach proxy (secondary; modeled, never observed liquidation), per-coin block-bootstrap CI95, survivors-vs-exited sensitivity arm, Holm-adjusted results, and an explicit symmetric verdict rule (null confirmed leakage-robust OR earlier null was a leakage artifact).
> 3. `fclr_pooled_robust002_recompute_<UTC>.{py,json}` — independent stdlib recompute from the stored input hashes, reproducing the headline numbers within a declared tolerance.
> 4. `fclr_pooled_robust002_evidence_audit_<UTC>.{json,md}` — evidence/provenance audit of the robustness run.
> 5. `evidence_audit_<UTC>.json` — gate-critical alias.
> 6. non-empty `trigger_check_<UTC>.json`.
>
> **Also carry forward** the complete `fclr_pooled001_*` (13 artifacts) and `fclr_pooled_audit001_*` (11 artifacts) bundles into your session dir so the older gate bindings (`FCLR-POOLED`, `FCLR-POOLED-AUDIT`) stay satisfied; they are already present under `session_20261122T165200Z/` and `session_20261122T092003Z/`.
>
> **Verdict discipline:** preserve the null honestly. Do NOT threshold-shop, do NOT relax the 2% floor after seeing outcomes, do NOT build an overlay, do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` (it cannot fire on frozen data). If the leakage-hardened design flips the result, report it as a leakage artifact with full evidence; if it confirms NOT_SUPPORTED, report the null as leakage-robust. Either outcome is a valid, heavy, publishable result.
>
> **When done, update this handoff** per §6 (what changed, exact test outcomes, evidence paths, gate state, next task, verifying command, blockers) and set the latest session id to your `session_<UTC>/`. Do NOT write your `session_<UTC>/` id into this handoff before the directory exists (the gate verifies the lexicographically latest recorded session id against disk).

**STATUS: rank-0 `FCLR-POOLED-ROBUST-002-20261122T180000Z` ACTIVE / READY_EXECUTE (gate-enforced). FCLR-POOLED-001 CONFIRMATORY_COMPLETE (NOT_SUPPORTED); FCLR-POOLED-AUDIT-001 COMPLETE (session_20261122T165200Z). No other rank-0 entry exists. Campaign start time has ELAPSED — next session is POST-START and gate requires full heavy artifacts.**

### 1a. Bottlenecks removed / verified clear (machine-checked)

1. **Stale rank-0 state fixed (the real bottleneck).** `research_state/experiment_frontier.json` still listed `FCLR-POOLED-AUDIT-001-20261122T120000Z` as **rank 0 / READY_EXECUTE / ACTIVE** with **PENDING** phases, even though it was complete on disk under `session_20261122T165200Z/`. A future agent reading the frontier would have seen a rank-0 ACTIVE campaign and could have re-run finished work. It is now demoted to **rank 1 / SUPERSEDED_TERMINAL / COMPLETE** with both phases marked COMPLETE, `completed_session=session_20261122T165200Z`, `last_verdict=NOT_SUPPORTED`, and `superseded_by=FCLR-POOLED-ROBUST-002-20261122T180000Z`. `test_active_campaign_gate` still passes (exactly one rank-0, ACTIVE, all others terminal).
2. **New rank-0 heavy campaign installed and gate-bound.** `FCLR-POOLED-ROBUST-002-20261122T180000Z` is the sole rank-0 ACTIVE entry, carrying a concrete `next_unfinished_task` and a 2-phase plan. `scripts/check_handoff_heavywork_gate.py` now binds it via `POOLED_ROBUST_CAMPAIGN_RE` (campaign start UTC `20261122T180000Z`); a post-start session (`UTC > 20261122T180000Z`) that does not carry the full heavy robustness artifact set (prereg json+md, robustness py+json+md, recompute py+json, evidence audit json+md, `evidence_audit_` json, non-empty `trigger_check_` json) fails closed. Zero-byte placeholders fail closed. Sessions at/before the campaign start (incl. `session_20261122T165200Z`) are grandfathered so this refresh stays green.
3. **Verify-and-stop escape hatch closed.** The prior handoff told future agents to "confirm green and stop." That is now replaced by an executable heavy campaign with a gate binding and a 5-test regression module (`tests/test_pooled_robust_002_campaign_gate.py`) proving the binding fails closed for missing/empty/trigger-less sessions and passes only with the full heavy set.
4. **No blocked / inefficient sessions remain.** FCLR-POOLED-ROBUST-002 is ready to execute on existing on-disk data (no new source, no network, no external trigger); FCLR-POOLED-AUDIT-001 and FCLR-POOLED-001 are complete; NEXT-SOURCE-VERIFY-01 is terminal. All 61 on-disk `session_*` dirs contain files (no empty dirs).
5. **Root churn cap respected.** `research_state` root md+json count = 499/500; all new artifacts must go under `session_<UTC>/`.

### 1b. Next session execution checklist (gate-enforced)

`FCLR-POOLED-ROBUST-002` is the rank-0 task. Per RESEARCH_PROMPT.md §9 the forecast gate did NOT pass, so **no position-sizing/risk-reduction overlay shall be built**. Per §16/§19 continue the valid volatility + liquidation-risk track rather than stopping.

**Next session must:**
1. **Freeze the outcome-blind prereg** (`fclr_pooled_robust002_prereg_<UTC>.{json,md}`) BEFORE inspecting any outcome, with all audit remediations and the alpha-spending k=2 rule recorded; assert input sha256.
2. **Execute the heavy robustness recompute** (`fclr_pooled_robust002_robustness_<UTC>.{py,json,md}`): 48h purge+embargo, non-overlapping 6h/24h/72h/168h forward windows, 1% mark/index tolerance filter, delisting-aware per-coin identity, survivors-vs-exited sensitivity arm, per-coin block-bootstrap CI95, QLIKE + Brier/log-loss vs RV-only baseline, Holm across the declared family.
3. **Produce the independent stdlib recompute** (`fclr_pooled_robust002_recompute_<UTC>.{py,json}`), the **evidence audit** (`fclr_pooled_robust002_evidence_audit_<UTC>.{json,md}`), the gate-critical **`evidence_audit_<UTC>.json`** alias, and a non-empty **`trigger_check_<UTC>.json`**.
4. **Carry forward** the complete `fclr_pooled001_*` (13) and `fclr_pooled_audit001_*` (11) bundles into your session dir so the older `FCLR-POOLED` / `FCLR-POOLED-AUDIT` bindings stay satisfied.
5. **Preserve the null discipline:** no threshold-shopping, no relaxing the 2% floor, no overlay, no waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE`.
6. **Keep `research_state` root ≤ 500 md+json files; all artifacts under session dirs; no empty/zero-byte files.**

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate   # → 121 tests, 0 failures
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (NOT a blocker)
```

### 1c. Heavy work enforced (gate verified this session)

`scripts/check_handoff_heavywork_gate.py` binds three active families: `FCLR-POOLED-001-20261122T040000Z` (start `20261122T040000Z`), `FCLR-POOLED-AUDIT-001-20261122T120000Z` (start `20261122T120000Z`), and the new `FCLR-POOLED-ROBUST-002-20261122T180000Z` (start `20261122T180000Z`). The current latest session `session_20261122T165200Z/` (UTC > the first two starts, ≤ the robust start) satisfies the pooled + pooled-audit families and is grandfathered for the robust family. **Any future recorded session with UTC > `20261122T180000Z` must produce the full heavy robustness artifact set (plus the carried-forward pooled + pooled-audit bundles) or the gate fails closed.** A prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop session fails closed.

### 1d. NEXT FOCUS CAMPAIGN (heavy-work enforced — cannot be skipped)

**Campaign:** `FCLR-POOLED-ROBUST-002-20261122T180000Z` — the mandatory leakage-hardened re-confirmation focus campaign for the next agentic work session.

**Why it cannot be avoided:** `scripts/check_handoff_heavywork_gate.py` binds `FCLR-POOLED-ROBUST` (start UTC `20261122T180000Z`). The gate fails closed for any post-start session (`UTC > 20261122T180000Z`) that does not carry the full heavy robustness artifact set under its own `session_<UTC>/`. `tests/test_pooled_robust_002_campaign_gate.py` proves the binding fails closed for missing/empty/trigger-less sessions and passes only with the full set. A session that only "verifies green and stops" trips the gate and fails closed.

**Required deliverables for the next session (all under `research_state/session_<UTC>/`, UTC > `20261122T180000Z`, non-empty, no zero-byte placeholders):**
1. `fclr_pooled_robust002_prereg_<UTC>.{json,md}` — outcome-blind freeze with all remediations + alpha-spending k=2, frozen before outcomes.
2. `fclr_pooled_robust002_robustness_<UTC>.{py,json,md}` — heavy robustness recompute (48h embargo, non-overlapping windows, mark/index filter, delisting-aware identity, survivors-vs-exited arm, block-bootstrap, QLIKE + Brier/log-loss vs RV-only, Holm).
3. `fclr_pooled_robust002_recompute_<UTC>.{py,json}` — independent stdlib recompute from stored hashes.
4. `fclr_pooled_robust002_evidence_audit_<UTC>.{json,md}` + gate-critical `evidence_audit_<UTC>.json` + non-empty `trigger_check_<UTC>.json`.
5. Carried-forward `fclr_pooled001_*` (13) and `fclr_pooled_audit001_*` (11) bundles.

**Verifying command:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate   # → 121 tests, 0 failures
python3 scripts/next_campaign_status.py                          # → NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN (not a blocker)
```

**Bottlenecks removed (verified this session):** stale rank-0 FCLR-POOLED-AUDIT-001 demoted to SUPERSEDED_TERMINAL/COMPLETE; new rank-0 FCLR-POOLED-ROBUST-002 installed and gate-bound; 0 empty session directories; 61/61 session dirs contain files; gate PASS reason=OK; 121/121 unittests pass; root count 499/500 ≤ cap; all campaigns terminal except the rank-0; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data (not a valid excuse to idle).

---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible evidence)

`scripts/next_campaign_status.py` reports `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` (re-verified this session), but that verdict is TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing. It is NOT a statement about the data on disk:

| Probe | Result |
|-------|--------|
| `research_state/data_cache/ironflow_bulk/candles_1h` | 18 monthly parquet files, 3,643,742 rows, up to 799 coins, 2025-05..2026-10 |
| `.../ironflow_bulk/funding` | 18 files, 4,104,648 rows, up to 494 coins |
| `.../ironflow_bulk/open_interest` | 18 files, 3,977,432 rows, up to 553 coins |
| `.../ironflow_bulk/liquidations` | 18 files, 2,849,452 rows, key on market/issuer (no coin column) |
| Leakage-hardened re-confirmation on pooled panel | FEASIBLE TODAY — no new source, no network, no external trigger |
| Track B modeled boundary-breach labels | FEASIBLE TODAY from mark-price history + public margin params |

The audit remediations (d2/d4/d6/d7/d9/d10) are all computable on the existing ironflow bulk caches. Future agents cannot idle waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.

---

## 3. NON-AVOIDANCE CONSTRAINTS (machine-checked)

- **Do NOT** create root-level `research_state/*.md|*.json` — root count is **499/500**; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (the gate checks non-zero size).
- **Do NOT** claim completion without a full heavy artifact set under a new `session_<UTC>/` (UTC > `20261122T180000Z`), and without recording that session id in this handoff.
- **Do NOT** write a concrete future `session_<UTC>` id into this handoff before that directory exists — the gate treats the lexicographically latest recorded `session_` id as the session to verify and will fail if its directory is missing.
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as `NOT_SUPPORTED`.
- **Do NOT** re-run any terminal/completed campaign (incl. FCLR-POOLED-001, FCLR-POOLED-AUDIT-001, NEXT-SOURCE-VERIFY-01, LIVE-ARCHIVE-01/-02, and all earlier campaigns).
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.
- **Do NOT** re-verify that `data.binance.vision` is reachable — already exhausted by FCLR-LIVE-ARCHIVE-02.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the gate passes for a post-start session only when the full heavy robustness artifact set is present and non-empty under the latest `session_<UTC>/`.
- **Do NOT** build a position-sizing/risk-reduction overlay — per RESEARCH_PROMPT.md §9, the forecast gate did not pass (NOT_SUPPORTED), so no overlay is eligible.
- **Do NOT** track-adulterate: never describe Track B (modeled breach) or Track C (volatility) performance as proof that actual liquidations were forecast.

---

## 4. FROZEN / ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

- **Ironflow bulk caches (the data source for FCLR-POOLED-ROBUST-002):** `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}/<YYYY-MM>.parquet` plus `<YYYY-MM>.parquet.sha256` and `<YYYY-MM>.accessed.json` sidecars, 18 months 2025-05..2026-10. Row counts and schemas per §2 and the frontier `evidence` block. Assert sha256 before reading; do NOT mutate the caches.
- **Combined liquidation panel (legacy, still frozen):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Not needed for the pooled robustness; do not substitute it for the bulk data.
- **FCLR-001 panel (funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`; `premium` all-null; not needed for the pooled robustness.

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
| FCLR-LIVE-ARCHIVE-02 | verified free-archive heavy 3-block design | SUPERSEDED_TERMINAL (session_20261122T013000Z; decision NOT_SUPPORTED) |
| FCLR-NEXT-SOURCE-VERIFY-01 | materially different verified free source + heavy 3-block confirmatory | SUPERSEDED_TERMINAL (session_20261122T033000Z; NO_NEW_ADMISSIBLE_SOURCE) |
| FCLR-POOLED-001 | pooled chronological OOS confirmatory on on-disk ironflow bulk data | CONFIRMATORY_COMPLETE — rank 1 SUPERSEDED_TERMINAL; EXECUTED under session_20261122T092003Z; 13 fclr_pooled_* artifacts; decision NOT_SUPPORTED |
| FCLR-POOLED-AUDIT-001 | adversarial leakage/quality audits on pooled ironflow bulk panel + Track B modeled breach labels | COMPLETE — executed under session_20261122T165200Z; demoted to rank 1 SUPERSEDED_TERMINAL; 11 fclr_pooled_audit001_* artifacts + evidence_audit_ + non-empty trigger_check_ |
| **FCLR-POOLED-ROBUST-002** | **leakage-hardened re-confirmation applying all audit remediations; sequential confirmatory look k=2** | **RANK-0 ACTIVE / READY_EXECUTE — gate-enforced via FCLR-POOLED-ROBUST (start UTC 20261122T180000Z); not yet started; heavy artifacts required under session_<UTC> (UTC > 20261122T180000Z)** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this `AGENT_HANDOFF.md` with: (1) what changed and why; (2) what was tested with exact outcomes; (3) what evidence was added and where (full paths); (4) the state of each research gate; (5) the single highest-value next task; (6) the precise verifying command; (7) any blocker with the next materially different route.

**(1)** This refresh updates the handoff timestamp to 2026-11-22T18:56:38Z (campaign start UTC 20261122T180000Z has elapsed; next session is definitively post-start). **(2)** Gate `check_handoff_heavywork_gate.py` → PASS reason=OK (pooled 13/13 + pooled_audit 11/11 artifacts present under session_20261122T165200Z; pooled_robust_02 not yet required — grandfathered); 121/121 gate unittests 0 failures (116 prior + 5 new in `tests/test_pooled_robust_002_campaign_gate.py`). **(3)** No new research_state artifacts written (this is a handoff timestamp refresh session). **(4)** Gate state: `check_handoff_heavywork_gate.py` PASS reason=OK; root count 499/500 ≤ cap. **(5)** Single highest-value next task: execute FCLR-POOLED-ROBUST-002 (leakage-hardened re-confirmation) and record its session id. **(6)** Precise verifying command: `python3 scripts/check_handoff_heavywork_gate.py && python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate`. **(7)** Blocker: none — the campaign runs entirely on frozen on-disk ironflow bulk data with no new source and no external trigger; `NEW_OBSERVED_LIQUIDATION_SOURCE` cannot fire on frozen data and is not a valid idle excuse.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK (latest session = session_20261122T165200Z; pooled 13/13 + pooled_audit 11/11 artifacts present and non-empty under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate tests.test_pooled_robust_002_campaign_gate   # → 121 tests, 0 failures
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (does NOT cover the pooled robustness — that is the point)
```

After the heavy robustness session writes its artifacts (UTC > `20261122T180000Z`), carries forward the pooled + pooled-audit bundles, and records its `session_<UTC>/` in this handoff, `check_handoff_heavywork_gate.py` PASSES because the full heavy artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)