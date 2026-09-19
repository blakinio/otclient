#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

START = "echo 'WORLDMAP_BASELINE_PRESECRET_ONLY_COMPLETE=true'\n"

TAIL = r'''echo 'WORLDMAP_BASELINE_LOGIN_V6=ARMED_AFTER_PRESECRET'

# Keep one blank, no-secret XWD reference for the login->character-selection
# aggregate transition. It is transient and never uploaded.
PRELOGIN_REFERENCE="$ROOT/prelogin-reference.xwd"
sleep .20
capture_xwd "$PRELOGIN_REFERENCE"

# Secrets enter this helper only through the already-created mode-0600 FIFO,
# after all v5 editability and semantic field gates have passed.
exec {CRED_FD}<>"$CRED_FIFO"
EMAIL_SECRET=''
PASSWORD_SECRET=''
IFS= read -r -d '' -t 180 -u "$CRED_FD" EMAIL_SECRET || fail credential_email_handoff_timeout
IFS= read -r -d '' -t 30 -u "$CRED_FD" PASSWORD_SECRET || fail credential_password_handoff_timeout
exec {CRED_FD}>&-
rm -f "$CRED_FIFO" "$READY"
[[ -n "$EMAIL_SECRET" && -n "$PASSWORD_SECRET" ]] || fail credential_handoff_empty
echo 'WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES'

# Reuse only the v4/v5 physically discovered field targets from this same
# launch. No historical login coordinate and no alternate XID is used.
xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"
xdo mousemove --window "$UI_WIN" "$EMAIL_X" "$EMAIL_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
printf '%s' "$EMAIL_SECRET" | xdo type --window "$UI_WIN" --delay 10 --file -
xdo mousemove --window "$UI_WIN" "$PASS_X" "$PASS_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
printf '%s' "$PASSWORD_SECRET" | xdo type --window "$UI_WIN" --delay 10 --file -
EMAIL_SECRET=''
PASSWORD_SECRET=''
unset EMAIL_SECRET PASSWORD_SECRET

# Password is the second physically proven local text field. Move exactly one
# focus step forward and activate the next control; success is never inferred
# from this keypress and requires the independent transition/structural gates.
xdo key --window "$UI_WIN" --clearmodifiers Tab
sleep .20
xdo key --window "$UI_WIN" --clearmodifiers Return
echo 'WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PASSWORD_TAB_RETURN'
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

POST_LOGIN_XWD=''
for i in $(seq 1 60); do
  sleep 1
  candidate="$ROOT/post-login-$i.xwd"
  capture_xwd "$candidate"
  set +e
  change_out="$(python3 "$COMPARE" change "$PRELOGIN_REFERENCE" "$candidate" --min-changed 5000 2>&1)"
  change_rc=$?
  set -e
  if [[ "$change_rc" -eq 0 ]]; then
    POST_LOGIN_XWD="$candidate"
    echo 'WORLDMAP_BASELINE_CHARACTER_SELECTION_TRANSITION=PROVEN_AGGREGATE'
    break
  fi
  rm -f "$candidate"
done
rm -f "$PRELOGIN_REFERENCE"
[[ -n "$POST_LOGIN_XWD" ]] || fail character_selection_transition_not_observed
rm -f "$POST_LOGIN_XWD"

# Historical 1020x650 row coordinates are not evidence. After the current
# launch has proven both live fields and character-selection transition, use
# their measured displacement only to form a bounded target neighborhood.
# The click itself must cause a localized aggregate row interaction before
# Return is permitted, and IN_GAME is still structural FullMap+strip proof.
DX=$(( ((EMAIL_X-535) + (PASS_X-535)) / 2 ))
DY=$(( ((EMAIL_Y-275) + (PASS_Y-304)) / 2 ))
ROW_X=$((285 + DX))
ROW_Y=$((193 + DY))
(( ROW_X >= 20 && ROW_X < ACTUAL_WIDTH-20 && ROW_Y >= 20 && ROW_Y < ACTUAL_HEIGHT-20 )) || fail translated_character_row_target_out_of_bounds
ROW_X0=$((100 + DX)); ROW_Y0=$((165 + DY)); ROW_X1=$((900 + DX)); ROW_Y1=$((230 + DY))
(( ROW_X0 < 0 )) && ROW_X0=0
(( ROW_Y0 < 0 )) && ROW_Y0=0
(( ROW_X1 > ACTUAL_WIDTH )) && ROW_X1=$ACTUAL_WIDTH
(( ROW_Y1 > ACTUAL_HEIGHT )) && ROW_Y1=$ACTUAL_HEIGHT
(( ROW_X0 < ROW_X1 && ROW_Y0 < ROW_Y1 )) || fail translated_character_row_roi_invalid
echo "WORLDMAP_BASELINE_CHARACTER_ROW_TARGET=$ROW_X,$ROW_Y"
echo "WORLDMAP_BASELINE_CHARACTER_ROW_ROI=$ROW_X0,$ROW_Y0,$ROW_X1,$ROW_Y1"

ROW_SELECTED=0
SELECT_X="$ROW_X"
SELECT_Y="$ROW_Y"
for yoff in 0 -24 24 -48 48; do
  ty=$((ROW_Y + yoff))
  (( ty >= ROW_Y0 && ty < ROW_Y1 )) || continue
  before="$ROOT/row-$yoff-before.xwd"
  after="$ROOT/row-$yoff-after.xwd"
  capture_xwd "$before"
  xdo mousemove --window "$UI_WIN" "$ROW_X" "$ty" click 1
  sleep .35
  capture_xwd "$after"
  set +e
  row_out="$(python3 "$COMPARE" change "$before" "$after" --min-changed 80 --x0 "$ROW_X0" --y0 "$ROW_Y0" --x1 "$ROW_X1" --y1 "$ROW_Y1" 2>&1)"
  row_rc=$?
  set -e
  rm -f "$before" "$after"
  if [[ "$row_rc" -eq 0 ]]; then
    ROW_SELECTED=1
    SELECT_Y="$ty"
    echo "WORLDMAP_BASELINE_CHARACTER_ROW_SELECTION_TARGET=$ROW_X,$ty"
    echo 'WORLDMAP_BASELINE_CHARACTER_ROW_SELECTION=PROVEN_AGGREGATE'
    break
  fi
done
[[ "$ROW_SELECTED" == 1 ]] || fail character_row_interaction_not_observed

xdo key --window "$UI_WIN" --clearmodifiers Return
echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_SENT=true'

world=0
for _ in $(seq 1 45); do
  sleep 1
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
    world=1
    break
  fi
done
if [[ "$world" != 1 ]]; then
  xdo mousemove --window "$UI_WIN" "$SELECT_X" "$SELECT_Y" click --repeat 2 --delay 120 1
  xdo key --window "$UI_WIN" --clearmodifiers Return
  echo 'WORLDMAP_BASELINE_CHARACTER_DOUBLECLICK_FALLBACK_SENT=true'
  for _ in $(seq 1 30); do
    sleep 1
    if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
      world=1
      break
    fi
  done
fi
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed
FULLMAP_COUNT="$(grep -Fc $'\tFullMap' "$EVENTS")"
PRE_MOVE_COUNT="$(wc -l <"$STRIPS")"
[[ "$FULLMAP_COUNT" -ge 1 && "$PRE_MOVE_COUNT" -ge 10 ]] || fail structural_world_entry_counts_invalid
echo 'WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS'
echo "WORLDMAP_BASELINE_STRUCTURAL_FULLMAP_COUNT=$FULLMAP_COUNT"
echo "WORLDMAP_BASELINE_STRUCTURAL_PRE_MOVE_STRIP_COUNT=$PRE_MOVE_COUNT"

python3 - "$PID" "$WARP_PORT" <<'PY'
from pathlib import Path
import os,socket,struct,sys
pid=int(sys.argv[1]); socks_port=int(sys.argv[2]); inodes=set()
for fd in (Path('/proc')/str(pid)/'fd').iterdir():
    try:s=os.readlink(fd)
    except OSError:continue
    if s.startswith('socket:['):inodes.add(s[8:-1])
def ip4(h):return socket.inet_ntoa(struct.pack('<I',int(h,16)))
def read(name):
    out=[];p=Path('/proc/net')/name
    if not p.exists():return out
    for line in p.read_text().splitlines()[1:]:
        f=line.split()
        if len(f)<10 or f[9] not in inodes:continue
        ra,rp=f[2].split(':')
        rip='ipv6' if name.endswith('6') else ip4(ra)
        out.append((rip,int(rp,16),f[3]))
    return out
tcp=read('tcp')+read('tcp6'); udp=read('udp')+read('udp6')
socks=sum(1 for rip,rp,st in tcp if rip=='127.0.0.1' and rp==socks_port and st=='01')
direct=sum(1 for rip,rp,st in tcp if st=='01' and not (rip=='127.0.0.1' and rp==socks_port))
print('WORLDMAP_BASELINE_CLIENT_LOCAL_SOCKS_ESTABLISHED='+str(socks))
print('WORLDMAP_BASELINE_CLIENT_DIRECT_TCP_ESTABLISHED='+str(direct))
print('WORLDMAP_BASELINE_CLIENT_UDP_SOCKET_COUNT='+str(len(udp)))
if socks<1 or direct!=0 or udp:raise SystemExit('WORLDMAP_BASELINE_ERROR=network_confinement_failed')
PY
echo 'WORLDMAP_BASELINE_TRANSPORT_CONFINEMENT=PASS'

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo key --window "$UI_WIN" --clearmodifiers Right
sleep 3
MID_COUNT="$(wc -l <"$STRIPS")"
xdo key --window "$UI_WIN" --clearmodifiers Left
sleep 3
POST_MOVE_COUNT="$(wc -l <"$STRIPS")"
echo "WORLDMAP_BASELINE_STRIP_COUNT_AFTER_RIGHT=$MID_COUNT"
echo "WORLDMAP_BASELINE_STRIP_COUNT_AFTER_REVERSAL=$POST_MOVE_COUNT"

python3 - "$STRIPS" "$FULLMAP_COUNT" "$PRE_MOVE_COUNT" "$MID_COUNT" "$POST_MOVE_COUNT" <<'PY'
import collections,json,sys
path,fullmap,pre,mid,post=sys.argv[1:]
recs=[]
for line in open(path):
    p=line.rstrip('\n').split('\t')
    if len(p)>=5:recs.append(tuple(map(int,p[:5])))
floors={}
for z in sorted({r[3] for r in recs}):
    pts=sorted(set((r[1],r[2]) for r in recs if r[3]==z))
    if not pts:continue
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    rows=collections.defaultdict(set); cols=collections.defaultdict(set)
    for x,y in pts: rows[y].add(x); cols[x].add(y)
    floors[str(z)]={
      'unique_coordinate_count':len(pts),'min_x':min(xs),'max_x':max(xs),'x_span':max(xs)-min(xs)+1,
      'min_y':min(ys),'max_y':max(ys),'y_span':max(ys)-min(ys)+1,
      'max_unique_x_per_y':max(map(len,rows.values())),'max_unique_y_per_x':max(map(len,cols.values()))}
primary=max(floors,key=lambda z:floors[z]['unique_coordinate_count']) if floors else None
summary={'schema':'worldmap-causal-baseline-v2','fullmap_event_count':int(fullmap),'pre_move_strip_count':int(pre),
 'after_right_strip_count':int(mid),'after_reversal_strip_count':int(post),'movement_added_strip_records':int(post)-int(pre),
 'floors':floors,'primary_floor':primary,'primary_floor_extent':floors.get(primary) if primary else None,
 'structural_in_game':bool(int(fullmap)>=1 and int(pre)>=10),'network_confinement':'PASS'}
print('WORLDMAP_BASELINE_STRUCTURAL_SUMMARY='+json.dumps(summary,sort_keys=True,separators=(',',':')))
PY

rm -f "$ROOT"/*.xwd "$ROOT"/*.png 2>/dev/null || true
echo 'WORLDMAP_BASELINE_PHYSICAL_CAPTURE=PASS'
'''

