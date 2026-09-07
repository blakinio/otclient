---
task_id: OTC-20260907-proven-login-user-owned-install
status: implementing
agent: ChatGPT
session_id: proven-login-user-owned-install-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_helper_install_repair
phase: regression_red
branch: fix/OTC-20260907-proven-login-user-owned-install
base_branch: main
base_main: c88269135863f45444d71b98001a59547e19b83d
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
  - OTC-20260907-proven-login-helper-install
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_proven.py
  - tests/tools/tibia_runtime_bridge/test_native_login_proven_secret_ingress_contract.py
  - docs/agents/tasks/active/OTC-20260907-proven-login-user-owned-install.md
modules_touched:
  - Track A proven native-login helper installation
---

# OTC-20260907 — user-owned helper install

## Evidence

Merged-main EXECUTE `34087244070 / 101633721022` on `c88269135863f45444d71b98001a59547e19b83d` passed fresh PRECHECK, canonical lease generation 53, rebind and Gate B, then failed as `TRACK_A_BE4F48_PHYSICAL_ERROR=helper_install_permissions_failed`. Sanitized evidence again contains only PRECHECK, so replacement did not complete and vault decrypt, credential ingress, native auth, character confirmation and causal IN_GAME were not reached. Credential-bearing attempt count remains 0.

The previous installer created the exact task root as root with mode 0700 and then attempted to repair file ownership after `docker cp`. That is internally inconsistent for a helper runtime that must be traversable by `kasm-user`; numeric chown also fails in this container topology.

## Repair

Reset only the exact task-owned `/tmp/otclient-native-login-current-sha` path while under the canonical guarded mutation. Recreate it directly as `kasm-user` mode 0700, stream each trusted helper bundle file through `docker exec -i -u kasm-user` into its exact path, and verify digests as `kasm-user`. Do not use `docker cp`, chown, wildcard ownership, sidecars, nsenter, or any credential material. Keep base replacement, auth semantics, character confirmation and one-shot budget unchanged.

## Acceptance

- exact task root is recreated as current target user, not root;
- helper bytes are written directly by `kasm-user` through bounded stdin;
- no `docker cp` or chown in the corrected helper-install seam;
- explicit mode/identity/digest checks and static safe failure codes;
- exact-head hosted checks GREEN with PR-head physical jobs SKIPPED;
- after merge: fresh PRECHECK then exactly one EXECUTE; no repeated credential attempt unless prior evidence proves auth was never reached.
