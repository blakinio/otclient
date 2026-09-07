#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${RUNNER_NAME:?RUNNER_NAME is required}"
: "${TIBIA_TEST_EMAIL:?TIBIA_TEST_EMAIL is required}"
: "${TIBIA_TEST_PASSWORD:?TIBIA_TEST_PASSWORD is required}"

[[ "$RUNNER_NAME" == "synology-otclient-01" ]]
command -v docker >/dev/null

CONTAINER="otclient-tibia-global-login-lab"
STATE_VOLUME="otclient-tibia-global-login-state"
RUNTIME_VOLUME="otclient-tibia-global-login-runtime"
IMAGE="ghcr.io/blakinio/otclient:latest"
TASK="OTC-20260813-tibia-global-login-lab"
ASSET_BASE="https://static.tibia.com/launcher/assets-current"
CLIENT_VERSION_STRING="15.32.bf29ac"
WGCF_VERSION="2.2.32"
WGCF_SHA256="2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c"
WIREPROXY_VERSION="1.1.3"
WIREPROXY_SHA256="e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c"

for volume in "$STATE_VOLUME" "$RUNTIME_VOLUME"; do
  docker volume inspect "$volume" >/dev/null
  owner=$(docker volume inspect --format '{{ index .Labels "com.blakinio.owner" }}' "$volume")
  task=$(docker volume inspect --format '{{ index .Labels "com.blakinio.task" }}' "$volume")
  [[ "$owner" == "otclient" && "$task" == "$TASK" ]]
done

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  timeout 240 docker pull "$IMAGE" >/dev/null
fi

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" --network bridge --user root \
  --label com.blakinio.owner=otclient \
  --label com.blakinio.repository=blakinio/otclient \
  --label com.blakinio.task="$TASK" \
  --label com.blakinio.purpose=tibia-global-login-lab \
  --mount "type=volume,src=$STATE_VOLUME,dst=/lab/state" \
  --mount "type=volume,src=$RUNTIME_VOLUME,dst=/lab/runtime" \
  "$IMAGE" sleep infinity >/dev/null

owner=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.owner" }}' "$CONTAINER")
task=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.task" }}' "$CONTAINER")
[[ "$owner" == "otclient" && "$task" == "$TASK" ]]

docker exec "$CONTAINER" bash -lc '
  set -Eeuo pipefail
  export DEBIAN_FRONTEND=noninteractive
  missing=0
  for cmd in curl python3 Xvfb xdpyinfo pgrep ss proxychains4 tar; do command -v "$cmd" >/dev/null 2>&1 || missing=1; done
  if [[ "$missing" -eq 1 ]]; then
    apt-get update -qq
    apt-get install -y --no-install-recommends curl python3 xvfb x11-utils procps iproute2 ca-certificates proxychains4 tar >/dev/null
  fi
  ! command -v tesseract >/dev/null 2>&1
'
echo LAB_OCR_BINARY_ABSENT=true

# Migrate the proven PR #48 userspace-WARP pattern into this lab-owned persistent volume.
docker exec \
  -e WGCF_VERSION="$WGCF_VERSION" \
  -e WGCF_SHA256="$WGCF_SHA256" \
  -e WIREPROXY_VERSION="$WIREPROXY_VERSION" \
  -e WIREPROXY_SHA256="$WIREPROXY_SHA256" \
  "$CONTAINER" bash -lc '
set -Eeuo pipefail
root=/lab/state/userspace-warp
bin="$root/bin"
state="$root/state"
mkdir -p "$bin" "$state"
chmod 700 "$root" "$state"

cd "$bin"
if [[ ! -x wgcf ]] || ! printf "%s  wgcf\n" "$WGCF_SHA256" | sha256sum -c - >/dev/null 2>&1; then
  rm -f wgcf
  curl -fL --retry 3 --retry-all-errors --connect-timeout 10 --max-time 180 \
    -o wgcf "https://github.com/ViRb3/wgcf/releases/download/v${WGCF_VERSION}/wgcf_${WGCF_VERSION}_linux_amd64"
  printf "%s  wgcf\n" "$WGCF_SHA256" | sha256sum -c -
  chmod 755 wgcf
fi

