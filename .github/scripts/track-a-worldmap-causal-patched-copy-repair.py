#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SCREEN_MARKER = "echo 'WORLDMAP_BASELINE_DESKTOP_GEOMETRY=1020x650'\nbash -n \"$WORKER\"\n"
LIVE_HASH = "[[ \"$(sha256sum \"$CLIENT\"|awk '{print $1}')\" == \"$EXPECTED_SHA\" ]] || fail client_sha_mismatch\n"
NAMESPACE = "NAMESPACE=worldmap-causal-baseline-ephemeral-v1\n"
EVIDENCE = 'EVIDENCE="$RUNNER_TEMP/worldmap-baseline-evidence"\n'

PATCH_WORKER = r'''echo 'WORLDMAP_BASELINE_DESKTOP_GEOMETRY=1020x650'
# Inject the already-authorized one-byte [19,14] patch into the task-owned
# session copy only. The copied exact client is verified by the canonical worker
# before this patch runs. VA->file offset is derived from this ELF's PT_LOAD
# headers and cross-checked against the accepted design evidence.
python3 - "$WORKER" <<'PY_PATCH_WORKER'
from pathlib import Path
import sys
worker_path=Path(sys.argv[1])
worker=worker_path.read_text()
anchor='''  client="$package/bin/client"
  verify_client "$client"
  metadata="$(dirname "$source")/../../launchermetadata.json"
'''
if worker.count(anchor)!=1:
    raise SystemExit(f'WORLDMAP_PATCH_WORKER_ERROR=client_copy_anchor_count:{worker.count(anchor)}')
replacement=r'''  client="$package/bin/client"
  verify_client "$client"
  python3 - "$client" <<'PY_WORLDMAP_PATCH'
from pathlib import Path
import hashlib,os,stat,struct,sys
client=Path(sys.argv[1])
SOURCE_SHA='e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe'
PATCHED_SHA='7c8d936fa43e4a026d2a69c32ff30fdea149bb7eff7938c1b1acfc173899b44c'
SIZE=51965216
TARGET_VA=0x01cdd958
EXPECTED_FILE_OFFSET=0x01cdd958
PREIMAGE=bytes.fromhex('120000000e0000000800000006000000')
POST_PREFIX=bytes.fromhex('130000000e000000')
data=client.read_bytes()
if len(data)!=SIZE:
    raise SystemExit(f'WORLDMAP_PATCH_ERROR=size:{len(data)}')
if hashlib.sha256(data).hexdigest()!=SOURCE_SHA:
    raise SystemExit('WORLDMAP_PATCH_ERROR=source_sha')
if data[:4]!=b'\x7fELF' or data[4]!=2 or data[5]!=1:
    raise SystemExit('WORLDMAP_PATCH_ERROR=elf64_le_required')
e_phoff=struct.unpack_from('<Q',data,32)[0]
e_phentsize=struct.unpack_from('<H',data,54)[0]
e_phnum=struct.unpack_from('<H',data,56)[0]
if e_phentsize<56 or not (1<=e_phnum<=128):
    raise SystemExit('WORLDMAP_PATCH_ERROR=phdr_shape')
file_offset=None
for i in range(e_phnum):
    off=e_phoff+i*e_phentsize
    if off+56>len(data):
        raise SystemExit('WORLDMAP_PATCH_ERROR=phdr_oob')
    p_type=struct.unpack_from('<I',data,off)[0]
    if p_type!=1:
        continue
    p_offset=struct.unpack_from('<Q',data,off+8)[0]
    p_vaddr=struct.unpack_from('<Q',data,off+16)[0]
    p_filesz=struct.unpack_from('<Q',data,off+32)[0]
    if p_vaddr<=TARGET_VA<TARGET_VA+1<=p_vaddr+p_filesz:
        candidate=p_offset+(TARGET_VA-p_vaddr)
        if file_offset is not None and file_offset!=candidate:
            raise SystemExit('WORLDMAP_PATCH_ERROR=ambiguous_pt_load')
        file_offset=candidate
if file_offset is None:
    raise SystemExit('WORLDMAP_PATCH_ERROR=target_va_unmapped')
if file_offset!=EXPECTED_FILE_OFFSET:
    raise SystemExit(f'WORLDMAP_PATCH_ERROR=file_offset:{file_offset:#x}')
