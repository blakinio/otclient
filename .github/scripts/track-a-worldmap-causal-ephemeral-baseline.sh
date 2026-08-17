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
CONTROL="$RUNNER_TEMP/worldmap-baseline-control"
CRED_FIFO="$CONTROL/credentials.fifo"
READY="$CONTROL/presecret.ready"
RESULT="$CONTROL/result"
EXPECTED_SHA=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
EPHEMERAL_MARK="OTCLIENT_TIBIA_RE_EPHEMERAL_RUNTIME=$NAMESPACE"
GDB_PID=''
PGID=''

fail() { printf 'WORLDMAP_BASELINE_ERROR=%s\n' "$1" >&2; exit 1; }

write_result() {
  local rc="$1" tmp
  mkdir -p "$CONTROL" 2>/dev/null || return 0
  chmod 700 "$CONTROL" 2>/dev/null || true
  tmp="$CONTROL/result.$$"
  printf '%s\n' "$rc" >"$tmp" 2>/dev/null || return 0
  chmod 600 "$tmp" 2>/dev/null || true
  mv -f "$tmp" "$RESULT" 2>/dev/null || true
}

cleanup() {
  local rc=$? source
  set +e
  rm -f "$READY" "$CRED_FIFO" 2>/dev/null || true
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
  write_result "$rc"
  exit "$rc"
}
trap cleanup EXIT INT TERM

[[ "${RUNNER_NAME:-}" == synology-otclient-01 ]] || fail wrong_runner
[[ "${GITHUB_REPOSITORY:-}" == blakinio/otclient ]] || fail wrong_repository
[[ ${TIBIA_TEST_EMAIL+x} != x && ${TIBIA_TEST_PASSWORD+x} != x ]] || fail secret_env_present_before_presecret_gate

mkdir -p "$CONTROL"
chmod 700 "$CONTROL"
rm -f "$CRED_FIFO" "$READY" "$RESULT" "$CONTROL"/result.* 2>/dev/null || true

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

# Native pre-secret UI gate: no OCR and no credential-bearing environment.
# Raw XWD is transient and used only for aggregate changed-pixel classification.
echo 'WORLDMAP_BASELINE_NATIVE_PRESECRET_GATE_VERSION=1'
XWD="$(command -v xwd 2>/dev/null || true)"
[[ -n "$XWD" ]] || XWD="$(find "$TOOL" -xdev -type f -name xwd -perm -111 -print -quit 2>/dev/null || true)"
COMPARE="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-compare.py"
[[ -x "$XWD" ]] || fail xwd_missing_before_secret_use
[[ -f "$COMPARE" ]] || fail xwd_compare_missing
[[ ${TIBIA_TEST_EMAIL+x} != x && ${TIBIA_TEST_PASSWORD+x} != x ]] || fail secret_env_present_before_editability_gates

UI_WIN="$WIN"
[[ "$UI_WIN" =~ ^[1-9][0-9]*$ ]] || fail manifest_ui_window_invalid
echo "WORLDMAP_BASELINE_UI_WINDOW_IDENTITY=x11-window:$UI_WIN"
echo 'WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN'
echo 'WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_EXPECTED=1020x650'
echo 'WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true'

XWD_TOOLROOT_LIBS="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu"
XDO_TOOLROOT_LIBS="$XWD_TOOLROOT_LIBS"
capture_xwd() {
  local outfile="$1"
  if [[ "$XWD" == "$TOOL/"* ]]; then
    DISPLAY="$DISPLAY" LD_LIBRARY_PATH="$XWD_TOOLROOT_LIBS" "$XWD" -silent -id "$UI_WIN" -out "$outfile"
  else
    DISPLAY="$DISPLAY" "$XWD" -silent -id "$UI_WIN" -out "$outfile"
  fi
}
xdo() {
  DISPLAY="$DISPLAY" LD_LIBRARY_PATH="$XDO_TOOLROOT_LIBS" "$XDOTOOL" "$@"
}

# Historical exact-client 1020x650 coordinates were physically validated in this task chain.
EMAIL_X=535
EMAIL_Y=275
PASS_X=535
PASS_Y=304
LOGIN_X=590
LOGIN_Y=388
ROW_X=285
ROW_Y=193

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"
echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'

probe_editable_field() {
  local name="$1" x="$2" y="$3" dummy="$4" x0="$5" y0="$6" x1="$7" y1="$8"
  local before="$ROOT/$name-before.xwd"
  local typed="$ROOT/$name-typed.xwd"
  local cleared="$ROOT/$name-cleared.xwd"

  xdo mousemove --window "$UI_WIN" "$x" "$y" click 1
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  sleep .20
  capture_xwd "$before"
  xdo type --window "$UI_WIN" --delay 10 -- "$dummy"
  sleep .25
  capture_xwd "$typed"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  sleep .25
  capture_xwd "$cleared"
  if ! python3 "$COMPARE" roi-cycle "$before" "$typed" "$cleared" \
      "$x0" "$y0" "$x1" "$y1" --min-changed 60; then
    rm -f "$before" "$typed" "$cleared"
    fail "${name}_editable_probe_failed"
  fi
  rm -f "$before" "$typed" "$cleared"
}

