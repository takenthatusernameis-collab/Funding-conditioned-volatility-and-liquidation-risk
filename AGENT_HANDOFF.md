## Initial Task Message (2026-11-08T13:13Z, git HEAD `ec2502f7c` + uncommitted campaign changes — see below; sealed artifacts untouched) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority (enforced):** (1) **funding-conditioned volatility forecasting** (Track C / Gate 4, local admissible Binance kline+funding data — measurable, unblocked, heavy) → (2) **liquidation risk** (Track A observed / Track B modeled — **never conflated**; Track A blocked, no trigger). **Mission:** empirical/research only; **no trading/orders**; no fabricated data/terms/reviews; chronological leakage-resistant OOS only; sealed holdouts untouched; **no `.github/workflows` edits**; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff/status files.**

### Session 2026-11-08T12:40Z — FCLR-NEXT-139 delivered (heavy, measurable, unblocked; no claims)
- **Delivered `scripts/fclr017_gate4_cache_coverage_audit.py`** (deterministic, read-only, **no network, no model-outcome computation**). Scans `research_state/data_cache/{SYMBOL}_{YYYY_MM}/` for default 5 symbols (BTC/ETH/SOL/XRP/BNB) × 2024-04..09: inventories daily 1h `klines`/`markPriceKlines`/`indexPriceKlines`/`premiumIndexKlines` + `fundingRate`, records per-symbol/month file counts, deterministic source-path/metadata fingerprints, bounded per-file content SHA-256s (default), flags missing month dirs/days, duplicate/extra day dirs, missing canonical zip/csv, missing funding expected source, quarantine/placeholder path patterns. Emits timestamped+latest JSON/MD under `research_state/fclr017_local_audit/` with `no_confirmatory_outcomes=true`, `exploratory_only=true`, `no_network=true`, `not_go_for_confirmatory_outcomes=true`, v5 terms blocker unresolved caveat, FCLR-015 identity-verified-slice-only-where-evidenced caveat, and explicit audit/planning-only statement. **Does not overwrite sealed v3 artifacts.**
- **Added `tests/test_fclr017_gate4_cache_coverage_audit.py`** (6 deterministic tmp-fixture tests, no network): complete coverage, missing day/month, quarantine/placeholder, missing funding, default scope constants, content-hash presence.
- **Registered** `fclr017_gate4_cache_coverage_audit.py` in `research_state/tracka_script_scope_registry.json` (`track_c_or_aux_audit_utility`).
- **Real-cache result (planning evidence only):** `research_state/fclr017_local_audit/fclr017_gate4_cache_audit_latest.{json,md}` (`b2613bb910f714d5` / `a024e824a63621b5`) → `global_all_months_ok=true`, `v3_30d_calendar_consistency=CONSISTENT`, `requested_scope_matches_v3_30d_default=true`, 5 sym × 6 months, no missing days, no quarantine/placeholder anomalies, funding expected source present each month. Confirms local 2024-04..09 cache calendar/lineage/coverage is internally consistent with the v3-30d design window; **does not recompute model outcomes or reproduce sealed metrics**. Sealed v3 artifacts remain authoritative.
- **`_v3_30d_verify` outputs created for verification and removed** after exact reproduction (n_obs=12969, n_blocks=120, E_vs_A point=0.4879023125556385, CI [-0.042160777324701186, 1.1973379300276015] spans 0).

### Working-tree note (not committed)
- `research_state/run_manifest.json` — prior session repair preserved (`split_boundaries_fclr010` merged; funding-ablations keys preserved). **Do not remove `split_boundaries_fclr010`; do not replace with LFS pointer.**
- `research_state/tracka_script_scope_registry.json` — adds `fclr017_gate4_cache_coverage_audit.py` registration (drift 102/102 PASS).
- `research_state/evaluation_summary.md`, `research_state/evaluation_summary_funding.md`, `research_state/leakage_audit.md`, `research_state/ironflow_fastpath_cache.json` — refreshed by campaign re-runs (timestamps/appends/honest verdict context only; no sealed artifact overwritten, no outcomes recomputed beyond honest pilot verdicts).
- New/untracked planning artifacts: `scripts/fclr017_gate4_cache_coverage_audit.py`, `tests/test_fclr017_gate4_cache_coverage_audit.py`, `research_state/fclr017_local_audit/` (latest+timestamped JSON/MD; **planning evidence only, not GO**).
- `_v3_30d_verify` outputs **removed**.

