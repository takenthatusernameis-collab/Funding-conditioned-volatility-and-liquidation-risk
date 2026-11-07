# AGENT_HANDOFF.md — SINGLE DURABLE HANDOFF

**INITIAL TASK MESSAGE (2026-11-07T18:47Z, git `1ddb7d6c57e2cf10ace9fb11b9ddda26a6bcb428`):** Repo `Funding-conditioned-volatility-and-liquidation-risk` → prioritize **funding-conditioned volatility & liquidation risk**. **Track C is the only open claim-path (heavy work required; NO SKIPPING).** FCLR-015 identity is complete for 2024-04..09 cache vs Binance Vision (3690/3690 MATCH). **Gate 4 v4 prereg is now FROZEN before outcomes**: `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md|json` (`frozen_before_outcomes=true`, `outcome_metrics_present=false`, manifest sha256 `3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c`). **Boundary constraint (do not skip):** the 2024-04..09 slice overlaps the domain family of sealed 2024 panels (FCLR-002/v3 lineage); therefore any v4 run on this slice is **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE** unless a distinct admissible non-confounded boundary is preregistered before outcomes. Next heavy campaign: (1) record explicit v4 boundary/admissibility GO/NO-GO evidence vs sealed anchors; (2) run bounded deterministic exploratory smoke only after freeze in tmp/non-canonical output paths with leakage checks and required label; (3) pursue a materially distinct admissible boundary if confirmatory is ever attempted (separate prereg). **Track A/B remain closed/blocked — DO NOT re-probe. Never overwrite sealed confirmatory anchors.**

## What changed this session (2026-11-07T18:45Z–18:47Z) and why
- Verified repo state, recent commits, and `AGENT_HANDOFF.md` authority.
- Ran `python3 scripts/tracka_resume_check.py` → **pass:true, network:false, writes_real_research_state:false** (keeps Track A churn removed).
- Confirmed FCLR-015 2024-04..09 identity/manifest artifacts exist (`fclr015_input_manifest_2024_04_09_20261107T180626Z.json`, sha256 `3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c`, 3690 files).
- **Removed P0 bottleneck:** created Gate 4 v4 prereg frozen before outcomes (`research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md|json`) with git SHA, manifest path+sha256, 2024-04..09 5-symbol slice, chronological splits/purge/embargo, ablations A–E, primary QLIKE + secondary MAE/RMSE, block-bootstrap uncertainty plan, leakage controls, and explicit sealed-anchor conflict rationale. No outcome metrics included.
- Updated this single durable handoff with an unambiguous heavy next campaign and guardrails.

## What was actually tested (exact outcomes)
- `python3 scripts/tracka_resume_check.py` → JSON shows `"pass": true`, `"network": false`, `"writes_real_research_state": false`, `"elapsed_s": 0.632445` (2026-11-07 run in this session).
- Prereg JSON field verification (Python): `frozen_before_outcomes is True`, `outcome_metrics_present is False`, manifest sha256 matches expected → `ok`.
- No full pytest/deps-suite run in this session (environment noted previously as deps-sensitive; pandas/numpy absent in runner context historically). No exploratory outcome run executed.

## Evidence added and where
- `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md` — frozen Gate 4 v4 prereg (human-readable).
- `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` — machine-readable freeze record (`frozen_before_outcomes=true`, `confirmatory_claim_go=NO_GO`, boundary rationale, splits/ablations/metrics).
- Existing FCLR-015 identity evidence referenced (not regenerated): `research_state/fclr015_local_audit/fclr015_input_manifest_2024_04_09_20261107T180626Z.json` and probe artifacts.
- `AGENT_HANDOFF.md` (this file) updated as the only root durable handoff.

## Current state of each research gate
- **Track A (observed liquidation data / overlay trigger):** **BLOCKED/NO TRIGGER.** ironflow `data_through=2026-10`, probes==2, forward edge 2026-11..2027-02 absent → 404. `tracka_resume_check` pass. **DO NOT re-probe.** Resume only on admissible unauthenticated observed-liquidation data + strict GO rubric + prereg before outcomes.
- **Track B (liquidation boundary labels):** **CLOSED/INCONCLUSIVE.** Modeled boundaries ≠ observed liquidations; never relabel. No re-probe.
- **Track C (funding-conditioned volatility / Gate 4):** **ACTIVE (only open claim-path).** FCLR-015 2024-04..09 cache identity **COMPLETE for checked scope** (3690/3690 MATCH vs Binance Vision; confirmatory still gated). **v4 prereg frozen before outcomes** exists. **Confirmatory remains NO-GO on the 2024-04..09 slice** due to sealed-anchor domain/confounding rationale; only exploratory runs labeled `EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE` are authorized on this slice after freeze. Claim-worthy confirmatory requires a distinct admissible non-confounded boundary preregistered before outcomes + ≥5 instruments + ≥3 non-overlapping 30-day test blocks + clean leakage + stable preregistered uncertainty.
- **Confirmatory anchors (never overwrite/promote/overlay):** FCLR-002 test 2024-07-23..2024-09-30; FCLR-003 sha256 `a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2` (test 2024-10-02..2024-12-31); FCLR-013 sha256 `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a` (2026-08-26..2026-09-30, NOT_MET, 1×30d). v3 anchor oid in tests `9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e`. Confirmatory CLOSED NEGATIVE on executed claim-worthy panels; **no overlay eligible**.

