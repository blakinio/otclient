---
task_id: OTC-20260828-current-loginservice-request-contract
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260828-current-loginservice-request-contract
base_branch: main
base_main: b359d583ba91ae45b0cac2c2fc94c0993d527ef7
created: 2026-08-28T01:30:00+02:00
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
  - .github/workflows/tibia-official-client-re-loginservice-request.yml
  - tools/tibia_re_loginservice_request/**
  - docs/agents/tasks/active/OTC-20260828-current-loginservice-request-contract.md
modules_touched: []
reuses:
  - trusted exact current client fence from PR #731
  - Track B HTTP errorCode=7 evidence in PR #284
---

# Objective

Resolve, without runtime/login/secret access, the exact-current official-client loginservice request key contract needed to diagnose Track B's stable pre-session `errorCode=7` rejection.

The only authorized question is whether exact `15.32.75d4a0` contains and co-locates the request keys `email`, `password`, `stayloggedin`, `type`, `clientversion`, `clienttype`, `assetversion`, `devicecookie`, `fromtimestamp`, `isreturner`, `showrewardnews`, `viewedid`, and what builder dataflow/defaults are directly visible.

No HTTP login is performed. No credentials or session values are read. No raw official binary is uploaded.

# Acceptance

1. Re-bind the exact public client fence.
2. Locate exact request-key literals and RIP-relative xrefs.
3. Group them by exact FDE and emit bounded disassembly snapshots only.
4. Promote only keys/defaults whose current exact dataflow is visible; otherwise leave value semantics UNKNOWN.
5. Source workflow/analyzer remains unmerged; coordinator-only clean evidence promotion if sufficient.

next_action: run exact hosted static discriminator, independently inspect/re-hash the sanitized artifact, then decide whether Track B has a material evidence-derived HTTP request repair.
