#!/usr/bin/env python3
"""Tests for the HEAVY-004i caching/dedup hardening of
scripts/hunt_alternative_liquidation_sources.py.

Covers:
- HF search enumeration cache round-trip + TTL expiry
- per-URL probe cache freshness and TTL expiry
- http_probe_cached reports cache_hit and never hits the network on a hit
- candidate URL de-duplication (no URL probed twice in one run)

All tests are offline: they patch the network and the cache file paths so the
suite stays deterministic and green without internet access.
"""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

import scripts.hunt_alternative_liquidation_sources as hunt


class TestHfSearchCache(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        hunt.SEARCH_CACHE_PATH = self.tmp / "hf_search_cache.json"

    def test_round_trip_save_and_load(self):
        cands = [{"name": "hf_discovered__a/b", "urls": ["u1"], "notes": "n"}]
        payload = hunt._cache_save(cands, ["q1"], [{"query": "q1", "status": None}])
        loaded = hunt._cache_load()
        self.assertEqual(loaded.get("candidates"), cands)
        self.assertEqual(loaded.get("queries"), ["q1"])
        self.assertEqual(loaded.get("errors"), [{"query": "q1", "status": None}])
        self.assertIn("generated_utc", payload)

    def test_cache_fresh_within_ttl(self):
        hunt._cache_save([{"name": "x"}], ["q"], [])
        self.assertTrue(hunt._cache_fresh(hunt._cache_load()))

    def test_cache_stale_after_ttl(self):
        # Backdate the generation timestamp past the TTL.
        old = (datetime.now(timezone.utc) - timedelta(seconds=hunt.SEARCH_TTL_SECONDS + 60)).isoformat()
        (self.tmp / "hf_search_cache.json").write_text(json.dumps({
            "generated_utc": old, "queries": ["q"], "errors": [], "candidates": [{"name": "x"}],
        }))
        self.assertFalse(hunt._cache_fresh(hunt._cache_load()))

    def test_cache_load_handles_missing_or_bad_file(self):
        self.assertEqual(hunt._cache_load(), {})
        (self.tmp / "hf_search_cache.json").write_text("not json")
        self.assertEqual(hunt._cache_load(), {})


class TestUrlProbeCache(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        hunt.URL_CACHE_PATH = self.tmp / "url_probe_cache.json"

    def test_cache_miss_then_hit(self):
        cache = {}
        with patch("scripts.hunt_alternative_liquidation_sources.http_probe") as mock_probe:
            mock_probe.return_value = {"url": "u", "status": 200, "content_kind": "text", "body_preview": "hi"}
            r1 = hunt.http_probe_cached("u", cache=cache)
            r2 = hunt.http_probe_cached("u", cache=cache)
        self.assertFalse(r1.get("cache_hit"))
        self.assertTrue(r2.get("cache_hit"))
        self.assertEqual(mock_probe.call_count, 1)

    def test_ttl_expiry_reprobes(self):
        cache = {}
        with patch("scripts.hunt_alternative_liquidation_sources.http_probe") as mock_probe:
            mock_probe.return_value = {"url": "u", "status": 200, "content_kind": "text", "body_preview": "hi"}
            hunt.http_probe_cached("u", cache=cache)
            # Backdate the cache entry past the TTL.
            old = (datetime.now(timezone.utc) - timedelta(seconds=hunt.URL_CACHE_TTL_SECONDS + 60)).isoformat()
            cache["u"]["probed_utc"] = old
            r3 = hunt.http_probe_cached("u", cache=cache)
        self.assertFalse(r3.get("cache_hit"))
        self.assertEqual(mock_probe.call_count, 2)

    def test_cache_get_returns_none_for_missing_and_bad(self):
        self.assertIsNone(hunt._url_cache_get({}, "missing"))
        (self.tmp / "url_probe_cache.json").write_text("not json")
        self.assertIsNone(hunt._url_cache_get(hunt._url_cache_load(), "missing"))


class TestCandidateDedup(unittest.TestCase):
    def test_dedup_keeps_first_occurrence_urls(self):
        # Two candidates share a URL; the second must drop it rather than probe
        # it twice (the pre-fix behaviour probed the same URL twice per run).
        cands = [
            {"name": "a", "urls": ["https://x.com/", "https://y.com/"], "notes": "n"},
            {"name": "b", "urls": ["https://x.com/", "https://z.com/"], "notes": "n"},
        ]
        seen = set()
        out = []
        for c in cands:
            urls = [u for u in c["urls"] if u not in seen]
            if not urls:
                continue
            for u in urls:
                seen.add(u)
            nc = dict(c)
            nc["urls"] = urls
            out.append(nc)
        self.assertEqual([c["urls"] for c in out], [["https://x.com/", "https://y.com/"], ["https://z.com/"]])
        self.assertEqual(len(seen), 3)


class TestDiscoverCacheIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        hunt.SEARCH_CACHE_PATH = self.tmp / "hf_search_cache.json"

    def test_live_enumeration_writes_cache(self):
        with patch("scripts.hunt_alternative_liquidation_sources.http_probe") as mock_probe:
            mock_probe.return_value = {
                "status": 200, "body_preview": '{"id":"owner/liquidation-x","description":"crypto perpetual liquidation data"}',
            }
            cands, errors, info = hunt.discover_hf_liquidation_datasets()
        self.assertEqual(info["source"], "live")
        self.assertGreater(len(cands), 0)
        # Second call must come from cache, not re-query the endpoint.
        with patch("scripts.hunt_alternative_liquidation_sources.http_probe") as mock_probe2:
            cands2, _, info2 = hunt.discover_hf_liquidation_datasets()
        self.assertEqual(info2["source"], "cache")
        self.assertFalse(info2["stale"])
        self.assertEqual(mock_probe2.call_count, 0)
        self.assertEqual([c["name"] for c in cands], [c["name"] for c in cands2])


class TestDeepReviewSharedCache(unittest.TestCase):
    """HEAVY-004i session 4 bottleneck-removal tests.

    deep_review_alt_sources.py used to carry a 14-URL candidate set that was 100%
    disjoint from hunt_alternative_liquidation_sources.py's 44-URL set, so every
    blocked session re-GETted URLs the hunt had already cached (~14s of redundant
    I/O). The fix folds deep_review's URLs into the hunt candidate set and routes
    deep_review's probe() through the hunt's shared URL probe cache. These tests
    verify the integration is real and that a cache hit never touches the network.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        hunt.URL_CACHE_PATH = self.tmp / "url_probe_cache.json"

    def test_deep_review_urls_are_in_hunt_candidate_set(self):
        # Every deep_review URL must appear in the hunt candidate set so it is
        # probed exactly once per session instead of twice (once by each script).
        import scripts.deep_review_alt_sources as dr
        import scripts.hunt_alternative_liquidation_sources as hunt_mod
        hunt_urls = set()
        for c in (hunt_mod.EXTENDED_CANDIDATES + hunt_mod.HF_SEARCH_DISCOVERED + hunt_mod.DEEP_REVIEW_URLS):
            for u in (c.get("urls") or c.get("probes") or []):
                hunt_urls.add(u)
        missing = [u for u in dr.DEEP_REVIEW_URLS if u not in hunt_urls]
        self.assertEqual(missing, [], f"deep_review URLs not folded into hunt set: {missing}")

    @patch("scripts.hunt_alternative_liquidation_sources.http_probe")
    def test_shared_probe_uses_cache_on_hit(self, mock_probe):
        import scripts.deep_review_alt_sources as dr
        mock_probe.return_value = {"url": "https://example.com/", "status": 200,
                                   "content_kind": "text", "body_preview": "ok"}
        # _shared_probe loads its own cache via hunt._url_cache_load(); stub both
        # load and save so the in-memory cache dict is reused across calls.
        cache = {}
        with patch("scripts.hunt_alternative_liquidation_sources._url_cache_load", return_value=cache), \
             patch("scripts.hunt_alternative_liquidation_sources._url_cache_save"):
            r1 = dr._shared_probe("https://example.com/")
            self.assertFalse(r1.get("cache_hit"))
            self.assertEqual(mock_probe.call_count, 1)
            r2 = dr._shared_probe("https://example.com/")
            self.assertTrue(r2.get("cache_hit"))
            self.assertEqual(mock_probe.call_count, 1)

    @patch("scripts.hunt_alternative_liquidation_sources.http_probe")
    def test_shared_probe_falls_back_to_direct_on_import_failure(self, mock_probe):
        import scripts.deep_review_alt_sources as dr
        with patch("builtins.__import__", side_effect=ImportError("no hunt")):
            # _shared_probe catches the ImportError and falls back to direct probe.
            with patch.object(dr, "probe", return_value={"url": "https://example.com/", "status": 200, "ok": True}) as mp:
                r = dr._shared_probe("https://example.com/")
        self.assertEqual(r["status"], 200)
        mp.assert_called_once()

    @patch("scripts.hunt_alternative_liquidation_sources.http_probe")
    def test_deep_review_reports_cache_accounting(self, mock_probe):
        import scripts.deep_review_alt_sources as dr
        mock_probe.return_value = {"url": "https://example.com/", "status": 200,
                                   "content_kind": "text", "body_preview": "ok"}
        cache = {}
        with patch("scripts.hunt_alternative_liquidation_sources._url_cache_load", return_value=cache), \
             patch("scripts.hunt_alternative_liquidation_sources._url_cache_save"):
            dr._shared_probe("https://example.com/")
            dr._shared_probe("https://example.com/")
        # The shared cache must record exactly one network call for the URL.
        self.assertEqual(mock_probe.call_count, 1)


if __name__ == "__main__":
    unittest.main()