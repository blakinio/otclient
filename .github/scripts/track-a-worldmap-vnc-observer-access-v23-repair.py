#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

PORT_OLD='  vnc_port="$(free_port 6082 6120)" || die no_free_vnc_port\n'
PORT_NEW='  vnc_port=6082\n  ! listen "$vnc_port" || die observer_vnc_port_6082_busy\n'

START_ANCHOR="  printf 'TRACK_A_CANONICAL_STAGE=vnc_start\\n'\n"
START_REPLACEMENT=r'''  # User-observer VNC remains the exact same task-owned Xvfb/display. It is
  # view-only and password protected. The password is persistent private runner
  # state (0600), never an argv value, environment value, log line or artifact.
  local vnc_password_file="$BASE/vnc-viewonly.password"
  if [[ ! -s "$vnc_password_file" ]]; then
    python3 - "$vnc_password_file" <<'PYVNC'
import os,secrets,string,sys
p=sys.argv[1]
alphabet=string.ascii_letters+string.digits
password=''.join(secrets.choice(alphabet) for _ in range(8))
fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:f.write(password+'\n')
PYVNC
  fi
  [[ -f "$vnc_password_file" && ! -L "$vnc_password_file" ]] || die vnc_password_file_invalid
  chmod 600 "$vnc_password_file"
  [[ "$(stat -c %a "$vnc_password_file")" == 600 ]] || die vnc_password_mode_invalid

  printf 'TRACK_A_CANONICAL_STAGE=vnc_start\n'
'''

CMD_OLD=r'''    nohup "$vnc" -display "$display" -rfbport "$vnc_port" -forever -shared -viewonly \
    -localhost -nopw -noxdamage >"$SESSION/vnc.log" 2>&1 </dev/null &
  echo $! >"$SESSION/vnc.pid"
'''
CMD_NEW=r'''    nohup "$vnc" -display "$display" -rfbport "$vnc_port" -forever -shared -viewonly \
    -listen 0.0.0.0 -passwdfile "$vnc_password_file" -noxdamage >"$SESSION/vnc.log" 2>&1 </dev/null &
  echo $! >"$SESSION/vnc.pid"
  echo "$vnc_password_file" >"$SESSION/vnc-password-file"
  chmod 600 "$SESSION/vnc-password-file"
  printf 'TRACK_A_USER_VNC_MODE=VIEW_ONLY_PASSWORD_PROTECTED\n'
  printf 'TRACK_A_USER_VNC_PORT=%s\n' "$vnc_port"
  printf 'TRACK_A_USER_VNC_PASSWORD_FILE=%s\n' "$vnc_password_file"
'''

class Refused(RuntimeError): pass

def transform(text:str)->str:
    if text.count(PORT_OLD)!=1: raise Refused(f'PORT_ANCHOR_COUNT:{text.count(PORT_OLD)}')
    out=text.replace(PORT_OLD,PORT_NEW,1)
    if out.count(START_ANCHOR)!=1: raise Refused(f'START_ANCHOR_COUNT:{out.count(START_ANCHOR)}')
    out=out.replace(START_ANCHOR,START_REPLACEMENT,1)
    if out.count(CMD_OLD)!=1: raise Refused(f'CMD_ANCHOR_COUNT:{out.count(CMD_OLD)}')
    out=out.replace(CMD_OLD,CMD_NEW,1)
    required=(
        'vnc_port=6082','observer_vnc_port_6082_busy',
        'TRACK_A_USER_VNC_MODE=VIEW_ONLY_PASSWORD_PROTECTED',
        'TRACK_A_USER_VNC_PORT=%s','-viewonly','-listen 0.0.0.0',
        '-passwdfile "$vnc_password_file"','vnc-viewonly.password',
        'chmod 600 "$vnc_password_file"',
    )
    miss=[x for x in required if x not in out]
    if miss: raise Refused('REQUIRED_MISSING:'+','.join(miss))
    if '-localhost -nopw' in out: raise Refused('LEGACY_UNREACHABLE_VNC_SURVIVED')
    return out

def main()->int:
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:out=transform(a.source.read_text(encoding='utf-8'))
    except Refused as e:
        print('TRACK_A_VNC_OBSERVER_ACCESS_V23_REFUSED='+str(e));return 44
    a.output.write_text(out,encoding='utf-8');a.output.chmod(0o700)
    print('TRACK_A_VNC_OBSERVER_ACCESS_V23_REPAIR=PASS');return 0

if __name__=='__main__':raise SystemExit(main())
