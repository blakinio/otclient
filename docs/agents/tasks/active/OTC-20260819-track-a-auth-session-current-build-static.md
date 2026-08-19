---
task_id: OTC-20260819-track-a-auth-session-current-build-static
status: investigating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track: official-client-re
task_kind: reverse_engineering_protocol
phase: investigate
branch: research/OTC-20260819-track-a-auth-session-current-build-static
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
worktree: github-hosted-ephemeral:research/OTC-20260819-track-a-auth-session-current-build-static
created: 2026-08-19T09:34:30+02:00
updated: 2026-08-19T09:34:30+02:00
risk: medium
execution_mode: github-only
execution_reason: deterministic disposable exact-binary static analysis and repository delivery use GitHub connector plus GitHub-hosted Actions
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: terminal_only
context_pressure: medium
decomposition_decision: single
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
promotion_authority: coordinator_only
researcher_delivery: draft_pr_only
owned_paths:
  - .github/workflows/track-a-auth-session-current-build-static.yml
  - docs/agents/evidence/OTC-20260819-track-a-auth-session-current-build-static/**
  - docs/agents/tasks/active/OTC-20260819-track-a-auth-session-current-build-static.md
dependencies:
  - PR #555 current official-client fence advance; read-only dependency, do not edit its paths
  - PR #528 native-login E2E; consume durable evidence only, do not edit or perform login
  - PR #498 historical auth/session static evidence; exact old-build evidence only
  - PR #499 historical game-login credential schema evidence; exact old-build evidence only
---

# TIBIA-RE-AUTH-SESSION — current-build static revalidation

## Objective

Revalidate the authentication/session structural surface against the independently fingerprinted current public official native-Linux Tibia binary (`size=52109920`, `sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`) without inheriting old addresses, credential authority, login authority, or canonical-runtime authority.

This task consumes the durable historical findings from #498/#499/#528 as hypotheses only. It does not modify those PRs and does not overlap PR #555's trusted-base fence/governance update.

## Admission

```yaml
track_id: official-client-re
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
```

No Synology physical runtime, KasmVNC/X11, process memory, input, credentials, Secrets, session values, login, character selection, relogin, gameplay, package mutation, proxy mutation, or canonical lease/registration mutation is authorized or required by this static slice.

## Bounded hypotheses

1. The current exact public binary still exposes a uniquely recoverable `tibia::client::TGameClient` QMetaObject containing `onRequestLoginWithCredentials(QString,QString)`.
2. The current binary still exposes structural character/world/play-session and character-selection/game-server-login families, but historical addresses are not assumed.
3. A current-build static discriminator can produce new addresses/signatures/fences or explicitly classify each target `UNKNOWN` without executing the client.

## Acceptance inventory

- [ ] Fetch the current public Linux `client.lzma` through the already-used disposable WARP path on `ubuntu-24.04` and verify packed/unpacked size/SHA before analysis.
- [ ] Do not upload, commit, or retain the proprietary raw client as an artifact.
- [ ] Recover `TGameClient` QMeta class/method metadata and cold-auth method identity on the current exact binary, or fail closed with bounded diagnostics.
- [ ] Recover a current-build QMeta dispatch target/instruction fence for `onRequestLoginWithCredentials` without reusing the old target address.
- [ ] Inventory current-build structural strings/QMeta families for character list, world list, play-session, character selection, game-server login, reconnect/disconnect paths.
- [ ] Preserve historical #498/#499 addresses as `SUPERSEDED_FOR_CURRENT_BUILD` unless independently rediscovered on the current SHA.
- [ ] Persist sanitized evidence under the task namespace; no credential/session values and no raw binary.
- [ ] Exact-head workflow and repository/governance checks pass before researcher closeout.
- [ ] Leave the result in a Draft PR for coordinator promotion; researcher does not merge or update canonical coverage.

## Non-overlap

- PR #555 owns trusted-base current-fence enforcement/governance. This task may cite its proven package fingerprint but does not change its paths.
- PR #528 owns physical native-login/current-package lifecycle work. This task performs no login, package mutation, Secrets use, physical runtime action, or changes to #528.
- PR #536 owns the shared full-client coverage matrix/checklist. This task does not edit shared canonical coverage.

## Execution budget checkpoint

```yaml
invocation_started_at: 2026-08-19T09:26:00+02:00
last_progress_at: 2026-08-19T09:34:30+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-19T09:34:30+02:00
status: investigating
phase: investigate
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
branch: research/OTC-20260819-track-a-auth-session-current-build-static
head: pending-claim-commit
proven:
  - The short alias resolves from docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md.
  - The alias forbids credentials/new login/character selection/relogin unless separately authorized; this invocation grants none of those effects.
  - PR #555 independently records current public unpacked binary size 52109920 and SHA256 ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8 while trusted main still carries the older runtime fence.
  - PR #528 remains the separate native-login E2E owner.
unknown:
  - Current-build QMeta metadata addresses and cold-auth dispatch target.
  - Current-build character/world/play-session and game-server-login structural addresses.
blockers:
  - none for static current-build research
next_action: Add the task-owned GitHub-hosted exact-current-build static discriminator, open a Draft PR, and execute it without retaining the raw client.
```
