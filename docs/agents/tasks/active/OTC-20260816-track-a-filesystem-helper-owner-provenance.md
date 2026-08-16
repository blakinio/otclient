---
task_id: OTC-20260816-track-a-filesystem-helper-owner-provenance
status: ready
agent: ChatGPT
session_id: chatgpt-filesystem-helper-owner-provenance-20260816
session_role: validator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: close
branch: docs/OTC-20260816-track-a-filesystem-helper-owner-provenance
base_branch: main
base_main: 9008bb7933db9e96119a61280941e695744e8408
risk: low
updated: 2026-08-16T12:15:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-filesystem-helper-owner-provenance.md
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-owner-provenance.md
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
run_scope: single_task
continuation_policy: continue_within_owner_request
task_completion_policy: checkpoint_and_continue
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded static provenance question linking a proven TTibiaFileSystemHelper shared allocation through application bootstrap into TGameClient ownership fields
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
validation_runs:
  - run: 31939981168
    job: 95147643269
    conclusion: success
    purpose: initial constructor/getter/loader bounded evidence
  - run: 31940685188
    job: 95149277266
    conclusion: success
    purpose: exact TGameApplication slot +0x78 RTTI/control-flow binding
  - run: 31940827055
    job: 95149640180
    conclusion: success
    purpose: TGameClient vtable and +0x748 structural binding
  - run: 31940915391
    job: 95149862971
    conclusion: success
    purpose: exact TGameClient +0x748 and +0x20/+0x28 anchors
  - run: 31940971580
    job: 95149999248
    conclusion: success
    purpose: exploratory loader-entry reference search; no direct reference found, absence not used as global proof
  - run: 31941120670
    job: 95150360284
    conclusion: success
    purpose: final deterministic ownership-provenance validator
report: docs/agents/reports/OTCLIENT-20260816-filesystem-helper-owner-provenance.md
audit:
  result: PASS
  basis: deterministic final exact-client validator plus explicit PROVEN/DERIVED/NOT_DIRECTLY_PROVEN separation
  material_findings_open: 0
e2e: NOT_APPLICABLE
e2e_reason: static evidence reconstruction only; no executable/runtime behavior changed
temporary_workflow_removed: true
last_completed_step: report audited; temporary workflow removed; retained diff is documentation only
next_action: exact-head CI/merge/archive, then continue with client-side shared::TFileSystemHelper resolver mapping
---

# Objective

Trace exact `TTibiaFileSystemHelper` shared ownership through application bootstrap and game-client construction into the `+0x20/+0x28` fields used by client code, without promoting the exact dynamic type of the separate loader callback receiver beyond direct evidence.

# Final result

## PROVEN

```text
TTibiaFileSystemHelper shared_ptr
  -> TGameApplication+0x18/+0x20
  -> TGameApplication::vtable+0x78
  -> TGameClient factory 0x6c8020
  -> TGameClient+0x20/+0x28
```

The same concrete TGameClient construction owns/uses `+0x748`. The loader entry separately reads receiver `+0x748` and passes the same receiver to helper `0x6ba0b0`, which reads `+0x20/+0x28`.

Final deterministic validator: `31941120670 / 95150360284`, success.

## DERIVED

Loader receiver has a high-confidence `TGameClient` layout correlation.

## NOT DIRECTLY PROVEN

Exact dynamic/source-level type and dispatch provenance of receiver at `0x6fc034` remain not directly proven.

## Correction

The exact `TGameApplication::slot+0x78` function entry is `0x6c9760`, not temporary heuristic address `0x6c976e`.

# Audit

PASS. Direct TGameClient filesystem-helper ownership is PROVEN; loader callback receiver type remains explicitly bounded.

# Safety

Static exact retained-file analysis only (`runtime_access: none`). No Tibia/BattlEye execution/loading, live process observation, memory/maps, attach/debug/injection, input/network/session mutation, binary patching, unpacking, anti-debug/detection analysis or bypass/evasion work.

# E2E

`NOT_APPLICABLE`: no executable/runtime behavior changed.
