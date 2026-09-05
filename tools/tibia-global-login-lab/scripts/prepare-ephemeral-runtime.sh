#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${GITHUB_ACTIONS:?GITHUB_ACTIONS is required}"
: "${RUNNER_OS:?RUNNER_OS is required}"
[[ "${LAB_EPHEMERAL_HOSTED:-0}" == "1" ]]
[[ "$GITHUB_ACTIONS" == "true" && "$RUNNER_OS" == "Linux" ]]
command -v docker >/dev/null
docker version >/dev/null

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
TASK=OTC-20260813-tibia-global-login-lab
CONTAINER=otclient-tibia-global-login-ephemeral-prepare
STATE_VOLUME=otclient-tibia-global-login-state
RUNTIME_VOLUME=otclient-tibia-global-login-runtime
BASE_IMAGE=ghcr.io/blakinio/otclient:latest
RUNTIME_IMAGE=otclient-tibia-global-login-lab-runtime:local
WGCF_VERSION=2.2.32
WGCF_SHA256=2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c
WIREPROXY_VERSION=1.1.3
WIREPROXY_SHA256=e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

python3 - "$ROOT" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
paths = [
    root / 'tools/tibia-global-login-lab/scripts/bootstrap.sh',
    root / 'tools/tibia-global-login-lab/scripts/http-login-preflight.sh',
    root / 'tools/tibia-global-login-lab/scripts/world-entry-probe.sh',
    root / 'tools/tibia-global-login-lab/scripts/refresh-current-assets.sh',
]
old = '[[ "$RUNNER_NAME" == "synology-otclient-01" ]]'
new = '[[ "${LAB_EPHEMERAL_HOSTED:-0}" == "1" && "${GITHUB_ACTIONS:-}" == "true" && "${RUNNER_OS:-}" == "Linux" ]]'
for path in paths:
    text = path.read_text(encoding='utf-8')
    if text.count(old) != 1:
        raise SystemExit(f'runner guard count mismatch: {path}')
    text = text.replace(old, new, 1)
    if path.name == 'bootstrap.sh':
        marker = 'RUNNER=synology-otclient-01'
        if text.count(marker) != 1:
            raise SystemExit('bootstrap runner marker count mismatch')
        text = text.replace(marker, 'RUNNER=github-hosted-ephemeral', 1)
    path.write_text(text, encoding='utf-8')
PY
echo LAB_EPHEMERAL_RUNNER_GUARDS_PATCHED=true

for volume in "$STATE_VOLUME" "$RUNTIME_VOLUME"; do
  if docker volume inspect "$volume" >/dev/null 2>&1; then
    owner=$(docker volume inspect --format '{{ index .Labels "com.blakinio.owner" }}' "$volume")
    task=$(docker volume inspect --format '{{ index .Labels "com.blakinio.task" }}' "$volume")
    [[ "$owner" == "otclient" && "$task" == "$TASK" ]]
  else
    docker volume create \
      --label com.blakinio.owner=otclient \
      --label com.blakinio.repository=blakinio/otclient \
      --label com.blakinio.task="$TASK" \
      "$volume" >/dev/null
  fi
done

docker pull "$BASE_IMAGE" >/dev/null
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" --network bridge --user root \
  --label com.blakinio.owner=otclient \
  --label com.blakinio.repository=blakinio/otclient \
  --label com.blakinio.task="$TASK" \
  --label com.blakinio.purpose=tibia-global-login-ephemeral-prepare \
  --mount "type=volume,src=$STATE_VOLUME,dst=/lab/state" \
  --mount "type=volume,src=$RUNTIME_VOLUME,dst=/lab/runtime" \
  "$BASE_IMAGE" sleep infinity >/dev/null

docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y --no-install-recommends \
  curl python3 xvfb x11-utils procps iproute2 ca-certificates proxychains4 tar >/dev/null
! command -v tesseract >/dev/null 2>&1
'
echo LAB_EPHEMERAL_RUNTIME_PACKAGES_READY=true

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

curl -fL --retry 3 --retry-all-errors --connect-timeout 10 --max-time 180 \
  -o wgcf "https://github.com/ViRb3/wgcf/releases/download/v${WGCF_VERSION}/wgcf_${WGCF_VERSION}_linux_amd64"
printf "%s  wgcf\n" "$WGCF_SHA256" | sha256sum -c - >/dev/null
chmod 755 wgcf

curl -fL --retry 3 --retry-all-errors --connect-timeout 10 --max-time 180 \
  -o wireproxy.tar.gz "https://github.com/windtf/wireproxy/releases/download/v${WIREPROXY_VERSION}/wireproxy_linux_amd64.tar.gz"
printf "%s  wireproxy.tar.gz\n" "$WIREPROXY_SHA256" | sha256sum -c - >/dev/null
rm -rf wireproxy-extract
mkdir wireproxy-extract
tar -xzf wireproxy.tar.gz -C wireproxy-extract
wp=$(find wireproxy-extract -type f -name wireproxy -print -quit)
[[ -n "$wp" ]]
cp "$wp" wireproxy
chmod 755 wireproxy

cd "$state"
rm -f wgcf-account.toml wgcf-profile.conf wireproxy.conf
"$bin/wgcf" register --accept-tos >/dev/null
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
nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null &
echo $! >"$root/wireproxy.pid"
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
rm -f /tmp/warp-trace
'
echo LAB_EPHEMERAL_WARP_CHANGED_EGRESS_VERIFIED=true

docker commit "$CONTAINER" "$RUNTIME_IMAGE" >/dev/null
docker image inspect "$RUNTIME_IMAGE" >/dev/null
echo LAB_EPHEMERAL_RUNTIME_IMAGE_READY=true

cleanup
trap - EXIT
