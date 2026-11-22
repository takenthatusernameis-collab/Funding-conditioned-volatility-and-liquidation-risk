# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T17:20:03Z (supersedes 2026-11-22T17:18:20Z)
**Session type:** handoff refresh — single durable handoff; sole rank-0 campaign `FCLR-POOLED-AUDIT-001-20261122T120000Z` is now **COMPLETE** (executed under `session_20261122T165200Z`), gate-enforced. Gate PASS reason=OK; root 499/500; 116/116 gate unittests pass; no blocked/inefficient sessions; no empty session dirs; latest disk session = latest recorded handoff session (`session_20261122T165200Z`).

**Sole rank-0 campaign (gate-enforced):** `FCLR-POOLED-AUDIT-001-20261122T120000Z` — **COMPLETE**, executed under `session_20261122T165200Z/` (UTC > campaign start `20261122T110000Z`). Adversarial leakage/quality audits on the pooled ironflow bulk panel with optional Track B modeled boundary-breach labels; all 11 `fclr_pooled_audit001_*` artifacts plus `evidence_audit_` and `trigger_check_` present and non-empty under `session_20261122T165200Z/`. Demoted to rank 1 SUPERSEDED_TERMINAL. No other rank-0 entry exists; no further rank-0 campaign remains.

**Latest completed heavy session on disk:** `session_20261122T165200Z` — executed FCLR-POOLED-AUDIT-001 to completion: the 11 `fclr_pooled_audit001_*` artifacts (prereg json+md, audit py+json+md, recompute py+json, evidence audit json+md), plus `evidence_audit_` (json) and non-empty `trigger_check_` (json); carried forward the complete `fclr_pooled001_*` bundle (13 artifacts) from `session_20261122T092003Z/`. Decision basis preserved: FCLR-POOLED-001 NOT_SUPPORTED (funding-conditioned features add no QLIKE improvement over RV-only baseline). All earlier sessions remain terminal/grandfathered.

**Gate baseline (verified this session, 2026-11-22T16:52:00Z):** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK` (`latest_handoff=session_20261122T165200Z`, `latest_disk=session_20261122T165200Z`, `handoff_stale=False`, `pooled.required=True` 13/13 artifacts present under latest session, `pooled_audit.required=True` 11/11 artifacts present, `root=499/500`); all 6 gate unittest modules (`test_tracka_hardening_143`, `test_tracka_hardening_144`, `test_active_campaign_gate`, `test_fclr_heavy_confirm_gate`, `test_fclr_campaign_gate`, `test_fclr_starter_001_campaign_gate`) → **116 tests, 0 failures**; `research_state` root md+json count = **499/500**; latest on-disk session = latest recorded in this handoff (`session_20261122T165200Z`); no empty session directories (61 session dirs scanned); no `fclr_pooled_audit*` artifacts missing. On-disk ironflow bulk caches unchanged: candles_1h/funding/open_interest/liquidations each **18 parquet files + 18 sha256 sidecars + 18 accessed.json** (2025-05..2026-10).

**Environment (verified):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy` NOT installed (`ModuleNotFoundError`). `pyarrow` 26.0.1 installed — reads ironflow bulk parquet. Use stdlib + pyarrow only. Do NOT rely on numpy/pandas/scipy.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001/002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01/02, FCLR-NEXT-SOURCE-VERIFY-01, FCLR-POOLED-001) are terminal / superseded / completed — **do NOT re-run them**. The reachable-free-source frontier (NEXT-SOURCE-VERIFY-01) is executed and terminal (NO_NEW_ADMISSIBLE_SOURCE). **FCLR-POOLED-001 is CONFIRMATORY_COMPLETE** — executed under `session_20261122T092003Z` with all 13 `fclr_pooled_*` artifacts; decision NOT_SUPPORTED. A future session must NOT re-run this completed campaign; per §9, no risk overlay should be built since the forecast gate did not pass.

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars (RESEARCH_PROMPT.md §Mission/§3). Never drift into unrelated work, risk overlays, or live/paper trading.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (handoff refresh 2026-11-22T17:20:03Z; campaign executed 2026-11-22T16:52:00Z under `session_20261122T165200Z/`; originally timestamped 2026-11-22T14:36:15Z)

