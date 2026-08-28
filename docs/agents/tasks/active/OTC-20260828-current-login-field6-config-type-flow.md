---
task_id: OTC-20260828-current-login-field6-config-type-flow
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: specify
branch: research/OTC-20260828-current-login-field6-config-type-flow
base_branch: main
base_main: 76515d605f7a76eebe25af0fd0dd68781f086f88
created: 2026-08-28T19:02:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-current-login-field6-config-type-flow.yml
  - tools/tibia_re_current_login_field6_config_type_flow/**
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-config-type-flow.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-config-type-flow/**
modules_touched: []
reuses:
  - trusted-main promotion #747 field6 producer boundary
  - trusted-main exact-current fence #754
  - closed source PR #757 owner-pair boundary
blocks:
  - Track B PR #284 CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN
---

# Objective

On exact public Linux Tibia `15.32.75d4a0`, identify the exact RTTI/vtable type of the config object stored at `TAuthenticationProcessController owner+0x9c8` in constructor FDE `0x7d15c0..0x7d1a8a`, then inspect only that type's owned methods / direct helpers for a causal transfer of its `+0x30` dword into `edx` at `TLoginProtocolMessageHandler::slot+0x60 -> 0xe25620`.

# Safety

Static GitHub-hosted analysis only. No official-client execution, login, credentials/session access, process memory, packet capture, gameplay, or proprietary binary upload.

# Acceptance

1. Re-assert exact current SHA/size and owner constructor/handler slot identities.
2. Recover the vtable store that initializes the exact object later stored to owner `+0x9c8`; resolve exactly one RTTI type or return `CONFIG_TYPE_UNKNOWN`.
3. Enumerate only methods owned by that exact type (vtable targets and QMeta cases when available), plus direct callees depth <=2.
4. Prove field6 only if one bounded path reads `this/config +0x30`, supplies that value to ABI `edx`, supplies the exact login handler to ABI `rdi`, and calls virtual slot `+0x60` on that handler.
5. Do not rank unrelated callsites or infer value from constructor defaults alone.
6. Emit sanitized structural JSON only; no Track B mutation/E2E from source task.

next_action: prove hosted contract RED before package/client acquisition, then implement focused config-type analyzer.
