---
task_id: OTC-20260828-current-gameserver-dispatch-envelope-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260828-current-gameserver-dispatch-envelope-promotion
related_pr: 738
base_branch: main
base_main: 470d5bd285e29f9d3f24f70ff3fc5370e2990e2a
created: 2026-08-28T09:47:00+02:00
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
  - docs/agents/evidence/OTC-20260828-current-gameserver-dispatch-envelope-promotion/**
  - docs/agents/tasks/active/OTC-20260828-current-gameserver-dispatch-envelope-promotion.md
modules_touched: []
reuses:
  - trusted main current inbound XTEA/padding promotions
  - source-only PR #737 exact-current dispatch resolver
blocks:
  - Track B PR #284 current 0x34 fallback handling
---

# Objective

Promote only independently revalidated exact-current facts from source PR #737 that are necessary to stop Track B #284 from interpreting current dispatch `0x34` as legacy opcode 52.

# Primary evidence

```text
source PR       #737
source head     5273d52e0fdd3f0e2c212f633fb8e406409851ff
run             33152704802 = SUCCESS
job             98788182962 = SUCCESS
artifact        9678356574
artifact sha256 9bb4f18d2d684b4a7a0f5c9254367fdfc9786c633890b2beb5fe324c421aa918
result sha256   eabcb9445cdafd699fb266ee94b4aca9a1b006170007cbefe682b7a6579d3764
```

# Acceptance

1. Docs/evidence only; source workflow/analyzer is not promoted.
2. Exact `15.32.75d4a0` client fence is preserved.
3. Controls `0x14 -> LoginError`, `0x17 -> LoginSuccess`, `0x1f -> LoginChallenge` are independently retained.
4. `0x34` is promoted only as `UNKNOWN_FALLBACK`; no invented semantic name or payload schema.
5. Track B consequence is structural only: current 0x34 must not enter the legacy opcode-52 parser.
6. Exact-head CI and Track A governance must pass.
7. After merge, close source #737 unmerged as consumed, archive lifecycle, then allow #284 to implement a fail-closed current-fallback handler and one materially changed E2E.

next_action: require PR #738 exact-head green CI/governance and zero review blockers, merge, close source #737 unmerged as consumed, then continue Track B #284 with TDD.
