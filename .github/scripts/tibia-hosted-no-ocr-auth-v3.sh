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

email_roundtrip() {
  local got=''
  printf '%s' '__OTC_SENTINEL__' | xclip -selection clipboard -in
  xdotool mousemove --window "$best" 535 275 click 1
  xdotool key --window "$best" ctrl+a
  printf '%s' "$TIBIA_TEST_EMAIL" | xdotool type --window "$best" --clearmodifiers --delay 3 --file -
  sleep 0.5
  xdotool key --window "$best" ctrl+a
  xdotool key --window "$best" ctrl+c
  sleep 0.4
  got=$(timeout 2 xclip -selection clipboard -out 2>/dev/null || true)
  printf '' | xclip -selection clipboard -in
  [[ "$got" == "$TIBIA_TEST_EMAIL" ]]
}

# Establish the actual form state without OCR. Nothing copied from the field is emitted.
form_state='none'
if email_roundtrip; then
  form_state='direct'
  echo EMAIL_FIELD_DIRECT_ROUNDTRIP=true
else
  echo EMAIL_FIELD_DIRECT_ROUNDTRIP=false
  # Bounded known alternate state: earlier hosted experiments used this control to open Account Login.
  xdotool mousemove --window "$best" 510 302 click 1
  sleep 2
  if email_roundtrip; then
    form_state='open-click'
    echo EMAIL_FIELD_AFTER_OPEN_CLICK_ROUNDTRIP=true
  else
    echo EMAIL_FIELD_AFTER_OPEN_CLICK_ROUNDTRIP=false
    # Keyboard-only fallback for a focused landing control.
    xdotool key --window "$best" Return
    sleep 2
    if email_roundtrip; then
      form_state='return'
      echo EMAIL_FIELD_AFTER_RETURN_ROUNDTRIP=true
    else
      echo EMAIL_FIELD_AFTER_RETURN_ROUNDTRIP=false
    fi
  fi
fi
[[ "$form_state" != none ]]
echo "LOGIN_FORM_STATE_PROVEN=$form_state"

# Email has already been proven in-place. Enter password from stdin; value never appears in argv/logs.
xdotool mousemove --window "$best" 535 304 click 1
xdotool key --window "$best" ctrl+a
printf '%s' "$TIBIA_TEST_PASSWORD" | xdotool type --window "$best" --clearmodifiers --delay 3 --file -
unset TIBIA_TEST_PASSWORD
sleep 0.5

# First submit from the password field, then bounded button fallback if no network attempt appears.
xdotool key --window "$best" Return
echo LOGIN_RETURN_SUBMITTED_WITHOUT_OCR=true
submit_network=0; submit_max=0; submit_direct=0; submit_udp=0
for _ in $(seq 1 60); do
  sleep 0.2
  kill -0 "$pid"
  read -r lc dc uc < <(socket_counts)
  (( lc > submit_max )) && submit_max=$lc || true
  (( dc > 0 )) && submit_direct=1 || true
  (( uc > 0 )) && submit_udp=1 || true
  if (( lc > 0 )); then submit_network=1; break; fi
done
if (( submit_network == 0 )); then
  xdotool mousemove --window "$best" 590 388 click 1
  echo LOGIN_BUTTON_FALLBACK_SENT_WITHOUT_OCR=true
  for _ in $(seq 1 60); do
    sleep 0.2
    kill -0 "$pid"
    read -r lc dc uc < <(socket_counts)
    (( lc > submit_max )) && submit_max=$lc || true
    (( dc > 0 )) && submit_direct=1 || true
    (( uc > 0 )) && submit_udp=1 || true
    if (( lc > 0 )); then submit_network=1; break; fi
  done
fi
echo "ACCOUNT_SUBMIT_LOCAL_SOCKS_MAX=$submit_max"
echo "ACCOUNT_SUBMIT_NETWORK_OBSERVED=$submit_network"
echo "ACCOUNT_SUBMIT_DIRECT_TCP_SEEN=$submit_direct"
echo "ACCOUNT_SUBMIT_UDP_SEEN=$submit_udp"
[[ "$submit_direct" -eq 0 && "$submit_udp" -eq 0 ]]
(( submit_network == 1 ))
unset TIBIA_TEST_EMAIL

# Allow account response/character list to settle. No image/text inspection.
sleep 8
kill -0 "$pid"

