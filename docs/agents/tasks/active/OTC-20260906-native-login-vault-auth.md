---
task_id: OTC-20260906-native-login-vault-auth
status: implementing
agent: ChatGPT
session_id: native-login-vault-auth-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME-P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: implementation
branch: feat/OTC-20260906-native-login-vault-auth
base_branch: main
created: 2026-09-06T14:12:00Z
updated_at: 2026-09-06T14:12:00Z
base_main: 874b95d6e90da693868af9ec504654b8635ea462
policy_version: 2
prompting_standard_version: 2.1
execution_mode: chatgpt
execution_reason: bridge the existing machine-local encrypted Track A secret vault to the exact-current native auth FD transport without credential environment or argv ingress
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: true
run_scope: bounded
continuation_policy: continue_until_real_stop
owned_paths:
  - tools/tibia_runtime_bridge/secret_vault_auth.py
  - tests/tools/tibia_runtime_bridge/test_secret_vault_auth.py
  - .github/workflows/track-a-native-auth-bridge.yml
  - docs/agents/tasks/active/OTC-20260906-native-login-vault-auth.md
modules_touched:
  - Track A native auth secret producer
reuses:
  - tools/tibia_runtime_bridge/secret_vault.py
  - tools/tibia_runtime_bridge/experimental_auth_client.py
  - tools/tibia_re_control_center/current_client_fence.py
depends_on:
  - OTC-20260905-control-center-native-login-start
blocks:
  - OTC-20260905-control-center-native-login-start
cross_repository_task_ids: []
next_action: prove a focused RED contract for current-fence vault-to-auth FD handoff before adding the producer
---

# OTC-20260906 — native login vault auth

## Objective

Add the smallest secret-free command surface that consumes the already-proven machine-local encrypted Track A vault and hands one fully sealed credential memfd to the exact-current native auth socket with a Gate-B-approved runtime identity.

## Required behavior

- actual login consumption must reject `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` in the environment;
- no credential value or credential file path is accepted through argv, stdin, browser/API, task text or logs;
- decrypt only through `secret_vault.decrypt_to_sealed_memfd()`;
- pass only the sealed descriptor through `experimental_auth_client.auth_with_credentials_fd()`;
- runtime identity must match the central current-client fence and explicit boot/PID/start identity;
- always close the credential descriptor;
- output only a small allowlisted sanitized result;
- no official client execution or physical runtime access occurs from this PR branch.

## Validation plan

1. focused test RED because the producer does not exist;
2. minimal producer implementation;
3. focused synthetic GREEN tests;
4. native-auth bridge validation + Track A governance + self-hosted PR boundary + general CI;
5. full diff/review hygiene; Ready and protected squash merge.
