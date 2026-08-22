from __future__ import annotations

import json
from typing import Callable

from .runtime import EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE, EXPECTED_TARGET_CONTAINER

READER_ID = "ui_settings_typed_reader"
TYPE_NAME = "tibia::config::TClientOptions"
STATIC_SETTINGS_PROBE = r"""
import hashlib,json,os,pathlib,sys
pid=int(sys.argv[1]); start=int(sys.argv[2]); size=int(sys.argv[3]); sha=sys.argv[4]
def ticks():
 raw=pathlib.Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
 return int(raw[raw.rfind(")")+2:].split()[19])
def digest(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
if ticks()!=start: raise SystemExit("STATIC_START_TICKS_MISMATCH")
exe=pathlib.Path(os.path.realpath(f"/proc/{pid}/exe"))
if exe.stat().st_size!=size or digest(exe)!=sha: raise SystemExit("STATIC_EXACT_FENCE_MISMATCH")
data=exe.read_bytes()
if len(data)!=size: raise SystemExit("STATIC_EXECUTABLE_SIZE_CHANGED")
type_count=data.count(b"tibia::config::TClientOptions\x00")
path_count=data.count(b"clientoptions.json\x00")
if type_count<1: raise SystemExit("STATIC_CLIENT_OPTIONS_TYPE_MISSING")
if path_count!=1: raise SystemExit("STATIC_CLIENTOPTIONS_LITERAL_COUNT="+str(path_count))
if ticks()!=start: raise SystemExit("STATIC_START_TICKS_CHANGED")
print(json.dumps({"state":"AVAILABLE","type_name":"tibia::config::TClientOptions","type_string_count":type_count,"clientoptions_literal_count":path_count},sort_keys=True))
"""

