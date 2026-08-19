---
task_id: OTC-20260819-track-a-native-login-operator
status: active
session_role: implementer
project_lane: otclient
lane: RUNTIME_TOOLING
track_id: official-client-re
task_kind: permanent_operator
branch: ci/OTC-20260819-track-a-native-login-operator
base_branch: main
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
owned_paths:
  - .github/workflows/track-a-native-login.yml
  - docs/agents/operators/TRACK_A_NATIVE_LOGIN.md
  - docs/agents/tasks/active/OTC-20260819-track-a-native-login-operator.md
  - docs/agents/CHANGELOG.md
modules_touched: []
reuses:
  - tools/tibia_runtime_bridge current-SHA helpers
  - proven no-kill runtime flow from PR #599
depends_on:
  - PR #599
blocks: []
---

# Goal
Promote the proven Track A no-kill native login sequence into a permanent manually dispatched repository operator, with a short canonical invocation document for future agents.

# Constraints
This implementation task has `runtime_access: none`. It does not execute a physical login or touch a live official-client runtime. The permanent operator must preserve the exact current-client fence, one-shot admission, no-GUI login rule, no-kill post-handoff rule, helper peer provenance checks, unique-character fail-closed behavior, and structural IN_GAME 3/3 success gate.

# Validation
Review the full diff and run exact-head CI/governance. Runtime execution remains a separately authorized action at dispatch time.
