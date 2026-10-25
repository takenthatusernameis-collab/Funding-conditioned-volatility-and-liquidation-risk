# Continuous Research Agent Prompt — Funding-Conditioned Volatility and Liquidation Risk

## Mission

Continuously and autonomously investigate whether extreme perpetual-futures funding conditions, realized volatility, and pre-specified delayed/smoothed-price features improve forecasts of future volatility and liquidation-related stress. Begin with forecast validation; do not build a risk-reduction or position-sizing overlay until an out-of-sample forecasting gate passes.

Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk

This is an empirical research and engineering workflow only. It must never place, simulate live, or paper-trade orders. The end product is an auditable answer about predictive value, not a promise of trading profitability.

## 1. Non-negotiable constraints

- Use only data and software that can be accessed and run automatically without payment, paid trials, paid plans, account registration, personal API keys, manual downloads, user-provided files, or human approval to continue ordinary research.
- Never request credentials or ask the user to unblock a source. Do not bypass access controls, regional restrictions, rate limits, or usage terms. Exclude sources that require payment, a signup, a manually issued key, or requester-pays transfer charges from the core pipeline.
- A source described as “free” is not automatically admissible. Verify the actual unauthenticated download path, relevant history, schema, licensing, and limits before integrating it.
- Preserve raw-source provenance, timestamps, dataset versions/hashes where practical, and reproducible transformations. Never fabricate data or silently replace unavailable values with zeroes.
- Separate observed liquidation events from modeled or synthetic liquidation-boundary breaches. Never label a modeled proxy as an observed liquidation.
- Use chronological, leakage-resistant out-of-sample evaluation. Do not use a random train/test split for time-series claims. Do not tune thresholds or models against the sealed final holdout.
- Freeze the research protocol before examining the holdout. Preserve negative and inconclusive results. Correct for multiple comparisons and dependence.
- No live trading, paper trading, API order endpoints, account operations, exchange accounts, wallet signing, or deployment of trading logic.
- Keep the task within this repository. Do not modify other repositories as part of this work.
- Do not modify any file under .github/workflows without explicit maintainer authorization. Treat the current workflow as a protected control plane. If workflow code itself must change, document the exact blocker and smallest proposed patch, but do not make it.
- Do not add redundant controllers, schedulers, agents, polling loops, status-only files, repeated wrappers, or endless retry loops. Every iteration must create measurable research, data, testing, or engineering progress.

## 2. Required operating loop and prompt improvement

At the start of every worker session:

1. Read this file and AGENT_HANDOFF.md completely, then inspect the working tree, recent commits, current research artifacts, tests, source registry, and latest run manifest. Treat repository state and evidence as authoritative; do not assume that earlier prose remains current.
2. Improve the immediate task plan through six brief passes: scope and state; data feasibility; scientific validity; automation and cost; adversarial leakage/quality; smallest verifiable execution. Save the revised task plan in a durable research note only when it adds information, changes priorities, or records a decision.
3. Choose the highest-value unfinished task that can be completed in this session without credentials or human intervention.
4. Execute it, run the cheapest relevant deterministic checks first, then broader checks that are justified.
5. Record exact changes, commands, results, uncovered issues, and the next actionable task in AGENT_HANDOFF.md and the applicable research-state artifact.
6. Commit nothing merely to show activity. If no meaningful progress is possible, write the evidence for the blocker, identify the next materially different route, and stop that session cleanly.

Use bounded downloads, pagination, retries, and compute. Add exponential backoff with a maximum retry budget and honor source rate limits. Cache valid responses, checkpoint incremental work, and resume rather than restart. A transient endpoint failure is not evidence that an entire source family is unusable; repeated retries without new evidence are not progress either.

## 3. Hypothesis and evidence boundary

### Primary research question

Do funding extremes, realized volatility, and a pre-specified price dislocation/smoothing feature set improve out-of-sample forecasts of:

1. Future realized volatility or volatility stress; and
2. The probability of crossing a clearly defined hypothetical liquidation boundary, or an actual liquidation-risk outcome if reliable freely accessible historical liquidation labels exist?

The combined predictors must be compared against a simple realized-volatility-only baseline. The incremental value of funding and price features matters more than a significant standalone association.

### Secondary replication question

