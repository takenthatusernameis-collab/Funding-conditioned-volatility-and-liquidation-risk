#!/usr/bin/env python3
"""
FCLR-LIVE-ARCHIVE-08 Phase 3 — Independent stdlib recompute skeleton.
STDLIB ONLY. No numpy/pandas/pyarrow/requests. No network. Read-only cache.

This is a skeleton that must be completed with the actual independent recompute:
- Rebuild S from cache using a separate code path from the eval script
- Confirm all five symbols in every block/fold
- Confirm n_test >= 500
- Report all_checks_match=true
- Write fclr_live_archive08_recompute_<UTC>.json with complete results
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SESSION = RS / "session_20261128T040000Z"

SYMBOLS = ["BNBUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    print("Skeleton: independent recompute not yet implemented.")
    print("Must report all_checks_match=true before the gate can pass.")


if __name__ == "__main__":
    main()
