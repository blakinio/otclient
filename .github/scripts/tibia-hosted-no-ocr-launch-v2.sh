#!/usr/bin/env bash
set -Eeuo pipefail

state=/tmp/tibia-world
pkg="$HOME/.local/share/CipSoft GmbH/Tibia/packages/Tibia"
client="$pkg/bin/client"
[[ -x "$client" ]]
mkdir -p "$state"

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

tcp_rows=$(ss -ntp 2>/dev/null | grep "pid=$pid," || true)
udp_rows=$(ss -nup 2>/dev/null | grep "pid=$pid," || true)
local_count=$(printf '%s\n' "$tcp_rows" | awk '$5 ~ /127\.0\.0\.1:25344$/ || $5 ~ /\[::1\]:25344$/ {n++} END{print n+0}')
total_count=$(printf '%s\n' "$tcp_rows" | grep -c . || true)
direct_count=$((total_count-local_count))
udp_count=$(printf '%s\n' "$udp_rows" | grep -c . || true)
echo "PRELOGIN_LOCAL_SOCKS=$local_count"
echo "PRELOGIN_DIRECT_TCP=$direct_count"
echo "PRELOGIN_UDP=$udp_count"
[[ "$direct_count" -eq 0 && "$udp_count" -eq 0 ]]

# The independently successful exact-client run typed directly into the form at this point.
# Do not add the previously-failing extra click at 510,302.
xdotool windowactivate --sync "$best" 2>/dev/null || true
kill -0 "$pid"
echo EXACT_LOGIN_FORM_GEOMETRY_READY_WITHOUT_EXTRA_CLICK=true