> **READ THIS FIRST.**
>
> Campaign `FCLR-POOLED-AUDIT-001-20261122T120000Z` has been **executed to completion** under
> `research_state/session_20261122T165200Z/` (UTC `20261122T165200Z` > campaign start `20261122T120000Z`).
> Ranked by repo name **Funding-conditioned-volatility-and-liquidation-risk**, this was the single
> highest-value unfinished task: the adversarial leakage/quality audit of the pooled ironflow panel,
> because the pooled confirmatory forecast (FCLR-POOLED-001, `session_20261122T092003Z`) came back
> **NOT_SUPPORTED** and RESEARCH_PROMPT.md §10 priority 8 is to attack the result before any further
> modeling. Everything else is terminal.
>
> **What was executed (all under `session_20261122T165200Z/`, no new source, no network, no external trigger):**
> - Carried forward the complete `fclr_pooled001_*` bundle (13 artifacts) from `session_20261122T092003Z/`.
> - Produced the full `fclr_pooled_audit001_*` artifact set (11 artifacts, all non-empty): prereg json+md,
>   audit py+json+md (10 adversarial domains + Track B modeled boundary-breach labels), recompute py+json,
>   evidence audit json+md; plus `evidence_audit_20261122T165200Z.json` (gate-critical alias) and
>   non-empty `trigger_check_20261122T165200Z.json`.
> - Audit domains: d1 future-row perturbation (0 monotonicity violations, 0 cross-file overlaps);
>   d2 split embargo (train/test gap = 1 hour — 48h purge+embargo NOT present in raw panel, reported not assumed);
>   d3 funding sign/timing (publication-timing reading: corr fwd 0.00113 vs lag 0.00060);
>   d4 mark/index alignment (6.8% of rows above 1% tolerance; max premium 37x STRAX-PERP);
>   d5 missingness preservation (zero nulls in candles/funding; OI mark_price nulls concentrated 2026-07..09);
>   d6 delisting/symbol migration (344 coins new in last month; 44 exited; survivor share 38%);
>   d7 survivorship (mean abs funding survivors 2.77e-5 vs non-survivors 3.20e-5 — no strong difference);
>   d8 stress concentration (top market share of stress hours 2.5% — not single-coin dominated);
>   d9 threshold drift (mean monthly p66 drift 1.1e-5); d10 overlapping outcomes (pairwise Jaccard 0.52..0.92 —
>   forward liquidation-intensity outcomes not independent); trackb modeled boundary-breach (modeled breach rate
>   4.1% at 2.5% band; high funding tercile 4.7% vs low 2.9% — modeled proxy, NOT observed liquidation).
> - Independent stdlib recompute: daily-RV stress, positive-only liquidation median, 5% breach band — all
>   material domains corroborated; strict exact-timestamp alignment not estimable (funding grid ≠ hourly grid),
>   reported as a coverage null.
>
> **Gate result:** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK` with
> `session_20261122T165200Z/` recorded; all 6 gate unittest modules → 116 tests, 0 failures;
> `research_state` root md+json count = 499/500 (unchanged; no root-level artifacts written).
>
> **Verdict preserved:** NOT_SUPPORTED — no position-sizing/risk-reduction overlay may be built
> (RESEARCH_PROMPT.md §9 gate did not pass). No further rank-0 campaign remains; the program holds at
> NOT_SUPPORTED. Threshold-shopping after outcomes is forbidden; nulls are preserved.
>
> **Next session task:** confirm the gate is still green (`check_handoff_heavywork_gate.py` → PASS,
> latest session = `session_20261122T165200Z`), re-run the 6 gate unittest modules (0 failures), and
> preserve/negative-report the NOT_SUPPORTED outcome. Do NOT start any new rank-0 campaign, do NOT build a
> risk overlay, do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen data).

**STATUS: FCLR-POOLED-001 CONFIRMATORY_COMPLETE (NOT_SUPPORTED); FCLR-POOLED-AUDIT-001 COMPLETE (session_20261122T165200Z); no rank-0 ACTIVE campaign remains.**

FCLR-POOLED-001 (pooled chronological OOS confirmatory on the on-disk ironflow bulk data, 18 months 2025-05..2026-10, 799 markets, ~2.3M train / ~1.3M test rows) is **complete** under `research_state/session_20261122T092003Z/` (UTC `20261122T092003Z` > campaign start `20261122T040000Z`). All 13 `fclr_pooled_*` artifacts are present and non-empty. Verdict: **NOT_SUPPORTED** — funding-conditioned features add no predictive value over the RV-only baseline (QLIKE B1=65.190573 vs C2=65.190702, diff +0.000129, rel +0.0002%, far below the −2.0% materiality floor; bootstrap CI95 includes zero). Null preserved. Independent stdlib recompute concurs (QLIKE_B1=52.945004, QLIKE_C2=52.944664, rel −0.0006%, NOT_SUPPORTED).

FCLR-POOLED-AUDIT-001 is **complete** under `research_state/session_20261122T165200Z/` with all 11 `fclr_pooled_audit001_*` artifacts plus `evidence_audit_` and non-empty `trigger_check_`. Per RESEARCH_PROMPT.md §9 no position-sizing/risk overlay may be built (gate did not pass). Per §10 priority 8 the adversarial audit has been executed; per §15 Track B modeled boundary-breach labels were produced as a clearly-labeled modeled proxy (Track A exhausted). No further rank-0 campaign remains.


### 1a. Bottlenecks removed / verified clear (machine-checked)

1. **Rank-0 stale-state fixed.** `research_state/experiment_frontier.json` rank-0 `FCLR-POOLED-001-20261122T040000Z` was left `READY_EXECUTE`/`ACTIVE` despite being `CONFIRMATORY_COMPLETE` under `session_20261122T092003Z/` — demoted to rank 1 `SUPERSEDED_TERMINAL`/`COMPLETE` so no future agent re-executes finished work. The sole rank-0 campaign `FCLR-POOLED-AUDIT-001-20261122T120000Z` was executed under `session_20261122T165200Z/` and is likewise demoted to rank 1 `SUPERSEDED_TERMINAL`/`COMPLETE`; **no rank-0 `ACTIVE` entry remains**. No duplicate rank-0 deadlock.
2. **Pooled-audit gate armed and satisfied.** `scripts/check_handoff_heavywork_gate.py` binds `FCLR-POOLED-AUDIT-001` via `POOLED_AUDIT_CAMPAIGN_RE` (campaign start UTC `20261122T120000Z`); the post-start session `session_20261122T165200Z/` carries the full heavy audit artifact set (`fclr_pooled_audit001_prereg_` json+md, `fclr_pooled_audit001_audit_` py+json+md, `fclr_pooled_audit001_recompute_` py+json, `fclr_pooled_audit001_evidence_audit_` json+md, `evidence_audit_` json, non-empty `trigger_check_` json), all non-empty, under its own session dir. Zero-byte placeholders fail closed. The `FCLR-POOLED-001` bundle (13 `fclr_pooled001_*` artifacts) was carried forward into the same session dir so the pooled campaign binding is also satisfied.
3. **No blocked / inefficient sessions remain.** FCLR-POOLED-AUDIT-001 complete; FCLR-POOLED-001 confirmatory complete; NEXT-SOURCE-VERIFY-01 terminal; no external trigger or new source needed. All on-disk `session_*` dirs contain files (no empty dirs).
4. **Empty-session scan clear.** All 61 on-disk `research_state/session_*` directories contain files.
5. **No "verify-green-and-stop" escape hatch.** The gate fails closed for any session with UTC > `20261122T040000Z` that does not carry a full heavy artifact set under its own `session_<UTC>/`. Prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop sessions fail closed.
6. **3-block framing deadlock broken.** `next_campaign_status.py` reports `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` — TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing, NOT a statement about the data on disk. The pooled chronological OOS design (FCLR-POOLED-001) was feasible and executed on existing ironflow bulk data (18 months, 799 coins, ~15M aligned rows). Future agents cannot cite the 3-block exhaustion as a blocker.

### 1b. Next session confirmation (campaign complete; machine-enforced constraints remain)

`FCLR-POOLED-AUDIT-001` is complete. Per RESEARCH_PROMPT.md §9 the forecast gate did NOT pass, so **no position-sizing/risk-reduction overlay shall be built**. Per RESEARCH_PROMPT.md §10 priority 8 the adversarial audit has been executed; per §15 Track B modeled boundary-breach labels were produced as a clearly-labeled modeled proxy (Track A observed-liquidation labels remain exhausted: NO_NEW_ADMISSIBLE_SOURCE).

**Next session must:**
1. **Confirm the gate:** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK`, latest session = `session_20261122T165200Z/`, full heavy artifact set present and non-empty.
2. **Re-run gate unittests:** the 6 modules → 0 failures.
3. **Preserve the NOT_SUPPORTED null:** do not threshold-shop, do not relax the 2% materiality floor, do not build an overlay, do not start a new rank-0 campaign, do not wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`.
4. **Keep `research_state` root ≤ 500 md+json files; all artifacts under session dirs; no empty/zero-byte files.**

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (NOT a blocker)
```

