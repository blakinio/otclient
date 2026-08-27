---
task_id: OTC-20260828-current-game-login-value-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260827-current-game-login-value-promotion
base_branch: main
base_main: 462320593ce3efc764af443c23c51ac725e1759a
created: 2026-08-28T00:09:00+02:00
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
  - docs/agents/evidence/OTC-20260828-current-game-login-value-promotion/**
  - docs/agents/tasks/active/OTC-20260828-current-game-login-value-promotion.md
modules_touched: []
reuses:
  - PR #706 current final writer promotion
  - PR #719 current game-login schema promotion
  - PR #724 current AuthInfo-to-wire structural provenance
  - PR #729 source-only exact current discriminator
---

# Objective

Promote only independently audited exact-current facts needed to replace Track B #284's disproven legacy login application body. Do not merge source workflow/analyzer code and do not invent unresolved user-facing semantic field names.

# Primary evidence

```text
source PR       #729
source head     9876df611c8bf7f9c5cd07b3b28f5d12ee8c6e28
run             33121134592 = SUCCESS
job             98687978755 = SUCCESS
artifact        9666544571
artifact sha256 af5b57e8dbd5a5b0b597f71d4d367e7c9511aa98c56c10ba7cc8380db9050ebf
trace sha256    c1b37821925939295cde1bdcae657af338d7cfd370704e201bcb438d7d52180d
```

# Acceptance

1. Docs/evidence only.
2. Exact current `GameclientMessage` envelope and field-1000 login payload are preserved.
3. Linux field1=7, field2=1532, field3=1532 and nested field5=XTEA-key are promoted only at their proved strength.
4. No unsupported password/session/character field names are promoted.
5. CI and Track A governance must pass on the exact promotion head.
6. After merge, close source #729 unmerged as consumed/superseded, archive lifecycle, then allow #284 to consume the promoted facts.

next_action: open clean promotion PR, require green CI/governance, merge, close/archive source, then continue Track B #284 with TDD and one materially changed E2E.
