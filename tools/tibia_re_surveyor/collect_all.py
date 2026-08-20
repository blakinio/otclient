from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Dict, Iterable, List, Mapping, Sequence


SCHEMA_VERSION = "otclient.tibia-re-surveyor.collect-all.v2"
ALIAS_SCHEMA_VERSION = "otclient.tibia-re-surveyor.alias-view.v2"
TELEMETRY_SCHEMA_VERSION = "otclient.tibia-re-surveyor.telemetry.v2"
MISSING_SCHEMA_VERSION = "otclient.tibia-re-surveyor.missing-readers.v2"


def _ids(prefix: str, start: int, end: int) -> List[str]:
    return [f"{prefix}{value:02d}" for value in range(start, end + 1)]


ALIAS_ROWS: Dict[str, List[str]] = {
    "TIBIA-RE-AUTH-SESSION": _ids("A", 1, 16) + _ids("H", 20, 22),
    "TIBIA-RE-PLAYER-STATE": _ids("C", 1, 10),
    "TIBIA-RE-INVENTORY-CONTAINERS": _ids("D", 9, 22),
    "TIBIA-RE-CREATURE-COMBAT": _ids("D", 1, 8) + _ids("C", 15, 17),
    "TIBIA-RE-WORLD-MINIMAP": _ids("F", 1, 15),
    "TIBIA-RE-ACTION-PROTOCOL": ["B04"] + _ids("C", 11, 22) + _ids("D", 17, 18) + ["E02"],
    "TIBIA-RE-ITEM-LOOT": _ids("D", 12, 14) + _ids("D", 19, 25),
    "TIBIA-RE-CHAT-SOCIAL": _ids("E", 1, 14),
    "TIBIA-RE-FEATURES": _ids("G", 1, 23),
    "TIBIA-RE-UI-SETTINGS": _ids("H", 1, 19),
    "TIBIA-RE-ECONOMY-PANELS": _ids("G", 24, 31),
    "TIBIA-RE-COORDINATOR": _ids("A", 1, 16)
    + _ids("B", 1, 13)
    + _ids("C", 1, 22)
    + _ids("D", 1, 25)
    + _ids("E", 1, 14)
    + _ids("F", 1, 15)
    + _ids("G", 1, 41)
    + _ids("H", 1, 23),
}

TELEMETRY_FILES = {
    "TIBIA-RE-AUTH-SESSION": "auth-session.json",
    "TIBIA-RE-PLAYER-STATE": "player-state.json",
    "TIBIA-RE-INVENTORY-CONTAINERS": "inventory-containers.json",
    "TIBIA-RE-CREATURE-COMBAT": "creature-combat.json",
    "TIBIA-RE-WORLD-MINIMAP": "world-minimap.json",
    "TIBIA-RE-ACTION-PROTOCOL": "action-protocol.json",
    "TIBIA-RE-ITEM-LOOT": "item-loot.json",
    "TIBIA-RE-CHAT-SOCIAL": "chat-social.json",
    "TIBIA-RE-FEATURES": "features.json",
    "TIBIA-RE-UI-SETTINGS": "ui-settings.json",
    "TIBIA-RE-ECONOMY-PANELS": "economy-panels.json",
}

TYPED_READER_IDS = {
    alias: alias.lower().replace("tibia-re-", "").replace("-", "_") + "_typed_reader"
    for alias in ALIAS_ROWS
    if alias != "TIBIA-RE-COORDINATOR"
}

_STATUS_SCORE = {"BLOCKED": 100, "NOT_STARTED": 60, "PARTIAL": 40, "DONE": 0}
_EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_BEARER_RE = re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}")
_JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
_SECRET_VALUE_RE = re.compile(
    r'(?i)"(?:password|passwd|secret|token|cookie|credential|otp|2fa)"\s*:\s*"(?!<redacted>|<not-retained>)[^"\s][^"]*"'
)


