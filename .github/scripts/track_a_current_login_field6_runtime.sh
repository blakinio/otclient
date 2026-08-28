#!/usr/bin/env bash
set +x
set -Eeuo pipefail
umask 077

TASK_ID='OTC-20260828-current-login-field6-runtime'
TRACK_ID='official-client-re'
EXPECTED_CLIENT_VERSION='15.32.75d4a0'
EXPECTED_CLIENT_SIZE='52105824'
EXPECTED_CLIENT_SHA256='d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
PRODUCER_OFFSET='0xe25620'
WGCF_VER='2.2.32'
WGCF_SHA='2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c'
WIREPROXY_VER='1.1.3'
WIREPROXY_TAR_SHA='e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c'
DISPLAY_NUMBER='131'
DISPLAY_VALUE=":$DISPLAY_NUMBER"
WARP_PORT='25441'
BASE='/home/runner/_work/_otclient_tibia_re_state'
TASK_BASE="$BASE/tasks/$TASK_ID"
RUN_ID="${GITHUB_RUN_ID:-manual-unknown}"
ROOT="$TASK_BASE/runs/$RUN_ID"
RUNTIME="$ROOT/runtime"
HOME_DIR="$ROOT/home"
WARP="$ROOT/warp"
RECORD="$ROOT/field6-value.txt"
PID_OUT="$ROOT/client.pid"
PIE_OUT="$ROOT/pie-base.txt"
START_OUT="$ROOT/process-start-ticks.txt"
GDB_SCRIPT="$ROOT/field6.gdb"
LAUNCHER="$ROOT/client-launcher.sh"
OUTPUT=''
TOOL=''
SOURCE=''
PACKAGE=''
CLIENT=''
GDB=''
XDO=''
XDO_LD=''
DID_LOGIN_SUBMIT=0

fail() { printf 'TRACK_A_FIELD6_RUNTIME_ERROR=%s\n' "$1" >&2; exit 1; }

listen() {
  python3 - "$1" <<'PY'
import pathlib,sys
needle=f'{int(sys.argv[1]):04X}'
for name in ('tcp','tcp6'):
    path=pathlib.Path('/proc/net')/name
    if not path.exists():
        continue
    for row in path.read_text(encoding='ascii',errors='replace').splitlines()[1:]:
        fields=row.split()
        if len(fields)>3 and fields[1].rsplit(':',1)[-1].upper()==needle and fields[3]=='0A':
            raise SystemExit(0)
raise SystemExit(1)
PY
}

read_pid() {
  local role="$1" path="$RUNTIME/$role.pid"
  [[ -r "$path" ]] || return 1
  tr -cd '0-9' <"$path"
}

owned() {
  local pid="$1" role="$2" executable="${3:-}"
  [[ "$pid" =~ ^[1-9][0-9]*$ && -r "/proc/$pid/environ" ]] || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_TRACK=$TRACK_ID" "/proc/$pid/environ" || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_TASK=$TASK_ID" "/proc/$pid/environ" || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_RUN_ID=$RUN_ID" "/proc/$pid/environ" || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_ROLE=$role" "/proc/$pid/environ" || return 1
  [[ -z "$executable" || "$(readlink -f "/proc/$pid/exe")" == "$(readlink -f "$executable")" ]]
}

nosecret() {
  local pid="$1" role="$2"
  [[ -r "/proc/$pid/environ" ]] || fail "${role}_environ_missing"
  ! grep -azEq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD)=' "/proc/$pid/environ" \
    || fail "${role}_secret_env_leak"
}

verify_client() {
  local client="$1"
  [[ -x "$client" && ! -L "$client" ]] || fail client_not_exact_regular_executable
  [[ "$(stat -Lc %s "$client")" == "$EXPECTED_CLIENT_SIZE" ]] || fail client_size_mismatch
  [[ "$(sha256sum "$client" | awk '{print $1}')" == "$EXPECTED_CLIENT_SHA256" ]] || fail client_sha256_mismatch
}

