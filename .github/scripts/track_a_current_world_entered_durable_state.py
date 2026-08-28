"""Exact-current static recovery of a durable world-state candidate."""
from __future__ import annotations

from collections import defaultdict, deque
import json
import re
import struct
from pathlib import Path
import sys


class DurableStateError(RuntimeError):
    pass


RESET_METHODS = (
    "onGameSessionDisconnected",
    "onDialogResponseShowCharacterSelection",
    "onDialogResponseShowLoginDialog",
    "onSessionEndInformation",
)


def select_durable_field_candidate(observations: dict[str, list[dict[str, int]]]) -> dict[str, object]:
    world_writes = observations.get("onWorldEntered", [])
    candidates: list[dict[str, object]] = []
    for world in world_writes:
        offset = int(world["offset"])
        width = int(world["width"])
        world_value = int(world["value"])
        if world_value == 0:
            continue
        reset_methods: list[str] = []
        reset_values: set[int] = set()
        for method in RESET_METHODS:
            for write in observations.get(method, []):
                if int(write["offset"]) != offset or int(write["width"]) != width:
                    continue
                value = int(write["value"])
                if value == world_value:
                    continue
                reset_methods.append(method)
                reset_values.add(value)
        if len(set(reset_methods)) < 2:
            continue
        if len(reset_values) != 1:
            continue
        reset_value = next(iter(reset_values))
        candidates.append({
            "offset": offset,
            "width": width,
            "world_value": world_value,
            "reset_value": reset_value,
            "reset_methods": sorted(set(reset_methods)),
        })

    if not candidates:
        if world_writes:
            raise DurableStateError("DURABLE_FIELD_RESET_PATHS_INSUFFICIENT")
        raise DurableStateError("DURABLE_FIELD_NOT_FOUND")
    unique = {(c["offset"], c["width"], c["world_value"], c["reset_value"]): c for c in candidates}
    if len(unique) != 1:
        raise DurableStateError(f"DURABLE_FIELD_NOT_UNIQUE:{sorted(unique)}")
    return next(iter(unique.values()))


TARGET_CLASS = "tibia::gamewindow::TGameSessionDisconnectReactionController"
GAME_WINDOW_CLASS = "tibia::gamewindow::TGameWindowController"
INTERESTING_METHODS = (
    "onWorldEntered",
    "onGameSessionDisconnected",
    "onDialogResponseShowCharacterSelection",
    "onDialogResponseShowLoginDialog",
    "onSessionEndInformation",
    "onConnectionError",
)


def recover_qmeta_class(raw: bytes, sections, relocs: dict[int, int], class_name: str) -> dict[str, object]:
    import track_a_current_world_entered_anchor as base

    candidates = []
    for stringdata in base._stringdata_candidates(raw, sections, class_name):
        try:
            if base._qstring(raw, sections, stringdata, 0) != class_name:
                continue
        except base.AnchorError:
            continue
        for slot, target in relocs.items():
            if target != stringdata or slot < 8:
                continue
            static_meta = slot - 8
            metadata = relocs.get(static_meta + 16)
            static_metacall = relocs.get(static_meta + 24)
            if metadata is None or static_metacall is None or not base._is_executable(sections, static_metacall):
                continue
            try:
                header = [base._u32(raw, sections, metadata + i * 4) for i in range(14)]
                method_count, method_data, signal_count = header[4], header[5], header[13]
                property_count, property_data = header[6], header[7]
                if not (0 < method_count <= 4096 and 0 <= signal_count <= method_count):
                    continue
                methods = []
                for index in range(method_count):
                    row_va = metadata + (method_data + index * 6) * 4
                    row = [base._u32(raw, sections, row_va + field * 4) for field in range(6)]
                    methods.append({
                        "index": index,
                        "name": base._qstring(raw, sections, stringdata, row[0]),
                        "argc": row[1],
                        "flags": row[4],
                        "is_signal": index < signal_count,
                    })
                properties = parse_qmeta_properties(raw, sections, stringdata, metadata, property_count, property_data)
            except base.AnchorError:
                continue
            candidates.append({
                "class_name": class_name,
                "static_metaobject_va": static_meta,
                "stringdata_va": stringdata,
                "metadata_va": metadata,
                "static_metacall_va": static_metacall,
                "method_count": method_count,
                "signal_count": signal_count,
                "property_count": property_count,
                "properties": properties,
                "methods": methods,
            })
    unique = {(c["static_metaobject_va"], c["metadata_va"], c["static_metacall_va"]): c for c in candidates}
    if len(unique) != 1:
        raise DurableStateError(f"CONTROLLER_QMETA_NOT_UNIQUE:{sorted(unique)}")
    return next(iter(unique.values()))


def recover_dispatch_targets(raw: bytes, sections, meta: dict[str, object]) -> list[int]:
    import track_a_current_world_entered_anchor as base

    synthetic = {
        "static_metacall_va": int(meta["static_metacall_va"]),
        "method_count": int(meta["method_count"]),
        "world_entered_method_index": 0,
    }
    recovered = base.recover_dispatch_case(raw, sections, synthetic)
    targets = [int(value) for value in recovered["dispatch_targets_va"]]
    if len(targets) != int(meta["method_count"]):
        raise DurableStateError("CONTROLLER_DISPATCH_TARGET_COUNT_MISMATCH")
    return targets


