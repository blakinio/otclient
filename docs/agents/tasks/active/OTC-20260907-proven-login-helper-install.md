---
task_id: OTC-20260907-proven-login-helper-install
status: implementing
agent: ChatGPT
session_id: proven-login-helper-install-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_helper_install_repair
phase: regression_red
branch: fix/OTC-20260907-proven-login-helper-install
base_branch: main
base_main: f7104146300f8e202aaed2f200c0b9e386e7db6d
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
credentials_allowed: none
parent_task: OTC-20260906-native-login-physical-executor
depends_on:
  - OTC-20260907-native-login-proven-secret-ingress
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_proven.py
  - tests/tools/tibia_runtime_bridge/test_native_login_proven_secret_ingress_contract.py
  - docs/agents/tasks/active/OTC-20260907-proven-login-helper-install.md
modules_touched:
  - Track A proven native-login helper installation
---

# OTC-20260907 — proven-login helper install repair

## Evidence

Merged-main EXECUTE `34086352053 / 101631159082` on `f7104146300f8e202aaed2f200c0b9e386e7db6d` passed PRECHECK, lease generation 52, rebind and Gate B, then failed during current helper replacement as `TRACK_A_BE4F48_PHYSICAL_ERROR=command_failed:docker:1` before any replacement result was written. The sanitized artifact contains only the PRECHECK JSON. Therefore vault decrypt, credential ingress, native auth, character confirmation and causal IN_GAME were not reached; credential-bearing attempt count remains 0.

The current base installer discovers numeric `kasm-user` UID/GID but later uses an unproven named `chown kasm-user:kasm-user` plus shell wildcard ownership/mode changes. Current physical evidence proves target UID/GID are `1000:1000` but does not prove a group named `kasm-user` exists.

## Repair

Override only the helper-install seam in the corrected proven-login wrapper. Keep base `replace()` and `confirm_unique()` untouched. Install each known path explicitly, use freshly discovered numeric UID:GID, avoid shell wildcard ownership, and map each Docker stage to a static safe error code. No auth/secret behavior changes.

## Acceptance

- regression contract requires numeric UID:GID install and forbids recursive replacement overrides;
- no raw Docker stderr is surfaced;
- helper cleanup/copy/ownership/mode/digest verification is explicit per known path;
- exact-head hosted CI GREEN with PR-head physical jobs SKIPPED;
- after merge: fresh PRECHECK then exactly one EXECUTE; no repeated credential attempt unless the first attempt was proven not to occur.
