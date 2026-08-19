#!/usr/bin/env bash
set +x
set -Eeuo pipefail
umask 077

BASE=/home/runner/_work/_otclient_tibia_re_state
ROOT="$BASE/canonical-live-runtime"
SESSION="$ROOT/session"
WARP="$ROOT/warp"
TOOL=''
TOOLROOT_HOME="$BASE/toolroot"
TOOLROOT_WORK=/work/_otclient_tibia_re_state/toolroot
SIZE=52109920
SHA=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
MARK='OTCLIENT_TIBIA_RE_TRACK=official-client-re'
RMARK='OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1'
WGCF_VER=2.2.32
WGCF_SHA=2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c
WP_VER=1.1.3
WP_TAR_SHA=e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c

die() { printf 'TRACK_A_CANONICAL_SESSION_ERROR=%s\n' "$1" >&2; exit 1; }
rpid() { [[ -r "$SESSION/$1.pid" ]] || return 0; tr -cd '0-9' <"$SESSION/$1.pid" 2>/dev/null || true; }
pgrp() { ps -o pgid= -p "$1" 2>/dev/null | tr -d ' '; }

listen() {
  python3 - "$1" <<'PY'
import pathlib, sys
port = f'{int(sys.argv[1]):04X}'
for name in ('tcp', 'tcp6'):
    path = pathlib.Path('/proc/net') / name
    if not path.exists():
        continue
    for row in path.read_text().splitlines()[1:]:
        fields = row.split()
        if len(fields) > 3 and fields[1].rsplit(':', 1)[-1].upper() == port and fields[3] == '0A':
            raise SystemExit(0)
raise SystemExit(1)
PY
}

owned() {
  local pid="$1" role="$2" executable="${3:-}"
  [[ "$pid" =~ ^[1-9][0-9]*$ && -r /proc/$pid/environ ]] || return 1
  grep -azFxq "$MARK" /proc/$pid/environ || return 1
  grep -azFxq "$RMARK" /proc/$pid/environ || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_ROLE=$role" /proc/$pid/environ || return 1
  [[ -z "$executable" || "$(readlink -f /proc/$pid/exe)" == "$(readlink -f "$executable")" ]]
}

nosecret() {
  ! grep -azEq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD|TRACK_A_CANONICAL_LEASE_TOKEN|TRACK_A_CANONICAL_LEASE_TOKEN_FILE)=' "/proc/$1/environ" || die "$2_secret_env_leak"
}

verify_client() {
  [[ -x "$1" && ! -L "$1" ]] || die client_not_executable
  [[ "$(stat -c %s "$1")" == "$SIZE" ]] || die client_size_mismatch
  [[ "$(sha256sum "$1" | awk '{print $1}')" == "$SHA" ]] || die client_sha_mismatch
}

