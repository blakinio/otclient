from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Callable, Mapping

from .player_state import parse_relative_relocations, parse_strings
from .runtime import EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE, EXPECTED_TARGET_CONTAINER

READER_ID = "auth_session_typed_reader"
GAME_CLIENT_TYPE = "tibia::client::TGameClient"
GAME_CLIENT_MANGLED = "N5tibia6client11TGameClientE"
AUTH_CONTROLLER_TYPE = "tibia::authentication::TAuthenticationProcessController"
AUTH_CONTROLLER_MANGLED = "N5tibia14authentication32TAuthenticationProcessControllerE"

QT_STATE_MACHINE_LIBRARY = "libQt6StateMachine.so.6"
QT_STATE_MACHINE_SIZE = 394_824
QT_STATE_MACHINE_SHA256 = "26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8"

_GAME_AUTH_LOAD = re.compile(
    r"\bmov\s+0x([0-9a-fA-F]+)\(%rdi\),%(?:rbx|rax|r12|r13|r14|r15|rbp)\b"
)
_QSTATE_PRIVATE_LOAD = re.compile(r"\bmov\s+0x([0-9a-fA-F]+)\(%rdi\),%rax\b")
_QSTATE_RUNNING_CMP = re.compile(
    r"\bcmpl?\s+\$0x([0-9a-fA-F]+),0x([0-9a-fA-F]+)\(%rax\)\b"
)
_QSTATE_BOOL = re.compile(r"\bsete\s+%al\b")


class AuthSessionResolverError(RuntimeError):
    pass


@dataclass(frozen=True)
class AuthSessionLayout:
    game_client_vptr: int
    game_client_typeinfo: int
    auth_controller_vptr: int
    auth_controller_typeinfo: int
    auth_controller_offset: int
    qstate_private_offset: int
    qstate_state_offset: int
    qstate_running_value: int

    def evidence(self) -> dict[str, object]:
        return {
            "source_object": GAME_CLIENT_TYPE,
            "auth_controller_object": AUTH_CONTROLLER_TYPE,
            "game_client_vptr_offset": hex(self.game_client_vptr),
            "game_client_typeinfo_offset": hex(self.game_client_typeinfo),
            "auth_controller_vptr_offset": hex(self.auth_controller_vptr),
            "auth_controller_typeinfo_offset": hex(self.auth_controller_typeinfo),
            "auth_controller_member_offset": hex(self.auth_controller_offset),
            "qstate_private_offset": hex(self.qstate_private_offset),
            "qstate_state_offset": hex(self.qstate_state_offset),
            "qstate_running_value": self.qstate_running_value,
            "representation": "qt_qstatemachine_isRunning_equivalent",
            "semantic_state": "TYPED_AUTH_LIFECYCLE_ONLY",
            "in_game_claimed": False,
            "credentials_retained": False,
            "session_secrets_retained": False,
        }


def _resolve_primary_vptr(
    *,
    strings: Mapping[str, list[int]],
    relative: Mapping[int, int],
    type_name: str,
    mangled_name: str,
) -> tuple[int, int]:
    if not strings.get(type_name):
        raise AuthSessionResolverError(f"missing type string: {type_name}")
    mangled = set(strings.get(mangled_name, []))
    if not mangled:
        raise AuthSessionResolverError(f"missing mangled type string: {mangled_name}")

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
        raise AuthSessionResolverError(
            f"primary vptr is not unique for {type_name}: {candidates!r}"
        )
    return candidates[0]


def derive_auth_controller_offset(disassembly: str) -> int:
    offsets = {
        int(match.group(1), 16)
        for match in _GAME_AUTH_LOAD.finditer(disassembly)
    }
    if len(offsets) != 1:
        raise AuthSessionResolverError(
            f"auth-controller member load is not unique: {sorted(offsets)!r}"
        )
    return next(iter(offsets))


def derive_qstate_running_layout(disassembly: str) -> tuple[int, int, int]:
    private_offsets = {
        int(match.group(1), 16)
        for match in _QSTATE_PRIVATE_LOAD.finditer(disassembly)
    }
    running = {
        (int(match.group(2), 16), int(match.group(1), 16))
        for match in _QSTATE_RUNNING_CMP.finditer(disassembly)
    }
    if len(private_offsets) != 1 or len(running) != 1 or not _QSTATE_BOOL.search(disassembly):
        raise AuthSessionResolverError(
            "QStateMachine::isRunning layout is incomplete or ambiguous"
        )
    state_offset, running_value = next(iter(running))
    return next(iter(private_offsets)), state_offset, running_value


