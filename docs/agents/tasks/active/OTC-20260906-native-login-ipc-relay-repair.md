---
task_id: OTC-20260906-native-login-ipc-relay-repair
status: implementing
agent: ChatGPT
session_id: native-login-ipc-relay-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_repair
phase: contract_red
branch: fix/OTC-20260906-native-login-ipc-relay
base_branch: main
created: 2026-09-06T21:07:00+02:00
updated_at: 2026-09-06T21:07:00+02:00
base_main: 27783fa784410a1b7c085bf5c051c4998d2d6805
execution_mode: chatgpt
execution_class: repository_only
runtime_access: none
runtime_owner_task: OTC-20260906-native-login-physical-executor
runtime_namespace: canonical-live-runtime
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

The current sidecar joins the target PID namespace but then uses `nsenter --mount --root=/proc/1/root`. On the current Synology Docker topology the bounded sidecar never returns its probe JSON and the outer worker times out at `docker run`.

The repair must remove the mount-namespace dependency rather than weaken the secret boundary.

## Design

Use a bounded shared-IPC relay:

1. runner starts one blocking relay process inside the existing Kasm container with `docker exec`;
2. relay listens on a unique `/dev/shm` Unix socket owned by the task/run;
3. ephemeral sidecar uses `--ipc container:otclient-track-a-kasmvnc`, no network, read-only root, no Docker socket and no `SYS_ADMIN`;
4. secret-free probe creates a synthetic sealed memfd, sends it to the Kasm relay with `SCM_RIGHTS`, and requires explicit relay proof that the FD remained sealed and the exact-current client is visible;
5. auth sidecar decrypts the machine-local vault once into a sealed memfd and sends only that FD to the Kasm relay with `SCM_RIGHTS`;
6. relay, already inside Kasm, forwards that same FD to the exact native auth helper through the existing `container_native_login_client` peer-identity checks;
7. relay is bounded, one-shot, cleaned up exactly, and never persists credential plaintext.

No PR-head self-hosted execution is allowed. This repair task itself has `runtime_access: none`; physical PRECHECK/EXECUTE resumes only from the merged parent workflow on trusted `main`.

## Acceptance

- focused contract tests first fail against the old `nsenter/SYS_ADMIN` design;
- implementation removes `nsenter` and `SYS_ADMIN` from the native-login sidecar path;
- sidecar uses `--ipc container:<canonical target>` and `SCM_RIGHTS` to a one-shot Kasm relay;
- relay validates sealed FDs and preserves current exact peer identity checks;
- no credentials appear in env, argv, stdin, logs or repository evidence;
- exact-head hosted CI passes and self-hosted PR execution remains skipped;
- after merge, parent task must rerun trusted-main PRECHECK, then a secret-free relay probe, and only if both pass may it perform the first credential-bearing auth attempt.

## Next action

Add the relay contract assertions as RED tests, publish a draft PR, and use hosted CI to prove the existing `nsenter/SYS_ADMIN` implementation fails the new contract before implementation.