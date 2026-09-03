#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import writer_path as base

QUEUE_MEMBER_OFFSETS = set(range(0x60, 0xD0, 8))
QUEUE_VTABLE_REF_SITES = (0xBE2A72, 0xBE3092)


def rip_refs_to_exact_target(img: base.Image, target: int) -> list[dict[str, Any]]:
    """Re-prove only the two exact-current queue-vtable refs exposed by prior sanitized evidence."""
    out: list[dict[str, Any]] = []
    for site in QUEUE_VTABLE_REF_SITES:
        fde = img.containing_fde(site)
        if fde is None:
            raise RuntimeError(f"no unique FDE for exact queue-vtable ref {base.hx(site)}")
        _, insns = img.fde_instructions(site)
        ins = base.one_at(insns, site)
        if ins.mnemonic != "lea":
            raise RuntimeError(f"expected lea at exact queue-vtable ref {base.hx(site)}")
        resolved = base.rip_target(ins)
        if resolved != target:
            raise RuntimeError(
                f"queue-vtable ref moved at {base.hx(site)}: {base.hx(resolved)} != {base.hx(target)}"
            )
        out.append(
            {
                "at": base.hx(site),
                "mnemonic": ins.mnemonic,
                "operand": ins.op_str,
                "resolved_target": base.hx(resolved),
                "fde": [base.hx(fde[0]), base.hx(fde[1])],
                "context": base.context(insns, site, before=8, after=10),
            }
        )
    return out


def executable_rip_lea_targets(img: base.Image, insns: list[Any]) -> list[dict[str, Any]]:
    from capstone.x86_const import X86_OP_MEM, X86_REG_RIP

    found: dict[int, dict[str, Any]] = {}
    for ins in insns:
        if ins.mnemonic != "lea" or len(ins.operands) < 2:
            continue
        op = ins.operands[1]
        if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
            continue
        target = int(ins.address) + int(ins.size) + int(op.mem.disp)
        if not img.executable(target):
            continue
        fde = img.containing_fde(target)
        if fde is None:
            continue
        row = found.setdefault(
            target,
            {
                "target": base.hx(target),
                "fde": [base.hx(fde[0]), base.hx(fde[1])],
                "refs": [],
            },
        )
        row["refs"].append(
            {
                "at": base.hx(int(ins.address)),
                "operand": ins.op_str,
                "context": base.context(insns, int(ins.address), before=5, after=5),
            }
        )
    return [found[key] for key in sorted(found)]


def relevant_member_accesses(insns: list[Any]) -> list[dict[str, Any]]:
    return [row for row in base.memory_displacements(insns) if int(row["disp"]) in QUEUE_MEMBER_OFFSETS]


def direct_calls_to_targets(insns: list[Any], targets: set[int]) -> list[dict[str, Any]]:
    out = []
    for row in base.direct_calls(insns):
        target = int(row["target"], 16)
        if target in targets:
            out.append(row)
    return out


def full_fde_snapshot(img: base.Image, target: int, limit: int = 900) -> dict[str, Any]:
    bounds, insns = img.fde_instructions(target)
    return {
        "fde": [base.hx(bounds[0]), base.hx(bounds[1])],
        "instructions": [base.insn_record(row) for row in insns[:limit]],
        "direct_calls": base.direct_calls(insns)[:120],
        "indirect_calls": base.indirect_call_rows(insns)[:80],
        "queue_member_accesses": relevant_member_accesses(insns)[:160],
    }


def choose_constructor(
    refs: list[dict[str, Any]], queue_vtable: dict[str, Any]
) -> tuple[tuple[int, int] | None, dict[str, Any]]:
    slot_targets = {
        int(row["target"], 16)
        for row in queue_vtable["slots"]
        if row.get("executable")
    }
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for ref in refs:
        fde = (int(ref["fde"][0], 16), int(ref["fde"][1], 16))
        grouped.setdefault(fde, []).append(ref)
    non_vslot = [fde for fde in grouped if fde[0] not in slot_targets]
    evidence = {
        "queue_vtable_refs": refs,
        "queue_executable_vslot_targets": [base.hx(x) for x in sorted(slot_targets)],
        "non_vslot_reference_fdes": [[base.hx(a), base.hx(b)] for a, b in sorted(non_vslot)],
        "selection_rule": "unique exact-seed queue-vtable reference FDE whose start is not an executable queue vslot target",
    }
    if len(non_vslot) != 1:
        return None, evidence
    return non_vslot[0], evidence


def analyze_callback_target(
    img: base.Image,
    row: dict[str, Any],
    gameclient_slot_targets: set[int],
) -> dict[str, Any]:
    target = int(row["target"], 16)
    bounds, insns = img.fde_instructions(target)
    member_hits = relevant_member_accesses(insns)
    icalls = base.indirect_call_rows(insns)
    object_calls = direct_calls_to_targets(insns, gameclient_slot_targets)
    snapshot = {
        **row,
        "actual_fde": [base.hx(bounds[0]), base.hx(bounds[1])],
        "queue_member_accesses": member_hits[:160],
        "indirect_calls": icalls[:80],
        "direct_calls": base.direct_calls(insns)[:120],
        "direct_calls_to_gameclient_vslots": object_calls,
        "instructions": [base.insn_record(ins) for ins in insns[:900]],
    }
    snapshot["owned_drain_candidate"] = bool(member_hits) and bool(icalls or object_calls)
    return snapshot