# Arm post-auth decoded-map observation before character activation if tracefs permits it.
tracefs=/sys/kernel/tracing
[[ -d "$tracefs" ]] || tracefs=/sys/kernel/debug/tracing
uprobe_armed=0
if sudo test -d "$tracefs"; then
  link=/tmp/tibia-client-uprobe
  rm -f "$link"
  ln -s "$client" "$link"
  offsets=$(python3 - "$client" <<'PY'
import struct,sys
path=sys.argv[1]
target=[0xcec8d0,0xcd3190,0x19a8a80,0x19a8ea3]
with open(path,'rb') as f:
    e=f.read(64)
    phoff=struct.unpack_from('<Q',e,32)[0]; entsz=struct.unpack_from('<H',e,54)[0]; n=struct.unpack_from('<H',e,56)[0]
    f.seek(phoff); ph=f.read(entsz*n)
segs=[]
for i in range(n):
    o=i*entsz
    if struct.unpack_from('<I',ph,o)[0] != 1: continue
    segs.append((struct.unpack_from('<Q',ph,o+8)[0],struct.unpack_from('<Q',ph,o+16)[0],struct.unpack_from('<Q',ph,o+32)[0]))
for va in target:
    for po,pv,pf in segs:
        if pv <= va < pv+pf:
            print(hex(po+va-pv)); break
    else: raise SystemExit(1)
PY
) || offsets=''
  fullfile=$(printf '%s\n' "$offsets" | sed -n '1p'); fieldfile=$(printf '%s\n' "$offsets" | sed -n '2p')
  commonfile=$(printf '%s\n' "$offsets" | sed -n '3p'); contentfile=$(printf '%s\n' "$offsets" | sed -n '4p')
  if [[ -n "$fullfile" && -n "$fieldfile" && -n "$commonfile" && -n "$contentfile" ]]; then
    sudo sh -c "echo 0 > '$tracefs/tracing_on'; echo > '$tracefs/trace'; echo > '$tracefs/uprobe_events'" 2>/dev/null || true
    if sudo sh -c "printf '%s\n' 'p:otc_fullmap $link:$fullfile' 'p:otc_fielddata $link:$fieldfile' 'p:otc_common $link:$commonfile' 'p:otc_content $link:$contentfile' > '$tracefs/uprobe_events'" 2>/dev/null && \
       sudo sh -c "for e in otc_fullmap otc_fielddata otc_common otc_content; do echo 1 > '$tracefs/events/uprobes/'\$e'/enable'; done; echo 1 > '$tracefs/tracing_on'" 2>/dev/null; then
      uprobe_armed=1
    fi
  fi
fi
echo "PRE_CHARACTER_DECODED_MAP_UPROBES_ARMED=$uprobe_armed"

# Same exact first row used by the independently successful exact-client reference.
xdotool mousemove --window "$best" 285 193 click 1
sleep 0.4
xdotool key --window "$best" Return
echo FIRST_CHARACTER_RETURN_SENT=true
sleep 3
xdotool mousemove --window "$best" 285 193 click --repeat 2 --delay 160 1
echo FIRST_CHARACTER_DOUBLECLICK_SENT=true

stable=0; max_local=0; direct_seen=0; udp_seen=0; consecutive=0; semantic=0
for _ in $(seq 1 120); do
  sleep 0.5
  kill -0 "$pid"
  read -r lc dc uc < <(socket_counts)
  (( lc > max_local )) && max_local=$lc || true
  (( dc > 0 )) && direct_seen=1 || true
  (( uc > 0 )) && udp_seen=1 || true
  if (( lc > 0 )); then consecutive=$((consecutive+1)); else consecutive=0; fi
  if (( consecutive >= 12 )); then stable=1; fi
  if (( uprobe_armed == 1 )) && sudo grep -qE 'otc_(fullmap|fielddata|common|content):' "$tracefs/trace" 2>/dev/null; then semantic=1; fi
  if (( stable == 1 && semantic == 1 )); then break; fi
done
echo "POST_CHARACTER_LOCAL_SOCKS_MAX=$max_local"
echo "POST_CHARACTER_DIRECT_TCP_SEEN=$direct_seen"
echo "POST_CHARACTER_UDP_SEEN=$udp_seen"
echo "POST_CHARACTER_SUSTAINED_SESSION=$stable"
echo "DECODED_WORLDMAP_UPROBE_HIT=$semantic"
[[ "$direct_seen" -eq 0 && "$udp_seen" -eq 0 ]]
(( stable == 1 ))

if (( semantic == 0 )); then
  # Post-entry fallback only: debugger is never attached before a sustained session exists.
  sudo sysctl -w kernel.yama.ptrace_scope=0 >/dev/null 2>&1 || true
  map_line=$(grep -F "$client" "/proc/$pid/maps" | awk '$2 ~ /r-xp/ {print; exit}')
  [[ -n "$map_line" ]]
  start_hex=$(printf '%s\n' "$map_line" | awk '{split($1,a,"-"); print a[1]}')
  offset_hex=$(printf '%s\n' "$map_line" | awk '{print $3}')
  bias=$((16#$start_hex-16#$offset_hex))
  full=$((bias+0xcec8d0)); field=$((bias+0xcd3190)); common=$((bias+0x19a8a80)); content=$((bias+0x19a8ea3))
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
break *$field
commands 3
 silent
 shell printf 'FIELDDATA_HANDLER_HIT=true\\n' > $state/worldmap-hit
 detach
 quit
end
break *$full
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
  gpid=$!; armed=0
  for _ in $(seq 1 80); do
    if grep -Eq 'Breakpoint (1|2|3|4)' "$state/worldmap-gdb.log" 2>/dev/null; then armed=1; break; fi
    kill -0 "$gpid" 2>/dev/null || break
    sleep 0.1
  done
  [[ "$armed" == 1 ]]
  for key in Right Left Up Down Right; do
    xdotool key --window "$best" "$key" || true
    for _ in $(seq 1 15); do [[ -s "$state/worldmap-hit" ]] && break 2; sleep 0.2; done
  done
  [[ -s "$state/worldmap-hit" ]]
  cat "$state/worldmap-hit"
  semantic=1
  echo DECODED_WORLDMAP_GDB_HIT=true
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
