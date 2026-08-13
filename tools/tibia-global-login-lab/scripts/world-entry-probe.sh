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
CLIENT_VERSION_STRING=15.32.df7b29

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
  --tmpfs /lab/secrets:rw,noexec,nosuid,nodev,size=2m,mode=0700 \
  "$IMAGE" sleep infinity >/dev/null

cleanup_secrets() {
  docker exec "$CONTAINER" sh -c 'rm -f /lab/secrets/*' >/dev/null 2>&1 || true
}
trap cleanup_secrets EXIT

asset_count=$(docker exec "$CONTAINER" bash -lc 'find /lab/state/things/1532 -maxdepth 1 -type f | wc -l')
[[ "$asset_count" -ge 5088 ]]
docker exec "$CONTAINER" bash -lc 'test -s /lab/state/things/1532/catalog-content.json; rm -rf /otclient/data/things/1532; mkdir -p /otclient/data/things/1532; cp -a /lab/state/things/1532/. /otclient/data/things/1532/'
ASSET_VERSION=$(docker exec "$CONTAINER" bash -lc "awk 'NR==1{print \$1}' /lab/state/things/1532/assets.json.sha256")
[[ "$ASSET_VERSION" =~ ^[0-9a-fA-F]{64}$ ]]
echo LAB_REUSED_VERIFIED_ASSETS=true
echo LAB_ASSET_VERSION_READY=true

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
localnet 127.0.0.0/255.0.0.0
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 25344
EOF
docker cp /tmp/lab-proxychains.conf "$CONTAINER:/lab/runtime/proxychains.conf"
rm -f /tmp/lab-proxychains.conf

# Authenticate through the already-proven userspace-WARP path. The complete
# official response and the reduced game-session handoff live only in tmpfs.
docker exec -i \
  -e TIBIA_TEST_EMAIL -e TIBIA_TEST_PASSWORD \
  -e TIBIA_ASSET_VERSION="$ASSET_VERSION" \
  -e TIBIA_CLIENT_VERSION_STRING="$CLIENT_VERSION_STRING" \
  "$CONTAINER" python3 - <<'PY'
import json
import os
from pathlib import Path

payload = {
    "email": os.environ["TIBIA_TEST_EMAIL"],
    "password": os.environ["TIBIA_TEST_PASSWORD"],
    "stayloggedin": True,
    "type": "login",
    "clientversion": os.environ["TIBIA_CLIENT_VERSION_STRING"],
    "clienttype": 2,
    "assetversion": os.environ["TIBIA_ASSET_VERSION"],
}
path = Path('/lab/secrets/login-request.json')
path.write_text(json.dumps(payload, separators=(',', ':')), encoding='utf-8')
path.chmod(0o600)
PY

http_status=$(docker exec "$CONTAINER" bash -lc \
  "curl --socks5-hostname 127.0.0.1:25344 --compressed -sS --connect-timeout 15 --max-time 60 -A 'Mozilla/5.0' -H 'Content-Type: application/json' -H 'Accept: */*' --data-binary @/lab/secrets/login-request.json -o /lab/secrets/login-response.json -w '%{http_code}' https://www.tibia.com/clientservices/loginservice.php")
[[ "$http_status" == "200" ]]
echo LAB_TRANSIENT_HTTP_LOGIN_STATUS_200=true

docker exec "$CONTAINER" python3 - <<'PY'
import json
import os
from pathlib import Path

response_path = Path('/lab/secrets/login-response.json')
request_path = Path('/lab/secrets/login-request.json')
handoff_path = Path('/lab/secrets/login-handoff.json')

doc = json.loads(response_path.read_text(encoding='utf-8'))
if doc.get('errorCode') not in (None, 0):
    raise SystemExit('official login response rejected')

session = doc.get('session')
playdata = doc.get('playdata')
worlds = playdata.get('worlds') if isinstance(playdata, dict) else None
characters = playdata.get('characters') if isinstance(playdata, dict) else None
if not isinstance(session, dict) or not isinstance(worlds, list) or not worlds or not isinstance(characters, list) or not characters:
    raise SystemExit('official login response missing session/world/character data')

