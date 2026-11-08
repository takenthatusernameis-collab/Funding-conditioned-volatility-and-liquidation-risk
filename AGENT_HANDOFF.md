## Initial Task Message (2026-11-08T05:50:15Z, git HEAD `47d881001` at session entry) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority (inferred):** (1) funding-conditioned volatility forecasting, (2) liquidation risk (Track A observed / Track B modeled — never conflated). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Session verification (2026-11-08T05:50Z, do not re-run as status-only)
- `python3 scripts/fclr016_v5_preflight_summary.py ...` (4 blocked v5 artifacts) => `ok:true, all_go:false, confirmatory_outcomes_permitted:false`; explicit refusals present (terms unresolved, prereg draft/GO claims, refs mismatch, completeness verdict inconsistency); no outcome data loaded.
- `python3 scripts/fclr016_v5_promotion_dryrun.py ...` (4 blocked v5 artifacts) => `ok:true, all_go:false, confirmatory_outcomes_permitted:false`; `i_expect_go_blocked_contract` refused with stable non-GO contract; `j_synthetic_go_fixture_only` is labeled synthetic fixture only (never real evidence).
- `python3 -m unittest tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q` => green in this environment (validator emitted `ok:true`).
- `python3 scripts/tracka_resume_check.py` => `pass:true` (17/17 pass fields, `network:false`, `writes_real_research_state:false`, probes semantics pass `live<=1 && non_20261104T==0`).
- `tracka_resume_gate.py --bogus --json` emits stable JSON refusal/usage contract; `tracka_resume_check.py --bogus` emits stable CLI refusal. No competing handoff files (`AGENT_HANDOFF.md` only). `git status` clean at entry except prior session artifacts already reflected in repo state as applicable.

### Delivered previously (do not repeat)
- v5 admissibility stack present/green in targeted suites: validator, guard, package/report/preflight, confirmatory CLI refusal e2e, and `scripts/fclr016_v5_promotion_dryrun.py` + `tests/test_fclr016_v5_promotion_dryrun.py` (mandatory refusal/acceptance matrix a–j; tmp-isolated; no network/kline/funding/outcome loaders; canonicals/real inputs byte-identical in tests).
- FCLR-NEXT-110..131 guard/harness/CLI/refusal hardening delivered historically (tmp-isolated, no network/parquet/outcome reads, no real `research_state` writes where required, resume/gate/operator/drift pass as recorded). Treat as complete unless a concrete failing test/regression is found.

### Verified current state (do not re-litigate without new evidence)
- **Protocol:** `research_state/research_protocol.md` FROZEN 2026-11-06T20:36:32Z. Gates: G1 data, G2 frozen, G3 met (`rv_baseline_complete`), G4 blocked (insufficient claim-worthy data/uncertainty on current panels).
- **H001 (funding-conditioned volatility vs RV-only): NOT_SUPPORTED** on every claim-worthy panel (FCLR-003, FCLR-006, FCLR-008, FCLR-013, v3 30d/5sym). Primary C2 vs B1 fails CI/block/materiality gates. **Forecast gate NOT_MET; risk-overlay phase INELIGIBLE. No economic/overlay value claim.**
- **Track C (volatility/stress):** sealed/locked; unsealed confirmatory panels exhausted (needs >=5 symbols, >=3 non-overlapping 30-day blocks). No further confirmatory cell feasible without NEW admissible data.
- **Track A (observed liquidation risk): BLOCKED/EXHAUSTED.** `data_through=2026-10`; Hyperliquid 2026-11..2027-02 absent; probes exhausted (resume check: `live<=1`, `non_20261104T==0`). **NO re-probe absent months.** Resume trigger only: unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200) OR an admissible unauthenticated observed-liquidation source passing the full-manifest GO rubric/gate. **PREREGISTER BEFORE inspecting outcomes; modeled != observed.**
- **Track B (modeled boundary breach): CLOSED_NEGATIVE.** Never conflate modeled vs observed.
- **v5 confirmatory package (2025+): `all_go=false`, `confirmatory_outcomes_permitted=false`.** Hard blocker (not agent-resolvable): Binance Vision/data-use terms not human-verified (`EXPLICIT_BLOCKER_UNRESOLVED`, `fabricated=false`). **Agent must not fabricate legal terms/reviews, must not freeze/promote prereg while blockers exist, must not load confirmatory outcome data on refusal.**
- Records preserved: `research_state/final_confirmatory_verdict.md` (CLOSEOUT COMPLETE, H001 NOT_SUPPORTED), `research_state/negative_results_report.md` (null/failed/inconclusive), `research_state/final_record_closure_audit.md`. Canonicals `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` must not be mutated by handoff/status-only work.