def _canonical_register(name: str) -> str:
    groups = {
        "rax": {"rax", "eax", "ax", "al", "ah"},
        "rbx": {"rbx", "ebx", "bx", "bl", "bh"},
        "rcx": {"rcx", "ecx", "cx", "cl", "ch"},
        "rdx": {"rdx", "edx", "dx", "dl", "dh"},
        "rsi": {"rsi", "esi", "si", "sil"},
        "rdi": {"rdi", "edi", "di", "dil"},
        "rbp": {"rbp", "ebp", "bp", "bpl"},
        "rsp": {"rsp", "esp", "sp", "spl"},
    }
    for index in range(8, 16):
        groups[f"r{index}"] = {f"r{index}", f"r{index}d", f"r{index}w", f"r{index}b"}
    for canonical, names in groups.items():
        if name in names:
            return canonical
    return name


def resolve_generated_slot_body(raw: bytes, sections, case_target: int) -> dict[str, object]:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_IMM
    except ImportError as exc:
        raise DurableStateError("CAPSTONE_REQUIRED") from exc
    import track_a_current_world_entered_anchor as base

    offset = base._va_to_offset(sections, case_target)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    instructions = list(md.disasm(raw[offset: offset + 0x90], case_target))
    direct: list[tuple[str, int]] = []
    for ins in instructions:
        if ins.mnemonic in ("call", "jmp") and ins.operands and ins.operands[0].type == X86_OP_IMM:
            target = int(ins.operands[0].imm)
            if base._is_executable(sections, target):
                direct.append((ins.mnemonic, target))
        if ins.mnemonic == "ret":
            break
    tail = [target for mnemonic, target in direct if mnemonic == "jmp"]
    if len(set(tail)) == 1:
        return {"case_target_va": case_target, "body_target_va": tail[0], "resolution": "TAIL_JUMP"}
    calls = [target for mnemonic, target in direct if mnemonic == "call"]
    if len(set(calls)) == 1:
        return {"case_target_va": case_target, "body_target_va": calls[0], "resolution": "SINGLE_CALL"}
    if not direct:
        return {"case_target_va": case_target, "body_target_va": case_target, "resolution": "INLINE"}
    return {"case_target_va": case_target, "body_target_va": None, "resolution": "AMBIGUOUS_BRANCHES"}


