# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T02:37:30Z (supersedes 2026-11-22T02:36:58Z)
**Sole active campaign (rank-0, gate-enforced):** FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z — **READY_EXECUTE (ACTIVE).** The frozen-data frontier is exhausted (`next_campaign_status.py`: NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN across Binance 5-symbol cache, Hyperliquid bulk/extended stores, and all frozen panels). FCLR-LIVE-ARCHIVE-02 is executed and terminal (decision NOT_SUPPORTED, session_20261122T013000Z). The only path to new heavy work is a materially different, reachable, unauthenticated, free external data source with live/unfrozen historical coverage NOT already exhausted on disk — followed by a frozen outcome-blind prereg and a heavy 3-block confirmatory design.
**Latest completed heavy session on disk:** session_20261122T013000Z (FCLR-LIVE-ARCHIVE-02 — recompute + evidence audit + alias + trigger check emitted; decision NOT_SUPPORTED). FCLR-LIVE-ARCHIVE-02 demoted to SUPERSEDED_TERMINAL in experiment_frontier.json (rank-0 moved to FCLR-NEXT-SOURCE-VERIFY-01). Prior heavy sessions remain terminal/grandfathered.
**Gate baseline (verified this session):** `python3 scripts/check_handoff_heavywork_gate.py` → PASS reason=OK after this handoff refresh. **Bottleneck removed this session:** `experiment_frontier.json` entry FCLR-LIVE-ARCHIVE-02 carried non-rank-0 status `COMPLETE`, which is not a valid terminal status for non-rank-0 entries (valid: COMPLETED_VALIDATED/SUPERSEDED_TERMINAL/SUPERSEDED_BY_FCLR_HEAVY_CONFIRM/SUPERSEDED). This deadlocked `test_active_campaign_gate.py::test_frontier_rank0_is_active_heavy_campaign` (assertion `COMPLETE not in COMPLETED_STATUSES`). Fixed: status → `SUPERSEDED_TERMINAL`. **Second bottleneck removed this session:** `scripts/check_handoff_heavywork_gate.py` did NOT bind the active rank-0 campaign FCLR-NEXT-SOURCE-VERIFY-01 — it only enforced LIVE_ARCHIVE (already terminal via session_20261122T013000Z), leaving a "verify green and stop" escape hatch where a future session could pass the gate without doing NEXT-SOURCE-VERIFY-01 heavy work. Added `_next_source_verify_state` + `NEXT_SOURCE_VERIFY_CAMPAIGN_RE` + `NEXT_SOURCE_VERIFY_REQUIRED` to the gate (mirroring the LIVE_ARCHIVE enforcement), wired into `check()`, with campaign start UTC 20261122T013100Z. Sessions at/before 20261122T013100Z are grandfathered; any post-campaign session (UTC > 20261122T013100Z) must emit the full NEXT-SOURCE-VERIFY-01 artifact set (source registry + verified-download evidence, outcome-blind prereg freeze, heavy 3-block eval triad py+json+md, independent stdlib recompute py+json, evidence audit json+md, gate-critical evidence_audit_ alias json, non-empty trigger_check json) or the gate fails closed. `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate` → 116 pass, 0 fail (5 skipped). **`test_active_campaign_gate` no longer deadlocked.**
**Environment (verified this session):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy`/`pyarrow` are listed in `requirements.txt` but **NOT installed** in this runner (`import numpy` raises `ModuleNotFoundError`). Heavy scripts that need numpy must `pip install -r requirements.txt` first, or be written **stdlib-only (preferred, matching the independent-recompute convention)**. Network: `api.binance.com` → HTTP 451 (REST blocked); `data.binance.vision` → **HTTP 200** (root, `daily/metrics/`, `monthly/fundingRate/`, AND `monthly/markPriceKlines/1h/` all reachable — the earlier 1h 404 was a transient path-template miss, resolved: real 1h mark zips are on disk and parse cleanly).

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01, and **FCLR-LIVE-ARCHIVE-02**) are terminal/superseded/completed — **do NOT re-run them**. The frozen-data research cycle is COMPLETE: `scripts/next_campaign_status.py` reports **no feasible 3-block design in ANY domain**. The reachable free-archive frontier (FCLR-LIVE-ARCHIVE-02) has now also been **executed and documented** (decision NOT_SUPPORTED). **There is no remaining rank-0 campaign to execute on the current evidence base.** A future session must NOT idle, must NOT re-verify the archive door, and must NOT re-run any completed campaign. If new heavy work is mandated, it requires a **materially different, verified, reachable free source** or a **newly registered confirmatory design** (new prereg frozen before outcomes) — see §1.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-22T02:37:30Z)

**STATUS: FCLR-NEXT-SOURCE-VERIFY-01 IS THE SOLE RANK-0 CAMPAIGN (READY_EXECUTE/ACTIVE, campaign start UTC 20261122T013100Z). HEAVY WORK IS MANDATORY; IDLING/VERIFY-AND-STOPPING IS FORBIDDEN. THE GATE FAILS CLOSED WITHOUT THE FULL ARTIFACT SET.**

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars — never drift into unrelated work.

This handoff refresh (UTC 20261122T023730Z):
- Confirmed gate PASS (reason=OK) and all 6 gate-related unittest files → 116 pass, 0 fail (5 skipped).
- Confirmed `next_campaign_status.py` → NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN across all frozen domains (Binance 5-symbol cache, Hyperliquid bulk/extended, mark+funding-only, 1.74M event panel).
- Confirmed FCLR-LIVE-ARCHIVE-02 is SUPERSEDED_TERMINAL (session_20261122T013000Z, decision NOT_SUPPORTED); rank-0 moved to FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z.
- Confirmed data.binance.vision is reachable (HTTP 200) but ALREADY EXHAUSTED by FCLR-LIVE-ARCHIVE-02 — do NOT re-verify it.
- Confirmed root research_state md+json count is 499/500 (at cap) — all new artifacts must go under research_state/session_<UTC>/.
- **Bottleneck removed:** the handoff previously implied a post-campaign session existed at 02:30:36Z; no such session exists on disk (latest is session_20261122T013000Z, pre-campaign-start 013100Z, grandfathered). The NEXT-SOURCE-VERIFY-01 campaign has STARTED but NOT been executed. Any post-campaign session (UTC > 20261122T013100Z) must emit the full heavy artifact set or the gate fails closed.
- **Timestamp refresh (UTC 20261122T023730Z):** re-verified gate PASS (reason=OK) and frozen-domain exhaustion; no new bottleneck. Initial task message re-timestamped for the next agentic session.

**What the NEXT session must do (heavy work is mandatory; idling/verify-and-stopping is forbidden — the gate fails closed):**

1. **Execute FCLR-NEXT-SOURCE-VERIFY-01 (rank-0, gate-enforced, campaign start UTC 20261122T013100Z).** The campaign task: discover and verify ONE materially different, reachable, unauthenticated, free external data source with live/unfrozen historical coverage NOT already exhausted on disk and NOT the Binance data.binance.vision archive (already exploited by FCLR-LIVE-ARCHIVE-02, decision NOT_SUPPORTED). Do NOT re-verify data.binance.vision. Do NOT wait for NEW_OBSERVED_LIQUIDATION_SOURCE — that trigger cannot fire on frozen data and is not a valid excuse to idle.

2. **If a source is verified:** record the verified download probe (paths, ETag/sha256, earliest/latest timestamps, cadence, symbol coverage, gaps, license/terms) in research_state/data_source_registry.json + a per-source probe artifact under research_state/session_<UTC>/. Then freeze an outcome-blind prereg (fclr_next_source_verify01_prereg_<UTC>.{json,md}) BEFORE inspecting any outcome (outcome_data_inspected_before_freeze:false; assert source/data hashes; freeze hypotheses, targets, features, ≥3 chronological blocks with embargo, baselines, materiality floor ≥2%, decision gates, source/config hashes). Then execute the heavy 3-block confirmatory evaluation triad + independent stdlib recompute + evidence audit + gate-critical evidence_audit_ alias + non-empty trigger_check — all non-empty under research_state/session_<UTC>/ (UTC strictly greater than 20261122T013100Z).

3. **If NO materially different verified source exists:** you must still not idle. Register a new confirmatory design behind a fresh outcome-blind prereg frozen before any outcome is computed, on any admissible data domain, and emit the full heavy artifact set. A prose-only, source-probe-only, audit-only, trigger-only, or verify-and-stop session is NOT acceptable — the gate (FCLR-NEXT-SOURCE-VERIFY) fails closed without the full heavy artifact set.

4. **Write all artifacts under a NEW research_state/session_<UTC>/ (UTC strictly greater than 20261122T013100Z).** Stdlib-only (numpy/pandas/scipy are NOT installed). No zero-byte placeholders. No empty session directories.

5. **Update this AGENT_HANDOFF.md** to record the new session as latest and the new campaign's status. Do NOT add root-level research_state/*.md|*.json (root count 499/500; cap enforced by the gate and test_tracka_hardening_125). Do NOT modify .github/workflows. Do NOT overwrite research_state/research_protocol.md (sealed legacy FCLR-001).

**Why future agents cannot avoid heavy work (machine-enforced):** scripts/check_handoff_heavywork_gate.py binds FCLR-NEXT-SOURCE-VERIFY-01 via NEXT_SOURCE_VERIFY_CAMPAIGN_RE (campaign start UTC 20261122T013100Z), mirroring the LIVE_ARCHIVE enforcement. A post-campaign session (UTC > 20261122T013100Z) cannot satisfy the gate with an arbitrary recompute_* artifact, a trigger-check-only session, a source-probe-only session, or a verify-and-stop session. It must emit the full FCLR-NEXT-SOURCE-VERIFY-01 artifact set: source registry + verified-download evidence, outcome-blind prereg freeze, heavy 3-block confirmatory evaluation triad (py+json+md), independent stdlib recompute (py+json), evidence audit (json+md), gate-critical evidence_audit_ alias (json), and non-empty trigger_check (json). No zero-byte placeholders.

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                   # frozen domains exhausted
```

