---
task_id: OTC-20260819-track-a-auth-session-current-build-static
status: waiting
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track: official-client-re
task_kind: reverse_engineering_protocol
phase: validate
branch: research/OTC-20260819-track-a-auth-session-current-build-static
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
worktree: github-hosted-ephemeral:research/OTC-20260819-track-a-auth-session-current-build-static
created: 2026-08-19T09:34:30+02:00
updated: 2026-08-19T09:39:27+02:00
risk: medium
execution_mode: github-only
execution_reason: deterministic disposable exact-binary static analysis and repository delivery use GitHub connector plus GitHub-hosted Actions
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
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

This task consumes #498/#499/#528 only as historical hypotheses and leaves #555's current-fence governance paths untouched.

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

1. The exact current public binary still exposes a uniquely recoverable `tibia::client::TGameClient` QMetaObject containing `onRequestLoginWithCredentials(QString,QString)`.
2. Character/world/play-session and character-selection/game-server-login structural families remain discoverable, but historical addresses must not be reused.
3. A current-build static discriminator can either produce new QMeta/dispatch/instruction fences or explicitly leave a target `UNKNOWN` without client execution.

## Acceptance inventory

- [ ] Verify current public packed fingerprint `10214529 / 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354` and unpacked fingerprint `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8` before analysis.
- [ ] Do not upload, commit, or retain the proprietary raw client as an artifact.
- [ ] Recover current-build `TGameClient` QMeta class/method metadata and `onRequestLoginWithCredentials` method identity, or fail closed with bounded diagnostics.
- [ ] Recover its current-build QMeta dispatch target/instruction fence without reusing an old address.
- [ ] Inventory current-build structural strings/QMeta families for character list, world list, play-session, character selection, game-server login and disconnect/reconnect paths.
- [ ] Mark historical #498/#499 addresses `SUPERSEDED_FOR_CURRENT_BUILD_UNLESS_REDISCOVERED`.
- [ ] Persist sanitized evidence; no credential/session values and no raw binary.
- [ ] Exact-head workflow and repository/governance checks pass before researcher closeout.
- [ ] Leave result in Draft PR #556; researcher does not merge or promote canonical coverage.

## Implemented discriminator

`.github/workflows/track-a-auth-session-current-build-static.yml` now runs on `ubuntu-24.04` with `runtime_access:none`. It:

- uses the previously established disposable WARP fetch pattern;
- exact-fences packed and unpacked current public bytes plus expected ELF build-id;
- reconstructs Qt metaobjects from ELF `R_X86_64_RELATIVE` relocation structure rather than historical addresses;
- recovers the `TGameClient` QMeta method table and full-range static-metacall dispatch table;
- inventories targeted auth/session QMeta methods and structural strings;
- emits only sanitized addresses/signatures/counts;
- deletes both packed and unpacked client bytes and has no artifact-upload step.

## CI checkpoint

Research workflow generation for workflow commit `8ce1c7e29c376806c955d775050b151921cd4ff0`:

```text
Draft PR: #556
Track A current-build auth session static discriminator run: 32228689953
job: 95993698970
first state observation: queued
second/final ordinary state observation: in_progress
step 1 Set up job: success
step 2 Fetch exact public client and recover current-build structure: in_progress at final permitted ordinary observation
```

A job-log fetch while the job was still running returned GitHub `404 BlobNotFound`; it produced no evidence and was not retried. Per `ANTI_STALL_AND_EXECUTION_BUDGET.md`, the same exact workflow head is not polled a third time in this invocation.

## Execution budget checkpoint

```yaml
invocation_started_at: 2026-08-19T09:26:00+02:00
last_progress_at: 2026-08-19T09:39:27+02:00
ci_checks_for_current_head: 2
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 1
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-19T09:39:27+02:00
status: waiting
phase: validate
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
branch: research/OTC-20260819-track-a-auth-session-current-build-static
workflow_implementation_head: 8ce1c7e29c376806c955d775050b151921cd4ff0
draft_pr: 556
workflow_run: 32228689953
workflow_job: 95993698970
facts:
  - Alias resolution, ownership and routing are proven from current repository governance.
  - This invocation does not grant credential access, login, character-selection, relogin or second-session authority.
  - PR #555 independently records the candidate current public unpacked identity 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8; trusted main still carries the older canonical runtime fence.
  - PR #528 remains the separate native-login E2E owner and was not modified.
  - A task-owned exact-current-build static discriminator is committed and its first workflow run was accepted by GitHub-hosted Actions.
unknown:
  - Terminal result and logs of run 32228689953 / job 95993698970.
  - Current-build recovered QMeta addresses and cold-auth dispatch target until that result is read.
blocker: ORDINARY_CI_STATE_CHECK_BUDGET_EXHAUSTED_WHILE_STATIC_DISCRIMINATOR_IN_PROGRESS
next_action: Read the terminal result/log of run 32228689953 job 95993698970 once it is complete and persist its sanitized outcome under this task evidence namespace.
```