resolve_source() {
  local package
  for package in \
    "$BASE/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia" \
    "/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"; do
    if [[ -x "$package/bin/client" && ! -L "$package/bin/client" \
      && "$(stat -Lc %s "$package/bin/client" 2>/dev/null || true)" == "$EXPECTED_CLIENT_SIZE" \
      && "$(sha256sum "$package/bin/client" 2>/dev/null | awk '{print $1}')" == "$EXPECTED_CLIENT_SHA256" ]]; then
      printf '%s\n' "$package"
      return 0
    fi
  done
  return 1
}

toolroot_ok() {
  local root="$1" name
  [[ -d "$root" && ! -L "$root" ]] || return 1
  for name in Xvfb xdotool gdb; do
    [[ -x "$root/usr/bin/$name" && ! -L "$root/usr/bin/$name" ]] || return 1
  done
  [[ -d "$root/usr/share/X11/xkb" ]] || return 1
  [[ -f "$root/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so" ]] || return 1
  find "$root" -xdev -type f -name libproxychains.so.4 -print -quit 2>/dev/null | grep -q .
}

resolve_toolroot() {
  local root
  for root in "$BASE/toolroot" /work/_otclient_tibia_re_state/toolroot; do
    toolroot_ok "$root" && { printf '%s\n' "$root"; return 0; }
  done
  return 1
}

prepare_home() {
  local tibia_root metadata
  tibia_root="$HOME_DIR/.local/share/CipSoft GmbH/Tibia"
  PACKAGE="$tibia_root/packages/Tibia"
  mkdir -p "$tibia_root/packages"
  cp -a --reflink=auto "$SOURCE" "$PACKAGE"
  CLIENT="$PACKAGE/bin/client"
  verify_client "$CLIENT"
  metadata="$(dirname "$(dirname "$SOURCE")")/launchermetadata.json"
  if [[ -f "$metadata" && ! -L "$metadata" ]]; then
    python3 - "$metadata" <<'PY'
import json,re,sys
value=json.load(open(sys.argv[1],encoding='utf-8'))
bad=re.compile(r'(?i)(password|credential|access[_-]?token|refresh[_-]?token|email|cookie|session)')
def walk(x):
    if isinstance(x,dict):
        for k,v in x.items():
            if bad.search(str(k)): raise SystemExit('metadata_sensitive_key')
            walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
walk(value)
PY
    install -m600 "$metadata" "$tibia_root/launchermetadata.json"
  fi
  : >"$tibia_root/.running"
  chmod 600 "$tibia_root/.running"
}

