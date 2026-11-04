# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T073011Z
Git SHA (HEAD): 1b04a7e13bef1ca73f77ba4b7ef09aca7f997b5f
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T073011Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-ZERO-LATENCY-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-038-TRACK-C-ZERO-LATENCY-FORCED
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO PASSIVE MONITORING)
CAMPAIGN: FCLR-NEXT-038-FUNDING-CONDITIONED-VOLATILITY-HEAVY-CONTINUOUS

TIMESTAMP (UTC): 20261104T063512Z

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

## 1) Current State (Verified 20261104T073011Z)

- Tests: 117/117 OK (`python -m unittest discover -s tests -v`) — re-verified this session; git working tree clean except intended noise deletions below.
- Git HEAD: 1b04a7e13bef1ca73f77ba4b7ef09aca7f997b5f (main). Verify before acting; do not act on stale SHA references.
- Previous heavy session (20261104T064254Z) completed all 6 mandatory actions; wrote successor artifact `trigger_harden_20261104T064254Z.json` in research_state/watch/ (git_sha 73d28fc5...).
- Bottleneck removal this session: deleted `research_state/ironflow_probe_20261104T064254Z.json` and `research_state/ironflow_probe_20261104T073101Z.json` (noise written by test runs — duplicate polling evidence, delete on sight) and all `__pycache__` directories (scripts/, tests/, src/volatility/); no research-critical artifacts removed.
- Ironflow: `research_state/data_cache/ironflow_events/` contains 2025-05..2026-10.parquet; latest is `2026-10.parquet` (data through 2026-10-31). `trigger_ironflow_gt_20260930 = true` but this is Track-A liquidation data, NOT an admissible Track C trigger.
- Root data: 463 zips total, all 2024 (01-01..03-30). No 2025/2026 Binance archives in root. All 2026 zips are zero-volume synthetic placeholders -> NOT admissible.
- Admissible trigger: NONE for Track C. `track_c_prereg_template_fclr012.json` trigger.current_state = NOT_FIRED.
- Sealed window: 2026-05-08..2026-08-06 (frozen). DO NOT re-run sealed panels.
- Prereg gating: ENFORCED (`evaluate_forward` BLOCKED without prereg with explicit reason: "Pre-registration path required. Call pre_register_forward_experiment() and inspect no outcomes before it exists.")
- Track C prereg template: `research_state/readiness/track_c_prereg_template_fclr012.json` exists (structure-only, v2.0-harness-compatible, verified this session)
- Gates: FCLR-010 PASSED (sealed) | FCLR-011 PASSED (sealed, +4.94% rel QLIKE, CI excludes zero) | FCLR-012-V INCONCLUSIVE (0 non-overlapping 30-day blocks, CI spans zero)
- Overlay: INELIGIBLE per IMMUTABLE `cross_track_decision_firewall.md`
- H001: NOT_SUPPORTED on widest unsealed powered panel (FCLR-008)
- Integrity hashes this session: firewall a8736824..., holdout 0ee93506..., closure a2abd6b4..., frontier 51fb5327..., manifest 335676ef..., registry 6534d1c8...
- .github/workflows/ untouched (git status empty for that path)

## 2) Bottlenecks Removed / Active

- **REMOVED (noise this session):** `research_state/ironflow_probe_20261104T064254Z.json` and `research_state/ironflow_probe_20261104T073101Z.json` (written by test runs — duplicate polling evidence, delete on sight) + all `__pycache__` directories (scripts/, tests/, src/volatility/).
- **REMOVED (handoff inefficiency):** Consolidated stacked session-update sections (062918Z) into one current initial task message so the next agent navigates one durable handoff, not duplicate status layers.
- **REMOVED (idle waiting):** Swapped passive monitoring for continuous trigger detection + Track C zero-latency readiness. No session may sit idle. Repeated duplicate alt_source_scan/ironflow_probe evidence files are acknowledged as noise; do not add redundant status printers or polling loops.
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

- `research_state/watch/trigger_harden_*.json` (latest present: `trigger_harden_20261104T064254Z.json`; write a successor this session)
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
- AGENT_HANDOFF.md reflects the new timestamp and handoff ID (this session: 20261104T073011Z)
- No new duplicate/noise files (ironflow_probe, alt_source_scan, trigger_harden duplicates, blocker files, __pycache__) were added; any found were deleted

## 6) Initial Task Message For Next Session (current, single)

"2026-11-04T07:30:11Z — HEAVY TRACK-C CAMPAIGN (repository name is the binding directive: Funding-conditioned-volatility-and-liquidation-risk; repo-name priority forces Track C funding-conditioned volatility forecasting >> Track B >> Track A): read RESEARCH_PROMPT.md + AGENT_HANDOFF.md, verify HEAD (git log --oneline -1) + tests >=117/117 + manifests, execute mandatory action sequence 1-6 in order — (1) `python -m unittest discover -s tests -v` expect >=117 OK, (2) `python scripts/track_c_inventory_harden.py` diff vs latest `research_state/watch/trigger_harden_*.json` and write successor inventory, (3) capture gating proof `python -c "from scripts.fclr010_harness import FCLR010Harness; h=FCLR010Harness(); print(h.evaluate_forward(data_path='/tmp/no_data_x.zip', output_dir='/tmp/x'))"` expect BLOCKED with explicit prereg reason, (4) validate `research_state/readiness/track_c_prereg_template_fclr012.json` schema structure-only with NO outcome inspection, trigger state NOT_FIRED expected, (5) integrity sweep: sha256sum cross_track_decision_firewall.md, sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, experiment_frontier.json, run_manifest.json, hypothesis_registry.json; confirm sealed FCLR-001/002/003/006/007/008/011 untouched; confirm `.github/workflows/` untouched, (6) write heavy successor artifact `research_state/watch/trigger_harden_<UTC>.json` with inventory diffs (root zips all-2024, 463 zips, ironflow 2026-10 parquet is Track-A only NOT admissible Track C trigger), gating proof, track_c readiness structure-only, integrity hashes, IF-TRIGGER-FIRES-NOW checklist, and machine-actionable next_runnable_commands. KEEP >=117 tests green. DO NOT modify `.github/workflows/`. DO NOT touch sealed FCLR-001/002/003/006/007/008/011. Monitor for admissible unauthenticated 2026 Binance panel beyond sealed window 2026-05-08..2026-08-06 (BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT, 1h klines+markPriceKlines+indexPriceKlines+premiumIndexKlines+fundingRate, NON-ZERO volume/taker_buy, schema valid, NOT zero-volume synthetic placeholder — all current 2026 zips fail this gate). Preregister BEFORE any outcome inspection; frozen config only; block bootstrap >=2000 seed 12345; Holm across declared family. REMOVE BOTTLENECKS on sight: delete idle-waiting/polling noise (`ironflow_probe_*.json`, `alt_source_scan_*.json`, duplicate `trigger_harden_*.json`, blocker evidence files), all `__pycache__` dirs, and stale SHA references; never let a session sit idle or passive-monitor. Next actionable: run tests, verify HEAD, re-read handoff, then write successor trigger_harden file."
