---
task_id: OTC-20260816-track-a-filesystem-helper-owner-provenance
status: completed
agent: ChatGPT
session_id: chatgpt-filesystem-helper-owner-provenance-20260816
session_role: closeout
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: close
base_branch: main
implementation_pr: 346
superseded_pr: 340
implementation_head: 7308174a2770210989f2bf7d71abfc9e97df3caf
implementation_merge_commit: 2ad0dff19a3c6818d4c91915afbd2ee9a6655463
updated: 2026-08-16T12:24:00+02:00
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
report: docs/agents/reports/OTCLIENT-20260816-filesystem-helper-owner-provenance.md
semantic_validator:
  run: 31941120670
  job: 95150360284
  result: PASS
final_ci:
  head: 7308174a2770210989f2bf7d71abfc9e97df3caf
  run: 31941466306
  required_job: 95151212129
  result: PASS
track_a_governance:
  run: 31941466171
  deterministic_policy_job: 95151186340
  fresh_admission_job: 95151186391
  result: PASS
audit:
  result: PASS
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static evidence reconstruction only; no executable/runtime behavior changed
temporary_workflow_removed: true
ownership_released: true
next_action: none
---

# Final result

Direct ownership is PROVEN on the exact client:

```text
TTibiaFileSystemHelper shared_ptr
  -> TGameApplication+0x18/+0x20
  -> TGameApplication::vtable+0x78 @ 0x6c9760
  -> TGameClient factory @ 0x6c8020
  -> TGameClient+0x20/+0x28
```

The same concrete `TGameClient` construction owns/uses `+0x748`. The separate loader entry `0x6fc034` reads receiver `+0x748` and passes the same receiver to helper `0x6ba0b0`, which reads `+0x20/+0x28`.

## Evidence boundary

- `TGameClient+0x20/+0x28` direct `TTibiaFileSystemHelper` ownership: **PROVEN**.
- Loader receiver `+0x20/+0x28/+0x748` shape: **PROVEN**.
- Loader receiver exact dynamic/source-level type: **NOT_DIRECTLY_PROVEN**.
- Loader receiver `TGameClient` layout correlation: **DERIVED_HIGH_CONFIDENCE**.

The correct `TGameApplication::vtable+0x78` function entry is `0x6c9760`; temporary heuristic `0x6c976e` was rejected.

PR #340 was intentionally closed unmerged after its base became stale; PR #346 replayed only the audited final report/checkpoint on fresh `main` and passed current-base CI/governance before merge.

No Tibia/BattlEye execution/loading, live process observation, process memory/maps, attach/debug/injection, input/network/session mutation, binary patching, unpacking, anti-debug/detection analysis or bypass/evasion work occurred.