start_warp() {
  local bin="$WARP/bin" state="$WARP/state" archive extracted pid
  listen "$WARP_PORT" && fail warp_port_collision || true
  mkdir -p "$bin" "$state"
  chmod 700 "$WARP" "$bin" "$state"

  curl -fL --retry 3 --connect-timeout 10 -o "$bin/wgcf.tmp" \
    "https://github.com/ViRb3/wgcf/releases/download/v$WGCF_VER/wgcf_${WGCF_VER}_linux_amd64"
  [[ "$(sha256sum "$bin/wgcf.tmp" | awk '{print $1}')" == "$WGCF_SHA" ]] || fail wgcf_hash_mismatch
  chmod 755 "$bin/wgcf.tmp"
  mv "$bin/wgcf.tmp" "$bin/wgcf"

  archive="$bin/wireproxy.tar.gz"
  curl -fL --retry 3 --connect-timeout 10 -o "$archive.tmp" \
    "https://github.com/windtf/wireproxy/releases/download/v$WIREPROXY_VER/wireproxy_linux_amd64.tar.gz"
  [[ "$(sha256sum "$archive.tmp" | awk '{print $1}')" == "$WIREPROXY_TAR_SHA" ]] || fail wireproxy_archive_hash_mismatch
  mv "$archive.tmp" "$archive"
  mkdir "$bin/unpack"
  tar -xzf "$archive" -C "$bin/unpack"
  extracted="$(find "$bin/unpack" -type f -name wireproxy -print -quit)"
  [[ -n "$extracted" ]] || fail wireproxy_binary_missing
  install -m755 "$extracted" "$bin/wireproxy"
  rm -rf --one-file-system "$bin/unpack"

  (
    cd "$state"
    "$bin/wgcf" register --accept-tos >/dev/null
    chmod 600 wgcf-account.toml
    "$bin/wgcf" generate >/dev/null
    chmod 600 wgcf-profile.conf
  )
  cat >"$RUNTIME/wireproxy.conf" <<EOF
WGConfig = $state/wgcf-profile.conf
[Socks5]
BindAddress = 127.0.0.1:$WARP_PORT
EOF
  chmod 600 "$RUNTIME/wireproxy.conf"
  "$bin/wireproxy" -n -c "$RUNTIME/wireproxy.conf" >/dev/null
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK="$TRACK_ID" OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_RUN_ID="$RUN_ID" OTCLIENT_TIBIA_RE_ROLE=wireproxy \
    nohup "$bin/wireproxy" -c "$RUNTIME/wireproxy.conf" \
    >"$RUNTIME/wireproxy.log" 2>&1 </dev/null &
  pid=$!
  printf '%s\n' "$pid" >"$RUNTIME/wireproxy.pid"
  for _ in $(seq 1 60); do
    kill -0 "$pid" 2>/dev/null || fail wireproxy_exited
    listen "$WARP_PORT" && break
    sleep .25
  done
  owned "$pid" wireproxy "$bin/wireproxy" || fail wireproxy_ownership_failed
  nosecret "$pid" wireproxy
  listen "$WARP_PORT" || fail wireproxy_not_listening
  curl --socks5-hostname "127.0.0.1:$WARP_PORT" -fsS --max-time 15 \
    https://www.cloudflare.com/cdn-cgi/trace | grep -Eq '^warp=(on|plus)$' || fail warp_egress_not_verified
  printf 'TRACK_A_FIELD6_WARP=PASS\n'
}

start_xvfb() {
  local xvfb="$TOOL/usr/bin/Xvfb" pid
  [[ ! -e "/tmp/.X${DISPLAY_NUMBER}-lock" && ! -e "/tmp/.X11-unix/X${DISPLAY_NUMBER}" ]] || fail display_collision
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK="$TRACK_ID" OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_RUN_ID="$RUN_ID" OTCLIENT_TIBIA_RE_ROLE=xvfb \
    HOME="$HOME_DIR" PATH="$TOOL/usr/bin:$TOOL/usr/sbin:/usr/bin:/bin" \
    LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu" \
    LIBGL_DRIVERS_PATH="$TOOL/usr/lib/x86_64-linux-gnu/dri" XKB_CONFIG_ROOT="$TOOL/usr/share/X11/xkb" \
    nohup "$xvfb" "$DISPLAY_VALUE" -screen 0 1920x1080x24 -xkbdir "$TOOL/usr/share/X11/xkb" \
    -nolisten tcp -noreset >"$RUNTIME/xvfb.log" 2>&1 </dev/null &
  pid=$!
  printf '%s\n' "$pid" >"$RUNTIME/xvfb.pid"
  for _ in $(seq 1 80); do
    kill -0 "$pid" 2>/dev/null || fail xvfb_exited
    [[ -e "/tmp/.X11-unix/X${DISPLAY_NUMBER}" ]] && break
    sleep .2
  done
  [[ -e "/tmp/.X11-unix/X${DISPLAY_NUMBER}" ]] || fail xvfb_socket_missing
  owned "$pid" xvfb "$xvfb" || fail xvfb_ownership_failed
  nosecret "$pid" xvfb
  printf 'TRACK_A_FIELD6_XVFB=PASS display=%s\n' "$DISPLAY_VALUE"
}

