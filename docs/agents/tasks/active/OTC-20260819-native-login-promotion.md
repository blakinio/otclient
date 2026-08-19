---
task_id: OTC-20260819-native-login-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: promotion
phase: exact-head-validation
branch: runtime/OTC-20260818-native-login-promotion
base_branch: main
base_main: aaf6706cfcd02e70511e5fa7e9ef9b0d7e1f0d12
execution_class: github_hosted
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
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
source_task: OTC-20260818-native-login-to-ingame-e2e
source_pr: 528
source_head: 8e029f5849a1d51f69486adcc3716c80f139e60e
coordinator_review: 4971140006
promotion_pr: 577
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-native-login-promotion.md
  - docs/agents/tasks/archive/OTC-20260818-native-login-to-ingame-e2e.md
  - docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
  - tools/tibia_runtime_bridge/current_sha_native_login_gate.py
  - tools/tibia_runtime_bridge/current_sha_secret_ingress.cpp
  - tools/tibia_runtime_bridge/experimental_character_control_current.cpp
---

# Native-login clean promotion admission

This coordinator task exists only to satisfy the Track A admission contract while accepted runtime-sensitive helper source is promoted from stale source PR #528 onto fresh `main`.

The promotion itself performs no physical runtime operation. It carries already-audited helper source and durable E2E evidence into canonical repository history.

```yaml
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
```

The physical login-to-world proof is historical accepted source evidence and is not repeated by this promotion task. The coordinator independent closeout audit used only GitHub-hosted static analysis and synthetic credentials.

## Exact next action

Run exact-head governance, CI and native-auth bridge validation for PR #577. If all required checks pass, revalidate `main` freshness and review hygiene, squash-merge #577, then remove this active promotion record in the lifecycle-only closeout while finalizing the source task archive and releasing ownership.