session_key = session.get('sessionkey')
if not isinstance(session_key, str) or not session_key:
    raise SystemExit('official login response missing session key')

world_by_id = {str(world.get('id')): world for world in worlds if isinstance(world, dict)}
character = next((c for c in characters if isinstance(c, dict) and c.get('ismaincharacter') is True), None)
if character is None:
    character = next((c for c in characters if isinstance(c, dict)), None)
if not character:
    raise SystemExit('official login response has no usable character')

world = world_by_id.get(str(character.get('worldid')))
if not isinstance(world, dict):
    raise SystemExit('character world id has no matching world')

world_name = world.get('name')
world_host = world.get('externaladdressprotected')
world_port = world.get('externalportprotected')
character_name = character.get('name')
if not isinstance(world_name, str) or not world_name:
    raise SystemExit('world name missing')
if not isinstance(world_host, str) or not world_host:
    raise SystemExit('protected world address missing')
try:
    world_port = int(world_port)
except (TypeError, ValueError):
    raise SystemExit('protected world port invalid')
if not (1 <= world_port <= 65535):
    raise SystemExit('protected world port out of range')
if not isinstance(character_name, str) or not character_name:
    raise SystemExit('character name missing')

handoff = {
    'sessionKey': session_key,
    'worldName': world_name,
    'worldHost': world_host,
    'worldPort': world_port,
    'characterName': character_name,
}
handoff_path.write_text(json.dumps(handoff, separators=(',', ':')), encoding='utf-8')
handoff_path.chmod(0o600)
request_path.unlink(missing_ok=True)
response_path.unlink(missing_ok=True)

print('LAB_TRANSIENT_LOGIN_RESPONSE_VALID=true')
print('LAB_TRANSIENT_WORLD_COUNT=' + str(len(worlds)))
print('LAB_TRANSIENT_CHARACTER_COUNT=' + str(len(characters)))
print('LAB_TRANSIENT_GAME_HANDOFF_READY=true')
PY
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD ASSET_VERSION

docker exec "$CONTAINER" bash -lc 'test "$(stat -c %a /lab/secrets/login-handoff.json)" = 600'

docker exec -i "$CONTAINER" python3 - <<'PY'
import json
import subprocess

with open('/lab/secrets/login-handoff.json', 'r', encoding='utf-8') as handle:
    handoff = json.load(handle)