READ_ONLY_SETTINGS_PROBE = r"""
import hashlib,json,os,pathlib,stat,sys
pid=int(sys.argv[1]); start=int(sys.argv[2]); size=int(sys.argv[3]); sha=sys.argv[4]
def ticks():
 raw=pathlib.Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
 return int(raw[raw.rfind(")")+2:].split()[19])
def digest_fd(fd):
 h=hashlib.sha256()
 os.lseek(fd,0,os.SEEK_SET)
 while True:
  chunk=os.read(fd,1024*1024)
  if not chunk: break
  h.update(chunk)
 os.lseek(fd,0,os.SEEK_SET)
 return h.hexdigest()
def descriptor_path(fd,code):
 try: raw=os.readlink(f"/proc/self/fd/{fd}")
 except OSError: raise SystemExit(code)
 if not raw.startswith("/") or raw.endswith(" (deleted)"): raise SystemExit(code)
 return pathlib.Path(raw)
def assert_root_binding(exe_fd,root_fd):
 exe_path=descriptor_path(exe_fd,"CLIENT_EXE_DESCRIPTOR_PATH_INVALID")
 root_path=descriptor_path(root_fd,"CLIENT_PACKAGE_ROOT_DESCRIPTOR_PATH_INVALID")
 if exe_path!=root_path/"bin"/"client": raise SystemExit("CLIENT_PACKAGE_ROOT_BINDING_MISMATCH")
 return exe_path
if ticks()!=start: raise SystemExit("START_TICKS_MISMATCH")
proc_exe=f"/proc/{pid}/exe"
try: exe_fd=os.open(proc_exe,os.O_RDONLY|os.O_CLOEXEC)
except OSError: raise SystemExit("CLIENT_EXE_OPEN_FAILED")
try:
 exe_st=os.fstat(exe_fd)
 if exe_st.st_size!=size or digest_fd(exe_fd)!=sha: raise SystemExit("EXACT_FENCE_MISMATCH")
 current_exe_st=os.stat(proc_exe)
 if (current_exe_st.st_dev,current_exe_st.st_ino)!=(exe_st.st_dev,exe_st.st_ino):
  raise SystemExit("CLIENT_EXE_IDENTITY_CHANGED")
 uid=os.stat(f"/proc/{pid}").st_uid
 exe=descriptor_path(exe_fd,"CLIENT_EXE_DESCRIPTOR_PATH_INVALID")
 if exe.name!="client" or exe.parent.name!="bin": raise SystemExit("CLIENT_PACKAGE_LAYOUT_INVALID")
 package_root=exe.parent.parent
 if not hasattr(os,"O_DIRECTORY") or not hasattr(os,"O_NOFOLLOW"):
  raise SystemExit("CLIENT_NOFOLLOW_UNAVAILABLE")
 dir_flags=os.O_RDONLY|os.O_CLOEXEC|os.O_DIRECTORY|os.O_NOFOLLOW
 file_flags=os.O_RDONLY|os.O_CLOEXEC|os.O_NOFOLLOW
 try: root_fd=os.open(package_root,dir_flags)
 except OSError: raise SystemExit("CLIENT_PACKAGE_ROOT_OPEN_FAILED")
 try:
  assert_root_binding(exe_fd,root_fd)
  try: bin_fd=os.open("bin",dir_flags,dir_fd=root_fd)
  except OSError: raise SystemExit("CLIENT_PACKAGE_BIN_OPEN_FAILED")
  try:
   try: package_exe_fd=os.open("client",file_flags,dir_fd=bin_fd)
   except OSError: raise SystemExit("CLIENT_PACKAGE_EXECUTABLE_OPEN_FAILED")
   try:
    package_exe_st=os.fstat(package_exe_fd)
    if (package_exe_st.st_dev,package_exe_st.st_ino)!=(exe_st.st_dev,exe_st.st_ino):
     raise SystemExit("CLIENT_PACKAGE_EXECUTABLE_IDENTITY_MISMATCH")
   finally: os.close(package_exe_fd)
  finally: os.close(bin_fd)
  try: conf_fd=os.open("conf",dir_flags,dir_fd=root_fd)
  except OSError: raise SystemExit("CLIENTOPTIONS_PARENT_OPEN_FAILED")
  try:
   try: fd=os.open("clientoptions.json",file_flags,dir_fd=conf_fd)
   except OSError: raise SystemExit("CLIENTOPTIONS_OPEN_FAILED")
  finally: os.close(conf_fd)
  try:
   st=os.fstat(fd)
   if not stat.S_ISREG(st.st_mode) or st.st_uid!=uid: raise SystemExit("CLIENTOPTIONS_IDENTITY_INVALID")
   if st.st_size<=0 or st.st_size>2*1024*1024: raise SystemExit("CLIENTOPTIONS_SIZE_INVALID")
   raw=b""
   while len(raw)<st.st_size:
    chunk=os.read(fd,min(1024*1024,st.st_size-len(raw)))
    if not chunk: break
    raw+=chunk
  finally: os.close(fd)
  if len(raw)!=st.st_size: raise SystemExit("CLIENTOPTIONS_SHORT_READ")
  try: doc=json.loads(raw)
  except Exception: raise SystemExit("CLIENTOPTIONS_JSON_INVALID")
  options=doc.get("options") if isinstance(doc,dict) else None
  if not isinstance(options,dict): raise SystemExit("CLIENTOPTIONS_OPTIONS_MISSING")
  values={}
  for key in ("soundMasterVolume","soundMasterVolumeOld"):
   value=options.get(key)
   if isinstance(value,bool) or not isinstance(value,int) or not 0<=value<=100:
    raise SystemExit("CLIENTOPTIONS_MASTER_VOLUME_INVALID")
   values[key]=value
  if ticks()!=start: raise SystemExit("START_TICKS_CHANGED_DURING_READ")
  current_exe_st=os.stat(proc_exe)
  if (current_exe_st.st_dev,current_exe_st.st_ino)!=(exe_st.st_dev,exe_st.st_ino):
   raise SystemExit("CLIENT_EXE_IDENTITY_CHANGED")
  assert_root_binding(exe_fd,root_fd)
  print(json.dumps({"state":"AVAILABLE","reader_id":"ui_settings_typed_reader","master_volume":values["soundMasterVolume"],"master_volume_old":values["soundMasterVolumeOld"],"persistence_relative_path":"conf/clientoptions.json","filesystem_access":"read_only","process_memory_access":"not_used"},sort_keys=True))
 finally:
  os.close(root_fd)
finally:
 os.close(exe_fd)
"""

_SAFE_RUNTIME_CODES = (
    "START_TICKS_MISMATCH",
    "EXACT_FENCE_MISMATCH",
    "CLIENT_EXE_OPEN_FAILED",
    "CLIENT_EXE_IDENTITY_CHANGED",
    "CLIENT_EXE_DESCRIPTOR_PATH_INVALID",
    "CLIENT_PACKAGE_LAYOUT_INVALID",
    "CLIENT_NOFOLLOW_UNAVAILABLE",
    "CLIENT_PACKAGE_ROOT_OPEN_FAILED",
    "CLIENT_PACKAGE_ROOT_DESCRIPTOR_PATH_INVALID",
    "CLIENT_PACKAGE_ROOT_BINDING_MISMATCH",
    "CLIENT_PACKAGE_BIN_OPEN_FAILED",
    "CLIENT_PACKAGE_EXECUTABLE_OPEN_FAILED",
    "CLIENT_PACKAGE_EXECUTABLE_IDENTITY_MISMATCH",
    "CLIENTOPTIONS_PARENT_OPEN_FAILED",
    "CLIENTOPTIONS_OPEN_FAILED",
    "CLIENTOPTIONS_IDENTITY_INVALID",
    "CLIENTOPTIONS_SIZE_INVALID",
    "CLIENTOPTIONS_SHORT_READ",
    "CLIENTOPTIONS_JSON_INVALID",
    "CLIENTOPTIONS_OPTIONS_MISSING",
    "CLIENTOPTIONS_MASTER_VOLUME_INVALID",
    "START_TICKS_CHANGED_DURING_READ",
)


