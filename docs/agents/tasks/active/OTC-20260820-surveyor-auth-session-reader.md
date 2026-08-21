---
task_id: OTC-20260820-surveyor-auth-session-reader
status: implementing
phase: validate
agent: ChatGPT
project_lane: otclient
lane: P0-AUTH
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
execution_mode: trusted_main_self_hosted_read_only
execution_reason: implementation #636 is merged; complete a separately reviewed trusted-main passive acceptance with GitHub-hosted authority/report jobs and a self-hosted physical read-only job
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded read-only physical acceptance followed by evidence/archive cleanup
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: canonical-live-runtime
canonical_registration: UNKNOWN
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
base_main: 3caf2d46d29f506b3b6d1fca5706892be098c19d
branch: fix/OTC-20260820-surveyor-auth-session-observable-e2e
implementation_pr: 636
implementation_merge_sha: 16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3
acceptance_workflow_pr: 637
acceptance_workflow_merge_sha: ea796e7037f1ca92164b069b6b55ceb20e94190a
reporting_workflow_pr: 638
reporting_workflow_merge_sha: 3caf2d46d29f506b3b6d1fca5706892be098c19d
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-21T08:30:00+02:00
next_action: validate and merge the observable one-shot revision with ONE_SHOT_SURVEYOR_AUTH_READ_ONLY; retrieve its run_id from the GitHub-hosted authority comment, inspect the physical job directly, then accept only the final sanitized PASS report
---

# Surveyor v2 next gap — auth/session typed reader

## Selected gap and baseline

Fresh pre-implementation repository-only and admitted physical Surveyor `--collect-all` both produced 169 canonical rows, 12 alias views, 10 missing typed readers and privacy PASS. `auth_session_typed_reader` ranked first at score 125. `world_minimap_typed_reader` tied at 125 but overlapped active #475/#593, so auth/session was selected.

Historical pre-implementation physical target evidence: one exact current client in `otclient-track-a-kasmvnc`, display `:1`, PID `19590`, start ticks `76611792`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, one matching visible Tibia window, released lease generation `19`, matching canonical registration generation `2` / lease generation `19`, registration semantic state `UNKNOWN`. These PID/start/control values remain historical before-evidence only.

## Implementation complete

PR #636 merged to `main` as `16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3`.

The merged reader exact-fences the official client and deployed Qt StateMachine library, resolves singleton `TGameClient`, validates `TGameClient + 0x8d0 -> TAuthenticationProcessController`, and exposes only the exact `QStateMachine::isRunning()`-equivalent lifecycle boolean. It emits `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, `credentials_retained=false`, `session_secrets_retained=false`, and `semantic_promotion_allowed=false`.

Exact implementation head `18bee436f57915bf61d59f0d068448a5b91e6ab1` passed 40/40 focused Surveyor tests, repository-only collect-all 169 / 12 / 9 with privacy PASS, CI `32452573404`, Track A agent runtime governance `32452573189`, Track A canonical live governance `32452573109`, and fresh exact-head validator audit with 0 material findings.

Durable current-build evidence: `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/current-build-auth-lifecycle.md`.

## Acceptance workflow history

PR #637 installed the first trusted-main one-shot and merged as `ea796e7037f1ca92164b069b6b55ceb20e94190a`. Its exact head passed CI `32453287954`, Track A agent runtime governance `32453287783`, actionlint/yamllint and a fresh validator audit. That audit repaired two defects before merge: wrong implementation-SHA labeling and insufficiently strict `pgrep`/active-lease handling.

PR #638 added sanitized PASS/FAIL reporting and merged as `3caf2d46d29f506b3b6d1fca5706892be098c19d`. Exact head `d316b6c2484ff73e104bf9d15c96cca9615642be` passed CI `32453919718`, Track A agent runtime governance `32453919720`, actionlint/yamllint and fresh validator audit with 0 material findings.

The available GitHub connector cannot enumerate push-event workflow runs. No physical result from #637/#638 is assumed or guessed in the absence of a generated verdict comment.

## Observable trusted-main one-shot

The current revision splits one workflow run into three jobs:

1. GitHub-hosted `authority` validates the protected-main marker and exact owner-authored push identity, then immediately publishes the run ID to PR #637. This is explicitly not PASS evidence.
2. Self-hosted `acceptance` on `[otclient, synology]` has only `contents: read`; it performs the previously audited fail-closed target preflight and passive Surveyor collection. No GitHub write token is passed into the physical job. It exposes only a sanitized one-line JSON job output after all physical assertions succeed.
3. GitHub-hosted `report` runs with `always()`, has the only final `issues: write` permission, and posts either the sanitized PASS details or an explicit generic FAIL. This removes ambiguity from queued/failed/skipped physical execution and allows the run to be inspected by exact `run_id` through the connector.

## Physical acceptance contract

Before `/proc/PID/mem` is opened, the physical job must freshly prove:

- no fresh active canonical lease (`runtime_owner_task=NOT_APPLICABLE`);
- exactly one `client` in `otclient-track-a-kasmvnc`;
- exact current size/SHA;
- fresh process start ticks;
- display `:1` connectivity;
- exactly one visible Tibia window owned by that PID;
- canonical registration identity consistency when registration exists;
- implementation merge ancestry.

Only then may it run merged passive Surveyor `--collect-all`. PASS requires canonical rows `169`, aliases `12`, `auth_session_typed_reader=AVAILABLE`, `process_memory_access=read_only`, `semantic_state=TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, credentials/session secrets retained false, missing readers `9`, and privacy PASS.

The exact causal delta is implementation-only: `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`, missing readers `10 -> 9`, privacy `PASS -> PASS`. The lifecycle boolean itself need not change and is not an `IN_GAME` discriminator.

## Hard safety boundary

No login/logout/relogin, user credential access, GUI/gameplay input, process control, attach/debug/injection, process-memory write, client/container restart, target-network mutation, item/economic action or local-model execution is authorized. The runtime reader opens process memory only with `O_RDONLY|O_CLOEXEC`.

`BRIDGE_3_OF_3` remains structural presence only and is never `IN_GAME` proof.

## Remaining closeout

1. exact-head CI/governance/audit for observable revision PASS;
2. merge with exact one-shot marker;
3. retrieve run ID from authority comment and inspect physical job status/logs;
4. require final sanitized PASS;
5. record durable post-merge evidence;
6. delete temporary one-shot workflow;
7. archive this task with runtime access reset to none and merge final closeout.
