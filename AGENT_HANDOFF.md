# AGENT_HANDOFF.md — SINGLE DURABLE INITIAL TASK (NEXT SESSION)

**TIMESTAMP (UTC):** 2026-11-07T02:21:24Z
**REPO (priority):** `Funding-conditioned-volatility-and-liquidation-risk` — **P0 = funding-conditioned volatility (Gate 4)** using local admissible data. **Liquidation risk (Track A) = BLOCKED/GUARDED, no trigger** — do not resume Track A probing/outcome inspection.
**AUTHORITY:** This file is the **only** durable session handoff. If `research_state/FCLR_CAMPAIGN_NEXT.md`, frontier entries, or stale notes conflict, follow this file and record reconciliation in durable artifacts (not status-only files).

## VERIFIED STATE (2026-11-07T02:21:24Z)
- Git HEAD: `ba032422` (`chore(kilo): checkpoint agent session`) on `main`. Working tree has local changes: `scripts/run_funding_ablations.py` (fixed), `tests/test_funding_ablations.py` (rewritten, 6 tests), `tests/__init__.py` (new), tracked `__pycache__/*.pyc` removed from index (`git rm --cached` cleanup; `.gitignore` already ignores `__pycache__/`/`*.pyc`), and minor artifact timestamp churn from rerunning ablations (`research_state/evaluation_summary.md`, `evaluation_summary_funding.md`, `run_manifest.json`, `leakage_audit.md`). **No workflow changes.**
- `scripts/tracka_resume_check.py`: **pass:true, 17/17**, `network:false`, `writes_real_research_state:false`.
- `python -m unittest tests.test_funding_ablations -v`: **6/6 OK** (no-duplicate-merge-columns, Gate 3 A_rv_only QLIKE reproduces 1.5954100026198477, all ablations finite, bounded predictions, funding alignment no-future-leakage, trailing pct past-only).
- `python scripts/run_funding_ablations.py` (reproducible): `{"A_rv_only":1.59541000261996,"B_rv_signed":1.4392367821430467,"C_rv_abs":1.4392367821430467,"D_rv_signed_abs":1.4392367821409628,"E_rv_funding_trails":1.0644322409593807}`
- Full suite baseline (prior verified run this cycle): **717 tests, 8 pre-existing failures** — all Track A scope/registry-drift hardening (`test_tracka_hardening_114`–`129`, unregistered `_debug_*.py` vs `tracka_script_scope_registry.json`). **Unrelated to Gate 4; Track A is blocked — do not “fix” by resuming Track A.** Expect the same 8 unless intentionally addressed as a separate, evidence-backed Track A hardening task under lockdown rules.
- Deps: `pip install -r requirements.txt` (numpy/pandas/scipy). Data: **local only** — BTC/ETH/SOL/XRP 1h klines + fundingRate, 2024-01..03 under `data/raw` (372 CSV). Missing = NaN, never zero. **No creds, no paid data, no bypass, no re-probe of absent months.**
- Bounds/invariants: research_state root file count maintained; ironflow probes == 2; no new probe/scan families.

## GATE 4 (funding-conditioned volatility) — HONEST PILOT STATUS
- **Gate 3 (RV-only baseline): COMPLETE** — A_rv_only QLIKE 1.59541000261996 reproduced.
- **Gate 4 pilot: COMPLETE but PILOT/INCONCLUSIVE** — fixed invalid log-target/exponentiated ridge (root cause of absurd prior metrics) to **direct-variance OLS HAR** matching Gate 3, train-only normalization, 7d purge/embargo, funding last-known-at/before-hour (no lookahead), trailing pct/z past-only.
- Single walk-forward split (test 2024-02-22..2024-03-31), 4 assets, Q1 2024 only. Funding variants improve QLIKE vs A in this pilot (B/C/D Δ≈-0.156, E Δ≈-0.531) **but**: 1 split, no block-aware CIs, no multiple-comparison control, Q1-2024-only cannot satisfy FCLR-001 claim-worthy criteria (need **≥3 non-overlapping 30-day test blocks** and robust uncertainty). **Do NOT promote to confirmatory, do NOT claim economic value, do NOT build any overlay.**

## NEXT HEAVY-WORK CAMPAIGN (MANDATORY — P0, no coasting)
**Objective:** Turn the single-split Gate 4 pilot into a **defensible multi-split, pre-registered, uncertainty-quantified** evaluation within local 2024-01..03 data. Every session must produce a **measurable delta** (code + tests + run + durable artifact) or an evidence-backed blocker + next materially different route. **Do not stop after reading.**

