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
updated: 2026-08-15T17:53:00+02:00
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
last_progress_at: 2026-08-15T17:53:00+02:00
loader_evidence_run: 31893811826
loader_evidence_job: 95033921299
qt_plugin_evidence_run: 31893939190
qt_plugin_evidence_job: 95034223662
---

# Objective

Determine, without launching or mutating the official client, whether the exact-build base dynamic-loader or Qt XCB/GLX plugin dependency chain explains PR #303's `client_gen_1_window_missing` failure.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Ownership and safety

This task is read-only with respect to Track A runtime state. Its proving workflows did not launch the official client, use credentials, signal processes, touch displays/ports or mutate shared runtime state.

# Result

## Base ELF loader — FACT

Run `31893811826` / job `95033921299` completed `SUCCESS`:

- interpreter `/lib64/ld-linux-x86-64.so.2`;
- exact client `RUNPATH $ORIGIN/lib`;
- bundled client libraries live under `Tibia/bin/lib`; there is no top-level `Tibia/lib`;
- today's toolroot also contains Qt `6.4.2`, so toolroot Qt must not shadow the exact client's bundled Qt;
- historical-style `LD_LIBRARY_PATH=$runtime/lib:$tool_lib` expressed against today's mutable toolroot fails (`RC=127`, first missing `libpxbackend-1.0.so`);
- current #303 path `$runtime/bin/lib:$toolroot/usr/lib/x86_64-linux-gnu/libproxy:$tool_lib` resolves completely (`RC=0`) with bundled Qt and toolroot EGL/GLX/X11.

Therefore undoing #303's bundled-Qt/libproxy precedence is **DISPROVEN** as the next fix.

## Qt platform/plugin chain — FACT

Run `31893939190` / job `95034223662` completed `SUCCESS`:

- `bin/qt.conf` exists with `[Paths] Prefix=.`;
- `plugins/platforms/libqxcb.so` exists;
- `plugins/xcbglintegrations/libqxcb-glx-integration.so` exists;
- no qxcb EGL integration plugin was found in the bounded package search;
- under #303's current loader fence, `ldd` for both `libqxcb.so` and `libqxcb-glx-integration.so` returns `RC=0`;
- bundled `Qt6XcbQpa/Qt6Gui/Qt6Core` resolve from `bin/lib` and X11/xcb/EGL/GLX/OpenGL support resolves from toolroot with no `not found` dependency.

Therefore missing base qxcb/GLX plugin bytes or unresolved plugin dependencies are **DISPROVEN** as the cause of the current window gate.

Durable base-loader report: `docs/agents/evidence/OTC-20260815-track-a-loader-diagnostic/20260815-loader-differential.md`.

# Acceptance

- [x] exact client SHA/size verified;
- [x] ELF interpreter and dynamic search-path contract recorded;
- [x] package/toolroot Qt and GL layout recorded without proprietary bytes;
- [x] historical-style vs current #303-style loader resolution compared;
- [x] qxcb/GLX plugin presence and dependency resolution checked;
- [x] no client launch or secret access;
- [x] results handed to PR #303 comments `5303004854` and `5303013623`;
- [ ] final exact-head repository CI after this checkpoint.

# Next action

PR #303 should investigate runtime Qt platform/X11 state with sanitized `QT_DEBUG_PLUGINS=1` and an all-window/X11-extension census while preserving current exact-SHA, bundled-Qt/libproxy, WARP, task-owned display and no-secret fences.
