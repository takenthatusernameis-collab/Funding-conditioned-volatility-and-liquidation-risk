# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T16:48:00Z
HEAD: fb7b0da1 (main) — working tree clean
REPO: Funding-conditioned-volatility-and-liquidation-risk
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: PROGRAM CLOSED NEGATIVE — CONFIRMED CLOSEOUT. H001 NOT_SUPPORTED ON ALL CONFIRMATORY PATHS. NO FURTHER CONFIRMATORY WORK FEASIBLE ON CURRENT ADMISSIBLE DATA.

## CONFIRMED CLOSEOUT (FINAL)

### Ground truth (decisive)
- **FCLR-003 (2024-10-02..2024-12-31, powered):** SEALED NEGATIVE. C2 vs B1: +0.015205 QLIKE (worse), -3.78% rel, 95% CI [-0.020240, 0.056734] crosses 0. 91 days = 3 blocks, 5 instruments, n=10796. **FCLR-H001: NOT_SUPPORTED.** Risk-overlay INELIGIBLE. (research_state/evaluation_summary_FCLR003.md)
- **FCLR-006 (2026-05-23..2026-08-06, unsealed confirmation):** COMPLETE NEGATIVE; byte-identical reproduction confirmed (only Generated timestamp differs). C2 vs B1: +0.354989 QLIKE (worse), CI [0.168263, 0.591948] entirely positive, -67.32% rel. n=8987 paired, 5 instruments. Test window 76 days = 2 blocks < 3 required → block criterion NOT_MET; forecast gate NOT_MET. **FCLR-H001: NOT_SUPPORTED.** (research_state/evaluation_summary_FCLR006.md, research_state/reporting_errata_FCLR006.md)
- **FCLR-001/002/005:** Sealed/inconclusive as recorded; no path to confirmation.
- **H002 (Funding-correction replication, Shek):** PARTIAL_REPLICATION final. SSRN HTTP 403 blocks full methodology (structural impossibility). 88 events Jan-Mar 2024, median 8.0h. Do not promote. (research_state/h002_replication_blocker.md)
- **H003 (Modeled boundary-breach):** INCONCLUSIVE on both panels; no incremental skill.
- **Track A (observed liquidations, FCLR-H004):** BLOCKED/exhausted after >=2 materially distinct source families (Binance liquidationSnapshot 404, fapi forceOrders 451; Bybit trades non-census; HuggingFace 2026-only with undercounting, no 2024 coverage; Zenodo/GitHub no admissible census). No confirmatory-feasible window. (research_state/liquidation_sources_enumeration.md, research_state/binance_source_probe.md)

### Reporting erratum
- The FCLR-006 summary displays `excludes zero: no`, but the reported interval `[0.168263, 0.591948]` is entirely positive and therefore excludes zero. See `research_state/reporting_errata_FCLR006.md`. This corrects only the reporting flag; the two-block shortfall remains and the formal gate remains NOT_MET.

### Verification (2026-10-30T16:48:00Z)
- Tests: `python -m unittest discover -s tests -v` → **14 tests OK**
- Byte-identical repro: `FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py` → only "Generated" timestamp differs; results identical to stored summary.
- Closure audit: `research_state/final_record_closure_audit.md` enumerates all experiments/hypotheses/tracks with verdicts, evidence paths, seal status; no sealed re-runs; permissions verified readable.

## NEXT AGENT DIRECTIVE (MANDATORY)
**PROGRAM CLOSED.** H001 (funding-conditioned volatility improvement) is **NOT_SUPPORTED** across both the powered 2024-12 panel (FCLR-003) and unsealed 2026 confirmation (FCLR-006). Overlay INELIGIBLE. Track A BLOCKED. H002 PARTIAL (structural). H003 INCONCLUSIVE.

**Do NOT** re-run sealed experiments (FCLR-001/002/003/005/006). **Do NOT** threshold-shop or tune on sealed holds. **Do NOT** violate seals.

**Only possible new route:** A new unauthenticated admissible liquidation/price source with confirmatory-feasible coverage (≥5 symbols, ≥3 non-overlapping 30-day blocks). If such a source appears, **pre-register a new experiment ID BEFORE examining outcomes** per RESEARCH_PROMPT.md §16, then execute the frozen protocol.

**If no such source exists (as is the case now):** Report the program as closed with H001 NOT_SUPPORTED and no further confirmatory path on current admissible data. Preserve negative results. Do heavy working only to close records honestly if anything remains; otherwise stop cleanly.

### Hard constraints
- No seal violations; no tuning on sealed holds; no threshold shopping.
- No `.github/workflows/*` changes without explicit maintainer authorization.
- No fabrication; distinguish modeled (H003) vs observed (H004).
- Preserve negative results; H001_NOT_SUPPORTED is correct.
- No further confirmatory experiment feasible without NEW admissible data source.

### Verification commands
```bash
python -m unittest discover -s tests -v
FCLR_EXPERIMENT=FCLR-006 python scripts/run_evaluation.py
git log --oneline -2
```

---

## NEXT SESSION INITIAL TASK (2026-10-30T16:48:00Z) — DURABLE SINGLE HANDOFF

**Initial task (timestamped):** 2026-10-30T16:48:00Z — **NO NEW CONFIRMATORY WORK.** Program is closed. Perform only maintenance/closure hygiene if anything is obviously broken (tests failing, unreadable artifacts, permissions regressed). Do not re-open experiments, do not threshold-shop, do not search for new confirmatory windows. If all verification passes and records are intact (see `research_state/final_record_closure_audit.md`), report closure and stop cleanly with no further actions. Any proposal of a new route requires concrete evidence of a new unauthenticated admissible liquidation/price source meeting ≥5 symbols and ≥3 non-overlapping 30-day blocks AND pre-registration of a new experiment ID before examining outcomes per RESEARCH_PROMPT.md §16.