write_launcher() {
  local preload
  preload="$(find "$TOOL" -xdev -type f -name libproxychains.so.4 -print -quit 2>/dev/null || true)"
  [[ -n "$preload" ]] || fail proxychains_unavailable
  python3 - "$LAUNCHER" "$CLIENT" "$PACKAGE" "$HOME_DIR" "$DISPLAY_VALUE" "$TOOL" "$ROOT" "$preload" "$TRACK_ID" "$TASK_ID" "$RUN_ID" <<'PY'
import shlex,sys
out,client,package,home,display,tool,root,preload,track,task,run=sys.argv[1:]
q=shlex.quote
text=f'''#!/usr/bin/env bash
set -Eeuo pipefail
unset RUNNER_TRACKING_ID TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
export OTCLIENT_TIBIA_RE_TRACK={q(track)}
export OTCLIENT_TIBIA_RE_TASK={q(task)}
export OTCLIENT_TIBIA_RE_RUN_ID={q(run)}
export OTCLIENT_TIBIA_RE_ROLE=client
export HOME={q(home)}
export DISPLAY={q(display)}
export PATH={q(tool+'/usr/bin')}:{q(tool+'/usr/sbin')}:/usr/bin:/bin
export LD_LIBRARY_PATH={q(package+'/bin/lib')}:{q(tool+'/usr/lib/x86_64-linux-gnu')}:{q(tool+'/usr/lib/x86_64-linux-gnu/libproxy')}:{q(tool+'/lib/x86_64-linux-gnu')}
export LIBGL_ALWAYS_SOFTWARE=1
export LIBGL_DRIVERS_PATH={q(tool+'/usr/lib/x86_64-linux-gnu/dri')}
export QT_QUICK_BACKEND=software
export QSG_INFO=1
export XDG_DATA_DIRS={q(tool+'/usr/share')}:/usr/share
export FONTCONFIG_PATH={q(tool+'/etc/fonts')}
export FONTCONFIG_FILE={q(tool+'/etc/fonts/fonts.conf')}
export LD_PRELOAD={q(preload)}
export PROXYCHAINS_CONF_FILE={q(root+'/runtime/proxychains.conf')}
cd {q(package)}
exec {q(client)} >{q(root+'/runtime/client.log')} 2>&1 </dev/null
'''
open(out,'w',encoding='utf-8').write(text)
PY
  chmod 700 "$LAUNCHER"
}

write_gdb_script() {
  python3 - "$GDB_SCRIPT" "$LAUNCHER" "$CLIENT" "$PID_OUT" "$PIE_OUT" "$RECORD" "$PRODUCER_OFFSET" <<'PY'
import shlex,sys
out,launcher,client,pid_out,pie_out,record,offset=sys.argv[1:]
text=f'''set pagination off
set confirm off
set startup-with-shell off
set disable-randomization off
set follow-exec-mode same
handle SIGTERM pass nostop noprint
file /bin/bash
unset environment RUNNER_TRACKING_ID
unset environment TIBIA_TEST_EMAIL
unset environment TIBIA_TEST_PASSWORD
set args {shlex.quote(launcher)}
catch exec
run
delete
python
import gdb,os,time
pid=int(gdb.selected_inferior().pid)
expected=os.path.realpath({client!r})
actual=os.path.realpath(f'/proc/{{pid}}/exe')
if actual != expected: raise gdb.GdbError('exact client exec mismatch')
line=None
for _ in range(80):
    for row in open(f'/proc/{{pid}}/maps',encoding='utf-8',errors='replace'):
        fields=row.rstrip('\\n').split(maxsplit=5)
        if len(fields)>=6 and 'r-xp' in fields[1] and os.path.realpath(fields[5])==expected:
            line=fields; break
    if line: break
    time.sleep(0.05)
if not line: raise gdb.GdbError('exact client executable mapping missing')
bias=int(line[0].split('-',1)[0],16)-int(line[2],16)
open({pid_out!r},'w',encoding='ascii').write(str(pid)+'\\n')
open({pie_out!r},'w',encoding='ascii').write(f'0x{{bias:x}}\\n')
record_path={record!r}
class Field6BP(gdb.Breakpoint):
    def __init__(self): super().__init__('*0x%x' % (bias+int({offset!r},0)))
    def stop(self):
        if os.path.exists(record_path): self.enabled=False; return False
        value=int(gdb.parse_and_eval('$edx')) & 0xffffffff
        fd=os.open(record_path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        try:
            os.write(fd,(str(value)+'\\n').encode('ascii')); os.fsync(fd)
        finally: os.close(fd)
        self.enabled=False
        gdb.write(f'TRACK_A_FIELD6_BREAKPOINT_HIT=true FIELD6_VALUE={{value}}\\n')
        return False
Field6BP()
gdb.write(f'TRACK_A_FIELD6_GDB_READY=true pid={{pid}} pie=0x{{bias:x}} offset={offset}\\n')
end
continue
'''
open(out,'w',encoding='utf-8').write(text)
PY
  chmod 600 "$GDB_SCRIPT"
}

