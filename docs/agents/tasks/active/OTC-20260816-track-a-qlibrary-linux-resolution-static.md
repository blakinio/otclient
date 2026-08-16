---
task_id: OTC-20260816-track-a-qlibrary-linux-resolution-static
status: investigating
agent: ChatGPT
session_id: chatgpt-qlibrary-linux-resolution-static-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260816-track-a-qlibrary-linux-resolution-static
base_branch: main
base_main: 250d48849ac6cce3214ca9d25e7b1abb3450ada6
risk: low
updated: 2026-08-16T12:54:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qlibrary-linux-resolution-static.md
  - .github/workflows/tibia-official-client-re-qlibrary-linux-resolution-static.yml
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
  - docs/agents/reports/OTCLIENT-20260816-beclient-static-integration.md
  - retained exact-client package from run 31904939696 as static file input only
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: GitHub Actions on synology-otclient-01 can statically inventory the retained exact package and linked Qt library without target execution
run_scope: single_task
continuation_policy: continue_within_owner_request
task_completion_policy: checkpoint_and_continue
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded downstream platform-resolution question from proven extensionless QLibrary input to Linux candidate filenames
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
next_action: identify the exact QtCore library/version linked by the retained official client and statically recover its Unix QLibrary candidate-name expansion for an extensionless absolute path ending in BattlEye/BEClient
---

# Objective

Continue downstream from the PROVEN client-generated QLibrary input formula:

```text
J([J([QCoreApplication::applicationDirPath(), "BattlEye"]), "BEClient"])
```

and determine, from the exact retained Linux package / exact linked Qt implementation where possible, how `QLibrary::load()` expands an extensionless path ending in `BattlEye/BEClient` into candidate native library filenames.

# Acceptance

1. Revalidate exact client size/SHA before every semantic run.
2. Statically identify client ELF `DT_NEEDED`, `RPATH/RUNPATH`, and the exact QtCore library file used/provided by the retained package if determinable without execution.
3. Fence the exact QtCore file by path, size and SHA-256 before semantic analysis.
4. Recover exact Qt version from static ELF/version/string/package metadata where directly available.
5. Locate `QLibrary` / `QLibraryPrivate` Unix load implementation in the exact QtCore binary or, if stripped beyond direct recovery, correlate the exact Qt version with official Qt source only and classify that layer distinctly from binary-proven facts.
6. Determine candidate prefix/suffix expansion for an extensionless absolute/path-containing input, especially whether `.../BattlEye/BEClient.so` is directly generated/attempted by the exact Qt implementation.
7. Preserve distinctions between:
   - client-generated input string;
   - Qt candidate filenames;
   - actual successfully mapped file;
   - unique retained package `Init` exporter.
8. Do not execute the client/Qt/BattlEye target, call `dlopen`, inspect live processes, or broaden into BattlEye internals/anti-cheat logic.
9. Remove temporary workflow before terminal closeout.

# Safety

Static retained-file analysis only (`runtime_access: none`). No Tibia/BattlEye/Qt target execution or loading, no live `/proc`, process memory/maps, attach/debug/injection, network/session mutation, binary patching, unpacking, anti-debug/detection research or bypass/evasion work.

# E2E

`NOT_APPLICABLE`: static evidence reconstruction only.
