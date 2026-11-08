## Initial Task Message (2026-11-08T07:27Z, git HEAD `ccb8b7e6d`) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** (1) funding-conditioned volatility forecasting, (2) liquidation risk (Track A observed / Track B modeled — never conflated). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Session FCLR-NEXT-134 delivered (P0, end-to-end v5 refusal verification + resume-trigger watch; read-only checks; no network/kline/funding/outcome loaders; no real `research_state` writes)

**P0 completed (verification-only; no new confirmatory outcomes, no Track A re-probe):**

1. **v5 targeted suite (8 modules):** `test_fclr016_v5_promotion_dryrun`, `preflight_summary`, `admissibility_report`, `admissibility_hardening`, `admissibility_guard`, `admissibility_validator`, `confirmatory_cli_refusal_e2e`, `cli_refusal_parity_132` → **100 tests, 0 failures, OK**.
2. **Full suite:** `python -m unittest discover tests -q` → **845 tests, 7 failures, 21 errors** (ran ~79s in this env). This is the **identical pre-existing** set vs FCLR-NEXT-133 baseline: loader import errors (`test_data_loading`/`test_funding_ablations*`/`test_timestamp_parsing`), `tracka_hardening_114/115` import errors, `tracka_hardening_116–119` errors, and 7 registry-drift failures `MISSING_IN_REGISTRY` for v5 scripts (`fclr016_v5_admissibility_report.py`, `fclr016_v5_preflight_summary.py`, `fclr016_v5_promotion_dryrun.py`, `fclr016_v5_terms_evidence_template.py`, `fclr016_validate_v5_admissibility.py`). **No new failures/errors introduced.**
3. **Real blocked package refusal contracts (no data load):** all 4 package-check entry points refuse the current blocked package with non-GO, `confirmatory_outcomes_permitted=false`:
   - `fclr016_v5_preflight_summary.py` (4 positional args) → `all_go:false, ok:true` (summary).
   - `fclr016_v5_promotion_dryrun.py --json-only` (4 positional) → `all_go False cop False ok True`.
   - `fclr016_validate_v5_admissibility.py` (`--provenance-manifest/--completeness-audit/--terms-evidence/--prereg-draft`) → `validator ok True all_go False cop False`.
   - `fclr016_v5_admissibility_report.py` (4 positional) → `report all_go False cop False`.
   - `run_funding_ablations.py --check-admissibility-package <4> --expect-go` → JSON `ok:true all_go:false cop:false expect_go_refused:true`, **rc=2** (stable refusal; no data/outcome load).
4. **CLI `--bogus` behavior (recorded, no scope expansion):** `fclr016_validate_v5_admissibility.py --bogus` and `tracka_resume_gate.py/check.py --bogus` emit usage/non-zero (stable refusal path exercised). `fclr016_v5_admissibility_report.py --bogus` and `fclr016_v5_promotion_dryrun.py --bogus` emit argparse usage to stderr/stdout (non-JSON) — **not the hardened JSON-refusal form**; changing them is out of scope for 134 but is a small candidate hardening if a future session needs uniform machine-parseable refusal on all v5 CLIs.
5. **Track A resume-trigger watch (local evidence only, bounded, no re-probe of absent months):** `research_state/ironflow_monitor_state.json` `data_through=2026-10`; `ironflow_probe_digest_latest.json`/`hl_coverage_probe.json` show no 2026-11+ signal; **0 local cached 2026-11+ liquidation/event/fill artifacts** under `research_state/data_cache`. **No trigger fired. No re-probe performed.**
6. **Invariants:** `tracka_resume_check.py` => `pass:true` (17/17, `network:false`, `writes_real_research_state:false`, `live<=1 && non_20261104T==0`). No competing handoff files. Canonicals `experiment_frontier.json`/`run_manifest.json`/`evaluation_summary.md` unchanged. No `.github/workflows` edits. No status-only/poller/wrapper/scheduler families added.

### Verified current state (do not re-litigate without new evidence)

