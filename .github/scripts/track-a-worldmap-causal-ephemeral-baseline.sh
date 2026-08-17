#!/usr/bin/env bash
set +x
set -Eeuo pipefail
umask 077

TASK_ID=OTC-20260817-track-a-worldmap-server-delivery-causal-validation
NAMESPACE=worldmap-causal-baseline-ephemeral-v1
BASE=/home/runner/_work/_otclient_tibia_re_state
ROOT="$BASE/tasks/$TASK_ID/$NAMESPACE"
SESSION="$ROOT/session"
MANIFEST="$ROOT/manifest.json"
EVIDENCE="$RUNNER_TEMP/worldmap-baseline-evidence"
STAGE_WORKER="$RUNNER_TEMP/worldmap-baseline-stage-worker"
WORKER="$RUNNER_TEMP/worldmap-baseline-xres-worker"
GCMD="$RUNNER_TEMP/worldmap-baseline.gdb"
EVENTS="$ROOT/worldmap-events.tsv"
STRIPS="$ROOT/worldmap-strips.tsv"
GOUT="$ROOT/worldmap-gdb.stdout"
EXPECTED_SHA=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
EPHEMERAL_MARK="OTCLIENT_TIBIA_RE_EPHEMERAL_RUNTIME=$NAMESPACE"
GDB_PID=''
PGID=''

fail() { printf 'WORLDMAP_BASELINE_ERROR=%s\n' "$1" >&2; exit 1; }

cleanup() {
  local rc=$? pid source
  set +e
  if [[ -n "$GDB_PID" && "$GDB_PID" =~ ^[1-9][0-9]*$ ]] && kill -0 "$GDB_PID" 2>/dev/null; then
    kill -INT "$GDB_PID" 2>/dev/null || true
    for _ in $(seq 1 40); do kill -0 "$GDB_PID" 2>/dev/null || break; sleep .1; done
    kill -KILL "$GDB_PID" 2>/dev/null || true
  fi
  if [[ -z "$PGID" && -r "$SESSION/bootstrap-pgid" ]]; then PGID="$(tr -cd '0-9' <"$SESSION/bootstrap-pgid")"; fi
  if [[ -n "$PGID" && "$PGID" =~ ^[1-9][0-9]*$ ]]; then
    kill -TERM -- "-$PGID" 2>/dev/null || true
    for _ in $(seq 1 60); do
      ps -eo pgid= 2>/dev/null | tr -d ' ' | grep -Fxq "$PGID" || break
      sleep .1
    done
    kill -KILL -- "-$PGID" 2>/dev/null || true
    sleep .2
    [[ ! -x "$WORKER" ]] || "$WORKER" rollback "$PGID" >/dev/null 2>&1 || true
  fi
  rm -rf --one-file-system "$ROOT" 2>/dev/null || true
  rm -f "$STAGE_WORKER" "$WORKER" "$GCMD" 2>/dev/null || true

  source="$BASE/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"
  if [[ ! -x "$source" ]]; then source="/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"; fi
  if [[ -x "$source" && "$(sha256sum "$source" 2>/dev/null | awk '{print $1}')" == "$EXPECTED_SHA" ]]; then
    echo 'WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS'
  else
    echo 'WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=FAIL' >&2
    [[ $rc -ne 0 ]] || rc=97
  fi
  echo 'WORLDMAP_BASELINE_CLEANUP=COMPLETE'
  exit "$rc"
}
trap cleanup EXIT INT TERM

[[ "${RUNNER_NAME:-}" == synology-otclient-01 ]] || fail wrong_runner
[[ "${GITHUB_REPOSITORY:-}" == blakinio/otclient ]] || fail wrong_repository
[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]] || fail protected_login_secrets_missing

# Fail closed if any process from this task-owned namespace survived a prior run.
python3 - "$EPHEMERAL_MARK" <<'PY'
from pathlib import Path
import sys
marker=sys.argv[1].encode()
found=[]
for p in Path('/proc').iterdir():
    if not p.name.isdigit(): continue
    try: fields=set((p/'environ').read_bytes().split(b'\0'))
    except OSError: continue
    if marker in fields: found.append(int(p.name))
