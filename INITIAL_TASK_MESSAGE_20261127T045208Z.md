# INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — 2026-11-27T04:52:08Z

**Program:** Funding-Conditioned Volatility and Liquidation Risk (FCLR)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (repo-name driven):** **Funding-conditioned next-24h volatility forecasting** — the single highest-value unfinished confirmatory task.

---

## CURRENT STATE (authoritative as of 2026-11-27T04:52:08Z)

- **Active rank-0 task:** `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` — status `READY_EXECUTE`
- **HEAD:** `dc69eae02` (working tree clean)
- **Latest completed heavy session:** `session_20261126T133828Z` (campaign-06, `NOT_SUPPORTED`, `all_checks_match=true`)
- **Heavy-work gate:** GREEN (armed) — `pass=true`, `reason_code=OK`, `failures=[]`, `live_archive.pass=true`
- **No bottlenecks:** The prior ambiguity (dueling root-level INITIAL_TASK_MESSAGE files) was resolved at 2026-11-27T03:06:12Z; both archived. The single durable handoff is `AGENT_HANDOFF.md`.

**Key numerical correction (frozen by direct cache measurement at 2026-11-27T03:59:57Z):**
- Common support `S` = UTC hourly timestamps where **all five symbols** (BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT) have a `markPriceKlines` close > 0
- `|S| = 22,584` (NOT 22,608; NOT 8,976)
- Per-symbol 1h counts: BNBUSDT=22,608, BTCUSDT=22,608, ETHUSDT=22,608, SOLUSDT=22,608, **XRPUSDT=22,584** (binds by 24h)
- XRPUSDT 2025-10-19 has **24 negative/corrupt mark-price closes** → quarantine, do NOT zero-fill
- Embargoed 60/20/20 split on `S` (168h purge): train ≈13,550 ts / val ≈4,517 ts / test ≈4,517 ts ≈ **22,585 test rows across all 5 symbols**; three chronological test blocks of ≈1,500 ts each, all five symbols present in every block

**Cache layout heterogeneity (must be handled correctly):**
- Three layouts for `markPriceKlines-*` CSVs across 2024-04..2026-10; month dirs also carry a separate **regular klines stream** (top-level `<SYM>-1h-<date>.zip`) that is NOT mark price — verified different values
- **Rule:** read ONLY `markPriceKlines-*` CSVs/ZIPs (walk to any depth), dedup by `open_time`, drop `close<=0`; NEVER fold top-level `<SYM>-1h-*.zip` into the mark-price panel

---

## MANDATORY NEXT SESSION WORK: EXECUTE CAMPAIGN-07

Create exactly **one fresh** `research_state/session_<UTC>/` with UTC id **lexicographically greater than `20261126T153244Z`** and execute the complete heavy evaluation under that single session.

### Step-by-step execution sequence

1. **Create session directory**
   ```bash
   export UTC=$(date -u +%Y%m%dT%H%M%SZ)
   mkdir -p research_state/session_$UTC
   ```

2. **Copy the recovery template** into the new session directory:
   ```bash
   cp handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py \
      research_state/session_$UTC/
   cd research_state/session_$UTC
   ```

3. **Modify the template** to implement the **mark-price-only common-support filter `S` before pooling** (not merely filtering final rows):
   - Read ONLY `markPriceKlines-*` mark-price CSVs/ZIPs (any of the three layouts, walk to any depth)
   - Dedup by `open_time` (ms)
   - Drop `close <= 0` (removes the corrupt XRPUSDT 2025-10-19 day)
   - Compute the all-five-symbol hourly intersection `S`
   - Retain only rows whose timestamp `t ∈ S` **before** computing returns, rolling history, or forward targets
   - Recompute and freeze `|S| = 22,584`, per-symbol counts, and split sizes in the prereg

4. **Run the heavy evaluation** producing the complete artifact set (§2 below) under that one fresh session directory.

5. **Run independent stdlib recompute** that rebuilds `S` from scratch and confirms `all_checks_match=true`, all five symbols in every block/fold, `n_test >= 500`.

