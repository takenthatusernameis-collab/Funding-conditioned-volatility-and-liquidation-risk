## Initial Task Message (2026-11-08T03:53:28Z, git HEAD; session verified) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility forecasting + liquidation risk). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff.**

### Verified current state (do not re-litigate without new evidence)
- **P0 Track C / Gate 4 v5 confirmatory:** `NOT_READY / confirmatory_claim_go=NO_GO / admissibility_complete=false / confirmatory_outcomes_permitted=false`. Identity consolidated (1855/1855 MATCH, hazards 0; `f7361042…`). Completeness/leakage deterministic PASS but package blocked (`32dfcddc…`, frozen 2025-08-01..2025-10-31, 5 symbols × 5 kinds). **Hard blocker (cannot be bypassed):** Binance Vision/data-use license/terms **not human-verified** — `EXPLICIT_BLOCKER_UNRESOLVED` (`8128c1d5…`). Provenance manifest blocked (`6888116a…`). Prereg DRAFT/not frozen (`8bf5e7f2…`). `fclr016_validate_v5_admissibility.py` + `run_funding_ablations --check-admissibility-package` + `fclr016_v5_admissibility_report.py` all refuse; `--expect-go` exits 2. Confirmatory 2025+ data/outcome loading prohibited.
- **Track C history:** FCLR-H001 `NOT_SUPPORTED`; forecast gate NOT MET (FCLR-003 -3.78%, FCLR-006 -69.90%, FCLR-007 -3.42%, FCLR-008 +4.30% CI crosses zero). Gate 4 v4 `EXPLORATORY_INCONCLUSIVE` (confounded). No threshold-shopping; no sealed anchor reopen.
- **Track A (observed liquidation risk):** `DATA_BLOCKED` (Hyperliquid ironflow `data_through=2026-10`; 2026-11..2027-02 absent). **NO re-probe.** Trigger-only guarded protocol if admissible unauthenticated Hyperliquid data appears + rubric passes; preregister before outcome inspection.
- **Track B (modeled boundary breach):** `CLOSED_NEGATIVE`. Never conflate modeled vs observed.
- **Regression (last recorded):** 709 OK, 0 failures, 0 errors. Drift 17/17 pass; network false; bounds 143/163 root md+json.

### Session (2026-11-08T03:53Z) — verification / no bottleneck-removal changes needed
v5 hardening artifacts present and green: `fclr016_v5_admissibility_report.py` + `fclr016_v5_terms_evidence_template.py` + validator/guard/CLI refuse-paths + tests. **Verified this session (read-only, no canonical mutation):**
```bash
python3 -m py_compile scripts/fclr016_v5_admissibility_report.py tests/test_fclr016_v5_admissibility_report.py  # OK
python3 -m unittest tests.test_fclr016_v5_admissibility_report -q  # 8/8 OK
python3 -m unittest discover -s tests -p 'test_fclr016*' -q  # 85/85 OK
python3 scripts/fclr016_v5_admissibility_report.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # all_go=false, confirmatory_outcomes_permitted=false, blockers=[terms_resolved_verified,provenance_manifest_go,completeness_leakage_pass,prereg_frozen_non_draft,prereg_claim_go]
python3 scripts/fclr016_validate_v5_admissibility.py --provenance-manifest research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json --completeness-audit research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json --terms-evidence research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json --prereg-draft research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # all_go=false, confirmatory_outcomes_permitted=false
git diff --name-only -- research_state/experiment_frontier.json research_state/run_manifest.json research_state/evaluation_summary.md  # (no output)
```

### Current blocker (explicit)
No in-repo **human-verified** Binance Vision/data-use terms evidence (`EXPLICIT_BLOCKER_UNRESOLVED`). Automated agent cannot fabricate/review legal terms. Confirmatory 2025+ outcomes remain prohibited until all admissibility gates green with real evidence.

