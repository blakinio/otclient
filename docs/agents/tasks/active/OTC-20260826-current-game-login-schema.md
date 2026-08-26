---
task_id: OTC-20260826-current-game-login-schema
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260826-current-game-login-schema
base_branch: main
base_main: cfd535402bba8fe3f95d05c1b07c430b4efdddac
created: 2026-08-26T21:34:00+02:00
updated: 2026-08-26T21:34:00+02:00
risk: high
execution_mode: github_actions_hosted
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
promotion_authority: coordinator_only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
policy_version: 2
validation_level: focused
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml
  - tools/tibia_re_current_game_login_schema/**
  - docs/agents/evidence/OTC-20260826-current-game-login-schema/**
  - docs/agents/tasks/active/OTC-20260826-current-game-login-schema.md
modules_touched:
  - official-client-re
  - protocol-research
reuses:
  - PR #499 historical protobuf schema methodology only
  - PR #706 promoted current wire-writer contract
depends_on:
  - main@64189859 current wire-writer archive lineage
  - PR #284 structured current-build 0x14 checkpoint
blocks:
  - PR #284 next login-payload mutation/retry
cross_repo_tasks: []
implementation_authorized: true
---

# Current game-login protobuf schema

Recover the exact current `GameclientMessageLogin` and `LoginRSAEncryptedBlock` protobuf wire schema for the official Linux client. Historical addresses and hashes are forbidden as current proof.

## Acceptance

- [ ] Dynamically resolve and verify the current public Linux package fence.
- [ ] Recover unique current RTTI/vtables for `GameclientMessageLogin` and `LoginRSAEncryptedBlock`, with controls.
- [ ] Recover current ordered protobuf field numbers and wire types from generated serialization code.
- [ ] Prove the nested-message relationship or keep it `UNKNOWN` if the current binary does not support it.
- [ ] Recover only causal producer provenance necessary to distinguish Track B's legacy login payload; never infer semantic field names from strings/proximity.
- [ ] No official-client execution, credentials, login, session capture, process memory or raw proprietary client upload.
- [ ] Publish sanitized structural evidence only; historical `df7b29` addresses/hashes are forbidden as current inputs.
- [ ] Fresh independent coordinator audit, exact-head CI/governance and terminal source lifecycle before Track B consumes the result.

## Current boundary

Trusted `main` already proves current outer padding/XTEA/sequence/framing/Qt writer and rejects changing generic outer framing as the next hypothesis. This task is limited to the login-specific typed payload representation before that layer.

```yaml
checkpoint_version: 1
status: investigating
head: cfd535402bba8fe3f95d05c1b07c430b4efdddac
pr: 711
proven:
  - no existing open PR/branch owns this exact current-login-schema scope
unknown:
  - current GameclientMessageLogin field schema
  - current LoginRSAEncryptedBlock field schema
  - current causal mapping of those fields to retained auth/session state
blockers: []
next_action: publish the claim as an early Draft PR, then implement a TDD current-package static schema producer
```
