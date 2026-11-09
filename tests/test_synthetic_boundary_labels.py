import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from synthetic_boundary_labels import (
    liquidation_boundary_price,
    boundary_crossed_future,
    synthetic_boundary_label,
    attach_labels,
)
from run_h003 import build_mark_index, find_mark_csv

REPO = Path(__file__).resolve().parents[1]


def _make_tmp_mark_csv(sym="BTCUSDT", date_str="2024-07-23"):
    tmp = Path(tempfile.mkdtemp())
    mark_dir = tmp / f"markPriceKlines-1h-{date_str}"
    mark_dir.mkdir(parents=True)
    csv_file = mark_dir / f"{sym}-1h-{date_str}.csv"
    csv_file.write_text("open_time,close\n1721692800000,67458.10\n")
    klines_dir = tmp / f"klines-1h-{date_str}"
    klines_dir.mkdir(parents=True)
    (klines_dir / f"{sym}-1h-{date_str}.csv").write_text("open_time,close\n1721692800000,67458.10\n")
    return tmp, csv_file


def test_boundary_price_long():
    b = liquidation_boundary_price(100.0, 5.0, "long", 0.0)
    assert abs(b - 80.0) < 1e-12


def test_boundary_crossing_future():
    prices = [100.0, 95.0, 79.0, 81.0]
    # at idx0 boundary 80, future min 79 -> crossed
    assert boundary_crossed_future(prices, 0, 80.0, "long", 3) is True


def test_no_leakage_uses_future_only():
    prices = [50.0, 100.0, 95.0, 90.0]
    # boundary based on entry at idx1? label at idx0 uses entry prices[0]=50 -> boundary 40; future after 0 all >40 => false
    assert synthetic_boundary_label(prices, 0, horizon=3, leverage=5.0) == 0


def test_insufficient_horizon_none():
    prices = [100.0, 99.0]
    assert synthetic_boundary_label(prices, 0, horizon=3, leverage=5.0) is None


def test_attach_length():
    prices = [100.0, 99.0, 98.0, 97.0, 96.0]
    out = attach_labels(prices, horizon=2, leverage=5.0)
    assert len(out) == len(prices)
    assert out[-1] is None
    assert out[-2] is None


def test_build_mark_index_finds_mark_price_csvs():
    tmp, csv_file = _make_tmp_mark_csv()
    index = build_mark_index(root=tmp)
    assert ('BTCUSDT', '2024-07-23') in index
    assert index[('BTCUSDT', '2024-07-23')] == csv_file.resolve()


def test_build_mark_index_ignores_non_csv():
    tmp = Path(tempfile.mkdtemp())
    mark_dir = tmp / "markPriceKlines-1h-2024-07-23"
    mark_dir.mkdir(parents=True)
    (mark_dir / "BTCUSDT-1h-2024-07-23.zip").write_text("not csv")
    (mark_dir / "BTCUSDT-1h-2024-07-23.csv").write_text("open_time,close\n1,100\n")

    index = build_mark_index(root=tmp)
    assert len(index) == 1


def test_find_mark_csv_with_index_matches_without_index():
    index = build_mark_index()
    key = ('BTCUSDT', '2024-07-23')
    assert key in index, "FCLR-002 test window mark data must be indexed"
    with_index = find_mark_csv('BTCUSDT', '2024-07-23', index)
    without_index = find_mark_csv('BTCUSDT', '2024-07-23')
    assert with_index == without_index
