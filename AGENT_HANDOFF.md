# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261105T120604Z
Git SHA (HEAD, baseline): fe487722 (working tree modified by FCLR-NEXT-096 hardening; not committed)
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261105T120604Z | Priority: P0 - REPO-NAME PRIORITIZED + HEAVY WORK MANDATORY | Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Bottleneck-State: HARDENED-HEAVY-097-READY

## REPO-NAME PRIORITIZATION (INFERRED)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — **SEALED/LOCKED**. Forecast gate PASSED. DO NOT retune/re-run sealed cells/conflate.
- LIQUIDATION RISK component = Track A (FCLR-010) — **ONLY UNFINISHED HALF**. BLOCKED on admissible unauthenticated liquidation data (Hyperliquid-only). Track B = **NOT_SUPPORTED**.
- BOTH components are core to repo identity. While volatility is sealed, liquidation risk MUST be driven to completion via admissible data or hardened to resume instantly on trigger. NO SCOPE DRIFT TO SEALED TRACKS.

## CURRENT VERIFIED STATE (096, MEASURABLE DELTA DELIVERED)
- Tests: `python -m unittest discover tests` — **226 tests, OK** (>=208). MUST remain green.
- Track C: SEALED/LOCKED. Track B: NOT_SUPPORTED.
- Track A: ON-TRIGGER/MONITOR ONLY. Latest blocker: `research_state/liquidation_forward_validate_016_blocker_20261105T120604Z.md`. Latest sweep: `research_state/campaign_sweep_tracka_20261105T120604Z.md`. Frontier: `research_state/experiment_frontier.json` updated (`last_checked_utc=20261105T120604Z`, `track_a_blocked=true`, `artifact_churn_096`).
- Artifact churn (096, counted): root `research_state/*.md+*.json` = **157** (155 baseline + 2 required evidence artifacts: sweep+016 blocker). Ironflow probes = **2** (canonical digest + 1 live). No new recurring timestamped probe/scan families. Canonical alt outputs only.
- Watch consolidation (096, generator-compatible, provenance preserved): `research_state/watch/trigger_harden_20261104T*` live **28→1** (`trigger_harden_20261104T113550Z.json`, 2156 bytes). **27 archived** to `research_state/watch/archive/` with per-file bytes/sha256/excerpt in `research_state/watch/archive/trigger_harden_20261104T_096_archive.json` (archived_total_bytes 139350). Non-recursive generator globs in `scripts/write_trigger_harden_successor.py`/`scripts/track_c_inventory_harden.py` still resolve previous snapshot to kept live file (proved). `zero-safe-removable` blocker removed by tested-compatible consolidation.
- Rubric hardening (096, additive fail-closed, strict-manifest opt-in): `scripts/tracka_rubric.py` adds 096 checks for access/dataset provenance (`observed_access_provenance_missing`), label-definition/observed semantics (`label_definition_missing`), machine-verifiable month/block coverage evidence (`coverage_month_evidence_missing`, `block_count_evidence_insufficient`), claimed-symbols normalization proof completeness (`symbol_normalization_proof_incomplete`), raw-epoch normalization/unit evidence (`timestamp_unit_ambiguous`); `schema_mismatch` preserved. Adversarial suites 093+094+095+096 = **67 tests green** (`tests/test_tracka_adversarial_rubric_096.py` = 15).
- Safe side-effect isolation (096): `tests.test_monitor_ironflow.TestVerifyAndDriftSafety` = **3 tests green** proving `verify_state`/state-only drift tmp isolation does not create real `research_state` files and leaves real probe mtimes/root counts unchanged. `python scripts/tracka_resume_check.py` **PASS <5s**, JSON contract intact, no network, no real writes.
- Trigger probe (20261105T120604Z): `monitor --quick` **NO RESUME TRIGGER** (`data_through=2026-10`; probed 2026-11..2027-02; probe_diff no change; baseline drift intact; kaggle mirror unchanged/triggered false). `deep_review`/`hunt` refreshed canonical latest outputs; **no rubric-GO source**. No prereg created; no outcome inspection.
- **NO COASTING ALLOWED.** "Monitor only / no data / blocked" is NOT a valid session outcome unless accompanied by measurable new bottleneck reduction, stricter tests, reduced churn, or irrefutable new evidence.