### Next single highest-value task
**Default (no human terms evidence; heavy bounded fail-closed work):** implement deterministic read-only `scripts/fclr016_v5_preflight_summary.py` + `tests/test_fclr016_v5_preflight_summary.py` (no outcomes, no network, no canonical mutation). Accept the 4 package artifact paths + optional human terms-evidence path; run validator/package/report parity checks; emit one machine-readable + markdown "human action checklist" + refusal matrix: exact missing/blocked gates, required human terms fields with source/fill guidance, exact promotion sequence, and explicit refusal reasons for every attempted shortcut (template-as-evidence, draft->frozen, RESOLVED without human fields, confirmatory with `--expect-go`/missing refs). Tests must prove: never claims GO on blocked/template/malformed inputs, refuses missing/fabricated/resolved-without-human-fields, cannot mutate canonicals, no data/network loaders, `--expect-go` contract stable. Respect root bounds (single script + single test file).
```bash
python3 -m py_compile scripts/fclr016_v5_preflight_summary.py tests/test_fclr016_v5_preflight_summary.py
python3 scripts/fclr016_v5_preflight_summary.py research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
python3 -m unittest tests.test_fclr016_v5_preflight_summary tests.test_fclr016_v5_terms_evidence_template tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q
```
**If real human-verified terms review appears (only then):** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only (`terms_url_reviewed`, `access_date_utc`, `terms_version_or_snapshot_id` or justified `not_provided_by_source`, `relevant_clause_summary`, human/legal `reviewer_role`, `conclusion`, `conditions_or_restrictions`, `evidence_artifacts`/hashes, `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope). Reconcile `admissibility_refs_sha256`/paths. Promote prereg to frozen **only after** all guards green. Run package check + confirmatory guard/report (must refuse until frozen+all GO; must not load data on refusal). Do not compute outcomes until `all_go=true` and frozen prereg hashes recorded.

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files.

---

## Prior sessions (preserved)

## Prior session (preserved)
## Initial Task Message (2026-11-08T02:50:19Z, git 789e3b75; verified clean before edits) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility forecasting + liquidation risk). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources.

### Session (2026-11-08T02:50Z, P0 v5 fail-closed hardening — substantive, no confirmatory outcomes)
**Changes (why):** closed the 2026-11-08T02:49Z P0 campaign items without bypassing blockers.
- `scripts/run_funding_ablations.py` — added `--terms-evidence` and fail-closed `check_confirmatory_provenance(..., terms_evidence=...)` cross-check: validates RESOLVED_TERMS required human fields (`terms_url_reviewed`, `access_date_utc`, `reviewer_role`, `conclusion`), refuses `fabricated!=false`, refuses agent-only reviewer, refuses unresolved/fabricated terms even when paired with a manifest; wired CLI to pass `--terms-evidence` before any confirmatory data load.
- `tests/test_fclr016_v5_confirmatory_cli_refusal_e2e.py` (new, 17 tests, tmp-isolated, no network, no canonical mutation) — (a) end-to-end `run_funding_ablations.main()` confirmatory CLI on synthetic 2025+ invocations refuses **before** any `load_kline_series`/`load_funding_series`/`load_kline_panel`/`load_funding_panel`/`run_multisplit` (monkeypatched loaders boom if reached) for: unprovenanced 2025+; blocked provenance manifest; blocked terms evidence with otherwise-GO synthetic manifest; RESOLVED terms missing human fields. Subprocess confirms parseable JSON refusal `{"status":"REFUSED",...}` exit 2. Canonical `research_state/experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` byte-identical after refusals. (b) `check_confirmatory_provenance` terms-evidence cross-check rejects missing URL/access/reviewer/conclusion, agent-only reviewer, fabricated=true, unresolved terms; accepts synthetic RESOLVED+GO fixture; blocks real blocked terms. Read-only `--check-admissibility-package` path loads no data.

**Commands + exact results:**
```bash
python3 -m py_compile scripts/run_funding_ablations.py tests/test_fclr016_v5_confirmatory_cli_refusal_e2e.py  # OK
python3 -m unittest tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q  # 17/17 OK
python3 -m unittest tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator tests.test_fclr016_v5_confirmatory_cli_refusal_e2e -q  # 55/55 OK
git diff --name-only -- research_state/experiment_frontier.json research_state/run_manifest.json research_state/evaluation_summary.md  # (no output) canonical unchanged
```

### Gate status (verified; do not re-litigate without new evidence)
- **P0 Track C / Gate 4 v5 confirmatory:** `NOT_READY / confirmatory_claim_go=NO_GO / admissibility_complete=false / confirmatory_outcomes_permitted=false`. Identity consolidated (1855/1855 MATCH, hazards 0). Completeness/leakage deterministic PASS but package remains blocked (artifact `32dfcdd...`). **Hard blocker (cannot be bypassed):** Binance Vision/data-use license/terms **not human-verified** — `EXPLICIT_BLOCKER_UNRESOLVED` (`8128c1d...`). Provenance manifest blocked (`6888116...`). Prereg DRAFT/not frozen (`8bf5e7f...`). Validator + package check + provenance guard + `--terms-evidence` cross-check + confirmatory CLI refuse; no data/outcome loading on confirmatory 2025+.
- **Track C history:** FCLR-H001 `NOT_SUPPORTED`; forecast gate NOT MET (FCLR-003 -3.78%, FCLR-006 -69.90%, FCLR-007 -3.42%, FCLR-008 +4.30% CI crosses zero). Gate 4 v4 `EXPLORATORY_INCONCLUSIVE` (confounded). No threshold-shopping; no sealed anchor reopen.
- **Track A (observed liquidation risk):** `DATA_BLOCKED` (Hyperliquid ironflow `data_through=2026-10`; 2026-11..2027-02 absent). **NO re-probe.** Trigger-only guarded protocol if admissible unauthenticated Hyperliquid data appears + rubric passes; preregister before outcome inspection.
- **Track B (modeled boundary breach):** `CLOSED_NEGATIVE`. Never conflate modeled vs observed.

### Blocker (current)
No in-repo **human-verified** Binance Vision/data-use terms evidence. Automated agent cannot fabricate/review legal terms (`EXPLICIT_BLOCKER_UNRESOLVED`). Confirmatory 2025+ outcomes prohibited until all admissibility gates green with real evidence.

### Next single highest-value task
**If real human-verified terms review appears in-repo (only then):** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only (`terms_url_reviewed`, `access_date_utc`, `terms_version_or_snapshot_id` or justified `not_provided_by_source`, `relevant_clause_summary`, human/legal `reviewer_role`, `conclusion`, `conditions_or_restrictions`, `evidence_artifacts`/hashes, `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope). Reconcile `admissibility_refs_sha256`/paths across provenance+completeness+prereg. Promote prereg to frozen **only after** all guards green. Verify: `python3 scripts/fclr016_validate_v5_admissibility.py --provenance-manifest <pm> --completeness-audit <ca> --terms-evidence <te> --prereg-draft <pr> --expect-go && python3 scripts/run_funding_ablations.py --check-admissibility-package <pm> <ca> <te> <pr> --expect-go && python3 scripts/run_funding_ablations.py --confirmatory --provenance-manifest <pm> --terms-evidence <te> --start 2025-08-01 --end 2025-10-31 --pre-registration <pr_frozen> --out-suffix _v5_confirmatory --experiment-id G4V5_CONFIRMATORY --help`-independent dry/guard checks (must refuse until frozen+all GO; must not load data on refusal). Do not compute outcomes until `all_go=true` and frozen prereg hashes recorded.
**If no human terms evidence appears (default, heavy bounded work):** add a small deterministic `scripts/fclr016_v5_admissibility_report.py` (read-only, no outcomes/network) that loads the 4 real package artifacts + optional terms-evidence path, runs `check_admissibility_package`/validator logic parity, and emits a machine-readable + markdown blocker summary with hashes, gate states, exact required human fields, and "next materially different route" (human terms review) — plus tests proving it cannot claim GO, cannot mutate canonicals, and refuses on malformed/fabricated inputs. Keep root bounds respected.

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files. **This file is the single durable handoff.**

