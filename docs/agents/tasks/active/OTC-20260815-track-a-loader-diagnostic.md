---
task_id: OTC-20260815-track-a-loader-diagnostic
status: ready
agent: ChatGPT
session_id: chatgpt-loader-diagnostic-20260815-1706
session_role: researcher
project_lane: otclient
lane: RUNTIME-DIAGNOSTIC
track_id: official-client-re
task_kind: runtime-research
phase: loader-differential
branch: research/OTC-20260815-track-a-runtime-loader-diagnostic
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-loader-diagnostic
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 307
updated: 2026-08-15T17:50:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-loader-diagnostic.md
  - docs/agents/evidence/OTC-20260815-track-a-loader-diagnostic/**
  - .github/workflows/tibia-official-client-re-loader-diagnostic.yml
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - PR #303 runtime reacquisition as consumer only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
last_progress_at: 2026-08-15T17:50:00+02:00
runtime_evidence_run: 31893811826
runtime_evidence_job: 95033921299
runtime_evidence_head: 5e6df5fe39cdc2fdf0240eef8600483f727ec2d5
---

# Objective

Determine, without launching or mutating the official client, whether the exact-build dynamic-loader resolution differs materially between the historically successful Track A client environment and PR #303's current task-local environment.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Ownership and safety

This task is read-only with respect to Track A runtime state. The proving run did not launch the official client, use credentials, signal processes, touch displays/ports or mutate shared runtime state.

# Result

Run `31893811826` / job `95033921299` on exact-client head `5e6df5fe39cdc2fdf0240eef8600483f727ec2d5` completed `SUCCESS` and established:

- ELF interpreter `/lib64/ld-linux-x86-64.so.2`;
- exact client `RUNPATH $ORIGIN/lib`;
- canonical package has no top-level `Tibia/lib`; bundled client libraries are under `Tibia/bin/lib`;
- today's toolroot contains Qt `6.4.2` alongside the exact client's bundled Qt library set;
- the historical-style `LD_LIBRARY_PATH=$runtime/lib:$tool_lib` expressed against today's toolroot fails dependency resolution (`RC=127`) because `libpxbackend-1.0.so` is not on that search path;
- PR #303's current style `LD_LIBRARY_PATH=$runtime/bin/lib:$toolroot/usr/lib/x86_64-linux-gnu/libproxy:$tool_lib` resolves successfully (`RC=0`), selecting bundled client Qt from `bin/lib` and GL/EGL/X11 support from toolroot.

Therefore reverting #303's explicit bundled-Qt/libproxy loader fence is **DISPROVEN as the next fix**. `client_gen_1_window_missing` remains above the base ELF dependency-resolution layer.

Durable report: `docs/agents/evidence/OTC-20260815-track-a-loader-diagnostic/20260815-loader-differential.md`.

# Acceptance

- [x] exact client SHA/size verified;
- [x] exact ELF interpreter and `DT_NEEDED`/`DT_RPATH`/`DT_RUNPATH` recorded;
- [x] package Qt/library layout recorded without proprietary bytes;
- [x] dependency resolution compared for historical-style and current #303-style search paths;
- [x] material difference classified with exact return codes and paths;
- [x] no client launch or secret access;
- [x] result persisted as bounded evidence;
- [ ] final exact-head repository CI after this documentation checkpoint;

# Next action

Hand the bounded negative loader result to PR #303 and coordinator PR #300; investigate Qt platform/plugin/X11 runtime state without undoing bundled Qt precedence.
