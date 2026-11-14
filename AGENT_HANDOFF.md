# SINGLE DURABLE HANDOFF — 2026-11-14T13:15:35Z (initial task for next agentic session)

## Repository / mission
- **Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility & liquidation risk; Binance 5-symbol Track C + Hyperliquid/Track A frontier). Forecast validation only; no trading/overlay promotion.
- **Verified baseline (this session, 2026-11-14):** `python3 scripts/next_campaign_status.py` → **no frozen preregs without evaluation artifacts**; Binance 5-symbol 3-block design exhausted (READY disjoint months 2025-01/06/11/12 form no contiguous ≥127d run); **Hyperliquid 2026-01-18..2026-04-30 is listed FEASIBLE (forward-reduced 60/7/3×10, 103d) but is ALREADY TESTED/EXHAUSTED** by `TRACKA-LIQ-XSEC-FORWARD` (`evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json`, EXPLORATORY_NULL) and `TRACKA-VOL-FORWARD` (`evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T03:30:40Z.json`, EXPLORATORY_NULL/VALID_EXPLORATORY). Do not treat it as a fresh claimable window. `tests/test_next_campaign_status.py` 12/12 PASS. Gate 4 Branch 1 remains **EXTERNAL_BLOCKED** (no valid `fclr016_v5_terms_evidence_RESOLVED_*.json` with `status==RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation); matches found only: `*_BLOCKED_*`, `*_UNRESOLVED_*`.

## Completed / terminal (do not reopen, re-acquire, rebuild, re-evaluate, or relitigate)
- **FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z:** COMPLETE, `EXPLAINED_BY_ESTIMATOR` (EXPLORATORY_ONLY, promotable=false). 2×2 on identical 1,472 (coin,ts) keys: sealed+sealed 19.0371%, recompute+sealed 19.0371%, sealed+recompute 6.19%, recompute+recompute 6.19% C2_vs_B1 QLIKE reduction. Gap = estimator (raw/unscaled fill-missing-0 vs z-scored train-only drop-missing), not data. Artifacts: `research_state/prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.{json,md}`, `evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T113226Z.{json,md}`, `scripts/fclr_liq_expansion_reconcile.py`, `tests/test_fclr_liq_expansion_reconcile.py`. Sealed verdicts unchanged.
- **TRACKA-HL-EXPANSION (2026-05..2026-10, 8-symbol, observed liq):** executed; sealed PASS 19.04% but robustness FRAGILE (LOIO 4/8, placebo FAIL); independent recompute INCONCLUSIVE (6.19%); reconciled above. Terminal for this panel/design.
- **TRACKA-VOL-FULLHIST (2025-06-01..2026-01-17):** NOT_MET (terminal).
- **Forward 2026Q1Q2 (2026-01-18..2026-04-30):** LIQ-XSEC-FORWARD EXPLORATORY_NULL; VOL-FORWARD EXPLORATORY_NULL/VALID_EXPLORATORY. Region exhausted.
- **Track C volatility cross-period:** FCLR-011 sealed PASS (2026-05..2026-08) does not generalize (2024Q4/2025/2025H2/2025Q1Q2/forward all NOT_REPLICATED). H1_primary NOT_SUPPORTED. Gate 4 Branch 1 EXTERNAL_BLOCKED (agent must never set `RESOLVED_VERIFIED` or `fabricated=true`).
- Preserve all sealed artifacts (FCLR-002/003/011, Track A/B/C records).

## CURRENT BOTTLENECK (why no routine confirmatory/heavy cell is queued)
- No unfrozen/unexecuted preregistered heavy cell on cached/admissible data; Binance and Hyperliquid forward designs exhausted/tested; no valid Gate 4 trigger; no verified NEW observed-liquidation source meeting §16 minima (≥5 instruments, ≥3 non-overlapping 30-day blocks or equivalent preregistered complete-month design, unauthenticated, provenance/license, observed-only labels, venue-consistent, joinable).
- **STALE DIRECTIVES REMOVED:** `NEXT_SESSION_HANDOFF.md` (2026-11-14T09:23:34Z) still says "Execute Step 1 of TRACKA-HL-EXPANSION" and treats forward window as actionable — this is obsolete. `AGENT_HANDOFF.md` and this block supersede it; do not follow stale steps.

## NEXT HEAVY WORK CAMPAIGN (mandatory, bounded, fail-closed) — `FCLR-NEW-ADMISSIBLE-SOURCE-AUDIT-2026-11-14T13:15:35Z`
**Objective:** convert "no obvious source" into timestamped, evidence-backed admissibility decisions; if and only if a source passes §16, freeze+execute a new prereg in-session. No status-only completion.

### Step 1 — Gate 4 trigger check (deterministic, first action)
- Search for `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` where `status==RESOLVED_VERIFIED`, `fabricated==false`, and human/legal attestation present.
- **Result this session:** NONE found (only BLOCKED/UNRESOLVED). Record `NO_VALID_GATE4_TRIGGER` with evidence in the audit artifact. If a valid file later appears, immediately execute Gate 4 Branch 1 per gate scripts/tests (no outcome peeking beyond prereg).

### Step 2 — Bounded admissibility re-audit/probe (heavy, evidence-first)
- Inputs: `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/data_source_registry*.json`, `scripts/hunt_alternative_liquidation_sources.py`, `research_state/url_probe_cache.json`/`hf_search_cache.json`.
- Re-evaluate candidates not terminally impossible for §16: prioritize `ochinimus/crypto-liquidation-ticks`, `nick128373/crypto-liquidation-ticks` (license/unauth present but coverage/blocks/instruments unverified or insufficient in prior review), `craftify2221/hyperliquid-builder-liquidation-panel` (overlap/coverage unverified), and any exchange public archives with plausible liquidation paths not yet conclusively probed. Perform **single-pass, bounded, unauthenticated probes** (no credentials/payment/manual download; respect rate limits/backoff). Verify: access, schema/fields, observed-vs-modeled label nature, history depth, instrument count, complete months / non-overlapping 30-day blocks, license/provenance, venue consistency/joinability.
- **This session produced:** `research_state/new_data_admissibility_audit_20261114T123710Z.json` (bounded probes incl. HF datasets-server splits/rows for crypto-liquidation-ticks, Bybit public paths, OKX liquidation-orders endpoint). Use it as baseline evidence; extend if materially new endpoints/files appear.

### Step 3 — Branch (must execute)
- **If any candidate passes all §16 minima:** write `research_state/<source>_admissibility_audit_<UTC>.{json,md}` with PASS evidence; freeze a NEW prereg (`FROZEN_PRE_OUTCOMES`, before outcomes) with design/splits/estimand/gates/hashes; execute acquisition→panel build→evaluation→verdict; run relevant gates/tests; update `experiment_frontier.json`/`hypothesis_registry.json`/`run_manifest.json`/`final_confirmatory_verdict.md` atomically.
- **If none pass (expected given current evidence):** emit/update timestamped `research_state/structural_exhaustion_confirmation_<UTC>.md` citing per-candidate probe evidence and exact failing §16 minima, confirming no agent-removable heavy work remains until a material external trigger; update frontier/task state to bounded trigger-only. **Do not poll or repeat identical probes.**

## Forbidden / regression guards
- No "campaign exhausted/closed" without citing specific UTC probe evidence and failing minima.
- No reading sealed/terminal windows for new claims; no outcome inspection before prereg freeze; no threshold shopping; no modeled/synthetic labels labeled observed.
- No `.github/workflows` edits; no fabricated `RESOLVED_VERIFIED`; no conflating venues/designs.
- `run_manifest.json` may be a Git LFS pointer in CI — do not parse as authoritative JSON if unresolved.

## Immediate action for next session
1. Read `research_state/new_data_admissibility_audit_20261114T123710Z.json` and `research_state/alt_source_deep_review_latest.md`.
2. If no new material evidence since 2026-11-14T12:38:21Z, produce `research_state/structural_exhaustion_confirmation_<UTC>.md` (heavy documentation with exact per-source minima failures) and update `experiment_frontier.json` to reflect bounded trigger-only state; otherwise run step 2 probes only for the materially new candidate and branch per step 3.
3. Record commands/hashes/verdicts; run `scripts/next_campaign_status.py` and relevant tests before any "done" claim.

## Verification commands:
```bash
python3 scripts/next_campaign_status.py
python3 -m pytest tests/test_next_campaign_status.py -v
python3 -m pytest tests/test_fclr_final_structural_closure.py -v
python3 -m pytest tests/test_fclr019_gate4_evidence_bundle_index.py tests/test_fclr020_gate4_readiness_action_matrix.py tests/test_fclr021_gate4_blocker_resolution_checklist_validator.py tests/test_fclr022_gate4_blocker_resolution_evidence_preflight.py tests/test_fclr023_gate4_blocker_resolution_action_plan.py -v
```