print('WORLDMAP_BASELINE_PREEXISTING_NAMESPACE_PROCESS_COUNT='+str(len(found)))
if found: raise SystemExit('WORLDMAP_BASELINE_ERROR=namespace_not_unique')
PY
rm -rf --one-file-system "$ROOT"
mkdir -p "$ROOT" "$EVIDENCE"
chmod 700 "$ROOT" "$EVIDENCE"

# Compose the reviewed canonical worker into a task-owned ephemeral namespace, then apply merged #465 XRes identity.
python3 - "$STAGE_WORKER" "$TASK_ID" "$NAMESPACE" <<'PY'
from pathlib import Path
import sys
out,task,ns=sys.argv[1:]
src=Path('.github/scripts/tibia-official-client-re-canonical-live-session.sh').read_text()
old='ROOT="$BASE/canonical-live-runtime"'
new=f'ROOT="$BASE/tasks/{task}/{ns}"'
if src.count(old)!=1: raise SystemExit('WORLDMAP_BASELINE_ERROR=root_anchor_drift')
src=src.replace(old,new)
oldmark='OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1'
newmark=f'OTCLIENT_TIBIA_RE_EPHEMERAL_RUNTIME={ns}'
if src.count(oldmark)<5: raise SystemExit('WORLDMAP_BASELINE_ERROR=runtime_marker_anchor_drift')
src=src.replace(oldmark,newmark)
Path(out).write_text(src)
Path(out).chmod(0o700)
PY
python3 .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py \
  "$STAGE_WORKER" "$WORKER" \
  --owner-helper .github/scripts/tibia-official-client-re-xres-window-owner.py \
  --wire-helper .github/scripts/tibia-official-client-re-xres-wire.py
bash -n "$WORKER"
test -x "$WORKER"
! grep -F 'search --onlyvisible --pid' "$WORKER" >/dev/null || fail legacy_window_selector_survived
! grep -F 'OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1' "$WORKER" >/dev/null || fail canonical_marker_survived
! grep -F 'canonical-live-runtime' "$WORKER" >/dev/null || fail canonical_namespace_survived
grep -F "$EPHEMERAL_MARK" "$WORKER" >/dev/null || fail ephemeral_marker_missing
echo 'WORLDMAP_BASELINE_EPHEMERAL_XRES_WORKER=PASS'

# Start one exact task-owned process group. No canonical lease/registration is touched.
env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
  setsid "$WORKER" bootstrap "$MANIFEST"

python3 - "$MANIFEST" <<'PY'
import json,sys,re
m=json.load(open(sys.argv[1]))
for k in ('pid','process_group_id','display','window_identity','remote_view_endpoint','remote_view_mapping'):
    if k not in m: raise SystemExit('WORLDMAP_BASELINE_ERROR=manifest_missing_'+k)
if m['remote_view_mapping']!='PROVEN': raise SystemExit('WORLDMAP_BASELINE_ERROR=remote_view_mapping_not_proven')
if not re.fullmatch(r'x11-window:[1-9][0-9]*',str(m['window_identity'])): raise SystemExit('WORLDMAP_BASELINE_ERROR=xres_window_identity_invalid')
print('WORLDMAP_BASELINE_MANIFEST_FENCE=PASS')
print('WORLDMAP_BASELINE_CLIENT_PID='+str(m['pid']))
print('WORLDMAP_BASELINE_WINDOW_IDENTITY='+str(m['window_identity']))
PY
PID="$(python3 -c 'import json;print(json.load(open("'"$MANIFEST"'"))["pid"])')"
PGID="$(python3 -c 'import json;print(json.load(open("'"$MANIFEST"'"))["process_group_id"])')"
DISPLAY="$(python3 -c 'import json;print(json.load(open("'"$MANIFEST"'"))["display"])')"
WIN="$(python3 -c 'import json;print(json.load(open("'"$MANIFEST"'"))["window_identity"].split(":",1)[1])')"
[[ "$PID" =~ ^[1-9][0-9]*$ && "$PGID" =~ ^[1-9][0-9]*$ && "$WIN" =~ ^[1-9][0-9]*$ ]] || fail manifest_numeric_field_invalid
kill -0 "$PID" || fail client_not_alive_after_bootstrap
grep -azFxq 'OTCLIENT_TIBIA_RE_TRACK=official-client-re' "/proc/$PID/environ" || fail client_track_marker_missing
grep -azFxq "$EPHEMERAL_MARK" "/proc/$PID/environ" || fail client_ephemeral_marker_missing
! grep -azFxq 'OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1' "/proc/$PID/environ" || fail client_canonical_marker_present
CLIENT="$SESSION/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"
[[ "$(readlink -f "/proc/$PID/exe")" == "$(readlink -f "$CLIENT")" ]] || fail client_exe_identity_mismatch
[[ "$(sha256sum "$CLIENT"|awk '{print $1}')" == "$EXPECTED_SHA" ]] || fail client_sha_mismatch
TOOL="$(cat "$SESSION/toolroot")"
XDOTOOL="$TOOL/usr/bin/xdotool"
[[ -x "$XDOTOOL" ]] || fail xdotool_missing
WARP_PORT="$(cat "$SESSION/warp-port")"

