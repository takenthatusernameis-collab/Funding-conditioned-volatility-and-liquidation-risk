# AGENT_HANDOFF.md — SINGLE DURABLE INITIAL TASK (NEXT SESSION)

**TIMESTAMP (UTC):** 2026-11-07T03:34:26Z (handoff refreshed; v2 5-symbol pilot recorded; v1 unchanged)
**REPO (priority):** `Funding-conditioned-volatility-and-liquidation-risk` — **P0 = funding-conditioned volatility (Gate 4, Track C)** using local admissible data. **Liquidation risk (Track A) = BLOCKED/GUARDED, no trigger** — do not resume Track A probing/outcome inspection.
**AUTHORITY:** This file is the **only** durable session handoff. If `research_state/FCLR_CAMPAIGN_NEXT.md`, frontier entries, or stale notes conflict, follow this file and record reconciliation in durable artifacts (not status-only files).

## THIS SESSION (measurable delta, 2026-11-07T03:24:39Z–03:32:30Z)
- **v2 5-symbol Gate 4 pilot (pre-registered, local only, v1 preserved):**
  - Frozen prereg BEFORE outcomes: `research_state/pre_registration_gate4_funding_multisplit_v2_5sym_20261107T032439Z.md` (GATE4-FUND-VOL-ABLATIONS-MSPLIT-V2-5SYM; adds BNBUSDT; same leakage/splits/model/contrasts; 30-day block criterion still NOT MET under Q1-only). BNBUSDT local alignment verified (90 daily 1h zips 2024-01-01..03-30 + monthly funding 2024-01..03; same OHLCV schema as BTC; loaded via existing loader path).
  - `scripts/run_funding_ablations.py`: added CLI/config for versioned runs (`--symbols`, `--pre-registration`, `--out-suffix`, `--experiment-id`, `--skip-main-summary`); default behavior = v1 (backward compatible). Caveat text now reflects actual instrument sufficiency. v1 outputs **not overwritten**.
  - v2 run (local, no network): `python scripts/run_funding_ablations.py --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --pre-registration research_state/pre_registration_gate4_funding_multisplit_v2_5sym_20261107T032439Z.md --out-suffix _v2_5sym --experiment-id GATE4-FUND-VOL-ABLATIONS-MSPLIT-V2-5SYM --skip-main-summary` → `research_state/evaluation_summary_funding_v2_5sym.md`, `research_state/run_manifest_funding_v2_5sym.json`. Verdict **PILOT/INCONCLUSIVE** (data-sufficiency criteria not met). `instruments=5 MET`, but `no_30day_non_overlapping_test_blocks`, `q1_2024_only_local_data` => `meets_claim_worthy:false`. Aggregate QLIKE A=5.803459241308542, B=2.555662519851302, C=17.1533038908623, D=13.181698445411909, E=5.78538142648025. Primary E vs A: ΔQLIKE=-1.6489202390149797, 95% block-bootstrap CI [-3.9918278213500464, 0.30332204461053297], n_obs=2920, n_blocks=42 (CI spans 0). Per-split paired Δ and 12h/24h/48h sensitivity remain unstable/inconclusive; **do not promote**. v1 manifest/v1 summaries unchanged (v1 A=7.4632551696362475, pre-reg path unchanged).
  - `research_state/leakage_audit.md` updated with v1/v2 prereg traceability; checks remain clean.
- **Repo hygiene (measurable):** removed tracked `scripts/__pycache__` / `tests/__pycache__` bytecode from git index (already gitignored; working-tree files remain untracked locally). No workflow changes.
- **Verification:** `python -m unittest tests.test_funding_ablations tests.test_funding_ablations_multisplit -v` → **11/11 OK**. `python -m unittest discover -s tests -t .` → **722/722 OK**. `python scripts/tracka_resume_check.py` → **pass:true, 17/17**. research_state root md+json = **151** (under cap). Probes/watch invariants per resume check. No Track A probing/outcome inspection. No creds/paid data/manual downloads/bypass.

