# Liquidation Source Campaign — Track A (Observed Liquidation Labels)

Updated: 2026-10-30T22:48:49Z
Status: STRUCTURALLY BLOCKED (no admissible free source found)

## Scope
Track A requires actual historical forced-liquidation records (liquidationSnapshot/forceOrders or equivalent observed events) with defensible provenance and adequate coverage. Track separation strictly enforced (Track B uses modeled boundary breaches only).

## Sources tested (unauthenticated, free)
### Binance public archive (github.com/binance/binance-public-data)
Probed paths (representative):
- `data/spot/daily/liquidationSnapshot/...` and related liquidation paths
- `data/futures/um/daily/liquidationSnapshot/` and `forceOrders/`
- Also checked common variants under futures archives

Method: directory/path probing / small HTTP requests to public GitHub/raw paths and archive structure inspection. Results: 404/451 observed in prior probes (documented in AGENT_HANDOFF and source-attempt evidence). No accessible historical liquidation snapshot/forceOrders datasets found with usable schema/coverage.

### Public exchange APIs
Reviewed public unauthenticated endpoints for liquidation data. Observations: live/public streams do not reconstruct history; endpoints requiring signed/auth requests are not admissible; no free historical liquidation archive with adequate coverage discovered.

### Other archives (GitHub/Zenodo/HF/institutional)
Searched for freely downloadable historical liquidation/event records without signup/API keys/payment/manual files. No admissible source with defensible provenance and sufficient coverage identified in this environment.

## Conclusion
Track A: no admissible observed liquidation dataset found; structurally blocked for this repo/environment. No fabricated labels created. All liquidation-risk analysis for this campaign proceeded via Track B (modeled boundary breaches) with strict separation.

## Evidence pointers
- AGENT_HANDOFF.md (DELAY-ELIMINATION OVERRIDE, Track A source status)
- research_state/data_source_registry.json (rejections documented)
- Prior probe logs/evidence in repo history