start_client() {
  local observer client_pid
  write_launcher
  write_gdb_script
  GDB="$TOOL/usr/bin/gdb"
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK="$TRACK_ID" OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_RUN_ID="$RUN_ID" OTCLIENT_TIBIA_RE_ROLE=observer \
    HOME="$HOME_DIR" PATH="$TOOL/usr/bin:$TOOL/usr/sbin:/usr/bin:/bin" \
    LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/usr/lib/x86_64-linux-gnu/libproxy:$TOOL/lib/x86_64-linux-gnu" \
    nohup "$GDB" -q -nx -batch -x "$GDB_SCRIPT" >"$RUNTIME/gdb.log" 2>&1 </dev/null &
  observer=$!
  printf '%s\n' "$observer" >"$RUNTIME/observer.pid"
  for _ in $(seq 1 160); do
    [[ -s "$PID_OUT" && -s "$PIE_OUT" ]] && break
    kill -0 "$observer" 2>/dev/null || { tail -n 60 "$RUNTIME/gdb.log" >&2 || true; fail gdb_exited_before_client_ready; }
    sleep .1
  done
  [[ -s "$PID_OUT" && -s "$PIE_OUT" ]] || fail gdb_child_metadata_timeout
  client_pid="$(tr -cd '0-9' <"$PID_OUT")"
  printf '%s\n' "$client_pid" >"$RUNTIME/client.pid"
  owned "$observer" observer "$GDB" || fail observer_ownership_failed
  owned "$client_pid" client "$CLIENT" || fail client_ownership_failed
  nosecret "$observer" observer
  nosecret "$client_pid" client
  [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$client_pid/status")" == "$observer" ]] || fail parent_tracer_not_active
  verify_client "$CLIENT"
  python3 - "$client_pid" "$START_OUT" <<'PY'
import os,pathlib,sys
pid,out=sys.argv[1:]
raw=pathlib.Path('/proc/'+pid+'/stat').read_text(encoding='ascii')
rparen=raw.rfind(')')
if rparen<0: raise SystemExit('process_stat_comm_invalid')
fields=raw[rparen+2:].split()
if len(fields)<20: raise SystemExit('process_stat_too_short')
start=int(fields[19])
if start<1: raise SystemExit('process_start_ticks_invalid')
fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w',encoding='ascii') as f:
    f.write(str(start)+'\n'); f.flush(); os.fsync(f.fileno())
PY
  [[ -s "$START_OUT" ]] || fail process_start_ticks_snapshot_missing
  printf 'TRACK_A_FIELD6_PROCESS_IDENTITY_SNAPSHOTTED=true\n'
  printf 'TRACK_A_FIELD6_INSTRUMENTED_CLIENT=PASS pid=%s pie=%s\n' "$client_pid" "$(cat "$PIE_OUT")"
}

xd() {
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    DISPLAY="$DISPLAY_VALUE" LD_LIBRARY_PATH="$XDO_LD" "$XDO" "$@"
}

wait_window() {
  local pid="$1" win geometry width height area best best_area
  for _ in $(seq 1 120); do
    kill -0 "$pid" 2>/dev/null || return 2
    best=''; best_area=0
    for win in $(xd search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null || true); do
      geometry="$(xd getwindowgeometry --shell "$win" 2>/dev/null || true)"
      width="$(sed -n 's/^WIDTH=//p' <<<"$geometry")"
      height="$(sed -n 's/^HEIGHT=//p' <<<"$geometry")"
      [[ "$width" =~ ^[0-9]+$ && "$height" =~ ^[0-9]+$ ]] || continue
      area=$((width*height))
      if (( area>best_area )); then best="$win"; best_area=$area; fi
    done
    [[ -n "$best" ]] && { printf '%s\n' "$best"; return 0; }
    sleep .25
  done
  return 1
}