def resolve_layout(
    *,
    strings_text: str,
    relocations_text: str,
    game_session_connected_disassembly: str,
    qstate_is_running_disassembly: str,
) -> AuthSessionLayout:
    strings = parse_strings(strings_text)
    relative = parse_relative_relocations(relocations_text)
    game_vptr, game_typeinfo = _resolve_primary_vptr(
        strings=strings,
        relative=relative,
        type_name=GAME_CLIENT_TYPE,
        mangled_name=GAME_CLIENT_MANGLED,
    )
    auth_vptr, auth_typeinfo = _resolve_primary_vptr(
        strings=strings,
        relative=relative,
        type_name=AUTH_CONTROLLER_TYPE,
        mangled_name=AUTH_CONTROLLER_MANGLED,
    )
    auth_offset = derive_auth_controller_offset(game_session_connected_disassembly)
    private_offset, state_offset, running_value = derive_qstate_running_layout(
        qstate_is_running_disassembly
    )
    return AuthSessionLayout(
        game_client_vptr=game_vptr,
        game_client_typeinfo=game_typeinfo,
        auth_controller_vptr=auth_vptr,
        auth_controller_typeinfo=auth_typeinfo,
        auth_controller_offset=auth_offset,
        qstate_private_offset=private_offset,
        qstate_state_offset=state_offset,
        qstate_running_value=running_value,
    )


CURRENT_LAYOUT = AuthSessionLayout(
    game_client_vptr=0x30ADCE8,
    game_client_typeinfo=0x30A7778,
    auth_controller_vptr=0x30B5290,
    auth_controller_typeinfo=0x30B4410,
    auth_controller_offset=0x8D0,
    qstate_private_offset=0x8,
    qstate_state_offset=0xF0,
    qstate_running_value=2,
)


