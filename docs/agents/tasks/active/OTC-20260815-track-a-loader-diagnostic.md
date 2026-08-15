---
task_id: OTC-20260815-track-a-loader-diagnostic
status: investigating
agent: ChatGPT
session_id: chatgpt-loader-diagnostic-20260815-1706
session_role: researcher
project_lane: otclient
lane: RUNTIME-DIAGNOSTIC
track_id: official-client-re
task_kind: runtime-research
phase: loader-and-support-state-differential
branch: research/OTC-20260815-track-a-runtime-loader-diagnostic
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-loader-diagnostic
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 307
updated: 2026-08-15T18:00:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-loader-diagnostic.md
  - docs/agents/evidence/OTC-20260815-track-a-loader-diagnostic/**
  - .github/workflows/tibia-official-client-re-loader-diagnostic.yml
  - .github/workflows/tibia-official-client-re-support-state-diagnostic.yml
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
last_progress_at: 2026-08-15T18:00:00+02:00
loader_evidence_run: 31893811826
loader_evidence_job: 95033921299
qt_plugin_evidence_run: 31893939190
qt_plugin_evidence_job: 95034223662
---

# Objective

Determine, without launching or mutating the official client, whether base dynamic loading, Qt XCB/GLX plugin dependencies, or missing canonical HOME support-state metadata explains PR #303's `client_gen_1_window_missing` failure.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Ownership and safety

This task is read-only with respect to Track A runtime state. It must not launch the client, use credentials, signal processes, touch displays/ports or read account/session values. Support-state inspection is metadata-only: relevant directory names, file counts, aggregate bytes and configuration basenames/sizes only; no file contents or cookies/cache payloads.

# Proven result

## Base ELF loader — FACT

Run `31893811826` / job `95033921299` completed `SUCCESS`: exact client `RUNPATH $ORIGIN/lib`; current #303 loader path resolves completely (`RC=0`) with bundled Qt and toolroot libproxy/EGL/GLX/X11. Historical literal loader replay against today's mutable toolroot fails (`RC=127`). Undoing bundled-Qt/libproxy precedence is DISPROVEN as the next fix.

## Qt platform/plugin chain — FACT

Run `31893939190` / job `95034223662` completed `SUCCESS`: `bin/qt.conf` has `Prefix=.`, `libqxcb.so` and `libqxcb-glx-integration.so` are present, and both dependency chains resolve `RC=0` under the current loader fence. Missing base qxcb/GLX plugin bytes or dependencies are DISPROVEN.

Durable report: `docs/agents/evidence/OTC-20260815-track-a-loader-diagnostic/20260815-loader-differential.md`.

# Acceptance

- [x] exact client SHA/size verified;
- [x] ELF/search-path and Qt plugin dependency chain classified;
- [x] no client launch or secret access;
- [x] loader/plugin results handed to PR #303;
- [ ] metadata-only canonical HOME support-state census completed;
- [ ] any support-state difference classified without reading values;
- [ ] final exact-head repository CI after final checkpoint.

# Next action

Run one metadata-only census of canonical `~/.config`/`~/.cache` application/Qt support state and hand the bounded result to PR #303; do not copy or inspect sensitive values.
