---
task_id: OTC-20260813-tibia-global-login-lab
status: implementing
agent: ChatGPT
project_lane: otclient
lane: otclient
track: legacy-analysis
task_kind: infrastructure
phase: bootstrap
branch: feat/OTC-20260813-tibia-global-login-lab
base_branch: main
created: 2026-08-13T09:10:00+02:00
updated: 2026-08-13T09:10:00+02:00
risk: medium
related_pr: pending
owned_paths:
  - tools/tibia-global-login-lab/**
  - .github/workflows/tibia-global-login-lab.yml
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
modules_touched:
  - legacy-analysis
  - github-actions
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - PR #48 runtime evidence and runner labels as read-only input
  - synology-otclient-01 self-hosted runner
cross_repo_tasks: []
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
---

# Goal

Create an isolated repository-owned runtime lab for investigating whether the legacy OTClient can authenticate to and enter the official Tibia game service, with execution pinned to the dedicated `synology-otclient-01` self-hosted runner.

# Safety and isolation

- Writes are confined to `blakinio/otclient` and this task branch.
- The lab owns a separate persistent runner workspace and Docker container namespace.
- It must not mutate `oteryn-staging` services or reuse their writable state.
- It must not commit proprietary Tibia binaries/assets, credentials, cookies, session keys, private captures, screenshots containing secrets, or generated account data.
- Owner-funded Codex/API/token quota is forbidden unless the owner explicitly authorizes that specific use.
- Existing test-account secrets from PR #48 remain restricted to their already-authorized runtime path until a separate explicit migration is recorded.
- No OCR/Tesseract is part of the login proof path.

# Acceptance inventory

- [ ] Dedicated project root exists under `tools/tibia-global-login-lab/`.
- [ ] Dedicated workflow exists and targets `[self-hosted, otclient, synology]` only.
- [ ] Bootstrap verifies `RUNNER_NAME=synology-otclient-01`, Docker availability and an isolated persistent state root.
- [ ] Bootstrap creates or refreshes only a lab-owned container with deterministic labels.
- [ ] Runner execution emits non-secret proof markers for workspace/container/image identity.
- [ ] The workflow does not consume login credentials in this bootstrap phase.
- [ ] PR is opened as draft and runner bootstrap is observed on the exact head.
- [ ] Full changed-file inventory is limited to declared owned paths.

# Current evidence

- `main` at task creation: `05450748daca8344d9555638b638e98b6dc3abc7`.
- PR #48 proves the repository can route a job to runner `synology-otclient-01` with labels `otclient` and `synology`.
- PR #48 remains separate operational work and is not mutated by this task.

# Next action

Implement project files and workflow, open the draft PR, then verify the emitted self-hosted bootstrap job on the exact head.
