#!/usr/bin/env bash
set -Eeuo pipefail

[[ "${GITHUB_REPOSITORY:-}" == blakinio/otclient ]]
[[ "${RUNNER_NAME:-}" == synology-otclient-01 ]]
[[ -n "${GITHUB_RUN_ID:-}" ]]

workspace="${GITHUB_WORKSPACE:?}"
entry="$workspace/.github/scripts/tibia-official-client-re-canonical-live-lease"
script="$workspace/.github/scripts/tibia-official-client-re-canonical-live-lease.py"
root="/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-live-runtime-lease-manager/selftest/$GITHUB_RUN_ID"
state="$root/state"
token_a="$root/a.token"
token_b="$root/b.token"
guard_out="$root/guard.out"
canonical="/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime"

[[ "$state" != "$canonical" ]]
bash -n "$entry"

set +e
override_output="$(bash "$entry" --state-dir "$root/forbidden" status 2>&1)"
override_rc=$?
set -e
[[ "$override_rc" -eq 64 ]]
grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=noncanonical_state_override_forbidden' <<<"$override_output"
[[ ! -e "$root/forbidden" ]]

set +e
token_path_output="$(bash "$entry" acquire \
  --task-id OTC-selftest-a --session-id run-a --token-file /tmp/not-task-owned.token 2>&1)"
token_path_rc=$?
set -e
[[ "$token_path_rc" -eq 64 ]]
grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=token_path_outside_task_state' <<<"$token_path_output"

traversal="/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-selftest-a/../escaped.token"
set +e
traversal_output="$(bash "$entry" acquire \
  --task-id OTC-selftest-a --session-id run-a --token-file "$traversal" 2>&1)"
traversal_rc=$?
set -e
[[ "$traversal_rc" -eq 64 ]]
grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=token_path_outside_task_state' <<<"$traversal_output"

mkdir -p "$root"
chmod 700 "$root"
trap 'rm -rf -- "$root"' EXIT

python3 "$script" --state-dir "$state" acquire \
  --task-id OTC-selftest-a --session-id run-a --token-file "$token_a" --ttl-seconds 300
raw_token="$(cat "$token_a")"
[[ -n "$raw_token" ]]
[[ "$(stat -c %a "$token_a")" == 600 ]]
[[ "$(stat -c %a "$state/lease.json")" == 600 ]]
! grep -Fq -- "$raw_token" "$state/lease.json"

set +e
conflict_output="$(python3 "$script" --state-dir "$state" acquire \
  --task-id OTC-selftest-b --session-id run-b --token-file "$token_b" --ttl-seconds 300 2>&1)"
conflict_rc=$?
set -e
[[ "$conflict_rc" -eq 2 ]]
grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=lease_conflict' <<<"$conflict_output"
[[ ! -e "$token_b" ]]

python3 "$script" --state-dir "$state" validate \
  --task-id OTC-selftest-a --session-id run-a --token-file "$token_a"
python3 "$script" --state-dir "$state" renew \
  --task-id OTC-selftest-a --session-id run-a --token-file "$token_a" --ttl-seconds 300
python3 "$script" --state-dir "$state" guard-run \
  --task-id OTC-selftest-a --session-id run-a --token-file "$token_a" -- \
  python3 -c "from pathlib import Path; Path('$guard_out').write_text('guarded')"
[[ "$(cat "$guard_out")" == guarded ]]

status_output="$(python3 "$script" --state-dir "$state" status --json)"
[[ "$status_output" != *"$raw_token"* ]]
[[ "$status_output" != *token_sha256* ]]
[[ "$status_output" != *'"token"'* ]]

python3 "$script" --state-dir "$state" release \
  --task-id OTC-selftest-a --session-id run-a --token-file "$token_a"
[[ ! -e "$token_a" ]]

python3 "$script" --state-dir "$state" acquire \
  --task-id OTC-selftest-b --session-id run-b --token-file "$token_b" --ttl-seconds 300
python3 "$script" --state-dir "$state" release \
  --task-id OTC-selftest-b --session-id run-b --token-file "$token_b"

expired_state="$root/expired-state"
token_e="$root/e.token"
token_f="$root/f.token"
python3 "$script" --state-dir "$expired_state" acquire \
  --task-id OTC-selftest-e --session-id run-e --token-file "$token_e" --ttl-seconds 60
