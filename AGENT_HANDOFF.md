## Initial Task Message (2026-11-07T21:13:44Z) — Next Agentic Session

**Repo priority (by name: Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary, unblocked, measurable; (2) **Track A observed liquidation risk** — DATA_BLOCKED, no trigger (data_through 2026-10; 2026-11..2027-02 absent; Hyperliquid-only; NO re-probe); monitor/guard only; (3) **Track B modeled boundary breach** — CLOSED_NEGATIVE. Forecast gate NOT MET (H001 NOT_SUPPORTED). Gate 4 v4 EXPLORATORY_INCONCLUSIVE (confounded 2024-04..09 slice, not promotable). Gate 4 v5 NOT_READY (confirmatory NO-GO; sampled 2025-01 identity GO_PARTIAL_BOUNDED; guard active; v5 prereg pending license+completeness+freeze).

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Complete FCLR-016 bounded identity manifest for a v5-candidate boundary (NO OUTCOMES):**
1. Run bounded unauthenticated Binance Vision verification for **5 symbols (BTC/ETH/BNB/SOL/XRP)** across candidate months for a **non-overlapping v5 test window** (~2025-08-01..2025-10-29 or later; compute & document non-overlap proof vs FCLR-002/003/013/v3/v4 consumed windows before prereg). Verify `fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines` for sampled days (1,15,last per month; `--sample-days full` only if bounded). Write deterministic JSON+MD under `research_state/fclr016_local_audit/`. 2025-01 BTC/ETH already probe-matched (6 MATCH, 0 MISMATCH); extend to remaining 3 symbols and candidate months.
2. If identity GO_PARTIAL/GO for candidate scope: draft v5 prereg template documenting boundary, non-overlap proof, splits (>=3x30d), purge/embargo, train-only normalization, missing!=0, primary contrast, multiplicity/bootstrap, license/terms TODO — keep `frozen_before_outcomes=false` / "PENDING LICENSE+COMPLETENESS+FREEZE". **Do not run outcomes.**
3. If mismatches/errors: record NO-GO evidence, keep guard; do not relax. Per FCLR-014 heavy-work fallback, ship ≥1 substantive hardening/test/guardrail with green gates (e.g., guardrail blocking consumed/confounded windows 2024-01..12, 2026-07..09 and unprovenanced manifests) and record evidence in this handoff, then stop cleanly.
4. Track A: only on genuinely new unauthenticated source (ironflow >=2026-11 or admissible Hyperliquid observed-liquidation source passing strict rubric); otherwise skip re-probe.

### Bottlenecks removed this session
- Confirmatory provenance guard (FCLR-014/FCLR-016) in `scripts/run_funding_ablations.py`: confirmatory 2025+ runs fail closed (rc=2, JSON REFUSED) without `--provenance-manifest`; exploratory/pilot unaffected. Guarded and tested (rc=2 path covered by `test_confirmatory_provenance_guard_refuses_unprovenanced_2025`).
- Track A inefficiency removed: no re-probe of exhausted/absent months (2026-11..2027-02, data_through 2026-10); monitor-only until rubric-GO trigger appears.
- Gate 4 v4 closed to confirmatory: confounded 2024-04..09 slice, EXPLORATORY_INCONCLUSIVE; no threshold-shopping, no merge with v5.
- FCLR-016 bounded identity probe for 2025-01 (BTC/ETH): match=6 mismatch=0 missing=0 remote_error=0, `cache_identity_vs_binance_vision=GO_PARTIAL_BOUNDED`, `confirmatory_claim_go=NO_GO` — establishes the bounded probe pattern to extend to 5 symbols × candidate months.

### Verification commands
```bash
python3 -m unittest tests.test_funding_ablations -v
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/run_funding_ablations.py
python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days 1,15,28
python3 scripts/tracka_resume_check.py
python3 -m unittest discover -s tests -q
```

### Acceptance criteria
- All tests pass (baseline 7/7 funding ablations; full suite green).
- FCLR-016 probe writes deterministic JSON+MD under `research_state/fclr016_local_audit/`; `cache_identity_vs_binance_vision` in {GO_PARTIAL_BOUNDED, NO_GO, INCOMPLETE}; `confirmatory_claim_go=NO_GO` unless full identity+license+completeness evidence exists.
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged.
- Drift 17/17 pass; root md+json <=172; no new timestamped probe/sweep/scan/wrapper/report families at root.
- No confirmatory outcomes on unprovenanced 2025+ cache; guard active; `frozen_before_outcomes=false` on any v5 prereg draft.

### Do NOT
- Re-probe exhausted Track A months/windows; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat v4/exploratory as confirmatory; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families.

### Current gate state
- Track A=DATA_BLOCKED (no trigger; monitor-only).
- Track B=CLOSED_NEGATIVE.
- Track C/H001=NOT_SUPPORTED (forecast gate NOT MET; CI crosses zero; <3 blocks on FCLR-002 test; FCLR-008 +4.30% but CI [-0.029938,0.000524] crosses zero).
- Gate 4 v4=EXPLORATORY_INCONCLUSIVE (not promotable).
- Gate 4 v5=NOT_READY (confirmatory NO-GO; sampled 2025-01 identity GO_PARTIAL_BOUNDED; guard active; v5 prereg pending license+completeness+freeze).

**Status:** Track A=DATA_BLOCKED; Track B=CLOSED_NEGATIVE; Track C/H001=NOT_SUPPORTED; Gate 4 v4=EXPLORATORY_INCONCLUSIVE; Gate 4 v5=NOT_READY.

---

**Focus campaign (mandatory, no opt-out):** Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 bounded identity verification across symbols×months with green gates, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked on NO-GO. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions.
