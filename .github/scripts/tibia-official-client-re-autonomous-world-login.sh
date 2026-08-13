#!/usr/bin/env bash
set +x
set -Eeuo pipefail

: "${CANONICAL_STATE:?}" "${LEGACY_IMAGE_STATE:?}" "${TRACK_DISPLAY:?}" "${TRACK_WARP_PORT:?}" "${EXPECTED_CLIENT_SHA256:?}" "${TIBIA_TEST_EMAIL:?}" "${TIBIA_TEST_PASSWORD:?}"
[[ "$GITHUB_REPOSITORY" == blakinio/otclient ]]
[[ "$RUNNER_NAME" == synology-otclient-01 ]]
[[ "$RUNNER_OS" == Linux && "$(uname -s)" == Linux ]]

if [[ -d /work && -w /work ]]; then state="$LEGACY_IMAGE_STATE"; else state="$CANONICAL_STATE"; fi
marker='OTCLIENT_TIBIA_RE_TRACK=official-client-re'
runtime="$state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"
client="$runtime/bin/client"
toolroot="$state/toolroot"
tool_path="$toolroot/usr/bin:$toolroot/usr/sbin:/usr/bin:/bin"
tool_lib="$toolroot/usr/lib/x86_64-linux-gnu:$toolroot/lib/x86_64-linux-gnu"
proxy_conf="$state/config/proxychains.conf"
evidence="$state/evidence/autonomous-login-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$state/runtime" "$state/evidence" "$evidence"
chmod 700 "$state/runtime" "$state/evidence" "$evidence"

[[ -x "$client" ]]
[[ "$(stat -c %s "$client")" == 51965216 ]]
[[ "$(sha256sum "$client" | awk '{print $1}')" == "$EXPECTED_CLIENT_SHA256" ]]
echo TRACK_A_EXACT_OFFICIAL_CLIENT_VERIFIED=true

warp_pid="$(tr -cd '0-9' <"$state/runtime/wireproxy.pid" 2>/dev/null || true)"
[[ -n "$warp_pid" && -r "/proc/$warp_pid/environ" ]]
grep -azFxq "$marker" "/proc/$warp_pid/environ"
kill -0 "$warp_pid"
curl --socks5-hostname "127.0.0.1:$TRACK_WARP_PORT" -fsS --max-time 15 https://www.cloudflare.com/cdn-cgi/trace | grep -Eq '^warp=(on|plus)$'
echo TRACK_A_WARP_VERIFIED=true

old_pid="$(tr -cd '0-9' <"$state/runtime/client.pid" 2>/dev/null || true)"
if [[ -n "$old_pid" && -r "/proc/$old_pid/environ" ]]; then
  grep -azFxq "$marker" "/proc/$old_pid/environ"
  [[ "$(readlink -f "/proc/$old_pid/exe")" == "$client" ]]
  kill "$old_pid" 2>/dev/null || true
  for _ in $(seq 1 30); do kill -0 "$old_pid" 2>/dev/null || break; sleep .2; done
done_old=true
fi

xvfb_pid="$(tr -cd '0-9' <"$state/runtime/xvfb.pid" 2>/dev/null || true)"
if [[ -z "$xvfb_pid" || ! -r "/proc/$xvfb_pid/environ" || ! -e /tmp/.X11-unix/X98 ]]; then
  rm -f /tmp/.X98-lock /tmp/.X11-unix/X98 2>/dev/null || true
  private_xvfb="$state/runtime/Xvfb-track-a"
  [[ -x "$private_xvfb" ]]
  cd "$toolroot/usr/bin"
  env -u RUNNER_TRACKING_ID OTCLIENT_TIBIA_RE_TRACK=official-client-re \
    PATH="$tool_path" LD_LIBRARY_PATH="$tool_lib" XKB_CONFIG_ROOT="$toolroot/usr/share/X11/xkb" \
    nohup "$private_xvfb" "$TRACK_DISPLAY" -screen 0 1280x800x24 \
    -xkbdir "$toolroot/usr/share/X11/xkb" +extension GLX +iglx +render -nolisten tcp -noreset \
    >"$state/runtime/xvfb.log" 2>&1 </dev/null &
  xvfb_pid=$!
  printf '%s\n' "$xvfb_pid" >"$state/runtime/xvfb.pid"
  chmod 600 "$state/runtime/xvfb.pid"
  for _ in $(seq 1 30); do [[ -e /tmp/.X11-unix/X98 ]] && break; kill -0 "$xvfb_pid"; sleep 1; done
fi
[[ -e /tmp/.X11-unix/X98 ]]
[[ -r "/proc/$xvfb_pid/environ" ]]
grep -azFxq "$marker" "/proc/$xvfb_pid/environ"
echo TRACK_A_XVFB_VERIFIED=true

proxy_lib="$(find "$toolroot" -type f -name 'libproxychains.so.4' -print -quit)"
vk_icd="$(find "$toolroot/usr/share/vulkan/icd.d" -type f -name 'lvp_icd*.json' -print -quit)"
swrast="$(find "$toolroot" \( -type f -o -type l \) -name 'swrast_dri.so' -print -quit)"
[[ -n "$proxy_lib" && -n "$vk_icd" && -n "$swrast" && -s "$proxy_conf" ]]
dri_dir="$(dirname "$swrast")"

