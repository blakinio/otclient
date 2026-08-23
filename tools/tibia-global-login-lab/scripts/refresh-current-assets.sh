#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${RUNNER_NAME:?RUNNER_NAME is required}"
[[ "$RUNNER_NAME" == "synology-otclient-01" ]]

CONTAINER=otclient-tibia-global-login-lab
TASK=OTC-20260813-tibia-global-login-lab
ASSET_BASE=https://static.tibia.com/launcher/assets-current

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
"$bin/wireproxy" -n -c "$state/wireproxy.conf"
if [[ -s "$root/wireproxy.pid" ]]; then kill "$(cat "$root/wireproxy.pid")" 2>/dev/null || true; fi
nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null &
echo $! >"$root/wireproxy.pid"
for _ in $(seq 1 30); do
  curl --socks5-hostname 127.0.0.1:25344 -fsS --max-time 10 https://www.cloudflare.com/cdn-cgi/trace >/tmp/lab-refresh-warp.trace 2>/dev/null && exit 0
  sleep 2
done
exit 1
'
docker exec -e ASSET_BASE="$ASSET_BASE" -i "$CONTAINER" python3 - <<'PY'
import hashlib
import json
import lzma
import os
import pathlib
import subprocess
import tempfile
import urllib.parse

base = os.environ['ASSET_BASE'].rstrip('/')
out = pathlib.Path('/lab/state/things/1532')
out.mkdir(parents=True, exist_ok=True)
def get(url, path):
    subprocess.run([
        'curl', '--socks5-hostname', '127.0.0.1:25344', '-fsSL', '-A', 'Mozilla/5.0',
        '--retry', '3', '--retry-all-errors', '--connect-timeout', '15',
        '--max-time', '180', url, '-o', str(path),
    ], check=True)

manifest = pathlib.Path('/tmp/assets.json')
get(base + '/assets.json', manifest)
doc = json.loads(manifest.read_text(encoding='utf-8'))
rows = []

def walk(value):
    if isinstance(value, dict):
        if isinstance(value.get('url'), str) and isinstance(value.get('packedhash'), str):
            rows.append((value['url'], value['packedhash'].lower(), str(value.get('unpackedhash') or '').lower()))
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)

walk(doc)

def decode(data, rel, unpacked):
    if not unpacked or not rel.endswith('.lzma'):
        return data, rel
    if hashlib.sha256(data).hexdigest() == unpacked:
        return data, rel[:-5]
    if len(data) < 45:
        raise RuntimeError('short lzma')
    prop = data[32]
    lc = prop % 9
    rest = prop // 9
    lp = rest % 5
    pb = rest // 5
    dict_size = int.from_bytes(data[33:37], 'little')
    filt = {'id': lzma.FILTER_LZMA1, 'dict_size': dict_size, 'lc': lc, 'lp': lp, 'pb': pb}
    return lzma.decompress(data[45:], format=lzma.FORMAT_RAW, filters=[filt]), rel[:-5]

def fetch(row):
    rel, packed, unpacked = row
    with tempfile.NamedTemporaryFile(delete=False) as handle:
        tmp = pathlib.Path(handle.name)
    try:
        get(base + '/' + urllib.parse.quote(rel, safe='/._-~'), tmp)
        data = tmp.read_bytes()
        if hashlib.sha256(data).hexdigest() != packed:
            raise RuntimeError('packed hash mismatch')
        raw, final = decode(data, rel, unpacked)
        if unpacked and hashlib.sha256(raw).hexdigest() != unpacked:
            raise RuntimeError('unpacked hash mismatch')
        return raw, final
    finally:
        tmp.unlink(missing_ok=True)

catalog_row = next((r for r in rows if r[0].endswith('catalog-content.json') or r[0].endswith('catalog-content.json.lzma')), None)
if not catalog_row:
    raise RuntimeError('catalog-content row absent')
catalog_raw, _ = fetch(catalog_row)
(out / 'catalog-content.json').write_bytes(catalog_raw)
catalog = json.loads(catalog_raw)
wanted = {
    item['file'] for item in catalog
    if isinstance(item, dict)
    and item.get('type') in {'appearances', 'staticdata', 'sprite', 'proficiencies'}
    and isinstance(item.get('file'), str)
}
mapping = {}
for row in rows:
    rel = row[0][:-5] if row[0].endswith('.lzma') and row[2] else row[0]
    key = rel.rsplit('/', 1)[-1]
    if key in wanted and key not in mapping:
        mapping[key] = row
missing = wanted - set(mapping)
if missing:
    raise RuntimeError(f'required catalog assets missing: {len(missing)}')
for name in sorted(wanted):
    (out / name).write_bytes(fetch(mapping[name])[0])
get(base + '/assets.json.sha256', out / 'assets.json.sha256')
print('LAB_CURRENT_ASSET_FILE_COUNT=' + str(len(wanted)))
print('LAB_CURRENT_ASSETS_REFRESHED=true')
PY

asset_version=$(docker exec "$CONTAINER" sh -c "tr -d '\\r\\n ' </lab/state/things/1532/assets.json.sha256")
[[ "$asset_version" =~ ^[0-9a-fA-F]{64}$ ]]
echo LAB_CURRENT_ASSET_VERSION_LENGTH=64
