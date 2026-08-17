#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ANCHOR = "S()\nend\ncontinue\n"

REPLACEMENT = r'''S()
# V15 read-only object provenance. Scan only readable+writable private mappings
# for exact relocated primary vpointers recovered statically on the same SHA.
import os,json
vptrs={
  'auth':@BIAS@+0x307f1b0,
  'charsel':@BIAS@+0x308ed68,
  'gameclient':@BIAS@+0x3076908,
  'uploader':@BIAS@+0x30d36f8,
}
proc_maps=f'/proc/{inf.pid}/maps'
ranges=[]
for line in open(proc_maps,errors='replace'):
    p=line.split()
    if len(p)<2: continue
    perms=p[1]
    if not (perms.startswith('rw') and 'p' in perms): continue
    lo,hi=(int(x,16) for x in p[0].split('-'))
    if hi<=lo: continue
    ranges.append((lo,hi,p[-1] if len(p)>=6 else ''))

def scan_ptr(value):
    needle=struct.pack('<Q',value); hits=[]
    for lo,hi,name in ranges:
        cur=lo
        while cur<hi:
            try: found=inf.search_memory(cur,hi-cur,needle)
            except: found=None
            if found is None: break
            a=int(found); hits.append(a)
            if len(hits)>64: return hits
            cur=a+8
    return hits

objects={k:scan_ptr(v) for k,v in vptrs.items()}
root=os.path.dirname(ev); objfile=os.path.join(root,'v15-native-objects.json')
with open(objfile,'w') as f:
    json.dump({'schema':'worldmap-native-object-provenance-v15','objects':objects},f,sort_keys=True,separators=(',',':'))
os.chmod(objfile,0o600)
for k in ('auth','charsel','gameclient','uploader'):
    gdb.write('WORLDMAP_V15_LIVE_'+k.upper()+'_INSTANCE_COUNT='+str(len(objects[k]))+'\n')
# Auth and GameClient are required before any credentials. Character-selection
# controller is required for the native semantic continuation. Uploader may be
# absent until a cold login request is constructed.
if len(objects['auth'])==1 and len(objects['charsel'])==1 and len(objects['gameclient'])==1:
    gdb.write('WORLDMAP_V15_NATIVE_OBJECT_PROVENANCE=PASS\n')
else:
    gdb.write('WORLDMAP_V15_NATIVE_OBJECT_PROVENANCE=FAIL\n')
end
continue
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(ANCHOR) != 1:
        raise TransformRefused(f"ANCHOR_COUNT:{text.count(ANCHOR)}")
    out=text.replace(ANCHOR,REPLACEMENT,1)
    required=(
        "WORLDMAP_V15_LIVE_AUTH_INSTANCE_COUNT=",
        "WORLDMAP_V15_LIVE_CHARSEL_INSTANCE_COUNT=",
        "WORLDMAP_V15_LIVE_GAMECLIENT_INSTANCE_COUNT=",
        "WORLDMAP_V15_LIVE_UPLOADER_INSTANCE_COUNT=",
        "WORLDMAP_V15_NATIVE_OBJECT_PROVENANCE=PASS",
        "v15-native-objects.json",
        "0x307f1b0","0x308ed68","0x3076908","0x30d36f8",
    )
    missing=[x for x in required if x not in out]
    if missing: raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    if out.count("WORLDMAP_V15_NATIVE_OBJECT_PROVENANCE=PASS") != 1:
        raise TransformRefused('PROVENANCE_MARKER_NOT_UNIQUE')
    return out


def main() -> int:
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try: out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_NATIVE_OBJECT_PROVENANCE_V15_REPAIR_REFUSED={exc}');return 44
    a.output.write_text(out,encoding='utf-8');a.output.chmod(0o700)
    print('WORLDMAP_NATIVE_OBJECT_PROVENANCE_V15_REPAIR=PASS');return 0

if __name__=='__main__': raise SystemExit(main())
