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

## 13. Immutable experiment IDs, versioning, and evidence accounting

Treat this as a long-running research program, not one model run. Allocate stable hypothesis IDs such as FCLR-H001 (incremental 24-hour volatility forecasting), FCLR-H002 (funding-extreme correction-time replication), FCLR-H003 (hypothetical boundary-breach forecast), and FCLR-H004 (observed liquidation outcomes, conditional on adequate labels). Allocate experiment IDs such as FCLR-001 for the frozen starter forecast experiment, with deterministic run IDs incorporating the UTC start time, git SHA, and configuration hash.

Maintain the following only when there is meaningful content:
- research_state/hypothesis_registry.json: each hypothesis, directional claim, estimand, status, prior tests, next falsification test, and links to immutable artifacts.
- research_state/experiment_frontier.json: ordered unfinished tasks, source/feature coverage, candidate instrument universe, blockers and next actions. Do not claim that the frontier is exhausted until the discovery procedure and pagination have been audited.
- research_state/run_manifest.json: git SHA, configuration hash, UTC timestamps, exact source vintages and data hashes, cutoff dates, split boundaries, package/runtime versions, expected/observed sample counts, result status, and artifact locations.
- research_state/result_ledger.jsonl or a documented equivalent: exactly one terminal record for every expected configuration/target/model combination, including NOT_RUN, BLOCKED, INVALID, FAILED, INCONCLUSIVE, and COMPLETE states with reasons.
- research_state/research_protocol.md: the preregistered design and decision gates, updated only by issuing a new protocol version after the prior version is frozen.
- research_state/negative_results_report.md and research_state/leakage_audit.md: maintain durable nulls, failed routes, exclusions, and adversarial findings.

Never overwrite a prior experiment, frozen configuration, opened holdout, raw source vintage, or conclusion. If the question, feature, outcome, universe, cost assumption, margin scenario, split, data source, model family or parameter changes after outcomes are inspected, create a new version/ID and explain the estimand change. Do not relabel a previously exploratory result as confirmatory. Every manifest must distinguish planned, started, completed, blocked and independently verified work. A green test suite proves only the contracts actually tested.

## 14. Mandatory frozen starter protocol: FCLR-001

Before computing any target outcome, create research_state/research_protocol.md and preregister the following starter study. First inspect source availability, but do not inspect outcome summaries or choose cutoffs based on forecast results. Freeze exact timestamp cutoffs and source hashes after a coverage-only audit and before target generation. If a material detail below is infeasible, record the precise reason and register a separate pilot/alternative version before computing its outcomes.

### Unit, timing, and universe

- Unit: one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- Forecast timestamp t is immediately after all data for the closed hour t are available. Every input must have been available by that instant. Outcomes begin with the next hourly interval; no same-bar or future data may enter a predictor.
- Build the broadest defensible, expanding universe of linear perpetual contracts discoverable automatically from public listing/instrument metadata and historical archives, including delisted contracts where evidence is available. There is no fixed top-N cutoff. Record first verified listing, last verified eligibility, migrations, symbol reuse, contract type, source coverage, and missing periods. Current survivors alone are not a valid historical universe.
- Do not make historical market-cap rankings a hard dependency for this mechanism. If credible free point-in-time ranks exist, maintain a separate descending-cap universe arm; never substitute present-day ranks for historical ranks or merge a restricted arm into the primary venue-native universe without a new protocol version.
- All model comparisons use identical forecast origins and a common eligible sample. Separately report coverage gained or lost by each feature group. Missing features remain missing; do not zero-fill or forward-fill them to make models comparable.

### Primary outcome and forecast target

The single primary outcome is the next-24-hour realized variance of mark-price returns, defined as the sum of squared log returns over the next 24 complete hourly intervals, from t+1 through t+24. Record target units and the exact mark-price field. If trustworthy historic mark-price data cannot support adequate coverage, do not silently substitute last price or index price: register a separate price-source version and label it accordingly.

Secondary target horizons are 6 hours, 72 hours and 168 hours. They are explicitly secondary; include every tested horizon/model/feature comparison in the declared multiplicity family. Do not promote a secondary horizon because it happens to perform better than the primary target.

### Frozen predictor definitions

