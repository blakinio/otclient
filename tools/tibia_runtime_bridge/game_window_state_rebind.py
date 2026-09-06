from __future__ import annotations

"""Exact-current static rebind of the native game-window IN_GAME discriminator."""

import hashlib
import importlib
import json
from pathlib import Path
import sys
from typing import Any

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52_105_824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
GAME_WINDOW_CLASS = "tibia::gamewindow::TGameWindowController"
GAME_WINDOW_STATE_PROPERTY = "gameWindowState"
GAME_WINDOW_STATE_SIGNAL = "gameWindowStateChanged"
INGAME_TEXT = "INGAME"


def _load_static_helpers() -> tuple[Any, Any]:
    root = Path(__file__).resolve().parents[2]
    scripts = root / ".github" / "scripts"
    token = str(scripts)
    if token not in sys.path:
        sys.path.insert(0, token)
    anchor = importlib.import_module("track_a_current_world_entered_anchor")
    durable = importlib.import_module("track_a_current_world_entered_durable_state")
    return anchor, durable


def _exact_client(path: Path) -> bytes:
    raw = path.read_bytes()
    if len(raw) != EXPECTED_SIZE:
        raise RuntimeError(f"EXACT_CLIENT_SIZE_MISMATCH:{len(raw)}")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CLIENT_SHA256_MISMATCH:{digest}")
    return raw


def analyze_game_window_state(client: Path) -> dict[str, object]:
    anchor, durable = _load_static_helpers()
    raw = _exact_client(client)
    sections, relocs = anchor.parse_elf_layout(raw)

    player = anchor.recover_world_entered_anchor(raw, sections, relocs)
    player_dispatch = anchor.recover_dispatch_case(raw, sections, player)
    activation = anchor.recover_activation_boundary(raw, sections, player, player_dispatch)
    if activation.get("state") != "PROVEN" or activation.get("qmeta_activate_target_va") is None:
        raise RuntimeError(f"QMETA_ACTIVATE_NOT_PROVEN:{activation!r}")
    qmeta_activate = int(activation["qmeta_activate_target_va"])

    meta = durable.recover_qmeta_class(raw, sections, relocs, GAME_WINDOW_CLASS)
    rtti = durable.resolve_primary_vptr_from_rtti(raw, sections, relocs, GAME_WINDOW_CLASS)
    properties = [
        item for item in meta["properties"]
        if item.get("name") == GAME_WINDOW_STATE_PROPERTY
    ]
    if len(properties) != 1:
        raise RuntimeError(f"GAME_WINDOW_STATE_PROPERTY_NOT_UNIQUE:{len(properties)}")
    prop = dict(properties[0])
    if prop.get("type_name") != "QString":
        raise RuntimeError(f"GAME_WINDOW_STATE_TYPE_CHANGED:{prop.get('type_name')!r}")

    entry_trace = durable.extract_bounded_case_trace(
        raw,
        sections,
        int(meta["static_metacall_va"]),
    )
    read_case = durable.recover_property_dispatch_case(
        raw,
        sections,
        meta,
        int(prop["index"]),
        1,
    )
    read_trace = durable.extract_bounded_case_trace(
        raw,
        sections,
        int(read_case["case_target_va"]),
    )
    backing_shape = durable.classify_qstring_member_copy(read_trace)
    backing = durable.prove_qmeta_backing_member(entry_trace, backing_shape)
    if backing.get("state") != "PROVEN_STATIC_QMETA_BACKING_MEMBER":
        raise RuntimeError(f"GAME_WINDOW_STATE_BACKING_NOT_PROVEN:{backing!r}")
    if int(backing.get("byte_width", 0)) != 24:
        raise RuntimeError(f"GAME_WINDOW_STATE_WIDTH_CHANGED:{backing.get('byte_width')!r}")
    member_offset = int(backing["member_offset"])

    methods = {
        str(item["name"]): item
        for item in meta["methods"]
    }
    signal = methods.get(GAME_WINDOW_STATE_SIGNAL)
    if signal is None or signal.get("is_signal") is not True:
        raise RuntimeError("GAME_WINDOW_STATE_SIGNAL_MISSING")
    signal_index = int(signal["index"])
    if int(prop.get("notify_index", -1)) != signal_index:
        raise RuntimeError(
            f"GAME_WINDOW_STATE_NOTIFY_CHANGED:{prop.get('notify_index')!r}:{signal_index}"
        )

    emitters = durable.scan_qmeta_signal_activation_sites(
        raw,
        sections,
        int(meta["static_metaobject_va"]),
        signal_index,
        qmeta_activate,
    )
    if not emitters:
        raise RuntimeError("GAME_WINDOW_STATE_EMITTERS_NOT_FOUND")
    assignments = durable.extract_qstring_member_assignment_sources(emitters, member_offset)
    if not assignments:
        raise RuntimeError("GAME_WINDOW_STATE_ASSIGNMENTS_NOT_FOUND")

    source_targets = {int(item["source_va"]) for item in assignments}
    xrefs = durable.scan_rip_target_xrefs(
        raw,
        sections,
        source_targets,
        pre_count=16,
        post_count=32,
    )
    literal_records: list[dict[str, object]] = []
    semantic_values: set[str] = set()
    for source in sorted(source_targets):
        calls = durable.extract_global_qstring_initializer_literals(xrefs.get(source, []))
        for call in calls:
            decoded = durable.decode_bounded_c_string_literal(
                raw,
                sections,
                int(call["literal_va"]),
            )
            value = decoded.get("printable_utf8")
            if decoded.get("length") == 0:
                value = ""
            if value not in {INGAME_TEXT, ""}:
                continue
            semantic_values.add(str(value))
            literal_records.append(
                {
                    "source_va": source,
                    "literal_va": int(call["literal_va"]),
                    "helper_target_va": int(call["helper_target_va"]),
                    "value": value,
                    "length": int(decoded["length"]),
                    "sha256": str(decoded["sha256"]),
                }
            )
    if semantic_values != {INGAME_TEXT, ""}:
        raise RuntimeError(
            "GAME_WINDOW_STATE_LITERAL_SET_NOT_PROVEN:"
            + json.dumps(sorted(semantic_values))
        )

    dedup_literals = {
        (item["source_va"], item["literal_va"], item["value"]): item
        for item in literal_records
    }
    return {
        "class_name": GAME_WINDOW_CLASS,
        "rtti": rtti,
        "static_metaobject": int(meta["static_metaobject_va"]),
        "static_metacall": int(meta["static_metacall_va"]),
        "method_count": int(meta["method_count"]),
        "signal_count": int(meta["signal_count"]),
        "property_count": int(meta["property_count"]),
        "property": prop,
        "notify_signal": {
            "name": GAME_WINDOW_STATE_SIGNAL,
            "index": signal_index,
            "emitter_count": len(emitters),
        },
        "read_property": {
            "selector": int(read_case["selector"]),
            "property_index": int(read_case["property_index"]),
            "case_target": int(read_case["case_target_va"]),
            "backing_member": backing,
        },
        "literal_values": [
            dedup_literals[key]
            for key in sorted(dedup_literals)
        ],
        "semantic_candidate": {
            "expression": 'gameWindowState == "INGAME"',
            "positive_value": INGAME_TEXT,
            "negative_value": "",
            "classification": "PROVEN_STATIC_SEMANTIC_CANDIDATE_NOT_RUNTIME_PROMOTED",
        },
        "safety": {
            "runtime_access": "none",
            "official_client_executed": False,
            "process_memory_access": False,
            "credentials_used": False,
            "in_game_claimed": False,
            "semantic_promotion_performed": False,
        },
    }


