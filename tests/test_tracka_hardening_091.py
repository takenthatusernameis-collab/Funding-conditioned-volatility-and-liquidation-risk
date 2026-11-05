#!/usr/bin/env python3
"""Stricter Track A rubric/harness hardening tests (091). Additive only."""
import unittest, json, tempfile
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestTrackARubricStrictness(unittest.TestCase):
    def test_hunt_rubric_minimums_strict(self):
        import scripts.hunt_alternative_liquidation_sources as hunt
        r = hunt.RUBRIC
        self.assertTrue(r.get('unauthenticated_only'))
        self.assertTrue(r.get('no_requester_pays'))
        self.assertGreaterEqual(r.get('min_symbols', 0), 5)
        self.assertTrue(r.get('completeness_doc_required'))
        self.assertTrue(r.get('license_ok'))
        self.assertTrue(r.get('schema_compatible_fclr010'))

    def test_deep_review_rubric_alignment(self):
        import scripts.deep_review_alt_sources as dr
        r = dr.RUBRIC
        self.assertTrue(r.get('unauthenticated_only'))
        self.assertTrue(r.get('no_requester_pays'))
        self.assertGreaterEqual(r.get('min_symbols', 0), 5)

    def test_url_cache_ttl_reasonable(self):
        import scripts.hunt_alternative_liquidation_sources as hunt
        self.assertGreater(hunt.URL_CACHE_TTL_SECONDS, 0)
        self.assertLessEqual(hunt.URL_CACHE_TTL_SECONDS, 86400)

    def test_no_scheduler_polling_in_monitor_interface(self):
        # monitor is CLI-invoked, not a daemon/scheduler
        src = (Path(__file__).parent.parent / 'scripts/monitor_ironflow_liquidations.py').read_text()
        for bad in ['schedule.every','apscheduler','croniter','while True','time.sleep(60','poll_forever']:
            self.assertNotIn(bad, src, f'monitor must not contain scheduler/poller pattern: {bad}')

class TestFCLR010HarnessDryRun(unittest.TestCase):
    def test_harness_main_zero_latency(self):
        import time, subprocess, sys
        t=time.time()
        r=subprocess.run([sys.executable,'scripts/fclr010_harness.py'],capture_output=True,text=True,timeout=15)
        self.assertEqual(r.returncode, 0)
        self.assertLess(time.time()-t, 10.0, 'harness cold load must be <10s')
        cfg=json.loads(r.stdout)
        self.assertEqual(cfg['experiment_id'],'FCLR-010')
        self.assertTrue(cfg['splits']['frozen_before_outcomes'])

    def test_evaluate_forward_requires_prereg(self):
        from scripts.fclr010_harness import FCLR010Harness
        h=FCLR010Harness()
        res=h.evaluate_forward(Path('/tmp/no'), Path('/tmp/out'), pre_reg_path=None)
        self.assertEqual(res['status'],'BLOCKED')

    def test_preregister_writes_frozen_record(self):
        from scripts.fclr010_harness import FCLR010Harness
        with tempfile.TemporaryDirectory() as td:
            h=FCLR010Harness()
            p=h.pre_register_forward_experiment(Path(td))
            data=json.loads(p.read_text())
            self.assertEqual(data['experiment_id'],'FCLR-012')
            self.assertTrue(data['splits_frozen_before_outcomes'])
            self.assertTrue(data['rules']['no_retuning'])
            self.assertTrue(data['rules']['no_holdout_reuse'])
            self.assertEqual(data['rules']['overlay_changes'],'NONE')

    def test_fixtures_manifest_consistent(self):
        fx=Path(__file__).parent.parent/'tests/fixtures/tracka/manifest.json'
        if not fx.exists():
            self.skipTest('fixtures not generated')
        m=json.loads(fx.read_text())
        self.assertEqual(len(m['symbols']), 6)
        self.assertTrue(m['splits']['frozen_before_outcomes'])
        for split in ['train','validation','test']:
            self.assertIn(split, m['files'])
            self.assertGreater(m['files'][split]['rows'], 0)

if __name__=='__main__':
    unittest.main()