def terminalize(result: dict[str, Any], follow: dict[str, Any]) -> None:
    candidates = [row for row in follow["constructor_executable_callbacks"] if row["owned_drain_candidate"]]
    follow["owned_drain_candidate_count"] = len(candidates)
    follow["owned_drain_candidates"] = [
        {"target": row["target"], "fde": row["actual_fde"]} for row in candidates
    ]

    result["final_queue_writer_identified"] = False
    result["final_queue_writer_identity"] = "UNKNOWN"
    result["final_tcp_writer_identified"] = False
    result["final_tcp_writer_identity"] = "UNKNOWN"
    result["final_writer_contract"] = "UNKNOWN"
    result["terminal_result"] = "SOURCE_BLOCKER"

    if follow["constructor_fde"] is None:
        result["FIRST_MISSING_BOUNDARY"] = (
            "TProtocolMessageQueue concrete object -> unique owned constructor/callback provenance"
        )
    elif len(candidates) != 1:
        result["FIRST_MISSING_BOUNDARY"] = (
            "TProtocolMessageQueue constructor -> unique owned drain callback "
            f"(bounded constructor callback candidates={len(candidates)})"
        )
    else:
        candidate = candidates[0]
        if not candidate["direct_calls_to_gameclient_vslots"]:
            result["FIRST_MISSING_BOUNDARY"] = (
                f"owned queue callback {candidate['target']} -> causal consumption of queued "
                "tibia::protobuf::protocol::GameclientMessage object"
            )
        else:
            result["FIRST_MISSING_BOUNDARY"] = (
                f"owned queue callback {candidate['target']} consuming GameclientMessage -> "
                "unique final packet/frame/TCP writer ownership"
            )
    result["next_action"] = (
        "one evidence-derived queue-owner follow-up has been consumed; persist this SOURCE_BLOCKER "
        "and return to clean coordinator promotion rather than broadening source discovery"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", type=Path, required=True)
    ap.add_argument("--base-result", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    raw = args.client.read_bytes()
    if len(raw) != base.EXPECTED_SIZE:
        raise SystemExit("exact-client size mismatch in owned-callback follow-up")
    if hashlib.sha256(raw).hexdigest() != base.EXPECTED_SHA256:
        raise SystemExit("exact-client SHA mismatch in owned-callback follow-up")

    result = json.loads(args.base_result.read_text(encoding="utf-8"))
    exact = result.get("exact_client", {})
    if (
        exact.get("version") != base.EXPECTED_VERSION
        or exact.get("size") != base.EXPECTED_SIZE
        or exact.get("sha256") != base.EXPECTED_SHA256
        or not exact.get("fence_proven")
    ):
        raise SystemExit("base result is not exact-current fenced")
    if result.get("terminal_result") != "SOURCE_BLOCKER":
        raise SystemExit("follow-up is admissible only from the pass-1 SOURCE_BLOCKER")

    img = base.Image(args.client)
    adapter = result["analysis"]["adapter"]
    queue_vtable = adapter["queue_vtable"]
    refs = rip_refs_to_exact_target(img, base.QUEUE_VTABLE_AP)
    constructor_fde, constructor_selection = choose_constructor(refs, queue_vtable)

    follow: dict[str, Any] = {
        "schema": "otclient.track-a.be4f48-final-login-writer.queue-owner-followup.v1",
        "admission_reason": (
            "pass-1 proved GameclientMessage queue insertion but found zero vtable-local drain candidates; "
            "follow only exact queue vtable ownership into its unique non-vslot constructor FDE"
        ),
        "queue_vtable_address_point": base.hx(base.QUEUE_VTABLE_AP),
        "constructor_selection": constructor_selection,
        "constructor_fde": [base.hx(constructor_fde[0]), base.hx(constructor_fde[1])]
        if constructor_fde
        else None,
        "constructor_snapshot": None,
        "constructor_executable_rip_leas": [],
        "constructor_executable_callbacks": [],
    }

    if constructor_fde is not None:
        ctor_snapshot = full_fde_snapshot(img, constructor_fde[0])
        follow["constructor_snapshot"] = ctor_snapshot
        _, ctor_insns = img.fde_instructions(constructor_fde[0])
        callback_refs = executable_rip_lea_targets(img, ctor_insns)
        follow["constructor_executable_rip_leas"] = callback_refs
        gameclient_slot_targets = {
            int(row["target"], 16)
            for row in adapter["queued_object_vtable"]["slots"]
            if row.get("executable")
        }
        follow["gameclient_executable_vslot_targets"] = [
            base.hx(x) for x in sorted(gameclient_slot_targets)
        ]
        follow["constructor_executable_callbacks"] = [
            analyze_callback_target(img, row, gameclient_slot_targets) for row in callback_refs
        ]

    result["schema"] = "otclient.track-a.be4f48-final-login-writer.source-followup.v1"
    result["analysis"]["queue_owner_followup"] = follow
    result["field6_value"] = "UNKNOWN"
    result["runtime_access"] = "none"
    result["official_client_execution"] = False
    result["login_performed"] = False
    result["credential_access"] = False
    result["process_memory_access"] = False
    result["packet_capture"] = False
    result["official_service_e2e_count"] = 0
    result["raw_client_uploaded"] = False
    result["track_b_pr_284_modified"] = False
    terminalize(result, follow)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("BE4F48_FINAL_LOGIN_WRITER_QUEUE_OWNER_FOLLOWUP=PASS")
    print("TERMINAL_RESULT=" + result["terminal_result"])
    print("FIRST_MISSING_BOUNDARY=" + result["FIRST_MISSING_BOUNDARY"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