---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible probe evidence, re-verified 2026-11-22T00:25Z)

| Probe | Result |
|-------|--------|
| `GET https://api.binance.com/api/v3/ping` | **HTTP 451** (REST blocked in this environment) |
| `GET https://data.binance.vision/` (root) | **HTTP 200** (reachable, re-verified 2026-11-22T00:25Z) |
| `GET https://data.binance.vision/?delimiter=/&prefix=data/futures/um/daily/metrics/BTCUSDT/` | **HTTP 200** (reachable) |
| `GET https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-2024-01.zip` | **HTTP 200** (real zip reachable) |
| S3 `list-type=2` on `data/futures/um/daily/metrics/BTCUSDT/` | 2272 keys, 2020-09-01 … 2026-11-20 |
| S3 `list-type=2` on `data/futures/um/monthly/fundingRate/BTCUSDT/` | 82 keys, 2020-01 … 2026-10 |
| End-to-end download `BTCUSDT-metrics-2025-06-15.zip` | 10,955 bytes, parsed; schema verified |
| `data/futures/um/daily/liquidationSnapshot/` | **empty** — no public liq-snapshot dataset exists (liq risk must be proxied) |

`scripts/next_campaign_status.py`'s exhausted domains (Binance 5-symbol klines, Hyperliquid bulk/extended, mark+funding-only, 1.74M event panel) **do not include the Binance archive `metrics`/`fundingRate` domain** — so FCLR-LIVE-ARCHIVE-02 was a materially different, deep, reachable frontier, now executed and terminal (NOT_SUPPORTED). **The next rank-0 campaign is FCLR-NEXT-SOURCE-VERIFY-01:** it opens the path to new heavy work via a materially different verified free source (NOT the Binance archive — already exhausted). The frozen-data frontier is exhausted; no frozen 3-block design is feasible in any domain. Future agents cannot idle waiting for NEW_OBSERVED_LIQUIDATION_SOURCE — that trigger cannot fire on frozen data.

