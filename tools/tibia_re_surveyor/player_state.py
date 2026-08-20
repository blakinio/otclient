from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Callable, Mapping

from .runtime import EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE, EXPECTED_TARGET_CONTAINER

READER_ID = "player_state_typed_reader"
TYPE_NAME = "tibia::cyclopedia::TCyclopediaMapStorage"
MANGLED_TYPE_NAME = "N5tibia10cyclopedia21TCyclopediaMapStorageE"
POSITION_SIGNAL = "playerPositionChanged"
POSITION_HANDLER = "onPlayerPositionWasUpdated"
_STRING = re.compile(r"^\s*([0-9a-fA-F]+)\s+(.+?)\s*$")
_XREF = re.compile(r"^\s*([0-9a-fA-F]+):.*#\s*([0-9a-fA-F]+)\b")
_STORE_XY = re.compile(r"\bmovq\s+%xmm0,0x([0-9a-fA-F]+)\(%rdi\)")
_STORE_Z = re.compile(r"\bmov\s+%eax,0x([0-9a-fA-F]+)\(%rdi\)")
_INPUT_XY = re.compile(r"\bmovq\s+0x8\(%rax\),%xmm0")
_INPUT_Z = re.compile(r"\bmov\s+0x10\(%rax\),%eax")
_MUTATE_XY = re.compile(r"\bpaddd\s+%xmm1,%xmm0")
_MUTATE_Z = re.compile(r"\badd\s+\$0x1,%eax")


@dataclass(frozen=True)
class PlayerStateLayout:
    vptr: int
    typeinfo: int
    metacast: int
    position_handler: int
    primary_offsets: tuple[int, int, int]
    mirror_offsets: tuple[int, int, int]

    def evidence(self) -> dict[str, object]:
        return {
            "source_object": TYPE_NAME,
            "source_handler": POSITION_HANDLER,
            "source_signal": POSITION_SIGNAL,
            "cyclopedia_vptr_offset": hex(self.vptr),
            "cyclopedia_typeinfo_offset": hex(self.typeinfo),
            "qt_metacast_offset": hex(self.metacast),
            "position_handler_offset": hex(self.position_handler),
            "position_primary_offsets": [hex(v) for v in self.primary_offsets],
            "position_mirror_offsets": [hex(v) for v in self.mirror_offsets],
            "representation": "signed_i32_x3_mirrored",
            "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E",
        }


class PlayerStateResolverError(RuntimeError):
    pass


def parse_strings(text: str) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for line in text.splitlines():
        match = _STRING.match(line)
        if match:
            out.setdefault(match.group(2), []).append(int(match.group(1), 16))
    return out


