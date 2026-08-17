#!/usr/bin/env python3
"""Deterministic, repository-native wave planner for autonomous agent coordination.

The tool deliberately does not invoke an AI model.  It plans independent work, emits
compact resume commands, validates standardized worker results, recomputes barriers,
and applies context-rotation gates.  A real model executor is an adapter boundary.
"""

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable

import control_room

TASK_ID_RE = re.compile(r"\b(?:FTAI|OTH|OTERYN|CAN|OTC2?|OTS)-[A-Z0-9][A-Z0-9-]*\b", re.I)
SHA_RE = re.compile(r"^[0-9a-f]{40}$", re.I)
GLOB_CHARS = set("*?[")
VALID_PRESSURES = {"low", "medium", "high", "unbounded"}
VALID_GROWTH = {"falling", "stable", "rising", "rapid", "unknown"}
VALID_RESULT_STATUS = {"completed", "ready", "waiting", "blocked"}
VALID_VALIDATION_RESULT = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}
IGNORED_TASK_FILENAMES = {"README.md", "TASK_TEMPLATE.md", "CONTEXT_HANDOFF.md", "EXECUTION_PROTOCOL.md"}


class OrchestratorError(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class ContextState:
    pressure: str
    growth: str
    score: int | None
    provider_remaining_ratio: float | None = None


@dataclasses.dataclass(frozen=True)
class TaskRecord:
    task_id: str
    path: str
    lane: str
    state: str
    branch: str
    head: str
    owned_paths: tuple[str, ...]
    dependency_items: tuple[str, ...]
    dependency_ids: tuple[str, ...]
    external_dependencies: tuple[str, ...]
    priority: int
    read_only: bool
    context: ContextState


@dataclasses.dataclass(frozen=True)
class Overlay:
    state: str
    head: str | None = None
    context: ContextState | None = None
    reason: str = ""


def load_config(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != 1:
        raise OrchestratorError("orchestrator config schema_version must be 1")
    max_workers = raw.get("max_parallel_workers")
    if not isinstance(max_workers, int) or max_workers < 1:
        raise OrchestratorError("max_parallel_workers must be a positive integer")
    return raw


def _strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _yaml_block(text: str, checkpoint: bool) -> str | None:
    if checkpoint:
        marker = re.search(r"(?m)^## Context checkpoint\s*$", text)
        if not marker:
            return None
        remainder = text[marker.end() :]
        fence = re.search(r"```(?:yaml|yml)\s*\n", remainder, re.I)
        if not fence:
            return None
        end = remainder.find("```", fence.end())
        return remainder[fence.end() : end] if end >= 0 else None
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return text[4:end] if end >= 0 else None


def _top_level_lists(block: str | None) -> dict[str, list[str]]:
    if not block:
        return {}
    result: dict[str, list[str]] = {}
    current: str | None = None
    for raw in block.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 0 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            current = key
            if value == "[]":
                result[key] = []
            elif value:
                result[key] = [_strip_scalar(value)]
            else:
                result.setdefault(key, [])
            continue
        if current is not None and indent >= 2 and stripped.startswith("- "):
            result.setdefault(current, []).append(_strip_scalar(stripped[2:]))
    return result


def task_lists(text: str) -> dict[str, list[str]]:
    result = _top_level_lists(_yaml_block(text, checkpoint=False))
    checkpoint_lists = _top_level_lists(_yaml_block(text, checkpoint=True))
    for key, value in checkpoint_lists.items():
        result[key] = value
    return result


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    normalized = value.strip().casefold()
    if normalized in {"true", "yes", "1", "on"}:
        return True
    if normalized in {"false", "no", "0", "off"}:
        return False
    raise OrchestratorError(f"invalid boolean value: {value!r}")


def _int(value: str | None, default: int | None = None) -> int | None:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise OrchestratorError(f"invalid integer value: {value!r}") from exc


def normalize_state(raw_status: str) -> str:
    value = raw_status.strip().casefold().replace(" ", "_").replace("-", "_")
    if value in {"done", "complete", "completed", "merged", "closed", "archived"}:
        return "DONE"
    if value == "blocked":
        return "BLOCKED"
    if value in {"waiting", "waiting_ci", "waiting_external", "waiting_dependency"}:
        return "WAITING"
    if value == "ready":
        return "READY"
    if value in {"active", "in_progress", "investigating", "implementing", "validating", "running"}:
        return "RUNNING"
    return "UNKNOWN"


def pressure_from_score(score: int, config: dict[str, Any]) -> str:
    if not 0 <= score <= 15:
        raise OrchestratorError(f"context score must be in 0..15, got {score}")
    bands = config.get("context", {}).get("pressure_bands", {})
    for pressure in ("low", "medium", "high", "unbounded"):
        band = bands.get(pressure)
        if isinstance(band, list) and len(band) == 2 and all(isinstance(x, int) for x in band):
            if band[0] <= score <= band[1]:
                return pressure
    raise OrchestratorError(f"context score {score} does not fit configured pressure bands")


def parse_context(values: dict[str, str], config: dict[str, Any]) -> ContextState:
    pressure = values.get("context_pressure", "").strip().casefold()
    growth = values.get("context_growth", "unknown").strip().casefold() or "unknown"
    if growth not in VALID_GROWTH:
        growth = "unknown"
    score = _int(values.get("context_score"))
    ratio_raw = values.get("provider_context_remaining_ratio", "").strip()
    ratio: float | None = None
    if ratio_raw:
        try:
            ratio = float(ratio_raw)
        except ValueError as exc:
            raise OrchestratorError(f"invalid provider_context_remaining_ratio {ratio_raw!r}") from exc
        if not 0.0 <= ratio <= 1.0:
            raise OrchestratorError("provider_context_remaining_ratio must be in 0..1")
    if score is not None:
        computed = pressure_from_score(score, config)
        if pressure and pressure in VALID_PRESSURES and computed != pressure:
            raise OrchestratorError(
                f"context_pressure={pressure} conflicts with context_score={score} ({computed})"
            )
        pressure = computed
    if not pressure:
        pressure = "unknown"
    return ContextState(pressure=pressure, growth=growth, score=score, provider_remaining_ratio=ratio)


def _task_id_from(path: Path, text: str, values: dict[str, str]) -> str:
    explicit = values.get("task_id") or values.get("id")
    if explicit:
        return explicit.strip()
    match = TASK_ID_RE.search(path.stem) or TASK_ID_RE.search(text)
    return match.group(0) if match else path.stem


def _dependencies(items: Iterable[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    ids: list[str] = []
    external: list[str] = []
    for item in items:
        stripped = item.strip()
        if not stripped or stripped.casefold() in {"none", "n/a", "not_applicable"}:
            continue
        found = [match.group(0) for match in TASK_ID_RE.finditer(stripped)]
        if found:
            ids.extend(found)
        else:
            external.append(stripped)
    return tuple(dict.fromkeys(ids)), tuple(external)


def task_from_path(path: Path, config: dict[str, Any]) -> TaskRecord:
    text = path.read_text(encoding="utf-8")
    values = control_room.scalar_map(text)
    lists = task_lists(text)
    task_id = _task_id_from(path, text, values)
    dependency_items = tuple(lists.get("depends_on", []))
    dependency_ids, external_dependencies = _dependencies(dependency_items)
    priority = _int(values.get("orchestrator_priority"), 100)
    assert priority is not None
    return TaskRecord(
        task_id=task_id,
        path=path.as_posix(),
        lane=values.get("project_lane") or values.get("lane") or "",
        state=normalize_state(values.get("status", "unknown")),
        branch=values.get("branch", ""),
        head=values.get("head", ""),
        owned_paths=tuple(lists.get("owned_paths", [])),
        dependency_items=dependency_items,
        dependency_ids=dependency_ids,
        external_dependencies=external_dependencies,
        priority=priority,
        read_only=_bool(values.get("orchestrator_read_only"), False),
        context=parse_context(values, config),
    )


def discover_tasks(tasks_root: Path, config: dict[str, Any]) -> list[TaskRecord]:
    if not tasks_root.exists():
        raise OrchestratorError(f"tasks root does not exist: {tasks_root}")
    tasks = [
        task_from_path(path, config)
        for path in sorted(tasks_root.glob("*.md"))
        if path.name not in IGNORED_TASK_FILENAMES
    ]
    seen: set[str] = set()
    duplicates: list[str] = []
    for task in tasks:
        if task.task_id in seen:
            duplicates.append(task.task_id)
        seen.add(task.task_id)
    if duplicates:
        raise OrchestratorError(f"duplicate task ids: {', '.join(sorted(set(duplicates)))}")
    return tasks


def context_decision(context: ContextState, config: dict[str, Any]) -> tuple[str, list[str]]:
    cfg = config.get("context", {})
    reasons: list[str] = []
    ratio_threshold = cfg.get("provider_remaining_ratio_rotate_below")
    if context.provider_remaining_ratio is not None and isinstance(ratio_threshold, (int, float)):
        if context.provider_remaining_ratio <= float(ratio_threshold):
            reasons.append("PROVIDER_CONTEXT_LOW")
            return "rotate", reasons
    if context.pressure not in VALID_PRESSURES:
        if cfg.get("require_pressure", True):
            return "hold", ["CONTEXT_UNKNOWN"]
        return "dispatch", []
    rotate_at = {str(item).casefold() for item in cfg.get("rotate_at_pressure", ["high", "unbounded"])}
    if context.pressure in rotate_at:
        reasons.append("CONTEXT_ROTATE_REQUIRED")
        return "rotate", reasons
    growth_triggers = {
        str(item).casefold() for item in cfg.get("rotate_medium_when_growth", ["rising", "rapid"])
    }
    if context.pressure == "medium" and context.growth in growth_triggers:
        reasons.append("CONTEXT_MEDIUM_RISING")
        return "rotate", reasons
    return "dispatch", reasons


def _pattern_prefix(pattern: str) -> str:
    value = pattern.strip().replace("\\", "/").lstrip("./")
    for marker in ("/**", "/*"):
        if value.endswith(marker):
            return value[: -len(marker)].rstrip("/")
    first_glob = min((value.find(ch) for ch in GLOB_CHARS if ch in value), default=-1)
    if first_glob >= 0:
        slash = value.rfind("/", 0, first_glob)
        return value[:slash] if slash >= 0 else ""
    return value.rstrip("/")


def path_patterns_overlap(left: str, right: str) -> bool:
    left_n = left.strip().replace("\\", "/").lstrip("./")
    right_n = right.strip().replace("\\", "/").lstrip("./")
    if left_n == right_n:
        return True
    left_prefix = _pattern_prefix(left_n)
    right_prefix = _pattern_prefix(right_n)
    if not left_prefix or not right_prefix:
        return True  # unknown broad glob: fail closed
    if left_prefix == right_prefix:
        # Distinct explicit files in the same directory do not overlap.
        left_glob = any(ch in left_n for ch in GLOB_CHARS)
        right_glob = any(ch in right_n for ch in GLOB_CHARS)
        return left_glob or right_glob or left_n == right_n
    return left_prefix.startswith(right_prefix + "/") or right_prefix.startswith(left_prefix + "/")


def ownership_conflicts(task: TaskRecord, selected: list[TaskRecord]) -> list[str]:
    conflicts: list[str] = []
    for other in selected:
        if any(path_patterns_overlap(a, b) for a in task.owned_paths for b in other.owned_paths):
            conflicts.append(other.task_id)
    return conflicts


def _effective(task: TaskRecord, overlays: dict[str, Overlay]) -> tuple[str, str, ContextState]:
    overlay = overlays.get(task.task_id)
    if not overlay:
        return task.state, task.head, task.context
    return overlay.state, overlay.head or task.head, overlay.context or task.context


def _task_json(task: TaskRecord, head: str, context: ContextState) -> dict[str, Any]:
    return {
        "task_id": task.task_id,
        "task_path": task.path,
        "lane": task.lane,
        "branch": task.branch,
        "dispatch_head": head,
        "owned_paths": list(task.owned_paths),
        "depends_on": list(task.dependency_ids),
        "priority": task.priority,
        "context": dataclasses.asdict(context),
        "resume_command": f"python tools/agents/resume.py --task {task.path}",
    }


def build_plan(
    tasks: list[TaskRecord],
    config: dict[str, Any],
    *,
    overlays: dict[str, Overlay] | None = None,
    lane: str | None = None,
    max_parallel: int | None = None,
    parent_wave_id: str | None = None,
    generation: int = 1,
) -> dict[str, Any]:
    overlays = overlays or {}
    configured_max = int(config["max_parallel_workers"])
    limit = max_parallel if max_parallel is not None else configured_max
    if limit < 1:
        raise OrchestratorError("max_parallel must be positive")

    effective_state: dict[str, str] = {}
    effective_head: dict[str, str] = {}
    effective_context: dict[str, ContextState] = {}
    for task in tasks:
        state, head, context = _effective(task, overlays)
        effective_state[task.task_id] = state
        effective_head[task.task_id] = head
        effective_context[task.task_id] = context

    known_ids = {task.task_id for task in tasks}
    done_ids = {task_id for task_id, state in effective_state.items() if state == "DONE"}
    candidates = [
        task
        for task in tasks
        if effective_state[task.task_id] == "READY" and (lane is None or task.lane == lane)
    ]
    candidates.sort(key=lambda item: (item.priority, item.task_id, item.path))

    selected_tasks: list[TaskRecord] = []
    selected_json: list[dict[str, Any]] = []
    held: list[dict[str, Any]] = []
    selection_cfg = config.get("selection", {})

    for task in candidates:
        reasons: list[str] = []
        details: dict[str, Any] = {}
        missing = [dep for dep in task.dependency_ids if dep not in known_ids]
        pending = [dep for dep in task.dependency_ids if dep in known_ids and dep not in done_ids]
        if missing:
            reasons.append("DEPENDENCY_UNKNOWN")
            details["unknown_dependencies"] = missing
        if pending:
            reasons.append("DEPENDENCY_NOT_DONE")
            details["pending_dependencies"] = pending
        if task.external_dependencies and selection_cfg.get("hold_unresolved_external_dependencies", True):
            reasons.append("EXTERNAL_DEPENDENCY_UNRESOLVED")
            details["external_dependencies"] = list(task.external_dependencies)

        context_action, context_reasons = context_decision(effective_context[task.task_id], config)
        if context_action != "dispatch":
            reasons.extend(context_reasons)
            details["context_action"] = context_action

        head = effective_head[task.task_id]
        if not SHA_RE.fullmatch(head):
            reasons.append("HEAD_UNKNOWN")

        if selection_cfg.get("require_owned_paths", True) and not task.owned_paths and not task.read_only:
            reasons.append("OWNED_PATHS_MISSING")

        conflicts = ownership_conflicts(task, selected_tasks) if not reasons else []
        if conflicts:
            reasons.append("OWNERSHIP_OVERLAP")
            details["conflicts_with"] = conflicts

        if not reasons and len(selected_tasks) >= limit:
            reasons.append("CAPACITY")
            details["max_parallel_workers"] = limit

        if reasons:
            held.append({"task_id": task.task_id, "task_path": task.path, "reasons": reasons, **details})
            continue

        selected_tasks.append(task)
        selected_json.append(_task_json(task, head, effective_context[task.task_id]))

    inactive = [
        {
            "task_id": task.task_id,
            "state": effective_state[task.task_id],
            "task_path": task.path,
        }
        for task in sorted(tasks, key=lambda item: item.task_id)
        if effective_state[task.task_id] != "READY" or (lane is not None and task.lane != lane)
    ]

    digest_payload = {
        "generation": generation,
        "parent": parent_wave_id,
        "selected": [(item["task_id"], item["dispatch_head"]) for item in selected_json],
        "held": [(item["task_id"], item["reasons"]) for item in held],
    }
    digest = hashlib.sha256(
        json.dumps(digest_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "schema_version": 1,
        "wave_id": f"wave-{generation}-{digest}",
        "parent_wave_id": parent_wave_id,
        "generation": generation,
        "lane": lane,
        "max_parallel_workers": limit,
        "selected": selected_json,
        "held": held,
        "inactive": inactive,
        "executor": config.get("executor", {}),
    }