def extract_this_immediate_writes(raw: bytes, sections, target: int) -> list[dict[str, int]]:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG
    except ImportError as exc:
        raise DurableStateError("CAPSTONE_REQUIRED") from exc
    import track_a_current_world_entered_anchor as base

    offset = base._va_to_offset(sections, target)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    aliases = {"rdi"}
    constants: dict[str, int] = {}
    writes: list[dict[str, int]] = []
    for ins in md.disasm(raw[offset: offset + 0x280], target):
        operands = ins.operands
        if ins.mnemonic == "xor" and len(operands) == 2 and all(op.type == X86_OP_REG for op in operands):
            left = _canonical_register(ins.reg_name(operands[0].reg))
            right = _canonical_register(ins.reg_name(operands[1].reg))
            if left == right:
                constants[left] = 0
                aliases.discard(left)
        elif ins.mnemonic == "lea" and len(operands) == 2 and operands[0].type == X86_OP_REG and operands[1].type == X86_OP_MEM:
            dest = _canonical_register(ins.reg_name(operands[0].reg))
            base_reg = _canonical_register(ins.reg_name(operands[1].mem.base)) if operands[1].mem.base else ""
            aliases.discard(dest)
            constants.pop(dest, None)
            if base_reg in aliases and operands[1].mem.index == 0 and operands[1].mem.disp == 0:
                aliases.add(dest)
        elif ins.mnemonic == "mov" and len(operands) == 2:
            dest, source = operands
            if dest.type == X86_OP_REG:
                dreg = _canonical_register(ins.reg_name(dest.reg))
                aliases.discard(dreg)
                constants.pop(dreg, None)
                if source.type == X86_OP_REG:
                    sreg = _canonical_register(ins.reg_name(source.reg))
                    if sreg in aliases:
                        aliases.add(dreg)
                    if sreg in constants:
                        constants[dreg] = constants[sreg]
                elif source.type == X86_OP_IMM:
                    constants[dreg] = int(source.imm)
            elif dest.type == X86_OP_MEM and dest.mem.base and dest.mem.index == 0:
                base_reg = _canonical_register(ins.reg_name(dest.mem.base))
                if base_reg in aliases and 0 <= int(dest.mem.disp) <= 0x4000:
                    value: int | None = None
                    if source.type == X86_OP_IMM:
                        value = int(source.imm)
                    elif source.type == X86_OP_REG:
                        value = constants.get(_canonical_register(ins.reg_name(source.reg)))
                    if value is not None:
                        width = int(dest.size)
                        if width in (1, 2, 4, 8):
                            mask = (1 << (width * 8)) - 1
                            writes.append({"offset": int(dest.mem.disp), "width": width, "value": value & mask})
        if ins.mnemonic == "ret":
            break
        if ins.mnemonic == "jmp":
            break
    unique = {(w["offset"], w["width"], w["value"]): w for w in writes}
    return [unique[key] for key in sorted(unique)]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        raise SystemExit("usage: track_a_current_world_entered_durable_state.py CLIENT OUTPUT_JSON")
    import hashlib
    import track_a_current_world_entered_anchor as base

    client = Path(argv[1])
    output = Path(argv[2])
    raw = client.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) != base.EXPECTED_SIZE or digest != base.EXPECTED_SHA256:
        raise DurableStateError(f"EXACT_CLIENT_FENCE_MISMATCH:{len(raw)}:{digest}")
    sections, relocs = base.parse_elf_layout(raw)
    player_anchor = base.recover_world_entered_anchor(raw, sections, relocs)
    player_dispatch = base.recover_dispatch_case(raw, sections, player_anchor)
    player_activation = base.recover_activation_boundary(raw, sections, player_anchor, player_dispatch)
    if player_activation.get("state") != "PROVEN" or player_activation.get("qmeta_activate_target_va") is None:
        raise DurableStateError(f"CURRENT_QMETA_ACTIVATE_TARGET_NOT_PROVEN:{player_activation}")
    qmeta_activate_target = int(player_activation["qmeta_activate_target_va"])
    meta = recover_qmeta_class(raw, sections, relocs, TARGET_CLASS)
    game_window_meta = recover_qmeta_class(raw, sections, relocs, GAME_WINDOW_CLASS)
    game_window_entry_trace = extract_bounded_case_trace(raw, sections, int(game_window_meta["static_metacall_va"]))
    game_window_semantic_properties = select_world_semantic_properties(game_window_meta["properties"])
    game_window_state_properties = [prop for prop in game_window_meta["properties"] if prop["name"] == "gameWindowState"]
    game_window_state_read: dict[str, object] = {"state": "NOT_PROVEN"}
    if len(game_window_state_properties) == 1:
        property_meta = game_window_state_properties[0]
        try:
            read_case = recover_property_dispatch_case(raw, sections, game_window_meta, int(property_meta["index"]), 1)
            case_trace = extract_bounded_case_trace(raw, sections, int(read_case["case_target_va"]))
            body = resolve_generated_slot_body(raw, sections, int(read_case["case_target_va"]))
            try:
                backing_shape = {"state": "PROVEN_STATIC_DIRECT_QSTRING_MEMBER_SHAPE", **classify_qstring_member_copy(case_trace)}
                backing_member = prove_qmeta_backing_member(game_window_entry_trace, backing_shape)
            except DurableStateError as exc:
                backing_shape = {"state": "NOT_PROVEN", "reason": str(exc)}
                backing_member = {"state": "NOT_PROVEN", "reason": str(exc)}
            game_window_state_read = {
                **read_case, **body, "case_trace": case_trace,
                "backing_member_shape": backing_shape,
                "qmeta_backing_member": backing_member,
                "property": property_meta,
            }
        except DurableStateError as exc:
            game_window_state_read = {"state": "NOT_PROVEN", "reason": str(exc), "property": property_meta}
    elif len(game_window_state_properties) != 1:
        game_window_state_read = {"state": "NOT_PROVEN", "reason": f"GAME_WINDOW_STATE_PROPERTY_NOT_UNIQUE:{len(game_window_state_properties)}"}
    game_window_dispatch_targets = recover_dispatch_targets(raw, sections, game_window_meta)
    game_window_methods_by_name = {str(method["name"]): method for method in game_window_meta["methods"]}
    game_window_display_signal_cases: dict[str, object] = {}
    for signal_name in ("gameWindowStateChanged", "startScreenNowDisplayed", "gameScreenNowDisplayed"):
        signal_method = game_window_methods_by_name.get(signal_name)
        if signal_method is None:
            game_window_display_signal_cases[signal_name] = {"state": "MISSING"}
            continue
        signal_index = int(signal_method["index"])
        signal_case = game_window_dispatch_targets[signal_index]
        game_window_display_signal_cases[signal_name] = {
            "index": signal_index,
            "case_target_va": signal_case,
            "case_trace": extract_bounded_case_trace(raw, sections, signal_case),
        }
    game_window_display_signal_emitters: dict[str, object] = {}
    for signal_name in ("gameWindowStateChanged", "startScreenNowDisplayed", "gameScreenNowDisplayed"):
        signal_method = game_window_methods_by_name.get(signal_name)
        if signal_method is None:
            game_window_display_signal_emitters[signal_name] = {"state": "MISSING"}
            continue
        signal_index = int(signal_method["index"])
        sites = scan_qmeta_signal_activation_sites(
            raw, sections, int(game_window_meta["static_metaobject_va"]), signal_index, qmeta_activate_target
        )
        game_window_display_signal_emitters[signal_name] = {
            "state": "FOUND" if sites else "NOT_FOUND",
            "signal_index": signal_index,
            "qmeta_activate_target_va": qmeta_activate_target,
            "sites": sites,
        }
    state_emitter_sites = list(game_window_display_signal_emitters.get("gameWindowStateChanged", {}).get("sites", []))
    raw_assignments = extract_qstring_member_assignment_sources(state_emitter_sites, 0x60)
    grouped_assignments: dict[tuple[int, int], dict[str, object]] = {}
    for assignment in raw_assignments:
        key = (int(assignment["source_va"]), int(assignment["helper_target_va"]))
        item = grouped_assignments.setdefault(key, {
            "source_va": key[0],
            "helper_target_va": key[1],
            "member_offset": int(assignment["member_offset"]),
            "site_vas": [],
        })
        item["site_vas"].append(int(assignment["site_va"]))
    game_window_state_assignment_sources: list[dict[str, object]] = []
    for key in sorted(grouped_assignments):
        item = grouped_assignments[key]
        item["site_vas"] = sorted(set(int(value) for value in item["site_vas"]))
        try:
            decoded = decode_static_qstring_source(raw, sections, relocs, int(item["source_va"]))
            item["decode_state"] = "PROVEN_STATIC_QSTRING_VALUE"
            item["qstring"] = decoded
        except DurableStateError as exc:
            item["decode_state"] = "NOT_PROVEN"
            item["decode_reason"] = str(exc)
        game_window_state_assignment_sources.append(item)
    source_targets = {int(item["source_va"]) for item in game_window_state_assignment_sources}
    raw_initializer_xrefs = scan_rip_target_xrefs(raw, sections, source_targets) if source_targets else {}
    game_window_state_initializer_xrefs = {
        f"0x{target:x}": {
            "source_va": target,
            "xref_count": len(raw_initializer_xrefs.get(target, [])),
            "xrefs": raw_initializer_xrefs.get(target, []),
        }
        for target in sorted(source_targets)
    }
    game_window_state_method_traces: dict[str, object] = {}
    for writer_name in ("goToLogin", "goToCreateNewAccount", "loginPressed", "onAuthenticatedChanged", "onGameWindowClosed"):
        writer = game_window_methods_by_name.get(writer_name)
        if writer is None:
            game_window_state_method_traces[writer_name] = {"state": "MISSING"}
            continue
        writer_index = int(writer["index"])
        writer_case = game_window_dispatch_targets[writer_index]
        writer_case_trace = extract_bounded_case_trace(raw, sections, writer_case)
        writer_resolution = resolve_generated_slot_body(raw, sections, writer_case)
        writer_body = writer_resolution.get("body_target_va")
        game_window_state_method_traces[writer_name] = {
            "index": writer_index,
            "case_target_va": writer_case,
            "case_trace": writer_case_trace,
            "body_target_va": writer_body,
            "resolution": writer_resolution["resolution"],
            "trace": None if writer_body is None else extract_bounded_case_trace(raw, sections, int(writer_body)),
        }

    dispatch_targets = recover_dispatch_targets(raw, sections, meta)

    methods_by_name = {str(method["name"]): method for method in meta["methods"]}
    missing = [name for name in INTERESTING_METHODS if name not in methods_by_name]
    observations: dict[str, list[dict[str, int]]] = {}
    method_results: dict[str, dict[str, object]] = {}
    for name in INTERESTING_METHODS:
        method = methods_by_name.get(name)
        if method is None:
            observations[name] = []
            method_results[name] = {"state": "MISSING"}
            continue
        index = int(method["index"])
        case_target = dispatch_targets[index]
        resolution = resolve_generated_slot_body(raw, sections, case_target)
        body_target = resolution.get("body_target_va")
        writes: list[dict[str, int]] = []
        if body_target is not None:
            writes = extract_this_immediate_writes(raw, sections, int(body_target))
        observations[name] = writes
        method_results[name] = {
            "index": index,
            "argc": int(method["argc"]),
            "is_signal": bool(method["is_signal"]),
            "case_target_va": case_target,
            "body_target_va": body_target,
            "resolution": resolution["resolution"],
            "this_immediate_writes": writes,
        }

    candidate: dict[str, object] | None = None
    candidate_state = "NOT_PROVEN"
    candidate_reason: str | None = None
    try:
        candidate = select_durable_field_candidate(observations)
        candidate_state = "PROVEN_STATIC_SIMPLE_FIELD_CANDIDATE"
    except DurableStateError as exc:
        candidate_reason = str(exc)

    document = {
        "schema": "otclient.track-a.current-world-entered-durable-state.v1",
        "classification": "STATIC_DURABLE_STATE_CANDIDATE_NOT_RUNTIME_PROMOTED",
        "exact_client": {"version": "15.32.75d4a0", "size": base.EXPECTED_SIZE, "sha256": base.EXPECTED_SHA256},
        "game_window_property_census": {
            "class_name": game_window_meta["class_name"],
            "static_metacall_entry_trace": game_window_entry_trace,
            "static_metaobject_va": game_window_meta["static_metaobject_va"],
            "static_metacall_va": game_window_meta["static_metacall_va"],
            "method_count": game_window_meta["method_count"],
            "signal_count": game_window_meta["signal_count"],
            "property_count": game_window_meta["property_count"],
            "methods": game_window_meta["methods"],
            "state_related_methods": [
                method for method in game_window_meta["methods"]
                if any(term in str(method["name"]).lower() for term in ("state", "login", "world", "character", "window"))
            ],
            "properties": game_window_meta["properties"],
            "world_semantic_properties": game_window_semantic_properties,
            "game_window_state_read": game_window_state_read,
            "game_window_display_signal_cases": game_window_display_signal_cases,
            "game_window_display_signal_emitters": game_window_display_signal_emitters,
            "game_window_state_assignment_sources": game_window_state_assignment_sources,
            "game_window_state_initializer_xrefs": game_window_state_initializer_xrefs,
            "game_window_state_method_traces": game_window_state_method_traces,
        },
        "controller": {
            "class_name": meta["class_name"],
            "static_metaobject_va": meta["static_metaobject_va"],
            "static_metacall_va": meta["static_metacall_va"],
            "method_count": meta["method_count"],
            "signal_count": meta["signal_count"],
            "interesting_methods_missing": missing,
            "methods": method_results,
        },
        "candidate": {"state": candidate_state, "reason": candidate_reason, "field": candidate},
        "safety": {
            "runtime_access": "none",
            "client_executed": False,
            "raw_client_retained": False,
            "historical_address_reuse": False,
            "credentials_accessed": False,
            "session_secrets_accessed": False,
            "packet_payloads_captured": False,
            "in_game_claimed": False,
            "semantic_promotion_performed": False,
        },
    }
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("WORLD_ENTERED_DURABLE_STATE_STATIC_ANALYSIS=PASS")
    print(f"WORLD_ENTERED_DURABLE_STATE_CANDIDATE={candidate_state}")
    print(f"GAME_WINDOW_PROPERTY_COUNT={game_window_meta['property_count']}")
    print("GAME_WINDOW_WORLD_SEMANTIC_PROPERTIES=" + ",".join(str(p["name"]) for p in game_window_semantic_properties))
    print(f"GAME_WINDOW_STATE_READ={game_window_state_read.get('state')}")
    if game_window_state_read.get("case_target_va") is not None:
        print(f"GAME_WINDOW_STATE_READ_CASE=0x{int(game_window_state_read['case_target_va']):x}")
    if candidate_reason:
        print(f"WORLD_ENTERED_DURABLE_STATE_REASON={candidate_reason}")
    print("IN_GAME_CLAIMED=false")
    print("SEMANTIC_PROMOTION_PERFORMED=false")
    return 0




