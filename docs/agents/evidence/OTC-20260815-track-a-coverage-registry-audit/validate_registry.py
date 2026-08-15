#!/usr/bin/env python3
import base64,hashlib,json,sys,zlib
from pathlib import Path
r=Path(sys.argv[1] if len(sys.argv)>1 else ".")
def jl(n): return [json.loads(x) for x in (r/n).read_text().splitlines() if x.strip()]
p=jl("protocol_messages.jsonl")
assert len(p)==2 and sum(x["count"] for x in p)==349
names=[]
for x in p:
    raw=zlib.decompress(base64.b64decode(x["items_zlib_b64"]))
    assert hashlib.sha256(raw).hexdigest()==x["items_raw_sha256"]
    xs=raw.decode().splitlines()
    assert len(xs)==x["count"] and all(v.startswith(x["item_prefix"]) for v in xs)
    names+=xs
assert len(names)==len(set(names))==349
dq=json.loads((r/"protocol_direct_qmeta_cases.json").read_text()); assert dq["count"]==len(dq["ids"])==27 and all(x in names for x in dq["ids"])
rt=jl("runtime_types.jsonl"); assert len(rt)==1 and rt[0]["count"]==len(rt[0]["items"])==47
caps=jl("capabilities.jsonl"); assert len(caps)==16 and sorted(int(x["id"].split(":")[1]) for x in caps)==list(range(16))
b=jl("bridge_fields.jsonl"); assert len(b)==8 and sum(x["kind"]=="v1_profile_discovery_target" for x in b)==7
g=json.loads((r/"gameaction_connects.json").read_text()); assert g["count"]==len(g["items"])==31 and g["summary"]=={"exact":29,"mismatch":1,"semantic_edge_default":"UNKNOWN","unresolved":1}
l=json.loads((r/"legacy_qobject_connect_edges.json").read_text()); assert l["count"]==41 and l["classified"]==40 and l["unclassified"]==1
s=jl("supersessions.jsonl"); assert any("b5b880" in x["claim"] and x["classification"]=="DISPROVEN/SUPERSEDED" for x in s)
c=json.loads((r/"coverage-summary.json").read_text()); m=c["metrics"]
assert m["protocol_identifier_inventory"]["numerator"]==m["protocol_identifier_inventory"]["denominator"]==349
assert m["generated_message_semantic_support"]["numerator"] is None and m["generated_message_semantic_support"]["denominator"]==349
assert m["direct_qt_connection_raw_census"]["denominator"]==2184 and m["direct_qt_connection_semantic_classification"]["numerator"] is None
assert m["p0_top_level_group_registry"]["denominator"]==16 and m["p0_live_read_coverage"]["denominator"] is None
assert m["p1_overall_field_to_evidence_coverage"]["denominator"] is None and m["p2_chain_closure"]["denominator"]==5
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