def _safe_runtime(runtime: object) -> dict:
    if not isinstance(runtime, dict):
        return {
            "state": "UNKNOWN",
            "evidence_level": "UNKNOWN",
            "value": None,
            "source": "surveyor.runtime",
        }
    processes = runtime.get("processes") if isinstance(runtime.get("processes"), list) else []
    process = processes[0] if len(processes) == 1 and isinstance(processes[0], dict) else {}
    control = runtime.get("canonical_control") if isinstance(runtime.get("canonical_control"), dict) else {}
    registration = control.get("registration") if isinstance(control.get("registration"), dict) else {}
    lease = control.get("lease") if isinstance(control.get("lease"), dict) else {}
    fence = runtime.get("exact_current_fence") if isinstance(runtime.get("exact_current_fence"), dict) else {}
    value = {
        "observed_at_epoch": runtime.get("observed_at_epoch"),
        "target_container": runtime.get("target_container"),
        "control_container": runtime.get("control_container"),
        "display": runtime.get("display"),
        "target_running": runtime.get("target_running"),
        "runtime_namespace_scope": runtime.get("runtime_namespace_scope"),
        "external_containers_scanned": runtime.get("external_containers_scanned"),
        "target_process_count": runtime.get("target_process_count"),
        "target_uniqueness_scope": runtime.get("target_uniqueness_scope"),
        "target_uniqueness": runtime.get("target_uniqueness"),
        "runtime_access": runtime.get("runtime_access"),
        "exact_current_fence": {
            "version": fence.get("version"),
            "size": fence.get("size"),
            "sha256": fence.get("sha256"),
            "match": fence.get("match"),
        },
        "process": {
            "pid": process.get("pid"),
            "process_start_ticks": process.get("process_start_ticks"),
            "exe_basename": process.get("exe_basename"),
            "client_size": process.get("client_size"),
            "client_sha256": process.get("client_sha256"),
            "exact_fence_match": process.get("exact_fence_match"),
        },
        "canonical_control": {
            "registration_present": control.get("registration_present"),
            "registration_generation": registration.get("registration_generation"),
            "runtime_id": registration.get("runtime_id"),
            "registered_state": registration.get("state"),
            "lease_present": control.get("lease_present"),
            "lease_generation": lease.get("generation"),
            "lease_status": lease.get("status"),
            "lease_expired": control.get("lease_expired"),
        },
        "visible_tibia_window_count": len(runtime.get("visible_tibia_windows") or []),
        "window_title_values_retained": False,
    }
    admitted = runtime.get("runtime_access") == "READ_ONLY_ADMITTED"
    return {
        "state": "AVAILABLE" if admitted else "OBSERVED_NOT_ADMITTED",
        "evidence_level": "PROVEN",
        "value": value,
        "source": "surveyor.runtime",
    }


def _run_provenance(bundle: Mapping[str, object]) -> dict:
    runtime_observation = _safe_runtime(bundle.get("runtime"))
    runtime_value = runtime_observation.get("value") or {}
    process = runtime_value.get("process") if isinstance(runtime_value, dict) else {}
    control = runtime_value.get("canonical_control") if isinstance(runtime_value, dict) else {}
    return {
        "generated_at": bundle.get("generated_at"),
        "client_sha256": process.get("client_sha256") if isinstance(process, dict) else None,
        "runtime_id": control.get("runtime_id") if isinstance(control, dict) else None,
        "registration_generation": control.get("registration_generation") if isinstance(control, dict) else None,
        "lease_generation": control.get("lease_generation") if isinstance(control, dict) else None,
        "semantic_promotion_allowed": False,
    }


def _row_documents(coverage_rows: Sequence[Mapping[str, object]], wanted: Iterable[str]) -> List[dict]:
    by_id = {str(item["row_id"]): item for item in coverage_rows}
    output: List[dict] = []
    for row_id in sorted(set(wanted)):
        item = by_id.get(row_id)
        if item is None:
            continue
        evidence = item.get("evidence_index") if isinstance(item.get("evidence_index"), dict) else {}
        output.append(
            {
                "row_id": row_id,
                "title": item.get("title"),
                "canonical_status": item.get("canonical_status"),
                "repository_evidence_mentions": evidence.get("mention_count", 0),
                "current_sha_evidence_mentions": evidence.get("current_sha_match_count", 0),
                "semantic_promotion_allowed": False,
            }
        )
    return output


