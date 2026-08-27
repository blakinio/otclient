---
task_id: OTC-20260828-current-game-login-value-promotion
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: archived
related_pr: 731
base_branch: main
base_main: 462320593ce3efc764af443c23c51ac725e1759a
created: 2026-08-28T00:09:00+02:00
completed: 2026-08-28T00:18:43+02:00
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
implementation_authorized: false
owned_paths: []
modules_touched: []
---

# Archived coordinator promotion — current game-login envelope/value facts

Terminal result: **DONE / PASS_BOUNDED / ACCEPT_WITH_EDITS**.

```text
source PR        #729 CLOSED UNMERGED
promotion PR     #731 MERGED
promotion head   2d385b479851973686948b0056af0965f3471648
promotion merge  13ffa467cb0743f07285e7dff481983a4f528c3d
CI               SUCCESS
Track A governance SUCCESS
```

Canonical evidence: `docs/agents/evidence/OTC-20260828-current-game-login-value-promotion/`.

The promotion proves the current `GameclientMessage` field-1000 login envelope, Linux scalar values `7/1532/1532`, nested field 5 as the 16-byte XTEA key, and rejects the legacy raw `0x0A` + fixed RSA login body for the exact current client. Unsupported semantic names remain bounded/UNKNOWN.

Track B #284 may now consume only these trusted-main facts and must make a material evidence-derived payload change before any further official-service E2E.
