---
task_id: OTC-20260828-current-loginservice-request-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260828-current-loginservice-request-promotion
base_branch: main
base_main: b359d583ba91ae45b0cac2c2fc94c0993d527ef7
created: 2026-08-28T01:48:00+02:00
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
owned_paths:
  - docs/agents/evidence/OTC-20260828-current-loginservice-request-promotion/**
  - docs/agents/tasks/active/OTC-20260828-current-loginservice-request-promotion.md
modules_touched: []
---

# Objective

Promote only the independently audited exact-current primary loginservice request contract recovered by source PR #733. The source workflow/analyzer remains unmerged.

# Primary evidence

```text
source PR        #733
source head      d278ae8e05e5f6a74c63b598d9d11e1c21f20b14
run              33127322903 = SUCCESS
job              98708447828 = SUCCESS
artifact         9668894065
artifact sha256  bd56db67ddb29e7e95915bfe13df10431afa016f3cbb369b42da096a700c876d
result sha256    43ec2cba35b22c4f8e651d7039c1b6aefd7047ee3cae8654e8af8acd21f392c9
```

# Acceptance

1. Docs/evidence only.
2. Primary builder `0xe1e780..0xe1eb21` and exact mandatory/conditional key split preserved.
3. Track B missing mandatory `operatingsystem` is promoted with value source `QSysInfo::prettyProductName()`.
4. Optional token/code fields are not synthesized.
5. `fromtimestamp/isreturner/showrewardnews/viewedid` are not promoted into the primary login request.
6. CI/governance pass on exact promotion head.
7. After merge, source #733 closes unmerged and lifecycle is archived before Track B service retry.

next_action: merge clean promotion, close/archive source, then add one evidence-derived `operatingsystem` field to Track B and perform one HTTP-only validation before any game login.
