## Initial Task Message (2026-11-08T12:23:50Z, git HEAD `cf26002f5` + uncommitted campaign repairs only — see below; sealed artifacts untouched) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`. **Repo-name priority (enforced):** (1) **funding-conditioned volatility forecasting** (Track C / Gate 4, local admissible Binance kline+funding data — measurable, unblocked, heavy) → (2) **liquidation risk** (Track A observed / Track B modeled — **never conflated**; Track A blocked, no trigger). **Mission:** empirical/research only; **no trading/orders**; no fabricated data/terms/reviews; chronological leakage-resistant OOS only; sealed holdouts untouched; **no `.github/workflows` edits**; no credentials/paid/manual/API-key/bypass sources. **This file is the single durable handoff — do not create competing handoff/status files.**

### Session 2026-11-08T12:23Z — bottleneck removed (do not redo)
- **`research_state/run_manifest.json` repaired (genuine blocker):** manifest had been restored from `run_manifest.json.bak_fclr001` (14 funding-ablations keys) but was missing `split_boundaries_fclr010` (frozen Track A FCLR-010 boundaries: train 2025-11-01..2026-02-22 / validation 2026-03-02..2026-04-30 / test 2026-05-08..2026-08-06). This caused import-time `KeyError` in `scripts/coupled_build_panel.py` (and 11+ dependents) → 144 failures / 34 errors across Track A hardening tests and `tracka_resume_check` `pass:false`. **Fix:** merged `split_boundaries_fclr010` from git history (`a438a3aeb:research_state/run_manifest.json`, LFS-smudged read) into current manifest, preserving all existing funding-ablations/split_boundaries keys. **Do not remove `split_boundaries_fclr010`; do not replace manifest with an LFS pointer.**

### Working-tree note (not committed)
- `research_state/run_manifest.json` — campaign repair above (adds `split_boundaries_fclr010`; preserves prior keys).
- `research_state/evaluation_summary.md`, `research_state/evaluation_summary_funding.md`, `research_state/leakage_audit.md`, `research_state/ironflow_fastpath_cache.json` — refreshed by campaign re-runs (timestamps/appends only; no sealed artifact overwritten, no outcomes recomputed beyond honest pilot verdicts).
- `_v3_30d_verify` outputs created for verification and **removed** after verification per campaign rule.

### Verified 2026-11-08T12:23Z (local, no network)
- `python -m unittest discover tests -q` → **890 tests, 0 failures, OK** (88s).
- `check_tracka_scope_registry_drift.py` → **101/101 PASS**.
- `tracka_resume_check.py` → **pass:true, 17 checks, network:false**.
- `fclr016_v5_admissibility_report.py --bogus` / `fclr016_v5_promotion_dryrun.py --bogus` → parseable JSON refusals, `exit!=0`, no traceback.
- Gate 4 baseline `run_funding_ablations.py` → clean honest verdict (primary CI spans 0).
- `run_funding_ablations.py --include-cache --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --start 2024-04-01 --end 2024-09-30 --out-suffix _v3_30d_verify` → **reproduces sealed numbers exactly**: `n_obs=12969, n_blocks=120, E_vs_A point=0.4879023125556385, 95% CI [-0.042160777324701186, 1.1973379300276015] spans 0`; verify outputs removed. Sealed artifacts untouched.

### Hard stops (genuine — do NOT re-probe in loops)
1. Track A/H004 Hyperliquid `data/events|fills` 2026-11 = 404 (probed 2026-11-08T07:28Z/07:30Z), `data_through=2026-10`.
2. v5 `all_go=false`, `confirmatory_outcomes_permitted=false`, terms `EXPLICIT_BLOCKER_UNRESOLVED` (`fabricated=false`). Economic/overlay claims **INELIGIBLE**.
3. Resume only on triggers below (fresh prereg before outcomes where required).

### Current evidence state (honest; preserve nulls)
- **Gate 4 delivered (pre-registered, claim-worthy data-sufficiency MET, forecast skill NOT demonstrated):** `GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D` (5 sym BTC/ETH/SOL/XRP/BNB, 2024-04-01..2024-09-30, 4×30-day walk-forward, 7d purge/embargo, block bootstrap seed=12345 reps=2000 block=24h). Primary **E (RV+funding trails) vs A (RV-only): +0.488, 95% CI [-0.042, 1.197] spans 0** (n_obs=12969, n_blocks=120). A_rv_only best aggregate QLIKE (0.798). **Verdict: PILOT/INCONCLUSIVE on primary; no incremental forecast skill; H001 NOT_SUPPORTED; risk overlay INELIGIBLE.** Sealed: `research_state/evaluation_summary_funding_v3_30d.md`, `research_state/run_manifest_funding_v3_30d.json` (SHA-256 `774e4a9f…` / `9fd540bd…`), prereg `pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md`. **Do not re-run variants chasing significance (threshold shopping).**
- **Track C FCLR-013 (2026 Q3, 5 sym, 1×30d block):** primary C2 vs B1 -1.32%, CI crosses 0, <2% floor, block-count NOT_MET → **NOT_SUPPORTED/gate NOT_MET**. FCLR-011 sealed PASS preserved.
- **Data ceiling (local, admissible):** raw Jan–Mar 2024 zips; `research_state/data_cache` has BTC/ETH/SOL/XRP/BNB 2024-01..12 (+ extended 2025/2026 for some) in monthly `{SYMBOL}_{YYYY_MM}` layout. Claim-worthy Gate 4 satisfied by v3-30d on 2024-04..09. Extending range/design requires **fresh frozen prereg before outcomes** and admissible local panel (confirmatory only within `PROVENANCED_CONFIRMATORY_RANGES` 2024-04..09 with manifest/terms evidence; else exploratory).