def augment_rebind_output(client: Path, output: Path) -> None:
    result = json.loads(output.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise RuntimeError("NATIVE_LOGIN_REBIND_RESULT_INVALID")
    exact = result.get("exact_client")
    if exact != {
        "version": EXPECTED_VERSION,
        "size": EXPECTED_SIZE,
        "sha256": EXPECTED_SHA256,
    }:
        raise RuntimeError("NATIVE_LOGIN_REBIND_EXACT_CLIENT_MISMATCH")
    qmeta = result.get("qmeta")
    if not isinstance(qmeta, dict):
        raise RuntimeError("NATIVE_LOGIN_REBIND_QMETA_INVALID")
    qmeta["game_window_controller"] = analyze_game_window_state(client)
    result["in_game_discriminator"] = {
        "source": "game_window_controller.gameWindowState",
        "expression": 'gameWindowState == "INGAME"',
        "static_rebind": "PROVEN",
        "live_causal_validation": "REQUIRED",
    }
    result["terminal_result"] = "BE4F48_NATIVE_LOGIN_AND_INGAME_STATIC_REBIND_PROVEN"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("BE4F48_GAME_WINDOW_STATE_STATIC_REBIND=PASS")
    print("BE4F48_IN_GAME_DISCRIMINATOR=STATIC_PROVEN_LIVE_CAUSAL_REQUIRED")


__all__ = ("analyze_game_window_state", "augment_rebind_output")
