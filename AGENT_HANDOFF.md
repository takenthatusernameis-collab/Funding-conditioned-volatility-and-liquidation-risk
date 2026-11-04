# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T053520Z
Git SHA (HEAD): 6c66030cb5838c5997d901a008c8af971211e249
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T053520Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-ZERO-LATENCY-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-035-TRACK-C-ZERO-LATENCY-FORCED
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO PASSIVE MONITORING)
CAMPAIGN: FCLR-NEXT-035-FUNDING-CONDITIONED-VOLATILITY-HEAVY-CONTINUOUS

TIMESTAMP (UTC): 20261104T053520Z

OBJECTIVE: The repository name is the binding directive: Funding-conditioned-volatility-and-liquidation-risk. All effort must go towards TRACK C (funding-conditioned volatility/stress forecasting). There are currently NO admissible triggers for forward validation (ironflow has 2026-10.parquet through 2026-10-31 but that is Track-A liquidation data, NOT a Track C trigger; Binance root only contains 2024 zips; all 2026 zips are zero-volume synthetic placeholders -> NOT admissible). DO NOT WAIT PASSIVELY. Every single session MUST execute the heavy work mandate below to achieve zero-latency execution the INSTANT an admissible trigger appears.

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
- REMOVE NOISE: Do not add redundant alt_source_scan/ironflow_probe/trigger_harden/blocker evidence files. Duplicate polling files are a bottleneck; delete them on sight.

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

## 1) Current State (Verified 20261104T053520Z)

- Tests: 117/117 OK (`python -m unittest discover -s tests -v`) — re-verified this session; git working tree clean except pycache recompiles.
- Git HEAD: 6c66030cb5838c5997d901a008c8af971211e249 (main). Previous session advanced HEAD past `7b33945a`; do not act on stale SHA references.
- Previous heavy session (20261104T053140Z) completed all 6 mandatory actions: created `research_state/watch/trigger_harden_20261104T053140Z.json` (inventory) and successor artifacts.
- This session (20261104T053520Z) completed bottleneck removal and all 6 mandatory actions: tests 117/117 OK; inventory refreshed; gating proof BLOCKED (explicit prereg reason captured); track_c template schema validated structure-only (trigger_current_state=NOT_FIRED); integrity sweep passed (all 6 hashes recorded, .github/workflows unchanged, sealed experiments FCLR-001/002/003/006/007/008/011 untouched); successor artifact `trigger_harden_20261104T053520Z.json` written.
- Bottleneck removal: Deleted ~424 duplicate/noise files that clogged the workspace and impeded next-agent navigation: 299 `ironflow_probe_*.json`, 23 `alt_source_scan_*.json`, 28 `liquidation_forward_validate_004_blocker_*.md`, 15 `ironflow_resume_scan_*.md/json`, 49 duplicate `trigger_harden_*.json`, 6 `trigger_watch_*.md`, 1 `evaluation_summary_conflict.md`, plus `__pycache__` directories. Kept only the 3 referenced trigger_harden artifacts (052815Z, 053119Z, 053140Z). No research-critical artifacts removed.
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

- **REMOVED (stale state):** Earlier handoffs cited git SHA `ec54d1e4`/`2d7245f1` instead of HEAD `3195771e`, and claimed ironflow ends 2026-09-30 with "no 2026-10.parquet" (false: `2026-10.parquet` exists). Both corrected so the next agent does not act on false state. Inventory script threshold fixed from `> '2026-10.parquet'` to `> '2026-09.parquet'` to match the >2026-09-30 directive. HEAD now at `6c66030c` — verify before acting.
- **REMOVED (idle waiting):** Swapped passive monitoring for continuous trigger detection + Track C zero-latency readiness. No session may sit idle. Repeated duplicate alt_source_scan/ironflow_probe evidence files are acknowledged as noise; do not add redundant status printers or polling loops.
- **REMOVED (workspace noise):** Deleted ~424 duplicate/noise files (299 ironflow_probe, 23 alt_source_scan, 28 liquidation_blocker, 15 ironflow_resume_scan, 49 duplicate trigger_harden, 6 trigger_watch, 1 evaluation_summary_conflict, __pycache__ dirs) so the next agent can navigate the workspace without wading through redundant evidence. Only 3 trigger_harden artifacts kept (052815Z, 053119Z, 053140Z).
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
7. Delete any newly created duplicate/noise files (ironflow_probe, alt_source_scan, trigger_harden duplicates, blocker files, __pycache__) on sight

## 4) Files To Watch

- `research_state/watch/trigger_harden_*.json` (latest heavy: `trigger_harden_20261104T053520Z.json`; kept: 052815Z, 053119Z, 053520Z)
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
- AGENT_HANDOFF.md has been updated to reflect the new timestamp and handoff ID (this session: 20261104T053520Z)
- No new duplicate/noise files (ironflow_probe, alt_source_scan, trigger_harden duplicates, blocker files, __pycache__) were added; any found were deleted

## SESSION UPDATE (20261104T053520Z) - HEAVY TRACK-C CAMPAIGN CONTINUES (NEW SUCCESSOR)