### Single highest-value next task (heavy, measurable — do not coast)
**FCLR-NEXT-132 (P0, code/test hardening): v5 admissibility CLI/guard refusal parity under edge seams.** The confirmatory program remains CLOSED NEGATIVE on current admissible data; this is hardening only, not a claim of confirmatory progress.

**Mandatory deliverables (tmp-isolated, deterministic, no network, no kline/funding/outcome loaders, no real `research_state` writes):**
1. **Empty/unreadable/nonexistent data-path seams under valid prereg/package refs:** prove confirmatory/expect-go paths remain blocked with stable machine-readable reason codes and that **no outcome/data loader is called**. Cover `scripts/run_funding_ablations.py` confirmatory refusal/admissibility-package check and relevant guard contracts; add/extend tests only where a real gap exists.
2. **CLI argparse/edge-case contracts:** bulletproof `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_v5_admissibility_report.py`, and `scripts/fclr016_v5_promotion_dryrun.py` for missing/extra args, wrong file order/types where applicable, malformed JSON, unreadable files, and candidate-path edge cases. Refusal output must remain stable: `ok:false` or explicit refusal contract, `all_go:false` where applicable, `confirmatory_outcomes_permitted:false`, **no GO claim**.
3. **Cross-CLI parity + canonical/output integrity:** same real blocked 4-artifact package => consistent blocked/refusal semantics across `run_funding_ablations --check-admissibility-package`, validator, preflight, report, promotion-dryrun. Same synthetic tmp GO fixture (labeled `synthetic_test_fixture=true`, `no_real_terms_evidence=true`) => consistent synthetic-only GO semantics; **never mutate canonicals/real inputs; never treat synthetic as real evidence.**
4. **Regression evidence:** run targeted v5 suite(s) plus `python -m unittest discover tests -q`; record exact counts/outcomes in this handoff. Keep existing tests green; add only legitimate tests.
5. **Invariants unchanged:** Track A resume 17/17 pass, bogus CLI stable refusals, probes `live<=1 && non_20261104T==0`, no competing campaign markers, no new poller/wrapper/scheduler/status-only families, root bounds unchanged except legitimate code/test/handoff edits.

### Commands
```bash
pip install -r requirements.txt
python3 scripts/fclr016_v5_preflight_summary.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 scripts/fclr016_v5_promotion_dryrun.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 -m unittest tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q
python -m unittest discover tests -q
python3 scripts/tracka_resume_check.py
python3 scripts/tracka_resume_gate.py --bogus --json 2>&1 | head -c 220; echo
python3 scripts/tracka_resume_check.py --bogus 2>&1 | head -c 180; echo
python3 scripts/tracka_operator_report.py --bogus --json 2>&1 | head -c 220; echo
```

### Resume triggers (only then — preregister BEFORE outcomes)
1. **Track A/H004 liquidation risk:** unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200) OR admissible unauthenticated observed-liquidation source passing full-manifest GO rubric. Fresh experiment ID, prereg before outcomes, modeled!=observed.
2. **v5 terms blocker resolved by human/legal review:** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only (`terms_url_reviewed`, `access_date_utc`, version/snapshot or justified `not_provided_by_source`, relevant clause summary, human/legal `reviewer_role`, conclusion, conditions/restrictions, evidence artifacts/hashes, `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope). Reconcile `admissibility_refs_sha256`/paths. Promote prereg to frozen only after all guards green. Run validator/package/report/preflight/promotion-dryrun with `--expect-go` where applicable (must not load data on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New admissible funding/volatility data (Track C context):** >=5 symbols, >=3 non-overlapping 30-day blocks, unauthenticated/admissible, fresh prereg before outcomes.

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete/blocked data; freeze/promote prereg while blockers exist; reopen sealed anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A absent months; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files; run confirmation without fresh pre-registration + new admissible data.
