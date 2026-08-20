from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Callable, Mapping

from .runtime import EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE, EXPECTED_TARGET_CONTAINER

READER_ID = "player_state_typed_reader"
TYPE_NAME = "tibia::game::TPlayerData"
MANGLED_TYPE_NAME = "N5tibia4game11TPlayerDataE"
POSITION_KEY = "playerPosition"
_STRING = re.compile(r"^\s*([0-9a-fA-F]+)\s+(.+?)\s*$")
_XREF = re.compile(r"^\s*([0-9a-fA-F]+):.*#\s*([0-9a-fA-F]+)\b")
_MOVSLQ = re.compile(r"^\s*([0-9a-fA-F]+):(?:\s+[0-9a-fA-F]{2})*\s+movslq\s+(-?0x[0-9a-fA-F]+)\(%([a-z0-9]+)\),%[a-z0-9]+(?:\s*)$")

@dataclass(frozen=True)
class PlayerStateLayout:
    vptr: int
    metacast: int
    position_xref: int
    offsets: tuple[int, int, int]

    def evidence(self) -> dict[str, object]:
        return {"tplayerdata_vptr_offset": hex(self.vptr), "qt_metacast_offset": hex(self.metacast),
                "position_serializer_xref": hex(self.position_xref), "position_offsets": [hex(v) for v in self.offsets],
                "representation": "signed_i32_x3", "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E"}

class PlayerStateResolverError(RuntimeError):
    pass


def parse_strings(text: str) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for line in text.splitlines():
        m = _STRING.match(line)
        if m:
            out.setdefault(m.group(2), []).append(int(m.group(1), 16))
    return out


def parse_xrefs(text: str, targets: set[int]) -> list[tuple[int, int]]:
    out = []
    for line in text.splitlines():
        m = _XREF.match(line)
        if m:
            pair = (int(m.group(1), 16), int(m.group(2), 16))
            if pair[1] in targets:
                out.append(pair)
    return sorted(set(out))


def parse_relative_relocations(text: str) -> dict[int, int]:
    out: dict[int, int] = {}
    for line in text.splitlines():
        if "R_X86_64_RELATIVE" not in line:
            continue
        parts = line.split()
        if len(parts) >= 4 and re.fullmatch(r"[0-9a-fA-F]+", parts[0]) and re.fullmatch(r"[0-9a-fA-F]+", parts[-1]):
            out[int(parts[0], 16)] = int(parts[-1], 16)
    return out

def derive_position_offsets(disassembly: str, *, xref: int) -> tuple[int, int, int]:
    by_base: dict[str, list[tuple[int, int]]] = {}
    for line in disassembly.splitlines():
        m = _MOVSLQ.match(line)
        if not m:
            continue
        address, displacement = int(m.group(1), 16), int(m.group(2), 16)
        if address < xref and xref - address <= 0x240:
            by_base.setdefault(m.group(3), []).append((address, displacement))
    candidates: set[tuple[int, int, int]] = set()
    for loads in by_base.values():
        offsets = sorted({d for _, d in loads if 0 <= d <= 0x1000})
        for first in offsets:
            triple = (first, first + 4, first + 8)
            if all(v in offsets for v in triple):
                addresses = [a for a, d in loads if d in triple]
                if addresses and max(addresses) - min(addresses) <= 0x100:
                    candidates.add(triple)
    if len(candidates) != 1:
        raise PlayerStateResolverError(f"position movslq triplet is not unique: {sorted(candidates)}")
    return next(iter(candidates))


def resolve_layout(*, strings_text: str, relocations_text: str, xrefs_text: str,
                   position_disassembly: Mapping[int, str]) -> PlayerStateLayout:
    strings = parse_strings(strings_text)
    type_strings = set(strings.get(TYPE_NAME, [])); mangled = set(strings.get(MANGLED_TYPE_NAME, []))
    position_strings = set(strings.get(POSITION_KEY, []))
    if not type_strings or not mangled or not position_strings:
        raise PlayerStateResolverError("required TPlayerData/playerPosition strings are missing")
    relative = parse_relative_relocations(relocations_text)
    xrefs = parse_xrefs(xrefs_text, type_strings | position_strings)
    type_xrefs = [src for src, target in xrefs if target in type_strings]
    position_xrefs = [src for src, target in xrefs if target in position_strings]
    if not type_xrefs or not position_xrefs:
        raise PlayerStateResolverError("required static xrefs are missing")
    metacast_candidates: list[tuple[int, int]] = []
    for slot, target in relative.items():
        if not any(0 <= xref - target <= 0x60 for xref in type_xrefs):
            continue
        typeinfo = relative.get(slot - 0x10)
        if typeinfo is None or relative.get(slot - 0x08) is None or relative.get(slot + 0x08) is None:
            continue
        if relative.get(typeinfo + 0x08) in mangled:
            metacast_candidates.append((slot, target))
    if len(metacast_candidates) != 1:
        raise PlayerStateResolverError(f"TPlayerData qt_metacast/vtable candidate is not unique: {metacast_candidates}")
    metacast_slot, metacast = metacast_candidates[0]
    position_candidates = []
    for xref in sorted(set(position_xrefs)):
        text = position_disassembly.get(xref)
        if not text:
            continue
        try:
            offsets = derive_position_offsets(text, xref=xref)
        except PlayerStateResolverError:
            continue
        position_candidates.append((xref, offsets))
    if len(position_candidates) != 1:
        raise PlayerStateResolverError(f"playerPosition serializer candidate is not unique: {position_candidates}")
    position_xref, offsets = position_candidates[0]
    return PlayerStateLayout(metacast_slot - 0x08, metacast, position_xref, offsets)


