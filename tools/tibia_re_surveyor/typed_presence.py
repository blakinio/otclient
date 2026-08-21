from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Callable, Mapping

from .player_state import parse_relative_relocations, parse_strings
from .runtime import EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE, EXPECTED_TARGET_CONTAINER


class TypedPresenceResolverError(RuntimeError):
    pass


@dataclass(frozen=True)
class TypedPresenceLayout:
    type_name: str
    mangled_name: str
    vptr: int
    typeinfo: int

    def evidence(self) -> dict[str, object]:
        return {
            "type_name": self.type_name,
            "mangled_name": self.mangled_name,
            "vptr_offset": hex(self.vptr),
            "typeinfo_offset": hex(self.typeinfo),
            "representation": "exact_rtti_primary_vptr_object_identity",
        }


def resolve_primary_vptr(
    *,
    strings_text: str,
    relocations_text: str,
    type_name: str,
    mangled_name: str,
) -> TypedPresenceLayout:
    strings = parse_strings(strings_text)
    if not strings.get(type_name):
        raise TypedPresenceResolverError(f"missing type string: {type_name}")
    mangled = set(strings.get(mangled_name, []))
    if not mangled:
        raise TypedPresenceResolverError(f"missing mangled type string: {mangled_name}")
    relative = parse_relative_relocations(relocations_text)
    typeinfos = {slot - 8 for slot, target in relative.items() if target in mangled}
    candidates: list[tuple[int, int]] = []
    for slot, target in relative.items():
        if target not in typeinfos:
            continue
        vptr = slot + 8
        if relative.get(vptr) is None:
            continue
        candidates.append((vptr, target))
    candidates = sorted(set(candidates))
    if len(candidates) != 1:
        raise TypedPresenceResolverError(
            f"primary vptr is not unique for {type_name}: {candidates!r}"
        )
    vptr, typeinfo = candidates[0]
    return TypedPresenceLayout(type_name, mangled_name, vptr, typeinfo)


READ_ONLY_PRESENCE_PROBE = r'''
import hashlib,json,os,pathlib,struct,sys
pid=int(sys.argv[1]); start=int(sys.argv[2]); size=int(sys.argv[3]); sha=sys.argv[4]
vptr_off=int(sys.argv[5],16); reader_id=sys.argv[6]; type_name=sys.argv[7]
def ticks():
 raw=pathlib.Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
 return int(raw[raw.rfind(")")+2:].split()[19])
def digest(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
if ticks()!=start: raise SystemExit("START_TICKS_MISMATCH")
exe=pathlib.Path(os.path.realpath(f"/proc/{pid}/exe"))
if exe.stat().st_size!=size or digest(exe)!=sha: raise SystemExit("EXACT_FENCE_MISMATCH")
regions=[]
for line in pathlib.Path(f"/proc/{pid}/maps").read_text().splitlines():
 parts=line.split(maxsplit=5); begin,end=(int(x,16) for x in parts[0].split("-"))
 regions.append((begin,end,parts[1],int(parts[2],16),parts[5] if len(parts)==6 else ""))
bases=[begin-off for begin,end,perms,off,path in regions if path==str(exe)]
if not bases: raise SystemExit("CLIENT_MAPPING_MISSING")
base=min(bases); expected_vptr=base+vptr_off
rw=[r for r in regions if r[2].startswith("rw") and 0 < r[1]-r[0] <= 512*1024*1024]
if not rw: raise SystemExit("NO_BOUNDED_RW_MAPPINGS")
if sum(end-begin for begin,end,*_ in rw) > 1536*1024*1024: raise SystemExit("RW_SCAN_BOUND_EXCEEDED")
def in_rw(addr): return any(begin<=addr<end for begin,end,*_ in rw)
fd=os.open(f"/proc/{pid}/mem",os.O_RDONLY|os.O_CLOEXEC)
pat=struct.pack("<Q",expected_vptr); hits=[]
try:
 for begin,end,perms,off,path in rw:
  cur=begin; tail=b""
  while cur<end:
   want=min(1024*1024,end-cur)
   try: data=os.pread(fd,want,cur)
   except OSError: cur+=want; tail=b""; continue
   if not data: cur+=want; tail=b""; continue
   merged=tail+data; merged_base=cur-len(tail); pos=0
   while True:
    idx=merged.find(pat,pos)
    if idx<0: break
    obj=merged_base+idx
    if obj%8==0:
     try: qprivate=struct.unpack("<Q",os.pread(fd,8,obj+8))[0]
     except Exception: qprivate=0
     if qprivate and in_rw(qprivate): hits.append(obj)
    pos=idx+1
   tail=merged[-7:]; cur+=len(data)
 hits=sorted(set(hits))
 if len(hits)!=1: raise SystemExit("TYPED_OBJECT_COUNT="+str(len(hits)))
finally:
 os.close(fd)
if ticks()!=start: raise SystemExit("START_TICKS_CHANGED_DURING_READ")
print(json.dumps({
 "state":"AVAILABLE","reader_id":reader_id,"type_name":type_name,
 "object_count":1,"typed_object_identity":"PROVEN","process_memory_access":"read_only"
},sort_keys=True))
'''


def read_typed_presence(
    *,
    reader_id: str,
    type_name: str,
    mangled_name: str,
    pid: int,
    start_ticks: int,
    runner: Callable[[list[str]], str],
    container: str = EXPECTED_TARGET_CONTAINER,
) -> dict[str, object]:
    try:
        strings_text = runner(
            ["docker", "exec", container, "strings", "-a", "-t", "x", f"/proc/{pid}/exe"]
        )
        relocations_text = runner(
            ["docker", "exec", container, "readelf", "-rW", f"/proc/{pid}/exe"]
        )
        layout = resolve_primary_vptr(
            strings_text=strings_text,
            relocations_text=relocations_text,
            type_name=type_name,
            mangled_name=mangled_name,
        )
        raw = runner(
            [
                "docker", "exec", container, "python3", "-c", READ_ONLY_PRESENCE_PROBE,
                str(pid), str(start_ticks), str(EXPECTED_CLIENT_SIZE), EXPECTED_CLIENT_SHA256,
                hex(layout.vptr), reader_id, type_name,
            ]
        ).strip()
        doc = json.loads(raw)
    except Exception as exc:
        return {
            "state": "UNAVAILABLE",
            "reader_id": reader_id,
            "reason": f"READ_FAILED:{type(exc).__name__}",
            "semantic_promotion_allowed": False,
        }
    doc["layout_evidence"] = layout.evidence()
    doc["semantic_promotion_allowed"] = False
    return doc
