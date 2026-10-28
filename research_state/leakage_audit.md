# Leakage Audit — FCLR-001

Date: 2026-10-26
Protocol: research_state/research_protocol.md v1.0 (FROZEN)
Scope: all feature, label, split, and transformation checks for the frozen FCLR-001 panel.

## Audit checklist

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Future-row perturbation cannot change earlier features or forecasts | PASS | tests/test_forecast_pipeline.py::test_target_no_future_leak_index; next_realized_variance uses only t+1..t+horizon and trailing_rv uses t-window..t |
| 2 | Target intervals never overlap across splits after purge/embargo | PASS | 7-calendar-day embargo at every split boundary; train ends 2024-02-24T08:00Z, val starts 2024-03-02T08:00Z (>=7d), val ends 2024-03-20T02:00Z, test starts 2024-03-27T02:00Z (>=7d). Secondary horizon 168h (7d) is fully covered by the embargo |
| 3 | Funding publication/settlement times and sign handled correctly | PASS | signed funding retained with sign; latest funding observation with availability timestamp <= t only; source cadence recorded |
| 4 | Mark/index alignment respects pre-registered timestamp tolerance | PASS (with documented limitation) | premium computed only when mark and index are contemporaneously aligned under the frozen tolerance; missing pairs remain missing, never zero-filled |
| 5 | Zero/missing funding and market observations remain missing, not invented | PASS | no forward-fill or zero-fill; missing features remain missing; paired comparisons use a common panel so coverage differences cannot masquerade as skill |
| 6 | Delisted contracts and symbol migrations retain correct identity and eligibility | PASS | universe built from archival listing/instrument metadata; per-instrument eligibility recorded; no use of present-day survivors as the historical universe |
| 7 | Duplicate, out-of-order, and missing pages detected | PASS | duplicate detection and idempotent merge in ingestion; gap/stale-row diagnostics recorded in run_manifest.json coverage_audit_multi.gaps |
| 8 | Censored correction events and incomplete liquidation labels not treated as completed negatives | PASS | funding-correction replication treats censored events per survival rules; direct liquidation labels are unavailable and are NOT used as absence labels |
| 9 | Interrupted grid resumes to exact expected terminal-key set | PASS | campaign_resume.py reconciles by stable key rather than appending duplicate rows |
| 10 | Multiplicity and sequential alpha-spending calculations deterministic | PASS | Holm correction declared in protocol; no sequential looks executed beyond FCLR-001, so alpha-spending not yet triggered |
| 11 | Independent result recomputation matches canonical metrics | PASS | metrics recorded in research_state/evaluation_summary.md; recomputation from stored input hashes reproduces headline QLIKE within declared tolerance |

## Known residual issues

- **Test window concentration.** The frozen test panel is a single ~4-day block
  (2024-03-27..2024-03-30). This is a statistical-power/coverage shortfall, not a
  leakage defect, but it limits the dependence-aware uncertainty estimate.
- **Mark/index premium coverage.** Not fully integrated where source data is
  missing; missingness is recorded, not imputed. C2 therefore uses a subset of the
  C1 panel where premium features are available.
- **No holdout reuse.** The sealed test partition was opened once for the frozen
  protocol and is permanently marked as inspected/development evidence. No
  subsequent selection, tuning, or re-evaluation has used it.

## Verdict

No unresolved leakage, timestamp, label, or transformation defect capable of
reversing the INCONCLUSIVE conclusion was found. The dominant limitation is
statistical power (single short test block), not look-ahead or data corruption.
## Leakage Audit — FCLR-002 (Extended 5-symbol panel)

Date: 2026-10-28
Protocol: research_state/research_protocol.md v1.0 §80-144 (FCLR-002 v1.0, FROZEN)
Scope: adversarial leakage re-audit on new 5-symbol panel prior to opening sealed holdout.

### Panel verification
- Universe (frozen): BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (Binance USDⓈ-M perpetuals)
- Coverage audit: `research_state/fclr002_coverage_audit.json` — 4392 common hourly timestamps 2024-04-01T00:00:00Z to 2024-09-30T23:00:00Z, contiguous window, >=5 instruments. Met.
- Cached data present under `research_state/data_cache/` for all 5 symbols across required months (2024-04 through 2024-09). Verified by directory listing.

### Split/embargo integrity
- Frozen splits (FCLR-002): train 2024-04-01T00:00:00Z..2024-06-08T23:00:00Z, val 2024-06-16T00:00:00Z..2024-07-15T23:00:00Z, test/holdout 2024-07-23T00:00:00Z..2024-09-30T23:00:00Z (7-calendar-day embargo). Boundaries match `research_state/run_manifest.json` and `research_state/run_manifest_FCLR002.json`.
- Embargo between partitions >=7d enforced by chronological separation with gaps (train ends 06-08T23:00Z, val starts 06-16T00:00Z = 7d gap; val ends 07-15T23:00Z, test starts 07-23T00:00Z = 7d gap). Purge/embargo at boundaries holds.
- No reuse of FCLR-001 sealed holdout (2024-03-27..2024-03-30). Development uses only common paired panel for FCLR-002 window.

### Timestamp alignment & feature computation
- Unit is one contract × closed UTC hourly timestamp; forecast at t uses only information available by t. Targets use t+1..t+h (mark-price close). No same-bar leakage.
- Funding: latest funding with calc_time/availability <= t only, sign retained; past-only 90d window for absolute-funding percentile (>=30 obs). No forward-fill/zero-fill.
- Premium/EMA: mark/index contemporaneously aligned under tolerance when available; missing not imputed to zero. Core RV features required; rows dropped if core RV missing as per pipeline.
- Common panel enforcement for paired comparisons prevents coverage differences masquerading as skill.

### Leakage checks
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| F2-1 | No future information in features/targets | PASS | Same construction as FCLR-001 (trailing only; next-RV from t+1 onward). |
| F2-2 | Split/embargo integrity on new boundaries | PASS | 7d embargo verified; chronological ordering holds. |
| F2-3 | Funding availability/sign correct | PASS | Funding loaded by month, latest with ts_f <= ts_t only; no leakage. |
| F2-4 | Alignment/missingness handled without fabrication | PASS | Missing premium/alignments remain missing; no zero-fill. |
| F2-5 | No holdout reuse / no contamination | PASS | FCLR-002 uses disjoint window (Apr 2024–Sep 2024); FCLR-001 holdout not accessed for selection/tuning. |
| F2-6 | Panel intersection correct | PASS | Common timestamps across all 5 symbols = 4392; paired comparisons use intersection. |

### Residual notes
- Mark/index premium coverage may be partial for some symbols/timestamps (missingness tracked, not imputed) — consistent with FCLR-001.
- Holdout (test) not yet "opened" for outcome inspection beyond pre-registered execution; this audit is recorded before opening per requirement.

### Verdict (FCLR-002)
No unresolved leakage/timestamp/label/transformation defect found. Proceed to FCLR-002 out-of-sample evaluation on frozen splits/panel per protocol. Holdout remains sealed until execution under frozen protocol with this audit on record.
