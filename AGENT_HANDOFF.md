## Initial Task Message (2026-11-08T05:52:00Z, git HEAD `47d881001` before this edit) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** funding-conditioned volatility forecasting + liquidation risk (both tracks in scope). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Delivered this session (do not repeat)

- `scripts/fclr016_v5_promotion_dryrun.py` — deterministic, read-only, no network, no kline/funding/outcome loaders, no canonical mutation. Inputs: 4 package artifact paths + optional `--candidate-terms-evidence` + optional `--candidate-prereg` (copied/evaluated in tmp; never mutates inputs/canonicals). Emits JSON + markdown with per-scenario status, exact refusal reasons, required human fields, forbidden values/shortcuts, and explicit statement: *confirmatory outcomes still prohibited until real human-verified resolved terms evidence exists in-repo and the real package passes all guards*.
- `tests/test_fclr016_v5_promotion_dryrun.py` — 20 tmp-isolated tests; monkeypatches/booms data/outcome loader paths to prove they are never used; keeps canonicals and real package inputs byte-identical.
- Mandatory matrix covered (a–j): real blocked package refused; missing required human fields refused; `fabricated=true` refused; agent-only reviewer refused; `TEMPLATE_NOT_EVIDENCE`/`EXPLICIT_BLOCKER_UNRESOLVED` treated as resolved refused; draft promoted/frozen/GO claims refused; provenance GO while terms unresolved refused; `admissibility_refs_sha256` mismatch refused; completeness verdict/pass inconsistencies refused; confirmatory `--expect-go` on blocked package refused with stable contract; synthetic fully-satisfied GO reported **only** on labeled tmp fixture (`synthetic_test_fixture=true`, `no_real_terms_evidence=true`) and never as real evidence / never mutating canonicals / never loading data.
- Verified this session: `python3 -m py_compile scripts/fclr016_v5_promotion_dryrun.py tests/test_fclr016_v5_promotion_dryrun.py`; `python3 -m unittest tests.test_fclr016_v5_promotion_dryrun -q` => 20 OK; `python3 -m unittest tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q` => 95 OK; `python3 scripts/fclr016_v5_promotion_dryrun.py ...` (4 real blocked artifacts) => `ok:true, all_go:false, confirmatory_outcomes_permitted:false`; `python3 scripts/tracka_resume_check.py` => pass (17/17, probes==2/live==1, no baseline drift/content-hash issues reported). `research_state/ironflow_fastpath_cache.json` appeared modified in the working tree during checks; treat as unrelated/uncommitted state unless intentionally produced — do not fold into handoff claims.

### Inferred single initial task (next session)

**Heavy companion hardening on v5 admissibility CLIs/guards (mandatory, measurable).** The confirmatory program remains CLOSED NEGATIVE on all current admissible data; no confirmatory outcomes are permitted. Deliver legitimate hardening tests/code only where gaps exist; do not add status-only files, pollers, wrappers, schedulers, or competing handoff files.

**Required work:**
1. **Empty/unreadable data-path seams under valid prereg**: prove that confirmatory/expect-go paths remain blocked with stable reason codes when package/prereg refs are valid but data paths are empty/unreadable/nonexistent — and crucially that no outcome/data loader is called. Add tmp-isolated tests around `run_funding_ablations` confirmatory refusal and/or package/guard CLI contracts as needed.
2. **CLI argparse/edge-case contracts (3 CLIs)**: bulletproof `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_v5_admissibility_report.py` (if present), and `scripts/fclr016_v5_promotion_dryrun.py` for missing/extra args, wrong file types/order where applicable, malformed JSON, unreadable files, candidate-path edge cases, and stable machine-readable refusal output (`ok:false`, `all_go:false`, `confirmatory_outcomes_permitted:false`, no GO claim).
3. **Cross-CLI parity + canonical output integrity**: assert parity of refusal/GO semantics across `run_funding_ablations --check-admissibility-package`, validator, preflight, report (if present), and promotion-dryrun for the same real blocked package and for the same synthetic tmp GO fixture; ensure canonicals and real inputs remain byte-identical.
4. **Regression**: run full `python -m unittest discover tests -q`; keep all existing tests green and add only legitimate tests. Record the final count in this handoff after execution.
5. **Invariants**: `tracka_resume_check` 17/17, `tracka_resume_gate --bogus`/operator/report bogus stable JSON exit contracts, root bounds, probes==2, no competing campaign markers, no new poller/wrapper/scheduler/status-only families.

### Verified current state (do not re-litigate without new evidence)