if [[ ! -x wireproxy ]]; then
  rm -f wireproxy wireproxy.tar.gz
  curl -fL --retry 3 --retry-all-errors --connect-timeout 10 --max-time 180 \
    -o wireproxy.tar.gz "https://github.com/windtf/wireproxy/releases/download/v${WIREPROXY_VERSION}/wireproxy_linux_amd64.tar.gz"
  printf "%s  wireproxy.tar.gz\n" "$WIREPROXY_SHA256" | sha256sum -c -
  rm -rf wireproxy-extract
  mkdir wireproxy-extract
  tar -xzf wireproxy.tar.gz -C wireproxy-extract
  wp=$(find wireproxy-extract -type f -name wireproxy -print -quit)
  [[ -n "$wp" ]]
  cp "$wp" wireproxy
  chmod 755 wireproxy
fi

echo LAB_WARP_TOOLING_VERIFIED=true

cd "$state"
if [[ ! -s wgcf-account.toml ]]; then
  "$bin/wgcf" register --accept-tos >/dev/null
fi
chmod 600 wgcf-account.toml
"$bin/wgcf" generate >/dev/null
chmod 600 wgcf-profile.conf
cat >wireproxy.conf <<EOF
WGConfig = $state/wgcf-profile.conf

[Socks5]
BindAddress = 127.0.0.1:25344
EOF
chmod 600 wireproxy.conf
"$bin/wireproxy" -n -c "$state/wireproxy.conf"
pkill -f "/wireproxy .*wireproxy.conf" 2>/dev/null || true
nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null &

ready=0
for _ in $(seq 1 30); do
  if curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/warp-trace 2>/dev/null; then
    ready=1
    break
  fi
  sleep 2
done
[[ "$ready" == 1 ]]
direct_ip=$(curl -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace | sed -n "s/^ip=//p")
warp_ip=$(sed -n "s/^ip=//p" /tmp/warp-trace)
warp_state=$(sed -n "s/^warp=//p" /tmp/warp-trace)
[[ -n "$direct_ip" && -n "$warp_ip" && "$direct_ip" != "$warp_ip" ]]
[[ "$warp_state" == on || "$warp_state" == plus ]]
echo LAB_WARP_CHANGED_EGRESS_VERIFIED=true
'

# Proxychains is used for the OTClient process itself; asset retrieval explicitly uses the same SOCKS endpoint.
docker exec "$CONTAINER" bash -lc 'cat >/lab/runtime/proxychains.conf <<EOF
strict_chain
proxy_dns
quiet_mode
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 25344
EOF
chmod 600 /lab/runtime/proxychains.conf'

# Fetch and verify only the current catalog files required by OTClient, through verified WARP egress.
docker exec -e ASSET_BASE="$ASSET_BASE" -i "$CONTAINER" python3 - <<'PY'
import hashlib,json,lzma,os,pathlib,subprocess,tempfile,urllib.parse
base=os.environ['ASSET_BASE'].rstrip('/')
out=pathlib.Path('/lab/state/things/1532')
out.mkdir(parents=True,exist_ok=True)
def get(url,path):
    subprocess.run(['curl','--socks5-hostname','127.0.0.1:25344','-fsSL','--retry','3','--retry-all-errors','--connect-timeout','15','--max-time','180',url,'-o',str(path)],check=True)
manifest=pathlib.Path('/tmp/assets.json'); get(base+'/assets.json',manifest); doc=json.loads(manifest.read_text())
rows=[]
def walk(v):
    if isinstance(v,dict):
        if isinstance(v.get('url'),str) and isinstance(v.get('packedhash'),str): rows.append((v['url'],v['packedhash'].lower(),str(v.get('unpackedhash') or '').lower()))
        for x in v.values(): walk(x)
    elif isinstance(v,list):
        for x in v: walk(x)
walk(doc)
def decode(data,rel,unpacked):
    if not unpacked or not rel.endswith('.lzma'): return data,rel
    if hashlib.sha256(data).hexdigest()==unpacked: return data,rel[:-5]
    if len(data)<45: raise RuntimeError('short lzma')
    prop=data[32]; lc=prop%9; rest=prop//9; lp=rest%5; pb=rest//5; ds=int.from_bytes(data[33:37],'little')
    filt={'id':lzma.FILTER_LZMA1,'dict_size':ds,'lc':lc,'lp':lp,'pb':pb}
    return lzma.decompress(data[45:],format=lzma.FORMAT_RAW,filters=[filt]),rel[:-5]
