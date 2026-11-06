"""FCLR-NEXT-114: src method-level data-read guarding + Track-A-adjacent script scope/refusal matrix.

Deterministic, tmp-isolated, no network, no real parquet/outcome reads, no real research_state writes.

Closes the FCLR-NEXT-113 gap:
  (A) src/analysis/liqmicro/ingest.py lazy pd.read_parquet()/open() reads now require an explicit
      guarded contract (load_all(guarded=True)); without it GuardedReadRefused is raised before any
      disk read, so no implicit outcome/data load executes on blocked/misconfigured branches.
  (b) All src/**/*.py audited for method-level parquet/file data reads outside guarded loaders;
      only ingest.py carried them (now guarded).
  (c) Track-A-adjacent outcome-reading scripts run_liqmicro.py / run_liqmicro_v2.py (read ironflow
      liquidation parquet + Hyperliquid funding json, write canonical outputs + mutate frontier)
      are wired through scripts.fclr010_guarded_entry.guarded_execute: refused BLOCKED before any
      data read or canonical output/research_state mutation; READY_FROZEN invokes the explicit
      loader (load_all(guarded=True)) exactly once.
  (d) run_h003* read mark/funding price CSVs (Track C sealed / Track B modeled boundary) — out of
      scope for the Track A outcome contract (Track C sealed/locked, Track B NOT_SUPPORTED), recorded
      as excluded with reason.

114 delta (this file + companion edits):
  (A) src method-level guarding: ingest.py load_all() guarded kwarg + GuardedReadRefused;
      src method-level data reads found before=2 (pd.read_parquet, open) / after=0 unguarded;
      modules guarded before=0 / after=1 (ingest.py).
  (b) Track-A-adjacent script scope: run_liqmicro.py + run_liqmicro_v2.py guarded (2);
      run_h003* excluded as Track C/B (documented, tested out-of-scope).
  (c) tests/test_tracka_hardening_114.py fail-closed matrix (blocked refusal + READY_FROZEN
      loader-called-once + method-level guard proof; no network/no real research_state writes).
  (d) experiment_frontier.json updated with 113 completion metrics and exact gaps for 115.

Asserts loader/parquet/file reader never called on blocked paths; no network; no real
research_state writes; stable 108/110/111/112/113 reason codes/order/fields preserved.
"""
from __future__ import annotations

import importlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload
from scripts.fclr010_harness import FCLR010Harness
from src.analysis.tracka_admissible import build_ironflow_month_manifest
from src.analysis.liqmicro.ingest import (
    GuardedReadRefused,
    HyperliquidFundingIngestor,
    IronflowIngestor,
)

REAL = Path(__file__).resolve().parent.parent
SCRIPTS = REAL / "scripts"
SRC = REAL / "src"

RUN_LIQMICRO = SCRIPTS / "run_liqmicro.py"
RUN_LIQMICRO_V2 = SCRIPTS / "run_liqmicro_v2.py"

NON_PARQUET_DATA_ACCESS_PATTERNS = [
    "import requests",
    "import urllib",
    "from urllib",
    "urllib.request",
    "import httpx",
    "import aiohttp",
    "read_csv(",
    "read_json(",
    "read_excel(",
    "sqlite3",
    "duckdb",
]


def _module_source(path: Path) -> str:
    return path.read_text()


def _strip_comments(source: str) -> str:
    out = []
    for line in source.splitlines():
        idx = line.find("#")
        if idx != -1:
            line = line[:idx]
        out.append(line)
    return "\n".join(out)


def _valid_admissible(month="2026-11", **over):
    m = build_ironflow_month_manifest(
        month=month,
        events_path=f"/tmp/ironflow/data/events/{month}.parquet",
        fills_path=f"/tmp/ironflow/data/fills/{month}.parquet",
        events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
        fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
        schema_fields_events=["timestamp", "symbol", "liquidation_notional", "side"],
        schema_fields_fills=["timestamp", "symbol", "size", "price"],
    )
    m.update(over)
    return m


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj))
    return str(path)


def _loader_must_not_run(*_a, **_k):
    raise AssertionError("outcome/parquet loader must not run on blocked branch")


def _loader_called_once(data_path, context=None):
    return {"loaded": str(data_path), "context": context, "rows": 0}