def build_collect_all(bundle: Mapping[str, object], coverage_rows: Sequence[Mapping[str, object]]) -> dict:
    if set(ALIAS_ROWS) != {
        "TIBIA-RE-AUTH-SESSION",
        "TIBIA-RE-PLAYER-STATE",
        "TIBIA-RE-INVENTORY-CONTAINERS",
        "TIBIA-RE-CREATURE-COMBAT",
        "TIBIA-RE-WORLD-MINIMAP",
        "TIBIA-RE-ACTION-PROTOCOL",
        "TIBIA-RE-ITEM-LOOT",
        "TIBIA-RE-CHAT-SOCIAL",
        "TIBIA-RE-FEATURES",
        "TIBIA-RE-UI-SETTINGS",
        "TIBIA-RE-ECONOMY-PANELS",
        "TIBIA-RE-COORDINATOR",
    }:
        raise ValueError("collect-all alias registry must contain exactly the twelve canonical aliases")
    runtime_observation = _safe_runtime(bundle.get("runtime"))
    provenance = _run_provenance(bundle)
    telemetry: Dict[str, dict] = {}
    alias_views: Dict[str, dict] = {}
    reader_gaps: List[dict] = []
    run_unavailable_inputs: List[dict] = []
    priority_by_row = {
        str(item["row_id"]): int(item.get("priority_score", 0))
        for item in bundle.get("recommended_next", [])
        if isinstance(item, dict) and item.get("row_id")
    }
    all_rows = {str(item["row_id"]): item for item in coverage_rows}

    if runtime_observation["state"] == "UNKNOWN":
        run_unavailable_inputs.append(
            {
                "surface": "runtime_identity",
                "state": "UNAVAILABLE",
                "reason": "NO_RUNTIME_INPUT_THIS_RUN",
                "semantic_promotion_allowed": False,
            }
        )

    for alias, row_ids in ALIAS_ROWS.items():
        rows = _row_documents(coverage_rows, row_ids)
        reader_id = TYPED_READER_IDS.get(alias)
        source_states = {
            "repository_evidence_index": {
                "state": "AVAILABLE",
                "evidence_level": "PROVEN",
                "source": "surveyor.coverage",
            },
            "runtime_identity": runtime_observation,
            "bridge_profile_compatibility": {
                "state": (bundle.get("bridge_profile") or {}).get("state", "UNKNOWN"),
                "evidence_level": "PROVEN" if bundle.get("bridge_profile") else "UNKNOWN",
                "source": "surveyor.bridge_profile",
                "value": bundle.get("bridge_profile"),
            },
            "bridge_endpoint": {
                "state": "UNKNOWN",
                "evidence_level": "UNKNOWN",
                "source": "current admitted runtime binding",
                "reason": "NO_CANONICAL_BRIDGE_ENDPOINT_PROBED_BY_REPOSITORY_ONLY_COLLECTOR",
            },
        }
        if reader_id is not None:
            implemented = reader_id == "player_state_typed_reader"
            typed = (bundle.get("typed_readers") or {}).get(reader_id) if implemented else None
            if implemented:
                source_states["subsystem_typed_reader"] = {
                    "state": typed.get("state", "UNAVAILABLE") if isinstance(typed, dict) else "UNAVAILABLE",
                    "evidence_level": "PROVEN" if isinstance(typed, dict) and typed.get("state") == "AVAILABLE" else "UNKNOWN",
                    "source": reader_id,
                    "value": typed,
                    "reason": None if isinstance(typed, dict) and typed.get("state") == "AVAILABLE" else "RUNTIME_INPUT_UNAVAILABLE_THIS_RUN",
                }
            else:
                source_states["subsystem_typed_reader"] = {
                    "state": "UNAVAILABLE",
                    "evidence_level": "UNKNOWN",
                    "source": reader_id,
                    "reason": "NO_TYPED_READER_IMPLEMENTED",
                }
                unresolved = [row for row in rows if row.get("canonical_status") != "DONE"]
                status_score = max((_STATUS_SCORE.get(str(row.get("canonical_status")), 0) for row in unresolved), default=0)
                dependency_score = max((priority_by_row.get(str(row.get("row_id")), 0) for row in unresolved), default=0)
                reader_gaps.append(
                    {
                        "reader_id": reader_id,
                        "alias": alias,
                        "state": "UNAVAILABLE",
                        "reason": "NO_TYPED_READER_IMPLEMENTED",
                        "affected_rows": [row["row_id"] for row in unresolved],
                        "canonical_priority_score": max(status_score, dependency_score),
                        "semantic_promotion_allowed": False,
                    }
                )
        else:
            source_states["subsystem_typed_reader"] = {
                "state": "NOT_REQUIRED",
                "evidence_level": "PROVEN",
                "source": "collect-all coordinator aggregation",
            }

        doc = {
            "schema": TELEMETRY_SCHEMA_VERSION,
            "alias": alias,
            "generated_at": bundle.get("generated_at"),
            "run_provenance": provenance,
            "canonical_rows": rows,
            "source_states": source_states,
            "guardrails": {
                "read_only": True,
                "credentials_retained": False,
                "window_title_values_retained": False,
                "chat_message_contents_retained": False,
                "packet_payloads_retained": False,
                "runtime_mutation_requested": False,
                "semantic_promotion_allowed": False,
            },
        }
        if alias in TELEMETRY_FILES:
            telemetry[TELEMETRY_FILES[alias]] = doc
        alias_views[alias] = {
            "schema": ALIAS_SCHEMA_VERSION,
            "alias": alias,
            "generated_at": bundle.get("generated_at"),
            "run_provenance": provenance,
            "collector_result": (
                "STRUCTURAL_RUNTIME_AND_REPOSITORY_INPUT"
                if runtime_observation["state"] != "UNKNOWN"
                else "REPOSITORY_INPUT_ONLY"
            ),
            "telemetry_file": f"telemetry/{TELEMETRY_FILES[alias]}" if alias in TELEMETRY_FILES else None,
            "canonical_rows": [row["row_id"] for row in rows],
            "missing_reader": reader_id,
            "semantic_promotion_allowed": False,
        }

    reader_gaps.sort(key=lambda item: (-int(item["canonical_priority_score"]), str(item["alias"])))
    for index, item in enumerate(reader_gaps, start=1):
        item["rank"] = index

    missing = {
        "schema": MISSING_SCHEMA_VERSION,
        "generated_at": bundle.get("generated_at"),
        "reader_gaps": reader_gaps,
        "run_unavailable_inputs": run_unavailable_inputs,
        "ranking_contract": "canonical blocker/dependency priority first, then alias name",
        "guardrails": {
            "gap_is_semantic_proof": False,
            "gap_authorizes_runtime_mutation": False,
        },
    }
    return {
        "schema": SCHEMA_VERSION,
        "generated_at": bundle.get("generated_at"),
        "telemetry": telemetry,
        "aliases": alias_views,
        "missing_readers": missing,
    }