target = f"telnet://{handoff['worldHost']}:{int(handoff['worldPort'])}"
probe = subprocess.run(
    [
        'curl', '--silent', '--show-error', '--verbose', '--socks5-hostname', '127.0.0.1:25344',
        '--connect-timeout', '15', '--max-time', '20', target,
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)
granted = 'SOCKS5 request granted' in probe.stderr or 'Connected to ' in probe.stderr
print(f"LAB_GAME_TCP_VIA_WARP_SOCKS_GRANTED={'true' if granted else 'false'}")
PY

docker cp tools/tibia-global-login-lab/scripts/game-socks-forward.py "$CONTAINER:/lab/runtime/game-socks-forward.py"
docker exec "$CONTAINER" bash -lc '
  chmod 700 /lab/runtime/game-socks-forward.py
  rm -f /lab/runtime/game-socks-forward.ready /lab/runtime/game-socks-forward.granted
  nohup python3 /lab/runtime/game-socks-forward.py >/dev/null 2>&1 </dev/null &
  echo $! >/lab/runtime/game-socks-forward.pid
'
forward_ready=false
for _ in $(seq 1 30); do
  if docker exec "$CONTAINER" test -f /lab/runtime/game-socks-forward.ready; then forward_ready=true; break; fi
  sleep 0.2
done
echo "LAB_GAME_SOCKS_FORWARD_READY=$forward_ready"
[[ "$forward_ready" == true ]]

cp init.lua /tmp/lab-init.lua
cat >>/tmp/lab-init.lua <<'LUA'
if os.getenv('OTCLIENT_TIBIA_GLOBAL_LAB') == '1' then
  if Services and Services.clientAssets then Services.clientAssets.enabled = false end
  local function mark(s) g_logger.info('[TIBIA_GLOBAL_LAB] ' .. s) end

  connect(g_game, {
    onLogin=function() mark('GAME_LOGIN=true') end,
    onPendingGame=function() mark('GAME_PENDING=true') end,
    onEnterGame=function() mark('GAME_ENTER=true') end,
    onGameStart=function() mark('GAME_START=true') end,
    onLoginWait=function() mark('GAME_LOGIN_WAIT=true') end,
    onLoginError=function() mark('GAME_LOGIN_ERROR=true') end,
    onConnectionError=function(_, code)
      mark('GAME_CONNECTION_ERROR=true')
      mark('GAME_CONNECTION_ERROR_CODE_' .. tostring(tonumber(code) or -1) .. '=true')
    end,
    onSessionEnd=function() mark('GAME_SESSION_END=true') end,
    onUpdateNeeded=function() mark('GAME_UPDATE_NEEDED=true') end
  })

  local function consumeHandoff()
    local file=io.open('/lab/secrets/login-handoff.json','rb')
    if not file then mark('HANDOFF_FILE_UNAVAILABLE=true'); return nil end
    local raw=file:read('*a')
    file:close()
    if not raw or raw=='' then mark('HANDOFF_FILE_EMPTY=true'); return nil end
    local ok,data=pcall(json.decode,raw)
    raw=nil
    if not ok or type(data)~='table' then mark('HANDOFF_JSON_INVALID=true'); return nil end
    if type(data.sessionKey)~='string' or data.sessionKey=='' or
       type(data.worldName)~='string' or data.worldName=='' or
       type(data.worldHost)~='string' or data.worldHost=='' or
       type(data.characterName)~='string' or data.characterName=='' or
       not tonumber(data.worldPort) then
      mark('HANDOFF_FIELDS_INVALID=true')
      return nil
    end
    os.remove('/lab/secrets/login-handoff.json')
    mark('HANDOFF_CONSUMED=true')
    return data
  end

  scheduleEvent(function()
    local handoff=consumeHandoff()
    if not handoff then return end

    g_game.setClientVersion(1532)
    g_game.setProtocolVersion(g_game.getClientProtocolVersion(1532))
    g_game.chooseRsa('www.tibia.com')

    if modules.game_things and modules.game_things.isLoaded and not modules.game_things.isLoaded() then
      handoff.sessionKey=nil
      mark('THINGS_NOT_LOADED=true')
      return
    end
    mark('THINGS_LOADED=true')

    if not g_game.getFeature(GameSessionKey) then
      handoff.sessionKey=nil
      mark('SESSION_KEY_FEATURE_MISSING=true')
      return
    end
    mark('SESSION_KEY_FEATURE=true')

    local sessionKey=handoff.sessionKey
    handoff.sessionKey=nil
    mark('CHARACTER_LOGIN_ATTEMPT=true')
    local ok=pcall(function()
      mark('GAME_SOCKS_FORWARD_SELECTED=true')
      g_game.loginWorld('', '', handoff.worldName, '127.0.0.1', 37171, handoff.characterName, '', sessionKey)
    end)
    sessionKey=nil
    handoff=nil
    if not ok then
      mark('CHARACTER_LOGIN_CALL_ERROR=true')
      return
    end
    mark('CHARACTER_LOGIN_CALL_RETURNED=true')
  end,1500)

  scheduleEvent(function()
    if not g_game.isOnline() then mark('PROBE_TIMEOUT=true'); g_app.exit() end
  end,120000)
end
LUA
docker cp /tmp/lab-init.lua "$CONTAINER:/otclient/init.lua"
rm -f /tmp/lab-init.lua
docker exec "$CONTAINER" chmod 600 /otclient/init.lua

docker exec "$CONTAINER" bash -lc ': >/lab/runtime/otclient.stdout.log; nohup Xvfb :100 -screen 0 1280x800x24 -nolisten tcp >/lab/runtime/xvfb.log 2>&1 </dev/null &'
for _ in $(seq 1 30); do docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null 2>&1 && break; sleep 1; done
docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null

docker exec -d -e DISPLAY=:100 -e HOME=/lab/state/home -e LIBGL_ALWAYS_SOFTWARE=1 \
  -e OTCLIENT_TIBIA_GLOBAL_LAB=1 \
  "$CONTAINER" bash -lc 'cd /otclient && exec proxychains4 -f /lab/runtime/proxychains.conf ./otclient >>/lab/runtime/otclient.stdout.log 2>&1'

client_started=false
for _ in $(seq 1 60); do
  if docker exec "$CONTAINER" pgrep -f '/otclient/otclient|./otclient' >/dev/null 2>&1; then client_started=true; break; fi
  sleep 0.5
done
echo "LAB_OTCLIENT_PROCESS_STARTED=$client_started"
[[ "$client_started" == true ]]

for _ in $(seq 1 300); do
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_START=true' /lab/runtime/otclient.stdout.log && break
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] PROBE_TIMEOUT=true' /lab/runtime/otclient.stdout.log && break
  docker exec "$CONTAINER" pgrep -f '/otclient/otclient|./otclient' >/dev/null 2>&1 || break
  sleep 0.5
