#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${RUNNER_NAME:?RUNNER_NAME is required}"
: "${TIBIA_TEST_EMAIL:?TIBIA_TEST_EMAIL is required}"
: "${TIBIA_TEST_PASSWORD:?TIBIA_TEST_PASSWORD is required}"
[[ "$RUNNER_NAME" == "synology-otclient-01" ]]

CONTAINER=otclient-tibia-global-login-lab
STATE_VOLUME=otclient-tibia-global-login-state
RUNTIME_VOLUME=otclient-tibia-global-login-runtime
IMAGE=otclient-tibia-global-login-lab-runtime:local
TASK=OTC-20260813-tibia-global-login-lab

docker volume inspect "$STATE_VOLUME" >/dev/null
docker image inspect "$IMAGE" >/dev/null

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" --network bridge --user root \
  --label com.blakinio.owner=otclient \
  --label com.blakinio.repository=blakinio/otclient \
  --label com.blakinio.task="$TASK" \
  --label com.blakinio.purpose=tibia-global-login-lab \
  --mount "type=volume,src=$STATE_VOLUME,dst=/lab/state" \
  --mount "type=volume,src=$RUNTIME_VOLUME,dst=/lab/runtime" \
  "$IMAGE" sleep infinity >/dev/null

asset_count=$(docker exec "$CONTAINER" bash -lc 'find /lab/state/things/1532 -maxdepth 1 -type f | wc -l')
[[ "$asset_count" -ge 5088 ]]
docker exec "$CONTAINER" bash -lc 'test -s /lab/state/things/1532/catalog-content.json; rm -rf /otclient/data/things/1532; mkdir -p /otclient/data/things/1532; cp -a /lab/state/things/1532/. /otclient/data/things/1532/'
echo LAB_REUSED_VERIFIED_ASSETS=true

docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
root=/lab/state/userspace-warp
bin="$root/bin"
state="$root/state"
[[ -x "$bin/wireproxy" && -s "$state/wireproxy.conf" ]]
"$bin/wireproxy" -n -c "$state/wireproxy.conf"
if [[ -s "$root/wireproxy.pid" ]]; then oldpid=$(cat "$root/wireproxy.pid"); kill "$oldpid" 2>/dev/null || true; fi
nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null &
echo $! >"$root/wireproxy.pid"
for _ in $(seq 1 30); do curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/lab-warp.trace 2>/dev/null && break; sleep 2; done
direct=$(curl -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace | sed -n "s/^ip=//p")
warp=$(sed -n "s/^ip=//p" /tmp/lab-warp.trace)
statev=$(sed -n "s/^warp=//p" /tmp/lab-warp.trace)
[[ -n "$direct" && -n "$warp" && "$direct" != "$warp" ]]
[[ "$statev" == on || "$statev" == plus ]]
echo LAB_WARP_CHANGED_EGRESS_VERIFIED=true
'

cat > /tmp/lab-proxychains.conf <<'EOF'
strict_chain
proxy_dns
quiet_mode
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 25344
EOF
docker cp /tmp/lab-proxychains.conf "$CONTAINER:/lab/runtime/proxychains.conf"

