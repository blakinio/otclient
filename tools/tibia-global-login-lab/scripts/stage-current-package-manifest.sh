#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${LAB_EPHEMERAL_HOSTED:?LAB_EPHEMERAL_HOSTED is required}"
[[ "$LAB_EPHEMERAL_HOSTED" == "1" ]]

CONTAINER=otclient-tibia-global-login-package-manifest
STATE_VOLUME=otclient-tibia-global-login-state
RUNTIME_VOLUME=otclient-tibia-global-login-runtime
IMAGE=otclient-tibia-global-login-lab-runtime:local
TASK=OTC-20260813-tibia-global-login-lab
PACKAGE_BASE=https://static.tibia.com/launcher/tibiaclient-linux-current

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker image inspect "$IMAGE" >/dev/null
for volume in "$STATE_VOLUME" "$RUNTIME_VOLUME"; do
  owner=$(docker volume inspect --format '{{ index .Labels "com.blakinio.owner" }}' "$volume")
  task=$(docker volume inspect --format '{{ index .Labels "com.blakinio.task" }}' "$volume")
  [[ "$owner" == "otclient" && "$task" == "$TASK" ]]
done

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" --network bridge --user root \
  --label com.blakinio.owner=otclient \
  --label com.blakinio.repository=blakinio/otclient \
  --label com.blakinio.task="$TASK" \
  --label com.blakinio.purpose=tibia-global-login-package-manifest \
  --mount "type=volume,src=$STATE_VOLUME,dst=/lab/state" \
  --mount "type=volume,src=$RUNTIME_VOLUME,dst=/lab/runtime" \
  "$IMAGE" sleep infinity >/dev/null

docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
root=/lab/state/userspace-warp
bin="$root/bin"
state="$root/state"
[[ -x "$bin/wireproxy" && -s "$state/wireproxy.conf" ]]
rm -f "$root/wireproxy.pid"
nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/package-manifest-wireproxy.log" 2>&1 </dev/null &
echo $! >"$root/wireproxy.pid"
for _ in $(seq 1 30); do
  if curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/package-warp.trace 2>/dev/null; then
    break
  fi
  sleep 2
done
grep -Eq "^warp=(on|plus)$" /tmp/package-warp.trace
rm -f /tmp/package-warp.trace
'

docker exec -e PACKAGE_BASE="$PACKAGE_BASE" -i "$CONTAINER" python3 - <<'PY'
import json
import os
from pathlib import Path
import subprocess

base = os.environ['PACKAGE_BASE'].rstrip('/')
url = base + '/package.json'
out_dir = Path('/lab/state/current-package')
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / 'package.json'
subprocess.run([
    'curl', '--socks5-hostname', '127.0.0.1:25344', '--compressed', '-fL',
    '-A', 'Mozilla/5.0 (X11; Linux x86_64)', '-e', url, '-H', 'Accept: */*',
    '--retry', '3', '--retry-all-errors', '--connect-timeout', '15',
    '--max-time', '180', url, '-o', str(out),
], check=True)

doc = json.loads(out.read_text(encoding='utf-8'))
version = str(doc.get('version') or '')
if not version.startswith('15.32'):
    raise SystemExit('unexpected current package version family')
files = doc.get('files')
if not isinstance(files, list) or not files:
    raise SystemExit('current package file list missing')
rows = [row for row in files if isinstance(row, dict)]
client_rows = [row for row in rows if row.get('localfile') == 'bin/client']
if len(client_rows) != 1:
    raise SystemExit('current package bin/client row missing or ambiguous')
client = client_rows[0]
if not isinstance(client.get('url'), str) or not client['url']:
    raise SystemExit('current package bin/client URL missing')
for key in ('packedhash', 'unpackedhash'):
    value = str(client.get(key) or '')
    if len(value) != 64 or any(ch not in '0123456789abcdefABCDEF' for ch in value):
        raise SystemExit(f'current package bin/client {key} invalid')
out.chmod(0o600)
print('LAB_CURRENT_PACKAGE_VERSION_FAMILY_15_32=true')
print('LAB_CURRENT_PACKAGE_FILE_COUNT=' + str(len(rows)))
print('LAB_CURRENT_PACKAGE_CLIENT_ROW=true')
print('LAB_CURRENT_PACKAGE_MANIFEST_STAGED=true')
PY

docker exec "$CONTAINER" sh -c 'rm -f /lab/state/userspace-warp/wireproxy.pid'
cleanup
trap - EXIT