The working paper “Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates” (Helvin Shek, posted 29 September 2026) reports 1,696 events across 18 Binance perpetual contracts and median time to funding-extreme correction of 27 hours in high-volatility conditions versus 3 hours in low-volatility conditions. It also reports a lower correction hazard with higher realized volatility. Paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7529458

Treat these numbers as a working-paper claim to be independently assessed, not as established truth and not as proof of liquidation predictability. Correction time, future volatility, a hypothetical margin-boundary breach, and an observed forced liquidation are different outcomes. Do not conflate them. Do not copy or redistribute the paper itself; cite it and record the version and methodology actually reviewed.

Test whether the reported funding-correction pattern can be independently reconstructed from admissible public data and a pre-specified event definition. If the paper's full methodology or data cannot be independently obtained, state that the replication is partial rather than claiming an exact replication.

## 4. Start by establishing the repository baseline and fixing ordinary-code blockers

Inspect the repository and workflow expectations before building a large pipeline. Establish what exists, what is missing, what has run, and what the last remote-verified commit is. At initial inspection, the repository contained a general Kilo workflow and an empty workflow diagnostics ledger, but no normal research implementation or root research handoff was visible. Recheck rather than assuming that state persists.

Audit references made by the existing workflow to scripts, tests, progress ledgers, and research handoffs. If an ordinary non-workflow artifact required by the controller is missing, implement the smallest compatible script and focused tests outside .github/workflows. Do not guess at controller semantics: derive them from all call sites, workflow summaries, existing tests in the repository, and deterministic behavior. Do not report an agent-loop repair as verified until the added code has been tested and an actual eligible run validates the behavior. Never invent a completed Actions run.

Establish a minimal, understandable research layout as required, such as:

- research_state/research_protocol.md — frozen hypothesis, targets, features, splits, baselines, thresholds, and decision gates.
- research_state/data_source_registry.json — source access, fields, ranges, gaps, terms, tests, and acceptance status.
- research_state/run_manifest.json — run ID, git SHA, UTC times, configuration, data hashes, sample counts, software versions, results status, and blocker state.
- research_state/hypothesis_registry.json — stable IDs for the primary and secondary hypotheses and each status transition.
- research_state/evaluation_summary.md — current results, including metrics and uncertainty only where computed.
- research_state/negative_results_report.md — null, failed, and inconclusive outcomes, preserved with explanations.
- research_state/leakage_audit.md — timestamp, label, split, universe, and transformation checks.
- AGENT_HANDOFF.md — durable next task and session-to-session continuity.
- tests/ — small fixture-based tests for new logic and regression cases.

Do not generate empty placeholder files for every suggested artifact merely to satisfy a checklist. Create and maintain each artifact when its contents are meaningful. Keep bulky raw data and caches out of Git; commit code, concise manifests, provenance, and reports. Make clean-clone reproduction possible.

## 5. Free data discovery and acceptance

Do not prematurely conclude that no liquidation labels exist. Enumerate, test, and rank admissible sources. At the same time, do not let an unattainable direct-liquidation dataset block all valid volatility-forecast research.

### Initial source families to verify

- Official Binance public market-data archive: https://github.com/binance/binance-public-data
  Investigate public USDⓈ-M perpetual funding-rate archives, contract klines, mark-price klines, index-price klines, premium-index klines, public metrics/open-interest series, and any currently available public liquidation snapshots. Check real paths, checksums, coverage, timestamp semantics, delisted symbols, and gaps with small requests before doing full historical backfills.
- Public unauthenticated exchange APIs for historical funding, mark prices, index prices, klines, and instrument metadata. Verify each endpoint's actual history depth, pagination, geofencing, and authentication requirements.
- Public GitHub, Zenodo, Hugging Face, institutional or academic archives that provide downloadable historical liquidation/event records without signups, API keys, payment, or manually supplied files.
- Other venue-native historical archives with lawful, unauthenticated downloads and sufficient overlap across required features and outcomes.

For each source, store the exact URL/endpoint, access date, test method, no-auth result, license/terms, fields, earliest/latest timestamp, observed cadence, symbol/venue coverage, known gaps, file hashes or ETags where feasible, data revision limitations, and rejection reason if inadmissible.

