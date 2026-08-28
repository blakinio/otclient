#!/usr/bin/env bash
set +x
set -Eeuo pipefail
umask 077

TASK_ID='OTC-20260828-current-login-field6-runtime'
TRACK_ID='official-client-re'
EXPECTED_CLIENT_SIZE='52105824'
EXPECTED_CLIENT_SHA256='d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
WGCF_VER='2.2.32'
WGCF_SHA='2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c'
WIREPROXY_VER='1.1.3'
WIREPROXY_TAR_SHA='e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c'
WARP_PORT='25442'
FILE_WORKERS='8'
BASE='/home/runner/_work/_otclient_tibia_re_state'
TASK_BASE="$BASE/tasks/$TASK_ID"
RUN_ID="${GITHUB_RUN_ID:-manual-unknown}"
ROOT="$TASK_BASE/package-acquisition/$RUN_ID"
WARP="$ROOT/warp"
SOURCE="$ROOT/current-package"
MATERIALIZER="${BASH_SOURCE[0]%/*}/track_a_current_client_package_materialize.py"
WIRE_PID_FILE="$ROOT/wireproxy.pid"
WIRE_PID=''
WIRE_BIN="$WARP/bin/wireproxy"

fail() { printf 'TRACK_A_FIELD6_PACKAGE_ERROR=%s\n' "$1" >&2; exit 1; }

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

read_wire_pid() {
  local pid=''
  if [[ "${WIRE_PID:-}" =~ ^[1-9][0-9]*$ ]]; then
    pid="$WIRE_PID"
  elif [[ -r "$WIRE_PID_FILE" && ! -L "$WIRE_PID_FILE" ]]; then
    pid="$(cat "$WIRE_PID_FILE")"
  fi
  [[ "$pid" =~ ^[1-9][0-9]*$ ]] || return 1
  printf '%s\n' "$pid"
}

process_is_zombie() {
  local pid="$1" state=''
  [[ "$pid" =~ ^[1-9][0-9]*$ && -r "/proc/$pid/stat" ]] || return 1
  state="$(awk '{print $3}' "/proc/$pid/stat" 2>/dev/null || true)"
  [[ "$state" == 'Z' ]]
}

wire_owned() {
  local pid="$1"
  [[ "$pid" =~ ^[1-9][0-9]*$ && -x "$WIRE_BIN" && ! -L "$WIRE_BIN" && -r "/proc/$pid/environ" ]] || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_TRACK=$TRACK_ID" "/proc/$pid/environ" || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_TASK=$TASK_ID" "/proc/$pid/environ" || return 1
  grep -azFxq "OTCLIENT_TIBIA_RE_RUN_ID=$RUN_ID" "/proc/$pid/environ" || return 1
  grep -azFxq 'OTCLIENT_TIBIA_RE_ROLE=package-wireproxy' "/proc/$pid/environ" || return 1
  [[ "$(readlink -f "/proc/$pid/exe")" == "$(readlink -f "$WIRE_BIN")" ]]
}

stop_warp() {
  local pid=''
  pid="$(read_wire_pid 2>/dev/null || true)"
  if [[ -z "$pid" ]]; then
    [[ ! -e "$WIRE_PID_FILE" && ! -L "$WIRE_PID_FILE" ]] || return 1
    listen "$WARP_PORT" && return 1 || true
    return 0
  fi

  if [[ -e "/proc/$pid" ]]; then
    if process_is_zombie "$pid"; then
      wait "$pid" 2>/dev/null || true
    else
      wire_owned "$pid" || return 1
      kill -TERM "$pid" 2>/dev/null || true
      for _ in $(seq 1 40); do
        [[ ! -e "/proc/$pid" ]] && break
        if process_is_zombie "$pid"; then
          wait "$pid" 2>/dev/null || true
          break
        fi
        sleep .1
      done
      if [[ -e "/proc/$pid" ]] && ! process_is_zombie "$pid"; then
        wire_owned "$pid" || return 1
        kill -KILL "$pid" 2>/dev/null || true
        for _ in $(seq 1 20); do
          [[ ! -e "/proc/$pid" ]] && break
          if process_is_zombie "$pid"; then
            wait "$pid" 2>/dev/null || true
            break
          fi
          sleep .1
        done
      fi
      if [[ -e "/proc/$pid" ]] && process_is_zombie "$pid"; then
        wait "$pid" 2>/dev/null || true
      fi
      if [[ -e "/proc/$pid" ]] && ! process_is_zombie "$pid"; then
        return 1
      fi
    fi
  fi

  rm -f "$WIRE_PID_FILE"
  WIRE_PID=''
  listen "$WARP_PORT" && return 1 || true
}

rollback_prepare() {
  local rc=$? cleanup_ok=1
  trap - EXIT
  set +e
  stop_warp || cleanup_ok=0
  if [[ "$cleanup_ok" == 1 ]]; then
    if [[ -d "$ROOT" && ! -L "$ROOT" ]]; then
      rm -rf --one-file-system "$ROOT"
    fi
  else
    printf 'TRACK_A_FIELD6_PACKAGE_ERROR=rollback_ownership_refused\n' >&2
    exit 98
  fi
  exit "$rc"
}