cd "$runtime"
env -u RUNNER_TRACKING_ID OTCLIENT_TIBIA_RE_TRACK=official-client-re \
  HOME="$state/home" DISPLAY="$TRACK_DISPLAY" PATH="$tool_path" \
  LD_LIBRARY_PATH="$runtime/lib:$tool_lib" \
  LIBGL_ALWAYS_SOFTWARE=1 LIBGL_DRIVERS_PATH="$dri_dir" QSG_RHI_BACKEND=vulkan \
  VK_ICD_FILENAMES="$vk_icd" XDG_DATA_DIRS="$toolroot/usr/share:/usr/share" \
  FONTCONFIG_PATH="$toolroot/etc/fonts" FONTCONFIG_FILE="$toolroot/etc/fonts/fonts.conf" \
  LD_PRELOAD="$proxy_lib" PROXYCHAINS_CONF_FILE="$proxy_conf" \
  nohup "$client" >"$state/runtime/client.log" 2>&1 </dev/null &
pid=$!
printf '%s\n' "$pid" >"$state/runtime/client.pid"
chmod 600 "$state/runtime/client.pid"
sleep 12
kill -0 "$pid"
grep -azFxq "$marker" "/proc/$pid/environ"
echo TRACK_A_OFFICIAL_CLIENT_RUNNING=true

export HOME="$state/home" DISPLAY="$TRACK_DISPLAY" PATH="$tool_path" LD_LIBRARY_PATH="$tool_lib"
resolve_window() {
  local w g width height area best='' best_area=0
  for _ in $(seq 1 60); do
    best=''; best_area=0
    for w in $("$toolroot/usr/bin/xdotool" search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null || true); do
      g="$("$toolroot/usr/bin/xdotool" getwindowgeometry --shell "$w" 2>/dev/null || true)"
      width="$(printf '%s\n' "$g" | sed -n 's/^WIDTH=//p')"; height="$(printf '%s\n' "$g" | sed -n 's/^HEIGHT=//p')"
      [[ -n "$width" && -n "$height" ]] || continue
      area=$((width*height)); if ((area>best_area)); then best="$w"; best_area=$area; fi
    done
    [[ -n "$best" ]] && { printf '%s\n' "$best"; return 0; }
    sleep .4
  done
  return 1
}

socket_state() {
python3 - "$pid" "$TRACK_WARP_PORT" <<'PY'
import os,pathlib,sys
pid,port=sys.argv[1],int(sys.argv[2]); ino=set()
for fd in pathlib.Path('/proc',pid,'fd').iterdir():
    try:t=os.readlink(fd)
    except OSError:continue
    if t.startswith('socket:['):ino.add(t[8:-1])
local=direct=udp=0
for name,is_udp in [('tcp',0),('tcp6',0),('udp',1),('udp6',1)]:
    try:rows=pathlib.Path('/proc',pid,'net',name).read_text().splitlines()[1:]
    except OSError:continue
    for row in rows:
        c=row.split()
        if len(c)<10 or c[9] not in ino:continue
        rp=int(c[2].rsplit(':',1)[1],16)
        if is_udp:udp+=1
        elif c[3]=='01':
            if rp==port:local+=1
            else:direct+=1
print(local,direct,udp)
PY
}

window="$(resolve_window)"
"$toolroot/usr/bin/xdotool" windowactivate --sync "$window" 2>/dev/null || true
"$toolroot/usr/bin/xdotool" windowfocus --sync "$window"
# Account-login bootstrap only; no OCR/image interpretation.
"$toolroot/usr/bin/xdotool" mousemove --window "$window" 535 275 click 1
"$toolroot/usr/bin/xdotool" key --window "$window" ctrl+a
"$toolroot/usr/bin/xdotool" type --window "$window" --delay 12 -- "$TIBIA_TEST_EMAIL"
"$toolroot/usr/bin/xdotool" mousemove --window "$window" 535 304 click 1
"$toolroot/usr/bin/xdotool" key --window "$window" ctrl+a
"$toolroot/usr/bin/xdotool" type --window "$window" --delay 12 -- "$TIBIA_TEST_PASSWORD"
"$toolroot/usr/bin/xdotool" mousemove --window "$window" 590 388 click 1
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
echo TRACK_A_ACCOUNT_LOGIN_SUBMITTED=true

sleep 8
kill -0 "$pid"
window="$(resolve_window)"
"$toolroot/usr/bin/xdotool" windowactivate --sync "$window" 2>/dev/null || true
"$toolroot/usr/bin/xdotool" windowfocus --sync "$window"
# Historical first-character activation, with its bounded double-click fallback.
"$toolroot/usr/bin/xdotool" mousemove --window "$window" 285 193 click 1
sleep .4
"$toolroot/usr/bin/xdotool" key --window "$window" Return
echo TRACK_A_FIRST_CHARACTER_RETURN_SENT=true
sleep 3
if kill -0 "$pid" 2>/dev/null; then
  window="$(resolve_window || true)"
  [[ -z "$window" ]] || "$toolroot/usr/bin/xdotool" mousemove --window "$window" 285 193 click --repeat 2 --delay 160 1 || true
  echo TRACK_A_FIRST_CHARACTER_DOUBLECLICK_FALLBACK_SENT=true
fi

sustained=0; consecutive=0; max_local=0
for _ in $(seq 1 45); do
  sleep 1
  kill -0 "$pid"
  read -r local direct udp < <(socket_state)
  (( local > max_local )) && max_local=$local || true
  [[ "$direct" == 0 && "$udp" == 0 ]]
  if (( local >= 2 )); then consecutive=$((consecutive+1)); else consecutive=0; fi
  if (( consecutive >= 6 )); then sustained=1; break; fi
done
echo TRACK_A_LOCAL_SOCKS_MAX="$max_local"
echo TRACK_A_SUSTAINED_TUNNELED_SESSION="$sustained"
[[ "$sustained" == 1 ]]
grep -azFxq "$marker" "/proc/$pid/environ"
kill -0 "$pid"
echo TRACK_A_SESSION_LEFT_LOGGED_IN=true
