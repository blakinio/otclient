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

die() {
  printf 'TRACK_A_RUNTIME_ERROR=%s\n' "$1" >&2
  exit "${2:-1}"
}

require_context() {
  [[ "${GITHUB_REPOSITORY:-}" == 'blakinio/otclient' ]] || die 'wrong_repository'
  [[ "${RUNNER_NAME:-}" == 'synology-otclient-01' ]] || die 'wrong_runner'
  [[ "$(uname -s)" == 'Linux' ]] || die 'non_linux_runner'
  [[ "${GITHUB_REF_NAME:-}" == 'research/OTC-20260815-track-a-runtime-reacquisition' ]] || die 'wrong_branch'
  [[ -n "${GITHUB_RUN_ID:-}" ]] || die 'missing_github_run_id'
  [[ -d "$BASE_STATE" && -w "$BASE_STATE" ]] || die 'canonical_state_unavailable'
}

run_root() {
  printf '%s/runs/%s\n' "$TASK_ROOT" "$GITHUB_RUN_ID"
}

runtime_dir() {
  printf '%s/runtime\n' "$(run_root)"
}

evidence_dir() {
  printf '%s/artifacts/runtime-reacquisition\n' "$GITHUB_WORKSPACE"
}

source_package() {
  printf '%s/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia\n' "$BASE_STATE"
}

package_dir() {
  printf '%s/package\n' "$(run_root)"
}

toolroot() {
  printf '%s/toolroot\n' "$BASE_STATE"
}

pidfile() {
  local role="$1"
  printf '%s/%s.pid\n' "$(runtime_dir)" "$role"
}

role_exe_matches() {
  local pid="$1" role="$2" expected="${3:-}"
  [[ -r "/proc/$pid/environ" ]] || return 1
  grep -azFxq "$TRACK_MARKER" "/proc/$pid/environ" || return 1
  grep -azFxq "$TASK_MARKER" "/proc/$pid/environ" || return 1
  grep -azFxq "$ROLE_VAR=$role" "/proc/$pid/environ" || return 1
  [[ -z "$expected" || "$(readlink -f "/proc/$pid/exe")" == "$(readlink -f "$expected")" ]] || return 1
}

read_pid() {
  local role="$1" file
  file="$(pidfile "$role")"
  [[ -r "$file" ]] || return 1
  tr -cd '0-9' <"$file"
}

assert_no_credential_env() {
  local pid="$1" role="$2"
  [[ -r "/proc/$pid/environ" ]] || die "missing_${role}_environ"
  if grep -azEq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD)=' "/proc/$pid/environ"; then
    die "credential_env_leak_${role}"
  fi
  printf 'TRACK_A_CREDENTIAL_ENV_CLEAR role=%s pid=%s\n' "$role" "$pid"
}

verify_client_identity() {
  local client="$1"
  [[ -x "$client" ]] || die 'client_not_executable'
  local size sha
  size="$(stat -c '%s' "$client")"
  sha="$(sha256sum "$client" | awk '{print $1}')"
  [[ "$size" == "$EXPECTED_CLIENT_SIZE" ]] || die "client_size_mismatch_${size}"
  [[ "$sha" == "$EXPECTED_CLIENT_SHA256" ]] || die "client_sha_mismatch_${sha}"
  printf 'TRACK_A_EXACT_CLIENT_VERIFIED size=%s sha256=%s\n' "$size" "$sha"
}

copy_package_once() {
  local src dst
  src="$(source_package)"
  dst="$(package_dir)"
  verify_client_identity "$src/bin/client"
  if [[ ! -d "$dst" ]]; then
    mkdir -p "$dst"
    cp -a --reflink=auto "$src/." "$dst/"
  fi
  verify_client_identity "$dst/bin/client"
}

