## Initial Task Message (2026-11-08T05:44:48Z, git HEAD `47d881001`, working tree clean at handoff write) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** funding-conditioned volatility forecasting + liquidation risk (both tracks in scope). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Inferred single initial task (next session)

**Implement the FCLR-016 v5 promotion dry-run harness (heavy, mandatory, measurable).** The confirmatory program is CLOSED NEGATIVE on all current admissible data; no confirmatory outcomes are permitted. The only productive path while data/terms blockers remain is fail-closed gatekeeping/hardening engineering that makes every bypass provably refused and records evidence in tests.

**Deliverables (required, no status-only files):**
1. `scripts/fclr016_v5_promotion_dryrun.py` — deterministic, read-only, no network, no kline/funding/outcome loaders, no canonical mutation. Inputs: 4 package artifact paths + optional `--candidate-terms-evidence` + optional `--candidate-prereg` (load/copy to tmp; never mutate inputs/canonicals). Output: JSON + markdown with per-scenario status, exact refusal reasons, required human fields, forbidden values/shortcuts, and explicit statement: *confirmatory outcomes still prohibited until real human-verified resolved terms evidence exists in-repo and the real package passes all guards*.
2. `tests/test_fclr016_v5_promotion_dryrun.py` — tmp-isolated; monkeypatch/boom any data/network/outcome loader paths to prove they are never used; keep canonicals byte-identical.

**Mandatory refusal/acceptance matrix (every scenario machine-readable):**
- (a) Real blocked package (`research_state/fclr016_local_audit/fclr016_v5_{provenance_license_manifest_20261108T014405Z,completeness_leakage_audit_20261108T014405Z,terms_evidence_BLOCKED_20261108T014835Z,confirmatory_prereg_DRAFT_20261108T014835Z}.json`) — GO refused.
- (b) Candidate terms missing any required human field (`terms_url_reviewed`, `access_date_utc`, `terms_version_or_snapshot_id` or justified `not_provided_by_source`, `relevant_clause_summary`, human/legal `reviewer_role`, `conclusion`, `conditions_or_restrictions`, `evidence_artifacts`/hashes, `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope) — refused.
- (c) `fabricated=true` or agent-only reviewer — refused.
- (d) `TEMPLATE_NOT_EVIDENCE` / `EXPLICIT_BLOCKER_UNRESOLVED` treated as resolved — refused.
- (e) Draft promoted/frozen/GO claims without guards — refused.
- (f) Provenance GO while terms unresolved — refused.
- (g) `admissibility_refs_sha256`/path mismatch or reconciliation failure — refused.
- (h) Completeness verdict/pass inconsistency (`verdict!=PASS`, `admissibility_complete!=true`, leak/gap blockers) — refused.
- (i) Confirmatory `--expect-go` contract on blocked package — refused with stable contract.
- (j) Synthetic fully-satisfied GO fixture — GO may be reported **only on a synthetic tmp fixture** labeled `synthetic_test_fixture=true` / `no_real_terms_evidence=true`; never writes/claims real evidence, never mutates canonicals, never loads data.

**Heavy companion hardening (same session if dryrun lands cleanly):** extend seam tests (empty/unreadable data path under valid prereg -> blocked with stable reason codes); bulletproof CLI argparse/edge-case contracts on the 3 CLIs; cross-CLI parity + canonical output integrity; add legitimate hardening tests (regression must remain >=709 OK). Verify invariants: `tracka_resume_check` 17/17, root bounds, probes==2, no competing campaign markers, no new poller/wrapper/scheduler/status-only families.

### Verified current state (do not re-litigate without new evidence)

- HEAD `47d881001` (chore checkpoint), branch aligned with origin/main at last inspection; `AGENT_HANDOFF.md` updated this session as single durable handoff.
- `research_state/research_protocol.md` FROZEN 2026-11-06T20:36:32Z. Gates: G1 data, G2 frozen, G3 met (`rv_baseline_complete`), G4 blocked on unmet data-sufficiency/uncertainty on current panels.
- **H001 (funding-conditioned volatility vs RV-only): NOT_SUPPORTED** on every claim-worthy panel (FCLR-003, FCLR-006, FCLR-008, FCLR-013, v3 30d/5sym). Primary contrast C2 vs B1 fails CI/block/materiality gates on each. Risk-overlay phase INELIGIBLE. No economic/overlay value claim.
- **Track C (volatility/stress):** sealed/locked; forecast gate NOT_MET; all unsealed confirmatory panels exhausted (>=5 symbols, >=3 non-overlapping 30-day blocks). No further confirmatory cell feasible without NEW admissible data.
- **Track A (observed liquidation risk): BLOCKED/EXHAUSTED.** `data_through=2026-10`; Hyperliquid 2026-11..2027-02 absent (probes==2, probing exhausted). **NO re-probe of absent months.** Resume trigger only: unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200) OR an admissible unauthenticated observed-liquidation source passing the full-manifest GO rubric/gate; PREREGISTER before inspecting outcomes; modeled != observed.
- **Track B (modeled boundary breach): CLOSED_NEGATIVE.** Never conflate modeled vs observed.
- **v5 confirmatory package (2025+): `all_go=false`, `confirmatory_outcomes_permitted=false`.** Hard blocker: Binance Vision/data-use terms not human-verified (`EXPLICIT_BLOCKER_UNRESOLVED`, `fabricated=false`) — not agent-resolvable; agent cannot fabricate legal terms. `fclr016_v5_preflight_summary` + package/report/validator/guard/CLI refusal paths exist and are green (75+ tests in v5 family subset verified 2026-11-08).
- `research_state/final_confirmatory_verdict.md` (FCLR-FINAL-001): CLOSEOUT COMPLETE, H001 NOT_SUPPORTED, no path forward on existing admissible data. `research_state/negative_results_report.md` preserves null/failed/inconclusive outcomes. `research_state/final_record_closure_audit.md`: closed negative.
- `experiment_frontier.json`/FCLR-NEXT-131 COMPLETE; no competing campaign markers; recurring probe/scan families = 0; root trigger-harden files = 0. Canonicals `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` not mutated by handoff/status work.
- `scripts/fclr016_v5_promotion_dryrun.py` and `tests/test_fclr016_v5_promotion_dryrun.py` do **not** yet exist — this is the current bottleneck/next heavy task.

### Bottlenecks removed (delivered — do not repeat)

1. Dual-P0 ambiguity resolved; `FCLR-NEXT-131` single P0 COMPLETE.
2. `scripts/fclr016_v5_preflight_summary.py` + `tests/test_fclr016_v5_preflight_summary.py` delivered (deterministic read-only, refusal matrix, 12/12 tests; v5 family 75 OK verified).
3. FCLR-NEXT-110..131 guard/harness/CLI/refusal hardening complete: tmp-isolated tests, no network/parquet/outcome reads, no real `research_state` writes, regression green, resume/gate/operator/drift pass.
4. Status-only churn eliminated; Track A absent-month re-probes prohibited.

### Commands (verify before/after changes)

```bash
pip install -r requirements.txt
python3 scripts/fclr016_v5_preflight_summary.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 -m unittest tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q
# after implementing promotion dryrun:
python3 -m py_compile scripts/fclr016_v5_promotion_dryrun.py tests/test_fclr016_v5_promotion_dryrun.py
python3 scripts/fclr016_v5_promotion_dryrun.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 -m unittest tests.test_fclr016_v5_promotion_dryrun -q
python -m unittest discover tests
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
