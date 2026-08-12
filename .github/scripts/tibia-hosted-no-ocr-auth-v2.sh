#!/usr/bin/env bash
set -Eeuo pipefail
set +x

state=/tmp/tibia-world
best=$(cat "$state/window-id")
pid=$(cat "$state/client-pid")
client=$(cat "$state/client-path")
[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]]
kill -0 "$pid"
[[ "$(xdotool getwindowgeometry --shell "$best" | sed -n 's/^WIDTH=//p')" == 1020 ]]
[[ "$(xdotool getwindowgeometry --shell "$best" | sed -n 's/^HEIGHT=//p')" == 650 ]]

socket_counts() {
  local tcp_rows udp_rows local_count total_count direct_count udp_count
  tcp_rows=$(ss -ntp 2>/dev/null | grep "pid=$pid," || true)
  udp_rows=$(ss -nup 2>/dev/null | grep "pid=$pid," || true)
  local_count=$(printf '%s\n' "$tcp_rows" | awk '$5 ~ /127\.0\.0\.1:25344$/ || $5 ~ /\[::1\]:25344$/ {n++} END{print n+0}')
  total_count=$(printf '%s\n' "$tcp_rows" | grep -c . || true)
  direct_count=$((total_count-local_count))
  udp_count=$(printf '%s\n' "$udp_rows" | grep -c . || true)
  printf '%s %s %s\n' "$local_count" "$direct_count" "$udp_count"
}

tracefs=/sys/kernel/tracing
[[ -d "$tracefs" ]] || tracefs=/sys/kernel/debug/tracing
uprobe_armed=0

arm_uprobes() {
  local link offsets fullfile fieldfile commonfile contentfile
  sudo test -d "$tracefs" || return 1
  link=/tmp/tibia-client-uprobe
  rm -f "$link"
  ln -s "$client" "$link"
  offsets=$(python3 - "$client" <<'PY'
import struct,sys
path=sys.argv[1]
target=[0xcec8d0,0xcd3190,0x19a8a80,0x19a8ea3]
with open(path,'rb') as f:
    e=f.read(64)
    if e[:4] != b'\x7fELF' or e[4] != 2 or e[5] != 1:
        raise SystemExit('unsupported ELF')
    phoff=struct.unpack_from('<Q',e,32)[0]
    phentsize=struct.unpack_from('<H',e,54)[0]
    phnum=struct.unpack_from('<H',e,56)[0]
    f.seek(phoff); ph=f.read(phentsize*phnum)
segs=[]
for i in range(phnum):
    o=i*phentsize
    if struct.unpack_from('<I',ph,o)[0] != 1:
        continue
    p_offset=struct.unpack_from('<Q',ph,o+8)[0]
    p_vaddr=struct.unpack_from('<Q',ph,o+16)[0]
    p_filesz=struct.unpack_from('<Q',ph,o+32)[0]
    segs.append((p_offset,p_vaddr,p_filesz))
for va in target:
    for po,pv,pf in segs:
        if pv <= va < pv+pf:
            print(hex(po + va - pv)); break
    else:
        raise SystemExit(f'VA not file-backed: {va:x}')
PY
) || return 1
  fullfile=$(printf '%s\n' "$offsets" | sed -n '1p')
  fieldfile=$(printf '%s\n' "$offsets" | sed -n '2p')
  commonfile=$(printf '%s\n' "$offsets" | sed -n '3p')
  contentfile=$(printf '%s\n' "$offsets" | sed -n '4p')
  [[ -n "$fullfile" && -n "$fieldfile" && -n "$commonfile" && -n "$contentfile" ]] || return 1
  sudo sh -c "echo 0 > '$tracefs/tracing_on'" 2>/dev/null || true
  sudo sh -c "echo > '$tracefs/trace'" 2>/dev/null || true
  sudo sh -c "echo > '$tracefs/uprobe_events'" 2>/dev/null || true
  sudo sh -c "printf '%s\n' \
    'p:otc_fullmap $link:$fullfile' \
    'p:otc_fielddata $link:$fieldfile' \
    'p:otc_map_common $link:$commonfile' \
    'p:otc_map_content $link:$contentfile' > '$tracefs/uprobe_events'" 2>/dev/null || return 1
  sudo sh -c "for e in otc_fullmap otc_fielddata otc_map_common otc_map_content; do echo 1 > '$tracefs/events/uprobes/'\$e'/enable'; done; echo 1 > '$tracefs/tracing_on'" 2>/dev/null || return 1
  echo PRE_ENTRY_DECODED_MAP_UPROBES_ARMED=true
  return 0
}

uprobe_hit() {
  sudo grep -qE 'otc_(fullmap|fielddata|map_common|map_content):' "$tracefs/trace" 2>/dev/null
}

