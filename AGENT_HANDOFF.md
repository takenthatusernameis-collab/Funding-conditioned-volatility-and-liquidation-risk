## Initial Task Message (2026-11-08T01:58:16Z, git e2ab9df2 working tree) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Gate 4 v5 admissibility package — Track C funding-conditioned volatility forecasting** — primary; FCLR-H001 `NOT_SUPPORTED`, forecast gate `NOT MET`. Identity consolidated (1855/1855 MATCH, hazards 0; `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`) + deterministic completeness/leakage **PASS** (`32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`) for frozen 2025-08-01..2025-10-31 (5 symbols × 5 kinds). **`confirmatory_claim_go=NO_GO`, `admissibility_complete=false`, `confirmatory_outcomes_permitted=false`.** Unresolved blocker: Binance Vision/data-use **license/terms evidence not human-verified** — automated environment cannot verify; fabrication forbidden. (2) **Track A observed liquidation risk** — `DATA_BLOCKED`; **NO re-probe**. (3) **Track B modeled boundary breach** — `CLOSED_NEGATIVE`.

### Completed this session (substantive hardening, heavy, green; NO confirmatory outcomes)
- **State re-verified 2026-11-08T01:58:16Z (base e2ab9df2):** Gate 4 v5 remains blocked on terms/prereg freeze; all frozen v5 evidence artifacts unchanged.
- **P0.4 hardening — v5 admissibility validator strengthened (fail-closed):** `scripts/fclr016_validate_v5_admissibility.py` (sha256 `ba73200cfc62d2db9adb7f24dc66ec2d5b8b4ebb2b0a364b8e36ab3bfad619d0`, read-only, no network/outcomes). Adds explicit gate breakdown (`terms_resolved_verified`, `provenance_manifest_go`, `completeness_leakage_pass`, `prereg_frozen_non_draft`, `prereg_claim_go`), stricter `RESOLVED_VERIFIED` terms checks (requires `fabricated=false`, non-empty `terms_url_reviewed`/`access_date_utc`/`reviewer_role`/`conclusion`; refuses apparent agent-only reviewer role), completeness verdict/ok consistency check, and enforcement of `admissibility_refs_sha256.terms_evidence` when present. Blocked package => `ok=true, all_go=false, confirmatory_outcomes_permitted=false`; `--expect-go` => exit 2 with parseable gates/blockers.
- **Tests hardened:** `tests/test_fclr016_v5_admissibility_validator.py` (sha256 `4fe2b31503966fadcaa063e65eea397a3fbc96d106d723081aabcc19d510798c`) adds refusal cases for resolved terms without human-review fields / agent-only role and for terms-evidence hash-ref mismatch. Existing refusal/acceptance behavior preserved.
- **Unchanged v5 evidence (referenced):** provenance/license manifest `6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346` (terms blocker), completeness/leakage `32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8` (PASS deterministic), identity consolidation `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`, terms evidence BLOCKED `8128c1d513bee2e16a57f3ee19d103d17ad0d68ca15378724c7d432e35d59923`, prereg DRAFT `8bf5e7f2ac593048c9782cbb8cfabd041dea97cc46c30288d0cb09ddc8957f7f`. `run_funding_ablations.check_confirmatory_provenance` refuses actual v5 manifest as expected (`confirmatory_provenance_go!=true NO_GO`).
- **Verified green:** `py_compile` OK (`scripts/fclr016_validate_v5_admissibility.py`, `scripts/run_funding_ablations.py`). `python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator -v` **16/16 OK** (adds 2 new validator cases). Validator current package: `ok=true, all_go=false, confirmatory_outcomes_permitted=false, gates all false`; `--expect-go` refused (exit 2).

### Single highest-value next task (heavy, measurable, NO confirmatory outcomes)
**P0 — Obtain/record verifiable human-reviewed license/terms evidence for Gate 4 v5 frozen scope (2025-08-01..2025-10-31, BTC/ETH/BNB/SOL/XRP × 5 kinds), then update v5 manifest/prereg/guards only with verifiable facts. If human review unavailable, ship further fail-closed hardening (validator↔manifest/prereg/guard linkage, CI-style command surface, synthetic refusal fixtures) with green gates; keep `confirmatory_claim_go=NO_GO`.**

