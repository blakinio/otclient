"""Exact-current static recovery of a durable world-state candidate."""
from __future__ import annotations

from collections import defaultdict
import json
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
    meta = recover_qmeta_class(raw, sections, relocs, TARGET_CLASS)
    game_window_meta = recover_qmeta_class(raw, sections, relocs, GAME_WINDOW_CLASS)
    game_window_semantic_properties = select_world_semantic_properties(game_window_meta["properties"])
    game_window_state_properties = [prop for prop in game_window_meta["properties"] if prop["name"] == "gameWindowState"]
    game_window_state_read: dict[str, object] = {"state": "NOT_PROVEN"}
    if len(game_window_state_properties) == 1:
        property_meta = game_window_state_properties[0]
        try:
            read_case = recover_property_dispatch_case(raw, sections, game_window_meta, int(property_meta["index"]), 1)
            body = resolve_generated_slot_body(raw, sections, int(read_case["case_target_va"]))
            game_window_state_read = {**read_case, **body, "property": property_meta}
        except DurableStateError as exc:
            game_window_state_read = {"state": "NOT_PROVEN", "reason": str(exc), "property": property_meta}
    elif len(game_window_state_properties) != 1:
        game_window_state_read = {"state": "NOT_PROVEN", "reason": f"GAME_WINDOW_STATE_PROPERTY_NOT_UNIQUE:{len(game_window_state_properties)}"}
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
            "static_metaobject_va": game_window_meta["static_metaobject_va"],
            "static_metacall_va": game_window_meta["static_metacall_va"],
            "method_count": game_window_meta["method_count"],
            "signal_count": game_window_meta["signal_count"],
            "property_count": game_window_meta["property_count"],
            "properties": game_window_meta["properties"],
            "world_semantic_properties": game_window_semantic_properties,
            "game_window_state_read": game_window_state_read,
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
    matches = [candidate for candidate in candidates if candidate.get("full_range") is True and int(candidate.get("selector", -1)) == selector]
    if len(matches) != 1:
        raise DurableStateError(f"READ_PROPERTY_DISPATCH_NOT_UNIQUE:{[(c.get('selector'), c.get('table')) for c in matches]}")
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
        for selector_value in selector_values:
            candidates.append({"selector": selector_value, "full_range": full_range, "table": table, "lea": ins.address, "targets": targets})
    selected = select_unique_property_dispatch_candidate(candidates, selector)
    target = [int(value) for value in selected["targets"]][property_index]
    return {
        "state": "PROVEN_STATIC_READ_PROPERTY_CASE",
        "selector": selector,
        "property_index": property_index,
        "dispatch_lea_va": int(selected["lea"]),
        "dispatch_table_va": int(selected["table"]),
        "case_target_va": target,
    }


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
