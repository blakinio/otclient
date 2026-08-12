#!/usr/bin/env bash
set +x
set -Eeuo pipefail

SOURCE_CONTAINER=otclient-tibia-login-analysis
SOURCE_STATE=/var/lib/oteryn-staging-state/tibia-linux-analysis
PROBE_CONTAINER=otclient-global-login-probe
PROBE_STATE="$SOURCE_STATE/current/otclient-global-probe"
OTCLIENT_IMAGE=ghcr.io/blakinio/otclient:latest
ASSET_BASE=https://static.tibia.com/launcher/assets-current

[[ "$RUNNER_NAME" == "oteryn-synology-staging" ]]
[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]]
docker version >/dev/null
docker ps -a --filter 'label=com.docker.compose.project=oteryn-staging' --format '{{.ID}}\t{{.Names}}' | sort >/tmp/oteryn-before.tsv
test -s /tmp/oteryn-before.tsv
docker inspect "$SOURCE_CONTAINER" >/dev/null
[[ "$(docker inspect --format '{{ index .Config.Labels "com.blakinio.owner" }}' "$SOURCE_CONTAINER")" == otclient ]]
[[ "$(docker inspect --format '{{ index .Config.Labels "com.blakinio.task" }}' "$SOURCE_CONTAINER")" == OTC-20260727-tibia-linux-runner-analysis ]]
[[ "$(docker inspect --format '{{range .Mounts}}{{if eq .Destination "/analysis"}}{{.Source}}{{end}}{{end}}' "$SOURCE_CONTAINER")" == "$SOURCE_STATE" ]]
echo PROBE_PREFLIGHT_VERIFIED=true

docker start "$SOURCE_CONTAINER" >/dev/null 2>&1 || true
docker exec -i "$SOURCE_CONTAINER" bash <<'INNER'
set -Eeuo pipefail
root=/analysis/current/runtime/userspace-warp
cfg="$root/state/wireproxy.conf"
[[ -x "$root/bin/wireproxy" && -f "$cfg" ]]
if ! curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/otclient-probe-warp.trace 2>/dev/null; then
  pkill -f '/wireproxy .*wireproxy.conf' 2>/dev/null || true
  nohup "$root/bin/wireproxy" -c "$cfg" >"$root/wireproxy.log" 2>&1 </dev/null &
  for _ in $(seq 1 30); do
    curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/otclient-probe-warp.trace 2>/dev/null && break
    sleep 2
  done
fi
direct=$(curl -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace | sed -n 's/^ip=//p')
warp=$(sed -n 's/^ip=//p' /tmp/otclient-probe-warp.trace)
state=$(sed -n 's/^warp=//p' /tmp/otclient-probe-warp.trace)
[[ -n "$direct" && -n "$warp" && "$direct" != "$warp" ]]
[[ "$state" == on || "$state" == plus ]]
echo CHANGED_WARP_EGRESS_VERIFIED=true
INNER

# Materialize only assets OTClient needs; all bytes remain transient on task-owned runner state.
docker exec -e ASSET_BASE="$ASSET_BASE" -i "$SOURCE_CONTAINER" python3 - <<'PY'
import hashlib,json,lzma,os,pathlib,subprocess,tempfile,urllib.parse
base=os.environ['ASSET_BASE'].rstrip('/')
out=pathlib.Path('/analysis/current/otclient-global-probe/things/1532')
out.mkdir(parents=True,exist_ok=True)
for p in [out.parent.parent,out.parent,out]: os.chmod(p,0o755)
def get(url,path):
    subprocess.run(['curl','--socks5-hostname','127.0.0.1:25344','-fsSL','--retry','3','--retry-all-errors','--connect-timeout','15','--max-time','180',url,'-o',str(path)],check=True)
mp=pathlib.Path('/tmp/otclient-assets.json'); get(base+'/assets.json',mp); doc=json.loads(mp.read_text())
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
sha=out/'assets.json.sha256'
try: get(base+'/assets.json.sha256',sha)
except subprocess.CalledProcessError: sha.unlink(missing_ok=True)
print('OTCLIENT_CATALOG_FILE_COUNT='+str(len(wanted)))
print('OTCLIENT_REQUIRED_ASSETS_READY=true')
print('ASSET_IDENTIFIER_FILE_PRESENT='+str(sha.exists()).lower())
PY

