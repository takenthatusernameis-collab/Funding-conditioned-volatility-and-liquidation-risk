## Initial Task Message (2026-11-08T07:21Z, git HEAD `f252885b3`) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** (1) funding-conditioned volatility forecasting, (2) liquidation risk (Track A observed / Track B modeled — never conflated). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Session FCLR-NEXT-133 delivered (P0, code/test hardening — tmp-isolated; no network/kline/funding/outcome loaders; no real `research_state` writes)

**P0 completed:** `fclr016_validate_v5_admissibility.py` refusal-parity hardening for `--bogus`/unknown args + malformed top-level JSON types. Fail-closed: every structural defect emits stable machine-readable JSON on `stdout` (`ok:false`, `all_go:false`, `confirmatory_outcomes_permitted:false`, no GO claim, `expect_go_refused:true`, exit 2) and loads NO data/network/outcomes.

1. **Unknown args (`--bogus`) / missing required args / argparse errors:** caught via `SystemExit`, emitted as `_cli_refusal` JSON (exit 2), usage kept on `stderr`.
2. **Malformed JSON top-level types:** `load()` now requires a top-level JSON object; array / string / number / null roots refused (`cannot load artifact: top-level JSON must be an object...`, exit 2) instead of an uncaught `AttributeError` traceback.
3. **Malformed syntax / unreadable / nonexistent paths:** read+parse wrapped in try/except → `fail("cannot load artifact: ...")` / `fail("missing: ...")` JSON refusal, exit 2; directory paths refused (`Is a directory`).
4. **Outer `except Exception`** around `main()` so any unexpected defect still yields machine-readable refusal (exit 2), never a traceback.
5. All pre-existing business-logic refusals (draft/frozen/terms/resolution/scope/refs/hash guards) unchanged; `--expect-go` contract unchanged (exit 2 on blocked package).
6. **New regression:** `tests.test_fclr016_v5_admissibility_validator.TestCliRefusalHardening` (9 tests: `--bogus`, missing required arg, top-level array/string/number/null, malformed syntax, directory, nonexistent path). Validator file now 14 tests, all pass.
7. **Fixed 2 pre-existing bugs** in `tests.test_fclr016_v5_cli_refusal_parity_132`: (a) `all()` refusal assertion incorrectly required the synthetic-GO scenario (expected_refused=False) to be refused — now restricted to non-synthetic scenarios; (b) `j.get("result", {}).get("all_go")` read a non-existent key — now `result_summary`.
8. **Targeted v5 suites all OK:** `test_fclr016_v5_promotion_dryrun`, `test_fclr016_v5_preflight_summary`, `test_fclr016_v5_admissibility_report`, `test_fclr016_v5_admissibility_hardening`, `test_fclr016_v5_admissibility_guard`, `test_fclr016_v5_admissibility_validator`, `test_fclr016_v5_confirmatory_cli_refusal_e2e`, `test_fclr016_v5_cli_refusal_parity_132` → **100 tests, 0 failures**.
9. **Full suite:** `python -m unittest discover tests -q` → 845 tests (was 836; +9 new hardening). failures=7, errors=21 — **identical pre-existing set** to before this session (loader import errors `test_data_loading`/`test_funding_ablations*`/`test_timestamp_parsing`; `tracka_hardening_114/115` import errors; `tracka_hardening_116–119` errors; registry-drift `MISSING_IN_REGISTRY` for v5 scripts `fclr016_v5_admissibility_report.py`, `fclr016_v5_preflight_summary.py`, `fclr016_v5_promotion_dryrun.py`, `fclr016_v5_terms_evidence_template.py`, `fclr016_validate_v5_admissibility.py`). The 2 previously-failing 132 tests now pass; **no new failures or errors introduced**.
10. **Invariants:** `tracka_resume_check.py` => `pass:true` (17/17, `network:false`, `writes_real_research_state:false`, `live<=1 && non_20261104T==0`). `tracka_resume_gate.py --bogus --json` / `tracka_resume_check.py --bogus` stable non-zero (rc=1). No competing handoff files. Canonicals `experiment_frontier.json`/`run_manifest.json`/`evaluation_summary.md` unchanged. No `.github/workflows` edits. No status-only/poller/wrapper/scheduler families added.

### Verified current state (do not re-litigate without new evidence)