echo 'WORLDMAP_BASELINE_TARGET_UNIQUENESS=PROVEN'

# Arm the already-proven pre-Storage worldmap observer before login.
line="$(grep -F "$CLIENT" "/proc/$PID/maps" | awk '$2~/r-xp/{print;exit}')"
[[ -n "$line" ]] || fail client_exec_mapping_missing
start="$(awk '{split($1,a,"-");print a[1]}'<<<"$line")"
off="$(awk '{print $3}'<<<"$line")"
bias=$((16#$start-16#$off))
:>"$EVENTS"; :>"$STRIPS"; :>"$GOUT"; chmod 600 "$EVENTS" "$STRIPS" "$GOUT"
python3 - "$GCMD" "$PID" "$bias" "$EVENTS" "$STRIPS" <<'PY'
import sys
out,pid,bias,ev,strips=sys.argv[1:]
t=r'''set pagination off
set confirm off
attach @PID@
python
import gdb,struct,time
inf=gdb.selected_inferior();ev=r'@EV@';strips=r'@STRIPS@'
def mem(a,n):
    try:return bytes(inf.read_memory(a,n))
    except:return None
class M(gdb.Breakpoint):
    def __init__(self,o,n):self.n=n;super().__init__('*0x%x'%(@BIAS@+o),internal=False)
    def stop(self):
        try:
            with open(ev,'a') as f:f.write(f'{time.time_ns()}\t{self.n}\n')
        except:pass
        return False
M(0xcec8d0,'FullMap');M(0xcecc70,'CreateOnMap');M(0xcecf40,'ChangeOnMap');M(0xcd4e20,'DeleteOnMap')
class S(gdb.Breakpoint):
    def __init__(self):super().__init__('*0x%x'%(@BIAS@+0x19a8ea3),internal=False)
    def stop(self):
        try:
            ns=time.time_ns();rsp=int(gdb.parse_and_eval('$rsp'));order=int(gdb.parse_and_eval('$rbp'))&0xffffffff;b=mem(rsp+0x88,12)
            if b:
                x,y,z=struct.unpack('<III',b)
                if 0<x<100000 and 0<y<100000 and z<32 and order<128:
                    with open(strips,'a') as f:f.write(f'{ns}\t{x}\t{y}\t{z}\t{order}\n')
        except:pass
        return False
S()
end
continue
'''
open(out,'w').write(t.replace('@PID@',pid).replace('@BIAS@',bias).replace('@EV@',ev).replace('@STRIPS@',strips))
PY
chmod 600 "$GCMD"
GDB="$TOOL/usr/bin/gdb"
[[ -x "$GDB" ]] || fail gdb_missing
nohup setsid env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
  OTCLIENT_TIBIA_RE_TRACK=official-client-re "$EPHEMERAL_MARK" OTCLIENT_TIBIA_RE_ROLE=worldmap-observer \
  "$GDB" -q -nx -batch -x "$GCMD" >"$GOUT" 2>&1 </dev/null &
GDB_PID=$!
echo "$GDB_PID" >"$ROOT/gdb.pid"
sleep 2
kill -0 "$PID" || fail client_died_while_arming_observer
kill -0 "$GDB_PID" || fail gdb_observer_not_alive
[[ "$(awk '/^TracerPid:/{print $2}' "/proc/$PID/status")" == "$GDB_PID" ]] || fail gdb_not_attached_to_exact_client
echo 'WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED'

# Screenshot/OCR is used only to locate login/character-selection controls. No screenshot or OCR text is retained.
XWD="$(command -v xwd 2>/dev/null || true)"
[[ -n "$XWD" ]] || XWD="$(find "$TOOL" -xdev -type f -name xwd -perm -111 -print -quit 2>/dev/null || true)"
TESS="$(command -v tesseract 2>/dev/null || true)"
CONVERT="$(command -v convert 2>/dev/null || true)"
MAGICK="$(command -v magick 2>/dev/null || true)"
[[ -x "$XWD" ]] || fail xwd_missing_before_secret_use
[[ -x "$TESS" ]] || fail tesseract_missing_before_secret_use
[[ -x "$CONVERT" || -x "$MAGICK" ]] || fail imagemagick_missing_before_secret_use

echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=PASS'

capture_ocr() {
  local stem="$1" xwdfile="$ROOT/$stem.xwd" png="$ROOT/$stem.png" tsv="$ROOT/$stem.tsv"
  DISPLAY="$DISPLAY" "$XWD" -silent -id "$WIN" -out "$xwdfile"
  if [[ -x "$MAGICK" ]]; then "$MAGICK" "$xwdfile" "$png" >/dev/null 2>&1; else "$CONVERT" "$xwdfile" "$png" >/dev/null 2>&1; fi
  "$TESS" "$png" stdout --psm 6 tsv 2>/dev/null >"$tsv"
  rm -f "$xwdfile" "$png"
  printf '%s\n' "$tsv"
}

PRE_TSV="$(capture_ocr prelogin)"
COORDS="$(python3 - "$PRE_TSV" <<'PY'
import csv,json,sys
a=[]
with open(sys.argv[1],newline='',errors='replace') as f:
    for r in csv.DictReader(f,delimiter='\t'):
        text=(r.get('text') or '').strip(); low=text.casefold().strip(':')
        try: conf=float(r.get('conf') or -1)
        except: conf=-1
        if not text or conf<20: continue
        try: box=[int(r[k]) for k in ('left','top','width','height')]
        except: continue
        a.append((low,box))
def pick(word,which='first'):
    hits=[b for t,b in a if t==word or t.startswith(word)]
    if not hits:return None
    b=(max(hits,key=lambda x:x[1]) if which=='lowest' else min(hits,key=lambda x:x[1]))
    return [b[0]+b[2]//2,b[1]+b[3]//2]
out={'email':pick('email'),'password':pick('password'),'login':pick('login','lowest')}
print(json.dumps(out,separators=(',',':')))
PY
)"
rm -f "$PRE_TSV"
python3 - "$COORDS" <<'PY'
import json,sys
c=json.loads(sys.argv[1])
if not all(c.get(k) for k in ('email','password','login')): raise SystemExit('WORLDMAP_BASELINE_ERROR=login_ocr_anchors_missing')
print('WORLDMAP_BASELINE_LOGIN_OCR_ANCHORS=PASS')
PY
EMAIL_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email"][0])' "$COORDS")"
EMAIL_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email"][1])' "$COORDS")"
PASS_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password"][0])' "$COORDS")"
PASS_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password"][1])' "$COORDS")"
LOGIN_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["login"][0])' "$COORDS")"
LOGIN_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["login"][1])' "$COORDS")"

