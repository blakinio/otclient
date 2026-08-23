#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${RUNNER_NAME:?RUNNER_NAME is required}"
[[ "$RUNNER_NAME" == "synology-otclient-01" ]]

CONTAINER=otclient-tibia-global-login-lab
TASK=OTC-20260813-tibia-global-login-lab
PACKAGE_BASE=https://static.tibia.com/launcher/tibiaclient-linux-current
ASSET_HASH_URL=https://static.tibia.com/launcher/assets-current/assets.json.sha256
PACKAGE_MANIFEST=/lab/state/current-package/package.json

docker inspect "$CONTAINER" >/dev/null
owner=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.owner" }}' "$CONTAINER")
task=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.task" }}' "$CONTAINER")
[[ "$owner" == "otclient" && "$task" == "$TASK" ]]

docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
root=/lab/state/userspace-warp
bin="$root/bin"
state="$root/state"
[[ -x "$bin/wireproxy" && -s "$state/wireproxy.conf" ]]
rm -f "$root/wireproxy.pid"
nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/asset-refresh-wireproxy.log" 2>&1 </dev/null &
echo $! >"$root/wireproxy.pid"
for _ in $(seq 1 30); do
  if curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/lab-refresh-warp.trace 2>/dev/null; then
    break
  fi
  sleep 2
done
grep -Eq "^warp=(on|plus)$" /tmp/lab-refresh-warp.trace
rm -f /tmp/lab-refresh-warp.trace
'

docker exec \
  -e PACKAGE_BASE="$PACKAGE_BASE" \
  -e ASSET_HASH_URL="$ASSET_HASH_URL" \
  -e PACKAGE_MANIFEST="$PACKAGE_MANIFEST" \
  -i "$CONTAINER" python3 - <<'PY'
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.parse

base = os.environ['PACKAGE_BASE'].rstrip('/')
manifest_path = Path(os.environ['PACKAGE_MANIFEST'])
asset_hash_url = os.environ['ASSET_HASH_URL']
out = Path('/lab/state/things/1532')
if not manifest_path.is_file():
    raise SystemExit('staged current package manifest missing')
doc = json.loads(manifest_path.read_text(encoding='utf-8'))
version = str(doc.get('version') or '')
if not version.startswith('15.32'):
    raise SystemExit('staged package version family mismatch')
rows = [row for row in doc.get('files', []) if isinstance(row, dict) and isinstance(row.get('localfile'), str)]
by_local = {row['localfile']: row for row in rows}

out.mkdir(parents=True, exist_ok=True)
for old in out.iterdir():
    if old.is_file():
        old.unlink()

def curl_get(url, path):
    subprocess.run([
        'curl', '--socks5-hostname', '127.0.0.1:25344', '--compressed', '-fL',
        '-A', 'Mozilla/5.0 (X11; Linux x86_64)', '-e', url, '-H', 'Accept: */*',
        '--retry', '3', '--retry-all-errors', '--connect-timeout', '15',
        '--max-time', '180', url, '-o', str(path),
    ], check=True)

def decode_package(data, row):
    packed_hash = str(row.get('packedhash') or '').lower()
    unpacked_hash = str(row.get('unpackedhash') or '').lower()
    if packed_hash and hashlib.sha256(data).hexdigest() != packed_hash:
        raise RuntimeError('packed hash mismatch')
    packed_size = row.get('packedsize')
    if isinstance(packed_size, int) and len(data) != packed_size:
        raise RuntimeError('packed size mismatch')
    url = str(row.get('url') or '')
    if not url.endswith('.lzma') or not unpacked_hash or hashlib.sha256(data).hexdigest() == unpacked_hash:
        raw = data
    else:
        if len(data) < 45:
            raise RuntimeError('short lzma payload')
        prop = data[32]
        lc = prop % 9
        rest = prop // 9
        lp = rest % 5
        pb = rest // 5
        dict_size = int.from_bytes(data[33:37], 'little')
        filt = {'id': lzma.FILTER_LZMA1, 'dict_size': dict_size, 'lc': lc, 'lp': lp, 'pb': pb}
        raw = lzma.decompress(data[45:], format=lzma.FORMAT_RAW, filters=[filt])
    if unpacked_hash and hashlib.sha256(raw).hexdigest() != unpacked_hash:
        raise RuntimeError('unpacked hash mismatch')
    unpacked_size = row.get('unpackedsize')
    if isinstance(unpacked_size, int) and len(raw) != unpacked_size:
        raise RuntimeError('unpacked size mismatch')
    return raw

def fetch_row(row):
    rel = str(row.get('url') or '')
    if not rel:
        raise RuntimeError('package row URL missing')
    url = base + '/' + urllib.parse.quote(rel, safe='/._-~')
    with tempfile.NamedTemporaryFile(delete=False) as handle:
        tmp = Path(handle.name)
    try:
        curl_get(url, tmp)
        return decode_package(tmp.read_bytes(), row)
    finally:
        tmp.unlink(missing_ok=True)

catalog_row = by_local.get('assets/catalog-content.json')
if not catalog_row:
    raise SystemExit('package catalog-content row missing')
catalog_raw = fetch_row(catalog_row)
(out / 'catalog-content.json').write_bytes(catalog_raw)
catalog = json.loads(catalog_raw)

required_types = {'appearances', 'staticdata', 'proficiencies'}
wanted = {
    entry['file'] for entry in catalog
    if isinstance(entry, dict)
    and entry.get('type') in required_types
    and isinstance(entry.get('file'), str)
}
if not any(name.startswith('appearances-') and name.endswith('.dat') for name in wanted):
    raise SystemExit('catalog appearances entry missing')
if not any(name.startswith('staticdata-') and name.endswith('.dat') for name in wanted):
    raise SystemExit('catalog staticdata entry missing')

for name in sorted(wanted):
    row = by_local.get('assets/' + name)
    if not row:
        raise SystemExit('required package asset row missing')
    (out / name).write_bytes(fetch_row(row))

with tempfile.NamedTemporaryFile(delete=False) as handle:
    hash_tmp = Path(handle.name)
try:
    curl_get(asset_hash_url, hash_tmp)
    asset_hash = hash_tmp.read_text(encoding='utf-8').strip().split()[0]
finally:
    hash_tmp.unlink(missing_ok=True)
if len(asset_hash) != 64 or any(ch not in '0123456789abcdefABCDEF' for ch in asset_hash):
    raise SystemExit('official asset identifier invalid')
(out / 'assets.json.sha256').write_text(asset_hash, encoding='utf-8')

print('LAB_CURRENT_PACKAGE_VERSION_FAMILY_15_32=true')
print('LAB_CURRENT_ASSET_FILE_COUNT=' + str(len(wanted) + 2))
print('LAB_LOGIN_MINIMAL_ASSETS_REFRESHED=true')
PY

docker exec "$CONTAINER" sh -c 'rm -f /lab/state/userspace-warp/wireproxy.pid'
echo LAB_CURRENT_ASSET_VERSION_LENGTH=64
