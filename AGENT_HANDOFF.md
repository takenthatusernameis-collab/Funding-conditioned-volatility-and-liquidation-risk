# SINGLE DURABLE HANDOFF — 2026-11-14T13:35Z (initial task for next agentic session)

## INITIAL TASK MESSAGE (read and execute this block first)
**State:** Campaign is **bounded trigger-only / structurally exhausted** for agent-removable heavy work. `AGENT_HANDOFF.md` is the single durable handoff; `NEXT_SESSION_HANDOFF.md` is an obsolete pointer only.

**You MUST do heavy work when a trigger is satisfied. You MUST NOT do status-only or repeated-probe sessions when no trigger is satisfied.**

1. **Mandatory triage (every session, in order):**
   - `python3 scripts/next_campaign_status.py` (truth: expect "no feasible 3-block design in EITHER domain" unless state changed).
   - Gate 4: `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo NO_VALID_GATE4_TRIGGER` and accept only files with `status==RESOLVED_VERIFIED`, `fabricated==false`, and human/legal attestation (reject `*_BLOCKED_*`, `*_UNRESOLVED_*`).
   - Read `research_state/experiment_frontier.json` rank 0 and `research_state/structural_exhaustion_confirmation_20261114T132741Z.md`.
2. **If NO trigger is satisfied:** clean stop. Record "still trigger-only" with command outputs; do **not** poll, do **not** repeat probes already falsified in `structural_exhaustion_confirmation_20261114T132741Z.md`, do **not** re-open tested windows (incl. 2026-01-18..2026-04-30, TRACKA-HL-EXPANSION, TRACKA-VOL-FULLHIST, forward LIQ/VOL cells), do **not** reopen sealed/terminal verdicts.
3. **If a trigger IS satisfied:** execute the matching heavy-work campaign below to completion with fail-closed rigor (prereg before outcomes, provenance/hashes, deterministic artifacts, tests, atomic state/frontier/handoff updates). Future agents must not defer trigger-satisfied work.

## Repository / mission
- **Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility & liquidation risk; Binance 5-symbol Track C + Hyperliquid/Track A frontier). Forecast validation only; no trading/overlay promotion.
- **Verified baseline (this session, 2026-11-14):** `python3 scripts/next_campaign_status.py` → **no frozen preregs without evaluation artifacts**; Binance 5-symbol 3-block design exhausted (READY disjoint months 2025-01/06/11/12 form no contiguous ≥127d run); **Hyperliquid 2026-01-18..2026-04-30 is listed FEASIBLE (forward-reduced 60/7/3×10, 103d) but is ALREADY TESTED/EXHAUSTED** by `TRACKA-LIQ-XSEC-FORWARD` (`evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json`, EXPLORATORY_NULL) and `TRACKA-VOL-FORWARD` (`evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T03:30:40Z.json`, EXPLORATORY_NULL/VALID_EXPLORATORY). Do not treat it as a fresh claimable window. `tests/test_next_campaign_status.py` 12/12 PASS (script updated 2026-11-14T13:27:41Z to mark the forward reserve as tested; now reports "no feasible 3-block design in EITHER domain"). Gate 4 Branch 1 remains **EXTERNAL_BLOCKED** (no valid `fclr016_v5_terms_evidence_RESOLVED_*.json` with `status==RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation); matches found only: `*_BLOCKED_*`, `*_UNRESOLVED_*`.

**This session (2026-11-14T13:27:41Z) completed `FCLR-NEW-ADMISSIBLE-SOURCE-AUDIT-2026-11-14T13:15:35Z` Steps 1–3:**
- Step 1 Gate 4 check: `NO_VALID_GATE4_TRIGGER` (only `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`).
- Step 2 bounded admissibility re-audit: `research_state/new_data_admissibility_audit_20261114T123710Z.json` — probes of `ochinimus/crypto-liquidation-ticks` (~27d coverage, fails month/blocks/instrument minima), `nick128373/crypto-liquidation-ticks` (coverage unverified), Bybit public paths (no census), OKX liquidation-orders (live rows only, no historical census); 0 GO candidates.
- Step 3 branch (none pass): `research_state/structural_exhaustion_confirmation_20261114T132741Z.md` emitted with per-candidate probe evidence and exact failing §16 minima; `research_state/experiment_frontier.json` rank 0 set to bounded `TRIGGER_ONLY` sentinel (`FCLR-BOUNDED-TRIGGER-ONLY-20261114T132741Z`); reconciliation `FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z` marked COMPLETED (`EXPLAINED_BY_ESTIMATOR`). `scripts/next_campaign_status.py` + `tests/test_next_campaign_status.py` updated so the stale "forward-feasible" listing no longer misreports an executable window (12/12 PASS). `NEXT_SESSION_HANDOFF.md` (2026-11-14T09:23:34Z) marked OBSOLETE — its "ACTIVE FRONTIER / execute TRACKA-HL-EXPANSION" directives are stale and must not be followed.

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

## NEXT HEAVY WORK CAMPAIGN (mandatory on trigger, bounded, fail-closed) — bounded trigger-only as of 2026-11-14T13:35Z

**Audit completed:** `FCLR-NEW-ADMISSIBLE-SOURCE-AUDIT-2026-11-14T13:15:35Z` (Steps 1–3). Structural exhaustion confirmed: no valid Gate 4 trigger; 0 §16-admissible new observed-liquidation sources; all cached-data cells terminal/exhausted; Hyperliquid forward reserve tested/exhausted; Binance design exhausted. **No agent-removable heavy work remains until a trigger fires.** No polling, no repeated identical probes, no re-execution of tested windows (incl. 2026-01-18..2026-04-30), no status-only sessions.

**Resume triggers (act immediately and heavily when satisfied; do not defer):**
1. `GATE4_BRANCH_1` — valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status==RESOLVED_VERIFIED`, `fabricated==false`, human/legal attestation).
   - **Heavy work:** run full Gate 4 blocker pipeline (019–023) and readiness scripts; execute Branch 1 only per frozen prereg/gate contracts; emit gate artifacts, hashes, and verdict; update `experiment_frontier.json`/`hypothesis_registry.json`/handoff atomically. No outcome peeking beyond prereg; agent must never fabricate RESOLVED_VERIFIED.