def parse_xrefs(text: str, targets: set[int]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for line in text.splitlines():
        match = _XREF.match(line)
        if match:
            pair = (int(match.group(1), 16), int(match.group(2), 16))
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


def derive_mirrored_position_offsets(disassembly: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    if not _INPUT_XY.search(disassembly) or not _INPUT_Z.search(disassembly):
        raise PlayerStateResolverError("world-coordinate input loads are missing")
    if not _MUTATE_XY.search(disassembly) or not _MUTATE_Z.search(disassembly):
        raise PlayerStateResolverError("derived-coordinate mutation boundary is missing")

    xy: set[int] = set()
    z: set[int] = set()
    xy_source_live = True
    z_source_live = True
    for line in disassembly.splitlines():
        if _MUTATE_XY.search(line):
            xy_source_live = False
        if _MUTATE_Z.search(line):
            z_source_live = False
        if xy_source_live:
            match = _STORE_XY.search(line)
            if match:
                xy.add(int(match.group(1), 16))
        if z_source_live:
            match = _STORE_Z.search(line)
            if match:
                z.add(int(match.group(1), 16))

    triples = sorted({(base, base + 4, base + 8) for base in xy if base + 8 in z})
    if len(triples) != 2:
        raise PlayerStateResolverError(f"mirrored world-coordinate stores are not unique: {triples}")
    return triples[0], triples[1]


def resolve_layout(
    *,
    strings_text: str,
    relocations_text: str,
    metacast_disassembly: Mapping[int, str],
    position_handler_disassembly: Mapping[int, str],
) -> PlayerStateLayout:
    strings = parse_strings(strings_text)
    type_strings = set(strings.get(TYPE_NAME, []))
    mangled = set(strings.get(MANGLED_TYPE_NAME, []))
    if not type_strings or not mangled or not strings.get(POSITION_SIGNAL) or not strings.get(POSITION_HANDLER):
        raise PlayerStateResolverError("required Cyclopedia player-position strings are missing")

    relative = parse_relative_relocations(relocations_text)
    typeinfos = {slot - 8 for slot, target in relative.items() if target in mangled}
    vptr_candidates: list[tuple[int, int, int]] = []
    for typeinfo_slot, typeinfo in relative.items():
        if typeinfo not in typeinfos:
            continue
        vptr = typeinfo_slot + 8
        first_virtual = relative.get(vptr)
        metacast = relative.get(vptr + 8)
        if first_virtual is None or metacast is None:
            continue
        disassembly = metacast_disassembly.get(metacast, "")
        if parse_xrefs(disassembly, type_strings):
            vptr_candidates.append((vptr, typeinfo, metacast))
    if len(vptr_candidates) != 1:
        raise PlayerStateResolverError(f"Cyclopedia vptr/qt_metacast candidate is not unique: {vptr_candidates}")

    handler_candidates: list[tuple[int, tuple[int, int, int], tuple[int, int, int]]] = []
    for address, disassembly in position_handler_disassembly.items():
        try:
            primary, mirror = derive_mirrored_position_offsets(disassembly)
        except PlayerStateResolverError:
            continue
        handler_candidates.append((address, primary, mirror))
    if len(handler_candidates) != 1:
        raise PlayerStateResolverError(f"position handler candidate is not unique: {handler_candidates}")

    vptr, typeinfo, metacast = vptr_candidates[0]
    handler, primary, mirror = handler_candidates[0]
    return PlayerStateLayout(vptr, typeinfo, metacast, handler, primary, mirror)


def validate_mirrored_position(primary: tuple[int, int, int], mirror: tuple[int, int, int]) -> tuple[int, int, int]:
    if primary != mirror:
        raise PlayerStateResolverError(f"mirrored position mismatch: {primary} != {mirror}")
    x, y, z = primary
    if not (1 <= x <= 65535 and 1 <= y <= 65535 and 0 <= z <= 15):
        raise PlayerStateResolverError(f"implausible Tibia world coordinate: {primary}")
    return primary


CURRENT_LAYOUT = PlayerStateLayout(
    vptr=0x30C2738,
    typeinfo=0x30C0AA0,
    metacast=0xD1EEF0,
    position_handler=0xD19EF0,
    primary_offsets=(0x2F0, 0x2F4, 0x2F8),
    mirror_offsets=(0x408, 0x40C, 0x410),
)


READ_ONLY_PROBE = r'''
import hashlib,json,os,pathlib,struct,sys
pid=int(sys.argv[1]); start=int(sys.argv[2]); size=int(sys.argv[3]); sha=sys.argv[4]
vptr_off=int(sys.argv[5],16)
primary=tuple(int(x,16) for x in sys.argv[6:9]); mirror=tuple(int(x,16) for x in sys.argv[9:12])
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
expected_vptr=min(bases)+vptr_off
rw=[r for r in regions if r[2].startswith("rw") and 0<r[1]-r[0]<=512*1024*1024]
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
     try: private=struct.unpack("<Q",os.pread(fd,8,obj+8))[0]
     except Exception: private=0
     if private and in_rw(private): hits.append(obj)
    pos=idx+1
   tail=merged[-7:]; cur+=len(data)
 hits=sorted(set(hits))
 if len(hits)!=1: raise SystemExit("CYCLOPEDIA_OBJECT_COUNT="+str(len(hits)))
 obj=hits[0]
 def read_triplet(offsets): return tuple(struct.unpack("<i",os.pread(fd,4,obj+off))[0] for off in offsets)
 a=read_triplet(primary); b=read_triplet(mirror)
 if a!=b: raise SystemExit("CYCLOPEDIA_POSITION_MIRROR_MISMATCH")
 x,y,z=a
 if not (1<=x<=65535 and 1<=y<=65535 and 0<=z<=15): raise SystemExit("CYCLOPEDIA_POSITION_IMPLAUSIBLE")
finally: os.close(fd)
print(json.dumps({"state":"AVAILABLE","reader_id":"player_state_typed_reader","position":{"x":x,"y":y,"z":z},"object_count":1,"position_mirror_consistent":True,"process_memory_access":"read_only","semantic_state":"CANDIDATE_PENDING_CAUSAL_E2E"},sort_keys=True))
'''


def read_player_state(*, pid: int, start_ticks: int, runner: Callable[[list[str]], str], container: str = EXPECTED_TARGET_CONTAINER) -> dict[str, object]:
    layout = CURRENT_LAYOUT
    args = [
        "docker", "exec", container, "python3", "-c", READ_ONLY_PROBE,
        str(pid), str(start_ticks), str(EXPECTED_CLIENT_SIZE), EXPECTED_CLIENT_SHA256,
        hex(layout.vptr), *(hex(v) for v in layout.primary_offsets), *(hex(v) for v in layout.mirror_offsets),
    ]
    try:
        raw = runner(args).strip()
        doc = json.loads(raw)
    except Exception as exc:
        return {
            "state": "UNAVAILABLE",
            "reader_id": READER_ID,
            "reason": f"READ_FAILED:{type(exc).__name__}",
            "semantic_promotion_allowed": False,
        }
    doc["layout_evidence"] = layout.evidence()
    doc["semantic_promotion_allowed"] = False
    return doc
