---
task_id: OTC-20260826-current-game-login-schema
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260826-current-game-login-schema
related_pr: 711
base_branch: main
base_main: cfd535402bba8fe3f95d05c1b07c430b4efdddac
created: 2026-08-26T21:34:00+02:00
updated: 2026-08-27T00:07:00+02:00
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
repair_cycles_for_current_gate: 2
owned_paths:
  - .github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml
  - tools/tibia_re_current_game_login_schema/**
  - docs/agents/evidence/OTC-20260826-current-game-login-schema/**
  - docs/agents/tasks/active/OTC-20260826-current-game-login-schema.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_CURRENT_SCHEMA_CONTINUE_ALIAS.md
modules_touched:
  - official-client-re
  - protocol-research
reuses:
  - PR #499 historical protobuf schema methodology only
  - PR #706 promoted current wire-writer contract
depends_on:
  - current trusted-main wire-writer promotion/closeout lineage #706/#707
  - PR #284 structured current-build 0x14 checkpoint
blocks:
  - PR #284 next login-payload mutation/retry until coordinator promotion reaches trusted main
cross_repo_tasks: []
implementation_authorized: true
---

# Current game-login protobuf schema

Recover the exact current `GameclientMessageLogin` and `LoginRSAEncryptedBlock` protobuf wire schema for the official Linux client. Historical addresses and hashes are forbidden as current proof.

## Acceptance

- [x] Dynamically resolve and verify the current public Linux package fence.
- [x] Recover unique current RTTI/vtables for `GameclientMessageLogin` and `LoginRSAEncryptedBlock`, with controls.
- [x] Recover current ordered protobuf field numbers and wire types from generated serialization code.
- [x] Prove the nested-message relationship or keep it `UNKNOWN` if the current binary does not support it.
- [x] Recover only causal producer provenance necessary to distinguish Track B's legacy login payload; never infer semantic field names from strings/proximity.
- [x] No official-client execution, credentials, login, session capture, process memory or raw proprietary client upload.
- [x] Publish sanitized structural evidence only; historical `df7b29` addresses/hashes are forbidden as current inputs.
- [ ] Fresh independent coordinator audit, exact-head CI/governance and terminal source lifecycle before Track B consumes the result.

## Current boundary

Trusted `main` already proves current outer padding/XTEA/sequence/framing/Qt writer and rejects changing generic outer framing as the next hypothesis. This task is limited to the login-specific typed payload representation before that layer.

Durable evidence:

- `docs/agents/evidence/OTC-20260826-current-game-login-schema/20260826-current-game-login-schema.md`
- `docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_CURRENT_SCHEMA_CONTINUE_ALIAS.md`

Continuation alias:

`OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-SCHEMA-CONTINUE`

```yaml
checkpoint_version: 2
status: validating
phase: validate
branch: research/OTC-20260826-current-game-login-schema
pr: 711
main_observed: 8c7bc507aa5c1118aca0b8252dc422675add1be0
source_evidence_head: d24b6e61d1086094112020db6e7d959c24bdb34a
final_producer_run: 33017207072
final_producer_job: 98338388458
artifact: 9625060590
artifact_digest: sha256:be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
result_json_sha256: 1940d58a7fcb2615da7f9d47179e6dbdf41397f89b8b522af52da75b076154dc
exact_client:
  version: 15.32.75d4a0
  packed_sha256: 075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
  unpacked_sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
  unpacked_size: 52105824
proven:
  - Current generated protobuf ABI is +0x10 Clear, +0x18 ByteSizeLong, +0x28 InternalSerialize; +0x30 is the class-vtable terminator.
  - Current GameclientMessageLogin has fields 1/2/3/6 varint, 4/5 length-delimited, and field 7 embedded LoginRSAEncryptedBlock.
  - Current LoginRSAEncryptedBlock has fields 1/2/5/6/7 length-delimited and fields 3/4 varint.
  - Current producer is TLoginProtocolMessageHandler vslot +0x60 at 0xe25620, FDE 0xe25620..0xe2656d.
  - Current retained producer source type is TAuthenticationAndEncryptionInfo.
  - Track B generic outer framing remains structurally aligned; another outer-framing guess is rejected.
unknown:
  - User-facing semantic names of retained AuthInfo fields.
  - Password/session-token-to-specific-RSA-field semantic mapping.
  - Final causal explanation of Track B structured 0x14.
blockers:
  - Source evidence is not yet independently coordinator-promoted to trusted main; Track B may not consume unpromoted source facts.
continuation_prompt: docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_CURRENT_SCHEMA_CONTINUE_ALIAS.md
continuation_alias: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-SCHEMA-CONTINUE
next_action: Fresh independent coordinator must re-download/re-hash the exact source artifact, audit PR #711, promote accepted sanitized facts from current main, close/archive source lifecycle, then let Track B PR #284 consume only the promoted result.
```
