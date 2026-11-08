## Initial Task Message (2026-11-08T05:40Z, git HEAD `4e1d26028`, working tree clean) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** funding-conditioned volatility forecasting + liquidation risk (both tracks in scope). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff.**

### Inferred single initial task (next session)

**Confirm and lock the closeout state; run NO confirmatory outcomes.** The confirmatory program is CLOSED NEGATIVE on all current admissible data:
- H001 (funding-conditioned volatility vs RV-only): NOT_SUPPORTED on every claim-worthy panel (FCLR-003, FCLR-006, FCLR-008, FCLR-013, v3 30d/5sym). Primary contrast C2 vs B1 fails CI/block/materiality gates on each. Risk-overlay phase INELIGIBLE. No economic/overlay value claim.
- Track C (volatility/stress): sealed/locked; forecast gate NOT_MET; all unsealed confirmatory panels exhausted (>=5 symbols, >=3 non-overlapping 30-day blocks). No further confirmatory cell feasible without NEW admissible data.
- Track A (observed liquidation risk): BLOCKED/EXHAUSTED. `data_through=2026-10`; Hyperliquid 2026-11..2027-02 absent (probes==2, probing exhausted). NO re-probe of absent months. Resume trigger only: unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 (HTTP 200) OR an admissible unauthenticated observed-liquidation source passing the full-manifest GO rubric/gate; PREREGISTER before inspecting outcomes; modeled != observed.
- Track B (modeled boundary breach): CLOSED_NEGATIVE. Never conflate modeled vs observed.
- v5 confirmatory package (2025+): `all_go=false`, `confirmatory_outcomes_permitted=false`. Hard blocker: Binance Vision/data-use terms not human-verified (`EXPLICIT_BLOCKER_UNRESOLVED`) — not agent-resolvable; agent cannot fabricate legal terms.

**Inferred task:** Until new admissible unauthenticated data (>=5 symbols, >=3 non-overlapping 30-day blocks) appears with a fresh pre-registration frozen BEFORE outcomes are inspected, the only permitted work is heavy gatekeeping/hardening engineering (below) that keeps the system provably fail-closed and prereg-before-outcomes, plus regression maintenance. Do not run, tune, threshold-shop, or re-evaluate any sealed holdout. Do not relabel pilot/inconclusive as confirmatory.

### Verified current state (do not re-litigate without new evidence)

- HEAD `4e1d26028` (chore checkpoint), tree clean, branch == origin/main.
- `research_state/research_protocol.md` FROZEN 2026-11-06T20:36:32Z. Gates: G1 data, G2 protocol frozen, G3 RV-baseline sanity, G4 incremental only after G3. G3 met (rv_baseline_complete); G4 blocked on unmet data-sufficiency/uncertainty on current panels.
- `research_state/negative_results_report.md`: preserves all null/failed/inconclusive outcomes (FCLR-001/002/003/004/012-V/FCLR-013, GATE4, H002 partial, H003 untested, H004 blocked).
- `research_state/final_confirmatory_verdict.md` (FCLR-FINAL-001): CLOSEOUT COMPLETE, H001 NOT_SUPPORTED, no path forward on existing admissible data.
- `research_state/final_record_closure_audit.md`: program closed negative; all five deliverables recorded; no stale next-task pointers outside this handoff.
- `research_state/experiment_frontier.json`: FCLR-NEXT-110..131 complete; FCLR-NEXT-131 COMPLETE 20261106T133740Z; root md+json <=163; probes==2; resume 17 PASS; drift pass; operator pass; no trigger side effects.
- Regression: `python -m unittest discover tests` green (77 test files; dep-light subset green where numpy/pandas absent in this runner).
- Canonicals `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` not mutated this session.

### Bottlenecks removed (already delivered — do not repeat)

1. Dual-P0 ambiguity (`FCLR-NEXT-132`/`FCLR-NEXT-139` vs `FCLR-NEXT-131`): resolved; `FCLR-NEXT-131` is the single P0 and is COMPLETE. No competing campaign markers.
2. Prior next-task bottleneck (`scripts/fclr016_v5_preflight_summary.py` + tests): delivered, deterministic read-only preflight, 12/12 tests OK, refusal matrix, no canonical mutation.
3. FCLR-NEXT-110..131 guard/harness/CLI/refusal hardening complete: tmp-isolated tests, no network/parquet/outcome reads, no real research_state writes, regression green, resume/gate/operator/drift pass.
4. Status-only churn eliminated: no new timestamped probe/sweep/scan/wrapper/report families; recurring probe/scan families = 0; root trigger-harden files = 0.

### Current blocker (explicit, not agent-resolvable)

No in-repo human-verified Binance Vision/data-use terms evidence; no new admissible unauthenticated data beyond 2026-11-02. Confirmatory 2025+/2026 outcomes prohibited until all admissibility gates green with real human-verified terms evidence AND new data + fresh prereg exist. Agent stops cleanly here; writes evidence, does not fabricate.

