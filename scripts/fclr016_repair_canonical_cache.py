#!/usr/bin/env python3
"""FCLR-016 bounded canonical cache repair (admissibility evidence only, no outcomes).

Downloads missing canonical daily Binance Vision UM futures zips for specified
sample days into <kind>-<day>/<sym>-1h-<day>.zip under research_state/data_cache.
Only fills files absent at canonical path; never overwrites. Records deterministic
sha256 + remote metadata. Source: https://data.binance.vision/ (unauthenticated,
public archive). No credentials/paid/manual/API keys/auth bypass. No trading.
"""
from __future__ import annotations
import argparse, calendar, hashlib, json, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
OUT = REPO / "research_state" / "fclr016_local_audit"
BASE = "https://data.binance.vision/"
UA = {"User-Agent": "kilo-fclr016-repair/1.0 (unauthenticated canonical provenance repair)"}
TIMEOUT, SLEEP, MAX_ATTEMPTS = 60, 0.08, 3
KINDS_TPL = {
    "klines": "data/futures/um/daily/klines/{sym}/1h/{sym}-1h-{day}.zip",
    "markPriceKlines": "data/futures/um/daily/markPriceKlines/{sym}/1h/{sym}-1h-{day}.zip",
    "indexPriceKlines": "data/futures/um/daily/indexPriceKlines/{sym}/1h/{sym}-1h-{day}.zip",
    "premiumIndexKlines": "data/futures/um/daily/premiumIndexKlines/{sym}/1h/{sym}-1h-{day}.zip",
    "fundingRate": "data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip",
}

def sha256(b: bytes) -> str: return hashlib.sha256(b).hexdigest()

def fetch_bytes(url: str):
    last = None
    for i in range(MAX_ATTEMPTS):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                body = r.read()
                return {"status": r.status, "bytes": len(body), "etag": r.headers.get("ETag"), "last_modified": r.headers.get("Last-Modified"), "sha256": sha256(body), "body": body, "error": None}
        except urllib.error.HTTPError as e:
            return {"status": e.code, "bytes": 0, "etag": None, "last_modified": None, "sha256": None, "body": None, "error": str(e)}
        except Exception as e:
            last = e; time.sleep(1.5 ** i)
    return {"status": None, "bytes": 0, "etag": None, "last_modified": None, "sha256": None, "body": None, "error": str(last)}

