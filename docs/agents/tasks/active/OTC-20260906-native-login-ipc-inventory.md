---
task_id: OTC-20260906-native-login-ipc-inventory
status: active
agent: ChatGPT
session_role: diagnostician
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: read_only_runtime_transport_inventory
phase: implementation
branch: diag/OTC-20260906-native-login-ipc-inventory
base_branch: main
created: 2026-09-06T18:58:00+02:00
updated_at: 2026-09-06T18:58:00+02:00
base_main: 09fe1e2ddd334b2e97d5e60f15ec5de4e9024ae7
runtime_access: read_only
runtime_owner_task: OTC-20260906-native-login-ipc-inventory
runtime_namespace: synology:otclient-track-a-kasmvnc:transport-inventory
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
physical_e2e_required: false
parent_task: OTC-20260906-native-login-physical-executor
owned_paths:
  - .github/workflows/track-a-native-login-ipc-inventory.yml
  - docs/agents/tasks/active/OTC-20260906-native-login-ipc-inventory.md
modules_touched:
  - Track A runtime transport diagnostics
reuses:
  - Docker read-only inspect API through the existing trusted Synology runner
blocks:
  - OTC-20260906-native-login-physical-executor
---

# OTC-20260906 — native-login IPC inventory

## Objective

Determine, without mutation or credential access, whether the trusted self-hosted runner container and canonical KasmVNC container already share a filesystem/IPC seam that can carry a Unix-domain socket for SCM_RIGHTS.

## Admission evidence

Merged-main PRECHECK run `34046945750`, physical job `101523685277`, proved the exact-current unique target and registration match before failing at `target_host_pid_namespace_not_visible`. The same run did not decrypt the vault, did not attempt login, and did not mutate the canonical client.

## Scope

The diagnostic may read only Docker container metadata for the runner and `otclient-track-a-kasmvnc`. It must not read process memory, client environment, credentials, files from the vault, packet data, or user input; it must not create/restart/exec/stop containers or processes. Host mount source paths are not emitted raw: sources are SHA-256 hashed solely to correlate shared mounts. Output is limited to container identity class, destination paths, mount type/read-write flags, namespace modes and shared-source correlation.
