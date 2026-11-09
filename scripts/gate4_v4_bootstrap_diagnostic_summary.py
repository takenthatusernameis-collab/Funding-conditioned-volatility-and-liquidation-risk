"""Gate 4 v4 EXPLORATORY bootstrap diagnostic summary (deterministic, read-only).

Consumes saved Gate 4 exploratory JSON artifacts (stab/diag/leakage_audit) and
emits a compact, versioned markdown risk table under results/ (dated UTC). NOT
CONFIRMATORY / NOT PROMOTABLE. No network, no recomputation, no real
research_state writes.

No spurious improvement is claimable when CIs are degenerate/invalid or when a
contrast lacks the required diagnostic gates (degenerate==False, ci_valid==True,
inference_ok==True and a finite CI excluding zero).

Optional --enrich-diagnostics-from-leakage <leakage_json>: read-only. Copies
matching block_bootstrap_reproducibility run/run_diagnostics CI-gate fields into
summary-row computation ONLY for rows that can be unambiguously mapped by exact
context (point, ci_low, ci_high, n_obs, n_blocks/effective basis, block_hours,
seed when present). Ambiguous mappings preserve MISSING_DIAGNOSTIC_FIELDS and
claimable_excludes_zero=false. Source JSONs are never mutated.

Optional --backfill-derivable-diagnostics: read-only. Derives CI-gate diagnostics
from fields already present in each saved contrast row where mathematically and
audibly derivable, and refuses otherwise:
  - effective_block_count := n_blocks (when n_blocks is present and > 0)
  - ci_valid := True (when ci_low, ci_high, point, n_obs are all finite and
    ci_low <= ci_high)
Never infers degenerate / inference_ok from CI width, point, or excludes-zero
alone; those require explicit saved diagnostic evidence. Rows that remain
unproven keep MISSING_DIAGNOSTIC_FIELDS and claimable_excludes_zero=false.
Emits a versioned per-row audit trace (derivation rule, source field path,
applied/refused, refusal reason) and a backfill_rules_version. No source
mutation, no recomputation, no network, no real research_state writes.
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

BACKFILL_RULES_VERSION = "1.0"


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


_ENRICH_FLOAT_KEYS = ("point", "ci_low", "ci_high")
_ENRICH_INT_KEYS = ("n_obs", "n_blocks", "block_hours", "seed", "n_reps")
_ENRICH_DIAG_KEYS = (
    "ci_accounting_valid", "ci_valid", "effective_block_count",
    "degenerate", "inference_ok", "regime_flags", "n_reps_effective", "n_obs_finite",
)


def _float_close(a: Any, b: Any, *, rel: float = 1e-12, abs_: float = 1e-15) -> bool:
    if not _is_finite_number(a) or not _is_finite_number(b):
        return False
    af, bf = float(a), float(b)
    scale = max(abs(af), abs(bf), 1.0)
    return abs(af - bf) <= max(abs_, rel * scale)


def _enrich_context_match(row_ci: Dict[str, Any], cand: Dict[str, Any]) -> bool:
    """Unambiguous only when all comparable context keys match exactly (within float tol).

    Requires candidate to have CI identity (point/ci_low/ci_high) so it can map to a
    contrast CI row. Refuses (returns False) when no comparable key is shared or when
    any shared comparable key disagrees.
    """
    if not all(k in cand for k in _ENRICH_FLOAT_KEYS):
        return False
    compared = 0
    for k in _ENRICH_FLOAT_KEYS:
        if k in row_ci and k in cand:
            if not _float_close(row_ci[k], cand[k]):
                return False
            compared += 1
    for k in _ENRICH_INT_KEYS:
        if k in row_ci and k in cand and row_ci[k] is not None and cand[k] is not None:
            try:
                if int(row_ci[k]) != int(cand[k]):
                    return False
                compared += 1
            except Exception:
                if str(row_ci[k]) != str(cand[k]):
                    return False
                compared += 1
    # require at least CI identity + one sizing key to avoid vacuous matches
    return compared >= 4


def backfill_derivable_diagnostics(ci: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Derive only provably-deducible CI-gate diagnostics from fields already in the row.

    Derivable (never mutates `ci`):
      - effective_block_count := n_blocks  when n_blocks present and > 0
      - ci_valid := True                   when ci_low, ci_high, point, n_obs are all
                                            finite and ci_low <= ci_high
    Never infers:
      - degenerate / inference_ok from CI width, point, or excludes-zero alone;
        those require explicit saved diagnostic evidence in the same artifact.
    Returns (copy, trace_entries). Each trace entry has keys:
      field, rule, source_field, applied, value, refusal_reason.
    """
    out = dict(ci)
    trace: List[Dict[str, Any]] = []

    def entry(field: str, rule: str, source_field: Optional[str], applied: bool,
              value: Any = None, refusal_reason: Optional[str] = None) -> None:
        trace.append({
            "field": field,
            "rule": rule,
            "source_field": source_field,
            "applied": bool(applied),
            "value": value,
            "refusal_reason": refusal_reason,
        })

    missing_diag = any(k not in ci for k in ("degenerate", "inference_ok")) or (
        "ci_accounting_valid" not in ci and "ci_valid" not in ci
    )

    if "effective_block_count" not in ci:
        nb = ci.get("n_blocks")
        if nb is None:
            entry("effective_block_count", "effective_block_count_from_n_blocks", "n_blocks", False,
                  refusal_reason="n_blocks_missing")
        else:
            try:
                nbi = int(nb)
            except Exception:
                entry("effective_block_count", "effective_block_count_from_n_blocks", "n_blocks", False,
                      refusal_reason="n_blocks_not_integer")
            else:
                if nbi > 0:
                    out["effective_block_count"] = nbi
                    entry("effective_block_count", "effective_block_count_from_n_blocks", "n_blocks", True, value=nbi)
                else:
                    entry("effective_block_count", "effective_block_count_from_n_blocks", "n_blocks", False,
                          refusal_reason="n_blocks_not_positive")

    if "ci_accounting_valid" not in ci and "ci_valid" not in ci:
        lo, hi = ci.get("ci_low"), ci.get("ci_high")
        pt = ci.get("point")
        nobs = ci.get("n_obs")
        finite = _is_finite_number(lo) and _is_finite_number(hi) and _is_finite_number(pt) and _is_finite_number(nobs)
        if not finite:
            entry("ci_valid", "ci_valid_from_finite_ordered_ci", "ci_low,ci_high,point,n_obs", False,
                  refusal_reason="ci_or_point_or_n_obs_not_finite")
        else:
            lo_f, hi_f = float(lo), float(hi)
            if lo_f <= hi_f:
                out["ci_valid"] = True
                entry("ci_valid", "ci_valid_from_finite_ordered_ci", "ci_low,ci_high,point,n_obs", True, value=True)
            else:
                entry("ci_valid", "ci_valid_from_finite_ordered_ci", "ci_low,ci_high,point,n_obs", False,
                      refusal_reason="ci_low_exceeds_ci_high")

    # degenerate / inference_ok are never inferred from CI geometry
    if "degenerate" not in ci:
        entry("degenerate", "degenerate_from_ci_width", None, False,
              refusal_reason="degenerate_not_inferrable_from_ci_width_or_point")
    if "inference_ok" not in ci:
        entry("inference_ok", "inference_ok_from_explicit_evidence", None, False,
              refusal_reason="inference_ok_not_inferrable_without_explicit_diagnostic_field")

    still_missing = any(k not in out for k in ("degenerate", "inference_ok")) or (
        "ci_accounting_valid" not in out and "ci_valid" not in out
    )
    entry("diagnostic_gates_residual", "residual_missing_diagnostic_fields", None, not still_missing,
          value=not still_missing,
          refusal_reason=None if not still_missing else "degenerate_or_inference_ok_unproven")

    # Only attach trace when the row actually lacked diagnostics; otherwise it is a
    # no-op pass-through with a residual "already_complete" note.
    if not missing_diag:
        trace.insert(0, {
            "field": "diagnostic_gates_residual",
            "rule": "residual_missing_diagnostic_fields",
            "source_field": None,
            "applied": True,
            "value": True,
            "refusal_reason": None,
        })

    return out, trace


