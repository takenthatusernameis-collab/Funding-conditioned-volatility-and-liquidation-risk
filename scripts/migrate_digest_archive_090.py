#!/usr/bin/env python3
"""[HEAVY-090] Migrate legacy per-run ironflow_probe_digest_<ts>.json files into
the single canonical running archive ironflow_probe_digest_latest.json.

Root cause fixed in scripts/monitor_ironflow_liquidations.py: the old
_consolidate_ironflow_probes named the digest after the CURRENT latest probe
(ironflow_probe_digest_<latest_ts>.json), so every --quick run wrote a new
digest file and never removed the prior one. By 20261105T0714Z the directory
held 37 digest files, each a 1-entry archive of the immediately-removed probe
(all data_through=2026-10, all triggered=false). generate_trend_report() merges
every one of them, so the 36 stale digests were pure artifact churn inflating
every --report run.

This script folds every legacy digest's entries into the canonical archive
(de-duplicated by probe_id), deletes the legacy files, and leaves exactly one
digest file. It is idempotent: re-running it is a no-op once the migration is
complete. It is offline (no network) and does not touch the live probe file.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = REPO_ROOT / "research_state"
CANONICAL = EVIDENCE_DIR / "ironflow_probe_digest_latest.json"


def main():
    legacy = sorted(
        (p for p in EVIDENCE_DIR.glob("ironflow_probe_digest_*.json")
         if p.name != CANONICAL.name),
        key=lambda p: p.name,
    )
    if not legacy:
        print("no legacy digest files to migrate")
        return 0

    entries = []
    seen = set()
    for dp in legacy:
        try:
            dg = json.loads(dp.read_text())
        except Exception as e:
            print(f"WARN could not parse {dp.name}: {e!r}")
            continue
        for e in dg.get("entries", []) or []:
            pid = e.get("probe_id") or e.get("source_file")
            if pid and pid in seen:
                continue
            if pid:
                seen.add(pid)
            entries.append(e)

    # Merge any existing canonical archive (first run).
    if CANONICAL.exists():
        try:
            dg = json.loads(CANONICAL.read_text())
            for e in dg.get("entries", []) or []:
                pid = e.get("probe_id") or e.get("source_file")
                if pid and pid in seen:
                    continue
                if pid:
                    seen.add(pid)
                entries.append(e)
        except Exception as e:
            print(f"WARN could not parse canonical {CANONICAL.name}: {e!r}")

    # Sort by timestamp for a stable, auditable archive.
    entries.sort(key=lambda e: e.get("timestamp_utc") or e.get("source_file") or "")

    digest = {
        "digest_ts": __import__("datetime").datetime.now(timezone.utc).isoformat(),
        "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",
        "migrated_by": "scripts/migrate_digest_archive_090.py",
        "latest_probe": None,
        "latest_data_through": (entries[-1].get("data_through") if entries else None),
        "removed_count": 0,
        "total_entries": len(entries),
        "entries": entries,
    }
    # Preserve the latest_probe pointer if the canonical archive had one.
    if CANONICAL.exists():
        try:
            old = json.loads(CANONICAL.read_text())
            digest["latest_probe"] = old.get("latest_probe")
        except Exception:
            pass

    CANONICAL.write_text(json.dumps(digest, indent=2))
    for dp in legacy:
        try:
            dp.unlink()
        except Exception as e:
            print(f"WARN could not remove {dp.name}: {e!r}")

    remaining = list(EVIDENCE_DIR.glob("ironflow_probe_digest_*.json"))
    print(f"migrated {len(legacy)} legacy digest(s) -> {CANONICAL.name} "
          f"({len(entries)} entries); remaining digest files: {len(remaining)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())