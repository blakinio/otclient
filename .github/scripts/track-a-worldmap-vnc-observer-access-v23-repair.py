#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

VNC_OLD = r'''  printf 'TRACK_A_CANONICAL_STAGE=vnc_start\n'
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 \
    OTCLIENT_TIBIA_RE_ROLE=vnc HOME="$home" DISPLAY="$display" \
    nohup "$vnc" -display "$display" -rfbport "$vnc_port" -forever -shared -viewonly \
    -localhost -nopw -noxdamage >"$SESSION/vnc.log" 2>&1 </dev/null &
  echo $! >"$SESSION/vnc.pid"
'''

VNC_NEW = r'''  # User-observer VNC remains the exact same task-owned Xvfb/display. It is
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
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 \
    OTCLIENT_TIBIA_RE_ROLE=vnc HOME="$home" DISPLAY="$display" \
    nohup "$vnc" -display "$display" -rfbport "$vnc_port" -forever -shared -viewonly \
    -listen 0.0.0.0 -passwdfile "$vnc_password_file" -noxdamage >"$SESSION/vnc.log" 2>&1 </dev/null &
  echo $! >"$SESSION/vnc.pid"
  echo "$vnc_password_file" >"$SESSION/vnc-password-file"
  chmod 600 "$SESSION/vnc-password-file"
  printf 'TRACK_A_USER_VNC_MODE=VIEW_ONLY_PASSWORD_PROTECTED\n'
  printf 'TRACK_A_USER_VNC_PORT=%s\n' "$vnc_port"
  printf 'TRACK_A_USER_VNC_PASSWORD_FILE=%s\n' "$vnc_password_file"
'''

class Refused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(VNC_OLD) != 1:
        raise Refused(f"VNC_ANCHOR_COUNT:{text.count(VNC_OLD)}")
    out = text.replace(VNC_OLD, VNC_NEW, 1)
    required = (
        "TRACK_A_USER_VNC_MODE=VIEW_ONLY_PASSWORD_PROTECTED",
        "TRACK_A_USER_VNC_PORT=%s",
        "-viewonly",
        "-listen 0.0.0.0",
        "-passwdfile \"$vnc_password_file\"",
        "vnc-viewonly.password",
        "chmod 600 \"$vnc_password_file\"",
    )
    missing = [x for x in required if x not in out]
    if missing:
        raise Refused("REQUIRED_MISSING:" + ",".join(missing))
    for forbidden in ("-localhost -nopw", "TIBIA_TEST_PASSWORD=", "TIBIA_TEST_EMAIL="):
        if forbidden in out and forbidden == "-localhost -nopw":
            raise Refused("LEGACY_UNREACHABLE_VNC_SURVIVED")
    return out


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('source',type=Path)
    ap.add_argument('output',type=Path)
    a=ap.parse_args()
    try:
        out=transform(a.source.read_text(encoding='utf-8'))
    except Refused as exc:
        print(f'TRACK_A_VNC_OBSERVER_ACCESS_V23_REFUSED={exc}')
        return 44
    a.output.write_text(out,encoding='utf-8')
    a.output.chmod(0o700)
    print('TRACK_A_VNC_OBSERVER_ACCESS_V23_REPAIR=PASS')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
