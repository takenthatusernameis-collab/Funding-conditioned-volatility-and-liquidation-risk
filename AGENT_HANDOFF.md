## FCLR-NEXT-157 (archived) — 2026-11-08T18:55:54Z
Archived. State at archive (verified 2026-11-08T19:45Z, HEAD context): 935 tests OK, drift 108/108→109/109 fixed this session, resume pass 17, fclr023 45/45 draft-only/non-confirmatory (`confirmatory_outcomes_go=false, packet_ready_for_human_or_prereg_action=false, satisfied=false`), ablations PILOT/INCONCLUSIVE (CI spans 0), v5 terms EXPLICIT_BLOCKER_UNRESOLVED, Track A blocked/no trigger.

## FCLR-NEXT-158 (archived) — 2026-11-08T19:46:00Z
Archived. Session entry verified; drift 109/109 PASS; tests 935 OK; fclr023 45/45 draft-only (confirmatory_outcomes_go=false, packet_ready=false, satisfied=false); v5 terms EXPLICIT_BLOCKER_UNRESOLVED; Track A blocked/no trigger; fclr015 MATCH 6/6 GO_SAMPLED_OR_PARTIAL; fclr016 MATCH 1/1 GO_PARTIAL_BOUNDED; `run_funding_ablations.py` PILOT/INCONCLUSIVE (CI spans 0). `scripts/build_fclr002_panel_local.py` added to registry (109/109). No `.github/workflows` edits; no data fabrication; sealed anchors untouched.

## FCLR-NEXT-159 (archived/superseded) — 2026-11-08T20:06:00Z
Planned next-session task carried forward into FCLR-NEXT-160. Verified state at 2026-11-08T20:06Z: 935 tests OK, drift 109/109 PASS, resume 17 pass, fclr017 Gate 4 cache coverage audit DONE (2024-04..09, 5 symbols, global_all_months_ok=true, CONSISTENT), ablations PILOT/INCONCLUSIVE, v5 terms EXPLICIT_BLOCKER_UNRESOLVED, Track A blocked/no trigger, data_inventory.json lacks 2024-04..09 refs.

---

## NEXT SESSION INITIAL TASK — 2026-11-08T20:11:44Z (SINGLE DURABLE HANDOFF; FCLR-NEXT-160)
**SESSION ENTRY VERIFIED 2026-11-08T20:11:44Z:** `AGENT_HANDOFF.md` is the sole durable handoff (`./AGENT_HANDOFF.md` only). **No status-only work allowed next session.** Working tree clean (test side effect on `research_state/ironflow_fastpath_cache.json` reverted).

**Task ID:** FCLR-NEXT-160 (P0, heavy, unblocked, measurable) — repo-name priority: **Track C / Gate 4 funding-conditioned volatility forecasting FIRST** (local admissible Binance kline+funding cache; leakage-resistant OOS only). **Track A liquidation risk BLOCKED/no trigger** (Hyperliquid `data/events|fills` 2026-11 = 404, `data_through=2026-10`; do **NOT** re-probe absent Track A months in a loop — bottleneck removed). **Never conflate observed vs modeled (Track B).** No trading/orders; no fabricated data/terms/reviews; chronological walk-forward, train-only normalization, purge/embargo; sealed holdouts untouched; no credentials/paid/manual/API-key/bypass sources.

