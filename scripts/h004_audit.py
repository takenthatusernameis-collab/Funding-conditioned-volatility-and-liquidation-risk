#!/usr/bin/env python3
"""Audit the HF crypto-liquidation-ticks dataset: schema, coverage, completeness per venue/symbol."""
import csv
import os
import sys
from collections import Counter, defaultdict

CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "research_state", "data_cache")
LIQ = os.path.join(CACHE, "liquidations_full_20260807.csv")
COV = os.path.join(CACHE, "coverage_20260807.csv")
TARGETS = {"BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"}

def audit_liq():
    n = 0
    first = last = None
    cols = None
    per_venue = Counter()
    per_sym_venue = Counter()
    sym_first = {}
    sym_last = {}
    with open(LIQ, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        cols = rdr.fieldnames
        for row in rdr:
            n += 1
            ts = row["ts_ms"]
            if first is None or ts < first:
                first = ts
            if last is None or ts > last:
                last = ts
            v = row["exchange"]
            s = row["symbol"]
            per_venue[v] += 1
            per_sym_venue[(s, v)] += 1
            if s in TARGETS:
                sym_first.setdefault(s, ts)
                sym_last.setdefault(s, ts)
                if ts < sym_first[s]:
                    sym_first[s] = ts
                if ts > sym_last[s]:
                    sym_last[s] = ts
    print("== liquidations_full_20260807.csv ==")
    print("columns:", cols)
    print("total rows:", n)
    print("first ts:", first, "last ts:", last)
    print("by venue:", dict(per_venue))
    print("\ntarget symbols (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT):")
    for s in sorted(TARGETS):
        c = sum(n_ for (sym, v), n_ in per_sym_venue.items() if sym == s)
        print(f"  {s}: rows={c} first={sym_first.get(s)} last={sym_last.get(s)}")

def audit_cov():
    print("\n== coverage_20260807.csv ==")
    with open(COV, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        rows = list(rdr)
    print("columns:", rdr.fieldnames)
    print("rows:", len(rows))
    tgt = [r for r in rows if r["symbol"] in TARGETS]
    for r in sorted(tgt, key=lambda x: (x["exchange"], x["symbol"])):
        print(f"  {r['symbol']:10s} {r['exchange']:6s} rows={r['rows']:>7s} first={r['first_utc']} last={r['last_utc']} usd={r['total_usd']}")

if __name__ == "__main__":
    audit_liq()
    audit_cov()