write_relay() {
  local root relay
  root="$(run_root)"
  relay="$root/tcp-relay.py"
  cat >"$relay" <<'PY'
import socket
import sys
import threading

listen_port = int(sys.argv[1])
upstream_port = int(sys.argv[2])

def pump(source, target):
    try:
        while True:
            data = source.recv(65536)
            if not data:
                break
            target.sendall(data)
    except OSError:
        pass
    finally:
        try:
            target.shutdown(socket.SHUT_WR)
        except OSError:
            pass

def handle(client):
    upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        upstream.connect(("127.0.0.1", upstream_port))
        left = threading.Thread(target=pump, args=(client, upstream), daemon=True)
        right = threading.Thread(target=pump, args=(upstream, client), daemon=True)
        left.start()
        right.start()
        left.join()
        right.join()
    finally:
        try:
            upstream.close()
        finally:
            client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", listen_port))
server.listen(32)
while True:
    client, _ = server.accept()
    threading.Thread(target=handle, args=(client,), daemon=True).start()
PY
  chmod 600 "$relay"
}

write_proxy_config() {
  local conf
  conf="$(run_root)/proxychains.conf"
  cat >"$conf" <<EOF
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 $TASK_SOCKS_PORT
EOF
  chmod 600 "$conf"
}

verify_upstream_warp() {
  local warp_pid
  warp_pid="$(tr -cd '0-9' <"$BASE_STATE/runtime/wireproxy.pid" 2>/dev/null || true)"
  [[ -n "$warp_pid" && -r "/proc/$warp_pid/environ" ]] || die 'upstream_wireproxy_unavailable'
  grep -azFxq "$TRACK_MARKER" "/proc/$warp_pid/environ" || die 'upstream_wireproxy_wrong_owner'
  kill -0 "$warp_pid" || die 'upstream_wireproxy_dead'
  curl --socks5-hostname "127.0.0.1:$UPSTREAM_SOCKS_PORT" -fsS --max-time 15 \
    https://www.cloudflare.com/cdn-cgi/trace | grep -Eq '^warp=(on|plus)$' \
    || die 'upstream_warp_not_verified'
  printf 'TRACK_A_UPSTREAM_WARP_VERIFIED=true pid=%s\n' "$warp_pid"
}

port_is_listening() {
  python3 - "$1" <<'PY'
import pathlib, sys
port = int(sys.argv[1])
needle = f"{port:04X}"
for name in ("tcp", "tcp6"):
    path = pathlib.Path("/proc/net") / name
    if not path.exists():
        continue
    for line in path.read_text().splitlines()[1:]:
        parts = line.split()
        if len(parts) > 3 and parts[1].rsplit(":", 1)[-1].upper() == needle and parts[3] == "0A":
            raise SystemExit(0)
raise SystemExit(1)
PY
}

start_relay() {
  local root relay pid
  root="$(run_root)"
  relay="$root/tcp-relay.py"
  if port_is_listening "$TASK_SOCKS_PORT"; then
    die 'task_socks_port_collision'
  fi
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re \
    OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE=socks-relay \
    nohup python3 "$relay" "$TASK_SOCKS_PORT" "$UPSTREAM_SOCKS_PORT" \
    >"$(runtime_dir)/relay.log" 2>&1 </dev/null &
  pid=$!
  printf '%s\n' "$pid" >"$(pidfile socks-relay)"
  for _ in $(seq 1 50); do
    if kill -0 "$pid" 2>/dev/null && port_is_listening "$TASK_SOCKS_PORT"; then
      break
    fi
    sleep .1
  done
  role_exe_matches "$pid" socks-relay "$(command -v python3)" || die 'relay_ownership_verification_failed'
  assert_no_credential_env "$pid" socks-relay
  port_is_listening "$TASK_SOCKS_PORT" || die 'relay_not_listening'
  curl --socks5-hostname "127.0.0.1:$TASK_SOCKS_PORT" -fsS --max-time 15 \
    https://www.cloudflare.com/cdn-cgi/trace | grep -Eq '^warp=(on|plus)$' \
    || die 'task_relay_warp_not_verified'
  printf 'TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=%s pid=%s\n' "$TASK_SOCKS_PORT" "$pid"
}

