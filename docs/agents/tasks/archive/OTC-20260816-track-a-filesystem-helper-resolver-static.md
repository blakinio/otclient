---
task_id: OTC-20260816-track-a-filesystem-helper-resolver-static
status: completed
agent: ChatGPT
session_id: chatgpt-filesystem-helper-resolver-static-20260816
session_role: closeout
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: close
base_branch: main
implementation_pr: 352
superseded_pr: 348
implementation_head: 0e37d7cf32212d545a44cf217cacfd808015340e
implementation_merge_commit: a541fcc7e7188d9dccca4cd6ad89141e1fff2147
updated: 2026-08-16T12:52:00+02:00
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
report: docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
semantic_validator:
  run: 31942437204
  job: 95153445603
  result: PASS
final_ci:
  head: 0e37d7cf32212d545a44cf217cacfd808015340e
  run: 31942702348
  required_job: 95154088650
  result: PASS
track_a_governance:
  run: 31942702271
  deterministic_policy_job: 95154066828
  fresh_admission_job: 95154066849
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

The exact client-side QLibrary input is now reduced to the PROVEN symbolic/dynamic formula:

```text
J([J([QCoreApplication::applicationDirPath(), "BattlEye"]), "BEClient"])
```

where `J` appends `"/"`, appends each QString component, and finishes with `QDir::toNativeSeparators`.

Stable path-equivalent relative suffix:

```text
BattlEye/BEClient
```

The client resolver does not append `.so`.

## Evidence boundary

- symbolic/dynamic client formula: **PROVEN**;
- suffix `BattlEye/BEClient`: **PROVEN**;
- runtime application-directory prefix: **DYNAMIC**;
- exact native-Linux QLibrary candidate expansion / exact mapped file: downstream **UNKNOWN** in this task.

PR #348 was intentionally closed unmerged after its base became stale. Fresh-main PR #352 replayed only the audited report/checkpoint and passed current-base CI/governance before merge.

No Tibia/BattlEye execution/loading, live process observation, memory/maps, attach/debug/injection, input/network/session mutation, binary patching, unpacking, anti-debug/detection research, protocol inspection or bypass/evasion work occurred.
