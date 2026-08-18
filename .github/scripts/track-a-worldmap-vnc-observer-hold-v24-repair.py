#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

OLD = '''# Secrets enter this shell only through the protected FIFO after both dummy gates.\nexec {CRED_FD}<>"$CRED_FIFO"\nEMAIL_SECRET=''\nPASSWORD_SECRET=''\nIFS= read -r -d '' -t 180 -u "$CRED_FD" EMAIL_SECRET || fail credential_email_handoff_timeout\nIFS= read -r -d '' -t 30 -u "$CRED_FD" PASSWORD_SECRET || fail credential_password_handoff_timeout\nexec {CRED_FD}>&-\nrm -f "$CRED_FIFO" "$READY"\n[[ -n "$EMAIL_SECRET" && -n "$PASSWORD_SECRET" ]] || fail credential_handoff_empty\necho 'WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES'\n'''

NEW = '''# V24 observer-only hold. Never consume credentials and never advance into login.\n# Keep the exact client/Xvfb/x11vnc alive until the workflow explicitly stops it.\necho 'TRACK_A_VNC_OBSERVER_HOLD=ACTIVE_NO_SECRET_NO_LOGIN'\nwhile :; do\n  [[ -e "$ROOT/vnc-observer-stop" ]] && break\n  kill -0 "$PID" 2>/dev/null || fail observer_client_exited\n  sleep 1\ndone\nfail observer_stop_requested\n'''

class Refused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(OLD) != 1:
        raise Refused(f'CREDENTIAL_BLOCK_COUNT:{text.count(OLD)}')
    out = text.replace(OLD, NEW, 1)
    for marker in (
        'TRACK_A_VNC_OBSERVER_HOLD=ACTIVE_NO_SECRET_NO_LOGIN',
        'vnc-observer-stop',
        'kill -0 "$PID"',
    ):
        if marker not in out:
            raise Refused('MISSING:'+marker)
    if 'credential_email_handoff_timeout' in out:
        raise Refused('CREDENTIAL_TIMEOUT_SURVIVED')
    return out


def main() -> int:
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
    try: out=transform(a.source.read_text(encoding='utf-8'))
    except Refused as exc:
        print(f'TRACK_A_VNC_OBSERVER_HOLD_V24_REFUSED={exc}');return 44
    a.output.write_text(out,encoding='utf-8');a.output.chmod(0o700)
    print('TRACK_A_VNC_OBSERVER_HOLD_V24_REPAIR=PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