start_xvfb() {
  local root td tl private_xvfb pid
  root="$(run_root)"
  td="$(toolroot)"
  tl="$td/usr/lib/x86_64-linux-gnu:$td/lib/x86_64-linux-gnu"
  private_xvfb="$BASE_STATE/runtime/Xvfb-track-a"
  [[ -x "$private_xvfb" ]] || private_xvfb="$td/usr/bin/Xvfb"
  [[ -x "$private_xvfb" ]] || die 'xvfb_binary_unavailable'
  [[ ! -e "/tmp/.X${DISPLAY_NUM}-lock" && ! -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]] || die 'display_collision'
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re \
    OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE=xvfb \
    HOME="$root/home" \
    PATH="$td/usr/bin:$td/usr/sbin:/usr/bin:/bin" \
    LD_LIBRARY_PATH="$tl" \
    XKB_CONFIG_ROOT="$td/usr/share/X11/xkb" \
    nohup "$private_xvfb" "$TRACK_DISPLAY" -screen 0 1280x800x24 \
    -xkbdir "$td/usr/share/X11/xkb" +extension GLX +iglx +render -nolisten tcp -noreset \
    >"$(runtime_dir)/xvfb.log" 2>&1 </dev/null &
  pid=$!
  printf '%s\n' "$pid" >"$(pidfile xvfb)"
  for _ in $(seq 1 60); do
    [[ -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]] && break
    kill -0 "$pid" 2>/dev/null || die 'xvfb_exited'
    sleep .25
  done
  role_exe_matches "$pid" xvfb "$private_xvfb" || die 'xvfb_ownership_verification_failed'
  assert_no_credential_env "$pid" xvfb
  [[ -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]] || die 'xvfb_socket_missing'
  printf 'TRACK_A_TASK_XVFB_VERIFIED=true display=%s pid=%s\n' "$TRACK_DISPLAY" "$pid"
}

bootstrap() {
  require_context
  local root
  root="$(run_root)"
  mkdir -p "$TASK_ROOT/runs" "$root/home" "$(runtime_dir)" "$(evidence_dir)"
  printf '%s\n' "$TASK_ID" >"$root/task-id"
  write_relay
  write_proxy_config
  verify_upstream_warp
  copy_package_once
  start_relay
  start_xvfb
  printf 'TRACK_A_RUNTIME_NAMESPACE_READY=true root=%s display=%s task_socks=%s\n' \
    "$root" "$TRACK_DISPLAY" "$TASK_SOCKS_PORT"
}

resolve_window() {
  local pid="$1" td w g width height area best='' best_area=0
  td="$(toolroot)"
  for _ in $(seq 1 100); do
    best=''
    best_area=0
    for w in $(DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null || true); do
      g="$(DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" getwindowgeometry --shell "$w" 2>/dev/null || true)"
      width="$(printf '%s\n' "$g" | sed -n 's/^WIDTH=//p')"
      height="$(printf '%s\n' "$g" | sed -n 's/^HEIGHT=//p')"
      [[ -n "$width" && -n "$height" ]] || continue
      area=$((width * height))
      if (( area > best_area )); then
        best="$w"
        best_area=$area
      fi
    done
    if [[ -n "$best" ]]; then
      printf '%s\n' "$best"
      return 0
    fi
    sleep .3
  done
  return 1
}