def build_enrichment_candidates(leakage_obj: Dict[str, Any], source_name: str) -> List[Dict[str, Any]]:
    rep = leakage_obj.get("block_bootstrap_reproducibility") or {}
    if not isinstance(rep, dict):
        return []
    cands: List[Dict[str, Any]] = []
    for run_key in ("run1", "run2"):
        run = rep.get(run_key)
        if not isinstance(run, dict):
            continue
        diag = rep.get(f"{run_key}_diagnostics")
        if not isinstance(diag, dict):
            diag = {}
        cand = {"_source": source_name, "_run": run_key}
        for k in _ENRICH_FLOAT_KEYS + _ENRICH_INT_KEYS:
            if k in run:
                cand[k] = run[k]
        for k in _ENRICH_DIAG_KEYS:
            if k in run:
                cand[k] = run[k]
            elif k in diag:
                cand[k] = diag[k]
        cands.append(cand)
    return cands


def enrich_contrast_ci(
    ci: Dict[str, Any],
    candidates: Optional[Sequence[Dict[str, Any]]],
) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    """Return (possibly-enriched copy, meta). Never mutates source ci.

    Enrichment applies only when ci is missing diagnostic fields. If 0 or >1 candidates
    match (ambiguous), returns original copy with meta.reason and no diagnostic fill.
    """
    missing_diag = any(k not in ci for k in ("degenerate", "inference_ok")) or (
        "ci_accounting_valid" not in ci and "ci_valid" not in ci
    )
    if not missing_diag or not candidates:
        return dict(ci), None
    matches = [c for c in candidates if _enrich_context_match(ci, c)]
    if len(matches) != 1:
        return dict(ci), {"applied": False, "reason": "AMBIGUOUS_MAPPING", "matches": len(matches)}
    c = matches[0]
    out = dict(ci)
    for k in _ENRICH_DIAG_KEYS:
        if k in c and c[k] is not None:
            out[k] = c[k]
    # verify enrichment actually resolved diagnostic gates; if not, refuse
    still_missing = any(k not in out for k in ("degenerate", "inference_ok")) or (
        "ci_accounting_valid" not in out and "ci_valid" not in out
    )
    if still_missing:
        return dict(ci), {"applied": False, "reason": "AMBIGUOUS_MAPPING", "matches": 1, "insufficient_diag": True}
    return out, {"applied": True, "reason": "UNAMBIGUOUS_MATCH", "matches": 1, "source": c.get("_source"), "run": c.get("_run")}


