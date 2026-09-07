---
task_id: OTC-20260907-proven-login-explicit-root-reset
status: implementing
agent: ChatGPT
session_id: proven-login-explicit-root-reset-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_helper_install_repair
phase: exact_head_ci
branch: fix/OTC-20260907-proven-login-explicit-root-reset
base_branch: main
base_main: d9c08388bdb48154170037abefca82d0b598c7ea
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
  - OTC-20260907-proven-login-user-owned-install
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_proven.py
  - tests/tools/tibia_runtime_bridge/test_native_login_proven_secret_ingress_contract.py
  - docs/agents/tasks/active/OTC-20260907-proven-login-explicit-root-reset.md
modules_touched:
  - Track A proven native-login helper installation
---

# OTC-20260907 — explicit-root helper reset

## Evidence

Merged-main PRECHECK `34092839825 / 101649949119` on `d9c08388bdb48154170037abefca82d0b598c7ea` passed terminally with EXECUTE skipped and no secret access.

The single authorized EXECUTE `34093005780 / 101650483277` then passed fresh admission, acquired canonical lease generation 54, completed rebind and Gate B, and stopped before replacement completion/auth with `TRACK_A_BE4F48_PHYSICAL_ERROR=helper_install_reset_failed`. The uploaded sanitized artifact again contained only PRECHECK, so vault decrypt and credential-bearing auth were not reached; current credential attempt count remains 0.

## Repair

Do not inherit the container image default user for cleanup of stale task-owned helper state. Prove explicit container UID 0 via `docker exec -u 0 ... id -u`, then use that identity only to remove the exact bounded `/tmp/otclient-native-login-current-sha` path. Immediately recreate and populate the helper runtime exclusively as `kasm-user`; keep no chown/docker-cp path and do not alter auth, one-shot, character or IN_GAME semantics.

## Acceptance

- explicit root readback must equal `0` before reset;
- exact task root reset uses `docker exec -u 0` and no default user ambiguity;
- all creation/write/stat/digest operations after reset are explicit `kasm-user`;
- no `docker cp`, chown, sidecar, nsenter, or credential access introduced;
- exact-head CI/Track A contracts GREEN with physical jobs skipped on PR-head;
- after merge, fresh PRECHECK then exactly one EXECUTE; no second credential attempt unless evidence proves auth was not reached.