All features are causal and computed per contract from data ending no later than t:
- RV1h, RV24h and RV168h: trailing realized variances from hourly mark-price log returns.
- Signed funding: the latest funding observation whose availability timestamp is no later than t, retaining sign and its source cadence.
- Funding extremeness: the percentile rank of absolute funding versus that contract's preceding 90 calendar days only. Require at least 30 valid historical funding observations before emitting the percentile; record the actual observation count. Also keep the signed funding value separately.
- Premium feature: mark price divided by index price minus one, only when the two fields have a valid, contemporaneous alignment under a frozen tolerance.
- Smoothing/dislocation feature: mark price divided by a 24-hour exponential moving average minus one, with the EMA computed from prior/current fully closed bars only.
- Do not invent a direct price-delay measurement. Mark/index premium and EMA distance are observable dislocation proxies, not proof that a price was delayed. Any extra predictors require a new registered version or must be declared in the original protocol before any results are inspected.

Feature standardization, scaling, transformations and missing-data eligibility must be fitted or calculated using training information only. Use the same common panel for paired comparisons to prevent coverage differences from masquerading as forecasting skill.

### Frozen baseline and nested model comparisons

Evaluate these fixed model definitions:
- B0, persistence baseline: forecast the next-24-hour realized variance using the preceding RV24h.
- B1, volatility baseline: a fixed-form HAR-style model using log RV1h, log RV24h and log RV168h as predictors of log next-24-hour realized variance.
- C1, funding-augmented model: the same model form and fitting procedure as B1, plus signed funding and the past-only 90-day absolute-funding percentile.
- C2, combined candidate: the same model form and fitting procedure, plus the C1 features and the mark/index premium and mark/EMA24 distance.

Use a transparent fixed log-linear regression procedure for B1, C1 and C2; transform forecasts back to strictly positive variance with a documented, training-only back-transformation correction. Freeze any regularization, clipping, epsilon, feature scaling, missingness, and fitting rules before outcome calculation. Do not tune model families or penalties against validation/final-holdout outcomes.

Primary contrast: C2 versus B1 on 24-hour out-of-sample QLIKE. C1 versus B1 and C2 versus C1 are registered secondary contrasts. B0 supplies a simple, interpretable baseline; report all baselines, not only the weakest one. Use paired forecast origins and identical eligible rows across the compared models.

### Splits, embargo, and inference

- Determine date boundaries from data availability alone, store them in the preregistration, and hash/freeze the eligible panel before computing results.
- Use chronological development/training, validation, and final holdout partitions in time order. Use a 60%/20%/20% chronological split as the default when the audited coverage supports it; boundaries are based on unique UTC timestamps, not randomly sampled rows.
- Apply a 7-calendar-day purge/embargo at all split boundaries because the registered secondary horizon extends to 168 hours. No target interval can overlap training, validation and test folds.
- Any feature selection or model correction is done on development/validation data. The final holdout is opened once for the frozen protocol and then permanently marked as inspected/development evidence for subsequent research.
- The minimum claim-worthy test requires at least five instruments represented in the paired out-of-sample panel, at least three non-overlapping 30-day evaluation blocks, and valid uncertainty estimation. If these are not met, report PILOT/INCONCLUSIVE and state the exact data shortfall; do not relax thresholds after seeing outcomes.
- Primary metric: paired out-of-sample QLIKE difference, defined consistently and reported as both absolute difference and relative reduction. Secondary metrics: MAE/RMSE on the stated target and rank/error diagnostics where appropriate. Event predictions additionally require Brier score, log loss, calibration, and precision-recall analysis.
- Estimate uncertainty with a reproducible block bootstrap that resamples complete UTC time blocks jointly across instruments (preserving common market shocks and serial dependence), with at least 2,000 deterministic-seed replicates if sample size permits. Report sensitivity to instrument concentration, leave-one-instrument-out results, and regime/time-block stability. If the method is infeasible, disclose why and use a pre-registered dependence-aware alternative; never replace invalid inference with an ordinary IID standard error without qualification.
- Pre-register a minimum practically meaningful improvement—default at least 2% relative reduction in primary QLIKE—before the holdout is opened. A smaller apparent gain does not pass the forecast gate unless a different justified materiality threshold was frozen in advance.
- Use a two-sided uncertainty interval for the paired loss difference and require the interval to support improvement, the practical threshold to be met, and the predeclared multiplicity rule to pass. No significance claim based on an in-sample coefficient alone.

The exact timestamp boundaries, cutoff, eligible sample definition, regression/back-transformation details, bootstrap configuration, and source hashes must be recorded in research_state/research_protocol.md before computing holdout outcomes. Changes thereafter require a new protocol/experiment ID.

## 15. Keep outcome families distinct and impose an honest liquidation-label gate