within_toolroot() {
  local root_real="$1" path="$2" resolved
  resolved="$(realpath -e -- "$path" 2>/dev/null)" || return 1
  case "$resolved" in
    "$root_real"/*) printf '%s\n' "$resolved" ;;
    *) return 1 ;;
  esac
}

contained_dri_root() {
  local root="$1" root_real dri dri_real swrast swrast_real
  [[ -n "$root" && -d "$root" && ! -L "$root" ]] || return 1
  root_real="$(realpath -e -- "$root" 2>/dev/null)" || return 1
  dri="$root/usr/lib/x86_64-linux-gnu/dri"
  [[ -d "$dri" && ! -L "$dri" ]] || return 1
  dri_real="$(within_toolroot "$root_real" "$dri")" || return 1
  swrast="$dri/swrast_dri.so"
  [[ -e "$swrast" ]] || return 1
  swrast_real="$(within_toolroot "$root_real" "$swrast")" || return 1
  case "$swrast_real" in
    "$dri_real"/*) ;;
    *) return 1 ;;
  esac
  [[ -f "$swrast_real" ]] || return 1
  printf '%s\n' "$dri_real"
}

toolroot_complete() {
  local root="$1" root_real name path xkb_real preload preload_real
  [[ -n "$root" && -d "$root" && ! -L "$root" ]] || return 1
  root_real="$(realpath -e -- "$root" 2>/dev/null)" || return 1
  for name in Xvfb x11vnc xdotool; do
    path="$root/usr/bin/$name"
    [[ -x "$path" && ! -L "$path" ]] || return 1
    within_toolroot "$root_real" "$path" >/dev/null || return 1
  done
  xkb_real="$(within_toolroot "$root_real" "$root/usr/share/X11/xkb")" || return 1
  [[ -d "$xkb_real" ]] || return 1
  contained_dri_root "$root" >/dev/null || return 1
  preload="$(find "$root" -xdev -type f -name libproxychains.so.4 -print -quit 2>/dev/null || true)"
  [[ -n "$preload" ]] || return 1
  preload_real="$(within_toolroot "$root_real" "$preload")" || return 1
  [[ -f "$preload_real" ]]
}

toolroot_candidates() {
  local raw item
  if [[ "${TRACK_A_CANONICAL_WORKER_CONTRACT_TEST:-}" == 1 \
    && -n "${TRACK_A_CANONICAL_TOOLROOT_TEST_CANDIDATES:-}" ]]; then
    raw="$TRACK_A_CANONICAL_TOOLROOT_TEST_CANDIDATES"
    while [[ -n "$raw" ]]; do
      if [[ "$raw" == *';'* ]]; then
        item="${raw%%;*}"
        raw="${raw#*;}"
      else
        item="$raw"
        raw=''
      fi
      [[ -n "$item" ]] && printf '%s\n' "$item"
    done
    return
  fi
  printf '%s\n' "$TOOLROOT_HOME" "$TOOLROOT_WORK"
}

resolve_toolroot() {
  local candidate
  while IFS= read -r candidate; do
    if toolroot_complete "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(toolroot_candidates)
  return 1
}

tool() {
  local root_real path resolved
  root_real="$(realpath -e -- "$TOOL" 2>/dev/null)" || return 1
  path="$TOOL/usr/bin/$1"
  [[ -x "$path" && ! -L "$path" ]] || return 1
  resolved="$(within_toolroot "$root_real" "$path")" || return 1
  printf '%s\n' "$resolved"
}

free_display() {
  local number
  for number in $(seq 98 130); do
    if [[ ! -e /tmp/.X$number-lock && ! -e /tmp/.X11-unix/X$number ]]; then
      echo "$number"
      return
    fi
  done
  return 1
}

free_port() {
  local port
  for port in $(seq "$1" "$2"); do
    if ! listen "$port"; then
      echo "$port"
      return
    fi
  done
  return 1
}

source_pkg() {
  local package client
  for package in \
    "$BASE/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia" \
    "/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"; do
    client="$package/bin/client"
    if [[ -x "$client" && ! -L "$client" \
      && "$(stat -c %s "$client" 2>/dev/null || true)" == "$SIZE" \
      && "$(sha256sum "$client" 2>/dev/null | awk '{print $1}')" == "$SHA" ]]; then
      echo "$package"
      return
    fi
  done
  return 1
}

window() {
  local pid="$1" display="$2" xdotool="$3" attempts="$4" delay="$5"
  local win geometry candidate_area best='' best_area=0 width height
  [[ "$attempts" =~ ^[1-9][0-9]*$ ]] || return 3
  for _ in $(seq 1 "$attempts"); do
    kill -0 "$pid" 2>/dev/null || return 2
    best=''
    best_area=0
    for win in $(DISPLAY="$display" "$xdotool" search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null || true); do
      geometry="$(DISPLAY="$display" "$xdotool" getwindowgeometry --shell "$win" 2>/dev/null || true)"
      width="$(sed -n 's/^WIDTH=//p' <<<"$geometry")"
      height="$(sed -n 's/^HEIGHT=//p' <<<"$geometry")"
      [[ "$width" =~ ^[0-9]+$ && "$height" =~ ^[0-9]+$ ]] || continue
      candidate_area=$((width * height))
      if ((candidate_area > best_area)); then
        best="$win"
        best_area=$candidate_area
      fi
    done
    if [[ -n "$best" ]]; then
      echo "$best"
      return 0
    fi
    sleep "$delay"
  done
  kill -0 "$pid" 2>/dev/null || return 2
  return 1
}

wait_for_window() {
  local pid="$1" display="$2" xdotool="$3" attempts="$4" delay="$5" win rc=0
  win="$(window "$pid" "$display" "$xdotool" "$attempts" "$delay")" || rc=$?
  case "$rc" in
    0) printf '%s\n' "$win" ;;
    1) die client_window_missing ;;
    2) die client_exited ;;
    *) die client_window_probe_failed ;;
  esac
}

contract_test() {
  [[ "${TRACK_A_CANONICAL_WORKER_CONTRACT_TEST:-}" == 1 ]] || return 1
  case "${1:-}" in
    bootstrap)
      [[ $# == 2 ]] || die usage
      python3 - "$2" <<'PY'
import json, os, sys
pid = os.getpid()
json.dump({
    'pid': pid,
    'process_group_id': os.getpgrp(),
    'tracked_processes': {'client': pid, 'xvfb': pid + 1, 'vnc': pid + 2, 'wireproxy': pid + 3},
    'display': ':199', 'window_identity': 'test',
    'remote_view_endpoint': '127.0.0.1:6199', 'remote_view_mapping': 'UNKNOWN', 'state': 'UNKNOWN'
}, open(sys.argv[1], 'w'))
PY
      ;;
    probe)
      [[ $# == 2 ]] || die usage
      python3 - "$2" <<'PY'
import json, os, sys
pid = os.getpid()
json.dump({
    'pid': pid,
    'process_group_id': os.getpgrp(),
    'tracked_processes': {'client': pid, 'xvfb': pid + 1, 'vnc': pid + 2, 'wireproxy': pid + 3},
    'display': ':199', 'window_identity': 'test',
    'remote_view_endpoint': '127.0.0.1:6199', 'remote_view_mapping': 'UNKNOWN', 'state': 'UNKNOWN'
}, open(sys.argv[1], 'w'))
PY
      ;;
    rollback)
      [[ $# == 2 ]] || die usage
      ;;
    toolroot)
      [[ $# == 1 ]] || die usage
      resolve_toolroot || die toolroot_unavailable
      ;;
    window)
      [[ $# == 6 ]] || die usage
      wait_for_window "$2" "$3" "$4" "$5" "$6"
      ;;
    *) die usage ;;
  esac
  exit 0
}

warp_tools() {
  local bin="$WARP/bin" archive extracted
  mkdir -p "$bin" "$WARP/state"
  chmod 700 "$WARP" "$WARP/state"
  if [[ ! -x "$bin/wgcf" || "$(sha256sum "$bin/wgcf" 2>/dev/null | awk '{print $1}')" != "$WGCF_SHA" ]]; then
    archive="$bin/.wgcf"
    curl -fL --retry 3 --connect-timeout 10 -o "$archive" \
      "https://github.com/ViRb3/wgcf/releases/download/v$WGCF_VER/wgcf_${WGCF_VER}_linux_amd64"
    [[ "$(sha256sum "$archive" | awk '{print $1}')" == "$WGCF_SHA" ]] || die wgcf_hash_mismatch
    chmod 755 "$archive"
    mv -f "$archive" "$bin/wgcf"
  fi
  archive="$bin/wireproxy.tar.gz"
  if [[ ! -s "$archive" || "$(sha256sum "$archive" 2>/dev/null | awk '{print $1}')" != "$WP_TAR_SHA" ]]; then
    curl -fL --retry 3 --connect-timeout 10 -o "$archive.tmp" \
      "https://github.com/windtf/wireproxy/releases/download/v$WP_VER/wireproxy_linux_amd64.tar.gz"
    [[ "$(sha256sum "$archive.tmp" | awk '{print $1}')" == "$WP_TAR_SHA" ]] || die wireproxy_archive_hash_mismatch
    mv -f "$archive.tmp" "$archive"
  fi
  rm -rf "$bin/.wpx"
  mkdir "$bin/.wpx"
  tar -xzf "$archive" -C "$bin/.wpx"
  extracted="$(find "$bin/.wpx" -type f -name wireproxy -print -quit)"
  [[ -n "$extracted" ]] || die wireproxy_binary_missing
  install -m755 "$extracted" "$bin/wireproxy"
  rm -rf "$bin/.wpx"
}

start_warp() {
  local bin="$WARP/bin" state="$WARP/state" port pid
  warp_tools
  cd "$state"
  if [[ ! -s wgcf-account.toml ]]; then
    "$bin/wgcf" register --accept-tos >/dev/null
  fi
  chmod 600 wgcf-account.toml
  "$bin/wgcf" generate >/dev/null
  chmod 600 wgcf-profile.conf
  port="$(free_port 25354 25420)" || die no_free_warp_port
  cat >"$SESSION/wireproxy.conf" <<EOF
WGConfig = $state/wgcf-profile.conf
[Socks5]
BindAddress = 127.0.0.1:$port
EOF
  chmod 600 "$SESSION/wireproxy.conf"
  printf 'TRACK_A_CANONICAL_STAGE=wireproxy_configtest_start\n'
  "$bin/wireproxy" -n -c "$SESSION/wireproxy.conf" >/dev/null
  printf 'TRACK_A_CANONICAL_STAGE=wireproxy_configtest_pass\n'
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re \
    OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=wireproxy \
    nohup "$bin/wireproxy" -c "$SESSION/wireproxy.conf" \
    >"$SESSION/wireproxy.log" 2>&1 </dev/null &
  pid=$!
  echo "$pid" >"$SESSION/wireproxy.pid"
  echo "$port" >"$SESSION/warp-port"
  echo "$bin/wireproxy" >"$SESSION/wireproxy-bin"
  for _ in $(seq 1 40); do
    kill -0 "$pid" 2>/dev/null || die wireproxy_exited
    listen "$port" && break
    sleep .25
  done
  owned "$pid" wireproxy "$bin/wireproxy" || die wireproxy_ownership_failed
  nosecret "$pid" wireproxy
  listen "$port" || die wireproxy_not_listening
  printf 'TRACK_A_CANONICAL_STAGE=warp_egress_probe_start\n'
  curl --socks5-hostname "127.0.0.1:$port" -fsS --max-time 15 \
    https://www.cloudflare.com/cdn-cgi/trace | grep -Eq '^warp=(on|plus)$' || die warp_egress_not_verified
  printf 'TRACK_A_CANONICAL_STAGE=warp_egress_probe_pass\n'
}

write_manifest() {
  local output="$1" client_pid="$2" pgid="$3" display="$4" window_id="$5" vnc_port="$6"
  local xvfb_pid vnc_pid wireproxy_pid
  xvfb_pid="$(rpid xvfb)"
  vnc_pid="$(rpid vnc)"
  wireproxy_pid="$(rpid wireproxy)"
  python3 - "$output" "$client_pid" "$pgid" "$display" "$window_id" "$vnc_port" "$xvfb_pid" "$vnc_pid" "$wireproxy_pid" <<'PY'
import json, sys
output, client, pgid, display, window, vnc, xvfb, vnc_pid, wireproxy = sys.argv[1:]
json.dump({
    'pid': int(client),
    'process_group_id': int(pgid),
    'tracked_processes': {
        'client': int(client), 'xvfb': int(xvfb), 'vnc': int(vnc_pid), 'wireproxy': int(wireproxy)
    },
    'display': display,
    'window_identity': 'x11-window:' + window,
    'remote_view_endpoint': '127.0.0.1:' + vnc,
    'remote_view_mapping': 'PROVEN',
    'state': 'UNKNOWN',
}, open(output, 'w'))
PY
}

verify_tracked_group() {
  local pgid="$1" role pid executable
  for role in client xvfb vnc wireproxy; do
    pid="$(rpid "$role")"
    executable=''
    [[ "$role" != wireproxy ]] || executable="$(cat "$SESSION/wireproxy-bin")"
    owned "$pid" "$role" "$executable" || die "${role}_ownership_failed"
    kill -0 "$pid" || die "${role}_dead"
    nosecret "$pid" "$role"
    [[ "$(pgrp "$pid")" == "$pgid" ]] || die "${role}_wrong_process_group"
  done
}

bootstrap() {
  local manifest="$1" source home package display display_number vnc_port xvfb vnc xdotool preload client pid win pgid metadata warp_port dri
  [[ "${RUNNER_NAME:-}" == synology-otclient-01 ]] || die wrong_runner
  [[ "${GITHUB_REPOSITORY:-}" == blakinio/otclient ]] || die wrong_repository
  [[ ! -e "$SESSION" ]] || die session_root_exists
  pgid="$(pgrp $$)"
  [[ "$pgid" == "$$" ]] || die bootstrap_not_group_leader
  source="$(source_pkg)" || die exact_source_missing
  mkdir -p "$SESSION"
  chmod 700 "$SESSION"
  echo "$pgid" >"$SESSION/bootstrap-pgid"
  TOOL="$(resolve_toolroot)" || die toolroot_unavailable
  dri="$(contained_dri_root "$TOOL")" || die dri_provider_unavailable
  printf '%s\n' "$TOOL" >"$SESSION/toolroot"
  printf 'TRACK_A_CANONICAL_TOOLROOT=%s\n' "$TOOL"

  printf 'TRACK_A_CANONICAL_STAGE=warp_start\n'
  start_warp
  printf 'TRACK_A_CANONICAL_STAGE=warp_pass\n'
  warp_port="$(cat "$SESSION/warp-port")"
  xvfb="$(tool Xvfb)" || die xvfb_unavailable
  vnc="$(tool x11vnc)" || die vnc_unavailable
  xdotool="$(tool xdotool)" || die xdotool_unavailable
  preload="$(find "$TOOL" -xdev -type f -name libproxychains.so.4 -print -quit 2>/dev/null || true)"
  [[ -n "$preload" ]] || die proxychains_unavailable
  display_number="$(free_display)" || die no_free_display
  display=":$display_number"
  vnc_port="$(free_port 6082 6120)" || die no_free_vnc_port
  home="$SESSION/home"
  package="$home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"
  mkdir -p "$(dirname "$package")"
  cp -a --reflink=auto "$source" "$package"
  client="$package/bin/client"
  verify_client "$client"
  metadata="$(dirname "$source")/../../launchermetadata.json"
  [[ ! -f "$metadata" || -L "$metadata" ]] || install -m600 "$metadata" "$(dirname "$(dirname "$package")")/launchermetadata.json"

  cat >"$SESSION/proxychains.conf" <<EOF
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 $warp_port
EOF
  chmod 600 "$SESSION/proxychains.conf"

  printf 'TRACK_A_CANONICAL_STAGE=xvfb_start\n'
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 \
    OTCLIENT_TIBIA_RE_ROLE=xvfb HOME="$home" PATH="$TOOL/usr/bin:$TOOL/usr/sbin:/usr/bin:/bin" \
    LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu" \
    LIBGL_DRIVERS_PATH="$dri" XKB_CONFIG_ROOT="$TOOL/usr/share/X11/xkb" \
    nohup "$xvfb" "$display" -screen 0 1920x1080x24 -xkbdir "$TOOL/usr/share/X11/xkb" \
    -nolisten tcp -noreset >"$SESSION/xvfb.log" 2>&1 </dev/null &
  echo $! >"$SESSION/xvfb.pid"
  for _ in $(seq 1 60); do
    [[ -e /tmp/.X11-unix/X$display_number ]] && break
    sleep .2
  done
  [[ -e /tmp/.X11-unix/X$display_number ]] || die xvfb_socket_missing
  printf 'TRACK_A_CANONICAL_STAGE=xvfb_pass\n'

  printf 'TRACK_A_CANONICAL_STAGE=vnc_start\n'
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 \
    OTCLIENT_TIBIA_RE_ROLE=vnc HOME="$home" DISPLAY="$display" \
    nohup "$vnc" -display "$display" -rfbport "$vnc_port" -forever -shared -viewonly \
    -localhost -nopw -noxdamage >"$SESSION/vnc.log" 2>&1 </dev/null &
  echo $! >"$SESSION/vnc.pid"
  for _ in $(seq 1 60); do
    listen "$vnc_port" && break
    sleep .2
  done
  listen "$vnc_port" || die vnc_not_listening
  printf 'TRACK_A_CANONICAL_STAGE=vnc_pass\n'

  printf 'TRACK_A_CANONICAL_STAGE=client_start\n'
  (
    cd "$package"
    env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
      OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 \
      OTCLIENT_TIBIA_RE_ROLE=client HOME="$home" DISPLAY="$display" \
      PATH="$TOOL/usr/bin:$TOOL/usr/sbin:/usr/bin:/bin" \
      LD_LIBRARY_PATH="$package/bin/lib:$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/usr/lib/x86_64-linux-gnu/libproxy:$TOOL/lib/x86_64-linux-gnu" \
      QT_QUICK_BACKEND=software QSG_INFO=1 \
      XDG_DATA_DIRS="$TOOL/usr/share:/usr/share" FONTCONFIG_PATH="$TOOL/etc/fonts" \
      FONTCONFIG_FILE="$TOOL/etc/fonts/fonts.conf" LD_PRELOAD="$preload" \
      PROXYCHAINS_CONF_FILE="$SESSION/proxychains.conf" \
      nohup "$client" >"$SESSION/client.log" 2>&1 </dev/null &
    echo $! >"$SESSION/client.pid"
  )

  pid="$(rpid client)"
  printf 'TRACK_A_CANONICAL_STAGE=client_window_wait_start\n'
  win="$(wait_for_window "$pid" "$display" "$xdotool" 120 .25)"
  printf 'TRACK_A_CANONICAL_STAGE=client_window_wait_pass\n'
  verify_client "$client"
  echo "$display" >"$SESSION/display"
  echo "$win" >"$SESSION/window"
  echo "$vnc_port" >"$SESSION/vnc-port"
  verify_tracked_group "$pgid"
  write_manifest "$manifest" "$pid" "$pgid" "$display" "$win" "$vnc_port"
}

probe() {
  local manifest="$1" pid display win vnc_port client xdotool pgid persisted_toolroot
  [[ -d "$SESSION" ]] || die session_missing
  persisted_toolroot="$(cat "$SESSION/toolroot" 2>/dev/null || true)"
  toolroot_complete "$persisted_toolroot" || die toolroot_unavailable
  TOOL="$persisted_toolroot"
  pgid="$(cat "$SESSION/bootstrap-pgid")"
  pid="$(rpid client)"
  display="$(cat "$SESSION/display")"
  vnc_port="$(cat "$SESSION/vnc-port")"
  client="$SESSION/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client"
  verify_client "$client"
  verify_tracked_group "$pgid"
  listen "$vnc_port" || die vnc_not_listening
  listen "$(cat "$SESSION/warp-port")" || die wireproxy_not_listening
  xdotool="$(tool xdotool)" || die xdotool_unavailable
  win="$(wait_for_window "$pid" "$display" "$xdotool" 120 .25)"
  echo "$win" >"$SESSION/window"
  write_manifest "$manifest" "$pid" "$pgid" "$display" "$win" "$vnc_port"
}

rollback() {
  local pgid="$1" role pid display_number
  [[ -d "$SESSION" ]] || return 0
  [[ "$(cat "$SESSION/bootstrap-pgid" 2>/dev/null || true)" == "$pgid" ]] || die rollback_pgid_mismatch
  for role in client xvfb vnc wireproxy; do
    pid="$(rpid "$role")"
    [[ -z "$pid" || ! -e /proc/$pid ]] || die rollback_role_still_alive
  done
  display_number="$(sed 's/^://' "$SESSION/display" 2>/dev/null || true)"
  if [[ -n "$display_number" && -e /tmp/.X$display_number-lock ]]; then
    pid="$(tr -cd '0-9' </tmp/.X$display_number-lock 2>/dev/null || true)"
    [[ -z "$pid" || ! -e /proc/$pid ]] || die rollback_x11_owner_alive
    rm -f "/tmp/.X$display_number-lock" "/tmp/.X11-unix/X$display_number"
  elif [[ -n "$display_number" && -e /tmp/.X11-unix/X$display_number ]]; then
    die rollback_x11_ambiguous
  fi
  rm -rf --one-file-system "$SESSION"
}

contract_test "$@" || true
case "${1:-}" in
  bootstrap) [[ $# == 2 ]] || die usage; bootstrap "$2" ;;
  probe) [[ $# == 2 ]] || die usage; probe "$2" ;;
  rollback) [[ $# == 2 ]] || die usage; rollback "$2" ;;
  *) die usage ;;
esac
