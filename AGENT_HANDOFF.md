# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T070842Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION REOPEN = MAINTAIN-ONLY (structural blocker CONFIRMED with evidence — all alt sources NO-GO, ironflow forward 404 through 2027-02, blocker_evidence_20261103T070800Z.md complete) | VOLATILITY H001 = STREAM_B_HEAVY (UNBLOCKED heavy execution on frozen splits — extend features, ablations, block-bootstrap CIs; do NOT re-run sealed panels FCLR-001..008)
**CAMPAIGN:** STREAM_B_HEAVY_FEATURE_EXTENSION-001 — extend Track B volatility features (funding percentiles/zscore trailing-only, RV ratios 6h/24h/7d, price-dislocation MA/EMA deviation), train-only normalized models, block-bootstrap CIs, full ablations on frozen splits. Heavy work mandatory; Track A monitor-only keep-alive.

## SESSION GOAL
Pivot from idle Track A wait to heavy Stream B Track B work. Track A: <1 min `monitor --quick` keep-alive only (resume trigger: ironflow 2026-11+ returns 200 OR new rubric-GO source). Every remaining minute of this session: Stream B feature extension + ablation execution on frozen splits. No polling loops, no re-probing dead routes, no re-running sealed confirmatory panels.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY, IN THIS ORDER)

```bash
# PHASE 1: STATE VERIFY (< 2 min) — bounded, never idle-wait
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -3   # must stay 111+/111 PASS

# PHASE 2: HEAVY — STREAM_B_FEATURE_EXTENSION (this session's main work)
# Track B volatility on frozen splits — do NOT re-run sealed FCLR-001..008 panels:
#   - funding percentiles / zscore (trailing-only)
#   - RV ratios 6h / 24h / 7d
#   - price-dislocation MA / EMA deviation features
#   - train-only normalized models
#   - block-bootstrap CIs
#   - full ablations
# Add tests for any new volatility modules; keep all green.

# PHASE 3: TRACK A KEEP-ALIVE (monitor only)
# monitor_ironflow_liquidations.py --quick  (resume trigger met only if 2026-11+ returns 200)

# PHASE 4: RECORD
#   Update AGENT_HANDOFF.md + research_state/experiment_frontier.json with successor's exact next task
#   Keep tests green (111+)
```

## VERIFIED TRUTH (20261103T070842Z)

- **Track A (observed liquidations):** BLOCKED_ON_DATA (STRUCTURAL, evidence-backed). Ironflow cached through 2026-10 intact (18 month pairs, content_hash_complete=True, baseline_drift=False). Forward months 2026-11,12,2027-01,02 all 404; consec_absent=3; resume_trigger_met=false. FCLR-010 (Hyperliquid census 2025-11..2026-10) COMPLETE, gate PASSED, sealed. Alt sources: 15+ REVIEW_REQUIRED deep-reviewed, 0 GO. Blocker evidence complete: research_state/blocker_evidence_20261103T070800Z.md + research_state/alt_source_deep_review_20261103T070705Z.md. No admissible unauthenticated liquidation source found. Sole reopen path = NEW admissible unauthenticated source passing FULL rubric (>=5 symbols or equivalent, >=1 complete month OR >=3 non-overlapping 30-day blocks, schema mappable to FCLR-010 events/fills, unauthenticated, no keys/signed/requester-pays, license OK, completeness documented).
- **Track B (funding-conditioned volatility):** H001 INCONCLUSIVE on decisive unsealed panel FCLR-008 (2026-01-01..2026-08-06, 5 symbols, 218 days, 7 blocks, n=10785; C2 vs B1 +4.30% rel QLIKE, CI [-0.029938, 0.000524] crosses zero). All confirmatory panels exhausted (FCLR-001/002/003/006/007/008). Overlay INELIGIBLE. Stream B heavy feature-extension work is UNBLOCKED on frozen splits (not a sealed-panel re-run). Do NOT re-run sealed panels. Tests: 111/111 PASS. Keep green.

## BOTTLENECKS ELIMINATED NOW

1. **Idle-wait on Track A removed** — Session starts with <1 min `monitor --quick` / `--verify`; then 100% Stream B heavy work. No polling loops, no repeated re-probes of dead routes (Binance 404/451, Bybit 404, OKX 403/404, Deribit connect-fail, GitHub 401, CCD, paywalled Tardis/CryptoHFT).
2. **Shallow source review removed** — All REVIEW_REQUIRED alt sources deep-tested with full rubric evidence; blocker evidence written. No "REVIEW_REQUIRED" left unevaluated.
3. **Track B sealed-panel re-run removed** — H001 INCONCLUSIVE; all confirmatory panels exhausted. No threshold-shopping, no relaxing the >=2% floor or CI criterion, no relabeling exploratory as confirmatory. Stream B feature work proceeds on frozen splits instead.
4. **Unverifiable "GO" removed** — A source is GO only after full rubric evidence is written; HTTP 200 / green CI / model convergence is NOT acceptance.

## FOCUS CAMPAIGN: STREAM_B_HEAVY_FEATURE_EXTENSION-001 (NON-OPTIONAL, HEAVY)

Objective: extend Track B volatility feature pipeline on frozen splits — funding percentiles/zscore (trailing-only), RV ratios 6h/24h/7d, price-dislocation MA/EMA deviation, train-only normalized models, block-bootstrap CIs, full ablations. This is heavy engineering + evaluation work; it does NOT re-open sealed confirmatory panels.

Acceptance:
- New volatility modules implemented + tested (fixture-based, offline where possible)
- Block-bootstrap CIs computed on ablations
- `python -m unittest discover -s tests -v` passes (111+)
- AGENT_HANDOFF.md + experiment_frontier.json updated with successor's exact next task

Resume triggers (Track A):
- Ironflow: GET https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/YYYY-MM.parquet and /data/fills/YYYY-MM.parquet return 200 for YYYY-MM >= 2026-11 (via `scripts/monitor_ironflow_liquidations.py --quick` / `--decision` / `--scan`).
- OR new source passes GO: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010 (Hyperliquid-only for Track A).

## MANDATORY DELIVERABLES THIS SESSION

- [ ] `python -m unittest discover -s tests -v` passes (111+); add tests for new volatility modules
- [ ] Stream B heavy feature-extension artifacts (new modules, ablations, block-bootstrap CIs) on frozen splits
- [ ] Track A keep-alive: `monitor_ironflow_liquidations.py --quick` evidence (< 1 min)
- [ ] Updated `research_state/experiment_frontier.json` and this `AGENT_HANDOFF.md` with successor's exact next task

## CRITICAL RULES

- Research only. No trading / paper / live / API orders. No credentials. Unauthenticated sources only.
- No .github/workflows changes (protected control plane).
- Track separation: modeled boundary breaches != observed liquidations. Never label a modeled proxy as observed.
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo, freeze protocol before holdout.
- Never re-run sealed/exhausted confirmatory panels (FCLR-001..008). Fresh experiment ID required for any new confirmatory cell.
- Heavy work always. If Track A blocked, full effort on Stream B heavy work. Never idle.
- Evidence-based. Timestamp everything. No placeholder "REVIEW_REQUIRED" without a dated artifact.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK

Continue STREAM_B_HEAVY_FEATURE_EXTENSION-001: extend Track B volatility features on frozen splits with block-bootstrap CIs and full ablations; keep tests green (111+). Maintain Track A `<1 min` `monitor --quick` keep-alive as the sole idle-wait. If ironflow 2026-11+ returns 200 OR a new rubric-GO source appears, pre-register BEFORE outcome inspection and run the frozen Track A harness.
