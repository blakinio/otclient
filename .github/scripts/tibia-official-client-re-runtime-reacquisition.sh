#!/usr/bin/env bash
set +x
set -Eeuo pipefail
umask 077

TASK_ID='OTC-20260815-track-a-runtime-reacquisition'
TRACK_MARKER='OTCLIENT_TIBIA_RE_TRACK=official-client-re'
TASK_MARKER="OTCLIENT_TIBIA_RE_TASK=$TASK_ID"
ROLE_VAR='OTCLIENT_TIBIA_RE_ROLE'
BASE_STATE='/home/runner/_work/_otclient_tibia_re_state'
TASK_ROOT="$BASE_STATE/tasks/$TASK_ID"
DISPLAY_NUM='115'
TRACK_DISPLAY=":$DISPLAY_NUM"
TASK_SOCKS_PORT='25415'
UPSTREAM_SOCKS_PORT='25354'
EXPECTED_CLIENT_SHA256='e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe'
EXPECTED_CLIENT_SIZE='51965216'
MAP_CAPTURE_OFFSET='0x19a8ea3'
REQUIRED_RECORDS='8'

die() { printf 'TRACK_A_RUNTIME_ERROR=%s\n' "$1" >&2; exit "${2:-1}"; }
run_root() { printf '%s/runs/%s\n' "$TASK_ROOT" "$GITHUB_RUN_ID"; }
runtime_dir() { printf '%s/runtime\n' "$(run_root)"; }
evidence_dir() { printf '%s/artifacts/runtime-reacquisition\n' "$GITHUB_WORKSPACE"; }
package_dir() { printf '%s/package\n' "$(run_root)"; }
toolroot() { printf '%s/toolroot\n' "$BASE_STATE"; }
pidfile() { printf '%s/%s.pid\n' "$(runtime_dir)" "$1"; }
read_pid() { [[ -r "$(pidfile "$1")" ]] || return 1; tr -cd '0-9' <"$(pidfile "$1")"; }

require_context() {
  [[ "${GITHUB_REPOSITORY:-}" == 'blakinio/otclient' ]] || die wrong_repository
  [[ "${RUNNER_NAME:-}" == 'synology-otclient-01' ]] || die wrong_runner
  [[ "${GITHUB_REF_NAME:-}" == 'research/OTC-20260815-track-a-runtime-reacquisition' ]] || die wrong_branch
  [[ -n "${GITHUB_RUN_ID:-}" ]] || die missing_run_id
  [[ -d "$BASE_STATE" && -w "$BASE_STATE" ]] || die canonical_state_unavailable
}

role_owned() {
  local pid="$1" role="$2" expected="${3:-}"
  [[ -r "/proc/$pid/environ" ]] || return 1
  grep -azFxq "$TRACK_MARKER" "/proc/$pid/environ" || return 1
  grep -azFxq "$TASK_MARKER" "/proc/$pid/environ" || return 1
  grep -azFxq "$ROLE_VAR=$role" "/proc/$pid/environ" || return 1
  [[ -z "$expected" || "$(readlink -f "/proc/$pid/exe")" == "$(readlink -f "$expected")" ]]
}

assert_no_secret_env() {
  local pid="$1" role="$2"
  [[ -r "/proc/$pid/environ" ]] || die "missing_${role}_environ"
  ! grep -azEq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD)=' "/proc/$pid/environ" \
    || die "credential_env_leak_${role}"
  printf 'TRACK_A_CREDENTIAL_ENV_CLEAR role=%s pid=%s\n' "$role" "$pid"
}

verify_client() {
  local client="$1" size sha
  [[ -x "$client" ]] || die client_not_executable
  size="$(stat -c '%s' "$client")"
  sha="$(sha256sum "$client" | awk '{print $1}')"
  [[ "$size" == "$EXPECTED_CLIENT_SIZE" ]] || die "client_size_mismatch_$size"
  [[ "$sha" == "$EXPECTED_CLIENT_SHA256" ]] || die "client_sha_mismatch_$sha"
  printf 'TRACK_A_EXACT_CLIENT_VERIFIED size=%s sha256=%s\n' "$size" "$sha"
}