prepare() {
  local win pid rc=0
  [[ "${GITHUB_REPOSITORY:-}" == 'blakinio/otclient' ]] || fail wrong_repository
  [[ "${RUNNER_NAME:-}" == 'synology-otclient-01' ]] || fail wrong_runner
  [[ "$RUN_ID" =~ ^[1-9][0-9]*$ ]] || fail invalid_run_id
  [[ ! -e "$ROOT" ]] || fail run_root_collision
  mkdir -p "$RUNTIME" "$HOME_DIR"
  chmod 700 "$TASK_BASE" "$TASK_BASE/runs" "$ROOT" "$RUNTIME" "$HOME_DIR" 2>/dev/null || true
  SOURCE="$(resolve_source)" || fail exact_current_source_package_missing
  TOOL="$(resolve_toolroot)" || fail exact_toolroot_missing
  XDO="$TOOL/usr/bin/xdotool"
  XDO_LD="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/usr/lib/x86_64-linux-gnu/libproxy:$TOOL/lib/x86_64-linux-gnu"
  prepare_home
  start_warp
  cat >"$RUNTIME/proxychains.conf" <<EOF
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 $WARP_PORT
EOF
  chmod 600 "$RUNTIME/proxychains.conf"
  start_xvfb
  start_client
  pid="$(read_pid client)"
  win="$(wait_window "$pid")" || rc=$?
  [[ "$rc" == 0 ]] || { [[ "$rc" == 2 ]] && fail client_exited_before_window; fail client_window_missing; }
  printf '%s\n' "$win" >"$RUNTIME/window.id"
  xd windowsize "$win" 1020 650 >/dev/null 2>&1 || fail client_window_resize_failed
  xd windowmove "$win" 0 0 >/dev/null 2>&1 || fail client_window_move_failed
  sleep 2
  [[ ! -e "$RECORD" ]] || fail producer_hit_before_login_submission
  printf 'TRACK_A_FIELD6_PRELOGIN_READY=true window=%s\n' "$win"
}

submit_login_once() {
  local pid win email password
  : "${TIBIA_TEST_EMAIL:?missing_TIBIA_TEST_EMAIL}"
  : "${TIBIA_TEST_PASSWORD:?missing_TIBIA_TEST_PASSWORD}"
  [[ "$DID_LOGIN_SUBMIT" == 0 ]] || fail duplicate_login_submit_refused
  pid="$(read_pid client)"
  win="$(cat "$RUNTIME/window.id")"
  owned "$pid" client "$CLIENT" || fail client_not_owned_before_login
  nosecret "$pid" client
  nosecret "$(read_pid observer)" observer
  [[ ! -e "$RECORD" ]] || fail producer_hit_before_login_submission
  email="$TIBIA_TEST_EMAIL"; password="$TIBIA_TEST_PASSWORD"
  xd windowfocus --sync "$win"
  xd mousemove --window "$win" 535 275 click 1
  xd key --window "$win" ctrl+a
  xd type --window "$win" --delay 12 -- "$email"
  xd mousemove --window "$win" 535 304 click 1
  xd key --window "$win" ctrl+a
  xd type --window "$win" --delay 12 -- "$password"
  xd mousemove --window "$win" 590 388 click 1
  DID_LOGIN_SUBMIT=1
  unset email password TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
  printf 'TRACK_A_FIELD6_LOGIN_SUBMIT_COUNT=1\n'
  for _ in $(seq 1 200); do
    [[ -s "$RECORD" ]] && break
    kill -0 "$pid" 2>/dev/null || fail client_exited_before_field6_capture
    sleep .1
  done
  [[ -s "$RECORD" ]] || fail field6_capture_timeout
}

