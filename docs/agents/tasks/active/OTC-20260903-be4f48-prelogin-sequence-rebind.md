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

# TDD gate

1. RED: copied #743 workflow remains on `75d4a0`; `test_contract.py` must fail because exact-current `be4f48` is required.
2. GREEN: update only the exact-current fence and any minimally proven drift; contract must pass before package acquisition.
3. Run one source-only analysis and consume only sanitized `result.json`.

# Terminal outputs

- `PRE_LOGIN_SEQUENCE_COMPLETE=true|false`
- `PRE_LOGIN_MESSAGE_ORDER=<sanitized identities or UNKNOWN>`
- `PRE_LOGIN_REQUIRED_MESSAGE_MISSING_IN_OTCLIENT=<type or NONE/UNKNOWN>`
- `terminal_result=IMPLEMENTABLE_DELTA_PROVEN|STATIC_BOUNDARY_COMPLETE|INCONCLUSIVE`

next_action: prove RED on the stale #743 fence before changing the workflow fence.