Do not assume that a REST endpoint provides complete historical labels because it returns recent records. A live-only public stream does not reconstruct the past. A current API response cannot establish a historical point-in-time universe by itself. An exchange endpoint that requires a signed request or account credential is not an unauthenticated source. Do not use a requester-pays archive in the core pipeline.

### Separate source tracks

Track A — observed liquidation labels: use only when actual historical forced-liquidation records are available with defensible provenance and adequate coverage. Record venue scope and label construction. Missing event coverage must not be interpreted as zero liquidations.

Track B — modeled boundary-breach labels: use public historical mark-price data plus documented, publicly available contract/margin parameters that can be verified without login. Predefine hypothetical leverage/margin scenarios and calculate whether the observed mark-price path would have crossed the modeled boundary. Clearly call this a synthetic or modeled breach proxy. State that it does not reconstruct account-specific liquidation mechanics, portfolio margin, liquidation engine execution, or actual forced liquidations.

Track C — volatility/stress outcomes: construct directly from admissible public price/mark-price history. This track can proceed even if actual liquidation labels are unavailable.

Never silently merge these tracks or describe Track B/C performance as proof that actual liquidations were forecast.

## 6. Universe and data engineering

Build an expanding, auditable universe of perpetual instruments using archival listing/delisting metadata and the widest defensible historical coverage. Where reliable, freely accessible point-in-time market-cap rankings exist, use them as a parallel descending-cap universe. If those historical ranks require paid data, credentials, manual data, or unverifiable hindsight reconstruction, do not let that block all work: preserve a separate venue-native historical-universe track and explicitly state that it answers a different question. Never use today's surviving symbols as if they were the historical universe.

Implement restartable incremental ingestion with:

- deterministic source paths and pagination;
- raw-file checksums and manifest updates;
- duplicate detection and idempotent merges;
- UTC-normalized timestamps while preserving original values and source units;
- schema and unit validation;
- explicit mapping of venue-specific symbols and contract types;
- handling of listing, delisting, migration, and ticker reuse;
- gap and stale-row diagnostics;
- source-to-feature lineage and source-specific caveats;
- bounded memory and download sizes; and
- fixture-based repeatability without internet access.

Investigate historical timestamp-unit or column-definition changes, interval-label changes, archive revisions, symbol reuse, and missing files. Compare file boundaries and sampled rows across adjacent periods. Do not repair suspicious historical records by guessing; quarantine them with provenance and quantify the impact.

Use independent source cross-checks where they can actually validate a claim. Do not add fragile multi-source dependencies just for the appearance of robustness.

## 7. Freeze features, targets, and a compact research grid

Write a protocol and freeze it before reading holdout outcomes. Start with simple interpretable features; do not launch unconstrained machine-learning searches.

### Candidate predictors — all computed with information available at the forecast timestamp

Funding features:
- signed funding rate, retaining positive and negative sides separately;
- absolute funding rate as a distinct feature, not a replacement for signed values;
- trailing-only funding percentile or standardized funding score, with thresholds computed only from prior observations;
- time-to-next-funding / funding interval information only where it was actually knowable at prediction time.

Realized-volatility features:
- trailing 6-hour, 24-hour, and 7-day realized volatility;
- pre-specified volatility ratio such as RV24/RV168 where coverage is valid;
- a simple lagged volatility baseline/persistence feature.

Price-dislocation or smoothing features:
- perpetual premium versus index and, where aligned data is freely available, spot/perpetual basis;
- mark-to-index and mark-to-last differences using correctly aligned timestamps;
- difference between current price and a pre-specified trailing moving average or exponentially smoothed price;
- lagged price changes only if the lag is explicit and available at forecast time.

Measure feature availability and survivorship carefully. Treat missing spot/reference data as missing, not as zero basis. Do not invent a “delay” variable: define an observable proxy and explain what it represents.

### Targets

1. Primary volatility target: forward realized variance/volatility over pre-registered horizons such as 6h, 24h, 72h, and 7d. Start with a compact core subset and label any additional horizon as a registered secondary analysis.
2. Boundary-breach target: whether future mark prices breach the precomputed hypothetical long or short liquidation boundary within a pre-specified horizon under disclosed margin/leverage assumptions. Keep long and short labels separate; account for funding/cost assumptions if modeled.
3. Observed liquidation target: event or liquidation-notional intensity, only for Track A source periods/venues that pass the direct-label quality gate. Normalize notional by a defensible contemporaneous scale such as open interest or volume where available, while retaining raw counts and source limits.
4. Secondary correction-time target: time until a funding extreme crosses its frozen normalization threshold, with censored events handled using survival methods where justified.

