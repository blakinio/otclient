#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
import io
import json
import os
import re
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANON = REPO_ROOT / "docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit"
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "semantic-denominator-output")
OUT.mkdir(parents=True, exist_ok=True)

EXACT_CLIENT = {"version":"15.32.df7b29","size":51965216,"sha256":"e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"}
QMETA_JOB=94736106350
QMETA_RUN=31790507112
QMETA_SOURCE_HEAD="c04ff82918f954af019ab533bf6af0792dc730bf"
DIRECT_QMETA=json.loads((CANON/"protocol_direct_qmeta_cases.json").read_text())
DIRECT_QMETA_IDS=set(DIRECT_QMETA["ids"])


def jsonl(path): return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
def write_jsonl(name, rows):
    with (OUT/name).open("w",encoding="utf-8") as f:
        for row in rows: f.write(json.dumps(row,sort_keys=True,separators=(",",":"))+"\n")


def protocol_names():
    out=[]
    for row in jsonl(CANON/"protocol_messages.jsonl"):
        raw=zlib.decompress(base64.b64decode(row["items_zlib_b64"]))
        names=raw.decode().splitlines(); assert len(names)==row["count"]
        out.extend((row["direction"],n) for n in names)
    assert len(out)==349==len({n for _,n in out}); return out


def split_camel(v): return re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+",v)
def lexical_family(name):
    aliases={"Player":"player","Creature":"creature","Container":"container","Map":"map","World":"world","Worldmap":"worldmap","Chat":"chat","Talk":"chat","Channel":"chat","Vip":"social","Friend":"social","Market":"market","Store":"store","Quest":"quest","Prey":"prey","Bestiary":"bestiary","Boss":"boss","Cyclopedia":"cyclopedia","Skill":"skills","Spell":"spells","Combat":"combat","Attack":"combat","Trade":"trade","Npc":"npc","NPC":"npc","Login":"session","Game":"game","Connection":"network","Network":"network","Sound":"sound","Effect":"effect","Tutorial":"tutorial"}
    for prefix in ("GameserverMessage","GameclientMessage"):
        if name.startswith(prefix):
            t=split_camel(name[len(prefix):]); return aliases.get(t[0],t[0].lower()) if t else "UNCLASSIFIED"
    return "UNCLASSIFIED"


def make_e51():
    rows=[]
    for direction,name in sorted(protocol_names(),key=lambda x:(x[0],x[1])):
        family=lexical_family(name)
        rows.append({"id":f"protocol:{name}","identifier":name,"direction":direction,"family":family,"family_classification":"LEXICAL_NORMALIZATION" if family!="UNCLASSIFIED" else "UNCLASSIFIED","semantic_state":"UNKNOWN","direct_qmeta_structural_link":name in DIRECT_QMETA_IDS,"classification":"FACT","denominator_membership":"INCLUDED","provenance":["canonical:protocol_messages.jsonl","canonical:protocol_direct_qmeta_cases.json"],"boundary":"family is deterministic lexical grouping only; semantic support remains UNKNOWN until item-specific proof"})
    assert len(rows)==349; return rows


def fetch_qmeta_log():
    token=os.environ.get("GITHUB_TOKEN","")
    if not token: raise SystemExit("GITHUB_TOKEN is required")
    url=f"https://api.github.com/repos/blakinio/otclient/actions/jobs/{QMETA_JOB}/logs"
    p=subprocess.run(["curl","-fsSL","--max-time","30","-H",f"Authorization: Bearer {token}","-H","Accept: application/vnd.github+json","-H","X-GitHub-Api-Version: 2022-11-28",url],check=True,stdout=subprocess.PIPE)
    data=p.stdout
    if data.startswith(b"PK\x03\x04"):
        zf=zipfile.ZipFile(io.BytesIO(data)); data=b"\n".join(zf.read(n) for n in zf.namelist() if not n.endswith("/"))
    elif data.startswith(b"\x1f\x8b"): data=gzip.decompress(data)
    return data.decode("utf-8",errors="replace")