---
## Prior session (preserved)
## Initial Task Message (2026-11-08T02:37:50Z, git f17c20ca/HEAD-at-start; verified HEAD 789e3b75 clean-before-session; 2026-11-08T02:41:06Z session) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility forecasting + liquidation risk). **Mission constraint:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources.

### Verified current state (do not re-litigate without new evidence)
- **P0 Track C / Gate 4 v5 confirmatory (funding-conditioned volatility):** `NOT_READY / confirmatory_claim_go=NO_GO`, `admissibility_complete=false`, `confirmatory_outcomes_permitted=false`. Identity consolidated (1855/1855 MATCH, hazards 0; `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`). Completeness/leakage deterministic **PASS** but `admissibility_complete` remains false in frozen artifact (`32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`, frozen 2025-08-01..2025-10-31, 5 symbols × 5 kinds). **Hard blocker (cannot be bypassed):** Binance Vision/data-use license/terms **not human-verified** — `EXPLICIT_BLOCKER_UNRESOLVED` (`8128c1d513bee2e16a57f3ee19d103d17ad0d68ca15378724c7d432e35d59923`). Provenance manifest blocked (`6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346`). Prereg **DRAFT/not frozen** (`8bf5e7f2ac593048c9782cbb8cfabd041dea97cc46c30288d0cb09ddc8957f7f`). Validator + `run_funding_ablations` package check both refuse confirmatory GO with blockers `[terms_resolved_verified, provenance_manifest_go, completeness_leakage_pass, prereg_frozen_non_draft, prereg_claim_go]`; `--expect-go` exits 2.
- **Historical signal context:** FCLR-H001 `NOT_SUPPORTED`; forecast gate NOT MET; Track C confirmatory closed on 2024 sealed evidence (e.g., FCLR-003 -3.78%, FCLR-006 -69.90%, FCLR-007 -3.42%, FCLR-008 +4.30% CI crosses zero). Gate 4 v4 `EXPLORATORY_INCONCLUSIVE` (confounded). No threshold-shopping; no sealed anchor reopen.
- **Track A (observed liquidation risk):** `DATA_BLOCKED` (Hyperliquid ironflow `data_through=2026-10`; 2026-11..2027-02 absent). **NO re-probe.** Follow trigger-only guarded protocol only if admissible unauthenticated Hyperliquid data appears AND rubric passes; preregister before outcome inspection.
- **Track B (modeled boundary breach):** `CLOSED_NEGATIVE`. Never conflate modeled vs observed.

