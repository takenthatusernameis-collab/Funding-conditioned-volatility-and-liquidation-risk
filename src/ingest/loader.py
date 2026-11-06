"""Minimal ingestion: extract zips, load CSVs, normalize to UTC hourly frames.

Design goals:
- No trading, no credentials, no network.
- Treat missing basis/spot as NaN, never zero.
- Normalize timestamps to UTC; klines use ms, funding uses ms.
- Deduplicate and hash for reproducibility.
"""
from __future__ import annotations

import hashlib
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

# Canonical column sets (Binance public archive layout).
KLINE_COLS = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_volume", "count", "taker_buy_volume",
    "taker_buy_quote_volume", "ignore",
]
FUNDING_COLS = ["calc_time", "funding_interval_hours", "last_funding_rate"]


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def extract_zip(zip_path: Path, dest: Path) -> List[Path]:
    """Extract a zip into dest; return list of extracted file paths."""
    dest.mkdir(parents=True, exist_ok=True)
    out: List[Path] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            target = dest / member
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as src, open(target, "wb") as dst:
                dst.write(src.read())
            out.append(target)
    return out


def discover_zips(root: Path) -> List[Path]:
    return sorted(p for p in root.glob("*.zip") if p.is_file())


def _to_utc_ms(series: pd.Series) -> pd.Series:
    """Coerce a numeric millisecond timestamp column to UTC datetime."""
    s = pd.to_numeric(series, errors="coerce")
    return pd.to_datetime(s, unit="ms", utc=True)


def load_klines(path: Path) -> pd.DataFrame:
    """Load a klines CSV into a UTC-indexed frame (open_time -> index)."""
    df = pd.read_csv(path)
    # Standardize columns if present.
    df = df.rename(columns={c: c.strip() for c in df.columns})
    if "open_time" not in df.columns:
        raise ValueError(f"{path}: missing open_time")
    df["open_time"] = _to_utc_ms(df["open_time"])
    df = df.sort_values("open_time").drop_duplicates("open_time", keep="last")
    df = df.set_index("open_time")
    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_funding(path: Path) -> pd.DataFrame:
    """Load a funding-rate CSV into a UTC-indexed frame keyed by calc_time."""
    df = pd.read_csv(path)
    df = df.rename(columns={c: c.strip() for c in df.columns})
    if "calc_time" not in df.columns:
        raise ValueError(f"{path}: missing calc_time")
    df["calc_time"] = _to_utc_ms(df["calc_time"])
    df = df.sort_values("calc_time").drop_duplicates("calc_time", keep="last")
    df = df.set_index("calc_time")
    if "last_funding_rate" in df.columns:
        df["last_funding_rate"] = pd.to_numeric(df["last_funding_rate"], errors="coerce")
    if "funding_interval_hours" in df.columns:
        df["funding_interval_hours"] = pd.to_numeric(
            df["funding_interval_hours"], errors="coerce"
        ).astype("Int64")
    return df


def load_basis(path: Path, kind: str) -> pd.DataFrame:
    """Load mark/index/premium klines; return close indexed by open_time UTC."""
    df = load_klines(path)
    out = df[["close"]].rename(columns={"close": f"{kind}_close"})
    return out


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class LoadedSeries:
    symbol: str
    kind: str  # klines | funding | mark | index | premium
    df: pd.DataFrame
    source_path: str
    sha256: str
    rows: int


def inventory_raw(raw_dir: Path = RAW) -> Dict[str, object]:
    """Summarize what is present under data/raw."""
    files = sorted(p for p in raw_dir.rglob("*") if p.is_file() and p.suffix == ".csv")
    by_kind: Dict[str, int] = {}
    by_symbol: Dict[str, int] = {}
    for p in files:
        kind = "funding" if "fundingRate" in p.name else "klines"
        by_kind[kind] = by_kind.get(kind, 0) + 1
        sym = p.name.split("-")[0]
        by_symbol[sym] = by_symbol.get(sym, 0) + 1
    return {
        "raw_dir": str(raw_dir),
        "csv_count": len(files),
        "by_kind": by_kind,
        "by_symbol": by_symbol,
    }