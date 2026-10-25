#!/usr/bin/env python3
"""Classify whether a base..head range contains meaningful project progress.

Meaningful progress means at least one non-workflow file changed. Workflow-only
changes, marker-only commits, and status-only changes never count. Invalid or
missing SHAs fail closed (non-zero exit).
"""
from __future__ import annotations

import argparse
import subprocess
import sys


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def _valid_sha(sha: str) -> bool:
    if not sha:
        return False
    result = _git("cat-file", "-t", sha)
    return result.returncode == 0 and result.stdout.strip() == "commit"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--verified-remote-sha")
    args = parser.parse_args()

    base = args.base_sha.strip()
    head = args.head_sha.strip()
    if not _valid_sha(base) or not _valid_sha(head):
        return 1
    if base == head:
        return 1

    if args.verified_remote_sha is not None:
        remote = args.verified_remote_sha.strip()
        if not _valid_sha(remote) or remote != head:
            return 1

    result = _git("diff", "--name-only", f"{base}..{head}")
    if result.returncode != 0:
        return 1
    changed = [p for p in result.stdout.splitlines() if p.strip()]
    meaningful = [p for p in changed if not p.startswith(".github/workflows/")]
    return 0 if meaningful else 1


if __name__ == "__main__":
    sys.exit(main())
PYEOF