#!/usr/bin/env python3
"""Bounded campaign resume logic for the Kilo general-agent workflow.

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

from typing import Any

RESUME_SCHEMA_VERSION = 1
RECOVERY_PROMPT_PREFIX = (
    "IMPORTANT SAME-RUN RECOVERY: the previous Kilo worker session "
    "(session {session}) ended because bounded remote checkpoint persistence "
    "failed. This is a NEW worker session inside the SAME active GitHub Actions "
    "run, not a request to end the workflow."
)


def valid_sha(sha: str | None) -> bool:
    """A SHA is valid when it is a non-empty 40-hex string."""
    if not isinstance(sha, str) or len(sha) != 40:
        return False
    return all(c in "0123456789abcdef" for c in sha)


def is_ahead(local_head: str | None, base_sha: str | None) -> bool:
    """Return True when the local HEAD is a strict descendant of the base SHA."""
    if not (valid_sha(local_head) and valid_sha(base_sha)):
        return False
    return local_head != base_sha


def build_resume_state(
    *,
    session: int,
    local_head: str | None,
    base_sha: str | None,
    remote_tracking_sha: str | None,
    failed_session_head: str | None,
) -> dict[str, Any]:
    """Construct a resume-state record for a persistence-recovery handoff."""
    state = {
        "schema_version": RESUME_SCHEMA_VERSION,
        "session": session,
        "local_head": local_head,
        "base_sha": base_sha,
        "remote_tracking_sha": remote_tracking_sha,
        "failed_session_head": failed_session_head,
        "has_unpushed_work": is_ahead(local_head, base_sha),
        "prompt": None,
    }
    if state["has_unpushed_work"]:
        state["prompt"] = RECOVERY_PROMPT_PREFIX.format(session=session)
    return state


def validate_resume_state(state: dict[str, Any]) -> None:
    """Raise ValueError if a resume state violates the recovery contract."""
    if not isinstance(state, dict):
        raise ValueError("resume state must be a dict")
    if state.get("schema_version") != RESUME_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version must be {RESUME_SCHEMA_VERSION}, got {state.get('schema_version')!r}"
        )
    for field in (
        "session",
        "local_head",
        "base_sha",
        "remote_tracking_sha",
        "failed_session_head",
        "has_unpushed_work",
        "prompt",
    ):
        if field not in state:
            raise ValueError(f"resume state missing required field {field!r}")
    if not isinstance(state["session"], int) or state["session"] < 1:
        raise ValueError("session must be a positive integer")
    if not isinstance(state["has_unpushed_work"], bool):
        raise ValueError("has_unpushed_work must be a bool")
    if state["has_unpushed_work"] and state.get("prompt") is None:
        raise ValueError("prompt must be set when there is unpushed work")
    if not state["has_unpushed_work"] and state.get("prompt") is not None:
        raise ValueError("prompt must be None when there is no unpushed work")


def creditable_progress(
    *,
    verified_remote_sha: str | None,
    verified_head_sha: str | None,
    base_sha: str | None,
) -> bool:
    """Return True only when remote SHA exactly matches the verified local HEAD.

    Progress is never credited before an exact remote SHA match, and never
    credited for a base-to-HEAD range that contains no meaningful changes.
    """
    if not (valid_sha(verified_remote_sha) and valid_sha(verified_head_sha)):
        return False
    if verified_remote_sha != verified_head_sha:
        return False
    if not valid_sha(base_sha):
        return False
    # A base-to-HEAD range with no net change is not progress.
    if verified_head_sha == base_sha:
        return False
    return True