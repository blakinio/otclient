---
task_id: OTC-20260816-track-a-filesystem-helper-resolver-static
status: ready
agent: ChatGPT
session_id: chatgpt-filesystem-helper-resolver-static-20260816
session_role: validator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: close
branch: docs/OTC-20260816-track-a-filesystem-helper-resolver-static-refresh
base_branch: main
base_main: 3a3d0fd00d25fa4ea65ea7e6b3ef189a21d753d8
risk: low
updated: 2026-08-16T12:50:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-filesystem-helper-resolver-static.md
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-path-service-rtti-static.md
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-owner-provenance.md
  - closed superseded evidence PR #348
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
decomposition_reason: final documentation replay of completed exact-client resolver research from fresh current main after original PR base became stale
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
  - run: 31941609207
    job: 95151515942
    conclusion: success
    purpose: base-helper RTTI/+0x78 and caller correlation
  - run: 31941660701
    job: 95151640998
    conclusion: success
    purpose: exact base resolver and slash handling
  - run: 31941716491
    job: 95151777224
    conclusion: success
    purpose: Qt append/toNativeSeparators mapping
  - run: 31941768535
    job: 95151899494
    conclusion: success
    purpose: TTibia +0x28 / outer two-QString construction
  - run: 31941829706
    job: 95152041120
    conclusion: success
    purpose: category switch/forwarding
  - run: 31941909566
    job: 95152225148
    conclusion: success
    purpose: category-9 jump-table cases
  - run: 31942173414
    job: 95152833368
    conclusion: success
    purpose: exact BattlEye initializer boundary
  - run: 31942213755
    job: 95152924982
    conclusion: success
    purpose: initializer helper -> strlen/fromUtf8
  - run: 31942437204
    job: 95153445603
    conclusion: success
    purpose: deterministic final path-formula validator
report: docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
audit:
  result: PASS
  basis: deterministic final validator plus explicit symbolic/path-equivalent/runtime/downstream boundaries
  material_findings_open: 0
e2e: NOT_APPLICABLE
e2e_reason: static evidence reconstruction only; no executable/runtime behavior changed
temporary_workflow_removed: true
superseded_pr: 348
last_completed_step: final two-file documentation replayed onto fresh main without re-running semantic probes
next_action: exact-head CI/merge/archive, then continue with QLibrary native-Linux extension/platform resolution
---

# Final result

## PROVEN

The exact client-side formula passed toward `QLibrary::setFileName` is:

```text
J([J([QCoreApplication::applicationDirPath(), "BattlEye"]), "BEClient"])
```

where:

```text
J(components):
  for each QString component:
    append("/")
    append(component)
  return QDir::toNativeSeparators(accumulator)
```

Stable path-equivalent suffix: `BattlEye/BEClient`.

The client resolver does not append `.so`.

Final deterministic validator: `31942437204 / 95153445603`, success.

## DYNAMIC / downstream boundary

The application-directory prefix is runtime-derived. Native-Linux QLibrary expansion for extensionless `BEClient` and the exact file ultimately mapped remain separate downstream questions.

## Corrections

Raw global xref counts, raw bytes of runtime-initialized QString storage, and failed `objdump` diagnostics are not used as load-bearing evidence.

# Audit

PASS. The QLibrary client input is now a PROVEN symbolic/dynamic formula without overclaiming the downstream mapped `.so` file.

# Safety

Static exact retained-file client analysis only (`runtime_access: none`). No Tibia/BattlEye execution/loading, live process observation, process memory/maps, attach/debug/injection, input/network/session mutation, binary patching, unpacking, anti-debug/detection analysis, protocol inspection or bypass/evasion work.

# E2E

`NOT_APPLICABLE`: no executable/runtime behavior changed.