port_listening() {
  python3 - "$1" <<'PY'
import pathlib, sys
needle=f"{int(sys.argv[1]):04X}"
for name in ("tcp","tcp6"):
    p=pathlib.Path("/proc/net")/name
    if not p.exists(): continue
    for row in p.read_text().splitlines()[1:]:
        f=row.split()
        if len(f)>3 and f[1].rsplit(":",1)[-1].upper()==needle and f[3]=="0A":
            raise SystemExit(0)
raise SystemExit(1)
PY
}

verify_upstream_warp() {
  local pid
  pid="$(tr -cd '0-9' <"$BASE_STATE/runtime/wireproxy.pid" 2>/dev/null || true)"
  [[ -n "$pid" && -r "/proc/$pid/environ" ]] || die upstream_wireproxy_unavailable
  grep -azFxq "$TRACK_MARKER" "/proc/$pid/environ" || die upstream_wireproxy_wrong_owner
  kill -0 "$pid" || die upstream_wireproxy_dead
  curl --socks5-hostname "127.0.0.1:$UPSTREAM_SOCKS_PORT" -fsS --max-time 15 \
    https://www.cloudflare.com/cdn-cgi/trace | grep -Eq '^warp=(on|plus)$' \
    || die upstream_warp_not_verified
  printf 'TRACK_A_UPSTREAM_WARP_VERIFIED=true pid=%s\n' "$pid"
}

start_relay() {
  local relay="$(run_root)/tcp-relay.py" pid
  port_listening "$TASK_SOCKS_PORT" && die task_socks_port_collision || true
  cat >"$relay" <<'PY'
import socket, sys, threading
listen_port, upstream_port = map(int, sys.argv[1:3])
def pump(src,dst):
    try:
        while True:
            data=src.recv(65536)
            if not data: break
            dst.sendall(data)
    except OSError: pass
    finally:
        try: dst.shutdown(socket.SHUT_WR)
        except OSError: pass
def handle(client):
    upstream=socket.socket()
    try:
        upstream.connect(("127.0.0.1",upstream_port))
        a=threading.Thread(target=pump,args=(client,upstream),daemon=True)
        b=threading.Thread(target=pump,args=(upstream,client),daemon=True)
        a.start(); b.start(); a.join(); b.join()
    finally:
        upstream.close(); client.close()
server=socket.socket()
server.bind(("127.0.0.1",listen_port))
server.listen(32)
while True:
    client,_=server.accept()
    threading.Thread(target=handle,args=(client,),daemon=True).start()
PY
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE=socks-relay \
    nohup python3 "$relay" "$TASK_SOCKS_PORT" "$UPSTREAM_SOCKS_PORT" \
    >"$(runtime_dir)/relay.log" 2>&1 </dev/null &
  pid=$!; printf '%s\n' "$pid" >"$(pidfile socks-relay)"
  for _ in $(seq 1 50); do
    kill -0 "$pid" 2>/dev/null && port_listening "$TASK_SOCKS_PORT" && break
    sleep .1
  done
  role_owned "$pid" socks-relay "$(command -v python3)" || die relay_ownership_failed
  assert_no_secret_env "$pid" socks-relay
  port_listening "$TASK_SOCKS_PORT" || die relay_not_listening
  curl --socks5-hostname "127.0.0.1:$TASK_SOCKS_PORT" -fsS --max-time 15 \
    https://www.cloudflare.com/cdn-cgi/trace | grep -Eq '^warp=(on|plus)$' \
    || die task_relay_warp_not_verified
  printf 'TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=%s pid=%s\n' "$TASK_SOCKS_PORT" "$pid"
}

start_xvfb() {
  local td="$(toolroot)" xvfb="$BASE_STATE/runtime/Xvfb-track-a" pid
  [[ -x "$xvfb" ]] || xvfb="$td/usr/bin/Xvfb"
  [[ -x "$xvfb" ]] || die xvfb_unavailable
  [[ ! -e "/tmp/.X${DISPLAY_NUM}-lock" && ! -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]] \
    || die display_collision
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE=xvfb HOME="$(run_root)/home" \
    PATH="$td/usr/bin:$td/usr/sbin:/usr/bin:/bin" \
    LD_LIBRARY_PATH="$td/usr/lib/x86_64-linux-gnu:$td/lib/x86_64-linux-gnu" \
    XKB_CONFIG_ROOT="$td/usr/share/X11/xkb" \
    nohup "$xvfb" "$TRACK_DISPLAY" -screen 0 1280x800x24 \
    -xkbdir "$td/usr/share/X11/xkb" +extension GLX +iglx +render -nolisten tcp -noreset \
    >"$(runtime_dir)/xvfb.log" 2>&1 </dev/null &
  pid=$!; printf '%s\n' "$pid" >"$(pidfile xvfb)"
  for _ in $(seq 1 60); do
    [[ -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]] && break
    kill -0 "$pid" 2>/dev/null || die xvfb_exited
    sleep .25
  done
  role_owned "$pid" xvfb "$xvfb" || die xvfb_ownership_failed
  assert_no_secret_env "$pid" xvfb
  [[ -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]] || die xvfb_socket_missing
  printf 'TRACK_A_TASK_XVFB_VERIFIED=true display=%s pid=%s\n' "$TRACK_DISPLAY" "$pid"
}

