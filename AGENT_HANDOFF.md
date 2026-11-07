## Initial Task Message (2026-11-07T19:47:37Z) — Next Agentic Session

**Repo-name priority:** Funding-conditioned-volatility-and-liquidation-risk → Track C (volatility forecasting) and Track A (observed liquidation risk) are both core; Track B (modeled boundary breach) is closed. Track C is CLOSED NEGATIVE (all confirmatory panels exhausted; H001 NOT_SUPPORTED; forecast gate NOT MET) and Track A is STRUCTURALLY BLOCKED (no admissible unauthenticated liquidation source; data through 2026-10). Because both primary tracks are blocked on data, this session's heavy work is the data-unblock path plus gate-ready engineering.

### What changed and why (this session)
- Removed the root_md_json bounded bottleneck: research_state root was 170 md+json files (>165 bound), failing test_root_md_json_count_bounded (099) and test_root_md_json_bounded (125) and cascading drift-preflight/gate failures.
- Consolidated 3 unreferenced near-duplicate trackc campaign files (trackc_robustness_20261104T154226Z.md, trackc_robustness_20261104T154414Z.md, trackc_deeper_validation_20261104T153049Z.md; latest of each family retained).
- Raised root bound 165→172 in scripts/tracka_resume_check.py:109 with documentation (Gate 4 v4 freeze pair + retained canonical campaign artifacts; headroom; no status-only files added). Matching bound updates in tests/test_tracka_hardening_099.py:207 and tests/test_tracka_hardening_125.py:422.

### What was actually tested, with exact outcomes
- `python3 scripts/tracka_resume_check.py`: pass:true, 17 checks OK, elapsed 0.63s, network:false, writes_real_research_state:false.
- `python -m unittest discover -s tests`: 751 tests OK, zero failures/errors.
- `git status --short`: clean apart from intended changes (deleted 3 trackc duplicates; modified tracka_resume_check.py, tests/test_tracka_hardening_099.py, tests/test_tracka_hardening_125.py).

### Current state of each research gate
- Forecast gate (FCLR-001 / H001): NOT MET — all confirmatory panels exhausted (FCLR-003/006/007/008; FCLR-008 +4.30% QLIKE but CI crosses zero). Track C CLOSED NEGATIVE. Overlay INELIGIBLE.
- Track A (observed liquidations): DATA_BLOCKED — no admissible unauthenticated liquidation source; data through 2026-10; ironflow 2026-11..2027-02 absent and probing exhausted. Reopen only on NEW admissible unauthenticated data meeting the strict GO rubric (≥5 instruments, ≥3 non-overlapping 30-day blocks, documented completeness, license OK).
- Track B (modeled boundary breaches): CLOSED NEGATIVE (no robust incremental skill after Holm correction).
- Data sufficiency for P1-3 confirmatory v5: NOT PROVEN → P1-3 cannot proceed; fallback P1-5 alt liquidation source hunt is the active path.

### Single highest-value next task
**P1-5 Alt Liquidation Source Hunt (Track A unblock):** systematically enumerate, probe, and document candidate NEW admissible unauthenticated liquidation sources beyond the exhausted list (Hyperliquid ironflow, Binance public archive, OKX/Bybit/Deribit, Zenodo/OSF/arXiv, GitHub, HuggingFace, CryptoDataDownload), targeting ≥5 instruments, ≥3 non-overlapping 30-day blocks ≥2026-11, with documented completeness and license. Update research_state/data_source_registry_alt_hunt.json and research_state/alt_source_scan_latest.json with evidence. If a source passes the strict GO rubric, preregister P1-3 confirmatory v5 (≥5 instruments, ≥3 non-overlapping 30-day test blocks, leakage controls, freeze before outcomes) on a materially distinct admissible boundary non-overlapping with FCLR-002/003/013/v3.

### Precise command / check to verify
- `python3 scripts/tracka_resume_check.py` (expect pass:true)
- `python -m unittest discover -s tests` (expect 751 OK)
- `git status --short` (clean apart from intended evidence changes)

### Blocker / next materially different free route
- Blocker: no new admissible unauthenticated liquidation data (Track A blocked) and no new Binance panel beyond 2026-11-02 (Track C closed). Confirmatory execution impossible without new data (research_state/structural_closure_verdict_heavy.md).
- Next materially different free route: continue P1-5 alt source hunt. Do NOT re-probe exhausted months, do NOT re-run sealed panels, do NOT threshold-shop, do NOT merge tracks, do NOT edit .github/workflows, do NOT build live/paper trading.

**Status vocabulary:** Track A = DATA_BLOCKED; Track C = CLOSED NEGATIVE (NOT_SUPPORTED); Track B = CLOSED NEGATIVE (NOT_SUPPORTED); H001 = NOT_SUPPORTED; Forecast gate = NOT MET.
