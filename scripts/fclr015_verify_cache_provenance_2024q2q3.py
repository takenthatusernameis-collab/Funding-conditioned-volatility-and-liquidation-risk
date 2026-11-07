#!/usr/bin/env python3
"""FCLR-015: Bounded unauthenticated Binance Vision provenance verification for
cached 2024-04..2024-09 Binance UM futures daily 1h klines/mark/index/premium
and monthly fundingRate files under research_state/data_cache.

Admissibility evidence only (no credentials/paid/manual/API keys/auth bypass).
Does NOT run model outcomes. Writes deterministic JSON+MD artifacts.
"""
from __future__ import annotations
import hashlib, json, os, os, sys, time, urllib.request, urllib.error
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


def _check_key(rec):
    return (rec.get("symbol"), rec.get("month"), rec.get("kind"), rec.get("day"))

def _write_artifacts(results, ts, suffix=""):
    OUT.mkdir(parents=True, exist_ok=True)
    jp = OUT / f"fclr015_binance_vision_2024_04_09_probe{suffix}_{ts}.json"
    mp = OUT / f"fclr015_binance_vision_2024_04_09_probe{suffix}_{ts}.md"
    jp.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    by = {}
    for c in results["checks"]:
        by.setdefault(c["result"], 0); by[c["result"]] += 1
    lines = [f"# FCLR-015 Binance Vision provenance probe 2024-04..09 ({ts}{suffix})",
             "", f"- method: {results['method']}", f"- source_base: {BASE}",
             f"- cache_identity_vs_binance_vision: **{results['cache_identity_vs_binance_vision']}**",
             f"- confirmatory_claim_go: **NO_GO** (frozen prereg before outcomes + leakage/split controls still required)",
             f"- summary: {json.dumps(results['summary'], sort_keys=True)}",
             "", "## Notes", results["license_terms_note"],
             "Sampling: day 1,15,28,last per month × 4 kline kinds × 5 symbols + monthly fundingRate (bounded). Use --full-days for exhaustive daily coverage.",
             "MATCH means local cached zip sha256 == remote Binance Vision zip sha256 (HTTP 200/ETag recorded). Full-coverage manifest/hashes recommended before confirmatory Gate 4 rerun."]
    lines += ["", "## Result counts"] + [f"- {k}: {v}" for k,v in sorted(by.items())]
    if any(c["result"] in ("MISMATCH","MISSING_REMOTE","REMOTE_ERROR") for c in results["checks"]):
        lines += ["", "## Failures (first 80)"]
        n = 0
        for c in results["checks"]:
            if c["result"] in ("MISMATCH","MISSING_REMOTE","REMOTE_ERROR"):
                lines.append(f"- {c['result']} {c['symbol']} {c['month']} {c['kind']} {c.get('day')} {c['url']} local={c.get('local_path')}")
                n += 1
                if n >= 80: break
    mp.write_text("\n".join(lines) + "\n")
    return jp, mp

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-days", action="store_true", help="Check every calendar day (exhaustive; slow)")
    ap.add_argument("--resume", help="Path to partial JSON to resume from (skips completed MATCH/MISMATCH/MISSING_LOCAL keys)")
    ap.add_argument("--checkpoint-every", type=int, default=25)
    ap.add_argument("--max-checks", type=int, default=0, help="Stop after N checks (0=unlimited)")
    args = ap.parse_args()
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    done = {}
    if args.resume and os.path.exists(args.resume):
        try:
            prev = json.loads(Path(args.resume).read_text())
            for c in prev.get("checks", []):
                done[_check_key(c)] = c
            print(f"resumed {len(done)} checks from {args.resume}", file=sys.stderr)
        except Exception as e:
            print(f"resume failed: {e}", file=sys.stderr)
    method = "bounded unauthenticated GET vs local cached zip sha256/etag" + (" (full days)" if args.full_days else " (sampled days)")
    results = {"timestamp_utc": ts, "method": method, "source_base": BASE, "symbols": SYMBOLS, "months": MONTHS, "checks": list(done.values()), "summary": {}, "resumed_from": args.resume}
    pending = []
    for sym in SYMBOLS:
        for ym in MONTHS:
            dim = days_in_month(ym)
            sdays = list(range(1, dim + 1)) if args.full_days else sorted(set([d for d in SAMPLE_DAYS if d <= dim] + [dim]))
            for kind, _, tpl in KINDS:
                for sd in sdays:
                    day = f"{ym}-{sd:02d}"
                    k = (sym, ym, kind, day)
                    if k not in done:
                        pending.append(("kline", sym, ym, kind, day, tpl))
            k = (sym, ym, "fundingRate", None)
            if k not in done:
                pending.append(("funding", sym, ym, "fundingRate", None, FUNDING_TPL))
    nchecks = 0
    for item in pending:
        if args.max_checks and nchecks >= args.max_checks:
            break
        typ, sym, ym, kind, day, tpl = item
        if typ == "funding":
            lp = local_zip(sym, ym, "fundingRate", None)
            url = BASE + tpl.format(sym=sym, ym=ym)
            rec = {"symbol": sym, "month": ym, "kind": "fundingRate", "day": None, "url": url, "local_path": str(lp.relative_to(REPO)) if lp else None}
        else:
            lp = local_zip(sym, ym, kind, day)
            url = BASE + tpl.format(sym=sym, day=day)
            rec = {"symbol": sym, "month": ym, "kind": kind, "day": day, "url": url, "local_path": str(lp.relative_to(REPO)) if lp else None}
        if not lp:
            rec.update({"result": "MISSING_LOCAL"}); results["checks"].append(rec); nchecks += 1; continue
        lb = lp.read_bytes(); lsha = sha256(lb)
        r = fetch(url); time.sleep(SLEEP)
        rec.update({"local_bytes": len(lb), "local_sha256": lsha, "remote_status": r["status"], "remote_bytes": r["bytes"], "remote_etag": r["etag"], "remote_last_modified": r["last_modified"], "remote_sha256": r["sha256"], "remote_error": r["error"]})
        if r["status"] != 200:
            rec["result"] = "MISSING_REMOTE" if r["status"] in (403,404) else "REMOTE_ERROR"
        elif r["sha256"] == lsha:
            rec["result"] = "MATCH"
        else:
            rec["result"] = "MISMATCH"
        results["checks"].append(rec); nchecks += 1
        if args.checkpoint_every and nchecks % args.checkpoint_every == 0:
            by = {}
            for c in results["checks"]: by[c["result"]] = by.get(c["result"], 0) + 1
            ck = {"timestamp_utc": ts, "partial": True, "checks": results["checks"], "summary": by}
            (OUT / f"_partial_probe_{ts}.json").write_text(json.dumps(ck))
            print(f"checkpoint {nchecks} checks total={len(results['checks'])} {by}", file=sys.stderr)
    by = {}
    for c in results["checks"]: by[c["result"]] = by.get(c["result"], 0) + 1
    results["summary"] = {"match": by.get("MATCH",0), "mismatch": by.get("MISMATCH",0), "missing_local": by.get("MISSING_LOCAL",0), "missing_remote": by.get("MISSING_REMOTE",0), "remote_error": by.get("REMOTE_ERROR",0), "total": len(results["checks"]), "new_checks_this_run": nchecks}
    cache_identity_go = results["summary"]["match"] > 0 and results["summary"]["mismatch"] == 0 and results["summary"]["missing_remote"] == 0 and results["summary"]["remote_error"] == 0
    results["cache_identity_vs_binance_vision"] = "GO_SAMPLED_OR_PARTIAL" if cache_identity_go else "NO_GO"
    results["confirmatory_claim_go"] = "NO_GO"
    results["license_terms_note"] = "Binance Vision public historical market data; accessed unauthenticated via HTTPS. Verify Binance Vision/market-data terms before redistribution; checksums/provenance evidence only."
    suffix = "_full" if args.full_days else "_sampled"
    if args.max_checks: suffix += f"_partial{args.max_checks}"
    jp, mp = _write_artifacts(results, ts, suffix=suffix)
    print(json.dumps({"json": str(jp.relative_to(REPO)), "md": str(mp.relative_to(REPO)), "summary": results["summary"], "cache_identity_vs_binance_vision": results["cache_identity_vs_binance_vision"]}, indent=2))
    return 0 if cache_identity_go else 2

if __name__ == "__main__":
    sys.exit(main())
