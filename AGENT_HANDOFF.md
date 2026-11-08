## Initial Task Message (2026-11-08T02:42:00Z, git 4f54baf1 working tree + uncommitted hardening) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Gate 4 v5 admissibility package — Track C funding-conditioned volatility forecasting** — primary; FCLR-H001 `NOT_SUPPORTED`, forecast gate `NOT MET`. Identity consolidated (1855/1855 MATCH, hazards 0; `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`) + deterministic completeness/leakage **PASS** (`32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`) for frozen 2025-08-01..2025-10-31 (5 symbols × 5 kinds). **`confirmatory_claim_go=NO_GO`, `admissibility_complete=false`, `confirmatory_outcomes_permitted=false`.** Unresolved blocker: Binance Vision/data-use **license/terms evidence not human-verified** — automated environment cannot verify; fabrication forbidden. Option (a) human-terms-review path is **blocked in this environment**; option (b) fail-closed hardening path is **open and in progress**. (2) **Track A observed liquidation risk** — `DATA_BLOCKED`; **NO re-probe**. (3) **Track B modeled boundary breach** — `CLOSED_NEGATIVE`.

### Completed this session (substantive hardening, heavy, green; NO confirmatory outcomes)
- **State re-verified 2026-11-08 (base 4f54baf1):** Gate 4 v5 remains blocked on terms/prereg freeze; all frozen v5 evidence artifacts unchanged.
- **P0.4 hardening — v5 admissibility validator strengthened (fail-closed):** `scripts/fclr016_validate_v5_admissibility.py` (sha256 `ba73200cfc62d2db9adb7f24dc66ec2d5b8b4ebb2b0a364b8e36ab3bfad619d0`, read-only, no network/outcomes). Adds explicit gate breakdown (`terms_resolved_verified`, `provenance_manifest_go`, `completeness_leakage_pass`, `prereg_frozen_non_draft`, `prereg_claim_go`), stricter `RESOLVED_VERIFIED` terms checks (requires `fabricated=false`, non-empty `terms_url_reviewed`/`access_date_utc`/`reviewer_role`/`conclusion`; refuses apparent agent-only reviewer role), completeness verdict/ok consistency check, and enforcement of `admissibility_refs_sha256.terms_evidence` when present. Blocked package => `ok=true, all_go=false, confirmatory_outcomes_permitted=false`; `--expect-go` => exit 2 with parseable gates/blockers.
- **P0.5 hardening — run_funding_ablations admissibility package check (NEW):** `scripts/run_funding_ablations.py` adds `check_admissibility_package()` (fail-closed, read-only, no kline/funding/outcome data loaded) plus `--check-admissibility-package PROVENANCE COMPLETENESS TERMS PREREG`, `--dry-run-admissibility` alias, and `--expect-go` (exit 2 when not all_go). Emits canonical JSON summary (gates/blockers/errors/hashes) for guard acceptance evidence. Mirrors validator gate logic: common artifact checks, scope alignment, terms/resolved checks, completeness/leakage, prereg consistency, refs sha256 integrity.
- **Tests hardened:** `tests/test_fclr016_v5_admissibility_guard.py` adds `TestFclr016V5AdmissibilityPackage` (5 cases): current blocked package ok=true/all_go=false with exact 5 blockers and hash values; expect_go refused; missing file => error; draft prereg cannot claim frozen; terms hash ref mismatch refused. `tests/test_fclr016_v5_admissibility_validator.py` (sha256 `4fe2b31503966fadcaa063e5eea397a3fbc96d106d723081aabcc19d510798c`) adds refusal cases for resolved terms without human-review fields / agent-only role and for terms-evidence hash-ref mismatch. Existing refusal/acceptance behavior preserved.
- **Unchanged v5 evidence (referenced):** provenance/license manifest `6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346` (terms blocker), completeness/leakage `32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8` (PASS deterministic), identity consolidation `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`, terms evidence BLOCKED `8128c1d513bee2e16a57f3ee19d103d17ad0d68ca15378724c7d432e35d59923`, prereg DRAFT `8bf5e7f2ac593048c9782cbb8cfabd041dea97cc46c30288d0cb09ddc8957f7f`. `run_funding_ablations.check_confirmatory_provenance` refuses actual v5 manifest as expected (`confirmatory_provenance_go!=true NO_GO`).
- **Verified green:** `py_compile` OK (`scripts/fclr016_validate_v5_admissibility.py`, `scripts/run_funding_ablations.py`). `python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator -v` **23/23 OK** (adds 5 new package-check cases). Validator current package: `ok=true, all_go=false, confirmatory_outcomes_permitted=false, gates all false`; `--expect-go` refused (exit 2). run_funding_ablations package check on current artifacts: `all_go=false`, 5 blockers, exit 0 without `--expect-go`, exit 2 with `--expect-go`.

