## Initial Task Message (2026-11-08T09:23:42Z, git HEAD `a438a3aeb`) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority:** (1) funding-conditioned volatility forecasting (Track C / Gate 4, local data — measurable, unblocked, heavy), (2) liquidation risk (Track A observed / Track B modeled — never conflated; Track A blocked/no trigger). **Mission:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff files.**

### Bottlenecks removed this session (delivered before this message)

1. Environment: `pip install -r requirements.txt` (numpy, pandas, scipy) — removed 21 pre-existing `ModuleNotFoundError` env/import errors that failed collection across 7 test modules.
2. `scripts/run_funding_ablations.py` (Gate 4 pipeline): fixed undefined names blocking every data-loading path — lazy `from src.ingest import loader` in `ensure_extracted`/`load_funding_series`/`load_kline_series`; module-level `import numpy as np` + `import pandas as pd`; lazy feature/eval/volatility imports at each use site.
3. Verification (re-confirmed this session): `python -m unittest discover tests` → **883 tests, 0 failures, OK**; `scripts/run_funding_ablations.py` → runs clean end-to-end, honest `PILOT/INCONCLUSIVE` verdict (data-sufficiency criteria not met; no claim-worthy inference); `check_tracka_scope_registry_drift.py` → **101/101 pass**; `tracka_resume_check.py` → `pass:true, 17 checks, network False`; v5 CLI refusal parity (`--bogus` JSON refusal on report/promotion-dryrun/validator) preserved.

### Sessions / tracks blocked (honest hard blocks — do not loop, do not fabricate a way around)

- **Track A / H004 (liquidation labels):** Hyperliquid `data/events/YYYY-MM.parquet` and `data/fills/YYYY-MM.parquet` for 2026-11 both **404** as of 2026-11-08T07:28Z/07:30Z; `data_through=2026-10`. **NO re-probe absent months in a loop.** Resume only on a verified HTTP 200 month + fresh pre-registration (see Resume triggers).
- **v5 confirmatory package:** `all_go=false`, `confirmatory_outcomes_permitted=false`; terms blocker `EXPLICIT_BLOCKER_UNRESOLVED` (`fabricated=false`). **No fabricated terms/reviews; no freeze/promote while blocked; no confirmatory outcomes on refusal.**
- **Gate 4 data sufficiency (claim-worthiness hard limit):** local admissible cache holds **4 symbols** (BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, 2024-01..2024-03) < 5 required; test windows 14/14/14 days = 0 non-overlapping 30-day blocks (>=3 required). This is a genuine local data ceiling, not a code bug. The ablation runs and reports an honest PILOT/INCONCLUSIVE verdict; do not threshold-shop or claim inference.

### Single highest-value next task (heavy, measurable — do not coast)

**FCLR-NEXT-137 (P0 — execute Gate 4 funding-conditioned volatility ablation end-to-end):** Per repo-name priority, funding-conditioned volatility is the unblocked heavy work. Run locally, no network:

1. Run the pre-registered Gate 4 pipeline: `python scripts/run_funding_ablations.py` (multisplit walk-forward, purge/embargo >= 7d, train-only normalization, last-known funding at/before hour, block-bootstrap ΔQLIKE CIs, honest PILOT/INCONCLUSIVE verdict when data-sufficiency criteria unmet). Confirm it runs cleanly and writes only its own pre-registered pilot outputs under research_state/ — non-confirmatory evidence only.
2. Re-run full suite: `python -m unittest discover tests -q` → must stay **>=883 OK, 0 failures**.
3. Apply `FCLR_CAMPAIGN_NEXT.md` lockdown hardening only: seam tests (empty/unreadable data path under valid prereg -> blocked with stable reason codes); CLI argparse contract edge cases on the 3 CLIs; cross-CLI parity + canonical output integrity. **No** new status-only/poller/wrapper/scheduler families, no competing handoff files, no research_state writes beyond the ablation's own pre-registered outputs, no `.github/workflows` edits.
4. Gate discipline: no confirmatory outcomes, no freeze/promote while the v5 terms blocker is unresolved; no Track A outcomes without a resume trigger + fresh pre-registration.

### Focus campaign (future agents cannot avoid the heavy work)

Run this campaign every session until a resume trigger fires; it is the only permitted forward path:

```
pip install -r requirements.txt
python -m unittest discover tests -q
python scripts/check_tracka_scope_registry_drift.py
python scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass',d['pass'],'checks',len(d['checks']))"
python scripts/fclr016_v5_admissibility_report.py --bogus 2>&1 | tail -1
python scripts/fclr016_v5_promotion_dryrun.py --bogus 2>&1 | tail -1
python scripts/run_funding_ablations.py   # Gate 4 funding-conditioned volatility ablation (P0 heavy work)
python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_resume_gate.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_operator_report.py --bogus --json 2>&1 | head -c 200
```

Acceptance: all tests pass (>=883 OK); refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged; drift 17/17 pass; bounds respected, no new families; ablation verdict honestly PILOT/INCONCLUSIVE (no claim-worthy inference claimed).

### Resume triggers (only then — preregister BEFORE outcomes)

1. **Track A/H004:** unauthenticated Hyperliquid `data/events/YYYY-MM.parquet` or `data/fills/YYYY-MM.parquet` >=2026-11 with **HTTP 200, verified content** (probe only specific months; no loop) OR admissible unauthenticated observed-liquidation source passing full-manifest GO rubric. Fresh experiment ID, prereg before outcomes, modeled!=observed.
2. **v5 terms resolved by human/legal review:** create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with verifiable facts only; `fabricated=false`, `status=RESOLVED_VERIFIED`, matching frozen scope. Reconcile refs/hashes; promote prereg to frozen only after all guards green; run package/validator/report/preflight/promotion-dryrun with `--expect-go` as applicable (no data load on refusal). Compute confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New admissible Track C data:** >=5 symbols, >=3 non-overlapping 30-day blocks, unauthenticated/admissible, fresh prereg before outcomes.

### Do-NOT

Fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete/blocked data; freeze/promote prereg while blockers exist; reopen sealed anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe absent months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files; run confirmation without fresh pre-registration + new admissible data.