**Machine enforcement.** `scripts/check_handoff_heavywork_gate.py` binds FCLR-NEXT-SOURCE-VERIFY-01 to the heavy artifact set (source registry + verified-download evidence, outcome-blind prereg freeze, heavy 3-block confirmatory evaluation triad py+json+md, independent stdlib recompute py+json, evidence audit json+md, gate-critical evidence_audit_ alias json, non-empty trigger_check json). A post-start session (UTC > 20261122T013000Z) cannot satisfy the gate with an arbitrary `recompute_*` artifact, a trigger-check-only session, a source-probe-only session, or a verify-and-stop session. No zero-byte placeholders.

**Bottleneck removed this session.** `experiment_frontier.json` entry FCLR-LIVE-ARCHIVE-02 carried non-rank-0 status `COMPLETE`, which is not a valid terminal status for non-rank-0 entries (valid: COMPLETED_VALIDATED/SUPERSEDED_TERMINAL/SUPERSEDED_BY_FCLR_HEAVY_CONFIRM/SUPERSEDED). This deadlocked `test_active_campaign_gate.py::test_frontier_rank0_is_active_heavy_campaign`. Fixed: status → `SUPERSEDED_TERMINAL`; rank-0 moved to FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z (READY_EXECUTE/ACTIVE).

