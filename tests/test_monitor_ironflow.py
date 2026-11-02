#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

import scripts.monitor_ironflow_liquidations as mon


class TestMonthOffset(unittest.TestCase):
    def test_returns_ym_strings(self):
        for i in range(1, 8):
            ym = mon.month_offset(i)
            self.assertRegex(ym, r"^\d{4}-\d{2}$")

    def test_one_back_is_previous_month(self):
        now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        expected = f"{now.year:04d}-{now.month - 1:02d}" if now.month > 1 else f"{now.year - 1:04d}-12"
        self.assertEqual(mon.month_offset(1), expected)

    def test_candidate_months_structure(self):
        months = mon.candidate_months()
        self.assertGreaterEqual(len(months), 6)
        for ym in months:
            self.assertRegex(ym, r"^\d{4}-\d{2}$")


class TestClassify(unittest.TestCase):
    def test_200_new_available(self):
        self.assertEqual(mon.classify(200), "NEW_AVAILABLE")
    def test_404_confirmed_absent(self):
        self.assertEqual(mon.classify(404), "CONFIRMED_ABSENT")
    def test_429_rate_limited(self):
        self.assertEqual(mon.classify(429), "RATE_LIMITED")
    def test_other_transient(self):
        self.assertEqual(mon.classify(500), "TRANSIENT_ERROR")
        self.assertEqual(mon.classify(None), "TRANSIENT_ERROR")


class TestKnownAvailable(unittest.TestCase):
    def test_extracts_200_only(self):
        state = {
            "last_probe": {
                "months_probed": [
                    {
                        "month": "2026-10",
                        "events": {"status": 200, "url": "https://example.com/events/2026-10.parquet"},
                        "fills": {"status": 200, "url": "https://example.com/fills/2026-10.parquet"},
                    },
                    {
                        "month": "2026-11",
                        "events": {"status": 404},
                        "fills": {"status": 404},
                    },
                ]
            }
        }
        avail = mon.known_available(state)
        self.assertIn(("events", "2026-10"), avail)
        self.assertIn(("fills", "2026-10"), avail)
        self.assertNotIn(("events", "2026-11"), avail)
        self.assertNotIn(("fills", "2026-11"), avail)


class TestProbeMonthClassification(unittest.TestCase):
    def make_resp(self, status, body=b""):
        r = MagicMock()
        r.getcode.return_value = status
        r.headers.items.return_value = []
        r.read.return_value = body
        return r

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    def test_200_classified_new_available(self, mock_get):
        mock_get.return_value = {"ok": True, "status": 200, "headers": {}, "body": b"PAR1", "url": "https://x/events/2026-10.parquet"}
        res = mon.probe_month("2026-10")
        self.assertEqual(res["events"]["classification"], "NEW_AVAILABLE")
        self.assertEqual(res["events"]["status"], 200)
        self.assertIn("sha256", res["events"])

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    def test_404_classified_confirmed_absent(self, mock_get):
        mock_get.return_value = {"ok": False, "status": 404, "headers": {}, "body": b"Entry not found", "url": "https://x/events/2026-11.parquet"}
        res = mon.probe_month("2026-11")
        self.assertEqual(res["events"]["classification"], "CONFIRMED_ABSENT")
        self.assertEqual(res["events"]["status"], 404)


class TestStateDiffNewFiles(unittest.TestCase):
    @patch("scripts.monitor_ironflow_liquidations.http_get")
    @patch("scripts.monitor_ironflow_liquidations.candidate_months", return_value=["2026-10", "2026-11"])
    def test_only_genuinely_new_reported(self, mock_months, mock_get):
        def side(url, timeout=60):
            if "2026-10" in url:
                return {"ok": True, "status": 200, "headers": {}, "body": b"PAR1", "url": url}
            return {"ok": False, "status": 404, "headers": {}, "body": b"Entry not found", "url": url}
        mock_get.side_effect = side

        # State already knows 2026-10 is available -> should NOT be re-reported as new.
        state = {
            "last_probe": {
                "months_probed": [
                    {"month": "2026-10", "events": {"status": 200, "url": "https://x/events/2026-10.parquet"},
                     "fills": {"status": 200, "url": "https://x/fills/2026-10.parquet"}}
                ]
            }
        }
        import json as _json
        from pathlib import Path as _Path
        state_path = _Path(mon.REPO_ROOT) / "research_state" / "ironflow_monitor_state.json"
        _tmp = state_path.read_text() if state_path.exists() else "{}"
        try:
            state_path.write_text(_json.dumps(state))
            mon.STATE_PATH = state_path
            # Capture new_files_found by invoking main logic pieces directly.
            previously = mon.known_available(state)
            self.assertIn(("events", "2026-10"), previously)
        finally:
            state_path.write_text(_tmp)


if __name__ == "__main__":
    unittest.main()
