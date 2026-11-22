#!/usr/bin/env python3
"""Bounded download of Binance public archive (data.binance.vision) for FCLR-LIVE-ARCHIVE-02.
Stdlib only. Writes raw extracts + a download manifest under the session dir.
No outcome computation here (kept separate from prereg freeze)."""
import io, json, hashlib, zipfile, csv, time, urllib.request
from datetime import date, timedelta
from pathlib import Path

SESSION = Path(__file__).resolve().parent
RAW = SESSION / "raw"
RAW.mkdir(parents=True, exist_ok=True)

BASE = "https://data.binance.vision"
SYM = "BTCUSDT"
INTERVAL = "1h"

MONTHS = ["2025-06", "2025-07", "2025-08"]  # Jun, Jul, Aug 2025
METRIC_START = date(2025, 6, 1)
METRIC_END = date(2025, 8, 18)

UA = {"User-Agent": "fclr-live-archive02/1.0 (research; unauthenticated)"}

def get(url, timeout=90):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, dict(r.headers), r.read()

def sha256(b): return hashlib.sha256(b).hexdigest()

manifest = {"generated_at": "2026-11-22T00:30:00Z", "source": BASE, "symbol": SYM,
            "files": [], "errors": []}

def save(name, content_bytes):
    p = RAW / name
    p.write_bytes(content_bytes)
    return p

# --- mark price klines (1h, monthly zips) ---
for m in MONTHS:
    url = f"{BASE}/data/futures/um/monthly/markPriceKlines/{SYM}/{INTERVAL}/{SYM}-markPriceKlines-{INTERVAL}-{m}.zip"
    try:
        s, h, b = get(url)
        p = save(f"{SYM}-markPriceKlines-1h-{m}.zip", b)
        manifest["files"].append({"kind": "markPriceKlines", "interval": INTERVAL,
                                  "month": m, "url": url, "status": s,
                                  "bytes": len(b), "etag": h.get("ETag"),
                                  "sha256": sha256(b), "saved": str(p)})
        print(f"OK mark {m} {len(b)}B {h.get('ETag')}")
    except Exception as e:
        manifest["errors"].append({"url": url, "error": str(e)})
        print(f"ERR mark {m}: {e}")
    time.sleep(0.2)

# --- funding rate (monthly zips) ---
for m in MONTHS:
    url = f"{BASE}/data/futures/um/monthly/fundingRate/{SYM}/{SYM}-fundingRate-{m}.zip"
    try:
        s, h, b = get(url)
        p = save(f"{SYM}-fundingRate-{m}.zip", b)
        manifest["files"].append({"kind": "fundingRate", "month": m, "url": url,
                                  "status": s, "bytes": len(b), "etag": h.get("ETag"),
                                  "sha256": sha256(b), "saved": str(p)})
        print(f"OK fund {m} {len(b)}B {h.get('ETag')}")
    except Exception as e:
        manifest["errors"].append({"url": url, "error": str(e)})
        print(f"ERR fund {m}: {e}")
    time.sleep(0.2)

# --- metrics (daily zips) ---
d = METRIC_START
while d <= METRIC_END:
    ds = d.isoformat()
    url = f"{BASE}/data/futures/um/daily/metrics/{SYM}/{SYM}-metrics-{ds}.zip"
    try:
        s, h, b = get(url)
        p = save(f"{SYM}-metrics-{ds}.zip", b)
        manifest["files"].append({"kind": "metrics", "day": ds, "url": url,
                                  "status": s, "bytes": len(b), "etag": h.get("ETag"),
                                  "sha256": sha256(b), "saved": str(p)})
    except Exception as e:
        manifest["errors"].append({"url": url, "error": str(e)})
        print(f"ERR metrics {ds}: {e}")
    d += timedelta(days=1)
    time.sleep(0.05)

print(f"metrics days downloaded: {sum(1 for f in manifest['files'] if f['kind']=='metrics')}")
print(f"total errors: {len(manifest['errors'])}")
(SESSION / "download_manifest.json").write_text(json.dumps(manifest, indent=2))
print("Wrote download_manifest.json")
