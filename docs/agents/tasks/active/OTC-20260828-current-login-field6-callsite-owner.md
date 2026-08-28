---
task_id: OTC-20260828-current-login-field6-callsite-owner
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: specify
branch: research/OTC-20260828-current-login-field6-callsite-owner
base_branch: main
base_main: 7a7a7cc4d09dee08ea07f8c91144d8ac869111b7
created: 2026-08-28T11:58:00+02:00
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
  - .github/workflows/tibia-official-client-re-current-login-field6-callsite-owner.yml
  - tools/tibia_re_current_login_field6_callsite_owner/**
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-callsite-owner.md
modules_touched: []
reuses:
  - trusted-main promotion #747 current login field6 boundary
blocks:
  - Track B PR #284 CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN
---

# Objective

On exact public Linux Tibia `15.32.75d4a0`, resolve only the virtual `TLoginProtocolMessageHandler` slot `+0x60` caller that reaches promoted producer `0xe25620`. Use compiler/static type evidence to reject unrelated `+0x60` calls, then recover the reaching value supplied in `edx` at that exact callsite.

# Safety

Static GitHub-hosted analysis only. Do not execute the official client, log in, access credentials/session material/process memory, capture packets, perform gameplay, or upload the proprietary client. The exact client is transient and hash-fenced.

# Acceptance

1. Re-assert promoted exact-current client hash and handler slot target.
2. Enumerate `call [vtable+0x60]` sites but accept a caller only with a deterministic type/target binding to `TLoginProtocolMessageHandler::slot+0x60 -> 0xe25620`.
3. Recover CFG reaching definitions of `edx` at the accepted callsite. If no unique callsite/value is proven, return UNKNOWN and stop; do not rank heuristics.
4. Emit only sanitized addresses, RTTI names, instruction mnemonics/operands, classifications and scalar value if statically proven.
5. No Track B mutation or official-service E2E in this source task.

next_action: prove hosted contract RED before package/client acquisition, then implement the smallest static discriminator.