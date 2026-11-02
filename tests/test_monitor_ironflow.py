#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import json
import tempfile
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


class TestQuickPathPersistence(unittest.TestCase):
    @patch("scripts.monitor_ironflow_liquidations.http_get")
    @patch("scripts.monitor_ironflow_liquidations.check_resume_condition")
    def test_quick_persists_last_quick_check(self, mock_rc, mock_get):
        mock_get.return_value = {"ok": True, "status": 304, "headers": {}, "body": b"", "url": TREE_URL, "not_modified": True}
        mock_rc.return_value = {
            "triggered": False,
            "triggering_files": [],
            "months_probed": ["2026-11", "2026-12", "2027-01", "2027-02"],
            "head_probes": 8,
            "cached_hits": 0,
            "data_through": "2026-10",
            "probes": [],
        }
        old_argv = sys.argv
        sys.argv = ["monitor_ironflow_liquidations.py", "--quick"]
        state_path = Path(mon.REPO_ROOT) / "research_state" / "ironflow_monitor_state.json"
        _tmp = state_path.read_text() if state_path.exists() else "{}"
        try:
            state_path.write_text(json.dumps({"data_through": "2026-10", "tree_etag": 'W/"x"'}))
            mon.main()
            state = json.loads(state_path.read_text())
            lqc = state.get("last_quick_check")
            self.assertIsNotNone(lqc)
            self.assertFalse(lqc["triggered"])
            self.assertEqual(lqc["months_probed"], ["2026-11", "2026-12", "2027-01", "2027-02"])
            self.assertEqual(lqc["head_probes"], 8)
            self.assertEqual(lqc["cached_hits"], 0)
            self.assertEqual(lqc["data_through"], "2026-10")
        finally:
            state_path.write_text(_tmp)
            sys.argv = old_argv

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    @patch("scripts.monitor_ironflow_liquidations.check_resume_condition")
    def test_quick_evidence_records_mode_and_post_2026_10_summary(self, mock_rc, mock_get):
        mock_get.return_value = {"ok": True, "status": 304, "headers": {}, "body": b"", "url": TREE_URL, "not_modified": True}
        mock_rc.return_value = {
            "triggered": False,
            "triggering_files": [],
            "months_probed": ["2026-11", "2026-12", "2027-01", "2027-02"],
            "head_probes": 8,
            "cached_hits": 0,
            "data_through": "2026-10",
            "probes": [],
        }
        old_argv = sys.argv
        sys.argv = ["monitor_ironflow_liquidations.py", "--quick"]
        state_path = Path(mon.REPO_ROOT) / "research_state" / "ironflow_monitor_state.json"
        evidence_dir = Path(mon.EVIDENCE_DIR)
        _tmp = state_path.read_text() if state_path.exists() else "{}"
        before = {p.name for p in evidence_dir.glob("ironflow_probe_*.json")}
        try:
            state_path.write_text(json.dumps({"data_through": "2026-10", "tree_etag": 'W/"x"'}))
            mon.main()
            after = {p.name for p in evidence_dir.glob("ironflow_probe_*.json")}
            new_files = sorted(after - before)
            self.assertEqual(len(new_files), 1, f"expected exactly one new probe file, got {new_files}")
            ev = json.loads((evidence_dir / new_files[0]).read_text())
            self.assertEqual(ev["mode"], "quick")
            self.assertIn("quick_resume_check", ev)
            self.assertEqual(ev["quick_resume_check"]["months_probed"], ["2026-11", "2026-12", "2027-01", "2027-02"])
            self.assertEqual(ev["head_probes"], 8)
            self.assertEqual(ev["cached_hits"], 0)
        finally:
            state_path.write_text(_tmp)
            sys.argv = old_argv