done

docker exec "$CONTAINER" bash -lc "grep -o '\[TIBIA_GLOBAL_LAB\] [A-Z0-9_-]*=true' /lab/runtime/otclient.stdout.log | sort -u || true"
if docker exec "$CONTAINER" test -f /lab/runtime/game-socks-forward.granted; then
  echo LAB_GAME_SOCKS_FORWARD_GRANTED=true
else
  echo LAB_GAME_SOCKS_FORWARD_GRANTED=false
fi
pid=$(docker exec "$CONTAINER" pgrep -f '/otclient/otclient|./otclient' | head -n1 || true)
if [[ -n "$pid" ]]; then
  rows=$(docker exec "$CONTAINER" ss -ntp 2>/dev/null | grep "pid=$pid," || true)
  direct=$(printf '%s\n' "$rows" | awk '{print $5}' | grep -Ev '^(127\.0\.0\.1|\[::1\]):(25344|37171)$' | grep -c . || true)
  echo "LAB_OTCLIENT_DIRECT_TCP_COUNT=$direct"
  [[ "$direct" -eq 0 ]]
fi

cleanup_secrets
trap - EXIT

if docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_START=true' /lab/runtime/otclient.stdout.log; then
  echo TIBIA_GLOBAL_LAB_GAME_START_PROVEN=true
  exit 0
fi

echo TIBIA_GLOBAL_LAB_GAME_START_PROVEN=false
if docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_ENTER=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=after_game_enter_before_game_start
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_PENDING=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=after_pending_game_before_enter_game
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_LOGIN=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=after_game_login_before_pending_game
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_UPDATE_NEEDED=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=game_update_needed
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_LOGIN_ERROR=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=game_login_rejected
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_CONNECTION_ERROR=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=game_connection_error
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] CHARACTER_LOGIN_CALL_RETURNED=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=after_character_login_call_before_game_callback
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] CHARACTER_LOGIN_CALL_ERROR=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=character_login_call_error
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] SESSION_KEY_FEATURE_MISSING=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=session_key_feature_missing
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] THINGS_NOT_LOADED=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=things_not_loaded
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HANDOFF_CONSUMED=true' /lab/runtime/otclient.stdout.log; then echo FAILURE_STAGE=after_handoff_before_character_login
else echo FAILURE_STAGE=before_handoff_consumption; fi
exit 1
