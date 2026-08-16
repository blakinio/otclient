---
task_id: OTC-20260816-track-a-battleye-readonly
status: completed
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
related_pr: 326
updated: 2026-08-16T09:00:45+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-battleye-readonly.md
modules_touched: []
reuses:
  - synology-otclient-01
  - /home/runner/_work/_otclient_tibia_re_state
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
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: synology-otclient-01:host-readonly-package-and-proc-name-index
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
validation_run: 31932798483
validation_job: 95130062729
validation_conclusion: success
e2e: NOT_APPLICABLE_READ_ONLY_DIAGNOSTIC
mutation_performed: false
next_action: none
---

# Objective

Determine directly on `synology-otclient-01` whether the installed exact official native Linux Tibia client contains BattlEye-named files/directories or literal BattlEye/BEClient/BEService references, and whether a BattlEye-named process is presently visible.

# Result — direct runtime evidence

GitHub Actions run `31932798483`, job `95130062729`, completed `success` on runner `synology-otclient-01`.

The historical canonical-home client path was absent in the first diagnostic run `31932757700` / job `95129962611`; this was treated as stale-path evidence only and the workflow was repaired to discover the exact client by size plus SHA rather than assuming that historical location.

The successful read-only discovery found 8 BattlEye-related paths in the retained PR #303 task-owned run `31904939696`, including both copied package trees:

- `.../package/bin/BattlEye/BEClient.so`
- `.../package/bin/BattlEye/BEClient.cfg`
- `.../package/3rdpartylicences/battleye-eula.txt`
- matching copies under `.../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia/`.

Two exact-fence client files were found, both size `51965216` and SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`:

- `.../runs/31904939696/package/bin/client`
- `.../runs/31904939696/home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client`

Literal exact-client token checks returned:

- `BattlEye`: `PRESENT`
- `BEClient`: `PRESENT`
- `BEService`: `ABSENT`

Current process-name inventory returned `BATTLEYE_AUDIT_PROCESS_NAME_HIT_COUNT=0` and exact-fence Tibia process count `0`. This proves only that no matching process was visible during this specific job; it does not claim BattlEye is never started when Tibia runs.

The job emitted `BATTLEYE_AUDIT_MUTATION_PERFORMED=false`. It did not launch/stop Tibia, attach/inject/debug, read credentials, send input, mutate displays/network/session state, alter canonical lease/registration state, or inspect PR #303 process memory/maps.

# Cleanup

The temporary workflow `.github/workflows/tibia-official-client-re-battleye-readonly.yml` was removed from this branch after successful evidence collection. PR #326 is intentionally temporary and must be closed unmerged after this checkpoint; no diagnostic workflow should enter `main`.