if data[file_offset:file_offset+len(PREIMAGE)]!=PREIMAGE:
    raise SystemExit('WORLDMAP_PATCH_ERROR=preimage')
after=bytearray(data)
after[file_offset:file_offset+len(POST_PREFIX)]=POST_PREFIX
diffs=[i for i,(a,b) in enumerate(zip(data,after)) if a!=b]
if diffs!=[file_offset]:
    raise SystemExit(f'WORLDMAP_PATCH_ERROR=diff:{len(diffs)}')
patched_hash=hashlib.sha256(after).hexdigest()
if patched_hash!=PATCHED_SHA:
    raise SystemExit('WORLDMAP_PATCH_ERROR=patched_sha')
mode=stat.S_IMODE(client.stat().st_mode)
tmp=client.with_name(client.name+'.worldmap-patched-tmp')
with open(tmp,'wb') as f:
    f.write(after)
    f.flush(); os.fsync(f.fileno())
os.chmod(tmp,mode)
os.replace(tmp,client)
print('WORLDMAP_PATCH_TARGET_VA=0x01cdd958')
print(f'WORLDMAP_PATCH_DERIVED_FILE_OFFSET={file_offset:#x}')
print('WORLDMAP_PATCH_PREIMAGE=PASS')
print('WORLDMAP_PATCH_CHANGED_BYTE_COUNT=1')
print('WORLDMAP_PATCHED_SHA256='+patched_hash)
print('WORLDMAP_PATCH_TASK_OWNED_COPY=PASS')
PY_WORLDMAP_PATCH
  metadata="$(dirname "$source")/../../launchermetadata.json"
'''
worker=worker.replace(anchor,replacement,1)
worker_path.write_text(worker)
worker_path.chmod(0o700)
print('WORLDMAP_PATCH_WORKER_INJECTION=PASS')
PY_PATCH_WORKER
bash -n "$WORKER"
'''

PATCHED_LIVE_HASH = r'''PATCHED_EXPECTED_SHA=7c8d936fa43e4a026d2a69c32ff30fdea149bb7eff7938c1b1acfc173899b44c
[[ "$(sha256sum "$CLIENT"|awk '{print $1}')" == "$PATCHED_EXPECTED_SHA" ]] || fail patched_client_sha_mismatch
echo 'WORLDMAP_PATCH_LIVE_CLIENT_SHA=PASS'
'''


class TransformRefused(RuntimeError):
    pass


def replace_exact(text: str, old: str, new: str, label: str) -> str:
    count=text.count(old)
    if count!=1:
        raise TransformRefused(f"{label}_COUNT:{count}")
    return text.replace(old,new,1)


def transform(text: str) -> str:
    text=replace_exact(text,SCREEN_MARKER,PATCH_WORKER,"SCREEN_MARKER")
    text=replace_exact(text,LIVE_HASH,PATCHED_LIVE_HASH,"LIVE_HASH")
    text=replace_exact(text,NAMESPACE,"NAMESPACE=worldmap-causal-patched-ephemeral-v1\n","NAMESPACE")
    text=replace_exact(text,EVIDENCE,'EVIDENCE="$RUNNER_TEMP/worldmap-patched-evidence"\n',"EVIDENCE")
    required=(
        "WORLDMAP_PATCH_WORKER_INJECTION=PASS",
        "WORLDMAP_PATCH_TARGET_VA=0x01cdd958",
        "WORLDMAP_PATCH_DERIVED_FILE_OFFSET=",
        "WORLDMAP_PATCH_CHANGED_BYTE_COUNT=1",
        "WORLDMAP_PATCHED_SHA256=",
        "WORLDMAP_PATCH_TASK_OWNED_COPY=PASS",
        "WORLDMAP_PATCH_LIVE_CLIENT_SHA=PASS",
        "worldmap-causal-patched-ephemeral-v1",
        "worldmap-patched-evidence",
    )
    missing=[token for token in required if token not in text]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:"+",".join(missing))
    return text


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path)
    p.add_argument("output",type=Path)
    args=p.parse_args()
    try:
        result=transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_PATCHED_COPY_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(result,encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_PATCHED_COPY_REPAIR=PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
