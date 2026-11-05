"""Track A admissible liquidation ingestion/manifest seam (stdlib-only, FCLR-NEXT-107).

Pre-wires an Ironflow month>=2026-11 admissibility boundary for the liquidation-risk
resume path. Enforces Hyperliquid-only provenance, observed-liquidation label semantics,
fail-closed schema/gap/leakage guards, and no observed/modeled conflation. No network.
No pandas/numpy dependency; safe to import in minimal environments and tests.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

# Canonical Hyperliquid/Ironflow venue identity (Track A only).
ALLOWED_VENUES = {"hyperliquid", "hl", "ironflow_hyperliquid"}
REQUIRED_ROLES = ("events", "fills")
MONTH_RE = re.compile(r"^(?P<y>\d{4})-(?P<m>0[1-9]|1[0-2])$")
TRIGGER_MONTH = "2026-11"  # first month that can satisfy resume trigger (>= 2026-11)

REQUIRED_EVENT_FIELDS = {"timestamp", "symbol"}
# liquidations must carry notional/size/value-like field and must not be modeled/proxy.
LIQUIDATION_VALUE_FIELDS = {"liquidation_notional", "notional_usd", "notional", "usd_size", "size", "closed_pnl"}
FORBIDDEN_SCHEMA_COLUMNS = {
    "modeled", "proxy", "liquidation_estimate", "estimated_liquidation",
    "synthetic_liquidation", "simulated_liquidation", "model_liquidation",
    "is_modeled", "is_proxy", "is_estimate", "liquidation_proxy", "breach_proxy",
    "predicted_liquidation", "forecast_liquidation",
}

IRONFLOW_RESUME_URL_RE = re.compile(
    r"https://huggingface\.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/(events|fills)/(?P<month>\d{4}-\d{2})\.parquet$"
)


def month_gte(a: str, b: str) -> bool:
    """Return True if YYYY-MM month a >= b (fail-closed on malformed)."""
    ma, mb = MONTH_RE.match(a or ""), MONTH_RE.match(b or "")
    if not ma or not mb:
        return False
    return (int(ma.group("y")), int(ma.group("m"))) >= (int(mb.group("y")), int(mb.group("m")))


def normalize_month(value: Any) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip()
    m = MONTH_RE.match(s)
    return f"{m.group('y')}-{m.group('m')}" if m else None


def _forbidden_hits(fields: Iterable[Any]) -> List[str]:
    s = {str(f).strip().lower() for f in (fields or []) if f is not None and str(f).strip()}
    return sorted(c for c in FORBIDDEN_SCHEMA_COLUMNS if c in s)


def build_ironflow_month_manifest(
    *,
    month: str,
    venue: str = "hyperliquid",
    source: str = "ironflow/hyperliquid-liquidations",
    events_path: Optional[str] = None,
    fills_path: Optional[str] = None,
    events_url: Optional[str] = None,
    fills_url: Optional[str] = None,
    observed_liquidations: bool = True,
    modeled_or_proxy: bool = False,
    merges_non_hyperliquid: bool = False,
    unauthenticated: bool = True,
    requires_api_key: bool = False,
    requires_signature: bool = False,
    label_definition: str = "observed_hyperliquid_liquidation_event_rows_from_ironflow",
    timestamp_normalized_utc: bool = True,
    schema_fields_events: Optional[Sequence[str]] = None,
    schema_fields_fills: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """Build a machine-readable, fail-closed-checkable manifest for one Ironflow month."""
    return {
        "track": "A",
        "source_family": "ironflow_hyperliquid_liquidations",
        "venue": venue,
        "source": source,
        "month": month,
        "unauthenticated": unauthenticated,
        "requires_api_key": requires_api_key,
        "requires_signature": requires_signature,
        "observed_liquidations": observed_liquidations,
        "modeled_or_proxy": modeled_or_proxy,
        "merges_non_hyperliquid": merges_non_hyperliquid,
        "label_definition": label_definition,
        "timestamp_normalized_utc": timestamp_normalized_utc,
        "artifacts": {
            "events": {"path": events_path, "url": events_url, "schema_fields": list(schema_fields_events or [])},
            "fills": {"path": fills_path, "url": fills_url, "schema_fields": list(schema_fields_fills or [])},
        },
    }


def _check_role_artifact(role: str, art: Dict[str, Any], failures: List[str], *, require_local_path: bool) -> None:
    path = art.get("path")
    url = art.get("url")
    if require_local_path and not (isinstance(path, str) and path.strip()):
        failures.append(f"{role}_path_missing")
    if isinstance(path, str) and path.strip():
        p = Path(path)
        # fail-closed on obviously unsafe/path-traversal-ish resolved escapes is caller concern;
        # here enforce non-empty local file existence is NOT checked (no IO in manifest-only mode).
        if not p.name.endswith(".parquet"):
            failures.append(f"{role}_path_not_parquet")
        # role evidence may appear in filename or parent dirs (e.g. data/events/2026-11.parquet);
        # fail-closed only when path contains the *other* role token, indicating a swap/mismatch.
        low_path = str(p).replace("\\", "/").lower()
        other = "fills" if role == "events" else "events"
        if f"/{other}/" in f"/{low_path}/" or low_path.endswith(f"/{other}.parquet"):
            failures.append(f"{role}_path_role_mismatch")
    if isinstance(url, str) and url.strip():
        m = IRONFLOW_RESUME_URL_RE.match(url.strip())
        if not m:
            failures.append(f"{role}_url_not_admissible_ironflow")
        elif m.group(1) != role:
            failures.append(f"{role}_url_role_mismatch")
    fields = art.get("schema_fields") or []
    if fields:
        low = {str(f).strip().lower() for f in fields}
        hits = _forbidden_hits(fields)
        if hits:
            failures.append(f"{role}_forbidden_columns:{','.join(hits)}")
        if not (REQUIRED_EVENT_FIELDS & low):
            failures.append(f"{role}_missing_required_identity_fields")
        if role == "events" and not (LIQUIDATION_VALUE_FIELDS & low):
            failures.append(f"{role}_missing_liquidation_value_field")


def validate_ironflow_month_manifest(
    manifest: Dict[str, Any],
    *,
    min_trigger_month: Optional[str] = TRIGGER_MONTH,
    require_local_paths: bool = False,
    require_urls: bool = False,
) -> Dict[str, Any]:
    """Fail-closed admissibility validation for an Ironflow month manifest.

    Does not read parquet contents or perform network IO. Validates provenance,
    Hyperliquid-only/observed semantics, month format/trigger threshold, required
    events+fills artifacts, and anti-conflation schema guards.
    """
    failures: List[str] = []
    m = manifest or {}
    month = normalize_month(m.get("month"))
    if not month:
        failures.append("month_missing_or_invalid")
    elif min_trigger_month and not month_gte(month, min_trigger_month):
        failures.append(f"month_below_trigger:{month}<{min_trigger_month}")

    venue = str(m.get("venue") or "").strip().lower()
    if venue not in ALLOWED_VENUES:
        failures.append("venue_not_hyperliquid_only")

    source = str(m.get("source") or "").strip().lower()
    if "ironflow" not in source or "hyperliquid" not in source:
        failures.append("source_not_ironflow_hyperliquid")

    if not m.get("unauthenticated", False):
        failures.append("not_unauthenticated")
    for k in ("requires_api_key", "requires_signature", "modeled_or_proxy", "merges_non_hyperliquid"):
        if m.get(k) is True:
            failures.append(k)

    if m.get("observed_liquidations") is not True:
        failures.append("observed_liquidations_not_true")
    if not str(m.get("label_definition") or "").strip():
        failures.append("label_definition_missing")
    else:
        ld = str(m.get("label_definition")).lower()
        if any(tok in ld for tok in ("modeled", "proxy", "synthetic", "estimated", "simulated", "forecast")):
            failures.append("label_definition_conflates_modeled")

    if m.get("timestamp_normalized_utc") is not True:
        failures.append("timestamp_not_normalized_utc")

    artifacts = m.get("artifacts") or {}
    if not isinstance(artifacts, dict):
        failures.append("artifacts_missing")
        artifacts = {}
    for role in REQUIRED_ROLES:
        art = artifacts.get(role)
        if not isinstance(art, dict):
            failures.append(f"{role}_artifact_missing")
            continue
        _check_role_artifact(role, art, failures, require_local_path=require_local_paths)
        if require_urls and not (isinstance(art.get("url"), str) and art.get("url", "").strip()):
            failures.append(f"{role}_url_missing")
        # if url present, month in url must match manifest month
        url = art.get("url")
        if month and isinstance(url, str) and url.strip():
            mu = IRONFLOW_RESUME_URL_RE.match(url.strip())
            if mu and mu.group("month") != month:
                failures.append(f"{role}_url_month_mismatch")

    verdict = "GO" if not failures else "NO-GO"
    return {
        "track": "A",
        "verdict": verdict,
        "pass": verdict == "GO",
        "fail_closed": True,
        "month": month,
        "min_trigger_month": min_trigger_month,
        "failures": sorted(set(failures)),
        "guards": {
            "hyperliquid_only": True,
            "observed_only": True,
            "no_modeled_conflation": True,
            "no_network": True,
            "required_roles": list(REQUIRED_ROLES),
        },
    }


def assess_ironflow_month_admissibility(
    manifest: Dict[str, Any],
    *,
    for_resume_trigger: bool = True,
    require_local_paths: bool = False,
    require_urls: bool = False,
) -> Dict[str, Any]:
    """Public seam used by ingestion/resume code before loading outcomes/data."""
    min_trigger = TRIGGER_MONTH if for_resume_trigger else None
    return validate_ironflow_month_manifest(
        manifest,
        min_trigger_month=min_trigger,
        require_local_paths=require_local_paths,
        require_urls=require_urls,
    )


def month_from_ironflow_path(path_or_url: str) -> Optional[str]:
    if not path_or_url:
        return None
    m = re.search(r"(\d{4}-\d{2})\.parquet$", str(path_or_url).strip())
    return m.group(1) if m else None
