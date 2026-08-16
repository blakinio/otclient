#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_CLIENT_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
EXPECTED_CLIENT_SIZE = 51965216
EXPECTED_SOURCE_RUN = 31944051248
EXPECTED_SOURCE_JOB = 95157306712
EXPECTED_SOURCE_ARTIFACT = 9262800114
EXPECTED_SOURCE_ARTIFACT_ZIP_SHA256 = "30bd87d94088019b42fcf8504dfb6082af53b447547c544fec816e35b86407f3"


def require(value: bool, marker: str) -> None:
    if not value:
        raise SystemExit(f"P2_REPLAY_FAIL={marker}")
    print(f"P2_REPLAY_OK={marker}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--fixture-sha256", required=True)
    args = ap.parse_args()

    require(args.fixture.is_file(), "fixture_present")
    digest = sha256(args.fixture)
    require(digest == args.fixture_sha256, "fixture_exact_head_digest")
    data = json.loads(args.fixture.read_text(encoding="utf-8"))
    require(data["schema_version"] == 2, "schema_v2")

    p = data["provenance"]
    require(p["source_run"] == EXPECTED_SOURCE_RUN, "source_run")
    require(p["source_job"] == EXPECTED_SOURCE_JOB, "source_job")
    require(p["source_artifact_id"] == EXPECTED_SOURCE_ARTIFACT, "source_artifact")
    require(p["source_artifact_zip_sha256"] == EXPECTED_SOURCE_ARTIFACT_ZIP_SHA256, "source_artifact_digest")
    require(p["source_execution"] == "historical_exact_binary_synology_quarantined_for_routing", "historical_routing_provenance")
    require(p["current_hosted_replay_can_upgrade_exact_binary_provenance"] is False, "no_provenance_upgrade")
    require(p["contains_client_binary_bytes"] is False, "no_client_bytes")
    correlations = {x["id"]: x for x in p["correlation_artifacts"]}
    for artifact_id in (9229609330, 9228087310, 9228207514, 9228275973):
        require(artifact_id in correlations, f"correlation_artifact_{artifact_id}")

    client = data["exact_client"]
    require(client["version_mapping"] == "15.32.df7b29", "version_fence")
    require(client["size"] == EXPECTED_CLIENT_SIZE, "size_fence")
    require(client["sha256"] == EXPECTED_CLIENT_SHA256, "sha_fence")

    h = data["historical_exact_binary_result"]
    require(h["semantic_result"] == "POST_SERIALIZATION_PROCESSOR_CHAIN_PROVEN", "historical_semantic_result")
    require(h["persistent_qbuffer_direct_readall"] == "PROVEN", "persistent_qbuffer_readall")
    require(h["first_downstream_consumer"] == "PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80", "first_consumer")
    require(h["first_downstream_transform"] == "PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130", "first_transform")
    require(h["same_message_handoff_to_dualconnection"] == "PROVEN", "same_message_handoff")
    require(h["protocol_stage_order"] == "PROVEN_PARTIAL", "stage_order_partial")
    require(h["framing"] == "PROVEN_PARTIAL", "framing_partial")
    for key in ("sequence", "compression", "encryption", "final_binary_egress"):
        require(h[key] == "UNKNOWN", f"unknown_preserved_{key}")

    stages = data["stage_order"]
    require([s["entry"] for s in stages] == ["0xc2df80", "0xb47130", "0xb56d60", "0xb56970"], "ordered_entries")
    require(stages[1]["input"] == "same message object", "raw_same_message")
    require(stages[2]["input"] == "same post-raw message object", "dual80_same_post_raw")
    require(stages[3]["input"] == "same post-raw message object", "dual78_same_post_raw")

    typed = data["typed_dependencies"]
    raw_stream = typed["raw_processor_this_plus_8_10"]
    require(raw_stream["type"] == "tibia::network::TUnencryptedRawMessageStream", "raw_stream_type")
    require(raw_stream["address_point"] == "0x3084c58", "raw_stream_ap")
    require(raw_stream["rtti"] == "0x3080660", "raw_stream_rtti")
    require(raw_stream["base"] == "QBuffer", "raw_stream_qbuffer_base")

    compression = typed["raw_processor_this_plus_18_20"]
    require(compression["primary_type"] == "shared::TCompressionHelper", "compression_helper_type")
    require(compression["primary_address_point"] == "0x2f69430", "compression_helper_ap")
    require(compression["contained_or_secondary_vptr_type"] == "shared::TZlibInflateWrapper", "zlib_wrapper_type")
    require(compression["secondary_address_point"] == "0x2f69410", "zlib_wrapper_ap")

    sequence = typed["sequence_flow_processor"]
    require(sequence["type"] == "tibia::network::TGameserverNetworkPacketSequenceFlowProcessor", "sequence_processor_type")
    require(sequence["address_point"] == "0x3084d68", "sequence_processor_ap")
    require(sequence["rtti"] == "0x3080678", "sequence_processor_rtti")
    require(sequence["temporal_position_relative_to_raw_and_dual"] == "UNKNOWN", "sequence_order_not_overclaimed")

    framing = data["framing_evidence"]
    require(framing["processor"] == "TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130", "framing_processor")
    require(framing["prepend_header_call"].startswith("0xb47189"), "framing_prepend_header")
    require(framing["alignment_test"] == "0xb47210 test sil,0x7", "framing_mod8_test")
    require(framing["padding_append_call"].startswith("0xb47206"), "framing_padding_append")
    require(framing["header_value_store"].startswith("0xb47285"), "framing_header_store")
    require(framing["alignment_modulus"] == 8, "framing_alignment_8")
    require(framing["classification"] == "PROVEN_PARTIAL", "framing_classification")
    require(framing["pad_byte_semantics"] == "UNKNOWN", "padding_semantics_unknown")
    require(framing["exact_header_semantic_name"] == "UNKNOWN", "header_semantic_name_unknown")

    markers = set(data["instruction_markers"])
    for marker in (
        "197108f: mov QWORD PTR [rax+0x28],rsi",
        "7dd67f: call QWORD PTR [rax+0x10]",
        "7dd693: call QWORD PTR [rax+0x10]",
        "7dd6a7: call QWORD PTR [rax+0x80]",
        "7dd6be: call QWORD PTR [rax+0x78]",
        "c2dfa5: mov rdi,QWORD PTR [rbp+0x18]",
        "c2dfd5: call QIODevice::readAll",
        "b47189: call QByteArray::insert",
        "b47206: call QByteArray::append",
        "b47210: test sil,0x7",
        "b47285: write framing delta byte",
        "b47300: call QByteArray::operator=",
    ):
        require(marker in markers, f"marker_{marker.split(':',1)[0]}")

    egress = data["egress_discriminators"]
    require(egress["dual_precondition_qiodevice_write"]["classification"] == "NOT_FINAL_EGRESS_PROOF", "b4066b_not_egress")
    require(egress["dual_precondition_qiodevice_write"]["direction"] == "UNKNOWN", "b4066b_direction_unknown")
    require(egress["tcp_text_write"]["classification"] == "DISPROVEN_AS_BINARY_GAMEPLAY_SINK", "b46c75_disproven_binary_sink")

    require(not any(data["negative_controls"].values()), "negative_controls")

    result = {
        "schema_version": 2,
        "execution_class": "github_hosted",
        "runtime_access": "none",
        "hosted_replay_consistency": "PROVEN",
        "historical_exact_binary_chain": "PROVEN_WITH_QUARANTINED_ROUTING_PROVENANCE",
        "current_exact_binary_reexecution": "NOT_PERFORMED",
        "current_exact_binary_provenance_upgraded": False,
        "accepted_chain_for_hypothesis_selection": ["0xc2df80", "0xb47130", "0xb56d60", "0xb56970"],
        "typed_dependencies": {
            "raw_stream": "TUnencryptedRawMessageStream@0x3084c58",
            "compression_helper": "TCompressionHelper@0x2f69430",
            "zlib_wrapper": "TZlibInflateWrapper@0x2f69410",
            "sequence_processor": "TGameserverNetworkPacketSequenceFlowProcessor@0x3084d68"
        },
        "classification": {
            "framing": "PROVEN_PARTIAL",
            "sequence": "UNKNOWN",
            "compression": "UNKNOWN",
            "encryption": "UNKNOWN",
            "final_binary_egress": "UNKNOWN"
        },
        "remaining_discriminators": [
            "resolve 0x1832b90 pad-byte generator semantics",
            "prove temporal position of sequence-flow processor relative to raw and dual stages",
            "prove whether and where TCompressionHelper participates in outbound direction",
            "prove final binary QTcpSocket/QIODevice ownership and write edge"
        ],
        "fixture_sha256": digest,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("P2_REPLAY_COMPLETE=true")
    print("P2_REPLAY_HOSTED_CONSISTENCY=PROVEN")
    print("P2_REPLAY_CURRENT_EXACT_BINARY_REEXECUTION=NOT_PERFORMED")
    print("P2_REPLAY_FRAMING=PROVEN_PARTIAL")
    print("P2_REPLAY_SEQUENCE=UNKNOWN")
    print("P2_REPLAY_COMPRESSION=UNKNOWN")
    print("P2_REPLAY_ENCRYPTION=UNKNOWN")
    print("P2_REPLAY_FINAL_BINARY_EGRESS=UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
