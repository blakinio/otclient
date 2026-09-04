#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import peer_metaowner as base
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RSP

CONNECTIMPL_HAS_HIDDEN_SRET = True
SRET_BINARY_PROOF_REQUIRED = True
CONNECTIMPL_FORMAL_ABI = {
    "sender": "rsi",
    "signal": "rdx",
    "receiver": "rcx",
    "slot_ptr": "r8",
    "slot_object": "r9",
    "connection_type": "stack0",
    "types": "stack8",
    "sender_metaobject": "stack16",
}
SLOT_OBJECT_ADAPTER_FIELD_OFFSET = 0x10
FAIL_CLOSED_DEFAULTS = {
    "receiver_endpoint_identity": "UNKNOWN",
    "track_b_pr_284_modified": False,
}

CALLER_SAVED = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}
VECTOR_MOVES = {"movdqa", "movdqu", "movaps", "movups"}


def is_rsp_register(img: base.Image, operand: Any) -> bool:
    return operand.type == X86_OP_REG and base.canonical_reg(img, operand.reg) == "rsp"


def stack_deltas(img: base.Image, instructions: list[Any]) -> list[int]:
    delta = 0
    before: list[int] = []
    for ins in instructions:
        before.append(delta)
        if ins.mnemonic in ("sub", "add") and len(ins.operands) >= 2:
            dst, src = ins.operands[0], ins.operands[1]
            if is_rsp_register(img, dst) and src.type == X86_OP_IMM:
                amount = int(src.imm)
                delta += -amount if ins.mnemonic == "sub" else amount
        elif ins.mnemonic == "push":
            delta -= 8
        elif ins.mnemonic == "pop":
            delta += 8
    return before


def stack_key(img: base.Image, ins: Any, delta_before: int, operand_index: int) -> int | None:
    if operand_index >= len(ins.operands):
        return None
    op = ins.operands[operand_index]
    if op.type != X86_OP_MEM or op.mem.base != X86_REG_RSP:
        return None
    return delta_before + int(op.mem.disp)


