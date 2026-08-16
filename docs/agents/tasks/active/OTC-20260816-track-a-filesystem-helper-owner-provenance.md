---
task_id: OTC-20260816-track-a-filesystem-helper-owner-provenance
status: investigating
agent: ChatGPT
session_id: chatgpt-filesystem-helper-owner-provenance-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260816-track-a-filesystem-helper-owner-provenance
base_branch: main
base_main: 9008bb7933db9e96119a61280941e695744e8408
risk: low
updated: 2026-08-16T11:46:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-filesystem-helper-owner-provenance.md
  - .github/workflows/tibia-official-client-re-filesystem-helper-owner-provenance-static.yml
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-beclient-path-static.md
  - docs/agents/reports/OTCLIENT-20260816-path-service-rtti-static.md
  - retained exact-client package from run 31904939696 as static file input only
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: GitHub Actions on synology-otclient-01 may inspect the retained exact client file statically without target execution
run_scope: single_task
continuation_policy: continue_within_owner_request
task_completion_policy: checkpoint_and_continue
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded static provenance question linking an already-proven TTibiaFileSystemHelper construction to the loader owner's shared field +0x20/+0x28
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
next_action: trace exact TTibiaFileSystemHelper construction/shared_ptr ownership into the object whose helper 0x6ba0b0 returns fields +0x20/+0x28, preserving UNKNOWN if a single causal chain cannot be proven
---

# Objective

Close the remaining direct-provenance gap between the exact client's proven `tibia::shared::TTibiaFileSystemHelper` construction sites and the loader path that calls helper `0x6ba0b0`, where that helper copies the owner's shared-pointer-like field `+0x20/+0x28` before invoking virtual slot `+0xd8` and ultimately feeding `QLibrary::setFileName`.

# Acceptance

1. Revalidate exact client size/SHA before every semantic run.
2. Prefer `objdump`/`llvm-objdump` bounded static disassembly when available; never execute or attach to the target.
3. Recover function boundaries/data flow around concrete TTibiaFileSystemHelper vptr construction sites `0x5ef510/0x5ef517` and `0x19a6a9e/0x19a6aa8`.
4. Recover the owner/helper path around `0x6ba0b0` and the loader callsite `0x6fc4f2`.
5. Search for a single instruction-boundary-safe causal chain from a constructed TTibiaFileSystemHelper object/shared_ptr to writes into the exact owner field `+0x20/+0x28` consumed by `0x6ba0b0`.
6. Promote the loader-owner field dynamic type to PROVEN only if that chain is direct; otherwise retain `NOT_DIRECTLY_PROVEN` and record the narrowest missing link.
7. Do not inspect BattlEye internal implementation, protection checks, anti-debug/detection logic, packet semantics, bypass/evasion, patching or unpacking.
8. Remove the temporary workflow before terminal closeout.

# Safety

Static exact retained-file analysis only (`runtime_access: none`). No Tibia/BattlEye execution/loading, live `/proc`, process memory/maps, attach/debug/injection, input/network/session mutation, credentials, binary patching, unpacking, anti-debug/detection or bypass/evasion work.

# E2E

`NOT_APPLICABLE`: static evidence reconstruction only; no executable behavior is changed.