## Bottlenecks removed / progress
1. **Gate 4 v4 prereg frozen (P0 removed):** `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md|json` exists with `frozen_before_outcomes=true` and no outcome metrics. Removes “no frozen v4 prereg” blocker.
2. **FCLR-015 identity/manifest complete (prior, verified):** 3690/3690 MATCH for 2024-04..09 scope. Identity bottleneck removed for this slice; confirmatory still gated.
3. **Track A/B churn removed:** no re-probe; guarded fail-closed behavior preserved conceptually; `tracka_resume_check` still passes.
4. **Handoff hardened:** single durable root, timestamped initial message, explicit non-skippable heavy campaign, sealed-anchor/boundary guardrails.

## Next focus campaign (heavy, ordered, measurable — NO SKIPPING)
**P0 — 1. Boundary/admissibility evidence record (mandatory before any v4 run):** write `research_state/gate4_v4_boundary_admissibility_20261107T1845Z.md` (or timestamped equivalent) documenting GO/NO-GO vs sealed anchors using FCLR-002/003/013/v3 test windows and v4 prereg rationale. **GO for exploratory-only on 2024-04..09 slice; NO-GO for confirmatory on this slice.** If confirmatory is desired, stop and preregister a materially distinct admissible non-confounded boundary before outcomes.
**P0 — 2. Deterministic exploratory smoke (only after P0; never confirmatory):** small bounded ablation on the preregistered 2024-04..09 slice (reuse v3-compatible logic if present; adapt to v4 manifest/provenance) with leakage checks, tmp/non-canonical output paths, and every artifact labeled **`EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE`**. Record seed/reps, git SHA, manifest sha256, split coverage, and null/inconclusive honestly. **Never overwrite** sealed anchors or v3 canonical outputs.
**P1 — 3. Confirmatory-path design (heavy, separate prereg required):** if exploratory smoke is clean, design a v5 prereg only on a **materially distinct admissible boundary** not confounded with sealed FCLR-002/003/013/v3 test windows; prove non-overlap, data sufficiency for ≥3×30-day non-overlapping test blocks, leakage controls, and freeze before outcomes. Do not retrofit v4 into confirmatory.
**P1 — 4. Canonical artifact/LFS/hash debt (evidence-only):** investigate `tests.test_fclr_canonical_artifacts` failures in non-LFS envs (`run_manifest_funding_v3_30d.json` LFS pointer oid `9fd540bd...`; `evaluation_summary_funding_v3_30d.md` hash divergence). Propose minimal non-destructive fix (e.g., LFS-aware test or committed-text source) without regenerating sealed confirmatory outputs; land only with deps-env green tests.
**P1 — 5. Alt liquidation source hunt (materially distinct, bounded):** scan for actual forced-liquidation event records meeting rubric (≥5 symbols, ≥1 complete month or ≥3×30-day blocks, completeness/license/provenance). Update `research_state/alt_source_scan_latest.json` / `alt_source_deep_review_latest.md` only with concrete evidence. **Never fabricate. Never relabel modeled breaches as observed.**
**P2 — 6. Hygiene/tests:** keep `tracka_resume_check` pass; add tmp-isolated tests for any new runner/manifest logic; run full `pytest tests/` in deps env before claiming green; no `.github/workflows` edits; no `__pycache__`/bulk `data/` commits; no status-only churn.

## Single highest-value next task
Write the v4 boundary/admissibility evidence record (P0-1) and then execute a bounded deterministic exploratory smoke (P0-2) on the frozen v4 2024-04..09 slice, strictly labeled `EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE`, with outputs isolated from sealed/canonical artifacts.

## Precise command/check that verifies it
- Resume gate: `python3 scripts/tracka_resume_check.py` (expect `"pass": true`, `"network": false`, `"writes_real_research_state": false`).
- Prereg freeze sanity: `python3 -c "import json; d=json.load(open('research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json')); assert d['frozen_before_outcomes'] and not d['outcome_metrics_present']; print('ok')"` (expect `ok`).
- Full suite (deps env): `pytest tests/` (note known LFS/hash sensitivity in `tests.test_fclr_canonical_artifacts` in non-LFS environments; investigate/fix non-destructively).

## Source/engineering blocker with evidence and next materially different free route
- **Blocker:** Confirmatory Gate 4 evidence is not claim-worthy on the current 2024-04..09 slice because that calendar domain family is confounded with sealed 2024 panel lineage (FCLR-002/v3/FCLR-003 context); v4 therefore authorizes exploratory-only on this slice. Track A observed liquidations remain absent/blocked (ironflow edge 404, probes exhausted). Track B modeled labels are non-admissible as observed liquidations.
- **Evidence:** `AGENT_HANDOFF.md` sealed anchors; `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` (`confirmatory_claim_go: NO_GO`); `python3 scripts/tracka_resume_check.py` pass/blocked state.
- **Next materially different free route:** (a) run exploratory v4 smoke for signal/leakage plumbing only (non-confirmatory), then (b) preregister v5 on a distinct admissible non-confounded window/slice if sufficient local/cache data exists with non-overlap proof; (c) continue bounded unauthenticated scans for actual forced-liquidation event records (≥5 symbols, ≥1 month or ≥3×30-day blocks, license/provenance/completeness) — only concrete evidence recorded.

## Per-session contract (end-of-session)
AGENT_HANDOFF.md states: (1) what changed and why; (2) what was actually tested, with exact outcomes; (3) what evidence was added and where; (4) current state of each research gate; (5) the single highest-value next task; (6) the precise command or check that verifies it (`python3 scripts/tracka_resume_check.py` for resume gate; `pytest tests/` in deps env for suite); (7) any source/engineering blocker with evidence and the next materially different free route.

**Authority:** this file is the only root durable handoff.
