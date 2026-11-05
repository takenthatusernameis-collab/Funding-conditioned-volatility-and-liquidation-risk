#!/usr/bin/env python3
"""FCLR-NEXT-104: consolidate unreferenced source_probe_FCLR-NEXT-002_* family.

The 8 per-venue source-probe artifacts (academic_archives, binance_alt_paths,
bybit, cryptodatadownload, deribit, github_raw, huggingface, okx) are
unreferenced by AGENT_HANDOFF.md, experiment_frontier.json, run_manifest.json,
scripts/* and tests/* (verified by exact name/stem scan at 20261105T1826Z).
Their substantive content is already summarised in
tracka_source_hardening_history_091.md (the canonical source-hardening
history). This script preserves provenance (sha256 + bytes + first-60-lines
excerpt) for each removed file inside that canonical history, then deletes
the originals so the root md+json bound (<=163) regains slack before any
new evidence is written.

Idempotent: if the files are already gone, it is a no-op. No network. No
writes outside research_state. Deterministic.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"

TARGETS = [
    "source_probe_FCLR-NEXT-002_academic_archives.md",
    "source_probe_FCLR-NEXT-002_binance_alt_paths.md",
    "source_probe_FCLR-NEXT-002_bybit.md",
    "source_probe_FCLR-NEXT-002_cryptodatadownload.md",
    "source_probe_FCLR-NEXT-002_deribit.md",
    "source_probe_FCLR-NEXT-002_github_raw.md",
    "source_probe_FCLR-NEXT-002_huggingface.md",
    "source_probe_FCLR-NEXT-002_okx.md",
]

HISTORY = RS / "tracka_source_hardening_history_091.md"
MARKER_BEGIN = "<!-- CONSOLIDATED 104: source_probe_FCLR-NEXT-002_* family (provenance preserved) BEGIN -->"
MARKER_END = "<!-- CONSOLIDATED 104: source_probe_FCLR-NEXT-002_* family (provenance preserved) END -->"


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _excerpt(p: Path, n: int = 60) -> str:
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()[:n]
    return "\n".join(lines)


def main() -> int:
    present = [t for t in TARGETS if (RS / t).exists()]
    if not present:
        print("no_source_probe_files_present_noop")
        return 0

    blocks = []
    for t in present:
        p = RS / t
        blocks.append(
            f"### {t} (sha256={_sha256(p)} bytes={p.stat().st_size})\n"
            f"```\n{_excerpt(p)}\n```"
        )
    section = (
        f"\n\n## CONSOLIDATED 104 (20261105T1826Z, FCLR-NEXT-104 root-bound pre-evidence)\n"
        f"Consolidated unreferenced `source_probe_FCLR-NEXT-002_*` per-venue probe family "
        f"(verified ref-free by exact name/stem scan vs AGENT_HANDOFF/frontier/manifest/scripts/tests). "
        f"Provenance preserved as sha256+bytes+excerpt; originals deleted to regain root md+json slack.\n"
        f"{MARKER_BEGIN}\n" + "\n\n".join(blocks) + f"\n{MARKER_END}\n"
    )

    txt = HISTORY.read_text(encoding="utf-8")
    if MARKER_BEGIN in txt and MARKER_END in txt:
        # replace existing block (idempotent re-run)
        start = txt.index(MARKER_BEGIN)
        end = txt.index(MARKER_END) + len(MARKER_END)
        txt = txt[:start] + section.lstrip("\n") + txt[end:]
    else:
        txt = txt.rstrip("\n") + section

    HISTORY.write_text(txt, encoding="utf-8")

    for t in present:
        (RS / t).unlink()

    after = len(list(RS.glob("*.md"))) + len(list(RS.glob("*.json")))
    print(f"consolidated={len(present)} root_md_json_after={after}")
    return 0


if __name__ == "__main__":
    sys.exit(main())