write_artifact() {
  local value pid start_ticks pie
  value="$(tr -cd '0-9' <"$RECORD")"
  [[ "$value" =~ ^[0-9]+$ ]] || fail field6_value_not_uint32
  (( value>=0 && value<=4294967295 )) || fail field6_value_out_of_range
  pid="$(read_pid client)"
  start_ticks="$(tr -cd '0-9' <"$START_OUT")"
  [[ "$start_ticks" =~ ^[1-9][0-9]*$ ]] || fail process_start_ticks_snapshot_invalid
  pie="$(tr -d '\r\n' <"$PIE_OUT")"
  mkdir -p "$(dirname "$OUTPUT")"
  python3 - "$OUTPUT" "$value" "$pid" "$start_ticks" "$pie" <<'PY'
import json,sys
out,value,pid,start,pie=sys.argv[1:]
d={
 'schema':'otclient.track-a.current-login-field6-runtime.v1','track_id':'official-client-re',
 'task_id':'OTC-20260828-current-login-field6-runtime','client_version':'15.32.75d4a0',
 'client_size':52105824,'client_sha256':'d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a',
 'producer_offset':'0xe25620','capture_source':'gdb_parent_breakpoint_edx','pid':int(pid),
 'process_start_ticks':int(start),'pie_base':pie,'field6_value':int(value),'field6_value_proven':True,
 'login_submit_count':1,'character_selection_performed':False,'world_entry_performed':False,
 'gameplay_performed':False,'network_payload_capture_performed':False,'credentials_retained':False,
 'packet_payloads_retained':False,'process_environment_retained':False,'raw_memory_retained':False,
}
with open(out,'w',encoding='utf-8') as f:
    json.dump(d,f,sort_keys=True,separators=(',',':')); f.write('\n')
PY
  chmod 600 "$OUTPUT"
  printf 'TRACK_A_FIELD6_RUNTIME_CAPTURED=true\n'
  printf 'FIELD6_VALUE_PROVEN=true\n'
  printf 'FIELD6_VALUE=%s\n' "$value"
  printf 'TRACK_A_FIELD6_CHARACTER_SELECTION=false\n'
  printf 'TRACK_A_FIELD6_WORLD_ENTRY=false\n'
}

stop_owned() {
  local role="$1" expected="${2:-}" pid
  pid="$(read_pid "$role" 2>/dev/null || true)"
  [[ -n "$pid" && -e "/proc/$pid" ]] || return 0
  owned "$pid" "$role" "$expected" || fail "cleanup_${role}_ownership_refused"
  kill -CONT "$pid" 2>/dev/null || true
  kill -TERM "$pid" 2>/dev/null || true
  for _ in $(seq 1 80); do [[ ! -e "/proc/$pid" ]] && return 0; sleep .1; done
  owned "$pid" "$role" "$expected" || fail "cleanup_${role}_identity_changed"
  kill -KILL "$pid" 2>/dev/null || true
  for _ in $(seq 1 30); do [[ ! -e "/proc/$pid" ]] && return 0; sleep .1; done
  fail "cleanup_${role}_timeout"
}

cleanup() {
  local wire=''
  [[ -d "$RUNTIME" ]] || return 0
  [[ -x "$WARP/bin/wireproxy" ]] && wire="$WARP/bin/wireproxy"
  stop_owned client "${CLIENT:-}"
  stop_owned observer "${GDB:-}"
  stop_owned xvfb "${TOOL:+$TOOL/usr/bin/Xvfb}"
  stop_owned wireproxy "$wire"
  [[ ! -e "/tmp/.X${DISPLAY_NUMBER}-lock" && ! -e "/tmp/.X11-unix/X${DISPLAY_NUMBER}" ]] || fail display_residue_after_owned_cleanup
  listen "$WARP_PORT" && fail warp_port_residue_after_owned_cleanup || true
  rm -rf --one-file-system "$ROOT"
}

run() {
  [[ $# == 1 ]] || fail usage
  OUTPUT="$1"
  [[ "$OUTPUT" == /* ]] || fail output_must_be_absolute
  case "$OUTPUT" in "$TASK_BASE"/*) fail output_must_be_outside_task_state ;; esac
  trap 'rc=$?; trap - EXIT; cleanup; exit "$rc"' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  prepare
  submit_login_once
  write_artifact
  cleanup
  trap - EXIT INT TERM
}

case "${1:-}" in
  run) shift; run "$@" ;;
  *) fail usage ;;
esac