prepare_generation() {
  require_context
  local gen="${1:?generation}" root package client td tool_path tool_lib proxy_lib vk_icd swrast dri_dir pid window line start off bias gen_dir gcmd gdb gp
  root="$(run_root)"
  package="$(package_dir)"
  client="$package/bin/client"
  td="$(toolroot)"
  tool_path="$td/usr/bin:$td/usr/sbin:/usr/bin:/bin"
  tool_lib="$td/usr/lib/x86_64-linux-gnu:$td/lib/x86_64-linux-gnu"
  proxy_lib="$(find "$td" -type f -name 'libproxychains.so.4' -print -quit)"
  vk_icd="$(find "$td/usr/share/vulkan/icd.d" -type f -name 'lvp_icd*.json' -print -quit)"
  swrast="$(find "$td" \( -type f -o -type l \) -name 'swrast_dri.so' -print -quit)"
  [[ -n "$proxy_lib" && -n "$vk_icd" && -n "$swrast" ]] || die 'software_render_or_proxy_dependency_missing'
  dri_dir="$(dirname "$swrast")"
  verify_client_identity "$client"
  role_exe_matches "$(read_pid xvfb)" xvfb || die 'xvfb_not_owned_or_dead'
  role_exe_matches "$(read_pid socks-relay)" socks-relay || die 'relay_not_owned_or_dead'
  port_is_listening "$TASK_SOCKS_PORT" || die 'task_socks_relay_not_listening'
  gen_dir="$root/generation-$gen"
  mkdir -p "$gen_dir" "$root/home-gen-$gen"
  : >"$gen_dir/map-records.tsv"
  : >"$gen_dir/gdb.log"
  cd "$package"
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re \
    OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE="client-gen-$gen" \
    HOME="$root/home-gen-$gen" DISPLAY="$TRACK_DISPLAY" PATH="$tool_path" \
    LD_LIBRARY_PATH="$package/lib:$tool_lib" \
    LIBGL_ALWAYS_SOFTWARE=1 LIBGL_DRIVERS_PATH="$dri_dir" QSG_RHI_BACKEND=vulkan \
    VK_ICD_FILENAMES="$vk_icd" VK_DRIVER_FILES="$vk_icd" \
    XDG_DATA_DIRS="$td/usr/share:/usr/share" \
    FONTCONFIG_PATH="$td/etc/fonts" FONTCONFIG_FILE="$td/etc/fonts/fonts.conf" \
    LD_PRELOAD="$proxy_lib" PROXYCHAINS_CONF_FILE="$root/proxychains.conf" \
    nohup "$client" >"$gen_dir/client.log" 2>&1 </dev/null &
  pid=$!
  printf '%s\n' "$pid" >"$(pidfile "client-gen-$gen")"
  for _ in $(seq 1 80); do
    kill -0 "$pid" 2>/dev/null || die "client_gen_${gen}_exited"
    [[ -r "/proc/$pid/maps" ]] && break
    sleep .25
  done
  role_exe_matches "$pid" "client-gen-$gen" "$client" || die "client_gen_${gen}_ownership_failed"
  assert_no_credential_env "$pid" "client-gen-$gen"
  verify_client_identity "$client"
  window="$(resolve_window "$pid")" || die "client_gen_${gen}_window_not_found"
  DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" windowsize "$window" 1020 650 >/dev/null 2>&1 || true
  DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" windowmove "$window" 0 0 >/dev/null 2>&1 || true
  printf '%s\n' "$window" >"$gen_dir/window.id"
  line="$(grep -F "$(readlink -f "$client")" "/proc/$pid/maps" | awk '$2~/r-xp/{print;exit}')"
  [[ -n "$line" ]] || die "client_gen_${gen}_text_mapping_missing"
  start="$(printf '%s\n' "$line" | awk '{split($1,a,"-");print a[1]}')"
  off="$(printf '%s\n' "$line" | awk '{print $3}')"
  bias=$((16#$start - 16#$off))
  printf '0x%x\n' "$bias" >"$gen_dir/pie-base.txt"
  printf '%s\n' "$pid" >"$gen_dir/pid.txt"
  awk '/^TracerPid:/{print $2}' "/proc/$pid/status" | grep -qx '0' || die "client_gen_${gen}_already_traced"
  [[ "$(cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null || printf unknown)" == '0' ]] || die 'ptrace_scope_not_zero'
  gcmd="$gen_dir/world.gdb"
  cat >"$gcmd" <<EOF
set pagination off
set confirm off
attach $pid
python
import gdb, struct, time
inf = gdb.selected_inferior()
out = r'$gen_dir/map-records.tsv'
class MapBP(gdb.Breakpoint):
    def __init__(self):
        super().__init__('*0x%x' % ($bias + $MAP_CAPTURE_OFFSET))
    def stop(self):
        try:
            rsp = int(gdb.parse_and_eval('\\$rsp'))
            order = int(gdb.parse_and_eval('\\$rbp')) & 0xffffffff
            x, y, z = struct.unpack('<III', bytes(inf.read_memory(rsp + 0x88, 12)))
            if 0 < x < 100000 and 0 < y < 100000 and z < 32 and order < 128:
                with open(out, 'a') as handle:
                    handle.write(f'{time.monotonic_ns()}\\t{x}\\t{y}\\t{z}\\t{order}\\n')
                    handle.flush()
        except Exception:
            pass
        return False
MapBP()
end
continue
EOF
  chmod 600 "$gcmd"
  gdb="$td/usr/bin/gdb"
  [[ -x "$gdb" ]] || die 'gdb_unavailable'
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re \
    OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_ROLE="observer-gen-$gen" \
    HOME="$root/home" PATH="$tool_path" LD_LIBRARY_PATH="$tool_lib" \
    nohup "$gdb" -q -nx -batch -x "$gcmd" >"$gen_dir/gdb.log" 2>&1 </dev/null &
  gp=$!
  printf '%s\n' "$gp" >"$(pidfile "observer-gen-$gen")"
  for _ in $(seq 1 40); do
    if [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$pid/status")" == "$gp" ]]; then
      break
    fi
    kill -0 "$gp" 2>/dev/null || die "observer_gen_${gen}_exited"
    sleep .15
  done
  role_exe_matches "$gp" "observer-gen-$gen" "$gdb" || die "observer_gen_${gen}_ownership_failed"
  assert_no_credential_env "$gp" "observer-gen-$gen"
  [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$pid/status")" == "$gp" ]] || die "observer_gen_${gen}_not_attached"
  sleep 5
  local baseline
  baseline="$(wc -l <"$gen_dir/map-records.tsv")"
  printf '%s\n' "$baseline" >"$gen_dir/baseline-count.txt"
  printf 'TRACK_A_NO_STIMULUS_BASELINE generation=%s records=%s\n' "$gen" "$baseline"
  [[ "$baseline" == '0' ]] || die "logged_out_worldmap_noise_gen_${gen}"
  printf 'TRACK_A_GENERATION_PREPARED generation=%s pid=%s pie=0x%x observer=%s\n' "$gen" "$pid" "$bias" "$gp"
}