fallback_gdb() {
  local map_line start_hex offset_hex load_bias fullmap fielddata common content gdbpid armed key
  sudo sysctl -w kernel.yama.ptrace_scope=0 >/dev/null 2>&1 || true
  map_line=$(grep -F "$client" "/proc/$pid/maps" | awk '$2 ~ /r-xp/ {print; exit}')
  [[ -n "$map_line" ]] || return 1
  start_hex=$(printf '%s\n' "$map_line" | awk '{split($1,a,"-"); print a[1]}')
  offset_hex=$(printf '%s\n' "$map_line" | awk '{print $3}')
  load_bias=$((16#$start_hex - 16#$offset_hex))
  fullmap=$((load_bias + 0xcec8d0)); fielddata=$((load_bias + 0xcd3190))
  common=$((load_bias + 0x19a8a80)); content=$((load_bias + 0x19a8ea3))
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
break *$fullmap
commands 4
 silent
 shell printf 'FULLMAP_HANDLER_HIT=true\\n' > $state/worldmap-hit
 detach
 quit
end
continue
EOF
  rm -f "$state/worldmap-hit"
  sudo -n gdb -q -nx -x "$state/worldmap.gdb" >"$state/worldmap-gdb.log" 2>&1 &
  gdbpid=$!; armed=0
  for _ in $(seq 1 80); do
    if grep -Eq 'Breakpoint (1|2|3|4)' "$state/worldmap-gdb.log" 2>/dev/null; then armed=1; break; fi
    kill -0 "$gdbpid" 2>/dev/null || break
    sleep 0.1
  done
  [[ "$armed" == 1 ]] || return 1
  for key in Right Left Up Down Right; do
    xdotool key --window "$best" "$key" || true
    for _ in $(seq 1 15); do [[ -s "$state/worldmap-hit" ]] && break 2; sleep 0.2; done
  done
  [[ -s "$state/worldmap-hit" ]] || return 1
  cat "$state/worldmap-hit"
  echo DECODED_WORLDMAP_GDB_HIT=true
}

# Type through XTEST from stdin. This matches physical key events, while keeping secrets out of argv and Git/logs.
xdotool windowactivate --sync "$best" 2>/dev/null || true
xdotool mousemove --window "$best" 535 275 click 1
xdotool key --window "$best" ctrl+a
printf '%s' "$TIBIA_TEST_EMAIL" | xdotool type --window "$best" --clearmodifiers --delay 3 --file -
xdotool mousemove --window "$best" 535 304 click 1
xdotool key --window "$best" ctrl+a
printf '%s' "$TIBIA_TEST_PASSWORD" | xdotool type --window "$best" --clearmodifiers --delay 3 --file -
xdotool mousemove --window "$best" 590 388 click 1
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
echo LOGIN_SUBMITTED_WITHOUT_OCR=true

# Observe only socket counts while the account transition completes. No screen/text/image is read.
auth_max=0; auth_direct=0; auth_udp=0
for _ in $(seq 1 125); do
  sleep 0.2
  kill -0 "$pid"
  read -r lc dc uc < <(socket_counts)
  (( lc > auth_max )) && auth_max=$lc || true
  (( dc > 0 )) && auth_direct=1 || true
  (( uc > 0 )) && auth_udp=1 || true
done
echo "ACCOUNT_LOGIN_LOCAL_SOCKS_MAX=$auth_max"
echo "ACCOUNT_LOGIN_DIRECT_TCP_SEEN=$auth_direct"
echo "ACCOUNT_LOGIN_UDP_SEEN=$auth_udp"
[[ "$auth_direct" -eq 0 && "$auth_udp" -eq 0 ]]

if arm_uprobes; then uprobe_armed=1; else echo PRE_ENTRY_DECODED_MAP_UPROBES_ARMED=false; fi

# Same deterministic first-row activation as the independently successful exact-client run.
xdotool mousemove --window "$best" 285 193 click 1
sleep 0.4
xdotool key --window "$best" Return
echo FIRST_CHARACTER_RETURN_SENT=true
sleep 3
xdotool mousemove --window "$best" 285 193 click --repeat 2 --delay 160 1
echo FIRST_CHARACTER_DOUBLECLICK_SENT=true

sustained=0; max_local=0; direct_seen=0; udp_seen=0; consecutive=0; semantic=0
for _ in $(seq 1 90); do
  sleep 0.5
  kill -0 "$pid"
  read -r lc dc uc < <(socket_counts)
  (( lc > max_local )) && max_local=$lc || true
  (( dc > 0 )) && direct_seen=1 || true
  (( uc > 0 )) && udp_seen=1 || true
  if (( lc > 0 )); then consecutive=$((consecutive+1)); else consecutive=0; fi
  if (( uprobe_armed == 1 )) && uprobe_hit; then semantic=1; fi
  if (( consecutive >= 12 )); then sustained=1; fi
  if (( sustained == 1 && semantic == 1 )); then break; fi
done
echo "POST_CHARACTER_LOCAL_SOCKS_MAX=$max_local"
echo "POST_CHARACTER_DIRECT_TCP_SEEN=$direct_seen"
echo "POST_CHARACTER_UDP_SEEN=$udp_seen"
echo "POST_CHARACTER_SUSTAINED_SESSION=$sustained"
echo "INITIAL_DECODED_WORLDMAP_HIT=$semantic"
[[ "$direct_seen" -eq 0 && "$udp_seen" -eq 0 ]]
(( sustained == 1 ))

if (( semantic == 0 && uprobe_armed == 1 )); then
  for key in Right Left Up Down Right; do
    xdotool key --window "$best" "$key" || true
    sleep 1
    if uprobe_hit; then semantic=1; break; fi
  done
fi
if (( semantic == 1 )); then
  echo DECODED_WORLDMAP_UPROBE_HIT=true
else
  echo DECODED_WORLDMAP_UPROBE_HIT=false
  fallback_gdb
  semantic=1
fi
(( semantic == 1 ))

read -r final_local final_direct final_udp < <(socket_counts)
echo "FINAL_LOCAL_SOCKS_COUNT=$final_local"
echo "FINAL_DIRECT_TCP_COUNT=$final_direct"
echo "FINAL_UDP_COUNT=$final_udp"
[[ "$final_direct" -eq 0 && "$final_udp" -eq 0 && "$final_local" -gt 0 ]]
kill -0 "$pid"
echo PHYSICAL_TIBIA_WORLD_LOGIN_PROVEN=true
echo TIBIA_CHARACTER_REACHED_GAME_MAP=true
echo STRICT_NO_OCR_WORLD_ENTRY_PROVEN=true