def fetch(row):
    rel,packed,unpacked=row
    with tempfile.NamedTemporaryFile(delete=False) as f: tmp=pathlib.Path(f.name)
    try:
        get(base+'/'+urllib.parse.quote(rel,safe='/._-~'),tmp); data=tmp.read_bytes()
        if hashlib.sha256(data).hexdigest()!=packed: raise RuntimeError('packed hash mismatch')
        raw,final=decode(data,rel,unpacked)
        if unpacked and hashlib.sha256(raw).hexdigest()!=unpacked: raise RuntimeError('unpacked hash mismatch')
        return raw,final
    finally: tmp.unlink(missing_ok=True)
catrow=next((r for r in rows if r[0].endswith('catalog-content.json') or r[0].endswith('catalog-content.json.lzma')),None)
if not catrow: raise RuntimeError('catalog-content row absent')
catraw,_=fetch(catrow); (out/'catalog-content.json').write_bytes(catraw); catalog=json.loads(catraw)
wanted={o['file'] for o in catalog if isinstance(o,dict) and o.get('type') in {'appearances','staticdata','sprite','proficiencies'} and isinstance(o.get('file'),str)}
mapping={}
for r in rows:
    rel=r[0][:-5] if r[0].endswith('.lzma') and r[2] else r[0]
    key=rel.rsplit('/',1)[-1]
    if key in wanted and key not in mapping: mapping[key]=r
missing=wanted-set(mapping)
if missing: raise RuntimeError(f'required catalog assets missing: {len(missing)}')
for name in sorted(wanted): (out/name).write_bytes(fetch(mapping[name])[0])
sha=out/'assets.json.sha256'; get(base+'/assets.json.sha256',sha)
print('LAB_ASSET_FILE_COUNT='+str(len(wanted)))
print('LAB_ASSETS_READY=true')
PY

ASSET_VERSION=$(docker exec "$CONTAINER" bash -lc "tr -d '\\r\\n ' </lab/state/things/1532/assets.json.sha256")
[[ -n "$ASSET_VERSION" ]]

# Keep proprietary asset bytes in the runner-local lab volume only.
docker exec "$CONTAINER" bash -lc 'rm -rf /otclient/data/things/1532 && mkdir -p /otclient/data/things/1532 && cp -a /lab/state/things/1532/. /otclient/data/things/1532/'

docker cp init.lua "$CONTAINER:/lab/runtime/init.lua"
docker exec "$CONTAINER" bash -lc 'cp /lab/runtime/init.lua /otclient/init.lua && chmod 600 /lab/runtime/init.lua'

