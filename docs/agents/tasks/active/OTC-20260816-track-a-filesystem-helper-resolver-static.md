---
task_id: OTC-20260816-track-a-filesystem-helper-resolver-static
status: investigating
agent: ChatGPT
session_id: chatgpt-filesystem-helper-resolver-static-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260816-track-a-filesystem-helper-resolver-static
base_branch: main
base_main: 2c56f7f2c7c01d8dbc1b66febeea22b1d4aff6e8
risk: low
updated: 2026-08-16T12:25:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-filesystem-helper-resolver-static.md
  - .github/workflows/tibia-official-client-re-filesystem-helper-resolver-static.yml
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-path-service-rtti-static.md
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-owner-provenance.md
  - retained exact-client package from run 31904939696 as static file input only
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: GitHub Actions on synology-otclient-01 can statically inspect the retained exact client without target execution
run_scope: single_task
continuation_policy: continue_within_owner_request
task_completion_policy: checkpoint_and_continue
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded client-side filesystem resolver question beneath TTibiaFileSystemHelper's proven BEClient wrapper
validation_level: focused
track_a_runtime_agent_admission_version: 1
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
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
next_action: validate shared::TFileSystemHelper primary vtable and trace exact slot +0x78 @ 0xcfa5e0 from TTibiaFileSystemHelper +0x30, following BEClient key/path transformations only on the client side
---

# Objective

Map the exact client-side filesystem/path resolver beneath the already-proven `TTibiaFileSystemHelper` wrapper:

```text
TTibiaFileSystemHelper +0xd8
  -> constructs "BEClient"
  -> TTibiaFileSystemHelper +0x30 @ 0xc9b890
  -> proven member this+0x18 = shared::TFileSystemHelper
  -> base helper virtual +0x78
```

Prove the base helper `+0x78` target and trace how the `"BEClient"` key plus forwarded value `9` are transformed toward the non-trivial result eventually passed to `QLibrary::setFileName`.

# Acceptance

1. Revalidate exact client size/SHA before every semantic run.
2. Validate `shared::TFileSystemHelper` RTTI/typeinfo/vtable boundaries before assigning slot `+0x78`.
3. Prove exact `+0x78` target (`0xcfa5e0` only if re-derived) and correlate the call at `0xc9b96f` with the same member object proven at `TTibiaFileSystemHelper+0x18`.
4. Decode bounded client-side resolver code and identify direct string/path transformations, Qt calls, constants, extension/platform rules, base-directory/resource-provider interactions and return-object construction only where statically proven.
5. Determine whether final value can be promoted to an exact filename/path (`BEClient`, `BEClient.so`, absolute/relative path, etc.); otherwise keep the narrowest unresolved transformation UNKNOWN.
6. Do not inspect or execute `BEClient.so` internals, anti-cheat protection checks, anti-debug/detection logic, packets, bypass/evasion, patching or unpacking.
7. Remove temporary workflow before terminal closeout.

# Safety

Static exact retained-file analysis only (`runtime_access: none`). No Tibia/BattlEye execution/loading, live `/proc`, process memory/maps, attach/debug/injection, input/network/session/credential mutation, binary patching, unpacking, anti-debug/detection or bypass/evasion work.

# E2E

`NOT_APPLICABLE`: static evidence reconstruction only.