cp init.lua /tmp/lab-init.lua
cat >>/tmp/lab-init.lua <<'LUA'
if os.getenv('OTCLIENT_TIBIA_GLOBAL_LAB') == '1' then
  if Services and Services.clientAssets then Services.clientAssets.enabled = false end
  local function mark(s) g_logger.info('[TIBIA_GLOBAL_LAB] ' .. s) end
  connect(g_game, {
    onGameStart=function() mark('GAME_START=true') end,
    onLoginError=function() mark('GAME_LOGIN_ERROR=true') end,
    onConnectionError=function() mark('GAME_CONNECTION_ERROR=true') end,
    onSessionEnd=function() mark('GAME_SESSION_END=true') end,
    onUpdateNeeded=function() mark('GAME_UPDATE_NEEDED=true') end
  })
  local success=EnterGame.loginSuccess
  EnterGame.loginSuccess=function(requestId,jsonSession,jsonWorlds,jsonCharacters)
    mark('HTTP_LOGIN_SUCCESS=true')
    success(requestId,jsonSession,jsonWorlds,jsonCharacters)
    scheduleEvent(function()
      if CharacterList and CharacterList.doLogin then
        mark('CHARACTER_LOGIN_ATTEMPT=true')
        CharacterList.doLogin()
      else
        mark('CHARACTER_LIST_UNAVAILABLE=true')
      end
    end,1000)
  end
  local failed=EnterGame.loginFailed
  EnterGame.loginFailed=function(requestId,msg,result)
    mark('HTTP_LOGIN_FAILED=true')
    failed(requestId,msg,result)
  end
  scheduleEvent(function()
    local email=os.getenv('TIBIA_TEST_EMAIL') or ''
    local password=os.getenv('TIBIA_TEST_PASSWORD') or ''
    if email=='' or password=='' then mark('SECRET_GATE_FAILED=true'); return end
    EnterGame.setDefaultServer('https://www.tibia.com/clientservices/loginservice.php',443,1532)
    local a=rootWidget:recursiveGetChildById('accountNameTextEdit')
    local p=rootWidget:recursiveGetChildById('accountPasswordTextEdit')
    local h=rootWidget:recursiveGetChildById('httpLoginBox')
    local stay=rootWidget:recursiveGetChildById('stayLoggedBox')
    if not a or not p or not h then mark('LOGIN_WIDGETS_UNAVAILABLE=true'); return end
    a:setText(email); p:setText(password); h:setChecked(true); if stay then stay:setChecked(false) end
    email=nil; password=nil
    mark('LOGIN_START=true')
    EnterGame.doLogin()
  end,1500)
  scheduleEvent(function() if not g_game.isOnline() then mark('PROBE_TIMEOUT=true'); g_app.exit() end end,90000)
end
LUA
docker cp /tmp/lab-init.lua "$CONTAINER:/otclient/init.lua"
docker exec "$CONTAINER" chmod 600 /otclient/init.lua

docker exec "$CONTAINER" bash -lc ': >/lab/runtime/otclient.stdout.log; nohup Xvfb :100 -screen 0 1280x800x24 -nolisten tcp >/lab/runtime/xvfb.log 2>&1 </dev/null &'
for _ in $(seq 1 30); do docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null 2>&1 && break; sleep 1; done
docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null

docker exec -d -e DISPLAY=:100 -e HOME=/lab/state/home -e LIBGL_ALWAYS_SOFTWARE=1 \
  -e OTCLIENT_TIBIA_GLOBAL_LAB=1 -e TIBIA_TEST_EMAIL -e TIBIA_TEST_PASSWORD \
  "$CONTAINER" bash -lc 'cd /otclient && exec proxychains4 -f /lab/runtime/proxychains.conf ./otclient >>/lab/runtime/otclient.stdout.log 2>&1'
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD

for _ in $(seq 1 220); do
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_START=true' /lab/runtime/otclient.stdout.log && break
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] PROBE_TIMEOUT=true' /lab/runtime/otclient.stdout.log && break
  docker exec "$CONTAINER" pgrep -f '/otclient/otclient|./otclient' >/dev/null 2>&1 || break
  sleep 0.5
done

docker exec "$CONTAINER" bash -lc "grep -o '\[TIBIA_GLOBAL_LAB\] [A-Z_]*=true' /lab/runtime/otclient.stdout.log | sort -u || true"
pid=$(docker exec "$CONTAINER" pgrep -f '/otclient/otclient|./otclient' | head -n1 || true)
if [[ -n "$pid" ]]; then
  rows=$(docker exec "$CONTAINER" ss -ntp 2>/dev/null | grep "pid=$pid," || true)
  direct=$(printf '%s\n' "$rows" | awk '{print $5}' | grep -Ev '^(127\.0\.0\.1|\[::1\]):25344$' | grep -c . || true)
  echo "LAB_OTCLIENT_DIRECT_TCP_COUNT=$direct"
  [[ "$direct" -eq 0 ]]
fi

if docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_START=true' /lab/runtime/otclient.stdout.log; then echo TIBIA_GLOBAL_LAB_GAME_START_PROVEN=true; exit 0; fi

echo TIBIA_GLOBAL_LAB_GAME_START_PROVEN=false
if docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_LOGIN_SUCCESS=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=after_http_login_before_game_start
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_LOGIN_FAILED=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=http_login_rejected
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] LOGIN_START=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=http_login_no_success_callback
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] LOGIN_WIDGETS_UNAVAILABLE=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=login_widgets_unavailable
else echo FAILURE_STAGE=before_login_start; fi
exit 1
