#!/usr/bin/env python3
"""Bounded probe acquisition for GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10 candidate symbols.

1. Ranks frozen candidate symbols by ex-ante observed label notional_usd over cached
   ironflow_events 2026-05..2026-10 (label-only computation; NOT an outcome/forecast).
2. For top candidates (excluding closed 9 and excluded prefixes): bounded first-time
   unauthenticated Hyperliquid fundingHistory (full window) + candleSnapshot 1h
   2026-05..2026-10, cached with .accessed.json + .sha256 provenance.
   Skips existing valid caches (no redundant polling). Bounded call count.
Outputs:
- research_state/tracka_hl_expansion_probe_report_<UTC>.json (ranking, acquisition status per candidate)
- caches under research_state/data_cache/hyperliquid_funding/ and hyperliquid_candles/<COIN>/
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq
import requests

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
FUNDING = CACHE / "hyperliquid_funding"
CANDLES = CACHE / "hyperliquid_candles"
LABELS = CACHE / "ironflow_events"

INFO = "https://api.hyperliquid.xyz/info"
CLOSED_NINE = {"BTC","ETH","BNB","SOL","XRP","AVAX","DOGE","LINK","SUI"}
EXCLUDE_PREFIXES = ("cash:","flx:","hyna:","io:","km:","mkts:","para:","vntl:","xyz:","kBONK","kFLOKI","kLUNC","kNEIRO","kPEPE","kSHIB")
CANDIDATES = ["ADA","LTC","DOT","TRX","ATOM","BCH","ETC","FIL","ICP","NEAR","ALGO","VET","HBAR","FTM","AAVE","UNI","CRV","SNX","COMP","MKR","SUSHI","1INCH","BAL","BNT","CTSI","ENJ","IOTA","KSM","NU","OCEAN","OMG","ONT","QTUM","ZEC","ZIL","CELO","CHZ","IOST","HOT","MTL","NEXO","PNT","REN","RSR","STMX","TROY","WAN","WAVES","ZRX"]
MONTHS = ["2026-05","2026-06","2026-07","2026-08","2026-09","2026-10"]
WINDOW_START_MS = int(datetime(2026,5,1,tzinfo=timezone.utc).timestamp()*1000)
WINDOW_END_MS = int(datetime(2026,10,31,23,59,59,tzinfo=timezone.utc).timestamp()*1000) + 999
TOP_N = 8


def iso_ms(s: str) -> int:
    return int(datetime.fromisoformat(s.replace("Z","+00:00")).timestamp()*1000)


def month_range(m: str):
    y, mo = m.split("-")
    start = iso_ms(f"{y}-{mo}-01T00:00:00Z")
    if mo == "12":
        ny, nmo = f"{int(y)+1}","01"
    else:
        ny, nmo = y, f"{int(mo)+1:02d}"
    end = iso_ms(f"{ny}-{nmo}-01T00:00:00Z") - 1
    return start, end


def post(payload, retries=6, pause=2.0):
    last = None
    for attempt in range(retries):
        try:
            r = requests.post(INFO, json=payload, timeout=30)
            if r.status_code == 200:
                try:
                    return r.json(), None
                except Exception as e:
                    last = f"JSON_ERR {e}"
            else:
                last = f"HTTP {r.status_code}"
                if r.status_code == 429:
                    time.sleep(pause*(2**attempt)+1.0)
                    continue
        except Exception as e:
            last = f"ERR {e}"
        time.sleep(pause*(1.5**attempt))
    return None, last


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_provenance(sha_p: Path, acc_p: Path, data, fetched_utc: str, coin: str, month: str | None,
                     endpoint: str, start_ms: int | None, end_ms: int | None, http_status: int = 200):
    digest = hashlib.sha256(data).hexdigest()
    sha_p.write_text(digest + "\n")
    prov = {
        "fetched_utc": fetched_utc,
        "coin": coin,
        "month": month,
        "endpoint": endpoint,
        "interval": "1h" if endpoint == "candleSnapshot" else None,
        "start_ms": start_ms,
        "end_ms": end_ms,
        "rows": len(data) if isinstance(data, list) else None,
        "sha256": digest,
        "http_status": http_status,
        "api_key_required": False,
        "requester_pays": False,
        "signature_required": False,
        "unauthenticated": True,
    }
    acc_p.write_text(json.dumps(prov, indent=2) + "\n")
    return digest


def cache_valid(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text())
        return isinstance(data, list) and len(data) > 0
    except Exception:
        return False


def rank_candidates():
    totals = {c: 0.0 for c in CANDIDATES}
    months_with_event = {c: set() for c in CANDIDATES}
    for m in MONTHS:
        p = LABELS / f"{m}.parquet"
        if not p.exists():
            continue
        df = pq.read_table(p).to_pandas()
        df = df[df["market"].str.endswith("-PERP", na=False)].copy()
        df["coin"] = df["market"].str.replace("-PERP","",regex=False)
        sub = df[df["coin"].isin(CANDIDATES)]
        for coin, g in sub.groupby("coin"):
            totals[coin] += float(g["notional_usd"].sum())
            months_with_event[coin].add(m)
    ranked = sorted(CANDIDATES, key=lambda c: totals[c], reverse=True)
    return ranked, totals, months_with_event


def main() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    summary = {"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "prereg": "research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json",
               "ranking": [], "acquisition": {}, "errors": [], "selected": []}
    ranked, totals, months_with_event = rank_candidates()
    for c in ranked:
        summary["ranking"].append({"coin": c, "label_notional_usd": totals[c],
                                   "months_with_event": sorted(months_with_event[c]),
                                   "eligible": c not in CLOSED_NINE and not c.startswith(EXCLUDE_PREFIXES) and totals[c] > 0 and len(months_with_event[c]) >= 2})
    print("ex-ante label ranking (label-only, pre-outcomes):", json.dumps(summary["ranking"], indent=2))

    eligible = [r["coin"] for r in summary["ranking"] if r["eligible"]][:TOP_N]
    print("eligible top candidates for bounded acquisition:", eligible, flush=True)

    for coin in eligible:
        coin_acq = {"funding": {}, "candles": {}}
        summary["acquisition"][coin] = coin_acq
        # --- fundingHistory (full window), new file only (not the 9 cached coins) ---
        fpath = FUNDING / f"{coin}.json"
        if not cache_valid(fpath):
            data, err = post({"type":"fundingHistory","coin":coin,"startTime":WINDOW_START_MS,"endTime":WINDOW_END_MS})
            fetched_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if err is not None or not isinstance(data, list):
                coin_acq["funding"] = {"status":"error","error":err,"fetched_utc":fetched_utc}
                summary["errors"].append(f"{coin} funding: {err}")
                time.sleep(1.0)
            else:
                fpath.write_text(json.dumps(data, separators=(",",":")))
                digest = write_provenance(FUNDING/f"{coin}.sha256", FUNDING/f"{coin}.accessed.json",
                                          json.dumps(data, separators=(",",":")).encode(), fetched_utc,
                                          coin, None, "fundingHistory", WINDOW_START_MS, WINDOW_END_MS)
                coin_acq["funding"] = {"status":"fetched","n":len(data),"fetched_utc":fetched_utc,"sha256":digest}
                print(f"{coin} funding: {len(data)} rows", flush=True)
                time.sleep(0.5)
        else:
            coin_acq["funding"] = {"status":"cached","n":len(json.loads(fpath.read_text()))}
        # --- candleSnapshot 2026-05..2026-10 ---
        coin_dir = CANDLES / coin
        coin_dir.mkdir(parents=True, exist_ok=True)
        candle_ok = 0
        for m in MONTHS:
            out = coin_dir / f"{m}.json"
            if cache_valid(out):
                coin_acq["candles"][m] = {"status":"cached","n":len(json.loads(out.read_text()))}
                candle_ok += 1
                continue
            s, e = month_range(m)
            data, err = post({"type":"candleSnapshot","req":{"coin":coin,"interval":"1h","startTime":s,"endTime":e}})
            fetched_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if err is not None or not isinstance(data, list):
                coin_acq["candles"][m] = {"status":"error","error":err,"fetched_utc":fetched_utc}
                summary["errors"].append(f"{coin} {m}: {err}")
                time.sleep(1.0)
                continue
            raw = json.dumps(data, separators=(",",":"))
            out.write_text(raw)
            digest = write_provenance(coin_dir/f"{m}.sha256", coin_dir/f"{m}.accessed.json",
                                      raw.encode(), fetched_utc, coin, m, "candleSnapshot", s, e)
            coin_acq["candles"][m] = {"status":"fetched","n":len(data),"fetched_utc":fetched_utc,"sha256":digest}
            candle_ok += 1
            print(f"{coin} {m}: {len(data)} rows", flush=True)
            time.sleep(0.5)
        if candle_ok == len(MONTHS):
            summary["selected"].append(coin)
        time.sleep(0.5)

    report_path = RS / f"tracka_hl_expansion_probe_report_{ts}.json"
    report_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"report": str(report_path), "selected": summary["selected"], "errors": summary["errors"]}, indent=2))


if __name__ == "__main__":
    main()
