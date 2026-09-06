---
task_id: OTC-20260906-native-login-shm-bind-relay
status: implementing
agent: ChatGPT
session_id: native-login-shm-bind-relay-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_repair
phase: contract_red
branch: fix/OTC-20260906-native-login-shm-bind-relay
base_branch: main
created: 2026-09-06T21:35:00+02:00
updated_at: 2026-09-06T21:35:00+02:00
base_main: aedd3a9dac833523b5e69fd5037ce591c33bfd25
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
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - tests/tools/tibia_runtime_bridge/test_native_login_physical_executor_contract.py
  - docs/agents/tasks/active/OTC-20260906-native-login-shm-bind-relay.md
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

# OTC-20260906 — native-login target shm bind relay repair

## Objective

Repair the trusted-main be4f48 physical executor after run `34055153655 / 101545727674` passed lease generation 47, generation rebind and Gate B, then failed fail-closed at the secret-free relay probe with `relay_response_missing`.

No replacement, vault decrypt, credential send or native auth attempt occurred. Credential-bearing attempt count remains `0`.

## Root cause

The merged relay used a pathname AF_UNIX socket under the Kasm container `/dev/shm`, while the sidecar only joined the target IPC namespace. Linux IPC namespaces do not share filesystem pathname visibility; `/dev/shm` pathname visibility follows mount namespace topology. Therefore the sidecar had no proven path to the relay socket even though `--ipc container:<target>` was present.

## Repair design

Keep the existing one-shot `SCM_RIGHTS` relay and `--network none`, but expose only the target container's own Docker-managed shm mount to the sidecar:

1. derive the target container directory from its exact Docker inspect `ResolvConfPath` and exact 64-hex container id;
2. derive `<container-dir>/mounts/shm` as the daemon-side bind source;
3. add a read-only `--mount type=bind,src=<target-shm>,dst=/relay-shm,readonly` to the ephemeral sidecar before the immutable image;
4. keep the relay server path inside Kasm as `/dev/shm/<task-run-name>`;
5. map only the sidecar client path to `/relay-shm/<same-name>`;
6. preserve `SCM_RIGHTS`, sealed memfd validation, `--network none`, cap-drop, one-shot cleanup and exact-current peer checks;
7. Docker `--mount` missing-source behavior remains fail-closed; no host plaintext or credential path is copied into Kasm.

## Acceptance

- focused tests first fail against current `main` because target shm bind derivation/mount and sidecar `/relay-shm` mapping are absent;
- implementation derives target shm source only from exact inspected target identity;
- sidecar receives only a read-only bind of that shm mount and remains network-isolated;
- relay stays one-shot and `SCM_RIGHTS`-based;
- no credentials appear in env, argv, stdin, logs or repository evidence;
- exact-head hosted CI passes and all PR-head self-hosted jobs remain skipped;
- after merge, parent runs PRECHECK and then one secret-free `EXECUTE` transport probe before any credential-bearing step.

## Next action

Add RED contract assertions for target Docker shm bind derivation and sidecar relay-path mapping, then obtain hosted RED before implementation.