login_generation() {
  require_context
  local gen="${1:?generation}" root td pid gp client window email password
  : "${TIBIA_TEST_EMAIL:?missing_TIBIA_TEST_EMAIL}"
  : "${TIBIA_TEST_PASSWORD:?missing_TIBIA_TEST_PASSWORD}"
  email="$TIBIA_TEST_EMAIL"
  password="$TIBIA_TEST_PASSWORD"
  root="$(run_root)"
  td="$(toolroot)"
  client="$(package_dir)/bin/client"
  pid="$(read_pid "client-gen-$gen")" || die "missing_client_pid_gen_${gen}"
  gp="$(read_pid "observer-gen-$gen")" || die "missing_observer_pid_gen_${gen}"
  role_exe_matches "$pid" "client-gen-$gen" "$client" || die "client_gen_${gen}_not_owned"
  role_exe_matches "$gp" "observer-gen-$gen" "$td/usr/bin/gdb" || die "observer_gen_${gen}_not_owned"
  assert_no_credential_env "$pid" "client-gen-$gen"
  assert_no_credential_env "$gp" "observer-gen-$gen"
  window="$(cat "$root/generation-$gen/window.id")"
  export DISPLAY="$TRACK_DISPLAY"
  "$td/usr/bin/xdotool" windowactivate --sync "$window" 2>/dev/null || true
  "$td/usr/bin/xdotool" windowfocus --sync "$window"
  "$td/usr/bin/xdotool" mousemove --window "$window" 535 275 click 1
  "$td/usr/bin/xdotool" key --window "$window" ctrl+a
  env -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD "$td/usr/bin/xdotool" type --window "$window" --delay 12 -- "$email"
  "$td/usr/bin/xdotool" mousemove --window "$window" 535 304 click 1
  "$td/usr/bin/xdotool" key --window "$window" ctrl+a
  env -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD "$td/usr/bin/xdotool" type --window "$window" --delay 12 -- "$password"
  "$td/usr/bin/xdotool" mousemove --window "$window" 590 388 click 1
  unset email password TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
  printf 'TRACK_A_ACCOUNT_LOGIN_SUBMITTED generation=%s\n' "$gen"
  sleep 8
  kill -0 "$pid" || die "client_gen_${gen}_died_after_login"
  window="$(resolve_window "$pid")" || die "client_gen_${gen}_select_window_missing"
  printf '%s\n' "$window" >"$root/generation-$gen/window.id"
  "$td/usr/bin/xdotool" windowactivate --sync "$window" 2>/dev/null || true
  "$td/usr/bin/xdotool" windowfocus --sync "$window"
  "$td/usr/bin/xdotool" mousemove --window "$window" 285 193 click 1
  sleep .4
  "$td/usr/bin/xdotool" key --window "$window" Return
  printf 'TRACK_A_CHARACTER_RETURN_SENT generation=%s\n' "$gen"
  sleep 3
  kill -0 "$pid" || die "client_gen_${gen}_died_after_character_return"
  window="$(resolve_window "$pid" || true)"
  if [[ -n "$window" ]]; then
    "$td/usr/bin/xdotool" mousemove --window "$window" 285 193 click --repeat 2 --delay 160 1 >/dev/null 2>&1 || true
    printf 'TRACK_A_CHARACTER_DOUBLECLICK_FALLBACK_SENT generation=%s\n' "$gen"
  fi
}

