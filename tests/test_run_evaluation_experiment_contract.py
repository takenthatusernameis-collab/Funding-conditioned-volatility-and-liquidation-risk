"""Tests for the experiment-selection contract in scripts/run_evaluation.py.

run_evaluation.py selects its output path / split key / data window from the
FCLR_EXPERIMENT env var through a big if/elif chain. A gap in that chain silently
falls through to the canonical ``evaluation_summary.md`` branch, which (a) overwrites
a committed artifact and (b) reports a 0-row NOT_EVALUABLE result under a frozen-but-
unmatched split set. These tests make that contract fail-closed and machine-checkable.

All checks are import-time / static: no outcomes are computed, no network is used,
and no file is written.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path

import unittest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def _load_module(monkeypatch_env: dict, sandbox: Path):
    """Import run_evaluation.py from inside the sandbox so REPO resolves to it.

    The module derives REPO from __file__ at import time, so the module file must
    physically live under <sandbox>/scripts for the canonical-summary guard to see
    the sandbox's research_state/ rather than the real repo's. The sandbox path is
    resolved through realpath() because the module's own resolve() can follow a
    symlinked temp dir to a different string than the one the test used to create
    the fixture files.
    """
    sandbox = Path(os.path.realpath(sandbox))
    old_cwd = os.getcwd()
    old_env = dict(os.environ)
    os.chdir(sandbox)
    for k, v in monkeypatch_env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    sys.modules.pop("run_evaluation", None)
    spec = importlib.util.spec_from_file_location(
        "run_evaluation", sandbox / "scripts" / "run_evaluation.py"
    )
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    finally:
        os.chdir(old_cwd)
        os.environ.clear()
        os.environ.update(old_env)
        sys.modules.pop("run_evaluation", None)
    return mod


class TestExperimentContract(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        # Canonical summary must exist for the guard's existence check.
        (self.tmp / "research_state").mkdir()
        (self.tmp / "research_state" / "evaluation_summary.md").write_text("# canonical\n")
        (self.tmp / "scripts").mkdir()
        (self.tmp / "scripts" / "run_evaluation.py").write_text(
            (SCRIPTS / "run_evaluation.py").read_text()
        )
        # The guard also refuses to create a brand-new summary file, so every
        # registered experiment's expected OUT must pre-exist in the sandbox.
# OUT is built as f"evaluation_summary_{EXPERIMENT}.md", so the FCLR-009 and
        # FCLR-013 branches (which keep the dash in the experiment id) produce
# evaluation_summary_FCLR-009.md and evaluation_summary_FCLR-013.md.
        for name in ("evaluation_summary_FCLR002.md", "evaluation_summary_FCLR003.md",
                     "evaluation_summary_FCLR006.md", "evaluation_summary_FCLR-007.md",
                     "evaluation_summary_FCLR-008.md", "evaluation_summary_FCLR-009.md",
                     "evaluation_summary_FCLR-011.md", "evaluation_summary_FCLR-012-V.md",
                     "evaluation_summary_FCLR-013.md"):
            (self.tmp / "research_state" / name).write_text("# existing\n")

    def test_registered_experiment_writes_its_own_summary(self):
        mod = _load_module({"FCLR_EXPERIMENT": "FCLR-009"}, self.tmp)
        self.assertEqual(mod.EXPERIMENT, "FCLR-009")
        # OUT is f"evaluation_summary_{EXPERIMENT}.md" -> keeps the dash in the id
        self.assertEqual(mod.OUT.name, "evaluation_summary_FCLR-009.md")
        self.assertNotEqual(mod.OUT, mod._CANONICAL_SUMMARY)
        self.assertEqual(mod.SPLIT_KEY, "split_boundaries_fclr009")
        self.assertEqual(mod.START_ALL, "2025-01-01")
        self.assertEqual(mod.DATA_END, "2025-12-31")

    def test_canonical_experiment_keeps_canonical_path(self):
        mod = _load_module({"FCLR_EXPERIMENT": "FCLR-001"}, self.tmp)
        self.assertEqual(mod.OUT, mod._CANONICAL_SUMMARY)

    def test_unregistered_experiment_refuses_before_writing(self):
        with self.assertRaises(SystemExit) as cm:
            _load_module({"FCLR_EXPERIMENT": "FCLR-BOGUS"}, self.tmp)
        self.assertIn("REFUSAL", str(cm.exception))
        self.assertIn("FCLR-BOGUS", str(cm.exception))
        self.assertIn("evaluation_summary.md", str(cm.exception))
        # canonical summary must be untouched
        self.assertEqual(
            (self.tmp / "research_state" / "evaluation_summary.md").read_text(),
            "# canonical\n",
        )

    def test_fclr013_branch_is_registered(self):
        mod = _load_module({"FCLR_EXPERIMENT": "FCLR-013"}, self.tmp)
        self.assertEqual(mod.OUT.name, "evaluation_summary_FCLR-013.md")
        self.assertEqual(mod.SPLIT_KEY, "split_boundaries_fclr013")
        self.assertEqual(mod.START_ALL, "2026-07-01")

    def test_known_experiments_have_distinct_outputs(self):
        outs = {}
        for exp in ("FCLR-001", "FCLR-002", "FCLR-003", "FCLR-006", "FCLR-007",
                    "FCLR-008", "FCLR-009", "FCLR-011", "FCLR-012-V", "FCLR-013"):
            mod = _load_module({"FCLR_EXPERIMENT": exp}, self.tmp)
            outs[exp] = mod.OUT
        # every registered experiment writes its own file; only FCLR-001 is canonical
        canonical = [e for e, p in outs.items() if p.name == "evaluation_summary.md"]
        self.assertEqual(canonical, ["FCLR-001"])
        self.assertEqual(len(set(outs.values())), len(outs))

    def test_missing_out_file_refuses(self):
        # Remove a registered experiment's summary: the guard must refuse rather
        # than create a new file from an unregistered path.
        (self.tmp / "research_state" / "evaluation_summary_FCLR-009.md").unlink()
        with self.assertRaises(SystemExit) as cm:
            _load_module({"FCLR_EXPERIMENT": "FCLR-009"}, self.tmp)
        self.assertIn("REFUSAL", str(cm.exception))
        self.assertIn("does not exist", str(cm.exception))


if __name__ == "__main__":
    unittest.main()