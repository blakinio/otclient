#!/usr/bin/env python3
import base64, hashlib, json, math, sys, zlib
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
ALLOWED = {"FACT","INFERENCE","ASSUMPTION","RECOMMENDATION","UNKNOWN","DISPROVEN/SUPERSEDED","NOT_APPLICABLE_WITH_REASON"}

def load(name): return json.loads((root / name).read_text(encoding="utf-8"))
def jl(name): return [json.loads(x) for x in (root / name).read_text(encoding="utf-8").splitlines() if x.strip()]
def blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
def refs(row):
    value = row.get("provenance_refs", row.get("provenance"))
    if isinstance(value, str): return [value]
    return value if isinstance(value, list) else []

manifest = load("canonical-manifest.json")
assert manifest["schema"] == "otclient.tibia-re.canonical-coverage-registry.v1"
assert manifest["source"]["pr"] == 304
assert manifest["source"]["head"] == "43a60bd96cc644b656b200c9edbfb75578b330b6"
assert manifest["source"]["client"]["sha256"] == "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
assert manifest["source"]["client"]["size"] == 51965216
for name, expected in manifest["baseline_git_blob_sha1"].items():
    path = root / name
    assert path.is_file(), f"missing fenced baseline {name}"
    assert blob_sha(path) == expected, f"baseline drift: {name}"

provenance = load("provenance.json")
source_ids = set(provenance["sources"])
assert source_ids and provenance["client_ref"]["sha256"] == manifest["source"]["client"]["sha256"]

record_files = ["protocol_messages.jsonl","runtime_types.jsonl","capabilities.jsonl","bridge_fields.jsonl","supersessions.jsonl"]
records = {name: jl(name) for name in record_files}
ids = []
for name, rows in records.items():
    for i, row in enumerate(rows, 1):
        assert row.get("classification") in ALLOWED, f"classification {name}:{i}"
        assert row.get("id"), f"missing id {name}:{i}"
        ids.append(row["id"])
        r = refs(row)
        assert r and set(r) <= source_ids, f"provenance {name}:{i}"
assert len(ids) == len(set(ids))

protocol = records["protocol_messages.jsonl"]
assert len(protocol) == 2 and sum(x["count"] for x in protocol) == 349
names = []
for row in protocol:
    raw = zlib.decompress(base64.b64decode(row["items_zlib_b64"]))
    assert hashlib.sha256(raw).hexdigest() == row["items_raw_sha256"]
    part = raw.decode().splitlines()
    assert len(part) == row["count"] and all(x.startswith(row["item_prefix"]) for x in part)
    names.extend(part)
assert len(names) == len(set(names)) == 349
assert sum(x.startswith("GameserverMessage") for x in names) == 189
assert sum(x.startswith("GameclientMessage") for x in names) == 160

runtime = records["runtime_types.jsonl"]
assert len(runtime) == 1 and runtime[0]["count"] == len(set(runtime[0]["items"])) == 47
assert runtime[0]["semantic_default"] == "UNKNOWN"
caps = records["capabilities.jsonl"]
assert len(caps) == 16 and sorted(int(x["id"].split(":")[1]) for x in caps) == list(range(16))
assert len(records["bridge_fields.jsonl"]) == 8
assert any("b5b880" in x["claim"] and x["classification"] == "DISPROVEN/SUPERSEDED" for x in records["supersessions.jsonl"])
assert any(x["classification"] == "UNKNOWN" for x in records["supersessions.jsonl"])

direct = load("protocol_direct_qmeta_cases.json")
assert direct["classification"] in ALLOWED and direct["count"] == len(set(direct["ids"])) == 27
assert all(x in names for x in direct["ids"])
gameaction = load("gameaction_connects.json")
assert gameaction["classification"] in ALLOWED and gameaction["count"] == len(gameaction["items"]) == 31
assert gameaction["summary"] == {"exact":29,"mismatch":1,"semantic_edge_default":"UNKNOWN","unresolved":1}
legacy = load("legacy_qobject_connect_edges.json")
assert legacy["classification"] in ALLOWED and legacy["count"] == 41 and legacy["classified"] == 40 and legacy["unclassified"] == 1

