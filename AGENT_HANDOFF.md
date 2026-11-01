# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T13:35:38Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 85458d67 (up to date with origin/main)
**HANDOFF ID:** FCLR-HANDOFF-042-20261101T133538Z
**SUPERSEDES:** FCLR-HANDOFF-041 (20261101T133405Z); research_state/AGENT_HANDOFF_OUTCOME.md (2026-11-01T13:31:24Z) is archived read-only — this file is the single durable handoff going forward.
**PRIORITIZATION RATIONALE:** Repo name = funding-conditioned volatility ∩ liquidation risk, read as ONE coupled problem. Track C (volatility-only forecast): all confirmatory panels exhausted, H001 NOT_SUPPORTED/INCONCLUSIVE, sealed — no cells remain without new admissible data + fresh pre-registration; do not rerun (FCLR-003/006/007/008). Track B (modeled boundary breaches): CLOSED_NEGATIVE; codepath separation irrefutable; do not rerun. H002 (funding-correction replication): PERMANENTLY BLOCKED (SSRN HTTP 403; methodology unreconstructible from admissible sources) — stop scheduling, do not promote, no speculative pre-registration. Track A (observed liquidations, ironflow Hyperliquid census): FCLR-010 FORECAST_GATE_PASSED (C2 vs B1 Brier diff −0.003077, 95% CI [−0.004892, −0.001263], relative reduction 2.21% ≥ 2% floor, n=199 instruments, 5 non-overlapping 30-day blocks, 7-day embargo; pre-registered research_state/research_protocol_fclr010.md v1.0 before outcomes; splits frozen_before_outcomes=true at 2026-11-01T05:39:07Z) — the ONLY live confirmatory track; forecast gate MET → risk-overlay eligible ONLY via pre-registration. H_COUPLED-001 (funding × vol regime × lagged observed flow): PASSED at 500 block-bootstrap reps (+4.61% rel Brier vs B1, CI [0.002511, 0.003158], 199 perps, 164 blocks) but pre-registration requires ≥2000 reps — robustness campaign is the mandatory next heavy work.
**STATUS:** Tests 27/27 PASS at HEAD 85458d67 (re-verified 2026-11-01T13:35:00Z). Working tree clean except __pycache__/ rebuilds. FCLR-010 gate PASSED; H_COUPLED-001 PASSED (500 reps), ROBUST (≥2000 reps) NOT STARTED — MANDATORY. Cross-track firewall IMMUTABLE (ironflow Hyperliquid ONLY; no Binance merge; modeled ≠ observed). scripts/fclr010_execute_fast.py banned for confirmatory numbers (fabricated shortcut).

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T13:35:38Z
**PRIORITY P0 | TYPE: FCLR-COUPLED-ROBUST + FCLR-010 VERIFICATION (HEAVY, UNAVOIDABLE) | NO DISCOVERY | NO CROSS-TRACK MERGE | NO FABRICATED METRICS | NO OUTCOME RE-INSPECTION**

All work uses FROZEN FCLR-010 splits from run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z). Ironflow Hyperliquid ONLY. Test window 2026-05-28 .. 2026-10-31 SEALED — no outcome re-inspection, no threshold tuning, no split changes, no relabeling.

1. **Verify baseline (30s):**
   `git -C <repo> log --oneline -1` → 85458d67
   `python -m unittest discover -s tests -v` → 27/27 PASS; record result here.
   Confirm `research_state/evaluation_summary_FCLR010.md`: gate PASS; C2 vs B1 −0.003077; CI [−0.004892, −0.001263]; rel reduction 2.21% ≥ 2%; 199 instruments; 5 blocks.
   Confirm `research_state/evaluation_summary_FCLR-COUPLED-001.md`: all gates PASS; +4.61% rel Brier; CI [0.002511, 0.003158]; 500 reps; 199 perps; 164 blocks.

2. **Independent recomputation audit of FCLR-010 headline (heavy):** from cached inputs + SHA-256 hashes only — no new downloads, no outcome re-inspection — reproduce B0/B1/C1/C2 Brier, paired C2 vs B1 diff −0.003077, CI approx [−0.004892, −0.001263], relative reduction 2.21%, n=199, 5 non-overlapping 30-day blocks, 7-day embargoes → write `research_state/independent_recompute_audit_FCLR010.md`. Must match `evaluation_summary_FCLR010.md` within declared tolerance.

3. **FCLR-010 leakage / label-history audit:** audit every predictor for future-label leakage; document per-feature provenance; fix/remove any leaking feature before any promotion claim. Zero unresolved leaking features is a hard acceptance gate → document in `research_state/fclr010_leakage_audit.md` (consolidate into research_state/leakage_audit.md if preferred).

4. **≥2000 block-bootstrap robustness of H_COUPLED-001 (coupled):** recompute C_coupled vs B1 on the frozen test set with ≥2000 block-bootstrap replicates (~24h blocks); report mean diff, 95% CI, relative Brier reduction. Acceptance: relative Brier reduction ≥ +1.0% AND CI does not cross zero.

