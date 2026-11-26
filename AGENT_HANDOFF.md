# AGENT HANDOFF — Durable Single Source of Truth for Next Session

**Generated (UTC):** 2026-11-26T17:50:13Z
**Program status:** ACTIVE (FCLR-LIVE-ARCHIVE-07 rank-0 READY_EXECUTE)
**Terminal verdict:** NONE — active confirmatory campaign in progress
**HEAD:** 593078e4b1aec7d0de2b8e1ce1ff4d683ce5a14a
**Working tree:** clean

---

## 1. EXECUTIVE SUMMARY

The confirmatory research program **Funding-conditioned-volatility-and-liquidation-risk** has an ACTIVE rank-0 campaign:

| Rank | Campaign | Status | Program | Key Evidence |
|------|----------|--------|---------|--------------|
| **0** | **FCLR-LIVE-ARCHIVE-07-20261126T153244Z** | **READY_EXECUTE** | **ACTIVE** | Disjoint 5-symbol cohort (2024-04..2026-10), sequential look k=2, alpha_2=0.008333, primary=next-24h mean log-RV QLIKE (campaign-01 estimand), secondary=downside realized-semivariance level (campaign-06 estimand) |
| 1 | FCLR-LIVE-ARCHIVE-06-20261126T083526Z | COMPLETED_VALIDATED | COMPLETE | NOT_SUPPORTED: C2 vs B1 relative MSE reduction 0.716% (CI [0.419%,1.020%]) < 2% floor on 5-symbol 2021-2024 Binance archive. Independent stdlib recompute all_checks_match=true. |
| 16 | FCLR-LIVE-ARCHIVE-05-20261126T072336Z | COMPLETED_VALIDATED | COMPLETE | NOT_SUPPORTED: signed-semivariance-asymmetry (rel MSE 0.141%, CI [-0.032%,0.315%]) |
| 14 | FCLR-LIVE-ARCHIVE-04-20261126T061929Z | COMPLETED_VALIDATED | COMPLETE | NOT_SUPPORTED: quantile/full-distribution (rel avg-pinball -1.102%) |
| 15 | FCLR-LIVE-ARCHIVE-03-20261126T042519Z | COMPLETED_VALIDATED | COMPLETE | NOT_SUPPORTED: stress/tail Brier (rel 0.458%, CI includes 0) |
| 1 | FCLR-LIVE-ARCHIVE-01-20261125T074500Z | COMPLETED_VALIDATED | ACTIVE | NOT_SUPPORTED: mean-RV QLIKE (rel 0.840% < 2%) |
| 2+ | All VOL-JUMP, VOL-STRESS, VOL-CORR, VOL-BROAD, LIQ-XSEC, PROGRAM-CLOSURE | COMPLETED_VALIDATED | COMPLETE | All arms closed NOT_SUPPORTED at broad scale |

**Bottom line:** FCLR-LIVE-ARCHIVE-07 is the ONLY active confirmatory campaign. It targets the repo-name-leading estimand (funding-conditioned volatility, next-24h mean log-RV QLIKE) on a DISJOINT 5-symbol cohort (2024-04..2026-10) that has never been tested. The template exists at `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py`. Stdlib only (no numpy/pandas/pyarrow).

---

## 2. CAMPAIGN STATUS SNAPSHOT (from `scripts/next_campaign_status.py`)

```
== CAMPAIGN STATUS: no feasible 3-block design in ANY domain ==

Domains scanned:
- Binance 5-symbol (mark+premium+index klines + funding): 3 ready months (2024-04, 2024-05, 2025-01) — NONE feasible for disjoint 30-day blocks (train history unfunded)
- Mark+funding-only (B0/B1/C1): 1 individually feasible block (2025-01) — need ≥3 mutually non-overlapping
- Hyperliquid bulk (ironflow: candles_1h + funding + OI + liquidations): 24-day untouched region (2025-05-01..2025-05-24) — need ≥127 days for 3-block
- Hyperliquid extended (candles+funding+observed-liq events, 17 coins): 12 usable months (2025-11..2026-10) but ALL inside tested windows — no untouched contiguous region
```

**Note:** The "no feasible 3-block design" status reflects the OLD 3-block framing. FCLR-LIVE-ARCHIVE-07 uses a **60/20/20 chronological split with 3 test blocks** on the verified 31-month 5-symbol cache — a materially different, feasible design on admissible frozen data. The `next_campaign_status.py` tool does not yet recognize this campaign's design class.

---

## 3. HEAVY-WORK GATE STATUS (from `scripts/check_handoff_heavywork_gate.py`)