bootstrap() {
  require_context
  local root="$(run_root)" src="$BASE_STATE/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia" dst
  mkdir -p "$TASK_ROOT/runs" "$root/home" "$(runtime_dir)" "$(evidence_dir)"
  printf '%s\n' "$TASK_ID" >"$root/task-id"
  verify_upstream_warp
  verify_client "$src/bin/client"
  dst="$(package_dir)"; mkdir -p "$dst"; cp -a --reflink=auto "$src/." "$dst/"
  verify_client "$dst/bin/client"
  cat >"$root/proxychains.conf" <<EOF
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 $TASK_SOCKS_PORT
EOF
  start_relay
  start_xvfb
  printf 'TRACK_A_RUNTIME_NAMESPACE_READY=true root=%s display=%s socks=%s\n' \
    "$root" "$TRACK_DISPLAY" "$TASK_SOCKS_PORT"
}

resolve_window() {
  local pid="$1" td="$(toolroot)" w g width height area best best_area
  for _ in $(seq 1 100); do
    best=''; best_area=0
    for w in $(DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null || true); do
      g="$(DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" getwindowgeometry --shell "$w" 2>/dev/null || true)"
      width="$(sed -n 's/^WIDTH=//p' <<<"$g")"; height="$(sed -n 's/^HEIGHT=//p' <<<"$g")"
      [[ -n "$width" && -n "$height" ]] || continue
      area=$((width*height))
      (( area > best_area )) && { best="$w"; best_area=$area; }
    done
    [[ -n "$best" ]] && { printf '%s\n' "$best"; return 0; }
    sleep .3
  done
  return 1
}

make_gdb_script() {
  local out="$1" pid="$2" bias="$3" records="$4"
  python3 - "$out" "$pid" "$bias" "$records" "$MAP_CAPTURE_OFFSET" <<'PY'
import sys
out,pid,bias,records,offset=sys.argv[1:]
text=f"""set pagination off
set confirm off
attach {pid}
python
import gdb, struct, time
inf=gdb.selected_inferior()
out=r'{records}'
class MapBP(gdb.Breakpoint):
    def __init__(self):
        super().__init__('*0x%x' % (int('{bias}',0)+int('{offset}',0)))
    def stop(self):
        try:
            rsp=int(gdb.parse_and_eval('$rsp'))
            order=int(gdb.parse_and_eval('$rbp')) & 0xffffffff
            x,y,z=struct.unpack('<III',bytes(inf.read_memory(rsp+0x88,12)))
            if 0<x<100000 and 0<y<100000 and z<32 and order<128:
                with open(out,'a') as f:
                    f.write(f'{{time.monotonic_ns()}}\\t{{x}}\\t{{y}}\\t{{z}}\\t{{order}}\\n')
                    f.flush()
        except Exception:
            pass
        return False
MapBP()
end
continue
"""
open(out,"w").write(text)
PY
  chmod 600 "$out"
}

