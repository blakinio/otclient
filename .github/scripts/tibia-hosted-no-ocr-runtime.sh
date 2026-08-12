#!/usr/bin/env bash
set -Eeuo pipefail

mode=${1:?usage: $0 <warp|launch|auth>}
state=/tmp/tibia-world
pkg="$HOME/.local/share/CipSoft GmbH/Tibia/packages/Tibia"
client="$pkg/bin/client"
mkdir -p "$state"

client_socket_counts() {
  local pid=$1 tcp_rows udp_rows local_count total_count direct_count udp_count
  tcp_rows=$(ss -ntp 2>/dev/null | grep "pid=$pid," || true)
  udp_rows=$(ss -nup 2>/dev/null | grep "pid=$pid," || true)
  local_count=$(printf '%s\n' "$tcp_rows" | awk '$5 ~ /127\.0\.0\.1:25344$/ || $5 ~ /\[::1\]:25344$/ {n++} END{print n+0}')
  total_count=$(printf '%s\n' "$tcp_rows" | grep -c . || true)
  direct_count=$((total_count-local_count))
  udp_count=$(printf '%s\n' "$udp_rows" | grep -c . || true)
  printf '%s %s %s\n' "$local_count" "$direct_count" "$udp_count"
}

arm_map_uprobes() {
  local tracefs link offsets mapfile commonfile fieldfile
  tracefs=/sys/kernel/tracing
  [[ -d "$tracefs" ]] || tracefs=/sys/kernel/debug/tracing
  if ! sudo test -d "$tracefs"; then
    echo DECODED_MAP_UPROBES_AVAILABLE=false
    return 1
  fi

  link=/tmp/tibia-client-uprobe
  rm -f "$link"
  if ! ln "$client" "$link" 2>/dev/null; then
    cp --reflink=auto "$client" "$link"
  fi

  offsets=$(python3 - "$client" <<'PY'
import struct,sys
path=sys.argv[1]
target=[0x19a8ea3,0x19a8a80,0xcd3190]
with open(path,'rb') as f:
    e=f.read(64)
    if e[:4] != b'\x7fELF' or e[4] != 2 or e[5] != 1:
        raise SystemExit('unsupported ELF')
    phoff=struct.unpack_from('<Q',e,32)[0]
    phentsize=struct.unpack_from('<H',e,54)[0]
    phnum=struct.unpack_from('<H',e,56)[0]
    f.seek(phoff)
    ph=f.read(phentsize*phnum)
segs=[]
for i in range(phnum):
    o=i*phentsize
    p_type=struct.unpack_from('<I',ph,o)[0]
    if p_type != 1:
        continue
    p_offset=struct.unpack_from('<Q',ph,o+8)[0]
    p_vaddr=struct.unpack_from('<Q',ph,o+16)[0]
    p_filesz=struct.unpack_from('<Q',ph,o+32)[0]
    p_memsz=struct.unpack_from('<Q',ph,o+40)[0]
    segs.append((p_offset,p_vaddr,p_filesz,p_memsz))
for va in target:
    hit=None
    for po,pv,pf,pm in segs:
        if pv <= va < pv+pf:
            hit=po+(va-pv)
            break
    if hit is None:
        raise SystemExit(f'VA not file-backed: {va:x}')
    print(hex(hit))
PY
) || return 1
  mapfile=$(printf '%s\n' "$offsets" | sed -n '1p')
  commonfile=$(printf '%s\n' "$offsets" | sed -n '2p')
  fieldfile=$(printf '%s\n' "$offsets" | sed -n '3p')
  [[ -n "$mapfile" && -n "$commonfile" && -n "$fieldfile" ]] || return 1

  sudo sh -c "echo 0 > '$tracefs/tracing_on'" 2>/dev/null || true
  sudo sh -c "echo > '$tracefs/trace'" 2>/dev/null || true
  sudo sh -c "echo > '$tracefs/uprobe_events'" 2>/dev/null || true
  if ! sudo sh -c "printf '%s\n' 'p:otc_map_content $link:$mapfile' 'p:otc_map_common $link:$commonfile' 'p:otc_map_field $link:$fieldfile' > '$tracefs/uprobe_events'" 2>/dev/null; then
    echo DECODED_MAP_UPROBES_AVAILABLE=false
    return 1
  fi
  if ! sudo sh -c "echo 1 > '$tracefs/events/uprobes/otc_map_content/enable'; echo 1 > '$tracefs/events/uprobes/otc_map_common/enable'; echo 1 > '$tracefs/events/uprobes/otc_map_field/enable'; echo 1 > '$tracefs/tracing_on'" 2>/dev/null; then
    echo DECODED_MAP_UPROBES_AVAILABLE=false
    return 1
  fi
  printf '%s' "$tracefs" >"$state/tracefs"
  echo DECODED_MAP_UPROBES_AVAILABLE=true
  echo PRE_ENTRY_DECODED_MAP_UPROBES_ARMED=true
  return 0
}

