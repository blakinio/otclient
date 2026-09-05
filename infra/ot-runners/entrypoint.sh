#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "$(id -u)" -eq 0 ]]; then
    chown -R runner:runner /runner-state /home/runner/_work
    exec gosu runner "$0" "$@"
fi

: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required, e.g. blakinio/otclient}"
: "${RUNNER_NAME:?RUNNER_NAME is required}"
: "${RUNNER_LABELS:?RUNNER_LABELS is required}"
: "${GITHUB_RUNNER_PAT:?GITHUB_RUNNER_PAT is required}"

RUNNER_ROOT=/home/runner
STATE_DIR=/runner-state
API_ROOT="https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/runners"
REPO_URL="https://github.com/${GITHUB_REPOSITORY}"
API_VERSION="2026-03-10"
STATE_FILES=(.runner .credentials .credentials_rsaparams .env .path)
runner_pid=""

api_token() {
    local endpoint="$1"
    curl --fail-with-body --silent --show-error --location \
        --request POST \
        --header 'Accept: application/vnd.github+json' \
        --header "Authorization: Bearer ${GITHUB_RUNNER_PAT}" \
        --header "X-GitHub-Api-Version: ${API_VERSION}" \
        "${API_ROOT}/${endpoint}" | jq -er '.token'
}

restore_state() {
    local file
    for file in "${STATE_FILES[@]}"; do
        if [[ -f "${STATE_DIR}/${file}" ]]; then
            cp -f "${STATE_DIR}/${file}" "${RUNNER_ROOT}/${file}"
        fi
    done
}

persist_state() {
    local file
    for file in "${STATE_FILES[@]}"; do
        if [[ -f "${RUNNER_ROOT}/${file}" ]]; then
            cp -f "${RUNNER_ROOT}/${file}" "${STATE_DIR}/${file}"
            chmod 0600 "${STATE_DIR}/${file}" || true
        fi
    done
}

clear_local_state() {
    local file
    for file in "${STATE_FILES[@]}"; do
        rm -f "${RUNNER_ROOT:?}/${file}" "${STATE_DIR:?}/${file}"
    done
}

remove_registration() {
    if [[ ! -f "${RUNNER_ROOT}/.runner" ]]; then
        clear_local_state
        return 0
    fi

    local remove_token
    if remove_token="$(api_token remove-token)"; then
        (cd "${RUNNER_ROOT}" && ./config.sh remove --unattended --token "${remove_token}") || true
    fi
    clear_local_state
}

forward_shutdown() {
    if [[ -n "${runner_pid}" ]] && kill -0 "${runner_pid}" 2>/dev/null; then
        kill -TERM "${runner_pid}" 2>/dev/null || true
    fi
}

cleanup() {
    set +e
    remove_registration
}

trap forward_shutdown INT TERM
trap cleanup EXIT

restore_state
# A previous unclean shutdown may have left the same logical runner registered.
# Remove local/server state when possible, then replace by name during registration.
remove_registration

registration_token="$(api_token registration-token)"

cd "${RUNNER_ROOT}"
./config.sh \
    --url "${REPO_URL}" \
    --token "${registration_token}" \
    --name "${RUNNER_NAME}" \
    --labels "${RUNNER_LABELS}" \
    --work "_work" \
    --unattended \
    --replace \
    --disableupdate

persist_state

./run.sh &
runner_pid=$!
wait "${runner_pid}"