DISPLAY="$DISPLAY" "$XDOTOOL" windowactivate --sync "$WIN"
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$WIN" "$EMAIL_X" "$EMAIL_Y" click 1 key --clearmodifiers ctrl+a
printf '%s' "$TIBIA_TEST_EMAIL" | DISPLAY="$DISPLAY" "$XDOTOOL" type --window "$WIN" --clearmodifiers --file -
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$WIN" "$PASS_X" "$PASS_Y" click 1 key --clearmodifiers ctrl+a
printf '%s' "$TIBIA_TEST_PASSWORD" | DISPLAY="$DISPLAY" "$XDOTOOL" type --window "$WIN" --clearmodifiers --file -
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$WIN" "$LOGIN_X" "$LOGIN_Y" click 1
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

SELECT_TSV=''
for i in $(seq 1 35); do
  sleep 2
  tsv="$(capture_ocr "select-$i")"
  if python3 - "$tsv" <<'PY'
import csv,sys
w=[]
with open(sys.argv[1],newline='',errors='replace') as f:
    for r in csv.DictReader(f,delimiter='\t'):
        t=(r.get('text') or '').strip().casefold().strip(':')
        try:c=float(r.get('conf') or -1)
        except:c=-1
        if c>=20 and t:w.append(t)
raise SystemExit(0 if any(x.startswith('character') for x in w) and any(x.startswith('status') for x in w) else 1)
PY
  then SELECT_TSV="$tsv"; break; fi
  rm -f "$tsv"
