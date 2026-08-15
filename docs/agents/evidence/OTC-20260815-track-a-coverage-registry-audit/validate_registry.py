#!/usr/bin/env python3
import base64
import hashlib
import json
import math
import sys
import zlib
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
ALLOWED = {
    "FACT", "INFERENCE", "ASSUMPTION", "RECOMMENDATION", "UNKNOWN",
    "DISPROVEN/SUPERSEDED", "NOT_APPLICABLE_WITH_REASON",
}

def jsonl(name):
    return [json.loads(line) for line in (root / name).read_text().splitlines() if line.strip()]

def require_classification(obj, where):
    value = obj.get("classification")
    assert value in ALLOWED, f"invalid classification {value!r} at {where}"

def provenance_refs(obj):
    value = obj.get("provenance_refs", obj.get("provenance"))
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return []

provenance = json.loads((root / "provenance.json").read_text())
source_ids = set(provenance["sources"])
assert source_ids, "provenance source registry is empty"

record_files = [
    "protocol_messages.jsonl", "runtime_types.jsonl", "capabilities.jsonl",
    "bridge_fields.jsonl", "supersessions.jsonl",
]
records = {name: jsonl(name) for name in record_files}
all_record_ids = []
for name, rows in records.items():
    for i, row in enumerate(rows):
        require_classification(row, f"{name}:{i+1}")
        assert row.get("id"), f"missing id at {name}:{i+1}"
        all_record_ids.append(row["id"])
        refs = provenance_refs(row)
        assert refs, f"missing provenance at {name}:{i+1}"
        assert set(refs) <= source_ids, f"unknown provenance refs at {name}:{i+1}: {set(refs)-source_ids}"
assert len(all_record_ids) == len(set(all_record_ids)), "duplicate registry record id"

protocol = records["protocol_messages.jsonl"]
assert len(protocol) == 2 and sum(x["count"] for x in protocol) == 349
message_names = []
for row in protocol:
    raw = zlib.decompress(base64.b64decode(row["items_zlib_b64"]))
    assert hashlib.sha256(raw).hexdigest() == row["items_raw_sha256"]
    names = raw.decode().splitlines()
    assert len(names) == row["count"] and all(n.startswith(row["item_prefix"]) for n in names)
    message_names.extend(names)
assert len(message_names) == len(set(message_names)) == 349, "duplicate protocol identifier"
assert sum(n.startswith("GameserverMessage") for n in message_names) == 189
assert sum(n.startswith("GameclientMessage") for n in message_names) == 160

direct_cases = json.loads((root / "protocol_direct_qmeta_cases.json").read_text())
require_classification(direct_cases, "protocol_direct_qmeta_cases.json")
assert provenance_refs(direct_cases) and set(provenance_refs(direct_cases)) <= source_ids
assert direct_cases["count"] == len(direct_cases["ids"]) == 27
assert len(set(direct_cases["ids"])) == 27 and all(x in message_names for x in direct_cases["ids"])

runtime = records["runtime_types.jsonl"]
assert len(runtime) == 1
handler_items = runtime[0]["items"]
assert runtime[0]["count"] == len(handler_items) == len(set(handler_items)) == 47
for key, value in runtime[0].get("negative_evidence", {}).items():
    require_classification(value, f"runtime_types.negative_evidence.{key}")

caps = records["capabilities.jsonl"]
assert len(caps) == 16
assert sorted(int(x["id"].split(":")[1]) for x in caps) == list(range(16))
assert all(x.get("next") for x in caps), "P0 item missing concrete next hypothesis"

bridge = records["bridge_fields.jsonl"]
assert len(bridge) == 8 and sum(x["kind"] == "v1_profile_discovery_target" for x in bridge) == 7

supersessions = records["supersessions.jsonl"]
assert any("b5b880" in x["claim"] and x["classification"] == "DISPROVEN/SUPERSEDED" for x in supersessions)

gameaction = json.loads((root / "gameaction_connects.json").read_text())
require_classification(gameaction, "gameaction_connects.json")
assert provenance_refs(gameaction) and set(provenance_refs(gameaction)) <= source_ids
assert gameaction["count"] == len(gameaction["items"]) == 31
assert gameaction["summary"] == {"exact": 29, "mismatch": 1, "semantic_edge_default": "UNKNOWN", "unresolved": 1}

