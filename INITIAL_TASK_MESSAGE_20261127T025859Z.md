# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**Generated (UTC):** 2026-11-27T02:58:59Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority focus (repo-name driven):** Funding-conditioned next-24h volatility forecasting

---

## EXECUTE IMMEDIATELY

**Campaign:** `FCLR-LIVE-ARCHIVE-07-20261126T153244Z`
**Status:** `READY_EXECUTE` (rank-0 in `experiment_frontier.json`)
**Gate:** GREEN & ARMED — no setup or gate-repair required

### Primary Estimand (repo-name priority)
**Next-24h mean log-realized-variance QLIKE, C2 versus B1**
- Cohort: 2024-04-01 through 2026-10-31 UTC (disjoint from 2021-2024 campaigns 01-06)
- Symbols: `BNBUSDT`, `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`
- Support: **mark-price common support `S`** = UTC hourly timestamps where all 5 symbols have `markPriceKlines` close > 0
- **`|S| = 22,584`** (recompute from cache; freeze exact value in prereg)
  - BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT: 22,608 clean 1h closes each
  - XRPUSDT: 22,584 (binds by exactly 24h on 2025-10-19 due to 24 corrupt negative close values)

### Sequential Confirmatory Look
- **Look `k=2`** (first was campaign-06)
- **Frozen `alpha_2 = 0.05/(2*3) = 0.008333`**
- **Declared Holm secondary:** next-24h downside realized-semivariance level, judged by MSE

### Frozen Design (DO NOT RE-DERIVE)
1. **Target:** `y = log(RV_24h_next + 1e-09)` from 1h mark-price log returns; metric = OOS QLIKE
2. **B1 baseline:** signed-HAR (log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h)
3. **C2 challenger:** B1 + signed funding(24h), trailing 90d |funding| percentile, mark/index premium, mark/EMA24 distance
4. **Split:** 60/20/20 chronological on `S`, 168h purge/embargo, **3 chronological test blocks**
5. **Models:** fixed-form stdlib OLS only — no regularization, no model/feature/threshold search
6. **Inference:** ≥2,000 fixed-seed block-bootstrap replicates (complete UTC blocks jointly across symbols); per-block + leave-one-symbol-out diagnostics
7. **Verdict threshold:** `PROMOTED` requires ≥2% relative QLIKE reduction, 95% bootstrap CI lower bound > 0 at alpha_2, consistent Holm secondary direction; else `NOT_SUPPORTED` (use `INCONCLUSIVE` only when evidence supports neither)

---

## MANDATORY EXECUTION SEQUENCE

1. **Create fresh session:** `research_state/session_<UTC>/` with id > `20261126T153244Z`
2. **Copy template:** `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` → new session dir
   - Set `SESSION` = fresh UTC id, `CAMPAIGN_START` = `20261126T153244Z`
3. **Apply mark-price-only common-support filter** (in `build_symbol_panel` or immediately after):
   - Read **ONLY** `markPriceKlines-*` CSVs (any of 3 layouts)
   - Dedup by `open_time` (mandatory — ~2,352 duplicate overwrites/symbol)
   - Drop `close<=0` (removes XRPUSDT 2025-10-19 corrupt day)
   - Retain only timestamps in all-5-symbol intersection `S`
   - **Never** read top-level `<SYM>-1h-*.zip` klines (regular price, NOT mark price)
4. **Verify every consumed file:** sha256 vs `.sha256` sidecar (hash-only, single 64-hex line) AND `cached_inputs_hashes.json["hashes"][path]`
5. **Produce all 8 required artifacts** in the fresh session (non-empty, real session_id):
   - `fclr_live_archive07_source_registry_<UTC>.{json,md}`
   - `fclr_live_archive07_prereg_<UTC>.{json,md}` (outcome-blind, `outcome_data_inspected_before_freeze:false`)
   - `fclr_live_archive07_eval_<UTC>.{py,json,md}`
   - `fclr_live_archive07_recompute_<UTC>.{py,json}` (independent stdlib, `all_checks_match:true`)
   - `fclr_live_archive07_evidence_audit_<UTC>.{json,md}` (`audit_pass=true`, no unresolved blockers)
   - `evidence_audit_<UTC>.{json,md}` (gate-critical alias)
   - `trigger_check_<UTC>.json` (`external_trigger_required:false`)
   - `_headline_<UTC>.json`
6. **Run verification:** gate `pass=true`, `reason_code=OK`, `failures=[]`, `live_archive.pass=true`
7. **Update** `experiment_frontier.json` rank-0 → `COMPLETED_VALIDATED`, demote campaign-07, promote next distinct task
8. **Finish only when §4 verification passes** — no missing/empty artifacts

---

## BOTTLENECKS REMOVED / NON-BLOCKERS

- ✅ No session is blocked; heavy-work gate is GREEN (armed)
- ✅ 5-symbol 2024-04..2026-10 mark-price cache on disk, verified
- ✅ Stdlib recovery template compiles (`py_compile` OK)
- ✅ `scripts/next_campaign_status.py` legacy "no feasible 3-block design" message is a **known non-blocker** — ignore it
- ✅ No network, no package installation, no new data required
- ✅ Quarantined invalid attempts (`20261126T153717Z`, `20261126T144850Z`) archived — do not reuse

---

## NON-AVOIDANCE CONSTRAINTS (MACHINE-ENFORCED)

- `scripts/check_handoff_heavywork_gate.py` binds this session to the **full `fclr_live_archive07_*` artifact family** + `evidence_audit_<UTC>.{json,md}` + `trigger_check_<UTC>.json`
- A trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder session **FAILS CLOSED**
- The gate is green ONLY because the newest on-disk session predates campaign start; **first post-start session without full heavy set fails**
- Closed/not re-runnable: campaigns 01/03/04/05/06; VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP; terminal liquidation-risk program
- Stdlib only. No package installation. No root-level `research_state/*.md`/`*.json` (root at 500-file cap)
- Single durable handoff: update `AGENT_HANDOFF.md` and `experiment_frontier.json` **only after artifacts exist and verify**

---

## DOMINANT LIMITATION TO DISCLOSE

Mark-price cache stored in **3 heterogeneous layouts** (2024_04-2024_09 nested; 2024_10-2024_12 flat; 2025_01-2026_10 + top-level zips). Month dirs **also carry separate regular-klines stream** (top-level `<SYM>-1h-*.zip`) that must NOT be confused with mark price. XRPUSDT 2025-10-19 has **24 negative (corrupt) mark-price closes** — quarantine, record provenance, do NOT zero-fill/repair/substitute. Recompute must use mark-price only, dedup by `open_time`, drop `close<=0`, quarantine XRP day. Per-block + leave-one-symbol-out diagnostics remain mandatory.

---

## CONCRETE FALSIFICATION TEST

C2 improves relative test QLIKE by ≥2% with frozen uncertainty and Holm conditions on the untouched balanced mark-price cohort (`|S|=22,584`, 3 test blocks, all 5 symbols in every fold).

---

## END OF INITIAL TASK MESSAGE — 2026-11-27T02:58:59Z

Next agent must execute campaign-07 exactly as frozen above. No substitutions, no threshold-shopping, no outcome inspection before prereg freeze.