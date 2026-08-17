#!/usr/bin/env python3
import base64, hashlib, json, math, sys, zlib
from collections import Counter
from pathlib import Path

root=Path(sys.argv[1] if len(sys.argv)>1 else ".")
BASE_ALLOWED={"FACT","INFERENCE","ASSUMPTION","RECOMMENDATION","UNKNOWN","DISPROVEN/SUPERSEDED","NOT_APPLICABLE_WITH_REASON"}
SUMMARY_ALLOWED=BASE_ALLOWED|{"CONFLICT"}
def load(n):return json.loads((root/n).read_text(encoding="utf-8"))
def jl(n):return [json.loads(x) for x in (root/n).read_text(encoding="utf-8").splitlines() if x.strip()]
def blob_sha(p):
    d=p.read_bytes();return hashlib.sha1(f"blob {len(d)}\0".encode()+d).hexdigest()
def pct(n,d):return n*100.0/d

manifest=load("canonical-manifest.json")
assert manifest["schema"]=="otclient.tibia-re.canonical-coverage-registry.v1"
assert manifest["source"]["head"]=="43a60bd96cc644b656b200c9edbfb75578b330b6"
assert manifest["source"]["client"]["sha256"]=="e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
for name,expected in manifest["baseline_git_blob_sha1"].items():
    assert (root/name).is_file() and blob_sha(root/name)==expected,f"baseline drift: {name}"

protocol=jl("protocol_messages.jsonl");names=[]
assert len(protocol)==2 and sum(x["count"] for x in protocol)==349
for row in protocol:
    raw=zlib.decompress(base64.b64decode(row["items_zlib_b64"]));assert hashlib.sha256(raw).hexdigest()==row["items_raw_sha256"]
    part=raw.decode().splitlines();assert len(part)==row["count"];names.extend(part)
assert len(names)==len(set(names))==349
assert sum(x.startswith("GameserverMessage") for x in names)==189
assert sum(x.startswith("GameclientMessage") for x in names)==160
direct=load("protocol_direct_qmeta_cases.json");assert direct["count"]==len(set(direct["ids"]))==27 and set(direct["ids"])<=set(names)

e51=jl("protocol_message_semantics.jsonl")
assert len(e51)==349==len({x["id"] for x in e51})
assert {x["identifier"] for x in e51}==set(names)
assert Counter(x["direction"] for x in e51)==Counter({"server_to_client":189,"client_to_server":160})
assert all(x["denominator_membership"]=="INCLUDED" and x["semantic_state"]=="UNKNOWN" for x in e51)
assert all(x["family"] and x["family_classification"] in {"LEXICAL_NORMALIZATION","UNCLASSIFIED"} for x in e51)
assert {x["identifier"] for x in e51 if x["direct_qmeta_structural_link"]}==set(direct["ids"])

e52=jl("runtime_type_semantics.jsonl")
assert len(e52)==642==len({x["id"] for x in e52})==len({x["type_name"] for x in e52})==len({x["qmeta_record_va"] for x in e52})
assert all(x["type_name"].startswith("tibia::") and x["scope_decision"]=="INCLUDED_TIBIA_QMETA" for x in e52)
assert all(x["semantic_state"]=="UNKNOWN" and x["denominator_membership"]=="INCLUDED" for x in e52)
assert Counter(x["kind_detail"] for x in e52)==Counter({"OTHER_QMETA":303,"CONTROLLER":187,"STORAGE":77,"HANDLER":47,"ACTION_HANDLER":28})
for x in e52:
    p=x["provenance"][0];assert (p["run"],p["job"],p["source_head"])==(31790507112,94736106350,"c04ff82918f954af019ab533bf6af0792dc730bf")

p0=jl("p0_items.jsonl");assert len(p0)==180==len({x["id"] for x in p0})
assert set(x["group"] for x in p0)==set(range(16)) and all(x["denominator_membership"]=="INCLUDED" for x in p0)
assert all(x["classification"]=="REQUIREMENT" and x["semantic_state"]=="UNKNOWN" for x in p0)
assert Counter(x["kind"] for x in p0)==Counter({"READ_OR_STATE":166,"ACTION":14})

p1=jl("p1_items.jsonl");assert len(p1)==28==len({x["id"] for x in p1})
assert sum(x["kind"]=="DISCOVERY_TARGET" for x in p1)==7 and all(x["denominator_membership"]=="INCLUDED" for x in p1)
byid={x["id"]:x for x in p1}
assert byid["p1:session_status.in_game_candidate"]["semantic_state"]=="DERIVED_UNTIL_LIVE_CORRELATION"
assert byid["p1:health.restart_relogin_semantic_reacquisition"]["semantic_state"]=="UNKNOWN"

