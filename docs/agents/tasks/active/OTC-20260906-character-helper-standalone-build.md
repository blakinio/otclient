---
task_id: OTC-20260906-character-helper-standalone-build
status: validating
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: physical_executor_build_repair
phase: exact_head_validation
branch: fix/OTC-20260906-character-helper-standalone-build
base_branch: main
created: 2026-09-06T18:48:00+02:00
updated_at: 2026-09-06T18:52:00+02:00
base_main: 65f6a96e099f77ce93ac5023456cf4a65c84b463
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
parent_task: OTC-20260906-native-login-physical-executor
owned_paths:
  - tools/tibia_runtime_bridge/experimental_character_control_current.cpp
  - .github/workflows/track-a-character-helper-standalone-build.yml
  - docs/agents/tasks/active/OTC-20260906-character-helper-standalone-build.md
modules_touched:
  - Track A native character helper build
reuses:
  - .github/workflows/track-a-native-login-be4f48-physical.yml
blocks:
  - OTC-20260906-native-login-physical-executor
---

# OTC-20260906 — character helper standalone build repair

## Objective

Repair the trusted-main physical PRECHECK preparation failure without weakening compiler diagnostics. The be4f48 character helper must compile as the standalone shared object used by the physical executor with `-Wall -Wextra -Wpedantic -Werror`.

## RED evidence

Merged-main PRECHECK run `34046535436`, prepare job `101522467183` verified trusted `main` `65f6a96e099f77ce93ac5023456cf4a65c84b463` and the exact be4f48 fence, then failed before artifact upload and before any Synology physical job at:

`experimental_character_control_current.cpp:57:13: error: errorJson(const char*) defined but not used [-Werror=unused-function]`

The physical job was skipped. No canonical runtime mutation, vault decryption, credential access, or secret attempt occurred.

## Minimal repair

- remove only the unused `errorJson` dead helper;
- add a dedicated PR-head hosted standalone build gate using the same warning/error policy as the trusted-main physical preparer;
- keep `-Werror`; do not suppress the warning or weaken the physical executor.

## Validation target

The PR is complete only when the new hosted gate compiles the exact helper successfully, confirms `CONFIRM_UNIQUE` and the current confirmation signature remain in the shared object, Track A runtime governance remains PASS with `runtime_access: none`, ordinary CI is GREEN, and review/diff hygiene is clean.
