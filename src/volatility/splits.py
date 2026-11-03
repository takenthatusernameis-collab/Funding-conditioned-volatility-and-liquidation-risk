from __future__ import annotations

from datetime import datetime, timezone
from typing import Tuple


def parse_iso(s: str) -> datetime:
    if s.endswith('Z'):
        s2 = s[:-1] + '+00:00'
    else:
        s2 = s
    dt = datetime.fromisoformat(s2)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def in_split(ts_dt: datetime, bounds: Tuple[str, str]) -> bool:
    lo = parse_iso(bounds[0])
    hi = parse_iso(bounds[1])
    return lo <= ts_dt <= hi