### Verified state (2026-11-08T20:11Z, local, no network; timestamp-only side effects restored)
- `python -m unittest discover tests -q` → **OK, Ran 935 tests** (exit 0). `check_tracka_scope_registry_drift.py` → **109/109 PASS**. `tracka_resume_check.py` → **pass:true, 17 checks, network:false**. `--bogus`/`--bogus --json` refusals parseable JSON, exit!=0, no traceback.
- `run_funding_ablations.py` → clean, honest **PILOT/INCONCLUSIVE** (primary E vs A **+4.612, 95% CI [-0.129, 13.122] spans 0**, n_obs=1819, n_blocks=41, n_reps=2000, seed=12345, block_hours=24). **No incremental forecast skill; H001 NOT_SUPPORTED; risk overlay INELIGIBLE.** Sealed `GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D` anchors untouched.
- **fclr023 latest:** 45/45 draft-only/non-confirmatory; `confirmatory_outcomes_go=false, packet_ready_for_human_or_prereg_action=false, satisfied=false`. **Not GO, not frozen, not confirmatory.**
- **Provenance identity:** fclr015 → **MATCH 6/6, `GO_SAMPLED_OR_PARTIAL`**. fclr016 → **MATCH 1/1, `GO_PARTIAL_BOUNDED`**, `placeholder_duplicate_files=0`. Identity evidence only (necessary, not sufficient); v5 terms **EXPLICIT_BLOCKER_UNRESOLVED** (`fabricated=false`); `all_go=false`.
- **fclr017 Gate 4 cache coverage audit (2024-04..09, 5 symbols, `--no-content-hash`):** `global_all_months_ok=true`, `v3_30d_calendar_consistency=CONSISTENT`, `exploratory_only=true`, `no_confirmatory_outcomes=true`, `no_network=true`. Artifacts: `research_state/fclr017_local_audit/fclr017_gate4_cache_audit_latest.json|md`. **All 5 symbols × 6 months fully covered** (klines, markPriceKlines, indexPriceKlines, premiumIndexKlines daily dirs + fundingRate; no quarantine/placeholder anomalies). **Objective 2 (coverage audit) DONE.**
- **Cache layout:** `research_state/data_cache/{SYM}_2024_{MM}/` daily-extracted layout exists for all 5 symbols × 6 months. `run_funding_ablations.py` globs find 2024-04..09 sources. `data_inventory.json` lacks 2024-04..09 refs. **Loader/layout + inventory compatibility still to be verified end-to-end.**
- Focus campaign scripts compile clean: run_funding_ablations, fclr017_gate4_cache_coverage_audit, fclr016_v5_admissibility_report, fclr016_v5_promotion_dryrun, fclr023_gate4_blocker_resolution_action_plan, check_tracka_scope_registry_drift, tracka_resume_check.

### Objective (heavy, no status-only) — measurable deltas required
1. **Integrity gate (every session):** focus campaign below; restore timestamp-only side effects; remove verify outputs. Keep `tests` OK, drift 109/109, resume 17 pass.
2. **End-to-end loader/layout compatibility (unblocked, heavy, NO outcomes):** prove Gate 4/ablations/provenance tooling can consume `research_state/data_cache/{SYM}_2024_{MM}/...` daily layout for 2024-04..09 (5 symbols) without fabrication. Produce scripted read-only audit artifact (paths, kinds, per-symbol/month counts, coverage, loader gaps) and/or minimal tmp-fixture test. If gaps exist, implement **minimal, test-backed** loader normalization for local admissible cache only. **No confirmatory model runs.**
3. **Reconcile cache inventory/manifest refs (bounded, evidence-based):** align `data_inventory.json`/manifest/hash references with actual `{SYM}_2024_{MM}` layout; compute from local files only or record explicit gaps. Deterministic, testable.
4. **Extend provenance identity evidence (bounded, NO outcomes):** resume `fclr015`/`fclr016` with bounded `--max-checks`/`--checkpoint-every` (5-symbol panel, 2024-04..09 then 2025+). Record MATCH/MISMATCH/MISSING/INCOMPLETE. **Identity only (necessary, not sufficient).**
5. **Draft (NOT freeze) loader-compatible Gate 4 prereg v4 candidate (no outcomes):** DRAFT prereg keyed to verified local coverage (>=5 sym, >=3 non-overlapping 30-day blocks, 7d purge/embargo, chronological walk-forward, train-only normalization, leakage guards, fixed seeds/bootstrap/block-aware CIs/Holm family). Mark `DRAFT_NOT_FROZEN`, `confirmatory_outcomes_permitted=false`. **Human/legal terms unresolved = hard blocker.**
6. **Deterministic test delta (>935, no network/outcomes):** add regression coverage for loader/layout normalization, inventory reconciliation, or output isolation (tmp dirs, no sealed overwrite).

### Focus campaign (mandatory every session)
```bash
pip install -r requirements.txt
python -m unittest discover tests -q
python scripts/check_tracka_scope_registry_drift.py
python scripts/tracka_resume_check.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('tracka pass', d['pass'], 'checks', len(d['checks']), 'network', d['network'])"
python scripts/fclr016_v5_admissibility_report.py --bogus 2>&1 | tail -1
python scripts/fclr016_v5_promotion_dryrun.py --bogus 2>&1 | tail -1
python scripts/run_funding_ablations.py   # Gate 4 baseline pilot; honest verdict (no outcome forcing)
python scripts/fclr023_gate4_blocker_resolution_action_plan.py   # draft-only, packet_ready=false unless evidence changes
python scripts/fclr017_gate4_cache_coverage_audit.py   # re-run if scope changes; currently CONSISTENT
```
Acceptance: **>=935 tests OK**, refusals parseable/exit!=0/no traceback, drift **109/109+**, resume **17/17**, ablations honest (CI spans 0 unless evidence changes), **measurable heavy delta delivered**. Restore timestamp-only side effects; remove verify outputs.

