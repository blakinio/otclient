#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_FIXTURE_SHA256 = "__SET_BY_WORKFLOW__"
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
    require(digest == args.fixture_sha256, "fixture_immutable_digest")
    data = json.loads(args.fixture.read_text(encoding="utf-8"))

    p = data["provenance"]
    require(p["source_run"] == EXPECTED_SOURCE_RUN, "source_run")
    require(p["source_job"] == EXPECTED_SOURCE_JOB, "source_job")
    require(p["source_artifact_id"] == EXPECTED_SOURCE_ARTIFACT, "source_artifact")
    require(p["source_artifact_zip_sha256"] == EXPECTED_SOURCE_ARTIFACT_ZIP_SHA256, "source_artifact_digest")
    require(p["source_execution"] == "historical_exact_binary_synology_quarantined_for_routing", "historical_routing_provenance")
    require(p["current_hosted_replay_can_upgrade_exact_binary_provenance"] is False, "no_provenance_upgrade")
    require(p["contains_client_binary_bytes"] is False, "no_client_bytes")

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
    for key in ("framing", "sequence", "compression", "encryption", "final_binary_egress"):
        require(h[key] == "UNKNOWN", f"unknown_preserved_{key}")

    stages = data["stage_order"]
    require([s["entry"] for s in stages] == ["0xc2df80", "0xb47130", "0xb56d60", "0xb56970"], "ordered_entries")
    require(stages[1]["input"] == "same message object", "raw_same_message")
    require(stages[2]["input"] == "same post-raw message object", "dual80_same_post_raw")
    require(stages[3]["input"] == "same post-raw message object", "dual78_same_post_raw")

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
        "b47300: call QByteArray::operator=",
    ):
        require(marker in markers, f"marker_{marker.split(':',1)[0]}")

    nxt = data["next_discriminator_observation"]
    require(nxt["address"] == "0xb4066b", "next_qiodevice_write_address")
    require(nxt["observed_call"] == "QIODevice::write(QByteArray)", "next_qiodevice_write_observed")
    require(nxt["direction"] == "UNKNOWN", "next_direction_unknown")
    require(nxt["outbound_egress_claim"] == "FORBIDDEN_UNTIL_DIRECTION_AND_OWNERSHIP_PROVEN", "no_false_egress_claim")

    require(not any(data["negative_controls"].values()), "negative_controls")

    result = {
        "schema_version": 1,
        "execution_class": "github_hosted",
        "runtime_access": "none",
        "hosted_replay_consistency": "PROVEN",
        "historical_exact_binary_chain": "PROVEN_WITH_QUARANTINED_ROUTING_PROVENANCE",
        "current_exact_binary_reexecution": "NOT_PERFORMED",
        "current_exact_binary_provenance_upgraded": False,
        "accepted_chain_for_hypothesis_selection": ["0xc2df80", "0xb47130", "0xb56d60", "0xb56970"],
        "remaining_unknowns": ["framing", "sequence", "compression", "encryption", "final_binary_egress"],
        "next_discriminator": {
            "function_window": "0xb40370",
            "qiodevice_write_call": "0xb4066b",
            "direction": "UNKNOWN",
            "required_proof": "prove direction plus concrete owning QIODevice/socket before any egress classification"
        },
        "fixture_sha256": digest,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("P2_REPLAY_COMPLETE=true")
    print("P2_REPLAY_HOSTED_CONSISTENCY=PROVEN")
    print("P2_REPLAY_CURRENT_EXACT_BINARY_REEXECUTION=NOT_PERFORMED")
    print("P2_REPLAY_NEXT_DISCRIMINATOR=0xb40370/0xb4066b")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