_QT_BUILTIN_TYPES = {
    1: "bool",
    2: "int",
    3: "uint",
    4: "qlonglong",
    5: "qulonglong",
    6: "double",
    7: "QChar",
    8: "QVariantMap",
    9: "QVariantList",
    10: "QString",
    11: "QStringList",
    12: "QByteArray",
    43: "void",
}


def parse_qmeta_properties(raw: bytes, sections, stringdata: int, metadata: int,
                           property_count: int, property_data: int) -> list[dict[str, object]]:
    import track_a_current_world_entered_anchor as base

    properties: list[dict[str, object]] = []
    for index in range(property_count):
        row_va = metadata + (property_data + index * 5) * 4
        row = [base._u32(raw, sections, row_va + field * 4) for field in range(5)]
        name_index, raw_type, flags, notify_index, revision = row
        name = base._qstring(raw, sections, stringdata, name_index)
        if raw_type & 0x80000000:
            type_name = base._qstring(raw, sections, stringdata, raw_type & 0x7FFFFFFF)
        else:
            type_name = _QT_BUILTIN_TYPES.get(raw_type, f"metatype:{raw_type}")
        properties.append({
            "index": index,
            "name": name,
            "raw_type": raw_type,
            "type_name": type_name,
            "flags": flags,
            "notify_index": notify_index,
            "revision": revision,
        })
    return properties


