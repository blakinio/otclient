---
task_id: OTC-20260816-track-a-beclient-path-static
status: completed
agent: ChatGPT
session_id: chatgpt-beclient-path-static-20260816
session_role: closeout
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: close
base_branch: main
implementation_pr: 335
implementation_head: 05eac806e933c6dd3241bb8e17a91b1dbaef3ee4
implementation_merge_commit: 875c70cf492000409f083053ed53e00e35a734ca
updated: 2026-08-16T11:20:00+02:00
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
report: docs/agents/reports/OTCLIENT-20260816-beclient-path-static.md
audit:
  result: PASS
  basis: deterministic exact-client validator plus final diff/provenance review
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static evidence reconstruction only; no executable or runtime behavior changed
final_ci:
  head: 05eac806e933c6dd3241bb8e17a91b1dbaef3ee4
  run: 31938673744
  required_job: 95144535650
  result: PASS
track_a_governance:
  run: 31938654965
  fresh_admission_job: 95144467595
  deterministic_policy_job: 95144467613
  result: PASS
temporary_workflow_removed: true
ownership_released: true
next_action: none
---

# Final result

The exact client-side value flow feeding `QLibrary::setFileName` was recovered without executing Tibia or BattlEye:

```text
owner shared service (+0x20/+0x28)
  -> helper 0x6ba0b0
  -> service object
  -> virtual slot +0xd8 writes a local non-trivial result at [rbp-0xc0]
  -> same local pointer saved at [rbp-0x138]
  -> QLibrary::setFileName @ 0x6fcaba
  -> QLibrary::load @ 0x6fcac2
```

Final deterministic semantic evidence: run `31938495208`, job `95144070320`, `success`.

## Evidence classification

### PROVEN

- loader-specific instruction-boundary chain above;
- exact `QLibrary::setFileName` and `QLibrary::load` call targets;
- exact full literals `BEClient.so`, `BattlEye/BEClient.so`, `/BattlEye/BEClient.so` absent in tested ASCII/UTF-16LE forms;
- temporary workflow removed before merge;
- no target/runtime/mutation activity occurred.

### DERIVED

The service virtual method behaves consistently with a string/non-trivial result producer supplying the QLibrary filename value. Together with predecessor proof that `bin/BattlEye/BEClient.so` is the only retained exact-package ELF exporting exact `Init`, client-to-BEClient linkage remains high-confidence DERIVED.

### UNKNOWN

- concrete runtime `QString` passed to `QLibrary::setFileName`;
- exact source-level service class and method name;
- exact filesystem path ultimately opened.

### DISPROVEN / corrected

A raw client-wide byte sweep for apparent `vtable+0xd8` calls was not instruction-boundary-safe. Its numerical census is rejected and carries no semantic conclusion. The loader-specific `+0xd8` call is separately proven at a known exact instruction boundary.

## Validation provenance

```text
31938041809 / 95142953265
31938092847 / 95143078419
31938126533 / 95143159436
31938202217 / 95143350273
31938263883 / 95143505149
31938348199 / 95143716438  exploratory raw sweep; count rejected
31938451474 / 95143965655  failed only on rejected raw census assertion
31938495208 / 95144070320  final deterministic validator: SUCCESS
```

Final required repository CI and Track A governance checks passed on the exact implementation head before PR #335 was squash-merged.

No BattlEye internal checks, packed implementation, anti-debug/detection behavior, network protocol, patching, disabling, spoofing, stealth or evasion mechanisms were inspected or derived.