6. **Only after artifacts exist and verify**, update `research_state/experiment_frontier.json` and `AGENT_HANDOFF.md`:
   - Set rank-0 to `COMPLETED_VALIDATED` with reproduced verdict
   - Demote campaign-07 to non-zero rank
   - Promote the next materially distinct unfinished task without reopening a closed arm

---

## REQUIRED HEAVY ARTIFACTS (all under the SAME fresh session directory)

| Artifact | Purpose |
|----------|---------|
| `fclr_live_archive07_source_registry_<UTC>.{json,md}` | Exact cache paths, per-file SHA-256 vs sidecars + `cached_inputs_hashes.json["hashes"]`, coverage/layout/shortfalls, `S` definition, `|S|=22584`, XRPUSDT 2025-10-19 quarantine |
| `fclr_live_archive07_prereg_<UTC>.{json,md}` | Outcome-blind, hash-bound to source registry, `outcome_data_inspected_before_freeze:false`, look `k=2`, `alpha_2=0.008333`, frozen `|S|` and split sizes |
| `fclr_live_archive07_eval_<UTC>.{py,json,md}` | Heavy 3-block evaluation on balanced mark-price support `S`, ≥2,000 deterministic block-bootstrap replicates, per-block + leave-one-symbol-out diagnostics |
| `fclr_live_archive07_recompute_<UTC>.{py,json}` | Independent stdlib recompute with `all_checks_match:true`, rebuilds `S` (mark-price only, `close>0`) |
| `fclr_live_archive07_evidence_audit_<UTC>.{json,md}` | Leakage/evidence audit with `audit_pass`, verdict, `unresolved_blockers` |
| `evidence_audit_<UTC>.{json,md}` | Substantive gate-critical alias matching the verdict |
| `trigger_check_<UTC>.json` | `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false` |
| `_headline_<UTC>.json` | Concise headline metrics for independent gate validation |

**Constraints:** Every file non-empty; every JSON carries real `session_id` and experiment id; **no root-level `research_state/*.md` or `*.json` files** (root is at exactly 500 md+json files, zero headroom — a single root-level write makes 501 and fails the gate).

---

## FROZEN DESIGN — DO NOT RE-DERIVE OR THRESHOLD-SHOP

1. **Cohort / support:** 2024-04-01 through 2026-10-31 UTC; exactly the five symbols above; restricted to the mark-price common support `S` = UTC hourly timestamps where all five symbols have a `markPriceKlines` close > 0 (`|S| = 22,584` balanced-for-four / XRPUSDT-binds-by-24h). Disjoint from the 2021-2024 cohort used by campaigns 01–06.
2. **Primary target:** `y = log(RV_24h_next + 1e-09)` from one-hour mark-price log returns; metric: out-of-sample **QLIKE**.
3. **Declared secondary (Holm 2-family):** `log(RV_minus_next24h + 1e-09)`; metric: **MSE** (campaign-06 estimand).
4. **B1:** fixed signed-HAR history set: log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 features).
5. **C2:** B1 + signed funding(24h) + trailing 90-day absolute-funding percentile + mark/index premium + mark/EMA24 distance (11 features). All scaling train-only.
6. **Split:** 60/20/20 by unique UTC timestamp **on `S`**, 168-hour purge/embargo, three chronological test blocks.
7. **Models:** fixed-form deterministic stdlib OLS only. No regularization, model-family search, feature search, or threshold tuning.
8. **Inference:** ≥2,000 fixed-seed block-bootstrap replicates, preserving complete UTC blocks jointly across symbols; report per-block and leave-one-symbol-out concentration diagnostics.
9. **Verdict:** `PROMOTED` requires primary C2-versus-B1 relative QLIKE reduction ≥ 2%, 95% bootstrap CI lower bound > 0 at look `k=2` alpha, and consistent Holm-adjusted secondary direction. Otherwise preserve `NOT_SUPPORTED`; use `INCONCLUSIVE` only when evidence supports neither conclusion.
10. **Sequential look:** `k=2`, `alpha_2 = 0.05/(2*3) = 0.008333` (RESEARCH_PROMPT.md §17).

