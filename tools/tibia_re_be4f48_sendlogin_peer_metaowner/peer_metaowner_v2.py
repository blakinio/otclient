#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import peer_metaowner as base
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RSP


def latest_stack_source(img: base.Image, window: list[Any], before: int, displacement: int) -> dict[str, Any] | None:
    for idx in range(before - 1, -1, -1):
        ins = window[idx]
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or dst.mem.base != X86_REG_RSP or int(dst.mem.disp) != displacement:
            continue
        row: dict[str, Any] = {
            "site": base.hx(ins.address),
            "stack_displacement": base.fmt_disp(displacement),
            "op_str": ins.op_str,
        }
        if src.type == X86_OP_REG:
            row["source"] = base.resolve_reg(img, window, idx, base.canonical_reg(img, src.reg))
        elif src.type == X86_OP_IMM:
            row["source"] = {"classification": "CONSTANT", "value": base.hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)}
        else:
            row["source"] = {"classification": "UNRESOLVED_STORE_SOURCE"}
        return row
    return None


def instruction_row(img: base.Image, ins: Any) -> dict[str, Any]:
    row: dict[str, Any] = {"site": base.hx(ins.address), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
    target = base.rip_target(img, ins)
    if target is not None:
        row["rip_target"] = base.hx(target)
        if target in (base.METAOBJECT_ANCHOR, base.PEER_TARGET, base.ADAPTER_TARGET):
            row["bounded_target_classification"] = base.classify_static(target)
    direct = base.direct_target(ins)
    if direct is not None:
        row["direct_target"] = base.hx(direct)
        if ins.mnemonic == "call":
            symbol = img.plt_symbol(direct)
            row["symbol"] = symbol
            row["demangled"] = base.demangle(symbol)
    return row


def analyze_connection(img: base.Image, owner: str) -> dict[str, Any]:
    instructions = img.disassemble(*base.CONNECTION_OWNER_FDE)
    anchors = [
        i for i, ins in enumerate(instructions)
        if ins.address == base.ADAPTER_REFERENCE_SITE and base.rip_target(img, ins) == base.ADAPTER_TARGET
    ]
    result: dict[str, Any] = {
        "owner_fde": [base.hx(base.CONNECTION_OWNER_FDE[0]), base.hx(base.CONNECTION_OWNER_FDE[1])],
        "adapter_reference_site": base.hx(base.ADAPTER_REFERENCE_SITE),
        "adapter_reference_exact_count": len(anchors),
        "actual_qt_connection_primitive": "UNKNOWN",
        "actual_qt_connection_callsite": None,
        "sender_endpoint_identity": "UNKNOWN",
        "receiver_endpoint_identity": "UNKNOWN",
        "peer_signal_bound_to_connection": False,
        "sender_metaobject_bound_to_connection": False,
        "sendlogin_adapter_bound_to_connection": False,
        "sendlogin_causal_binding_proven": False,
    }
    if len(anchors) != 1:
        result["classification"] = "ADAPTER_REFERENCE_NOT_EXACT"
        return result

    connect_candidates: list[tuple[int, dict[str, Any]]] = []
    for idx, ins in enumerate(instructions):
        if ins.mnemonic != "call":
            continue
        target = base.direct_target(ins)
        if target is None:
            continue
        symbol = img.plt_symbol(target)
        dm = base.demangle(symbol)
        text = (dm or symbol or "").lower()
        if "qobject" in text and "connect" in text and "disconnect" not in text and "connectnotify" not in text:
            connect_candidates.append((idx, {
                "site": base.hx(ins.address),
                "target": base.hx(target),
                "symbol": symbol,
                "demangled": dm,
            }))

    center = anchors[0]
    previous = [(idx, row) for idx, row in connect_candidates if idx < center]
    following = [(idx, row) for idx, row in connect_candidates if idx > center]
    result["qt_connection_candidate_count_in_owner_fde"] = len(connect_candidates)
    result["qt_connection_candidates_in_owner_fde"] = [row for _, row in connect_candidates]
    if not following:
        result["classification"] = "NO_QT_CONNECT_AFTER_EXACT_ADAPTER_REFERENCE"
        return result

    call_idx, primitive = following[0]
    previous_idx = previous[-1][0] if previous else -1
    block_start = previous_idx + 1
    block = instructions[block_start : call_idx + 1]
    local_call_idx = len(block) - 1

    block_refs: list[dict[str, Any]] = []
    for ins in block:
        target = base.rip_target(img, ins)
        if target in (base.METAOBJECT_ANCHOR, base.PEER_TARGET, base.ADAPTER_TARGET):
            block_refs.append({
                "site": base.hx(ins.address),
                "target": base.hx(target),
                "classification": base.classify_static(target),
                "mnemonic": ins.mnemonic,
                "op_str": ins.op_str,
            })
    adapter_refs = [r for r in block_refs if r["classification"] == "ADAPTER_FUNCTION"]
    peer_refs = [r for r in block_refs if r["classification"] == "PEER_FUNCTION"]
    meta_refs = [r for r in block_refs if r["classification"] == "METAOBJECT_ANCHOR"]

    result["selected_construction_block"] = {
        "start": base.hx(block[0].address) if block else None,
        "end": primitive["site"],
        "previous_qt_connect_callsite": previous[-1][1]["site"] if previous else None,
        "selected_first_qt_connect_after_adapter": primitive["site"],
        "adapter_reference_count": len(adapter_refs),
        "peer_reference_count": len(peer_refs),
        "metaobject_reference_count": len(meta_refs),
        "references": block_refs,
        "instructions": [instruction_row(img, ins) for ins in block],
    }

    block_is_unique = (
        len(adapter_refs) == 1
        and adapter_refs[0]["site"] == base.hx(base.ADAPTER_REFERENCE_SITE)
        and len(peer_refs) == 1
        and len(meta_refs) == 1
        and int(adapter_refs[0]["site"], 16) < int(peer_refs[0]["site"], 16) < int(primitive["site"], 16)
        and int(meta_refs[0]["site"], 16) < int(primitive["site"], 16)
    )
    result["construction_block_unique"] = block_is_unique
    if not block_is_unique:
        result["classification"] = "EXACT_ADAPTER_CONSTRUCTION_BLOCK_NOT_UNIQUE"
        return result

    primitive_name = primitive.get("demangled") or primitive.get("symbol") or "UNKNOWN"
    if "qobject::connectimpl(" not in primitive_name.lower():
        result["classification"] = "SELECTED_CALL_IS_NOT_QOBJECT_CONNECTIMPL"
        return result

    result["actual_qt_connection_primitive"] = primitive_name
    result["actual_qt_connection_callsite"] = primitive["site"]
    result["connection_selection_reason"] = "FIRST_QOBJECT_CONNECTIMPL_AFTER_EXACT_ADAPTER_REFERENCE_WITHIN_UNIQUE_REPEATED_CONSTRUCTION_BLOCK"
    result["qt_call_contract"] = {
        "signature": primitive_name,
        "arg1_sender": "rdi",
        "arg2_signal": "rsi",
        "arg3_receiver": "rdx",
        "arg4_slot": "rcx",
        "arg5_slot_object": "r8",
        "arg6_connection_type": "r9",
        "arg7_types": "[rsp+0x0] at call",
        "arg8_sender_metaobject": "[rsp+0x8] at call",
    }

    args = {reg: base.resolve_reg(img, block, local_call_idx, reg) for reg in ("rdi", "rsi", "rdx", "rcx", "r8", "r9")}
    result["connection_register_arguments"] = args

    signal_stack = args["rsi"].get("stack_displacement_value") if args["rsi"].get("classification") == "STACK_ADDRESS" else None
    if signal_stack is not None:
        signal_store = latest_stack_source(img, block, local_call_idx, int(signal_stack))
        result["signal_pointer_store"] = signal_store
        result["peer_signal_bound_to_connection"] = base.contains_classification(signal_store, "PEER_FUNCTION") if signal_store else False

    arg7 = latest_stack_source(img, block, local_call_idx, 0)
    arg8 = latest_stack_source(img, block, local_call_idx, 8)
    result["stack_arg7_types_store"] = arg7
    result["stack_arg8_sender_metaobject_store"] = arg8
    result["sender_metaobject_bound_to_connection"] = base.contains_classification(arg8, "METAOBJECT_ANCHOR") if arg8 else False

    # The sender class identity is promoted only if both the exact signal pointer and
    # the explicit connectImpl senderMetaObject argument independently bind this call
    # to the decoded 0x30b68a0 metaobject. The receiver class is intentionally not
    # inferred from object layout or adjacency.
    if result["peer_signal_bound_to_connection"] and result["sender_metaobject_bound_to_connection"] and owner != "UNKNOWN":
        result["sender_endpoint_identity"] = owner
    result["receiver_endpoint_provenance"] = args["rdx"]
    result["slot_object_provenance"] = args["r8"]

    # Keep the exact sendLogin adapter reference in the selected construction block as
    # evidence, but do not call it a bound slot until its dataflow into the slot object
    # is explicitly recoverable.
    result["sendlogin_adapter_reference_in_selected_block"] = len(adapter_refs) == 1
    result["classification"] = "EXACT_LOCAL_QOBJECT_CONNECTIMPL_SELECTED"
    return result


def main() -> None:
    base.analyze_connection = analyze_connection
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = base.analyze(args.client, args.output)
    print("BE4F48_SENDLOGIN_PEER_METAOWNER_V2_ANALYSIS=PASS")
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
