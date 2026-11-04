# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T041140Z
Git SHA (HEAD): 3195771e8cf4f51d5b37ec513612d1d6a2b0a5bd
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T041140Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-ZERO-LATENCY-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-030-TRACK-C-ZERO-LATENCY-FORCED
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL)
CAMPAIGN: FCLR-NEXT-030-FUNDING-CONDITIONED-VOLATILITY-HEAVY-CONTINUOUS

TIMESTAMP (UTC): 20261104T040853Z

OBJECTIVE: The repository name is the binding directive. All effort must go towards TRACK C. There are currently NO admissible triggers for forward validation (ironflow has 2026-10.parquet through 2026-10-31 but that is Track-A liquidation data, NOT a Track C trigger; Binance root only contains 2024 zips; all 2026 zips are zero-volume synthetic placeholders -> NOT admissible). DO NOT WAIT PASSIVELY. Every single session MUST execute the heavy work mandate below to achieve zero-latency execution the INSTANT an admissible trigger appears.

HEAVY WORK MANDATE (NON-NEGOTIABLE - EXECUTE ALL 5 EVERY SESSION):

(1) FULL INVENTORY HARDENING
    - Enumerate all root zips by asset/month/year
    - Scan research_state/data_cache/ironflow_events/ for any files > 2026-09-30
    - Scan all binance data_vision artifacts
    - Diff against LATEST trigger_harden_*.json in research_state/watch/
    - Write a successor trigger_harden_<UTC>.json with concrete diffs (no "no change" fluff)

(2) PREREG GATING PROOF
    - Run: python -c "from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); print(h.evaluate_forward(data_path='/tmp/no_data_x.zip', output_dir='/tmp/x'))"
    - MUST return BLOCKED with an explicit preregistration error. Capture exact output and traceback in the artifact.
    - Verify pre_register_forward_experiment() is importable and testable

(3) TRACK C READINESS VALIDATION
    - Load and schema-validate research_state/readiness/track_c_prereg_template_fclr012.json
    - Verify frozen components: features (funding, RV, premium/EMA), targets (24h primary + 6h/72h/168h secondary), baselines (B0/B1), ablations (C1/C2), CV/walk-forward, embargo, sealed holdout, multiplicity (Holm), block bootstrap (>=2000, seed 12345)
    - Structure-only. NEVER inspect outcomes. Ensure template is consumable by pre_register_forward_experiment() with zero outcome-snooping

(4) INTEGRITY SWEEP
    - Hash check: cross_track_decision_firewall.md (IMMUTABLE/SEALED), sealed_holdout_integrity.md, structural_closure_verdict_heavy.md
    - Verify manifests untouched in a breaking way: experiment_frontier.json, run_manifest.json, hypothesis_registry.json
    - Confirm NO modifications under .github/workflows/
    - Explicitly confirm sealed experiments FCLR-001,002,003,006,007,008,011 are UNTOUCHED
    - Record all hashes in artifact

(5) TRIGGER ALERTING + ACTIONABLE ARTIFACT
    - Write research_state/watch/trigger_harden_<UTC>.json containing: inventory, gating_proof, track_c_readiness, integrity_hashes, concrete diffs, next_runnable_commands
    - MUST include an "IF TRIGGER FIRES NOW" checklist: (a) load frozen template, (b) preregister BEFORE inspecting outcomes, (c) enforce embargo/splits, (d) run ONLY pre-registered contrasts, (e) apply Holm + block-bootstrap, (f) do NOT touch sealed panels
    - MUST include a machine-actionable next_runnable_commands array

BOTTLENECK REMOVAL RULES (HARD):
- If any check > 30s, parallelize, optimize, or use cache. Do not block on passive downloads.
- Every artifact must ENABLE IMMEDIATE ACTION. No status-only, no "all good" summaries with no commands.
- Tests MUST remain >= 117 passing. Run `python -m unittest discover -s tests -v` first if anything is touched. Fix immediately on failure.
- NEVER re-run sealed FCLR-001/002/003/006/007/008/011. Firewall is IMMUTABLE.
- FCLR-012-V is BLOCKED on admissible data. The remedy is continuous hardening + zero-latency readiness, NOT idling.
- Preregister BEFORE inspecting holdout outcomes. Frozen config ONLY. Block bootstrap >=2000 with seed 12345. Holm correction across declared family.
- All current 2026 zips are zero-volume synthetic placeholders -> NOT admissible. Ironflow has 2026-10.parquet (Track A only); it does NOT fire the Track C trigger.
- Do not snoop outcomes to "pre-validate". Structure-only for readiness.