## SINGLE INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (COPY/PASTE VERBATIM)
```text
TASK ID: FCLR-NEXT-097-TRACK-A-NO-COAST-STRICT-MANIFEST-DEFAULTS-RESUME-GATE-COVERAGE
PRIORITY: P0 - REPO-NAME PRIORITIZED (Volatility SEALED/LOCKED; Liquidation Risk = ONLY ACTIVE OBJECTIVE)
TIMESTAMP (UTC): 20261105T120604Z
CAMPAIGN: TRACK A LIQUIDATION RISK - IMPOSSIBLE-TO-COAST WHILE BLOCKED. MEASURABLE DELTA REQUIRED. ZERO CHURN. INSTANT IRREFUTABLE RESUME.
ENFORCEMENT: ALL STEPS MANDATORY. SESSION IS A FAILURE IF IT ONLY REPEATS PROBES/REPORTS WITHOUT NEW HARDENING DELTA. PREREGISTER BEFORE INSPECTING OUTCOMES IF TRIGGERED. NO IDLE TURNS. NO "MONITOR ONLY" STATUS-ONLY OUTPUT. NO NEW TIMESTAMPED PROBE/SWEEP/SCAN FAMILIES. NO SCHEDULERS/POLLERS/STATUS FILES/REPEATED WRAPPERS/AGENT-CONTROLLERS. NO WORKFLOW CHANGES.

OBJECTIVE (INFERRED): Complete liquidation-risk half of "Funding-conditioned-volatility-and-liquidation-risk". Data blocked (Hyperliquid data_through 2026-10; 2026-11.. absent). While blocked produce measurable hardening delta against 096 baseline (root md+json 157, probes 2, tests 226, rubric adversarial 67, resume PASS <5s, watch 20261104T live 1+archive 27): (A) keep root md+json <=159 (only required evidence; count explicitly) and ironflow probes == 2; add no new recurring timestamped families, (B) convert 096 opt-in rubric flags to a **strict full-manifest default path** (new `strict_tracka_manifest`/equivalent mode that fail-closes on missing provenance/label/block-month evidence/raw-epoch unit evidence by default for GO-shaped observed Hyperliquid claims) while preserving backward compatibility for existing 093-096 minimal fixtures via explicit `minimal_fixture_compat`/non-strict path; add tests proving both modes, (C) extend `scripts/tracka_resume_check.py` to validate strict-manifest mode, assert rubric rejects candidates that only satisfy minimal fields but lack machine-verifiable provenance/coverage evidence, and keep PASS <5s/no-network/no-real-writes (machine-readable), (D) add monitor tests proving `--quick`/`--verify` code paths used for state-only decisions do not call network in the cached/state-only branches when tree unchanged or when forced to state-only in tmp isolation (mock/patch network fetch; assert not called), and prove real `research_state` unchanged, (E) audit and reduce remaining non-20261104T `trigger_harden_*` live residue in `research_state/watch/` only via SAFE generator-compatible consolidation with provenance+tests (do not break generators); if unsafe, provide tested incompatibility proof and a compensating measurable hardening delta with exact numbers, (F) re-run exhaustive trigger probes and record irrefutable evidence in one canonical blocker/update. Never stop for "no data". Do not repeat 096 work unless extending it.

CONSTRAINTS: No credentials/manual files/.github/workflows changes. Leakage-safe, preregister-before-outcomes. Track C/B locked/unsupported. Raw data/caches out of git. Clean-clone reproducible. Hyperliquid-only for Track A. Never conflate observed/modeled liquidations. No threshold-shopping. No scope drift. Canonical outputs only (`ironflow_probe_digest_latest.json` + 1 live probe; `alt_source_scan_latest.json`; `alt_source_deep_review_latest.md`). If triggered, freeze prereg before reading outcomes.

MANDATORY EXECUTION (ALL REQUIRED; PRODUCE CONCRETE METRICS):
1) ENTRY VERIFY + EVIDENCE: `python -m unittest discover tests` (>=226 green). Run `monitor --quick`, `deep_review`, `hunt`, `python scripts/tracka_resume_check.py`. Record exact root md+json, ironflow probes, tests, resume timing. If NO NEW DATA, continue immediately to hardening.
2) STRICT-MANIFEST DEFAULTS (MEASURABLE): Implement strict full-manifest rubric default path + compat path with tests. Prove a candidate that was "GO-shaped" only by minimal fields is NO-GO in strict mode unless machine-verifiable provenance/label/coverage/block evidence present. Update resume script and keep <5s.
3) NETWORK-ISOLATION PROOF FOR MONITOR STATE-ONLY PATHS: Add deterministic tests (tmp dirs, mocks/patches) proving state-only/cached verify paths do not perform network calls and do not mutate real `research_state`.
4) SAFE WATCH RESIDUE CONSOLIDATION (OR TESTED INCOMPATIBILITY): Inventory all `trigger_harden_*` in watch; consolidate only safely with generator compatibility + archive provenance + tests. Report exact before/after counts/bytes.
5) EVIDENCE, FRONTIER, HANDOFF (MANDATORY): Write `research_state/campaign_sweep_tracka_$(date -u +%Y%m%dT%H%M%SZ).md` and `research_state/liquidation_forward_validate_017_blocker_$(date -u +%Y%m%dT%H%M%SZ).md` with full before/after metrics, strict-mode/compat proof, network-isolation proof, watch consolidation/incompatibility proof, probe evidence, and concrete resume instructions. Update `research_state/experiment_frontier.json` (last_checked now, track_a_blocked true, pointer to new blocker, artifact_churn_097 metrics). Update `AGENT_HANDOFF.md` with a NEW stricter timestamped task (FCLR-NEXT-098) that cannot be satisfied by status reporting and names exact uncovered gaps.

RESUME CONDITION (only): ironflow `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` for month>=2026-11 returns HTTP 200 unauthenticated OR admissible unauthenticated Hyperliquid source passes strict GO rubric. Hyperliquid-only. PREREGISTER BEFORE INSPECTING OUTCOMES.

STOP RULE: Complete ALL steps + ALL artifacts with concrete metrics. Track C locked. Track B unsupported. No conflation. No schedulers/pollers/status-only/repeated wrappers/agent-controllers/workflow changes. No new recurring probe/scan timestamped families. Any "blocked/no data" claim without measurable hardening delta is noncompliant. Leave state STRICTER than found.
```