def select_world_semantic_properties(properties: list[dict[str, object]]) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    game_state_terms = ("visible", "state", "active", "session", "ready", "connected", "online", "running")
    for prop in properties:
        name = str(prop.get("name", ""))
        lower = name.lower()
        if lower.startswith("world") or lower.startswith("session"):
            selected.append(prop)
            continue
        if lower.startswith("game") and any(term in lower for term in game_state_terms):
            selected.append(prop)
    return selected

def select_unique_property_dispatch_candidate(candidates: list[dict[str, object]], selector: int) -> dict[str, object]:
    matches = [
        candidate for candidate in candidates
        if candidate.get("full_range") is True
        and {int(value) for value in candidate.get("selector_values", [])} == {selector}
    ]
    if len(matches) != 1:
        details = [(candidate.get("selector_values"), candidate.get("table")) for candidate in matches]
        raise DurableStateError(f"READ_PROPERTY_DISPATCH_NOT_UNIQUE:{details}")
    return matches[0]


def recover_property_dispatch_case(raw: bytes, sections, meta: dict[str, object], property_index: int,
                                   selector: int = 1) -> dict[str, object]:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_ESI, X86_REG_RIP
    except ImportError as exc:
        raise DurableStateError("CAPSTONE_REQUIRED") from exc
    import track_a_current_world_entered_anchor as base

    property_count = int(meta["property_count"])
    if not (0 <= property_index < property_count):
        raise DurableStateError(f"PROPERTY_INDEX_OUT_OF_RANGE:{property_index}:{property_count}")
    start = int(meta["static_metacall_va"])
    offset = base._va_to_offset(sections, start)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    instructions = list(md.disasm(raw[offset: min(len(raw), offset + 0x3000)], start))
    candidates: list[dict[str, object]] = []
    for pos, ins in enumerate(instructions):
        if ins.mnemonic != "lea" or len(ins.operands) < 2:
            continue
        dest, source = ins.operands[0], ins.operands[1]
        if dest.type != X86_OP_REG or source.type != X86_OP_MEM or source.mem.base != X86_REG_RIP:
            continue
        table = ins.address + ins.size + source.mem.disp
        reg = dest.reg
        used = False
        for nxt in instructions[pos + 1:pos + 12]:
            if any(op.type == X86_OP_MEM and op.mem.base == reg and op.mem.scale == 4 for op in nxt.operands):
                used = True
                break
        if not used:
            continue
        try:
            targets = [table + base._i32(raw, sections, table + index * 4) for index in range(property_count)]
        except base.AnchorError:
            continue
        if not all(base._is_executable(sections, target) for target in targets):
            continue
        context = instructions[max(0, pos - 24):pos + 4]
        normalized = [(item.mnemonic, item.op_str.replace(" ", "")) for item in context]
        range_tokens = (f"edx,{property_count - 1}", f"edx,0x{property_count - 1:x}")
        full_range = any(mnemonic == "cmp" and operands in range_tokens for mnemonic, operands in normalized)
        selector_values: set[int] = set()
        for item in context:
            if item.mnemonic != "cmp" or len(item.operands) != 2:
                continue
            left, right = item.operands
            if left.type == X86_OP_REG and left.reg == X86_REG_ESI and right.type == X86_OP_IMM:
                selector_values.add(int(right.imm))
        candidates.append({
            "selector_values": sorted(selector_values),
            "full_range": full_range,
            "table": table,
            "lea": ins.address,
            "targets": targets,
            "context": [f"{item.mnemonic} {item.op_str}" for item in context],
        })
    selected = select_unique_property_dispatch_candidate(candidates, selector)
    target = [int(value) for value in selected["targets"]][property_index]
    return {
        "state": "PROVEN_STATIC_READ_PROPERTY_CASE",
        "selector": selector,
        "selector_context_values": selected["selector_values"],
        "selector_context": selected["context"],
        "property_index": property_index,
        "dispatch_lea_va": int(selected["lea"]),
        "dispatch_table_va": int(selected["table"]),
        "case_target_va": target,
    }