## PRIOR SESSION (kept, 2026-11-07T03:15:53Z–03:25:00Z)
- **Gate 4 pilot rigor strengthened (code + tests + run + durable artifacts):**
  - `scripts/run_funding_ablations.py`: added per-split paired ΔQLIKE table vs A (instability visibility), exploratory block-bootstrap sensitivity (12h/24h/48h; 24h remains primary per prereg) using same pooled paired observations/seed/reps/CI method, and per-split paired frame capture. No change to pre-registered contrasts/ablations/splits/model/metrics.
  - `tests/test_funding_ablations_multisplit.py`: asserts 3 per-split paired frames returned.
  - `research_state/pre_registration_gate4_funding_multisplit_20261107_exploratory_sensitivity_addendum.md` (EXPL-SENS-001, frozen before running sensitivity outputs): exploratory only, not confirmatory/claim-bearing.
  - Regenerated: `research_state/evaluation_summary_funding.md` (2026-11-07T03:21:33Z, SHA 97dbc2add1a0441f49b1d901e4aae546a1282a37), `research_state/evaluation_summary.md` section, `research_state/run_manifest.json` (adds `per_split_paired_delta_vs_A`, `exploratory_sensitivity_block_hours`, addendum ref), `research_state/leakage_audit.md` unchanged/clean.
- **Verification (local, no network in tests):** `python -m unittest tests.test_funding_ablations tests.test_funding_ablations_multisplit -v` → **11/11 OK**. `python scripts/run_funding_ablations.py` (local data only) → pilot verdict unchanged: **PILOT/INCONCLUSIVE** (data-sufficiency criteria not met). `python -m unittest discover -s tests -t .` → **722/722 OK**. `python scripts/tracka_resume_check.py` → **pass:true, 17/17**. `research_state` root md+json = **148** (under cap). Probes == 2. No workflow changes. No Track A probing/outcome inspection. No creds/paid data/manual downloads/bypass.

## VERIFIED PILOT RESULTS (pre-registered; do not promote)
### v1 (4 symbols, preserved)
- Pre-reg: `research_state/pre_registration_gate4_funding_multisplit_20261107.md` (frozen 2026-11-07T01:36:11Z). Exploratory addendum frozen before sensitivity outputs.
- Data: local BTC/ETH/SOL/XRP 1h klines + fundingRate 2024-01..03. Missing = NaN, never zero. Basis/premium omitted.
- Aggregate QLIKE A=7.4632551696362475, B=16.987894189880944, C=16.987894189880944, D=16.987894191103717, E=5.543607735488995. Primary E vs A (block=24h): ΔQLIKE=4.6124034791315704, 95% CI [-0.1288482496015316, 13.12243540310433], n_obs=1819, n_blocks=41 (CI spans 0). Per-split E vs A = [7.225674132309532 (n=1091), 1.6403717659065886 (n=343), -0.14518458575410795 (n=385)] — unstable.
- Verdict **PILOT/INCONCLUSIVE**. Shortfalls: `instruments=4 < 5`, `no_30day_non_overlapping_test_blocks`, `q1_2024_only_local_data`. v1 outputs: `evaluation_summary_funding.md`, `run_manifest.json` (v1 section).

### v2 (5 symbols, side run; do not overwrite v1)
- Pre-reg (frozen BEFORE outcomes): `research_state/pre_registration_gate4_funding_multisplit_v2_5sym_20261107T032439Z.md`. Data adds BNBUSDT (90 daily 1h zips 2024-01-01..03-30 + funding 2024-01..03), same schema/alignment/leakage controls.
- `instruments=5 MET` for pilot set; `meets_claim_worthy:false` due to `no_30day_non_overlapping_test_blocks` and `q1_2024_only_local_data`.
- Aggregate QLIKE A=5.803459241308542, B=2.555662519851302, C=17.1533038908623, D=13.181698445411909, E=5.78538142648025. Primary E vs A: ΔQLIKE=-1.6489202390149797, 95% CI [-3.9918278213500464, 0.30332204461053297], n_obs=2920, n_blocks=42 (CI spans 0).
- Per-split E vs A = [0.1812727189915471 (n=1465), -3.6027369611810673 (n=822), -3.347491072915515 (n=633)] — sign/scale instability across splits; 12h/24h/48h sensitivity all span 0 and do not resolve uncertainty.
- Verdict **PILOT/INCONCLUSIVE**. No confirmatory claim, no economic value, no overlay. v2 outputs: `evaluation_summary_funding_v2_5sym.md`, `run_manifest_funding_v2_5sym.json`.

