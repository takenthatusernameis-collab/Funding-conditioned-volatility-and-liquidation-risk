# TRACK A TRIGGER AUDIT (HEAVY) - 20261104T183900Z

Repo: Funding-conditioned-volatility-and-liquidation-risk
Git SHA (HEAD): ade33dd0
Branch: main
Handoff: FCLR-HANDOFF-20261104T183334Z
Mode: CAMPAIGN-DRIVEN | Enforcement: NO-SKIP | Priority: P0

## TRIGGER STATUS: NO NEW DATA - ON HOLD

### Ironflow probe (primary Track A source)
- Probe: research_state/ironflow_probe_20261104T183629Z.json
- Dataset: ironflow/hyperliquid-liquidations (Hyperliquid-only per firewall)
- data_through: 2026-10
- Tree ETag unchanged (304), cached_hits: 0
- Probed months: 2026-11, 2026-12, 2027-01, 2027-02 (events + fills)
- All probes: 404 CONFIRMED_ABSENT (HEAD confirmed)
- consecutive_absent: 3
- New files found: 0
- Resume trigger: NOT MET

### Alternative sources review
- Review: research_state/alt_source_deep_review_20261104T183735Z.md
- Conclusion: No admissible unauthenticated source with observed liquidation labels found that would satisfy preregistration/firewall requirements for Track A trigger. Track B remains NOT_SUPPORTED.

### Track A state (frozen)
- FCLR-010: COMPLETE_SEALED, FORECAST_GATE_PASSED (Brier rel -2.21%, CI excludes zero)
- Consolidated: research_state/track_a_fclr010_consolidated.md
- Prereq for resuming: ANY new files >=2026-11 in ironflow/hyperliquid-liquidations (events or fills). Must preregister before inspecting outcomes with frozen splits/hypothesis/metrics/stop rule. Only run via frozen FCLR-010 harness (scripts/fclr010_execute.py or scripts/fclr010_harness.py). No source merging, no widening scope.

### Resume conditions (concrete)
1. New parquet appears at data/events/YYYY-MM.parquet or data/fills/YYYY-MM.parquet with YYYY-MM >= 2026-11
2. On detection: HALT inspection, write fclr010_prereg_$(date -u +%Y%m%dT%H%M%SZ).json BEFORE examining outcomes
3. Prereg must include: frozen hypothesis, splits (FCLR-010 frozen), metrics, guardrails, stop rule
4. Execute only via frozen harness on existing sealed configuration
5. No re-tuning on new data; maintain Hyperliquid-only firewall

### Bottlenecks / hygiene
- Tests: 164/164 pass
- Working tree clean
- No new schedulers/controllers/status-only files
- Track C remains LOCKED (no modifications)
- __pycache__/pyc cleaned as needed

## VERDICT
NO NEW DATA - ON HOLD. Monitoring readiness maintained. No heavy work possible on Track A without trigger; cannot skip to other tracks. Follow resume conditions strictly.
