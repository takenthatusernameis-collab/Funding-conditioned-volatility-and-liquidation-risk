"""FCLR-STARTER-001: §14 frozen-protocol campaign non-avoidance regression.

tmp-isolated, read-only, no network, no parquet/outcome reads, no real
research_state writes. Pins the invariant that, once the starter campaign is
announced in the durable handoff, a later session cannot satisfy the
handoff-heavywork gate with prose, placeholders, or an arbitrary artifact: it
must emit a §14-hash-bound protocol freeze, a panel hash freeze recorded before
target generation, and the B0/B1 baseline triad (plus a trigger check).

It also pins that the campaign may never overwrite the sealed legacy
``research_state/research_protocol.md`` (the FCLR-001 2024-01..03 experiment
definition consumed by ``scripts/run_evaluation.py``).
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

REAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REAL / "scripts"))

import check_handoff_heavywork_gate as gate  # noqa: E402

CAMPAIGN_START = "20261119T215623Z"
CAMPAIGN_ID = f"FCLR-STARTER-001-{CAMPAIGN_START}"
PRE_START_SESSION = "session_20261119T180650Z"
POST_START_SESSION = "session_20261120T010000Z"
PROTOCOL_REL = "research_state/protocol_fclr_starter_001_20261119T215623Z.md"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _seed_prompt(repo: Path) -> str:
    body = (
        gate.STARTER_SECTION_HEADING
        + "\n\nStarter protocol body: next-24h realized variance, OLS HAR.\n\n"
    )
    _write(repo / "RESEARCH_PROMPT.md", body + "## 15. Next section\nmore text\n")
    return gate.section14_body(repo)


def _seed_protocol(repo: Path, body: str, rel: str = PROTOCOL_REL) -> str:
    text = "# FCLR-STARTER-001 protocol\n\n" + body + "\n"
    _write(repo / rel, text)
    return (repo / rel).read_text(encoding="utf-8")


def _valid_artifacts(repo: Path, session: Path, body: str) -> dict:
    protocol_text = _seed_protocol(repo, body)
    freeze = {
        "experiment_id": "FCLR-STARTER-001",
        "protocol_path": PROTOCOL_REL,
        "section14_sha256": hashlib.sha256(body.encode()).hexdigest(),
        "protocol_sha256": hashlib.sha256(protocol_text.encode()).hexdigest(),
        "outcome_data_inspected_before_freeze": False,
    }
    panel = {
        "experiment_id": "FCLR-STARTER-001",
        "panel_sha256": "a" * 64,
        "source_hashes": {"mark_klines": "b" * 64, "funding": "c" * 64},
        "panel_frozen_before_target_generation": True,
        "eligible_definition": "linear perp x closed UTC hour, all discoverable listings",
        "cutoff_utc": "2026-11-01T00:00:00Z",
    }
    baselines = {
        "experiment_id": "FCLR-STARTER-001",
        "split_used": "development_validation",
        "holdout_opened": False,
        "n_obs": 1000,
        "models": {"B0": {"qlike": 0.42}, "B1": {"qlike": 0.38}},
    }
    _write(session / f"fclr_starter001_protocol_freeze_{CAMPAIGN_START}.json",
           json.dumps(freeze))
    _write(session / f"fclr_starter001_protocol_freeze_{CAMPAIGN_START}.md", "# frozen\n")
    _write(session / f"fclr_starter001_panel_freeze_{CAMPAIGN_START}.json",
           json.dumps(panel))
    _write(session / f"fclr_starter001_panel_freeze_{CAMPAIGN_START}.md", "# panel\n")
    _write(session / f"fclr_starter001_baselines_{CAMPAIGN_START}.py", "print('b0b1')\n")
    _write(session / f"fclr_starter001_baselines_{CAMPAIGN_START}.json",
           json.dumps(baselines))
    _write(session / f"fclr_starter001_baselines_{CAMPAIGN_START}.md", "# baselines\n")
    _write(session / f"trigger_check_{CAMPAIGN_START}.json", '{"checks": []}')
    return freeze


class TestStarterCampaignGate(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.body = _seed_prompt(self.repo)
        self.session = self.repo / "research_state" / POST_START_SESSION
        self.session.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def _state(self, sid: str = POST_START_SESSION, files: list[str] | None = None):
        if files is None:
            files = [p.name for p in self.session.glob("*") if p.is_file()]
        return gate._starter_001_state(
            f"campaign {CAMPAIGN_ID}", sid, files, self.session, self.repo
        )

    def test_no_campaign_means_not_required(self):
        st = gate._starter_001_state("no campaign here", POST_START_SESSION,
                                     [], self.session, self.repo)
        self.assertFalse(st["required"])
        self.assertTrue(st["pass"])

    def test_pre_start_session_grandfathered(self):
        st = self._state(sid=PRE_START_SESSION)
        self.assertFalse(st["required"])
        self.assertTrue(st["pass"])

    def test_post_start_missing_artifacts_fails_closed(self):
        st = self._state()
        self.assertTrue(st["required"])
        self.assertFalse(st["pass"])
        self.assertTrue(st["missing_required_artifacts"])

    def test_placeholder_artifacts_fail_closed(self):
        for name in (
            f"fclr_starter001_protocol_freeze_{CAMPAIGN_START}.json",
            f"fclr_starter001_panel_freeze_{CAMPAIGN_START}.json",
            f"fclr_starter001_baselines_{CAMPAIGN_START}.json",
            f"trigger_check_{CAMPAIGN_START}.json",
        ):
            _write(self.session / name, "{}")
        st = self._state()
        self.assertFalse(st["pass"])
        self.assertTrue(st["content_failures"])

    def test_valid_artifacts_pass(self):
        _valid_artifacts(self.repo, self.session, self.body)
        st = self._state()
        self.assertTrue(st["required"])
        self.assertTrue(st["pass"], st)
        self.assertEqual(st["content_failures"], [])

    def test_sealed_protocol_overwrite_fails(self):
        freeze = _valid_artifacts(self.repo, self.session, self.body)
        freeze["protocol_path"] = gate.STARTER_SEALED_PROTOCOL
        _write(
            self.session / f"fclr_starter001_protocol_freeze_{CAMPAIGN_START}.json",
            json.dumps(freeze),
        )
        st = self._state()
        self.assertIn("PROTOCOL_FREEZE_OVERWRITES_SEALED", st["content_failures"])
        self.assertFalse(st["pass"])

    def test_section14_mismatch_fails(self):
        _valid_artifacts(self.repo, self.session, self.body)
        _write(self.repo / PROTOCOL_REL, "# unrelated protocol\n")
        st = self._state()
        self.assertIn("PROTOCOL_FREEZE_SECTION14_MISMATCH", st["content_failures"])
        self.assertFalse(st["pass"])

    def test_panel_before_target_order_enforced(self):
        _valid_artifacts(self.repo, self.session, self.body)
        p = self.session / f"fclr_starter001_panel_freeze_{CAMPAIGN_START}.json"
        panel = json.loads(p.read_text())
        panel["panel_frozen_before_target_generation"] = False
        _write(p, json.dumps(panel))
        st = self._state()
        self.assertIn("PANEL_FREEZE_ORDER", st["content_failures"])


if __name__ == "__main__":
    unittest.main()