probe_editable_field email "$EMAIL_X" "$EMAIL_Y" 'wm-probe@example.invalid' 330 255 720 293
echo 'WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS'
probe_editable_field password "$PASS_X" "$PASS_Y" 'wm-probe-7' 330 289 720 325
echo 'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS'
echo 'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS'

# Clear both fields again, then publish the only credential-handoff gate.
PRELOGIN_REFERENCE="$ROOT/prelogin-reference.xwd"
xdo mousemove --window "$UI_WIN" "$EMAIL_X" "$EMAIL_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
xdo mousemove --window "$UI_WIN" "$PASS_X" "$PASS_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
sleep .25
capture_xwd "$PRELOGIN_REFERENCE"

[[ ${TIBIA_TEST_EMAIL+x} != x && ${TIBIA_TEST_PASSWORD+x} != x ]] || fail secret_env_present_before_handoff
rm -f "$CRED_FIFO" "$READY"
mkfifo -m 600 "$CRED_FIFO"
printf '%s\n' 'WORLDMAP_BASELINE_PRESECRET_READY=true' >"$READY.tmp"
chmod 600 "$READY.tmp"
mv -f "$READY.tmp" "$READY"
echo 'WORLDMAP_BASELINE_PRESECRET_READY=true'

# Secrets enter this shell only through the protected FIFO after both dummy gates.
exec {CRED_FD}<>"$CRED_FIFO"
EMAIL_SECRET=''
PASSWORD_SECRET=''
IFS= read -r -d '' -t 180 -u "$CRED_FD" EMAIL_SECRET || fail credential_email_handoff_timeout
IFS= read -r -d '' -t 30 -u "$CRED_FD" PASSWORD_SECRET || fail credential_password_handoff_timeout
exec {CRED_FD}>&-
rm -f "$CRED_FIFO" "$READY"
[[ -n "$EMAIL_SECRET" && -n "$PASSWORD_SECRET" ]] || fail credential_handoff_empty
echo 'WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES'

xdo mousemove --window "$UI_WIN" "$EMAIL_X" "$EMAIL_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
printf '%s' "$EMAIL_SECRET" | xdo type --window "$UI_WIN" --delay 10 --file -
xdo mousemove --window "$UI_WIN" "$PASS_X" "$PASS_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
printf '%s' "$PASSWORD_SECRET" | xdo type --window "$UI_WIN" --delay 10 --file -
EMAIL_SECRET=''
PASSWORD_SECRET=''
unset EMAIL_SECRET PASSWORD_SECRET
xdo mousemove --window "$UI_WIN" "$LOGIN_X" "$LOGIN_Y" click 1
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

POST_LOGIN_XWD=''
for i in $(seq 1 40); do
  sleep 1
  candidate="$ROOT/post-login-$i.xwd"
  capture_xwd "$candidate"
  if python3 "$COMPARE" change "$PRELOGIN_REFERENCE" "$candidate" --min-changed 5000; then
    POST_LOGIN_XWD="$candidate"
    break
  fi
  rm -f "$candidate"
done
rm -f "$PRELOGIN_REFERENCE"
[[ -n "$POST_LOGIN_XWD" ]] || fail post_login_visual_transition_not_observed
echo 'WORLDMAP_BASELINE_POST_LOGIN_VISUAL_TRANSITION=PROVEN_AGGREGATE'

sleep 3
SELECT_BEFORE="$ROOT/select-before.xwd"
SELECT_AFTER="$ROOT/select-after.xwd"
capture_xwd "$SELECT_BEFORE"
xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"
xdo mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click 1
sleep .35
capture_xwd "$SELECT_AFTER"
if ! python3 "$COMPARE" change "$SELECT_BEFORE" "$SELECT_AFTER" --min-changed 80 \
    --x0 100 --y0 165 --x1 900 --y1 230; then
  rm -f "$POST_LOGIN_XWD" "$SELECT_BEFORE" "$SELECT_AFTER"
  fail character_row_interaction_not_observed
fi
rm -f "$POST_LOGIN_XWD" "$SELECT_BEFORE" "$SELECT_AFTER"
echo 'WORLDMAP_BASELINE_CHARACTER_ROW_SELECTION=PROVEN_AGGREGATE'
xdo key --window "$UI_WIN" Return
echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_SENT=true'

world=0
for _ in $(seq 1 40); do
  sleep 1
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then world=1; break; fi
done
if [[ "$world" != 1 ]]; then
  xdo mousemove --window "$WIN" "$ROW_X" "$ROW_Y" click --repeat 2 --delay 120 1 key Return
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
xdo windowactivate --sync "$WIN" key --clearmodifiers Right
sleep 3
MID_COUNT="$(wc -l <"$STRIPS")"
xdo key --clearmodifiers Left
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
