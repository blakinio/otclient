#!/usr/bin/env bash
set +x
set -Eeuo pipefail

: "${TIBIA_TEST_EMAIL:?missing_TIBIA_TEST_EMAIL}"
: "${TIBIA_TEST_PASSWORD:?missing_TIBIA_TEST_PASSWORD}"

# Keep the values available to the sourced helper as shell variables, but
# remove their export attribute before any external preflight command runs.
export -n TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD

if env | grep -Eq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD)='; then
  printf 'TRACK_A_FIELD6_SECRET_ENV_ERROR=export_scrub_failed\n' >&2
  exit 1
fi

HELPER="${BASH_SOURCE[0]%/*}/track_a_current_login_field6_runtime.sh"
[[ -f "$HELPER" && ! -L "$HELPER" ]] || {
  printf 'TRACK_A_FIELD6_SECRET_ENV_ERROR=helper_missing_or_symlink\n' >&2
  exit 1
}

printf 'TRACK_A_FIELD6_SECRET_ENV_SCRUBBED=true\n'
source "$HELPER" "$@"
