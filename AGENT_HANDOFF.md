# AGENT_HANDOFF — Funding-Conditioned Volatility & Liquidation Risk
**Timestamp (UTC):** 2026-11-11T10:10:28Z
**Repository:** `Funding-conditioned-volatility-and-liquidation-risk`
**Single Durable Handoff — Read First, Execute Only This**

---

## 🎯 REPOSITORY PRIORITY (from name: Funding-conditioned Volatility & Liquidation Risk)

The repository name encodes the **primary research mission**: test whether **funding extremes + realized volatility + price-dislocation features** improve **out-of-sample forecasts** of (1) future realized volatility and (2) liquidation-risk outcomes — vs. a realized-volatility-only baseline.

**Highest-value confirmatory path:** Track C (Binance 2025-08..2025-10, 5 symbols × 5 data kinds) — **complete pipeline, tests, validators, frozen prereg exist; ONLY blocker is human terms review.**

---

## 🔴 CRITICAL BOTTLENECK (Structural — Cannot Be Resolved by Code)

**FCLR-016 v5 Terms Evidence: `EXPLICIT_BLOCKER_UNRESOLVED`**
File: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`

```json
{
  "structural_blocker": {
    "reason": "Automated agent environment cannot perform verifiable human/legal review of external Binance Vision/Binance market-data terms. Recording permissions without verifiable review evidence would be fabrication (forbidden).",
    "blocked_by": "requires human-maintainer/legal review with verifiable evidence capture",
    "environment_can_verify_externally": false
  }
}
```

**Required to unblock:** A **human maintainer/legal reviewer** must:
1. Review the exact Binance Vision / Binance market-data terms URL
2. Populate all 8 required verifiable evidence fields in a **new file** `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`:
   - `terms_url_reviewed` — exact URL reviewed
   - `access_date_utc` — UTC date/time of review
   - `terms_version_or_snapshot_id` — version/snapshot ID or `not_provided_by_source`
   - `relevant_clause_summary` — factual summary of research-use/retention/attribution clauses
   - `reviewer_role` — human/legal/maintainer (NOT agent-only)
   - `conclusion` — PERMITTED / PERMITTED_WITH_CONDITIONS / RESTRICTED / PROHIBITED / UNCLEAR
   - `conditions_or_restrictions` — explicit list or justified empty
   - `evidence_artifacts` — optional archived snapshot paths/hashes/URLs
3. Set `fabricated=false`, `status=RESOLVED_VERIFIED`
4. Save in `research_state/fclr016_local_audit/`

**Until done:** All confirmatory outcomes on 2025+ data are **prohibited** by fail-closed guards (`check_confirmatory_provenance`, `check_admissibility_package`, preflight summary). No code changes, test passes, or data processing can bypass this.

---

## 🟡 SECONDARY BLOCKERS (Depend on Primary)

| Blocker | File | Status | Unlock Condition |
|---------|------|--------|------------------|
| Pre-registration draft | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` | `draft: true` | Terms resolved → promote to frozen/non-draft |
| Provenance manifest v5 | `fclr016_v5_provenance_license_manifest_20261108T014405Z.json` | `confirmatory_provenance_go: false` | Terms resolved + identity GO |
| Completeness/leakage audit | `fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` | `verdict: PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC` | Already green; needs terms resolved for package GO |

---

## ✅ WHAT IS WORKING (No Action Needed)

- **Data ingestion:** `src/ingest/loader.py` — extracts zips, loads CSVs, normalizes to UTC hourly frames
- **Feature engineering:** `src/features/funding.py`, `src/volatility/feature_engineering.py` — funding trailing stats, volatility features, train-only scalers
- **Track A admissibility seam:** `src/analysis/tracka_admissible.py` — Ironflow/Hyperliquid manifest validation (stdlib-only, fail-closed)
- **Track C pipeline:** `scripts/run_funding_ablations.py` — walk-forward splits, purge/embargo, block bootstrap, HAR regression
- **Test suite:** 90+ tests covering admissibility, provenance, leakage, funding ablations, feature splits, timestamp parsing
- **FCLR-016 v5 preflight summary:** `scripts/fclr016_v5_preflight_summary.py` — read-only parity check, emits JSON + markdown checklist + refusal matrix
- **Validator:** `scripts/fclr016_validate_v5_admissibility.py` — fail-closed admissibility gate

---

## 🛑 TRACK A (Hyperliquid) — Separate Campaign, Lower Priority for *This* Repo Mission

- **Status:** `research_state/tracka_hl_alignment_blocker.md` — full 2025-06..2026-10 aligned panel **NOT buildable** from admissible unauthenticated Hyperliquid-native sources (mark price missing 2025-06..2026-04, funding missing 2025-06..2025-10, no index/premium endpoint)
- **Prereg frozen:** `research_state/tracka_prereg_hyperliquid_2026.json` (TRACKA-HL-20261111T073000Z)
- **Paths:** (a) find additional admissible Hyperliquid source back to 2025-06, (b) scope-down + re-prereg, (c) terminal closure NOT_SUPPORTED
- **Verdict:** This is a **data availability blocker**, not a process blocker. It does not unblock the primary repo mission (funding-conditioned volatility forecasting on Binance 2025+). Track separately; do not conflate.

---

## 🎯 NEXT FOCUS CAMPAIGN (Inescapable Heavy Work for Future Agents)

### Campaign: **Human Review Execution & Gate 4 Promotion (Track C / FCLR-016 v5)**

**Objective:** Obtain verifiable human/legal review of Binance Vision terms → promote Gate 4 package to frozen/GO → enable confirmatory Track C runs on 2025-08..2025-10 scope.

