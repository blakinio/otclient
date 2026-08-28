---
task_id: OTC-20260828-current-game-login-pre-success-outbound
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: specify
branch: research/OTC-20260828-current-game-login-pre-success-outbound
base_branch: main
base_main: a1e6c1a563e62499abfbf411aacfbbf688fad523
created: 2026-08-28T10:18:00+02:00
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
  - .github/workflows/tibia-official-client-re-current-game-login-pre-success-outbound.yml
  - tools/tibia_re_current_game_login_pre_success_outbound/**
  - docs/agents/tasks/active/OTC-20260828-current-game-login-pre-success-outbound.md
modules_touched: []
reuses:
  - trusted main current game-login schema/value/provenance promotions
  - sanitized source artifact from closed PR #729
blocks:
  - Track B PR #284 next material outbound hypothesis
---

# Objective

Recover, on exact public Linux Tibia `15.32.75d4a0`, the complete static outbound boundary from first game-server connection through native `sendLogin` and up to the first login-success receive edge. Determine whether native code emits any additional `GameclientMessage*` before success and whether `GameclientMessageLogin.field6` or `LoginRSAEncryptedBlock.fields1/2/6/7` are actually populated on the proved primary producer path.

# Safety

Static-only GitHub-hosted research. Do not execute the official client, log in, access credentials/session values/process memory, capture packets, or upload proprietary client bytes. Exact client is transient and hash-fenced; artifacts contain only sanitized structural JSON.

# Acceptance

1. Re-derive current QMeta/RTTI identities; do not trust old absolute addresses as authority.
2. Recover the full `TLoginProtocolMessageHandler` primary login producer FDE and the complete current message storage writes.
3. Classify presence/absence of outer field6 and nested fields1/2/6/7 structurally, without inventing user-facing names.
4. Recover all current `TProtocolMessageQueue` `send*` methods causally reachable in the first game-server connection/login path before the login-success receive edge; distinguish direct proof from UNKNOWN.
5. Emit fail-closed sanitized JSON and preserve unsupported semantics as UNKNOWN.
6. No Track B mutation or official-service E2E in this source task.

next_action: prove hosted TDD RED before package acquisition, then implement the smallest exact-current static analyzer.
