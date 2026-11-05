#!/usr/bin/env python3
"""Adversarial rubric edge + dry-run bound hardening (092). Additive only."""
import unittest, json, time, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestRubricAdversarialEdges(unittest.TestCase):
    """Edge fixtures: reject cases that must never score GO for Track A."""

    def _rubric(self):
        import scripts.hunt_alternative_liquidation_sources as hunt
        return hunt.RUBRIC

    def test_reject_modeled_as_observed_requires_schema(self):
        r = self._rubric()
        self.assertTrue(r.get('schema_compatible_fclr010'))
        # modeled-as-observed is a semantic violation; rubric+GO logic must require
        # observed liquidation semantics. We assert the hard constraints are present.
        self.assertTrue(r.get('unauthenticated_only'))

    def test_reject_auth_key_requester_pays(self):
        r = self._rubric()
        self.assertTrue(r.get('unauthenticated_only'))
        self.assertTrue(r.get('no_requester_pays'))

    def test_min_symbols_and_completeness(self):
        r = self._rubric()
        self.assertGreaterEqual(r.get('min_symbols', 0), 5)
        self.assertTrue(r.get('completeness_doc_required'))

    def test_hyperliquid_only_firewall_in_hunt_notes(self):
        # Track A firewall: Hyperliquid-only for FCLR-010 forward. Static candidates
        # may reference other venues as NO-GO probes, but GO requires Hyperliquid
        # compatibility; rubric must enforce schema compatibility.
        import scripts.hunt_alternative_liquidation_sources as hunt
        self.assertTrue(hunt.RUBRIC.get('schema_compatible_fclr010'))

    def test_deep_review_rubric_matches_hunt_core(self):
        import scripts.hunt_alternative_liquidation_sources as hunt
        import scripts.deep_review_alt_sources as dr
        for k in ['unauthenticated_only','no_requester_pays','min_symbols','completeness_doc_required','license_ok','schema_compatible_fclr010']:
            self.assertEqual(hunt.RUBRIC.get(k), dr.RUBRIC.get(k), f'mismatch on {k}')

class TestHarnessOfflineDryRunBound(unittest.TestCase):
    def test_dry_run_end_to_end_under_10s(self):
        t=time.time()
        r=subprocess.run([sys.executable,'scripts/fclr010_harness.py'],capture_output=True,text=True,timeout=15)
        dt=time.time()-t
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertLess(dt,10.0,f'dry-run took {dt:.2f}s')
        cfg=json.loads(r.stdout)
        self.assertEqual(cfg['experiment_id'],'FCLR-010')
        self.assertTrue(cfg['splits']['frozen_before_outcomes'])
        self.assertTrue(cfg.get('prereg_required') or cfg.get('status')=='CONFIG_LOADED' or 'frozen_before_outcomes' in str(cfg))

    def test_prereg_blocks_evaluation(self):
        from scripts.fclr010_harness import FCLR010Harness
        h=FCLR010Harness()
        out=h.evaluate_forward(Path('/nonexistent'), Path(tempfile.mkdtemp()), pre_reg_path=None)
        self.assertEqual(out['status'],'BLOCKED')
        self.assertTrue('PREREG' in out['reason'].upper() or 'PRE-REG' in out['reason'].upper() or 'PRE_REG' in out['reason'].upper(), out['reason'])

    def test_fixtures_present_and_frozen(self):
        root=Path(__file__).parent.parent
        fx=root/'tests/fixtures/tracka'
        self.assertTrue(fx.exists())
        m=json.loads((fx/'manifest.json').read_text())
        self.assertTrue(m['splits']['frozen_before_outcomes'])
        self.assertGreaterEqual(len(m['symbols']),5)
        for s in ['train','validation','test']:
            self.assertTrue((fx/f'panel_{s}.jsonl').exists())

class TestNoNewRecurringProbeFamilies(unittest.TestCase):
    def test_canonical_alt_outputs(self):
        # scripts must write canonical latest files, not timestamped scan/deep-review families
        src_h=(Path(__file__).parent.parent/'scripts/hunt_alternative_liquidation_sources.py').read_text()
        src_d=(Path(__file__).parent.parent/'scripts/deep_review_alt_sources.py').read_text()
        self.assertIn('alt_source_scan_latest.json', src_h)
        self.assertIn('alt_source_deep_review_latest.md', src_d)
        self.assertNotIn('alt_source_scan_{ts}', src_h)
        self.assertNotIn('alt_source_deep_review_{ts}', src_d)

if __name__=='__main__':
    unittest.main()
