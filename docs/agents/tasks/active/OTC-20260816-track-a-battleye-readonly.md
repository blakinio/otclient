---
task_id: OTC-20260816-track-a-battleye-readonly
status: investigating
agent: ChatGPT
session_id: chatgpt-battleye-readonly-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime-research
phase: read-only-package-and-process-inventory
branch: research/OTC-20260816-track-a-battleye-readonly
base_branch: main
base_main: 3a5568f36ebc326afd246d0d2da45b5d8eecabfa
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-battleye-readonly
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: null
updated: 2026-08-16T08:53:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-battleye-readonly.md
  - .github/workflows/tibia-official-client-re-battleye-readonly.yml
modules_touched: []
reuses:
  - synology-otclient-01
  - /home/runner/_work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia
  - exact official Linux client fence 15.32.df7b29
  - GitHub-only temporary workflow pattern
depends_on:
  - current main Track A governance
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
track_a_runtime_agent_admission_version: 1
runtime_access: read_only
runtime_owner_task: OTC-20260816-track-a-battleye-readonly
runtime_namespace: official-client-install-and-host-process-name-inventory
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
next_action: run the dedicated read-only workflow on synology-otclient-01 and inspect exact job logs; never attach, signal, launch, login, send input, read credentials, alter runtime state, or touch PR #303 task-owned namespace
---

# Objective

Determine directly on `synology-otclient-01` whether the installed exact official native Linux Tibia client contains BattlEye-named files/directories or literal BattlEye/BEClient/BEService references, and whether a BattlEye-named process is presently visible.

# Safety boundary

Read-only host/package metadata only. The workflow must not launch or stop Tibia, attach/inject/debug, read login credentials, send input, alter X11/display/network/session state, mutate canonical registration/lease state, or inspect PR #303 process memory/maps. Process observation is limited to `/proc/*/comm` names and exact-client candidate counting/ownership classification; another task's candidate is not inspected further.

# Acceptance

- exact installed client path is resolved and exact size/SHA fence is checked;
- BattlEye/BEClient/BEService filename and directory hits are enumerated as paths only;
- exact client binary is checked for those literal tokens without dumping proprietary binary content;
- process-name inventory reports only matching command names and exact-client candidate ownership class, with no args/environment values printed;
- no mutations occur;
- exact GitHub Actions run/job IDs and findings are recorded before closing the temporary PR.