- Protocol FROZEN 2026-11-06T20:36:32Z. Gates G1/G2/G3 satisfied in scope; G4 blocked.
- **H001 NOT_SUPPORTED** on all claim-worthy panels (FCLR-003/006/008/013, v3 30d/5sym). **Forecast gate NOT_MET; risk-overlay INELIGIBLE; no economic/overlay value claim.**
- **Track C:** sealed/locked; unsealed confirmatory panels exhausted (needs >=5 symbols, >=3 non-overlapping 30-day blocks).
- **Track A BLOCKED/EXHAUSTED.** `data_through=2026-10`; Hyperliquid 2026-11..2027-02 absent; `live<=1`, `non_20261104T==0`. **NO re-probe absent months. PREREGISTER BEFORE outcomes; modeled != observed.**
- **Track B CLOSED_NEGATIVE.** Never conflate.
- **v5 confirmatory package `all_go=false`, `confirmatory_outcomes_permitted=false`.** Terms hard blocker `EXPLICIT_BLOCKER_UNRESOLVED` (`fabricated=false`). **No fabricated terms/reviews; no freeze/promote while blocked; no confirmatory outcomes on refusal.**
- Records: `final_confirmatory_verdict.md` (CLOSEOUT COMPLETE, H001 NOT_SUPPORTED), `negative_results_report.md`, `final_record_closure_audit.md`.

### Single highest-value next task (heavy, measurable — do not coast)

**FCLR-NEXT-135 (P0, bounded free-data feasibility probe — RESEARCH_PROMPT priority 2; OR hold):** Research is blocked on all confirmatory tracks (no v5 terms resolution, no Track A trigger, no new admissible Track C panel). The only legitimate forward work is **bounded, unauthenticated, credential-free source discovery/diagnostics** that can materially change Track A/C feasibility.

- **Execute one concrete probe:** check Hyperliquid public `data/events/YYYY-MM.parquet` (or `data/fills/YYYY-MM.parquet`) availability for the **next month beyond known `2026-10` only if a single small HEAD/GET is cheap and non-repetitive** (record exact URL, HTTP status, bytes/headers, access date) — **do not loop/retry absent months, do not create polling**. If the probe shows HTTP 200 with verifiable content, STOP outcomes work: record evidence, update registry/handoff, and require **fresh experiment ID + preregistration BEFORE inspecting outcomes** (modeled!=observed).
- **If probe is not warranted or shows not-yet-available:** record the single check result and **hold**. Do not generate status artifacts, wrappers, or schedulers.
- **Optional small hardening (only if isolated, <30min, no scope creep):** make `fclr016_v5_admissibility_report.py`/`promotion_dryrun.py` `--bogus` emit stable JSON refusal (parity with validator 133). Do **not** touch the 7 registry-drift failures / 21 pre-existing env/import errors unless scoped separately.

### Commands
```bash
python3 -m unittest tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e tests.test_fclr016_v5_cli_refusal_parity_132 -q
python -m unittest discover tests -q 2>&1 | tail -3
python3 scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass',d['pass'],'checks',len(d['checks']))"
python3 scripts/run_funding_ablations.py --check-admissibility-package research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json --expect-go >/dev/null 2>&1; echo "package expect-go rc=$?"
# bounded single-month probe only if justified (example pattern; do NOT loop):
# curl -sI --max-time 20 'https://.../data/events/2026-11.parquet' | head -5   (record result; no retry storm)
```

### Resume triggers (only then — preregister BEFORE outcomes)
1. **Track A/H004:** unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200, verified) OR admissible unauthenticated observed-liquidation source passing full-manifest GO rubric. Fresh experiment ID, prereg before outcomes, modeled!=observed.
2. **v5 terms resolved by human/legal review:** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only; `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope. Reconcile refs/hashes; promote prereg to frozen only after all guards green; run package/validator/report/preflight/promotion-dryrun with `--expect-go` as applicable (no data load on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New admissible Track C data:** >=5 symbols, >=3 non-overlapping 30-day blocks, unauthenticated/admissible, fresh prereg before outcomes.

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete/blocked data; freeze/promote prereg while blockers exist; reopen sealed anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe absent months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files; run confirmation without fresh pre-registration + new admissible data.


---
