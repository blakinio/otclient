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
phase: loader-differential
branch: research/OTC-20260815-track-a-runtime-loader-diagnostic
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-loader-diagnostic
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: null
updated: 2026-08-15T17:06:00+02:00
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

This task is read-only with respect to `/home/runner/_work/_otclient_tibia_re_state` and `/work/_otclient_tibia_re_state`. It may inspect exact-client ELF metadata and dependency resolution only. It must not launch the client, use credentials, signal processes, touch displays/ports, write shared runtime state, or interfere with PR #303.

# Acceptance

- [ ] exact client SHA/size verified;
- [ ] exact ELF interpreter and `DT_NEEDED`/`DT_RPATH`/`DT_RUNPATH` recorded;
- [ ] package Qt/library layout recorded without proprietary bytes;
- [ ] dependency resolution compared for historical positive `LD_LIBRARY_PATH=$runtime/lib:$tool_lib` and current #303-style `$runtime/bin/lib:$tool_lib`;
- [ ] material difference classified FACT or exact no-difference recorded;
- [ ] no client launch or secret access;
- [ ] result persisted as bounded evidence and handed to #303/coordinator.

# Next action

Run the read-only exact-build loader differential on `synology-otclient-01` and classify the first material resolution difference, if any.
