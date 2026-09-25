#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${RUNNER_NAME:?RUNNER_NAME is required}"
[[ "$RUNNER_NAME" == "synology-otclient-01" ]]

CONTAINER=otclient-tibia-global-login-lab
TASK=OTC-20260813-tibia-global-login-lab
ASSET_BASE=https://static.tibia.com/launcher/assets-current
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
  -e ASSET_BASE="$ASSET_BASE" \
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

asset_base = os.environ['ASSET_BASE'].rstrip('/')
manifest_path = Path(os.environ['PACKAGE_MANIFEST'])
out = Path('/lab/state/things/1532')
assets_manifest = Path('/tmp/current-assets.json')
assets_hash_file = Path('/tmp/current-assets.json.sha256')

if not manifest_path.is_file():
    raise SystemExit('staged current package manifest missing')
package_doc = json.loads(manifest_path.read_text(encoding='utf-8'))
version = str(package_doc.get('version') or '')
if not version.startswith('15.32'):
    raise SystemExit('staged package version family mismatch')

def get(url, path):
    subprocess.run([
        'curl', '--socks5-hostname', '127.0.0.1:25344', '--compressed', '-fL',
        '-A', 'Mozilla/5.0 (X11; Linux x86_64)', '-e', url, '-H', 'Accept: */*',
        '--retry', '3', '--retry-all-errors', '--connect-timeout', '15',
        '--max-time', '180', url, '-o', str(path),
    ], check=True)

def collect_rows(node, rows):
    if isinstance(node, dict):
        if isinstance(node.get('url'), str) and node.get('packedhash'):
            rows.append(node)
        for value in node.values():
            collect_rows(value, rows)
    elif isinstance(node, list):
        for value in node:
            collect_rows(value, rows)

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
        raise RuntimeError('asset row URL missing')
    url = asset_base + '/' + urllib.parse.quote(rel, safe='/._-~')
    with tempfile.NamedTemporaryFile(delete=False) as handle:
        tmp = Path(handle.name)
    try:
        get(url, tmp)
        return decode_package(tmp.read_bytes(), row)
    finally:
        tmp.unlink(missing_ok=True)

try:
    get(asset_base + '/assets.json', assets_manifest)
    get(asset_base + '/assets.json.sha256', assets_hash_file)
    expected_manifest_hash = assets_hash_file.read_text(encoding='utf-8').strip().split()[0]
    actual_manifest_hash = hashlib.sha256(assets_manifest.read_bytes()).hexdigest()
    if len(expected_manifest_hash) != 64 or any(ch not in '0123456789abcdefABCDEF' for ch in expected_manifest_hash):
        raise SystemExit('official asset identifier invalid')
    if actual_manifest_hash.lower() != expected_manifest_hash.lower():
        raise SystemExit('current assets manifest hash mismatch')

    assets_doc = json.loads(assets_manifest.read_text(encoding='utf-8'))
    rows = []
    collect_rows(assets_doc, rows)
    if not rows:
        raise SystemExit('current assets manifest contains no package rows')

    catalog_rows = [
        row for row in rows
        if urllib.parse.unquote(str(row.get('url') or '')).split('/')[-1].replace('.lzma', '') == 'catalog-content.json'
    ]
    if len(catalog_rows) != 1:
        raise SystemExit('current assets catalog-content row missing or ambiguous')

    catalog_raw = fetch_row(catalog_rows[0])
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

    by_final = {}
    for row in rows:
        final = urllib.parse.unquote(str(row.get('url') or '')).split('/')[-1].replace('.lzma', '')
        if final:
            by_final.setdefault(final, []).append(row)

    out.mkdir(parents=True, exist_ok=True)
    for old in out.iterdir():
        if old.is_file():
            old.unlink()
    (out / 'catalog-content.json').write_bytes(catalog_raw)

    for name in sorted(wanted):
        matches = by_final.get(name, [])
        if len(matches) != 1:
            raise SystemExit(f'required current asset row missing or ambiguous: {name}')
        (out / name).write_bytes(fetch_row(matches[0]))

    (out / 'assets.json.sha256').write_text(expected_manifest_hash, encoding='utf-8')

    print('LAB_CURRENT_PACKAGE_VERSION_FAMILY_15_32=true')
    print('LAB_CURRENT_ASSETS_MANIFEST_HASH_MATCH=true')
    print('LAB_CURRENT_ASSET_FILE_COUNT=' + str(len(wanted) + 2))
    print('LAB_LOGIN_MINIMAL_ASSETS_REFRESHED=true')
finally:
    assets_manifest.unlink(missing_ok=True)
    assets_hash_file.unlink(missing_ok=True)
PY

docker exec "$CONTAINER" sh -c 'rm -f /lab/state/userspace-warp/wireproxy.pid'
echo LAB_CURRENT_ASSET_VERSION_LENGTH=64