Maintain separate hypothesis and result tracks:
- Volatility forecasting from observed mark/index/contract prices.
- Direct observed liquidation-event forecasting.
- Modeled hypothetical boundary-breach forecasting.
- Funding-extreme correction-time replication.

Direct liquidation data are admissible only if source documentation and empirical audits support the temporal coverage and meaning of observed records. Check event-reporting limits, truncation, rate caps, venue scope, missing periods and known changes to collection rules. A liquidation stream that reports only a capped sample of events is not a complete event census. Absence from such a feed cannot be labeled “no liquidation.” If completeness cannot be supported, use observed events as a partial positive signal only with an explicit incomplete-label design, or do not use them for a binary absence/presence target.

For hypothetical boundary breaches, register each margin/leverage scenario before examining outcomes. Use historical contract specifications and margin-tier/liquidation rules only when their time applicability is supported. If historical maintenance-margin parameters cannot be verified, label the label as an illustrative adverse-move proxy, not a liquidation boundary. Keep long and short outcomes separate and state funding, fees, price-reference and gap assumptions. Do not claim the proxy reproduces account-specific liquidation engines, cross/portfolio margin, or actual forced liquidations.

The funding-correction paper replication is a separate secondary hypothesis with its own frozen event definition, censoring rules, eligible contracts, volatility split, and uncertainty. Report it as exact replication only if the paper's required methods and data are sufficiently available and independently reconstructed. Its correction-time association cannot substitute for evidence on volatility forecast skill, boundary breaches, or actual liquidations.

## 16. Adaptive feasibility policy: progress without weakening evidence

Maintain two separate tracks:
- Confirmatory track: preserve each frozen hypothesis, universe, source eligibility gate, sample rule, model comparison, time split, costs/margin assumptions, metric and acceptance threshold.
- Exploratory/pilot track: if the same gate remains blocked after three materially distinct documented routes spanning at least two independent source families/methods, or if structural impossibility is established by access terms, schema, date coverage or sample counts, create the smallest useful alternative experiment with a new ID. Repeating the same failed endpoint is not a distinct route.

Relax only the least damaging feasibility constraint, one at a time, and only if the estimand remains meaningful. Examples include using a verified narrower historical-instrument cohort, studying the outcome with complete public mark-price data first, using a shorter sample for a low-powered pilot, or testing the frozen anchor before any secondary analysis. Record exactly which claim becomes narrower. Do not select a relaxation based on outcomes.

Hard safeguards never relax: no look-ahead, survivorship substitution, forward fill, synthetic market evidence, silent exclusions, unregistered feature/grid expansion, paid/manual inputs, reuse of an inspected holdout as fresh confirmation, or misleading labels. An alternative analysis never clears the original blocked gate. Do not write another blocker memo and wait if there is a valid, bounded free-data or diagnostic task available; execute that task and preserve the original status.

A blocked instrument, source, target or model cell blocks only the affected cell. Continue other source discovery, usable target tracks, ingestion tests, inference audits, coverage diagnostics and preregistered hypotheses. Continue expanding instrument discovery automatically; do not stop because a first cohort has been exhausted or because the latest performance result is unfavorable.

## 17. Continuous forward testing, multiplicity, and promotion

Treat the complete, declared family as including all tried primary/secondary targets, feature ablations, thresholds, model versions, price-source arms and universe arms. Apply Holm correction or another explicitly justified method to the whole relevant family, not just the winning subset. Report unadjusted and adjusted results and every failed/not-run cell with reasons.

Once the historical holdout has been inspected, it cannot be called untouched evidence again. For ongoing evaluation, preregister the next forward block, source cutoff, exact target maturity time and metrics before its outcomes are calculated. Never evaluate a truncated forward target. Record every sequential confirmatory look. For repeated looks at the same primary hypothesis, use a persistent alpha-spending rule such as alpha_k = 0.05 / (k × (k + 1)), where k is the sequential look number; save k and the allocated alpha in the registry. If a different policy is used, justify and freeze it before the next look.

A promotion decision requires all of the following:
1. The relevant data and label gates pass.
2. The frozen out-of-sample comparison beats the declared volatility baseline on the primary target.
3. The practical materiality floor and multiplicity/uncertainty conditions pass.
4. Skill is not dominated by one coin, one venue, one brief crisis or one time block.
5. Calibration and subgroup diagnostics are acceptable for any probability forecast.
6. Independent recomputation from the stored input hashes and configuration reproduces the headline result within a declared numerical tolerance.
7. Red-team and leakage audits show no unresolved issue capable of reversing the conclusion.