1. **Human/legal terms evidence (unblocker):** Produce a new `fclr016_v5_terms_evidence_RESOLVED_*` (or versioned equivalent) with **verifiable facts only**: exact terms URL reviewed, access date UTC, terms version/snapshot id or `not_provided_by_source`+explanation, relevant clause summary (research use; public-repo retention/redistribution of derived checksums/manifests; attribution/restrictions), human maintainer/legal `reviewer_role`, conclusion, conditions/restrictions, evidence artifacts/hashes. `fabricated=false`. **Never fabricate.** Only with RESOLVED_VERIFIED facts may a new versioned provenance manifest/prereg advance fields consistently with *all* gates — still `NO_GO` until prereg frozen before outcomes and validator+guard accept.
2. **Prereg freeze (after 1 + all gates):** Replace TO_FREEZE placeholders with exact splits/features/targets/metrics/stop rule from coverage-only design; freeze before any outcome inspection; record hashes; run validator `--expect-go` and `run_funding_ablations` confirmatory guard acceptance path; keep `confirmatory_claim_go=NO_GO` until full package passes. **No confirmatory outcomes until permitted.**
3. **If human review blocked:** substantive hardening only (e.g., `--check-admissibility-package`/`--dry-run-admissibility` path in `run_funding_ablations` that emits canonical validator+guard summary without loading outcomes; extend validator to require terms-evidence hash inside prereg refs when resolved file supplied; add refusal tests for `provenance GO + terms unresolved hash ref`, `RESOLVED_VERIFIED missing conclusion/access_date` edge cases, draft promoted without completeness pass). No status-only work.

### Focus campaign (mandatory, no opt-out)
Every session until Gate 4 v5 admissibility package is complete (`license_terms_resolved_verified`, `admissibility_complete=true`, prereg frozen before outcomes, validator/guard accept) while `confirmatory_claim_go` remains `NO_GO` until all pass must either (a) advance admissibility with verifiable evidence + green gates and **no confirmatory outcomes**, or (b) if blocked, ship ≥1 substantive hardening/test/guardrail/schema with green gates. Track A re-probe and confirmatory outcomes on unprovenanced/incomplete 2025+ are prohibited. No status-only sessions. A session without (a)/(b) plus updated `AGENT_HANDOFF.md` is incomplete.

### Current gate state (evidence-backed, 2026-11-08T01:58:16Z)
- **Track A** = `DATA_BLOCKED` (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent). **NO re-probe.**
- **Track B** = `CLOSED_NEGATIVE`.
- **Track C / FCLR-H001** = `NOT_SUPPORTED` (forecast gate NOT MET; FCLR-003 sealed 2024 -3.78%; FCLR-006 -69.90%; FCLR-007 -3.42%; FCLR-008 +4.30% CI crosses zero). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09).
- **Gate 4 v5 confirmatory** = `NOT_READY/NO_GO` (`admissibility_complete=false`, `confirmatory_outcomes_permitted=false`). Identity `GO_PARTIAL_BOUNDED` hazards 0 (1855/1855). Completeness/leakage `PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC`. Terms evidence `EXPLICIT_BLOCKER_UNRESOLVED`. Prereg `DRAFT`/not frozen. Provenance manifest terms blocker. Validator+guard refuse confirmatory GO.
- **Green gates:** `py_compile` OK (v5 validator, run_funding_ablations). `test_fclr014_anchor_integrity` + `test_fclr016_provenance_probe` + `test_fclr016_v5_admissibility_guard` + `test_fclr016_v5_admissibility_validator` = **16/16 OK**.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_validate_v5_admissibility.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator -v
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
```

### Acceptance criteria
- `confirmatory_claim_go=NO_GO` until full v5 package passes: verifiable RESOLVED_VERIFIED terms evidence (no fabrication), provenance manifest GO consistent with all gates, completeness/leakage PASS, prereg frozen before outcomes, validator+FCLR-014/v5 guard accept.
- Terms evidence = verifiable facts only; unresolved => explicit blocker and `confirmatory_provenance_go=false`.
- Guard/validator refusals parseable, exit!=0 where required, no tracebacks; canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims; **no confirmatory outcomes on unprovenanced/incomplete 2025+**.
- Root md/json bound respected; no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A; reopen sealed FCLR-001/002/003/006/007/008/013 anchors; threshold-shop; merge tracks; claim economic value/overlay; treat identity/completeness-only as confirmatory GO; fabricate license/terms permissions/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; promote/freeze prereg while terms unresolved; edit `.github/workflows`; add status-only families.
