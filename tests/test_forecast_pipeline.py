import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from forecast_pipeline import (
    next_realized_variance,
    trailing_rv,
    standardize_train_only,
    apply_standardization,
    load_splits,
    common_panel_timestamps,
)

def test_target_alignment():
    prices = [100.0, 101.0, 99.0, 102.0, 100.0, 103.0]
    # at index 0, horizon 2 => returns over indices 1,2
    r = next_realized_variance(prices, 0, 2)
    expected = (math_log(101/100))**2 + (math_log(99/101))**2 if False else None
    import math
    expected = math.log(101/100)**2 + math.log(99/101)**2
    assert abs(r - expected) < 1e-12

def test_target_no_future_leak_index():
    prices = [100.0, 101.0, 99.0, 102.0]
    # horizon 3 from index0 requires 4 prices -> indices 1,2,3
    r = next_realized_variance(prices, 0, 3)
    import math
    expected = math.log(101/100)**2 + math.log(99/101)**2 + math.log(102/99)**2
    assert abs(r - expected) < 1e-12

def test_target_none_when_insufficient():
    prices = [100.0, 101.0]
    assert next_realized_variance(prices, 0, 3) is None

def test_trailing_rv():
    prices = [100.0, 101.0, 99.0, 102.0]
    import math
    r = trailing_rv(prices, 2, 2)
    expected = math.log(101/100)**2 + math.log(99/101)**2
    # trailing_rv window=2 means prices[t-2..t] = 3 prices => 2 returns
    assert abs(r - expected) < 1e-12

def test_standardization_train_only():
    train = [1.0, 2.0, 3.0]
    m, sd = standardize_train_only(train)
    assert abs(m - 2.0) < 1e-12
    # apply to test with train stats
    out = apply_standardization([10.0], m, sd)
    assert out[0] is not None

def test_splits_load():
    s = load_splits()
    assert "train" in s

def test_common_panel():
    d = {"a": {"2024-01-01", "2024-01-02"}, "b": {"2024-01-02", "2024-01-03"}}
    assert common_panel_timestamps(d) == ["2024-01-02"]
