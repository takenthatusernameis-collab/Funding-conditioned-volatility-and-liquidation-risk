#!/usr/bin/env python3
"""Probe + extend the FCLR-012-V forward Binance panel by 2 days (bottleneck removal).

The FCLR-012-V forward window is 2026-08-07..2026-11-02 = 88 days = only 2
non-overlapping 30-day blocks, which FAILS the frozen >=3-block structural gate.
The gate needs >=90 days of forward data, i.e. data through at least
2026-11-04.  This script probes data.binance.vision (unauthenticated, admissible)
for 2026-11-03 and 2026-11-04 daily mark/index/premium klines for all 5 symbols
and downloads whatever is actually published.  Coverage-only: no outcomes.

Idempotent.  Never touches sealed panels.  No credentials.
"""
import datetime
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
BASE = "https://data.binance.vision/data/futures/um/daily"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
DAYS = ["2026-11-03", "2026-11-04"]
TIMEOUT = 60


def month_dir(sym: str, ds: str) -> Path:
    y, m, _ = ds.split("-")
    return CACHE / f"{sym}_{y}_{int(m):02d}"


def probe(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "kilo-research/1.0", "Range": "bytes=0-0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return {"url": url, "status": r.status, "ok": True,
                    "len": r.headers.get("Content-Length"), "ctype": r.headers.get("Content-Type")}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "ok": False, "reason": str(e)}
    except Exception as e:
        return {"url": url, "status": None, "ok": False, "reason": str(e)}


def fetch(url: str, dest: Path) -> str:
    if dest.exists() and dest.stat().st_size > 50:
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "kilo-research/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r, tmp.open("wb") as f:
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                f.write(chunk)
        if tmp.stat().st_size < 50:
            tmp.unlink()
            return "empty"
        tmp.replace(dest)
        return "ok"
    except Exception as e:
        if tmp.exists():
            tmp.unlink()
        return f"fail:{e}"


def extract(zip_path: Path, csv_path: Path) -> str:
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return "skip"
    try:
        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
            if not names:
                return "emptyzip"
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            csv_path.write_bytes(z.read(names[0]))
        return "ok"
    except Exception as e:
        return f"fail:{e}"


def main() -> int:
    results = {"probes": [], "downloads": {}, "extracts": {}}
    for sym in SYMBOLS:
        for ds in DAYS:
            y, m, _ = ds.split("-")
            for kind in KINDS:
                fname = f"{sym}-1h-{ds}.zip"
                url = f"{BASE}/{kind}/{sym}/1h/{fname}"
                p = probe(url)
                p["symbol"] = sym
                p["day"] = ds
                p["kind"] = kind
                results["probes"].append(p)
                if p["ok"]:
                    dest = month_dir(sym, ds) / fname
                    r = fetch(url, dest)
                    results["downloads"].setdefault(f"{sym}/{ds}/{kind}", r)
                    if r in ("ok", "skip"):
                        csv_path = month_dir(sym, ds) / f"{kind}-{ds}" / fname.replace(".zip", ".csv")
                        results["extracts"][f"{sym}/{ds}/{kind}"] = extract(dest, csv_path)
    out = REPO / "research_state" / "fclr012v_extension_probe.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    ok = sum(1 for p in results["probes"] if p["ok"])
    print(f"probed {len(results['probes'])} endpoints, {ok} available")
    print(f"wrote {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())