### Single highest-value next task (heavy, measurable, NO confirmatory outcomes)
**P0 — Option (b) fail-closed hardening (option (a) human terms review unavailable in this environment): continue shipping substantive hardening/test/guardrail with green gates until Gate 4 v5 admissibility package is complete or human-verified terms evidence appears. Do NOT fabricate terms/license evidence; do NOT re-probe Track A; do NOT run confirmatory outcomes on unprovenanced/incomplete 2025+.**

Next concrete steps (pick one or more per session):
1. **Extend refusal surface:** add refusal tests for `provenance GO + terms unresolved hash ref`, `RESOLVED_VERIFIED terms missing conclusion/access_date` edge cases, draft prereg promoted without completeness pass. Keep all dep-light, tmp-isolated, no network/outcome reads.
2. **CI-style command surface:** document/canonicalize the `run_funding_ablations --check-admissibility-package --expect-go` command as the admissibility gate check; verify it emits stable parseable JSON on blocked and (synthetic) resolved fixtures.
3. **If human terms evidence becomes available:** produce `fclr016_v5_terms_evidence_RESOLVED_*` with verifiable facts only (terms URL, access date UTC, version/snapshot, clause summary, human/legal reviewer_role, conclusion, conditions, artifacts/hashes, `fabricated=false`), then update provenance manifest/prereg consistently, run validator + package check `--expect-go`, freeze prereg before outcomes. Still `NO_GO` until full package passes.

### Focus campaign (mandatory, no opt-out)
Every session until Gate 4 v5 admissibility package is complete (`license_terms_resolved_verified`, `admissibility_complete=true`, prereg frozen before outcomes, validator+guard accept) while `confirmatory_claim_go` remains `NO_GO` until all pass must either (a) advance admissibility with verifiable evidence + green gates and **no confirmatory outcomes**, or (b) if blocked, ship ≥1 substantive hardening/test/guardrail/schema with green gates. Track A re-probe and confirmatory outcomes on unprovenanced/incomplete 2025+ are prohibited. No status-only sessions. A session without (a)/(b) plus updated `AGENT_HANDOFF.md` is incomplete.

### Current gate state (evidence-backed, 2026-11-08)
- **Track A** = `DATA_BLOCKED` (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent). **NO re-probe.**
- **Track B** = `CLOSED_NEGATIVE`.
- **Track C / FCLR-H001** = `NOT_SUPPORTED` (forecast gate NOT MET; FCLR-003 sealed 2024 -3.78%; FCLR-006 -69.90%; FCLR-007 -3.42%; FCLR-008 +4.30% CI crosses zero). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09).
- **Gate 4 v5 confirmatory** = `NOT_READY/NO_GO` (`admissibility_complete=false`, `confirmatory_outcomes_permitted=false`). Identity `GO_PARTIAL_BOUNDED` hazards 0 (1855/1855). Completeness/leakage `PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC`. Terms evidence `EXPLICIT_BLOCKER_UNRESOLVED`. Prereg `DRAFT`/not frozen. Provenance manifest terms blocker. Validator+guard refuse confirmatory GO.
- **Green gates:** `py_compile` OK (v5 validator, run_funding_ablations). `test_fclr014_anchor_integrity` + `test_fclr016_provenance_probe` + `test_fclr016_v5_admissibility_guard` + `test_fclr016_v5_admissibility_validator` = **23/23 OK**.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_validate_v5_admissibility.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator -v
# Validator package check (blocked, consistent, not GO):
python3 scripts/fclr016_validate_v5_admissibility.py \
  --provenance-manifest research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
  --completeness-audit research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
  --terms-evidence research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json \
  --prereg-draft research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 scripts/fclr016_validate_v5_admissibility.py --expect-go \
  --provenance-manifest research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
  --completeness-audit research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
  --terms-evidence research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json \
  --prereg-draft research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json; echo EXIT:$?
# run_funding_ablations admissibility package check (read-only, no outcomes loaded):
python3 scripts/run_funding_ablations.py --check-admissibility-package \
  research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
  research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
  research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json \
  research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 scripts/run_funding_ablations.py --check-admissibility-package \
  research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
  research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
  research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json \
  research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json \
  --expect-go; echo EXIT:$?
```

### Acceptance criteria
- `confirmatory_claim_go=NO_GO` until full v5 package passes: verifiable RESOLVED_VERIFIED terms evidence (no fabrication), provenance manifest GO consistent with all gates, completeness/leakage PASS, prereg frozen before outcomes, validator+run_funding_ablations package check accept.
- Terms evidence = verifiable facts only; unresolved => explicit blocker and `confirmatory_provenance_go=false`.
- Guard/validator/package-check refusals parseable, exit!=0 where required, no tracebacks; canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims; **no confirmatory outcomes on unprovenanced/incomplete 2025+**.
- Root md/json bound respected; no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A; reopen sealed FCLR-001/002/003/006/007/008/013 anchors; threshold-shop; merge tracks; claim economic value/overlay; treat identity/completeness-only as confirmatory GO; fabricate license/terms permissions/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; promote/freeze prereg while terms unresolved; edit `.github/workflows`; add status-only families.