MANDATORY ACTION SEQUENCE (EXECUTE IN ORDER):
1) TESTS: python -m unittest discover -s tests -v (expect >=117 OK)
2) INVENTORY: python scripts/track_c_inventory_harden.py (diff vs LATEST trigger_harden_*.json) -> write successor
3) GATING_PROOF: Capture evaluate_forward BLOCKED without prereg with exact message/traceback
4) TRACK_C_VALIDATE: Validate track_c_prereg_template_fclr012.json schema completeness
5) INTEGRITY: Run integrity sweep with hashes, verify sealed experiments untouched
6) HEAVY_ARTIFACT: Write timestamped successor in research_state/watch/ with all required sections + IF-TRIGGER-FIRES-NOW + next_runnable_commands

RANKED HEAVY TASKS (IF TIME REMAINS AFTER 1-6):
- Harden trigger detection script to exit 0/1 with machine-readable alert on admissible data (check for non-zero volume/taker_buy, valid date ranges, not synthetic placeholders)
- Ensure FCLR010Harness.pre_register_forward_experiment() can consume frozen template with NO outcome inspection
- Add strict admissibility check for any new zip (non-zero volume/taker_buy, schema valid, no placeholder signatures) - structure only, NO data snooping
- Keep experiment_frontier.json and hypothesis_registry.json current without scope creep
- Add regression test(s) to prevent accidental re-run of sealed experiments
```

## 1) Current State (Verified 20261104T035501Z)

- Tests: 117/117 OK (`python -m unittest discover -s tests -v`) — re-verified this session
- Git HEAD: 3195771e8cf4f51d5b37ec513612d1d6a2b0a5bd (main). Note: HEAD advanced past the SHA cited by earlier handoffs (ec54d1e4 / 2d7245f1); do not act on stale SHA references.
- Ironflow: `research_state/data_cache/ironflow_events/` contains 2025-05..2026-10.parquet; latest is `2026-10.parquet` (data through 2026-10-31). `trigger_ironflow_gt_20260930 = true` but this is Track-A liquidation data, NOT an admissible Track C trigger.
- Root data: 463 zips total, all 2024 (01-01..03-30). No 2025/2026 Binance archives in root. All 2026 zips are zero-volume synthetic placeholders -> NOT admissible.
- Admissible trigger: NONE for Track C. `track_c_prereg_template_fclr012.json` trigger.current_state = NOT_FIRED.
- Sealed window: 2026-05-08..2026-08-06 (frozen). DO NOT re-run sealed panels.
- Prereg gating: ENFORCED (`evaluate_forward` BLOCKED without prereg with explicit reason: "Pre-registration path required.")
- Track C prereg template: `research_state/readiness/track_c_prereg_template_fclr012.json` exists (structure-only, v2.0-harness-compatible)
- Gates: FCLR-010 PASSED (sealed) | FCLR-011 PASSED (sealed, +4.94% rel QLIKE, CI excludes zero) | FCLR-012-V INCONCLUSIVE (0 non-overlapping 30-day blocks, CI spans zero)
- Overlay: INELIGIBLE per IMMUTABLE `cross_track_decision_firewall.md`
- H001: NOT_SUPPORTED on widest unsealed powered panel (FCLR-008)

## 2) Bottlenecks Removed / Active

- **REMOVED (stale state):** Earlier handoffs cited git SHA `ec54d1e4`/`2d7245f1` instead of HEAD `3195771e`, and claimed ironflow ends 2026-09-30 with "no 2026-10.parquet" (false: `2026-10.parquet` exists). Both corrected so the next agent does not act on false state. Inventory script threshold fixed from `> '2026-10.parquet'` to `> '2026-09.parquet'` to match the >2026-09-30 directive.
- **REMOVED (idle waiting):** Swapped passive monitoring for continuous trigger detection + Track C zero-latency readiness. No session may sit idle.
- **PREVENTED:** Firewall enforced to block re-running sealed panels.
- **HARDENED:** Prereg gating proof is now a required per-session artifact.
- **ACTIVE:** Waiting for admissible unauthenticated 2026 Binance panel beyond sealed FCLR-011 test window 2026-05-08..2026-08-06 (non-zero volume/taker_buy, not placeholder). Harden everything NOW.

## 3) Immediate Next Actions (MANDATORY)

1. `python -m unittest discover -s tests -v` (confirm >=117 OK)
2. `python scripts/track_c_inventory_harden.py` (diff vs latest `trigger_harden_*.json`)
3. Capture gating proof: `python -c "from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); print(h.evaluate_forward(data_path='/tmp/no_data_x.zip', output_dir='/tmp/x'))"` -> record BLOCKED with exact output
4. Validate `research_state/readiness/track_c_prereg_template_fclr012.json` schema (structure-only)
5. Run integrity sweep (hashes of seals/firewalls/manifests) and verify sealed experiments untouched
6. Write heavy successor artifact to `research_state/watch/trigger_harden_<UTC>.json` with all required sections

## 4) Files To Watch

- `research_state/watch/trigger_harden_*.json` (latest: `trigger_harden_20261104T035729Z.json`)
- `research_state/readiness/track_c_prereg_template_fclr012.json`
- `scripts/fclr010_harness.py` (`pre_register_forward_experiment()`, `evaluate_forward()`)
- `scripts/track_c_inventory_harden.py`
- `scripts/write_trigger_harden_successor.py`
- `cross_track_decision_firewall.md` (IMMUTABLE)
- `sealed_holdout_integrity.md`, `structural_closure_verdict_heavy.md`
- `research_state/experiment_frontier.json`, `research_state/run_manifest.json`, `research_state/hypothesis_registry.json`

## 5) Definition Of Done For This Session

This session is NOT complete until:
- All 6 mandatory action sequence items have been executed
- A new `trigger_harden_<UTC>.json` exists in `research_state/watch/` with inventory diffs, gating proof, track_c readiness validation, integrity hashes, "IF TRIGGER FIRES NOW" checklist, and `next_runnable_commands`
- Tests are still >=117 passing
- No files under `.github/workflows/` were modified
- No sealed experiments (FCLR-001/002/003/006/007/008/011) were touched
- AGENT_HANDOFF.md has been updated to reflect the new timestamp and handoff ID
- This session's heavy artifacts: research_state/watch/trigger_harden_20261104T035639Z.json (inventory) and research_state/watch/trigger_harden_20261104T035729Z.json (heavy successor with gating proof, track_c readiness, integrity hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands)

## SESSION UPDATE (20261104T043231Z) - HEAVY TRACK-C CAMPAIGN EXECUTED
- Tests: 117/117 OK (confirmed after LFS pull of run_manifest.json)
- Created successor: research_state/watch/trigger_harden_20261104T043231Z.json (inventory from latest, gating proof BLOCKED without prereg with exact message, track_c_prereg_template_fclr012.json schema validated structure-only, integrity hashes of seals/firewalls/manifests, sealed experiments untouched, workflows unchanged, IF-TRIGGER-FIRES-NOW checklist + next_runnable_commands)
- Inventory hardening run produced trigger_harden_20261104T043112Z.json (diffs vs previous)
- Gating proof captured: evaluate_forward BLOCKED with reason "Pre-registration path required. Call pre_register_experiment() and inspect no outcomes before it exists."
- Bottlenecks: idle waiting removed (zero-latency readiness), stale SHA context corrected, ironflow 2026-10 correctly classified Track A only, all 2026 zips zero-volume placeholders not admissible, firewall/prereg enforced
- Next: monitor for admissible unauthenticated 2026 Binance panel (non-zero volume/taker_buy, schema valid, not placeholder). Do NOT snoop outcomes; preregister BEFORE inspecting.
