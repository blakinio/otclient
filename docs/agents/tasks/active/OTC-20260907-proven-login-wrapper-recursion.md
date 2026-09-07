---
task_id: OTC-20260907-proven-login-wrapper-recursion
status: implementing
agent: ChatGPT
session_id: proven-login-wrapper-recursion-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_wrapper_recursion_repair
phase: contract_red
branch: fix/OTC-20260907-proven-login-wrapper-recursion
base_branch: main
base_main: 9870ad0722017a53c3efb5f4074ce52294090b03
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
parent_task: OTC-20260906-native-login-physical-executor
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_proven.py
  - tests/tools/tibia_runtime_bridge/test_native_login_proven_secret_ingress_contract.py
  - docs/agents/tasks/active/OTC-20260907-proven-login-wrapper-recursion.md
modules_touched:
  - Track A current be4f48 proven native-login wrapper dispatch
---

# OTC-20260907 — proven-login wrapper recursion repair

## Evidence

Trusted-main EXECUTE run `34085307355`, job `101628189137`, on `main@9870ad0722017a53c3efb5f4074ce52294090b03` passed exact-current PRECHECK, acquired canonical lease generation 51, completed generation rebind and Gate B, then failed immediately in replacement with `RecursionError` because the wrapper assigned `_base.replace = replace` while `replace()` delegated to `_base.replace()`.

The failure occurred before replacement, vault decrypt, credential ingress, auth, character confirmation or causal IN_GAME. Sanitized evidence contains only precheck. Credential-bearing attempt count remains `0`.

## Repair

- Base replacement and character-confirm implementations are already current and correct; do not wrap or monkey-patch them.
- The public corrected worker patches only `precheck` and `auth_one_shot` into base dispatch.
- Remove recursive `replace` and `confirm_unique` wrapper dispatch.
- Add a regression contract that forbids `_base.replace = replace` and `_base.confirm_unique = confirm_unique` and requires only the two intended overrides.
- No secret, runtime or architecture change.

## Acceptance

TDD RED -> minimal code fix -> exact-head hosted GREEN with self-hosted PR jobs SKIPPED -> merge -> fresh PRECHECK -> one EXECUTE. A new EXECUTE is allowed because the failed run performed zero credential-bearing attempts.