If any condition fails, retain NOT_SUPPORTED, INCONCLUSIVE, EXPLORATORY_ONLY or DATA_BLOCKED as appropriate. The best model in a losing family is not a proven edge. No number of exploratory variants may rescue an unsuccessful confirmatory primary test.

## 18. Result integrity and deterministic resume

Before any grid or walk-forward run, create a complete manifest of expected model/feature/target/fold combinations. After execution, compare expected and observed keys exactly. Every expected unit must finish in exactly one terminal status; no duplicates, missing keys, silently skipped failures or partial output presented as a completed run.

Store the protocol version, grid hash, source/file hashes, preprocessing fingerprint, model specification, seed, software version, row counts before/after every filter, reason-coded exclusions, forecast count, target count, independent time-block count, per-instrument coverage, and final state in the manifest. Resume idempotently from checkpoints, reconciling by stable key rather than appending duplicate rows. Never rewrite raw inputs to repair a downstream calculation; produce a new cleaned dataset with lineage and preserve the original hash.

Add known-answer and adversarial tests for:
- future-row perturbation cannot change earlier features or forecasts;
- target intervals never overlap across splits after purge/embargo;
- funding publication/settlement times and sign are handled correctly;
- mark/index alignment respects the pre-registered timestamp tolerance;
- zero/missing funding and market observations remain missing rather than invented;
- delisted contracts and symbol migrations retain the correct identity and eligibility date;
- duplicate, out-of-order and missing pages are detected;
- censored correction events and incomplete liquidation labels are not treated as completed negatives;
- an interrupted grid resumes to the exact expected terminal-key set;
- multiplicity and sequential alpha-spending calculations are deterministic; and
- independent result recomputation matches the canonical metrics.

Run fixture tests offline as the default deterministic CI path. Use bounded live-source probes separately so a transient external outage does not randomly break ordinary unit tests. Do not use oversized raw archives or large generated ledgers to replace concise, verifiable summaries; keep bulk data/caches out of Git and store only permitted, necessary artifacts.

## 19. Per-session definition of done and research feedback

Each worker session must deliver one substantive, verifiable result: a source-probe with coverage/provenance, a tested adapter, a repaired blocker, a validated dataset/label, a preregistered experiment, a completed test block, an independent recomputation, or an explicit evidence-backed structural blocker plus execution of the next valid independent task.

Before finishing, answer in the handoff:
- What did the evidence support, contradict, or leave unknown?
- What is the strongest alternative explanation?
- Which data/label/inference limitation currently dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- What exact artifact and command/test demonstrate progress?

Read the actual branch head and latest artifacts at every session start. Inspect the full diff and verify frozen prior artifacts remain unchanged. Use stable source/experiment IDs; do not wait for manually assigned IDs. Do not declare the research complete because one worker, run, dataset or test ends. Do not spend repeated sessions on cosmetic status documents while the data, baseline, primary result or unresolved scientific gate remains untouched.

## 20. Final research status contract

Use explicit statuses per hypothesis, data track, and experiment: NOT_STARTED, SOURCE_PROBING, DATA_BLOCKED, DATA_READY, PROTOCOL_FROZEN, EXPLORATORY_ONLY, PILOT_ONLY, RUNNING, COMPLETE, NOT_SUPPORTED, INCONCLUSIVE, CONFIRMATORY_RUNNING, CONFIRMATORY_COMPLETE, FORECAST_GATE_PASSED, and OVERLAY_ELIGIBLE.

Never promote status on the basis of an HTTP 200, successful download, green CI, model convergence, a large raw point estimate, or completion of a scheduled activation. The status must be supported by the relevant manifest, tests, artifacts and review.

The initial goal is a reproducible, honest forecast test—not a positive result. If it discovers no edge, preserve the null. If data block only the direct-liquidation subproblem, continue the valid volatility track. If data quality blocks the primary test, complete the best separately registered pilot and keep confirmatory status blocked. Always leave a precise next task that the next worker can execute without user intervention.

## References to start from

- Shek, “Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates,” SSRN (posted 29 September 2026): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7529458
- Official Binance public market-data repository and archive instructions: https://github.com/binance/binance-public-data
- Binance public data archive: https://data.binance.vision/

These are starting points, not an exclusive source list. Verify current access, data rights, timestamps, and coverage directly. The protocol and analysis must stand on their own even if one of these sources becomes unavailable.