READ_ONLY_PROBE = r'''\
import hashlib,json,os,pathlib,struct,sys
pid=int(sys.argv[1]); start=int(sys.argv[2]); size=int(sys.argv[3]); sha=sys.argv[4]
game_vptr_off=int(sys.argv[5],16); auth_vptr_off=int(sys.argv[6],16)
auth_off=int(sys.argv[7],16); private_off=int(sys.argv[8],16)
state_off=int(sys.argv[9],16); running_value=int(sys.argv[10])
qt_size=int(sys.argv[11]); qt_sha=sys.argv[12]
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
qt=exe.parent/"lib"/"libQt6StateMachine.so.6"
if not qt.is_file() or qt.stat().st_size!=qt_size or digest(qt)!=qt_sha:
 raise SystemExit("QT_STATE_MACHINE_FENCE_MISMATCH")
regions=[]
for line in pathlib.Path(f"/proc/{pid}/maps").read_text().splitlines():
 parts=line.split(maxsplit=5); begin,end=(int(x,16) for x in parts[0].split("-"))
 regions.append((begin,end,parts[1],int(parts[2],16),parts[5] if len(parts)==6 else ""))
bases=[begin-off for begin,end,perms,off,path in regions if path==str(exe)]
if not bases: raise SystemExit("CLIENT_MAPPING_MISSING")
base=min(bases); expected_game_vptr=base+game_vptr_off; expected_auth_vptr=base+auth_vptr_off
heaps=[(begin,end) for begin,end,perms,off,path in regions if path=="[heap]" and perms.startswith("rw")]
if len(heaps)!=1: raise SystemExit("HEAP_MAPPING_COUNT="+str(len(heaps)))
begin,end=heaps[0]
if end-begin>768*1024*1024: raise SystemExit("HEAP_SCAN_BOUND_EXCEEDED")
def in_rw(addr):
 return any(b<=addr<e for b,e,perms,off,path in regions if perms.startswith("rw"))
fd=os.open(f"/proc/{pid}/mem",os.O_RDONLY|os.O_CLOEXEC)
pat=struct.pack("<Q",expected_game_vptr); hits=[]
try:
 cur=begin; tail=b""
 while cur<end:
  want=min(8*1024*1024,end-cur)
  try: data=os.pread(fd,want,cur)
  except OSError: raise SystemExit("PROC_MEM_READ_FAILED")
  if len(data)!=want: raise SystemExit("PROC_MEM_SHORT_READ")
  merged=tail+data; merged_base=cur-len(tail); pos=0
  while True:
   idx=merged.find(pat,pos)
   if idx<0: break
   obj=merged_base+idx
   if obj%8==0: hits.append(obj)
   pos=idx+1
  tail=merged[-7:]; cur+=want
 hits=sorted(set(hits))
 if len(hits)!=1: raise SystemExit("GAME_CLIENT_OBJECT_COUNT="+str(len(hits)))
 game=hits[0]
 auth=struct.unpack("<Q",os.pread(fd,8,game+auth_off))[0]
 if not auth or not in_rw(auth): raise SystemExit("AUTH_CONTROLLER_POINTER_INVALID")
 auth_vptr=struct.unpack("<Q",os.pread(fd,8,auth))[0]
 if auth_vptr!=expected_auth_vptr: raise SystemExit("AUTH_CONTROLLER_VPTR_MISMATCH")
 private=struct.unpack("<Q",os.pread(fd,8,auth+private_off))[0]
 if not private or not in_rw(private): raise SystemExit("QSTATE_PRIVATE_POINTER_INVALID")
 state=struct.unpack("<I",os.pread(fd,4,private+state_off))[0]
 if state not in (0,1,2): raise SystemExit("QSTATE_LIFECYCLE_VALUE_UNEXPECTED")
 running=state==running_value
finally:
 os.close(fd)
if ticks()!=start: raise SystemExit("START_TICKS_CHANGED_DURING_READ")
print(json.dumps({
 "state":"AVAILABLE",
 "reader_id":"auth_session_typed_reader",
 "game_client_object_count":1,
 "authentication_process_object_count":1,
 "authentication_state_machine_running":running,
 "process_memory_access":"read_only",
 "semantic_state":"TYPED_AUTH_LIFECYCLE_ONLY",
 "in_game_claimed":False,
 "credentials_retained":False,
 "session_secrets_retained":False
},sort_keys=True))
'''


def read_auth_session(
    *,
    pid: int,
    start_ticks: int,
    runner: Callable[[list[str]], str],
    container: str = EXPECTED_TARGET_CONTAINER,
) -> dict[str, object]:
    layout = CURRENT_LAYOUT
    args = [
        "docker", "exec", container, "python3", "-c", READ_ONLY_PROBE,
        str(pid), str(start_ticks), str(EXPECTED_CLIENT_SIZE), EXPECTED_CLIENT_SHA256,
        hex(layout.game_client_vptr), hex(layout.auth_controller_vptr),
        hex(layout.auth_controller_offset), hex(layout.qstate_private_offset),
        hex(layout.qstate_state_offset), str(layout.qstate_running_value),
        str(QT_STATE_MACHINE_SIZE), QT_STATE_MACHINE_SHA256,
    ]
    try:
        raw = runner(args).strip()
        doc = json.loads(raw)
        if (
            not isinstance(doc, dict)
            or doc.get("state") != "AVAILABLE"
            or doc.get("reader_id") != READER_ID
            or not isinstance(doc.get("authentication_state_machine_running"), bool)
            or doc.get("process_memory_access") != "read_only"
            or doc.get("semantic_state") != "TYPED_AUTH_LIFECYCLE_ONLY"
            or doc.get("in_game_claimed") is not False
            or doc.get("credentials_retained") is not False
            or doc.get("session_secrets_retained") is not False
        ):
            raise ValueError("invalid auth/session reader payload")
    except Exception as exc:
        return {
            "state": "UNAVAILABLE",
            "reader_id": READER_ID,
            "reason": f"READ_FAILED:{type(exc).__name__}",
            "semantic_promotion_allowed": False,
        }
    doc["layout_evidence"] = layout.evidence()
    doc["qt_state_machine_fence"] = {
        "library": QT_STATE_MACHINE_LIBRARY,
        "size": QT_STATE_MACHINE_SIZE,
        "sha256": QT_STATE_MACHINE_SHA256,
    }
    doc["semantic_promotion_allowed"] = False
    return doc