summary=load("coverage-summary.json")
assert summary["schema"]=="otclient.tibia-re.coverage-summary.v3"
assert summary["current_overlay_snapshot"]=="ec75e2606f7f4ad834e4b6be968fb03bdbff55df"
assert (summary["material_findings_after_merge"],summary["high_findings_after_merge"],summary["medium_findings_after_merge"])==(3,1,2)
assert summary["resolved_findings"]==["AUD-COV-001","AUD-COV-002"]
assert summary["remaining_findings"]==["AUD-COV-003","AUD-COV-004","AUD-COV-007"]
for name,m in summary["metrics"].items():
    assert m.get("classification") in SUMMARY_ALLOWED,f"summary classification: {name}"
    if any(k in m for k in ("numerator","denominator","percent")):
        n,d,p=m.get("numerator"),m.get("denominator"),m.get("percent")
        if n is None or d is None:assert p is None
        else:assert d>0 and 0<=n<=d and p is not None and math.isclose(p,pct(n,d),rel_tol=0,abs_tol=1e-8)
assert summary["metrics"]["protocol_semantic_denominator_registry"]["denominator"]==349 and summary["metrics"]["protocol_semantic_support"]["numerator"] is None
assert summary["metrics"]["full_tibia_qmeta_denominator_registry"]["denominator"]==642 and summary["metrics"]["full_tibia_qmeta_semantic_support"]["numerator"] is None
assert summary["metrics"]["p0_item_denominator_registry"]["denominator"]==180 and summary["metrics"]["p0_live_semantic_coverage"]["numerator"] is None
assert summary["metrics"]["p1_item_denominator_registry"]["denominator"]==28 and summary["metrics"]["p1_live_semantic_coverage"]["numerator"] is None

ov=load("current-main-overlay.json")
assert ov["schema"]=="otclient.tibia-re.coverage-current-overlay.v2" and ov["snapshot_main"]=="ec75e2606f7f4ad834e4b6be968fb03bdbff55df"
assert [x["id"] for x in ov["audit"]["remaining_findings"]]==["AUD-COV-003","AUD-COV-004","AUD-COV-007"]
assert (ov["audit"]["remaining_material_findings"],ov["audit"]["remaining_high"],ov["audit"]["remaining_medium"])==(3,1,2)
assert ov["coverage_boundaries"]["protocol_semantic_denominator"]["denominator"]==349
assert ov["coverage_boundaries"]["full_tibia_qmeta_denominator"]["denominator"]==642
assert ov["coverage_boundaries"]["p0_item_denominator"]["denominator"]==180
assert ov["coverage_boundaries"]["p1_item_denominator"]["denominator"]==28
for k in ("framing","sequence","compression","encryption","final_binary_egress","final_socket_ownership"):assert ov["p2"][k]=="UNKNOWN"
assert ov["worldmap"]["physical_validation_result"]=="NO_HANDLER_CANARY_OBSERVED_BOUNDED" and ov["worldmap"]["causal_propagation_proven"] is False
assert ov["runtime"]["physical_resource_to_exact_client_pid_identity"]=="PROVEN_AT_RUN"
assert ov["runtime"]["canonical_raw_xres_window_identity_integration_merge"]=="f8e628a255a18ec92839bbb45ef0e3b40bef8605"
assert ov["runtime"]["canonical_raw_xres_window_identity_integration_promoted"] is True
assert ov["runtime"]["final_p0_admission_merge"]=="ec75e2606f7f4ad834e4b6be968fb03bdbff55df"
assert ov["runtime"]["final_p0_admission_run"]==32019313320 and ov["runtime"]["final_p0_admission_job"]==95355423148
assert ov["runtime"]["canonical_lease_status"]=="released" and ov["runtime"]["canonical_lease_generation"]==7
assert ov["runtime"]["authoritative_registration"]=="ABSENT"
assert ov["runtime"]["p0_disposition"]=="BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE"
assert ov["runtime"]["current_exact_client_pid"]=="NOT_REGISTERED" and ov["runtime"]["canonical_gate_b"]=="NOT_PROVEN"
assert ov["programme"]["complete"] is False

b=load("blockers.json")
assert [x["id"] for x in b["resolved"]]==["AUD-COV-001","AUD-COV-002"]
assert [x[0] for x in b["items"]]==["AUD-COV-003","AUD-COV-004","AUD-COV-007"]

repo=root.parents[3];report=(repo/"docs/agents/reports/OTCLIENT-20260816-track-a-coverage-audit-refresh.md").read_text()
for t in ("snapshot_main: ec75e2606f7f4ad834e4b6be968fb03bdbff55df","material_findings_open: 3","high_findings_open: 1","medium_findings_open: 2","AUD-COV-002 — RESOLVED","E51 denominator: 349","E52 denominator: 642","P0 item denominator: 180","P1 item denominator: 28","programme_complete: false","BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE"):assert t in report,t

print("CANONICAL_COVERAGE_REGISTRY_VALIDATION=PASS")
print("SOURCE_BASELINE_BLOBS_EXACT=true")
print("E51_DENOMINATOR=349 semantics=UNKNOWN/349 direct_qmeta=27")
print("E52_DENOMINATOR=642 semantics=UNKNOWN/642 handlers=47 action_handlers=28")
print("P0_ITEM_DENOMINATOR=180 semantics=UNKNOWN/180")
print("P1_ITEM_DENOMINATOR=28 live_semantics=UNKNOWN/28")
print("P0_RUNTIME_DISPOSITION=BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE")
print("AUD_COV_002=RESOLVED_AS_DENOMINATOR_COMPLETENESS")
print("REMAINING_FINDINGS=3 high=1 medium=2")
