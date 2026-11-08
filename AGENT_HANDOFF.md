## Initial Task Message (2026-11-08T07:33Z, git HEAD `1b857882c`) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** (1) funding-conditioned volatility forecasting, (2) liquidation risk (Track A observed / Track B modeled — never conflated). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Session FCLR-NEXT-135 delivered (P0, bounded Track A feasibility probe + v5 CLI refusal hardening; read-only checks; no loops/retries; no kline/funding/outcome loaders; no real `research_state` writes)

**P0 completed (bounded, no new confirmatory outcomes, no re-probe of absent months beyond single checks):**

1. **Bounded Hyperliquid archive probe (single HEAD each, `--max-time 25`, no retry storm):**
   - `https://hyperliquid-archive-node.s3.amazonaws.com/data/events/2026-11.parquet` → **HTTP/1.1 404 Not Found** (AmazonS3, 2026-11-08T07:28:31Z). Not-yet-available; **no trigger**.
   - `https://hyperliquid-archive-node.s3.amazonaws.com/data/fills/2026-11.parquet` → **HTTP/1.1 404 Not Found** (2026-11-08T07:30:18Z). **No trigger.** No further months probed.
2. **Track A resume-trigger watch (local evidence only):** `ironflow_monitor_state.json` `data_through=2026-10`; `ironflow_probe_digest_latest.json` latest `2026-10`; no 2026-11+ local cached liquidation/event/fill artifacts. **No trigger fired. No re-probe loop performed.**
3. **v5 CLI refusal parity hardening (optional, isolated, deterministic):** `fclr016_v5_admissibility_report.py` and `fclr016_v5_promotion_dryrun.py` now emit stable JSON refusal on `--bogus`/argparse errors (`ok:false, all_go:false, expect_go_refused:true, validator=...`, rc=2) while preserving argparse usage on stderr — parity with `fclr016_validate_v5_admissibility.py`. No data/network tokens added; no canonical artifacts touched.
4. **Verification:**
   - Targeted: `tests.test_fclr016_v5_admissibility_report`, `test_fclr016_v5_promotion_dryrun`, `test_fclr016_v5_cli_refusal_parity_132` → **31 tests, 0 failures, OK**.
   - `--bogus` JSON refusal confirmed for report/promotion-dryrun/validator (all non-GO, `expect_go_refused:true`).
   - `tracka_resume_check.py` => **pass:true, checks 17, network False** (live<=1 && non_20261104T==0 invariant).
5. **Invariants:** no competing handoff files; canonicals `experiment_frontier.json`/`run_manifest.json`/`evaluation_summary.md` unchanged; no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families added; **no confirmatory outcomes run**.

### Verified current state (do not re-litigate without new evidence)

- Protocol FROZEN 2026-11-06T20:36:32Z. Gates G1/G2/G3 satisfied in scope; G4 blocked.
- **H001 NOT_SUPPORTED** on all claim-worthy panels (FCLR-003/006/008/013, v3 30d/5sym). **Forecast gate NOT_MET; risk-overlay INELIGIBLE; no economic/overlay value claim.**
- **Track C:** sealed/locked; unsealed confirmatory panels exhausted (needs >=5 symbols, >=3 non-overlapping 30-day blocks).
- **Track A BLOCKED/EXHAUSTED.** Hyperliquid `events/fills 2026-11.parquet` both **404** as of 2026-11-08T07:28Z/07:30Z; `data_through=2026-10`. `live<=1`, `non_20261104T==0`. **NO re-probe absent months in a loop. PREREGISTER BEFORE outcomes; modeled != observed.**
- **Track B CLOSED_NEGATIVE.** Never conflate.
- **v5 confirmatory package `all_go=false`, `confirmatory_outcomes_permitted=false`.** Terms hard blocker `EXPLICIT_BLOCKER_UNRESOLVED` (`fabricated=false`). **No fabricated terms/reviews; no freeze/promote while blocked; no confirmatory outcomes on refusal.**
- Records: `final_confirmatory_verdict.md` (CLOSEOUT COMPLETE, H001 NOT_SUPPORTED), `negative_results_report.md`, `final_record_closure_audit.md`.

### Single highest-value next task (heavy, measurable — do not coast)

**FCLR-NEXT-136 (P0, registry-drift cleanup OR hold — bounded deterministic):** Confirmatory research remains blocked (v5 terms unresolved; Track A 2026-11 absent/404; no new admissible Track C panel). The pre-existing 7 test failures are `MISSING_IN_REGISTRY` for v5 scripts (`fclr016_v5_admissibility_report.py`, `fclr016_v5_preflight_summary.py`, `fclr016_v5_promotion_dryrun.py`, `fclr016_v5_terms_evidence_template.py`, `fclr016_validate_v5_admissibility.py`) in `tracka_script_scope_registry.json` (read-only evidence; do not guess semantics).

- **If registry update is mechanically correct and isolated:** add those v5 scripts to the appropriate registry scope with accurate metadata (derive from existing entries; run `tests.test_tracka_script_scope_registry` / the 7 affected tests + targeted v5 suites). Keep change minimal, auditable, no behavior change to research logic.
- **If semantics are unclear:** do **not** guess; document the exact ambiguity and hold.
- **Do not** touch the 21 pre-existing env/import errors unless a cheap, local, deterministic fix is obvious and scoped.
- **Do not** generate status artifacts, wrappers, schedulers, or re-probe absent Track A months.

### Commands
```bash
python3 -m unittest tests.test_fclr016_v5_admissibility_report tests.test_fclr016_v5_promotion_dryrun tests.test_fclr016_v5_cli_refusal_parity_132 -q
python3 scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass',d['pass'],'checks',len(d['checks']))"
python3 scripts/fclr016_v5_admissibility_report.py --bogus 2>&1 | tail -1
python3 scripts/fclr016_v5_promotion_dryrun.py --bogus 2>&1 | tail -1
# single bounded probe only if a materially later month becomes plausible; NEVER loop:
# curl -sI --max-time 25 'https://hyperliquid-archive-node.s3.amazonaws.com/data/events/2026-12.parquet' | head -1
```

### Resume triggers (only then — preregister BEFORE outcomes)
1. **Track A/H004:** unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 with **HTTP 200, verified content** (probe only specific months; no loop) OR admissible unauthenticated observed-liquidation source passing full-manifest GO rubric. Fresh experiment ID, prereg before outcomes, modeled!=observed.
2. **v5 terms resolved by human/legal review:** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only; `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope. Reconcile refs/hashes; promote prereg to frozen only after all guards green; run package/validator/report/preflight/promotion-dryrun with `--expect-go` as applicable (no data load on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New admissible Track C data:** >=5 symbols, >=3 non-overlapping 30-day blocks, unauthenticated/admissible, fresh prereg before outcomes.

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete/blocked data; freeze/promote prereg while blockers exist; reopen sealed anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe absent months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files; run confirmation without fresh pre-registration + new admissible data.
