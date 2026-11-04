# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T025053Z
Git SHA (HEAD): 2d7245f1
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T024900Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-CONTINUOUS-HARDENING

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-026-TRACK-C-ZERO-LATENCY-READY
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting, no deferring)
CAMPAIGN: FCLR-NEXT-026-FUNDING-CONDITIONED-VOL-HEAVY-CONTINUOUS
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility forecasting) >> Track B (modeled boundary breaches) >> Track A (observed liquidation labels)
TIMESTAMP (UTC): 20261104T024900Z
OBJECTIVE: Repository name is MANDATORY - focus on FUNDING-CONDITIONED VOLATILITY. Build zero-latency execution path for Track C. Forward validation FCLR-NEXT-012 BLOCKED pending admissible triggers (ironflow > 2026-10-31 OR unsealed 2026 Binance panel beyond 2026-11-02; all current 2026 zips zero-volume synthetic placeholders -> NOT admissible). DO NOT WAIT PASSIVELY - every session MUST do heavy hardening so the INSTANT trigger fires, we pre-register frozen config and execute with zero latency.
HEAVY WORK MANDATE (NON-NEGOTIABLE - ALL FIVE EACH SESSION):
(1) FULL INVENTORY HARDENING: enumerate root zips (by asset/month/year), research_state/data_cache/ironflow_events/* (>2026-10-31 checked), all Binance data_vision artifacts. Diff vs LATEST trigger_harden_*.json. Must write successor with concrete diffs.
(2) PREREG GATING PROOF: python -c "from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); print(h.evaluate_forward(data_path='/tmp/no_data_x.zip', output_dir='/tmp/x'))" -> MUST return BLOCKED with explicit prereg error. Capture exact output.
(3) TRACK C READINESS VALIDATION: load and validate research_state/readiness/track_c_prereg_template_fclr012.json schema (frozen features/funding/RV/premium/targets/baselines/ablations/CV/walk-forward/sealed holdout/multiplicity). STRUCTURE-ONLY - never inspect outcomes. Ensure pre_register_forward_experiment() path is testable.
(4) INTEGRITY SWEEP: hash-check cross_track_decision_firewall.md (IMMUTABLE/SEALED), sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, experiment_frontier.json, run_manifest.json, hypothesis_registry.json. Verify NO .github/workflows modified. Confirm sealed FCLR-001/002/003/006/007/008/011 untouched.
(5) TRIGGER ALERTING + ACTIONABLE ARTIFACT: write research_state/watch/trigger_harden_<ts>.json with inventory/gating_proof/track_c_readiness/integrity_hashes/diffs/next_runnable_commands AND a concrete "IF TRIGGER FIRES NOW" checklist (pre-register before inspecting outcomes, load frozen template, run only pre-registered contrasts).

BOTTLENECK REMOVAL RULES:
- If any check >30s, parallelize/optimize; use cache if blocking on download.
- No status-only files. Every artifact MUST enable immediate action.
- Tests MUST stay >=117 passing. Run `python -m unittest discover -s tests -v` first if anything touched.
- NEVER re-run sealed FCLR-001/002/003/006/007/008/011 (firewall-sealed - would violate prereg/holdout discipline).
- FCLR-NEXT-012 BLOCKED on admissible data -> REMEDY: continuous trigger detection + Track C zero-latency readiness. Do NOT idle.
- All current 2026 zips are zero-volume synthetic placeholders -> NOT admissible. Ironflow ends 2026-10 (no >2026-10-31). Binance root only 2024.
- Pre-register BEFORE inspecting holdout outcomes. Frozen config only. Block bootstrap >=2000 with seed 12345. Holm correction across declared family.

MANDATORY ACTION SEQUENCE (execute in order):
1) TESTS: python -m unittest discover -s tests -v (expect 117 OK). Fix immediately if fail.
2) INVENTORY: python scripts/track_c_inventory_harden.py (diff vs LATEST trigger_harden_*.json) -> successor artifact
3) GATING_PROOF: capture evaluate_forward BLOCKED without prereg with exact traceback/message
4) TRACK_C_VALIDATE: validate track_c_prereg_template_fclr012.json schema completeness
5) INTEGRITY: verify seals/firewalls/manifests unchanged + hashes
6) HEAVY_ARTIFACT: write timestamped successor with full diffs, gating proof, readiness, integrity hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands

NEXT RANKED HEAVY TASKS (if time remains after above):
- Harden trigger detection script to exit 0/1 with machine-readable alert on admissible data
- Ensure FCLR010Harness.pre_register_forward_experiment() is ready to consume frozen template with no outcome inspection
- Add quick admissibility check for any new zip (non-zero volume/taker_buy) - structure only, no data snooping
- Keep experiment_frontier.json/hypothesis_registry.json current without expanding scope
```

## 1) Current State (verified 20261104T024900Z)
- Tests: 117/117 OK
- Git HEAD: 2d7245f1 (main, clean)
- Ironflow: latest 2026-10.parquet in research_state/data_cache/ironflow_events/ (ends 2026-10-31). trigger_ironflow_gt_20261031=false
- Root data zips: 463 total, all 2024 (01-01..03-30). No 2025/2026 Binance archives in root.
- Admissible trigger: NONE. All current 2026 zips are zero-volume synthetic placeholders -> NOT admissible.
- Sealed window: 2026-05-08..2026-08-06 (frozen). Do NOT re-run sealed panels.
- Prereg gating: ENFORCED (evaluate_forward BLOCKED without prereg with explicit reason)
- Track C prereg template: research_state/readiness/track_c_prereg_template_fclr012.json exists (structure-only, v2.0-harness-compatible)
- Gates: FCLR-010 PASSED (sealed), FCLR-011 PASSED (sealed, +4.94% rel QLIKE, CI excludes zero), FCLR-012-V INCONCLUSIVE
- Overlay: INELIGIBLE per IMMUTABLE cross_track_decision_firewall.md
- H001: NOT_SUPPORTED on widest unsealed powered panel (FCLR-008)

## 2) Bottlenecks Removed / Active
- Bottleneck REMOVED (idle waiting): Continuous trigger detection + Track C zero-latency readiness. No passive polling.
- Bottleneck PREVENTED: Firewall enforced to block re-running sealed panels.
- Bottleneck ADDRESSED: Gating proof automated/capturable.
- Active: Waiting for admissible unauthenticated 2026 Binance panel beyond 2026-08-06 (or ironflow>2026-10-31). Harden everything now.

## 3) Immediate Next Actions (MANDATORY)
1. `python -m unittest discover -s tests -v` (confirm 117 OK)
2. `python scripts/track_c_inventory_harden.py` (diff vs latest trigger_harden)
3. Prove gating: capture BLOCKED without prereg
4. Validate track_c prereg template schema
5. Integrity sweep + write heavy successor artifact in research_state/watch/

## 4) Files to Watch
- research_state/watch/trigger_harden_*.json (latest)
- research_state/readiness/track_c_prereg_template_fclr012.json
- scripts/fclr010_harness.py (pre_register_forward_experiment, evaluate_forward)
- cross_track_decision_firewall.md (IMMUTABLE)
- scripts/track_c_inventory_harden.py
