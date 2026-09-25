#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${RUNNER_NAME:?RUNNER_NAME is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"

[[ "$RUNNER_NAME" == "synology-otclient-01" ]]
command -v docker >/dev/null
docker version >/dev/null

CONTAINER="otclient-tibia-global-login-lab"
STATE_VOLUME="otclient-tibia-global-login-state"
RUNTIME_VOLUME="otclient-tibia-global-login-runtime"
BASE_IMAGE="ghcr.io/blakinio/otclient:latest"
RUNTIME_IMAGE="otclient-tibia-global-login-lab-runtime:local"
TASK="OTC-20260813-tibia-global-login-lab"

# If a previous lab container contains the expensive no-OCR runtime packages,
# preserve them in a runner-local image before refreshing the isolated container.
# Named-volume bytes (assets/WARP state) and docker-exec secrets are not part of
# the committed image filesystem/config.
if docker inspect "$CONTAINER" >/dev/null 2>&1; then
  owner=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.owner" }}' "$CONTAINER")
  task=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.task" }}' "$CONTAINER")
  [[ "$owner" == "otclient" && "$task" == "$TASK" ]]
  if docker exec "$CONTAINER" bash -lc 'command -v proxychains4 >/dev/null && command -v Xvfb >/dev/null && command -v python3 >/dev/null'; then
    docker commit "$CONTAINER" "$RUNTIME_IMAGE" >/dev/null
    echo TIBIA_GLOBAL_LOGIN_LAB_RUNTIME_IMAGE_CACHED=true
  fi
  docker rm -f "$CONTAINER" >/dev/null
fi

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

if ! docker image inspect "$BASE_IMAGE" >/dev/null 2>&1; then
  timeout 240 docker pull "$BASE_IMAGE" >/dev/null
fi
if docker image inspect "$RUNTIME_IMAGE" >/dev/null 2>&1; then
  IMAGE="$RUNTIME_IMAGE"
else
  IMAGE="$BASE_IMAGE"
fi
image_id=$(docker image inspect "$IMAGE" --format '{{.Id}}')

docker run -d --name "$CONTAINER" \
  --network none \
  --user root \
  --label com.blakinio.owner=otclient \
  --label com.blakinio.repository=blakinio/otclient \
  --label com.blakinio.task="$TASK" \
  --label com.blakinio.purpose=tibia-global-login-lab \
  --mount "type=volume,src=$STATE_VOLUME,dst=/lab/state" \
  --mount "type=volume,src=$RUNTIME_VOLUME,dst=/lab/runtime" \
  "$IMAGE" sleep infinity >/dev/null

EXACT_BINARY="$GITHUB_WORKSPACE/artifacts/exact-linux/otclient"
[[ -f "$EXACT_BINARY" ]]
EXACT_HEAD="${LAB_EXACT_HEAD:-$GITHUB_SHA}"
docker cp "$EXACT_BINARY" "$CONTAINER:/otclient/otclient.exact"
docker exec "$CONTAINER" bash -lc 'chown otclient:otclient /otclient/otclient.exact && chmod 0755 /otclient/otclient.exact && mv /otclient/otclient.exact /otclient/otclient'
docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
install -m 0755 /otclient/otclient /lab/runtime/otclient.exact
sha256sum /lab/runtime/otclient.exact | awk "{print \$1}" >/lab/runtime/otclient.exact.sha256
chmod 600 /lab/runtime/otclient.exact.sha256
'
echo TIBIA_GLOBAL_LOGIN_LAB_EXACT_BINARY_STAGED=true
container_id=$(docker inspect --format '{{.Id}}' "$CONTAINER")
container_network=$(docker inspect --format '{{.HostConfig.NetworkMode}}' "$CONTAINER")
[[ "$container_network" == "none" ]]

docker exec -e HEAD="$GITHUB_SHA" -e IMAGE_ID="$image_id" -e IMAGE="$IMAGE" "$CONTAINER" bash -lc 'cat >/lab/state/bootstrap.env <<EOF
TASK=OTC-20260813-tibia-global-login-lab
REPOSITORY=blakinio/otclient
HEAD=$HEAD
RUNNER=synology-otclient-01
CONTAINER=otclient-tibia-global-login-lab
IMAGE=$IMAGE
IMAGE_ID=$IMAGE_ID
NETWORK_MODE=none
EOF
chmod 600 /lab/state/bootstrap.env'

printf '%s\n' \
  'TIBIA_GLOBAL_LOGIN_LAB_BOOTSTRAP=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_RUNNER_VERIFIED=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_DOCKER_VERIFIED=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_VOLUMES_READY=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_CONTAINER_READY=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_NETWORK_ISOLATED=true' \
  "TIBIA_GLOBAL_LOGIN_LAB_HEAD=$EXACT_HEAD" \
  "TIBIA_GLOBAL_LOGIN_LAB_IMAGE=$IMAGE" \
  "TIBIA_GLOBAL_LOGIN_LAB_IMAGE_ID=$image_id"
echo TIBIA_GLOBAL_LOGIN_LAB_EXACT_LINUX_BINARY=true
