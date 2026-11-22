# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T13:38:27Z (supersedes 2026-11-22T13:37:16Z)
**Session type:** handoff refresh — single durable handoff; sole rank-0 ACTIVE campaign `FCLR-POOLED-AUDIT-001-20261122T120000Z` (NOT_STARTED), gate-enforced. Gate PASS reason=OK; root 499/500; 116/116 gate unittests pass; no blocked/inefficient sessions; no empty session dirs; latest disk session = latest recorded handoff session (`session_20261122T092003Z`).

**Sole active campaign (rank-0, gate-enforced):** `FCLR-POOLED-AUDIT-001-20261122T120000Z` — **NOT_STARTED (ACTIVE)**. Adversarial leakage/quality audits on the pooled ironflow bulk panel, with optional Track B modeled boundary-breach labels. Executable today on data already on disk: no new source, no network, no external trigger. The prior `FCLR-POOLED-001-20261122T040000Z` is CONFIRMATORY_COMPLETE (executed under `session_20261122T092003Z`, decision NOT_SUPPORTED) and demoted to rank 1 SUPERSEDED_TERMINAL. No other rank-0 entry exists.

**Latest completed heavy session on disk:** `session_20261122T092003Z` — executed FCLR-POOLED-001 to completion with all 13 `fclr_pooled_*` artifacts (decision NOT_SUPPORTED; funding-conditioned features add no QLIKE improvement over RV-only baseline). All earlier sessions remain terminal/grandfathered.

**Gate baseline (verified this session, 2026-11-22T13:38:27Z):** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK` (`latest_handoff=session_20261122T092003Z`, `latest_disk=session_20261122T092003Z`, `handoff_stale=False`, `pooled.required=True` 13/13 artifacts present, `root=499/500`); all 6 gate unittest modules (`test_tracka_hardening_143`, `test_tracka_hardening_144`, `test_active_campaign_gate`, `test_fclr_heavy_confirm_gate`, `test_fclr_campaign_gate`, `test_fclr_starter_001_campaign_gate`) → **116 tests, 0 failures**; `research_state` root md+json count = **499/500**; latest on-disk session = latest recorded in this handoff (`session_20261122T092003Z`); no empty session directories (60 session dirs scanned); no `fclr_pooled_audit*` artifacts on disk yet (campaign not started). On-disk ironflow bulk caches: candles_1h/funding/open_interest/liquidations each **18 parquet files + 18 sha256 sidecars + 18 accessed.json** (2025-05..2026-10, 54 files per dataset).

**Environment (verified):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy` NOT installed (`ModuleNotFoundError`). `pyarrow` 26.0.1 installed — reads ironflow bulk parquet. Use stdlib + pyarrow only. Do NOT rely on numpy/pandas/scipy.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001/002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01/02, FCLR-NEXT-SOURCE-VERIFY-01, FCLR-POOLED-001) are terminal / superseded / completed — **do NOT re-run them**. The reachable-free-source frontier (NEXT-SOURCE-VERIFY-01) is executed and terminal (NO_NEW_ADMISSIBLE_SOURCE). **FCLR-POOLED-001 is CONFIRMATORY_COMPLETE** — executed under `session_20261122T092003Z` with all 13 `fclr_pooled_*` artifacts; decision NOT_SUPPORTED. A future session must NOT re-run this completed campaign; per §9, no risk overlay should be built since the forecast gate did not pass.

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars (RESEARCH_PROMPT.md §Mission/§3). Never drift into unrelated work, risk overlays, or live/paper trading.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-22T13:38:27Z)