done
[[ -n "$SELECT_TSV" ]] || fail character_selection_transition_not_observed
echo 'WORLDMAP_BASELINE_CHARACTER_SELECTION=PROVEN_UI_TRANSITION'

ROW="$(python3 - "$SELECT_TSV" <<'PY'
import csv,json,sys,collections
rows=[]
with open(sys.argv[1],newline='',errors='replace') as f:
    for r in csv.DictReader(f,delimiter='\t'):
        t=(r.get('text') or '').strip(); low=t.casefold().strip(':')
        try:c=float(r.get('conf') or -1); left=int(r['left']);top=int(r['top']);width=int(r['width']);height=int(r['height'])
        except:continue
        if c<20 or not t:continue
        rows.append((low,left,top,width,height))
headers=[r for r in rows if r[0].startswith('character')]
if not headers: raise SystemExit(2)
h=min(headers,key=lambda r:r[2]); hy=h[2]+h[4]//2; hx=h[1]+h[3]//2
b=collections.defaultdict(list)
for r in rows:
    cy=r[2]+r[4]//2
    if cy<=hy+18:continue
    key=round(cy/8)*8;b[key].append(r)
cand=sorted((y,grp) for y,grp in b.items() if len(grp)>=2)
if not cand: y=hy+60
else:y=cand[0][0]
print(json.dumps({'x':hx,'y':y},separators=(',',':')))
PY
)"
rm -f "$SELECT_TSV"
ROW_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["x"])' "$ROW")"
ROW_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["y"])' "$ROW")"
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$WIN" "$ROW_X" "$ROW_Y" click 1 key Return
echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_SENT=true'

world=0
for _ in $(seq 1 40); do
  sleep 1
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then world=1; break; fi
done
if [[ "$world" != 1 ]]; then
  DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$WIN" "$ROW_X" "$ROW_Y" click --repeat 2 --delay 120 1 key Return
  echo 'WORLDMAP_BASELINE_CHARACTER_DOUBLECLICK_FALLBACK_SENT=true'
  for _ in $(seq 1 30); do
    sleep 1
    if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then world=1; break; fi
  done
fi
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed
FULLMAP_COUNT="$(grep -Fc $'\tFullMap' "$EVENTS")"
PRE_MOVE_COUNT="$(wc -l <"$STRIPS")"
[[ "$FULLMAP_COUNT" -ge 1 && "$PRE_MOVE_COUNT" -ge 10 ]] || fail structural_world_entry_counts_invalid
awk -F'\t' 'NF>=5{print $1"\t"$2"\t"$3"\t"$4"\t"$5}' "$STRIPS" >"$EVIDENCE/baseline-pre-move-strips.tsv"
echo "WORLDMAP_BASELINE_STRUCTURAL_FULLMAP_COUNT=$FULLMAP_COUNT"
echo "WORLDMAP_BASELINE_STRUCTURAL_PRE_MOVE_STRIP_COUNT=$PRE_MOVE_COUNT"

# Verify client transport confinement from its own socket inode set.
python3 - "$PID" "$WARP_PORT" <<'PY'
from pathlib import Path
import os,socket,struct,sys
pid=int(sys.argv[1]); socks_port=int(sys.argv[2]); inodes=set()
for fd in (Path('/proc')/str(pid)/'fd').iterdir():
    try:s=os.readlink(fd)
    except OSError:continue
    if s.startswith('socket:['):inodes.add(s[8:-1])
def ip4(h):return socket.inet_ntoa(struct.pack('<I',int(h,16)))
def read(name,udp=False):
    out=[];p=Path('/proc/net')/name
    if not p.exists():return out
    for line in p.read_text().splitlines()[1:]:
        f=line.split()
        if len(f)<10 or f[9] not in inodes:continue
        la,lp=f[1].split(':');ra,rp=f[2].split(':')
        if name.endswith('6'):
            rip='ipv6'
        else:rip=ip4(ra)
        out.append((rip,int(rp,16),f[3]))
    return out