socket_state() {
  python3 - "$1" "$TASK_SOCKS_PORT" <<'PY'
import os
import pathlib
import sys

pid = sys.argv[1]
port = int(sys.argv[2])
inodes = set()
for fd in pathlib.Path("/proc", pid, "fd").iterdir():
    try:
        target = os.readlink(fd)
    except OSError:
        continue
    if target.startswith("socket:["):
        inodes.add(target[8:-1])

local = direct = udp = 0
for name, is_udp in (("tcp", False), ("tcp6", False), ("udp", True), ("udp6", True)):
    path = pathlib.Path("/proc", pid, "net", name)
    try:
        rows = path.read_text().splitlines()[1:]
    except OSError:
        continue
    for row in rows:
        fields = row.split()
        if len(fields) < 10 or fields[9] not in inodes:
            continue
        remote_port = int(fields[2].rsplit(":", 1)[1], 16)
        if is_udp:
            udp += 1
        elif fields[3] == "01":
            if remote_port == port:
                local += 1
            else:
                direct += 1
print(local, direct, udp)
PY
}

verify_generation() {
  require_context
  local gen="${1:?generation}" root td gen_dir pid gp client records=0 local=0 direct=0 udp=0 consecutive=0 max_local=0 i pie epoch summary artifact_gen
  root="$(run_root)"
  td="$(toolroot)"
  gen_dir="$root/generation-$gen"
  client="$(package_dir)/bin/client"
  pid="$(read_pid "client-gen-$gen")" || die "missing_client_pid_gen_${gen}"
  gp="$(read_pid "observer-gen-$gen")" || die "missing_observer_pid_gen_${gen}"
  role_exe_matches "$pid" "client-gen-$gen" "$client" || die "client_gen_${gen}_not_owned"
  role_exe_matches "$gp" "observer-gen-$gen" "$td/usr/bin/gdb" || die "observer_gen_${gen}_not_owned"
  verify_client_identity "$client"
  assert_no_credential_env "$pid" "client-gen-$gen"
  assert_no_credential_env "$gp" "observer-gen-$gen"
  for i in $(seq 1 90); do
    kill -0 "$pid" || die "client_gen_${gen}_died_waiting_world"
    kill -0 "$gp" || die "observer_gen_${gen}_died_waiting_world"
    records="$(wc -l <"$gen_dir/map-records.tsv")"
    read -r local direct udp < <(socket_state "$pid")
    (( local > max_local )) && max_local=$local || true
    [[ "$direct" == '0' && "$udp" == '0' ]] || die "transport_escape_gen_${gen}"
    if (( local >= 2 )); then
      consecutive=$((consecutive + 1))
    else
      consecutive=0
    fi
    if (( records >= REQUIRED_RECORDS && consecutive >= 6 )); then
      break
    fi
    sleep 1
  done
  (( records >= REQUIRED_RECORDS )) || die "insufficient_structural_records_gen_${gen}"
  (( consecutive >= 6 )) || die "socks_session_not_sustained_gen_${gen}"
  awk -F '\t' 'NF==5 && $2>0 && $2<100000 && $3>0 && $3<100000 && $4>=0 && $4<32 && $5>=0 && $5<128 {ok++} END{exit !(ok==NR && NR>=8)}' \
    "$gen_dir/map-records.tsv" || die "invalid_structural_records_gen_${gen}"
  pie="$(cat "$gen_dir/pie-base.txt")"
  epoch="${GITHUB_RUN_ID}-gen${gen}-pid${pid}"
  printf '%s\n' "$epoch" >"$gen_dir/session-epoch.txt"
  summary="$gen_dir/summary.txt"
  {
    printf 'generation=%s\n' "$gen"
    printf 'session_epoch=%s\n' "$epoch"
    printf 'client_sha256=%s\n' "$EXPECTED_CLIENT_SHA256"
    printf 'client_size=%s\n' "$EXPECTED_CLIENT_SIZE"
    printf 'pid=%s\n' "$pid"
    printf 'pie_base=%s\n' "$pie"
    printf 'baseline_worldmap_records=%s\n' "$(cat "$gen_dir/baseline-count.txt")"
    printf 'postlogin_worldmap_records=%s\n' "$records"
    printf 'task_local_socks_max=%s\n' "$max_local"
    printf 'direct_tcp=%s\n' "$direct"
    printf 'client_udp=%s\n' "$udp"
    printf 'credential_env_clear=true\n'
    printf 'structural_in_game=true\n'
    printf 'gameplay_stimulus=none\n'
  } >"$summary"
  artifact_gen="$(evidence_dir)/generation-$gen"
  mkdir -p "$artifact_gen"
  cp "$summary" "$artifact_gen/summary.txt"
  cp "$gen_dir/map-records.tsv" "$artifact_gen/map-records.tsv"
  printf 'TRACK_A_STRUCTURAL_IN_GAME generation=%s records=%s pid=%s pie=%s\n' "$gen" "$records" "$pid" "$pie"
  printf 'TRACK_A_TRANSPORT_CONFINED generation=%s socks_max=%s direct=%s udp=%s\n' "$gen" "$max_local" "$direct" "$udp"
}