prepare_generation() {
  require_context
  local gen="$1" root="$(run_root)" package="$(package_dir)" client td tool_path tool_lib
  local proxy_lib vk_icd swrast dri pid window line start off bias gdir gdb gp
  client="$package/bin/client"; td="$(toolroot)"
  tool_path="$td/usr/bin:$td/usr/sbin:/usr/bin:/bin"
  tool_lib="$td/usr/lib/x86_64-linux-gnu:$td/lib/x86_64-linux-gnu"
  proxy_lib="$(find "$td" -type f -name libproxychains.so.4 -print -quit)"
  vk_icd="$(find "$td/usr/share/vulkan/icd.d" -type f -name 'lvp_icd*.json' -print -quit)"
  swrast="$(find "$td" \( -type f -o -type l \) -name swrast_dri.so -print -quit)"
  [[ -n "$proxy_lib" && -n "$vk_icd" && -n "$swrast" ]] || die software_or_proxy_dependency_missing
  dri="$(dirname "$swrast")"
  verify_client "$client"
  role_owned "$(read_pid xvfb)" xvfb || die xvfb_not_owned
  role_owned "$(read_pid socks-relay)" socks-relay || die relay_not_owned
  gdir="$root/generation-$gen"; mkdir -p "$gdir" "$root/home-gen-$gen"; : >"$gdir/map-records.tsv"
  cd "$package"
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE="client-gen-$gen" HOME="$root/home-gen-$gen" DISPLAY="$TRACK_DISPLAY" \
    PATH="$tool_path" LD_LIBRARY_PATH="$package/lib:$tool_lib" LIBGL_ALWAYS_SOFTWARE=1 \
    LIBGL_DRIVERS_PATH="$dri" QSG_RHI_BACKEND=vulkan VK_ICD_FILENAMES="$vk_icd" VK_DRIVER_FILES="$vk_icd" \
    XDG_DATA_DIRS="$td/usr/share:/usr/share" FONTCONFIG_PATH="$td/etc/fonts" \
    FONTCONFIG_FILE="$td/etc/fonts/fonts.conf" LD_PRELOAD="$proxy_lib" \
    PROXYCHAINS_CONF_FILE="$root/proxychains.conf" \
    nohup "$client" >"$gdir/client.log" 2>&1 </dev/null &
  pid=$!; printf '%s\n' "$pid" >"$(pidfile "client-gen-$gen")"
  for _ in $(seq 1 80); do kill -0 "$pid" 2>/dev/null || die "client_gen_${gen}_exited"; [[ -r "/proc/$pid/maps" ]] && break; sleep .25; done
  role_owned "$pid" "client-gen-$gen" "$client" || die "client_gen_${gen}_ownership_failed"
  assert_no_secret_env "$pid" "client-gen-$gen"
  window="$(resolve_window "$pid")" || die "client_gen_${gen}_window_missing"
  DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" windowsize "$window" 1020 650 >/dev/null 2>&1 || true
  DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" windowmove "$window" 0 0 >/dev/null 2>&1 || true
  printf '%s\n' "$window" >"$gdir/window.id"
  line="$(grep -F "$(readlink -f "$client")" "/proc/$pid/maps" | awk '$2~/r-xp/{print;exit}')"
  [[ -n "$line" ]] || die text_mapping_missing
  start="$(awk '{split($1,a,"-");print a[1]}' <<<"$line")"; off="$(awk '{print $3}' <<<"$line")"
  bias=$((16#$start-16#$off)); printf '0x%x\n' "$bias" >"$gdir/pie-base.txt"; printf '%s\n' "$pid" >"$gdir/pid.txt"
  [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$pid/status")" == 0 ]] || die existing_tracer
  [[ "$(cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null || true)" == 0 ]] || die ptrace_scope_not_zero
  make_gdb_script "$gdir/world.gdb" "$pid" "$(cat "$gdir/pie-base.txt")" "$gdir/map-records.tsv"
  gdb="$td/usr/bin/gdb"; [[ -x "$gdb" ]] || die gdb_unavailable
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE="observer-gen-$gen" HOME="$root/home" PATH="$tool_path" LD_LIBRARY_PATH="$tool_lib" \
    nohup "$gdb" -q -nx -batch -x "$gdir/world.gdb" >"$gdir/gdb.log" 2>&1 </dev/null &
  gp=$!; printf '%s\n' "$gp" >"$(pidfile "observer-gen-$gen")"
  for _ in $(seq 1 50); do [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$pid/status")" == "$gp" ]] && break; kill -0 "$gp" 2>/dev/null || die observer_exited; sleep .15; done
  role_owned "$gp" "observer-gen-$gen" "$gdb" || die observer_ownership_failed
  assert_no_secret_env "$gp" "observer-gen-$gen"
  [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$pid/status")" == "$gp" ]] || die observer_not_attached
  sleep 5
  local baseline="$(wc -l <"$gdir/map-records.tsv")"
  printf '%s\n' "$baseline" >"$gdir/baseline-count.txt"
  [[ "$baseline" == 0 ]] || die "logged_out_worldmap_noise_gen_$gen"
  printf 'TRACK_A_NO_STIMULUS_BASELINE generation=%s records=0\n' "$gen"
  printf 'TRACK_A_GENERATION_PREPARED generation=%s pid=%s pie=%s observer=%s\n' "$gen" "$pid" "$(cat "$gdir/pie-base.txt")" "$gp"
}

