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
phase: loader-and-support-state-differential
branch: research/OTC-20260815-track-a-runtime-loader-diagnostic
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-loader-diagnostic
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 307
updated: 2026-08-15T18:02:00+02:00
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
loader_evidence_run: 31893811826
loader_evidence_job: 95033921299
qt_plugin_evidence_run: 31893939190
qt_plugin_evidence_job: 95034223662
support_state_run: 31894272272
support_state_job: 95035023704
---

# Objective

Provide a read-only differential for PR #303's `client_gen_1_window_missing` failure without launching the official client or reading account/session data.

# Exact fence

`15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, native Linux, `synology-otclient-01`.

# Result

- **Base loader FACT:** run `31893811826` / job `95033921299` — current #303 loader resolves completely (`RC=0`) with client-bundled Qt and toolroot libproxy/EGL/GLX/X11. Reverting to the historical literal loader path is disproven on today's toolroot.
- **Qt platform FACT:** run `31893939190` / job `95034223662` — `qt.conf`, `libqxcb.so` and `libqxcb-glx-integration.so` are present; both plugin dependency chains resolve `RC=0`. Missing qxcb/GLX plugin bytes/dependencies are disproven.
- **Support-state FACT:** metadata-only run `31894272272` / job `95035023704` — canonical HOME has no `.config`, but has `.cache/CipSoft GmbH` containing 4 files / 6937 aggregate bytes. No cache contents were read or copied. This is the first concrete persistent-HOME support-state difference not reproduced by #303's fresh HOME, but its purpose/sensitivity remains UNKNOWN.

Durable evidence:
- `docs/agents/evidence/OTC-20260815-track-a-loader-diagnostic/20260815-loader-differential.md`
- `docs/agents/evidence/OTC-20260815-track-a-loader-diagnostic/20260815-support-state-metadata.md`

# Acceptance

- [x] exact client fence verified;
- [x] base ELF/search-path chain classified;
- [x] qxcb/GLX plugin chain classified;
- [x] canonical HOME support-state metadata classified without reading values;
- [x] no client launch, credentials, process/display/port mutation or cache payload read;
- [x] loader/plugin findings handed to PR #303;
- [ ] final exact-head CI for this final checkpoint.

# Next action

PR #303 should first capture sanitized runtime `QT_DEBUG_PLUGINS=1` plus all mapped/unmapped X11 windows/extensions. Treat `.cache/CipSoft GmbH` only as a bounded candidate and do not copy/read its payloads unless a separate fail-closed sensitivity classification is authorized and runtime evidence makes it causal.
