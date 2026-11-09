"""Gate 4 v4 EXPLORATORY bootstrap diagnostic summary (deterministic, read-only).

Consumes saved Gate 4 exploratory JSON artifacts (stab/diag/leakage_audit) and
emits a compact, versioned markdown risk table under results/ (dated UTC). NOT
CONFIRMATORY / NOT PROMOTABLE. No network, no recomputation, no real
research_state writes.

No spurious improvement is claimable when CIs are degenerate/invalid or when a
contrast lacks the required diagnostic gates (degenerate==False, ci_valid==True,
inference_ok==True and a finite CI excluding zero).
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

LABEL = "EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE"
RESULTS_DIR = Path("results")


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise ValueError(f"expected JSON object: {path}")
    return obj


def _is_finite_number(x: Any) -> bool:
    try:
        v = float(x)
    except Exception:
        return False
    return v == v and abs(v) != float("inf")


def _ci_excludes_zero(ci: Dict[str, Any]) -> Optional[bool]:
    lo, hi = ci.get("ci_low"), ci.get("ci_high")
    if not _is_finite_number(lo) or not _is_finite_number(hi):
        return None
    lo_f, hi_f = float(lo), float(hi)
    if lo_f > hi_f:
        return None
    return lo_f > 0.0 or hi_f < 0.0


def _as_flags(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if str(x)]
    if isinstance(v, str) and v.strip():
        return [v.strip()]
    return [str(v)]


def extract_contrast_row(source: str, section: str, name: str, ci: Dict[str, Any]) -> Dict[str, Any]:
    eff = ci.get("effective_block_count", ci.get("n_blocks"))
    ci_valid = ci.get("ci_accounting_valid", ci.get("ci_valid"))
    deg = ci.get("degenerate")
    inf = ci.get("inference_ok")
    flags = _as_flags(ci.get("regime_flags"))
    missing_diag = any(k not in ci for k in ("degenerate", "inference_ok")) or (
        "ci_accounting_valid" not in ci and "ci_valid" not in ci
    )
    if missing_diag:
        flags = flags + ["MISSING_DIAGNOSTIC_FIELDS"]
    excludes = _ci_excludes_zero(ci)
    gates_ok = deg is False and ci_valid is True and inf is True and excludes is True
    claimable = bool(gates_ok)
    if excludes is True and not gates_ok:
        flags = flags + ["EXCLUDES_ZERO_NOT_CLAIMABLE"]
    if deg is True or ci_valid is False or inf is False:
        flags = flags + ["NO_CLAIMABLE_IMPROVEMENT"]
    return {
        "source": source,
        "section": section,
        "contrast": name,
        "point": ci.get("point"),
        "ci_low": ci.get("ci_low"),
        "ci_high": ci.get("ci_high"),
        "n_obs": ci.get("n_obs", ci.get("n_obs_finite")),
        "eff_blocks": eff,
        "ci_valid": ci_valid,
        "regime_flags": sorted(set(flags)),
        "degenerate": deg,
        "inference_ok": inf,
        "ci_excludes_zero": excludes,
        "non_degenerate_excludes_zero_claimable": claimable,
        "missing_diagnostic_fields": missing_diag,
    }


def _iter_contrast_dict(container: Any, source: str, section: str) -> Iterable[Dict[str, Any]]:
    if not isinstance(container, dict):
        return []
    out = []
    for name, ci in container.items():
        if isinstance(ci, dict) and ("ci_low" in ci or "point" in ci):
            out.append(extract_contrast_row(source, section, str(name), ci))
    return out


def summarize_stab(path: Path, obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    variants = obj.get("variants") or {}
    if isinstance(variants, dict):
        for vname, vobj in variants.items():
            if not isinstance(vobj, dict):
                continue
            rows.extend(_iter_contrast_dict(vobj.get("contrasts_vs_A") or {}, path.name, f"{vname}.contrasts_vs_A"))
    rows.extend(_iter_contrast_dict(obj.get("loo_e_vs_a_v3") or {}, path.name, "loo_e_vs_a_v3"))
    return rows


def summarize_diag(path: Path, obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for key in ("pooled_contrasts_vs_A_primary_fit", "pooled_contrasts_vs_A_stabilized_exploratory"):
        rows.extend(_iter_contrast_dict(obj.get(key) or {}, path.name, key))
    loo = obj.get("instrument_loo_E_vs_A_exploratory")
    rows.extend(_iter_contrast_dict(loo or {}, path.name, "instrument_loo_E_vs_A_exploratory"))
    return rows


def summarize_leakage_audit(path: Path, obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    rep = obj.get("block_bootstrap_reproducibility") or {}
    if not isinstance(rep, dict):
        return rows
    for run_key in ("run1", "run2"):
        run = rep.get(run_key)
        if isinstance(run, dict) and ("ci_low" in run or "point" in run):
            rows.append(extract_contrast_row(path.name, f"block_bootstrap_reproducibility.{run_key}", "E_vs_A_probe", run))
    for dkey in ("run1_diagnostics", "run2_diagnostics"):
        d = rep.get(dkey)
        if isinstance(d, dict):
            # diagnostics-only rows: no CI; never claimable
            rows.append({
                "source": path.name,
                "section": f"block_bootstrap_reproducibility.{dkey}",
                "contrast": "diagnostics",
                "point": None, "ci_low": None, "ci_high": None,
                "n_obs": d.get("n_obs_finite"),
                "eff_blocks": d.get("effective_block_count"),
                "ci_valid": d.get("ci_accounting_valid"),
                "regime_flags": _as_flags(d.get("regime_flags")),
                "degenerate": d.get("degenerate"),
                "inference_ok": d.get("inference_ok"),
                "ci_excludes_zero": None,
                "non_degenerate_excludes_zero_claimable": False,
                "missing_diagnostic_fields": False,
            })
    return rows


def summarize_artifacts(paths: Sequence[Path]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in paths:
        obj = _load_json(path)
        name = path.name
        if "gate4_v4_exploratory_stab" in name or "variants" in obj and "loo_e_vs_a_v3" in obj:
            rows.extend(summarize_stab(path, obj))
        elif "gate4_v4_exploratory_diag" in name or "pooled_contrasts_vs_A_primary_fit" in obj:
            rows.extend(summarize_diag(path, obj))
        elif "gate4_v4_leakage_audit" in name or "block_bootstrap_reproducibility" in obj:
            rows.extend(summarize_leakage_audit(path, obj))
        else:
            # best-effort: scan for contrast-like dicts at top-level
            for k, v in obj.items():
                rows.extend(_iter_contrast_dict(v, name, k))
    return rows


def _fmt(v: Any) -> str:
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:.6g}"
    if isinstance(v, list):
        return ",".join(str(x) for x in v) if v else "ok"
    return str(v)


def render_markdown(rows: Sequence[Dict[str, Any]], artifacts: Sequence[Path], ts: Optional[str] = None) -> str:
    ts = ts or _ts()
    claimable = [r for r in rows if r.get("non_degenerate_excludes_zero_claimable")]
    degenerate = [r for r in rows if r.get("degenerate") is True or r.get("ci_valid") is False or r.get("inference_ok") is False]
    missing = [r for r in rows if r.get("missing_diagnostic_fields")]
    lines = [
        f"# Gate 4 v4 bootstrap diagnostic summary ({ts})",
        "",
        f"**{LABEL}**",
        "",
        "Deterministic summary of saved exploratory JSON artifacts. No recomputation, no network, no confirmatory claim, no promotion.",
        "A non-degenerate CI excluding zero is claimable **only** when `degenerate=false`, `ci_valid=true`, and `inference_ok=true`.",
        "",
        "## Artifacts consumed",
        "",
    ]
    for p in artifacts:
        lines.append(f"- `{p.as_posix()}`")
    lines += [
        "",
        "## Risk table",
        "",
        "| source | section | contrast | point | ci_low | ci_high | eff_blocks | ci_valid | regime_flags | degenerate | inference_ok | excludes_zero | claimable_excludes_zero |",
        "|---|---|---|---:|---:|---:|---:|:---:|---|:---:|:---:|:---:|:---:|",
    ]
    for r in rows:
        lines.append(
            "| {source} | {section} | {contrast} | {point} | {ci_low} | {ci_high} | {eff_blocks} | {ci_valid} | {regime_flags} | {degenerate} | {inference_ok} | {excludes_zero} | {claimable} |".format(
                source=_fmt(r.get("source")), section=_fmt(r.get("section")), contrast=_fmt(r.get("contrast")),
                point=_fmt(r.get("point")), ci_low=_fmt(r.get("ci_low")), ci_high=_fmt(r.get("ci_high")),
                eff_blocks=_fmt(r.get("eff_blocks")), ci_valid=_fmt(r.get("ci_valid")),
                regime_flags=_fmt(r.get("regime_flags")), degenerate=_fmt(r.get("degenerate")),
                inference_ok=_fmt(r.get("inference_ok")), excludes_zero=_fmt(r.get("ci_excludes_zero")),
                claimable=_fmt(r.get("non_degenerate_excludes_zero_claimable")),
            )
        )
    lines += [
        "",
        "## Decision guardrails (EXPLORATORY)",
        "",
        f"- contrasts with non-degenerate CI excluding zero (claimable): **{len(claimable)}**" + (" — " + ", ".join(f"`{r['source']}::{r['section']}::{r['contrast']}`" for r in claimable) if claimable else ""),
        f"- contrasts with degenerate/invalid/inference-not-ok risk: **{len(degenerate)}**",
        f"- contrasts missing diagnostic fields (treated as not claimable): **{len(missing)}**",
        "- If claimable count is 0, **no spurious improvement is claimable** from these artifacts.",
        "- These artifacts remain **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**; they do not change prereg A–E contrasts, estimands, or confirmatory status.",
        "",
    ]
    return "\n".join(lines)


def default_artifact_paths(repo_root: Path) -> List[Path]:
    candidates = []
    for pat in [
        "research_state/gate4_v4_exploratory_stab/*.json",
        "research_state/gate4_v4_exploratory_diag/*.json",
        "research_state/gate4_v4_leakage_audit/*.json",
    ]:
        candidates.extend(sorted(repo_root.glob(pat)))
    # prefer newest per directory family by name
    by_dir: Dict[str, Path] = {}
    for p in candidates:
        by_dir[p.parent.as_posix() + "::" + p.name.split("_202")[0]] = p
    return sorted(by_dir.values())


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Gate 4 v4 EXPLORATORY bootstrap diagnostic summary")
    ap.add_argument("--artifacts", nargs="*", help="JSON artifact paths (default: latest stab/diag/leakage_audit)")
    ap.add_argument("--out", help="Output markdown path (default: results/gate4_v4_bootstrap_diagnostic_summary_<UTC>.md)")
    ap.add_argument("--repo-root", default=".", help="Repo root for default artifact discovery")
    args = ap.parse_args(argv)
    root = Path(args.repo_root).resolve()
    artifacts = [Path(p) if Path(p).is_absolute() else (root / p) for p in (args.artifacts or [])]
    if not artifacts:
        artifacts = default_artifact_paths(root)
    if not artifacts:
        print("no Gate 4 v4 exploratory artifacts found", file=sys.stderr)
        return 2
    ts = _ts()
    rows = summarize_artifacts(artifacts)
    md = render_markdown(rows, artifacts, ts=ts)
    out = Path(args.out) if args.out else (root / RESULTS_DIR / f"gate4_v4_bootstrap_diagnostic_summary_{ts}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out} rows={len(rows)} claimable_excludes_zero={sum(1 for r in rows if r.get('non_degenerate_excludes_zero_claimable'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
