#!/usr/bin/env python3
"""Stdlib-only integrity verification for the Ironflow bulk parquet cache.

Why this exists
---------------
``scripts/fclr_ironflow_bulk.py verify`` also re-validates each parquet schema,
which needs ``pyarrow``. In a bare runner without ``requirements.txt`` installed
the *hash-integrity* signal is still available and is all RISK-08..12 sessions
need: those campaigns read the frozen 12-month Track A CSV, never a parquet.
Leaving the pyarrow-dependent command as the only mandatory data check made the
handoff verification block fail closed for an environment reason, not a research
reason, and would stall every fresh session.

This script verifies, with ``hashlib`` only:
  * the object file exists and is non-empty,
  * a sha256 sidecar exists and matches the recomputed digest,
  * a provenance ``<month>.accessed.json`` sidecar exists.

It never reads parquet content, never imports pyarrow/numpy/pandas, never
writes, and never touches the network.

Usage
-----
  python3 scripts/check_ironflow_cache_integrity.py --json
  python3 scripts/check_ironflow_cache_integrity.py \
      --datasets all --months 2025-11..2026-10
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache" / "ironflow_bulk"

DATASETS = ("candles_1h", "funding", "liquidations", "open_interest")
DEFAULT_MONTHS = "2025-11..2026-10"
MONTH_RE = re.compile(r"^(\d{4})-(\d{2})$")


def _resolve_datasets(values: Sequence[str]) -> List[str]:
    out: List[str] = []
    for value in values:
        for token in value.split(","):
            token = token.strip()
            if not token:
                continue
            if token == "all":
                out.extend(DATASETS)
            elif token in DATASETS:
                out.append(token)
            else:
                raise SystemExit(f"unknown dataset: {token}")
    seen: List[str] = []
    for name in out:
        if name not in seen:
            seen.append(name)
    return seen


def _month_range(spec: str) -> List[str]:
    parts = [p.strip() for p in spec.split(",") if p.strip()]
    months: List[str] = []
    for part in parts:
        if ".." in part:
            start, end = [p.strip() for p in part.split("..", 1)]
            start_year, start_month = _parse_month(start)
            end_year, end_month = _parse_month(end)
            year, month = start_year, start_month
            while (year, month) <= (end_year, end_month):
                months.append(f"{year:04d}-{month:02d}")
                month += 1
                if month > 12:
                    month = 1
                    year += 1
        else:
            _parse_month(part)
            months.append(part)
    out: List[str] = []
    for name in months:
        if name not in out:
            out.append(name)
    return out


def _parse_month(value: str) -> Tuple[int, int]:
    m = MONTH_RE.match(value)
    if not m:
        raise SystemExit(f"bad month: {value}")
    year, month = int(m.group(1)), int(m.group(2))
    if not 1 <= month <= 12:
        raise SystemExit(f"bad month: {value}")
    return year, month


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_object(dataset: str, month: str) -> Dict[str, object]:
    base = CACHE / dataset
    parquet = base / f"{month}.parquet"
    sidecar = base / f"{month}.parquet.sha256"
    accessed = base / f"{month}.accessed.json"
    record: Dict[str, object] = {
        "dataset": dataset,
        "month": month,
        "object_bytes": 0,
        "expected_sha256": None,
        "actual_sha256": None,
        "problems": [],
    }
    problems: List[str] = record["problems"]  # type: ignore[assignment]

    if not parquet.is_file() or parquet.stat().st_size == 0:
        problems.append("missing_or_empty_object")
    else:
        record["object_bytes"] = parquet.stat().st_size
    expected = None
    if not sidecar.is_file():
        problems.append("missing_sha256_sidecar")
    else:
        text = sidecar.read_text(encoding="utf-8").strip()
        expected = text.split()[0] if text else None
        if not expected:
            problems.append("empty_sha256_sidecar")
    record["expected_sha256"] = expected
    if record["object_bytes"]:
        actual = _sha256(parquet)
        record["actual_sha256"] = actual
        if expected and actual != expected:
            problems.append("sha256_mismatch")
    if not accessed.is_file() or accessed.stat().st_size == 0:
        problems.append("missing_accessed_provenance")
    record["status"] = "OK" if not problems else "FAIL"
    return record


def run(datasets: Iterable[str], months: Iterable[str]) -> Dict[str, object]:
    results = [verify_object(d, m) for d in datasets for m in months]
    failures = [r for r in results if r["status"] != "OK"]
    return {
        "script": "check_ironflow_cache_integrity",
        "read_only": True,
        "network": False,
        "requires_pyarrow": False,
        "cache_root": str(CACHE.relative_to(REPO)),
        "datasets": list(datasets),
        "months": list(months),
        "objects": len(results),
        "failures": len(failures),
        "passed": not failures,
        "results": results,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datasets", nargs="+", default=["all"])
    parser.add_argument("--months", default=DEFAULT_MONTHS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    payload = run(_resolve_datasets(args.datasets), _month_range(args.months))
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for r in payload["results"]:  # type: ignore[index]
            print(
                f"{r['status']:<6} {r['dataset']:<14} {r['month']}  "
                f"{str(r['actual_sha256'])[:12]:<12} {r['object_bytes']}"
            )
        print(f"integrity: {payload['objects']} objects, {payload['failures']} failure(s)")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
