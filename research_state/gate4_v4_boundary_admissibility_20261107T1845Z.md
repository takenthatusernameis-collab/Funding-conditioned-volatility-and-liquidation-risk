# Gate 4 v4 Boundary/Admissibility Evidence Record

**Timestamp:** 2026-11-07T19:15:00Z
**Git SHA:** 1ddb7d6c57e2cf10ace9fb11b9ddda26a6bcb428
**Experiment:** GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D (v4 prereg frozen before outcomes)
**Prereg:** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md|json` (frozen_before_outcomes=true, manifest_sha256=3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c)

## Sealed confirmatory anchors (forbidden to overwrite/promote)
- **FCLR-002**: Panel 2024-01-01..2024-09-30; test 2024-07-23T00:00Z..2024-09-30T23:00Z (7d embargo), 2×30d blocks → NOT_MET for claim-worthy. Anchor recorded in AGENT_HANDOFF.md.
- **FCLR-003**: Panel 2024-01-01..2024-12-31; test 2024-10-02T00:00Z..2024-12-31T23:00Z (7d embargo), 3×30d blocks PASS for block count but forecast/confirmatory NOT_MET/CLOSED NEGATIVE. Anchor sha256: `a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2`
- **FCLR-013**: 2026-08-26..2026-09-30 test, 1×30d block NOT_MET. Anchor sha256: `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a`. Different calendar regime.
- **v3 Gate 4**: 2024-04..09 local cache lineage (preserved), not overwritten. Anchor oid in tests: `9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e`

## v4 slice analysis
- **Slice**: 2024-04-01..2024-09-30 (5 symbols: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT)
- **Identity**: FCLR-015 verified 3690/3690 MATCH vs Binance Vision (manifest_sha256 3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c)
- **Domain overlap**: 2024-04..09 falls within 2024 domain family used by FCLR-002/v3; test windows of v4 (starting 2024-05-15) overlap temporally with FCLR-002 test region and share same venue/data lineage.

## GO/NO-GO determination
- **Exploratory-only on 2024-04..09 slice:** **GO** - allowed after v4 prereg freeze with strict labeling `EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE`. Must use tmp/non-canonical outputs, leakage checks, no overwrite of sealed anchors.
- **Confirmatory on 2024-04..09 slice:** **NO-GO** - confounded with sealed anchor lineage (FCLR-002/v3). Not claim-worthy. No promotion/overlay eligibility.
- **Confirmatory on distinct boundary:** **CONDITIONAL** - requires separate v5 preregistered before outcomes on materially distinct admissible non-confounded boundary with explicit non-overlap proof vs FCLR-002/003/013/v3 test windows, ≥5 instruments, ≥3×30-day non-overlapping test blocks, clean leakage audit, pre-registered uncertainty.

## Evidence
- Prereg v4: `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md|json`
- FCLR-015 manifest: `research_state/fclr015_local_audit/fclr015_input_manifest_2024_04_09_20261107T180626Z.json`
- Handoff: `AGENT_HANDOFF.md` (sealed anchors, gates)
- Track A check: `python3 scripts/tracka_resume_check.py` passes (network:false, writes_real_research_state:false)

**Verdict:** P0-1 COMPLETE. Proceed to P0-2 bounded deterministic exploratory smoke only if labeled EXPLORATORY/NOT CONFIRMATORY/NOT PROMOTABLE with outputs isolated from sealed/canonical artifacts.
