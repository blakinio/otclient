---
task_id: OTC-20260906-native-login-relay-observability
status: implementing
agent: ChatGPT
session_id: native-login-relay-observability-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_repair
phase: contract_red
branch: fix/OTC-20260906-native-login-relay-observability
base_branch: main
created: 2026-09-06T22:08:00+02:00
updated_at: 2026-09-06T22:08:00+02:00
base_main: c72fea67b5659075819ea4aaec68b89360a8e7c6
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
run_scope: bounded_secret_free_transport_observability_repair
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_parent_physical_qualification
parent_task: OTC-20260906-native-login-physical-executor
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_physical.py
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - tests/tools/tibia_runtime_bridge/test_native_login_physical_executor_contract.py
  - docs/agents/tasks/active/OTC-20260906-native-login-relay-observability.md
modules_touched:
  - Track A native-login sealed-FD transport
reuses:
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - .github/scripts/track_a_native_login_be4f48_physical.py
depends_on:
  - OTC-20260906-native-login-physical-executor
blocks:
  - OTC-20260906-native-login-physical-executor
---

# OTC-20260906 — native-login relay observability repair

## Objective

Make the secret-free native-login relay probe report the actual bounded transport failure instead of masking it as `relay_response_missing`.

Trusted-main run `34056826283 / 101550234967` on `c72fea67b5659075819ea4aaec68b89360a8e7c6` passed PRECHECK, lease generation 48, generation rebind and Gate B, then failed at the secret-free sidecar probe. The artifact contains only `native-login-precheck.json`; no sidecar-probe, replacement or auth evidence exists. Therefore client replacement, vault decrypt, credential FD send and native auth attempt did not occur, and credential-bearing attempt count remains `0`.

## Root cause boundary

The worker currently waits for the relay process and parses relay stdout before surfacing a nonzero sidecar process result. When the sidecar fails before connecting, the relay times out with empty stdout and `_finish_relay()` raises `relay_response_missing`, masking the original sidecar/Docker failure.

## Repair design

1. Keep all existing runtime/secret behavior unchanged.
2. Sidecar emits only a strict allowlist of static, secret-free error codes; arbitrary exception text is never serialized.
3. Secret-free probe inspects a nonzero sidecar result before letting relay timeout become the primary error.
4. Docker mount-source failures map to `target_shm_bind_source_unavailable` without echoing host paths.
5. Sidecar fail-closed responses map to a bounded `sidecar_probe_<safe-code>` error.
6. Relay is still allowed to reach its bounded timeout/cleanup so the exact task socket is not orphaned; any relay cleanup error is secondary to the already-proven sidecar failure.
7. No PR-head self-hosted execution is permitted.

## Acceptance

- focused tests first fail because current main lacks safe sidecar error-code emission and sidecar-first probe classification;
- implementation cannot serialize arbitrary exception messages;
- known Docker bind failure is classified without raw daemon stderr or host paths;
- secret-free sidecar failures are surfaced before relay timeout masking;
- exact-head hosted CI passes and PR-head self-hosted jobs remain skipped;
- after merge, parent may perform one fresh trusted-main PRECHECK and one EXECUTE because all prior EXECUTEs stopped before credential access.

## Next action

Add RED contract assertions for allowlisted sidecar errors and sidecar-first probe classification, then obtain hosted RED before implementation.
