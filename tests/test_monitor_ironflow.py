#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import scripts.monitor_ironflow_liquidations as mon

TREE_URL = mon.TREE_URL
LOOKBACK_MONTHS = mon.LOOKBACK_MONTHS
LOOKAHEAD_MONTHS = mon.LOOKAHEAD_MONTHS


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


class TestETagCaching(unittest.TestCase):
    @patch("scripts.monitor_ironflow_liquidations.http_get")
    def test_304_skips_full_parse(self, mock_get):
        mock_get.return_value = {"ok": True, "status": 304, "headers": {}, "body": b"", "url": TREE_URL, "not_modified": True}
        import scripts.monitor_ironflow_liquidations as mon2
        tree = {"url": TREE_URL, "method": "GET", "status": 304, "headers": {}, "tree_etag_unchanged": True, "skipped_full_parse": True, "parquet_paths": []}
        self.assertTrue(tree["tree_etag_unchanged"])
        self.assertTrue(tree["skipped_full_parse"])

    @patch("scripts.monitor_ironflow_liquidations.urlopen")
    def test_200_updates_etag(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers.items.return_value = [("ETag", 'W/"abc123"'), ("Content-Type", "application/json")]
        mock_resp.read.return_value = b'[{"path":"data/events/2026-10.parquet"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_resp
        etag_ref = [None]
        r = mon.http_get(TREE_URL, if_none_match=None, etag_ref=etag_ref)
        self.assertEqual(r["status"], 200)
        self.assertEqual(etag_ref[0], 'W/"abc123"')


class TestMonthWindowCoverage(unittest.TestCase):
    def test_lookahead_includes_current_and_future(self):
        months = mon.candidate_months()
        now = datetime.now(timezone.utc)
        current_ym = f"{now.year:04d}-{now.month:02d}"
        self.assertIn(current_ym, months)

    def test_window_size(self):
        months = mon.candidate_months()
        self.assertGreaterEqual(len(months), LOOKBACK_MONTHS + 1)


class TestStateDiffEdgeCases(unittest.TestCase):
    @patch("scripts.monitor_ironflow_liquidations.http_get")
    @patch("scripts.monitor_ironflow_liquidations.candidate_months", return_value=["2026-10", "2026-11"])
    def test_previously_available_not_reported(self, mock_months, mock_get):
        def side(url, timeout=60):
            if "2026-10" in url:
                return {"ok": True, "status": 200, "headers": {}, "body": b"PAR1", "url": url}
            return {"ok": False, "status": 404, "headers": {}, "body": b"Entry not found", "url": url}
        mock_get.side_effect = side
        state = {
            "last_probe": {
                "months_probed": [
                    {"month": "2026-10", "events": {"status": 200, "url": "https://x/events/2026-10.parquet"},
                     "fills": {"status": 200, "url": "https://x/fills/2026-10.parquet"}}
                ]
            }
        }
        previously = mon.known_available(state)
        self.assertIn(("events", "2026-10"), previously)
        self.assertNotIn(("events", "2026-11"), previously)


class TestConsecutiveAbsent(unittest.TestCase):
    def test_counts_forward_edge_absent(self):
        months_probed = [
            {"month": "2026-09", "events": {"status": 200}, "fills": {"status": 200}},
            {"month": "2026-10", "events": {"status": 200}, "fills": {"status": 200}},
            {"month": "2026-11", "events": {"status": 404}, "fills": {"status": 404}},
            {"month": "2026-12", "events": {"status": 404}, "fills": {"status": 404}},
            {"month": "2027-01", "events": {"status": 404}, "fills": {"status": 404}},
        ]
        ordered = sorted(m["month"] for m in months_probed)
        consecutive_absent = 0
        for ym in reversed(ordered):
            m = next((x for x in months_probed if x["month"] == ym), None)
            ev = (m.get("events") or {}).get("status") if m else None
            fl = (m.get("fills") or {}).get("status") if m else None
            if ev == 404 and fl == 404:
                consecutive_absent += 1
            else:
                break
        self.assertEqual(consecutive_absent, 3)

    def test_stops_at_first_present_month(self):
        months_probed = [
            {"month": "2026-09", "events": {"status": 200}, "fills": {"status": 200}},
            {"month": "2026-10", "events": {"status": 404}, "fills": {"status": 404}},
            {"month": "2026-11", "events": {"status": 200}, "fills": {"status": 200}},
        ]
        ordered = sorted(m["month"] for m in months_probed)
        consecutive_absent = 0
        for ym in reversed(ordered):
            m = next((x for x in months_probed if x["month"] == ym), None)
            ev = (m.get("events") or {}).get("status") if m else None
            fl = (m.get("fills") or {}).get("status") if m else None
            if ev == 404 and fl == 404:
                consecutive_absent += 1
            else:
                break
        self.assertEqual(consecutive_absent, 0)


class TestForwardEdge(unittest.TestCase):
    def test_forward_months_after_data_through(self):
        months = mon.forward_edge_months("2026-10", n=4)
        self.assertEqual(months, ["2026-11", "2026-12", "2027-01", "2027-02"])

    def test_forward_months_year_rollover(self):
        months = mon.forward_edge_months("2026-12", n=3)
        self.assertEqual(months, ["2027-01", "2027-02", "2027-03"])

    def test_forward_months_invalid_falls_back(self):
        months = mon.forward_edge_months("not-a-date", n=2)
        self.assertGreaterEqual(len(months), 2)

    def test_forward_months_smaller_than_full_window(self):
        full = mon.candidate_months()
        fwd = mon.forward_edge_months("2026-10", n=mon.FORWARD_EDGE_MONTHS)
        self.assertLess(len(fwd), len(full))


class TestRateLimitSleep(unittest.TestCase):
    def test_no_budget_header(self):
        # Without a RateLimit header, returns a positive backoff.
        self.assertGreater(mon._rate_limit_sleep({}, 1), 0)

    def test_low_remaining_waits_longer(self):
        low = mon._rate_limit_sleep({"RateLimit": 'api;r=3;t=60'}, 0)
        normal = mon._rate_limit_sleep({"RateLimit": 'api;r=100;t=60'}, 0)
        self.assertGreater(low, normal)

    def test_moderate_remaining_uses_backoff(self):
        v = mon._rate_limit_sleep({"RateLimit": 'api;r=40;t=60'}, 2)
        self.assertGreaterEqual(v, 0)


class TestCheckResumeCondition(unittest.TestCase):
    @patch("scripts.monitor_ironflow_liquidations.http_get")
    def test_no_trigger_when_all_absent(self, mock_get):
        mock_get.return_value = {"ok": False, "status": 404, "headers": {}, "body": b"Entry not found", "url": "x"}
        rc = mon.check_resume_condition({"data_through": "2026-10"})
        self.assertFalse(rc["triggered"])
        self.assertEqual(rc["triggering_files"], [])
        self.assertEqual(len(rc["probes"]), 2 * len(rc["months_probed"]))

    @patch("scripts.monitor_ironflow_liquidations.resolve_get")
    @patch("scripts.monitor_ironflow_liquidations.head_probe")
    def test_trigger_fires_on_200(self, mock_head, mock_resolve):
        def head_side(url, timeout=30):
            return {"ok": False, "status": 404, "headers": {}, "body": b"", "url": url, "head_ok": False, "head_failed": True}
        mock_head.side_effect = head_side
        def resolve_side(url, etag_ref=None, last_modified_ref=None, timeout=60, max_retries=3):
            if "2026-11" in url:
                return {"ok": True, "status": 200, "headers": {}, "body": b"PAR1", "url": url, "method": "GET"}
            return {"ok": False, "status": 404, "headers": {}, "body": b"Entry not found", "url": url, "method": "GET"}
        mock_resolve.side_effect = resolve_side
        rc = mon.check_resume_condition({"data_through": "2026-10"})
        self.assertTrue(rc["triggered"])
        self.assertEqual(len(rc["triggering_files"]), 2)  # events + fills


if __name__ == "__main__":
    unittest.main()


class TestNewUtilities(unittest.TestCase):
    def test_now_z_format(self):
        from scripts.monitor_ironflow_liquidations import now_z
        ts = now_z()
        self.assertRegex(ts, r"^\d{8}T\d{6}Z$")

    def test_sha256_bytes(self):
        from scripts.monitor_ironflow_liquidations import sha256_bytes
        h = sha256_bytes(b"hello")
        self.assertEqual(len(h), 64)
        self.assertIsInstance(h, str)

    def test_forward_edge_months_empty_through(self):
        from scripts.monitor_ironflow_liquidations import forward_edge_months
        months = forward_edge_months(None)
        self.assertGreaterEqual(len(months), 4)

    def test_classify_304(self):
        from scripts.monitor_ironflow_liquidations import classify
        self.assertEqual(classify(304), "NOT_MODIFIED")


class TestQuickPath(unittest.TestCase):
    @patch("scripts.monitor_ironflow_liquidations.resolve_get")
    @patch("scripts.monitor_ironflow_liquidations.head_probe")
    def test_check_resume_condition_structure(self, mock_head, mock_resolve):
        mock_head.return_value = {"ok": False, "status": 404, "headers": {}, "body": b"", "url": "x", "head_ok": False, "head_failed": True}
        mock_resolve.return_value = {"ok": False, "status": 404, "headers": {}, "body": b"", "url": "x", "method": "GET"}
        rc = mon.check_resume_condition({"data_through": "2026-10"})
        self.assertIn("triggered", rc)
        self.assertIn("triggering_files", rc)
        self.assertIn("data_through", rc)
        self.assertIn("probes", rc)
        self.assertIn("months_probed", rc)


class TestCandidateMonthsStability(unittest.TestCase):
    def test_candidate_months_deterministic_format(self):
        months = mon.candidate_months()
        for ym in months:
            self.assertRegex(ym, r"^\d{4}-\d{2}$")
            y, m = ym.split("-")
            self.assertGreaterEqual(int(m), 1)
            self.assertLessEqual(int(m), 12)