def make_e52(log):
    qmeta=[]; summary={}
    markers=("TRACK_A_QMETA_STRUCTURAL_RECORD_COUNT=","TRACK_A_QMETA_TIBIA_OWNED_COUNT=","TRACK_A_QMETA_NON_TIBIA_COUNT=","TRACK_A_QMETA_TIBIA_UNCLASSIFIED_COUNT=")
    for line in log.splitlines():
        for marker in markers:
            if marker in line: summary[marker[:-1]]=int(line.split(marker,1)[1].strip().split()[0])
        if "QMETA_JSON " in line: qmeta.append(json.loads(line.split("QMETA_JSON ",1)[1].strip()))
    expected=summary.get("TRACK_A_QMETA_TIBIA_OWNED_COUNT")
    if expected is None or expected!=len(qmeta) or not qmeta: raise SystemExit(f"retained QMeta log parse mismatch expected={expected} parsed={len(qmeta)}")
    rows=[]; seen=set()
    for rec in sorted(qmeta,key=lambda x:(x["type_name"],x["relationships"]["qmeta_record_va"])):
        key=(rec["type_name"],rec["relationships"]["qmeta_record_va"]); assert key not in seen; seen.add(key)
        family=rec.get("feature_family") or "UNCLASSIFIED"
        rows.append({"id":f"qmeta:{rec['relationships']['qmeta_record_va']}:{rec['type_name']}","type_name":rec["type_name"],"namespace":rec.get("namespace",""),"kind_detail":rec.get("kind_detail","OTHER_QMETA"),"feature_family":family,"family_classification":rec.get("classification_status","UNCLASSIFIED"),"method_count":len(rec.get("methods",[])),"signal_count":rec.get("signals_count",0),"property_count":rec.get("properties_count",0),"enum_count":rec.get("enums_count",0),"semantic_state":"UNKNOWN","scope_decision":"INCLUDED_TIBIA_QMETA","classification":"FACT","denominator_membership":"INCLUDED","qmeta_record_va":rec["relationships"]["qmeta_record_va"],"static_metacall_va":rec["relationships"]["static_metacall_va"],"provenance":[{"run":QMETA_RUN,"job":QMETA_JOB,"source_head":QMETA_SOURCE_HEAD}],"boundary":"full retained tibia:: QMeta structural census; semantic role remains UNKNOWN unless separately proven"})
    return rows,summary

P0_GROUPS={
0:("Exact runtime identity",["client_version","client_size","client_sha256","elf_identity","pid","pie_base","loaded_libraries","bridge_compatibility","session_protocol_objects","structural_in_game"]),
1:("Session state machine",["process_started","login_screen","authenticating","character_selection","connecting_game_server","pending_game","entering_world","in_game","connection_lost","logout","recovery"]),
2:("Player core state",["character_id","name","vocation","level","experience","xp_progress","hp","max_hp","hp_percent","mana","max_mana","mana_percent","capacity","soul","speed","base_speed","position_x","position_y","position_z","direction","outfit","mount_state","stamina","premium_account_state","blessings"]),
3:("Skills and combat statistics",["magic_level","skill_values","base_skill_values","effective_skill_values","loyalty_modified_values","skill_progress_percent","combat_statistics"]),
4:("Conditions buffs debuffs",["condition_ids","condition_lifetimes","haste","paralyze","poison","fire","energy","bleeding","drunk","pz_lock","logout_block","invisibility","mana_shield","condition_source","condition_icons","condition_expiry"]),
5:("Cooldowns and exhaustion",["spell_cooldowns","cooldown_groups","item_rune_cooldowns","action_exhaustion","attack_delay","cooldown_start","cooldown_end","cooldown_remaining"]),
6:("Map tile model",["tile_x","tile_y","tile_z","stack_order","ground","items","creatures","effects_projectiles","appearance_type_ids","count_subtype","elevation","blocking","pathability_walkability","usable","movable","pickupable","container_flag","doors","stairs_ramps_floor_transitions","magic_fields","zone_flags"]),
7:("Viewport cache minimap",["rendered_viewport_extent","decoded_known_world_extent","neighbor_floor_cache","minimap_cache","coordinate_coverage","cache_persistence_leave_area","cache_persistence_relog","cache_persistence_restart","offscreen_known_world"]),
8:("Creature registry",["creature_id","creature_name","creature_position_floor","creature_direction","creature_hp_percent","creature_class","creature_outfit_mount_light","creature_speed","creature_skull_shield_party","creature_targetability","creature_visibility","creature_summon_master","creature_lifecycle"]),
9:("Battle list",["battlelist_model_relation","battlelist_entries","battlelist_sort_keys","selected_creature","attacked_creature","followed_creature","battlelist_health","battlelist_distance_floor_filter","battlelist_hidden_offscreen"]),
10:("Combat targeting",["select_target","attack_target","switch_target","cancel_attack","follow_target","cancel_follow","target_disappearance","target_death","target_offscreen","target_floor_change"]),
11:("Combat modes",["stand_chase_mode","offensive_balanced_defensive","secure_mode","pvp_options","combat_mode_local_vs_protocol"]),
12:("Equipment",["equipment_slots","equipment_item_ids","equipment_count_subtype","equipment_tier","equipment_imbuement","equipment_duration_expiry","equipment_charges","equipment_change_event"]),
13:("Containers",["open_container_registry","container_ids","container_names_types","container_parents","container_slots","container_capacity","container_page_index","container_pagination","nested_containers","container_item_updates","container_close_up_seek","multiple_containers","container_id_lifetime_reopen","container_id_lifetime_relog"]),
14:("Item manipulation",["move_within_container","move_between_container_inventory","stack_split_merge","use_item","use_with","use_on_creature","rotate_item","open_item","browse_field"]),
15:("Quick loot and loot state",["quick_loot_configuration","assigned_loot_containers","corpse_interaction_state","loot_messages","loot_item_transfer_events"])}

