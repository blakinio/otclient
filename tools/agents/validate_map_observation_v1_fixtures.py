#!/usr/bin/env python3
"""Validate the deterministic, non-secret Map Observation v1 fixture corpus."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "docs/agents/contracts/fixtures/map_observation_v1/records.jsonl"
FORBIDDEN_TOKENS = (
    "account",
    "email",
    "password",
    "authenticator",
    "cookie",
    "token",
    "authorization",
    "bearer",
    "session_key",
    "login_payload",
    "packet_payload",
    "raw_packet",
)


def fail(message: str) -> None:
    raise SystemExit(f"map observation v1 fixture validation failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_position(value: object, field: str) -> None:
    require(isinstance(value, dict), f"{field} must be an object")
    require(list(value) == ["x", "y", "z"], f"{field} must use x/y/z order")
    require(all(isinstance(value[key], int) for key in ("x", "y", "z")), f"{field} must be integral")


def validate_thing(thing: object, context: str) -> None:
    require(isinstance(thing, dict), f"{context} must be an object")
    require(isinstance(thing.get("stack_position"), int) and thing["stack_position"] >= 0, f"{context} has invalid stack_position")
    require(thing.get("category") in {"item", "creature", "effect", "missile", "unknown"}, f"{context} has invalid category")
    identity = thing.get("identity")
    require(isinstance(identity, dict) and identity, f"{context} has no raw client identity")
    require(set(identity).issubset({"client_appearance_id", "client_creature_id"}), f"{context} claims a forbidden identity")
    require(all(isinstance(value, int) for value in identity.values()), f"{context} identity is not integral")


def main() -> None:
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    require(len(lines) == 6, "expected exactly six normative records")
    records = []
    for index, line in enumerate(lines, start=1):
        require(line and line == line.strip(), f"line {index} is not normalized")
        lowered = line.lower()
        require(not any(token in lowered for token in FORBIDDEN_TOKENS), f"line {index} contains a forbidden secret-shaped token")
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            fail(f"line {index} is not JSON: {error.msg}")
        require(json.dumps(record, separators=(",", ":")) == line, f"line {index} is not canonical JSON")
        records.append(record)

    sequences = [record.get("sequence") for record in records]
    require(sequences == list(range(1, len(records) + 1)), "sequence must be contiguous and monotonic")
    for record in records:
        require(record.get("schema_version") == 1, "schema_version must be 1")
        require(record.get("record_type") in {"tile_snapshot", "tile_delta", "transition_event", "navigation_action_result"}, "record_type is invalid")
        require(record.get("session_id") == "map-observation-fixture-session", "unexpected fixture session id")
        producer = record.get("producer")
        require(isinstance(producer, dict) and list(producer) == ["revision", "client_version", "protocol_version"], "producer shape changed")
        require(isinstance(producer["protocol_version"], int), "protocol_version must be integral")

    full, empty, unknown, delta, transition, action = records
    require(full["record_type"] == "tile_snapshot" and full["completeness"] == "FULL", "missing FULL snapshot")
    validate_position(full.get("position"), "FULL position")
    require([thing["stack_position"] for thing in full["things"]] == [0, 1], "FULL stack ordering changed")
    for index, thing in enumerate(full["things"]):
        validate_thing(thing, f"FULL thing {index}")

    require(empty["record_type"] == "tile_snapshot" and empty["completeness"] == "EMPTY" and empty.get("things") == [], "missing explicit EMPTY snapshot")
    validate_position(empty.get("position"), "EMPTY position")
    require(unknown["record_type"] == "tile_snapshot" and unknown["completeness"] == "UNKNOWN" and "things" not in unknown, "UNKNOWN must not become EMPTY")
    validate_position(unknown.get("position"), "UNKNOWN position")

    require(delta["record_type"] == "tile_delta" and delta["completeness"] == "PARTIAL", "missing PARTIAL delta")
    validate_position(delta.get("position"), "PARTIAL position")
    require([change["operation"] for change in delta["changes"]] == ["add", "change", "delete"], "delta operation order changed")
    for change in delta["changes"]:
        require(isinstance(change.get("stack_position"), int), "delta stack position must be explicit")
        if change["operation"] == "delete":
            require("thing" not in change, "delete must not fabricate a thing")
        else:
            validate_thing(change.get("thing"), f"delta {change['operation']}")

    require(transition["record_type"] == "transition_event" and transition.get("evidence") == "decoded_state", "transition evidence changed")
    validate_position(transition.get("before_position"), "transition before_position")
    validate_position(transition.get("after_position"), "transition after_position")
    require(action["record_type"] == "navigation_action_result" and action.get("result") == "unknown", "action result must not claim input success")
    require(action.get("evidence") == "input_emitted_without_decoded_result", "action evidence changed")
    print("map observation v1 fixture validation: PASS")


if __name__ == "__main__":
    main()
