import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from synthetic_boundary_labels import (
    liquidation_boundary_price,
    boundary_crossed_future,
    synthetic_boundary_label,
    attach_labels,
)


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
