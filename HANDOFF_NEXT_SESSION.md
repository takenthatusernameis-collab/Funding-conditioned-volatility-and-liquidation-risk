# HANDOFF: Next Agentic Work Session
**Timestamp**: 2026-11-22T21:05:29Z
**Repository**: Funding-conditioned-volatility-and-liquidation-risk
**Priority**: HIGH — Campaign complete; data frontier exhausted; Gate 4 pilot is the only viable heavy work

---

## 📊 CURRENT STATE (Verified 2026-11-22)

### FCLR-NEXT-CAMPAIGN-20261113T063000Z — **COMPLETE (GATE PASS)**
All three cells have **frozen pre-registrations** + **terminal evaluation artifacts**:

| Cell | Verdict | Primary Failure |
|------|---------|-----------------|
| **LIQ-010-CONFIRM** | `NOT_REPLICATED` | Materiality 0.50% < 2% floor; LOIO 0/17; placebo p95 52.5% > true 0.50% |
| **EXP-ROBUST-REDO** | `FRAGILE` | LOIO 4/8 (need ≥6); placebo null p95 21.89% > true 19.04% |
| **FWD-VOL-2025-CROSS** | `NOT_REPLICATED` | Materiality 0.29% < 2%; CI includes zero; LOIO 0/5; placebo failed |

**Gate script**: `python3 scripts/fclr_next_campaign_gate.py` → **PASS** (all checks green)

### DATA FRONTIER — **BLOCKED_ON_DESIGN** (Confirmed by `scripts/next_campaign_status.py`)
- **Binance 5-symbol**: No contiguous run ≥127d; no disjoint 30d block feasible
- **Mark+funding-only (B0/B1/C1)**: Only 1 mutually non-overlapping month (2025-01); need ≥3
- **Hyperliquid bulk (candles+funding+OI+liq)**: Max untouched span 24d; need ≥127d
- **Hyperliquid extended (17 coins, 18 event months)**: All 2025-11..2026-10 tested; no untouched region
- **Conclusion**: **No feasible 3-block confirmatory design exists in ANY domain with current cached data**

---

## 🎯 NEXT FOCUS CAMPAIGN (Mandatory — No Avoidance)

### **Gate 4 Funding Ablations (Multi-Split Pilot)** — *Pre-registered, Exploratory, Leakage-Resistant*
**Script**: `scripts/run_funding_ablations.py`
**Pre-registration**: `research_state/pre_registration_gate4_funding_multisplit_20261107.md`
**Status**: Ready to run — **no confirmatory intent required** (exploratory/pilot mode)

**Why this is the only viable heavy work**:
1. Uses **existing cached Binance data** (2024-04..09 v3_30d walk-forward design — 4×30-day blocks, purge/embargo 7d)
2. **Train-only normalization**, causal funding features (last-known at/before hour, trailing stats past-only)
3. **Direct-variance OLS HAR** (Gate 3 form); A_rv_only regression-stable baseline
4. **Block bootstrap ΔQLIKE CIs** resampling whole UTC time blocks jointly across instruments
5. **Honest verdict**: PILOT / INCONCLUSIVE when data-sufficiency unmet (no confirmatory claims)
6. **Admissibility package** (FCLR-016 v5) available for dry-run validation before execution

**Required command** (v3_30d design, 5 symbols, exploratory):
```bash
python3 scripts/run_funding_ablations.py \
  --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT \
  --start 2024-04-01 --end 2024-09-30 \
  --horizon 24 \
  --split-design v3_30d \
  --out-suffix _v4_5sym \
  --experiment-id FCLR-GATE4-FUNDING-V4-5SYM-$(date -u +%Y%m%dT%H%M%SZ)
```

**Expected artifacts** (in `research_state/`):
- `evaluation_summary_FCLR-GATE4-FUNDING-V4-5SYM-<UTC>.json` + `.md`
- `run_manifest_funding_v4_exploratory_<UTC>.json`
- Leakage audit update (append-only)

**Success criteria**: Pipeline runs without data-load errors; produces per-split metrics + pooled ΔQLIKE CIs + data-sufficiency report; verdict = `PILOT` or `INCONCLUSIVE` (never `CONFIRMED`).

---

## 🚫 WHAT NOT TO DO (Guardrails)

| ❌ Forbidden | ✅ Required Alternative |
|--------------|------------------------|
| Claim confirmatory outcomes on unprovenanced 2025+ data | Run exploratory/pilot only; label artifacts honestly |
| Mutate sealed FCLR-010 / FCLR-011 / expansion artifacts | Write NEW evaluation artifacts with new timestamps |
| Lower LOIO/materiality/placebo bars | Keep pre-registered thresholds; report FRAGILE/INCONCLUSIVE honestly |
| Shop for thresholds post-hoc | Use frozen pre-registration; verdict rules fixed at freeze |
| Use live/network data | Cached local data only (`research_state/data_cache/`) |
| Expand 17-symbol ironflow universe with live funding | Disclose 17-symbol limit; do not pretend it's 199 |

---

## 🔧 VERIFICATION CHECKLIST (Run Before Starting Heavy Work)

```bash
# 1. Confirm campaign gate still passes
python3 scripts/fclr_next_campaign_gate.py

# 2. Confirm no feasible confirmatory design exists
python3 scripts/next_campaign_status.py | grep "CAMPAIGN STATUS"

# 3. Verify cached data for v3_30d design exists
ls research_state/data_cache/BTCUSDT_2024_04/markPriceKlines-*/BTCUSDT-1h-*.csv 2>/dev/null | head -1
ls research_state/data_cache/BTCUSDT_2024_04/BTCUSDT-fundingRate-*/BTCUSDT-fundingRate-*.csv 2>/dev/null | head -1

# 4. Dry-run admissibility package (should return ok:true, expect_go_refused:true for real blocked package)
python3 scripts/run_funding_ablations.py --check-admissibility-package \
  research_state/fclr016_v5_provenance_license_manifest_<LATEST>.json \
  research_state/fclr016_v5_completeness_leakage_audit_<LATEST>.json \
  research_state/fclr016_v5_terms_evidence_<LATEST>.json \
  research_state/fclr016_v5_prereg_draft_<LATEST>.json
```

---

## 📝 SESSION LOG TEMPLATE (Append to this file on completion)

```markdown
## Session: <ISO8601_UTC>
**Agent**: <model/variant>
**Task**: Gate 4 Funding Ablations v4 5-symbol exploratory run
**Command**: <exact command run>
**Exit code**: <0/1/2>
**Artifacts produced**: <list paths>
**Verdict**: <PILOT / INCONCLUSIVE / ERROR>
**Key metrics**: <ΔQLIKE point, CI, data-sufficiency shortfalls>
**Blockers**: <if any>
**Next action**: <what the following session MUST do>
```

---

## 🎯 BOTTOM LINE FOR NEXT AGENT

**The FCLR-NEXT campaign is DONE. All three hypotheses failed to replicate. No confirmatory campaign is feasible with current data. The ONLY viable heavy work is the Gate 4 funding ablations pilot. Run it. Produce artifacts. Report honestly. Do not attempt confirmatory claims. Do not mutate sealed artifacts. Do not lower bars.**

**If you cannot run the Gate 4 pilot (data missing, pipeline broken), your task is to FIX THE PIPELINE/DATA — not to invent a new confirmatory campaign that the data frontier explicitly blocks.**

---

*This handoff is durable. It survives session restarts. The next agent MUST acknowledge by reading this file and running the verification checklist before starting work.*