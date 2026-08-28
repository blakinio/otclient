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

docker image inspect "$IMAGE" >/dev/null
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" --network bridge --user root \
  --label com.blakinio.owner=otclient \
  --label com.blakinio.repository=blakinio/otclient \
  --label com.blakinio.task="$TASK" \
  --label com.blakinio.purpose=tibia-global-login-http-preflight \
  --mount "type=volume,src=$STATE_VOLUME,dst=/lab/state" \
  --mount "type=volume,src=$RUNTIME_VOLUME,dst=/lab/runtime" \
  "$IMAGE" sleep infinity >/dev/null

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
for _ in $(seq 1 30); do
  curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/lab-warp.trace 2>/dev/null && break
  sleep 2
done
direct=$(curl -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace | sed -n "s/^ip=//p")
warp=$(sed -n "s/^ip=//p" /tmp/lab-warp.trace)
statev=$(sed -n "s/^warp=//p" /tmp/lab-warp.trace)
[[ -n "$direct" && -n "$warp" && "$direct" != "$warp" ]]
[[ "$statev" == on || "$statev" == plus ]]
assetversion=$(curl --socks5-hostname 127.0.0.1:25344 --compressed -fsSL --connect-timeout 15 --max-time 60 -A "Mozilla/5.0" https://static.tibia.com/launcher/assets-current/assets.json.sha256 | awk "NR==1{print \$1}")
[[ "$assetversion" =~ ^[0-9a-fA-F]{64}$ ]]
printf "%s" "$assetversion" >/tmp/tibia-assetversion
'

docker exec -i -e TIBIA_TEST_EMAIL -e TIBIA_TEST_PASSWORD "$CONTAINER" python3 - <<'PY'
import json, os
import platform
from pathlib import Path
assetversion = Path('/tmp/tibia-assetversion').read_text().strip()

def qsysinfo_pretty_product_name():
    try:
        pretty_name = platform.freedesktop_os_release().get('PRETTY_NAME', '')
    except OSError:
        pretty_name = ''
    if pretty_name:
        return pretty_name
    uname = os.uname()
    return f'{uname.sysname} {uname.release}'

payload = {
    "email": os.environ["TIBIA_TEST_EMAIL"],
    "password": os.environ["TIBIA_TEST_PASSWORD"],
    "stayloggedin": True,
    "type": "login",
    "clientversion": "15.32.bf29ac",
    "clienttype": 2,
    "assetversion": assetversion,
    "operatingsystem": qsysinfo_pretty_product_name(),
}
Path('/tmp/tibia-login-request.json').write_text(json.dumps(payload, separators=(',', ':')), encoding='utf-8')
print('LAB_HTTP_PREFLIGHT_ASSET_VERSION_LENGTH=' + str(len(assetversion)))
PY

http_status=$(docker exec "$CONTAINER" bash -lc "curl --socks5-hostname 127.0.0.1:25344 --compressed -sS --connect-timeout 15 --max-time 60 -A 'Mozilla/5.0' -H 'Content-Type: application/json' -H 'Accept: */*' --data-binary @/tmp/tibia-login-request.json -o /tmp/tibia-login-response.json -w '%{http_code}' https://www.tibia.com/clientservices/loginservice.php")
[[ "$http_status" =~ ^[0-9]{3}$ ]]
echo "LAB_HTTP_PREFLIGHT_STATUS=$http_status"

docker exec -i "$CONTAINER" python3 - <<'PY'
import json
from pathlib import Path
p = Path('/tmp/tibia-login-response.json')
try:
    doc = json.loads(p.read_text(encoding='utf-8'))
except Exception:
    print('LAB_HTTP_PREFLIGHT_JSON=false')
    print('LAB_HTTP_PREFLIGHT_HAS_SESSION=false')
    print('LAB_HTTP_PREFLIGHT_HAS_PLAYDATA=false')
    print('LAB_HTTP_PREFLIGHT_HAS_ERROR_CODE=false')
else:
    print('LAB_HTTP_PREFLIGHT_JSON=true')
    print('LAB_HTTP_PREFLIGHT_HAS_SESSION=' + str('session' in doc).lower())
    print('LAB_HTTP_PREFLIGHT_HAS_PLAYDATA=' + str('playdata' in doc).lower())
    print('LAB_HTTP_PREFLIGHT_HAS_ERROR_CODE=' + str('errorCode' in doc).lower())
    if isinstance(doc.get('errorCode'), int):
        print('LAB_HTTP_PREFLIGHT_ERROR_CODE=' + str(doc['errorCode']))
    print('LAB_HTTP_PREFLIGHT_HAS_ERROR_MESSAGE=' + str(bool(doc.get('errorMessage'))).lower())
    print('LAB_HTTP_PREFLIGHT_HAS_DEVICE_COOKIE=' + str('devicecookie' in doc).lower())
PY

docker exec "$CONTAINER" rm -f /tmp/tibia-login-request.json /tmp/tibia-login-response.json /tmp/tibia-assetversion
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
echo LAB_HTTP_PREFLIGHT_COMPLETE=true
