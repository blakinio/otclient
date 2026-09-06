---
task_id: OTC-20260906-native-login-proc-root-relay
status: validating
agent: ChatGPT
session_id: native-login-proc-root-relay-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_repair
phase: exact_head_validation
branch: fix/OTC-20260906-native-login-proc-root-relay
base_branch: main
created: 2026-09-06T22:51:00+02:00
updated_at: 2026-09-06T23:09:00+02:00
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
  - tests/tools/tibia_runtime_bridge/test_native_login_proc_root_relay_contract.py
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
5. Remove the invalid target-shm Docker bind and `/relay-shm` mapping.
6. Preserve `--network none`, `--read-only`, dropped capabilities with only SETUID/SETGID, sealed memfd validation, one-shot relay cleanup and `SCM_RIGHTS`.
7. Preserve all auth identity checks and the exactly-one secret-bearing attempt budget.
8. PR head remains repository-only; self-hosted physical jobs must stay skipped.

## TDD / implementation evidence

RED head `9bd83ee67ca782e9e5e58df3e1e3e02df72eb34d` contract run before implementation:
- run `34059408661`, job `101557120672`;
- focused physical executor contract failed on the new proc-root requirements as intended;
- trusted-main helper-build and physical PR-head jobs were skipped.

Implementation was then applied only to the public transport overlay and sidecar:
- `.github/scripts/track_a_native_login_be4f48_physical_base.py` remains the exact merged Git blob `666beeb601d93257585a5dd302afd255a57a0103`;
- public worker overrides sidecar command construction and relay pathname mapping for both probe and base `auth_one_shot`;
- replacement, auth state machine, process handoff, character confirmation and causal state logic remain delegated to the unchanged base worker;
- sidecar relay root is exactly `/proc/1/root/dev/shm` and suffixes are restricted to the native-login namespace;
- no `--ipc container:`, network sharing, SYS_ADMIN, nsenter, daemon shm bind, new secret source or auth retry was added.

Implementation validation head `9f027ce5c1c079d416f6d1490b27a1401f7a2d36`:
- physical executor contract `34060059813 / 101558864487`: PASS;
- both PR-head trusted-main/self-hosted jobs in that workflow: SKIPPED;
- Track A native auth bridge validation `34060059811`: PASS;
- Track A agent runtime governance `34060059817`: PASS;
- general CI `34060059966`: PASS;
- all PR workflows on this head reached terminal state with no failure conclusion.

## Acceptance

- TDD RED proves current main still depended on the invalid target-shm bind and lacked `/proc/1/root/dev/shm` mapping;
- implementation removes the Docker shm bind entirely from the active public transport path;
- sidecar accepts only the exact `/proc/1/root/dev/shm/<native-login-prefix+safe-suffix>` namespace;
- no `--network container:` or `--ipc container:` is introduced;
- hosted exact-head checks are GREEN and self-hosted PR jobs stay SKIPPED;
- after merge, parent runs fresh PRECHECK and exactly one EXECUTE, whose secret-free relay probe must pass before any replacement or credential access.

## Next action

Revalidate the final checkpoint head, inspect review threads/comments and mergeability, merge #968, then return immediately to the parent for a fresh trusted-main PRECHECK and one bounded EXECUTE.
