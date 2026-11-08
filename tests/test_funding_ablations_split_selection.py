"""Deterministic tests for Gate 4 cache-path resolution and split-selection-by-date.

No network. Proves: Apr–Sep 5-symbol cache range deterministically selects the
4×30-day v3_30d walk-forward design with cache included (no out_suffix/prereg
name coupling), v1 Jan–Mar default preserved, explicit split-design flag works,
and cache layout {SYMBOL}_{YYYY_MM}/ with nested klines/funding dirs is resolved.
"""
from __future__ import annotations

import io
import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import scripts.run_funding_ablations as rfa  # noqa: E402


def _write_kline_zip(path: Path, symbol: str, day: str, closes: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    base = pd.Timestamp(f"{day}T00:00:00Z")
    rows = []
    for i, c in enumerate(closes):
        ot = int((base + pd.Timedelta(hours=i)).timestamp() * 1000)
        rows.append([ot, c, c * 1.001, c * 0.999, c, 100.0, ot + 3599999, c * 100, 10, 50, c * 50, 0])
    cols = ["open_time", "open", "high", "low", "close", "volume", "close_time",
            "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]
    df = pd.DataFrame(rows, columns=cols)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{symbol}-1h-{day}.csv", df.to_csv(index=False))
    path.write_bytes(buf.getvalue())


def _write_funding_csv(path: Path, times_ms: list[int], rates: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"calc_time": times_ms, "funding_interval_hours": 8, "last_funding_rate": rates}).to_csv(path, index=False)


class TestSplitSelectionByDate(unittest.TestCase):
    def test_apr_sep_selects_v3_30d_by_date_range_no_name_coupling(self):
        sd, des, src = rfa.select_split_defs("2024-04-01", "2024-09-30", out_suffix="", pre_reg_path="", split_design="auto")
        self.assertEqual(des, "v3_30d")
        self.assertEqual(src, "date_range")
        self.assertEqual(len(sd), 4)
        self.assertEqual([rfa._test_days(s["test"]) for s in sd], [30, 30, 30, 30])
        self.assertIs(sd, rfa.PRE_REG_SPLITS_V3_30D)

    def test_jan_mar_default_preserves_v1(self):
        sd, des, src = rfa.select_split_defs("2024-01-01", "2024-03-31", "", "", "auto")
        self.assertEqual((des, src), ("v1", "default"))
        self.assertEqual(len(sd), 3)
        self.assertIs(sd, rfa.PRE_REG_SPLITS_V1)

    def test_legacy_name_coupling_still_works(self):
        sd, des, src = rfa.select_split_defs("2024-01-01", "2024-03-31", "_v3_30d", "", "auto")
        self.assertEqual((des, src), ("v3_30d", "legacy_name_coupling"))
        sd2, des2, src2 = rfa.select_split_defs("2024-04-01", "2024-09-30", "", "gate4_v4", "auto")
        self.assertEqual(des2, "v3_30d")  # date_range wins before legacy; both valid

    def test_explicit_split_design_flag(self):
        sd, des, src = rfa.select_split_defs("2024-01-01", "2024-03-31", "", "", "v3_30d")
        self.assertEqual((des, src, len(sd)), ("v3_30d", "explicit_split_design", 4))
        sd2, des2, src2 = rfa.select_split_defs("2024-04-01", "2024-09-30", "", "", "v1")
        self.assertEqual((des2, src2, len(sd2)), ("v1", "explicit_split_design", 3))

    def test_ambiguous_range_fails_closed_to_v1(self):
        sd, des, src = rfa.select_split_defs("2024-05-01", "2024-07-01", "", "", "auto")
        self.assertEqual(des, "v1")


class TestCachePathResolution(unittest.TestCase):
    def test_monthly_cache_layout_resolves_kline_and_funding(self):
        with TemporaryDirectory() as td:
            tmp_path = Path(td)
            syms = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
            cache = tmp_path / "research_state" / "data_cache"
            raw = tmp_path / "data" / "raw"
            raw.mkdir(parents=True, exist_ok=True)
            base_prices = {"BTCUSDT": 50000, "ETHUSDT": 3000, "SOLUSDT": 150, "XRPUSDT": 0.6, "BNBUSDT": 500}
            for sym in syms:
                bp = base_prices[sym]
                _write_kline_zip(cache / f"{sym}_2024_04" / "klines-2024-04-01" / f"{sym}-1h-2024-04-01.zip", sym, "2024-04-01", [bp * (1 + 0.001 * i) for i in range(24)])
                t0 = int(pd.Timestamp("2024-04-01T00:00:00Z").timestamp() * 1000)
                _write_funding_csv(cache / f"{sym}_2024_04" / f"{sym}-fundingRate-2024-04" / f"{sym}-fundingRate-2024-04.csv", [t0, t0 + 8 * 3600 * 1000], [0.0001, -0.00005])
            with patch.object(rfa, "REPO", tmp_path), patch.object(rfa, "RAW", raw), patch.object(rfa, "RES", tmp_path / "research_state"), patch.object(rfa, "CACHE", cache), patch.object(rfa, "ZIPS_DIR", tmp_path):
                k = rfa.load_kline_series(syms, "2024-04-01", "2024-04-01", horizon=24, include_cache=True)
                f = rfa.load_funding_series(syms, "2024-04-01", "2024-04-01", include_cache=True)
            self.assertEqual(set(k.index.get_level_values("symbol").unique()), set(syms))
            self.assertEqual(set(f.index.get_level_values("symbol").unique()), set(syms))
            self.assertFalse(f["last_funding_rate"].dropna().empty)

    def test_raw_primary_without_cache_by_default(self):
        with TemporaryDirectory() as td:
            tmp_path = Path(td)
            sym = "BTCUSDT"
            cache = tmp_path / "research_state" / "data_cache"
            raw = tmp_path / "data" / "raw"
            raw.mkdir(parents=True, exist_ok=True)
            # only cache populated; include_cache False => no sources
            _write_kline_zip(cache / f"{sym}_2024_04" / "klines-2024-04-01" / f"{sym}-1h-2024-04-01.zip", sym, "2024-04-01", [50000 + i for i in range(24)])
            with patch.object(rfa, "REPO", tmp_path), patch.object(rfa, "RAW", raw), patch.object(rfa, "RES", tmp_path / "research_state"), patch.object(rfa, "CACHE", cache), patch.object(rfa, "ZIPS_DIR", tmp_path):
                with self.assertRaises(RuntimeError):
                    rfa.load_kline_series([sym], "2024-04-01", "2024-04-01", horizon=24, include_cache=False)


if __name__ == "__main__":
    unittest.main()