### Verified 2026-11-08T12:40Z (local, no network)
- `python -m unittest discover tests -q` → **896 tests, OK** (includes 6 new fclr017 tests; 0 failures).
- `check_tracka_scope_registry_drift.py` → **102/102 PASS**.
- `tracka_resume_check.py` → **pass:true, 17 checks, network:false**.
- `fclr016_v5_admissibility_report.py --bogus` / `fclr016_v5_promotion_dryrun.py --bogus` → parseable JSON refusals, `exit!=0`, no traceback. `--bogus --json` / `tracka_resume_gate.py --bogus --json` / `tracka_operator_report.py --bogus --json` prefixes parseable (usage/refusal context).
- Gate 4 baseline `run_funding_ablations.py` → clean honest verdict (PILOT/INCONCLUSIVE, primary CI spans 0, data-sufficiency criteria not met).
- `run_funding_ablations.py --include-cache --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --start 2024-04-01 --end 2024-09-30 --out-suffix _v3_30d_verify` → **reproduces sealed numbers exactly**: `n_obs=12969, n_blocks=120, E_vs_A point=0.4879023125556385, 95% CI [-0.042160777324701186, 1.1973379300276015] spans 0`; verify outputs removed. Sealed artifacts untouched.

### Hard stops (genuine — do NOT re-probe in loops)
1. Track A/H004 Hyperliquid `data/events|fills` 2026-11 = 404 (probed 2026-11-08T07:28Z/07:30Z), `data_through=2026-10`.
2. v5 `all_go=false`, `confirmatory_outcomes_permitted=false`, terms `EXPLICIT_BLOCKER_UNRESOLVED` (`fabricated=false`). Economic/overlay claims **INELIGIBLE**.
3. Resume only on triggers below (fresh prereg before outcomes where required).

### Current evidence state (honest; preserve nulls)
- **Gate 4 delivered (pre-registered, claim-worthy data-sufficiency MET, forecast skill NOT demonstrated):** `GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D` (5 sym BTC/ETH/SOL/XRP/BNB, 2024-04-01..2024-09-30, 4×30-day walk-forward, 7d purge/embargo, block bootstrap seed=12345 reps=2000 block=24h). Primary **E (RV+funding trails) vs A (RV-only): +0.488, 95% CI [-0.042, 1.197] spans 0** (n_obs=12969, n_blocks=120). A_rv_only best aggregate QLIKE (0.798). **Verdict: PILOT/INCONCLUSIVE on primary; no incremental forecast skill; H001 NOT_SUPPORTED; risk overlay INELIGIBLE.** Sealed: `research_state/evaluation_summary_funding_v3_30d.md`, `research_state/run_manifest_funding_v3_30d.json` (SHA-256 `774e4a9f…` / `9fd540bd…`), prereg `pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md`. **Do not re-run variants chasing significance (threshold shopping).**
- **Track C FCLR-013 (2026 Q3, 5 sym, 1×30d block):** primary C2 vs B1 -1.32%, CI crosses 0, <2% floor, block-count NOT_MET → **NOT_SUPPORTED/gate NOT_MET**. FCLR-011 sealed PASS preserved.
- **Data ceiling (local, admissible):** raw Jan–Mar 2024 zips; `research_state/data_cache` has BTC/ETH/SOL/XRP/BNB 2024-01..12 (+ extended 2025/2026 for some) in monthly `{SYMBOL}_{YYYY_MM}` layout. **FCLR-017 audit (planning only):** 2024-04..09 5-sym cache calendar/lineage/coverage CONSISTENT with v3-30d design window (no missing days, no quarantine/placeholder anomalies, funding present). This is **not** confirmatory GO, not model evidence, and does not resolve v5 terms/admissibility. Confirmatory 2024-04..09 remains bounded by `PROVENANCED_CONFIRMATORY_RANGES` + manifest/terms evidence + frozen prereg before outcomes.

