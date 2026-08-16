---
task_id: OTC-20260816-track-a-qlibrary-linux-resolution-hosted
status: investigating
agent: ChatGPT
session_id: chatgpt-qlibrary-linux-resolution-hosted-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260816-track-a-qlibrary-linux-resolution-hosted
base_branch: main
base_main: 250d48849ac6cce3214ca9d25e7b1abb3450ada6
risk: low
updated: 2026-08-16T12:57:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qlibrary-linux-resolution-hosted.md
  - .github/workflows/tibia-official-client-re-qlibrary-linux-resolution-hosted.yml
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
  - closed coordinator-stopped evidence PR #354
  - historical retained-package inventory run 31942882982 / job 95154489699 only
  - official public Qt 6.9.3 qtbase source
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: github_hosted
runtime_access: none
persistent_session: none
physical_e2e: false
run_scope: single_task
continuation_policy: continue_within_owner_request
task_completion_policy: checkpoint_and_continue
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded official-source-correlated Qt 6.9.3 QLibrary candidate-name expansion question with no proprietary artifact access
validation_level: focused
track_a_runtime_agent_admission_version: 1
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
historical_exact_qtcore_inventory:
  source_run: 31942882982
  source_job: 95154489699
  execution_class: historical_synology_inventory_only_no_repeat
  client_needed: libQt6Core.so.6
  client_runpath: $ORIGIN/lib
  retained_path: bin/lib/libQt6Core.so.6
  size: 8789520
  sha256: 03ac3e4eb8730c2f6cbe6e3db9eb06c03477846eb3ac46ca2ebf19423270ffc5
  soname: libQt6Core.so.6
  static_version_string_set: [6.9.3]
  qVersion_symbol: 0xf62a0
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
next_action: use GitHub-hosted execution and official qt/qtbase v6.9.3 source to deterministically recover Unix QLibrary candidate expansion for an absolute extensionless path ending in BattlEye/BEClient, keeping source-correlated behavior separate from exact-binary inventory and actual runtime mapping
---

# Objective

Continue downstream from the exact-client PROVEN input formula ending in `BattlEye/BEClient` without any further Synology/proprietary semantic probing.

The historical inventory from the coordinator-stopped PR #354 is retained only as a static identity fence:

```text
client DT_NEEDED: libQt6Core.so.6
client RUNPATH: $ORIGIN/lib
retained QtCore: bin/lib/libQt6Core.so.6
size: 8789520
sha256: 03ac3e4eb8730c2f6cbe6e3db9eb06c03477846eb3ac46ca2ebf19423270ffc5
SONAME: libQt6Core.so.6
static exact version string: 6.9.3
qVersion symbol: 0xf62a0
```

All further semantic QLibrary resolution must be performed against the **official public Qt 6.9.3 source** using `github_hosted` execution only.

# Acceptance

1. Do not access the retained package, Synology runner, live runtime or proprietary client in semantic runs.
2. Fetch only official `qt/qtbase` source at exact tag `v6.9.3` from public GitHub.
3. Deterministically validate the Unix `QLibraryPrivate::suffixes_sys`, `prefix_sys`, absolute-path ordering, x86/glibc-hwcaps transformation, candidate construction and `dlopen` loop.
4. Derive the candidate sequence for symbolic absolute input `<APPDIR>/BattlEye/BEClient` for both runtime CPU branches relevant to x86 Linux:
   - `ArchHaswell` false;
   - `ArchHaswell` true under glibc.
5. Prove whether `<APPDIR>/BattlEye/BEClient.so` is generated as a candidate and establish its order relative to exact extensionless and `libBEClient*` candidates.
6. Distinguish:
   - exact-client generated input (PROVEN from predecessor report);
   - exact retained QtCore identity/version (historical exact-binary inventory);
   - official-source-correlated Qt 6.9.3 candidate behavior;
   - actual successful runtime `dlopen` mapping (UNKNOWN without runtime evidence).
7. No BattlEye internals, anti-cheat behavior, bypass/evasion, unpacking, patching, live process or network work.
8. Remove temporary hosted workflow before terminal merge.

# Safety

Public-source semantic analysis only. `runtime_access: none`, `persistent_session: none`, `physical_e2e: false`. No proprietary artifact access in hosted validation.

# E2E

`NOT_APPLICABLE`: documentation/static source-correlation only.