stop_generation() {
  require_context
  local gen="${1:?generation}" td client gp pid
  td="$(toolroot)"
  client="$(package_dir)/bin/client"
  gp="$(read_pid "observer-gen-$gen" 2>/dev/null || true)"
  pid="$(read_pid "client-gen-$gen" 2>/dev/null || true)"
  if [[ -n "$gp" ]] && kill -0 "$gp" 2>/dev/null; then
    role_exe_matches "$gp" "observer-gen-$gen" "$td/usr/bin/gdb" || die "refuse_foreign_observer_cleanup_gen_${gen}"
    kill -INT "$gp" 2>/dev/null || true
    for _ in $(seq 1 30); do kill -0 "$gp" 2>/dev/null || break; sleep .1; done
  fi
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    role_exe_matches "$pid" "client-gen-$gen" "$client" || die "refuse_foreign_client_cleanup_gen_${gen}"
    kill -CONT "$pid" 2>/dev/null || true
    kill -TERM "$pid" 2>/dev/null || true
    for _ in $(seq 1 50); do kill -0 "$pid" 2>/dev/null || break; sleep .1; done
    kill -0 "$pid" 2>/dev/null && die "client_gen_${gen}_did_not_exit"
  fi
  printf 'TRACK_A_GENERATION_STOPPED generation=%s\n' "$gen"
}

