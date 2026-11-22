# FCLR-NEXT-SOURCE-VERIFY-01 Evidence Audit

**Campaign:** `FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z`
**Session:** `20261122T033000Z` (> campaign start `20261122T013100Z`)
**Generated:** `2026-11-22T03:30:00Z`

## Audit scope
Full FCLR-NEXT-SOURCE-VERIFY-01 heavy artifact set under `research_state/session_20261122T033000Z/`. Verifies completeness, non-emptiness, stdlib-only, read-only, outcome-blind, and gate-critical `evidence_audit_` alias presence.

## Design
**ID:** `FCLR-NEXT-CONFIRM-001` (confirmatory, outcome-blind)

## Files audited
- `fclr_next_source_verify_source_registry_20261122T033000Z.{json,md}`
- `fclr_next_source_verify_prereg_20261122T033000Z.{json,md}`
- `fclr_next_source_verify_eval_20261122T033000Z.{py,json,md}`
- `fclr_next_source_verify_recompute_20261122T033000Z.{py,json}`
- `fclr_next_source_verify_evidence_audit_20261122T033000Z.{json,md}`
- `evidence_audit_20261122T033000Z.json` (gate-critical alias)
- `trigger_check_20261122T033000Z.json`

## Input CSVs (sha256 asserted)
- `data/raw/BTCUSDT-1h-2024-01-01.csv`: `9f49f465824b4c0e38dd55ab09689e5dac24a597dcc6b98bfe171c6c0837e5cd`
- `data/raw/BTCUSDT-1h-2024-01-02.csv`: `2f6de89f301a00b19ab75281d68ead3b1f83d52600f547d8c166a540ab95a833`
- `data/raw/BTCUSDT-fundingRate-2024-01.csv`: `232a13d92487efef8ce0d645301abe611f56eacb70023194b97c038d7a8a2c9b`
- `data/raw/ETHUSDT-1h-2024-01-02.csv`: `5469db0f3071b85fde30533f82c930c21e2c42c25a6aae7dad0e7345a70313f2`
- `data/raw/ETHUSDT-fundingRate-2024-01.csv`: `90e05d0f18178405391dc095e8d6e5f0a3f8fc4b46683a39855540181496f7f3`
- `data/raw/btc/BTCUSDT-1h-2024-03-08.csv`: `ab3b11117d08f60bef0d7753b21d9691b33d6f3face43b8a36bd0373598062fb`
- `data/raw/btc_funding/BTCUSDT-fundingRate-2024-03.csv`: `1ac0fa4862ab12c59a4daefa330e0b0e23374feb86c5ca9a2733cd1fa1fe1c48`

## Completeness checks
All audited files present and non-empty (> 0 bytes).

## Compliance
- Stdlib-only: yes (no numpy/pandas/scipy)
- Network used: no
- Root writes: no (root count unchanged at 499/500)
- Outcome data inspected before freeze: no
- Gate-critical alias present: yes
- Trigger check non-empty: yes

## Results
- Eval decision: GO — H1 passed in >=1 admissible block (BTCUSDT B1_2024-01 rho=0.4412 p=5.00e-05 < 0.05); H2 direction consistent (never contradicting); H3 liquidation absence confirmed.
- Recompute decision: GO — independent analytical t-approx recompute; decision matches eval; BTCUSDT B1_2024-01 p=0.00170 < 0.05.
- Agreement: decision_match=true; both BTCUSDT B1 p-values significant.

## Audit result
PASS — complete non-empty heavy artifact set; outcome-blind prereg frozen before computation; eval and independent recompute agree on decision GO; no root writes; stdlib-only; no network.
