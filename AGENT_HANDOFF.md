## Initial Task Message (2026-11-07T21:09:34Z) — Next Agentic Session

**Repo priority (by name: Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; (2) **Track A observed liquidation risk** — blocked on admissible data (monitor/guard only, no re-probe); (3) Track B modeled boundary breach — closed negative. Confirmatory forecast gate **NOT MET** (H001 NOT_SUPPORTED). Gate 4 v4 **EXPLORATORY_INCONCLUSIVE/NOT PROMOTABLE** (sealed context preserved). This session executed **heavy measurable work** unblocking Gate 4 v5 admissibility: (A) fail-closed confirmatory provenance guard in ablations runner; (B) bounded unauthenticated Binance Vision identity probe for 2025+ cache (FCLR-016).

### What changed and why (this session)
- `scripts/run_funding_ablations.py`: added **confirmatory provenance guard** (FCLR-014/FCLR-016). Confirmatory-labeled runs (`--confirmatory`, or confirmatory/v5+ naming without `exploratory`/`pilot`) touching **unprovenanced 2025+** cache windows now **fail closed (exit 2, JSON REFUSED)** unless `--provenance-manifest` points to a GO manifest. Exploratory/pilot runs unaffected. Prevents accidental claim outcomes on unprovenanced data.
- `scripts/fclr016_verify_cache_provenance_2025plus.py` (new): bounded unauthenticated Binance Vision SHA256/ETag identity verification for cached 2025+ UM futures files (fundingRate/klines/mark/index/premium), canonical subdir selection (fixes top-level placeholder mismatch), resumable/checkpointed. **Admissibility evidence only; no outcomes.**
- `tests/test_funding_ablations.py`: added `test_confirmatory_provenance_guard_refuses_unprovenanced_2025` (guard refuses confirmatory 2025+; allows exploratory). Funding ablations tests: **7/7 OK**.

### Bounded provenance evidence (this session)
- `research_state/fclr016_local_audit/fclr016_binance_vision_probe_202501_bounded_canonical_20261107T210712Z.json` + `.md` (unauthenticated Binance Vision): **BTCUSDT,ETHUSDT; 2025-01; fundingRate + klines sample days 1,31** → `match=6 mismatch=0 missing=0 remote_error=0`, `cache_identity_vs_binance_vision=GO_PARTIAL_BOUNDED`, `confirmatory_claim_go=NO_GO` (identity evidence only; license/terms/completeness/leakage/prereg/boundary non-overlap still required). **Materially different route from prior "provenance UNVERIFIED" memo**: sampled 2025-01 identity now verified; **not sufficient for confirmatory claims**.

### What was actually tested, with exact outcomes
- `python3 -m unittest tests.test_funding_ablations -v`: **7/7 OK**.
- `python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/run_funding_ablations.py`: **OK**.
- CLI smoke: `python3 scripts/run_funding_ablations.py --start 2025-01-01 --end 2025-06-30 --confirmatory --experiment-id GATE4-V5-CONFIRMATORY --pre-registration prereg_v5_confirmatory.md --out-suffix _v5 --include-cache` → **rc=2, REFUSED, guard=confirmatory_provenance_fclr014**.
- `python3 scripts/tracka_resume_check.py`: re-run to confirm (expected pass:true, 17 checks).
- Full suite: `python3 -m unittest discover -s tests -q` (baseline 751; additive changes).

### Current state of each research gate
- **Forecast gate (FCLR-001/H001): NOT MET / NOT_SUPPORTED** (all sealed confirmatory panels exhausted). Overlay INELIGIBLE.
- **Gate 4 v4 (2024-04..09): EXPLORATORY_INCONCLUSIVE / NOT PROMOTABLE** (confounded slice; primary CI spans 0). Sealed anchors preserved.
- **Gate 4 v5 confirmatory: NOT READY / NO-GO for claims** — FCLR-014 provenance decision stands. **New:** sampled 2025-01 identity GO_PARTIAL_BOUNDED (FCLR-016), but **confirmatory still blocked** pending: (a) broader 2025+ identity coverage (symbols/months/kinds) with deterministic manifest, (b) admissible license/terms evidence, (c) completeness/census checks, (d) **frozen prereg before outcomes** on a boundary **materially non-overlapping** FCLR-002/003/013/v3/v4 test windows (≥5 instruments, ≥3×30-day non-overlapping test blocks, 7d+ purge/embargo, train-only normalization, block bootstrap, primary contrast pre-specified). Runner now **enforces fail-closed** for confirmatory 2025+ without provenance manifest.
- **Track A (observed liquidations): DATA_BLOCKED** (no admissible unauthenticated source; data through 2026-10; exhausted). Reopen only on NEW admissible data meeting strict GO rubric + prereg before outcomes. **No re-probe of exhausted months/windows.**
- **Track B (modeled boundary breaches): CLOSED NEGATIVE**.

### Single highest-value next task (heavy, measurable)
**P0 — Complete FCLR-016 bounded identity manifest for a v5-candidate boundary (no outcomes):**
1. Run bounded unauthenticated Binance Vision verification for **5 symbols (BTC/ETH/BNB/SOL/XRP)** across candidate months for a **non-overlapping v5 test window** (propose: test ~2025-08-01..2025-10-29 or later; **compute & document non-overlap proof vs FCLR-002/003/013/v3/v4 before prereg**). Verify `fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines` for sampled days (1,15,last per month; escalate to `--sample-days full` only if bounded). Write deterministic JSON+MD under `research_state/fclr016_local_audit/`.
2. **If identity GO_PARTIAL/GO for candidate scope:** draft v5 prereg template documenting boundary, non-overlap proof, splits (≥3×30d), purge/embargo, train-only normalization, missing!=0, primary contrast, multiplicity/bootstrap, and **license/terms TODO** — keep `frozen_before_outcomes=false` / "PENDING LICENSE+COMPLETENESS+FREEZE". **Do not run outcomes.**
3. **If mismatches/errors:** record NO-GO evidence, keep guard; do not relax. **Route:** narrow to MATCH-only files/months with documented exclusions or verify alternate admissible checksums if available unauthenticated.
4. **Track A:** only on genuinely new unauthenticated source; otherwise **skip re-probe**.

### Precise commands / checks to verify
- `python3 -m unittest tests.test_funding_ablations -v` (expect **7 OK**)
- `python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/run_funding_ablations.py` (expect **OK**)
- `python3 scripts/run_funding_ablations.py --start 2025-01-01 --end 2025-06-30 --confirmatory --experiment-id GATE4-V5-CONFIRMATORY --pre-registration prereg_v5_confirmatory.md --out-suffix _v5 --include-cache` (expect **rc=2 REFUSED**)
- `python3 scripts/tracka_resume_check.py` (expect **pass:true, 17 checks**)
- `python3 -m unittest discover -s tests -q` (expect green)
- `find research_state -maxdepth 1 \( -name "*.md" -o -name "*.json" \) | wc -l` (expect **≤172**; FCLR-016 artifacts in subdir)

### Blockers / next materially different free routes
- **Confirmatory (Track C):** 2025+ confirmatory claims blocked by FCLR-014 (provenance/license/completeness/prereg/boundary). FCLR-016 gives **sampled 2025-01 identity GO_PARTIAL_BOUNDED** — necessary, not sufficient. **Route:** expand bounded identity manifest; record admissible terms/license evidence; freeze v5 prereg on verified non-overlapping boundary **before outcomes**. Guard prevents premature runs.
- **Track A:** no admissible unauthenticated liquidation data (through 2026-10). **Route:** P1-5 alt liquidation source hunt (strict GO rubric) only on materially different candidates; **do NOT re-probe exhausted months/windows**.
- **Do NOT:** re-probe exhausted Track A; re-run/open sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat v4/exploratory as confirmatory; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`.

**Status:** Track A=DATA_BLOCKED; Track B=CLOSED_NEGATIVE; Track C/H001=NOT_SUPPORTED (forecast gate NOT MET); Gate 4 v4=EXPLORATORY_INCONCLUSIVE; Gate 4 v5=NOT_READY (confirmatory NO-GO; sampled 2025-01 identity GO_PARTIAL_BOUNDED; guard active).

---

## Initial Task Message (2026-11-07T20:50:11Z) — Next Agentic Session

**Repo priority (by name: Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; (2) **Track A observed liquidation risk** — blocked on admissible data (monitor/guard only, no re-probe); (3) Track B modeled boundary breach — closed negative. Confirmatory forecast gate **NOT MET** (H001 NOT_SUPPORTED on all sealed confirmatory panels). This session executed **heavy measurable work** on the highest-value unblocked path: Gate 4 v4 exploratory ablations on the FCLR-015 identity-verified 2024-04..09 cache slice (after prereg freeze). **Exploratory only — NOT CONFIRMATORY, NOT PROMOTABLE** (confounded with sealed FCLR-002/v3 lineage per `research_state/gate4_v4_boundary_admissibility_20261107T1845Z.md`).

### What changed and why (this session)
- `scripts/run_funding_ablations.py`: fixed split-def selection so `--out-suffix`/`--pre-registration` containing `v4` uses `PRE_REG_SPLITS_V3_30D` (4×30-day, 2024-04..09 expanding train) and enables cache loading; v1/v2/v3 behavior preserved. This unblocked the frozen v4 prereg from silently selecting wrong (v1/Q1 14-day) splits and producing null outputs.
- Executed **GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D** (exploratory, prereg frozen 2026-11-07T18:45Z, `frozen_before_outcomes=true`, manifest SHA256 `3e6ac2…5406c`, 3690/3690 Binance Vision identity matches). 5 symbols (BTC/ETH/SOL/XRP/BNB), 2024-04-01..2024-09-30, 4×30d test blocks, 7d purge/embargo, train-only normalization, block bootstrap (24h, 2000 reps, seed 12345).

### Results (EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE)
- Verdict: **DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST** (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim).
- QLIKE (mean): A_rv_only=0.7983, B_rv_signed=12.1836, C_rv_abs=0.8460, D_rv_signed_abs=3.4493, E_rv_funding_trails=1.2417.
- Primary contrast E_rv_funding_trails vs A: ΔQLIKE=**0.4879** (95% CI **[-0.0422, 1.1973]**, n=12969, 120 blocks) — CI spans 0; **no confirmatory skill/incremental value claim**. Signed/abs funding ablations degrade QLIKE sharply here (exploratory diagnostic).
- Artifacts: `research_state/evaluation_summary_funding_v4_exploratory_30d.md`, `research_state/run_manifest_funding_v4_exploratory_30d.json` (overwritten with exploratory outcomes; prior file was null/INSUFFICIENT due to wrong split selection). No sealed confirmatory anchors overwritten.

### What was actually tested, with exact outcomes
- `python3 -m unittest tests.test_funding_ablations -v`: **6/6 OK** (incl. no-duplicate-cols, bounded preds, RV-only Gate 3 repro, trailing pct past-only).
- `python3 scripts/run_funding_ablations.py --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --start 2024-04-01 --end 2024-09-30 --pre-registration research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md --out-suffix _v4_exploratory_30d --experiment-id GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D --include-cache --skip-main-summary`: exit 0; verdict JSON above.
- `python3 scripts/tracka_resume_check.py`: **pass:true**, 17 checks OK, network:false, writes_real_research_state:false.
- `python3 -m unittest discover -s tests` (full suite): **not re-run this session** (prior baseline 751 OK in earlier handoff context); run next to confirm runner change causes no regressions.

### Current state of each research gate
- **Forecast gate (FCLR-001/H001): NOT MET / NOT_SUPPORTED** — all sealed confirmatory panels exhausted; no claim-worthy incremental skill after declared corrections. Overlay INELIGIBLE.
- **Gate 4 v4 (2024-04..09): EXPLORATORY INCONCLUSIVE** — data-sufficient pilot (4×30d) on confounded slice; primary CI spans 0. **Cannot be promoted**; distinct non-confounded confirmatory boundary required (v5 prereg before outcomes).
- **Track A (observed liquidations): DATA_BLOCKED** — no admissible unauthenticated liquidation source; data through 2026-10; probing exhausted. Reopen only on NEW admissible data meeting strict GO rubric (≥5 instruments, ≥3 non-overlapping 30-day blocks, documented completeness, license OK) with prereg before outcomes.
- **Track B (modeled boundary breaches): CLOSED NEGATIVE**.
- **Confirmatory v5 readiness: NOT PROVEN** — 2025+ cache months have **unverified provenance/licensing for confirmatory claims** (`research_state/fclr014_local_audit/fclr014_provenance_decision_20261107T133102Z.md` NO-GO). `research_state/data_cache/manifest_extract.json` is an LFS pointer in this checkout (no admissible 2025+ retrieval/hash provenance resolved locally).

### Single highest-value next task (heavy, measurable)
**P0 — Gate 4 v5 confirmatory boundary enablement (or hard fail-closed guard):** Establish an admissible, non-confounded confirmatory boundary for funding-volatility ablations.
1. **Admissibility pass:** for candidate months **2025-01..2025-12 and/or 2026-01..2026-06** (5 symbols, 1h+fundingRate) in `research_state/data_cache/`, produce machine-verifiable provenance evidence (unauthenticated Binance Vision origin, exact retrieval paths, terms/license acceptance, per-file checksums/manifest tied to source) **without network in CI-unsafe ways except bounded, logged, unauthenticated probes if explicitly permitted; prefer existing manifests/ETags if materialized**. If LFS manifests/pointers block evidence, document the exact blocker and the smallest free route (e.g., materialize LFS, or run bounded unauthenticated SHA256 verify like FCLR-015 against Binance Vision for sampled/full 2025+ months with deterministic artifacts).
2. **If provenance GO:** preregister **GATE4-FUND-VOL-V5** (`research_state/pre_registration_gate4_funding_multisplit_v5_<UTC>.md|json`, `frozen_before_outcomes=true`) on a boundary **materially non-overlapping** with FCLR-002/003/013/v3/v4 exploratory test windows (document non-overlap proof), ≥5 instruments, ≥3×30-day non-overlapping test blocks, 7d+ purge/embargo, train-only normalization, block bootstrap, primary contrast pre-specified. Only then run outcomes to versioned v5 outputs.
3. **If provenance NO-GO (expected given FCLR-014):** implement a **fail-closed guard** in `scripts/run_funding_ablations.py`/tests that refuses confirmatory-labeled runs on unprovenanced 2025+ cache windows (or requires `--provenance-manifest` with verified hashes) and records the decision; ship green tests. Do not run claim outcomes on unprovenanced data.

### Precise commands / checks to verify
- `python3 -m unittest tests.test_funding_ablations -v` (expect 6 OK)
- `python3 -m unittest discover -s tests` (expect green; confirm runner v4 selection fix has no regressions)
- `python3 scripts/tracka_resume_check.py` (expect pass:true, 17 checks)
- `git status --short` (only intended: `scripts/run_funding_ablations.py`, `AGENT_HANDOFF.md`, `research_state/evaluation_summary_funding_v4_exploratory_30d.md`, `research_state/run_manifest_funding_v4_exploratory_30d.json`)
- `find research_state -maxdepth 1 \( -name "*.md" -o -name "*.json" \) | wc -l` (expect ≤172; no new root files added)

### Blockers / next materially different free routes
- **Blocker (confirmatory):** 2025+ cache provenance/licensing unverified (FCLR-014 NO-GO); `manifest_extract.json` is LFS pointer here. **Route:** bounded unauthenticated Binance Vision SHA256 verification for 2025+ months (FCLR-015 pattern) producing a committed manifest + provenance decision artifact; or materialize LFS manifests if available.
- **Blocker (Track A):** no admissible unauthenticated liquidation data (through 2026-10). **Route:** P1-5 alt liquidation source hunt with strict GO rubric; do NOT re-probe exhausted months/windows.
- **Do NOT:** re-probe exhausted Track A months; re-run/open sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat exploratory v4 as confirmatory; edit `.github/workflows`.

**Status:** Track A=DATA_BLOCKED; Track B=CLOSED_NEGATIVE; Track C/H001=NOT_SUPPORTED (forecast gate NOT MET); Gate 4 v4=EXPLORATORY_INCONCLUSIVE; Gate 4 confirmatory v5=NOT_READY (provenance).