mkdir -p "$PROBE_STATE/runtime" "$PROBE_STATE/home"
cp init.lua "$PROBE_STATE/runtime/init.lua"
cat >>"$PROBE_STATE/runtime/init.lua" <<'LUA'
if os.getenv('OTCLIENT_GLOBAL_LOGIN_PROBE') == '1' then
  if Services.clientAssets then Services.clientAssets.enabled = false end
  local function mark(s) g_logger.info('[GLOBAL_PROBE] ' .. s) end
  connect(g_game, {
    onGameStart=function() mark('GAME_START=true') end,
    onLoginError=function() mark('GAME_LOGIN_ERROR=true') end,
    onConnectionError=function() mark('GAME_CONNECTION_ERROR=true') end,
    onSessionEnd=function() mark('GAME_SESSION_END=true') end
  })
  local success=EnterGame.loginSuccess
  EnterGame.loginSuccess=function(requestId,characters,session)
    mark('HTTP_LOGIN_SUCCESS=true'); success(requestId,characters,session)
    scheduleEvent(function()
      if CharacterList and CharacterList.doLogin then mark('CHARACTER_LOGIN_ATTEMPT=true'); CharacterList.doLogin()
      else mark('CHARACTER_LIST_UNAVAILABLE=true') end
    end,1000)
  end
  local failed=EnterGame.loginFailed
  EnterGame.loginFailed=function(requestId,msg,result) mark('HTTP_LOGIN_FAILED=true'); failed(requestId,msg,result) end
  scheduleEvent(function()
    local email=os.getenv('TIBIA_TEST_EMAIL') or ''; local password=os.getenv('TIBIA_TEST_PASSWORD') or ''
    if email=='' or password=='' then mark('SECRET_GATE_FAILED=true'); return end
    EnterGame.setDefaultServer('https://www.tibia.com/clientservices/loginservice.php',443,1532)
    local a=rootWidget:recursiveGetChildById('accountNameTextEdit'); local p=rootWidget:recursiveGetChildById('accountPasswordTextEdit'); local h=rootWidget:recursiveGetChildById('httpLoginBox'); local stay=rootWidget:recursiveGetChildById('stayLoggedBox')
    if not a or not p or not h then mark('LOGIN_WIDGETS_UNAVAILABLE=true'); return end
    a:setText(email); p:setText(password); h:setChecked(true); if stay then stay:setChecked(false) end
    email=nil; password=nil; mark('LOGIN_START=true'); EnterGame.doLogin()
  end,1500)
  scheduleEvent(function() if not g_game.isOnline() then mark('PROBE_TIMEOUT=true'); g_app.exit() end end,90000)
end
LUA
chmod 644 "$PROBE_STATE/runtime/init.lua"
echo NON_PERSISTENT_LOGIN_INSTRUMENTATION_READY=true

docker pull "$OTCLIENT_IMAGE" >/dev/null
docker rm -f "$PROBE_CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$PROBE_CONTAINER" \
  --network "container:$SOURCE_CONTAINER" --user root \
  --label com.blakinio.owner=otclient --label com.blakinio.purpose=global-login-probe --label com.blakinio.task=OTC-20260727-tibia-linux-runner-analysis \
  --mount "type=bind,src=$PROBE_STATE,dst=/probe" \
  --mount "type=bind,src=$PROBE_STATE/runtime/init.lua,dst=/otclient/init.lua,readonly" \
  --mount "type=bind,src=$PROBE_STATE/things/1532,dst=/otclient/data/things/1532,readonly" \
  "$OTCLIENT_IMAGE" sleep infinity >/dev/null