class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(START) != 1:
        raise TransformRefused(f"START_COUNT:{text.count(START)}")
    start=text.index(START)
    output=text[:start] + TAIL
    required=(
        'WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS',
        'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS',
        'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS',
        'WORLDMAP_BASELINE_PRESECRET_READY=true',
        'WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES',
        'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true',
        'WORLDMAP_BASELINE_CHARACTER_SELECTION_TRANSITION=PROVEN_AGGREGATE',
        'WORLDMAP_BASELINE_CHARACTER_ROW_SELECTION=PROVEN_AGGREGATE',
        'WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS',
        'WORLDMAP_BASELINE_TRANSPORT_CONFINEMENT=PASS',
        'WORLDMAP_BASELINE_PHYSICAL_CAPTURE=PASS',
        'UI_WIN="$WIN"',
        'EMAIL_X', 'PASS_X',
    )
    missing=[token for token in required if token not in output]
    if missing:
        raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    forbidden=(
        'WORLDMAP_BASELINE_PRESECRET_ONLY_COMPLETE=true',
        'presecret_only_stop_timeout',
        '"$XWD" -root',
        'xwd -root',
        'xrandr --output',
        'wmctrl -r',
        'printf \'%s\' "$TIBIA_TEST_EMAIL"',
        'printf \'%s\' "$TIBIA_TEST_PASSWORD"',
        'EMAIL_X=535',
        'PASS_X=535',
        'LOGIN_X=590',
    )
    survivors=[token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused('FORBIDDEN_SURVIVORS:'+','.join(survivors))
    if output.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused('MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE')
    return output


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('source',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
    try: out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_BASELINE_LOGIN_V6_REPAIR_REFUSED={exc}'); return 44
    a.output.write_text(out,encoding='utf-8'); a.output.chmod(0o700)
    print('WORLDMAP_BASELINE_LOGIN_V6_REPAIR=PASS'); return 0

if __name__=='__main__':
    raise SystemExit(main())