### Single highest-value next task — HEAVY, measurable, unblocked (no coasting)
**FCLR-NEXT-140 (P0 — heavy Track C prereg-readiness engineering, no new claims): build a deterministic, read-only Gate 4 prereg-readiness/draft design matrix from local evidence (`fclr017` latest + `run_manifest_funding_v3_30d.json` provenance/admissibility metadata where present + `PROVENANCED_CONFIRMATORY_RANGES`/v5 blocker state) that enumerates candidate windows and emits a *DRAFT, NOT FROZEN* prereg skeleton for the next feasible Gate 4 design — without computing confirmatory outcomes, without freezing/promoting, and without overwriting sealed artifacts.**
1. **Reproduce baseline first (no network):** run the focus campaign block below — all must pass before/after changes.
2. **Heavy code work:** add `scripts/fclr018_gate4_prereg_readiness_matrix.py` (read-only, no network, no model-outcome computation). Consume `research_state/fclr017_local_audit/fclr017_gate4_cache_audit_latest.json` and sealed v3 manifest/prereg references (read-only). For candidate windows present locally with complete calendar coverage (start from 2024-04..09 as evidenced; include 2024-10..12 / other local cache windows only as **EXPLORATORY/PROVENANCE_UNVERIFIED** unless explicit manifest/terms/provenance evidence exists in-repo), compute deterministic design feasibility fields: symbols, span days, max non-overlapping 30-day blocks, 7d purge/embargo fit, block-count gate (`>=3`), provenance status (`IDENTITY_VERIFIED_BOUNDED_FCLR015` only for evidenced 2024-04..09 slice; else `UNVERIFIED`), confirmatory eligibility (`ELIGIBLE_ONLY_IF_FRESH_FROZEN_PREREG_AND_ADMISSIBILITY_GATES_GREEN` / `INELIGIBLE_EXPLORATORY`), v5 terms blocker state (unresolved). Emit deterministic JSON+MD under `research_state/fclr018_local_audit/` with `prereg_status=DRAFT_NOT_FROZEN`, `no_confirmatory_outcomes=true`, `exploratory_only=true`, `no_network=true`, `not_go_for_confirmatory_outcomes=true`, and a clearly labeled **DRAFT prereg skeleton** section (hypotheses, primary contrast candidates, split/block/bootstrap params, leakage controls, acceptance/stop rules) — **not frozen, not promoted, not executable as confirmatory**.
3. **Add deterministic tests:** tmp-fixture unit tests (no network) for block-count math, confirmatory/exploratory labeling, `PROVENANCED/UNVERIFIED` classification, v5 unresolved terms forcing confirmatory ineligibility, draft-not-frozen metadata, and no sealed overwrite.
4. **Measurable acceptance (no claims):** matrix reproducible from local evidence; clearly separates 2024-04..09 bounded confirmatory-candidate path from unprovenanced exploratory windows; emits draft skeleton only. `python -m unittest discover tests -q` → **>=896 OK, 0 failures** (higher with added tests). Register script in scope registry (drift PASS).
5. **Gate discipline:** planning/draft evidence only — **does not** authorize confirmatory outcomes, freeze/promote, overlay, or H001 status change. Any claim-worthy run requires **fresh frozen prereg before outcomes**; 2024-04..09 confirmatory bounded by `PROVENANCED_CONFIRMATORY_RANGES` + manifest/terms evidence + admissibility guards; v5 `all_go=false` / terms `EXPLICIT_BLOCKER_UNRESOLVED`.
6. **No** new status-only/poller/wrapper/scheduler families, no competing handoff files, no `.github/workflows` edits.

### Focus campaign (run every session — future agents must do heavy work)
```bash
pip install -r requirements.txt
python -m unittest discover tests -q
python scripts/check_tracka_scope_registry_drift.py
python scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass', d['pass'], 'checks', len(d['checks']), 'network', d['network'])"
python scripts/fclr016_v5_admissibility_report.py --bogus 2>&1 | tail -1
python scripts/fclr016_v5_promotion_dryrun.py --bogus 2>&1 | tail -1
python scripts/run_funding_ablations.py   # Gate 4 baseline pilot (must run clean, honest verdict)
python scripts/run_funding_ablations.py --include-cache --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --start 2024-04-01 --end 2024-09-30 --out-suffix _v3_30d_verify  # must give n_obs=12969, n_blocks=120, CI spans 0; no sealed overwrite
python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_resume_gate.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_operator_report.py --bogus --json 2>&1 | head -c 200
```
Acceptance: >=896 tests OK (higher with added deterministic tests); refusals parseable/exit!=0/no traceback; drift 102/102 (or higher after registration); resume 17/17 pass; ablations honest verdict; bounds respected; **measurable heavy delta delivered** (no status-only). Remove `_v3_30d_verify` outputs after verification.

### Resume triggers (only then — preregister BEFORE outcomes)
1. **Track A/H004:** unauthenticated Hyperliquid `data/events` or `data/fills` YYYY-MM >=2026-11 with **HTTP 200 + verified content** (probe specific months only; no loop) OR admissible unauthenticated observed-liquidation source passing full-manifest GO. Fresh experiment ID + prereg before outcomes; modeled!=observed.
2. **v5 terms resolved (human/legal):** add `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (verifiable facts only; `fabricated=false`, `status=RESOLVED_VERIFIED`, frozen scope). Reconcile refs/hashes; promote prereg to frozen only after all guards green; run package/validator/report/preflight/promotion-dryrun `--expect-go` as applicable (no data load on refusal). Confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New claim-worthy Track C run:** loader-compatible admissible local panel, >=5 sym & >=3 non-overlapping 30-day blocks, **fresh frozen prereg before outcomes** (confirmatory within `PROVENANCED_CONFIRMATORY_RANGES` 2024-04..09 with manifest/terms evidence as required; else exploratory). A DRAFT prereg skeleton is **not** sufficient.

### Do-NOT
Fabricate terms/license/reviews or data; run confirmatory outcomes on unprovenanced/incomplete/blocked data or without frozen prereg; freeze/promote while blockers exist; reopen sealed anchors/holdouts; threshold-shop or relax gates post-hoc; merge Track A/B/C semantics or modeled!=observed; claim economic/overlay value; re-probe absent months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files.

---

## INITIAL TASK MESSAGE — 2026-11-08T13:13:46Z (next session entry point)
**Next task:** FCLR-NEXT-140 — build `scripts/fclr018_gate4_prereg_readiness_matrix.py` (read-only, no network, no confirmatory outcomes) + tests, emitting a DRAFT (not frozen) prereg skeleton under `research_state/fclr018_local_audit/`. Run the focus campaign block first; preserve sealed artifacts; do not promote/freeze. Track A remains blocked (no re-probe); v5 terms unresolved.