def _safe_path(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError(f"unsafe output path: {relative!r}")
    root = root.resolve()
    path = (root / relative).resolve()
    if root not in path.parents:
        raise ValueError(f"output path escapes root: {relative!r}")
    return path


def _chmod(path: Path, mode: int) -> None:
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def _write_json(root: Path, relative: str, doc: object) -> None:
    path = _safe_path(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    _chmod(path.parent, 0o700)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _chmod(temp, 0o600)
    temp.replace(path)
    _chmod(path, 0o600)


def _summary(result: Mapping[str, object]) -> str:
    aliases = result["aliases"]
    missing = result["missing_readers"]
    lines = [
        "# TIBIA-RE Surveyor v2 — collect-all summary",
        "",
        f"- aliases emitted: `{len(aliases)}/12`",
        f"- missing typed readers: `{len(missing['reader_gaps'])}`",
        "- runtime mutation requested: `false`",
        "- semantic promotion allowed: `false`",
        "",
        "## Alias views",
        "",
    ]
    for alias in sorted(aliases):
        item = aliases[alias]
        lines.append(f"- `{alias}`: `{item['collector_result']}`; missing reader: `{item['missing_reader']}`")
    lines.extend(["", "## Highest-priority missing readers", ""])
    for gap in missing["reader_gaps"][:10]:
        lines.append(
            f"- `{gap['rank']}` `{gap['alias']}` / `{gap['reader_id']}`: score `{gap['canonical_priority_score']}`"
        )
    lines.extend(
        [
            "",
            "Collection is discovery/evidence input only. Missing readers, structural observations and repository evidence mentions do not promote canonical coverage status.",
            "",
        ]
    )
    return "\n".join(lines)


def scan_generated_privacy(root: Path) -> dict:
    root = root.resolve()
    findings: List[dict] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "manifest.sha256" or path.suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for kind, pattern in (
            ("email_address", _EMAIL_RE),
            ("bearer_value", _BEARER_RE),
            ("jwt_value", _JWT_RE),
            ("sensitive_json_value", _SECRET_VALUE_RE),
        ):
            if pattern.search(text):
                findings.append({"path": str(path.relative_to(root)), "kind": kind})
    return {
        "schema": "otclient.tibia-re-surveyor.privacy-scan.v1",
        "result": "PASS" if not findings else "FAIL",
        "findings": findings,
    }


def _write_manifest(root: Path) -> None:
    lines = []
    for path in sorted(item for item in root.rglob("*") if item.is_file() and item.name != "manifest.sha256"):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
    manifest = _safe_path(root, "manifest.sha256")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    _chmod(manifest, 0o600)


def write_collect_all(root: Path, result: Mapping[str, object]) -> None:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    _chmod(root, 0o700)
    for filename, doc in result["telemetry"].items():
        _write_json(root, f"telemetry/{filename}", doc)
    for alias, doc in result["aliases"].items():
        _write_json(root, f"aliases/{alias}.json", doc)
    _write_json(root, "missing-readers.json", result["missing_readers"])
    summary = _safe_path(root, "summary.md")
    summary.write_text(_summary(result), encoding="utf-8")
    _chmod(summary, 0o600)
    privacy = scan_generated_privacy(root)
    _write_json(root, "privacy-scan.json", privacy)
    if privacy["result"] != "PASS":
        raise ValueError(f"generated evidence privacy scan failed: {privacy['findings']}")
    _write_manifest(root)
