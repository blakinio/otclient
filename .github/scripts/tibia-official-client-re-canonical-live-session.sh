#!/usr/bin/env bash
set +x
set -Eeuo pipefail
umask 077

BASE_STATE=/home/runner/_work/_otclient_tibia_re_state
STATE_ROOT="$BASE_STATE/canonical-live-runtime"
SESSION_ROOT="$STATE_ROOT/session"
TOOLROOT="$BASE_STATE/toolroot"
EXPECTED_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
EXPECTED_SIZE=51965216
TRACK_MARKER='OTCLIENT_TIBIA_RE_TRACK=official-client-re'
RUNTIME_MARKER='OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1'
UPSTREAM_SOCKS_PORT=25354
MAP_CAPTURE_OFFSET=0x19a8ea3
REQUIRED_RECORDS=8

die() { printf 'TRACK_A_CANONICAL_SESSION_ERROR=%s\n' "$1" >&2; exit 1; }
role_pid() { tr -cd '0-9' <"$SESSION_ROOT/$1.pid" 2>/dev/null || true; }
port_listening() {
  python3 - "$1" <<'PY'
import pathlib,sys
needle=f"{int(sys.argv[1]):04X}"
for name in ("tcp","tcp6"):
 p=pathlib.Path('/proc/net')/name
 if not p.exists(): continue
 for row in p.read_text().splitlines()[1:]:
  f=row.split()
  if len(f)>3 and f[1].rsplit(':',1)[-1].upper()==needle and f[3]=='0A': raise SystemExit(0)
raise SystemExit(1)
PY
}
verify_client() {
  local client="$1"
  [[ -x "$client" && ! -L "$client" ]] || die client_not_executable
  [[ "$(stat -c '%s' "$client")" == "$EXPECTED_SIZE" ]] || die client_size_mismatch
  [[ "$(sha256sum "$client" | awk '{print $1}')" == "$EXPECTED_SHA256" ]] || die client_sha_mismatch
}
assert_no_secret_env() {
  local pid="$1" role="$2"
  [[ -r "/proc/$pid/environ" ]] || die "${role}_environ_missing"
  ! grep -azEq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD|TRACK_A_CANONICAL_LEASE_TOKEN|TRACK_A_CANONICAL_LEASE_TOKEN_FILE)=' "/proc/$pid/environ" \
    || die "${role}_secret_env_leak"
}
owned_role() {
  local pid="$1" role="$2"
  [[ "$pid" =~ ^[1-9][0-9]*$ && -r "/proc/$pid/environ" ]] || return 1
  grep -azFxq "$TRACK_MARKER" "/proc/$pid/environ" || return 1
  grep -azFxq "$RUNTIME_MARKER" "/proc/$pid/environ" || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_ROLE=$role" "/proc/$pid/environ"
}
find_exact_source_package() {
  local candidate client
  for candidate in \
    "$BASE_STATE/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia" \
    "/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"; do
    client="$candidate/bin/client"
    if [[ -x "$client" && ! -L "$client" ]] && \
       [[ "$(stat -c '%s' "$client" 2>/dev/null || true)" == "$EXPECTED_SIZE" ]] && \
       [[ "$(sha256sum "$client" 2>/dev/null | awk '{print $1}')" == "$EXPECTED_SHA256" ]]; then
      printf '%s\n' "$candidate"; return 0
    fi
  done
  return 1
}
find_tool() {
  local name="$1" p
  p="$(command -v "$name" 2>/dev/null || true)"
  [[ -n "$p" && -x "$p" ]] && { printf '%s\n' "$p"; return 0; }
  p="$(find "$TOOLROOT" -type f -name "$name" -perm -u+x -print -quit 2>/dev/null || true)"
  [[ -n "$p" ]] && { printf '%s\n' "$p"; return 0; }
  return 1
}
choose_display() {
  local n
  for n in $(seq 98 130); do
    [[ ! -e "/tmp/.X${n}-lock" && ! -e "/tmp/.X11-unix/X${n}" ]] && { printf '%s\n' "$n"; return 0; }
  done
  return 1
}
choose_port() {
  local p start="$1" end="$2"
  for p in $(seq "$start" "$end"); do
    port_listening "$p" || { printf '%s\n' "$p"; return 0; }
  done
  return 1
}
resolve_window() {
  local pid="$1" display="$2" xdotool="$3" w g width height area best='' best_area=0
  for _ in $(seq 1 120); do
    best=''; best_area=0
    for w in $(DISPLAY="$display" "$xdotool" search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null || true); do
      g="$(DISPLAY="$display" "$xdotool" getwindowgeometry --shell "$w" 2>/dev/null || true)"
      width="$(sed -n 's/^WIDTH=//p' <<<"$g")"; height="$(sed -n 's/^HEIGHT=//p' <<<"$g")"
      [[ "$width" =~ ^[0-9]+$ && "$height" =~ ^[0-9]+$ ]] || continue
      area=$((width*height)); (( area > best_area )) && { best="$w"; best_area=$area; }
    done
    [[ -n "$best" ]] && { printf '%s\n' "$best"; return 0; }
    sleep .25
  done
  return 1
}
verify_upstream_warp() {
  local pid
  pid="$(tr -cd '0-9' <"$BASE_STATE/runtime/wireproxy.pid" 2>/dev/null || true)"
  [[ "$pid" =~ ^[1-9][0-9]*$ && -r "/proc/$pid/environ" ]] || die upstream_wireproxy_unavailable
  grep -azFxq "$TRACK_MARKER" "/proc/$pid/environ" || die upstream_wireproxy_wrong_owner
  kill -0 "$pid" 2>/dev/null || die upstream_wireproxy_dead
  curl --socks5-hostname "127.0.0.1:$UPSTREAM_SOCKS_PORT" -fsS --max-time 15 https://www.cloudflare.com/cdn-cgi/trace \
    | grep -Eq '^warp=(on|plus)$' || die upstream_warp_not_verified
}
write_relay() {
  cat >"$SESSION_ROOT/relay.py" <<'PY'
import socket,sys,threading
listen_port,upstream_port=map(int,sys.argv[1:3])
def pump(a,b):
 try:
  while True:
   d=a.recv(65536)
   if not d: break
   b.sendall(d)
 except OSError: pass
 finally:
  try:b.shutdown(socket.SHUT_WR)
  except OSError:pass
def handle(c):
 u=socket.socket(); u.connect(('127.0.0.1',upstream_port))
 t1=threading.Thread(target=pump,args=(c,u)); t2=threading.Thread(target=pump,args=(u,c)); t1.start();t2.start();t1.join();t2.join();u.close();c.close()
s=socket.socket();s.bind(('127.0.0.1',listen_port));s.listen(32)
while True:
 c,_=s.accept();threading.Thread(target=handle,args=(c,),daemon=True).start()
PY
  chmod 600 "$SESSION_ROOT/relay.py"
}
bootstrap() {
  local manifest="$1" source package home metadata_source display_num display socks_port vnc_port
  local xvfb x11vnc xdotool proxy_lib client pid window pgid
  [[ "${RUNNER_NAME:-}" == synology-otclient-01 ]] || die wrong_runner
  [[ "${GITHUB_REPOSITORY:-}" == blakinio/otclient ]] || die wrong_repository
  [[ ! -e "$SESSION_ROOT" ]] || die session_root_already_exists
  source="$(find_exact_source_package)" || die exact_source_package_missing
  verify_upstream_warp
  xvfb="$(find_tool Xvfb)" || die xvfb_unavailable
  x11vnc="$(find_tool x11vnc)" || die x11vnc_unavailable
  xdotool="$(find_tool xdotool)" || die xdotool_unavailable
  proxy_lib="$(find "$TOOLROOT" -type f -name libproxychains.so.4 -print -quit 2>/dev/null || true)"
  [[ -n "$proxy_lib" ]] || die proxychains_library_unavailable
  display_num="$(choose_display)" || die no_free_display
  display=":$display_num"
  socks_port="$(choose_port 25430 25480)" || die no_free_socks_port
  vnc_port="$(choose_port 6082 6120)" || die no_free_vnc_port
  mkdir -p "$SESSION_ROOT"; chmod 700 "$SESSION_ROOT"
  home="$SESSION_ROOT/home"; package="$home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"
  mkdir -p "$(dirname "$package")"
  cp -a --reflink=auto "$source" "$package"
  client="$package/bin/client"; verify_client "$client"
  metadata_source="$(dirname "$source")/../../launchermetadata.json"
  if [[ -f "$metadata_source" && ! -L "$metadata_source" ]]; then
    install -m 600 "$metadata_source" "$(dirname "$(dirname "$package")")/launchermetadata.json"
  fi
  : >"$(dirname "$(dirname "$package")")/.running"; chmod 600 "$(dirname "$(dirname "$package")")/.running"
  write_relay
  cat >"$SESSION_ROOT/proxychains.conf" <<EOF
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 $socks_port
EOF
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=socks-relay \
    nohup python3 "$SESSION_ROOT/relay.py" "$socks_port" "$UPSTREAM_SOCKS_PORT" >"$SESSION_ROOT/relay.log" 2>&1 </dev/null &
  printf '%s\n' "$!" >"$SESSION_ROOT/socks-relay.pid"
  for _ in $(seq 1 50); do port_listening "$socks_port" && break; sleep .1; done
  port_listening "$socks_port" || die relay_not_listening
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=xvfb \
    HOME="$home" PATH="$TOOLROOT/usr/bin:$TOOLROOT/usr/sbin:/usr/bin:/bin" \
    LD_LIBRARY_PATH="$TOOLROOT/usr/lib/x86_64-linux-gnu:$TOOLROOT/lib/x86_64-linux-gnu" XKB_CONFIG_ROOT="$TOOLROOT/usr/share/X11/xkb" \
    nohup "$xvfb" "$display" -screen 0 1920x1080x24 -xkbdir "$TOOLROOT/usr/share/X11/xkb" -nolisten tcp -noreset \
    >"$SESSION_ROOT/xvfb.log" 2>&1 </dev/null &
  printf '%s\n' "$!" >"$SESSION_ROOT/xvfb.pid"
  for _ in $(seq 1 60); do [[ -e "/tmp/.X11-unix/X${display_num}" ]] && break; sleep .2; done
  [[ -e "/tmp/.X11-unix/X${display_num}" ]] || die xvfb_socket_missing
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=vnc \
    HOME="$home" DISPLAY="$display" nohup "$x11vnc" -display "$display" -rfbport "$vnc_port" -forever -shared -viewonly -localhost -nopw -noxdamage \
    >"$SESSION_ROOT/x11vnc.log" 2>&1 </dev/null &
  printf '%s\n' "$!" >"$SESSION_ROOT/vnc.pid"
  for _ in $(seq 1 60); do port_listening "$vnc_port" && break; sleep .2; done
  port_listening "$vnc_port" || die vnc_not_listening
  (
    cd "$package"
    env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
      OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=client \
      HOME="$home" DISPLAY="$display" PATH="$TOOLROOT/usr/bin:$TOOLROOT/usr/sbin:/usr/bin:/bin" \
      LD_LIBRARY_PATH="$package/bin/lib:$TOOLROOT/usr/lib/x86_64-linux-gnu:$TOOLROOT/usr/lib/x86_64-linux-gnu/libproxy:$TOOLROOT/lib/x86_64-linux-gnu" \
      QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none XDG_DATA_DIRS="$TOOLROOT/usr/share:/usr/share" \
      FONTCONFIG_PATH="$TOOLROOT/etc/fonts" FONTCONFIG_FILE="$TOOLROOT/etc/fonts/fonts.conf" \
      LD_PRELOAD="$proxy_lib" PROXYCHAINS_CONF_FILE="$SESSION_ROOT/proxychains.conf" \
      nohup "$client" >"$SESSION_ROOT/client.log" 2>&1 </dev/null &
    printf '%s\n' "$!" >"$SESSION_ROOT/client.pid"
  )
  pid="$(role_pid client)"; [[ -n "$pid" ]] || die client_pid_missing
  for _ in $(seq 1 100); do kill -0 "$pid" 2>/dev/null || die client_exited; window="$(resolve_window "$pid" "$display" "$xdotool" || true)"; [[ -n "$window" ]] && break; sleep .25; done
  [[ -n "${window:-}" ]] || die client_window_missing
  verify_client "$client"; owned_role "$pid" client || die client_ownership_failed; assert_no_secret_env "$pid" client
  printf '%s\n' "$display" >"$SESSION_ROOT/display"; printf '%s\n' "$window" >"$SESSION_ROOT/window"
  printf '%s\n' "$socks_port" >"$SESSION_ROOT/socks-port"; printf '%s\n' "$vnc_port" >"$SESSION_ROOT/vnc-port"
  pgid="$(ps -o pgid= -p $$ | tr -d ' ')"; [[ "$pgid" == "$$" ]] || die bootstrap_not_process_group_leader
  python3 - "$manifest" "$pid" "$pgid" "$display" "$window" "$vnc_port" <<'PY'
import json,sys
out,pid,pgid,display,window,vnc=sys.argv[1:]
json.dump({"pid":int(pid),"process_group_id":int(pgid),"display":display,"window_identity":"x11-window:"+window,"remote_view_endpoint":"127.0.0.1:"+vnc,"remote_view_mapping":"PROVEN","state":"UNKNOWN"},open(out,'w'))
PY
}
probe() {
  local manifest="$1" pid display window vnc client xdotool role rp
  [[ -d "$SESSION_ROOT" ]] || die session_root_missing
  pid="$(role_pid client)"; display="$(cat "$SESSION_ROOT/display")"; vnc="$(cat "$SESSION_ROOT/vnc-port")"
  client="$SESSION_ROOT/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"; verify_client "$client"
  owned_role "$pid" client || die client_ownership_failed; kill -0 "$pid" 2>/dev/null || die client_dead; assert_no_secret_env "$pid" client
  for role in xvfb vnc socks-relay; do rp="$(role_pid "$role")"; owned_role "$rp" "$role" || die "${role}_ownership_failed"; kill -0 "$rp" 2>/dev/null || die "${role}_dead"; assert_no_secret_env "$rp" "$role"; done
  port_listening "$vnc" || die vnc_not_listening
  xdotool="$(find_tool xdotool)" || die xdotool_unavailable
  window="$(resolve_window "$pid" "$display" "$xdotool")" || die client_window_missing
  [[ "$(cat "$SESSION_ROOT/window")" == "$window" ]] || printf '%s\n' "$window" >"$SESSION_ROOT/window"
  python3 - "$manifest" "$pid" "$display" "$window" "$vnc" <<'PY'
import json,sys
out,pid,display,window,vnc=sys.argv[1:]
json.dump({"pid":int(pid),"display":display,"window_identity":"x11-window:"+window,"remote_view_endpoint":"127.0.0.1:"+vnc,"remote_view_mapping":"PROVEN","state":"UNKNOWN"},open(out,'w'))
PY
}
start_world_observer() {
  local output="$1" pid="$2" client="$3" gdb script line start off bias
  gdb="$(find_tool gdb)" || die gdb_unavailable
  [[ "$(cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null || true)" == 0 ]] || die ptrace_scope_not_zero
  line="$(grep -F "$(readlink -f "$client")" "/proc/$pid/maps" | awk '$2~/r-xp/{print;exit}')"; [[ -n "$line" ]] || die client_text_mapping_missing
  start="$(awk '{split($1,a,"-");print a[1]}' <<<"$line")"; off="$(awk '{print $3}' <<<"$line")"; bias=$((16#$start-16#$off))
  script="$SESSION_ROOT/world-proof.gdb"
  python3 - "$script" "$pid" "$bias" "$output" "$MAP_CAPTURE_OFFSET" <<'PY'
import sys
out,pid,bias,records,offset=sys.argv[1:]
open(out,'w').write(f'''set pagination off\nset confirm off\nattach {pid}\npython\nimport gdb,struct,time\ninf=gdb.selected_inferior(); out=r"{records}"\nclass B(gdb.Breakpoint):\n def __init__(self): super().__init__('*0x%x' % (int("{bias}",0)+int("{offset}",0)))\n def stop(self):\n  try:\n   rsp=int(gdb.parse_and_eval('$rsp')); order=int(gdb.parse_and_eval('$rbp')) & 0xffffffff\n   x,y,z=struct.unpack('<III',bytes(inf.read_memory(rsp+0x88,12)))\n   if 0<x<100000 and 0<y<100000 and z<32 and order<128:\n    with open(out,'a') as f: f.write(f"{{time.monotonic_ns()}}\\t{{x}}\\t{{y}}\\t{{z}}\\t{{order}}\\n"); f.flush()\n  except Exception: pass\n  return False\nB()\nend\ncontinue\n''')
PY
  chmod 600 "$script"; : >"$output"
  env -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=world-proof \
    nohup "$gdb" -q -nx -batch -x "$script" >"$SESSION_ROOT/world-proof.log" 2>&1 </dev/null &
  printf '%s\n' "$!" >"$SESSION_ROOT/world-proof.pid"
  for _ in $(seq 1 50); do [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$pid/status")" == "$(role_pid world-proof)" ]] && return 0; sleep .1; done
  die world_observer_not_attached
}
stop_world_observer() {
  local gp
  gp="$(role_pid world-proof)"; [[ -n "$gp" ]] || return 0
  kill -INT "$gp" 2>/dev/null || true
  for _ in $(seq 1 30); do kill -0 "$gp" 2>/dev/null || break; sleep .1; done
  kill -0 "$gp" 2>/dev/null && kill -KILL "$gp" 2>/dev/null || true
}
wait_structural_in_game() {
  local records="$1" pid="$2" count=0
  for _ in $(seq 1 90); do kill -0 "$pid" 2>/dev/null || die client_died_waiting_world; count="$(wc -l <"$records")"; (( count >= REQUIRED_RECORDS )) && break; sleep 1; done
  (( count >= REQUIRED_RECORDS )) || die structural_in_game_not_proven
  awk -F '\t' 'NF==5 && $2>0 && $2<100000 && $3>0 && $3<100000 && $4>=0 && $4<32 && $5>=0 && $5<128 {ok++} END{exit !(ok==NR && NR>=8)}' "$records" || die structural_records_invalid
}
login_e2e() {
  local pid display window xdotool client records email password
  : "${TIBIA_TEST_EMAIL:?missing_TIBIA_TEST_EMAIL}"; : "${TIBIA_TEST_PASSWORD:?missing_TIBIA_TEST_PASSWORD}"
  pid="$(role_pid client)"; display="$(cat "$SESSION_ROOT/display")"; client="$SESSION_ROOT/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"
  owned_role "$pid" client || die client_not_owned; assert_no_secret_env "$pid" client
  xdotool="$(find_tool xdotool)" || die xdotool_unavailable; window="$(resolve_window "$pid" "$display" "$xdotool")" || die login_window_missing
  records="$SESSION_ROOT/login-world-records.tsv"; start_world_observer "$records" "$pid" "$client"; sleep 4
  [[ "$(wc -l <"$records")" == 0 ]] || { stop_world_observer; die login_negative_control_failed; }
  email="$TIBIA_TEST_EMAIL"; password="$TIBIA_TEST_PASSWORD"
  DISPLAY="$display" "$xdotool" windowfocus --sync "$window"
  DISPLAY="$display" "$xdotool" mousemove --window "$window" 535 275 click 1; DISPLAY="$display" "$xdotool" key --window "$window" ctrl+a
  env -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD DISPLAY="$display" "$xdotool" type --window "$window" --delay 12 -- "$email"
  DISPLAY="$display" "$xdotool" mousemove --window "$window" 535 304 click 1; DISPLAY="$display" "$xdotool" key --window "$window" ctrl+a
  env -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD DISPLAY="$display" "$xdotool" type --window "$window" --delay 12 -- "$password"
  DISPLAY="$display" "$xdotool" mousemove --window "$window" 590 388 click 1
  unset email password TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
  sleep 8; window="$(resolve_window "$pid" "$display" "$xdotool")" || { stop_world_observer; die character_select_window_missing; }
  DISPLAY="$display" "$xdotool" windowfocus --sync "$window"; DISPLAY="$display" "$xdotool" mousemove --window "$window" 285 193 click 1; sleep .4; DISPLAY="$display" "$xdotool" key --window "$window" Return
  wait_structural_in_game "$records" "$pid"; stop_world_observer
  printf 'TRACK_A_CANONICAL_LOGIN_E2E=PASS\n'
}
relogin_e2e() {
  local pid display window xdotool client records
  pid="$(role_pid client)"; display="$(cat "$SESSION_ROOT/display")"; client="$SESSION_ROOT/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"
  owned_role "$pid" client || die client_not_owned; xdotool="$(find_tool xdotool)" || die xdotool_unavailable
  window="$(resolve_window "$pid" "$display" "$xdotool")" || die relog_window_missing
  DISPLAY="$display" "$xdotool" windowfocus --sync "$window"; DISPLAY="$display" "$xdotool" key --window "$window" ctrl+l
  sleep 6; kill -0 "$pid" 2>/dev/null || die client_pid_changed_on_logout
  records="$SESSION_ROOT/relogin-world-records.tsv"; start_world_observer "$records" "$pid" "$client"; sleep 4
  [[ "$(wc -l <"$records")" == 0 ]] || { stop_world_observer; die relog_logout_negative_control_failed; }
  window="$(resolve_window "$pid" "$display" "$xdotool")" || { stop_world_observer; die relog_character_select_missing; }
  DISPLAY="$display" "$xdotool" windowfocus --sync "$window"; DISPLAY="$display" "$xdotool" mousemove --window "$window" 285 193 click 1; sleep .4; DISPLAY="$display" "$xdotool" key --window "$window" Return
  wait_structural_in_game "$records" "$pid"; stop_world_observer
  kill -0 "$pid" 2>/dev/null || die client_pid_changed_after_relogin
  printf 'TRACK_A_CANONICAL_RELOGIN_E2E=PASS\n'
}

case "${1:-}" in
  bootstrap) [[ $# == 3 ]] || die usage; bootstrap "$2" ;;
  probe) [[ $# == 3 ]] || die usage; probe "$2" ;;
  login-e2e) [[ $# == 2 ]] || die usage; login_e2e ;;
  relogin-e2e) [[ $# == 2 ]] || die usage; relogin_e2e ;;
  *) die usage ;;
esac
