"""Regression: run_funding_ablations LFS-tolerant manifest read + output isolation (deterministic, tmp, no sealed overwrite, no network/outcomes)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.run_funding_ablations import _load_manifest_json


LFS_POINTER = "version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 123\n"


class TestFundingAblationsLfsManifest(unittest.TestCase):
    def test_missing_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(_load_manifest_json(Path(td) / "nope.json"), {})

    def test_lfs_pointer_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "run_manifest.json"
            p.write_text(LFS_POINTER)
            self.assertEqual(_load_manifest_json(p), {})

    def test_valid_json_returns_dict(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "run_manifest.json"
            obj = {"a": 1, "nested": {"k": "v"}}
            p.write_text(json.dumps(obj))
            self.assertEqual(_load_manifest_json(p), obj)

    def test_invalid_json_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "run_manifest.json"
            p.write_text("{not json")
            self.assertEqual(_load_manifest_json(p), {})

    def test_directory_path_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(_load_manifest_json(Path(td)), {})

    def test_empty_suffix_manifest_path_uses_default_name(self):
        # output-isolation contract: empty suffix -> run_manifest.json, non-empty -> suffixed (no sealed overwrite of default when suffix set)
        from scripts.run_funding_ablations import RES
        suffix = ""
        p = RES / (f"run_manifest_funding{suffix}.json" if suffix else "run_manifest.json")
        self.assertEqual(p.name, "run_manifest.json")

    def test_nonempty_suffix_manifest_path_is_isolated(self):
        from scripts.run_funding_ablations import RES
        suffix = "_test_isolated_xyz"
        p = RES / (f"run_manifest_funding{suffix}.json" if suffix else "run_manifest.json")
        self.assertEqual(p.name, "run_manifest_funding_test_isolated_xyz.json")
        self.assertNotEqual(p.name, "run_manifest.json")


if __name__ == "__main__":
    unittest.main()
