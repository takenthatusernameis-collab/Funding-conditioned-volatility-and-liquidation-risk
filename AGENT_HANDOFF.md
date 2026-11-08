## Initial Task Message (2026-11-08T08:45:16Z, git HEAD `592fdb09d`) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** (1) funding-conditioned volatility forecasting (Track C / Gate 4, local data — measurable, unblocked, heavy), (2) liquidation risk (Track A observed / Track B modeled — never conflated; Track A blocked/no trigger). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Bottlenecks removed this session (delivered before FCLR-NEXT-137)

1. Environment: `pip install -r requirements.txt` (numpy, pandas, scipy) — removed 21 pre-existing `ModuleNotFoundError` env/import errors that failed collection across 7 test modules (`test_data_loading`, `test_timestamp_parsing`, `test_tracka_hardening_114/115`, `test_funding_ablations*`, plus the 116-119 hardening modules).
2. `scripts/run_funding_ablations.py` (Gate 4 pipeline): fixed undefined names blocking every data-loading path — lazy `from src.ingest import loader` in `ensure_extracted`/`load_funding_series`/`load_kline_series`; module-level `import numpy as np` + `import pandas as pd`; lazy `from src.features import volatility as vf`, `from src.features import funding as ff`, `from src.eval import walkforward as wf`, `from src.volatility import block_bootstrap as bb`, `from src.volatility import eval as veval` at each use site.
3. Verification: `python -m unittest discover tests` → **883 tests, 0 failures, OK**; `check_tracka_scope_registry_drift.py` → **101/101 pass**; `tracka_resume_check.py` → **pass:true, 17 checks, network False**; v5 CLI refusal parity (`--bogus` JSON refusal on report/promotion-dryrun/validator) preserved.

### Session FCLR-NEXT-136 delivered (registry-drift probe — closed, no-op-verified)

- `research_state/tracka_script_scope_registry.json` already scopes all five v5 scripts (`fclr016_v5_admissibility_report.py`, `fclr016_v5_preflight_summary.py`, `fclr016_v5_promotion_dryrun.py`, `fclr016_v5_terms_evidence_template.py`, `fclr016_validate_v5_admissibility.py`) as `prereg_utility`; drift check **101/101 OK** — no registry edit required. Targeted v5 suites: **31 tests, 0 failures, OK** (unchanged).

### Verified current state (do not re-litigate without new evidence)

- Protocol FROZEN 2026-11-06T20:36:32Z. Gates G1/G2/G3 satisfied in scope; G4 blocked.
- **H001 NOT_SUPPORTED** on all claim-worthy panels (FCLR-003/006/008/013, v3 30d/5sym). **Forecast gate NOT_MET; risk-overlay INELIGIBLE; no economic/overlay value claim.**
- **Track C:** sealed/locked; unsealed confirmatory panels exhausted (needs >=5 symbols, >=3 non-overlapping 30-day blocks).
- **Track A BLOCKED/EXHAUSTED.** Hyperliquid `events/fills 2026-11.parquet` both **404** as of 2026-11-08T07:28Z/07:30Z; `data_through=2026-10`. `live<=1`, `non_20261104T==0`. **NO re-probe absent months in a loop. PREREGISTER BEFORE outcomes; modeled != observed.**
- **Track B CLOSED_NEGATIVE.** Never conflate.
- **v5 confirmatory package `all_go=false`, `confirmatory_outcomes_permitted=false`.** Terms hard blocker `EXPLICIT_BLOCKER_UNRESOLVED` (`fabricated=false`). **No fabricated terms/reviews; no freeze/promote while blocked; no confirmatory outcomes on refusal.**
- Records: `final_confirmatory_verdict.md` (CLOSEOUT COMPLETE, H001 NOT_SUPPORTED), `negative_results_report.md`, `final_record_closure_audit.md`.

### Single highest-value next task (heavy, measurable — do not coast)

**FCLR-NEXT-137 (P0 — execute Gate 4 funding-conditioned volatility ablation end-to-end):** Per repo-name priority, funding-conditioned volatility is the unblocked heavy work. Track A remains blocked (Hyperliquid `events/fills 2026-11.parquet` both 404; no trigger; no re-probe loop). Track B closed negative. Execute locally, no network:

1. Run the pre-registered Gate 4 pipeline: `python scripts/run_funding_ablations.py` (multisplit walk-forward, purge/embargo >= 7d, train-only normalization, last-known funding at/before hour, block-bootstrap ΔQLIKE CIs, honest PILOT/INCONCLUSIVE verdict when data-sufficiency criteria unmet). Confirm it runs cleanly and writes evaluation/manifest/leakage summaries under research_state as non-confirmatory pilot evidence only.
2. Re-run full suite: `python -m unittest discover tests -q` → must stay **>=883 OK, 0 failures**.
3. Apply `FCLR_CAMPAIGN_NEXT.md` lockdown hardening only: seam tests (empty/unreadable data path under valid prereg -> blocked with stable reason codes); CLI argparse contract edge cases on the 3 CLIs; cross-CLI parity + canonical output integrity. **No** new status-only/poller/wrapper/scheduler families, no competing handoff files, no research_state writes beyond the ablation's own pre-registered outputs, no `.github/workflows` edits.
4. Gate discipline: no confirmatory outcomes, no freeze/promote while the v5 terms blocker is unresolved; no Track A outcomes without a resume trigger + fresh pre-registration.

### Commands
```bash
pip install -r requirements.txt
python -m unittest discover tests -q
python scripts/check_tracka_scope_registry_drift.py
python scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass',d['pass'],'checks',len(d['checks']))"
python scripts/fclr016_v5_admissibility_report.py --bogus 2>&1 | tail -1
python scripts/fclr016_v5_promotion_dryrun.py --bogus 2>&1 | tail -1
python scripts/run_funding_ablations.py   # Gate 4 funding-conditioned volatility ablation (P0 heavy work)
```

### Resume triggers (only then — preregister BEFORE outcomes)

1. **Track A/H004:** unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 with **HTTP 200, verified content** (probe only specific months; no loop) OR admissible unauthenticated observed-liquidation source passing full-manifest GO rubric. Fresh experiment ID, prereg before outcomes, modeled!=observed.
2. **v5 terms resolved by human/legal review:** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only; `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope. Reconcile refs/hashes; promote prereg to frozen only after all guards green; run package/validator/report/preflight/promotion-dryrun with `--expect-go` as applicable (no data load on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New admissible Track C data:** >=5 symbols, >=3 non-overlapping 30-day blocks, unauthenticated/admissible, fresh prereg before outcomes.

### Do-NOT
Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete/blocked data; freeze/promote prereg while blockers exist; reopen sealed anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe absent months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files; run confirmation without fresh pre-registration + new admissible data.