### Single highest-value next task — HEAVY, measurable, unblocked (no coasting)
**FCLR-NEXT-139 (P0 — heavy Track C data/provenance engineering, no new claims): build a deterministic, read-only Gate 4 cache manifest/audit for `research_state/data_cache` 2024-04..09 (BTC/ETH/SOL/XRP/BNB) that proves coverage, source-file lineage, and integrity sufficient to justify the next *pre-registered* Track C design decision — without computing confirmatory outcomes or overwriting sealed artifacts.**
1. **Reproduce baseline first (no network):** run the focus campaign block below — all must pass before/after changes.
2. **Heavy code work:** add `scripts/fclr017_gate4_cache_coverage_audit.py` (read-only, no network, no model-outcome computation) that scans `research_state/data_cache/{SYMBOL}_{YYYY_MM}/` for 5 symbols over requested month range (default 2024-04..09). Inventory canonical 1h kline sources (`klines-*/*.zip|csv`, `markPriceKlines-*`, `indexPriceKlines-*`, `premiumIndexKlines-*` as present) and funding (`*-fundingRate-*` dir/zip/csv), record per-symbol/month file counts + deterministic hashes of source paths/metadata (and file content hashes where cheap/bounded), flag missing months/days/gaps/duplicate kinds/placeholders (reuse integrity/canonical rules where applicable; follow `fclr012v_coverage_audit.py`/`fclr015_verify_cache_provenance_2024q2q3.py` patterns as read-only evidence style, **but do not make network calls**). Emit deterministic JSON+MD under `research_state/fclr017_local_audit/` (timestamped + `*_latest` pointers) with `no_confirmatory_outcomes=true`, `exploratory_only=true`, `no_network=true`, provenance/terms caveats (v5 terms blocker unresolved; 2024-04..09 = FCLR-015 identity-verified slice only where evidenced), and explicit "audit/planning only — not GO for confirmatory outcomes".
3. **Add deterministic tests:** tmp-fixture unit tests (no network) for coverage detection, missing-month/day flagging, canonical-vs-placeholder/kind accounting, funding presence, and `no_network`/`no_confirmatory_outcomes` metadata.
4. **Measurable acceptance (no claims):** report shows 5-sym 2024-04..09 cache internally consistent with v3-30d design window (or documents exact gaps), reproducible from local files, and **does not overwrite** sealed v3 artifacts. `python -m unittest discover tests -q` → **>=890 OK, 0 failures** (higher with added tests).
5. **Gate discipline:** audit/planning evidence only — **does not** authorize confirmatory outcomes, freeze/promote, overlay, or H001 status change. Any new claim-worthy run requires **fresh frozen prereg before outcomes**; 2024-04..09 confirmatory bounded by `PROVENANCED_CONFIRMATORY_RANGES` + v5 terms/admissibility guards; v5 `all_go=false` / terms `EXPLICIT_BLOCKER_UNRESOLVED`.
6. **No** new status-only/poller/wrapper/scheduler families, no competing handoff files, no `.github/workflows` edits.

### Focus campaign (run every session — future agents must do heavy work)
```bash
pip install -r requirements.txt
python -m unittest discover tests -q
python scripts/check_tracka_scope_registry_drift.py
python scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass',d['pass'],'checks',len(d['checks']),'network',d['network']))"
python scripts/fclr016_v5_admissibility_report.py --bogus 2>&1 | tail -1
python scripts/fclr016_v5_promotion_dryrun.py --bogus 2>&1 | tail -1
python scripts/run_funding_ablations.py   # Gate 4 baseline pilot (must run clean, honest verdict)
python scripts/run_funding_ablations.py --include-cache --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --start 2024-04-01 --end 2024-09-30 --out-suffix _v3_30d_verify  # must give n_obs=12969, n_blocks=120, CI spans 0; no sealed overwrite
python scripts/fclr016_v5_admissibility_report.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_resume_gate.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_operator_report.py --bogus --json 2>&1 | head -c 200
```
Acceptance: >=890 tests OK (higher with added deterministic tests); refusals parseable/exit!=0/no traceback; drift 101/101; resume 17/17 pass; ablations honest verdict; bounds respected; **measurable heavy delta delivered** (no status-only). Remove `_v3_30d_verify` outputs after verification.

### Resume triggers (only then — preregister BEFORE outcomes)
1. **Track A/H004:** unauthenticated Hyperliquid `data/events` or `data/fills` YYYY-MM >=2026-11 with **HTTP 200 + verified content** (probe specific months only; no loop) OR admissible unauthenticated observed-liquidation source passing full-manifest GO. Fresh experiment ID + prereg before outcomes; modeled!=observed.
2. **v5 terms resolved (human/legal):** add `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (verifiable facts only; `fabricated=false`, `status=RESOLVED_VERIFIED`, frozen scope). Reconcile refs/hashes; promote prereg to frozen only after all guards green; run package/validator/report/preflight/promotion-dryrun `--expect-go` as applicable (no data load on refusal). Confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New claim-worthy Track C run:** loader-compatible admissible local panel, >=5 sym & >=3 non-overlapping 30-day blocks, **fresh frozen prereg before outcomes** (confirmatory within `PROVENANCED_CONFIRMATORY_RANGES` 2024-04..09 with manifest/terms evidence as required; else exploratory).

### Do-NOT
Fabricate terms/license/reviews or data; run confirmatory outcomes on unprovenanced/incomplete/blocked data or without frozen prereg; freeze/promote while blockers exist; reopen sealed anchors/holdouts; threshold-shop or relax gates post-hoc; merge Track A/B/C semantics or modeled!=observed; claim economic/overlay value; re-probe absent months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files.
