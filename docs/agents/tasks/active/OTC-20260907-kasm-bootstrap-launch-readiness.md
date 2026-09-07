---
task_id: OTC-20260907-kasm-bootstrap-launch-readiness
status: implementing
agent: ChatGPT
session_id: kasm-bootstrap-launch-readiness-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap_repair
phase: implementation
branch: fix/OTC-20260907-kasm-bootstrap-launch-readiness
base_branch: main
base_main: 7352d49dc3ba0cabfea3f020859ba8d26feabc15
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
physical_action_budget: 0
implementation_authorized: true
owned_paths:
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe-compatible.py
  - .github/workflows/track-a-canonical-kasm-bootstrap-retry.yml
  - tests/tools/tibia_runtime_bridge/test_kasm_bootstrap_launch_readiness.py
  - tests/tools/tibia_runtime_bridge/test_canonical_kasm_bootstrap_retry_contract.py
  - docs/agents/tasks/active/OTC-20260907-kasm-bootstrap-launch-readiness.md
  - docs/agents/tasks/active/OTC-20260907-canonical-kasm-bootstrap-retry-live.md
modules_touched:
  - track_a_kasm_bootstrap_worker_scoped
  - track_a_kasm_existing_runtime_probe_scoped
reuses:
  - track_a_native_login_be4f48_proven launcher environment
  - canonical Kasm scope contract
  - canonical live lease and scoped transition
  - existing identity-bound bootstrap rollback
depends_on:
  - OTC-20260907-same-boot-zero-client-bootstrap-v2-live
blocks:
  - OTC-20260906-native-login-physical-executor
---

# Kasm bootstrap launch-readiness repair

## Evidence

Trusted-main recovery-v2 EXECUTE run `34120696396`, job `101737810471`, on `main@7352d49dc3ba0cabfea3f020859ba8d26feabc15` proved:

- same-boot metadata invalidation PASS under lease generation 60;
- canonical registration became ABSENT;
- bootstrap preflight PASS under lease generation 61;
- plain client launch process discovery PASS;
- immediate adoption probe failed before registration with `ProbeError`;
- identity-bound bootstrap rollback PASS;
- no credential access occurred.

The create-new worker still used the older direct launch environment, while the physically repaired native-login replacement worker already proved the required Kasm launch shape with `XAUTHORITY`, `LD_LIBRARY_PATH`, working directory and `sh -lc '... exec ./client'`.

## Repair

The scoped create-new worker must use that same plain launch environment, strip helper/credential/lease variables, persist exact launch identity before waiting for GUI readiness, and require exactly one Tibia main window while the same exact PID/start/size/SHA remains alive.

The scoped adoption probe may retry only bounded transient readiness states (`candidate_count=0`, `main_window_count=0`, missing/mismatched early window PID). Hard identity/fence/conflict errors fail immediately. Error output remains sanitized.

## Non-goals

No physical retry, registration write, client launch/kill, credential access, auth, login, GUI input or Track B mutation is authorized by this repository-only task.