### Session log (2026-11-08T02:41Z, P0 v5 fail-closed hardening; substantive)
**Changes (why):** closed mandatory P0 campaign items 1–3 by adding adversarial refusal/acceptance tests and aligning guard/validator/package-check behavior on synthetic `GO` fixtures (fail-closed, no network, no outcome/kline/funding loading, no canonical mutation).
- `scripts/fclr016_validate_v5_admissibility.py` — added refusal for non-draft prereg claiming `GO`/`admissibility_complete` without `RESOLVED_VERIFIED` terms and without provenance manifest `GO`+`admissibility_complete` (prevents promotion bypass).
- `scripts/run_funding_ablations.py` — added `_check_resolved_terms_evidence_package()` (aligned with validator), enforced same resolved-terms required fields/human reviewer/`fabricated=false`, completeness verdict/pass consistency, non-draft GO/admissible prereg refusal, `errors` included in `all_go`, and `--expect-go` package refusal now returns parseable `ok=true` (validated) + `expect_go_refused=true` + gates/blockers/errors/hashes (CLI still exits 2).
- `tests/test_fclr016_v5_admissibility_hardening.py` (new, 21 tests, tmp-isolated) — resolved terms missing URL/access/reviewer/conclusion refuse; agent-only reviewer refuses; `fabricated=true` refuses; terms hash-ref mismatch refuses; completeness verdict PASS with `ok=false` refuses; draft cannot claim frozen/admissible; non-draft GO/admissible without terms/provenance refuses; validator/package CLI contract stable (`--expect-go` exit 2, parseable blocked output, package blocked-check exit 0); `run_funding --dry-run-admissibility` alias; synthetic GO fixture alignment (`check_confirmatory_provenance` vs `check_admissibility_package`) proves no false-accept, no canonical mutation (`experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` byte-identical), no outcome loading.

