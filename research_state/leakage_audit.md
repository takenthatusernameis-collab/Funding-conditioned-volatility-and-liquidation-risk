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