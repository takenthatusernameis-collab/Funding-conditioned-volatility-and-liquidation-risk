#!/usr/bin/env python3
"""FCLR-015: Bounded unauthenticated Binance Vision provenance verification for
cached 2024-04..2024-09 Binance UM futures daily 1h klines/mark/index/premium
and monthly fundingRate files under research_state/data_cache.

Admissibility evidence only (no credentials/paid/manual/API keys/auth bypass).
Does NOT run model outcomes. Writes deterministic JSON+MD artifacts.
"""
from __future__ import annotations
import hashlib, json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
OUT = REPO / "research_state" / "fclr015_local_audit"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
KINDS = [
    ("klines", "daily", "data/futures/um/daily/klines/{sym}/1h/{sym}-1h-{day}.zip"),
    ("markPriceKlines", "daily", "data/futures/um/daily/markPriceKlines/{sym}/1h/{sym}-1h-{day}.zip"),
    ("indexPriceKlines", "daily", "data/futures/um/daily/indexPriceKlines/{sym}/1h/{sym}-1h-{day}.zip"),
    ("premiumIndexKlines", "daily", "data/futures/um/daily/premiumIndexKlines/{sym}/1h/{sym}-1h-{day}.zip"),
]
FUNDING_TPL = "data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip"
BASE = "https://data.binance.vision/"
UA = {"User-Agent": "kilo-fclr015-provenance/1.0 (unauthenticated checksum verification)"}
SAMPLE_DAYS = [1, 15, 28]  # bounded; adjust per month length
TIMEOUT = 30
SLEEP = 0.05


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch(url: str):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read()
            return {"status": r.status, "bytes": len(body), "etag": r.headers.get("ETag"), "last_modified": r.headers.get("Last-Modified"), "sha256": sha256(body), "body": body, "error": None}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "bytes": 0, "etag": None, "last_modified": None, "sha256": None, "body": b"", "error": str(e)}
    except Exception as e:
        return {"status": None, "bytes": 0, "etag": None, "last_modified": None, "sha256": None, "body": b"", "error": str(e)}


def days_in_month(ym: str):
    y, m = map(int, ym.split("-"))
    import calendar
    return calendar.monthrange(y, m)[1]


def local_zip(sym: str, ym: str, kind: str, day: str | None):
    d = CACHE / f"{sym}_{ym.replace('-', '_')}"
    if kind == "fundingRate":
        p = d / f"{sym}-fundingRate-{ym}.zip"
        return p if p.exists() else None
    p = d / f"{kind}-{day}" / f"{sym}-1h-{day}.zip"
    if p.exists():
        return p
    # fallback: direct in dated folder
    for q in d.rglob(f"{sym}-1h-{day}.zip"):
        if kind in str(q):
            return q
    return None