### Resume triggers (only then — fresh prereg BEFORE outcomes)
1. **Track A/H004:** unauthenticated Hyperliquid `data/events|fills` YYYY-MM >=2026-11 **HTTP 200 + verified content** (specific months only; no loop) OR admissible unauthenticated observed-liquidation source passing full-manifest GO. Fresh experiment ID + prereg before outcomes; modeled!=observed.
2. **v5 terms resolved (human/legal):** add `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`fabricated=false`, `status=RESOLVED_VERIFIED`, frozen scope). Promote prereg to frozen only after all guards green. Confirmatory outcomes only when real package `all_go=true` and frozen prereg hashes recorded.
3. **New claim-worthy Track C run:** loader-compatible admissible local panel, >=5 sym & >=3 non-overlapping 30-day blocks, **fresh frozen prereg before outcomes** (confirmatory within `PROVENANCED_CONFIRMATORY_RANGES` 2024-04..09; else exploratory). DRAFT preregs/identity probes/loader audits/inventory reconciliations are **not** sufficient.

### Do-NOT
Fabricate terms/license/reviews or data; run confirmatory outcomes on unprovenanced/incomplete/blocked data or without frozen prereg; freeze/promote while blockers exist; reopen sealed anchors/holdouts; threshold-shop or relax gates post-hoc; merge Track A/B/C semantics or modeled!=observed; claim economic/overlay value; re-probe absent Track A months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files.

---

## NEXT SESSION INITIAL TASK — 2026-11-08T20:17:43Z (SINGLE DURABLE HANDOFF; FCLR-NEXT-161)
**SESSION ENTRY VERIFIED 2026-11-08T20:17:43Z:** `AGENT_HANDOFF.md` sole durable handoff. No status-only work. Working tree clean.

**Task ID:** FCLR-NEXT-161 (P0, heavy, unblocked, measurable) — repo-name priority: **Track C / Gate 4 funding-conditioned volatility FIRST** (local admissible Binance kline+funding cache; leakage-resistant OOS only). Track A liquidation risk BLOCKED/no trigger (Hyperliquid 2026-11 = 404; data_through=2026-10; do NOT re-probe absent months — bottleneck removed). Track B modeled != observed, never conflate. No trading/orders; no fabricated data/terms/reviews; chronological walk-forward, train-only normalization, purge/embargo; sealed holdouts untouched.

### Verified state (2026-11-08T20:17Z)
- Tests 935 OK; drift 109/109 PASS; resume 17 pass; refusals parseable/exit!=0/no traceback.
- Abations PILOT/INCONCLUSIVE (E vs A +4.612, CI [-0.129,13.122] spans 0); H001 NOT_SUPPORTED; overlay INELIGIBLE.
- fclr023 45/45 draft-only (confirmatory_outcomes_go=false, packet_ready=false, satisfied=false).
- fclr017 Gate 4 cache coverage 2024-04..09, 5 symbols, global_all_months_ok=true, CONSISTENT.
- Loader/layout + inventory compatibility still to verify end-to-end (data_inventory.json lacks 2024-04..09 refs).

### Heavy focus campaign (mandatory every session)
```bash
pip install -r requirements.txt
python -m unittest discover tests -q
python scripts/check_tracka_scope_registry_drift.py
python scripts/tracka_resume_check.py
python scripts/run_funding_ablations.py
python scripts/fclr023_gate4_blocker_resolution_action_plan.py
python scripts/fclr017_gate4_cache_coverage_audit.py
```
Deliver measurable deltas: end-to-end loader/layout compatibility audit for `research_state/data_cache/{SYM}_2024_{MM}/` (5 symbols × 6 months) with tmp-fixture tests; reconcile `data_inventory.json`/manifest refs from local files only; extend provenance identity (fclr015/fclr016 bounded runs) identity-only; draft (NOT freeze) Gate 4 prereg v4 candidate `DRAFT_NOT_FROZEN` (confirmatory_outcomes_permitted=false); deterministic test delta >935. Restore timestamp-only side effects; remove verify outputs. Acceptance: >=935 tests OK, drift 109/109+, resume 17/17, ablations honest, measurable heavy delta.

### Do-NOT
Fabricate terms/license/reviews/data; confirmatory outcomes without frozen prereg; freeze/promote while blockers; reopen sealed anchors/holdouts; threshold-shop; merge Track A/B/C; claim economic value; re-probe absent Track A months in a loop; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families or competing handoff files.
