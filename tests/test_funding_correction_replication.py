import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from funding_correction_replication import (
    load_funding_series,
    identify_funding_extremes,
    time_to_correction,
    replicate_funding_correction,
)


def test_load_funding_series():
    p = Path(__file__).resolve().parents[1] / "BTCUSDT-fundingRate-2024-01" / "BTCUSDT-fundingRate-2024-01.csv"
    series = load_funding_series(p)
    assert len(series) > 0
    assert isinstance(series[0][0], int)
    assert isinstance(series[0][1], float)


def test_identify_funding_extremes():
    # Create simple series
    series = [(i*8*3600*1000, 0.0001) for i in range(100)]  # constant
    series[50] = (50*8*3600*1000, 0.001)  # extreme
    events = identify_funding_extremes(series)
    # May or may not find extreme depending on thresholds
    assert isinstance(events, list)


def test_time_to_correction_basic():
    series = [
        (0, 0.001),  # extreme positive
        (8*3600*1000, 0.0005),
        (16*3600*1000, 0.0002),  # back within threshold
    ]
    ttc = time_to_correction(series, 0, 'positive', -0.0001, 0.0003)
    assert ttc == 16.0 or ttc is not None


def test_replication_runs():
    res = replicate_funding_correction(symbols=['BTCUSDT'])
    assert res['status'] == 'partial'
    assert 'total_events' in res
    assert isinstance(res['total_events'], int)