CURRENT_LAYOUT = PlayerStateLayout(
    vptr=0x30C1810,
    metacast=0xD40470,
    position_xref=0x82D101,
    offsets=(0x78, 0x7C, 0x80),
)

READ_ONLY_PROBE = r'''
import hashlib,json,os,pathlib,struct,sys
pid=int(sys.argv[1]); start=int(sys.argv[2]); size=int(sys.argv[3]); sha=sys.argv[4]
vptr_off=int(sys.argv[5],16); offsets=tuple(int(x,16) for x in sys.argv[6:9])
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
'''
READ_ONLY_PROBE += r'''
regions=[]
for line in pathlib.Path(f"/proc/{pid}/maps").read_text().splitlines():
 parts=line.split(maxsplit=5); begin,end=(int(x,16) for x in parts[0].split("-"))
 regions.append((begin,end,parts[1],int(parts[2],16),parts[5] if len(parts)==6 else ""))
bases=[begin-off for begin,end,perms,off,path in regions if path==str(exe)]
if not bases: raise SystemExit("CLIENT_MAPPING_MISSING")
expected_vptr=min(bases)+vptr_off
rw=[r for r in regions if r[2].startswith("rw") and 0<r[1]-r[0]<=512*1024*1024]
def in_rw(addr): return any(begin<=addr<end for begin,end,*_ in rw)
fd=os.open(f"/proc/{pid}/mem",os.O_RDONLY|os.O_CLOEXEC)
pat=struct.pack("<Q",expected_vptr); hits=[]
try:
 for begin,end,perms,off,path in rw:
  cur=begin
  while cur<end:
   want=min(1024*1024,end-cur)
   try: data=os.pread(fd,want,cur)
   except OSError: cur+=want; continue
   pos=0
   while True:
    idx=data.find(pat,pos)
    if idx<0: break
    obj=cur+idx
    if obj%8==0:
     try: private=struct.unpack("<Q",os.pread(fd,8,obj+8))[0]
     except Exception: private=0
     if private and in_rw(private): hits.append(obj)
    pos=idx+1
   cur+=len(data) if data else want
 hits=sorted(set(hits))
 if len(hits)!=1: raise SystemExit("TPLAYERDATA_OBJECT_COUNT="+str(len(hits)))
 obj=hits[0]; vals=[]
 for off in offsets: vals.append(struct.unpack("<i",os.pread(fd,4,obj+off))[0])
finally: os.close(fd)
print(json.dumps({"state":"AVAILABLE","reader_id":"player_state_typed_reader","position":{"x":vals[0],"y":vals[1],"z":vals[2]},"object_count":1,"process_memory_access":"read_only","semantic_state":"CANDIDATE_PENDING_CAUSAL_E2E"},sort_keys=True))
'''

def read_player_state(*, pid:int, start_ticks:int, runner:Callable[[list[str]], str], container:str=EXPECTED_TARGET_CONTAINER) -> dict[str, object]:
    layout=CURRENT_LAYOUT
    args=["docker","exec",container,"python3","-c",READ_ONLY_PROBE,str(pid),str(start_ticks),str(EXPECTED_CLIENT_SIZE),EXPECTED_CLIENT_SHA256,hex(layout.vptr),*(hex(v) for v in layout.offsets)]
    try:
        raw=runner(args).strip()
        doc=json.loads(raw)
    except Exception as exc:
        return {"state":"UNAVAILABLE","reader_id":READER_ID,"reason":f"READ_FAILED:{type(exc).__name__}","semantic_promotion_allowed":False}
    doc["layout_evidence"]=layout.evidence(); doc["semantic_promotion_allowed"]=False
    return doc