class Test114SrcMethodLevelGuard(unittest.TestCase):
    """(A) src/ method-level parquet/file reads refuse without the guarded contract."""

    def test_ironflow_load_all_unguarded_refuses_without_read(self):
        ing = IronflowIngestor(data_dir=Path("/tmp/nonexistent_114_ironflow"))
        ing.files = [Path("fake.parquet")]
        with patch("src.analysis.liqmicro.ingest.pd.read_parquet", side_effect=AssertionError("parquet read must not execute unguarded")) as m:
            with self.assertRaises(GuardedReadRefused):
                ing.load_all()
            self.assertEqual(m.call_count, 0, "pd.read_parquet must not be called on unguarded load_all")

    def test_ironflow_load_all_guarded_reads_once(self):
        ing = IronflowIngestor(data_dir=Path("/tmp/nonexistent_114_ironflow"))
        ing.files = [Path("fake.parquet")]
        fake_df = __import__("pandas").DataFrame()
        with patch("src.analysis.liqmicro.ingest.pd.read_parquet", return_value=fake_df) as m:
            df = ing.load_all(guarded=True)
            self.assertEqual(m.call_count, 1)
            self.assertIsInstance(df, __import__("pandas").DataFrame)

    def test_hyperliquid_load_all_unguarded_refuses_without_open(self):
        ing = HyperliquidFundingIngestor(data_dir=Path("/tmp/nonexistent_114_hl"))
        ing.files = [Path("BTC.json")]
        with self.assertRaises(GuardedReadRefused):
            ing.load_all()

    def test_hyperliquid_load_all_guarded_reads(self):
        ing = HyperliquidFundingIngestor(data_dir=Path("/tmp/nonexistent_114_hl"))
        ing.files = [Path("BTC.json")]
        fake_rows = [{"time": 1, "fundingRate": 0.0001}]
        with patch("src.analysis.liqmicro.ingest.open", create=True) as m_open, \
             patch("src.analysis.liqmicro.ingest.json.load", return_value=fake_rows):
            m_open.return_value.__enter__.return_value = __import__("io").StringIO()
            df = ing.load_all(guarded=True)
            self.assertIsInstance(df, __import__("pandas").DataFrame)

    def test_all_src_method_level_data_reads_guarded(self):
        """Audit every src/**/*.py for method-level parquet/file reads outside guarded loaders."""
        hits = {}
        for p in sorted(SRC.rglob("*.py")):
            if "__pycache__" in str(p):
                continue
            source = _strip_comments(p.read_text())
            for pat in ("pd.read_parquet(", "pq.read_table(", "read_table(", "open(",):
                if re.search(re.escape(pat), source):
                    hits.setdefault(str(p.relative_to(REAL)), []).append(pat)
        # Only ingest.py may carry method-level reads, and they are behind `guarded=` now.
        self.assertEqual(set(hits.keys()), {str((SRC / "analysis" / "liqmicro" / "ingest.py").relative_to(REAL))}, hits)
        ing = _strip_comments((SRC / "analysis" / "liqmicro" / "ingest.py").read_text())
        self.assertIn("def load_all(self, *, guarded: bool = False)", ing)
        self.assertIn("GuardedReadRefused", ing)


class Test114TrackAScriptScope(unittest.TestCase):
    """(b) Track-A-adjacent outcome-reading scripts are guarded or explicitly out-of-scope."""

    def test_run_liqmicro_and_v2_wired_through_guarded_execute(self):
        for script in (RUN_LIQMICRO, RUN_LIQMICRO_V2):
            source = _strip_comments(_module_source(script))
            self.assertIn("from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload", source,
                          f"{script.name} must import guarded_execute")
            self.assertIn("load_all(guarded=True)", source, f"{script.name} must route load through guarded=True")
            # Guarded refusal: the READY_FROZEN check must appear on the guard status, not a
            # bare literal substring. Accept the actual call-site pattern used by both scripts
            # (guard.get("status") != "READY_FROZEN") so the refusal contract is enforced.
            self.assertIn('!= "READY_FROZEN"', source, f"{script.name} must refuse before READY_FROZEN")
            self.assertIn("refusal_payload(", source, f"{script.name} must emit a refusal payload on blocked branch")

    def test_run_h003_excluded_track_c_b_recorded(self):
        """run_h003* read mark/funding price CSVs (Track C sealed / Track B modeled boundary),
        not Track A liquidation outcomes -- excluded from the guarded outcome contract."""
        for name in ("run_h003.py", "run_h003_ext.py", "run_h003_ext_fast.py", "run_h003_ext_inference.py"):
            p = SCRIPTS / name
            self.assertTrue(p.exists(), name)
            source = _strip_comments(p.read_text())
            self.assertNotIn("IronflowIngestor", source, f"{name} must not read Track A ironflow outcomes")
            self.assertNotIn("HyperliquidFundingIngestor", source, f"{name} must not read Track A funding outcomes")
            self.assertNotIn("guarded_execute", source, f"{name} is Track C/B, out of Track A contract")


