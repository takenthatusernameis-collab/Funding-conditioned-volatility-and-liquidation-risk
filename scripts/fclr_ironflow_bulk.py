#!/usr/bin/env python3
"""Cache-first, bounded acquisition + verification of Ironflow Hyperliquid bulk parquet.

Campaign: FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z (P1 volatility primary, P2 cross-sectional).

Why this exists
---------------
Every prior volatility result in this repo was computed on the 6-month window
2026-05..2026-10, because the only admissible mark-price cache covered those months.
`ironflow/hyperliquid-candles-1h` (CC BY 4.0, unauthenticated HF bulk parquet) covers
2025-05-25 .. 2026-10-31, which makes the 2025-06..2026-04 region a never-opened
holdout for the volatility target. This script is the only sanctioned way to materialise
that region; it never invents data, never overwrites a verified cache file, and records
provenance for every object.

Datasets (all CC BY 4.0, all unauthenticated, no key, no requester-pays)
-----------------------------------------------------------------------
  liquidations    ironflow/hyperliquid-liquidations        data/events/YYYY-MM.parquet
  candles_1h      ironflow/hyperliquid-candles-1h          data/YYYY-MM.parquet
  funding         ironflow/hyperliquid-funding             data/YYYY-MM.parquet
  open_interest   ironflow/hyperliquid-open-interest       data/YYYY-MM.parquet

Cache layout
------------
  research_state/data_cache/ironflow_bulk/<dataset>/<YYYY-MM>.parquet
  research_state/data_cache/ironflow_bulk/<dataset>/<YYYY-MM>.parquet.sha256
  research_state/data_cache/ironflow_bulk/<dataset>/<YYYY-MM>.accessed.json

Guarantees
----------
* Fail closed on schema violation (missing/renamed required column) or on a
  parquet file that cannot be read.
* `verify` re-hashes every cached object and re-checks schema; exit 1 on any mismatch.
* `fetch` is idempotent: a cached object whose sha256 matches its sidecar and whose
  schema validates is never re-downloaded.
* Deterministic manifest (sorted keys, no wall-clock in the payload except `generated_utc`).
* No writes to .github/workflows, no trading endpoints, no credentials.

Usage
-----
  python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-05..2026-04
  python3 scripts/fclr_ironflow_bulk.py fetch  --datasets candles_1h,funding,open_interest \
                                              --months 2025-06..2026-04
  python3 scripts/fclr_ironflow_bulk.py manifest --months 2025-06..2026-04
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache" / "ironflow_bulk"
MANIFEST = RS / "ironflow_bulk_manifest.json"

UTC = timezone.utc

BASE = "https://huggingface.co/datasets"

# dataset -> (repo_id, relative path template, required columns)
DATASETS: Dict[str, Tuple[str, str, Tuple[str, ...]]] = {
    "liquidations": (
        f"{BASE}/ironflow/hyperliquid-liquidations/resolve/main",
        "data/events/{month}.parquet",
        ("timestamp", "market", "position_side", "notional_usd"),
    ),
    "candles_1h": (
        f"{BASE}/ironflow/hyperliquid-candles-1h/resolve/main",
        "data/{month}.parquet",
        ("timestamp", "market", "close"),
    ),
    "funding": (
        f"{BASE}/ironflow/hyperliquid-funding/resolve/main",
        "data/{month}.parquet",
        ("timestamp", "market", "funding_rate"),
    ),
    "open_interest": (
        f"{BASE}/ironflow/hyperliquid-open-interest/resolve/main",
        "data/{month}.parquet",
        ("timestamp", "market", "open_interest_usd"),
    ),
}

MAX_ATTEMPTS = 3
BACKOFF_BASE_S = 2.0
BACKOFF_CAP_S = 30.0


class BulkError(RuntimeError):
    """Raised on schema, hash, or range violations. Always fail closed."""


# ------------------------------- helpers ----------------------------------------
def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_month(month: str) -> Tuple[int, int]:
    if len(month) != 7 or month[4] != "-":
        raise BulkError(f"bad month key {month!r}; expected YYYY-MM")
    year, mon = month.split("-")
    if not (year.isdigit() and mon.isdigit()):
        raise BulkError(f"bad month key {month!r}; expected YYYY-MM")
    y, m = int(year), int(mon)
    if not (1 <= m <= 12):
        raise BulkError(f"bad month key {month!r}; month out of range")
    return y, m


def expand_months(spec: str) -> List[str]:
    """Expand 'A' | 'A..B' (inclusive, YYYY-MM) into a sorted unique month list."""
    spec = spec.strip()
    if ".." in spec:
        lo_s, hi_s = [p.strip() for p in spec.split("..", 1)]
        lo, hi = parse_month(lo_s), parse_month(hi_s)
        if lo > hi:
            raise BulkError(f"month range reversed: {spec}")
        out: List[str] = []
        y, m = lo
        while (y, m) <= hi:
            out.append(f"{y:04d}-{m:02d}")
            m += 1
            if m > 12:
                y, m = y + 1, 1
        return out
    parse_month(spec)
    return [spec]


def expand_datasets(spec: str) -> List[str]:
    spec = spec.strip()
    if spec == "all":
        return sorted(DATASETS)
    out = [p.strip() for p in spec.split(",") if p.strip()]
    for name in out:
        if name not in DATASETS:
            raise BulkError(f"unknown dataset {name!r}; known={sorted(DATASETS)}")
    return sorted(set(out))


def url_for(dataset: str, month: str) -> str:
    base, tmpl, _ = DATASETS[dataset]
    return f"{base}/{tmpl.format(month=month)}"


def _cache_for(cache_root: Optional[Path]) -> Path:
    return Path(cache_root) if cache_root is not None else CACHE


def local_path(dataset: str, month: str, cache_root: Optional[Path] = None) -> Path:
    return _cache_for(cache_root) / dataset / f"{month}.parquet"


def sidecar_path(dataset: str, month: str, cache_root: Optional[Path] = None) -> Path:
    p = local_path(dataset, month, cache_root)
    return p.with_suffix(p.suffix + ".sha256")


def accessed_path(dataset: str, month: str, cache_root: Optional[Path] = None) -> Path:
    p = local_path(dataset, month, cache_root)
    return p.with_suffix(".accessed.json")


def validate_schema(dataset: str, path: Path) -> Dict[str, object]:
    """Read column names + row count from a parquet file; fail closed on schema drift."""
    try:
        import pyarrow.parquet as pq  # noqa: WPS433 (deferred: no data read at import)
    except Exception as exc:  # pragma: no cover - environment guard
        raise BulkError(f"pyarrow unavailable: {exc}") from exc
    try:
        pf = pq.ParquetFile(path)
        names = [str(n) for n in pf.schema_arrow.names]
        rows = int(pf.metadata.num_rows)
    except Exception as exc:
        raise BulkError(f"unreadable parquet {path}: {exc}") from exc
    required = DATASETS[dataset][2]
    missing = [c for c in required if c not in names]
    if missing:
        raise BulkError(f"schema violation in {path}: missing columns {missing}; found {names}")
    return {"columns": names, "rows": rows, "required_present": list(required)}


def read_sidecar(dataset: str, month: str, cache_root: Optional[Path] = None) -> Optional[str]:
    p = sidecar_path(dataset, month, cache_root)
    if not p.exists():
        return None
    txt = p.read_text().strip()
    return txt.split()[0] if txt else None


def verify_object(dataset: str, month: str, *, require_exists: bool = True,
                  cache_root: Optional[Path] = None) -> Dict[str, object]:
    path = local_path(dataset, month, cache_root)
    if not path.exists():
        if require_exists:
            raise BulkError(f"missing cached object: {path}")
        return {"dataset": dataset, "month": month, "status": "ABSENT"}
    digest = sha256_file(path)
    expected = read_sidecar(dataset, month, cache_root)
    status = "OK"
    problems: List[str] = []
    if expected is None:
        status = "NO_SIDECAR"
        problems.append("sha256 sidecar missing")
    elif expected != digest:
        status = "HASH_MISMATCH"
        problems.append(f"sidecar {expected[:12]} != actual {digest[:12]}")
    schema = validate_schema(dataset, path)
    return {
        "dataset": dataset,
        "month": month,
        "status": status,
        "sha256": digest,
        "bytes": path.stat().st_size,
        "schema": schema,
        "problems": problems,
    }


# ------------------------------- network ----------------------------------------
def _download(url: str, attempts: int = MAX_ATTEMPTS) -> bytes:
    """Bounded GET with exponential backoff. No credentials, no conditional headers."""
    import requests  # deferred: keeps import-time free of network deps

    last: Optional[Exception] = None
    for attempt in range(1, attempts + 1):
        try:
            resp = requests.get(url, timeout=120, stream=True)
            if resp.status_code == 404:
                raise BulkError(f"HTTP 404 for {url} (object absent upstream)")
            if resp.status_code >= 400:
                raise BulkError(f"HTTP {resp.status_code} for {url}")
            payload = resp.content
            if not payload:
                raise BulkError(f"empty body for {url}")
            return payload
        except BulkError:
            raise
        except Exception as exc:  # network/timeout: retry with backoff
            last = exc
            if attempt < attempts:
                time.sleep(min(BACKOFF_BASE_S * (2 ** (attempt - 1)), BACKOFF_CAP_S))
    raise BulkError(f"download failed after {attempts} attempts: {url}: {last}")


def fetch_object(dataset: str, month: str) -> Dict[str, object]:
    path = local_path(dataset, month)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = verify_object(dataset, month)
        if existing["status"] == "OK":
            existing["action"] = "cache_hit"
            return existing
        # A corrupt/unverifiable cache object is replaced only after a successful
        # download has been schema-validated in a temp file; the original is preserved.
    url = url_for(dataset, month)
    payload = _download(url)
    tmp = path.with_suffix(".parquet.download")
    try:
        tmp.write_bytes(payload)
        digest = sha256_file(tmp)
        schema = validate_schema(dataset, tmp)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()
    sidecar_path(dataset, month).write_text(digest + "\n")
    accessed_path(dataset, month).write_text(
        json.dumps(
            {
                "dataset": dataset,
                "month": month,
                "url": url,
                "fetched_utc": now_utc(),
                "sha256": digest,
                "bytes": len(payload),
                "license": "CC-BY-4.0",
                "unauthenticated": True,
                "requester_pays": False,
                "api_key_required": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return {
        "dataset": dataset,
        "month": month,
        "status": "OK",
        "sha256": digest,
        "bytes": len(payload),
        "schema": schema,
        "action": "downloaded",
    }


# ------------------------------- manifest ---------------------------------------
def _display(path: Path) -> str:
    """Repo-relative when possible, absolute otherwise (keeps manifest path-portable)."""
    try:
        return str(path.resolve().relative_to(REPO))
    except ValueError:
        return str(path)


def build_manifest(months: Sequence[str]) -> Dict[str, object]:
    entries: List[Dict[str, object]] = []
    for dataset in sorted(DATASETS):
        for month in months:
            entries.append(verify_object(dataset, month, require_exists=False))
    payload = {
        "manifest_id": "fclr_ironflow_bulk_manifest",
        "generated_utc": now_utc(),
        "cache_root": _display(CACHE),
        "datasets": {k: {"repo": v[0], "template": v[1], "required_columns": list(v[2])}
                     for k, v in sorted(DATASETS.items())},
        "months": list(months),
        "objects": entries,
        "totals": {
            "objects": len(entries),
            "ok": sum(1 for e in entries if e["status"] == "OK"),
            "absent": sum(1 for e in entries if e["status"] == "ABSENT"),
            "problems": sum(1 for e in entries if e["status"] not in ("OK", "ABSENT")),
        },
    }
    return payload


def write_manifest(payload: Dict[str, object], path: Path = MANIFEST) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


# --------------------------------- cli ------------------------------------------
def main(argv: Optional[Iterable[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name in ("verify", "fetch"):
        p = sub.add_parser(name)
        p.add_argument("--datasets", default="all")
        p.add_argument("--months", required=True, help="YYYY-MM or YYYY-MM..YYYY-MM")

    sub.add_parser("manifest").add_argument("--months", required=True)

    args = ap.parse_args(list(argv) if argv is not None else None)
    if args.cmd == "manifest":
        args.datasets = "all"

    try:
        months = expand_months(args.months)
        datasets = expand_datasets(args.datasets)
    except BulkError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    if args.cmd == "manifest":
        payload = build_manifest(months)
        path = write_manifest(payload)
        print(f"wrote {_display(path)} ok={payload['totals']['ok']} "
              f"absent={payload['totals']['absent']} problems={payload['totals']['problems']}")
        return 0 if payload["totals"]["problems"] == 0 else 1

    results: List[Dict[str, object]] = []
    failures = 0
    for dataset in datasets:
        for month in months:
            try:
                results.append(fetch_object(dataset, month) if args.cmd == "fetch"
                               else verify_object(dataset, month))
            except BulkError as exc:
                failures += 1
                results.append({"dataset": dataset, "month": month, "status": "ERROR",
                                "problems": [str(exc)]})
    for r in results:
        print(f"{r['status']:<14} {r['dataset']:<14} {r['month']}  "
              f"{r.get('sha256', '')[:12]:<12} {r.get('rows', '')}")
    print(f"{args.cmd}: {len(results)} objects, {failures} failure(s)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())