### 1) Pre-register contrasts BEFORE computing outcomes (durable artifact)
Create `research_state/pre_registration_gate4_funding_multisplit_20261107.md` (if absent; update only with versioned, timestamped, pre-outcome freeze text): primary contrast **E vs A** (ΔQLIKE, lower better); secondary **B/C/D vs A**; multiplicity treatment (Holm over pre-registered family or explicit justification); primary metric **QLIKE**; horizons/symbols/splits fixed; frozen before running multi-split outcomes. Record freeze timestamp.

### 2) Implement multi-split walk-forward evaluation (code)
Extend `scripts/run_funding_ablations.py` (or add a focused companion script, tested) to:
- Build **multiple chronological walk-forward splits** over 2024-01..03 using `src/eval.walkforward.build_walkforward_splits` (or equivalent) with **purge/embargo ≥7d**, train-only normalization, no random splits.
- Report **per-split and aggregate** QLIKE/MAE/RMSE for A..E and **ΔQLIKE vs A**. Keep the direct-variance OLS form; A_rv_only must still reproduce Gate 3 on comparable setup (add regression assertion in tests if split logic changes).
- **Block-aware uncertainty:** paired ΔQLIKE (primary E vs A, and secondaries) via **block bootstrap** resampling whole UTC time blocks jointly across instruments (deterministic seed, e.g. `np.random.default_rng(20261107)`; **≥2000 replicates** where sample permits; document if fewer). Report point estimate + CI (e.g. 95% percentile/basic) per contrast.
- **Data-sufficiency gate (honest):** Q1 2024 is ~90 days — explicitly test/report whether **≥3 non-overlapping 30-day test blocks** and instrument coverage criteria are met. If not met, verdict remains **PILOT/INCONCLUSIVE** with the exact shortfall stated; **do not relax thresholds**.

### 3) Basis/premium (only if real aligned coverage exists)
Include basis/premium/mark-index dislocation features **only** with verified, aligned, admissible local coverage and no lookahead. Otherwise omit and state “basis/premium unavailable/misaligned → NaN-omitted, never zero-filled”.

### 4) Tests (required)
Add/extend `tests/test_funding_ablations.py` (or new focused test module): multi-split embargo/purge correctness, block-bootstrap determinism (seeded), and A_rv_only regression stability. Keep tests fast/fixture-friendly; no network.

### 5) Durable artifacts (update, not status-only)
- `research_state/evaluation_summary.md` — Gate 4 table with per-split + aggregate + CIs + honest verdict.
- `research_state/evaluation_summary_funding.md` — full detail.
- `research_state/run_manifest.json` — run id, git SHA, UTC, config/params, split boundaries, sample counts, bootstrap seed/replicates, CIs, status.
- `research_state/leakage_audit.md` — confirm chronological splits, purge/embargo, train-only normalization, no-lookahead funding alignment, bootstrap resamples blocks (no leakage).

### Acceptance commands (report actual results)
```bash
pip install -r requirements.txt
python scripts/run_funding_ablations.py
python -m unittest tests.test_funding_ablations -v
python -m unittest discover -s tests -t .   # expect 717 + new tests; 8 pre-existing Track A scope-registry failures unrelated
python scripts/tracka_resume_check.py      # expect pass:true, 17/17
```

## TRACK A (liquidation risk) — GUARDED, NO TRIGGER
- Trigger: **NO** (data_through 2026-10; 2026-11..2027-02 absent). Probes == 2. **Do not re-probe, do not inspect outcomes, do not resume 131/132/139 numbering without coherent artifacts.** Maintain invariants (17/17, bounds, no new probe families). If trigger ever appears: **PREREG BEFORE INSPECTING OUTCOMES**, Hyperliquid-only, observed ≠ modeled, fail-closed.
- The 8 pre-existing full-suite failures are Track A scope-registry hardening drift — **do not let them block Gate 4 P0**; address only as a separate, evidence-backed Track A lockdown task if chosen.

## CONSTRAINTS (NON-NEGOTIABLE)
- **No trading, no creds/API keys, no paid data, no auth bypass, no manual downloads.** Local admissible files only.
- **Never modify `.github/workflows/`.**
- **Leakage-resistant:** chronological only, purge/embargo, train-only normalization/stats/thresholds.
- **Missing != 0. Observed liquidations ≠ modeled boundary breaches ≠ volatility/stress.** Never merge tracks.
- **PREREG BEFORE OUTCOMES** for confirmatory/trigger evaluation.
- **Heavy work required:** measurable delta or evidence-backed blocker + materially different next route. No status-only churn.

**START NOW (P0):** write the Gate 4 multi-split prereg (freeze), implement multi-split + block-bootstrap CIs in `scripts/run_funding_ablations.py` with tests, run, and update `research_state/` artifacts with an honest PILOT/INCONCLUSIVE verdict if data-sufficiency criteria are not met.
