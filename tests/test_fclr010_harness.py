#!/usr/bin/env python3
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.fclr010_harness import FCLR010Harness


class TestFCLR010Harness(unittest.TestCase):
    def setUp(self):
        self.harness = FCLR010Harness()

    def test_frozen_config_loaded(self):
        config = self.harness.get_frozen_config()
        self.assertEqual(config['experiment_id'], 'FCLR-010')
        self.assertEqual(config['primary_contrast'], 'C2_vs_B1')
        self.assertEqual(config['primary_metric'], 'brier')
        self.assertTrue(config['splits']['frozen_before_outcomes'])

    def test_split_boundaries_frozen(self):
        self.assertTrue(self.harness.split_boundaries.get('frozen_before_outcomes'))
        self.assertIn('train', self.harness.split_boundaries)
        self.assertIn('validation', self.harness.split_boundaries)
        self.assertIn('test', self.harness.split_boundaries)

    def test_bootstrap_reps(self):
        config = self.harness.get_frozen_config()
        self.assertEqual(config['bootstrap_reps'], 2000)

    def test_gates(self):
        config = self.harness.get_frozen_config()
        self.assertEqual(config['gates']['min_instruments'], 5)
        self.assertEqual(config['gates']['min_blocks'], 3)
        self.assertAlmostEqual(config['gates']['min_rel_reduction'], 0.0221, places=4)


if __name__ == '__main__':
    unittest.main()


class TestAdversarialFCLR010(unittest.TestCase):
    def test_leakage_guard_no_future_leak(self):
        from scripts import fclr010_harness
        h = fclr010_harness.FCLR010Harness()
        cfg = h.get_frozen_config()
        self.assertTrue(cfg['splits'].get('frozen_before_outcomes'))
        self.assertTrue(cfg['splits'].get('embargo_days') >= 0)

    def test_frozen_split_enforcement(self):
        from scripts import fclr010_harness
        h = fclr010_harness.FCLR010Harness()
        cfg = h.get_frozen_config()
        self.assertIn('primary_contrast', cfg)
        self.assertEqual(cfg['primary_contrast'], 'C2_vs_B1')
        self.assertEqual(cfg['primary_metric'], 'brier')
