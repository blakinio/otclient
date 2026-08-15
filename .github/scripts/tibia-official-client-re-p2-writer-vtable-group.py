#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CLIENT_SHA = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"


def require(value: bool, marker: str) -> None:
    if not value:
        print(f"P2_VTABLE_GROUP_FAIL={marker}", file=sys.stderr)
        raise SystemExit(2)
    print(f"P2_VTABLE_GROUP_OK={marker}")


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--rtti-artifact", type=Path, required=True)
    p.add_argument("--provenance-artifact", type=Path, required=True)
    p.add_argument("--writer-family-artifact", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def slot(text: str, label: str, rel: str) -> int:
    pattern = rf"^VTABLE_SLOT label={re.escape(label)} address_point=0x[0-9a-f]+ rel={re.escape(rel)} value=0x([0-9a-f]+) exec=[01]$"
    m = re.search(pattern, text, re.MULTILINE)
    require(m is not None, f"slot_{label}_{rel}")
    return int(m.group(1), 16)


def main() -> int:
    ns = args()
    rtti = ns.rtti_artifact.read_text(errors="replace")
    provenance = ns.provenance_artifact.read_text(errors="replace")
    writer_family = ns.writer_family_artifact.read_text(errors="replace")

    for name, text in (("rtti", rtti), ("provenance", provenance), ("writer_family", writer_family)):
        require(f"CLIENT_SHA256={CLIENT_SHA}" in text, f"{name}_exact_client_sha")

    require(
        "RTTI label=TProtocolWriter addr=0x3080728" in rtti
        and "VTABLE label=TProtocolWriter address_point=0x2f69dd0 offset_to_top=0x0 typeinfo=0x3080728" in rtti,
        "canonical_protocol_writer_identity",
    )
    require(
        "RTTI label=TIODeviceWriter addr=0x3080718" in rtti
        and "VTABLE label=TIODeviceWriter address_point=0x2f69d48 offset_to_top=0x0 typeinfo=0x3080718" in rtti,
        "canonical_iodevice_writer_identity",
    )

    # The scanner printed a bounded window following the TProtocolWriter primary address point.
    # Convert those relative entries back to absolute addresses. At +0x50/+0x58/+0x60
    # they form a fresh normal Itanium preamble/address-point tuple.
    offset_to_top = slot(rtti, "TProtocolWriter", "0x50")
    typeinfo = slot(rtti, "TProtocolWriter", "0x58")
    first = slot(rtti, "TProtocolWriter", "0x60")
    second = slot(rtti, "TProtocolWriter", "0x68")
    require(offset_to_top == 0, "adjacent_preamble_offset_to_top_zero")
    require(typeinfo == 0x3080748, "adjacent_preamble_typeinfo_3080748")
    require(first == 0x7DE7F0 and second == 0x7DFD60, "adjacent_address_point_first_slots")
    require(typeinfo != 0x3080728, "adjacent_typeinfo_differs_from_tprotocolwriter")
    require(typeinfo != 0x3080718, "adjacent_typeinfo_differs_from_tiodevicewriter")

    # The setup artifact proves this is not merely scanner overrun: a separately allocated
    # 0x250-byte shared object receives 0x2f69e30 at its object vptr (+0x10).
    setup_needles = [
        "0x0000000001970edd:\tbf 50 02 00 00",
        "0x0000000001970efc:\t48 8d 70 10",
        "0x0000000001970f31:\t48 8d 3d f8 8e 5f 01\tlea    rdi,[rip+0x15f8ef8]        # 0x2f69e30",
        "0x0000000001970f3b:\t48 89 7a 10",
    ]
    require(all(x in provenance for x in setup_needles), "separate_object_receives_2f69e30_vptr")

    # Bound the first two functions as teardown-like only. They both install the same vptr;
    # the first cleans linked/list state and resets object storage. Do not assign a symbol/name.
    teardown_needles = [
        "0x00000000007de7f1:\t48 8d 05 38 b6 78 02\tlea    rax,[rip+0x278b638]        # 0x2f69e30",
        "0x00000000007de807:\t48 89 07",
        "0x00000000007de800:\t48 8b af 18 02 00 00",
        "0x00000000007de826:\t48 8b 83 10 02 00 00",
        "0x00000000007dfd61:\t48 8d 05 c8 a0 78 02\tlea    rax,[rip+0x278a0c8]        # 0x2f69e30",
        "0x00000000007dfd77:\t48 89 07",
    ]
    require(all(x in rtti for x in teardown_needles), "2f69e30_teardown_like_functions")

    # Negative discriminator: the historical b40630 family is a different table/address
    # block, with RTTI zero and no direct LEA provenance in its own exact run.
    require(
        "VTABLE_PLUS_D0_WRITER_B_MATCH address_point=0x3084c70 offset_to_top=0 rtti=0x0" in writer_family,
        "historical_writer_family_structurally_separate",
    )
    require(
        "VTABLE_MATCH_LEA_XREFS address_point=0x3084c70 count=0 sites=none" in writer_family,
        "historical_writer_family_no_direct_lea_provenance",
    )
    require(
        "MATCH_SLOT address_point=0x3084c70 rel=+0xd0 value=0xb40630" in writer_family,
        "historical_writer_family_b40630_slot_retained_as_separate_lead",
    )

    result = {
        "exact_client_sha256": CLIENT_SHA,
        "semantic_result": "PROVEN_DISTINCT_ADJACENT_ITANIUM_VTABLE_IDENTITY_NAME_UNKNOWN",
        "facts": {
            "intermediate_object_vptr": "0x2f69e30",
            "intermediate_offset_to_top": 0,
            "intermediate_typeinfo": "0x3080748",
            "intermediate_typeinfo_differs_from_tprotocolwriter": True,
            "intermediate_typeinfo_differs_from_tiodevicewriter": True,
            "separate_allocated_object_receives_vptr": True,
            "first_functions": ["0x7de7f0", "0x7dfd60"],
            "historical_0x3084c70_family_separate": True,
        },
        "classification": {
            "simple_secondary_vtable_of_tprotocolwriter": "DISPROVEN_BY_DISTINCT_TYPEINFO_AND_SEPARATE_OBJECT",
            "rtti_0x3080748_name": "UNKNOWN",
            "rtti_0x3080748_base_relationship": "UNKNOWN",
            "0x7de7f0_0x7dfd60_role": "INFERENCE_TEARDOWN_LIKE",
            "pr301_intermediate_object_identity": "DISTINCT_TYPED_OBJECT_NAME_UNKNOWN",
            "first_writer_transform_boundary": "UNKNOWN",
            "framing_order": "UNKNOWN",
            "final_binary_egress": "UNKNOWN",
            "0x3084c70_relation_to_canonical_writer_branch": "UNKNOWN_SEPARATE_LEAD",
        },
    }

    ns.output.parent.mkdir(parents=True, exist_ok=True)
    ns.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("P2_VTABLE_GROUP_COMPLETE=true")
    print("P2_VTABLE_GROUP_RESULT=PROVEN_DISTINCT_ADJACENT_ITANIUM_VTABLE_IDENTITY_NAME_UNKNOWN")
    print("P2_FIRST_WRITER_TRANSFORM_BOUNDARY=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
