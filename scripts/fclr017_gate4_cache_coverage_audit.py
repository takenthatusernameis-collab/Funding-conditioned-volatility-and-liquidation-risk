#!/usr/bin/env python3
"""FCLR-NEXT-139 / FCLR-017: deterministic read-only Gate 4 cache coverage/audit.

Scans research_state/data_cache/{SYMBOL}_{YYYY_MM}/ for requested symbols/months
(default 2024-04..09, BTC/ETH/SOL/XRP/BNB). Inventories canonical 1h kline sources
(klines, markPriceKlines, indexPriceKlines, premiumIndexKlines) and fundingRate;
records per-symbol/month file counts, deterministic source path/metadata hashes,
and bounded content hashes; flags missing months/days, duplicate kinds, and
quarantine/placeholder path patterns.

Read-only, no network, no model-outcome computation. Audit/planning evidence only.
"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_CACHE = REPO / "research_state" / "data_cache"
DEFAULT_OUT = REPO / "research_state" / "fclr017_local_audit"
SYMBOLS_DEFAULT = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
MONTHS_DEFAULT = ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
DAILY_KINDS = ["klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
FUNDING_KIND = "fundingRate"
QUARANTINE_MARKERS = ("_quarantine", "quarantine", "placeholder", "_placeholder")
V3_30D_DESIGN = {
    "experiment_id": "GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D",
    "window": "2024-04-01..2024-09-30",
    "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"],
    "walk_forward": "4x30-day blocks, 7d purge/embargo",
    "sealed_expected_primary": {
        "n_obs": 12969,
        "n_blocks": 120,
        "E_vs_A_point": 0.4879023125556385,
        "ci95": [-0.042160777324701186, 1.1973379300276015],
        "ci_spans_0": True,
    },
    "sealed_artifacts": [
        "research_state/evaluation_summary_funding_v3_30d.md",
        "research_state/run_manifest_funding_v3_30d.json",
    ],
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def days_in_month(ym: str) -> int:
    y, m = map(int, ym.split("-"))
    return calendar.monthrange(y, m)[1]


def month_dir(cache: Path, sym: str, ym: str) -> Path:
    return cache / f"{sym}_{ym.replace('-', '_')}"


def is_quarantine_or_placeholder(name: str) -> bool:
    low = name.lower()
    return any(m in low for m in QUARANTINE_MARKERS)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except Exception:
        return str(path)


def inventory_daily_kind(kind_dir: Path, sym: str, ym: str, kind: str, content_hash: bool):
    day = kind_dir.name.replace(f"{kind}-", "", 1)
    expected_day_prefix = ym + "-"
    files = []
    quarantine_hits = []
    for child in sorted(kind_dir.iterdir(), key=lambda p: p.name):
        if not child.is_file():
            continue
        if is_quarantine_or_placeholder(child.name):
            quarantine_hits.append(child.name)
        entry = {
            "name": child.name,
            "path": rel(child),
            "bytes": child.stat().st_size,
            "ext": child.suffix.lower(),
        }
        if content_hash:
            entry["sha256"] = sha256_file(child)
        files.append(entry)
    canonical_zip = f"{sym}-1h-{day}.zip"
    canonical_csv = f"{sym}-1h-{day}.csv"
    names = {f["name"] for f in files}
    return {
        "day": day,
        "day_format_ok": day.startswith(expected_day_prefix) and len(day) == 10,
        "file_count": len(files),
        "files": files,
        "has_canonical_zip": canonical_zip in names,
        "has_canonical_csv": canonical_csv in names,
        "duplicate_files": len(files) > 1,
        "quarantine_or_placeholder_hits": quarantine_hits,
    }


def audit_kind_month(d: Path, sym: str, ym: str, kind: str, content_hash: bool):
    dim = days_in_month(ym)
    expected_days = [f"{ym}-{dd:02d}" for dd in range(1, dim + 1)]
    day_dirs = sorted(p for p in d.iterdir() if p.is_dir() and p.name.startswith(f"{kind}-"))
    by_day = {}
    anomalies = []
    for dd in day_dirs:
        rec = inventory_daily_kind(dd, sym, ym, kind, content_hash)
        day = rec["day"]
        if day in by_day:
            anomalies.append({"type": "duplicate_day_dir", "day": day, "path": rel(dd)})
        by_day[day] = rec
        if not rec["day_format_ok"]:
            anomalies.append({"type": "unexpected_day_format", "day": day, "path": rel(dd)})
        if rec["quarantine_or_placeholder_hits"]:
            anomalies.append({"type": "quarantine_or_placeholder_in_day_dir", "day": day, "hits": rec["quarantine_or_placeholder_hits"]})
        if not rec["has_canonical_zip"] and not rec["has_canonical_csv"]:
            anomalies.append({"type": "missing_canonical_zip_or_csv", "day": day, "path": rel(dd)})
    present_days = sorted(by_day)
    missing_days = [day for day in expected_days if day not in by_day]
    extra_days = [day for day in present_days if day not in expected_days]
    if extra_days:
        anomalies.append({"type": "extra_day_dirs", "days": extra_days})
    zip_count = sum(1 for r in by_day.values() if r["has_canonical_zip"])
    csv_count = sum(1 for r in by_day.values() if r["has_canonical_csv"])
    total_files = sum(r["file_count"] for r in by_day.values())
    total_bytes = sum(f["bytes"] for r in by_day.values() for f in r["files"])
    metadata_fingerprint = sha256_bytes(
        json.dumps(
            [{"day": day, "files": [(f["name"], f["bytes"]) for f in by_day[day]["files"]]} for day in present_days],
            sort_keys=True,
        ).encode()
    )
    return {
        "kind": kind,
        "month_dir": rel(d),
        "expected_days": dim,
        "day_dir_count": len(day_dirs),
        "present_day_count": len(present_days),
        "missing_days": missing_days,
        "missing_day_count": len(missing_days),
        "extra_days": extra_days,
        "canonical_zip_day_count": zip_count,
        "canonical_csv_day_count": csv_count,
        "total_file_count": total_files,
        "total_bytes": total_bytes,
        "metadata_fingerprint_sha256": metadata_fingerprint,
        "anomalies": anomalies,
        "days": by_day,
    }


def audit_funding(d: Path, sym: str, ym: str, content_hash: bool):
    expected_zip = f"{sym}-fundingRate-{ym}.zip"
    expected_dir = f"{sym}-fundingRate-{ym}"
    expected_csv = f"{sym}-fundingRate-{ym}.csv"
    hits = []
    anomalies = []
    for child in sorted(d.iterdir(), key=lambda p: p.name):
        if FUNDING_KIND not in child.name:
            continue
        if is_quarantine_or_placeholder(child.name):
            anomalies.append({"type": "quarantine_or_placeholder_funding_path", "path": rel(child)})
        if child.is_file():
            rec = {"name": child.name, "path": rel(child), "type": "file", "bytes": child.stat().st_size, "ext": child.suffix.lower()}
            if content_hash:
                rec["sha256"] = sha256_file(child)
            hits.append(rec)
        elif child.is_dir():
            inner = []
            for f in sorted(child.rglob("*"), key=lambda p: str(p)):
                if not f.is_file():
                    continue
                if is_quarantine_or_placeholder(f.name) or is_quarantine_or_placeholder(str(f.relative_to(child))):
                    anomalies.append({"type": "quarantine_or_placeholder_funding_inner", "path": rel(f)})
                e = {"name": str(f.relative_to(child)), "path": rel(f), "bytes": f.stat().st_size, "ext": f.suffix.lower()}
                if content_hash:
                    e["sha256"] = sha256_file(f)
                inner.append(e)
            hits.append({"name": child.name, "path": rel(child), "type": "dir", "inner_file_count": len(inner), "inner_files": inner})
    names = {h["name"] for h in hits}
    has_zip = expected_zip in names
    has_dir = expected_dir in names
    has_csv = any(h["type"] == "dir" and any(f["name"].endswith(expected_csv) or f["name"] == expected_csv for f in h.get("inner_files", [])) for h in hits) or any(h["name"] == expected_csv for h in hits)
    metadata_fingerprint = sha256_bytes(json.dumps([{k: v for k, v in h.items() if k not in ("inner_files",)} for h in hits], sort_keys=True).encode())
    return {
        "kind": FUNDING_KIND,
        "month_dir": rel(d),
        "present": bool(hits),
        "has_expected_zip": has_zip,
        "has_expected_dir": has_dir,
        "has_expected_csv": has_csv,
        "entry_count": len(hits),
        "entries": hits,
        "metadata_fingerprint_sha256": metadata_fingerprint,
        "anomalies": anomalies,
    }


def audit_month(cache: Path, sym: str, ym: str, content_hash: bool):
    d = month_dir(cache, sym, ym)
    if not d.exists():
        return {
            "symbol": sym,
            "month": ym,
            "month_dir": rel(d),
            "month_dir_exists": False,
            "kinds": {},
            "funding": None,
            "anomalies": [{"type": "missing_month_dir", "path": rel(d)}],
            "ok": False,
        }
    kind_reports = {}
    anomalies = []
    for child in sorted(d.iterdir(), key=lambda p: p.name):
        if is_quarantine_or_placeholder(child.name):
            anomalies.append({"type": "quarantine_or_placeholder_top_level", "path": rel(child)})
    for kind in DAILY_KINDS:
        kind_reports[kind] = audit_kind_month(d, sym, ym, kind, content_hash)
        anomalies.extend({"kind": kind, **a} for a in kind_reports[kind]["anomalies"])
    funding = audit_funding(d, sym, ym, content_hash)
    anomalies.extend({"kind": FUNDING_KIND, **a} for a in funding["anomalies"])
    missing_kinds = [k for k in DAILY_KINDS if kind_reports[k]["day_dir_count"] == 0]
    for k in missing_kinds:
        anomalies.append({"type": "missing_kind_day_dirs", "kind": k})
    if not funding["present"]:
        anomalies.append({"type": "missing_funding", "kind": FUNDING_KIND})
    ok = not any(a.get("type") in {"missing_month_dir", "missing_kind_day_dirs", "missing_funding", "missing_canonical_zip_or_csv"} or "quarantine_or_placeholder" in a.get("type", "") for a in anomalies)
    return {
        "symbol": sym,
        "month": ym,
        "month_dir": rel(d),
        "month_dir_exists": True,
        "kinds": kind_reports,
        "funding": funding,
        "anomalies": anomalies,
        "ok": ok,
    }


def summarize(report):
    per_sym = {}
    months = report["months"]
    for sym in report["symbols"]:
        rows = [report["inventory"][sym][ym] for ym in months]
        missing_month_dirs = [ym for ym in months if not rows[months.index(ym)]["month_dir_exists"]]
        missing_days_total = {k: 0 for k in DAILY_KINDS}
        canonical_zip_days = {k: 0 for k in DAILY_KINDS}
        quarantine_hits = 0
        funding_ok = 0
        for row in rows:
            for a in row.get("anomalies", []):
                if "quarantine_or_placeholder" in a.get("type", ""):
                    quarantine_hits += 1
            funding = row.get("funding") or {}
            if funding.get("has_expected_zip") or funding.get("has_expected_csv"):
                funding_ok += 1
            for k in DAILY_KINDS:
                kr = row.get("kinds", {}).get(k, {})
                missing_days_total[k] += kr.get("missing_day_count", 0)
                canonical_zip_days[k] += kr.get("canonical_zip_day_count", 0)
        per_sym[sym] = {
            "months_expected": len(months),
            "months_present": len(months) - len(missing_month_dirs),
            "missing_month_dirs": missing_month_dirs,
            "missing_days_by_kind": missing_days_total,
            "canonical_zip_days_by_kind": canonical_zip_days,
            "funding_months_with_expected_source": funding_ok,
            "quarantine_or_placeholder_anomaly_count": quarantine_hits,
            "all_months_ok": all(r["ok"] for r in rows) and not missing_month_dirs,
        }
    global_ok = all(v["all_months_ok"] for v in per_sym.values())
    return {"per_symbol": per_sym, "global_all_months_ok": global_ok}


def v3_consistency(summary, report):
    expected_days = {"2024-01": 31, "2024-02": 29, "2024-03": 31, "2024-04": 30, "2024-05": 31, "2024-06": 30, "2024-07": 31, "2024-08": 31, "2024-09": 30, "2024-10": 31, "2024-11": 30, "2024-12": 31}
    checks = []
    months = report["months"]
    requested_month_count = len(months)
    expected_total_by_kind = {}
    for k in DAILY_KINDS:
        expected_total_by_kind[k] = sum(expected_days[m] for m in months if m in expected_days)
    for sym in report["symbols"]:
        ps = summary["per_symbol"][sym]
        checks.append({"symbol": sym, "check": "all_requested_month_dirs_present", "pass": ps["months_present"] == requested_month_count, "detail": {"present": ps["months_present"], "expected": requested_month_count, "missing": ps["missing_month_dirs"]}})
        for k in DAILY_KINDS:
            checks.append({"symbol": sym, "kind": k, "check": "no_missing_days", "pass": ps["missing_days_by_kind"][k] == 0, "detail": ps["missing_days_by_kind"][k]})
            expected_total = expected_total_by_kind[k]
            checks.append({"symbol": sym, "kind": k, "check": "canonical_zip_covers_calendar_days", "pass": ps["canonical_zip_days_by_kind"][k] == expected_total, "detail": {"have": ps["canonical_zip_days_by_kind"][k], "expected": expected_total}})
        checks.append({"symbol": sym, "check": "funding_expected_source_each_requested_month", "pass": ps["funding_months_with_expected_source"] == requested_month_count, "detail": {"have": ps["funding_months_with_expected_source"], "expected": requested_month_count}})
        checks.append({"symbol": sym, "check": "no_quarantine_placeholder_anomalies", "pass": ps["quarantine_or_placeholder_anomaly_count"] == 0, "detail": ps["quarantine_or_placeholder_anomaly_count"]})
    all_pass = all(c["pass"] for c in checks)
    requested_matches_v3_default = months == MONTHS_DEFAULT and set(symbols := report["symbols"]) == set(SYMBOLS_DEFAULT)
    return {
        "design_window": V3_30D_DESIGN["window"],
        "design_symbols": V3_30D_DESIGN["symbols"],
        "requested_scope": {"symbols": report["symbols"], "months": months},
        "requested_scope_matches_v3_30d_default": requested_matches_v3_default,
        "consistent_with_requested_calendar_coverage": all_pass,
        "status": "CONSISTENT" if all_pass else "GAPS_OR_ANOMALIES_DOCUMENTED",
        "checks": checks,
        "note": "Calendar/lineage/coverage consistency check only for requested scope; does not recompute model outcomes or reproduce sealed metrics. Sealed v3 metrics remain authoritative in sealed artifacts.",
        "sealed_reference": V3_30D_DESIGN["sealed_expected_primary"],
    }


def write_markdown(report, path: Path):
    s = report["summary"]
    v3 = report["v3_30d_consistency"]
    lines = []
    lines.append(f"# FCLR-017 Gate 4 cache coverage audit ({report['timestamp_utc']})")
    lines.append("")
    lines.append("- method: deterministic local filesystem inventory; read-only; no network; no model-outcome computation")
    lines.append(f"- cache_root: `{report['cache_root']}`")
    lines.append(f"- symbols: {', '.join(report['symbols'])}")
    lines.append(f"- months: {', '.join(report['months'])}")
    lines.append(f"- global_all_months_ok: **{s['global_all_months_ok']}**")
    lines.append(f"- v3_30d_calendar_consistency: **{v3['status']}**")
    lines.append(f"- no_confirmatory_outcomes: **{report['no_confirmatory_outcomes']}**")
    lines.append(f"- exploratory_only: **{report['exploratory_only']}**")
    lines.append(f"- no_network: **{report['no_network']}**")
    lines.append("")
    lines.append("## Caveats / gates")
    lines.append("- Audit/planning evidence only — **not GO for confirmatory outcomes**.")
    lines.append("- v5 admissibility/terms blocker remains unresolved (`all_go=false`, terms `EXPLICIT_BLOCKER_UNRESOLVED`; `fabricated=false` per campaign state). This audit does not change that status.")
    lines.append("- 2024-04..09 identity/provenance context: FCLR-015 bounded Binance Vision identity verification applies only where separately evidenced; this audit records local lineage/coverage, not remote identity.")
    lines.append("- Confirmatory outcomes require fresh frozen prereg before outcomes and admissibility guards; 2024-04..09 confirmatory bounded by `PROVENANCED_CONFIRMATORY_RANGES` with manifest/terms evidence as required.")
    lines.append("- Sealed v3-30d artifacts are untouched by this audit.")
    lines.append("")
    lines.append("## Per-symbol summary")
    for sym, ps in s["per_symbol"].items():
        lines.append(f"### {sym}")
        lines.append(f"- months_present: {ps['months_present']}/{ps['months_expected']}")
        lines.append(f"- missing_month_dirs: `{ps['missing_month_dirs']}`")
        lines.append(f"- missing_days_by_kind: `{json.dumps(ps['missing_days_by_kind'], sort_keys=True)}`")
        lines.append(f"- canonical_zip_days_by_kind: `{json.dumps(ps['canonical_zip_days_by_kind'], sort_keys=True)}`")
        lines.append(f"- funding_months_with_expected_source: {ps['funding_months_with_expected_source']}/6")
        lines.append(f"- quarantine_or_placeholder_anomaly_count: {ps['quarantine_or_placeholder_anomaly_count']}")
        lines.append(f"- all_months_ok: **{ps['all_months_ok']}**")
        lines.append("")
    fails = [c for c in v3["checks"] if not c["pass"]]
    lines.append("## v3-30d calendar consistency checks")
    lines.append(f"- total: {len(v3['checks'])}, failed: {len(fails)}")
    if fails:
        for c in fails[:120]:
            lines.append(f"- FAIL {json.dumps(c, sort_keys=True)}")
    else:
        lines.append("- All calendar/coverage checks passed for requested scope.")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cache-root", default=str(DEFAULT_CACHE))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--symbols", default=",".join(SYMBOLS_DEFAULT))
    ap.add_argument("--months", default=",".join(MONTHS_DEFAULT), help="Comma-separated YYYY-MM")
    ap.add_argument("--no-content-hash", action="store_true", help="Skip per-file content hashes (metadata/path hashes still recorded)")
    ap.add_argument("--json-name", default=None, help="Override JSON filename (testing)")
    ap.add_argument("--md-name", default=None, help="Override MD filename (testing)")
    args = ap.parse_args(argv)

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    months = [m.strip() for m in args.months.split(",") if m.strip()]
    cache = Path(args.cache_root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    content_hash = not args.no_content_hash

    inventory = {}
    for sym in symbols:
        inventory[sym] = {}
        for ym in months:
            inventory[sym][ym] = audit_month(cache, sym, ym, content_hash)

    report = {
        "artifact": "fclr017_gate4_cache_coverage_audit",
        "version": 1,
        "timestamp_utc": ts,
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
        "purpose": "deterministic read-only Gate 4 cache manifest/audit for local coverage, source-file lineage, and integrity evidence; planning only",
        "not_go_for_confirmatory_outcomes": True,
        "cache_root": rel(cache),
        "symbols": symbols,
        "months": months,
        "daily_kinds": DAILY_KINDS,
        "funding_kind": FUNDING_KIND,
        "content_hash_enabled": content_hash,
        "v3_30d_design_reference": V3_30D_DESIGN,
        "caveats": {
            "v5_terms_blocker_unresolved": True,
            "fclr015_identity_verified_slice_only_where_evidenced": "2024-04..09",
            "sealed_artifacts_untouched": V3_30D_DESIGN["sealed_artifacts"],
            "confirmatory_requires_fresh_frozen_prereg_before_outcomes": True,
            "provenanced_confirmatory_ranges_gate_applies": True,
        },
        "inventory": inventory,
    }
    report["summary"] = summarize(report)
    report["v3_30d_consistency"] = v3_consistency(report["summary"], report)

    json_name = args.json_name or f"fclr017_gate4_cache_audit_{ts}.json"
    md_name = args.md_name or f"fclr017_gate4_cache_audit_{ts}.md"
    json_path = out_dir / json_name
    md_path = out_dir / md_name
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    (out_dir / "fclr017_gate4_cache_audit_latest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "fclr017_gate4_cache_audit_latest.md").write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")

    out = {
        "json": rel(json_path),
        "md": rel(md_path),
        "latest_json": rel(out_dir / "fclr017_gate4_cache_audit_latest.json"),
        "latest_md": rel(out_dir / "fclr017_gate4_cache_audit_latest.md"),
        "global_all_months_ok": report["summary"]["global_all_months_ok"],
        "v3_30d_calendar_consistency": report["v3_30d_consistency"]["status"],
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