docker exec "$PROBE_CONTAINER" bash -lc 'export DEBIAN_FRONTEND=noninteractive; apt-get update -qq && apt-get install -y --no-install-recommends proxychains4 xvfb x11-utils procps iproute2 >/dev/null'
docker exec "$PROBE_CONTAINER" bash -lc '! command -v tesseract >/dev/null 2>&1'
cat >"$PROBE_STATE/runtime/proxychains.conf" <<'EOF'
strict_chain
proxy_dns
quiet_mode
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 25344
EOF
: >"$PROBE_STATE/runtime/otclient.stdout.log"
docker exec "$PROBE_CONTAINER" bash -lc 'nohup Xvfb :100 -screen 0 1280x800x24 -nolisten tcp >/probe/runtime/xvfb.log 2>&1 </dev/null &'
for _ in $(seq 1 30); do docker exec "$PROBE_CONTAINER" xdpyinfo -display :100 >/dev/null 2>&1 && break; sleep 1; done
docker exec "$PROBE_CONTAINER" xdpyinfo -display :100 >/dev/null

docker exec -d -e DISPLAY=:100 -e HOME=/probe/home -e LIBGL_ALWAYS_SOFTWARE=1 -e OTCLIENT_GLOBAL_LOGIN_PROBE=1 -e TIBIA_TEST_EMAIL -e TIBIA_TEST_PASSWORD "$PROBE_CONTAINER" bash -lc 'cd /otclient && exec proxychains4 -f /probe/runtime/proxychains.conf ./otclient >>/probe/runtime/otclient.stdout.log 2>&1'
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD

for _ in $(seq 1 200); do
  grep -q '\[GLOBAL_PROBE\] GAME_START=true' "$PROBE_STATE/runtime/otclient.stdout.log" && break
  grep -q '\[GLOBAL_PROBE\] PROBE_TIMEOUT=true' "$PROBE_STATE/runtime/otclient.stdout.log" && break
  docker exec "$PROBE_CONTAINER" pgrep -f '/otclient/otclient|./otclient' >/dev/null 2>&1 || break
  sleep 0.5
done
grep -o '\[GLOBAL_PROBE\] [A-Z_]*=true' "$PROBE_STATE/runtime/otclient.stdout.log" | sort -u || true
pid=$(docker exec "$PROBE_CONTAINER" pgrep -f '/otclient/otclient|./otclient' | head -n1 || true)
if [[ -n "$pid" ]]; then
  rows=$(docker exec "$PROBE_CONTAINER" ss -ntp 2>/dev/null | grep "pid=$pid," || true)
  direct=$(printf '%s\n' "$rows" | awk '{print $5}' | grep -Ev '^(127\.0\.0\.1|\[::1\]):25344$' | grep -c . || true)
  echo "OTCLIENT_DIRECT_TCP_COUNT=$direct"
  [[ "$direct" -eq 0 ]]
fi

docker ps -a --filter 'label=com.docker.compose.project=oteryn-staging' --format '{{.ID}}\t{{.Names}}' | sort >/tmp/oteryn-after.tsv
diff -u /tmp/oteryn-before.tsv /tmp/oteryn-after.tsv
echo CANONICAL_STAGING_UNCHANGED=true

if grep -q '\[GLOBAL_PROBE\] GAME_START=true' "$PROBE_STATE/runtime/otclient.stdout.log"; then
  echo OTCLIENT_TIBIA_GLOBAL_LOGIN_PROVEN=true
  exit 0
fi
echo OTCLIENT_TIBIA_GLOBAL_LOGIN_PROVEN=false
if grep -q '\[GLOBAL_PROBE\] HTTP_LOGIN_SUCCESS=true' "$PROBE_STATE/runtime/otclient.stdout.log"; then echo FAILURE_STAGE=after_http_login_before_game_start
elif grep -q '\[GLOBAL_PROBE\] HTTP_LOGIN_FAILED=true' "$PROBE_STATE/runtime/otclient.stdout.log"; then echo FAILURE_STAGE=http_login_rejected
elif grep -q '\[GLOBAL_PROBE\] LOGIN_START=true' "$PROBE_STATE/runtime/otclient.stdout.log"; then echo FAILURE_STAGE=http_login_no_success_callback
else echo FAILURE_STAGE=before_login_start; fi
exit 1