5. **Chronological time-split robustness:** split the test window into earlier half and later half; evaluate each half separately and pooled; report per-half relative Brier and CIs.

6. **Leave-one-symbol-out (LOSO):** across all 199 native perps, drop each symbol in turn and recompute the paired contrast; report min/max relative Brier and worst-case CI; no single symbol may drive the improvement.

7. **Pre-specified ablations (fixed logistic form):** (a) drop interactions, (b) drop lagged observed flow terms; keep firewall, splits, decision-time features; report relative Brier vs B1 for each.

8. **Write full report + seal campaign:** create `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md` with tables for items 4–7. Update this handoff gate states (H_COUPLED-001 ROBUST PASS/FAIL with concrete numbers). Update `research_state/experiment_frontier.json` (FCLR-010 COMPLETE/gate PASSED; H_COUPLED-001 ROBUST status) and `research_state/cross_track_decision_log.md` (Track A status). Tree clean except __pycache__/; this file remains the single source of truth.

9. **Track A risk-overlay eligibility decision:** forecast gate MET → overlay eligible. Either (a) draft a liquidation-risk overlay / position-sizing specification and pre-register it BEFORE any overlay outcome inspection, or (b) formally close Track A with overlay rationale documented. No overlay building or tuning without pre-registration.

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- Cross-track firewall: ONLY ironflow Hyperliquid labels. NO Binance merge. Modeled != observed.
- Frozen splits only; no re-splitting; fixed logistic form unless strictly necessary and pre-registered with justification.
- Block-aware inference; Holm/BH if multiplicity introduced.
- No .github/workflows/* changes. No activity commits unless explicitly requested.
- All 27 tests MUST remain PASS.
- Do not rerun exhausted Track C/B/A discovery or sealed panels (FCLR-001..009); do not re-inspect sealed FCLR-010 outcomes.
- No threshold shopping, relabeling, or outcome inspection before/after split freeze.
- No risk overlay without pre-registration.
- If tempted to "explore" anything else — don't. The repo is funding-conditioned volatility ∩ liquidation risk. Finish coupled robustness + Track A verification first.

## BOTTLENECKS REMOVED (DO NOT RECREATE)
- H002: SSRN 403 accepted as permanent block; stop scheduling H002 confirmatory work; revisit only if SSRN becomes accessible, with pre-registration BEFORE outcome inspection.
- Track B: CLOSED_NEGATIVE; separation irrefutable; no rerun.
- Track C: H001 NOT_SUPPORTED / CONFIRMATORY CLOSED; all confirmatory panels exhausted; no rerun without new admissible data + fresh pre-registered experiment ID.
- Track A structural block: REMOVED — admissible ironflow source passes full rubric (12 monthly blocks 2025-11..2026-10, 199 native perps, CC BY 4.0, unauthenticated, no_keys, hashes in data_source_registry.json). Do not re-run exhausted source families unless a NEW source family appears.
- FCLR-010: execution complete, gate passed, window sealed. Do not re-fit, re-tune, or re-inspect outcomes.
- Fabricated shortcut removed: scripts/fclr010_execute_fast.py banned for confirmatory work; real computation path only (≥2000 reps).

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (paths: independent recompute audit, leakage audit, robust evaluation summary)
4. Gate states per track (H_COUPLED-001 ROBUST PASS/FAIL with numbers; Track A overlay decision)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW)
**Task:** Complete items 1–8 above: baseline verify, FCLR-010 independent recompute audit, leakage audit, ≥2000-rep block-bootstrap coupled robustness, chronological time-split halves, LOSO over 199 perps, pre-specified ablations; write `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md`; update this handoff, `experiment_frontier.json`, `cross_track_decision_log.md`; record Track A overlay decision (pre-registered spec or formal close).

**Verify:**
```bash
LATEST_ROBUST=$(ls -t research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST*.md 2>/dev/null | head -1); test -n "$LATEST_ROBUST" && echo "=== $LATEST_ROBUST ===" && grep -n -E "rel.*Brier|LOSO|time.*split|ablat|PASS|FAIL|CI|min.*rel|max.*rel" "$LATEST_ROBUST" | head -60
test -f research_state/independent_recompute_audit_FCLR010.md && grep -n -E "−0.003077|2\.21%|199|5 blocks" research_state/independent_recompute_audit_FCLR010.md | head
python -m unittest discover -s tests -v 2>&1 | tail -1
```

## DO-NOT RULES (CROSS-CUTTING)
- No merging Hyperliquid labels with Binance panels (cross-track firewall).
- No outcome/Brier/QLIKE inspection before split freeze; no sealed-window reuse (FCLR-010 test window sealed).
- Do not relax rubric, ≥2% floor (FCLR-010) / ≥1.0% floor (coupled), CI-excludes-zero, ≥5 instruments, ≥3-block minimums; no threshold shopping; no relabeling exploratory as confirmatory.
- No risk overlay without pre-registration; no .github/workflows/* changes; commit nothing merely for activity.
