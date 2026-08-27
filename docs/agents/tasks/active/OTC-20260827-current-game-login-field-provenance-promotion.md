---
task_id: OTC-20260827-current-game-login-field-provenance-promotion
status: in_progress
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: promotion
branch: docs/OTC-20260827-current-game-login-field-provenance-promotion
related_pr: 724
base_branch: main
base_main: faf3018d520f58ad7841cf3819b16ef159f27148
created: 2026-08-27T08:40:00+02:00
risk: high
execution_class: github_hosted
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
owned_paths:
  - docs/agents/evidence/OTC-20260827-current-game-login-field-provenance-promotion/
  - docs/agents/tasks/active/OTC-20260827-current-game-login-field-provenance-promotion.md
modules_touched: []
implementation_authorized: false
---

# Promote bounded current game-login field provenance

Coordinator source: Draft PR #722 at source head `36320a5e024f1ffab70592be52404da351b16b27`.

Fresh producer run `33046520991`, job `98431684189` passed on the exact fenced current Linux client and uploaded artifact `9635892718`. Coordinator independently re-downloaded it and verified:

```text
artifact sha256      fca8de5f33c1c80f57b80a7575a9f9eabf2664d7355c25275e02c2a479b49e62
result.json sha256   d4926050670959c78d3dc59d1fd3dff32ea328fbde0603c538ab43e3ea2510a7
```

Decision is `PASS_BOUNDED / ACCEPT_WITH_EDITS`: promote exact structural source-slot → protobuf-field relationships and exact identities only. Keep user-facing field names and password/session mapping `UNKNOWN`. The failed optional Qt metadata experiment is not promoted and does not weaken the fail-closed semantic boundary.

Runtime admission is explicitly non-runtime and fail-closed: every canonical runtime gate is `NOT_APPLICABLE`, no runtime namespace or registration is claimed, and mutation authorization is false.

No Track B #284 mutation or secret-bearing E2E is authorized by this task.
