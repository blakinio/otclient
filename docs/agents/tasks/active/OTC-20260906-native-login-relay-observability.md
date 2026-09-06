---
task_id: OTC-20260906-native-login-relay-observability
status: validating
agent: ChatGPT
session_id: native-login-relay-observability-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_repair
phase: final_validation
branch: fix/OTC-20260906-native-login-relay-observability
base_branch: main
created: 2026-09-06T22:08:00+02:00
updated_at: 2026-09-06T22:39:00+02:00
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
  - .github/scripts/track_a_native_login_be4f48_physical_base.py
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

The worker waited for the relay process and parsed relay stdout before surfacing a nonzero sidecar process result. When the sidecar failed before connecting, the relay timed out with empty stdout and `_finish_relay()` raised `relay_response_missing`, masking the original sidecar/Docker failure.

## Repair design

1. Keep replacement/auth/character runtime behavior byte-for-byte unchanged in a private base worker copied by Git blob identity from merged main.
2. Keep the public worker as a thin overlay that replaces only the secret-free `sidecar_probe` path.
3. Sidecar emits only a strict allowlist of static, secret-free error codes; arbitrary exception text is never serialized.
4. Secret-free probe inspects a nonzero sidecar result before relay timeout can become the primary error.
5. Docker mount-source failures map to `target_shm_bind_source_unavailable` without retaining host paths.
6. Sidecar failures map only to bounded `sidecar_probe_client_<allowlisted-code>` or `sidecar_probe_process_failed` states.
7. Exact per-run relay cleanup remains bounded to the task socket; no broad process or filesystem cleanup is introduced.
8. No PR-head self-hosted execution is permitted.

## TDD / implementation evidence

RED head `b953736ff3dad624e9efa0ce0265d46492b995de`:
- workflow run `34057131215`, job `101550965483`;
- 8 focused tests ran and the new observability contract produced 9 expected failures;
- PR-head trusted-main physical jobs were skipped.

Implementation:
- original merged physical worker blob `666beeb601d93257585a5dd302afd255a57a0103` is preserved as `.github/scripts/track_a_native_login_be4f48_physical_base.py` and its Git blob identity is asserted by the focused test;
- public worker changes only secret-free probe failure ordering/classification;
- sidecar emits only allowlisted static failure codes;
- no test-only contract marker shim remains;
- no credentials, runtime mutation authority or auth retry behavior was added.

Validated implementation head `6c33f4b04c582be6387ecebb701c7f01dee2de14`:
- focused physical executor workflow `34058535817` is GREEN; job `101554774360` is GREEN;
- its trusted-main helper-build and physical self-hosted PR jobs are SKIPPED;
- runtime governance `34058535778` is GREEN;
- native-auth bridge validation `34058535834` is GREEN;
- general CI `34058535955` is GREEN;
- review submissions and inline review threads are both empty at final audit.

## Acceptance

- focused tests first failed because current main lacked safe sidecar error-code emission and sidecar-first probe classification;
- implementation cannot serialize arbitrary exception messages;
- known Docker bind failure is classified without logging raw daemon stderr or host paths;
- secret-free sidecar failures are surfaced before relay timeout masking;
- exact-head hosted CI passes and PR-head self-hosted jobs remain skipped;
- after merge, parent may perform one fresh trusted-main PRECHECK and one EXECUTE because all prior EXECUTEs stopped before credential access.

## Next action

Obtain final exact-head GREEN after this evidence-only checkpoint, merge PR #967 with expected-head guard, then return immediately to the parent trusted-main PRECHECK and one bounded EXECUTE.