def make_p0():
    rows=[]
    verbs=("select","attack","switch","cancel","follow","move","use","rotate","open","browse")
    for group,(title,items) in P0_GROUPS.items():
        for item in items:
            rows.append({"id":f"p0:{group:02d}:{item}","group":group,"group_title":title,"item":item,"kind":"ACTION" if group in (10,11,14) and item.startswith(verbs) else "READ_OR_STATE","semantic_state":"UNKNOWN","restart_state":"UNKNOWN","classification":"REQUIREMENT","denominator_membership":"INCLUDED","provenance":"docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md","boundary":"normalized programme requirement; state may advance only with item-specific evidence"})
    assert len(rows)==len({r["id"] for r in rows}); return rows

P1_ITEMS=[("binding.runtime_id","IDENTITY_FIELD"),("binding.registration_generation","IDENTITY_FIELD"),("binding.lease_generation","IDENTITY_FIELD"),("binding.boot_id_sha256","IDENTITY_FIELD"),("binding.pid","IDENTITY_FIELD"),("binding.process_start_ticks","IDENTITY_FIELD"),("binding.client_version","IDENTITY_FIELD"),("binding.client_size","IDENTITY_FIELD"),("binding.client_sha256","IDENTITY_FIELD"),("binding.socket_path","BINDING_FIELD"),("ping.readiness","READ_FIELD"),("ping.identity_envelope_match","READ_FIELD"),("discover.scan_status","READ_FIELD"),("discover.player_protocol_handler","DISCOVERY_TARGET"),("discover.worldmap_handler","DISCOVERY_TARGET"),("discover.gameserver_game_session","DISCOVERY_TARGET"),("discover.player_data","DISCOVERY_TARGET"),("discover.container_storage","DISCOVERY_TARGET"),("discover.creature_storage","DISCOVERY_TARGET"),("discover.game_client","DISCOVERY_TARGET"),("session_status.in_game_candidate","DERIVED_FIELD"),("session_status.evidence_level","DERIVED_FIELD"),("health.state","HEALTH_FIELD"),("health.peer_identity","HEALTH_FIELD"),("health.stale_identity_rejection","LIFECYCLE_EVIDENCE"),("health.same_runtime_reacquisition","LIFECYCLE_EVIDENCE"),("health.changed_runtime_rejection","LIFECYCLE_EVIDENCE"),("health.restart_relogin_semantic_reacquisition","LIFECYCLE_EVIDENCE")]
def make_p1():
    rows=[]
    implemented={"IDENTITY_FIELD","BINDING_FIELD","READ_FIELD","DISCOVERY_TARGET","HEALTH_FIELD"}
    for name,kind in P1_ITEMS:
        state="STRUCTURALLY_IMPLEMENTED" if kind in implemented else "UNKNOWN"
        if name=="session_status.in_game_candidate": state="DERIVED_UNTIL_LIVE_CORRELATION"
        if name.endswith("restart_relogin_semantic_reacquisition"): state="UNKNOWN"
        rows.append({"id":f"p1:{name}","item":name,"kind":kind,"semantic_state":state,"restart_state":"UNKNOWN","classification":"REQUIREMENT","denominator_membership":"INCLUDED","provenance":"tools/tibia_runtime_bridge/README.md","boundary":"normalized P1 bridge/read/evidence requirement; implementation inventory is not live semantic proof"})
    assert len(rows)==len({r["id"] for r in rows}); return rows


def main():
    e51=make_e51(); log=fetch_qmeta_log(); e52,qmeta_summary=make_e52(log); p0=make_p0(); p1=make_p1()
    write_jsonl("protocol_message_semantics.jsonl",e51); write_jsonl("runtime_type_semantics.jsonl",e52); write_jsonl("p0_items.jsonl",p0); write_jsonl("p1_items.jsonl",p1)
    result={"schema":"otclient.tibia-re.semantic-denominators.v1","exact_client":EXACT_CLIENT,"e51":{"denominator":len(e51),"semantic_proven":sum(r["semantic_state"] not in {"UNKNOWN","UNCLASSIFIED"} for r in e51),"unknown":sum(r["semantic_state"]=="UNKNOWN" for r in e51)},"e52":{"denominator":len(e52),"semantic_proven":sum(r["semantic_state"] not in {"UNKNOWN","UNCLASSIFIED"} for r in e52),"unknown":sum(r["semantic_state"]=="UNKNOWN" for r in e52),"retained_summary":qmeta_summary,"source_run":QMETA_RUN,"source_job":QMETA_JOB},"p0":{"denominator":len(p0),"groups":16},"p1":{"denominator":len(p1),"historical_discovery_targets":7},"boundaries":{"denominator_complete_is_not_semantic_complete":True,"unknown_retained":True,"runtime_used":False}}
    (OUT/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("SEMANTIC_DENOMINATOR_GENERATION=PASS"); print(f"E51_DENOMINATOR={len(e51)}"); print(f"E52_DENOMINATOR={len(e52)}"); print(f"P0_ITEM_DENOMINATOR={len(p0)}"); print(f"P1_ITEM_DENOMINATOR={len(p1)}"); print(f"QMETA_SOURCE_RUN={QMETA_RUN} JOB={QMETA_JOB}"); print("DENOMINATOR_COMPLETE_IS_NOT_SEMANTIC_COMPLETE=true")

if __name__=="__main__": main()