Freeze a small first grid before holdout evaluation. Suggested initial dimensions are two or three trailing funding normalization windows, a small number of tail thresholds, the specified volatility/price feature ablations, and the core target horizons. Set exact values in the protocol before examining holdout outcomes. Avoid an unbounded Cartesian product.

Use feature ablations to isolate incremental information:
- Baseline 1: historical/persistence baseline.
- Baseline 2: realized-volatility-only (including a transparent HAR-style regression if feasible).
- Candidate 1: realized volatility plus funding features.
- Candidate 2: realized volatility plus funding plus the frozen price-dislocation/smoothing features.
- For event labels, use a simple calibrated logistic model as a baseline before attempting a more complex classifier.

The candidate's value is the out-of-sample improvement over the volatility-only baseline, not the fact that funding or volatility has an in-sample coefficient with a small p-value.

## 8. Leakage-resistant evaluation and statistical acceptance

- Use chronological walk-forward or expanding-window evaluation. If using fixed train/validation/test blocks, set the boundaries from data coverage before evaluating model outcomes.
- Use a sealed final holdout. Tune and choose features only inside the training/validation period. Keep a record of when the protocol was frozen.
- Purge or embargo overlapping label windows by at least the maximum forward horizon. Never allow the same future price path to leak across adjacent folds.
- Normalize features with training-period parameters only. Compute quantile thresholds from rolling historical information, never from the full sample.
- Handle serial correlation, cross-sectional dependence, overlapping horizons, event clustering, and rare-label imbalance. Prefer block or cluster-aware uncertainty estimates.
- Correct across pre-registered comparisons, for example with Holm familywise-error correction. Show raw and adjusted results and disclose the whole tested family.
- Report sample sizes, event prevalence, excluded rows, coverage by asset/venue/era, confidence intervals, calibration, and robustness checks—not just p-values.
- Test time periods and symbols separately enough to reveal concentration in one event or a small number of instruments.
- Preserve a strict distinction between statistical association, incremental forecast skill, hypothetical boundary prediction, observed liquidation prediction, and economic benefit.

### Metrics

Volatility forecast:
- QLIKE as a primary measure where its assumptions are appropriate;
- MAE/RMSE on a clearly defined realized-volatility or log-volatility target;
- out-of-sample loss relative to the realized-volatility-only baseline with block-aware confidence intervals.

Binary breach / stress forecast:
- Brier score and log loss, calibration slope/intercept, precision-recall performance for rare outcomes, and ROC-AUC as a secondary descriptive metric;
- precision/recall at a pre-specified alert budget or risk tolerance, not a threshold chosen after seeing the test results.

Survival/correction-time replication:
- survival curves, median correction times with uncertainty, proper censoring treatment, and cluster-aware inference by contract and time where sample size permits.

Observed liquidation-volume forecasts:
- an explicitly defined intensity target, scale normalization, lead-time constraints, and missing-event coverage diagnostics. Do not treat venue reporting gaps as zero.

Any final claim must include uncertainty estimates and be reproducible from recorded configuration and data hashes.

## 9. Gate before any risk overlay

Do not create or evaluate a position-sizing/risk-reduction overlay until the forecast results pass a gate defined in research_state/research_protocol.md before the sealed holdout is opened.

The gate must require:
- a meaningful out-of-sample improvement over the realized-volatility-only baseline on at least one pre-registered primary target;
- uncertainty that supports incremental skill after the declared multiple-testing treatment;
- acceptable calibration for event-probability predictions;
- evidence across multiple time blocks and more than one instrument rather than one crisis or one coin driving the result;
- no unresolved leakage, source, label, or timestamp defect; and
- practical relevance for the stated decision horizon.

If the gate fails, retain the null/negative outcome and continue only with a materially justified, separately registered test—not threshold shopping.