legacy = json.loads((root / "legacy_qobject_connect_edges.json").read_text())
require_classification(legacy, "legacy_qobject_connect_edges.json")
assert provenance_refs(legacy) and set(provenance_refs(legacy)) <= source_ids
assert legacy["count"] == 41 and legacy["classified"] == 40 and legacy["unclassified"] == 1
covered_ordinals = []
for group in legacy["groups"]:
    lo, hi = group["ordinals"]
    covered_ordinals.extend(range(lo, hi + 1))
assert sorted(covered_ordinals) == list(range(41)), "legacy ordinal denominator mismatch"

summary = json.loads((root / "coverage-summary.json").read_text())
metrics = summary["metrics"]
for name, metric in metrics.items():
    require_classification(metric, f"coverage-summary.metrics.{name}")
    numerator, denominator, percent = metric.get("numerator"), metric.get("denominator"), metric.get("percent")
    if numerator is None or denominator is None:
        assert percent is None, f"percent must be null for unknown metric {name}"
    else:
        assert denominator > 0 and 0 <= numerator <= denominator, f"invalid denominator arithmetic at {name}"
        expected = numerator * 100.0 / denominator
        assert percent is not None and math.isclose(percent, expected, rel_tol=0.0, abs_tol=1e-8), f"percentage mismatch at {name}"

assert metrics["protocol_identifier_inventory"]["numerator"] == metrics["protocol_identifier_inventory"]["denominator"] == len(message_names) == 349
assert metrics["generated_message_structurally_identified_in_this_registry"]["numerator"] == direct_cases["count"] == 27
assert metrics["generated_message_structurally_identified_in_this_registry"]["denominator"] == 349
assert metrics["generated_message_semantic_support"]["numerator"] is None and metrics["generated_message_semantic_support"]["denominator"] == 349
assert metrics["protocol_handler_qmeta_records"]["numerator"] == metrics["protocol_handler_qmeta_records"]["denominator"] == len(handler_items) == 47
assert metrics["direct_qt_connection_raw_census"]["numerator"] == metrics["direct_qt_connection_raw_census"]["denominator"] == 2184
assert metrics["direct_qt_connection_semantic_classification"]["numerator"] is None and metrics["direct_qt_connection_semantic_classification"]["denominator"] == 2184
assert metrics["legacy_qobject_connect_edges"]["numerator"] == legacy["classified"] and metrics["legacy_qobject_connect_edges"]["denominator"] == legacy["count"]
assert metrics["high_information_gameaction_sender_metaobjects"]["numerator"] == gameaction["summary"]["exact"] and metrics["high_information_gameaction_sender_metaobjects"]["denominator"] == gameaction["count"]
assert metrics["p0_top_level_group_registry"]["numerator"] == metrics["p0_top_level_group_registry"]["denominator"] == len(caps) == 16
assert metrics["p0_live_read_coverage"]["numerator"] is None and metrics["p0_live_read_coverage"]["denominator"] is None
assert metrics["bridge_v1_profile_target_inventory"]["numerator"] == metrics["bridge_v1_profile_target_inventory"]["denominator"] == 7
assert metrics["p1_overall_field_to_evidence_coverage"]["numerator"] is None and metrics["p1_overall_field_to_evidence_coverage"]["denominator"] is None
assert metrics["p2_chain_closure"]["numerator"] is None and metrics["p2_chain_closure"]["denominator"] == 5
assert metrics["restart_relogin_stability"]["numerator"] is None and metrics["restart_relogin_stability"]["denominator"] == 1

blockers = json.loads((root / "blockers.json").read_text())["items"]
assert blockers and all(len(x) == 3 and all(x) for x in blockers), "invalid blocker/next-experiment entry"

print("COVERAGE_AUDIT_VALIDATION=PASS")
print("PROTOCOL_MESSAGES=349 inbound=189 outbound=160")
print("PROTOCOL_HANDLER_QMETA=47")
print("PROTOCOL_STRUCTURAL_ITEM_LINKS=27/349")
print("LEGACY_CONNECT_EDGES=40/41")
print("GAMEACTION_SENDER_METAOBJECTS=29/31 mismatch=1 unresolved=1")
print("DIRECT_QT_RAW_CENSUS=2184 semantic=UNKNOWN")
print("P0_TOP_LEVEL_GROUPS=16/16 live_read_global=UNKNOWN/UNKNOWN")
print("BRIDGE_V1_PROFILE_TARGETS=7/7 overall_p1=UNKNOWN/UNKNOWN")
print("SUPERSEDED_B5B880_RETAINED=true")
