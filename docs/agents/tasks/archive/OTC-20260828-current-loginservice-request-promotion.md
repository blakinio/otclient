---
task_id: OTC-20260828-current-loginservice-request-promotion
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: archived
related_pr: 734
base_branch: main
base_main: b359d583ba91ae45b0cac2c2fc94c0993d527ef7
created: 2026-08-28T01:48:00+02:00
completed: 2026-08-28T01:49:44+02:00
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

# Archived coordinator promotion — current loginservice request contract

Terminal result: **DONE / PASS_BOUNDED / ACCEPT_WITH_EDITS**.

```text
source PR        #733 CLOSED UNMERGED
promotion PR     #734 MERGED
promotion head   311826e82bc69d3d9ee40a5db19eaed04df3d756
promotion merge  4c0454af60a14321b363c3dc7d1f224a46e64153
CI               SUCCESS
Track A governance SUCCESS
```

Canonical evidence: `docs/agents/evidence/OTC-20260828-current-loginservice-request-promotion/`.

Track B may now add the one proven mandatory request field `operatingsystem`, sourced equivalently to current `QSysInfo::prettyProductName()`, and perform one HTTP-only validation before any game-login attempt.
