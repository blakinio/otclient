---
task_id: OTC-20260828-current-game-login-pre-success-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260828-current-game-login-pre-success-promotion
related_pr: 747
base_branch: main
base_main: e7f710b04da8c6f3adae43a019c44a6acb4a2866
created: 2026-08-28T11:36:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
mutation_authorized: false
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - docs/agents/evidence/OTC-20260828-current-game-login-pre-success-promotion/**
  - docs/agents/tasks/active/OTC-20260828-current-game-login-pre-success-promotion.md
modules_touched: []
reuses:
  - source Draft PR #743 exact-current sanitized evidence
blocks:
  - Track B PR #284 next official-service game E2E
---

# Objective

Promote only independently verified exact-current facts from source Draft #743. Do not promote its analyzer/workflow or invent the unresolved field-6 value.

# Acceptance

1. Preserve exact `15.32.75d4a0` client fence and source run/artifact identities.
2. Promote outer `GameclientMessageLogin.field6` as PRESENT and sourced from producer input `edx`, while keeping its value/name UNKNOWN.
3. Promote only structural nested AuthInfo source references; field 2 remains conditional and runtime values remain UNKNOWN.
4. Record exhausted bounded callsite discriminators without turning negative searches into a guessed value.
5. Explicitly block Track B mutation and game E2E until a material exact-current value delta exists.
6. Exact-head CI/governance and fresh read-only review must pass before merge.

next_action: require PR #747 exact-head green checks and zero material review blockers, merge, close source #743 unmerged as consumed, archive this promotion lifecycle, then checkpoint #284 as blocked on CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN.
