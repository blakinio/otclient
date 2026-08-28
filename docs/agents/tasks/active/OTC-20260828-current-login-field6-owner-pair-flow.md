---
task_id: OTC-20260828-current-login-field6-owner-pair-flow
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: specify
branch: research/OTC-20260828-current-login-field6-owner-pair-flow
base_branch: main
base_main: 76515d605f7a76eebe25af0fd0dd68781f086f88
created: 2026-08-28T18:55:00+02:00
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
  - .github/workflows/tibia-official-client-re-current-login-field6-owner-pair-flow.yml
  - tools/tibia_re_current_login_field6_owner_pair_flow/**
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-owner-pair-flow.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-owner-pair-flow/**
modules_touched: []
reuses:
  - trusted-main promotion #747 current login field6 producer boundary
  - trusted-main exact-current fence #754
  - closed source PR #751 scalar candidates as eliminated hypothesis input only
blocks:
  - Track B PR #284 CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN
---

# Objective

On exact public Linux Tibia `15.32.75d4a0`, recover the real `edx` reaching value for `TLoginProtocolMessageHandler::slot+0x60 -> 0xe25620` by following the already-promoted `TAuthenticationProcessController` owner pair: handler pointer at `owner+0x9c0` and adjacent configuration object at `owner+0x9c8`.

The current exact constructor stores a mode-like dword at `config+0x30` immediately before committing that pair. Re-derive all exact reaching constants for that constructor store, then search only for causally linked reads of the same owner pair and prove whether `config+0x30` reaches producer `edx` at a handler `slot+0x60` call.

# Safety

Static GitHub-hosted analysis only. Do not execute the official client, log in, access credentials/session material/process memory, capture packets, perform gameplay, or upload the proprietary client. The exact client is transient and hash-fenced.

# Acceptance

1. Re-assert exact current SHA/size, handler vtable `0x30b6700`, slot `+0x60 -> 0xe25620`, owner constructor FDE `0x7d15c0..0x7d1a8a`, and owner pair stores `+0x9c0/+0x9c8`.
2. Recover CFG reaching constants for the exact constructor write to `config+0x30`; do not infer from nearby linear instructions.
3. Search for same-owner reads of `+0x9c0` and `+0x9c8`; accept a producer call only when the handler pointer reaches ABI `rdi`, the config value reaches ABI `edx`, and the call is exactly virtual slot `+0x60` on that same handler.
4. If same-FDE proof is absent, return `OWNER_PAIR_DIRECT_FLOW_UNKNOWN`; do not broaden automatically or rank heuristics.
5. Emit only sanitized addresses, instruction mnemonics/operands, constants and classifications.
6. No Track B mutation or official-service E2E from this source task.

next_action: prove hosted contract RED before package/client acquisition, then implement the smallest exact owner-pair analyzer.