### Next focus campaign — HEAVY, MANDATORY, no-status-only (default path while data absent)

**Single highest-value task:** implement deterministic read-only `scripts/fclr016_v5_promotion_dryrun.py` + `tests/test_fclr016_v5_promotion_dryrun.py` (no outcomes, no network, no kline/funding/outcome loaders, no canonical mutation). Heavy engineering: simulate the full promotion/refusal matrix against synthetic tmp fixtures AND the real blocked package, proving every shortcut is refused and the only GO path is the fully-satisfied frozen package.

1. **Inputs:** 4 package artifact paths + optional `--candidate-terms-evidence` + optional `--candidate-prereg`. Load/copy to tmp; never mutate inputs/canonicals.
2. **Dry-run matrix (must execute):** per scenario machine-readable result with gate states/hashes/errors: (a) real blocked package — refuse GO; (b) resolved terms missing each required human field — refuse; (c) `fabricated=true` or agent-only reviewer — refuse; (d) template/blocker status treated as resolved — refuse; (e) draft promoted/frozen/GO claims without guards — refuse; (f) provenance GO while terms unresolved — refuse; (g) `admissibility_refs_sha256`/path mismatch — refuse; (h) completeness verdict/pass inconsistency — refuse; (i) confirmatory `--expect-go` on blocked package — refuse with stable contract; (j) synthetic fully-satisfied GO fixture (all human fields present, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal reviewer, matching scope, completeness PASS+admissible, provenance GO+admissible, prereg frozen/non-draft/GO/admissible, refs reconciled) — GO may be reported **only on the synthetic tmp fixture**, labeled `synthetic_test_fixture=true` / `no_real_terms_evidence=true`; never writes/claims real evidence, never mutates canonicals, never loads data.
3. **Output:** JSON + markdown with per-scenario status, exact refusal reasons, required human fields, forbidden values, and explicit "confirmatory outcomes still prohibited until real human-verified resolved terms evidence exists in-repo and real package passes all guards."
4. **Tests (tmp-isolated, monkeypatch loaders boom):** every refusal case above; synthetic GO fixture accepted only in tmp with synthetic labels; real blocked package never GO; missing/malformed inputs refuse; canonicals byte-identical; no data/network loaders referenced/called. Keep root bounds (1 script + 1 test file).

**Companion default-path hardening (FCLR_CAMPAIGN_NEXT, measurable, no status files):** extend seam tests (empty/unreadable data path under valid prereg -> blocked with stable reason codes); bulletproof CLI argparse contract on all 3 CLIs (edge cases); cross-CLI parity + canonical output integrity; add/extend legitimate hardening tests keeping regression >=709 OK; verify invariants (17/17 drift, bounds, probes==2).

**Commands:**
```bash
pip install -r requirements.txt
python3 -m py_compile scripts/fclr016_v5_promotion_dryrun.py tests/test_fclr016_v5_promotion_dryrun.py
python3 scripts/fclr016_v5_promotion_dryrun.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 -m unittest tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q
python -m unittest discover tests
python scripts/tracka_resume_check.py
python scripts/tracka_resume_gate.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_resume_check.py --bogus 2>&1 | head -c 200
python scripts/tracka_operator_report.py --bogus --json 2>&1 | head -c 200
```

**Resume trigger (only then):** new admissible unauthenticated data (>=5 symbols, >=3 non-overlapping 30-day blocks) appears AND a fresh experiment ID is pre-registered BEFORE examining outcomes. Then execute the pre-registered cell, record run_manifest hashes/timestamps, and report outcomes (confirmatory only if all gates green).

### If real human-verified terms review appears (only then)

Create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only (`terms_url_reviewed`, `access_date_utc`, `terms_version_or_snapshot_id` or justified `not_provided_by_source`, `relevant_clause_summary`, human/legal `reviewer_role`, `conclusion`, `conditions_or_restrictions`, `evidence_artifacts`/hashes, `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope). Reconcile `admissibility_refs_sha256`/paths. Promote prereg to frozen only after all guards green. Run validator/package/report/preflight/promotion-dryrun with `--expect-go` as applicable (must not load data on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.

### Do-NOT

Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete data; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A absent months; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files; run any confirmation without fresh pre-registration + new admissible data.

---

## Prior sessions (preserved summary)

Prior detailed session logs remain in git history / prior handoff revisions. Key preserved facts: v5 report/validator/guard/CLI refusal hardening and lazy-import fix in `run_funding_ablations.py` delivered and green (86/86 v5-family tests). FCLR-NEXT-110..131 guard/harness hardening complete (tests 352+, regression green, resume 17 PASS, drift pass, root<=163, probes==2). Track A/B/C statuses, hashes, and blockers unchanged. Canonicals `experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` not mutated.