## BOTTLENECKS (evidence-backed)
1. **30-day non-overlapping blocks (binding, now primary):** v2 satisfies `instruments=5` on local Q1 2024 data, but **Q1 2024 local data cannot satisfy >=3 non-overlapping 30-day test blocks with train/purge** (~90 days total). This is the remaining claim-worthy shortfall. **Materially different route:** locate/verify **additional admissible local months/symbols** already present in repo/data (no creds/paid/auth/manual downloads) with provenance/alignment; if found, preregister claim-worthy 30-day blocks + instrument set + contrasts BEFORE outcomes and run as v3. If none exist locally, record as evidence-backed blocker (do not fetch).
2. **Cross-version instability:** v1 and v2 primary E vs A CIs both span 0 but point estimates/sign context differ (v1 Δ=+4.612…, v2 Δ=-1.649…) and per-split directions vary. **Do not cherry-pick or claim direction.** Treat as inconclusive/pilot sensitivity to instrument set and sample composition.
3. **Basis/premium omitted:** no aligned admissible local series verified; keep NaN-omitted. Add only with verified alignment/no-lookahead under a versioned prereg addendum.
4. **Repo/state hygiene addressed this session:** tracked `__pycache__` bytecode removed from index (gitignored); keep it untracked.

## NEXT HEAVY-WORK CAMPAIGN (MANDATORY — P0, do not stop after reading)
Every session must produce a **measurable delta** (code + tests + run + durable artifact) or an evidence-backed blocker + next materially different route. **No status-only churn.**

1. **Claim-worthy 30-day blocks v3 (ONLY if admissible local data exists):** Audit repo/data for additional local months/symbols beyond Q1 2024 with verified provenance/alignment (no creds/paid/auth/manual). If sufficient: write `research_state/pre_registration_gate4_funding_multisplit_v3_30d_<UTC>.md` **BEFORE outcomes** (>=3 non-overlapping 30-day test blocks, instrument set, contrasts, leakage/purge/embargo, model). Run v3 as separate versioned outputs; do not overwrite v1/v2. If insufficient locally: document blocker evidence (what was searched, counts, why insufficient) and stop — no fetch.
2. **5-symbol alignment tests (measurable hardening):** add tests proving BNBUSDT (and existing symbols) load/align with correct funding merge_asof/backward behavior, NaN-not-zero, and per-symbol presence using local fixtures/mocked CSV/zip shapes (no network). Keep tests fast and deterministic.
3. **Exploratory robustness addendum (bounded, pre-reg before outcomes):** stationary/circular-block edge handling or train-only ridge/HAR-regularized variant vs A/E — **only** under a frozen exploratory addendum before running; report stability/instability honestly; never tune to test; never promote to confirmatory.
4. **Cross-version synthesis (durable, honest):** create/update a short durable note/table comparing v1/v2 (same splits/model family, different instrument sets) emphasizing instability and data-sufficiency constraints; no directional claim.
5. **Durable artifacts/invariants:** keep `leakage_audit.md` clean; preserve v1/v2 outputs; root md+json under cap; Track A invariants 17/17, probes unchanged, no workflow edits, no Track A probing/outcome inspection.

## TRACK A — GUARDED, NO TRIGGER (BOTTLENECK REMOVED PREVIOUSLY)
Trigger **NO** (data_through 2026-10; 2026-11..2027-02 absent). Probes == 2. **Do not re-probe, do not inspect outcomes, do not resume 131/132/139 without coherent artifacts.** Maintain invariants (17/17, bounds, no new probe families). If trigger appears: **PREREG BEFORE INSPECTING OUTCOMES**, Hyperliquid-only, observed ≠ modeled, fail-closed.

## CONSTRAINTS (NON-NEGOTIABLE)
- **No trading, no creds/API keys, no paid data, no auth bypass, no manual downloads.** Local admissible files only.
- **Never modify `.github/workflows/`.**
- **Leakage-resistant:** chronological only, purge/embargo, train-only normalization/stats/thresholds.
- **Missing != 0. Observed liquidations ≠ modeled boundary breaches ≠ volatility/stress.** Never merge tracks.
- **PREREG BEFORE OUTCOMES** for confirmatory/trigger evaluation or instrument-set changes that affect claims.
- **Heavy work required:** measurable delta or evidence-backed blocker + materially different next route. No status-only churn.
