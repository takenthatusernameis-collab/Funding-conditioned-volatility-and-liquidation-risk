# BLOCKER EVIDENCE - Track A
**TIMESTAMP:** 20261103T060627Z
**STATUS:** BLOCKED_ON_DATA

## python scripts/monitor_ironflow_liquidations.py --verify
RC: 0
```
05",
        "kind": "fills",
        "cache_key": "fills:2026-05"
      },
      {
        "month": "2026-06",
        "kind": "events",
        "cache_key": "events:2026-06"
      },
      {
        "month": "2026-06",
        "kind": "fills",
        "cache_key": "fills:2026-06"
      },
      {
        "month": "2026-07",
        "kind": "events",
        "cache_key": "events:2026-07"
      },
      {
        "month": "2026-07",
        "kind": "fills",
        "cache_key": "fills:2026-07"
      },
      {
        "month": "2026-08",
        "kind": "events",
        "cache_key": "events:2026-08"
      },
      {
        "month": "2026-08",
        "kind": "fills",
        "cache_key": "fills:2026-08"
      },
      {
        "month": "2026-09",
        "kind": "events",
        "cache_key": "events:2026-09"
      },
      {
        "month": "2026-09",
        "kind": "fills",
        "cache_key": "fills:2026-09"
      },
      {
        "month": "2026-10",
        "kind": "events",
        "cache_key": "events:2026-10"
      },
      {
        "month": "2026-10",
        "kind": "fills",
        "cache_key": "fills:2026-10"
      }
    ],
    "stale_cache_entries": [],
    "missing_oids": [],
    "cache_incomplete": true,
    "drifted": false,
    "content_hash_missing": [],
    "content_hash_incomplete": false,
    "content_hash_complete": true
  }
}
VERIFY ok=True data_through=2026-10 consecutive_absent=3 baseline_drift=False content_hash_complete=True known_months=18

```

## python scripts/monitor_ironflow_liquidations.py --quick
RC: 0
```
Wrote evidence: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/ironflow_probe_20261103T060627Z.json
No resume trigger. data_through=2026-10 probed=['2026-11', '2026-12', '2027-01', '2027-02'] head_probes=8 cached_hits=0 probe_diff(added=0 changed=0 removed=0) baseline_drift(intact=True regressions=0 content_replaced=0 pairs_checked=36) kaggle_mirror(updated=False last=2026-11-01T06:18:48.21Z triggered=False)

```