def extract_contrast_row(source: str, section: str, name: str, ci: Dict[str, Any], *,
                         enrich_meta: Optional[Dict[str, Any]] = None,
                         backfill_trace: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
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
    if enrich_meta and enrich_meta.get("applied"):
        flags = flags + ["ENRICHED_FROM_LEAKAGE"]
    elif enrich_meta and not enrich_meta.get("applied"):
        flags = flags + ["ENRICHMENT_" + str(enrich_meta.get("reason", "REFUSED"))]
    excludes = _ci_excludes_zero(ci)
    gates_ok = deg is False and ci_valid is True and inf is True and excludes is True
    claimable = bool(gates_ok)
    if excludes is True and not gates_ok:
        flags = flags + ["EXCLUDES_ZERO_NOT_CLAIMABLE"]
    if deg is True or ci_valid is False or inf is False:
        flags = flags + ["NO_CLAIMABLE_IMPROVEMENT"]
    row = {
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
        "enrichment_applied": bool(enrich_meta.get("applied")) if enrich_meta else False,
        "enrichment_meta": enrich_meta,
    }
    if backfill_trace:
        row["backfill_trace"] = backfill_trace
    return row


def _iter_contrast_dict(container: Any, source: str, section: str, *,
                        candidates: Optional[Sequence[Dict[str, Any]]] = None,
                        backfill: bool = False) -> Iterable[Dict[str, Any]]:
    if not isinstance(container, dict):
        return []
    out = []
    for name, ci in container.items():
        if isinstance(ci, dict) and ("ci_low" in ci or "point" in ci):
            proc_ci: Dict[str, Any] = ci
            btrace: List[Dict[str, Any]] = []
            if backfill:
                proc_ci, btrace = backfill_derivable_diagnostics(ci)
                for e in btrace:
                    e["row_id"] = f"{source}::{section}::{name}"
            eff_ci, meta = enrich_contrast_ci(proc_ci, candidates)
            out.append(extract_contrast_row(source, section, str(name), eff_ci,
                                            enrich_meta=meta, backfill_trace=btrace or None))
    return out


def summarize_stab(path: Path, obj: Dict[str, Any], *, candidates: Optional[Sequence[Dict[str, Any]]] = None,
                   backfill: bool = False) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    variants = obj.get("variants") or {}
    if isinstance(variants, dict):
        for vname, vobj in variants.items():
            if not isinstance(vobj, dict):
                continue
            rows.extend(_iter_contrast_dict(vobj.get("contrasts_vs_A") or {}, path.name, f"{vname}.contrasts_vs_A",
                                            candidates=candidates, backfill=backfill))
    rows.extend(_iter_contrast_dict(obj.get("loo_e_vs_a_v3") or {}, path.name, "loo_e_vs_a_v3",
                                    candidates=candidates, backfill=backfill))
    return rows


def summarize_diag(path: Path, obj: Dict[str, Any], *, candidates: Optional[Sequence[Dict[str, Any]]] = None,
                   backfill: bool = False) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for key in ("pooled_contrasts_vs_A_primary_fit", "pooled_contrasts_vs_A_stabilized_exploratory"):
        rows.extend(_iter_contrast_dict(obj.get(key) or {}, path.name, key, candidates=candidates, backfill=backfill))
    loo = obj.get("instrument_loo_E_vs_A_exploratory")
    rows.extend(_iter_contrast_dict(loo or {}, path.name, "instrument_loo_E_vs_A_exploratory", candidates=candidates, backfill=backfill))
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


def summarize_artifacts(paths: Sequence[Path], *, enrichment_candidates: Optional[Sequence[Dict[str, Any]]] = None,
                        backfill: bool = False) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in paths:
        obj = _load_json(path)
        name = path.name
        if "gate4_v4_exploratory_stab" in name or "variants" in obj and "loo_e_vs_a_v3" in obj:
            rows.extend(summarize_stab(path, obj, candidates=enrichment_candidates, backfill=backfill))
        elif "gate4_v4_exploratory_diag" in name or "pooled_contrasts_vs_A_primary_fit" in obj:
            rows.extend(summarize_diag(path, obj, candidates=enrichment_candidates, backfill=backfill))
        elif "gate4_v4_leakage_audit" in name or "block_bootstrap_reproducibility" in obj:
            rows.extend(summarize_leakage_audit(path, obj))
        else:
            # best-effort: scan for contrast-like dicts at top-level
            for k, v in obj.items():
                rows.extend(_iter_contrast_dict(v, name, k, candidates=enrichment_candidates, backfill=backfill))
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


def render_markdown(
    rows: Sequence[Dict[str, Any]],
    artifacts: Sequence[Path],
    ts: Optional[str] = None,
    *,
    enrichment_source: Optional[Path] = None,
    enrichment_candidates: Optional[Sequence[Dict[str, Any]]] = None,
    backfill_trace: Optional[Sequence[Dict[str, Any]]] = None,
    backfill_mode: bool = False,
) -> str:
    ts = ts or _ts()
    claimable = [r for r in rows if r.get("non_degenerate_excludes_zero_claimable")]
    degenerate = [r for r in rows if r.get("degenerate") is True or r.get("ci_valid") is False or r.get("inference_ok") is False]
    missing = [r for r in rows if r.get("missing_diagnostic_fields")]
    enriched = [r for r in rows if r.get("enrichment_applied")]
    enrich_refused = [r for r in rows if r.get("enrichment_meta") and not r["enrichment_meta"].get("applied")]
    lines = [
        f"# Gate 4 v4 bootstrap diagnostic summary ({ts})",
        "",
        f"**{LABEL}**",
        "",
        "Deterministic summary of saved exploratory JSON artifacts. No recomputation, no network, no confirmatory claim, no promotion.",
        "A non-degenerate CI excluding zero is claimable **only** when `degenerate=false`, `ci_valid=true`, and `inference_ok=true`.",
        "",
    ]
    if enrichment_source is not None:
        lines += [
            "## Diagnostic enrichment (read-only; does not mutate source artifacts)",
            "",
            f"- enrichment source: `{enrichment_source.as_posix()}` (block_bootstrap_reproducibility candidates: {len(enrichment_candidates or [])})",
            f"- rows enriched by unambiguous exact-context match: **{len(enriched)}**",
            f"- rows with enrichment refused/ambiguous (kept MISSING_DIAGNOSTIC_FIELDS, not claimable): **{len(enrich_refused)}**",
            "- Enrichment copies CI-gate fields only for unambiguous matches; it never recomputes outcomes and never fabricates improvement.",
            "",
        ]
    if backfill_mode and backfill_trace is not None:
        applied = [e for e in backfill_trace if e.get("applied")]
        refused = [e for e in backfill_trace if not e.get("applied")]
        lines += [
            "",
            "## Diagnostic backfill audit trace (read-only; no source mutation)",
            "",
            f"- backfill_rules_version: `{BACKFILL_RULES_VERSION}`",
            "- derivable fields only: `effective_block_count` (from `n_blocks` > 0), `ci_valid` (from finite ordered "
            "CI `ci_low <= ci_high` + finite `point`/`n_obs`)",
            "- never inferred: `degenerate`, `inference_ok` (require explicit saved diagnostic evidence); "
            "backfilled fields alone never make a row claimable",
            f"- trace entries: **{len(backfill_trace)}** | fields backfilled (applied): **{len(applied)}** | "
            f"fields refused (not derivable): **{len(refused)}**",
            "",
        ]
        shown = 0
        for e in backfill_trace:
            if shown >= 200:
                lines.append(f"- ... ({len(backfill_trace) - shown} further trace entries omitted for brevity)")
                break
            lines.append(
                f"- `{e.get('row_id')}` | field={e.get('field')} | rule={e.get('rule')} | "
                f"applied={_fmt(e.get('applied'))} | source={_fmt(e.get('source_field'))} | "
                f"value={_fmt(e.get('value'))} | refusal={_fmt(e.get('refusal_reason'))}"
            )
            shown += 1
        lines += [
            "",
            "Claimability remains governed by degenerate==false, ci_valid==true, inference_ok==true and a finite CI "
            "excluding zero. Backfilled `ci_valid`/`effective_block_count` alone never make a row claimable while "
            "`degenerate`/`inference_ok` are unproven; such rows keep MISSING_DIAGNOSTIC_FIELDS and "
            "claimable_excludes_zero=false.",
            "",
        ]
    lines += [
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
        "research_state/gate4_v4_exploratory_leakage_audit/*.json",
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
    ap.add_argument(
        "--enrich-diagnostics-from-leakage",
        help="Read-only leakage audit JSON path; copies CI-gate fields only for unambiguous exact-context matches (never mutates source artifacts).",
    )
    ap.add_argument(
        "--backfill-derivable-diagnostics",
        action="store_true",
        help="Derive CI-gate diagnostics from fields already present in each saved contrast row where provably "
        "derivable (effective_block_count from n_blocks>0; ci_valid from finite ordered CI + finite point/n_obs). "
        "Never infers degenerate/inference_ok. Emits a versioned per-row audit trace; results/ output only.",
    )
    ap.add_argument(
        "--audit-trace",
        action="store_true",
        help="Include the full per-row diagnostic backfill audit trace section in the report (implied by "
        "--backfill-derivable-diagnostics).",
    )
    args = ap.parse_args(argv)
    root = Path(args.repo_root).resolve()
    artifacts = [Path(p) if Path(p).is_absolute() else (root / p) for p in (args.artifacts or [])]
    if not artifacts:
        artifacts = default_artifact_paths(root)
    if not artifacts:
        print("no Gate 4 v4 exploratory artifacts found", file=sys.stderr)
        return 2
    enrich_path: Optional[Path] = None
    candidates: Optional[List[Dict[str, Any]]] = None
    if args.enrich_diagnostics_from_leakage:
        enrich_path = Path(args.enrich_diagnostics_from_leakage)
        if not enrich_path.is_absolute():
            enrich_path = root / enrich_path
        if not enrich_path.exists():
            print(f"enrichment leakage JSON not found: {enrich_path}", file=sys.stderr)
            return 2
        candidates = build_enrichment_candidates(_load_json(enrich_path), enrich_path.name)
    ts = _ts()
    backfill_mode = bool(args.backfill_derivable_diagnostics)
    rows = summarize_artifacts(artifacts, enrichment_candidates=candidates, backfill=backfill_mode)
    backfill_trace: List[Dict[str, Any]] = []
    for r in rows:
        bt = r.get("backfill_trace")
        if isinstance(bt, list):
            backfill_trace.extend(bt)
    md = render_markdown(rows, artifacts, ts=ts, enrichment_source=enrich_path,
                         enrichment_candidates=candidates, backfill_trace=backfill_trace,
                         backfill_mode=(backfill_mode or args.audit_trace))
    if args.out:
        out = Path(args.out)
    elif backfill_mode:
        out = root / RESULTS_DIR / f"gate4_v4_bootstrap_diagnostic_summary_backfill_{ts}.md"
    else:
        out = root / RESULTS_DIR / f"gate4_v4_bootstrap_diagnostic_summary_{ts}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    enriched_n = sum(1 for r in rows if r.get("enrichment_applied"))
    bf_applied = sum(1 for e in backfill_trace if e.get("applied"))
    bf_refused = sum(1 for e in backfill_trace if not e.get("applied"))
    print(f"wrote {out} rows={len(rows)} claimable_excludes_zero={sum(1 for r in rows if r.get('non_degenerate_excludes_zero_claimable'))} "
          f"enriched={enriched_n} backfill_applied={bf_applied} backfill_refused={bf_refused}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
