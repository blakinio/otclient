#!/usr/bin/env bash
set -Eeuo pipefail
set +x

: "${GITHUB_ACTIONS:?GITHUB_ACTIONS is required}"
: "${RUNNER_OS:?RUNNER_OS is required}"
: "${LAB_EPHEMERAL_HOSTED:?LAB_EPHEMERAL_HOSTED is required}"
[[ "$GITHUB_ACTIONS" == true && "$RUNNER_OS" == Linux && "$LAB_EPHEMERAL_HOSTED" == 1 ]]

# The encryption runtime must be prepared before any Tibia credential secret
# is placed in the job step environment.
if [[ -n "${TIBIA_TEST_EMAIL:-}" || -n "${TIBIA_TEST_PASSWORD:-}" ]]; then
  echo 'credential environment reached pre-secret prepare' >&2
  exit 1
fi

bash tools/tibia-global-login-lab/scripts/prepare-ephemeral-runtime.sh

CONTAINER=otclient-tibia-global-login-encryption-prep
IMAGE=otclient-tibia-global-login-lab-runtime:local
cleanup() { docker rm -f "$CONTAINER" >/dev/null 2>&1 || true; }
trap cleanup EXIT

docker image inspect "$IMAGE" >/dev/null
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER" --network bridge --user root "$IMAGE" sleep infinity >/dev/null
docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y --no-install-recommends openssl >/dev/null
command -v openssl >/dev/null
openssl version >/dev/null
'

docker commit "$CONTAINER" "$IMAGE" >/dev/null
docker image inspect "$IMAGE" >/dev/null
echo LAB_ENCRYPTED_HANDOFF_OPENSSL_READY=true

cleanup
trap - EXIT
