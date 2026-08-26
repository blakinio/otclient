#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${GITHUB_ACTIONS:?GITHUB_ACTIONS is required}"
: "${RUNNER_OS:?RUNNER_OS is required}"
: "${LAB_EPHEMERAL_HOSTED:?LAB_EPHEMERAL_HOSTED is required}"
: "${TIBIA_TEST_EMAIL:?TIBIA_TEST_EMAIL is required}"
: "${TIBIA_TEST_PASSWORD:?TIBIA_TEST_PASSWORD is required}"
[[ "$GITHUB_ACTIONS" == true && "$RUNNER_OS" == Linux && "$LAB_EPHEMERAL_HOSTED" == 1 ]]

CONTAINER=otclient-tibia-global-login-handoff
STATE_VOLUME=otclient-tibia-global-login-state
IMAGE=otclient-tibia-global-login-lab-runtime:local
CERT=.github/track-b-encrypted-handoff/recipient.pem
OUT=artifacts/encrypted-handoff/handoff.cms
CLIENT_VERSION_STRING=15.32.bf29ac

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

test -s "$CERT"
docker image inspect "$IMAGE" >/dev/null
docker volume inspect "$STATE_VOLUME" >/dev/null
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" --network bridge --user root \
  --mount "type=volume,src=$STATE_VOLUME,dst=/lab/state" \
  --tmpfs /lab/secrets:rw,noexec,nosuid,nodev,size=2m,mode=0700 \
  "$IMAGE" sleep infinity >/dev/null
docker cp "$CERT" "$CONTAINER:/lab/recipient.pem"
docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
command -v openssl >/dev/null
root=/lab/state/userspace-warp
bin="$root/bin"
state="$root/state"
[[ -x "$bin/wireproxy" && -s "$state/wireproxy.conf" ]]
rm -f "$root/wireproxy.pid"
"$bin/wireproxy" -n -c "$state/wireproxy.conf"
nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null &
echo $! >"$root/wireproxy.pid"
ready=0
for _ in $(seq 1 30); do
  if curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 \
      https://www.cloudflare.com/cdn-cgi/trace >/tmp/handoff-warp.trace 2>/dev/null; then
    ready=1
    break
  fi
  sleep 2
done
[[ "$ready" == 1 ]]
grep -Eq "^warp=(on|plus)$" /tmp/handoff-warp.trace
'
echo LAB_ENCRYPTED_HANDOFF_WARP_READY=true

ASSET_VERSION=$(docker exec "$CONTAINER" bash -lc \
  "curl --socks5-hostname 127.0.0.1:25344 --compressed -fsSL --connect-timeout 15 --max-time 60 -A 'Mozilla/5.0' https://static.tibia.com/launcher/assets-current/assets.json.sha256 | awk 'NR==1{print \$1}'")
[[ "$ASSET_VERSION" =~ ^[0-9a-fA-F]{64}$ ]]
echo LAB_ENCRYPTED_HANDOFF_ASSET_IDENTIFIER_READY=true
docker exec -i -e TIBIA_TEST_EMAIL -e TIBIA_TEST_PASSWORD \
  -e TIBIA_ASSET_VERSION="$ASSET_VERSION" \
  -e TIBIA_CLIENT_VERSION_STRING="$CLIENT_VERSION_STRING" \
  "$CONTAINER" python3 - <<'PY'
import json
import os
from pathlib import Path
payload = {
    'email': os.environ['TIBIA_TEST_EMAIL'],
    'password': os.environ['TIBIA_TEST_PASSWORD'],
    'stayloggedin': False,
    'type': 'login',
    'clientversion': os.environ['TIBIA_CLIENT_VERSION_STRING'],
    'clienttype': 2,
    'assetversion': os.environ['TIBIA_ASSET_VERSION'],
}
path = Path('/lab/secrets/login-request.json')
path.write_text(json.dumps(payload, separators=(',', ':')), encoding='utf-8')
path.chmod(0o600)
PY