def extract_bounded_case_trace(raw: bytes, sections, start: int) -> dict[str, object]:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_IMM
    except ImportError as exc:
        raise DurableStateError("CAPSTONE_REQUIRED") from exc
    import track_a_current_world_entered_anchor as base

    offset = base._va_to_offset(sections, start)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    instructions: list[dict[str, object]] = []
    direct_calls: list[int] = []
    terminal_jump: int | None = None
    terminal_return = False
    for ins in md.disasm(raw[offset:min(len(raw), offset + 0x180)], start):
        instructions.append({"address": int(ins.address), "mnemonic": ins.mnemonic, "op_str": ins.op_str})
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            direct_calls.append(int(ins.operands[0].imm))
        if ins.mnemonic == "jmp":
            if ins.operands and ins.operands[0].type == X86_OP_IMM:
                terminal_jump = int(ins.operands[0].imm)
            break
        if ins.mnemonic == "ret":
            terminal_return = True
            break
        if len(instructions) >= 48:
            break
    return {
        "instructions": instructions,
        "direct_calls": sorted(set(direct_calls)),
        "terminal_jump": terminal_jump,
        "terminal_return": terminal_return,
    }


def classify_qstring_member_copy(trace: dict[str, object]) -> dict[str, object]:
    import re

    instructions = list(trace.get("instructions", []))
    candidates: list[dict[str, object]] = []
    for index, item in enumerate(instructions):
        mnemonic = str(item.get("mnemonic", ""))
        op_str = str(item.get("op_str", ""))
        if mnemonic not in ("movdqu", "movups", "movaps") or "xmmword ptr" not in op_str:
            continue
        match = re.search(r"xmmword ptr \[([a-z0-9]+) \+ 0x([0-9a-f]+)\]", op_str)
        if not match:
            continue
        base_register = match.group(1)
        if base_register == "rsp":
            continue
        member_offset = int(match.group(2), 16)
        found_tail = False
        for later in instructions[index + 1:]:
            later_mnemonic = str(later.get("mnemonic", ""))
            later_op = str(later.get("op_str", ""))
            if later_mnemonic == "call":
                break
            qmatch = re.search(r"qword ptr \[([a-z0-9]+) \+ 0x([0-9a-f]+)\]", later_op)
            if qmatch and qmatch.group(1) == base_register and int(qmatch.group(2), 16) == member_offset + 16:
                found_tail = True
                break
        if found_tail:
            candidates.append({"base_register": base_register, "member_offset": member_offset, "byte_width": 24})
    unique = {(c["base_register"], c["member_offset"], c["byte_width"]): c for c in candidates}
    if len(unique) != 1:
        raise DurableStateError(f"QSTRING_MEMBER_COPY_NOT_UNIQUE:{sorted(unique)}")
    return next(iter(unique.values()))


