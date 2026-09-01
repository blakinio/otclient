"""Fail-closed Phase 2 read-only runtime admission and provenance binding."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Any
from urllib.parse import urlsplit

from .canonical import sha256_jcs
from .model import (
    ValidationError,
    checked_non_negative,
    require_exact_keys,
    validate_opaque_id,
)

OBSERVATION_SCHEMA = "otclient.local-agent.runtime-observation.v1"
ADMISSION_SCHEMA = "otclient.local-agent.runtime-admission.v1"
PROVENANCE_SCHEMA = "otclient.local-agent.runtime-provenance.v1"
CURRENT_CLIENT_VERSION = "15.32.75d4a0"
CURRENT_CLIENT_SIZE = 52_105_824
CURRENT_CLIENT_SHA256 = "d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a"
RUNTIME_PLATFORM = "official_native_linux_only"

_OBSERVATION_KEYS = (
    "schema", "track_id", "task_id", "runtime_owner_task", "runtime_namespace",
    "observed_at_epoch_ms", "locator", "process", "window", "inventory", "safety",
)
_LOCATOR_KEYS = (
    "runner", "remote_device", "container", "container_gui_user", "display",
    "observer_endpoint", "host_reachable", "container_running", "display_reachable",
)
_PROCESS_KEYS = (
    "boot_id_sha256", "pid", "process_start_ticks", "exe_path", "display",
    "client_version", "client_size", "client_sha256",
)
_WINDOW_KEYS = ("xid", "pid", "display", "ownership_proven")
_INVENTORY_KEYS = (
    "inventory_scope", "official_client_candidate_count", "exact_client_candidate_count",
    "mismatched_or_unverifiable_candidate_count", "target_uniqueness",
)
_SAFETY_KEYS = (
    "credentials_used", "gui_input_sent", "anti_idle_input_sent", "process_control_used",
    "process_memory_access_used", "network_payload_capture_used", "physical_action_count",
)


def _require_mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValidationError("INVALID_FIELD", f"{field} must be a mapping", field)
    return value


@dataclass(frozen=True)
class ReadOnlyRuntimeAdmission:
    schema: str
    track_id: str
    task_id: str
    runtime_access: str
    runtime_platform: str
    runtime_owner_task: str
    runtime_namespace: str
    canonical_registration: str
    canonical_lease_generation: str
    registration_lease_generation: str
    target_uniqueness: str
    mutation_authorized: bool
    gate_a: str
    generation_rebind: str
    gate_b: str
    bootstrap: str
    observed_at_epoch_ms: int
    runtime_binding_sha256: str
    locator: Mapping[str, Any]
    process: Mapping[str, Any]
    window: Mapping[str, Any]
    inventory: Mapping[str, Any]
    safety: Mapping[str, Any]

    def to_provenance(self) -> dict[str, Any]:
        return {
            "schema": PROVENANCE_SCHEMA,
            "track_id": self.track_id,
            "task_id": self.task_id,
            "runtime_access": self.runtime_access,
            "runtime_platform": self.runtime_platform,
            "runtime_owner_task": self.runtime_owner_task,
            "runtime_namespace": self.runtime_namespace,
            "canonical_registration": self.canonical_registration,
            "canonical_lease_generation": self.canonical_lease_generation,
            "registration_lease_generation": self.registration_lease_generation,
            "gate_a": self.gate_a,
            "generation_rebind": self.generation_rebind,
            "gate_b": self.gate_b,
            "bootstrap": self.bootstrap,
            "target_uniqueness": self.target_uniqueness,
            "mutation_authorized": self.mutation_authorized,
            "observed_at_epoch_ms": self.observed_at_epoch_ms,
            "runtime_binding_sha256": self.runtime_binding_sha256,
            "locator": dict(self.locator),
            "process": dict(self.process),
            "window": dict(self.window),
            "inventory": dict(self.inventory),
            "safety": dict(self.safety),
        }


def admit_read_only_runtime(
    observation: Mapping[str, Any], *, now_epoch_ms: int, max_age_ms: int
) -> ReadOnlyRuntimeAdmission:
    observation = _require_mapping(observation, "observation")
    require_exact_keys(observation, _OBSERVATION_KEYS)
    if observation["schema"] != OBSERVATION_SCHEMA:
        raise ValidationError(
            "INVALID_SCHEMA",
            "runtime observation schema is not the accepted version",
            "schema",
        )
    if observation["track_id"] != "official-client-re":
        raise ValidationError(
            "INVALID_TRACK",
            "runtime observation is not for official-client-re",
            "track_id",
        )
    task_id_value = validate_opaque_id(observation["task_id"], field_name="task_id")
    runtime_owner_task_value = validate_opaque_id(
        observation["runtime_owner_task"], field_name="runtime_owner_task"
    )
    runtime_namespace_raw = observation["runtime_namespace"]
    if (
        not isinstance(runtime_namespace_raw, str)
        or not runtime_namespace_raw
        or runtime_namespace_raw in {"UNKNOWN", "NOT_APPLICABLE"}
    ):
        raise ValidationError(
            "INVALID_RUNTIME_NAMESPACE",
            "read-only runtime namespace must be explicit and non-conflicting",
            "runtime_namespace",
        )
    runtime_namespace_value = validate_opaque_id(
        runtime_namespace_raw, field_name="runtime_namespace", max_bytes=256
    )
    for field, keys in (
        ("locator", _LOCATOR_KEYS),
        ("process", _PROCESS_KEYS),
        ("window", _WINDOW_KEYS),
        ("inventory", _INVENTORY_KEYS),
        ("safety", _SAFETY_KEYS),
    ):
        nested = _require_mapping(observation[field], field)
        require_exact_keys(nested, keys)

    now_epoch_ms = checked_non_negative(now_epoch_ms, field_name="now_epoch_ms")
    max_age_ms = checked_non_negative(max_age_ms, field_name="max_age_ms")
    observed_at_epoch_ms = checked_non_negative(
        observation["observed_at_epoch_ms"], field_name="observed_at_epoch_ms"
    )
    if observed_at_epoch_ms > now_epoch_ms:
        raise ValidationError(
            "RUNTIME_OBSERVATION_FUTURE",
            "runtime observation timestamp is in the future",
            "observed_at_epoch_ms",
        )
    if now_epoch_ms - observed_at_epoch_ms > max_age_ms:
        raise ValidationError(
            "RUNTIME_OBSERVATION_STALE",
            "runtime observation is older than the admitted freshness window",
            "observed_at_epoch_ms",
        )
    locator = dict(observation["locator"])
    for field in ("runner", "remote_device", "container", "container_gui_user"):
        validate_opaque_id(locator[field], field_name=field)
    observer_endpoint = locator["observer_endpoint"]
    endpoint_valid = False
    if isinstance(observer_endpoint, str):
        try:
            parsed_endpoint = urlsplit(observer_endpoint)
            parsed_port = parsed_endpoint.port
            endpoint_valid = (
                parsed_endpoint.scheme == "https"
                and bool(parsed_endpoint.hostname)
                and parsed_endpoint.username is None
                and parsed_endpoint.password is None
                and not parsed_endpoint.query
                and not parsed_endpoint.fragment
                and (parsed_port is None or 1 <= parsed_port <= 65535)
            )
        except ValueError:
            endpoint_valid = False
    if not endpoint_valid:
        raise ValidationError(
            "INVALID_OBSERVER_ENDPOINT",
            "observer endpoint must be a credential-free HTTPS locator",
            "observer_endpoint",
        )
    if any(
        locator.get(field) is not True
        for field in ("host_reachable", "container_running", "display_reachable")
    ):
        raise ValidationError(
            "RUNTIME_LOCATOR_UNAVAILABLE",
            "read-only runtime locator is not freshly reachable",
            "locator",
        )
    process = dict(observation["process"])
    window = dict(observation["window"])
    display = locator.get("display")
    pid = process.get("pid")
    process_start_ticks = process.get("process_start_ticks")
    boot_id_sha256 = process.get("boot_id_sha256")
    exe_path = process.get("exe_path")
    xid = window.get("xid")
    identity_matches = (
        isinstance(display, str)
        and re.fullmatch(r":\d+", display) is not None
        and isinstance(pid, int) and not isinstance(pid, bool) and pid > 0
        and isinstance(process_start_ticks, int)
        and not isinstance(process_start_ticks, bool)
        and process_start_ticks > 0
        and isinstance(boot_id_sha256, str)
        and re.fullmatch(r"[0-9a-f]{64}", boot_id_sha256) is not None
        and isinstance(exe_path, str)
        and PurePosixPath(exe_path).is_absolute()
        and PurePosixPath(exe_path).name == "client"
        and process.get("display") == display
        and isinstance(xid, int) and not isinstance(xid, bool) and xid > 0
        and window.get("pid") == pid
        and window.get("display") == display
        and window.get("ownership_proven") is True
    )
    if not identity_matches:
        raise ValidationError(
            "RUNTIME_IDENTITY_MISMATCH",
            "process, display, and X11 window identity are not one exact proven target",
            "process",
        )
    safety = dict(observation["safety"])
    physical_action_count = checked_non_negative(
        safety["physical_action_count"], field_name="physical_action_count"
    )
    forbidden_read_only_flags = (
        "credentials_used",
        "gui_input_sent",
        "anti_idle_input_sent",
        "process_control_used",
        "process_memory_access_used",
        "network_payload_capture_used",
    )
    if (
        any(safety.get(field) is not False for field in forbidden_read_only_flags)
        or physical_action_count != 0
    ):
        raise ValidationError(
            "RUNTIME_READ_ONLY_VIOLATION",
            "observation contains an effect or access forbidden by Phase 2 read-only policy",
            "safety",
        )
    inventory = dict(observation["inventory"])
    official_client_candidate_count = checked_non_negative(
        inventory["official_client_candidate_count"],
        field_name="official_client_candidate_count",
    )
    exact_client_candidate_count = checked_non_negative(
        inventory["exact_client_candidate_count"],
        field_name="exact_client_candidate_count",
    )
    mismatched_or_unverifiable_candidate_count = checked_non_negative(
        inventory["mismatched_or_unverifiable_candidate_count"],
        field_name="mismatched_or_unverifiable_candidate_count",
    )
    if (
        inventory.get("inventory_scope") != "DECLARED_RUNTIME_NAMESPACE"
        or official_client_candidate_count != 1
        or exact_client_candidate_count != 1
        or mismatched_or_unverifiable_candidate_count != 0
        or inventory.get("target_uniqueness") != "PROVEN"
    ):
        raise ValidationError(
            "RUNTIME_TARGET_NOT_UNIQUE",
            "official-client target uniqueness is not freshly proven",
            "inventory",
        )
    if (
        process.get("client_version") != CURRENT_CLIENT_VERSION
        or process.get("client_size") != CURRENT_CLIENT_SIZE
        or process.get("client_sha256") != CURRENT_CLIENT_SHA256
    ):
        raise ValidationError(
            "RUNTIME_FENCE_MISMATCH",
            "observed client does not match the current exact official-client fence",
            "process",
        )
    runtime_namespace = runtime_namespace_value
    task_id = task_id_value
    runtime_owner_task = runtime_owner_task_value
    if runtime_owner_task != task_id:
        raise ValidationError(
            "RUNTIME_OWNERSHIP_MISMATCH",
            "read-only runtime target is not owned by the current task",
            "runtime_owner_task",
        )
    binding = {
        "track_id": observation["track_id"],
        "runtime_namespace": runtime_namespace,
        "runtime_owner_task": runtime_owner_task,
        "locator": {
            "runner": locator["runner"],
            "remote_device": locator["remote_device"],
            "container": locator["container"],
            "display": locator["display"],
            "observer_endpoint": locator["observer_endpoint"],
        },
        "process": process,
        "window": window,
    }
    return ReadOnlyRuntimeAdmission(
        schema=ADMISSION_SCHEMA,
        track_id="official-client-re",
        task_id=task_id,
        runtime_access="read_only",
        runtime_platform=RUNTIME_PLATFORM,
        runtime_owner_task=runtime_owner_task,
        runtime_namespace=runtime_namespace,
        canonical_registration="NOT_APPLICABLE",
        canonical_lease_generation="NOT_APPLICABLE",
        registration_lease_generation="NOT_APPLICABLE",
        target_uniqueness="PROVEN",
        mutation_authorized=False,
        gate_a="NOT_APPLICABLE",
        generation_rebind="NOT_APPLICABLE",
        gate_b="NOT_APPLICABLE",
        bootstrap="NOT_APPLICABLE",
        observed_at_epoch_ms=observed_at_epoch_ms,
        runtime_binding_sha256=sha256_jcs(binding),
        locator=MappingProxyType(locator),
        process=MappingProxyType(process),
        window=MappingProxyType(window),
        inventory=MappingProxyType(inventory),
        safety=MappingProxyType(safety),
    )