prepare_warp() {
  local bin="$WARP/bin" archive extracted state ready=false
  listen "$WARP_PORT" && fail warp_port_collision || true
  mkdir -p "$bin"
  chmod 700 "$WARP" "$bin"

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
  install -m755 "$extracted" "$WIRE_BIN"
  rm -rf --one-file-system "$bin/unpack"

  for attempt in 1 2; do
    state="$WARP/state-$attempt"
    mkdir -p "$state"
    chmod 700 "$state"
    (
      cd "$state"
      "$bin/wgcf" register --accept-tos >/dev/null 2>&1 || exit 10
      chmod 600 wgcf-account.toml
      "$bin/wgcf" generate >/dev/null 2>&1 || exit 11
      chmod 600 wgcf-profile.conf
    ) || continue
    cat >"$state/wireproxy.conf" <<EOF
WGConfig = $state/wgcf-profile.conf
[Socks5]
BindAddress = 127.0.0.1:$WARP_PORT
EOF
    chmod 600 "$state/wireproxy.conf"
    env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
      OTCLIENT_TIBIA_RE_TRACK="$TRACK_ID" OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
      OTCLIENT_TIBIA_RE_RUN_ID="$RUN_ID" OTCLIENT_TIBIA_RE_ROLE=package-wireproxy \
      nohup "$WIRE_BIN" -c "$state/wireproxy.conf" \
      >"$state/wireproxy.log" 2>&1 </dev/null &
    WIRE_PID=$!
    printf '%s\n' "$WIRE_PID" >"$WIRE_PID_FILE"
    chmod 600 "$WIRE_PID_FILE"
    ready=false
    for _ in $(seq 1 30); do
      if curl --socks5-hostname "127.0.0.1:$WARP_PORT" -fsS --max-time 4 \
        https://www.cloudflare.com/cdn-cgi/trace 2>/dev/null | grep -Eq '^warp=(on|plus)$'; then
        ready=true
        break
      fi
      kill -0 "$WIRE_PID" 2>/dev/null || break
      sleep 1
    done
    if [[ "$ready" == true ]]; then
      wire_owned "$WIRE_PID" || fail warp_ownership_failed
      printf 'TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=%s\n' "$attempt"
      return 0
    fi
    stop_warp || fail warp_cleanup_failed
  done
  fail warp_egress_not_verified
}

prepare() {
  [[ "${GITHUB_REPOSITORY:-}" == 'blakinio/otclient' ]] || fail wrong_repository
  [[ "${RUNNER_NAME:-}" == 'synology-otclient-01' ]] || fail wrong_runner
  [[ "$RUN_ID" =~ ^[1-9][0-9]*$ ]] || fail invalid_run_id
  [[ -f "$MATERIALIZER" && ! -L "$MATERIALIZER" ]] || fail materializer_missing_or_symlink
  [[ ! -e "$ROOT" && ! -L "$ROOT" ]] || fail acquisition_root_collision
  if env | grep -Eq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD)='; then
    fail secret_environment_present_during_package_preflight
  fi

  mkdir -p "$ROOT"
  chmod 700 "$TASK_BASE" "$TASK_BASE/package-acquisition" "$ROOT" 2>/dev/null || true
  trap rollback_prepare EXIT

  prepare_warp
  python3 "$MATERIALIZER" \
    --manifest-url 'https://static.tibia.com/launcher/tibiaclient-linux-current/package.json' \
    --base-url 'https://static.tibia.com/launcher/tibiaclient-linux-current' \
    --socks-port "$WARP_PORT" \
    --file-workers "$FILE_WORKERS" \
    --output "$SOURCE"

  [[ -x "$SOURCE/bin/client" && ! -L "$SOURCE/bin/client" ]] || fail materialized_client_invalid
  [[ "$(stat -Lc %s "$SOURCE/bin/client")" == "$EXPECTED_CLIENT_SIZE" ]] || fail materialized_client_size_mismatch
  [[ "$(sha256sum "$SOURCE/bin/client" | awk '{print $1}')" == "$EXPECTED_CLIENT_SHA256" ]] || fail materialized_client_hash_mismatch

  stop_warp || fail warp_cleanup_failed

  trap - EXIT
  printf 'TRACK_A_FIELD6_EXACT_PACKAGE_SOURCE=materialized\n'
  printf 'TRACK_A_FIELD6_PACKAGE_EXECUTED=false\n'
  printf 'TRACK_A_FIELD6_PACKAGE_PREFLIGHT=PASS\n'
}

cleanup() {
  [[ "$RUN_ID" =~ ^[1-9][0-9]*$ ]] || fail invalid_run_id
  stop_warp || fail cleanup_warp_ownership_refused
  if [[ -d "$ROOT" && ! -L "$ROOT" ]]; then
    rm -rf --one-file-system "$ROOT"
  elif [[ -e "$ROOT" || -L "$ROOT" ]]; then
    fail cleanup_root_ownership_refused
  fi
  printf 'TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS\n'
}

case "${1:-}" in
  prepare) [[ $# == 1 ]] || fail usage; prepare ;;
  cleanup) [[ $# == 1 ]] || fail usage; cleanup ;;
  *) fail usage ;;
esac