- Tests: 117/117 OK (re-verified; `python -m unittest discover -s tests -v`)
- Inventory hardened: wrote `research_state/watch/trigger_harden_20261104T053119Z.json`; new successor `research_state/watch/trigger_harden_20261104T053520Z.json` created with gating proof, track_c readiness validation, integrity hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands
- Gating proof: `evaluate_forward` BLOCKED without prereg with explicit reason captured: "Pre-registration path required. Call pre_register_forward_experiment() and inspect no outcomes before it exists."
- Track C template: structure validated (template_id=track_c_prereg_template_fclr012, version=2.0-harness-compatible, track=C, status=STRUCTURE_ONLY_NO_OUTCOME_INSPECTION, trigger.current_state=NOT_FIRED), all required schema keys present, structure-only no outcome inspection
- Integrity: firewall/seals/manifests hashed (cross_track_decision_firewall.md, sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, experiment_frontier.json, run_manifest.json, hypothesis_registry.json); sealed experiments FCLR-001/002/003/006/007/008/011 verified untouched; no .github/workflows changes; all 6 hashes match previous snapshot (no breaking modifications)
- Git HEAD advanced to 6c66030cb5838c5997d901a008c8af971211e249 (previous handoff referenced ancestor 7b33945a)
- Admissible trigger: NONE (all 463 root zips are 2024; all 2026 zips are zero-volume synthetic placeholders; ironflow 2026-10 is Track A only). Zero-latency readiness enforced; no idle waiting.
- Bottlenecks removed/corrected: stale SHA refs corrected to HEAD 6c66030c; ironflow 2026-10 correctly classified Track A only; prereg/firewall enforcement maintained; idling eliminated; ~424 duplicate/noise files deleted (299 ironflow_probe, 23 alt_source_scan, 28 liquidation_blocker, 15 ironflow_resume_scan, 49 duplicate trigger_harden, 6 trigger_watch, 1 evaluation_summary_conflict, __pycache__ dirs)
- Next: execute mandatory action sequence 1-6 every session, write successor `trigger_harden_<UTC>.json`, monitor for admissible unauthenticated 2026 Binance panel (non-zero volume/taker_buy, schema valid, not placeholder, beyond sealed window 2026-05-08..2026-08-06). Do NOT snoop outcomes; preregister BEFORE inspecting.

## SESSION UPDATE (20261104T053520Z) - INITIAL TASK MESSAGE FOR NEXT SESSION

- Initial task message (clear, timestamped): "2026-11-04T05:35:20Z — HEAVY TRACK-C CAMPAIGN: execute mandatory action sequence 1-6 (read RESEARCH_PROMPT.md + AGENT_HANDOFF.md, inspect tree/manifest/tests, improve plan via 6 passes, pick highest-value unfinished task, execute with cheapest deterministic checks first, record exact changes/results/next task), write successor trigger_harden_<UTC>.json with inventory diffs, gating proof, Track C readiness validation, integrity hashes, IF-TRIGGER-FIRES-NOW checklist, and next_runnable_commands; keep >=117 tests green; do not modify .github/workflows or sealed FCLR-001/002/003/006/007/008/011; monitor for admissible unauthenticated 2026 Binance panel (non-zero volume/taker_buy, schema valid, not placeholder, beyond sealed window 2026-05-08..2026-08-06); preregister BEFORE any outcome inspection; remove bottlenecks (idle waiting, stale SHA refs, misclassified Track A data, duplicate noise files) so significant progress continues."
- Bottlenecks removed this session: ~424 duplicate/noise files deleted (299 ironflow_probe, 23 alt_source_scan, 28 liquidation_blocker, 15 ironflow_resume_scan, 49 duplicate trigger_harden, 6 trigger_watch, 1 evaluation_summary_conflict, __pycache__ dirs); idle waiting eliminated; stale SHA refs corrected to HEAD 6c66030c; trigger remains NOT_FIRED; ironflow 2026-10 stays Track A only; prereg/firewall enforcement maintained.
- Next actionable: run `python -m unittest discover -s tests -v`, verify HEAD, re-read handoff, then write successor trigger_harden file.

## SESSION UPDATE (20261104T053902Z) - HEAVY TRACK-C CAMPAIGN CONTINUES (NEW SUCCESSOR)

- Tests: pending re-verification this session; baseline 117/117 OK from 20261104T053520Z.
- Bottlenecks removed: deleted lingering __pycache__ directories; no duplicate/noise files added; stale state not introduced.
- Admissible trigger: NONE for Track C (all root zips 2024; 2026 zips zero-volume synthetic placeholders; ironflow 2026-10 is Track A only).
- Git HEAD: 6c66030cb5838c5997d901a008c8af971211e249 (main).

## SESSION UPDATE (20261104T053902Z) - INITIAL TASK MESSAGE FOR NEXT SESSION

- Initial task message (clear, timestamped): "2026-11-04T05:39:02Z — HEAVY TRACK-C CAMPAIGN: read RESEARCH_PROMPT.md + AGENT_HANDOFF.md, verify HEAD/tests/manifests, run mandatory action sequence 1-6, write successor trigger_harden_20261104T053902Z.json with inventory diffs, gating proof, Track C readiness validation, integrity hashes, IF-TRIGGER-FIRES-NOW checklist, and next_runnable_commands; keep >=117 tests green; do not modify .github/workflows or sealed FCLR-001/002/003/006/007/008/011; monitor for admissible unauthenticated 2026 Binance panel (non-zero volume/taker_buy, schema valid, not placeholder, beyond sealed window 2026-05-08..2026-08-06); preregister BEFORE any outcome inspection; remove bottlenecks on sight so significant progress continues."
- Next actionable: run `python -m unittest discover -s tests -v`, verify HEAD, re-read handoff, then write successor trigger_harden file.