- HEAD `47d881001` at start of this session (new uncommitted files now: `scripts/fclr016_v5_promotion_dryrun.py`, `tests/test_fclr016_v5_promotion_dryrun.py`, `AGENT_HANDOFF.md` update; `research_state/ironflow_fastpath_cache.json` may be locally modified by checks — inspect before commit). `AGENT_HANDOFF.md` remains the single durable handoff.
- `research_state/research_protocol.md` FROZEN 2026-11-06T20:36:32Z. Gates: G1 data, G2 frozen, G3 met (`rv_baseline_complete`), G4 blocked on unmet data-sufficiency/uncertainty on current panels.
- **H001 (funding-conditioned volatility vs RV-only): NOT_SUPPORTED** on every claim-worthy panel (FCLR-003, FCLR-006, FCLR-008, FCLR-013, v3 30d/5sym). Primary contrast C2 vs B1 fails CI/block/materiality gates on each. Risk-overlay phase INELIGIBLE. No economic/overlay value claim.
- **Track C (volatility/stress):** sealed/locked; forecast gate NOT_MET; all unsealed confirmatory panels exhausted (>=5 symbols, >=3 non-overlapping 30-day blocks). No further confirmatory cell feasible without NEW admissible data.
- **Track A (observed liquidation risk): BLOCKED/EXHAUSTED.** `data_through=2026-10`; Hyperliquid 2026-11..2027-02 absent (probes==2, probing exhausted). **NO re-probe of absent months.** Resume trigger only: unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200) OR an admissible unauthenticated observed-liquidation source passing the full-manifest GO rubric/gate; PREREGISTER before inspecting outcomes; modeled != observed.
- **Track B (modeled boundary breach): CLOSED_NEGATIVE.** Never conflate modeled vs observed.
- **v5 confirmatory package (2025+): `all_go=false`, `confirmatory_outcomes_permitted=false`.** Hard blocker: Binance Vision/data-use terms not human-verified (`EXPLICIT_BLOCKER_UNRESOLVED`, `fabricated=false`) — not agent-resolvable; agent cannot fabricate legal terms. `fclr016_v5_preflight_summary`, package/report/validator/guard/CLI refusal paths, and new `fclr016_v5_promotion_dryrun` are present and green in targeted suites.
- `research_state/final_confirmatory_verdict.md` (FCLR-FINAL-001): CLOSEOUT COMPLETE, H001 NOT_SUPPORTED, no path forward on existing admissible data. `research_state/negative_results_report.md` preserves null/failed/inconclusive outcomes. `research_state/final_record_closure_audit.md`: closed negative.
- `experiment_frontier.json`/FCLR-NEXT-131 COMPLETE; no competing campaign markers; recurring probe/scan families = 0; root trigger-harden files = 0. Canonicals `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` not mutated by this session's handoff/status/dryrun work.

### Bottlenecks removed (delivered — do not repeat)

1. Dual-P0 ambiguity resolved; `FCLR-NEXT-131` single P0 COMPLETE.
2. `scripts/fclr016_v5_promotion_dryrun.py` + `tests/test_fclr016_v5_promotion_dryrun.py` delivered with mandatory refusal/acceptance matrix and safety invariants (20/20 OK; v5 target suite 95 OK this session).
3. FCLR-NEXT-110..131 guard/harness/CLI/refusal hardening complete: tmp-isolated tests, no network/parquet/outcome reads, no real `research_state` writes, resume/gate/operator/drift pass.
4. Status-only churn eliminated; Track A absent-month re-probes prohibited.

### Commands (verify before/after changes)

```bash
pip install -r requirements.txt
python3 scripts/fclr016_v5_preflight_summary.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 scripts/fclr016_v5_promotion_dryrun.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 -m unittest tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q
python -m unittest discover tests  # required for full regression before commit/claim
python scripts/tracka_resume_check.py
python scripts/tracka_resume_gate.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_resume_check.py --bogus 2>&1 | head -c 200
python scripts/tracka_operator_report.py --bogus --json 2>&1 | head -c 200
```

### Resume trigger (only then — preregister BEFORE outcomes)

New admissible unauthenticated data (>=5 symbols, >=3 non-overlapping 30-day blocks) appears **and** a fresh experiment ID is pre-registered BEFORE examining outcomes. For Track A: unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200) or admissible observed-liquidation source passing full-manifest GO rubric. Then execute only the pre-registered cell, record hashes/timestamps in run manifest, report outcomes.

### If real human-verified terms review appears (only then)

Create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only (`terms_url_reviewed`, `access_date_utc`, `terms_version_or_snapshot_id` or justified `not_provided_by_source`, `relevant_clause_summary`, human/legal `reviewer_role`, `conclusion`, `conditions_or_restrictions`, `evidence_artifacts`/hashes, `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope). Reconcile `admissibility_refs_sha256`/paths. Promote prereg to frozen only after all guards green. Run validator/package/report/preflight/promotion-dryrun with `--expect-go` as applicable (must not load data on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.

### Do-NOT

Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete data; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A absent months; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files; run any confirmation without fresh pre-registration + new admissible data.

---

## Prior sessions (preserved summary)

Prior detailed session logs remain in git history / prior handoff revisions. Key preserved facts: v5 report/validator/guard/CLI refusal hardening and lazy-import fix in `run_funding_ablations.py` delivered and green. FCLR-NEXT-110..131 guard/harness hardening complete (tests 352+, regression green, resume 17 PASS, drift pass, root<=163, probes==2). `fclr016_v5_preflight_summary.py` delivered and v5 family green. Track A/B/C statuses, hashes, and blockers unchanged. Canonicals `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` not mutated by handoff maintenance.
