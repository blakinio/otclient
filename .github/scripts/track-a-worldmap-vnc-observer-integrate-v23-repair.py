#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

VAR_OLD='WORKER="$RUNNER_TEMP/worldmap-baseline-xres-worker"\n'
VAR_NEW='XRES_WORKER="$RUNNER_TEMP/worldmap-baseline-xres-worker-base"\nWORKER="$RUNNER_TEMP/worldmap-baseline-xres-worker"\n'

BLOCK_OLD='''python3 .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py \\
  "$STAGE_WORKER" "$WORKER" \\
  --owner-helper .github/scripts/tibia-official-client-re-xres-window-owner.py \\
  --wire-helper .github/scripts/tibia-official-client-re-xres-wire.py
bash -n "$WORKER"
'''

BLOCK_NEW='''python3 .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py \\
  "$STAGE_WORKER" "$XRES_WORKER" \\
  --owner-helper .github/scripts/tibia-official-client-re-xres-window-owner.py \\
  --wire-helper .github/scripts/tibia-official-client-re-xres-wire.py
python3 .github/scripts/track-a-worldmap-vnc-observer-access-v23-repair.py \\
  "$XRES_WORKER" "$WORKER"
rm -f "$XRES_WORKER"
bash -n "$WORKER"
'''

class Refused(RuntimeError): pass

def transform(text:str)->str:
    if text.count(VAR_OLD)!=1: raise Refused(f'VAR_ANCHOR_COUNT:{text.count(VAR_OLD)}')
    out=text.replace(VAR_OLD,VAR_NEW,1)
    if out.count(BLOCK_OLD)!=1: raise Refused(f'BLOCK_ANCHOR_COUNT:{out.count(BLOCK_OLD)}')
    out=out.replace(BLOCK_OLD,BLOCK_NEW,1)
    for marker in (
        'track-a-worldmap-vnc-observer-access-v23-repair.py',
        '"$XRES_WORKER" "$WORKER"',
        'rm -f "$XRES_WORKER"',
    ):
        if marker not in out: raise Refused('REQUIRED_MISSING:'+marker)
    return out

def main()->int:
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:out=transform(a.source.read_text(encoding='utf-8'))
    except Refused as e:
        print('TRACK_A_VNC_OBSERVER_INTEGRATE_V23_REFUSED='+str(e));return 44
    a.output.write_text(out,encoding='utf-8');a.output.chmod(0o700)
    print('TRACK_A_VNC_OBSERVER_INTEGRATE_V23_REPAIR=PASS');return 0

if __name__=='__main__':raise SystemExit(main())