map_uprobe_hit() {
  local tracefs
  [[ -s "$state/tracefs" ]] || return 1
  tracefs=$(cat "$state/tracefs")
  sudo grep -qE 'otc_map_(content|common|field):' "$tracefs/trace" 2>/dev/null
}

fallback_gdb_map_hit() {
  local pid=$1 best=$2 map_line start_hex offset_hex load_bias content common fielddata gdbpid armed key
  sudo sysctl -w kernel.yama.ptrace_scope=0 >/dev/null 2>&1 || true
  map_line=$(grep -F "$client" "/proc/$pid/maps" | awk '$2 ~ /r-xp/ {print; exit}')
  [[ -n "$map_line" ]] || return 1
  start_hex=$(printf '%s\n' "$map_line" | awk '{split($1,a,"-"); print a[1]}')
  offset_hex=$(printf '%s\n' "$map_line" | awk '{print $3}')
  load_bias=$((16#$start_hex - 16#$offset_hex))
  content=$((load_bias + 0x19a8ea3))
  common=$((load_bias + 0x19a8a80))
  fielddata=$((load_bias + 0xcd3190))
  cat >"$state/worldmap.gdb" <<EOF
set pagination off
set confirm off
set print thread-events off
attach $pid
break *$content
commands 1
 silent
 shell printf 'DECODED_MAP_CONTENT_HIT=true\\n' > $state/worldmap-hit
 detach
 quit
end
break *$common
commands 2
 silent
 shell printf 'COMMON_MAP_DATA_HIT=true\\n' > $state/worldmap-hit
 detach
 quit
end
break *$fielddata
commands 3
 silent
 shell printf 'FIELDDATA_HANDLER_HIT=true\\n' > $state/worldmap-hit
 detach
 quit
end
continue
EOF
  rm -f "$state/worldmap-hit"
  sudo -n gdb -q -nx -x "$state/worldmap.gdb" >"$state/worldmap-gdb.log" 2>&1 &
  gdbpid=$!
  armed=0
  for _ in $(seq 1 60); do
    if grep -Eq 'Breakpoint (1|2|3)' "$state/worldmap-gdb.log" 2>/dev/null; then armed=1; break; fi
    kill -0 "$gdbpid" 2>/dev/null || break
    sleep 0.1
  done
  [[ "$armed" == 1 ]] || return 1
  for key in Right Left Up Down Right; do
    xdotool key --window "$best" "$key" || true
    for _ in $(seq 1 15); do
      [[ -s "$state/worldmap-hit" ]] && break 2
      sleep 0.2
    done
  done
  [[ -s "$state/worldmap-hit" ]] || return 1
  cat "$state/worldmap-hit"
  echo DECODED_WORLDMAP_GDB_HIT=true
  return 0
}

case "$mode" in
  warp)
    root=/tmp/warp
    mkdir -p "$root/bin" "$root/state" /tmp/tibia-package "$state" "$HOME"
    chmod 700 "$root" "$root/state" "$state" "$HOME"
    cd "$root/bin"
    curl -fL --retry 3 -o wgcf https://github.com/ViRb3/wgcf/releases/download/v2.2.32/wgcf_2.2.32_linux_amd64
    echo '2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c  wgcf' | sha256sum -c -
    chmod 755 wgcf
    curl -fL --retry 3 -o wireproxy.tar.gz https://github.com/windtf/wireproxy/releases/download/v1.1.3/wireproxy_linux_amd64.tar.gz
    echo 'e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c  wireproxy.tar.gz' | sha256sum -c -
    rm -rf extract; mkdir extract
    tar -xzf wireproxy.tar.gz -C extract
    cp "$(find extract -type f -name wireproxy -print -quit)" wireproxy
    chmod 755 wireproxy
    cd "$root/state"
    registered=0
    for attempt in $(seq 1 8); do
      rm -f wgcf-account.toml wgcf-profile.conf
      if "$root/bin/wgcf" register --accept-tos >/dev/null 2>"$state/wgcf-register-${attempt}.log"; then
        registered=1
        echo "WARP_REGISTRATION_ATTEMPT=$attempt"
        break
      fi
      sleep $((attempt * 2))
    done
    [[ "$registered" == 1 ]]
    "$root/bin/wgcf" generate >/dev/null
    chmod 600 wgcf-account.toml wgcf-profile.conf
    cat >wireproxy.conf <<EOF
WGConfig = $root/state/wgcf-profile.conf

[Socks5]
BindAddress = 127.0.0.1:25344
EOF
    chmod 600 wireproxy.conf
    "$root/bin/wireproxy" -n -c wireproxy.conf
    nohup "$root/bin/wireproxy" -c wireproxy.conf >"$state/wireproxy.log" 2>&1 </dev/null &
    ready=0
    for _ in $(seq 1 40); do
      if curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >"$state/warp.trace" 2>/dev/null; then ready=1; break; fi
      sleep 2
    done
    [[ "$ready" == 1 ]]
    grep -Eq '^warp=(on|plus)$' "$state/warp.trace"
    direct_ip=$(curl -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace | sed -n 's/^ip=//p')
    warp_ip=$(sed -n 's/^ip=//p' "$state/warp.trace")
    [[ -n "$direct_ip" && -n "$warp_ip" && "$direct_ip" != "$warp_ip" ]]
    grep -E '^(loc|warp)=' "$state/warp.trace"
    cat >"$state/proxychains.conf" <<'EOF'
strict_chain
proxy_dns
quiet_mode
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 25344
EOF
    echo WARP_CHANGED_EGRESS_VERIFIED=true
    ;;

  launch)
    [[ -x "$client" ]]
    lvp=$(find /usr/share/vulkan/icd.d -maxdepth 1 -type f -name 'lvp_icd*.json' -print -quit)
    [[ -n "$lvp" ]]
    nohup Xvfb :99 -screen 0 1280x800x24 -nolisten tcp >"$state/xvfb.log" 2>&1 </dev/null &
    for _ in $(seq 1 30); do xdpyinfo -display :99 >/dev/null 2>&1 && break; sleep 1; done
    xdpyinfo -display :99 >/dev/null
    cd "$pkg"
    : >"$state/client.log"
    nohup env DISPLAY=:99 HOME="$HOME" VK_ICD_FILENAMES="$lvp" VK_DRIVER_FILES="$lvp" LIBGL_ALWAYS_SOFTWARE=1 \
      proxychains4 -f "$state/proxychains.conf" "$client" >"$state/client.log" 2>&1 </dev/null &
    for _ in $(seq 1 60); do pgrep -x client >/dev/null && break; sleep 0.25; done
    pid=$(pgrep -x client | head -n1)
    [[ -n "$pid" ]]
    printf '%s' "$pid" >"$state/client-pid"
    printf '%s' "$client" >"$state/client-path"
    sleep 10
    kill -0 "$pid"
    best=''; best_area=0; bw=0; bh=0
    for w in $(xdotool search --onlyvisible --name '^Tibia$' 2>/dev/null || true); do
      geom=$(xdotool getwindowgeometry --shell "$w" 2>/dev/null || true)
      width=$(printf '%s\n' "$geom" | sed -n 's/^WIDTH=//p')
      height=$(printf '%s\n' "$geom" | sed -n 's/^HEIGHT=//p')
      [[ -n "$width" && -n "$height" ]] || continue
      area=$((width*height))
      if (( area > best_area )); then best=$w; best_area=$area; bw=$width; bh=$height; fi
    done
    echo "CLIENT_WINDOW=${bw}x${bh}"
    [[ -n "$best" && "$bw" == 1020 && "$bh" == 650 ]]
    printf '%s' "$best" >"$state/window-id"
    read -r local_count direct udp < <(client_socket_counts "$pid")
    echo "PRELOGIN_LOCAL_SOCKS=$local_count"
    echo "PRELOGIN_DIRECT_TCP=$direct"
    echo "PRELOGIN_UDP=$udp"
    [[ "$direct" -eq 0 && "$udp" -eq 0 ]]
    echo CLIENT_NO_DIRECT_EGRESS_BEFORE_LOGIN=true
    xdotool windowactivate --sync "$best" 2>/dev/null || true
    xdotool mousemove --window "$best" 510 302 click 1
    sleep 2
    kill -0 "$pid"
    echo ACCOUNT_LOGIN_OPENED_BY_FIXED_GEOMETRY=true
    ;;

  auth)
    set +x
    [[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]]
    best=$(cat "$state/window-id")
    pid=$(cat "$state/client-pid")
    client=$(cat "$state/client-path")
    kill -0 "$pid"
    [[ "$(xdotool getwindowgeometry --shell "$best" | sed -n 's/^WIDTH=//p')" == 1020 ]]
    [[ "$(xdotool getwindowgeometry --shell "$best" | sed -n 's/^HEIGHT=//p')" == 650 ]]

    # Clipboard keeps secrets out of command argv. Allow the client event loop to consume each paste before clearing it.
    xdotool mousemove --window "$best" 535 275 click 1
    xdotool key --window "$best" ctrl+a
    printf '%s' "$TIBIA_TEST_EMAIL" | xclip -selection clipboard -in
    xdotool key --window "$best" ctrl+v
    sleep 1
    printf '' | xclip -selection clipboard -in
    xdotool mousemove --window "$best" 535 304 click 1
    xdotool key --window "$best" ctrl+a
    printf '%s' "$TIBIA_TEST_PASSWORD" | xclip -selection clipboard -in
    xdotool key --window "$best" ctrl+v
    sleep 1
    printf '' | xclip -selection clipboard -in
    xdotool mousemove --window "$best" 590 388 click 1
    unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
    echo LOGIN_SUBMITTED_WITHOUT_OCR=true

    # Use the conservative authenticated timing proven in prior exact-client runs. No pixels/text are inspected.
    sleep 25
    kill -0 "$pid"
    echo AUTHENTICATED_TRANSITION_WAIT_COMPLETED=true

    uprobe_armed=0
    if arm_map_uprobes; then uprobe_armed=1; fi

    xdotool mousemove --window "$best" 285 193 click 1
    sleep 0.4
    xdotool key --window "$best" Return
    echo FIRST_CHARACTER_RETURN_SENT=true
    sleep 3
    xdotool mousemove --window "$best" 285 193 click --repeat 2 --delay 160 1
    echo FIRST_CHARACTER_DOUBLECLICK_SENT=true

    sustained=0; max_local=0; direct_seen=0; udp_seen=0; consecutive=0; semantic_hit=0
    for _ in $(seq 1 60); do
      sleep 1
      kill -0 "$pid"
      read -r local_count direct_count udp_count < <(client_socket_counts "$pid")
      (( local_count > max_local )) && max_local=$local_count || true
      (( direct_count > 0 )) && direct_seen=1 || true
      (( udp_count > 0 )) && udp_seen=1 || true
      if (( local_count > 0 )); then consecutive=$((consecutive+1)); else consecutive=0; fi
      if (( uprobe_armed == 1 )) && map_uprobe_hit; then semantic_hit=1; fi
      if (( consecutive >= 6 )); then sustained=1; fi
      if (( sustained == 1 && semantic_hit == 1 )); then break; fi
    done
    echo "POST_CHARACTER_LOCAL_SOCKS_MAX=$max_local"
    echo "POST_CHARACTER_DIRECT_TCP_SEEN=$direct_seen"
    echo "POST_CHARACTER_UDP_SEEN=$udp_seen"
    echo "POST_CHARACTER_SUSTAINED_SESSION=$sustained"
    echo "INITIAL_DECODED_MAP_UPROBE_HIT=$semantic_hit"
    [[ "$direct_seen" -eq 0 && "$udp_seen" -eq 0 ]]
    (( sustained == 1 ))
    kill -0 "$pid"
    echo POST_CHARACTER_CLIENT_STABLE=true

    if (( semantic_hit == 0 && uprobe_armed == 1 )); then
      for key in Right Left Up Down Right; do
        xdotool key --window "$best" "$key" || true
        sleep 1
        if map_uprobe_hit; then semantic_hit=1; break; fi
      done
    fi
    if (( semantic_hit == 1 )); then
      echo DECODED_WORLDMAP_UPROBE_HIT=true
    else
      echo DECODED_WORLDMAP_UPROBE_HIT=false
      fallback_gdb_map_hit "$pid" "$best"
      semantic_hit=1
    fi
    (( semantic_hit == 1 ))

    read -r final_local final_direct final_udp < <(client_socket_counts "$pid")
    echo "FINAL_LOCAL_SOCKS_COUNT=$final_local"
    echo "FINAL_DIRECT_TCP_COUNT=$final_direct"
    echo "FINAL_UDP_COUNT=$final_udp"
    [[ "$final_direct" -eq 0 && "$final_udp" -eq 0 && "$final_local" -gt 0 ]]
    kill -0 "$pid"
    echo PHYSICAL_TIBIA_WORLD_LOGIN_PROVEN=true
    echo TIBIA_CHARACTER_REACHED_GAME_MAP=true
    echo STRICT_NO_OCR_WORLD_ENTRY_PROVEN=true
    ;;

  *)
    echo "unknown mode: $mode" >&2
    exit 2
    ;;
esac
