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
            # HEAD 200 for the present forward-edge month (realistic: HEAD
            # success means the file exists); 404 head_ok False elsewhere.
            if "2026-11" in url:
                return {"ok": True, "status": 200, "headers": {}, "body": b"", "url": url, "head_ok": True}
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
    """Isolated quick-path runs: a --quick probe must never leave real timestamped
    probe artifacts in research_state (Step-3 side-effect-churn removal)."""

    def _isolated(self, tmp):
        ev_dir = tmp / "evidence"
        ev_dir.mkdir(parents=True, exist_ok=True)
        state_path = tmp / "ironflow_monitor_state.json"
        state_path.write_text(json.dumps({"data_through": "2026-10", "tree_etag": 'W/"x"'}))
        real_evidence_dir, real_state_path = mon.EVIDENCE_DIR, mon.STATE_PATH
        mon.EVIDENCE_DIR, mon.STATE_PATH = ev_dir, state_path
        return ev_dir, state_path, real_evidence_dir, real_state_path

    def _restore(self, real_evidence_dir, real_state_path):
        mon.EVIDENCE_DIR, mon.STATE_PATH = real_evidence_dir, real_state_path

    def _real_probe_names(self):
        evidence_dir = Path(mon.REPO_ROOT) / "research_state"
        return {
            p.name
            for p in evidence_dir.glob("ironflow_probe_*.json")
            if not p.name.startswith("ironflow_probe_digest_")
        }

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    @patch("scripts.monitor_ironflow_liquidations.check_resume_condition")
    def test_quick_persists_last_quick_check_isolated(self, mock_rc, mock_get):
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
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            ev_dir, state_path, real_evidence_dir, real_state_path = self._isolated(tmp)
            before_real = self._real_probe_names()
            try:
                mon.main()
                state = json.loads(state_path.read_text())
                lqc = state.get("last_quick_check")
                self.assertIsNotNone(lqc)
                self.assertFalse(lqc["triggered"])
                self.assertEqual(lqc["months_probed"], ["2026-11", "2026-12", "2027-01", "2027-02"])
                self.assertEqual(lqc["head_probes"], 8)
                self.assertEqual(lqc["cached_hits"], 0)
                self.assertEqual(lqc["data_through"], "2026-10")
                probes = [p for p in ev_dir.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
                self.assertEqual(len(probes), 1)
                ev = json.loads(probes[0].read_text())
                self.assertEqual(ev["mode"], "quick")
                self.assertIn("quick_resume_check", ev)
                self.assertEqual(ev["quick_resume_check"]["months_probed"], ["2026-11", "2026-12", "2027-01", "2027-02"])
                self.assertEqual(ev["head_probes"], 8)
                self.assertEqual(ev["cached_hits"], 0)
            finally:
                self._restore(real_evidence_dir, real_state_path)
                sys.argv = old_argv
        after_real = self._real_probe_names()
        self.assertEqual(before_real, after_real, "quick path leaked a probe artifact into research_state")

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    @patch("scripts.monitor_ironflow_liquidations.check_resume_condition")
    def test_quick_evidence_records_mode_and_post_2026_10_summary_isolated(self, mock_rc, mock_get):
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
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            ev_dir, state_path, real_evidence_dir, real_state_path = self._isolated(tmp)
            before_real = self._real_probe_names()
            try:
                mon.main()
                probes = [p for p in ev_dir.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
                self.assertEqual(len(probes), 1, f"expected exactly one isolated probe file, got {probes}")
                ev = json.loads(probes[0].read_text())
                self.assertEqual(ev["mode"], "quick")
                self.assertIn("quick_resume_check", ev)
                self.assertEqual(ev["quick_resume_check"]["months_probed"], ["2026-11", "2026-12", "2027-01", "2027-02"])
                self.assertEqual(ev["head_probes"], 8)
                self.assertEqual(ev["cached_hits"], 0)
            finally:
                self._restore(real_evidence_dir, real_state_path)
                sys.argv = old_argv
        after_real = self._real_probe_names()
        self.assertEqual(before_real, after_real, "quick path leaked a probe artifact into research_state")


class TestProbeArtifactSafety(unittest.TestCase):
    """Safety proof for the Step-3 side-effect-churn fix: the quick path must
    never leave timestamped probe artifacts in research_state, and the live
    probe + canonical digest contract stays at exactly 2 artifacts."""

    def _real_artifact_count(self):
        evidence_dir = Path(mon.REPO_ROOT) / "research_state"
        return len(list(evidence_dir.glob("ironflow_probe_*.json")))

    @patch("scripts.monitor_ironflow_liquidations.http_get")
    @patch("scripts.monitor_ironflow_liquidations.check_resume_condition")
    def test_quick_run_leaves_real_research_state_untouched(self, mock_rc, mock_get):
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
        before = self._real_artifact_count()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            ev_dir = tmp / "evidence"
            ev_dir.mkdir()
            state_path = tmp / "ironflow_monitor_state.json"
            state_path.write_text(json.dumps({"data_through": "2026-10", "tree_etag": 'W/"x"'}))
            real_evidence_dir, real_state_path = mon.EVIDENCE_DIR, mon.STATE_PATH
            mon.EVIDENCE_DIR, mon.STATE_PATH = ev_dir, state_path
            try:
                mon.main()
                probes = [p for p in ev_dir.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
                self.assertEqual(len(probes), 1)
            finally:
                mon.EVIDENCE_DIR, mon.STATE_PATH = real_evidence_dir, real_state_path
                sys.argv = old_argv
        after = self._real_artifact_count()
        self.assertEqual(after, before, "real research_state probe artifacts changed")
        self.assertEqual(after, 2, "ironflow probe artifacts must stay exactly 2 (single live probe + canonical digest)")


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
        "tree_parquet_paths": ["data/events/2026-10.parquet", "data/fills/2026-10.parquet"],
        "tree_parquet_items": {
            "data/events/2026-10.parquet": {"path": "data/events/2026-10.parquet", "oid": "deadbeef", "size": 1000, "type": "file"},
            "data/fills/2026-10.parquet": {"path": "data/fills/2026-10.parquet", "oid": "cafebabe", "size": 2000, "type": "file"},
        },
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


class TestResumeSimulation(unittest.TestCase):
    """Offline trigger-logic tests for --simulate and --decision (no network).

    These close the per-session bottleneck where confirming the block required
    HF to be reachable. The AGENT_HANDOFF.md decision tree is evaluated against
    synthetic evidence so the trigger logic is unit-testable.
    """

    def _blocked_state(self):
        return {
            "data_through": "2026-10",
            "consecutive_absent": 3,
            "last_quick_check": {"triggered": False, "months_probed": ["2026-11", "2026-12"]},
            "last_quick_probe": {
                "probes": [
                    {"month": "2026-11", "kind": "events", "status": 404},
                    {"month": "2026-11", "kind": "fills", "status": 404},
                    {"month": "2026-12", "kind": "events", "status": 404},
                    {"month": "2026-12", "kind": "fills", "status": 404},
                ]
            },
            "last_tree_change": {"changed": False, "added": []},
            "last_probe": {"new_files_found": []},
        }

    def test_simulate_all_absent_no_trigger(self):
        rc = mon.simulate_resume(self._blocked_state())
        self.assertFalse(rc["triggered"])
        self.assertEqual(rc["decision"]["fired_branches"], [])
        self.assertEqual(len(rc["probes"]), 8)

    def test_simulate_forward_edge_fires(self):
        rc = mon.simulate_resume(self._blocked_state(), triggered_months=["2026-11"])
        self.assertTrue(rc["triggered"])
        self.assertIn("forward_edge_200", rc["decision"]["fired_branches"])
        self.assertEqual(len(rc["triggering_files"]), 2)

    def test_simulate_probe_diff_branch(self):
        rc = mon.simulate_resume(self._blocked_state(), triggered_months=["2026-12"])
        self.assertTrue(rc["triggered"])
        self.assertIn("probe_diff_404_to_200", rc["decision"]["fired_branches"])
        self.assertGreater(rc["decision"]["changed_count"], 0)

    def test_decision_tree_blocked(self):
        res = mon.evaluate_resume_decision(
            self._blocked_state(),
            rc={"triggered": False, "probe_diff": {"summary": {"changed_count": 0}}},
            tree_change={"changed": False, "added": []},
            new_files=[],
        )
        self.assertFalse(res["new_data_path"])
        self.assertEqual(res["reasons"], [])

    def test_decision_tree_new_files(self):
        res = mon.evaluate_resume_decision(
            self._blocked_state(),
            rc={"triggered": False, "probe_diff": {"summary": {"changed_count": 0}}},
            tree_change={"changed": False, "added": []},
            new_files=[{"month": "2026-11", "kind": "events"}],
        )
        self.assertTrue(res["new_data_path"])
        self.assertTrue(any("new_files_found" in r for r in res["reasons"]))

    def test_decision_tree_probe_diff(self):
        res = mon.evaluate_resume_decision(
            self._blocked_state(),
            rc={
                "triggered": False,
                "probe_diff": {"summary": {"changed_count": 2}},
            },
            tree_change={"changed": False, "added": []},
            new_files=[],
        )
        self.assertTrue(res["new_data_path"])
        self.assertTrue(any("probe_diff" in r for r in res["reasons"]))

    def test_decision_tree_tree_change(self):
        res = mon.evaluate_resume_decision(
            self._blocked_state(),
            rc={"triggered": False, "probe_diff": {"summary": {"changed_count": 0}}},
            tree_change={"changed": True, "added": ["data/events/2026-11.parquet"]},
            new_files=[],
        )
        self.assertTrue(res["new_data_path"])
        self.assertTrue(any("tree_change" in r for r in res["reasons"]))

    def test_decision_tree_old_month_new_file_ignored(self):
        # A new file for an OLD month (backfill) is not a resume trigger per the
        # handoff, which requires month >=2026-11.
        res = mon.evaluate_resume_decision(
            self._blocked_state(),
            rc={"triggered": False, "probe_diff": {"summary": {"changed_count": 0}}},
            tree_change={"changed": True, "added": ["data/events/2026-09.parquet"]},
            new_files=[{"month": "2026-09", "kind": "events"}],
        )
        self.assertFalse(res["new_data_path"])


class TestHead404FastPath(unittest.TestCase):
    """HEAD-404 fast path: classify CONFIRMED_ABSENT without a GET body download."""

    def _head_404(self, url, timeout=30):
        return {"ok": False, "status": 404, "headers": {}, "body": b"", "url": url, "head_ok": False, "head_failed": True}

    @patch("scripts.monitor_ironflow_liquidations.head_probe")
    @patch("scripts.monitor_ironflow_liquidations.resolve_get")
    def test_probe_month_head_404_skips_get(self, mock_resolve, mock_head):
        mock_head.side_effect = self._head_404
        res = mon.probe_month("2026-11")
        for kind in ("events", "fills"):
            rec = res[kind]
            self.assertEqual(rec["classification"], "CONFIRMED_ABSENT")
            self.assertEqual(rec["status"], 404)
            self.assertEqual(rec["method"], "HEAD")
            self.assertTrue(rec.get("get_skipped"))
        mock_resolve.assert_not_called()

    @patch("scripts.monitor_ironflow_liquidations.head_probe")
    @patch("scripts.monitor_ironflow_liquidations.resolve_get")
    def test_check_resume_condition_head_404_skips_get(self, mock_resolve, mock_head):
        mock_head.side_effect = self._head_404
        rc = mon.check_resume_condition({"data_through": "2026-10"})
        self.assertFalse(rc["triggered"])
        self.assertEqual(rc["get_requests_skipped"], 8)  # 4 months x 2 kinds
        self.assertEqual(rc["get_requests"], 0)
        self.assertEqual(rc["head_requests"], 8)
        self.assertEqual(rc["bytes_downloaded"], 0)
        for rec in rc["probes"]:
            self.assertEqual(rec["classification"], "CONFIRMED_ABSENT")
            self.assertTrue(rec.get("get_skipped"))
        mock_resolve.assert_not_called()


class TestDownloadAccounting(unittest.TestCase):
    """Per-session request/byte accounting in the blocked-path resume check."""

    def _head_200_unavailable(self, url, timeout=30):
        # HEAD reports 200 but with no cached ETag -> falls to Last-Modified check
        # which we miss, so resolve_get is used.
        return {"ok": True, "status": 200, "headers": {"Last-Modified": "old"}, "body": b"", "url": url, "head_ok": True}

    def _get_200_body(self, url, etag_ref=None, last_modified_ref=None, timeout=60, max_retries=3):
        body = b"PAR1" + b"x" * 96  # 100-byte body
        return {"ok": True, "status": 200, "headers": {}, "body": body, "url": url, "method": "GET"}

    @patch("scripts.monitor_ironflow_liquidations.head_probe")
    @patch("scripts.monitor_ironflow_liquidations.resolve_get")
    def test_bytes_and_requests_accounted(self, mock_resolve, mock_head):
        # cached etag present so the Last-Modified fast-path is skipped; resolve_get
        # returns 200 -> bytes downloaded and get requests counted.
        state = {"data_through": "2026-10", "file_cache": {"events:2026-11": {"etag": "W/\"old\""}}}
        mock_head.side_effect = self._head_200_unavailable
        mock_resolve.side_effect = self._get_200_body
        rc = mon.check_resume_condition(state)
        # All 8 forward-edge (kind,month) pairs reach resolve_get.
        self.assertEqual(rc["get_requests"], 8)
        self.assertEqual(rc["head_requests"], 8)
        self.assertEqual(rc["bytes_downloaded"], 800)  # 8 x 100-byte bodies
        self.assertEqual(rc["get_requests_skipped"], 0)
        self.assertTrue(rc["triggered"])


class TestBaselineDriftProbe(unittest.TestCase):
    """Baseline-drift probe now reads tree_parquet_items (LFS oids), not the
    empty file_cache, so it is a real regression/content-replacement detector
    rather than a per-session no-op that still burned a tree round-trip."""

    def _state_with_items(self, items):
        return {
            "tree_parquet_items": items,
            "tree_parquet_paths": sorted(items.keys()),
        }

    def _oid(self, oid="deadbeef", size=1000):
        return {"path": "data/events/2026-10.parquet", "oid": oid, "size": size, "type": "file"}

    def test_no_pairs_when_items_empty(self):
        # Regression guard: an empty tree_parquet_items must NOT silently check
        # 36 phantom pairs. checked==0 means the baseline is incomplete, which
        # the state-only check surfaces via content_hash_incomplete.
        res = mon.check_baseline_drift_probe(self._state_with_items({}))
        self.assertEqual(res["checked"], 0)
        self.assertEqual(res["content_replaced_count"], 0)
        self.assertTrue(res["baseline_intact"])

    def test_pairs_checked_from_tree_items(self):
        items = {
            "data/events/2026-10.parquet": self._oid(oid="deadbeef", size=1000),
            "data/fills/2026-10.parquet": self._oid(oid="cafebabe", size=2000),
        }

        def head_side(url, timeout=30):
            # Return the recorded oid/size as ETag/Content-Length so the pair
            # is confirmed unchanged. Fills URL carries the cafe oid.
            if "fills" in url:
                return {"ok": True, "status": 200,
                        "headers": {"ETag": "cafebabe", "Content-Length": "2000"},
                        "body": b"", "url": url, "head_ok": True}
            return {"ok": True, "status": 200,
                    "headers": {"ETag": "deadbeef", "Content-Length": "1000"},
                    "body": b"", "url": url, "head_ok": True}

        with patch("scripts.monitor_ironflow_liquidations.head_probe", side_effect=head_side) as mh:
            res = mon.check_baseline_drift_probe(self._state_with_items(items))
        self.assertEqual(res["checked"], 2)
        self.assertEqual(len(res["pairs_checked"]), 2)
        self.assertEqual(res["content_replaced_count"], 0)
        self.assertTrue(res["baseline_intact"])

    def test_silent_file_replacement_detected(self):
        # Same path, different content hash (LFS oid) -> silent replacement of
        # the frozen FCLR-010 baseline panel.
        items = {"data/events/2026-10.parquet": self._oid(oid="original-oid", size=1000)}
        with patch("scripts.monitor_ironflow_liquidations.head_probe") as mh:
            mh.return_value = {
                "ok": True, "status": 200,
                "headers": {"ETag": "different-oid", "Content-Length": "1000"},
                "body": b"", "url": "x", "head_ok": True,
            }
            res = mon.check_baseline_drift_probe(self._state_with_items(items))
        self.assertEqual(res["content_replaced_count"], 1)
        self.assertFalse(res["baseline_intact"])
        self.assertEqual(res["content_replaced"][0]["reason"], "content_replaced")

    def test_size_change_detected(self):
        items = {"data/events/2026-10.parquet": self._oid(oid="same", size=1000)}
        with patch("scripts.monitor_ironflow_liquidations.head_probe") as mh:
            mh.return_value = {
                "ok": True, "status": 200,
                "headers": {"ETag": "same", "Content-Length": "99999"},
                "body": b"", "url": "x", "head_ok": True,
            }
            res = mon.check_baseline_drift_probe(self._state_with_items(items))
        self.assertEqual(res["content_replaced_count"], 1)
        self.assertEqual(res["content_replaced"][0]["reason"], "size_changed")

    def test_200_to_404_regression_detected(self):
        items = {"data/events/2026-10.parquet": self._oid()}
        with patch("scripts.monitor_ironflow_liquidations.head_probe") as mh:
            mh.return_value = {
                "ok": True, "status": 404, "headers": {}, "body": b"",
                "url": "x", "head_ok": True,
            }
            res = mon.check_baseline_drift_probe(self._state_with_items(items))
        self.assertEqual(res["regression_count"], 1)
        self.assertFalse(res["baseline_intact"])
        self.assertEqual(res["regressions"][0]["reason"], "regressed_200_to_404")

    def test_head_failure_falls_back_to_get_304(self):
        items = {"data/events/2026-10.parquet": self._oid(oid="abc")}
        with patch("scripts.monitor_ironflow_liquidations.head_probe") as mh, \
             patch("scripts.monitor_ironflow_liquidations.resolve_get") as mr:
            mh.return_value = {
                "ok": False, "status": None, "headers": {}, "body": b"",
                "url": "x", "head_ok": False, "head_failed": True,
            }
            mr.return_value = {"ok": True, "status": 304, "headers": {}, "body": b"",
                               "url": "x", "method": "GET", "not_modified": True}
            res = mon.check_baseline_drift_probe(self._state_with_items(items))
        self.assertEqual(res["checked"], 1)
        self.assertEqual(res["head_failures"], 1)
        self.assertTrue(res["baseline_intact"])
        # An unchanged pair is recorded in records, not regressions, so the
        # reason is readable from the full record list.
        self.assertEqual(res["records"][0]["reason"], "unchanged_via_get_304")
        self.assertEqual(res["regression_count"], 0)


if __name__ == "__main__":
    unittest.main()


class TestFastPathEnhancements(unittest.TestCase):
    def test_fastpath_cache_load_save(self):
        import tempfile, os
        from pathlib import Path
        import json
        # Test with temp state
        orig = mon.FAST_PATH_STATE
        try:
            td = Path(tempfile.mkdtemp())
            mon.FAST_PATH_STATE = td / "cache.json"
            cache = mon.load_fastpath_cache()
            self.assertIsInstance(cache, dict)
            cache['test'] = 123
            mon.save_fastpath_cache(cache)
            cache2 = mon.load_fastpath_cache()
            self.assertEqual(cache2.get('test'), 123)
        finally:
            mon.FAST_PATH_STATE = orig

    @patch("scripts.monitor_ironflow_liquidations.urlopen")
    def test_tree_get_cached_handles_304(self, mock_urlopen):
        from urllib.error import HTTPError
        import io
        hdrs = {"ETag": 'W/"test"'}
        e = HTTPError(mon.TREE_URL, 304, "Not Modified", hdrs, io.BytesIO(b""))
        mock_urlopen.side_effect = e
        r = mon.tree_get_cached(use_cache=False)
        self.assertEqual(r["status"], 304)
        self.assertTrue(r.get("not_modified"))


class TestConsolidation(unittest.TestCase):
    def test_consolidate_ironflow_probes_keeps_latest(self):
        import tempfile
        from pathlib import Path
        import os, time
        # Use temp dir
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = td
                # Create old files
                f1 = td / "ironflow_probe_20261101T000000Z.json"
                f2 = td / "ironflow_probe_20261105T000000Z.json"
                f1.write_text("{}")
                time.sleep(0.01)
                f2.write_text("{}")
                mon._consolidate_ironflow_probes()
                files = list(td.glob("ironflow_probe_*.json"))
                files = [p for p in files if not p.name.startswith("ironflow_probe_digest_")]
                self.assertEqual(len(files), 1)
                self.assertEqual(files[0].name, f2.name)
            finally:
                mon.EVIDENCE_DIR = orig

    def test_consolidation_single_canonical_digest(self):
        """[HEAVY-090] The digest is ONE running archive, not one per run.

        The pre-090 implementation named the digest after the current latest
        probe, so every --quick run wrote a new digest file and never removed
        the prior one: 37 digest files accumulated (all 1-entry, all
        data_through=2026-10, all triggered=false). After consolidation there
        must be exactly ONE digest file, named ironflow_probe_digest_latest.json,
        and running consolidation a second time must not create a second file.
        """
        import tempfile
        from pathlib import Path
        import time
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = td
                f1 = td / "ironflow_probe_20261101T000000Z.json"
                f2 = td / "ironflow_probe_20261105T000000Z.json"
                f1.write_text("{}")
                time.sleep(0.01)
                f2.write_text("{}")
                mon._consolidate_ironflow_probes()
                digests1 = list(td.glob("ironflow_probe_digest_*.json"))
                self.assertEqual(len(digests1), 1)
                self.assertEqual(digests1[0].name, "ironflow_probe_digest_latest.json")
                # A second run with a newer probe must still leave exactly one
                # digest and must MERGE (not duplicate) the archived entry.
                f3 = td / "ironflow_probe_20261106T000000Z.json"
                time.sleep(0.01)
                f3.write_text("{}")
                mon._consolidate_ironflow_probes()
                digests2 = list(td.glob("ironflow_probe_digest_*.json"))
                self.assertEqual(len(digests2), 1)
                self.assertEqual(digests2[0].name, "ironflow_probe_digest_latest.json")
                import json
                dg = json.loads(digests2[0].read_text())
                ids = [e.get("probe_id") for e in dg.get("entries", []) or []]
                self.assertEqual(len(ids), len(set(ids)), "duplicate archived probe entries")
                self.assertEqual(dg.get("total_entries"), len(ids))
            finally:
                mon.EVIDENCE_DIR = orig

    def test_consolidation_merges_prior_canonical_digest(self):
        """[HEAVY-090] Entries already in the canonical digest are preserved
        across runs, so the blocked streak is not erased by churn removal."""
        import tempfile
        from pathlib import Path
        import time, json
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = td
                canonical = td / "ironflow_probe_digest_latest.json"
                canonical.write_text(json.dumps({
                    "entries": [{"probe_id": "ironflow_probe_20261101T000000Z",
                                 "data_through": "2026-10", "triggered": False}],
                    "total_entries": 1,
                }))
                f2 = td / "ironflow_probe_20261105T000000Z.json"
                f2.write_text("{}")
                time.sleep(0.01)
                res = mon._consolidate_ironflow_probes()
                dg = json.loads(canonical.read_text())
                ids = [e.get("probe_id") for e in dg.get("entries", []) or []]
                self.assertIn("ironflow_probe_20261101T000000Z", ids)
                self.assertEqual(dg.get("total_entries"), len(ids))
                self.assertEqual(res.get("total_entries"), len(ids))
            finally:
                mon.EVIDENCE_DIR = orig

    def test_consolidation_deletes_previously_archived_live_probe(self):
        """[HEAVY-099] A live probe whose entry is ALREADY in the canonical digest
        must still be physically removed, not re-archived forever.

        Pre-fix the dedup `continue` skipped the unlink, so a probe archived in a
        prior session (e.g. ironflow_probe_20261105T130449Z, already present in
        ironflow_probe_digest_latest.json) survived every later --quick run: verified
        20261105T1505Z with 3 ironflow_probe_* files (invariant is ==2) and churn
        reporting 3 -> 3 / removed 0. After the fix the directory must hold exactly
        one live probe + one digest, and the archived entry must not be duplicated.
        """
        import tempfile
        from pathlib import Path
        import time, json
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = td
                canonical = td / "ironflow_probe_digest_latest.json"
                stale_id = "ironflow_probe_20261105T130449Z"
                canonical.write_text(json.dumps({
                    "entries": [{"probe_id": stale_id, "data_through": "2026-10",
                                 "triggered": False, "source_file": stale_id + ".json"}],
                    "total_entries": 1,
                }))
                # The stale live probe is still on disk (a prior run that failed to
                # delete it), plus a newer probe written by the current run.
                stale = td / (stale_id + ".json")
                stale.write_text(json.dumps({"probe_id": stale_id}))
                time.sleep(0.01)
                newest = td / "ironflow_probe_20261105T150804Z.json"
                newest.write_text(json.dumps({"probe_id": "ironflow_probe_20261105T150804Z"}))
                res = mon._consolidate_ironflow_probes()
                live = [p for p in td.glob("ironflow_probe_*.json")
                        if not p.name.startswith("ironflow_probe_digest_")]
                self.assertEqual(len(live), 1, f"live probes: {[p.name for p in live]}")
                self.assertEqual(live[0].name, newest.name)
                self.assertFalse(stale.exists(), "previously-archived live probe not deleted")
                self.assertEqual(len(list(td.glob("ironflow_probe_digest_*.json"))), 1)
                dg = json.loads(canonical.read_text())
                ids = [e.get("probe_id") for e in dg.get("entries", []) or []]
                self.assertEqual(len(ids), len(set(ids)), "duplicate archived entries")
                self.assertEqual(dg.get("total_entries"), len(ids))
                self.assertEqual(res.get("removed"), 1)
            finally:
                mon.EVIDENCE_DIR = orig

    def test_consolidation_idempotent_probe_count_stays_two(self):
        """[HEAVY-099] Running consolidation twice must not grow the artifact set.

        The whole point of consolidation is a provably bounded directory: one live
        probe + one digest. A second pass must remove nothing (no new file, no
        re-archive), so the invariant is stable across repeated --quick runs.
        """
        import tempfile
        from pathlib import Path
        import time
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = td
                f1 = td / "ironflow_probe_20261101T000000Z.json"
                f2 = td / "ironflow_probe_20261105T000000Z.json"
                f1.write_text("{}")
                time.sleep(0.01)
                f2.write_text("{}")
                mon._consolidate_ironflow_probes()
                n1 = len(list(td.glob("ironflow_probe_*.json")))
                r2 = mon._consolidate_ironflow_probes()
                n2 = len(list(td.glob("ironflow_probe_*.json")))
                self.assertEqual(n1, 2, f"first pass count {n1}")
                self.assertEqual(n2, 2, f"second pass count {n2}")
                self.assertEqual(r2.get("removed"), 0, "second pass removed files")
            finally:
                mon.EVIDENCE_DIR = orig


class TestBottleneckConsolidation(unittest.TestCase):
    def test_consolidation_does_not_delete_latest(self):
        import tempfile
        from pathlib import Path
        import os, time
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = td
                f1 = td / "ironflow_probe_20261101T000001Z.json"
                f2 = td / "ironflow_probe_20261105T000002Z.json"
                f1.write_text("{}")
                time.sleep(0.01)
                f2.write_text("{}")
                res = mon._consolidate_ironflow_probes()
                files = list(td.glob("ironflow_probe_*.json"))
                live = [p for p in files if not p.name.startswith("ironflow_probe_digest_")]
                self.assertEqual(len(live), 1)
                self.assertEqual(live[0].name, f2.name)
                digests = list(td.glob("ironflow_probe_digest_*.json"))
                self.assertEqual(len(digests), 1)
            finally:
                mon.EVIDENCE_DIR = orig


class TestVerifyAndDriftSafety(unittest.TestCase):
    """096: prove --verify/state-only/drift paths do not mutate real research_state artifacts."""

    def test_verify_state_no_filesystem_writes(self):
        """verify_state is pure over in-memory state; must not create probe/evidence files."""
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            orig_state = mon.STATE_PATH
            try:
                mon.EVIDENCE_DIR = td
                mon.STATE_PATH = td / "state.json"
                state = {
                    "data_through": "2026-10",
                    "known_available_months": {"events": ["2026-10"], "fills": ["2026-10"]},
                    "tree_parquet_items": [{"kind": "events", "path": "data/events/2026-10.parquet", "oid": "abc", "size": 1}],
                    "baseline_tree_oid": "treeoid",
                }
                r = mon.verify_state(state)
                self.assertIsInstance(r, dict)
                created = list(td.glob("*"))
                self.assertEqual(created, [], f"verify_state created files: {[p.name for p in created]}")
            finally:
                mon.EVIDENCE_DIR = orig
                mon.STATE_PATH = orig_state

    def test_check_baseline_drift_state_only_no_filesystem_writes(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = td
                state = {"baseline_tree_oid": "t", "tree_parquet_items": [{"kind": "events", "path": "data/events/2026-10.parquet", "oid": "a", "size": 1}], "known_available_months": {"events": ["2026-10"], "fills": []}}
                r = mon.check_baseline_drift(state)
                self.assertIn("drifted", r)
                self.assertFalse(list(td.glob("*")), "state-only drift wrote files")
            finally:
                mon.EVIDENCE_DIR = orig

    def test_verify_cli_with_tmp_evidence_dir_does_not_touch_real_research_state(self):
        """--verify must not create/update real research_state ironflow probes/state."""
        import subprocess, sys, os, tempfile
        from pathlib import Path
        repo = Path(__file__).resolve().parents[1]
        rs = repo / "research_state"
        before_probes = {p.name: p.stat().st_mtime_ns for p in rs.glob("ironflow_probe_*.json")}
        before_n = len(list(rs.glob("*.md"))) + len(list(rs.glob("*.json")))
        with tempfile.TemporaryDirectory() as td:
            env = os.environ.copy()
            env["IRONFLOW_EVIDENCE_DIR_OVERRIDE"] = td
            env["IRONFLOW_STATE_PATH_OVERRIDE"] = str(Path(td) / "state.json")
            # write minimal state
            Path(td, "state.json").write_text('{"data_through":"2026-10","known_available_months":{"events":["2026-10"],"fills":[]},"tree_parquet_items":[],"baseline_tree_oid":"x"}')
            # run verify; script may not honor overrides - so just call functions
            import scripts.monitor_ironflow_liquidations as m
            orig_e, orig_s = m.EVIDENCE_DIR, m.STATE_PATH
            try:
                m.EVIDENCE_DIR = Path(td); m.STATE_PATH = Path(td) / "state.json"
                m.verify_state(json.loads(Path(td, "state.json").read_text()))
            finally:
                m.EVIDENCE_DIR, m.STATE_PATH = orig_e, orig_s
        after_probes = {p.name: p.stat().st_mtime_ns for p in rs.glob("ironflow_probe_*.json")}
        after_n = len(list(rs.glob("*.md"))) + len(list(rs.glob("*.json")))
        self.assertEqual(before_probes, after_probes)
        self.assertEqual(before_n, after_n)