## VERIFICATION COMMANDS (RUN ON ENTRY)
- `python -m unittest discover tests` (must be >=226, green)
- `python scripts/tracka_resume_check.py` (must print JSON with `"pass": true`, <5s)
- `python scripts/monitor_ironflow_liquidations.py --quick`
- `python scripts/deep_review_alt_sources.py`
- `python scripts/hunt_alternative_liquidation_sources.py`
- `python scripts/fclr010_harness.py` (frozen config, offline)

## NEXT TASK (TIMESTAMPED)
20261105T120604Z: Execute FCLR-NEXT-097 as above. Volatility (Track C) SEALED/LOCKED. Liquidation Risk (Track A) = ONLY ACTIVE OBJECTIVE. 096 delivered measurable delta: 226 tests green (+18); rubric adversarial 67 (+15 strict-manifest 096 cases); `tracka_rubric.py` additive fail-closed provenance/label/month-block/symbol-proof/raw-epoch checks; monitor `TestVerifyAndDriftSafety` (+3) green; resume script PASS <5s/no-network/no-real-writes; watch `trigger_harden_20261104T*` live consolidated 28→1 with generator-compatible kept snapshot + archive provenance (27 files, sha256/excerpt); root md+json 157 (+2 required evidence), probes 2, no new recurring families. Trigger NO DATA. PREREG BEFORE OUTCOMES if triggered. 097 must add strict-manifest defaults+compat proof, monitor network-isolation proofs for state-only paths, and safe consolidation/audit of remaining watch residue with concrete metrics.
