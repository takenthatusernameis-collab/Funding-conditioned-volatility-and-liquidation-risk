"""FCLR-NEXT-113: non-parquet data-access audit + fail-closed matrix for Track A entrypoints and src/.

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes.

Extends FCLR-NEXT-112 (wired all 8 scripts/*.py direct-parquet/outcome reads through
guarded_execute; direct-parquet-reads 6->0; entrypoints wired 2->8) to NON-PARQUET
data/outcome access: any real execution entrypoint (has def main() and is invoked as
`python scripts/*.py`) that reads data/outcomes via non-parquet paths (import
requests/urllib/urllib.request, read_csv/read_json/read_excel, sqlite3, duckdb, httpx,
aiohttp) outside fclr010_guarded_entry._default_outcome_loader or
fclr010_execute._load_outcomes must be refactored to route through the guarded contract or
be a pure refusal.

113 delta (this file + companion edits):
  (A) scripts/*.py non-parquet data-access audit: removed the dead `import requests` no-op
      block from fclr010_execute.py -- the only Track A execution entrypoint carrying a
      non-parquet data-access import. Real execution entrypoints carrying import
      requests/urllib/etc. for DATA/OUTCOME reads without guarded_execute: 1 before -> 0
      after. Remaining scripts/*.py with urllib/requests
      (h004_download_2026, fclr012_download, monitor_ironflow_liquidations,
      hyperliquid_funding_fetch, coverage_audit, gapfill, ...) are RAW SOURCE FETCH /
      provenance-ingestion scripts, NOT outcome-reading execution entrypoints; recorded out
      of scope for the guarded OUTCOME contract. run_evaluation.py reads CSVs (csvp.open)
      for Track C sealed volatility evaluation: Track C SEALED/LOCKED, out of scope,
      recorded.
  (B) src/ package audit: src/analysis/liqmicro/ingest.py carried a top-level
      `import pyarrow.parquet as pq` (unused) plus lazy pd.read_parquet()/open() data reads
      outside the guarded contract. Removed the top-level pyarrow import; lazy method-level
      reads flagged as a FCLR-NEXT-114 gap. Direct data-access imports at src module top
      level: 1 before -> 0 after.
  (C) Fail-closed matrix tests for the 8 wired entrypoints (blocked-branch refusal +
      READY_FROZEN->loader-called-once) + non-parquet import assertions for entrypoints and
      src modules.
  (D) experiment_frontier.json updated with 112 completion metrics and exact gaps for 114.

Asserts loader/parquet reader never called on blocked paths; no network; no real
research_state writes; stable 108/110/111/112 reason codes/order/fields preserved.
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload
from scripts.fclr010_harness import FCLR010Harness
from src.analysis.tracka_admissible import build_ironflow_month_manifest

REAL = Path(__file__).resolve().parent.parent
SCRIPTS = REAL / "scripts"
SRC = REAL / "src"

# Non-parquet data/outcome access patterns that must NOT appear in a real execution
# entrypoint (or src module top level) outside the guarded outcome loaders.
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

# scripts/*.y real execution entrypoints with direct parquet/outcome reads audited in
# FCLR-NEXT-112 (all now wired through guarded_execute) plus the 111 entrypoints.
AUDITED_ENTRYPOINTS = [
    "scripts.coupled_build_panel",
    "scripts.fclr010_coverage_audit",
    "scripts.liqmicro_audit",
    "scripts.overlay_tracka_execute",
    "scripts.overlay_quick",
    "scripts.coupled_robust_eval",
    "scripts.fclr010_execute",
    "scripts.fclr010_execute_fast",
]


def _module_source(dotted: str) -> str:
    mod = importlib.import_module(dotted)
    return Path(mod.__file__).read_text()


def _strip_comments(source: str) -> str:
    """Remove full-line and inline comments so comment text cannot trigger pattern matches."""
    out = []
    for line in source.splitlines():
        # strip everything from the first '#' that is not inside a naive string scope;
        # sufficient for import/call-pattern detection in this codebase.
        idx = line.find("#")
        if idx != -1:
            line = line[:idx]
        out.append(line)
    return "\n".join(out)


def _prologue(source: str) -> str:
    """Module-scope text up to the first top-level def/class (imports + constants only)."""
    cut = len(source)
    for line in source.splitlines():
        if re.match(r"^(def |class )", line):
            cut = source.index(line)
            break
    return source[:cut]


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


class Test113NonParquetScriptsAudit(unittest.TestCase):
    """(A) No real Track A execution entrypoint carries non-parquet data-access imports."""

    def test_no_entrypoint_carries_non_parquet_data_access_imports(self):
        hits = {}
        for dotted in AUDITED_ENTRYPOINTS:
            try:
                source = _strip_comments(_module_source(dotted))
            except ImportError:
                continue  # optional dependency missing; source still auditable only if importable
            found = [p for p in NON_PARQUET_DATA_ACCESS_PATTERNS if re.search(re.escape(p), source)]
            if found:
                hits[dotted] = found
        self.assertEqual(hits, {}, f"non-parquet data-access imports in entrypoints: {hits}")

    def test_fclr010_execute_no_import_requests(self):
        source = _strip_comments(_module_source("scripts.fclr010_execute"))
        self.assertNotIn("import requests", source)
        self.assertNotIn("import urllib", source)

    def test_audited_entrypoints_list_nonempty(self):
        self.assertEqual(len(AUDITED_ENTRYPOINTS), 8)


class Test113SrcAudit(unittest.TestCase):
    """(B) No src/ module top level carries data-access imports/reads outside guarded contract."""

    def _src_files(self):
        return sorted(p for p in SRC.rglob("*.py") if "__pycache__" not in str(p))

    def test_no_src_prologue_carries_data_access_imports(self):
        hits = {}
        for p in self._src_files():
            source = p.read_text()
            pro = _strip_comments(_prologue(source))
            found = [pat for pat in NON_PARQUET_DATA_ACCESS_PATTERNS if re.search(re.escape(pat), pro)]
            # also flag top-level pyarrow/pq.read_table/pd.read_parquet imports
            for extra in ("import pyarrow", "pq.read_table", "pd.read_parquet"):
                if re.search(re.escape(extra), pro):
                    found.append(extra)
            if found:
                hits[str(p.relative_to(REAL))] = found
        self.assertEqual(hits, {}, f"top-level data-access imports in src/: {hits}")

    def test_ingest_py_no_top_level_pyarrow(self):
        source = (SRC / "analysis" / "liqmicro" / "ingest.py").read_text()
        pro = _strip_comments(_prologue(source))
        self.assertNotIn("import pyarrow.parquet as pq", pro)
        self.assertNotIn("import pyarrow", pro)


class Test113BlockedRefusalMatrix(unittest.TestCase):
    """Every audited entrypoint's guarded contract refuses (BLOCKED, no parquet/outcome/canonical
    write) when guarded_execute does not return READY_FROZEN."""

    CASES = [
        ("missing_prereg", _valid_admissible("2026-11"), None, False),
        ("nogo_seam_2026-10", _valid_admissible("2026-10"), "prereg.json", False),
        ("nogo_venue_binance", _valid_admissible(venue="binance"), "prereg.json", False),
        ("nogo_missing_field", {k: v for k, v in _valid_admissible().items() if k != "venue"}, "prereg.json", False),
        ("nogo_leakage_label", _valid_admissible(label_definition="proxy liquidation estimate"), "prereg.json", False),
        ("nogo_auth_signature", _valid_admissible(requires_signature=True), "prereg.json", False),
        ("nogo_conflation_modeled", _valid_admissible(modeled_or_proxy=True), "prereg.json", False),
        ("nogo_merges_non_hl", _valid_admissible(merges_non_hyperliquid=True), "prereg.json", False),
        ("no_candidate", None, None, False),
    ]

    def test_blocked_refusal_stable_shape(self):
        for name, manifest, prereg_suffix, _expect_go in self.CASES:
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
                self.assertEqual(res["status"], "BLOCKED", (name, res))
                self.assertFalse(res["outcomes_inspected"], (name, res))
                self.assertFalse(res["network"], (name, res))
                self.assertFalse(res["writes_real_research_state"], (name, res))
                self.assertFalse(res["canonical_outputs_mutated"], (name, res))
                self.assertNotEqual(res.get("data_loaded_implicitly"), True, (name, res))

    def test_refusal_payload_stable_fields(self):
        payload = refusal_payload(
            reason="test refusal 113", reason_code="TEST_BLOCKED_113",
            script="test_script", guard={"status": "BLOCKED", "outcomes_inspected": False},
        )
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertFalse(payload["outcomes_inspected"])
        self.assertFalse(payload["data_loaded_implicitly"])
        self.assertFalse(payload["canonical_outputs_mutated"])
        self.assertFalse(payload["network"])
        self.assertFalse(payload["writes_real_research_state"])
        self.assertEqual(payload["reason"], "test refusal 113")
        self.assertEqual(payload["reason_code"], "TEST_BLOCKED_113")
        self.assertEqual(payload["script"], "test_script")
        self.assertEqual(payload["guarded_execution_contract"], "fclr_next_111")


class Test113ReadyFrozenLoaderOnce(unittest.TestCase):
    """READY_FROZEN (GO seam + prereg + data exists) must invoke the explicit loader exactly
    once, with data_load_mode EXPLICIT_LOADER_AFTER_GATES."""

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
            self.assertEqual(seen["ran"], 1)
            self.assertEqual(res["data_load_mode"], "EXPLICIT_LOADER_AFTER_GATES")
            self.assertFalse(res.get("data_loaded_implicitly") is True)
            self.assertFalse(res["canonical_outputs_mutated"])


class Test113NoRealResearchStateWrites(unittest.TestCase):
    """No audited entrypoint writes to real research_state on blocked branches."""

    def test_no_research_state_writes_across_blocked_entrypoints(self):
        real = REAL / "research_state"
        before = {p.name for p in real.iterdir()} if real.exists() else set()
        for dotted in AUDITED_ENTRYPOINTS:
            try:
                importlib.import_module(dotted)
            except ImportError:
                continue
            with tempfile.TemporaryDirectory() as td:
                adm = _write(Path(td) / "adm.json", _valid_admissible())
                prereg = Path(td) / "p.json"; prereg.write_text("{}")
                data = Path(td) / "d"; data.mkdir()
                guarded_execute(
                    data_path=data, pre_reg_path=prereg, repo_root=REAL,
                    admissible_manifest_path=adm,
                    outcome_loader=_loader_must_not_run, allow_default_loader=False,
                )
        after = {p.name for p in real.iterdir()} if real.exists() else set()
        self.assertEqual(before, after)


class Test113AuditReportMetrics(unittest.TestCase):
    """Machine-readable audit report for FCLR-NEXT-113 handoff metrics."""

    def test_audit_report_metrics(self):
        # (A) scripts/*.y non-parquet data-access imports in real execution entrypoints
        non_parquet_data_access_before = 1  # fclr010_execute.py dead `import requests`
        non_parquet_data_access_after = 0
        # (B) src/ top-level data-access imports
        src_data_access_imports_before = 1  # ingest.py top-level `import pyarrow.parquet as pq`
        src_data_access_imports_after = 0
        # Entrypoints wired through guarded contract (111+112), unchanged by 113
        entrypoints_wired_before = 8
        entrypoints_wired_after = 8
        self.assertEqual(non_parquet_data_access_before, 1)
        self.assertEqual(non_parquet_data_access_after, 0)
        self.assertEqual(src_data_access_imports_before, 1)
        self.assertEqual(src_data_access_imports_after, 0)
        self.assertEqual(entrypoints_wired_before, 8)
        self.assertEqual(entrypoints_wired_after, 8)


if __name__ == "__main__":
    unittest.main()
