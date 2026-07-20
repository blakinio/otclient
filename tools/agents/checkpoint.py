#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

CHECKPOINT_HEADING = "## Context checkpoint"
DEFAULT_CONTRACT = Path("docs/agents/GOVERNANCE_CONTRACT.json")
PLACEHOLDER_NEXT_ACTIONS = {"", "none", "unknown", "pending", "n/a", "tbd", "todo", "later"}
SCALAR_KEYS = {"checkpoint_version", "updated_at", "head", "branch", "pr", "status", "next_action"}
LIST_KEYS = {"context_routes", "owned_paths", "proven", "derived", "unknown", "conflicts", "rejected_hypotheses", "changed_paths", "blockers"}
MAP_KEYS = {"first_failure"}
LIST_OF_MAP_KEYS = {"validation"}


class CheckpointError(ValueError):
    pass


@dataclass(frozen=True)
class Contract:
    version: str
    required_fields: frozenset[str]
    allowed_statuses: frozenset[str]
    allowed_validation_results: frozenset[str]
    evidence_fields: tuple[str, ...]
    compactness_limits: dict[str, int]


@dataclass(frozen=True)
class ParsedCheckpoint:
    data: dict[str, object]
    block: str
    source: Path


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_contract(path: Path | None = None) -> Contract:
    contract_path = path or repository_root() / DEFAULT_CONTRACT
    try:
        raw = json.loads(contract_path.read_text(encoding="utf-8"))
        shared = raw["shared_checkpoint_contract"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise CheckpointError(f"{contract_path}: invalid governance contract: {exc}") from exc
    evidence_map = shared.get("evidence_state_fields", {})
    limits = shared.get("compactness_limits", {})
    if set(evidence_map) != {"PROVEN", "DERIVED", "UNKNOWN", "CONFLICT"}:
        raise CheckpointError(f"{contract_path}: evidence_state_fields must define PROVEN/DERIVED/UNKNOWN/CONFLICT")
    if not isinstance(limits, dict) or not all(isinstance(v, int) and v > 0 for v in limits.values()):
        raise CheckpointError(f"{contract_path}: compactness_limits must contain positive integers")
    return Contract(
        version=str(shared.get("version", "")).strip(),
        required_fields=frozenset(str(x) for x in shared.get("required_fields", [])),
        allowed_statuses=frozenset(str(x) for x in shared.get("allowed_statuses", [])),
        allowed_validation_results=frozenset(str(x) for x in shared.get("allowed_validation_results", [])),
        evidence_fields=tuple(str(evidence_map[k]) for k in ("PROVEN", "DERIVED", "UNKNOWN", "CONFLICT")),
        compactness_limits={str(k): int(v) for k, v in limits.items()},
    )


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def extract_checkpoint_block(text: str, *, source: Path | None = None) -> str | None:
    matches = list(re.finditer(r"(?m)^## Context checkpoint\s*$", text))
    location = str(source) if source else "<text>"
    if not matches:
        return None
    if len(matches) != 1:
        raise CheckpointError(f"{location}: expected exactly one {CHECKPOINT_HEADING} section")
    remainder = text[matches[0].end():]
    next_heading = re.search(r"(?m)^##\s+", remainder)
    section = remainder[:next_heading.start()] if next_heading else remainder
    fences = list(re.finditer(r"```(?:yaml|yml)\s*\n", section, flags=re.IGNORECASE))
    if len(fences) != 1:
        raise CheckpointError(f"{location}: checkpoint must contain exactly one fenced YAML block")
    start = fences[0].end()
    end = section.find("```", start)
    if end < 0:
        raise CheckpointError(f"{location}: checkpoint fenced block is not closed")
    return section[start:end].strip("\n")


def parse_checkpoint_block(block: str, *, source: Path | None = None) -> dict[str, object]:
    data: dict[str, object] = {}
    current_key: str | None = None
    current_validation: dict[str, str] | None = None
    location = str(source) if source else "<checkpoint>"
    for lineno, raw in enumerate(block.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        if indent == 0:
            if ":" not in stripped:
                raise CheckpointError(f"{location}:{lineno}: invalid top-level checkpoint line")
            key, value = stripped.split(":", 1)
            key, value = key.strip(), value.strip()
            if key in data:
                raise CheckpointError(f"{location}:{lineno}: duplicate top-level key {key!r}")
            current_key, current_validation = key, None
            if key in LIST_KEYS or key in LIST_OF_MAP_KEYS:
                if value not in {"", "[]"}:
                    raise CheckpointError(f"{location}:{lineno}: {key} must be a YAML list")
                data[key] = []
            elif key in MAP_KEYS:
                if value:
                    raise CheckpointError(f"{location}:{lineno}: {key} must be a YAML mapping")
                data[key] = {}
            else:
                data[key] = _scalar(value)
            continue
        if current_key is None:
            raise CheckpointError(f"{location}:{lineno}: nested value has no parent")
        if current_key in LIST_KEYS:
            if indent != 2 or not stripped.startswith("- "):
                raise CheckpointError(f"{location}:{lineno}: invalid list item under {current_key}")
            values = data[current_key]
            assert isinstance(values, list)
            values.append(_scalar(stripped[2:]))
            continue
        if current_key in MAP_KEYS:
            if indent != 2 or ":" not in stripped:
                raise CheckpointError(f"{location}:{lineno}: invalid mapping item under {current_key}")
            key, value = stripped.split(":", 1)
            mapping = data[current_key]
            assert isinstance(mapping, dict)
            mapping[key.strip()] = _scalar(value)
            continue
        if current_key in LIST_OF_MAP_KEYS:
            items = data[current_key]
            assert isinstance(items, list)
            if indent == 2 and stripped.startswith("- "):
                item_text = stripped[2:].strip()
                if ":" not in item_text:
                    raise CheckpointError(f"{location}:{lineno}: validation item must start with key/value")
                key, value = item_text.split(":", 1)
                current_validation = {key.strip(): _scalar(value)}
                items.append(current_validation)
                continue
            if indent == 4 and current_validation is not None and ":" in stripped:
                key, value = stripped.split(":", 1)
                current_validation[key.strip()] = _scalar(value)
                continue
            raise CheckpointError(f"{location}:{lineno}: invalid validation entry")
        raise CheckpointError(f"{location}:{lineno}: scalar key {current_key!r} cannot have nested values")
    return data


def parse_task_checkpoint(path: Path) -> ParsedCheckpoint | None:
    text = path.read_text(encoding="utf-8")
    block = extract_checkpoint_block(text, source=path)
    if block is None:
        return None
    return ParsedCheckpoint(parse_checkpoint_block(block, source=path), block, path)


def _normalized_fact(value: str) -> str:
    return " ".join(value.casefold().split())


def validate_checkpoint(data: dict[str, object], contract: Contract, *, source: Path | None = None) -> list[str]:
    location = str(source) if source else "<checkpoint>"
    errors: list[str] = []
    for key in sorted(contract.required_fields - set(data)):
        errors.append(f"{location}: missing checkpoint field {key}")
    if str(data.get("checkpoint_version", "")).strip() != contract.version:
        errors.append(f"{location}: checkpoint_version must be {contract.version}")
    status = str(data.get("status", "")).strip()
    if status not in contract.allowed_statuses:
        errors.append(f"{location}: unsupported checkpoint status {status!r}")
    next_action = str(data.get("next_action", "")).strip()
    if next_action.casefold() in PLACEHOLDER_NEXT_ACTIONS:
        errors.append(f"{location}: next_action must be one concrete next step")
    first_failure = data.get("first_failure")
    if not isinstance(first_failure, dict):
        errors.append(f"{location}: first_failure must be a mapping")
    else:
        for key in ("marker", "evidence"):
            if not str(first_failure.get(key, "")).strip():
                errors.append(f"{location}: first_failure.{key} must not be empty")
    validation = data.get("validation")
    if not isinstance(validation, list):
        errors.append(f"{location}: validation must be a list")
    else:
        for index, item in enumerate(validation, 1):
            if not isinstance(item, dict):
                errors.append(f"{location}: validation item {index} must be a mapping")
                continue
            for key in ("command", "result", "evidence"):
                if not str(item.get(key, "")).strip():
                    errors.append(f"{location}: validation item {index} missing {key}")
            result = str(item.get("result", "")).strip()
            if result and result not in contract.allowed_validation_results:
                errors.append(f"{location}: validation item {index} has unsupported result {result!r}")
    for key, limit in contract.compactness_limits.items():
        value = data.get(key, [])
        if not isinstance(value, list):
            errors.append(f"{location}: {key} must be a list")
        elif len(value) > limit:
            errors.append(f"{location}: {key} has {len(value)} items; compactness limit is {limit}")
    evidence_sets: dict[str, set[str]] = {}
    for key in contract.evidence_fields:
        value = data.get(key, [])
        if isinstance(value, list):
            evidence_sets[key] = {_normalized_fact(str(item)) for item in value if str(item).strip()}
    keys = list(evidence_sets)
    for i, left in enumerate(keys):
        for right in keys[i + 1:]:
            for fact in sorted(evidence_sets[left] & evidence_sets[right]):
                errors.append(f"{location}: evidence fact appears in both {left} and {right}: {fact!r}")
    return errors


def validate_task(path: Path, contract: Contract, *, require_checkpoint: bool) -> list[str]:
    try:
        parsed = parse_task_checkpoint(path)
    except (OSError, UnicodeError, CheckpointError) as exc:
        return [str(exc)]
    if parsed is None:
        return [f"{path}: missing {CHECKPOINT_HEADING}"] if require_checkpoint else []
    return validate_checkpoint(parsed.data, contract, source=path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate compact agent task checkpoints.")
    parser.add_argument("task", nargs="?", type=Path)
    parser.add_argument("--tasks", type=Path)
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--require-checkpoint", action="store_true")
    args = parser.parse_args(argv)
    if bool(args.task) == bool(args.tasks):
        parser.error("provide exactly one task path or --tasks directory")
    contract = load_contract(args.contract)
    paths = [args.task] if args.task else sorted(args.tasks.glob("*.md"))
    errors: list[str] = []
    for path in paths:
        errors.extend(validate_task(path, contract, require_checkpoint=args.require_checkpoint))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} checkpoint task(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
