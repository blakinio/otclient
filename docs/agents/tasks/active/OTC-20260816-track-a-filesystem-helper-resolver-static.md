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
branch: docs/OTC-20260816-track-a-filesystem-helper-resolver-static
base_branch: main
base_main: 2c56f7f2c7c01d8dbc1b66febeea22b1d4aff6e8
risk: low
updated: 2026-08-16T12:45:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-filesystem-helper-resolver-static.md
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
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
run_scope: single_task
continuation_policy: continue_within_owner_request
task_completion_policy: checkpoint_and_continue
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded client-side filesystem resolver question beneath TTibiaFileSystemHelper's proven BEClient wrapper
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
    purpose: exact base-resolver/slash/caller windows
  - run: 31941716491
    job: 95151777224
    conclusion: success
    purpose: Qt append/toNativeSeparators symbol mapping
  - run: 31941768535
    job: 95151899494
    conclusion: success
    purpose: TTibia +0x28 and outer two-QString construction
  - run: 31941829706
    job: 95152041120
    conclusion: success
    purpose: +0x10/+0x18 category switch and category forwarding
  - run: 31941909566
    job: 95152225148
    conclusion: success
    purpose: exact category-9 jump-table cases
  - run: 31942173414
    job: 95152833368
    conclusion: success
    purpose: exact BattlEye global/literal initializer boundary
  - run: 31942213755
    job: 95152924982
    conclusion: success
    purpose: initializer helper -> strlen + QString::fromUtf8
  - run: 31942437204
    job: 95153445603
    conclusion: success
    purpose: final deterministic BEClient path-formula validator
report: docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
audit:
  result: PASS
  basis: deterministic final validator plus explicit symbolic/path-equivalent/runtime boundaries
  material_findings_open: 0
e2e: NOT_APPLICABLE
e2e_reason: static evidence reconstruction only; no executable/runtime behavior changed
temporary_workflow_removed: false
last_completed_step: final deterministic path-formula validator passed and durable report written
next_action: remove temporary workflow, audit retained diff, exact-head CI/merge/archive, then continue with QLibrary native-Linux extension/platform resolution
---

# Final result

## PROVEN

The exact client-side `shared::TFileSystemHelper::vtable+0x78 -> 0xcfa5e0` resolver implements:

```text
J(components):
  for each QString component:
    append("/")
    append(component)
  return QDir::toNativeSeparators(accumulator)
```

For the BattlEye loader wrapper:

```text
TTibiaFileSystemHelper +0xd8
  -> key "BEClient"
  -> category 9
  -> +0x30
  -> +0x28(category 9)
       -> +0x18(9) = QCoreApplication::applicationDirPath()
       -> +0x10(9) = QString("BattlEye")
       -> J([applicationDirPath(), "BattlEye"])
  -> J([previous result, "BEClient"])
  -> previously proven QLibrary::setFileName input
```

Authoritative symbolic formula:

```text
J([J([QCoreApplication::applicationDirPath(), "BattlEye"]), "BEClient"])
```

Stable path-equivalent relative suffix:

```text
BattlEye/BEClient
```

The client-side formula contains no `.so` extension.

Final deterministic validator: `31942437204 / 95153445603`, success.

## DYNAMIC / UNKNOWN downstream boundary

The actual application-directory prefix is runtime-derived. Exact platform-specific QLibrary candidate expansion/mapped file remains a separate downstream layer; this task does not silently promote `BEClient.so` as the exact client-generated string.

## Corrections

- raw global xref census for the `BattlEye` initializer is rejected as semantic evidence; only exact adjacent initializer instructions are retained;
- raw file reads of runtime-initialized QString global `0x31964a0` are invalid; the value is instead proved through its static initializer;
- one diagnostic `objdump` attempt failed because the runner lacks `objdump`; no evidence depends on that run.

# Audit

PASS. The report promotes the QLibrary input from wholly UNKNOWN to a PROVEN symbolic/dynamic formula while preserving runtime prefix and downstream QLibrary file-resolution boundaries.

# Safety

Static exact retained-file client analysis only (`runtime_access: none`). No Tibia/BattlEye execution/loading, live process observation, process memory/maps, attach/debug/injection, input/network/session mutation, binary patching, unpacking, anti-debug/detection analysis, protocol inspection or bypass/evasion work.

# E2E

`NOT_APPLICABLE`: no executable/runtime behavior changed.
