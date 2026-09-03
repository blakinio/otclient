---
task_id: OTC-20260903-be4f48-prelogin-sequence-rebind
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: implement
branch: research/OTC-20260903-be4f48-prelogin-sequence-rebind
base_branch: main
base_main: 05a0befa9670b164e5d88046584899ae3aaebb29
created: 2026-09-03T10:00:00+02:00
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
mutation_authorized: true
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-current-game-login-pre-success-outbound.yml
  - tools/tibia_re_current_game_login_pre_success_outbound/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-prelogin-sequence-rebind.md
reuses:
  - closed source PR #743 analyzer at 1342423c6fe4ef675f4b0b0cdc39ae012089f20e
  - trusted current client fence 15.32.be4f48 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
blocks:
  - Track B PR #284 next material outbound hypothesis
---

# Objective

Rebind the already-proven source-only pre-success outbound analyzer from closed PR #743 to exact current public Linux Tibia `15.32.be4f48` (`52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`) without changing analyzer architecture. Recover the bounded native outbound ordering from the game-server connection root through `GameclientMessageLogin` up to the first login-success receive edge.

# Safety

Static-only GitHub-hosted research. Do not execute the official client, log in, use credentials/session values, read process memory, capture packets, or upload the raw proprietary client. Do not modify Track B PR #284 and do not run an official-service E2E.

# Anti-loop

Only rebind the exact-client fence and repair the smallest build-drift assumptions proven by failing static gates. No new architecture, subsystem, or broad refactor.

# TDD evidence

1. Fence RED: commit `96ee55ae5b0757870359050ad6932cace4220c7e`, run `33742788471`, job `100608313904` failed at contract validation before package acquisition.
2. Fence GREEN: commit `17b1f32769570241174b74a48192a5274b00097f`, run `33742917386`, job `100608729800` succeeded on exact `be4f48`; sanitized result retained only.
3. Exact-current result remained `PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN`: direct-call BFS from current `TGameClient` roots did not reach any queue `send*`. This proves the next discriminator must target the indirect binding, not increase BFS depth.
4. Next RED requires a minimal `sendLogin` adapter xref/binding discriminator before implementation.

# Current exact boundary

`TProtocolMessageQueue::sendLogin` QMeta is proven exact-current and dispatches to an adapter, while the current `TGameClient` root graph has no direct edge to that QMeta entry. Recover the exact adapter and its static RIP/direct references, preserving UNKNOWN unless a unique causal binding is proven.

# Terminal outputs

- `PRE_LOGIN_SEQUENCE_COMPLETE=true|false`
- `PRE_LOGIN_MESSAGE_ORDER=<sanitized identities or UNKNOWN>`
- `PRE_LOGIN_REQUIRED_MESSAGE_MISSING_IN_OTCLIENT=<type or NONE/UNKNOWN>`
- `terminal_result=IMPLEMENTABLE_DELTA_PROVEN|STATIC_BOUNDARY_COMPLETE|INCONCLUSIVE`

next_action: prove RED for the missing sendLogin indirect-binding discriminator before implementing it.