def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results = {"timestamp_utc": ts, "method": "bounded unauthenticated HEAD/GET vs local cached zip sha256/etag", "source_base": BASE, "symbols": SYMBOLS, "months": MONTHS, "checks": [], "summary": {}}
    ok = mismatch = missing_local = missing_remote = errors = 0
    for sym in SYMBOLS:
        for ym in MONTHS:
            dim = days_in_month(ym)
            sdays = sorted(set([d for d in SAMPLE_DAYS if d <= dim] + [dim]))
            for kind, _, tpl in KINDS:
                for sd in sdays:
                    day = f"{ym}-{sd:02d}"
                    lp = local_zip(sym, ym, kind, day)
                    url = BASE + tpl.format(sym=sym, day=day)
                    rec = {"symbol": sym, "month": ym, "kind": kind, "day": day, "url": url, "local_path": str(lp.relative_to(REPO)) if lp else None}
                    if not lp:
                        rec.update({"result": "MISSING_LOCAL"}); missing_local += 1; results["checks"].append(rec); continue
                    lb = lp.read_bytes(); lsha = sha256(lb)
                    r = fetch(url); time.sleep(SLEEP)
                    rec.update({"local_bytes": len(lb), "local_sha256": lsha, "remote_status": r["status"], "remote_bytes": r["bytes"], "remote_etag": r["etag"], "remote_last_modified": r["last_modified"], "remote_sha256": r["sha256"], "remote_error": r["error"]})
                    if r["status"] != 200:
                        rec["result"] = "MISSING_REMOTE" if r["status"] in (403,404) else "REMOTE_ERROR"
                        (missing_remote if r["status"] in (403,404) else errors) if False else None
                        if r["status"] in (403,404): missing_remote += 1
                        else: errors += 1
                    elif r["sha256"] == lsha:
                        rec["result"] = "MATCH"; ok += 1
                    else:
                        rec["result"] = "MISMATCH"; mismatch += 1
                    results["checks"].append(rec)
            # funding
            lp = local_zip(sym, ym, "fundingRate", None)
            url = BASE + FUNDING_TPL.format(sym=sym, ym=ym)
            rec = {"symbol": sym, "month": ym, "kind": "fundingRate", "day": None, "url": url, "local_path": str(lp.relative_to(REPO)) if lp else None}
            if not lp:
                rec.update({"result": "MISSING_LOCAL"}); missing_local += 1; results["checks"].append(rec); continue
            lb = lp.read_bytes(); lsha = sha256(lb)
            r = fetch(url); time.sleep(SLEEP)
            rec.update({"local_bytes": len(lb), "local_sha256": lsha, "remote_status": r["status"], "remote_bytes": r["bytes"], "remote_etag": r["etag"], "remote_last_modified": r["last_modified"], "remote_sha256": r["sha256"], "remote_error": r["error"]})
            if r["status"] != 200:
                rec["result"] = "MISSING_REMOTE" if r["status"] in (403,404) else "REMOTE_ERROR"
                if r["status"] in (403,404): missing_remote += 1
                else: errors += 1
            elif r["sha256"] == lsha:
                rec["result"] = "MATCH"; ok += 1
            else:
                rec["result"] = "MISMATCH"; mismatch += 1
            results["checks"].append(rec)
    results["summary"] = {"match": ok, "mismatch": mismatch, "missing_local": missing_local, "missing_remote": missing_remote, "remote_error": errors, "total": len(results["checks"])}
    # provenance decision for cache identity
    cache_identity_go = ok > 0 and mismatch == 0 and missing_remote == 0 and errors == 0
    results["cache_identity_vs_binance_vision"] = "GO" if cache_identity_go else "NO_GO"
    results["confirmatory_claim_go"] = "NO_GO"  # still requires frozen prereg before outcomes + full manifest/integrity as applicable
    results["license_terms_note"] = "Binance Vision public historical market data; accessed unauthenticated via HTTPS. Verify Binance Vision/market-data terms before redistribution; this repo stores checksums/provenance evidence, not a claim of license grant beyond source terms."
    OUT.mkdir(parents=True, exist_ok=True)
    jp = OUT / f"fclr015_binance_vision_2024_04_09_probe_{ts}.json"
    mp = OUT / f"fclr015_binance_vision_2024_04_09_probe_{ts}.md"
    jp.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    lines = [f"# FCLR-015 Binance Vision provenance probe 2024-04..09 ({ts})",
             "", f"- method: {results['method']}", f"- source_base: {BASE}",
             f"- cache_identity_vs_binance_vision: **{results['cache_identity_vs_binance_vision']}**",
             f"- confirmatory_claim_go: **NO_GO** (frozen prereg before outcomes + leakage/split controls still required)",
             f"- summary: {json.dumps(results['summary'], sort_keys=True)}",
             "", "## Notes", results["license_terms_note"],
             "Samples: day 1,15,28,last per month × 4 kline kinds × 5 symbols + monthly fundingRate. MATCH means local cached zip sha256 == remote Binance Vision zip sha256 (and HTTP 200/ETag recorded).",
             "This verifies cache identity/provenance against Binance Vision for sampled files only; full-coverage manifest/hashes remain recommended before confirmatory Gate 4 rerun."]
    by = {}
    for c in results["checks"]:
        by.setdefault(c["result"], 0); by[c["result"]] += 1
    lines += ["", "## Result counts"] + [f"- {k}: {v}" for k,v in sorted(by.items())]
    if mismatch or missing_remote or errors:
        lines += ["", "## Failures (first 50)"]
        for c in results["checks"]:
            if c["result"] in ("MISMATCH","MISSING_REMOTE","REMOTE_ERROR"):
                lines.append(f"- {c['result']} {c['symbol']} {c['month']} {c['kind']} {c.get('day')} {c['url']} local={c.get('local_path')}")
            if len(lines) > 200: break
    mp.write_text("\n".join(lines) + "\n")
    print(json.dumps({"json": str(jp.relative_to(REPO)), "md": str(mp.relative_to(REPO)), "summary": results["summary"], "cache_identity_vs_binance_vision": results["cache_identity_vs_binance_vision"]}, indent=2))
    return 0 if cache_identity_go else 2

if __name__ == "__main__":
    sys.exit(main())