tcp=read('tcp')+read('tcp6');udp=read('udp',True)+read('udp6',True)
socks=sum(1 for rip,rp,st in tcp if rip=='127.0.0.1' and rp==socks_port and st=='01')
direct=sum(1 for rip,rp,st in tcp if st=='01' and not (rip=='127.0.0.1' and rp==socks_port))
print('WORLDMAP_BASELINE_CLIENT_LOCAL_SOCKS_ESTABLISHED='+str(socks))
print('WORLDMAP_BASELINE_CLIENT_DIRECT_TCP_ESTABLISHED='+str(direct))
print('WORLDMAP_BASELINE_CLIENT_UDP_SOCKET_COUNT='+str(len(udp)))
if socks<1 or direct!=0 or udp:raise SystemExit('WORLDMAP_BASELINE_ERROR=network_confinement_failed')
PY

# One bounded movement plus inverse; structural delivery is measured, command success is not assumed.
DISPLAY="$DISPLAY" "$XDOTOOL" windowactivate --sync "$WIN" key --clearmodifiers Right
sleep 3
MID_COUNT="$(wc -l <"$STRIPS")"
DISPLAY="$DISPLAY" "$XDOTOOL" key --clearmodifiers Left
sleep 3
POST_MOVE_COUNT="$(wc -l <"$STRIPS")"
echo "WORLDMAP_BASELINE_STRIP_COUNT_AFTER_RIGHT=$MID_COUNT"
echo "WORLDMAP_BASELINE_STRIP_COUNT_AFTER_REVERSAL=$POST_MOVE_COUNT"

# Build privacy-safe structural evidence only: coordinates/order and aggregate extents, never screenshots/OCR/raw memory.
awk -F'\t' 'NF>=5{print $1"\t"$2"\t"$3"\t"$4"\t"$5}' "$STRIPS" >"$EVIDENCE/baseline-all-strips.tsv"
python3 - "$EVIDENCE/baseline-pre-move-strips.tsv" "$EVIDENCE/summary.json" "$FULLMAP_COUNT" "$PRE_MOVE_COUNT" "$MID_COUNT" "$POST_MOVE_COUNT" <<'PY'
import collections,json,sys
path,out,fullmap,pre,mid,post=sys.argv[1:]
recs=[]
for line in open(path):
    p=line.rstrip('\n').split('\t')
    if len(p)>=5:recs.append(tuple(map(int,p[:5])))
floors={}
for z in sorted({r[3] for r in recs}):
    pts=[(r[1],r[2]) for r in recs if r[3]==z]
    unique=sorted(set(pts)); xs=[p[0] for p in unique];ys=[p[1] for p in unique]
    rows=collections.defaultdict(set);cols=collections.defaultdict(set)
    for x,y in unique:rows[y].add(x);cols[x].add(y)
    floors[str(z)]={
        'unique_coordinate_count':len(unique),
        'min_x':min(xs),'max_x':max(xs),'x_span':max(xs)-min(xs)+1,
        'min_y':min(ys),'max_y':max(ys),'y_span':max(ys)-min(ys)+1,
        'max_unique_x_per_y':max(map(len,rows.values())),
        'max_unique_y_per_x':max(map(len,cols.values())),
    }
primary=max(floors,key=lambda z:floors[z]['unique_coordinate_count']) if floors else None
summary={
 'schema':'worldmap-causal-baseline-v1',
 'exact_client_sha256':'e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe',
 'fullmap_event_count':int(fullmap),'pre_move_strip_count':int(pre),
 'after_right_strip_count':int(mid),'after_reversal_strip_count':int(post),
 'movement_added_strip_records':int(post)-int(pre),
 'floors':floors,'primary_floor':primary,
 'primary_floor_extent':floors.get(primary) if primary else None,
 'structural_in_game':bool(int(fullmap)>=1 and int(pre)>=10),
 'network_confinement':'PASS',
}
open(out,'w').write(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('WORLDMAP_BASELINE_STRUCTURAL_SUMMARY='+json.dumps(summary,sort_keys=True,separators=(',',':')))
PY
chmod 600 "$EVIDENCE"/*
rm -f "$ROOT"/*.xwd "$ROOT"/*.png "$ROOT"/*.tsv 2>/dev/null || true

echo 'WORLDMAP_BASELINE_PHYSICAL_CAPTURE=PASS'