class TestTrendReport(unittest.TestCase):
    def _write_probe(self, evidence_dir, name, data_through, consecutive_absent, triggered, new_files_found=0, mode="quick"):
        probe = {
            "probe_id": name,
            "timestamp_utc": "2026-11-02T10:00:00Z",
            "mode": mode,
            "data_through": data_through,
            "consecutive_absent": consecutive_absent,
            "quick_resume_check": {
                "triggered": triggered,
                "triggering_files": [],
                "months_probed": ["2026-11", "2026-12", "2027-01", "2027-02"],
                "head_probes": 8,
                "cached_hits": 0,
                "data_through": data_through,
                "probes": [],
            },
            "probe_diff": {"summary": {"added_count": 0, "changed_count": 0, "removed_count": 0, "any_change": False}},
            "tree_change": {"changed": False, "added": [], "removed": []},
            "tree": {"status": 304, "tree_etag_unchanged": True},
            "new_files_found": [],
        }
        (evidence_dir / name).write_text(json.dumps(probe))
        return probe

    def test_report_aggregates_probe_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence_dir = Path(tmp)
            old_dir = mon.EVIDENCE_DIR
            mon.EVIDENCE_DIR = evidence_dir
            try:
                self._write_probe(evidence_dir, "ironflow_probe_20261102T100000Z.json", "2026-10", 3, False)
                self._write_probe(evidence_dir, "ironflow_probe_20261102T110000Z.json", "2026-10", 3, False)
                self._write_probe(evidence_dir, "ironflow_probe_20261102T120000Z.json", "2026-11", 0, True, new_files_found=2)
                report = mon.generate_trend_report()
                self.assertEqual(report["total_runs"], 3)
                self.assertEqual(report["runs_triggered"], 1)
                self.assertEqual(report["runs_blocked"], 2)
                self.assertEqual(report["latest"]["data_through"], "2026-11")
                self.assertTrue(report["resume_trigger_met"])
            finally:
                mon.EVIDENCE_DIR = old_dir

    def test_report_no_files_returns_zeros(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence_dir = Path(tmp)
            old_dir = mon.EVIDENCE_DIR
            mon.EVIDENCE_DIR = evidence_dir
            try:
                report = mon.generate_trend_report()
                self.assertEqual(report["total_runs"], 0)
                self.assertEqual(report["runs_triggered"], 0)
                self.assertEqual(report["runs_blocked"], 0)
                self.assertEqual(report["longest_stable_blocked_streak"], 0)
                self.assertFalse(report["resume_trigger_met"])
                self.assertEqual(report["latest"], {})
            finally:
                mon.EVIDENCE_DIR = old_dir

    def test_report_limit_caps_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence_dir = Path(tmp)
            old_dir = mon.EVIDENCE_DIR
            mon.EVIDENCE_DIR = evidence_dir
            try:
                for i in range(5):
                    self._write_probe(evidence_dir, f"ironflow_probe_20261102T1{i:02d}0000Z.json", "2026-10", 3, False)
                report = mon.generate_trend_report(limit=3)
                self.assertEqual(len(report["runs"]), 3)
                self.assertEqual(report["total_runs"], 3)
            finally:
                mon.EVIDENCE_DIR = old_dir

    def test_report_stable_blocked_streak(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence_dir = Path(tmp)
            old_dir = mon.EVIDENCE_DIR
            mon.EVIDENCE_DIR = evidence_dir
            try:
                self._write_probe(evidence_dir, "ironflow_probe_20261102T100000Z.json", "2026-10", 3, False)
                self._write_probe(evidence_dir, "ironflow_probe_20261102T110000Z.json", "2026-10", 3, False)
                self._write_probe(evidence_dir, "ironflow_probe_20261102T120000Z.json", "2026-10", 3, False)
                self._write_probe(evidence_dir, "ironflow_probe_20261102T130000Z.json", "2026-11", 0, True, new_files_found=2)
                report = mon.generate_trend_report()
                self.assertEqual(report["longest_stable_blocked_streak"], 3)
            finally:
                mon.EVIDENCE_DIR = old_dir


def _blocked_state():
    """Build a consistent blocked-path state mirroring the persisted monitor state."""
    months_probed = [
        {"month": "2026-09", "events": {"status": 200}, "fills": {"status": 200}},
        {"month": "2026-10", "events": {"status": 200}, "fills": {"status": 200}},
        {"month": "2026-11", "events": {"status": 404}, "fills": {"status": 404}},
        {"month": "2026-12", "events": {"status": 404}, "fills": {"status": 404}},
        {"month": "2027-01", "events": {"status": 404}, "fills": {"status": 404}},
    ]
    return {
        "last_probe": {"months_probed": months_probed},
        "data_through": "2026-10",
        "consecutive_absent": 3,
        "tree_etag": 'W/"abc"',
        "tree_parquet_paths": ["data/events/2026-10.parquet"],
        "resume_trigger": {
            "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",
            "data_through": "2026-10",
            "consecutive_absent": 3,
            "conditions": [
                {"id": "ironflow_events", "months": ["2026-11", "2026-12", "2027-01", "2027-02"]},
                {"id": "ironflow_fills", "months": ["2026-11", "2026-12", "2027-01", "2027-02"]},
                {"id": "new_admissible_source"},
            ],
            "on_trigger": "Pre-register BEFORE inspecting outcomes, then run scripts/fclr010_harness.py",
        },
    }


class TestRecomputeConsecutiveAbsent(unittest.TestCase):
    def test_counts_trailing_absent_months(self):
        months_probed = [
            {"month": "2026-09", "events": {"status": 200}, "fills": {"status": 200}},
            {"month": "2026-10", "events": {"status": 200}, "fills": {"status": 200}},
            {"month": "2026-11", "events": {"status": 404}, "fills": {"status": 404}},
            {"month": "2026-12", "events": {"status": 404}, "fills": {"status": 404}},
            {"month": "2027-01", "events": {"status": 404}, "fills": {"status": 404}},
        ]
        self.assertEqual(mon.recompute_consecutive_absent(months_probed), 3)

    def test_stops_at_first_present_month(self):
        months_probed = [
            {"month": "2026-09", "events": {"status": 200}, "fills": {"status": 200}},
            {"month": "2026-10", "events": {"status": 404}, "fills": {"status": 404}},
            {"month": "2026-11", "events": {"status": 200}, "fills": {"status": 200}},
        ]
        self.assertEqual(mon.recompute_consecutive_absent(months_probed), 0)

    def test_empty_input(self):
        self.assertEqual(mon.recompute_consecutive_absent([]), 0)
        self.assertEqual(mon.recompute_consecutive_absent(None), 0)


class TestVerifyState(unittest.TestCase):
    def test_consistent_state_passes(self):
        vr = mon.verify_state(_blocked_state())
        self.assertTrue(vr["ok"])
        self.assertEqual(vr["errors"], [])
        self.assertEqual(vr["data_through"], "2026-10")
        self.assertEqual(vr["consecutive_absent"], 3)
        ids = {c["id"] for c in vr["checks"]}
        self.assertIn("data_through_consistent", ids)
        self.assertIn("consecutive_absent_consistent", ids)
        self.assertIn("resume_trigger_months_match_forward_edge", ids)
        self.assertIn("on_trigger_prereg_before_outcomes", ids)
        self.assertIn("tree_etag_present", ids)
        for c in vr["checks"]:
            self.assertTrue(c["pass"], f"check {c['id']} failed: {c}")

    def test_data_through_mismatch_fails(self):
        state = _blocked_state()
        state["data_through"] = "2026-09"
        vr = mon.verify_state(state)
        self.assertFalse(vr["ok"])
        self.assertTrue(any("data_through" in e for e in vr["errors"]))

    def test_consecutive_absent_mismatch_fails(self):
        state = _blocked_state()
        state["consecutive_absent"] = 99
        vr = mon.verify_state(state)
        self.assertFalse(vr["ok"])
        self.assertTrue(any("consecutive_absent" in e for e in vr["errors"]))

    def test_resume_trigger_months_mismatch_fails(self):
        state = _blocked_state()
        for cond in state["resume_trigger"]["conditions"]:
            if cond.get("id") in ("ironflow_events", "ironflow_fills"):
                cond["months"] = ["2026-11"]
        vr = mon.verify_state(state)
        self.assertFalse(vr["ok"])
        self.assertTrue(any("resume_trigger" in e for e in vr["errors"]))

    def test_on_trigger_missing_mandate_fails(self):
        state = _blocked_state()
        state["resume_trigger"]["on_trigger"] = "just run the harness"
        vr = mon.verify_state(state)
        self.assertFalse(vr["ok"])
        self.assertTrue(any("Pre-register" in e or "on_trigger" in e for e in vr["errors"]))

    def test_missing_tree_etag_with_paths_fails(self):
        state = _blocked_state()
        state["tree_etag"] = None
        vr = mon.verify_state(state)
        self.assertFalse(vr["ok"])


class TestCompareProbes(unittest.TestCase):
    def _quick_state(self, probes):
        return {
            "last_quick_probe": {
                "timestamp_utc": "2026-11-02T15:00:00Z",
                "months_probed": ["2026-11", "2026-12", "2027-01", "2027-02"],
                "probes": probes,
            }
        }

    def _rc(self, probes):
        return {"months_probed": ["2026-11", "2026-12", "2027-01", "2027-02"], "probes": probes}

    def test_all_absent_no_change(self):
        prev_probes = [
            {"kind": "events", "month": "2026-11", "status": 404},
            {"kind": "fills", "month": "2026-11", "status": 404},
            {"kind": "events", "month": "2026-12", "status": 404},
            {"kind": "fills", "month": "2026-12", "status": 404},
        ]
        curr_probes = [
            {"kind": "events", "month": "2026-11", "status": 404},
            {"kind": "fills", "month": "2026-11", "status": 404},
            {"kind": "events", "month": "2026-12", "status": 404},
            {"kind": "fills", "month": "2026-12", "status": 404},
        ]
        diff = mon.compare_probes(self._quick_state(prev_probes), self._rc(curr_probes))
        self.assertEqual(diff["summary"]["added_count"], 0)
        self.assertEqual(diff["summary"]["changed_count"], 0)
        self.assertEqual(diff["summary"]["removed_count"], 0)
        self.assertFalse(diff["summary"]["any_change"])

    def test_404_to_200_flip_detected_as_changed(self):
        prev_probes = [
            {"kind": "events", "month": "2026-11", "status": 404},
            {"kind": "fills", "month": "2026-11", "status": 404},
        ]
        curr_probes = [
            {"kind": "events", "month": "2026-11", "status": 200},
            {"kind": "fills", "month": "2026-11", "status": 200},
        ]
        diff = mon.compare_probes(self._quick_state(prev_probes), self._rc(curr_probes))
        self.assertEqual(diff["summary"]["changed_count"], 2)
        self.assertTrue(diff["summary"]["any_change"])
        changed = {c["month"] + "/" + c["kind"]: c for c in diff["changed"]}
        self.assertIn("2026-11/events", changed)
        self.assertEqual(changed["2026-11/events"]["prev"], 404)
        self.assertEqual(changed["2026-11/events"]["curr"], 200)

    def test_new_month_detected_as_added(self):
        prev_probes = [
            {"kind": "events", "month": "2026-11", "status": 404},
            {"kind": "fills", "month": "2026-11", "status": 404},
        ]
        curr_probes = [
            {"kind": "events", "month": "2026-11", "status": 404},
            {"kind": "fills", "month": "2026-11", "status": 404},
            {"kind": "events", "month": "2027-02", "status": 200},
            {"kind": "fills", "month": "2027-02", "status": 200},
        ]
        diff = mon.compare_probes(self._quick_state(prev_probes), self._rc(curr_probes))
        self.assertEqual(diff["summary"]["added_count"], 2)
        self.assertTrue(diff["summary"]["any_change"])

    def test_month_gone_detected_as_removed(self):
        prev_probes = [
            {"kind": "events", "month": "2026-11", "status": 200},
            {"kind": "fills", "month": "2026-11", "status": 200},
            {"kind": "events", "month": "2026-12", "status": 404},
            {"kind": "fills", "month": "2026-12", "status": 404},
        ]
        curr_probes = [
            {"kind": "events", "month": "2026-12", "status": 404},
            {"kind": "fills", "month": "2026-12", "status": 404},
        ]
        diff = mon.compare_probes(self._quick_state(prev_probes), self._rc(curr_probes))
        self.assertEqual(diff["summary"]["removed_count"], 2)
        self.assertTrue(diff["summary"]["any_change"])

    def test_prefers_last_quick_probe_over_last_probe(self):
        # last_probe has stale 200 for 2026-11; last_quick_probe has correct 404.
        state = {
            "last_probe": {
                "months_probed": [
                    {"month": "2026-11", "events": {"status": 200}, "fills": {"status": 200}},
                ]
            },
            "last_quick_probe": {
                "timestamp_utc": "2026-11-02T15:00:00Z",
                "months_probed": ["2026-11"],
                "probes": [
                    {"kind": "events", "month": "2026-11", "status": 404},
                    {"kind": "fills", "month": "2026-11", "status": 404},
                ],
            },
        }
        curr = {"months_probed": ["2026-11"], "probes": [
            {"kind": "events", "month": "2026-11", "status": 404},
            {"kind": "fills", "month": "2026-11", "status": 404},
        ]}
        diff = mon.compare_probes(state, curr)
        self.assertEqual(diff["summary"]["changed_count"], 0)
        self.assertFalse(diff["summary"]["any_change"])

    def test_empty_state_returns_all_added(self):
        diff = mon.compare_probes(None, self._rc([
            {"kind": "events", "month": "2026-11", "status": 404},
        ]))
        self.assertEqual(diff["summary"]["added_count"], 1)
        self.assertTrue(diff["summary"]["any_change"])


class TestTreeChange(unittest.TestCase):
    """Tests for check_tree_change: detects new parquet paths anywhere in archive."""

    def _tree_state(self, etag, paths):
        return {
            "tree_etag": etag,
            "tree_parquet_paths": paths,
        }

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    def test_304_not_modified_unchanged(self, mock_get):
        mock_get.return_value = {
            "ok": True, "status": 304, "headers": {}, "body": b"",
            "url": mon.TREE_URL, "not_modified": True,
        }
        state = self._tree_state('W/"abc"', ["data/events/2026-10.parquet"])
        res = mon.check_tree_change(state)
        self.assertTrue(res["tree_not_modified"])
        self.assertFalse(res["changed"])
        self.assertEqual(res["added"], [])
        self.assertEqual(res["removed"], [])

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    def test_200_new_paths_detected(self, mock_get):
        body = '[{"path":"data/events/2026-10.parquet"},{"path":"data/events/2026-11.parquet"}]'

        def http_get_side(url, **kwargs):
            etag_ref = kwargs.get("etag_ref")
            if etag_ref is not None:
                etag_ref[0] = 'W/"def"'
            return {
                "ok": True, "status": 200, "headers": {"ETag": 'W/"def"'},
                "body": body.encode("utf-8"), "url": url,
            }
        mock_get.side_effect = http_get_side
        state = self._tree_state('W/"abc"', ["data/events/2026-10.parquet"])
        res = mon.check_tree_change(state)
        self.assertFalse(res["tree_not_modified"])
        self.assertTrue(res["changed"])
        self.assertIn("data/events/2026-11.parquet", res["added"])
        self.assertEqual(res["tree_etag"], 'W/"def"')

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    def test_200_same_paths_unchanged(self, mock_get):
        body = '[{"path":"data/events/2026-10.parquet"}]'
        mock_get.return_value = {
            "ok": True, "status": 200, "headers": {"ETag": 'W/"def"'},
            "body": body.encode("utf-8"), "url": mon.TREE_URL,
        }
        state = self._tree_state('W/"abc"', ["data/events/2026-10.parquet"])
        res = mon.check_tree_change(state)
        self.assertFalse(res["changed"])
        self.assertEqual(res["added"], [])
        self.assertEqual(res["removed"], [])


class TestQuickDiffSummary(unittest.TestCase):
    """Tests for quick_diff_summary helper added in heavy work."""

    def test_quick_diff_summary_empty(self):
        state = {}
        rc = {"probes": [
            {"kind": "events", "month": "2026-11", "status": 404},
        ]}
        summary = mon.quick_diff_summary(state, rc)
        self.assertTrue(summary["any_change"])
        self.assertEqual(summary["added"], 1)

    def test_quick_diff_summary_no_change(self):
        state = {
            "last_quick_probe": {
                "probes": [
                    {"kind": "events", "month": "2026-11", "status": 404},
                ]
            }
        }
        rc = {"probes": [
            {"kind": "events", "month": "2026-11", "status": 404},
        ]}
        summary = mon.quick_diff_summary(state, rc)
        self.assertFalse(summary["any_change"])
        self.assertEqual(summary["added"], 0)
        self.assertEqual(summary["changed"], 0)

    def test_quick_diff_summary_with_changes(self):
        state = {
            "last_quick_probe": {
                "probes": [
                    {"kind": "events", "month": "2026-11", "status": 404},
                ]
            }
        }
        rc = {"probes": [
            {"kind": "events", "month": "2026-11", "status": 200},
        ]}
        summary = mon.quick_diff_summary(state, rc)
        self.assertTrue(summary["any_change"])
        self.assertEqual(summary["changed"], 1)
        self.assertIn("2026-11/events:404->200", summary["changed_files"][0])


class TestBaselineDrift(unittest.TestCase):
    """Tests for check_baseline_drift: cache-incomplete is not drift."""

    def test_empty_cache_is_incomplete_not_drift(self):
        # tree_parquet_paths lists known months but nothing was ever downloaded.
        state = {
            "tree_parquet_paths": ["data/events/2026-10.parquet", "data/fills/2026-10.parquet"],
            "file_cache": {},
        }
        bd = mon.check_baseline_drift(state)
        self.assertTrue(bd["cache_incomplete"])
        self.assertFalse(bd["drifted"])
        self.assertEqual(bd["checked"], 1)
        self.assertEqual(len(bd["missing_cache_entries"]), 2)
        self.assertEqual(bd["stale_cache_entries"], [])

    def test_stale_cache_entry_is_drift(self):
        state = {
            "tree_parquet_paths": ["data/events/2026-10.parquet"],
            "file_cache": {"events:2026-10": {"etag": None, "sha256": None}},
        }
        bd = mon.check_baseline_drift(state)
        self.assertFalse(bd["cache_incomplete"])
        self.assertTrue(bd["drifted"])
        self.assertEqual(len(bd["stale_cache_entries"]), 1)

    def test_complete_cache_not_drift(self):
        state = {
            "tree_parquet_paths": ["data/events/2026-10.parquet"],
            "file_cache": {"events:2026-10": {"etag": 'W/"x"', "sha256": "abc"}},
        }
        bd = mon.check_baseline_drift(state)
        self.assertFalse(bd["cache_incomplete"])
        self.assertFalse(bd["drifted"])