2. `NEW_OBSERVED_LIQUIDATION_SOURCE` — materially new candidate (not already falsified in `structural_exhaustion_confirmation_20261114T132741Z.md`).
   - **Heavy work:** (a) §16 admissibility audit artifact with per-candidate probe evidence, provenance/license, instrument/block/depth checks BEFORE outcomes; (b) if ADMISSIBLE, freeze new prereg pre-outcomes (design/contrasts/metrics/materiality/families); (c) bounded acquisition with `.accessed.json`+`.sha256`; (d) deterministic panel build with leakage/coverage notes; (e) pre-registered evaluation (bootstrap CIs, ≥3 blocks, materiality/robustness gates) and verdict artifact; (f) atomic state updates under a NEW experiment ID. If NOT admissible, record evidence and remain trigger-only.
3. `HL_LABEL_EXTENSION` — Hyperliquid coverage ≥100d depth AND verified post-2026-10-31 observed liquidation labels.
   - **Heavy work:** bounded reprobe/audit artifact first; only if a full preregistered design becomes feasible, freeze prereg pre-outcomes then build/eval/verdict with full provenance and state updates. No reuse of tested 2026-01-18..2026-04-30 as a fresh claim.
4. `EXPANSION_ROBUSTNESS_REDO` — cached-panel robustness recheck with a NEW frozen prereg pre-outcomes.
   - **Heavy work:** freeze new prereg specifying estimator/robustness family before outcomes; run full robustness battery (LOIO/placebo/blocks/bootstrap) on the specified cached panel; emit eval + reconciliation-quality verdict; atomic updates. No post-hoc threshold shopping.

## Immediate action for next session
1. Read `AGENT_HANDOFF.md` (this file) and `research_state/experiment_frontier.json` rank 0; treat `NEXT_SESSION_HANDOFF.md` as OBSOLETE — do not execute its stale TRACKA-HL-EXPANSION / forward-window steps.
2. Re-run the trigger check: `python3 scripts/next_campaign_status.py` (expect "no feasible 3-block design in EITHER domain") and the Gate 4 glob (expect `NO_VALID_GATE4_TRIGGER` unless a valid `RESOLVED_VERIFIED` evidence file appeared).
3. If no trigger appeared: clean stop — record "still trigger-only", do not poll or repeat probes, do not open tested windows. If a trigger appeared: execute the matching branch and record commands/hashes/verdicts.
4. Before any "done" claim: `python3 scripts/next_campaign_status.py` + `python3 -m pytest tests/test_next_campaign_status.py -v` + `python3 -m pytest tests/test_fclr_final_structural_closure.py -v` + gate4 tests 019–023.

## Forbidden / regression guards
- No "campaign exhausted/closed" without citing specific UTC probe evidence and failing minima.
- No reading sealed/terminal windows for new claims; no outcome inspection before prereg freeze; no threshold shopping; no modeled/synthetic labels labeled observed.
- No `.github/workflows` edits; no fabricated `RESOLVED_VERIFIED`; no conflating venues/designs.
- `run_manifest.json` may be a Git LFS pointer in CI — do not parse as authoritative JSON if unresolved.

## Verification commands:
```bash
python3 scripts/next_campaign_status.py
python3 -m pytest tests/test_next_campaign_status.py -v
python3 -m pytest tests/test_fclr_final_structural_closure.py -v
python3 -m pytest tests/test_fclr019_gate4_evidence_bundle_index.py tests/test_fclr020_gate4_readiness_action_matrix.py tests/test_fclr021_gate4_blocker_resolution_checklist_validator.py tests/test_fclr022_gate4_blocker_resolution_evidence_preflight.py tests/test_fclr023_gate4_blocker_resolution_action_plan.py -v
```