python3 - "$expired_state/lease.json" <<'PY'
import json, os, sys
path = sys.argv[1]
data = json.load(open(path, encoding='utf-8'))
data['expires_at'] = 1
with open(path, 'w', encoding='utf-8', newline='\n') as handle:
    json.dump(data, handle, sort_keys=True, indent=2)
    handle.write('\n')
os.chmod(path, 0o600)
PY

set +e
expired_release_output="$(python3 "$script" --state-dir "$expired_state" release \
  --task-id OTC-selftest-e --session-id run-e --token-file "$token_e" 2>&1)"
expired_release_rc=$?
set -e
[[ "$expired_release_rc" -eq 2 ]]
grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=lease_expired' <<<"$expired_release_output"
[[ -e "$token_e" ]]
expired_status="$(python3 "$script" --state-dir "$expired_state" status --json)"
grep -Fq '"status": "active"' <<<"$expired_status"
grep -Fq '"expired": true' <<<"$expired_status"

set +e
missing_reason_output="$(python3 "$script" --state-dir "$expired_state" acquire \
  --task-id OTC-selftest-f --session-id run-f --token-file "$token_f" --ttl-seconds 60 2>&1)"
missing_reason_rc=$?
set -e
[[ "$missing_reason_rc" -eq 2 ]]
grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=stale_takeover_reason_required' <<<"$missing_reason_output"

python3 "$script" --state-dir "$expired_state" acquire \
  --task-id OTC-selftest-f --session-id run-f --token-file "$token_f" --ttl-seconds 60 \
  --stale-takeover-reason 'self-hosted expired release fencing proof'
python3 "$script" --state-dir "$expired_state" release \
  --task-id OTC-selftest-f --session-id run-f --token-file "$token_f"

concurrent_state="$root/concurrent-state"
token_c="$root/c.token"
token_d="$root/d.token"
out_c="$root/c.out"
out_d="$root/d.out"

set +e
python3 "$script" --state-dir "$concurrent_state" acquire \
  --task-id OTC-selftest-c --session-id run-c --token-file "$token_c" --ttl-seconds 300 \
  >"$out_c" 2>&1 &
pid_c=$!
python3 "$script" --state-dir "$concurrent_state" acquire \
  --task-id OTC-selftest-d --session-id run-d --token-file "$token_d" --ttl-seconds 300 \
  >"$out_d" 2>&1 &
pid_d=$!
wait "$pid_c"; rc_c=$?
wait "$pid_d"; rc_d=$?
set -e

if [[ "$rc_c" -eq 0 && "$rc_d" -eq 2 ]]; then
  grep -Fq 'TRACK_A_CANONICAL_LEASE_ACQUIRE=true' "$out_c"
  grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=lease_conflict' "$out_d"
  python3 "$script" --state-dir "$concurrent_state" release \
    --task-id OTC-selftest-c --session-id run-c --token-file "$token_c"
elif [[ "$rc_c" -eq 2 && "$rc_d" -eq 0 ]]; then
  grep -Fq 'TRACK_A_CANONICAL_LEASE_ERROR=lease_conflict' "$out_c"
  grep -Fq 'TRACK_A_CANONICAL_LEASE_ACQUIRE=true' "$out_d"
  python3 "$script" --state-dir "$concurrent_state" release \
    --task-id OTC-selftest-d --session-id run-d --token-file "$token_d"
else
  echo "unexpected concurrent acquire return codes: c=$rc_c d=$rc_d" >&2
  exit 1
fi

echo TRACK_A_CANONICAL_LEASE_ENTRYPOINT_FENCED=true
echo TRACK_A_CANONICAL_LEASE_TOKEN_PATH_TRAVERSAL_REJECTED=true
echo TRACK_A_CANONICAL_LEASE_EXPIRED_RELEASE_REJECTED=true
echo TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER_REASON_REQUIRED=true
echo TRACK_A_CANONICAL_LEASE_CONCURRENT_SERIALIZATION_PROVEN=true
echo TRACK_A_CANONICAL_LEASE_SELFTEST_COMPLETE=true
echo TRACK_A_CANONICAL_LEASE_CANONICAL_STATE_UNTOUCHED=true
