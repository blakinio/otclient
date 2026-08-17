#!/usr/bin/env python3
import base64
import hashlib
import json
import math
import sys
import zlib
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
ALLOWED_BASELINE = {
    "FACT", "INFERENCE", "ASSUMPTION", "RECOMMENDATION", "UNKNOWN",
    "DISPROVEN/SUPERSEDED", "NOT_APPLICABLE_WITH_REASON",
}
ALLOWED_CURRENT = ALLOWED_BASELINE | {"CONFLICT"}


def load_json(name):
    return json.loads((root / name).read_text(encoding="utf-8"))


def jsonl(name):
    return [json.loads(line) for line in (root / name).read_text(encoding="utf-8").splitlines() if line.strip()]


def git_blob_sha1(path):
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def require_classification(obj, where, allowed=ALLOWED_BASELINE):
    value = obj.get("classification")
    assert value in allowed, f"invalid classification {value!r} at {where}"


def provenance_refs(obj):
    value = obj.get("provenance_refs", obj.get("provenance"))
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return []


manifest = load_json("canonical-manifest.json")
assert manifest["schema"] == "otclient.tibia-re.canonical-coverage-registry.v1"
assert manifest["source"]["pr"] == 304
assert manifest["source"]["head"] == "43a60bd96cc644b656b200c9edbfb75578b330b6"
assert manifest["source"]["client"] == {
    "version": "15.32.df7b29",
    "size": 51965216,
    "sha256": "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe",
    "platform": "official_native_linux_only",
}

# Exact source-fence: every accepted baseline/provenance blob must remain byte-for-byte #304 content.
for name, expected in manifest["baseline_git_blob_sha1"].items():
    path = root / name
    assert path.is_file(), f"missing fenced baseline file: {name}"
    actual = git_blob_sha1(path)
    assert actual == expected, f"source baseline drift at {name}: {actual} != {expected}"

provenance = load_json("provenance.json")
source_ids = set(provenance["sources"])
assert source_ids, "provenance source registry is empty"
assert provenance["client_ref"]["sha256"] == manifest["source"]["client"]["sha256"]
assert provenance["client_ref"]["size"] == manifest["source"]["client"]["size"]

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
    assert len(names) == row["count"]
    assert all(name.startswith(row["item_prefix"]) for name in names)
    message_names.extend(names)
assert len(message_names) == len(set(message_names)) == 349
assert sum(x.startswith("GameserverMessage") for x in message_names) == 189
assert sum(x.startswith("GameclientMessage") for x in message_names) == 160

runtime = records["runtime_types.jsonl"]
assert len(runtime) == 1
handlers = runtime[0]["items"]
assert runtime[0]["count"] == len(handlers) == len(set(handlers)) == 47
assert runtime[0]["semantic_default"] == "UNKNOWN"
for key, value in runtime[0].get("negative_evidence", {}).items():
    require_classification(value, f"runtime_types.negative_evidence.{key}")

caps = records["capabilities.jsonl"]
assert len(caps) == 16
assert sorted(int(row["id"].split(":")[1]) for row in caps) == list(range(16))
# Historical next-actions are baseline data, not current routing authority.
assert all(row.get("next") for row in caps)

bridge = records["bridge_fields.jsonl"]
assert len(bridge) == 8
assert sum(row["kind"] == "v1_profile_discovery_target" for row in bridge) == 7

supersessions = records["supersessions.jsonl"]
assert any("b5b880" in row["claim"] and row["classification"] == "DISPROVEN/SUPERSEDED" for row in supersessions)
assert any(row["classification"] == "UNKNOWN" for row in supersessions)

direct_cases = load_json("protocol_direct_qmeta_cases.json")
require_classification(direct_cases, "protocol_direct_qmeta_cases.json")
assert direct_cases["count"] == len(direct_cases["ids"]) == 27
assert len(set(direct_cases["ids"])) == 27
assert all(item in message_names for item in direct_cases["ids"])

gameaction = load_json("gameaction_connects.json")
require_classification(gameaction, "gameaction_connects.json")
assert gameaction["count"] == len(gameaction["items"]) == 31
assert gameaction["summary"] == {"exact": 29, "mismatch": 1, "semantic_edge_default": "UNKNOWN", "unresolved": 1}

legacy = load_json("legacy_qobject_connect_edges.json")
require_classification(legacy, "legacy_qobject_connect_edges.json")
assert legacy["count"] == 41 and legacy["classified"] == 40 and legacy["unclassified"] == 1
covered = []
for group in legacy["groups"]:
    lo, hi = group["ordinals"]
    covered.extend(range(lo, hi + 1))
assert sorted(covered) == list(range(41))

