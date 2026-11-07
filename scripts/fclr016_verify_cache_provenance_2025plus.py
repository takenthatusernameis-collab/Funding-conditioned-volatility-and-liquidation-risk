#!/usr/bin/env python3
"""FCLR-016: Bounded unauthenticated Binance Vision provenance verification for
cached 2025+ Binance UM futures files under research_state/data_cache.

Purpose: produce machine-verifiable identity evidence (local sha256 == remote
Binance Vision zip sha256) to unblock or rule out Gate 4 v5 confirmatory
admissibility (FCLR-014 NO-GO = provenance unverified). Admissibility evidence
only; no credentials/paid/manual/API keys/auth bypass. Does NOT run outcomes.

Usage (bounded):
  python3 scripts/fclr016_verify_cache_provenance_2025plus.py \\
    --symbols BTCUSDT,ETHUSDT --months 2025-01 --sample-days 1,15 --kinds fundingRate,klines
"""
from __future__ import annotations
import argparse, calendar, hashlib, json, os, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "research_state" / "data_cache"
OUT = REPO / "research_state" / "fclr016_local_audit"
BASE = "https://data.binance.vision/"
UA = {"User-Agent": "kilo-fclr016-provenance/1.0 (unauthenticated checksum verification)"}
TIMEOUT, SLEEP = 30, 0.05
KINDS_TPL = {
    "klines": "data/futures/um/daily/klines/{sym}/1h/{sym}-1h-{day}.zip",
    "markPriceKlines": "data/futures/um/daily/markPriceKlines/{sym}/1h/{sym}-1h-{day}.zip",
    "indexPriceKlines": "data/futures/um/daily/indexPriceKlines/{sym}/1h/{sym}-1h-{day}.zip",
    "premiumIndexKlines": "data/futures/um/daily/premiumIndexKlines/{sym}/1h/{sym}-1h-{day}.zip",
    "fundingRate": "data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip",
}

def sha256(b: bytes) -> str: return hashlib.sha256(b).hexdigest()

def fetch(url: str):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read()
            return {"status": r.status, "bytes": len(body), "etag": r.headers.get("ETag"), "last_modified": r.headers.get("Last-Modified"), "sha256": sha256(body), "error": None}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "bytes": 0, "etag": None, "last_modified": None, "sha256": None, "error": str(e)}
    except Exception as e:
        return {"status": None, "bytes": 0, "etag": None, "last_modified": None, "sha256": None, "error": str(e)}

def local_zip(sym: str, ym: str, kind: str, day: str | None):
    """Select the canonical cached zip for Binance Vision comparison.

    Only the kind-specific subdirectory `<kind>-<YYYY>-<MM>-<DD>/<sym>-1h-...zip`
    is admissible for daily kinds. A same-named top-level placeholder (a stale
    or merged duplicate) is NOT a substitute: it is reported as MISSING so the
    caller records a coverage gap instead of a false identity verdict.
    """
    d = CACHE / f"{sym}_{ym.replace('-', '_')}"
    if not d.exists(): return None
    if kind == "fundingRate":
        p = d / f"{sym}-fundingRate-{ym}.zip"; return p if p.exists() else None
    name = f"{sym}-1h-{day}.zip"
    canon = d / f"{kind}-{day}" / name
    return canon if canon.exists() else None


def placeholder_duplicate_paths(sym: str, ym: str, day: str) -> list[Path]:
    """Return same-named files sitting at the month-dir top level (potential placeholders).

    A top-level `<sym>-1h-<day>.zip` that duplicates a canonical kind subdir is a
    provenance hazard: one file cannot be the archive for klines, markPriceKlines,
    indexPriceKlines and premiumIndexKlines simultaneously. Flag them for the audit
    report so the NO_GO/INCOMPLETE verdict names the offending cache rather than
    silently trusting the wrong file.
    """
    d = CACHE / f"{sym}_{ym.replace('-', '_')}"
    if not d.exists(): return []
    name = f"{sym}-1h-{day}.zip"
    return [q for q in d.glob(name) if q.is_file() and q.parent == d]

