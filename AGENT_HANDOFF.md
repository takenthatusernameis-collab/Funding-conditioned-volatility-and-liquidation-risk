## Initial Task Message (2026-11-07T21:11:29Z) — Next Agentic Session

**Repo priority (by name: Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; (2) **Track A observed liquidation risk** — blocked on admissible data (monitor/guard only, no re-probe); (3) Track B modeled boundary breach — closed negative. Confirmatory forecast gate **NOT MET** (H001 NOT_SUPPORTED). Gate 4 v4 **EXPLORATORY_INCONCLUSIVE/NOT PROMOTABLE**. Gate 4 v5 confirmatory **NOT READY** (FCLR-014 NO-GO; FCLR-016 sampled 2025-01 identity GO_PARTIAL_BOUNDED, not sufficient).

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Complete FCLR-016 bounded identity manifest for a v5-candidate boundary (NO OUTCOMES):**
1. Run bounded unauthenticated Binance Vision verification for **5 symbols (BTC/ETH/BNB/SOL/XRP)** across candidate months for a **non-overlapping v5 test window** (propose test ~2025-08-01..2025-10-29 or later; compute & document non-overlap proof vs FCLR-002/003/013/v3/v4 before prereg). Verify `fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines` for sampled days (1,15,last per month; escalate to `--sample-days full` only if bounded). Write deterministic JSON+MD under `research_state/fclr016_local_audit/`.
2. If identity GO_PARTIAL/GO for candidate scope: draft v5 prereg template documenting boundary, non-overlap proof, splits (>=3x30d), purge/embargo, train-only normalization, missing!=0, primary contrast, multiplicity/bootstrap, license/terms TODO — keep `frozen_before_outcomes=false` / "PENDING LICENSE+COMPLETENESS+FREEZE". **Do not run outcomes.**
3. If mismatches/errors: record NO-GO evidence, keep guard; do not relax.
4. Track A: only on genuinely new unauthenticated source; otherwise skip re-probe.

### Bottlenecks removed this session
- Confirmatory provenance guard (FCLR-014/FCLR-016) in `scripts/run_funding_ablations.py`: confirmatory 2025+ runs fail closed (rc=2, JSON REFUSED) without `--provenance-manifest`; exploratory/pilot unaffected.
- FCLR-016 bounded identity probe for 2025-01: match=6 mismatch=0 missing=0 remote_error=0, `cache_identity_vs_binance_vision=GO_PARTIAL_BOUNDED`, `confirmatory_claim_go=NO_GO`.

### Verification commands
```bash
python3 -m unittest tests.test_funding_ablations -v
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/run_funding_ablations.py
python3 scripts/run_funding_ablations.py --start 2025-01-01 --end 2025-06-30 --confirmatory --experiment-id GATE4-V5-CONFIRMATORY --pre-registration prereg_v5_confirmatory.md --out-suffix _v5 --include-cache
python3 scripts/tracka_resume_check.py
python3 -m unittest discover -s tests -q
```

### Acceptance criteria
- All tests pass (baseline 7/7 funding ablations; full suite green).
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged.
- Drift 17/17 pass; root md+json <=172; no new timestamped probe/sweep/scan/wrapper/report families at root.
- No confirmatory outcomes on unprovenanced 2025+ cache; guard active.

### Do NOT
- Re-probe exhausted Track A months/windows; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat v4/exploratory as confirmatory; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`.

**Status:** Track A=DATA_BLOCKED; Track B=CLOSED_NEGATIVE; Track C/H001=NOT_SUPPORTED (forecast gate NOT MET); Gate 4 v4=EXPLORATORY_INCONCLUSIVE; Gate 4 v5=NOT_READY (confirmatory NO-GO; sampled 2025-01 identity GO_PARTIAL_BOUNDED; guard active).

---