---

## VERIFICATION COMMANDS (run at START and END of session)

```bash
export UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m unittest \
  tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 tests.test_active_campaign_gate
python3 -m json.tool research_state/experiment_frontier.json >/dev/null
git diff --check
```

**Gate must report at END:** top-level `pass=true`, `reason_code=OK`, `failures=[]`, `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive07"`, with empty missing/empty artifact lists. Six-module unittest must pass.

---

## COMPLETED SESSION RECORD (for reference — do not re-run)

**Campaign:** `FCLR-LIVE-ARCHIVE-06-20261126T083526Z`
**Verdict:** `NOT_SUPPORTED` — C2 vs B1 relative test-MSE reduction `0.716%`, 95% block-bootstrap CI `[0.419%, 1.020%]`, below the frozen 2% floor.
**Independent recompute:** `all_checks_match=true`; `n_test=35715`; `n_unique_timestamps=34872`.
**Evidence audit:** `audit_pass=true`; `unresolved_blockers=[]`.
**Complete artifacts under:** `research_state/session_20261126T133828Z/` (do not re-run campaign-06).

---

## FOCUS CAMPAIGN & NON-AVOIDANCE CONSTRAINTS

**Focus campaign (repo-name priority):** Funding-conditioned next-24h volatility forecasting. The repo name leads with **Funding-conditioned-volatility**, so the confirmatory campaign-07 contrast (C2 vs B1 on next-24h log-RV QLIKE, balanced mark-price disjoint 2024-04..2026-10 cohort) is the **single highest-value unfinished task** and the **only task this session may execute**.

- **Machine-enforced non-avoidance:** `scripts/check_handoff_heavywork_gate.py` binds campaign-07 to the `fclr_live_archive07_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the newest session. A trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder session **fails closed**.
- **Closed and not re-runnable:** campaigns 01/03/04/05/06 on the five-symbol archive; broad ironflow VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP arms; the terminal liquidation-risk program on the frozen ironflow panel.
- **Do not build a risk overlay:** the forecast gate has not passed.
- **Do not wait for an external trigger:** campaign-07 requires no network and no new source.
- **Do not modify** `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts.
- **Stdlib only** for campaign-07. No package installation (numpy/pandas/pyarrow are NOT installed).
- **Single durable handoff:** update `AGENT_HANDOFF.md` and `research_state/experiment_frontier.json` **only after** the heavy artifacts exist and verify. Do not create root-level `research_state/*.md`/`*.json` files.

---

## DOMINANT LIMITATION TO DISCLOSE

The mark-price cache is stored in **three heterogeneous layouts**, the month dirs also carry a **separate regular-klines stream**, and **XRPUSDT 2025-10-19 has 24 negative (corrupt) mark-price closes** — the recompute must use mark-price only, dedup by `open_time`, drop `close<=0`, and quarantine the XRP day; per-block + leave-one-symbol-out diagnostics remain mandatory.

---

## CONCRETE FALSIFICATION TEST

C2 improves relative test QLIKE by **at least 2%** with the frozen uncertainty and Holm conditions on the untouched balanced mark-price cohort.

---

## NEXT AGENT: START HERE

1. Read `AGENT_HANDOFF.md` and `RESEARCH_PROMPT.md` completely.
2. Run the verification commands above to confirm gate state.
3. Create the fresh session directory with UTC id > `20261126T153244Z`.
4. Copy and adapt the recovery template with the **mark-price-only `S` filter applied before pooling**.
5. Execute the complete heavy evaluation + independent recompute + evidence audit + trigger check.
6. Update frontier and handoff only after verification passes.

**Do not create a second active handoff. Do not produce a status-only session. The next session's purpose is the complete heavy evaluation, independent reproduction, and synchronized frontier.**

---

**END OF INITIAL TASK MESSAGE — 2026-11-27T04:52:08Z**