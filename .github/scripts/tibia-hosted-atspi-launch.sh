#!/usr/bin/env bash
set -Eeuo pipefail
state=/tmp/tibia-world
repo_root="${GITHUB_WORKSPACE:-$(pwd)}"
pkg="$HOME/.local/share/CipSoft GmbH/Tibia/packages/Tibia"
client="$pkg/bin/client"
controller="$repo_root/.github/scripts/tibia-atspi-controller.py"
[[ -x "$client" ]]
[[ -f "$controller" ]]
mkdir -p "$state"

nohup Xvfb :99 -screen 0 1280x800x24 -nolisten tcp >"$state/xvfb.log" 2>&1 </dev/null &
for _ in $(seq 1 30); do xdpyinfo -display :99 >/dev/null 2>&1 && break; sleep 1; done
xdpyinfo -display :99 >/dev/null

mapfile -t dbus_info < <(dbus-daemon --session --fork --print-address=1 --print-pid=1)
[[ ${#dbus_info[@]} -ge 2 && -n "${dbus_info[0]}" ]]
printf '%s' "${dbus_info[0]}" >"$state/dbus-address"
printf '%s' "${dbus_info[1]}" >"$state/dbus-pid"
export DBUS_SESSION_BUS_ADDRESS=${dbus_info[0]}

lvp=$(find /usr/share/vulkan/icd.d -maxdepth 1 -type f -name 'lvp_icd*.json' -print -quit)
[[ -n "$lvp" ]]
cd "$pkg"
: >"$state/client.log"
nohup env DISPLAY=:99 HOME="$HOME" DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" \
  QT_ACCESSIBILITY=1 QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1 \
  VK_ICD_FILENAMES="$lvp" VK_DRIVER_FILES="$lvp" LIBGL_ALWAYS_SOFTWARE=1 \
  proxychains4 -f "$state/proxychains.conf" "$client" >"$state/client.log" 2>&1 </dev/null &
for _ in $(seq 1 60); do pgrep -x client >/dev/null && break; sleep .25; done
pid=$(pgrep -x client | head -n1)
[[ -n "$pid" ]]
printf '%s' "$pid" >"$state/client-pid"
printf '%s' "$client" >"$state/client-path"
sleep 10
kill -0 "$pid"

best=''; best_area=0; bw=0; bh=0
for w in $(xdotool search --onlyvisible --name '^Tibia$' 2>/dev/null || true); do
  geom=$(xdotool getwindowgeometry --shell "$w" 2>/dev/null || true)
  width=$(printf '%s\n' "$geom" | sed -n 's/^WIDTH=//p'); height=$(printf '%s\n' "$geom" | sed -n 's/^HEIGHT=//p')
  [[ -n "$width" && -n "$height" ]] || continue
  area=$((width*height)); if ((area>best_area)); then best=$w; best_area=$area; bw=$width; bh=$height; fi
done
echo "CLIENT_WINDOW=${bw}x${bh}"
[[ -n "$best" && "$bw" == 1020 && "$bh" == 650 ]]
printf '%s' "$best" >"$state/window-id"

tcp_rows=$(ss -ntp 2>/dev/null | grep "pid=$pid," || true)
udp_rows=$(ss -nup 2>/dev/null | grep "pid=$pid," || true)
local_count=$(printf '%s\n' "$tcp_rows" | awk '$5 ~ /127\.0\.0\.1:25344$/ || $5 ~ /\[::1\]:25344$/ {n++} END{print n+0}')
total_count=$(printf '%s\n' "$tcp_rows" | grep -c . || true)
direct=$((total_count-local_count)); udp=$(printf '%s\n' "$udp_rows" | grep -c . || true)
echo "PRELOGIN_LOCAL_SOCKS=$local_count"
echo "PRELOGIN_DIRECT_TCP=$direct"
echo "PRELOGIN_UDP=$udp"
[[ "$direct" -eq 0 && "$udp" -eq 0 ]]

/usr/bin/python3 "$controller" inspect
echo ATSPI_LAUNCH_READY=true