login_generation() {
  require_context
  local gen="$1" root="$(run_root)" td="$(toolroot)" pid gp client window email password
  : "${TIBIA_TEST_EMAIL:?missing_TIBIA_TEST_EMAIL}"; : "${TIBIA_TEST_PASSWORD:?missing_TIBIA_TEST_PASSWORD}"
  email="$TIBIA_TEST_EMAIL"; password="$TIBIA_TEST_PASSWORD"; client="$(package_dir)/bin/client"
  pid="$(read_pid "client-gen-$gen")"; gp="$(read_pid "observer-gen-$gen")"
  role_owned "$pid" "client-gen-$gen" "$client" || die client_not_owned
  role_owned "$gp" "observer-gen-$gen" "$td/usr/bin/gdb" || die observer_not_owned
  assert_no_secret_env "$pid" "client-gen-$gen"; assert_no_secret_env "$gp" "observer-gen-$gen"
  window="$(cat "$root/generation-$gen/window.id")"; export DISPLAY="$TRACK_DISPLAY"
  "$td/usr/bin/xdotool" windowfocus --sync "$window"
  "$td/usr/bin/xdotool" mousemove --window "$window" 535 275 click 1
  "$td/usr/bin/xdotool" key --window "$window" ctrl+a
  env -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD "$td/usr/bin/xdotool" type --window "$window" --delay 12 -- "$email"
  "$td/usr/bin/xdotool" mousemove --window "$window" 535 304 click 1
  "$td/usr/bin/xdotool" key --window "$window" ctrl+a
  env -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD "$td/usr/bin/xdotool" type --window "$window" --delay 12 -- "$password"
  "$td/usr/bin/xdotool" mousemove --window "$window" 590 388 click 1
  unset email password TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
  printf 'TRACK_A_ACCOUNT_LOGIN_SUBMITTED generation=%s\n' "$gen"; sleep 8
  kill -0 "$pid" || die client_died_after_login
  window="$(resolve_window "$pid")" || die select_window_missing; printf '%s\n' "$window" >"$root/generation-$gen/window.id"
  "$td/usr/bin/xdotool" windowfocus --sync "$window"
  "$td/usr/bin/xdotool" mousemove --window "$window" 285 193 click 1
  sleep .4; "$td/usr/bin/xdotool" key --window "$window" Return
  printf 'TRACK_A_CHARACTER_ACTIVATION_SENT generation=%s\n' "$gen"; sleep 3
  window="$(resolve_window "$pid" || true)"
  [[ -n "$window" ]] && "$td/usr/bin/xdotool" mousemove --window "$window" 285 193 click --repeat 2 --delay 160 1 >/dev/null 2>&1 || true
}

socket_state() {
  python3 - "$1" "$TASK_SOCKS_PORT" <<'PY'
import os,pathlib,sys
pid,port=sys.argv[1],int(sys.argv[2]); inodes=set()
for fd in pathlib.Path("/proc",pid,"fd").iterdir():
    try:t=os.readlink(fd)
    except OSError:continue
    if t.startswith("socket:["):inodes.add(t[8:-1])
local=direct=udp=0
for name,is_udp in (("tcp",0),("tcp6",0),("udp",1),("udp6",1)):
    try:rows=pathlib.Path("/proc",pid,"net",name).read_text().splitlines()[1:]
    except OSError:continue
    for row in rows:
        f=row.split()
        if len(f)<10 or f[9] not in inodes:continue
        rp=int(f[2].rsplit(":",1)[1],16)
        if is_udp:udp+=1
        elif f[3]=="01":
            if rp==port:local+=1
            else:direct+=1
print(local,direct,udp)
PY
}

