---
task_id: OTC-20260828-current-login-field6-scalar-owner
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: specify
branch: research/OTC-20260828-current-login-field6-scalar-owner
base_branch: main
base_main: 7a7a7cc4d09dee08ea07f8c91144d8ac869111b7
created: 2026-08-28T14:27:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-current-login-field6-scalar-owner.yml
  - tools/tibia_re_current_login_field6_scalar_owner/**
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-scalar-owner.md
modules_touched: []
reuses:
  - trusted-main promotion #747 exact current login producer boundary
hypothesis_inputs:
  - source-only PR #749 bounded scalar census; must be independently re-derived, not trusted as authority
blocks:
  - Track B PR #284 CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN
---

# Objective

On exact public Linux Tibia `15.32.75d4a0`, independently re-derive the statically scalar `call [vtable+0x60]` candidates and recover deterministic RTTI/QMeta/constructor provenance for only those caller FDEs. The goal is to bind exactly one scalar callsite to promoted `TLoginProtocolMessageHandler::slot+0x60 -> 0xe25620` and recover its exact `edx` value without ranking or semantic guessing.

# Safety

Static GitHub-hosted analysis only. Do not execute the official client, log in, access credentials/session material/process memory, capture packets, perform gameplay, or upload the proprietary client. The exact client is transient and hash-fenced.

# Acceptance

1. Re-assert trusted-main exact-current client hash/size and handler slot target.
2. Re-enumerate all `call [vtable+0x60]` sites and use CFG reaching definitions to independently recover only `UNIQUE_STATIC_SCALAR` `edx` candidates.
3. For each scalar candidate, recover caller-FDE RTTI/vtable owner sets and receiver provenance. For parent-member receivers, inspect only deterministic constructor/member bindings to the promoted handler type.
4. Prove `FIELD6_VALUE_PROVEN` only when exactly one scalar callsite is deterministically bound to the promoted handler slot. Otherwise return `FIELD6_VALUE_UNKNOWN`; never rank by address, frequency, value, namespace, or apparent semantics.
5. Emit only sanitized addresses, RTTI/QMeta names, instruction mnemonics/operands, proof classifications and scalar value if proven.
6. No Track B mutation or official-service E2E in this source task.

next_action: prove hosted contract RED before any package/client acquisition, then implement the minimum exact-static scalar-owner discriminator.
