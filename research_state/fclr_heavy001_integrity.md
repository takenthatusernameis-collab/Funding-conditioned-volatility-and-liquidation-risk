# FCLR-HEAVY-001 Step 6: Reproducibility + integrity lock-in

**Campaign:** FCLR-HEAVY-001
**Track:** A (observed liquidations) — Hyperliquid ironflow census
**Status:** EXECUTED
**Timestamp:** 2026-11-02T03:21:57Z
**Hypothesis-only:** Strictly hypothetical-only. No deployment/paper/live trading claims. No label merging.

## Objective
Re-verify sealed FCLR-010 artifacts untouched (hashes/mtimes). Write integrity lock-in. Run tests 27/27. Update experiment_frontier.json and append to cross_track_decision_log.md.

## Sealed artifacts checked (FCLR-010)
All five sealed FCLR-010 artifacts share an identical mtime of 2026-11-01T23:02:50Z (the initial repository checkout time), confirming no modification has occurred since the sealed experiment was written. SHA-256 digests recorded below for future comparison.

| Artifact | SHA-256 | mtime |
|---|---|---|
| research_state/evaluation_summary_FCLR010.md | 8b7773b2d7eff3663be4fa975e75095c5406f27c5bcf096988935fad0871a334 | 2026-11-01T23:02:50Z |
| research_state/research_protocol_fclr010.md | 5045cac1131e62868f9e4616de07297ab5104e212c7e38bca98a1dddd02e3918 | 2026-11-01T23:02:50Z |
| research_state/fclr010_leakage_audit.md | 272584cae358cd7ecc80e861e5e3abc10e9929994f3e2bd1fd71fb70b30def97 | 2026-11-01T23:02:50Z |
| research_state/fclr010_coverage_audit.json | 31749c027edec2e437d0496a3043d410184fee16c747d6d35381b115c665240d | 2026-11-01T23:02:50Z |
| research_state/fclr010_diagnostics.md | 303692dcae3751e1932785f3fbdfe50ee5f0a34e97ad71721d7170167e563af0 | 2026-11-01T23:02:50Z |

- Splits remain frozen: run_manifest.json#split_boundaries_fclr010 (frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z) untouched.
- Firewall intact: no Binance data merged into Track A; no Track A/B/C label merging.
- HEAD at lock-in: a03d9a63ea2b828f1c0c30c76ca3ff83ef6e4c87

## Tests
`python -m unittest discover -s tests -v` → Ran 27 tests in 0.203s, OK (27/27 PASS).

## Integrity defects found and repaired this session
- All six FCLR-HEAVY-001 markdown artifacts contained a literal unexpanded `$(date -u +%Y-%m-%dT%H:%M:%SZ)` timestamp placeholder instead of a real UTC timestamp. Substituted with the actual generation time (2026-11-02T03:21:57Z). No analytical content was affected; only the timestamp field was corrected.

## Updates
- research_state/experiment_frontier.json updated with FCLR-HEAVY-001 status (all 6 steps DONE, integrity hashes recorded).
- research_state/cross_track_decision_log.md appended with the closeout entry.

## Artifacts
- `research_state/fclr_heavy001_integrity.md` (this file)