**Commands + exact results:**
```bash
python3 -m py_compile scripts/fclr016_validate_v5_admissibility.py scripts/run_funding_ablations.py  # OK
python3 -m unittest tests.test_fclr016_v5_admissibility_hardening tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator -q  # 38/38 OK
python3 -m unittest discover -s tests -p 'test_fclr016*' -q  # 41/41 OK
python3 scripts/fclr016_validate_v5_admissibility.py --provenance-manifest research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json --completeness-audit research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json --terms-evidence research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json --prereg-draft research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # all_go=false, confirmatory_outcomes_permitted=false
python3 scripts/run_funding_ablations.py --check-admissibility-package research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json --expect-go; echo $?  # parseable NO_GO, exit 2
```

**Gate status:** P0 v5 package remains **NOT_READY / confirmatory_claim_go=NO_GO / admissibility_complete=false / confirmatory_outcomes_permitted=false** (real blocked artifacts still refuse). Track A **DATA_BLOCKED** (no trigger; no probe). Track B **CLOSED_NEGATIVE**. Forecast gate **NOT MET**.

**Blocker:** No in-repo **human-verified** Binance Vision/data-use terms evidence (`EXPLICIT_BLOCKER_UNRESOLVED`, `8128c1d513bee2e16a57f3ee19d103d17ad0d68ca15378724c7d432e35d59923`). Cannot fabricate; cannot freeze/promote prereg; cannot run confirmatory 2025+ outcomes.