summary = load("coverage-summary.json")
assert summary["schema"] == "otclient.tibia-re.coverage-summary.v2"
assert (summary["material_findings_after_merge"], summary["high_findings_after_merge"], summary["medium_findings_after_merge"]) == (4,2,2)
assert summary["resolved_by_registry_promotion"] == ["AUD-COV-001"]
assert summary["remaining_findings"] == ["AUD-COV-002","AUD-COV-003","AUD-COV-004","AUD-COV-007"]
for name, metric in summary["metrics"].items():
    assert metric.get("classification") in ALLOWED, f"summary classification {name}"
    if any(k in metric for k in ("numerator","denominator","percent")):
        n, d, p = metric.get("numerator"), metric.get("denominator"), metric.get("percent")
        if n is None or d is None: assert p is None
        else:
            assert d > 0 and 0 <= n <= d
            assert p is not None and math.isclose(p, n * 100.0 / d, rel_tol=0.0, abs_tol=1e-8)
assert summary["metrics"]["generated_message_semantic_support"]["numerator"] is None
assert summary["metrics"]["p0_live_read_coverage"]["denominator"] is None
assert summary["metrics"]["p1_overall_field_to_evidence_coverage"]["denominator"] is None
assert summary["metrics"]["p2_transport_semantics"]["classification"] == "UNKNOWN"

overlay = load("current-main-overlay.json")
assert overlay["snapshot_main"] == manifest["trusted_base"]
assert [x["id"] for x in overlay["audit"]["remaining_findings"]] == ["AUD-COV-002","AUD-COV-003","AUD-COV-004","AUD-COV-007"]
assert (overlay["audit"]["remaining_material_findings"], overlay["audit"]["remaining_high"], overlay["audit"]["remaining_medium"]) == (4,2,2)
for key in ("framing","sequence","compression","encryption","final_binary_egress","final_socket_ownership"):
    assert overlay["p2"][key] == "UNKNOWN"
assert overlay["worldmap"]["mutation_design_ready"] is True
assert overlay["worldmap"]["safe_mutation_proven"] is False
assert overlay["worldmap"]["physical_validation_execution_authorized"] is False
assert overlay["runtime"]["raw_xres_promotion_merged"] is True
assert overlay["runtime"]["raw_xres_promotion_merge"] == "d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab"
assert overlay["runtime"]["exact_resource_to_official_client_pid"] == "UNKNOWN"
assert overlay["runtime"]["current_exact_client_pid"] == "NOT_REGISTERED"
assert overlay["runtime"]["canonical_gate_b"] == "NOT_PROVEN"
assert overlay["programme"]["complete"] is False

blockers = load("blockers.json")
assert blockers["resolved"][0]["id"] == "AUD-COV-001"
assert [x[0] for x in blockers["items"]] == ["AUD-COV-002","AUD-COV-003","AUD-COV-004","AUD-COV-007"]

repo = root.parents[3]
report = (repo / "docs/agents/reports/OTCLIENT-20260816-track-a-coverage-audit-refresh.md").read_text(encoding="utf-8")
for text in ("material_findings_open: 4","high_findings_open: 2","medium_findings_open: 2","AUD-COV-001 — RESOLVED","canonical_raw_xres_helper_promoted: true","programme_complete: false"):
    assert text in report, f"report mismatch: {text}"
for finding in ("AUD-COV-002","AUD-COV-003","AUD-COV-004","AUD-COV-007"):
    assert f"### {finding}" in report

print("CANONICAL_COVERAGE_REGISTRY_VALIDATION=PASS")
print("SOURCE_BASELINE_BLOBS_EXACT=true")
print("PROTOCOL_MESSAGES=349 inbound=189 outbound=160 semantics=UNKNOWN/349")
print("PROTOCOL_HANDLER_QMETA=47 full_runtime_semantics=UNKNOWN")
print("P0_GROUPS=16 item_level_live_read=UNKNOWN/UNKNOWN")
print("P1_ITEM_LEVEL=UNKNOWN/UNKNOWN")
print("RAW_XRES_HELPER_PROMOTED=true physical_xid_pid=UNKNOWN")
print("AUD_COV_001=RESOLVED_IN_CANDIDATE_TREE")
print("REMAINING_FINDINGS=4 high=2 medium=2")
