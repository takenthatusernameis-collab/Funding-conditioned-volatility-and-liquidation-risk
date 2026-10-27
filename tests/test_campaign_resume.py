#!/usr/bin/env python3
"""Tests for scripts/campaign_resume.py.

The controller (`.github/workflows/main.yml`) runs many sequential Kilo worker
sessions inside a single GitHub Actions run. When a checkpoint fails to persist
remotely, the controller preserves the local-ahead commit and starts a fresh
worker session in the SAME run with a recovery prompt. This module models the
deterministic resume-state contract so it can be unit-tested:

  * a resume state is only valid when the local HEAD is ahead of the base SHA;
  * the recovery prompt is only emitted when there is genuinely unpushed work;
  * resume never discards local commits or rewrites history;
  * a resumed session must not be credited for progress until the remote SHA
    matches the verified local HEAD.

No network access, no credentials, no trading.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from campaign_resume import (  # noqa: E402
    RECOVERY_PROMPT_PREFIX,
    RESUME_SCHEMA_VERSION,
    build_resume_state,
    creditable_progress,
    is_ahead,
    validate_resume_state,
    valid_sha,
)


def _sha(n: int) -> str:
    return f"{n:040x}"


def test_valid_sha_accepts_40_hex():
    assert valid_sha(_sha(1)) is True
    assert valid_sha("z" * 40) is False
    assert valid_sha("abc") is False
    assert valid_sha(None) is False


def test_is_ahead_requires_distinct_valid_shas():
    base = _sha(1)
    assert is_ahead(_sha(2), base) is True
    assert is_ahead(base, base) is False
    assert is_ahead(None, base) is False
    assert is_ahead(_sha(2), None) is False


def test_resume_state_with_no_unpushed_work_has_no_prompt():
    base = _sha(1)
    state = build_resume_state(
        session=3,
        local_head=base,
        base_sha=base,
        remote_tracking_sha=base,
        failed_session_head=base,
    )
    assert state["has_unpushed_work"] is False
    assert state["prompt"] is None
    validate_resume_state(state)  # must not raise


def test_resume_state_with_unpushed_work_has_prompt():
    base = _sha(1)
    head = _sha(2)
    state = build_resume_state(
        session=4,
        local_head=head,
        base_sha=base,
        remote_tracking_sha=base,
        failed_session_head=head,
    )
    assert state["has_unpushed_work"] is True
    assert state["prompt"] is not None
    # The formatted prompt begins with the literal prefix text preceding the
    # {session} placeholder and contains the interpolated session number.
    assert state["prompt"].startswith(RECOVERY_PROMPT_PREFIX.split("{session}", 1)[0])
    assert "session 4" in state["prompt"]
    validate_resume_state(state)


def test_validate_resume_state_rejects_prompt_without_unpushed_work():
    base = _sha(1)
    state = build_resume_state(
        session=1,
        local_head=base,
        base_sha=base,
        remote_tracking_sha=base,
        failed_session_head=base,
    )
    state["prompt"] = "injected"
    try:
        validate_resume_state(state)
    except ValueError:
        return
    raise AssertionError("expected ValueError when prompt set without unpushed work")


def test_creditable_progress_requires_exact_remote_match():
    base = _sha(1)
    head = _sha(2)
    assert creditable_progress(
        verified_remote_sha=head, verified_head_sha=head, base_sha=base
    ) is True
    # remote behind head -> not credited
    assert creditable_progress(
        verified_remote_sha=base, verified_head_sha=head, base_sha=base
    ) is False
    # head equals base -> no net change -> not credited
    assert creditable_progress(
        verified_remote_sha=base, verified_head_sha=base, base_sha=base
    ) is False
    # invalid inputs fail closed
    assert creditable_progress(
        verified_remote_sha=None, verified_head_sha=head, base_sha=base
    ) is False


def test_resume_state_schema_version_is_stable():
    assert RESUME_SCHEMA_VERSION == 1
    base = _sha(1)
    state = build_resume_state(
        session=1,
        local_head=base,
        base_sha=base,
        remote_tracking_sha=base,
        failed_session_head=base,
    )
    assert state["schema_version"] == RESUME_SCHEMA_VERSION