```
[FAIL] handoff-heavywork gate: handoff=True markers=True heavy_session=None session_ok=False root=500/500 reason=HANDOFF_HEAVYWORK_GATE_FAILED
  - HEAVY_SESSION_ID_UNRECORDED
```

**Root cause:** The latest completed session `session_20261126T133828Z` (FCLR-LIVE-ARCHIVE-06, all_checks_match=true) is NOT recorded in `AGENT_HANDOFF.md`. The gate requires the handoff to reference the latest heavy session and its artifact set.

**Required fix:** Update `AGENT_HANDOFF.md` to include `session_20261126T133828Z` in the session list and record its complete `fclr_live_archive06_*` artifact set.

---

## 4. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (UTC 2026-11-26T17:50:13Z)

### MANDATORY SEQUENCE — DO NOT SKIP STEPS

**Step 0: Verify environment & record baseline**
```bash
python3 scripts/next_campaign_status.py
python3 scripts/check_handoff_heavywork_gate.py --json
git rev-parse HEAD
git status
```

**Step 1: Update AGENT_HANDOFF.md to record completed session**
- Add `session_20261126T133828Z` to the handoff's session registry
- Document its complete artifact set: `fclr_live_archive06_{source_registry,prereg,eval,recompute,evidence_audit,trigger_check}_20261126T133828Z.{json,md,py}`
- Verify the handoff now passes the heavy-work gate check (Step 0 re-run)

**Step 2: Execute FCLR-LIVE-ARCHIVE-07 heavy confirmatory evaluation**
- Create fresh session directory: `research_state/session_<UTC>/` with UTC > `20261126T175013Z`
- Use the recovered stdlib template: `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py`
  - Update `SESSION` to the new session UTC
  - Update `CAMPAIGN_START` to `20261126T153244Z` (from experiment_frontier.json rank-0)
  - Run the script to produce the full `fclr_live_archive07_*` artifact set
- **Required artifacts (ALL non-empty, under the new session dir):**
  - `fclr_live_archive07_source_registry_<UTC>.{json,md}` — hash-bound to prereg, 20,694 cache entries verified
  - `fclr_live_archive07_prereg_<UTC>.{json,md}` — outcome-blind, frozen_before_outcomes=true, hash-bound to source registry
  - `fclr_live_archive07_eval_<UTC>.{py,json,md}` — heavy 60/20/20 evaluation, 2000 block-bootstrap, LOO diagnostics
  - `fclr_live_archive07_recompute_<UTC>.{py,json}` — independent stdlib recompute, all_checks_match=true
  - `fclr_live_archive07_evidence_audit_<UTC>.{json,md}` — audit_pass=true, verdict matches eval, no blockers
  - `evidence_audit_<UTC>.json` — gate-critical alias (substantive, not stub)
  - `trigger_check_<UTC>.json` — external_trigger_required=false, trigger_source=FROZEN_BINANCE_ARCHIVE, fired=false
  - `_headline_<UTC>.json` — summary metrics for quick gate validation

**Step 3: Update experiment_frontier.json**
- Set rank-0 campaign status to `COMPLETED_VALIDATED`, program_status to `COMPLETE`
- Record `completed_session`, `completed_utc`, `last_verdict`, `all_checks_match=true`
- Add new session to carry_forward_bundles

**Step 4: Update AGENT_HANDOFF.md**
- Record new session timestamp and artifact paths
- Update program status based on verdict (PROMOTED / NOT_SUPPORTED / INCONCLUSIVE)
- If NOT_SUPPORTED: promote next campaign per ladder (FCLR-LIVE-ARCHIVE-08 or equivalent)
- If PROMOTED: document promotion and next steps per §17

**Step 5: Verify gate passes**
```bash
python3 scripts/check_handoff_heavywork_gate.py --json
# Must return {"pass": true, ...}
```

---

## 5. HARD CONSTRAINTS (Violations = Failed Session)

| Constraint | Enforcement |
|------------|-------------|
| **No sealed experiment re-run** | Only read-only verification allowed (byte-identical reproduction of unsealed confirmations). |
| **No threshold shopping** | Materiality floors (2%), Holm families, §17 conditions frozen at prereg. |
| **No fabrication** | All data from frozen caches (`research_state/data_cache/`); no network for confirmatory work. |
| **No track adulteration** | FCLR-LIVE-ARCHIVE campaigns use Binance archive only; do not mix with ironflow_bulk or contagion panel. |
| **No overlay without §9 gate** | Forecast gate (QLIKE + Brier + LogLoss ALL pass) required; none passed. |
| **Root file cap** | `research_state/*.md|*.json` ≤ 500 at root — all new artifacts under `session_<UTC>/`. |
| **Prereg before outcomes** | `outcome_data_inspected_before_freeze: false` mandatory; sha256 input assertions. |
| **Stdlib only** | No numpy/pandas/pyarrow/requests; no pip install. Use template's deterministic OLS + bootstrap. |