If the gate passes, a second phase may evaluate a purely hypothetical historical risk-reduction overlay with frozen rules and realistic costs. Compare it against no overlay and a simple volatility-only overlay. Report effects on tail loss/drawdown, exposure reduction, missed opportunities, turnover, and return distribution. Do not use the same holdout to design the overlay and then claim unbiased performance. There must be a separate forward/holdout evaluation for overlay decisions. No live or paper trading.

## 10. Continuous research priorities

Work through these priorities in order, adapting only when logged evidence justifies it:

1. **State and controller audit:** inspect the current repository; verify whether the existing general-agent workflow can reliably read the handoff, checkpoint meaningful changes, and preserve progress. Repair missing ordinary code/tests outside protected workflow paths when directly required by existing call sites. Never change the workflow itself without authorization.
2. **Source feasibility map:** test small unauthenticated requests for price, mark/index, premium, funding, and direct liquidation history. Publish exact evidence of what is accessible.
3. **Minimum viable dataset:** build one instrument/venue pipeline end-to-end and prove schema, timestamps, labels, checksums, and restartability before scaling.
4. **Label decision:** decide whether Track A is viable. If not, explicitly open Track B and Track C without claiming that they replace direct observed liquidation validation.
5. **Protocol freeze:** preregister primary target(s), feature ablations, splits, metrics, correction method, and gate.
6. **Baseline first:** evaluate simple persistence and realized-volatility-only baselines; confirm target construction and sample size.
7. **Incremental features:** compare funding features, then add price-dislocation/smoothing features via registered ablations.
8. **Adversarial audits:** challenge timestamping, delisting, missingness, market stress concentration, survivorship, label construction, threshold drift, and overlapping outcomes.
9. **Out-of-sample inference:** run the frozen primary analysis, preserve complete results, and issue a scientifically honest verdict.
10. **Overlay only if eligible:** only after the forecast gate passes.

Do not spend multiple agent sessions polishing documentation, status printers, or the orchestration system while the core missing dataset, label, baseline, or out-of-sample analysis remains unresolved. Engineering repairs should directly unblock a verifiable research step.

## 11. Required status vocabulary

Use these statuses consistently and only with supporting evidence:

- NOT_STARTED
- SOURCE_PROBING
- DATA_BLOCKED
- DATA_READY
- PROTOCOL_FROZEN
- BASELINE_RUNNING
- EXPLORATORY_ONLY
- CONFIRMATORY_RUNNING
- CONFIRMATORY_COMPLETE
- NOT_SUPPORTED
- INCONCLUSIVE
- FORECAST_GATE_PASSED
- OVERLAY_ELIGIBLE

Do not mark a gate as passed because the code runs, the tests pass, an endpoint returns HTTP 200, a model converges, or a workflow completes. A source is accepted only after its schema, historical coverage, provenance, and intended label use have passed checks. A research claim is accepted only after the corresponding analysis and audit have passed.

## 12. Minimum deliverables and handoff contract

At each meaningful milestone, the repository should contain:

- a tested source inventory and small source-probe fixtures;
- a frozen protocol with hypotheses and target definitions;
- restartable ingestion and validated feature/label construction;
- deterministic tests for timestamp units, pagination, missing history, duplicates, delistings, symbol mapping, forward-label leakage, and split embargoes;
- run manifests with data hashes, git SHA, timestamps, configurations, sample counts, and success/failure status;
- evaluation and negative-result reports; and
- a durable handoff that specifies the next action, its expected artifact, acceptance test, and what must not be repeated.

At the end of every session, AGENT_HANDOFF.md must say:
1. what changed and why;
2. what was actually tested, with exact outcomes;
3. what evidence was added and where;
4. the current state of each research gate;
5. the single highest-value next task;
6. the precise command or check that can verify it; and
7. any source or engineering blocker, with evidence and the next materially different free route.

Do not claim success from prose alone. Make it possible for the next agent to continue from the persisted repository state without asking the user to repeat instructions.

## References to start from

- Shek, “Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates,” SSRN (posted 29 September 2026): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7529458
- Official Binance public market-data repository and archive instructions: https://github.com/binance/binance-public-data
- Binance public data archive: https://data.binance.vision/

These are starting points, not an exclusive source list. Verify current access, data rights, timestamps, and coverage directly. The protocol and analysis must stand on their own even if one of these sources becomes unavailable.
