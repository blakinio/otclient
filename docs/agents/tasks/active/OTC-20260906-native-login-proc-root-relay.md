---
task_id: OTC-20260906-native-login-proc-root-relay
status: implementing
agent: ChatGPT
session_id: native-login-proc-root-relay-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_repair
phase: contract_red
branch: fix/OTC-20260906-native-login-proc-root-relay
base_branch: main
created: 2026-09-06T22:51:00+02:00
updated_at: 2026-09-06T22:51:00+02:00
base_main: 3e95b6d46fd8463500fa0a222dfbb68db6c908b6
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
run_scope: bounded_secret_free_proc_root_relay_repair
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_parent_physical_qualification
parent_task: OTC-20260906-native-login-physical-executor
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_physical.py
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - tests/tools/tibia_runtime_bridge/test_native_login_physical_executor_contract.py
  - docs/agents/tasks/active/OTC-20260906-native-login-proc-root-relay.md
modules_touched:
  - Track A native-login sealed-FD relay transport
reuses:
  - .github/scripts/track_a_native_login_be4f48_physical_base.py
  - tools/tibia_runtime_bridge/container_native_login_client.py
depends_on:
  - OTC-20260906-native-login-physical-executor
blocks:
  - OTC-20260906-native-login-physical-executor
---

# OTC-20260906 — native-login proc-root relay repair

## Objective

Replace the invalid Docker-daemon `/dev/shm` bind-source assumption with a PID-namespace `/proc/1/root/dev/shm` pathname to the same Kasm relay socket, while preserving the sealed-memfd + `SCM_RIGHTS` contract and `--network none`.

## Live evidence

Trusted-main EXECUTE `34058941401 / 101555934172` on `3e95b6d46fd8463500fa0a222dfbb68db6c908b6`:
- PRECHECK PASS;
- lease generation 49;
- canonical rebind PASS;
- Gate B PASS;
- `NO_SECRET_ACCESS_BEFORE_SIDECAR_PROBE=true`;
- secret-free probe failed with `target_shm_bind_source_unavailable`;
- sanitized artifact upload contained only one file, so no successful sidecar probe, replacement, auth, character confirmation or causal IN_GAME evidence exists;
- credential-bearing auth attempt count remains `0`.

Trusted-main read-only IPC inventory `34059193718 / 101556542111`:
- `target_mounts=[]`;
- `shared_mount_count=0`;
- target IPC mode `private`;
- target network mode `default`;
- runner and target have no shared Docker mount source;
- runtime mutation false, credential access false, process memory access false.

These facts falsify both the Docker-managed `mounts/shm` bind design and `--volumes-from` as a `/dev/shm` solution.

## Repair design

1. Keep the relay server inside Kasm at `/dev/shm/otclient-native-login-relay-<run>-<operation>`.
2. Keep sidecar `--pid container:otclient-track-a-kasmvnc`, so its `/proc` exposes the target PID namespace.
3. Address the same pathname socket from the sidecar as `/proc/1/root/dev/shm/<same-basename>`.
4. Rely on Linux `/proc/<pid>/root` semantics: it exposes the target process filesystem view including its mount namespace and per-process mounts; target PID 1 is the Kasm container init and therefore anchors the container mount namespace.
5. Remove the invalid `target_shm_source` Docker bind and `/relay-shm` mapping.
6. Preserve `--network none`, `--read-only`, dropped capabilities with only SETUID/SETGID, sealed memfd validation, one-shot relay cleanup and `SCM_RIGHTS`.
7. Preserve all auth identity checks and the exactly-one secret-bearing attempt budget.
8. PR head remains repository-only; self-hosted physical jobs must stay skipped.

## Acceptance

- TDD RED proves current main still depends on `target_shm_source`, `dst=/relay-shm,readonly`, and `/relay-shm` sidecar root, and lacks `/proc/1/root/dev/shm` mapping;
- implementation removes the Docker shm bind entirely;
- sidecar accepts only the exact `/proc/1/root/dev/shm/<native-login-prefix+safe-suffix>` namespace;
- no `--network container:` or `--ipc container:` is introduced;
- hosted exact-head checks are GREEN and self-hosted PR jobs stay SKIPPED;
- after merge, parent runs fresh PRECHECK and exactly one EXECUTE, whose secret-free relay probe must pass before any replacement or credential access.

## Next action

Add focused RED assertions for proc-root relay mapping and obtain hosted RED before implementation.
