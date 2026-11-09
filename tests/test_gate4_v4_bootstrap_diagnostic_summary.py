"""Synthetic-fixture tests for gate4_v4_bootstrap_diagnostic_summary.

Covers exact JSON->table rendering, degenerate/invalid regime surfacing, and the
guardrail that no fabricated improvement appears when CIs are degenerate/invalid
or diagnostic gates do not pass. No network, no real research_state writes, no
exploratory recomputation.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import scripts.gate4_v4_bootstrap_diagnostic_summary as s  # noqa: E402


def _stab_artifact():
    return {
        "label": s.LABEL,
        "variants": {
            "V1_primary": {
                "contrasts_vs_A": {
                    "E_rv_funding_trails": {
                        "point": 0.5, "ci_low": -0.1, "ci_high": 1.2,
                        "n_obs": 100, "n_blocks": 10, "n_reps": 20, "seed": 1, "block_hours": 24, "alpha": 0.05,
                        "effective_block_count": 10, "ci_accounting_valid": True, "regime_flags": [],
                        "degenerate": False, "inference_ok": True, "n_reps_effective": 20,
                    },
                    "BAD_missing_diag": {
                        # missing diagnostic fields + CI excludes zero in raw numbers? make it cross zero to be safe
                        "point": 0.2, "ci_low": -0.2, "ci_high": 0.8,
                        "n_obs": 50, "n_blocks": 4,
                    },
                }
            }
        },
        "loo_e_vs_a_v3": {
            "all": {
                "point": 1.0, "ci_low": 0.2, "ci_high": 1.8,
                "n_obs": 80, "n_blocks": 8,
                "effective_block_count": 8, "ci_accounting_valid": True, "regime_flags": ["LOW_BLOCKS"],
                "degenerate": False, "inference_ok": True,
            }
        },
    }


def _diag_artifact():
    return {
        "label": s.LABEL,
        "pooled_contrasts_vs_A_primary_fit": {
            "D_rv_signed_abs": {
                "point": 2.0, "ci_low": 0.1, "ci_high": 4.0,
                "n_obs": 100, "n_blocks": 12,
                "effective_block_count": 2, "ci_accounting_valid": False, "regime_flags": ["DEGENERATE_CI"],
                "degenerate": True, "inference_ok": False,
            }
        },
        "pooled_contrasts_vs_A_stabilized_exploratory": {
            "E_rv_funding_trails": {
                "point": 0.1, "ci_low": -0.9, "ci_high": 1.1,
                "n_obs": 120, "n_blocks": 12,
                "effective_block_count": 12, "ci_accounting_valid": True, "regime_flags": [],
                "degenerate": False, "inference_ok": True,
            }
        },
    }


def _leakage_artifact():
    return {
        "label": s.LABEL,
        "leakage_invariance_all": True,
        "block_bootstrap_reproducibility": {
            "run1": {
                "point": 0.4, "ci_low": -0.1, "ci_high": 1.0,
                "n_obs": 90, "n_blocks": 9,
                "ci_accounting_valid": True, "effective_block_count": 9,
                "n_obs_finite": 90, "degenerate": False, "regime_flags": [], "inference_ok": True,
            },
            "run2": {
                "point": 0.4, "ci_low": -0.1, "ci_high": 1.0,
                "n_obs": 90, "n_blocks": 9,
                "ci_accounting_valid": True, "effective_block_count": 9,
                "n_obs_finite": 90, "degenerate": False, "regime_flags": [], "inference_ok": True,
            },
            "run1_diagnostics": {
                "effective_block_count": 9, "ci_accounting_valid": True, "regime_flags": [],
                "degenerate": False, "inference_ok": True, "n_reps_effective": 10, "n_obs_finite": 90,
            },
            "run2_diagnostics": {
                "effective_block_count": 9, "ci_accounting_valid": True, "regime_flags": [],
                "degenerate": False, "inference_ok": True, "n_reps_effective": 10, "n_obs_finite": 90,
            },
        },
    }


class TestBootstrapDiagnosticSummary(unittest.TestCase):
    def _write(self, td: Path, name: str, obj: dict) -> Path:
        p = td / name
        p.write_text(json.dumps(obj), encoding="utf-8")
        return p

    def test_exact_json_to_table_and_claimable_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            paths = [
                self._write(td, "gate4_v4_exploratory_stab_20990101T000000Z.json", _stab_artifact()),
                self._write(td, "gate4_v4_exploratory_diag_20990101T000000Z.json", _diag_artifact()),
                self._write(td, "gate4_v4_leakage_audit_20990101T000000Z.json", _leakage_artifact()),
            ]
            rows = s.summarize_artifacts(paths)
            md = s.render_markdown(rows, paths, ts="20990101T000000Z")
        # exact key rows present
        self.assertIn("| gate4_v4_exploratory_stab_20990101T000000Z.json | V1_primary.contrasts_vs_A | E_rv_funding_trails |", md)
        self.assertIn("| gate4_v4_exploratory_stab_20990101T000000Z.json | loo_e_vs_a_v3 | all |", md)
        self.assertIn("| gate4_v4_exploratory_diag_20990101T000000Z.json | pooled_contrasts_vs_A_primary_fit | D_rv_signed_abs |", md)
        self.assertIn("| gate4_v4_leakage_audit_20990101T000000Z.json | block_bootstrap_reproducibility.run1 | E_vs_A_probe |", md)
        # degenerate row surfaced with flags/gates
        d_row = [r for r in rows if r["contrast"] == "D_rv_signed_abs"][0]
        self.assertTrue(d_row["degenerate"])
        self.assertFalse(d_row["ci_valid"])
        self.assertFalse(d_row["inference_ok"])
        self.assertIn("DEGENERATE_CI", d_row["regime_flags"])
        self.assertIn("NO_CLAIMABLE_IMPROVEMENT", d_row["regime_flags"])
        self.assertFalse(d_row["non_degenerate_excludes_zero_claimable"])
        # loo all: gates pass and CI excludes zero => claimable
        loo = [r for r in rows if r["section"] == "loo_e_vs_a_v3" and r["contrast"] == "all"][0]
        self.assertTrue(loo["ci_excludes_zero"])
        self.assertTrue(loo["non_degenerate_excludes_zero_claimable"])
        self.assertIn("LOW_BLOCKS", loo["regime_flags"])  # surfaced, still claimable by gates+CI
        # missing diagnostics => not claimable
        bad = [r for r in rows if r["contrast"] == "BAD_missing_diag"][0]
        self.assertTrue(bad["missing_diagnostic_fields"])
        self.assertFalse(bad["non_degenerate_excludes_zero_claimable"])
        self.assertIn("MISSING_DIAGNOSTIC_FIELDS", bad["regime_flags"])
        # header/guardrails
        self.assertIn("EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE", md)
        self.assertIn("non-degenerate CI excluding zero (claimable): **1**", md)

    def test_no_fabricated_improvement_when_all_degenerate_or_invalid(self):
        obj = {
            "label": s.LABEL,
            "pooled_contrasts_vs_A_primary_fit": {
                "B": {"point": 9.0, "ci_low": 1.0, "ci_high": 20.0, "n_obs": 10, "n_blocks": 2,
                      "effective_block_count": 1, "ci_accounting_valid": False, "regime_flags": ["DEGENERATE_CI"],
                      "degenerate": True, "inference_ok": False},
                "C": {"point": 5.0, "ci_low": 0.5, "ci_high": 9.0, "n_obs": 10, "n_blocks": 2,
                      "effective_block_count": 1, "ci_accounting_valid": False, "regime_flags": ["DEGENERATE_CI"],
                      "degenerate": True, "inference_ok": False},
            },
            "pooled_contrasts_vs_A_stabilized_exploratory": {
                "D": {"point": 3.0, "ci_low": 0.1, "ci_high": 6.0, "n_obs": 10, "n_blocks": 10,
                      "effective_block_count": 10, "ci_accounting_valid": True, "regime_flags": [],
                      "degenerate": False, "inference_ok": False},
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "gate4_v4_exploratory_diag_x.json"
            p.write_text(json.dumps(obj), encoding="utf-8")
            rows = s.summarize_artifacts([p])
            md = s.render_markdown(rows, [p], ts="t")
        self.assertTrue(all(not r["non_degenerate_excludes_zero_claimable"] for r in rows))
        self.assertIn("claimable): **0**", md)
        self.assertIn("no spurious improvement is claimable", md)
        # B/C exclude zero numerically but must NOT be claimable
        for r in rows[:2]:
            self.assertTrue(r["ci_excludes_zero"])
            self.assertFalse(r["non_degenerate_excludes_zero_claimable"])
            self.assertIn("EXCLUDES_ZERO_NOT_CLAIMABLE", r["regime_flags"])

    def test_main_writes_versioned_results_file_no_real_research_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research_state" / "gate4_v4_exploratory_stab").mkdir(parents=True)
            art = root / "research_state" / "gate4_v4_exploratory_stab" / "gate4_v4_exploratory_stab_20990101T000000Z.json"
            art.write_text(json.dumps(_stab_artifact()), encoding="utf-8")
            rc = s.main(["--repo-root", str(root)])
            self.assertEqual(rc, 0)
            outs = list((root / "results").glob("gate4_v4_bootstrap_diagnostic_summary_*.md"))
            self.assertEqual(len(outs), 1)
            txt = outs[0].read_text(encoding="utf-8")
            self.assertIn("EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE", txt)
            # no new files written under research_state except the synthetic input we created
            rs_files = [p for p in (root / "research_state").rglob("*") if p.is_file()]
            self.assertEqual(rs_files, [art])

    def test_ci_excludes_zero_logic(self):
        self.assertTrue(s._ci_excludes_zero({"ci_low": 0.1, "ci_high": 0.2}))
        self.assertTrue(s._ci_excludes_zero({"ci_low": -0.2, "ci_high": -0.1}))
        self.assertFalse(s._ci_excludes_zero({"ci_low": -0.2, "ci_high": 0.1}))
        self.assertIsNone(s._ci_excludes_zero({"ci_low": None, "ci_high": 0.1}))
        self.assertIsNone(s._ci_excludes_zero({"ci_low": "nan", "ci_high": 0.1}))

    def test_enrichment_unambiguous_exact_match_applies_and_never_mutates_source(self):
        # stab row missing diagnostics but with exact context matching leakage run1
        stab = {
            "label": s.LABEL,
            "variants": {
                "V1_primary": {
                    "contrasts_vs_A": {
                        "E_rv_funding_trails": {
                            "point": 0.4879023125557301, "ci_low": -0.05470664399824281, "ci_high": 1.1856151857495267,
                            "n_obs": 12969, "n_blocks": 120, "n_reps": 2000, "seed": 20261109, "block_hours": 24, "alpha": 0.05,
                        }
                    }
                }
            },
        }
        leakage = {
            "label": s.LABEL,
            "block_bootstrap_reproducibility": {
                "run1": {
                    "point": 0.4879023125557301, "ci_low": -0.05470664399824281, "ci_high": 1.1856151857495267,
                    "n_obs": 12969, "n_blocks": 120, "seed": 20261109, "block_hours": 24, "n_reps": 2000,
                    "ci_accounting_valid": True, "effective_block_count": 120, "degenerate": False, "inference_ok": True, "regime_flags": [],
                },
                "run2": {
                    "point": 0.4879023125557301, "ci_low": -0.05470664399824281, "ci_high": 1.1856151857495267,
                    "n_obs": 12969, "n_blocks": 120, "seed": 99999999, "block_hours": 24, "n_reps": 2000,
                    "ci_accounting_valid": True, "effective_block_count": 120, "degenerate": False, "inference_ok": True, "regime_flags": [],
                },
            },
        }
        cands = s.build_enrichment_candidates(leakage, "leak.json")
        self.assertEqual(len(cands), 2)
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            sp = self._write(td, "gate4_v4_exploratory_stab_x.json", stab)
            lp = self._write(td, "leak.json", leakage)
            stab_before = sp.read_text(encoding="utf-8")
            leak_before = lp.read_text(encoding="utf-8")
            rows = s.summarize_artifacts([sp], enrichment_candidates=cands)
            self.assertEqual(sp.read_text(encoding="utf-8"), stab_before)
            self.assertEqual(lp.read_text(encoding="utf-8"), leak_before)
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertTrue(r["enrichment_applied"])
        self.assertFalse(r["missing_diagnostic_fields"])
        self.assertTrue(r["ci_valid"])
        self.assertFalse(r["degenerate"])
        self.assertTrue(r["inference_ok"])
        self.assertIn("ENRICHED_FROM_LEAKAGE", r["regime_flags"])
        # CI crosses zero in this probe => not claimable (no fabricated improvement)
        self.assertFalse(r["ci_excludes_zero"])
        self.assertFalse(r["non_degenerate_excludes_zero_claimable"])

    def test_enrichment_ambiguous_refused_keeps_missing_diag(self):
        base_ci = {
            "point": 0.5, "ci_low": -0.1, "ci_high": 1.0,
            "n_obs": 100, "n_blocks": 10, "seed": 7, "block_hours": 24, "n_reps": 20,
        }
        # two candidates match same context => ambiguous
        leakage = {"block_bootstrap_reproducibility": {
            "run1": {**base_ci, "ci_accounting_valid": True, "effective_block_count": 10, "degenerate": False, "inference_ok": True, "regime_flags": []},
            "run2": {**base_ci, "ci_accounting_valid": True, "effective_block_count": 10, "degenerate": False, "inference_ok": True, "regime_flags": []},
        }}
        cands = s.build_enrichment_candidates(leakage, "l.json")
        out, meta = s.enrich_contrast_ci(base_ci, cands)
        self.assertFalse(meta["applied"])
        self.assertEqual(meta["reason"], "AMBIGUOUS_MAPPING")
        self.assertEqual(meta["matches"], 2)
        self.assertTrue(any(k not in out for k in ("degenerate", "inference_ok")))
        row = s.extract_contrast_row("s.json", "sec", "c", out, enrich_meta=meta)
        self.assertTrue(row["missing_diagnostic_fields"])
        self.assertFalse(row["non_degenerate_excludes_zero_claimable"])
        self.assertIn("ENRICHMENT_AMBIGUOUS_MAPPING", row["regime_flags"])

    def test_enrichment_refused_when_context_mismatch(self):
        ci = {"point": 0.5, "ci_low": -0.1, "ci_high": 1.0, "n_obs": 100, "n_blocks": 10, "seed": 7, "block_hours": 24, "n_reps": 20}
        leakage = {"block_bootstrap_reproducibility": {
            "run1": {"point": 0.5, "ci_low": -0.1, "ci_high": 1.0, "n_obs": 999, "n_blocks": 10, "seed": 7, "block_hours": 24, "n_reps": 20,
                     "ci_accounting_valid": True, "effective_block_count": 10, "degenerate": False, "inference_ok": True},
        }}
        cands = s.build_enrichment_candidates(leakage, "l.json")
        _out, meta = s.enrich_contrast_ci(ci, cands)
        self.assertFalse(meta["applied"])
        self.assertEqual(meta["matches"], 0)
        row = s.extract_contrast_row("s.json", "sec", "c", ci, enrich_meta=meta)
        self.assertTrue(row["missing_diagnostic_fields"])
        self.assertFalse(row["non_degenerate_excludes_zero_claimable"])

    def test_enrichment_never_fabricates_claimable_even_if_ci_excludes_zero_and_enrichment_refused(self):
        # CI excludes zero numerically but diagnostics missing and enrichment ambiguous => not claimable
        ci = {"point": 5.0, "ci_low": 1.0, "ci_high": 9.0, "n_obs": 100, "n_blocks": 10, "seed": 1, "block_hours": 24, "n_reps": 20}
        cand = {**ci, "ci_accounting_valid": True, "effective_block_count": 10, "degenerate": False, "inference_ok": True, "regime_flags": []}
        leakage = {"block_bootstrap_reproducibility": {"run1": cand, "run2": cand}}
        cands = s.build_enrichment_candidates(leakage, "l.json")
        out, meta = s.enrich_contrast_ci(ci, cands)
        row = s.extract_contrast_row("s", "sec", "c", out, enrich_meta=meta)
        self.assertFalse(meta["applied"])
        self.assertTrue(row["ci_excludes_zero"])
        self.assertFalse(row["non_degenerate_excludes_zero_claimable"])
        self.assertIn("EXCLUDES_ZERO_NOT_CLAIMABLE", row["regime_flags"])
        self.assertIn("MISSING_DIAGNOSTIC_FIELDS", row["regime_flags"])

    def test_main_enrich_cli_writes_results_reports_counts_no_source_mutation(self):
        stab = {
            "label": s.LABEL,
            "variants": {"V1_primary": {"contrasts_vs_A": {"E_rv_funding_trails": {
                "point": 0.4, "ci_low": -0.1, "ci_high": 1.0, "n_obs": 90, "n_blocks": 9, "seed": 5, "block_hours": 24, "n_reps": 10,
            }}}},
        }
        leakage = {"block_bootstrap_reproducibility": {
            "run1": {"point": 0.4, "ci_low": -0.1, "ci_high": 1.0, "n_obs": 90, "n_blocks": 9, "seed": 5, "block_hours": 24, "n_reps": 10,
                     "ci_accounting_valid": True, "effective_block_count": 9, "degenerate": False, "inference_ok": True, "regime_flags": []},
        }}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research_state" / "gate4_v4_exploratory_stab").mkdir(parents=True)
            art = root / "research_state" / "gate4_v4_exploratory_stab" / "gate4_v4_exploratory_stab_x.json"
            art.write_text(json.dumps(stab), encoding="utf-8")
            lp = root / "leak.json"
            lp.write_text(json.dumps(leakage), encoding="utf-8")
            stab_before = art.read_text("utf-8")
            leak_before = lp.read_text("utf-8")
            outp = root / "results" / "out.md"
            rc = s.main(["--repo-root", str(root), "--enrich-diagnostics-from-leakage", str(lp), "--out", str(outp)])
            self.assertEqual(rc, 0)
            self.assertEqual(art.read_text("utf-8"), stab_before)
            self.assertEqual(lp.read_text("utf-8"), leak_before)
            txt = outp.read_text("utf-8")
            self.assertIn("Diagnostic enrichment", txt)
            self.assertIn("rows enriched by unambiguous exact-context match: **1**", txt)
            self.assertIn("ENRICHED_FROM_LEAKAGE", txt)
            self.assertIn("claimable): **0**", txt)  # CI crosses zero
            rs_files = sorted(p.relative_to(root).as_posix() for p in (root / "research_state").rglob("*") if p.is_file())
            self.assertEqual(rs_files, ["research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_x.json"])


if __name__ == "__main__":
    unittest.main()