http_status=$(docker exec "$CONTAINER" bash -lc \
  "curl --socks5-hostname 127.0.0.1:25344 --compressed -sS --connect-timeout 15 --max-time 60 -A 'Mozilla/5.0' -H 'Content-Type: application/json' -H 'Accept: */*' --data-binary @/lab/secrets/login-request.json -o /lab/secrets/login-response.json -w '%{http_code}' https://www.tibia.com/clientservices/loginservice.php")
[[ "$http_status" == 200 ]]
echo LAB_ENCRYPTED_HANDOFF_HTTP_LOGIN_200=true

docker exec -i "$CONTAINER" python3 - <<'PY'
import json
from pathlib import Path
response_path = Path('/lab/secrets/login-response.json')
handoff_path = Path('/lab/secrets/login-handoff.json')
doc = json.loads(response_path.read_text(encoding='utf-8'))
error_code = doc.get('errorCode')
if error_code not in (None, 0):
    if isinstance(error_code, int):
        print(f'LAB_ENCRYPTED_HANDOFF_ERROR_CODE={error_code}')
    else:
        print('LAB_ENCRYPTED_HANDOFF_ERROR_CODE=NONINTEGER')
    raise SystemExit('official login response rejected')
session = doc.get('session')
playdata = doc.get('playdata')
worlds = playdata.get('worlds') if isinstance(playdata, dict) else None
characters = playdata.get('characters') if isinstance(playdata, dict) else None
if not isinstance(session, dict) or not isinstance(worlds, list) or not worlds:
    raise SystemExit('official login response missing session/world data')
if not isinstance(characters, list) or not characters:
    raise SystemExit('official login response missing character data')
session_key = session.get('sessionkey')
if not isinstance(session_key, str) or not session_key:
    raise SystemExit('official login response missing session key')
world_by_id = {str(w.get('id')): w for w in worlds if isinstance(w, dict)}
character = next((c for c in characters if isinstance(c, dict) and c.get('ismaincharacter') is True), None)
character = character or next((c for c in characters if isinstance(c, dict)), None)
if not character:
    raise SystemExit('official login response has no usable character')
world = world_by_id.get(str(character.get('worldid')))
if not isinstance(world, dict):
    raise SystemExit('character world id has no matching world')
world_port = int(world.get('externalportprotected'))
handoff = {
    'sessionKey': session_key,
    'worldName': world.get('name'),
    'worldHost': world.get('externaladdressprotected'),
    'worldPort': world_port,
    'characterName': character.get('name'),
}
if not all(isinstance(handoff[k], str) and handoff[k] for k in ('worldName','worldHost','characterName')):
    raise SystemExit('handoff identity field missing')
if not (1 <= world_port <= 65535):
    raise SystemExit('protected world port invalid')
handoff_path.write_text(json.dumps(handoff, separators=(',', ':')), encoding='utf-8')
handoff_path.chmod(0o600)
print('LAB_ENCRYPTED_HANDOFF_PLAINTEXT_VALID=true')
PY
docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
openssl cms -encrypt -binary -aes-256-cbc -outform DER \
  -in /lab/secrets/login-handoff.json \
  -out /lab/handoff.cms /lab/recipient.pem
[[ -s /lab/handoff.cms ]]
rm -f /lab/secrets/login-request.json
rm -f /lab/secrets/login-response.json /lab/secrets/login-handoff.json
! find /lab/secrets -mindepth 1 -maxdepth 1 -type f -print -quit | grep -q .
! grep -a -q "sessionKey" /lab/handoff.cms
'
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD ASSET_VERSION
mkdir -p "$(dirname "$OUT")"
docker cp "$CONTAINER:/lab/handoff.cms" "$OUT"
[[ -s "$OUT" ]]
! grep -a -q 'sessionKey' "$OUT"
echo LAB_ENCRYPTED_HANDOFF_CIPHERTEXT_READY=true

docker exec "$CONTAINER" rm -f /lab/handoff.cms /lab/recipient.pem
cleanup
trap - EXIT
