# Liquidation Source Campaign (Track A) — Irrefutable Structural Block

Updated: 2026-10-30T22:05:00Z

## Objective
Find admissible free historical liquidation/force-order data for perpetuals with defensible provenance and adequate coverage to test Track A.

## Sources tested (unauthenticated only)
- Binance public data archive (binance/binance-public-data): searched for liquidationSnapshot, forceOrders, liquidation history paths. No accessible unauthenticated files found via repo paths/rglob in local cache and common public archive patterns returned 404/451 in prior probes (recorded in research_state/binance_source_probe.md).
- Public unauthenticated exchange APIs: not used (require auth or live-only; cannot reconstruct historical point-in-time labels).
- Public GitHub/Zenodo/HuggingFace/institutional archives: searched for liquidation event datasets; none found with unauthenticated downloadable historical liquidation labels matching required scope.
- Local repo caches: scanned for *liquidat*, *forceOrder*, *liquidationSnapshot* — no admissible datasets found.

## Conclusion
Track A (observed liquidation labels): **STRUCTURALLY BLOCKED**. No admissible free source with defensible historical liquidation labels was identified in this environment. No fabricated labels created. Track separation enforced (Track B only).

## Next materially different route (if exists)
None apparent under constraints (no credentials, no payment, no manual download). Any future attempt must satisfy same constraints or be explicitly rejected.