def resolve_register(
    img: base.Image,
    instructions: list[Any],
    before: int,
    wanted: str,
    deltas: list[int],
    depth: int = 0,
) -> dict[str, Any]:
    if depth > 10:
        return {"classification": "UNKNOWN", "reason": "MAX_STACK_AWARE_SLICE_DEPTH"}
    wanted = wanted.lower()
    for idx in range(before - 1, -1, -1):
        ins = instructions[idx]
        if ins.mnemonic == "call" and wanted in CALLER_SAVED:
            return {
                "classification": "UNKNOWN",
                "reason": "CALL_CLOBBER_BOUNDARY",
                "boundary_site": base.hx(ins.address),
            }
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or base.canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        out: dict[str, Any] = {
            "definition_site": base.hx(ins.address),
            "mnemonic": ins.mnemonic,
            "op_str": ins.op_str,
        }
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM:
            target = base.rip_target(img, ins)
            if target is not None:
                out.update({"classification": base.classify_static(target), "target": base.hx(target)})
                return out
            base_name = base.canonical_reg(img, src.mem.base) if src.mem.base else "none"
            disp = int(src.mem.disp)
            if base_name == "rsp":
                key = deltas[idx] + disp
                out.update(
                    {
                        "classification": "STACK_ADDRESS",
                        "stack_key": key,
                        "stack_displacement": base.fmt_disp(disp),
                    }
                )
                return out
            out.update(
                {
                    "classification": "OBJECT_ADDRESS",
                    "base_register": base_name,
                    "displacement": base.fmt_disp(disp),
                    "base": resolve_register(img, instructions, idx, base_name, deltas, depth + 1)
                    if base_name != "none"
                    else None,
                }
            )
            return out
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_IMM:
                out.update({"classification": "CONSTANT", "value": base.hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
                return out
            if src.type == X86_OP_REG:
                via = base.canonical_reg(img, src.reg)
                resolved = resolve_register(img, instructions, idx, via, deltas, depth + 1)
                out.update({"classification": resolved.get("classification", "UNKNOWN"), "via_register": via, "source": resolved})
                if "stack_key" in resolved:
                    out["stack_key"] = resolved["stack_key"]
                return out
            if src.type == X86_OP_MEM:
                if src.mem.base == X86_REG_RSP:
                    key = deltas[idx] + int(src.mem.disp)
                    store = resolve_stack_slot(img, instructions, idx, key, deltas, depth + 1)
                    out.update(
                        {
                            "classification": store.get("classification", "STACK_LOAD"),
                            "stack_key": key,
                            "stack_displacement": base.fmt_disp(int(src.mem.disp)),
                            "source": store,
                        }
                    )
                    return out
                target = base.rip_target(img, ins)
                if target is not None:
                    out.update({"classification": "STATIC_POINTER_LOAD", "address": base.hx(target)})
                    return out
                base_name = base.canonical_reg(img, src.mem.base) if src.mem.base else "none"
                out.update(
                    {
                        "classification": "OBJECT_FIELD",
                        "base_register": base_name,
                        "displacement": base.fmt_disp(int(src.mem.disp)),
                        "base": resolve_register(img, instructions, idx, base_name, deltas, depth + 1)
                        if base_name != "none"
                        else None,
                    }
                )
                return out
        if ins.mnemonic == "xor" and src is not None and src.type == X86_OP_REG:
            if base.canonical_reg(img, src.reg) == wanted:
                out.update({"classification": "CONSTANT", "value": "0x0"})
                return out
        out.update({"classification": "UNKNOWN", "reason": "UNSUPPORTED_DEFINITION"})
        return out
    return {"classification": f"ENTRY_ARG:{wanted}", "reason": "NO_BOUNDED_DEFINITION"}


def resolve_stack_slot(
    img: base.Image,
    instructions: list[Any],
    before: int,
    wanted_key: int,
    deltas: list[int],
    depth: int = 0,
) -> dict[str, Any]:
    if depth > 10:
        return {"classification": "UNKNOWN", "reason": "MAX_STACK_SLOT_DEPTH"}
    for idx in range(before - 1, -1, -1):
        ins = instructions[idx]
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        key = stack_key(img, ins, deltas[idx], 0)
        if key != wanted_key:
            continue
        src = ins.operands[1]
        row: dict[str, Any] = {
            "classification": "STACK_STORE",
            "site": base.hx(ins.address),
            "stack_key": wanted_key,
            "op_str": ins.op_str,
        }
        if src.type == X86_OP_REG:
            resolved = resolve_register(img, instructions, idx, base.canonical_reg(img, src.reg), deltas, depth + 1)
            row["source"] = resolved
            row["classification"] = resolved.get("classification", "UNKNOWN")
        elif src.type == X86_OP_IMM:
            row["classification"] = "CONSTANT"
            row["value"] = base.hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)
        else:
            row["classification"] = "UNRESOLVED_STORE_SOURCE"
        return row
    return {"classification": "UNKNOWN", "reason": "NO_STACK_STORE_FOR_KEY", "stack_key": wanted_key}


def push_source(
    img: base.Image,
    instructions: list[Any],
    idx: int,
    deltas: list[int],
) -> dict[str, Any]:
    ins = instructions[idx]
    if not ins.operands:
        return {"classification": "UNKNOWN", "reason": "PUSH_WITHOUT_OPERAND"}
    src = ins.operands[0]
    row: dict[str, Any] = {"site": base.hx(ins.address), "op_str": ins.op_str}
    if src.type == X86_OP_IMM:
        row.update({"classification": "CONSTANT", "value": base.hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
    elif src.type == X86_OP_REG:
        resolved = resolve_register(img, instructions, idx, base.canonical_reg(img, src.reg), deltas)
        row.update({"classification": resolved.get("classification", "UNKNOWN"), "source": resolved})
    else:
        row["classification"] = "UNSUPPORTED_PUSH_SOURCE"
    return row


def qt_connect_candidates(img: base.Image, instructions: list[Any]) -> list[tuple[int, dict[str, Any]]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    for idx, ins in enumerate(instructions):
        if ins.mnemonic != "call":
            continue
        target = base.direct_target(ins)
        if target is None:
            continue
        symbol = img.plt_symbol(target)
        dm = base.demangle(symbol)
        text = (dm or symbol or "").lower()
        if "qobject::connectimpl(" in text:
            rows.append(
                (
                    idx,
                    {
                        "site": base.hx(ins.address),
                        "target": base.hx(target),
                        "symbol": symbol,
                        "demangled": dm,
                    },
                )
            )
    return rows


def direct_register_source(img: base.Image, ins: Any, destination: str) -> str | None:
    if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
        return None
    dst, src = ins.operands[0], ins.operands[1]
    if dst.type != X86_OP_REG or src.type != X86_OP_REG:
        return None
    if base.canonical_reg(img, dst.reg) != destination:
        return None
    return base.canonical_reg(img, src.reg)


def prove_hidden_sret(img: base.Image, instructions: list[Any], call_idx: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "sret_binary_proven": False,
        "connect_call_site": base.hx(instructions[call_idx].address),
        "classification": "SRET_BINARY_PROOF_NOT_ESTABLISHED",
    }

    storage_reg = None
    storage_site = None
    for idx in range(call_idx - 1, max(-1, call_idx - 24), -1):
        source = direct_register_source(img, instructions[idx], "rdi")
        if source is not None:
            storage_reg = source
            storage_site = base.hx(instructions[idx].address)
            break
    if storage_reg is None:
        result["reason"] = "CONNECTIMPL_RDI_STORAGE_REGISTER_NOT_FOUND"
        return result

    destructor_idx = None
    destructor_symbol = None
    destructor_demangled = None
    for idx in range(call_idx + 1, min(len(instructions), call_idx + 24)):
        ins = instructions[idx]
        if ins.mnemonic != "call":
            continue
        target = base.direct_target(ins)
        if target is None:
            continue
        symbol = img.plt_symbol(target)
        dm = base.demangle(symbol)
        if dm and dm.startswith("QMetaObject::Connection::~Connection()"):
            destructor_idx = idx
            destructor_symbol = symbol
            destructor_demangled = dm
            break
    if destructor_idx is None:
        result.update(
            {
                "storage_register": storage_reg,
                "storage_definition_site": storage_site,
                "reason": "QMetaObject::Connection::~Connection()_NOT_FOUND_AFTER_CONNECTIMPL",
            }
        )
        return result

    destructor_arg_reg = None
    destructor_arg_site = None
    for idx in range(destructor_idx - 1, call_idx, -1):
        source = direct_register_source(img, instructions[idx], "rdi")
        if source is not None:
            destructor_arg_reg = source
            destructor_arg_site = base.hx(instructions[idx].address)
            break

    proven = destructor_arg_reg == storage_reg and destructor_arg_reg is not None
    result.update(
        {
            "classification": "CONNECTIMPL_HIDDEN_SRET_PROVEN" if proven else "CONNECTIMPL_HIDDEN_SRET_STORAGE_MISMATCH",
            "storage_register": storage_reg,
            "storage_definition_site": storage_site,
            "destructor_call_site": base.hx(instructions[destructor_idx].address),
            "destructor_symbol": destructor_symbol,
            "destructor_demangled": destructor_demangled,
            "destructor_argument_register": destructor_arg_reg,
            "destructor_argument_definition_site": destructor_arg_site,
            "sret_binary_proven": proven,
        }
    )
    return result


def adapter_slot_object_binding(
    img: base.Image,
    instructions: list[Any],
    deltas: list[int],
    start: int,
    call_idx: int,
) -> dict[str, Any]:
    adapter_indexes = [
        i
        for i in range(start, call_idx)
        if base.rip_target(img, instructions[i]) == base.ADAPTER_TARGET
    ]
    result: dict[str, Any] = {
        "adapter_reference_count": len(adapter_indexes),
        "adapter_bound_into_slot_object": False,
        "field_offset": base.hx(SLOT_OBJECT_ADAPTER_FIELD_OFFSET),
    }
    if len(adapter_indexes) != 1:
        result["classification"] = "ADAPTER_REFERENCE_NOT_UNIQUE_IN_SELECTED_BLOCK"
        return result

    adapter_idx = adapter_indexes[0]
    adapter_ins = instructions[adapter_idx]
    if not adapter_ins.operands or adapter_ins.operands[0].type != X86_OP_REG:
        result["classification"] = "ADAPTER_REFERENCE_DESTINATION_NOT_REGISTER"
        return result
    adapter_reg = base.canonical_reg(img, adapter_ins.operands[0].reg)

    scratch_store: tuple[int, int] | None = None
    for idx in range(adapter_idx + 1, call_idx):
        ins = instructions[idx]
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type == X86_OP_MEM and dst.mem.base == X86_REG_RSP and src.type == X86_OP_REG:
            if base.canonical_reg(img, src.reg) == adapter_reg:
                scratch_store = (idx, deltas[idx] + int(dst.mem.disp))
                break
    if scratch_store is None:
        result["classification"] = "ADAPTER_STACK_SCRATCH_STORE_NOT_FOUND"
        return result

    allocs: list[tuple[int, str | None]] = []
    for idx in range(scratch_store[0] + 1, call_idx):
        ins = instructions[idx]
        if ins.mnemonic != "call":
            continue
        target = base.direct_target(ins)
        if target is None:
            continue
        symbol = img.plt_symbol(target)
        if base.demangle(symbol) == "operator new(unsigned long)":
            allocs.append((idx, symbol))
    if len(allocs) != 1:
        result["classification"] = "SLOT_OBJECT_ALLOCATION_NOT_UNIQUE"
        result["allocation_count"] = len(allocs)
        return result
    alloc_idx, alloc_symbol = allocs[0]

    vector_loads: list[tuple[int, str]] = []
    wanted_key = scratch_store[1]
    for idx in range(alloc_idx + 1, call_idx):
        ins = instructions[idx]
        if ins.mnemonic not in VECTOR_MOVES or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_REG or src.type != X86_OP_MEM or src.mem.base != X86_REG_RSP:
            continue
        if deltas[idx] + int(src.mem.disp) == wanted_key:
            vector_loads.append((idx, img.md.reg_name(dst.reg)))
    if len(vector_loads) != 1:
        result["classification"] = "ADAPTER_VECTOR_LOAD_NOT_UNIQUE"
        result["vector_load_count"] = len(vector_loads)
        return result
    vector_idx, vector_reg = vector_loads[0]

    slot_reg_bindings: list[int] = []
    for idx in range(alloc_idx + 1, call_idx):
        ins = instructions[idx]
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if (
            dst.type == X86_OP_REG
            and src.type == X86_OP_REG
            and base.canonical_reg(img, dst.reg) == "r9"
            and base.canonical_reg(img, src.reg) == "rax"
        ):
            slot_reg_bindings.append(idx)
    if len(slot_reg_bindings) != 1:
        result["classification"] = "SLOT_OBJECT_REGISTER_BINDING_NOT_UNIQUE"
        result["slot_reg_binding_count"] = len(slot_reg_bindings)
        return result
    slot_bind_idx = slot_reg_bindings[0]

    field_stores: list[int] = []
    for idx in range(slot_bind_idx + 1, call_idx):
        ins = instructions[idx]
        if ins.mnemonic not in VECTOR_MOVES or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or src.type != X86_OP_REG:
            continue
        dst_base = base.canonical_reg(img, dst.mem.base) if dst.mem.base else "none"
        if (
            dst_base == "r9"
            and int(dst.mem.disp) == SLOT_OBJECT_ADAPTER_FIELD_OFFSET
            and img.md.reg_name(src.reg) == vector_reg
        ):
            field_stores.append(idx)
    if len(field_stores) != 1:
        result["classification"] = "ADAPTER_SLOT_OBJECT_FIELD_STORE_NOT_UNIQUE"
        result["field_store_count"] = len(field_stores)
        return result

    field_idx = field_stores[0]
    ordering = adapter_idx < scratch_store[0] < alloc_idx < vector_idx < slot_bind_idx < field_idx < call_idx
    result.update(
        {
            "classification": "ADAPTER_BOUND_IN_QSLOT_OBJECT",
            "adapter_reference_site": base.hx(adapter_ins.address),
            "scratch_store_site": base.hx(instructions[scratch_store[0]].address),
            "scratch_stack_key": wanted_key,
            "allocation_site": base.hx(instructions[alloc_idx].address),
            "allocation_symbol": alloc_symbol,
            "vector_load_site": base.hx(instructions[vector_idx].address),
            "vector_register": vector_reg,
            "slot_object_register_binding_site": base.hx(instructions[slot_bind_idx].address),
            "field_store_site": base.hx(instructions[field_idx].address),
            "ordering_proven": ordering,
            "adapter_bound_into_slot_object": ordering,
        }
    )
    return result


def analyze_connection(img: base.Image, owner: str) -> dict[str, Any]:
    instructions = img.disassemble(*base.CONNECTION_OWNER_FDE)
    deltas = stack_deltas(img, instructions)
    anchor_indexes = [
        i
        for i, ins in enumerate(instructions)
        if ins.address == base.ADAPTER_REFERENCE_SITE and base.rip_target(img, ins) == base.ADAPTER_TARGET
    ]
    result: dict[str, Any] = {
        "owner_fde": [base.hx(base.CONNECTION_OWNER_FDE[0]), base.hx(base.CONNECTION_OWNER_FDE[1])],
        "adapter_reference_site": base.hx(base.ADAPTER_REFERENCE_SITE),
        "adapter_reference_exact_count": len(anchor_indexes),
        "actual_qt_connection_primitive": "UNKNOWN",
        "actual_qt_connection_callsite": None,
        "sender_endpoint_identity": "UNKNOWN",
        "receiver_endpoint_identity": "UNKNOWN",
        "peer_signal_bound_to_connection": False,
        "sender_metaobject_bound_to_connection": False,
        "sendlogin_adapter_bound_to_connection": False,
        "sendlogin_causal_binding_proven": False,
        "connectimpl_has_hidden_sret": CONNECTIMPL_HAS_HIDDEN_SRET,
        "sret_binary_proof_required": SRET_BINARY_PROOF_REQUIRED,
        "connectimpl_formal_abi": CONNECTIMPL_FORMAL_ABI,
    }
    if len(anchor_indexes) != 1:
        result["classification"] = "ADAPTER_REFERENCE_NOT_EXACT"
        return result

    center = anchor_indexes[0]
    candidates = qt_connect_candidates(img, instructions)
    previous = [(idx, row) for idx, row in candidates if idx < center]
    following = [(idx, row) for idx, row in candidates if idx > center]
    result["qt_connection_candidate_count_in_owner_fde"] = len(candidates)
    if not following:
        result["classification"] = "NO_QOBJECT_CONNECTIMPL_AFTER_EXACT_ADAPTER_REFERENCE"
        return result

    call_idx, primitive = following[0]
    previous_idx = previous[-1][0] if previous else -1
    block_start = previous_idx + 1
    block_refs: list[dict[str, Any]] = []
    for idx in range(block_start, call_idx + 1):
        ins = instructions[idx]
        target = base.rip_target(img, ins)
        if target in (base.PEER_TARGET, base.ADAPTER_TARGET):
            block_refs.append(
                {
                    "site": base.hx(ins.address),
                    "target": base.hx(target),
                    "classification": base.classify_static(target),
                    "mnemonic": ins.mnemonic,
                    "op_str": ins.op_str,
                }
            )
    adapter_refs = [r for r in block_refs if r["classification"] == "ADAPTER_FUNCTION"]
    peer_refs = [r for r in block_refs if r["classification"] == "PEER_FUNCTION"]
    block_unique = (
        len(adapter_refs) == 1
        and adapter_refs[0]["site"] == base.hx(base.ADAPTER_REFERENCE_SITE)
        and len(peer_refs) == 1
        and center < call_idx
    )
    result["selected_construction_block"] = {
        "start": base.hx(instructions[block_start].address) if block_start < len(instructions) else None,
        "end": primitive["site"],
        "previous_qt_connect_callsite": previous[-1][1]["site"] if previous else None,
        "selected_first_qt_connect_after_adapter": primitive["site"],
        "adapter_reference_count": len(adapter_refs),
        "peer_reference_count": len(peer_refs),
        "references": block_refs,
        "unique": block_unique,
    }
    if not block_unique:
        result["classification"] = "EXACT_ADAPTER_PEER_CONSTRUCTION_BLOCK_NOT_UNIQUE"
        return result

    primitive_name = primitive.get("demangled") or primitive.get("symbol") or "UNKNOWN"
    result["actual_qt_connection_primitive"] = primitive_name
    result["actual_qt_connection_callsite"] = primitive["site"]
    result["connection_selection_reason"] = (
        "FIRST_QOBJECT_CONNECTIMPL_AFTER_EXACT_ADAPTER_REFERENCE_WITH_ONE_PEER_AND_ONE_ADAPTER_REFERENCE_SINCE_PREVIOUS_CONNECTIMPL"
    )

    sret = prove_hidden_sret(img, instructions, call_idx)
    result["sret_binary_proof"] = sret
    result["sret_binary_proven"] = bool(sret.get("sret_binary_proven"))
    if SRET_BINARY_PROOF_REQUIRED and not result["sret_binary_proven"]:
        result["actual_qt_connection_primitive"] = "UNKNOWN"
        result["actual_qt_connection_callsite"] = None
        result["classification"] = "CONNECTIMPL_HIDDEN_SRET_BINARY_PROOF_NOT_ESTABLISHED"
        return result

    args = {
        name: resolve_register(img, instructions, call_idx, reg, deltas)
        for name, reg in (
            ("hidden_sret", "rdi"),
            ("sender", "rsi"),
            ("signal", "rdx"),
            ("receiver", "rcx"),
            ("slot_ptr", "r8"),
            ("slot_object", "r9"),
        )
    }
    result["connection_arguments"] = args

    pushes = [idx for idx in range(block_start, call_idx) if instructions[idx].mnemonic == "push"]
    result["stack_argument_push_count"] = len(pushes)
    if len(pushes) == 3:
        stack_values = [push_source(img, instructions, idx, deltas) for idx in reversed(pushes)]
        result["connection_stack_arguments"] = {
            "connection_type": stack_values[0],
            "types": stack_values[1],
            "sender_metaobject": stack_values[2],
        }
        result["sender_metaobject_bound_to_connection"] = base.contains_classification(
            stack_values[2], "METAOBJECT_ANCHOR"
        )
    else:
        result["connection_stack_arguments"] = {
            "classification": "EXPECTED_EXACTLY_THREE_STACK_ARGUMENT_PUSHES"
        }

    signal = args["signal"]
    signal_store = None
    signal_key = signal.get("stack_key")
    if isinstance(signal_key, int):
        signal_store = resolve_stack_slot(img, instructions, call_idx, signal_key, deltas)
    result["signal_pointer_store"] = signal_store
    result["peer_signal_bound_to_connection"] = (
        base.contains_classification(signal, "PEER_FUNCTION")
        or (signal_store is not None and base.contains_classification(signal_store, "PEER_FUNCTION"))
    )

    slot_binding = adapter_slot_object_binding(img, instructions, deltas, block_start, call_idx)
    result["slot_object_adapter_binding"] = slot_binding
    result["sendlogin_adapter_bound_to_connection"] = bool(
        slot_binding.get("adapter_bound_into_slot_object")
    )

    if (
        result["peer_signal_bound_to_connection"]
        and result["sender_metaobject_bound_to_connection"]
        and owner != "UNKNOWN"
    ):
        result["sender_endpoint_identity"] = owner

    result["sender_endpoint_provenance"] = args["sender"]
    result["receiver_endpoint_provenance"] = args["receiver"]
    result["slot_ptr_provenance"] = args["slot_ptr"]
    result["slot_object_provenance"] = args["slot_object"]

    # The receiver object is statically proven only to a concrete object-field
    # provenance in this bounded function. Its class identity is deliberately
    # withheld rather than inferred from adjacency or the slot adapter.
    result["receiver_endpoint_identity"] = "UNKNOWN"
    result["sendlogin_causal_binding_proven"] = bool(
        result["peer_signal_bound_to_connection"]
        and result["sender_metaobject_bound_to_connection"]
        and result["sendlogin_adapter_bound_to_connection"]
        and result["sender_endpoint_identity"] != "UNKNOWN"
        and result["receiver_endpoint_identity"] != "UNKNOWN"
    )

    if (
        result["peer_signal_bound_to_connection"]
        and result["sender_metaobject_bound_to_connection"]
        and result["sendlogin_adapter_bound_to_connection"]
    ):
        result["classification"] = "QOBJECT_CONNECTIMPL_SIGNAL_ADAPTER_DIRECTION_PROVEN_RECEIVER_TYPE_WITHHELD"
    else:
        result["classification"] = "QOBJECT_CONNECTIMPL_SELECTED_BUT_REQUIRED_DATAFLOW_INCOMPLETE"
    return result


def main() -> None:
    base.analyze_connection = analyze_connection
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = base.analyze(args.client, args.output)
    print("BE4F48_SENDLOGIN_PEER_METAOWNER_V3_ANALYSIS=PASS")
    print("PEER_OWNER_IDENTITY=" + str(result["peer_owner_identity"]))
    print("ACTUAL_QT_CONNECTION_PRIMITIVE=" + str(result["actual_qt_connection_primitive"]))
    print("ACTUAL_QT_CONNECTION_CALLSITE=" + str(result["actual_qt_connection_callsite"]))
    print("SENDER_ENDPOINT_IDENTITY=" + str(result["sender_endpoint_identity"]))
    print("RECEIVER_ENDPOINT_IDENTITY=" + str(result["receiver_endpoint_identity"]))
    print("SENDLOGIN_CAUSAL_BINDING_PROVEN=" + str(result["sendlogin_causal_binding_proven"]).lower())
    print("FIRST_MISSING_BOUNDARY=" + str(result["first_missing_boundary"]))
    print("TERMINAL_RESULT=" + str(result["terminal_result"]))


if __name__ == "__main__":
    main()
