# AGENT_HANDOFF.md — SINGLE DURABLE INITIAL TASK (NEXT SESSION)

**TIMESTAMP (UTC):** 2026-11-07T00:32:30Z (refreshed; supersedes conflicting prior handoff text)
**REPO (priority):** Funding-conditioned-volatility-and-liquidation-risk — focus on **funding-conditioned volatility** (Gate 4) first; **liquidation risk** remains blocked/guarded (no trigger).
**AUTHORITY:** This file is the single durable handoff. If `research_state/FCLR_CAMPAIGN_NEXT.md` or frontier entries conflict, follow this file; record reconciliation in artifacts.

## VERIFIED STATE (this session, 2026-11-07T00:32:30Z)
- Git: clean `main` @ `8e0d7aee` (HEAD). No workflow changes.
- `scripts/tracka_resume_check.py`: **pass:true**, 17/17 checks, `network:false`, `writes_real_research_state:false`.
- `scripts/tracka_resume_gate.py`: **BLOCKED** `PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `fail_closed_order=drift_preflight->manifest_prereg`, `outcomes_inspected:false`.
- Recent hardening tests: `tests.test_tracka_hardening_{131,132,136,137}` **36 OK** (12.0s). `test_fclr010_harness` **OK**.
- Full-suite status in this runner: **not fully re-verified this session** (env lacks numpy/pandas for some paths; prior campaign claims 709 OK in deps env). Do not fabricate counts; run `python -m unittest discover tests` in a deps-complete env and report exact outcome.
- Bounds: `research_state/` root `*.md|*.json` **146**, ironflow probes **2** (<=163/==2). No new probe/scan families created.
- Track A trigger: **NO TRIGGER** — Hyperliquid/ironflow `data_through 2026-10`; `2026-11..2027-02` absent; **probing exhausted**. **DO NOT re-probe absent months.**
- Track C/B context preserved in frontier/gate artifacts (sealed/NOT_SUPPORTED as recorded). Do not reopen sealed claims.

## BOTTLENECKS REMOVED / AMBIGUITIES RESOLVED
- Normalized `research_state/experiment_frontier.json`: `FCLR-NEXT-131` frontier-list status corrected to `COMPLETE`; stale `next_action_heavy` pointing to missing `FCLR-NEXT-132` replaced with handoff-directed instruction. `handoff_refreshed_utc=20261107T003230Z`.
- `AGENT_HANDOFF.md` (root) vs `FCLR_CAMPAIGN_NEXT.md` (Track A lockdown, FCLR-NEXT-139) conflict: **resolved by prioritizing repo name** — Gate 4 funding ablations are the highest-value *unblocked* heavy work with local data; Track A remains blocked and guarded (hardening continues only when naming a specific uncovered gap with measurable tmp-isolated tests, no status-only churn).

## SINGLE MANDATORY HEAVY-WORK CAMPAIGN (NO COASTING)
Future sessions must complete the next unfinished deliverable below with **code + artifacts + exact command outcomes**. Status-only memos are non-compliant.

### P0 — PHASE 3: FUNDING-CONDITIONED VOLATILITY ABLATIONS (GATE 4)
**Goal:** Honest, leakage-resistant comparison of funding-conditioned models vs RV-only HAR (B2) on the same walk-forward splits/panel.

**Known issue to fix:** `research_state/evaluation_summary.md` “Funding Ablations (Gate 4)” shows a broken pilot (B–E `None`, absurd QLIKE/MAE magnitudes for A). Treat that pilot as **invalid/inconclusive**; do not cite it as evidence. Replace with a correct, reproducible run.

**Required steps (execute, verify, record):**
1. **Env/deps:** `pip install -r requirements.txt` (numpy/pandas/scipy). If deps unavailable, record exact blocker + run dep-light checks; do not claim ablation results.
2. **Data (local only):** Load BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT 1h klines 2024-01..03 and matching `*fundingRate*` zips. Align funding to 1h grid (document method; forward-fill only where justified, preserve gaps). **Missing basis/spot = NaN, never zero.** Preserve signed funding and `|funding|`.
3. **Features (train-only stats where applicable):** Use/extend `src/features/funding.py`, `src/volatility/feature_engineering.py` (trailing percentile/zscore windows as feasible). No lookahead; no full-sample normalization.
4. **Ablations vs B2 on identical chronological splits (purge/embargo >=7d):** A=RV-only (reconfirm), B=RV+signed funding, C=RV+|funding|, D=RV+signed+|funding| (+ basis/premium only if real coverage; else omit and state). Keep target definition consistent (forward RV horizon as in baseline; document if changed).
5. **Metrics:** QLIKE primary; MAE/RMSE secondary; **Δ vs B2** per ablation/split and aggregate; n, coverage, drop reasons. If sample/blocks insufficient for confirmatory claims, label **PILOT/INCONCLUSIVE** explicitly.
6. **Artifacts (update, not status-only):** `research_state/evaluation_summary.md` (correct Gate 4 table + narrative), `research_state/run_manifest.json` (run id, SHA, config hash/params, sample counts, status), `research_state/leakage_audit.md` (funding alignment/timing checks). Add/extend tests for funding alignment + no-lookahead if logic changes.
7. **Acceptance commands (report actual results):** `pip install -r requirements.txt`; `python -m unittest discover tests` (or scoped); `python scripts/run_rv_baseline.py` (if used) and/or new `scripts/run_funding_ablations.py`; `python scripts/tracka_resume_check.py`.

### P1 — TRACK A LIQUIDATION RISK (BLOCKED; GUARDED RESUME ONLY)
- **No trigger → no re-probe, no outcome inspection.** Maintain `resume_check`/gate invariants (17/17, probes==2, bounds).
- **If trigger appears:** PREREG before inspecting outcomes. Hyperliquid-only admissible path; manifest-only checks first; never conflate observed vs modeled; pass guarded seam + drift/admissible gates before any data load; record hashes/timestamps/provenance.
- Optional hardening only if a **specific uncovered gap** is named with a new tmp-isolated test (no network/parquet/outcome reads, no real `research_state` writes, no new families). Do not resume 131/132/139 numbering without creating the referenced artifacts coherently.

### P2 — PHASE 4 (AFTER GATE 4 RECORDED)
Track B modeled breaches (explicit assumptions) / Track A observed liquidations only when admissible data+prereg exist. Keep A/B/C separated.

## CONSTRAINTS (NON-NEGOTIABLE)
- **NO TRADING/CREDS/PAID DATA** — local files only; no auth/bypass.
- **NO WORKFLOW CHANGES** — never touch `.github/workflows/`.
- **LEAKAGE-RESISTANT** — chronological only, purge/embargo, train-only normalization/stats.
- **MISSING != ZERO**; **TRACK SEPARATION** (observed ≠ modeled ≠ volatility).
- **HEAVY WORK REQUIRED** — every session produces a measurable delta (code/tests/run/artifact) or an evidence-backed blocker + next materially different route.
- **PREREG BEFORE OUTCOMES** for any confirmatory/trigger evaluation.

**START NOW:** P0 Step 1 (deps + load/align funding). Do not stop after reading; implement and report.