def prove_qmeta_backing_member(entry_trace: dict[str, object], backing_shape: dict[str, object]) -> dict[str, object]:
    import re

    base_register = str(backing_shape.get("base_register", ""))
    aliases = {"rdi"}
    proven = False
    for item in entry_trace.get("instructions", []):
        mnemonic = str(item.get("mnemonic", ""))
        op_str = str(item.get("op_str", ""))
        if mnemonic != "mov":
            continue
        match = re.fullmatch(r"([a-z0-9]+), ([a-z0-9]+)", op_str)
        if not match:
            continue
        dest = _canonical_register(match.group(1))
        source = _canonical_register(match.group(2))
        aliases.discard(dest)
        if source in aliases:
            aliases.add(dest)
        if dest == base_register:
            proven = source in aliases
    if base_register not in aliases or not proven:
        raise DurableStateError(f"QMETA_BACKING_OBJECT_ALIAS_NOT_PROVEN:{base_register}")
    return {
        "state": "PROVEN_STATIC_QMETA_BACKING_MEMBER",
        "qmeta_object_argument_register": "rdi",
        "backing_register": base_register,
        "member_offset": int(backing_shape["member_offset"]),
        "byte_width": int(backing_shape["byte_width"]),
    }


def scan_qmeta_signal_activation_sites(raw: bytes, sections, static_metaobject: int,
                                       signal_index: int, activation_target: int) -> list[dict[str, object]]:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_EDX, X86_REG_RDX, X86_REG_RIP
    except ImportError as exc:
        raise DurableStateError("CAPSTONE_REQUIRED") from exc

    sites: list[dict[str, object]] = []
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    for section_va, file_offset, size, flags in sections:
        if not (flags & 0x4) or size <= 0:
            continue
        sequence = []
        code = raw[file_offset:file_offset + size]
        for ins in md.disasm(code, section_va):
            sequence.append(ins)
            if len(sequence) > 32:
                sequence.pop(0)
            branch_target = None
            if ins.mnemonic in ("call", "jmp") and ins.operands and ins.operands[0].type == X86_OP_IMM:
                branch_target = int(ins.operands[0].imm)
            if branch_target == activation_target:
                edx_values: set[int] = set()
                rip_refs: set[int] = set()
                for item in sequence:
                    for operand in item.operands:
                        if operand.type == X86_OP_MEM and operand.mem.base == X86_REG_RIP:
                            rip_refs.add(int(item.address + item.size + operand.mem.disp))
                    if item.mnemonic == "mov" and len(item.operands) >= 2:
                        dst, src = item.operands[0], item.operands[1]
                        if dst.type == X86_OP_REG and dst.reg in (X86_REG_EDX, X86_REG_RDX) and src.type == X86_OP_IMM:
                            edx_values.add(int(src.imm) & 0xFFFFFFFF)
                    if item.mnemonic == "xor" and len(item.operands) >= 2:
                        left, right = item.operands[0], item.operands[1]
                        if left.type == X86_OP_REG and right.type == X86_OP_REG and left.reg == right.reg and left.reg in (X86_REG_EDX, X86_REG_RDX):
                            edx_values.add(0)
                if signal_index in edx_values and static_metaobject in rip_refs:
                    sites.append({
                        "sequence_start_va": int(sequence[0].address),
                        "branch_site_va": int(ins.address),
                        "branch_kind": ins.mnemonic,
                        "edx_values": sorted(edx_values),
                        "static_meta_refs": sorted(ref for ref in rip_refs if ref == static_metaobject),
                        "context": [
                            {"address": int(item.address), "size": int(item.size), "mnemonic": item.mnemonic, "op_str": item.op_str}
                            for item in sequence
                        ],
                    })
            if ins.mnemonic in ("ret", "jmp"):
                sequence = []
    unique = {(site["sequence_start_va"], site["branch_site_va"]): site for site in sites}
    return [unique[key] for key in sorted(unique)]


def _parse_hex_displacement(op_str: str, base_register: str) -> int | None:
    compact = op_str.replace(" ", "")
    match = re.search(rf"\[{re.escape(base_register)}([+-]0x[0-9a-fA-F]+)?\]", compact)
    if not match:
        return None
    token = match.group(1)
    if not token:
        return 0
    sign = -1 if token.startswith("-") else 1
    return sign * int(token[1:], 16)


def extract_qstring_member_assignment_sources(sites: list[dict[str, object]], member_offset: int) -> list[dict[str, int]]:
    results: list[dict[str, int]] = []
    for site in sites:
        context = list(site.get("context", []))
        for index, item in enumerate(context):
            if item.get("mnemonic") != "lea":
                continue
            op_str = str(item.get("op_str", ""))
            if not op_str.replace(" ", "").startswith("rdi,[rbx"):
                continue
            if _parse_hex_displacement(op_str.split(",", 1)[1], "rbx") != member_offset:
                continue
            source = None
            helper_target = None
            for previous in reversed(context[max(0, index - 5):index]):
                if previous.get("mnemonic") != "lea":
                    continue
                previous_op = str(previous.get("op_str", ""))
                if not previous_op.replace(" ", "").startswith("rsi,[rip"):
                    continue
                disp = _parse_hex_displacement(previous_op.split(",", 1)[1], "rip")
                if disp is not None:
                    source = int(previous["address"]) + int(previous["size"]) + disp
                    break
            for following in context[index + 1:index + 5]:
                if following.get("mnemonic") != "call":
                    continue
                target = str(following.get("op_str", ""))
                if re.fullmatch(r"0x[0-9a-fA-F]+", target):
                    helper_target = int(target, 16)
                    break
            if source is not None and helper_target is not None:
                results.append({
                    "site_va": int(site.get("sequence_start_va", 0)),
                    "source_va": source,
                    "member_offset": member_offset,
                    "helper_target_va": helper_target,
                })
    unique = {(item["site_va"], item["source_va"], item["helper_target_va"]): item for item in results}
    return [unique[key] for key in sorted(unique)]