verify_generation() {
  require_context
  local gen="$1" root td gdir client
  root="$(run_root)"; td="$(toolroot)"; gdir="$root/generation-$gen"; client="$(package_dir)/bin/client"
  local pid gp records=0 local=0 direct=0 udp=0 streak=0 maxlocal=0
  pid="$(read_pid "client-gen-$gen")"; gp="$(read_pid "observer-gen-$gen")"
  role_owned "$pid" "client-gen-$gen" "$client" || die client_not_owned
  role_owned "$gp" "observer-gen-$gen" "$td/usr/bin/gdb" || die observer_not_owned
  verify_client "$client"; assert_no_secret_env "$pid" "client-gen-$gen"; assert_no_secret_env "$gp" "observer-gen-$gen"
  for _ in $(seq 1 90); do
    kill -0 "$pid" || die client_died_waiting_world; kill -0 "$gp" || die observer_died_waiting_world
    records="$(wc -l <"$gdir/map-records.tsv")"; read -r local direct udp < <(socket_state "$pid")
    (( local > maxlocal )) && maxlocal=$local || true
    [[ "$direct" == 0 && "$udp" == 0 ]] || die "transport_escape_gen_$gen"
    (( local >= 1 )) && streak=$((streak+1)) || streak=0
    (( records >= REQUIRED_RECORDS && streak >= 6 )) && break
    sleep 1
  done
  (( records >= REQUIRED_RECORDS )) || die "insufficient_structural_records_gen_$gen"
  (( streak >= 6 )) || die "socks_not_sustained_gen_$gen"
  awk -F '\t' 'NF==5 && $2>0 && $2<100000 && $3>0 && $3<100000 && $4>=0 && $4<32 && $5>=0 && $5<128 {ok++} END{exit !(ok==NR && NR>=8)}' "$gdir/map-records.tsv" \
    || die "invalid_structural_records_gen_$gen"
  local out="$(evidence_dir)/generation-$gen"; mkdir -p "$out"
  {
    printf 'generation=%s\n' "$gen"
    printf 'observer_epoch=%s-gen%s-pid%s\n' "$GITHUB_RUN_ID" "$gen" "$pid"
    printf 'client_sha256=%s\nclient_size=%s\npid=%s\npie_base=%s\n' "$EXPECTED_CLIENT_SHA256" "$EXPECTED_CLIENT_SIZE" "$pid" "$(cat "$gdir/pie-base.txt")"
    printf 'baseline_worldmap_records=0\npostlogin_worldmap_records=%s\ntask_local_socks_max=%s\ndirect_tcp=%s\nclient_udp=%s\n' "$records" "$maxlocal" "$direct" "$udp"
    printf 'credential_env_clear=true\nstructural_in_game=true\ngameplay_stimulus=none\n'
  } >"$out/summary.txt"
  cp "$gdir/map-records.tsv" "$out/map-records.tsv"
  printf 'TRACK_A_STRUCTURAL_IN_GAME generation=%s records=%s pid=%s pie=%s\n' "$gen" "$records" "$pid" "$(cat "$gdir/pie-base.txt")"
}

stop_generation() {
  require_context
  local gen="$1" td="$(toolroot)" client="$(package_dir)/bin/client" gp pid
  gp="$(read_pid "observer-gen-$gen" 2>/dev/null || true)"; pid="$(read_pid "client-gen-$gen" 2>/dev/null || true)"
  if [[ -n "$gp" ]] && kill -0 "$gp" 2>/dev/null; then
    role_owned "$gp" "observer-gen-$gen" "$td/usr/bin/gdb" || die refuse_foreign_observer_cleanup
    kill -INT "$gp" 2>/dev/null || true; for _ in $(seq 1 30); do kill -0 "$gp" 2>/dev/null || break; sleep .1; done
  fi
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    role_owned "$pid" "client-gen-$gen" "$client" || die refuse_foreign_client_cleanup
    kill -CONT "$pid" 2>/dev/null || true; kill -TERM "$pid" 2>/dev/null || true
    for _ in $(seq 1 50); do kill -0 "$pid" 2>/dev/null || break; sleep .1; done
    kill -0 "$pid" 2>/dev/null && die client_cleanup_timeout
  fi
  printf 'TRACK_A_GENERATION_STOPPED generation=%s\n' "$gen"
}