### 1c. Heavy work enforced (campaign executed; gate verified)

`scripts/check_handoff_heavywork_gate.py` binds `FCLR-POOLED-AUDIT-001` via `POOLED_AUDIT_CAMPAIGN_RE` (campaign start UTC `20261122T120000Z`). The recorded latest session `session_20261122T165200Z/` (UTC > campaign start) carries the full heavy adversarial-audit artifact set with no zero-byte placeholders, and the gate → `PASS ... reason=OK`. A prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop session fails closed. Sessions with UTC ≤ `20261122T040000Z` (incl. `session_20261122T033000Z`) are grandfathered.

The gate ensures any future recorded session with UTC > `20261122T120000Z` must produce the full heavy artifact set or the gate fails closed; no rank-0 `ACTIVE` campaign remains, so there is no heavy campaign left to skip. Future agents cannot idle waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.


---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible evidence)

`scripts/next_campaign_status.py` reports `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` (re-verified this session), but that verdict is TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing. It is NOT a statement about the data on disk:

| Probe | Result |
|-------|--------|
| `research_state/data_cache/ironflow_bulk/candles_1h` | 18 monthly parquet files, 3,643,742 rows, up to 799 coins, 2025-05..2026-10 |
| `.../ironflow_bulk/funding` | 18 files, 4,104,648 rows, up to 494 coins |
| `.../ironflow_bulk/open_interest` | 18 files, 3,977,432 rows, up to 553 coins |
| `.../ironflow_bulk/liquidations` | 18 files, 2,849,452 rows, key on market/issuer (no coin column) |
| Adversarial audits on pooled panel | FEASIBLE TODAY — no new source, no network, no external trigger |
| Track B modeled boundary-breach labels | FEASIBLE TODAY from mark-price history + public margin params |