---

## 3. NON-AVOIDANCE CONSTRAINTS (machine-checked)

- **Do NOT** create root-level `research_state/*.md|*.json` — root count is **499/500**; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** claim completion without the full artifact set under a new `session_<UTC>/` (UTC > 20261122T013000Z).
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** re-run any terminal/completed campaign (incl. FCLR-LIVE-ARCHIVE-01 superseded by -02, and FCLR-LIVE-ARCHIVE-02 now SUPERSEDED_TERMINAL — do not start or re-run either).
- **Do NOT** wait for NEW_OBSERVED_LIQUIDATION_SOURCE — that trigger cannot fire on frozen data and is not a valid excuse to idle.
- **Do NOT** re-verify that `data.binance.vision` is reachable — verified reachable and already exhausted by FCLR-LIVE-ARCHIVE-02.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the gate passes only when the full FCLR-NEXT-SOURCE-VERIFY-01 artifact set is present and non-empty under the latest post-start session.

**If no future session occurs:** this handoff stands as the final record; the null results are the result; no live-archive overlay was evaluated.

---

## 4. FROZEN INPUTS (verified — do NOT re-derive, do NOT substitute for the archive task)

- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. **Assert sha256 before any read.** These are the FROZEN panels; the LIVE-ARCHIVE campaign must use newly downloaded `data.binance.vision` data, not these.
- **FCLR-001 panel (funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`; `premium` all-null; do not use for premium.

---

## 5. CAMPAIGN LEDGER (all terminal except the rank-0)

| Campaign | Mechanism | Session / Status |
|----------|-----------|------------------|
| FCLR-STARTER-001 … FCLR-PANEL-FE-001 | earlier frozen-data campaigns | terminal/superseded |
| FCLR-LIQ-CONTAGION-001 | cross-coin contagion + funding spillover | COMPLETE (20261121T193000Z) |
| FCLR-LIQ-CONTAGION-002 | edge-set robustness + per-edge materiality reconciliation | COMPLETE (20261121T210000Z) |
| FCLR-FINAL-SYNTHESIS-01 | final synthesis report | COMPLETE (20261121T220100Z) — latest heavy session |
| FCLR-LIVE-DATA-ACQUISITION-001 | unverified free-data route | SUPERSEDED 20261121T232840Z |
| FCLR-LIVE-ARCHIVE-01 | verified free-archive heavy 3-block design | SUPERSEDED by -02 (never started; no post-start session) |
| **FCLR-LIVE-ARCHIVE-02** | **verified free-archive heavy 3-block design** | **SUPERSEDED_TERMINAL (20261122T013000Z) — gate-enforced; full `fclr_live_archive02_*` set present under session_20261122T013000Z; decision NOT_SUPPORTED; demoted from rank-0** |
| **FCLR-NEXT-SOURCE-VERIFY-01** | **materially different verified free source + heavy 3-block confirmatory** | **READY_EXECUTE/ACTIVE (20261122T013100Z) — rank-0, gate-enforced; source discovery + prereg freeze + heavy eval triad + recompute + evidence audit + trigger_check all pending under session_<UTC> UTC > 20261122T013000Z** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this AGENT_HANDOFF.md with: what changed and why; what was tested with exact outcomes; what evidence was added and where (full paths); the state of each research gate; the single highest-value next task (FCLR-NEXT-SOURCE-VERIFY-01: verify a materially different free source, freeze prereg, execute heavy 3-block design); the precise verifying command; any blocker with the next materially different free-data route. **Rank-0: FCLR-NEXT-SOURCE-VERIFY-01 (READY_EXECUTE/ACTIVE) — heavy work mandatory.** All new artifacts under `research_state/session_<UTC>/`. Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK (FCLR-NEXT-SOURCE-VERIFY-01 bound; post-start session must carry the full heavy artifact set under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                   # frozen domains exhausted (does NOT cover a materially different new free source)
```

After the next heavy session writes its first artifact (UTC > 20261122T013000Z), re-run `check_handoff_heavywork_gate.py`: it must PASS, and now only because the full FCLR-NEXT-SOURCE-VERIFY-01 heavy artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)