- Protocol FROZEN 2026-11-06T20:36:32Z. Gates G1/G2/G3 satisfied in scope; G4 blocked.
- **H001 NOT_SUPPORTED** on all claim-worthy panels (FCLR-003/006/008/013, v3 30d/5sym). **Forecast gate NOT_MET; risk-overlay INELIGIBLE; no economic/overlay value claim.**
- **Track C:** sealed/locked; unsealed confirmatory panels exhausted (needs >=5 symbols, >=3 non-overlapping 30-day blocks).
- **Track A BLOCKED/EXHAUSTED.** `data_through=2026-10`; Hyperliquid 2026-11..2027-02 absent; `live<=1`, `non_20261104T==0`. **NO re-probe absent months. PREREGISTER BEFORE outcomes; modeled != observed.**
- **Track B CLOSED_NEGATIVE.** Never conflate.
- **v5 confirmatory package `all_go=false`, `confirmatory_outcomes_permitted=false`.** Terms hard blocker `EXPLICIT_BLOCKER_UNRESOLVED` (`fabricated=false`). **No fabricated terms/reviews; no freeze/promote while blocked; no confirmatory outcomes on refusal.**
- Records: `final_confirmatory_verdict.md` (CLOSEOUT COMPLETE, H001 NOT_SUPPORTED), `negative_results_report.md`, `final_record_closure_audit.md`.

### Single highest-value next task (heavy, measurable — do not coast)

**FCLR-NEXT-134 (P0, end-to-end v5 refusal verification + resume-trigger watch):** Complete the refusal-parity surface across all v5 entry points and confirm no regressions, then hold for a resume trigger before any research work.

- Re-run the full v5 targeted set + `python -m unittest discover tests -q`; record exact counts; confirm the pre-existing failure/error set is unchanged and no new regressions (the 7 registry-drift failures and 21 errors are pre-existing and unrelated to v5; do not expand scope into the tracka registry without a separate decision).
- Confirm the 4 v5 check CLIs (preflight/report/dryrun/validator) + `run_funding_ablations --check-admissibility-package --expect-go` all emit stable non-GO refusal contracts on the real blocked package and never load data on refusal.
- Confirm no competing artifacts/pollers/wrappers/schedulers, no `.github/workflows` edits, `tracka_resume_check.py` 17/17.
- **Do not start confirmatory outcomes or Track A re-probe.** Research remains blocked until a resume trigger fires (see below). The only legitimate forward work while blocked is bounded, credential-free source discovery/diagnostics per RESEARCH_PROMPT.md priority 2 (source feasibility map) — execute only a concrete, bounded free-data probe if one is identified; otherwise hold.

### Commands
```bash
pip install -r requirements.txt
python3 scripts/fclr016_v5_preflight_summary.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json | head -c 400; echo
python3 scripts/fclr016_v5_promotion_dryrun.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json --json-only | python3 -c "import sys,json; d=json.load(sys.stdin); print('all_go',d['all_go'],'cop',d['confirmatory_outcomes_permitted'],'ok',d['ok'])"
python3 scripts/fclr016_validate_v5_admissibility.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('validator ok',d['ok'],'all_go',d['all_go'],'cop',d['confirmatory_outcomes_permitted'])"
python3 scripts/run_funding_ablations.py --check-admissibility-package research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json --expect-go >/dev/null 2>&1; echo "package expect-go rc=$?"
python3 -m unittest tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e tests.test_fclr016_v5_cli_refusal_parity_132 -q
python -m unittest discover tests -q > /tmp/full_suite_134.txt 2>&1; tail -3 /tmp/full_suite_134.txt
python3 scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass',d['pass'],'checks',len(d['checks']))"
```

### Resume triggers (only then — preregister BEFORE outcomes)
1. **Track A/H004:** unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200) OR admissible unauthenticated observed-liquidation source passing full-manifest GO rubric. Fresh experiment ID, prereg before outcomes, modeled!=observed.
2. **v5 terms resolved by human/legal review:** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only; `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope. Reconcile refs/hashes; promote prereg to frozen only after all guards green; run package/validator/report/preflight/promotion-dryrun with `--expect-go` as applicable (no data load on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New admissible Track C data:** >=5 symbols, >=3 non-overlapping 30-day blocks, unauthenticated/admissible, fresh prereg before outcomes.

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete/blocked data; freeze/promote prereg while blockers exist; reopen sealed anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A absent months; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files; run confirmation without fresh pre-registration + new admissible data.
