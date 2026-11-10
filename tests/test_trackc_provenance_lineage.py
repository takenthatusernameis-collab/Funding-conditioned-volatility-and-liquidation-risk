"""Dep-light tests for Track C provenance-lineage ingestion (stdlib, no network, no outcomes).

Covers: manifest-backed hash match -> verified; mismatch/unmapped -> not verified +
blocker; adjacent sidecars; deterministic; compatibility with verify_sha256_sidecars.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.trackc_provenance_lineage import (  # noqa: E402
    _sha256_file,
    load_manifest_indexes,
    verify_file,
    verify_paths,
    verify_paths_with_manifests,
)

ROOT = Path(__file__).resolve().parents[1]


def _write_manifest(path: Path, records):
    path.write_text(json.dumps({"generated_utc": "2026-11-10T00:00:00Z", "records": records}, indent=2) + "\n")


class TestProvenanceLineage(unittest.TestCase):
    def test_sha256_file_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "a.csv"
            p.write_text("open_time,open\n0,1\n")
            h1 = _sha256_file(p)
            h2 = _sha256_file(p)
            self.assertEqual(h1, h2)
            self.assertEqual(len(h1), 64)

    def test_manifest_backed_hash_match_verified(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            cache.mkdir(parents=True)
            csv_p = cache / "BTCUSDT_2024_01" / "markPriceKlines-1h-2024-01-01" / "BTCUSDT-1h-2024-01-01.csv"
            csv_p.parent.mkdir(parents=True)
            csv_p.write_text("open_time,open\n0,1\n")
            digest = _sha256_file(csv_p)
            _write_manifest(
                cache / "manifest_extended.json",
                [{"path": str(csv_p), "sha256": digest, "url": "https://example.com/x.zip", "size_bytes": csv_p.stat().st_size}],
            )
            idx, stats = load_manifest_indexes(td / "research_state", manifest_paths=[cache / "manifest_extended.json"])
            self.assertEqual(stats["manifests_loaded"], [str(cache / "manifest_extended.json")])
            self.assertEqual(stats["records_indexed"], 1)
            res = verify_paths_with_manifests([csv_p], repo_root=td / "research_state", manifest_paths=[cache / "manifest_extended.json"])
            self.assertTrue(res["provenance_verified"])
            self.assertEqual(res["verified_count"], 1)
            self.assertEqual(res["mismatch_count"], 0)
            self.assertEqual(res["unmapped_count"], 0)
            self.assertTrue(any(str(k).startswith("manifest") for k in res["provenance_source_counts"]))

    def test_manifest_hash_mismatch_not_verified(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            cache.mkdir(parents=True)
            csv_p = cache / "BTCUSDT_2024_01" / "markPriceKlines-1h-2024-01-01" / "BTCUSDT-1h-2024-01-01.csv"
            csv_p.parent.mkdir(parents=True)
            csv_p.write_text("open_time,open\n0,1\n")
            _write_manifest(
                cache / "manifest_extended.json",
                [{"path": str(csv_p), "sha256": "0" * 64, "url": "https://example.com/x.zip"}],
            )
            res = verify_paths_with_manifests([csv_p], repo_root=td / "research_state", manifest_paths=[cache / "manifest_extended.json"])
            self.assertFalse(res["provenance_verified"])
            self.assertEqual(res["verified_count"], 0)
            self.assertEqual(res["mismatch_count"], 1)
            self.assertEqual(res["unmapped_count"], 0)

    def test_unmapped_file_not_verified_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            cache.mkdir(parents=True)
            csv_p = cache / "BTCUSDT_2024_01" / "markPriceKlines-1h-2024-01-01" / "BTCUSDT-1h-2024-01-01.csv"
            csv_p.parent.mkdir(parents=True)
            csv_p.write_text("open_time,open\n0,1\n")
            _write_manifest(cache / "manifest_extended.json", [])
            res = verify_paths_with_manifests([csv_p], repo_root=td / "research_state")
            self.assertFalse(res["provenance_verified"])
            self.assertEqual(res["verified_count"], 0)
            self.assertEqual(res["mismatch_count"], 0)
            self.assertEqual(res["unmapped_count"], 1)

    def test_adjacent_sidecar_verified(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            cache.mkdir(parents=True)
            csv_p = cache / "BTCUSDT_2024_01" / "markPriceKlines-1h-2024-01-01" / "BTCUSDT-1h-2024-01-01.csv"
            csv_p.parent.mkdir(parents=True)
            csv_p.write_text("open_time,open\n0,1\n")
            Path(str(csv_p) + ".sha256").write_text(_sha256_file(csv_p) + "\n")
            _write_manifest(cache / "manifest_extended.json", [])
            res = verify_paths_with_manifests([csv_p], repo_root=td / "research_state")
            self.assertTrue(res["provenance_verified"])
            self.assertEqual(res["verified_count"], 1)
            self.assertIn("adjacent_sidecar", res["provenance_source_counts"])

    def test_verify_file_unmapped_returns_none(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            p = td / "nope.csv"
            p.write_text("x\n")
            rec = verify_file(p, repo_root=td, manifest_index={})
            self.assertEqual(rec["status"], "unmapped")
            self.assertEqual(rec["source"], "none")

    def test_deterministic_repeat(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            cache.mkdir(parents=True)
            csv_p = cache / "BTCUSDT_2024_01" / "markPriceKlines-1h-2024-01-01" / "BTCUSDT-1h-2024-01-01.csv"
            csv_p.parent.mkdir(parents=True)
            csv_p.write_text("open_time,open\n0,1\n")
            digest = _sha256_file(csv_p)
            _write_manifest(
                cache / "manifest_extended.json",
                [{"path": str(csv_p), "sha256": digest}],
            )
            r1 = verify_paths_with_manifests([csv_p], repo_root=td / "research_state")
            r2 = verify_paths_with_manifests([csv_p], repo_root=td / "research_state")
            self.assertEqual(r1, r2)

    def test_no_network_stdlib_only(self):
        # Module imports and functions must not require network; stdlib only.
        import importlib
        mod = importlib.import_module("scripts.trackc_provenance_lineage")
        src = Path(mod.__file__).read_text()
        self.assertNotIn("urllib", src)
        self.assertNotIn("requests", src)
        self.assertNotIn("socket", src)
        self.assertNotIn("httpx", src)

    def test_verify_sha256_sidecars_backward_compatible_fields(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            cache = Path(td) / "cache"
            cache.mkdir()
            csv_p = cache / "a.csv"
            csv_p.write_text("open_time,open\n0,1\n")
            Path(str(csv_p) + ".sha256").write_text(_sha256_file(csv_p) + "\n")
            from scripts.trackc_panel_admissibility_audit import verify_sha256_sidecars  # noqa: E402
            res = verify_sha256_sidecars([csv_p], repo_root=root)
            self.assertIn("files_considered", res)
            self.assertIn("sidecars_ok", res)
            self.assertIn("provenance_verified", res)
            self.assertIn("manifest_ingest", res)
            self.assertTrue(res["provenance_verified"])


if __name__ == "__main__":
    unittest.main()
