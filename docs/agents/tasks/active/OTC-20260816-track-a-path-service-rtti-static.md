---
task_id: OTC-20260816-track-a-path-service-rtti-static
status: investigating
agent: ChatGPT
session_id: chatgpt-path-service-rtti-static-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260816-track-a-path-service-rtti-static
base_branch: main
base_main: 8f81392f65ee53b2f7034771ba507e3ea422ccd7
risk: low
updated: 2026-08-16T11:22:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-path-service-rtti-static.md
  - .github/workflows/tibia-official-client-re-path-service-rtti-static.yml
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-beclient-static-integration.md
  - docs/agents/reports/OTCLIENT-20260816-beclient-path-static.md
  - retained exact-client package from run 31904939696 as static file input only
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded static type-identification question for the client service producing the QLibrary filename value
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
next_action: use exact-client RTTI/relocations/vtable evidence and instruction-boundary-safe static decoding where available to identify the owner+0x20/+0x28 service type and the source-level role/name of its loader-path virtual slot +0xd8
---

# Objective

Identify, if statically provable, the concrete client-side service type held in the owner shared-pointer field `+0x20/+0x28` and the source-level identity/role of the virtual method at slot `+0xd8` that produces the value later passed to `QLibrary::setFileName`.

# Safety

Static exact retained-file analysis only (`runtime_access: none`). No Tibia/BattlEye execution or loading, live `/proc`, attach/debug/injection, process memory, input, network/session mutation, binary patching, unpacking, anti-debug/detection analysis or bypass/evasion work.

# Acceptance

1. Revalidate exact client size/SHA before every semantic run.
2. Prefer instruction-boundary-safe decoders if already available on the runner; do not derive claims from raw byte-pattern counts.
3. Parse relocation/RTTI/vtable evidence around the helper cluster `0x6b9fa0`, `0x6ba000`, `0x6ba060`, `0x6ba0b0` and the service construction/ownership path.
4. Identify the service type/method only if direct typeinfo, vtable ownership, constructor assignment or equivalent causal evidence proves it.
5. Otherwise preserve the strongest bounded candidate set and exact missing link as UNKNOWN.
6. Do not broaden into BattlEye internal protection logic.
7. Remove temporary workflow before final merge.

# E2E

`NOT_APPLICABLE`: static evidence reconstruction only.
