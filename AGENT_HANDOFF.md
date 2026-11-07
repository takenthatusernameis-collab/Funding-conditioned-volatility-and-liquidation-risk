# AGENT_HANDOFF.md — SINGLE DURABLE INITIAL TASK (NEXT SESSION)

**TIMESTAMP (UTC):** 2026-11-07T02:42:03Z
**REPO (priority):** `Funding-conditioned-volatility-and-liquidation-risk` — **P0 = funding-conditioned volatility (Gate 4)** using local admissible data. **Liquidation risk (Track A) = BLOCKED/GUARDED, no trigger** — do not resume Track A probing/outcome inspection.
**AUTHORITY:** This file is the **only** durable session handoff. If `research_state/FCLR_CAMPAIGN_NEXT.md`, frontier entries, or stale notes conflict, follow this file and record reconciliation in durable artifacts (not status-only files).

## VERIFIED STATE (2026-11-07T02:37:08Z)
- Git base HEAD: `3aa41592` (`chore(kilo): checkpoint agent session`) on `main`. Working tree (this session, measurable Gate 4 delta): `scripts/run_funding_ablations.py` (multi-split pre-reg pilot + block-bootstrap CIs), `tests/test_funding_ablations_multisplit.py` (new, 5 tests), `research_state/evaluation_summary.md`, `research_state/evaluation_summary_funding.md`, `research_state/run_manifest.json`, `research_state/leakage_audit.md`. `__pycache__`/`ironflow_fastpath_cache.json` restored to HEAD in working tree where touched; **do not commit `__pycache__`/cache churn**. **No workflow changes.**
- `python scripts/run_funding_ablations.py` (reproducible, local data only): 3 pre-registered walk-forward splits (14-day tests: 2024-02-05..02-18, 02-19..03-03, 03-04..03-17; train-only normalization; purge/embargo=7d). Aggregate QLIKE (mean): A=7.4632551696362475, B=16.987894189880944, C=16.987894189880944, D=16.987894191103717, E=5.543607735488995. **Primary E vs A (pre-reg): ΔQLIKE=4.6124034791315704, 95% block-bootstrap CI [-0.1288482496015316, 13.12243540310433], n_obs=1819, n_blocks=41, seed=12345, reps=2000, block=24h, jointly across instruments.** (CI spans 0.)
- `python -m unittest tests.test_funding_ablations tests.test_funding_ablations_multisplit -v`: **11/11 OK** (Gate 3 A_rv_only regression 1.5954100026198477, multi-split embargo/purge, block-bootstrap determinism/joint time-block resampling).
- Full-suite baseline concern: pre-existing **8 Track A scope-registry hardening failures** (`test_tracka_hardening_114/117/118/119/120/121/123/129`) unrelated to Gate 4 (Track A blocked). Gate 4 tests pass; verify full suite in your run and report the same 8 if unchanged. **Do not "fix" by resuming Track A.**
- `python scripts/tracka_resume_check.py`: **pass:true, 17/17**.
- Deps: `pip install -r requirements.txt`. Data: **local only** BTC/ETH/SOL/XRP 1h klines + fundingRate 2024-01..03. Missing = NaN, never zero. Basis/premium **not added** (no aligned admissible local series verified) — NaN-omitted, never zero-filled. **No creds, no paid data, no bypass, no re-probe.**
- Bounds: `research_state` root md+json = **147** (<=163). Probes == 2. No new probe/scan families. No workflow changes.

## GATE 4 STATUS — HONEST (PILOT/INCONCLUSIVE)
- Pre-registration frozen before outcomes: `research_state/pre_registration_gate4_funding_multisplit_20261107.md`. **Do not change contrasts/metrics/splits after computing results.**
- Multi-split evaluation implemented with leakage controls: chronological splits, purge/embargo 7d, train-only normalization, funding last-known at/before hour, trailing stats past-only, direct-variance OLS (no log/exp), block-bootstrap CIs.
- **Verdict: PILOT/INCONCLUSIVE.** Data-sufficiency shortfalls: `instruments=4 < 5`, `no_30day_non_overlapping_test_blocks` (14-day windows; Q1 2024 local data insufficient for >=3×30-day), `q1_2024_only_local_data`. Primary CI spans 0. **Do NOT promote to confirmatory, do NOT claim economic value, do NOT build any overlay.**

## NEXT HEAVY-WORK CAMPAIGN (MANDATORY — P0)
Every session must produce a **measurable delta** (code + tests + run + durable artifact) or an evidence-backed blocker + next materially different route. **Do not stop after reading.**

1. **Report full-suite status honestly** (run `python -m unittest discover -s tests -t .`; expect 8 pre-existing Track A scope-registry failures unless addressed as a separate evidence-backed Track A lockdown task under P2/guarded rules). Do not let them block Gate 4 P0.
2. **Strengthen Gate 4 pilot rigor (local-data feasible):**
   - Add **per-contrast secondary CIs** reporting consistency checks (already computed for B/C/D vs A — verify reporting clarity) and a compact **per-split paired ΔQLIKE** table (E vs A) to make instability visible.
   - **Sensitivity (pre-registered as exploratory, label clearly):** block size {12h,24h,48h} and B sensitivity; report whether CI/sign stability changes. Do not promote if unstable.
   - **Regularization/tuning only on train (or train/val within split) — never test:** if ridge/feature-selection explored, preregister as a versioned addendum before running; record in manifest/leakage audit.
3. **Data-sufficiency blocker (evidence-backed):** FCLR-001 claim-worthy needs >=5 instruments and >=3 non-overlapping 30-day test blocks. Local admissible Q1 2024 cannot satisfy this. Record the blocker; next materially different route (only if/when admissible local data expands): add instruments/months from local admissible sources with verified alignment, **preregister** 30-day non-overlapping blocks, re-run. **No creds/paid data/manual downloads/re-probe.**
4. **Basis/premium:** include only with verified aligned admissible local coverage and no lookahead; otherwise keep omitted/NaN and state explicitly.
5. **Durable artifacts:** keep `evaluation_summary.md`, `evaluation_summary_funding.md`, `run_manifest.json`, `leakage_audit.md` synchronized with actual runs (no status-only churn). `leakage_audit.md` must remain clean (no stale log-ridge entry).

## TRACK A — GUARDED, NO TRIGGER (BOTTLECK REMOVED)
Trigger **NO** (data_through 2026-10; 2026-11..2027-02 absent). Probes == 2. **Do not re-probe, do not inspect outcomes, do not resume 131/132/139 without coherent artifacts.** Maintain invariants (17/17, bounds, no new probe families). If trigger appears: **PREREG BEFORE INSPECTING OUTCOMES**, Hyperliquid-only, observed ≠ modeled, fail-closed.

## CONSTRAINTS (NON-NEGOTIABLE)
- **No trading, no creds/API keys, no paid data, no auth bypass, no manual downloads.** Local admissible files only.
- **Never modify `.github/workflows/`.**
- **Leakage-resistant:** chronological only, purge/embargo, train-only normalization/stats/thresholds.
- **Missing != 0. Observed liquidations ≠ modeled boundary breaches ≠ volatility/stress.** Never merge tracks.
- **PREREG BEFORE OUTCOMES** for confirmatory/trigger evaluation.
- **Heavy work required:** measurable delta or evidence-backed blocker + materially different next route. No status-only churn.
