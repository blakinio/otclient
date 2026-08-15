#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPECTED_CLIENT_SHA = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
EXPECTED_SETUP_FDE = "0x196fee0..0x1972517"
TPROTOCOLWRITER_VPTR = "0x2f69dd0"
TGAMESERVERTCP_VPTR = "0x3084b38"


def require(condition: bool, marker: str) -> None:
    if not condition:
        print(f"P2_WRITER_OWNERSHIP_FAIL={marker}", file=sys.stderr)
        raise SystemExit(2)
    print(f"P2_WRITER_OWNERSHIP_OK={marker}")


def contains_all(text: str, *needles: str) -> bool:
    return all(needle in text for needle in needles)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-text", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    artifact = args.artifact.read_text(errors="replace")
    canonical = args.canonical.read_text(errors="replace")

    require(
        f"CLIENT_SHA256={EXPECTED_CLIENT_SHA}" in artifact,
        "artifact_exact_client_sha",
    )
    require(
        "SELECTED_FDE start=0x196fee0 end=0x1972517 size=0x2637" in artifact,
        "single_setup_fde_present",
    )
    require(
        "TProtocolWriter" in canonical
        and "RTTI: `0x3080728`" in canonical
        and "vtable address point: `0x2f69dd0`" in canonical,
        "canonical_tprotocolwriter_identity",
    )
    require(
        "TIODeviceWriter" in canonical
        and "RTTI: `0x3080718`" in canonical
        and "vtable address point: `0x2f69d48`" in canonical,
        "canonical_tiodevicewriter_identity",
    )
    require(
        "`TProtocolWriter : TIODeviceWriter`" in canonical,
        "canonical_writer_base_edge",
    )
    require(
        "`+0xa00/+0xa08` -> `TProtocolClientMessageProcessor`" in canonical,
        "canonical_client_processor_field",
    )
    require(
        "`+0xa10/+0xa18` -> `TGameserverNetworkPacketRawDataProcessor`" in canonical,
        "canonical_raw_processor_field",
    )
    require(
        "`+0xc18/+0xc20` -> `TGameserverDualConnection`" in canonical,
        "canonical_dualconnection_field",
    )

    dual_connection_sequence = [
        "0x0000000001970757:\tbf e8 00 00 00",
        "# 0x304c460",
        "0x0000000001970798:\t48 8d 43 10",
        "0x00000000019707a2:\te8 89 4c 1e ff",
        "0x00000000019707b5:\t4c 89 b8 18 0c 00 00",
        "0x00000000019707bc:\t48 89 98 20 0c 00 00",
    ]
    require(
        contains_all(artifact, *dual_connection_sequence),
        "dualconnection_retained_at_outer_c18_c20",
    )

    writer_construction_sequence = [
        "0x0000000001970d26:\tbf 28 00 00 00",
        "# 0x304c380",
        "0x0000000001970d63:\t48 8d 0d 66 90 5f 01\tlea    rcx,[rip+0x15f9066]        # 0x2f69dd0",
        "0x0000000001970d6d:\t48 89 4a 10",
        "0x0000000001970d71:\t48 89 5a 18",
        "0x0000000001970d7e:\t48 89 72 20",
    ]
    require(
        contains_all(artifact, *writer_construction_sequence),
        "canonical_tprotocolwriter_constructed_in_setup",
    )

    intermediate_retention_sequence = [
        "0x0000000001970edd:\tbf 50 02 00 00",
        "0x0000000001970efc:\t48 8d 70 10",
        "# 0x2f69e30",
        "0x0000000001970f3b:\t48 89 7a 10",
        "0x0000000001970f3f:\t48 89 72 18",
        "0x0000000001970f43:\t48 89 4a 20",
    ]
    require(
        contains_all(artifact, *intermediate_retention_sequence),
        "retained_object_holds_writer_shared_pair",
    )

    client_processor_sequence = [
        "0x0000000001971033:\tbf 38 00 00 00",
        "# 0x2f6a208",
        "0x0000000001971068:\t48 89 70 18",
        "0x0000000001971076:\t48 89 70 20",
        "0x00000000019710a7:\t48 89 91 00 0a 00 00",
        "0x00000000019710ae:\t48 89 81 08 0a 00 00",
    ]
    require(
        contains_all(artifact, *client_processor_sequence),
        "writer_branch_installed_at_client_processor_field",
    )

    dual_connection_use_sequence = [
        "0x00000000019712ef:\t48 8b 98 18 0c 00 00",
        "0x0000000001971320:\t48 89 de",
        "0x000000000197134f:\t48 89 df",
        "_ZN7QObject11connectImpl",
    ]
    require(
        contains_all(artifact, *dual_connection_use_sequence),
        "dualconnection_used_as_separate_retained_qobject_branch",
    )

    require(
        "`0xb46bd0` is now proven to write through `TGameserverTCPConnection::QTcpSocket*`"
        in canonical
        and "**not** promoted as the binary Tibia gameplay-frame sink" in canonical,
        "negative_control_b46bd0_not_gameplay_sink",
    )
    require(
        "`0xb5b880`" in canonical and "must not be promoted again" in canonical,
        "negative_control_b5b880_superseded",
    )
    require(
        "WRITER_DIRECT_CALL_COUNT=0" in artifact,
        "negative_control_no_direct_b46bd0_call_from_qmeta_refs",
    )

    result = {
        "exact_client_sha256": EXPECTED_CLIENT_SHA,
        "setup_fde": EXPECTED_SETUP_FDE,
        "tprotocolwriter_vptr": TPROTOCOLWRITER_VPTR,
        "tgameservertcpconnection_vptr": TGAMESERVERTCP_VPTR,
        "semantic_result": "PROVEN_WRITER_RETAINED_UPSTREAM_BY_TPROTOCOLCLIENTMESSAGEPROCESSOR",
        "facts": {
            "dualconnection_retained_outer_c18_c20": True,
            "tprotocolwriter_constructed_same_setup_fde": True,
            "writer_shared_pair_retained_by_intermediate_object": True,
            "writer_branch_installed_outer_a00_a08": True,
            "outer_a00_a08_canonical_type": "TProtocolClientMessageProcessor",
            "outer_c18_c20_canonical_type": "TGameserverDualConnection",
        },
        "classification": {
            "common_outer_owner_graph": "FACT",
            "writer_location_relative_to_dualconnection": "UPSTREAM_ON_TPROTOCOLCLIENTMESSAGEPROCESSOR_BRANCH",
            "tprotocolclientmessageprocessor_writer_ownership": "FACT",
            "tgameserverdualconnection_direct_writer_member": "NOT_PROVEN",
            "dualconnection_to_writer_reachability": "INFERENCE_FROM_CANONICAL_OUTBOUND_GRAPH",
            "framing_order": "UNKNOWN",
            "compression_encryption_sequence_boundary": "UNKNOWN",
            "final_binary_egress": "UNKNOWN",
            "causal_local_harness": "UNKNOWN",
        },
        "negative_controls": {
            "b46bd0_binary_gameplay_sink": "DISPROVEN",
            "b5b880_gameplay_endpoint": "SUPERSEDED",
        },
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    args.output_text.write_text(
        "P2_WRITER_OWNERSHIP_RESULT=PROVEN_WRITER_RETAINED_UPSTREAM_BY_TPROTOCOLCLIENTMESSAGEPROCESSOR\n"
        "P2_DIRECT_DUALCONNECTION_WRITER_MEMBER=NOT_PROVEN\n"
        "P2_FRAMING_ORDER=UNKNOWN\n"
        "P2_TRANSFORM_BOUNDARY=UNKNOWN\n"
        "P2_FINAL_BINARY_EGRESS=UNKNOWN\n"
        "P2_CAUSAL_LOCAL_HARNESS=UNKNOWN\n"
    )

    print("P2_WRITER_OWNERSHIP_COMPLETE=true")
    print(
        "P2_WRITER_OWNERSHIP_RESULT="
        "PROVEN_WRITER_RETAINED_UPSTREAM_BY_TPROTOCOLCLIENTMESSAGEPROCESSOR"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
