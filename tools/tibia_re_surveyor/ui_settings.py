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
import hashlib,json,os,pathlib,pwd,sys
pid=int(sys.argv[1]); start=int(sys.argv[2]); size=int(sys.argv[3]); sha=sys.argv[4]
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
uid=os.stat(f"/proc/{pid}").st_uid
home=pathlib.Path(pwd.getpwuid(uid).pw_dir).resolve()
path=(home/".local/share/CipSoft GmbH/Tibia/packages/Tibia/conf/clientoptions.json").resolve()
try: path.relative_to(home)
except ValueError: raise SystemExit("SETTINGS_PATH_ESCAPES_HOME")
flags=os.O_RDONLY|os.O_CLOEXEC
if hasattr(os,"O_NOFOLLOW"): flags|=os.O_NOFOLLOW
try: fd=os.open(path,flags)
except OSError: raise SystemExit("CLIENTOPTIONS_OPEN_FAILED")
try:
 st=os.fstat(fd)
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
print(json.dumps({"state":"AVAILABLE","reader_id":"ui_settings_typed_reader","master_volume":values["soundMasterVolume"],"master_volume_old":values["soundMasterVolumeOld"],"persistence_relative_path":"packages/Tibia/conf/clientoptions.json","filesystem_access":"read_only","process_memory_access":"not_used"},sort_keys=True))
"""

_SAFE_RUNTIME_CODES = (
    "START_TICKS_MISMATCH",
    "EXACT_FENCE_MISMATCH",
    "SETTINGS_PATH_ESCAPES_HOME",
    "CLIENTOPTIONS_OPEN_FAILED",
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
        if static.get("state") != "AVAILABLE" or static.get("type_name") != TYPE_NAME:
            raise RuntimeError("static settings model unavailable")
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
        if doc.get("state") != "AVAILABLE":
            raise RuntimeError("settings snapshot unavailable")
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
