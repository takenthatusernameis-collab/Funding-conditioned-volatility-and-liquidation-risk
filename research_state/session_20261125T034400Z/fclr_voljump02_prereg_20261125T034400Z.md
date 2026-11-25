# FCLR-VOL-JUMP-02 Prereg (20261125T034400Z)

- experiment_id: FCLR-VOL-JUMP-02
- session_id: session_20261125T034400Z
- frozen_before_outcomes: true
- outcome_data_inspected_before_freeze: false
- source_registry_sha256: 2ab473eca3f31a95031430cf9ca9e43813449f997e812a9b5503ccfaba185e71
- design.kind: walk_forward_classification_signed_jump_semivariance_asymmetry_nonoverlapping_leakage_hardened
- materiality_floor_rel: 0.02
- remediations: ['48h purge+embargo', 'non-overlapping forward-outcome windows (origin spacing >= 24h)', 'mark/index tolerance filter (|mark/oracle - 1| <= 0.01)', 'delisting-aware per-coin identity', 'per-coin cluster bootstrap', 'Holm across the declared family']

Outcome-blind freeze: this prereg was written before any outcome metric was computed. The jump null from FCLR-VOL-JUMP-01 is re-tested under full leakage remediation; a surviving null closes the volatility-jump arm for good.