def _safe_runtime_failure(exc: Exception) -> str:
    text = str(exc)
    for code in _SAFE_RUNTIME_CODES:
        if code in text:
            return code
    return type(exc).__name__


_STATIC_RESULT_KEYS = frozenset({"state", "type_name", "type_string_count", "clientoptions_literal_count"})
_LIVE_RESULT_KEYS = frozenset({
    "state", "reader_id", "master_volume", "master_volume_old",
    "persistence_relative_path", "filesystem_access", "process_memory_access",
})


def read_ui_settings(
    *,
    pid: int,
    start_ticks: int,
    runner: Callable[[list[str]], str],
    container: str = EXPECTED_TARGET_CONTAINER,
) -> dict[str, object]:
    try:
        raw_static = runner(
            [
                "docker", "exec", container, "python3", "-c", STATIC_SETTINGS_PROBE,
                str(pid), str(start_ticks), str(EXPECTED_CLIENT_SIZE), EXPECTED_CLIENT_SHA256,
            ]
        ).strip()
        static = json.loads(raw_static)
        if (
            not isinstance(static, dict)
            or set(static) != _STATIC_RESULT_KEYS
            or static.get("state") != "AVAILABLE"
            or static.get("type_name") != TYPE_NAME
            or isinstance(static.get("type_string_count"), bool)
            or not isinstance(static.get("type_string_count"), int)
            or static["type_string_count"] < 1
            or isinstance(static.get("clientoptions_literal_count"), bool)
            or static.get("clientoptions_literal_count") != 1
        ):
            raise RuntimeError("static settings model unavailable")
        static = {
            "state": "AVAILABLE",
            "type_name": TYPE_NAME,
            "type_string_count": static["type_string_count"],
            "clientoptions_literal_count": 1,
        }
    except Exception as exc:
        return {
            "state": "UNAVAILABLE",
            "reader_id": READER_ID,
            "reason": f"STATIC_SETTINGS_MODEL_FAILED:{type(exc).__name__}",
            "semantic_promotion_allowed": False,
        }

    try:
        raw_live = runner(
            [
                "docker", "exec", container, "python3", "-c", READ_ONLY_SETTINGS_PROBE,
                str(pid), str(start_ticks), str(EXPECTED_CLIENT_SIZE), EXPECTED_CLIENT_SHA256,
            ]
        ).strip()
        doc = json.loads(raw_live)
        master = doc.get("master_volume") if isinstance(doc, dict) else None
        master_old = doc.get("master_volume_old") if isinstance(doc, dict) else None
        if (
            not isinstance(doc, dict)
            or set(doc) != _LIVE_RESULT_KEYS
            or doc.get("state") != "AVAILABLE"
            or doc.get("reader_id") != READER_ID
            or isinstance(master, bool)
            or not isinstance(master, int)
            or not 0 <= master <= 100
            or isinstance(master_old, bool)
            or not isinstance(master_old, int)
            or not 0 <= master_old <= 100
            or doc.get("persistence_relative_path") != "conf/clientoptions.json"
            or doc.get("filesystem_access") != "read_only"
            or doc.get("process_memory_access") != "not_used"
        ):
            raise RuntimeError("settings snapshot unavailable")
        doc = {
            "state": "AVAILABLE",
            "reader_id": READER_ID,
            "master_volume": master,
            "master_volume_old": master_old,
            "persistence_relative_path": "conf/clientoptions.json",
            "filesystem_access": "read_only",
            "process_memory_access": "not_used",
        }
    except Exception as exc:
        return {
            "state": "UNAVAILABLE",
            "reader_id": READER_ID,
            "reason": f"LIVE_SETTINGS_READ_FAILED:{_safe_runtime_failure(exc)}",
            "static_evidence": static,
            "semantic_promotion_allowed": False,
        }

    doc.update(
        {
            "semantic_state": "TYPED_UI_SETTINGS_MASTER_VOLUME_FILE_READ_ONLY",
            "settings_model_type": TYPE_NAME,
            "settings_model_type_present": True,
            "persistence_fields": ["options.soundMasterVolume", "options.soundMasterVolumeOld"],
            "master_volume_persistence_field_semantics": "PROVEN_ON_EXACT_BUILD_BY_PRIOR_REVERSIBLE_CAUSAL_EVIDENCE",
            "live_ui_application_state_claimed": False,
            "all_settings_model_claimed": False,
            "qsettings_linkage_claimed": False,
            "client_options_to_file_linkage_claimed": False,
            "credentials_retained": False,
            "session_secrets_retained": False,
            "semantic_promotion_allowed": False,
            "static_evidence": static,
        }
    )
    return doc