def _static_va_to_offset(sections, va: int) -> int:
    for section_va, file_offset, size, _flags in sections:
        if int(section_va) <= va < int(section_va) + int(size):
            return int(file_offset) + va - int(section_va)
    raise DurableStateError(f"STATIC_QSTRING_VA_NOT_MAPPED:{va:#x}")


def _static_pointer(raw: bytes, sections, relocs: dict[int, int], va: int) -> int:
    if va in relocs:
        return int(relocs[va])
    offset = _static_va_to_offset(sections, va)
    if offset + 8 > len(raw):
        raise DurableStateError(f"STATIC_QSTRING_POINTER_OUT_OF_RANGE:{va:#x}")
    return int(struct.unpack_from("<Q", raw, offset)[0])


def decode_static_qstring_source(raw: bytes, sections, relocs: dict[int, int], source_va: int) -> dict[str, object]:
    source_offset = _static_va_to_offset(sections, source_va)
    if source_offset + 24 > len(raw):
        raise DurableStateError("STATIC_QSTRING_OBJECT_OUT_OF_RANGE")
    data_va = _static_pointer(raw, sections, relocs, source_va + 8)
    length = int(struct.unpack_from("<q", raw, source_offset + 16)[0])
    if length < 0 or length > 256:
        raise DurableStateError(f"STATIC_QSTRING_LENGTH_OUT_OF_BOUNDS:{length}")
    if length == 0:
        return {"source_va": source_va, "data_va": data_va, "length": 0, "value": ""}
    if data_va == 0:
        raise DurableStateError("STATIC_QSTRING_DATA_NULL")
    data_offset = _static_va_to_offset(sections, data_va)
    byte_length = length * 2
    if data_offset + byte_length > len(raw):
        raise DurableStateError("STATIC_QSTRING_DATA_OUT_OF_RANGE")
    payload = raw[data_offset:data_offset + byte_length]
    try:
        value = payload.decode("utf-16-le", "strict")
    except UnicodeDecodeError as exc:
        raise DurableStateError("STATIC_QSTRING_UTF16_INVALID") from exc
    if any(ord(ch) < 0x20 and ch not in "\t\r\n" for ch in value):
        raise DurableStateError("STATIC_QSTRING_CONTROL_CHAR_REJECTED")
    return {"source_va": source_va, "data_va": data_va, "length": length, "value": value}


def _instruction_record(ins) -> dict[str, object]:
    return {
        "address": int(ins.address),
        "size": int(ins.size),
        "mnemonic": ins.mnemonic,
        "op_str": ins.op_str,
    }


def scan_rip_target_xrefs(raw: bytes, sections, target_vas: set[int], *, pre_count: int = 12,
                           post_count: int = 12, max_per_target: int = 64) -> dict[int, list[dict[str, object]]]:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_MEM, X86_REG_RIP
    except ImportError as exc:
        raise DurableStateError("CAPSTONE_REQUIRED") from exc
    targets = {int(value) for value in target_vas}
    result: dict[int, list[dict[str, object]]] = {target: [] for target in sorted(targets)}
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    for section_va, file_offset, size, flags in sections:
        if not (int(flags) & 0x4) or int(size) <= 0:
            continue
        pre = deque(maxlen=pre_count)
        active: list[tuple[dict[str, object], int]] = []
        code = raw[int(file_offset):int(file_offset) + int(size)]
        for ins in md.disasm(code, int(section_va)):
            record = _instruction_record(ins)
            next_active: list[tuple[dict[str, object], int]] = []
            for site, remaining in active:
                site["context"].append(record)
                remaining -= 1
                if remaining > 0:
                    next_active.append((site, remaining))
            active = next_active
            refs: set[int] = set()
            for operand in ins.operands:
                if operand.type == X86_OP_MEM and operand.mem.base == X86_REG_RIP:
                    refs.add(int(ins.address + ins.size + operand.mem.disp))
            for target in sorted(refs & targets):
                if len(result[target]) >= max_per_target:
                    raise DurableStateError(f"RIP_TARGET_XREF_LIMIT_EXCEEDED:{target:#x}")
                site = {
                    "reference_va": int(ins.address),
                    "reference": record,
                    "context": list(pre) + [record],
                }
                result[target].append(site)
                if post_count > 0:
                    active.append((site, post_count))
            pre.append(record)
            if ins.mnemonic in ("ret", "jmp"):
                pre.clear()
    for target in result:
        unique = {int(site["reference_va"]): site for site in result[target]}
        result[target] = [unique[key] for key in sorted(unique)]
    return result


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