The exhausted-source frontier (NEXT-SOURCE-VERIFY-01 → NO_NEW_ADMISSIBLE_SOURCE) and the exhausted 3-block framing are both sidestepped by adversarial audits + Track B on existing data. Future agents cannot idle waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.

---

## 3. NON-AVOIDANCE CONSTRAINTS (machine-checked)

- **Do NOT** create root-level `research_state/*.md|*.json` — root count is **499/500**; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (the gate checks non-zero size).
- **Do NOT** claim completion without a full heavy artifact set under a new `session_<UTC>/` (UTC > `20261122T110000Z`), and without recording that session id in this handoff.
- **Do NOT** write a concrete future `session_<UTC>` id into this handoff before that directory exists — the gate treats the lexicographically latest recorded `session_` id as the session to verify and will fail if its directory is missing.
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as `NOT_SUPPORTED`.
- **Do NOT** re-run any terminal/completed campaign (incl. NEXT-SOURCE-VERIFY-01, LIVE-ARCHIVE-01/-02, FCLR-POOLED-001, and all earlier campaigns).
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.
- **Do NOT** re-verify that `data.binance.vision` is reachable — already exhausted by FCLR-LIVE-ARCHIVE-02.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the gate passes for a post-start session only when the full heavy artifact set is present and non-empty under the latest `session_<UTC>/`.
- **Do NOT** build a position-sizing/risk-reduction overlay — per RESEARCH_PROMPT.md §9, the forecast gate did not pass (NOT_SUPPORTED), so no overlay is eligible.
- **Do NOT** track-adulterate: never describe Track B (modeled breach) or Track C (volatility) performance as proof that actual liquidations were forecast.

---

## 4. FROZEN / ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

