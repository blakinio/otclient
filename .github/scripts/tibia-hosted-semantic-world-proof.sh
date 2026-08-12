#!/usr/bin/env bash
set -Eeuo pipefail
set +x
state=/tmp/tibia-world
pid=$(cat "$state/client-pid")
client=$(cat "$state/client-path")
best=$(cat "$state/window-id")
export DBUS_SESSION_BUS_ADDRESS=$(cat "$state/dbus-address")
kill -0 "$pid"

socket_counts() {
  local tcp udp_rows lc total dc uc
  tcp=$(ss -ntp 2>/dev/null | grep "pid=$pid," || true); udp_rows=$(ss -nup 2>/dev/null | grep "pid=$pid," || true)
  lc=$(printf '%s\n' "$tcp" | awk '$5 ~ /127\.0\.0\.1:25344$/ || $5 ~ /\[::1\]:25344$/ {n++} END{print n+0}')
  total=$(printf '%s\n' "$tcp" | grep -c . || true); dc=$((total-lc)); uc=$(printf '%s\n' "$udp_rows" | grep -c . || true)
  printf '%s %s %s\n' "$lc" "$dc" "$uc"
}

# Account login is semantic AT-SPI: no coordinates, pixels, OCR, or clipboard.
python3 .github/scripts/tibia-atspi-controller.py login
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
echo ATSPI_ACCOUNT_LOGIN_COMPLETED=true

# Arm non-stopping kernel probes after Select Character is proven, before character activation.
tracefs=/sys/kernel/tracing; [[ -d "$tracefs" ]] || tracefs=/sys/kernel/debug/tracing
sudo test -d "$tracefs"
link=/tmp/tibia-client-uprobe; rm -f "$link"; ln -s "$client" "$link"
offsets=$(python3 - "$client" <<'PY'
import struct,sys
p=sys.argv[1]; targets=[0xcec8d0,0xcd3190,0x19a8a80,0x19a8ea3]
with open(p,'rb') as f:
 e=f.read(64); phoff=struct.unpack_from('<Q',e,32)[0]; es=struct.unpack_from('<H',e,54)[0]; n=struct.unpack_from('<H',e,56)[0]; f.seek(phoff); ph=f.read(es*n)
segs=[]
for i in range(n):
 o=i*es
 if struct.unpack_from('<I',ph,o)[0]!=1: continue
 segs.append((struct.unpack_from('<Q',ph,o+8)[0],struct.unpack_from('<Q',ph,o+16)[0],struct.unpack_from('<Q',ph,o+32)[0]))
for va in targets:
 for po,pv,pf in segs:
  if pv<=va<pv+pf: print(hex(po+va-pv)); break
 else: raise SystemExit(1)
PY
)
full=$(printf '%s\n' "$offsets"|sed -n '1p'); field=$(printf '%s\n' "$offsets"|sed -n '2p'); common=$(printf '%s\n' "$offsets"|sed -n '3p'); content=$(printf '%s\n' "$offsets"|sed -n '4p')
sudo sh -c "echo 0 > '$tracefs/tracing_on'; echo > '$tracefs/trace'; echo > '$tracefs/uprobe_events'" 2>/dev/null || true
sudo sh -c "printf '%s\n' 'p:otc_fullmap $link:$full' 'p:otc_fielddata $link:$field' 'p:otc_common $link:$common' 'p:otc_content $link:$content' > '$tracefs/uprobe_events'"
sudo sh -c "for e in otc_fullmap otc_fielddata otc_common otc_content; do echo 1 > '$tracefs/events/uprobes/'\$e'/enable'; done; echo 1 > '$tracefs/tracing_on'"
echo PRE_CHARACTER_DECODED_MAP_UPROBES_ARMED=true

# Prefer semantic row action. Coordinate fallback is allowed only after Select Character was semantically proven.
set +e
python3 .github/scripts/tibia-atspi-controller.py character
rc=$?
set -e
if [[ "$rc" -eq 6 ]]; then
  echo ATSPI_CHARACTER_COORDINATE_FALLBACK=true
  xdotool mousemove --window "$best" 285 193 click 1
  sleep .4
  xdotool key --window "$best" Return
  sleep 3
  xdotool mousemove --window "$best" 285 193 click --repeat 2 --delay 160 1
elif [[ "$rc" -ne 0 ]]; then
  exit "$rc"
fi

semantic=0; max_local=0; direct_seen=0; udp_seen=0
for _ in $(seq 1 120); do
  sleep .5
  kill -0 "$pid"
  read -r lc dc uc < <(socket_counts)
  ((lc>max_local)) && max_local=$lc || true; ((dc>0)) && direct_seen=1 || true; ((uc>0)) && udp_seen=1 || true
  if sudo grep -qE 'otc_(fullmap|fielddata|common|content):' "$tracefs/trace" 2>/dev/null; then semantic=1; break; fi
done
echo "POST_CHARACTER_LOCAL_SOCKS_MAX=$max_local"
echo "POST_CHARACTER_DIRECT_TCP_SEEN=$direct_seen"
echo "POST_CHARACTER_UDP_SEEN=$udp_seen"
echo "DECODED_WORLDMAP_UPROBE_HIT=$semantic"
[[ "$direct_seen" -eq 0 && "$udp_seen" -eq 0 ]]
((semantic==1))

# Prove which semantic boundary fired without exposing runtime addresses or account data.
safe=$(sudo grep -Eo 'otc_(fullmap|fielddata|common|content):' "$tracefs/trace" | head -n1 | tr -d ':')
echo "DECODED_WORLDMAP_EVENT=$safe"
read -r fl fd fu < <(socket_counts)
echo "FINAL_LOCAL_SOCKS_COUNT=$fl"; echo "FINAL_DIRECT_TCP_COUNT=$fd"; echo "FINAL_UDP_COUNT=$fu"
[[ "$fd" -eq 0 && "$fu" -eq 0 ]]
kill -0 "$pid"
echo PHYSICAL_TIBIA_WORLD_LOGIN_PROVEN=true
echo TIBIA_CHARACTER_REACHED_GAME_MAP=true
echo STRICT_NO_OCR_WORLD_ENTRY_PROVEN=true