def canonical_path(sym: str, ym: str, kind: str, day: str | None) -> Path:
    d = CACHE / f"{sym}_{ym.replace('-', '_')}"
    if kind == "fundingRate":
        return d / f"{sym}-fundingRate-{ym}.zip"
    return d / f"{kind}-{day}" / f"{sym}-1h-{day}.zip"

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", required=True)
    ap.add_argument("--months", required=True)
    ap.add_argument("--kinds", default="klines,markPriceKlines,indexPriceKlines,premiumIndexKlines")
    ap.add_argument("--sample-days", default="1,15,28")
    ap.add_argument("--max-downloads", type=int, default=0)
    ap.add_argument("--out-tag", default="")
    args = ap.parse_args(argv)
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    months = [m.strip() for m in args.months.split(",") if m.strip()]
    kinds = [k.strip() for k in args.kinds.split(",") if k.strip()]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report = {"timestamp_utc": ts, "action": "bounded_canonical_repair_download", "source_base": BASE, "source_note": "Binance Vision public unauthenticated archive; no auth/paid/manual/key bypass; license/terms: record source URL+access time+remote metadata; confirmatory use still requires explicit license/terms/completeness/leakage/prereg verification per FCLR-014.", "symbols": symbols, "months": months, "kinds": kinds, "sample_days_arg": args.sample_days, "records": [], "summary": {}}
    targets = []
    for sym in symbols:
        for ym in months:
            dim = calendar.monthrange(*map(int, ym.split("-")))[1]
            if args.sample_days.strip().lower() == "full": sdays = list(range(1, dim+1))
            else:
                sdays = sorted(set([int(x) for x in args.sample_days.split(",") if x.strip()] + [dim]))
                sdays = [d for d in sdays if d <= dim]
            for kind in kinds:
                if kind == "fundingRate": targets.append((sym, ym, kind, None))
                else:
                    for sd in sdays: targets.append((sym, ym, kind, f"{ym}-{sd:02d}"))
    n = 0
    for sym, ym, kind, day in targets:
        if args.max_downloads and n >= args.max_downloads: break
        cp = canonical_path(sym, ym, kind, day)
        rec = {"symbol": sym, "month": ym, "kind": kind, "day": day, "canonical_path": str(cp.relative_to(REPO)), "url": BASE + (KINDS_TPL[kind].format(sym=sym, ym=ym) if kind=="fundingRate" else KINDS_TPL[kind].format(sym=sym, day=day))}
        if cp.exists() and cp.stat().st_size > 0:
            b = cp.read_bytes(); rec.update({"action": "SKIP_EXISTS", "local_sha256": sha256(b), "local_bytes": len(b)}); report["records"].append(rec); continue
        r = fetch_bytes(rec["url"]); time.sleep(SLEEP)
        rec.update({"remote_status": r["status"], "remote_bytes": r["bytes"], "remote_sha256": r["sha256"], "remote_etag": r["etag"], "remote_last_modified": r["last_modified"], "remote_error": r["error"]})
        if r["status"] == 200 and r["body"]:
            cp.parent.mkdir(parents=True, exist_ok=True)
            tmp = cp.with_suffix(".tmp")
            tmp.write_bytes(r["body"]); tmp.replace(cp)
            rec["action"] = "DOWNLOADED"
            rec["local_sha256"] = sha256(cp.read_bytes())
            rec["local_bytes"] = cp.stat().st_size
            rec["sha256_match"] = (rec["local_sha256"] == r["sha256"])
            n += 1
        elif r["status"] in (403, 404):
            rec["action"] = "MISSING_REMOTE"
        else:
            rec["action"] = "REMOTE_ERROR"
        report["records"].append(rec)
        if n and n % 25 == 0: print(f"progress {n}", file=sys.stderr)
    by = {}
    for r in report["records"]: by[r["action"]] = by.get(r["action"], 0) + 1
    bad = [r for r in report["records"] if r.get("sha256_match") is False]
    report["summary"] = {**by, "total": len(report["records"]), "sha256_mismatch_after_download": len(bad)}
    report["repair_identity_ok"] = len(bad) == 0 and by.get("REMOTE_ERROR", 0) == 0 and by.get("MISSING_REMOTE", 0) == 0
    OUT.mkdir(parents=True, exist_ok=True)
    tag = ("_" + args.out_tag) if args.out_tag else ""
    jp = OUT / f"fclr016_canonical_repair{tag}_{ts}.json"
    md = OUT / f"fclr016_canonical_repair{tag}_{ts}.md"
    jp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    lines = [f"# FCLR-016 canonical cache repair ({ts}{tag})", "", f"- source_base: {BASE}", f"- repair_identity_ok: **{report['repair_identity_ok']}** (bounded repair; not confirmatory GO)", f"- summary: `{json.dumps(report['summary'], sort_keys=True)}`", "", "## Source/terms note", report["source_note"], "", "## Non-skip records (first 80)"]
    for r in [x for x in report["records"] if x["action"] != "SKIP_EXISTS"][:80]:
        lines.append(f"- {r['action']} {r['symbol']} {r['month']} {r['kind']} {r.get('day')} status={r.get('remote_status')} local={str(r.get('local_sha256',''))[:16]} remote={str(r.get('remote_sha256',''))[:16]}")
    md.write_text("\n".join(lines) + "\n")
    print(json.dumps({"json": str(jp.relative_to(REPO)), "md": str(md.relative_to(REPO)), "summary": report["summary"], "repair_identity_ok": report["repair_identity_ok"]}, indent=2))
    return 0 if report["repair_identity_ok"] else 2

if __name__ == "__main__":
    sys.exit(main())