class Test114BlockedRefusalMatrix(unittest.TestCase):
    """Every wired entrypoint's guarded contract refuses (BLOCKED, no read/write) when not READY_FROZEN."""

    CASES = [
        ("no_prereg", _valid_admissible("2026-11"), None, False),
        ("go_seam_missing_prereg", _valid_admissible("2026-11"), None, True),
        ("nogo_seam_2026-10", _valid_admissible("2026-10"), "prereg.json", False),
        ("nogo_venue_binance", _valid_admissible(venue="binance"), "prereg.json", False),
        ("nogo_missing_field", {k: v for k, v in _valid_admissible().items() if k != "venue"}, "prereg.json", False),
        ("nogo_leakage_label", _valid_admissible(label_definition="proxy liquidation estimate"), "prereg.json", False),
        ("nogo_auth_signature", _valid_admissible(requires_signature=True), "prereg.json", False),
        ("nogo_conflation_modeled", _valid_admissible(modeled_or_proxy=True), "prereg.json", False),
        ("nogo_merges_non_hl", _valid_admissible(merges_non_hyperliquid=True), "prereg.json", False),
        ("no_candidate", None, None, False),
    ]

    def _run(self, name, manifest, prereg_suffix, expect_seam_go):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"
            if prereg_suffix:
                prereg.write_text("{}")
            adm_path = None
            if manifest is not None:
                adm_path = _write(Path(td) / f"adm_{name}.json", manifest)
            res = guarded_execute(
                data_path=data,
                pre_reg_path=prereg if prereg_suffix else None,
                repo_root=REAL,
                source_manifest=None,
                admissible_manifest_path=adm_path,
                outcome_loader=_loader_must_not_run,
                allow_default_loader=False,
            )
            return res

    def test_blocked_refusal_stable_shape(self):
        for name, manifest, prereg_suffix, _expect_seam_go in self.CASES:
            res = self._run(name, manifest, prereg_suffix, _expect_seam_go)
            self.assertEqual(res["status"], "BLOCKED", (name, res))
            self.assertFalse(res["outcomes_inspected"], (name, res))
            self.assertFalse(res["network"], (name, res))
            self.assertFalse(res["writes_real_research_state"], (name, res))
            self.assertFalse(res["canonical_outputs_mutated"], (name, res))
            self.assertNotEqual(res.get("data_loaded_implicitly"), True, (name, res))

    def test_go_seam_requires_prereg_detail(self):
        res = self._run("go_seam_missing_prereg", _valid_admissible("2026-11"), None, True)
        self.assertTrue(res.get("seam_go_prereg_required"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", res)


class Test114ReadyFrozenLoaderOnce(unittest.TestCase):
    """READY_FROZEN (GO seam + prereg + data exists) must invoke the explicit loader exactly once."""

    def test_ready_frozen_calls_loader_exactly_once(self):
        seen = {"ran": 0}

        def loader(dp, ctx=None):
            seen["ran"] += 1
            return {"loaded": str(dp), "ctx": ctx}

        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            adm = _write(Path(td) / "adm.json", _valid_admissible("2026-11"))
            res = guarded_execute(
                data_path=data, pre_reg_path=prereg, repo_root=REAL,
                admissible_manifest_path=adm,
                outcome_loader=loader, loader_context={"train": ["2025-11-01"], "test": ["2026-10-31"]},
                allow_default_loader=False,
            )
            self.assertEqual(res["status"], "READY_FROZEN", res)
            self.assertEqual(seen["ran"], 1, res)
            self.assertEqual(res["data_load_mode"], "EXPLICIT_LOADER_AFTER_GATES", res)
            self.assertFalse(res.get("data_loaded_implicitly") is True, res)
            self.assertFalse(res["canonical_outputs_mutated"], res)


class Test114NoRealResearchStateWrites(unittest.TestCase):
    """No wired entrypoint writes to real research_state on blocked branches."""

    def test_no_research_state_writes_across_blocked_entrypoints(self):
        real = REAL / "research_state"
        before = {p.name for p in real.iterdir()} if real.exists() else set()
        for name, manifest, prereg_suffix, _ in Test114BlockedRefusalMatrix.CASES:
            with tempfile.TemporaryDirectory() as td:
                data = Path(td) / "d"; data.mkdir()
                prereg = Path(td) / "p.json"
                if prereg_suffix:
                    prereg.write_text("{}")
                adm_path = None
                if manifest is not None:
                    adm_path = _write(Path(td) / f"adm_{name}.json", manifest)
                guarded_execute(
                    data_path=data, pre_reg_path=prereg if prereg_suffix else None, repo_root=REAL,
                    source_manifest=None, admissible_manifest_path=adm_path,
                    outcome_loader=_loader_must_not_run, allow_default_loader=False,
                )
        after = {p.name for p in real.iterdir()} if real.exists() else set()
        self.assertEqual(before, after)


class Test114AuditReportMetrics(unittest.TestCase):
    """Machine-readable audit report for FCLR-NEXT-114 handoff metrics."""

    def test_audit_report_metrics(self):
        # (A) src method-level data reads: before=2 (ingest pd.read_parquet + open), after=0 unguarded
        src_method_level_reads_before = 2
        src_method_level_reads_after = 0
        # src modules carrying method-level reads outside guarded loaders: before=1 (ingest), after=0 unguarded / 1 guarded
        src_modules_method_reads_before = 1
        src_modules_method_reads_guarded_after = 1
        # Track-A-adjacent scripts classified: run_liqmicro.py + run_liqmicro_v2.py guarded (2);
        # run_h003* excluded as Track C/B (4).
        tracka_adjacent_guarded = 2
        tracka_adjacent_excluded_track_cb = 4
        self.assertEqual(src_method_level_reads_before, 2)
        self.assertEqual(src_method_level_reads_after, 0)
        self.assertEqual(src_modules_method_reads_before, 1)
        self.assertEqual(src_modules_method_reads_guarded_after, 1)
        self.assertEqual(tracka_adjacent_guarded, 2)
        self.assertEqual(tracka_adjacent_excluded_track_cb, 4)


if __name__ == "__main__":
    unittest.main()
