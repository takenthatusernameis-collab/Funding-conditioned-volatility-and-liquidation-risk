#!/usr/bin/env python3
"""FCLR-NEXT-098: strict manifest gate integration in harness/resume path +
offline prereg-before-outcomes trigger simulation + alt/cache churn safety +
handoff drift audit proof.

All deterministic, no network, tmp-only, no real research_state mutation.
"""
import json
import os
import sys
import tempfile
import time
import types
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.fclr010_harness import FCLR010Harness
from scripts.tracka_resume_check import _valid_go, _valid_strict_manifest_go

REPO_RS = Path(__file__).resolve().parent.parent / "research_state"


def _snapshot_real_rs():
    return {
        "probe_files": sorted(p.name for p in REPO_RS.glob("ironflow_probe_*.json")),
        "root_count": len(list(REPO_RS.glob("*.md"))) + len(list(REPO_RS.glob("*.json"))),
        "url_cache_mtime": (REPO_RS / "url_probe_cache.json").stat().st_mtime_ns if (REPO_RS / "url_probe_cache.json").exists() else None,
        "url_cache_size": (REPO_RS / "url_probe_cache.json").stat().st_size if (REPO_RS / "url_probe_cache.json").exists() else None,
    }


class TestHarnessStrictGateIntegration098(unittest.TestCase):
    def setUp(self):
        self.h = FCLR010Harness()

    def test_default_strict_gate_rejects_minimal_only_manifest(self):
        r = self.h.evaluate_source_manifest(_valid_go(), strict=True)
        self.assertEqual(r["status"], "NO-GO")
        self.assertFalse(r["go"])
        self.assertTrue(r["strict_gate"])
        self.assertTrue(any(f in r["failures"] for f in ("observed_access_provenance_missing", "label_definition_missing")), r["failures"])

    def test_default_strict_gate_accepts_full_machine_verifiable_manifest(self):
        r = self.h.evaluate_source_manifest(_valid_strict_manifest_go(), strict=True)
        self.assertEqual(r["status"], "GO", r)
        self.assertTrue(r["go"])

    def test_compat_fixture_path_accepts_minimal_with_explicit_flag(self):
        r = self.h.evaluate_source_manifest(_valid_go(), strict=False)
        self.assertEqual(r["status"], "GO", r)
        self.assertFalse(r["strict_gate"])

    def test_evaluate_forward_rejects_minimal_manifest_on_default_path(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "prereg.json"
            prereg.write_text("{}")
            data = td / "data"; data.mkdir()
            r = self.h.evaluate_forward(data, td, pre_reg_path=prereg, source_manifest=_valid_go())
        self.assertEqual(r["status"], "BLOCKED")
        self.assertFalse(r["outcomes_inspected"])
        self.assertEqual(r["manifest_gate"]["status"], "NO-GO")
        self.assertIn("strict manifest gate NO-GO", r["reason"])

    def test_evaluate_forward_accepts_full_manifest_with_prereg_and_data(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "prereg.json"
            prereg.write_text("{}")
            data = td / "data"; data.mkdir()
            r = self.h.evaluate_forward(data, td, pre_reg_path=prereg, source_manifest=_valid_strict_manifest_go())
        self.assertEqual(r["status"], "READY_FROZEN", r)
        self.assertFalse(r["outcomes_inspected"])
        self.assertEqual(r["manifest_gate"]["status"], "GO")

    def test_evaluate_forward_compat_fixture_path_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg = td / "prereg.json"
            prereg.write_text("{}")
            data = td / "data"; data.mkdir()
            r = self.h.evaluate_forward(data, td, pre_reg_path=prereg, source_manifest=_valid_go(), strict_manifest_gate=False)
        self.assertEqual(r["status"], "READY_FROZEN", r)
        self.assertFalse(r["manifest_gate"]["strict_gate"])

    def test_legacy_no_manifest_preserves_prereg_block_behavior(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.h.evaluate_forward(Path("/tmp/no"), Path(td), pre_reg_path=None)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertNotIn("manifest_gate", r)
        self.assertTrue("pre-reg" in r["reason"].lower() or "prereg" in r["reason"].lower())


class TestOfflinePreregBeforeOutcomesTriggerSimulation098(unittest.TestCase):
    """Deterministic, no network, tmp-only: synthetic rubric-GO strict manifest +
    mocked 2026-11+ availability path must produce PREREG-BEFORE-OUTCOMES resume decision.
    Covers exact handoff decision branches: manifest NO-GO => blocked/no inspect;
    manifest GO but no prereg => blocked/no inspect; manifest GO + prereg + data => READY_FROZEN/no inspect.
    """

    def setUp(self):
        self.h = FCLR010Harness()

    def test_branch1_minimal_manifest_nogo_blocks_even_with_data_no_inspect(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            # mocked 2026-11+ availability: synthetic data dir exists
            data = td / "hl_2026_11"; data.mkdir()
            (data / "events.parquet").write_bytes(b"PAR1")
            prereg = td / "prereg.json"; prereg.write_text("{}")
            r = self.h.evaluate_forward(data, td, pre_reg_path=prereg, source_manifest=_valid_go())
        self.assertEqual(r["status"], "BLOCKED")
        self.assertFalse(r["outcomes_inspected"])
        self.assertEqual(r["manifest_gate"]["status"], "NO-GO")
        self.assertEqual(before, _snapshot_real_rs())

    def test_branch2_strict_go_manifest_but_no_prereg_blocks_no_inspect(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = td / "hl_2026_11"; data.mkdir()
            r = self.h.evaluate_forward(data, td, pre_reg_path=None, source_manifest=_valid_strict_manifest_go())
        self.assertEqual(r["status"], "BLOCKED")
        self.assertFalse(r["outcomes_inspected"])
        self.assertTrue(r["prereg_required"])
        self.assertTrue("prereg" in r["reason"].lower() or "pre-reg" in r["reason"].lower() or "pre_register" in r["reason"].lower(), r["reason"])
        # manifest gate evaluated (attached) and GO, but prereg still blocks outcomes path
        self.assertEqual(r["manifest_gate"]["status"], "GO")
        self.assertEqual(before, _snapshot_real_rs())

    def test_branch3_strict_go_manifest_missing_prereg_file_blocks_no_inspect(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = td / "hl_2026_11"; data.mkdir()
            missing = td / "experiment_prereg_fclr012_forward_validate.json"
            r = self.h.evaluate_forward(data, td, pre_reg_path=missing, source_manifest=_valid_strict_manifest_go())
        self.assertEqual(r["status"], "BLOCKED")
        self.assertFalse(r["outcomes_inspected"])
        self.assertTrue(r["prereg_required"])
        self.assertEqual(before, _snapshot_real_rs())

    def test_branch4_strict_go_manifest_prereg_present_data_present_ready_frozen_no_inspect(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            prereg_path = self.h.pre_register_forward_experiment(td)
            self.assertTrue(prereg_path.exists())
            data = td / "hl_2026_11"; data.mkdir()
            r = self.h.evaluate_forward(data, td, pre_reg_path=prereg_path, source_manifest=_valid_strict_manifest_go())
        self.assertEqual(r["status"], "READY_FROZEN", r)
        self.assertFalse(r["outcomes_inspected"])
        self.assertEqual(r["manifest_gate"]["status"], "GO")
        self.assertEqual(before, _snapshot_real_rs())

    def test_simulation_end_to_end_offline_under_5s(self):
        t = time.time()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data = td / "hl_2026_11"; data.mkdir()
            # no prereg -> blocked
            r1 = self.h.evaluate_forward(data, td, pre_reg_path=None, source_manifest=_valid_strict_manifest_go())
            self.assertEqual(r1["status"], "BLOCKED")
            # prereg -> ready
            prereg = self.h.pre_register_forward_experiment(td)
            r2 = self.h.evaluate_forward(data, td, pre_reg_path=prereg, source_manifest=_valid_strict_manifest_go())
            self.assertEqual(r2["status"], "READY_FROZEN")
        self.assertLess(time.time() - t, 5.0)


class TestAltCacheChurnSafety098(unittest.TestCase):
    """Deterministic tmp-isolated proof: deep_review/hunt cache behavior in
    cache-only/test mode does not create new recurring timestamped artifacts and
    does not mutate real research_state/url_probe_cache.json when redirected.
    """

    def test_deep_review_cache_only_no_new_recurring_artifacts_no_real_rs_mutation(self):
        before = _snapshot_real_rs()
        import scripts.deep_review_alt_sources as dr
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = {"https://example.invalid/x": {"status": 200, "body_preview": "ok", "cache_hit": False}}
            cache_path = td / "url_probe_cache.json"
            cache_path.write_text(json.dumps(cache))
            # monkeypatch hunt's cache load/save to tmp, and http probes to never network
            fake_hunt = types.SimpleNamespace()
            fake_hunt._url_cache_load = lambda: json.loads(cache_path.read_text())
            fake_hunt._url_cache_save = lambda c: cache_path.write_text(json.dumps(c))
            def _fake_cached(url, **kw):
                base = dict(cache.get(url, {"status": 404, "body_preview": "", "len": 0}))
                base.setdefault("url", url); base.setdefault("method", kw.get("method", "GET"))
                base.setdefault("cache_hit", url in cache); base.setdefault("ok", base.get("status")==200)
                return base
            fake_hunt.http_probe_cached = _fake_cached
            def _fake_post(url, body, **kw):
                return {"url": url, "method": "POST", "status": 405, "body_preview": "", "cache_hit": True, "len": 0, "ok": False}
            fake_hunt.http_probe_cached_post = _fake_post
            orig = sys.modules.get("scripts.hunt_alternative_liquidation_sources")
            sys.modules["scripts.hunt_alternative_liquidation_sources"] = fake_hunt
            orig_out = dr.RESEARCH
            try:
                dr.RESEARCH = td
                with patch.object(dr, "probe", side_effect=AssertionError("network")):
                    dr.main()
            finally:
                dr.RESEARCH = orig_out
                if orig is None:
                    sys.modules.pop("scripts.hunt_alternative_liquidation_sources", None)
                else:
                    sys.modules["scripts.hunt_alternative_liquidation_sources"] = orig
            # no recurring timestamped families created in tmp
            files = [p.name for p in td.iterdir()]
            self.assertTrue(any(n == "alt_source_deep_review_latest.md" for n in files), files)
            self.assertFalse(any(n.startswith("alt_source_deep_review_20") and n != "alt_source_deep_review_latest.md" for n in files), files)
        self.assertEqual(before, _snapshot_real_rs())

    def test_hunt_cache_only_no_new_recurring_artifacts_no_real_rs_mutation(self):
        before = _snapshot_real_rs()
        import scripts.hunt_alternative_liquidation_sources as hunt
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            orig_search = hunt.SEARCH_CACHE_PATH
            orig_url = hunt.URL_CACHE_PATH
            orig_repo = hunt.REPO_ROOT
            try:
                hunt.SEARCH_CACHE_PATH = td / "hf_search_cache.json"
                hunt.URL_CACHE_PATH = td / "url_probe_cache.json"
                hunt.REPO_ROOT = td  # main() writes REPO_ROOT/research_state/alt_source_scan_latest.json
                (td / "research_state").mkdir(exist_ok=True)
                hunt.SEARCH_CACHE_PATH.write_text(json.dumps({"generated_utc": "2099-01-01T00:00:00+00:00", "queries": [], "errors": [], "candidates": []}))
                hunt.URL_CACHE_PATH.write_text("{}")
                with patch.object(hunt, "http_probe", side_effect=AssertionError("network")):
                    hunt.main()
            finally:
                hunt.SEARCH_CACHE_PATH = orig_search
                hunt.URL_CACHE_PATH = orig_url
                hunt.REPO_ROOT = orig_repo
            files = [p.name for p in (td / "research_state").iterdir()]
            self.assertTrue(any(n == "alt_source_scan_latest.json" for n in files), files)
            self.assertFalse(any(n.startswith("alt_source_scan_20") and n != "alt_source_scan_latest.json" for n in files), files)
        self.assertEqual(before, _snapshot_real_rs())

    def test_unchanged_inputs_cache_bounded_no_unexpected_real_file_mutation(self):
        # repeated cache-only loads in tmp do not touch real url_probe_cache
        before = _snapshot_real_rs()
        import scripts.hunt_alternative_liquidation_sources as hunt
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = td / "url_probe_cache.json"
            p.write_text(json.dumps({"k": {"status": 200, "probed_utc": "2099-01-01T00:00:00+00:00"}}))
            orig = hunt.URL_CACHE_PATH
            try:
                hunt.URL_CACHE_PATH = p
                c1 = hunt._url_cache_load(); m1 = p.stat().st_mtime_ns
                c2 = hunt._url_cache_load(); m2 = p.stat().st_mtime_ns
                self.assertEqual(c1, c2)
                self.assertEqual(m1, m2)
            finally:
                hunt.URL_CACHE_PATH = orig
        self.assertEqual(before, _snapshot_real_rs())


class TestHandoffDriftAudit098(unittest.TestCase):
    """Deterministic proof of durable handoff contract: single root AGENT_HANDOFF.md,
    no stale root copies.
    """

    def test_single_durable_root_handoff(self):
        root = Path(__file__).resolve().parent.parent
        copies = [p for p in root.rglob("AGENT_HANDOFF.md") if ".git" not in p.parts and "node_modules" not in p.parts]
        rels = sorted(str(p.relative_to(root)) for p in copies)
        self.assertEqual(rels, ["AGENT_HANDOFF.md"], f"handoff drift: {rels}")

    def test_no_handoff_copies_in_research_state_or_scripts(self):
        root = Path(__file__).resolve().parent.parent
        for sub in ("research_state", "scripts", "tests", "src"):
            p = root / sub
            if not p.exists(): continue
            found = list(p.rglob("AGENT_HANDOFF*"))
            self.assertEqual(found, [], f"stale handoff under {sub}: {found}")


if __name__ == "__main__":
    unittest.main()