summary = load_json("coverage-summary.json")
assert summary["schema"] == "otclient.tibia-re.coverage-summary.v2"
assert summary["material_findings_after_merge"] == 4
assert summary["high_findings_after_merge"] == 2
assert summary["medium_findings_after_merge"] == 2
assert summary["resolved_by_registry_promotion"] == ["AUD-COV-001"]
assert summary["remaining_findings"] == ["AUD-COV-002", "AUD-COV-003", "AUD-COV-004", "AUD-COV-007"]
for name, metric in summary["metrics"].items():
    require_classification(metric, f"coverage-summary.metrics.{name}", ALLOWED_CURRENT)
    if "numerator" in metric or "denominator" in metric or "percent" in metric:
        numerator = metric.get("numerator")
        denominator = metric.get("denominator")
        percent = metric.get("percent")
        if numerator is None or denominator is None:
            assert percent is None, f"unknown metric must have null percent: {name}"
        else:
            assert denominator > 0 and 0 <= numerator <= denominator
            expected = numerator * 100.0 / denominator
            assert percent is not None and math.isclose(percent, expected, rel_tol=0.0, abs_tol=1e-8)
assert summary["metrics"]["generated_message_semantic_support"]["numerator"] is None
assert summary["metrics"]["generated_message_semantic_support"]["denominator"] == 349
assert summary["metrics"]["p0_live_read_coverage"]["denominator"] is None
assert summary["metrics"]["p1_overall_field_to_evidence_coverage"]["denominator"] is None
assert summary["metrics"]["p2_transport_semantics"]["classification"] == "UNKNOWN"

overlay = load_json("current-main-overlay.json")
assert overlay["schema"] == "otclient.tibia-re.coverage-current-overlay.v1"
assert overlay["snapshot_main"] == manifest["trusted_base"]
assert overlay["source_baseline"]["head"] == manifest["source"]["head"]
remaining = overlay["audit"]["remaining_findings"]
assert [row["id"] for row in remaining] == ["AUD-COV-002", "AUD-COV-003", "AUD-COV-004", "AUD-COV-007"]
assert overlay["audit"]["remaining_material_findings"] == 4
assert overlay["audit"]["remaining_high"] == 2
assert overlay["audit"]["remaining_medium"] == 2
assert overlay["p2"]["protocol_stage_order"] == "PROVEN_PARTIAL"
for key in ("framing", "sequence", "compression", "encryption", "final_binary_egress", "final_socket_ownership"):
    assert overlay["p2"][key] == "UNKNOWN"
assert overlay["worldmap"]["mutation_design_ready"] is True
assert overlay["worldmap"]["safe_mutation_proven"] is False
assert overlay["worldmap"]["physical_validation_execution_authorized"] is False
assert overlay["runtime"]["raw_xres_promotion_merged"] is False
assert overlay["runtime"]["exact_resource_to_official_client_pid"] == "UNKNOWN"
assert overlay["runtime"]["current_exact_client_pid"] == "NOT_REGISTERED"
assert overlay["programme"]["complete"] is False

blockers = load_json("blockers.json")
assert blockers["resolved"][0]["id"] == "AUD-COV-001"
assert [row[0] for row in blockers["items"]] == ["AUD-COV-002", "AUD-COV-003", "AUD-COV-004", "AUD-COV-007"]
assert all(len(row) == 3 and all(row) for row in blockers["items"])

# The promoted report must agree with the machine-readable overlay.
repo_root = root.parents[3]
report = (repo_root / "docs/agents/reports/OTCLIENT-20260816-track-a-coverage-audit-refresh.md").read_text(encoding="utf-8")
assert "material_findings_open: 4" in report
assert "high_findings_open: 2" in report
assert "medium_findings_open: 2" in report
assert "AUD-COV-001 — RESOLVED" in report
for finding in ("AUD-COV-002", "AUD-COV-003", "AUD-COV-004", "AUD-COV-007"):
    assert f"### {finding}" in report
assert "programme_complete: false" in report

print("CANONICAL_COVERAGE_REGISTRY_VALIDATION=PASS")
print("SOURCE_BASELINE_BLOBS_EXACT=true")
print("PROTOCOL_MESSAGES=349 inbound=189 outbound=160 semantics=UNKNOWN/349")
print("PROTOCOL_HANDLER_QMETA=47 full_runtime_semantics=UNKNOWN")
print("P0_GROUPS=16 item_level_live_read=UNKNOWN/UNKNOWN")
print("P1_ITEM_LEVEL=UNKNOWN/UNKNOWN")
print("AUD_COV_001=RESOLVED_IN_CANDIDATE_TREE")
print("REMAINING_FINDINGS=4 high=2 medium=2")