**Next single highest-value task:** If a real human-verified terms review appears in-repo, create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only (`terms_url_reviewed`, `access_date_utc`, `terms_version_or_snapshot_id` or justified `not_provided_by_source`, `relevant_clause_summary`, human/legal `reviewer_role`, `conclusion`, `conditions_or_restrictions`, `evidence_artifacts`/hashes, `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope), reconcile `admissibility_refs_sha256`/paths across provenance+completeness+prereg, promote prereg to frozen **only after** all guards green, then run: `python3 scripts/fclr016_validate_v5_admissibility.py ... --expect-go && python3 scripts/run_funding_ablations.py --check-admissibility-package ... --expect-go` (must exit 0 with `all_go=true`). **If no human terms evidence appears (default):** add next bounded fail-closed hardening — (a) end-to-end `run_funding_ablations` confirmatory CLI refusal test proving the package/manifest guard blocks before any `load_kline_series`/`load_funding_series`/outcome computation on a synthetic 2025+ confirmatory invocation (tmp-isolated, monkeypatched loaders), and (b) make `check_confirmatory_provenance` reject RESOLVED terms evidence missing the same required human fields when passed as package context or add a `--terms-evidence` cross-check path (no false-accept).

**Do-NOT:** fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files. This file remains the **single durable handoff**.

---
## Initial Task Message (2026-11-08T03:52:00Z, git e9d22bdc/HEAD; 2026-11-08T03:52:17Z session) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility forecasting + liquidation risk). Mission: empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources.

### Verified current state (do not re-litigate without new evidence)
- **P0 Track C / Gate 4 v5 confirmatory:** `NOT_READY / confirmatory_claim_go=NO_GO`, `admissibility_complete=false`, `confirmatory_outcomes_permitted=false`. Identity consolidated (1855/1855 MATCH, hazards 0; `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`). Completeness/leakage deterministic PASS; package blocked (`32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`). Hard blocker: Binance Vision/data-use terms **not human-verified** (`EXPLICIT_BLOCKER_UNRESOLVED`, `8128c1d513bee2e16a57f3ee19d103d17ad0d68ca15378724c7d432e35d59923`). Provenance manifest blocked (`6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346`). Prereg DRAFT/not frozen (`8bf5e7f2ac593048c9782cbb8cfabd041dea97cc46c30288d0cb09ddc8957f7f`). Validator + package check refuse; `--expect-go` exits 2.
- **Track A (observed liquidation risk):** `DATA_BLOCKED` (Hyperliquid ironflow `data_through=2026-10`; 2026-11..2027-02 absent). NO re-probe. Trigger-only guarded protocol.
- **Track B (modeled boundary breach):** `CLOSED_NEGATIVE`. Never conflate.
- **Historical signal:** FCLR-H001 `NOT_SUPPORTED`; forecast gate NOT MET (FCLR-003 -3.78%, FCLR-006 -69.90%, FCLR-007 -3.42%, FCLR-008 +4.30% CI crosses zero). Gate 4 v4 `EXPLORATORY_INCONCLUSIVE`. No threshold-shopping; no sealed anchor reopen.
- **Regression:** 709 OK, 0 failures, 0 errors (Track A guard). Drift 17/17 pass; network false; bounds 143/163 root md+json.

### Bottlenecks removed this session
- None new: confirmatory 2025+ outcomes remain prohibited by hard human-terms blocker. No session blocked on agent-side work; heavy bounded hardening continues.

### Next single highest-value task (heavy, default path — no human terms evidence)
Add read-only `scripts/fclr016_v5_admissibility_report.py` + tests:
1. Load the 4 real package artifacts (provenance manifest, completeness/leakage audit, terms evidence, prereg draft) + optional `--terms-evidence` path.
2. Run `check_admissibility_package`/validator logic parity (no outcomes, no network, no data loading).
3. Emit machine-readable + markdown blocker summary: artifact hashes, gate states, exact required human fields, and "next materially different route" (human terms review).
4. Tests prove it cannot claim GO, cannot mutate canonicals (`experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` byte-identical), refuses malformed/fabricated inputs.
Respect root bounds (no new timestamped probe/sweep/scan/wrapper/report families beyond this single script).

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files. This file remains the single durable handoff.

---
## Initial Task Message (2026-11-08T03:52:39Z, git HEAD clean) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility forecasting + liquidation risk). Mission: empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources.

### Verified current state (do not re-litigate without new evidence)
- **P0 Track C / Gate 4 v5 confirmatory:** `NOT_READY / confirmatory_claim_go=NO_GO`, `admissibility_complete=false`, `confirmatory_outcomes_permitted=false`. Identity consolidated (1855/1855 MATCH, hazards 0; `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`). Completeness/leakage deterministic PASS; package blocked (`32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`). Hard blocker: Binance Vision/data-use terms **not human-verified** (`EXPLICIT_BLOCKER_UNRESOLVED`, `8128c1d513bee2e16a57f3ee19d103d17ad0d68ca15378724c7d432e35d59923`). Provenance manifest blocked (`6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346`). Prereg DRAFT/not frozen (`8bf5e7f2ac593048c9782cbb8cfabd041dea97cc46c30288d0cb09ddc8957f7f`). Validator + package check refuse; `--expect-go` exits 2.
- **Track A (observed liquidation risk):** `DATA_BLOCKED` (Hyperliquid ironflow `data_through=2026-10`; 2026-11..2027-02 absent). NO re-probe. Trigger-only guarded protocol.
- **Track B (modeled boundary breach):** `CLOSED_NEGATIVE`. Never conflate.
- **Historical signal:** FCLR-H001 `NOT_SUPPORTED`; forecast gate NOT MET (FCLR-003 -3.78%, FCLR-006 -69.90%, FCLR-007 -3.42%, FCLR-008 +4.30% CI crosses zero). Gate 4 v4 `EXPLORATORY_INCONCLUSIVE`. No threshold-shopping; no sealed anchor reopen.
- **Regression:** 709 OK, 0 failures, 0 errors (Track A guard). Drift 17/17 pass; network false; bounds 143/163 root md+json.

### Bottlenecks removed this session
- None new; confirmatory 2025+ outcomes remain prohibited by hard human-terms blocker. Heavy bounded hardening continues.

### Next single highest-value task (heavy, default path — no human terms evidence)
Implement read-only `scripts/fclr016_v5_admissibility_report.py` + tests:
1. Load the 4 real package artifacts (provenance manifest, completeness/leakage audit, terms evidence, prereg draft) with optional `--terms-evidence` path.
2. Run `check_admissibility_package`/validator logic parity (no outcomes, no network, no data loading).
3. Emit machine-readable + markdown blocker summary: artifact hashes, gate states, exact required human fields, and "next materially different route" (human terms review).
4. Tests prove it cannot claim GO, cannot mutate canonicals (`experiment_frontier.json`, `run_manifest.json`, `evaluation_summary.md` byte-identical), refuses malformed/fabricated inputs.
Respect root bounds (no new timestamped probe/sweep/scan/wrapper/report families beyond this single script).

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files. This file remains the single durable handoff.