#### Phase 1: Human Review (External Dependency — Must Happen First)
- [ ] Identify human maintainer/legal reviewer with authority to review Binance data terms
- [ ] Provide them the exact required fields list (from `fclr016_v5_terms_evidence_BLOCKED_...json`)
- [ ] Capture review evidence (archived snapshot, screenshots, or hash-verified URL)
- [ ] Produce `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all fields populated

#### Phase 2: Package Reconciliation (Code Work — Deterministic)
- [ ] Run `scripts/fclr016_v5_preflight_summary.py` with resolved terms evidence
- [ ] Verify all 4 package artifacts have consistent `frozen_scope` (2025-08-01..2025-10-31, 5 symbols, 5 kinds)
- [ ] Reconcile `admissibility_refs_sha256` across provenance manifest, completeness audit, terms evidence, prereg draft
- [ ] Promote pre-registration to frozen/non-draft (`draft: false`, `confirmatory_claim_go: "GO"`, `admissibility_complete: true`, `frozen_before_outcomes: true`, `license_terms_resolved: true`)

#### Phase 3: Validator Acceptance (Code Work — Deterministic)
- [ ] Run `scripts/fclr016_validate_v5_admissibility.py --expect-go` → must exit 0 with `all_go=true`
- [ ] Run `scripts/run_funding_ablations.py --check-admissibility-package --expect-go` → must exit 0 with `confirmatory_outcomes_permitted=true`
- [ ] Both validators must return matching hashes and green gates

#### Phase 4: Confirmatory Execution (Heavy Compute — Only After Phase 3)
- [ ] Execute confirmatory Track C multi-split ablation on 2025-08..2025-10 scope
- [ ] Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- [ ] Kinds: fundingRate, klines, markPriceKlines, indexPriceKlines, premiumIndexKlines
- [ ] Walk-forward splits with ≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs
- [ ] Produce frozen evaluation artifacts + `evaluation_summary.md`

---

## 🛑 EXPLICIT FORBIDDEN ACTIONS (Will Be Refused by Guards)

| Action | Guard | Refusal Reason |
|--------|-------|----------------|
| Run confirmatory on 2025+ without resolved terms | `check_confirmatory_provenance` | "terms evidence not RESOLVED_VERIFIED" |
| Set `status=RESOLVED_VERIFIED` without human fields | `_check_resolved_terms_evidence_package` | "missing required field: terms_url_reviewed / access_date_utc / reviewer_role / conclusion" |
| Set `fabricated=true` on resolved evidence | Preflight / validator | "fabricated!=false on resolved evidence forbidden" |
| Use agent-only reviewer_role | Preflight / validator | "human/legal review required" |
| Promote prereg to frozen while any gate blocked | Preflight promotion sequence | "all guards must be green before promotion" |
| Load kline/funding/outcome data on refusal | `_confirmatory_data_path_seam_error` | "confirmatory outcomes prohibited until frozen+all GO" |

---

## 📂 KEY FILES FOR NEXT SESSION

```
research_state/fclr016_local_audit/
├── fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json    # CURRENT BLOCKER
├── fclr016_v5_provenance_license_manifest_20261108T014405Z.json
├── fclr016_v5_completeness_leakage_audit_20261108T014405Z.json
├── fclr016_v5_identity_consolidation_20261108T003908Z.json
├── fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
└── fclr016_v5_terms_evidence_RESOLVED_<UTC>.json              # MUST BE CREATED BY HUMAN

scripts/
├── fclr016_v5_preflight_summary.py          # Read-only parity check + markdown
├── fclr016_validate_v5_admissibility.py     # Validator (fail-closed)
├── run_funding_ablations.py                 # Main pipeline + --check-admissibility-package

src/
├── ingest/loader.py                         # Data ingestion
├── features/funding.py                      # Funding features (lagged, no lookahead)
├── volatility/feature_engineering.py        # Volatility features + train-only scaler
└── analysis/tracka_admissible.py            # Track A Ironflow seam
```

---

## 🔑 COMMANDS TO RUN (After Human Review Complete)

```bash
# 1. Preflight check with resolved terms evidence
python scripts/fclr016_v5_preflight_summary.py \
  research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
  research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
  research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json \
  research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json

# 2. Validator with --expect-go
python scripts/fclr016_validate_v5_admissibility.py \
  --provenance-manifest research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
  --completeness-audit research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
  --terms-evidence research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json \
  --prereg-draft research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json \
  --expect-go

# 3. Pipeline admissibility check with --expect-go
python scripts/run_funding_ablations.py \
  --check-admissibility-package \
  --provenance-manifest research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
  --completeness-audit research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
  --terms-evidence research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json \
  --prereg-draft research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json \
  --expect-go
```

---

## 📋 SUMMARY FOR NEXT AGENT

**This project is architecturally sound but blocked on a human-process dependency.** The codebase, tests, and validation infrastructure are complete and correct for the primary research mission (funding-conditioned volatility forecasting on Binance 2025+). The only path forward is:

1. **Human/legal review of Binance Vision terms** (external, cannot be automated)
2. **Deterministic package reconciliation** (code work, straightforward once terms resolved)
3. **Validator acceptance** (automated, will pass if reconciliation correct)
4. **Confirmatory compute** (heavy, only after validator GO)

**Do not waste cycles** trying to bypass the terms blocker — the fail-closed design is the correct scientific practice for confirmatory research on proprietary data. The next session should focus entirely on facilitating the human review and then executing the deterministic promotion sequence.

**Track A (Hyperliquid) is a separate, lower-priority campaign** with a data availability blocker, not a process blocker. Do not conflate the two tracks. The repository name and mission prioritize Track C (funding-conditioned volatility on Binance).

---

**End of Handoff — Next Agent Must Read This Entire File Before Any Action**