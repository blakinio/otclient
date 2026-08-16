---
task_id: OTC-20260816-track-a-path-service-rtti-static
status: ready
agent: ChatGPT
session_id: chatgpt-path-service-rtti-static-20260816
session_role: validator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: close
branch: research/OTC-20260816-track-a-path-service-rtti-static
base_branch: main
base_main: 8f81392f65ee53b2f7034771ba507e3ea422ccd7
risk: low
updated: 2026-08-16T11:35:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-path-service-rtti-static.md
  - docs/agents/reports/OTCLIENT-20260816-path-service-rtti-static.md
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
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded static type-identification question for the client service producing the QLibrary filename value
validation_level: focused
heavy_validation_runs: 0
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
validation_runs:
  - run: 31938853042
    job: 95144958602
    conclusion: success
    purpose: initial RTTI/relocation candidate discovery
  - run: 31938968180
    job: 95145240491
    conclusion: success
    purpose: candidate vtable-boundary validation and c95cb0 BEClient wrapper discovery
  - run: 31939144527
    job: 95145667546
    conclusion: success
    purpose: bounded concrete vtable, construction-site and generic-resolver windows
  - run: 31939306766
    job: 95146060860
    conclusion: success
    purpose: final deterministic path-service validator
report: docs/agents/reports/OTCLIENT-20260816-path-service-rtti-static.md
audit:
  result: PASS
  basis: deterministic final validator plus bounded offline decoding and fresh evidence-classification review
  material_findings_open: 0
e2e: NOT_APPLICABLE
e2e_reason: static evidence reconstruction only; no executable or runtime behavior changed
temporary_workflow_removed: true
last_completed_step: final deterministic validator passed; report persisted; temporary workflow removed; retained diff is documentation only
next_action: complete exact-head required repository CI, merge PR #337, then archive this task and release ownership
---

# Objective

Identify, if statically provable, the concrete client-side service type held in the owner shared-pointer field `+0x20/+0x28` and the source-level identity/role of the virtual method at slot `+0xd8` that produces the value later passed to `QLibrary::setFileName`.

# Final research result

## PROVEN

The exact binary contains and instantiates `tibia::shared::TTibiaFileSystemHelper`:

```text
mangled type name: N5tibia6shared22TTibiaFileSystemHelperE
name VA: 0x1c95880
typeinfo: 0x3070940
vtable typeinfo slot: 0x2f62078
offset-to-top: 0
vtable address point: 0x2f62080
```

Every relocation-backed virtual entry from `+0x00` through `+0xf8` in this vtable group resolves to `.text`. Relevant slots:

```text
+0x30 -> 0xc9b890
+0xd8 -> 0xc95cb0
```

The concrete vptr `0x2f62080` is written into embedded objects at two independent exact construction sites (`0x5ef510/0x5ef517` and `0x19a6a9e/0x19a6aa8`).

`0xc95cb0` directly constructs the exact key `"BEClient"` with length 8 through the Qt string-construction target `0x4df210`, then invokes the same object's virtual slot `+0x30`.

`0xc9b890` calls the same object's `+0x28`, reads a member at `this+0x18`, loads that member object's virtual slot `+0x78`, prepares a temporary non-trivial sequence/block and delegates through that slot.

## DERIVED

The client-side role of `TTibiaFileSystemHelper::vtable+0xd8` is a high-confidence **BEClient-key path/resource resolution wrapper**. This is a role description, not a recovered source-level method name.

Combined with the predecessor's proven loader flow (`owner service -> virtual +0xd8 -> local result -> QLibrary::setFileName`), this supplies the missing causal link for the earlier `BEClient` xref at `0xc95cb2`.

## UNKNOWN / NOT DIRECTLY PROVEN

- direct construction/assignment provenance proving that the exact loader owner field `+0x20/+0x28` stores a `TTibiaFileSystemHelper` instance;
- exact source-level names/signatures of slots `+0xd8`, `+0x30`, `+0x28` and the member object's `+0x78`;
- meaning of forwarded value `9`;
- exact type of the `this+0x18` member and temporary sequence/block;
- concrete runtime `QString` returned to `QLibrary::setFileName` and exact filesystem path opened.

## CORRECTION

Other similarly named FileSystemHelper candidates from the first RTTI sweep crossed new RTTI/vtable boundaries before the mechanically calculated `+0xd8`; those candidate mappings are rejected. Only the uninterrupted `TTibiaFileSystemHelper` group is retained for the `+0xd8` mapping.

The earlier `BEClient` string observation remains historically correct as insufficient on its own; the new RTTI/vtable + predecessor data-flow evidence now turns that exact xref into causally connected loader-side evidence.

# Audit

PASS. The final retained documentation preserves exact RTTI/vtable and deterministic validator facts, keeps the loader-owner field's direct dynamic type as not directly proven, keeps source-level method names and concrete runtime path UNKNOWN, and records rejected first-pass candidate mappings explicitly.

# Safety

Static exact retained-file analysis only (`runtime_access: none`). No Tibia/BattlEye execution/loading, live `/proc`, attach/debug/injection, process memory, input, network/session mutation, binary patching, unpacking, anti-debug/detection analysis or bypass/evasion work.

# E2E

`NOT_APPLICABLE`: static evidence reconstruction only.