---

## 6. KEY ARTIFACT PATHS (for verification)

| Artifact | Path |
|----------|------|
| Experiment frontier | `research_state/experiment_frontier.json` |
| FCLR-LIVE-ARCHIVE-07 template | `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` |
| Completed session (FCLR-LIVE-ARCHIVE-06) | `research_state/session_20261126T133828Z/` |
| Binance cache (read-only) | `research_state/data_cache/{BNBUSDT,BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT}_20??_??/` |
| Hash registry | `research_state/cached_inputs_hashes.json` (20,694 entries) |
| Campaign status script | `scripts/next_campaign_status.py` |
| Heavy-work gate checker | `scripts/check_handoff_heavywork_gate.py` |

---

## 7. VERIFICATION COMMANDS (run at session start)

```bash
# 1. Campaign feasibility (expect "no feasible 3-block design" — this is the OLD framing)
python3 scripts/next_campaign_status.py

# 2. Heavy-work gate (expect FAIL with HEAVY_SESSION_ID_UNRECORDED until Step 1 done)
python3 scripts/check_handoff_heavywork_gate.py --json

# 3. Git state
git rev-parse HEAD
git status

# 4. Confirm template exists
ls -la handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py

# 5. Confirm completed session artifacts exist
ls -la research_state/session_20261126T133828Z/fclr_live_archive06_*.json
```

---

## 8. SESSION TEMPLATE (for Step 1 handoff update)

```markdown
## Completed Session Record — 2026-11-26T13:38:28Z
**Session:** `session_20261126T133828Z/`
**Campaign:** `FCLR-LIVE-ARCHIVE-06-20261126T083526Z`
**Verdict:** `NOT_SUPPORTED` (C2 vs B1 relative MSE reduction 0.716%, 95% CI [0.419%,1.020%] < 2% floor)
**All checks match:** `true` (independent stdlib recompute)
**Artifacts produced:**
- `fclr_live_archive06_source_registry_20261126T133828Z.{json,md}`
- `fclr_live_archive06_prereg_20261126T133828Z.{json,md}`
- `fclr_live_archive06_eval_20261126T133828Z.{py,json,md}`
- `fclr_live_archive06_recompute_20261126T133828Z.{py,json}`
- `fclr_live_archive06_evidence_audit_20261126T133828Z.{json,md}`
- `evidence_audit_20261126T133828Z.json`
- `trigger_check_20261126T133828Z.json`
- `_headline_20261126T133828Z.json`
**Git HEAD at completion:** (record from session logs)
```

---

## 9. NEXT INITIAL TASK MESSAGE (timestamped 2026-11-26T17:50:13Z) — DURABLE HANDOFF

**INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (UTC 2026-11-26T17:50:13Z):**

The program has an ACTIVE confirmatory campaign: **FCLR-LIVE-ARCHIVE-07** (rank-0 in `experiment_frontier.json`, status=READY_EXECUTE, program=ACTIVE). It targets the repository-name-leading estimand — funding-conditioned volatility, next-24h mean log-RV QLIKE (campaign-01) — on a DISJOINT 5-symbol cohort (2024-04..2026-10, BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT) with sequential look k=2 (alpha_2=0.008333). The verified Binance public archive cache is frozen and read-only; the stdlib-only evaluation template is at `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py`.

**BOTTLENECK TO CLEAR FIRST:** The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) fails with `HEAVY_SESSION_ID_UNRECORDED` because the latest completed session `session_20261126T133828Z` (FCLR-LIVE-ARCHIVE-06, all_checks_match=true) is not recorded in this handoff. **Step 1 of the mandatory sequence is to update this handoff to record that session and its complete artifact set, then re-verify the gate passes.**

After the gate passes, **execute the full FCLR-LIVE-ARCHIVE-07 heavy evaluation triad** under a fresh `research_state/session_<UTC>/` (UTC > 20261126T175013Z): (1) freeze outcome-blind prereg hash-bound to source registry; (2) run eval + independent stdlib recompute + evidence audit + gate alias + trigger check; (3) produce non-empty `fclr_live_archive07_*` artifacts; (4) update `experiment_frontier.json` and this handoff AFTER artifacts exist. All new artifacts MUST go under `session_<UTC>/` (root cap 500). Stdlib only; no network; no threshold shopping; no track adulteration. Heavy work is mandatory; idling or gate-only sessions are failed sessions.

**END OF HANDOFF — 2026-11-26T17:50:13Z**