compare_generations() {
  require_context
  local root g1 g2
  root="$(run_root)"; g1="$root/generation-1"; g2="$root/generation-2"
  local pid1="$(cat "$g1/pid.txt")" pid2="$(cat "$g2/pid.txt")" pie1="$(cat "$g1/pie-base.txt")" pie2="$(cat "$g2/pie-base.txt")"
  local r1="$(wc -l <"$g1/map-records.tsv")" r2="$(wc -l <"$g2/map-records.tsv")"
  [[ "$pid1" != "$pid2" ]] || die pid_not_fresh
  [[ "$pie1" != "$pie2" ]] || die pie_not_fresh
  [[ "$(cat "$g1/baseline-count.txt")" == 0 && "$(cat "$g2/baseline-count.txt")" == 0 ]] || die negative_control_failed
  (( r1 >= REQUIRED_RECORDS && r2 >= REQUIRED_RECORDS )) || die restart_read_not_reacquired
  {
    printf 'task_id=%s\nresult=DRAFT_PROVEN_RESTART_RELOGIN_REACQUISITION\n' "$TASK_ID"
    printf 'client_sha256=%s\nclient_size=%s\n' "$EXPECTED_CLIENT_SHA256" "$EXPECTED_CLIENT_SIZE"
    printf 'generation_1_pid=%s\ngeneration_2_pid=%s\ngeneration_1_pie=%s\ngeneration_2_pie=%s\n' "$pid1" "$pid2" "$pie1" "$pie2"
    printf 'generation_1_postlogin_records=%s\ngeneration_2_postlogin_records=%s\n' "$r1" "$r2"
    printf 'read_gate_candidate=R3_RESTART_STABLE_READ\nbridge_session_epoch=NOT_PROVEN\naction_gate_a3=NOT_PROVEN\naction_gate_a4=NOT_PROVEN\n'
    printf 'gameplay_actions_performed=0\nside_effects=login_relogin_and_clean_process_restart_only\n'
  } >"$(evidence_dir)/result.txt"
  printf 'TRACK_A_RESTART_RELOGIN_REACQUISITION_PROVEN=true pid1=%s pid2=%s pie1=%s pie2=%s\n' "$pid1" "$pid2" "$pie1" "$pie2"
}

cleanup_role() {
  local role="$1" expected="$2" pid
  pid="$(read_pid "$role" 2>/dev/null || true)"
  [[ -n "$pid" ]] || return 0; kill -0 "$pid" 2>/dev/null || return 0
  role_owned "$pid" "$role" "$expected" || die "refuse_foreign_cleanup_$role"
  kill -TERM "$pid" 2>/dev/null || true; for _ in $(seq 1 40); do kill -0 "$pid" 2>/dev/null || break; sleep .1; done
  kill -0 "$pid" 2>/dev/null && die "cleanup_timeout_$role"
}

cleanup_all() {
  require_context
  stop_generation 1 || true; stop_generation 2 || true
  local td="$(toolroot)" xvfb="$BASE_STATE/runtime/Xvfb-track-a" root="$(run_root)"
  [[ -x "$xvfb" ]] || xvfb="$td/usr/bin/Xvfb"
  cleanup_role xvfb "$xvfb"; cleanup_role socks-relay "$(command -v python3)"
  printf 'TRACK_A_TASK_PROCESS_CLEANUP_COMPLETE=true\n'
  [[ -e "/tmp/.X${DISPLAY_NUM}-lock" || -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]] \
    && printf 'TRACK_A_TASK_X11_RESIDUE_PRESENT=true\n' || printf 'TRACK_A_TASK_X11_RESIDUE_PRESENT=false\n'
  [[ -r "$root/task-id" && "$(cat "$root/task-id")" == "$TASK_ID" ]] || die refuse_unmarked_run_root_cleanup
  [[ "$root" == "$TASK_ROOT/runs/$GITHUB_RUN_ID" ]] || die refuse_out_of_namespace_cleanup
  rm -rf --one-file-system "$root"
  printf 'TRACK_A_TASK_EPHEMERAL_STATE_REMOVED=true\n'
}

case "${1:-}" in
  bootstrap) bootstrap ;;
  prepare) prepare_generation "${2:?generation}" ;;
  login) login_generation "${2:?generation}" ;;
  verify) verify_generation "${2:?generation}" ;;
  stop) stop_generation "${2:?generation}" ;;
  compare) compare_generations ;;
  cleanup) cleanup_all ;;
  *) die usage ;;
esac