docker exec "$CONTAINER" bash -lc "cat >>/otclient/init.lua <<'LUA'
if os.getenv('OTCLIENT_TIBIA_GLOBAL_LAB') == '1' then
  if Services and Services.clientAssets then Services.clientAssets.enabled = false end
  if HTTP then HTTP.timeout = 20 end
  local function mark(s) g_logger.info('[TIBIA_GLOBAL_LAB] ' .. s) end
  connect(g_game, {
    onGameStart=function() mark('GAME_START=true') end,
    onLoginError=function() mark('GAME_LOGIN_ERROR=true') end,
    onConnectionError=function() mark('GAME_CONNECTION_ERROR=true') end,
    onSessionEnd=function() mark('GAME_SESSION_END=true') end,
    onUpdateNeeded=function() mark('GAME_UPDATE_NEEDED=true') end
  })
  scheduleEvent(function()
    local email=os.getenv('TIBIA_TEST_EMAIL') or ''
    local password=os.getenv('TIBIA_TEST_PASSWORD') or ''
    local assetversion=os.getenv('TIBIA_ASSET_VERSION') or ''
    local clientversion=os.getenv('TIBIA_CLIENT_VERSION_STRING') or ''
    if email=='' or password=='' then mark('SECRET_GATE_FAILED=true'); g_app.exit(); return end
    if assetversion=='' or clientversion=='' then mark('IDENTIFIER_GATE_FAILED=true'); g_app.exit(); return end
    G.account=email
    G.password=password
    G.host='https://www.tibia.com/clientservices/loginservice.php'
    G.port=443
    G.clientVersion=1532
    G.requestId=1
    g_game.setClientVersion(1532)
    g_game.setProtocolVersion(g_game.getClientProtocolVersion(1532))
    local payload={email=email,password=password,stayloggedin=false,type='login',clientversion=clientversion,clienttype=2,assetversion=assetversion,devicecookie=''}
    email=nil; password=nil
    mark('HTTP_LOGIN_START=true')
    HTTP.postJSON('https://www.tibia.com/clientservices/loginservice.php', payload, function(response, err)
      payload=nil
      if err then mark('HTTP_TRANSPORT_ERROR=true'); return end
      if type(response)~='table' then mark('HTTP_RESPONSE_INVALID=true'); return end
      if response.errorCode and tonumber(response.errorCode)~=0 then mark('HTTP_LOGIN_REJECTED=true'); return end
      if type(response.session)~='table' or type(response.playdata)~='table' or type(response.playdata.worlds)~='table' or type(response.playdata.characters)~='table' then mark('HTTP_RESPONSE_INCOMPLETE=true'); return end
      mark('HTTP_LOGIN_SUCCESS=true')
      EnterGame.loginSuccess(1, json.encode(response.session), json.encode(response.playdata.worlds), json.encode(response.playdata.characters))
      response=nil
      scheduleEvent(function()
        if CharacterList and CharacterList.doLogin then mark('CHARACTER_LOGIN_ATTEMPT=true'); CharacterList.doLogin()
        else mark('CHARACTER_LIST_UNAVAILABLE=true') end
      end,1000)
    end)
  end,1500)
  scheduleEvent(function() if not g_game.isOnline() then mark('PROBE_TIMEOUT=true'); g_app.exit() end end,70000)
end
LUA"

docker exec "$CONTAINER" bash -lc ': >/lab/runtime/otclient.stdout.log; nohup Xvfb :100 -screen 0 1280x800x24 -nolisten tcp >/lab/runtime/xvfb.log 2>&1 </dev/null &'
for _ in $(seq 1 30); do docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null 2>&1 && break; sleep 1; done
docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null

docker exec -d \
  -e DISPLAY=:100 \
  -e HOME=/lab/state/home \
  -e LIBGL_ALWAYS_SOFTWARE=1 \
  -e OTCLIENT_TIBIA_GLOBAL_LAB=1 \
  -e TIBIA_TEST_EMAIL \
  -e TIBIA_TEST_PASSWORD \
  -e TIBIA_ASSET_VERSION="$ASSET_VERSION" \
  -e TIBIA_CLIENT_VERSION_STRING="$CLIENT_VERSION_STRING" \
  "$CONTAINER" bash -lc 'cd /otclient && exec proxychains4 -f /lab/runtime/proxychains.conf ./otclient >>/lab/runtime/otclient.stdout.log 2>&1'
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD ASSET_VERSION

for _ in $(seq 1 180); do
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_START=true' /lab/runtime/otclient.stdout.log && break
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] PROBE_TIMEOUT=true' /lab/runtime/otclient.stdout.log && break
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_LOGIN_REJECTED=true' /lab/runtime/otclient.stdout.log && break
  docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_TRANSPORT_ERROR=true' /lab/runtime/otclient.stdout.log && break
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

if docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] GAME_START=true' /lab/runtime/otclient.stdout.log; then
  echo TIBIA_GLOBAL_LAB_GAME_START_PROVEN=true
  exit 0
fi

echo TIBIA_GLOBAL_LAB_GAME_START_PROVEN=false
if docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_LOGIN_SUCCESS=true' /lab/runtime/otclient.stdout.log; then
  echo FAILURE_STAGE=after_http_login_before_game_start
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_LOGIN_REJECTED=true' /lab/runtime/otclient.stdout.log; then
  echo FAILURE_STAGE=http_login_rejected
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_TRANSPORT_ERROR=true' /lab/runtime/otclient.stdout.log; then
  echo FAILURE_STAGE=http_transport
elif docker exec "$CONTAINER" grep -q '\[TIBIA_GLOBAL_LAB\] HTTP_LOGIN_START=true' /lab/runtime/otclient.stdout.log; then
  echo FAILURE_STAGE=http_login_no_callback
else
  echo FAILURE_STAGE=before_http_login
fi
exit 1
