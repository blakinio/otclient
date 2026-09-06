---
task_id: OTC-20260906-native-login-ipc-relay-repair
status: validating
agent: ChatGPT
session_id: native-login-ipc-relay-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_repair
phase: implementation_validation
branch: fix/OTC-20260906-native-login-ipc-relay
base_branch: main
created: 2026-09-06T21:07:00+02:00
updated_at: 2026-09-06T21:27:00+02:00
base_main: 27783fa784410a1b7c085bf5c051c4998d2d6805
execution_mode: chatgpt
execution_class: repository_only
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
physical_e2e_required: false
implementation_authorized: true
credentials_allowed: none
secret_values_logged: false
run_scope: bounded_secret_free_transport_repair
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_parent_physical_qualification
parent_task: OTC-20260906-native-login-physical-executor
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_physical.py
  - tools/tibia_runtime_bridge/container_native_login_client.py
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - tests/tools/tibia_runtime_bridge/test_native_login_physical_executor_contract.py
  - docs/agents/tasks/active/OTC-20260906-native-login-ipc-relay-repair.md
modules_touched:
  - Track A native-login sealed-FD transport
reuses:
  - tools/tibia_runtime_bridge/container_native_login_client.py
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - .github/scripts/track_a_native_login_be4f48_physical.py
depends_on:
  - OTC-20260906-native-login-physical-executor
blocks:
  - OTC-20260906-native-login-physical-executor
---

# OTC-20260906 — native-login IPC relay repair

## Objective

Repair the exact trusted-main physical executor after run `34051157365 / 101535022832` proved canonical lease generation 46, generation rebind and Gate B, then failed fail-closed during the secret-free Docker sidecar probe before client replacement or vault access.

Credential-bearing auth attempts remain `0` because the run emitted `NO_SECRET_ACCESS_BEFORE_SIDECAR_PROBE=true` and failed before the vault decrypt/auth step.

## Root cause boundary

The prior sidecar joined the target PID namespace and then attempted a mount-namespace transition. On the current Synology Docker topology the bounded sidecar never returned its probe JSON and the outer worker timed out at `docker run`.

The repair removes that mount-namespace transition from the transport rather than weakening the secret boundary.

## Design

Use a bounded shared-IPC relay:

1. the runner starts one blocking relay process inside the existing Kasm container with `docker exec -i`, streaming the reviewed relay source over stdin rather than installing pre-probe state;
2. the relay listens on a unique task/run-scoped `/dev/shm` Unix socket and accepts exactly one connection;
3. the ephemeral sidecar uses `--ipc container:otclient-track-a-kasmvnc`, `--pid container:otclient-track-a-kasmvnc`, no network, read-only root and no Docker socket;
4. the secret-free probe creates a synthetic fully sealed memfd, sends it to the Kasm relay with `SCM_RIGHTS`, and requires explicit relay proof that the FD remained sealed and the exact-current client path has the be4f48 size/SHA;
5. the auth sidecar decrypts the machine-local vault once into a sealed memfd and sends only that FD to the Kasm relay with `SCM_RIGHTS`;
6. the relay, already inside Kasm, validates the credential memfd, drops to the exact numeric Kasm UID/GID and forwards that same FD to the native auth helper through the existing `SO_PEERCRED`, boot-id, start-ticks and executable SHA checks;
7. relay and socket are bounded and one-shot; the pathname is unlinked immediately after accept and no credential plaintext is persisted.

No PR-head self-hosted execution is allowed. This repair task itself has `runtime_access: none`; physical PRECHECK/EXECUTE resumes only from the merged parent workflow on trusted `main`.

## TDD evidence

RED exact head `e17341510507b3d08513d3ac85653457c03ca394`:
- workflow run `34054107692`, job `101542740572`;
- 7 focused tests ran with 15 expected failures against the old transport;
- missing relay server/client markers included `relay-probe`, `relay-auth-fd`, `recvmsg`, `listen`, shared `/dev/shm` IPC and sidecar `SCM_RIGHTS`;
- the old transport still contained privileged mount-transition markers;
- all self-hosted physical jobs were skipped.

Implementation exact head before governance checkpoint `8251dbd2109787333543d0d6d4aa3eaef154e7c6`:
- the 7 focused relay contract tests themselves are GREEN;
- Python compile validation proceeds;
- native auth bridge validation run `34054767829` is GREEN;
- physical PR jobs remain skipped;
- the focused workflow and standalone governance workflow failed only because this newly added repository-only task initially omitted mandatory admission fields. This checkpoint supplies the required fail-closed `runtime_access:none` values without granting runtime authority.

A local synthetic Unix-domain relay smoke also transferred a sealed probe memfd by `SCM_RIGHTS`, validated the received seals/content, returned the bounded response, and removed the one-shot socket.

## Acceptance

- focused contract tests first fail against the old transport;
- implementation removes the privileged mount-transition dependency from worker/sidecar transport code;
- sidecar uses shared target IPC and `SCM_RIGHTS` to a one-shot Kasm relay;
- relay validates sealed FDs and preserves current exact peer identity checks;
- no credentials appear in env, argv, stdin, logs or repository evidence;
- exact-head hosted CI passes and self-hosted PR execution remains skipped;
- after merge, parent task reruns trusted-main PRECHECK, then a secret-free relay probe, and only if both pass may it perform the first credential-bearing auth attempt.

## Next action

Obtain exact-head hosted GREEN for PR #965, perform final diff/review-thread readback, merge, then return to the parent physical executor for trusted-main PRECHECK and secret-free relay qualification.