- **Ironflow bulk caches (the FCLR-POOLED-001 data source):** `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}/<YYYY-MM>.parquet` plus `<YYYY-MM>.parquet.sha256` and `<YYYY-MM>.accessed.json` sidecars, 18 months 2025-05..2026-10. Row counts and schemas per §1b/§2. Assert sha256 before reading; do NOT mutate the caches.
- **Combined liquidation panel (legacy, still frozen):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Not needed for the pooled audit; do not substitute it for the bulk data.
- **FCLR-001 panel (funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`; `premium` all-null; not needed for the pooled audit.

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
| FCLR-NEXT-SOURCE-VERIFY-01 | materially different verified free source + heavy 3-block confirmatory | SUPERSEDED_TERMINAL (session_20261122T033000Z; NO_NEW_ADMISSIBLE_SOURCE; confirmatory design FCLR-NEXT-CONFIRM-001 registered; decision GO; demoted to rank 2) |
| **FCLR-POOLED-001** | **pooled chronological OOS confirmatory on on-disk ironflow bulk data** | **CONFIRMATORY_COMPLETE — rank 1 SUPERSEDED_TERMINAL, gate-enforced; EXECUTED under session_20261122T092003Z; all 13 fclr_pooled_* artifacts present and non-empty; decision NOT_SUPPORTED (rel QLIKE ~0.0%, below -2% floor)** |
| **FCLR-POOLED-AUDIT-001** | **adversarial leakage/quality audits on pooled ironflow bulk panel + optional Track B modeled boundary-breach labels** | **COMPLETE — executed under session_20261122T165200Z; demoted to rank 1 SUPERSEDED_TERMINAL; gate-enforced via POOLED_AUDIT_CAMPAIGN_RE (start UTC 20261122T120000Z); all 11 fclr_pooled_audit001_* artifacts + evidence_audit_ + non-empty trigger_check_ present and non-empty under session_20261122T165200Z/; fclr_pooled001_* bundle (13 artifacts) carried forward; no rank-0 ACTIVE campaign remains** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this `AGENT_HANDOFF.md` with: (1) what changed and why; (2) what was tested with exact outcomes; (3) what evidence was added and where (full paths); (4) the state of each research gate; (5) the single highest-value next task; (6) the precise verifying command; (7) any blocker with the next materially different route. **(1) Executed FCLR-POOLED-AUDIT-001 under session_20261122T165200Z; demoted FCLR-POOLED-001 and FCLR-POOLED-AUDIT-001 to rank 1 SUPERSEDED_TERMINAL; no rank-0 ACTIVE campaign remains. (2) Gate PASS reason=OK (latest session = session_20261122T165200Z, pooled 13/13 + pooled_audit 11/11 artifacts present); 116/116 gate unittests 0 failures. (3) Evidence added under research_state/session_20261122T165200Z/: fclr_pooled_audit001_prereg_ (.json+.md), fclr_pooled_audit001_audit_ (.py+.json+.md), fclr_pooled_audit001_recompute_ (.py+.json), fclr_pooled_audit001_evidence_audit_ (.json+.md), evidence_audit_20261122T165200Z.json, trigger_check_20261122T165200Z.json, plus carried-forward fclr_pooled001_* bundle. (4) Gate state: check_handoff_heavywork_gate.py PASS reason=OK; root count 499/500 ≤ cap. (5) Single highest-value next task: confirm gate green and unittest suite green; preserve NOT_SUPPORTED; no new rank-0 campaign, no overlay. (6) Precise verifying command: python3 scripts/check_handoff_heavywork_gate.py && python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate. (7) Blocker: none — all campaigns terminal; frozen data cannot produce NEW_OBSERVED_LIQUIDATION_SOURCE.** Rank-0: FCLR-POOLED-001 (CONFIRMATORY_COMPLETE) — executed under session_20261122T092003Z; decision NOT_SUPPORTED; no overlay per §9 gate. All 13 artifacts under research_state/session_20261122T092003Z/ with the fclr_pooled_* family. FCLR-POOLED-AUDIT-001 (COMPLETE) — executed under session_20261122T165200Z/. Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK (latest session = session_20261122T165200Z; full heavy artifact set present and non-empty under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (does NOT cover the pooled audit — that is the point)
```

After the heavy session wrote its artifacts (UTC > `20261122T110000Z`) and recorded `session_20261122T165200Z/` in this handoff, `check_handoff_heavywork_gate.py` PASSES because the full heavy artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)