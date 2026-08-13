#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${RUNNER_NAME:?RUNNER_NAME is required}"
: "${RUNNER_WORKSPACE:?RUNNER_WORKSPACE is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"

[[ "$RUNNER_NAME" == "synology-otclient-01" ]]
command -v docker >/dev/null
docker version >/dev/null

LAB_ROOT="${RUNNER_WORKSPACE}/_otclient-labs/tibia-global-login"
STATE_ROOT="${LAB_ROOT}/state"
RUNTIME_ROOT="${LAB_ROOT}/runtime"
CONTAINER="otclient-tibia-global-login-lab"
IMAGE="ghcr.io/blakinio/otclient:latest"
TASK="OTC-20260813-tibia-global-login-lab"

mkdir -p "$STATE_ROOT" "$RUNTIME_ROOT"
chmod 700 "$LAB_ROOT" "$STATE_ROOT" "$RUNTIME_ROOT"

# Fail closed if the name is occupied by a container not owned by this lab.
if docker inspect "$CONTAINER" >/dev/null 2>&1; then
  owner=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.owner" }}' "$CONTAINER")
  task=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.task" }}' "$CONTAINER")
  [[ "$owner" == "otclient" && "$task" == "$TASK" ]]
  docker rm -f "$CONTAINER" >/dev/null
fi

# Reuse the runner-local image when available; otherwise pull with a hard bound.
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  timeout 240 docker pull "$IMAGE" >/dev/null
fi
image_id=$(docker image inspect "$IMAGE" --format '{{.Id}}')

# This container is intentionally network-isolated during bootstrap.
docker run -d --name "$CONTAINER" \
  --network none \
  --label com.blakinio.owner=otclient \
  --label com.blakinio.repository=blakinio/otclient \
  --label com.blakinio.task="$TASK" \
  --label com.blakinio.purpose=tibia-global-login-lab \
  --mount "type=bind,src=$STATE_ROOT,dst=/lab/state" \
  --mount "type=bind,src=$RUNTIME_ROOT,dst=/lab/runtime" \
  "$IMAGE" sleep infinity >/dev/null

container_id=$(docker inspect --format '{{.Id}}' "$CONTAINER")
container_network=$(docker inspect --format '{{.HostConfig.NetworkMode}}' "$CONTAINER")
[[ "$container_network" == "none" ]]

cat >"$STATE_ROOT/bootstrap.env" <<EOF
TASK=$TASK
REPOSITORY=blakinio/otclient
HEAD=$GITHUB_SHA
RUNNER=$RUNNER_NAME
CONTAINER=$CONTAINER
CONTAINER_ID=$container_id
IMAGE=$IMAGE
IMAGE_ID=$image_id
NETWORK_MODE=$container_network
EOF
chmod 600 "$STATE_ROOT/bootstrap.env"

printf '%s\n' \
  'TIBIA_GLOBAL_LOGIN_LAB_BOOTSTRAP=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_RUNNER_VERIFIED=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_DOCKER_VERIFIED=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_CONTAINER_READY=true' \
  'TIBIA_GLOBAL_LOGIN_LAB_NETWORK_ISOLATED=true' \
  "TIBIA_GLOBAL_LOGIN_LAB_HEAD=$GITHUB_SHA" \
  "TIBIA_GLOBAL_LOGIN_LAB_IMAGE_ID=$image_id"
