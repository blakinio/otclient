#!/usr/bin/env bash
set -Eeuo pipefail
set +x

CONTAINER=otclient-tibia-global-login-lab
TASK=OTC-20260813-tibia-global-login-lab
PID_FILE=/lab/state/userspace-warp/wireproxy.pid

docker inspect "$CONTAINER" >/dev/null
owner=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.owner" }}' "$CONTAINER")
task=$(docker inspect --format '{{ index .Config.Labels "com.blakinio.task" }}' "$CONTAINER")
[[ "$owner" == "otclient" && "$task" == "$TASK" ]]

# The next Track B stage recreates the entire container. A PID written by the
# current container must never be interpreted inside the next PID namespace.
docker exec "$CONTAINER" sh -c "rm -f '$PID_FILE'"
docker exec "$CONTAINER" test ! -e "$PID_FILE"
echo LAB_WIREPROXY_CROSS_CONTAINER_PID_CLEARED=true