> **READ THIS FIRST — THIS IS THE ONLY TASK YOU MAY START. DO NOT DEVIATE.**
>
> Repo = **Funding-conditioned-volatility-and-liquidation-risk**. Ranked by repo name, the single
> highest-value unfinished task is the **adversarial leakage/quality audit of the pooled
> funding/volatility/liquidation panel**, because the pooled confirmatory forecast came back
> **NOT_SUPPORTED** and the research program's next priority (RESEARCH_PROMPT.md §10 priority 8) is to
> attack the result before any further modeling. Everything else is terminal.
>
> **DO — execute campaign `FCLR-POOLED-AUDIT-001-<UTC>` under a NEW `research_state/session_<UTC>/`:**
> - UTC MUST be > `20261122T110000Z` (the pooled-audit campaign start). The lexicographically-latest
>   `session_<UTC>` directory on disk at the end MUST equal the one recorded in this handoff.
> - Produce the FULL `fclr_pooled_audit_*` artifact set (11 required artifacts, see §1b) — all non-empty.
> - No new source, no network, no external trigger — all inputs are already on disk (§4).
>
> **DO NOT:**
> - Idle, wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` (cannot fire on frozen data), or claim exhaustion.
> - Re-run any terminal/completed campaign (incl. FCLR-POOLED-001, NEXT-SOURCE-VERIFY-01, LIVE-ARCHIVE-01/-02).
> - Build a risk overlay (§9 gate NOT passed — NOT_SUPPORTED is preserved as the verdict).
> - Write root-level `research_state/*.md|*.json` (root=499/500, cap=500) — all artifacts go under `session_<UTC>/`.
> - Create empty/zero-byte placeholder files or empty session dirs.
> - Stop after prose-only, verify-only, trigger-only, source-probe-only, or audit-only output — the gate fails closed.
> - Threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
>
> **DONE WHEN:**
> - `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK`, with the new
>   `session_<UTC>/` recorded in this handoff and its full heavy artifact set present and non-empty.
> - All 6 gate unittest modules → 0 failures.
> - `research_state` root md+json count ≤ 500.

**STATUS: FCLR-POOLED-001 CONFIRMATORY_COMPLETE — NEXT HEAVY CAMPAIGN IS MANDATORY AND NON-AVOIDABLE.**

FCLR-POOLED-001 (pooled chronological OOS confirmatory on the on-disk ironflow bulk data, 18 months 2025-05..2026-10, 799 markets, ~2.3M train / ~1.3M test rows) is **complete** under `research_state/session_20261122T092003Z/` (UTC `20261122T092003Z` > campaign start `20261122T040000Z`). All 13 `fclr_pooled_*` artifacts are present and non-empty. Verdict: **NOT_SUPPORTED** — funding-conditioned features add no predictive value over the RV-only baseline (QLIKE B1=65.190573 vs C2=65.190702, diff +0.000129, rel +0.0002%, far below the −2.0% materiality floor; bootstrap CI95 includes zero). Null preserved. Independent stdlib recompute concurs (QLIKE_B1=52.945004, QLIKE_C2=52.944664, rel −0.0006%, NOT_SUPPORTED).

**The next session MUST execute `FCLR-POOLED-AUDIT-001-<UTC>`** — the adversarial leakage/quality audit of the pooled ironflow panel, with optional Track B modeled boundary-breach label construction. Per RESEARCH_PROMPT.md §9 the forecast gate did NOT pass, so **no position-sizing/risk overlay may be built**. Per RESEARCH_PROMPT.md §10 priority 8, adversarial audits are the next-highest-value task; per §15, Track B (modeled hypothetical boundary-breach labels) is the viable liquidation-risk path since Track A (observed liquidation labels) is exhausted (NO_NEW_ADMISSIBLE_SOURCE). Future agents cannot idle, cannot cite 3-block exhaustion, and cannot wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — the audit is executable today on data already on disk with no new source, no network, no external trigger.

### 1a. Bottlenecks removed / verified clear (machine-checked)

1. **Rank-0 stale-state fixed.** `research_state/experiment_frontier.json` rank-0 `FCLR-POOLED-001-20261122T040000Z` was left `READY_EXECUTE`/`ACTIVE` despite being `CONFIRMATORY_COMPLETE` under `session_20261122T092003Z/` — demoted to rank 1 `SUPERSEDED_TERMINAL`/`COMPLETE` so no future agent re-executes finished work. The sole `rank:0` `ACTIVE` entry is now `FCLR-POOLED-AUDIT-001-20261122T120000Z`. No duplicate rank-0 deadlock.
2. **Pooled-audit gate armed.** `scripts/check_handoff_heavywork_gate.py` binds `FCLR-POOLED-AUDIT-001` via `POOLED_AUDIT_CAMPAIGN_RE` (campaign start UTC `20261122T110000Z`); any session with UTC > `20261122T110000Z` must carry the full heavy audit artifact set under its own `session_<UTC>/`: `fclr_pooled_audit_prereg_` (.json+.md), `fclr_pooled_audit_audit_` (.py+.json+.md), `fclr_pooled_audit_recompute_` (.py+.json), `fclr_pooled_audit_evidence_audit_` (.json+.md), `evidence_audit_` (.json), and non-empty `trigger_check_` (.json). Zero-byte placeholders fail closed.
3. **No blocked / inefficient sessions remain.** FCLR-POOLED-001 complete; NEXT-SOURCE-VERIFY-01 terminal; no external trigger or new source needed. All 60 on-disk `session_*` dirs contain files (no empty dirs).
4. **Empty-session scan clear.** All 60 on-disk `research_state/session_*` directories contain files.
5. **No "verify-green-and-stop" escape hatch.** The gate fails closed for any session with UTC > `20261122T040000Z` that does not carry a full heavy artifact set under its own `session_<UTC>/`. Prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop sessions fail closed.
6. **3-block framing deadlock broken.** `next_campaign_status.py` reports `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` — TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing, NOT a statement about the data on disk. The pooled chronological OOS design (FCLR-POOLED-001) was feasible and executed on existing ironflow bulk data (18 months, 799 coins, ~15M aligned rows). Future agents cannot cite the 3-block exhaustion as a blocker.

### 1b. What the NEXT session MUST do (non-avoidable, machine-enforced)

FCLR-POOLED-001 is **complete**. Per RESEARCH_PROMPT.md §9 (gate before any risk overlay), the forecast gate did NOT pass (NOT_SUPPORTED), so **no position-sizing/risk-reduction overlay shall be built**. The next highest-value task per RESEARCH_PROMPT.md §10 priority 8 is **adversarial audits**: challenge timestamping, delisting, missingness, market stress concentration, survivorship, label construction, threshold drift, and overlapping outcomes. Also per RESEARCH_PROMPT.md §15, **Track B** (modeled hypothetical boundary-breach labels) is now the viable liquidation-risk path since Track A (observed liquidation labels) is exhausted (NO_NEW_ADMISSIBLE_SOURCE).

**Next focus campaign (mandatory, non-avoidable):** `FCLR-POOLED-AUDIT-001-<UTC>` — adversarial leakage/quality audits on the pooled ironflow bulk panel, with optional Track B modeled boundary-breach label construction.

**Required next actions (all under a NEW `research_state/session_<UTC>/` with UTC > `20261122T110000Z`):**

1. **Adversarial audits (priority 8, RESEARCH_PROMPT.md §10):** Execute and emit non-empty artifacts (py+json+md per audit domain) for:
   - Future-row perturbation cannot change earlier features/forecasts
   - Split embargo integrity (purge ≥ max horizon)
   - Funding sign/timing (publication vs settlement) handling
   - Mark/index alignment under frozen tolerance
   - Missingness preservation (no zero-fill/forward-fill)
   - Delisting/symbol-migration identity
   - Survivorship (today's survivors ≠ historical universe)
   - Market stress concentration (one coin/crisis driving result)
   - Threshold drift
   - Overlapping outcomes across horizons

2. **Track B modeled boundary-breach labels (RESEARCH_PROMPT.md §15):**
   - Use public historical mark-price data + documented publicly verifiable contract/margin parameters
   - Predefine hypothetical leverage/margin scenarios
   - Calculate whether observed mark-price path crosses modeled boundary
   - Clearly label as modeled breach proxy, NEVER as observed liquidation

3. **Document the NOT_SUPPORTED null result** in `research_state/negative_results_report.md` (new session dir; `fclr_pooled_*` family not required — this is a different artifact family).

4. **Verify gate passes:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS.

5. **Run gate unittests:** `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate` → 0 failures.

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (NOT a blocker — pooled design is the point)
```

### 1c. Why future agents CANNOT avoid heavy work (machine-enforced)

`scripts/check_handoff_heavywork_gate.py` binds `FCLR-POOLED-AUDIT-001` via `POOLED_AUDIT_CAMPAIGN_RE` (campaign start UTC `20261122T110000Z`). Any session with UTC > `20261122T110000Z` that is recorded in this handoff must carry the full heavy adversarial-audit artifact set under its own `session_<UTC>/` with no zero-byte placeholders. A prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop session fails closed. Sessions with UTC ≤ `20261122T040000Z` (incl. `session_20261122T033000Z`) are grandfathered.

Future agents cannot idle waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle. The next focus campaign (`FCLR-POOLED-AUDIT-001`) is executable today on data already on disk: no new source, no network, no external trigger. The gate ensures the next recorded session MUST produce heavy adversarial-audit artifacts or the gate fails closed.

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
| **FCLR-POOLED-AUDIT-001** | **adversarial leakage/quality audits on pooled ironflow bulk panel + optional Track B modeled boundary-breach labels** | **NOT_STARTED — rank-0 ACTIVE, next focus campaign; machine-enforced via gate POOLED_AUDIT_CAMPAIGN_RE (start UTC 20261122T110000Z); no prose-only/audit-only/verify-and-stop escape** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this `AGENT_HANDOFF.md` with: (1) what changed and why; (2) what was tested with exact outcomes; (3) what evidence was added and where (full paths); (4) the state of each research gate; (5) the single highest-value next task; (6) the precise verifying command; (7) any blocker with the next materially different route. **Rank-0: FCLR-POOLED-001 (CONFIRMATORY_COMPLETE) — executed under session_20261122T092003Z; decision NOT_SUPPORTED; no overlay per §9 gate.** All 13 artifacts under `research_state/session_20261122T092003Z/` with the `fclr_pooled_*` family. **Sole rank-0 ACTIVE: FCLR-POOLED-AUDIT-001-20261122T120000Z (NOT_STARTED) — adversarial audits + optional Track B modeled boundary-breach labels.** Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK (FCLR-POOLED-AUDIT-001 bound; post-start session must carry a full heavy artifact set under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (does NOT cover the pooled audit — that is the point)
```

After the next heavy session writes its first artifact (UTC > `20261122T110000Z`) and records the new `session_<UTC>/` in this handoff, re-run `check_handoff_heavywork_gate.py`: it must PASS, and now only because the full heavy artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)