compare_generations() {
  require_context
  local root g1 g2 pid1 pid2 pie1 pie2 base1 base2 records1 records2 out
  root="$(run_root)"
  g1="$root/generation-1"
  g2="$root/generation-2"
  pid1="$(cat "$g1/pid.txt")"
  pid2="$(cat "$g2/pid.txt")"
  pie1="$(cat "$g1/pie-base.txt")"
  pie2="$(cat "$g2/pie-base.txt")"
  base1="$(cat "$g1/baseline-count.txt")"
  base2="$(cat "$g2/baseline-count.txt")"
  records1="$(wc -l <"$g1/map-records.tsv")"
  records2="$(wc -l <"$g2/map-records.tsv")"
  [[ "$pid1" != "$pid2" ]] || die 'pid_not_fresh'
  [[ "$pie1" != "$pie2" ]] || die 'pie_not_fresh'
  [[ "$base1" == '0' && "$base2" == '0' ]] || die 'negative_control_failed'
  (( records1 >= REQUIRED_RECORDS && records2 >= REQUIRED_RECORDS )) || die 'restart_structural_read_not_reacquired'
  out="$(evidence_dir)/result.txt"
  {
    printf 'task_id=%s\n' "$TASK_ID"
    printf 'result=DRAFT_PROVEN_RESTART_RELOGIN_REACQUISITION\n'
    printf 'client_sha256=%s\n' "$EXPECTED_CLIENT_SHA256"
    printf 'client_size=%s\n' "$EXPECTED_CLIENT_SIZE"
    printf 'generation_1_pid=%s\n' "$pid1"
    printf 'generation_2_pid=%s\n' "$pid2"
    printf 'generation_1_pie=%s\n' "$pie1"
    printf 'generation_2_pie=%s\n' "$pie2"
    printf 'generation_1_baseline_records=%s\n' "$base1"
    printf 'generation_2_baseline_records=%s\n' "$base2"
    printf 'generation_1_postlogin_records=%s\n' "$records1"
    printf 'generation_2_postlogin_records=%s\n' "$records2"
    printf 'read_gate_candidate=R3_RESTART_STABLE_READ\n'
    printf 'bridge_read_gate=NOT_PROVEN\n'
    printf 'action_gate_a3=NOT_PROVEN\n'
    printf 'action_gate_a4=NOT_PROVEN\n'
    printf 'gameplay_actions_performed=0\n'
    printf 'side_effects=login_relogin_and_clean_process_restart_only\n'
  } >"$out"
  printf 'TRACK_A_RESTART_RELOGIN_REACQUISITION_PROVEN=true pid1=%s pid2=%s pie1=%s pie2=%s\n' \
    "$pid1" "$pid2" "$pie1" "$pie2"
}

cleanup_role() {
  local role="$1" expected="${2:-}" pid
  pid="$(read_pid "$role" 2>/dev/null || true)"
  [[ -n "$pid" ]] || return 0
  kill -0 "$pid" 2>/dev/null || return 0
  role_exe_matches "$pid" "$role" "$expected" || die "refuse_foreign_cleanup_${role}"
  kill -TERM "$pid" 2>/dev/null || true
  for _ in $(seq 1 40); do kill -0 "$pid" 2>/dev/null || break; sleep .1; done
  kill -0 "$pid" 2>/dev/null && die "cleanup_timeout_${role}"
}

cleanup_all() {
  require_context
  stop_generation 1 || true
  stop_generation 2 || true
  local td private_xvfb
  td="$(toolroot)"
  private_xvfb="$BASE_STATE/runtime/Xvfb-track-a"
  [[ -x "$private_xvfb" ]] || private_xvfb="$td/usr/bin/Xvfb"
  cleanup_role xvfb "$private_xvfb"
  cleanup_role socks-relay "$(command -v python3)"
  printf 'TRACK_A_TASK_PROCESS_CLEANUP_COMPLETE=true\n'
  if [[ -e "/tmp/.X${DISPLAY_NUM}-lock" || -e "/tmp/.X11-unix/X${DISPLAY_NUM}" ]]; then
    printf 'TRACK_A_TASK_X11_RESIDUE_PRESENT=true\n'
    # Never remove X11 residue here: ownership is not inferable from a path alone after the process exits.
  else
    printf 'TRACK_A_TASK_X11_RESIDUE_PRESENT=false\n'
  fi
  local root
  root="$(run_root)"
  [[ -r "$root/task-id" && "$(cat "$root/task-id")" == "$TASK_ID" ]] || die 'refuse_unmarked_run_root_cleanup'
  case "$root" in
    "$TASK_ROOT"/runs/"$GITHUB_RUN_ID")
      rm -rf --one-file-system "$root"
      printf 'TRACK_A_TASK_EPHEMERAL_STATE_REMOVED=true\n'
      ;;
    *)
      die 'refuse_out_of_namespace_run_root_cleanup'
      ;;
  esac
}

case "${1:-}" in
  bootstrap)
    bootstrap
    ;;
  prepare)
    prepare_generation "${2:?generation}"
    ;;
  login)
    login_generation "${2:?generation}"
    ;;
  verify)
    verify_generation "${2:?generation}"
    ;;
  stop)
    stop_generation "${2:?generation}"
    ;;
  compare)
    compare_generations
    ;;
  cleanup)
    cleanup_all
    ;;
  *)
    die 'usage_bootstrap_prepare_login_verify_stop_compare_cleanup'
    ;;
esac