def _ck(rec): return (rec.get("symbol"), rec.get("month"), rec.get("kind"), rec.get("day"))

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT")
    ap.add_argument("--months", required=True, help="comma-separated YYYY-MM")
    ap.add_argument("--kinds", default="fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines")
    ap.add_argument("--sample-days", default="1,15,28", help="days per month for daily kinds; or 'full'")
    ap.add_argument("--max-checks", type=int, default=0)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--checkpoint-every", type=int, default=25)
    ap.add_argument("--out-tag", default="")
    args = ap.parse_args(argv)
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    months = [m.strip() for m in args.months.split(",") if m.strip()]
    kinds = [k.strip() for k in args.kinds.split(",") if k.strip()]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    done = {}
    if args.resume and os.path.exists(args.resume):
        try:
            for c in json.loads(Path(args.resume).read_text()).get("checks", []): done[_ck(c)] = c
        except Exception: pass
    results = {"timestamp_utc": ts, "method": "bounded unauthenticated GET vs local cached zip sha256/etag (FCLR-016, 2025+ probe)", "source_base": BASE, "symbols": symbols, "months": months, "kinds": kinds, "checks": list(done.values()), "summary": {}, "confirmatory_claim_go": "NO_GO", "fclr014_context": "2025+ cache provenance UNVERIFIED per fclr014_provenance_decision_20261107T133102Z.md; identity match is necessary but not sufficient (license/terms/completeness/leakage/prereg still required).", "placeholder_duplicate_files": [], "placeholder_duplicate_note": "Daily kinds require a kind-specific subdir (<kind>-<day>/<sym>-1h-<day>.zip). A same-named top-level placeholder is not admissible for non-canonical kinds and is reported, never substituted."}
    pending = []
    for sym in symbols:
        for ym in months:
            dim = calendar.monthrange(*map(int, ym.split("-")))[1]
            if args.sample_days.strip().lower() == "full":
                sdays = list(range(1, dim+1))
            else:
                sdays = sorted(set([int(x) for x in args.sample_days.split(",") if x.strip()] + [dim]))
                sdays = [d for d in sdays if d <= dim]
            for kind in kinds:
                if kind == "fundingRate":
                    k = (sym, ym, kind, None)
                    if k not in done: pending.append((sym, ym, kind, None))
                elif kind in KINDS_TPL:
                    for sd in sdays:
                        day = f"{ym}-{sd:02d}"; k = (sym, ym, kind, day)
                        if k not in done: pending.append((sym, ym, kind, day))
    n = 0
    for sym, ym, kind, day in pending:
        if args.max_checks and n >= args.max_checks: break
        tpl = KINDS_TPL[kind]
        url = BASE + (tpl.format(sym=sym, ym=ym) if kind == "fundingRate" else tpl.format(sym=sym, day=day))
        lp = local_zip(sym, ym, kind, day)
        rec = {"symbol": sym, "month": ym, "kind": kind, "day": day, "url": url, "local_path": str(lp.relative_to(REPO)) if lp else None}
        if not lp:
            rec.update({"result": "MISSING_LOCAL"}); results["checks"].append(rec); n += 1; continue
        # Flag top-level placeholder duplicates for the same day (provenance hazard).
        if day and kind != "fundingRate":
            for q in placeholder_duplicate_paths(sym, ym, day):
                results["placeholder_duplicate_files"].append({
                    "symbol": sym, "month": ym, "day": day, "path": str(q.relative_to(REPO)),
                    "sha256": sha256(q.read_bytes()),
                    "canonical_kind_subdir": f"{kind}-{day}",
                })
        lb = lp.read_bytes(); lsha = sha256(lb)
        r = fetch(url); time.sleep(SLEEP)
        rec.update({"local_bytes": len(lb), "local_sha256": lsha, "remote_status": r["status"], "remote_bytes": r["bytes"], "remote_etag": r["etag"], "remote_last_modified": r["last_modified"], "remote_sha256": r["sha256"], "remote_error": r["error"]})
        if r["status"] != 200: rec["result"] = "MISSING_REMOTE" if r["status"] in (403,404) else "REMOTE_ERROR"
        elif r["sha256"] == lsha: rec["result"] = "MATCH"
        else: rec["result"] = "MISMATCH"
        results["checks"].append(rec); n += 1
        if args.checkpoint_every and n % args.checkpoint_every == 0:
            by = {};
            for c in results["checks"]: by[c["result"]] = by.get(c["result"], 0) + 1
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / f"_partial_{ts}.json").write_text(json.dumps({"ts": ts, "checks": results["checks"], "summary": by}, indent=2))
            print(f"ckpt {n}/{len(results['checks'])} {by}", file=sys.stderr)
    by = {}
    for c in results["checks"]: by[c["result"]] = by.get(c["result"], 0) + 1
    results["summary"] = {"match": by.get("MATCH",0), "mismatch": by.get("MISMATCH",0), "missing_local": by.get("MISSING_LOCAL",0), "missing_remote": by.get("MISSING_REMOTE",0), "remote_error": by.get("REMOTE_ERROR",0), "total": len(results["checks"]), "new_this_run": n, "placeholder_duplicate_files": len(results["placeholder_duplicate_files"])}
    identity_go = results["summary"]["match"] > 0 and results["summary"]["mismatch"] == 0 and results["summary"]["missing_remote"] == 0 and results["summary"]["remote_error"] == 0 and results["summary"]["missing_local"] == 0 and results["summary"]["placeholder_duplicate_files"] == 0
    results["cache_identity_vs_binance_vision"] = "GO_PARTIAL_BOUNDED" if identity_go else ("NO_GO" if (results["summary"]["mismatch"] or results["summary"]["remote_error"] or results["summary"]["placeholder_duplicate_files"]) else "INCOMPLETE")
    OUT.mkdir(parents=True, exist_ok=True)
    tag = ("_" + args.out_tag) if args.out_tag else ""
    jp = OUT / f"fclr016_binance_vision_probe{tag}_{ts}.json"
    mp = OUT / f"fclr016_binance_vision_probe{tag}_{ts}.md"
    jp.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    lines = [f"# FCLR-016 Binance Vision provenance probe 2025+ ({ts}{tag})", "", f"- method: {results['method']}", f"- cache_identity_vs_binance_vision: **{results['cache_identity_vs_binance_vision']}**", f"- confirmatory_claim_go: **NO_GO** (identity evidence only; prereg/leakage/license/completeness required)", f"- summary: `{json.dumps(results['summary'], sort_keys=True)}`", "", "## FCLR-014 context", results["fclr014_context"], "", "## Result counts"] + [f"- {k}: {v}" for k,v in sorted(by.items())]
    if any(c["result"] not in ("MATCH",) for c in results["checks"]):
        lines += ["", "## Non-MATCH (first 60)"]
        for c in [x for x in results["checks"] if x["result"]!="MATCH"][:60]:
            lines.append(f"- {c['result']} {c['symbol']} {c['month']} {c['kind']} {c.get('day')} local={c.get('local_sha256','')[:16]} remote={c.get('remote_sha256','')[:16] if c.get('remote_sha256') else c.get('remote_status')}")
    mp.write_text("\n".join(lines) + "\n")
    if results["placeholder_duplicate_files"]:
        mp.write_text("\n## Placeholder duplicate files (provenance hazard)\n")
        seen = {}
        for p in results["placeholder_duplicate_files"]:
            seen.setdefault((p["symbol"], p["month"], p["day"]), []).append(p["sha256"][:16])
        for (sym, ym, day), hashes in sorted(seen.items()):
            mp.write_text(f"- {sym} {ym} {day}: top-level placeholder sha256={hashes[0]} (canonical kind subdir missing/unmatched)\n")
    print(json.dumps({"json": str(jp.relative_to(REPO)), "md": str(mp.relative_to(REPO)), "summary": results["summary"], "cache_identity_vs_binance_vision": results["cache_identity_vs_binance_vision"]}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
