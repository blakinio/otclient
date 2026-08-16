---
task_id: OTC-20260816-track-a-path-service-rtti-static
status: completed
agent: ChatGPT
session_id: chatgpt-path-service-rtti-static-20260816
session_role: closeout
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: close
base_branch: main
implementation_pr: 337
implementation_head: 50a73889736fdf0a34ce8fadc4906ba67d80087b
implementation_merge_commit: 80dcb8359def08976d60f1389d244f0046cc3488
updated: 2026-08-16T11:38:00+02:00
owned_paths: []
modules_touched: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
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
report: docs/agents/reports/OTCLIENT-20260816-path-service-rtti-static.md
audit:
  result: PASS
  basis: deterministic final validator plus bounded offline decoding and fresh evidence-classification review
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static evidence reconstruction only; no executable or runtime behavior changed
final_ci:
  head: 50a73889736fdf0a34ce8fadc4906ba67d80087b
  run: 31939465432
  required_job: 95146470294
  result: PASS
track_a_governance:
  run: 31939456187
  fresh_admission_job: 95146406457
  deterministic_policy_job: 95146406506
  result: PASS
temporary_workflow_removed: true
ownership_released: true
next_action: none
---

# Final result

The exact official Linux Tibia client statically identifies and instantiates:

```text
tibia::shared::TTibiaFileSystemHelper
mangled: N5tibia6shared22TTibiaFileSystemHelperE
typeinfo: 0x3070940
vtable address point: 0x2f62080
```

The validated primary vtable is continuous with relocation-backed `.text` targets from `+0x00` through `+0xf8`; key slots are:

```text
+0x30 -> 0xc9b890
+0xd8 -> 0xc95cb0
```

The exact vptr is written into concrete embedded objects at two independent construction sites: `0x5ef510/0x5ef517` and `0x19a6a9e/0x19a6aa8`.

## PROVEN

`0xc95cb0`, the concrete class's `+0xd8` method, constructs exact key `"BEClient"` with length `8` through the Qt string-construction target and calls the same object's virtual slot `+0x30`.

`0xc9b890`, the class's `+0x30` method, calls own slot `+0x28`, reads member `this+0x18`, obtains that member object's slot `+0x78`, prepares a temporary non-trivial block/sequence and delegates through that slot.

Final deterministic validator: `31939306766 / 95146060860`, success.

## DERIVED

The client-side role of `TTibiaFileSystemHelper::vtable+0xd8` is a high-confidence **BEClient-key path/resource resolution wrapper**. This is not a recovered source-level method name.

Combined with the predecessor's independently proven loader flow (`owner service -> virtual +0xd8 -> result -> QLibrary::setFileName`), this supplies the missing causal link for the exact `BEClient` xref at `0xc95cb2`.

## UNKNOWN / NOT DIRECTLY PROVEN

- direct assignment proving that loader owner `+0x20/+0x28` stores a `TTibiaFileSystemHelper` instance;
- source-level names/signatures of virtual slots `+0xd8`, `+0x30`, `+0x28` and member `+0x78`;
- semantic meaning of forwarded value `9`;
- exact type of member `this+0x18` and the temporary sequence/block;
- concrete runtime `QString` passed to `QLibrary::setFileName` and exact filesystem path ultimately opened.

## Corrections

Other similarly named FileSystemHelper first-pass `+0xd8` mappings were rejected after exact vtable-boundary validation showed intervening RTTI/vtable groups. Only the uninterrupted `TTibiaFileSystemHelper` group is retained for this mapping.

The old observation of `BEClient` at `0xc95cb2` was correctly insufficient on its own; the new RTTI/vtable evidence plus predecessor filename data-flow now makes it causally connected loader-side evidence.

## Evidence

```text
31938853042 / 95144958602  RTTI/relocation candidate discovery
31938968180 / 95145240491  exact vtable-boundary validation and c95cb0 discovery
31939144527 / 95145667546  bounded vtable/construction/generic-resolver windows
31939306766 / 95146060860  deterministic final validator: PASS
```

No Tibia/BattlEye execution/loading, live runtime observation, process memory/maps, attach/debug/injection, input/network/session mutation, binary patching, unpacking, anti-debug/detection analysis or bypass/evasion work occurred.
