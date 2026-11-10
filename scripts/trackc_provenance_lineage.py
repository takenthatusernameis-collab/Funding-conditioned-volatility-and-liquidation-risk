#!/usr/bin/env python3
"""Local-only provenance lineage ingestion/verification for Track C artifacts.

Deterministic, stdlib-only, NO NETWORK, NO OUTCOMES.
Ingests local manifest metadata (manifest_extended.json, manifest_extract.json)
and verifies file content hashes where mapping is unambiguous. Adjacent
<file>.sha256 sidecars remain supported.

Does not fabricate provenance: URL/manifest presence alone is not sufficient
without a content hash match for the specific file.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MANIFEST_CANDIDATES = (
    Path("research_state/data_cache/manifest_extended.json"),
    Path("research_state/data_cache/manifest_extract.json"),
)


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _resolve(repo_root: Path, raw: str) -> Path | None:
    try:
        p = Path(raw)
        if not p.is_absolute():
            p = (repo_root / p).resolve()
        else:
            p = p.resolve()
        return p
    except Exception:
        return None


def load_manifest_indexes(repo_root: Path, manifest_paths=None):
    """Build hash indexes from local manifests. Returns (by_path_hash, stats)."""
    repo_root = Path(repo_root).resolve()
    by_path: dict[Path, dict] = {}
    stats = {"manifests_loaded": [], "manifests_missing": [], "records_indexed": 0}
    candidates = list(manifest_paths) if manifest_paths else [repo_root / c for c in MANIFEST_CANDIDATES]
    for mp in candidates:
        try:
            mp = Path(mp)
            if not mp.exists():
                stats["manifests_missing"].append(str(mp))
                continue
            data = json.loads(mp.read_text())
            stats["manifests_loaded"].append(str(mp))
        except Exception:
            stats["manifests_missing"].append(str(mp))
            continue
        # manifest_extended style: records[] with path+sha256
        for rec in data.get("records", []) if isinstance(data, dict) else []:
            raw = rec.get("path") or rec.get("file") or rec.get("zip")
            sha = rec.get("sha256") or rec.get("zip_sha256")
            if not raw or not sha:
                continue
            rp = _resolve(repo_root, str(raw))
            if not rp:
                continue
            sha = str(sha).strip().lower().split()[0]
            # keep first; manifests should agree
            if rp not in by_path:
                by_path[rp] = {"sha256": sha, "source": mp.name, "type": "manifest_record"}
                stats["records_indexed"] += 1
    return by_path, stats


def verify_file(p: Path, repo_root: Path | None = None, manifest_index: dict | None = None):
    """Verify one file via adjacent sidecar or manifest hash. Returns record dict."""
    p = Path(p)
    try:
        rp = p.resolve()
    except Exception:
        rp = p
    # 1) adjacent sidecar
    sc = Path(str(rp) + ".sha256")
    if not sc.exists():
        alt = rp.with_suffix(rp.suffix + ".sha256")
        if alt.exists():
            sc = alt
    if sc.exists():
        try:
            expected = sc.read_text(errors="ignore").strip().split()[0].lower()
            got = _sha256_file(rp)
            if expected and got == expected:
                return {"file": str(rp), "status": "verified", "source": "adjacent_sidecar", "sha256": got}
            return {
                "file": str(rp),
                "status": "mismatch",
                "source": "adjacent_sidecar",
                "expected_prefix": expected[:16],
                "got_prefix": got[:16],
            }
        except Exception as e:
            return {"file": str(rp), "status": "error", "source": "adjacent_sidecar", "error": str(e)[:120]}
    # 2) manifest hash (unambiguous path+hash match)
    if manifest_index is not None:
        rec = manifest_index.get(rp)
        if rec and rec.get("sha256"):
            try:
                expected = rec["sha256"]
                got = _sha256_file(rp)
                if got == expected:
                    return {
                        "file": str(rp),
                        "status": "verified",
                        "source": f"manifest:{rec.get('source', 'unknown')}",
                        "sha256": got,
                    }
                return {
                    "file": str(rp),
                    "status": "mismatch",
                    "source": f"manifest:{rec.get('source', 'unknown')}",
                    "expected_prefix": expected[:16],
                    "got_prefix": got[:16],
                }
            except Exception as e:
                return {"file": str(rp), "status": "error", "source": "manifest", "error": str(e)[:120]}
    return {"file": str(rp), "status": "unmapped", "source": "none"}


def verify_paths(paths, repo_root: Path | None = None, manifest_index: dict | None = None, limit: int | None = None):
    if limit is not None:
        paths = list(paths)[:limit]
    else:
        paths = list(paths)
    checked = 0
    ok = 0
    mismatches = []
    unmapped = 0
    by_source = {}
    details_ok = []
    for p in paths:
        rec = verify_file(Path(p), repo_root=repo_root, manifest_index=manifest_index)
        st = rec.get("status")
        src = rec.get("source", "none")
        if st == "verified":
            checked += 1
            ok += 1
            by_source[src] = by_source.get(src, 0) + 1
            if len(details_ok) < 10:
                details_ok.append({"file": rec["file"], "source": src, "sha256_prefix": (rec.get("sha256") or "")[:16]})
        elif st == "mismatch":
            checked += 1
            mismatches.append({k: rec.get(k) for k in ("file", "source", "expected_prefix", "got_prefix")})
            by_source[src] = by_source.get(src, 0) + 1
        elif st == "error":
            checked += 1
            mismatches.append({k: rec.get(k) for k in ("file", "source", "error")})
        else:
            unmapped += 1
    verified_all = ok > 0 and ok == len(paths) and len(mismatches) == 0 and unmapped == 0
    return {
        "files_considered": len(paths),
        "verified_count": ok,
        "checked_with_hash_source": checked,
        "mismatch_count": len(mismatches),
        "unmapped_count": unmapped,
        "provenance_verified": verified_all,
        "provenance_source_counts": by_source,
        "verified_samples": details_ok,
        "mismatch_samples": mismatches[:10],
        "verification_note": "Deterministic local check: adjacent *.sha256 sidecars or unambiguous manifest path+sha256 matches (content hash recomputed). No network. URL/manifest presence alone is not treated as verification.",
    }


def verify_paths_with_manifests(paths, repo_root: Path, manifest_paths=None, limit: int | None = None):
    repo_root = Path(repo_root).resolve()
    idx, mstats = load_manifest_indexes(repo_root, manifest_paths=manifest_paths)
    res = verify_paths(paths, repo_root=repo_root, manifest_index=idx, limit=limit)
    res["manifest_ingest"] = mstats
    return res
