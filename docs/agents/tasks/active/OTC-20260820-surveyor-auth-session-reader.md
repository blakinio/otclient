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
execution_mode: trusted_base_pr_target_self_hosted_read_only
execution_reason: implementation #636 is merged; complete one exact-head, same-repository, owner-triggered pull_request_target acceptance whose workflow and checkout both come only from trusted main
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
base_main: 5707af6c413cd9949f6c33b17744801cedef6eaf
branch: fix/OTC-20260820-surveyor-auth-session-pr-target-e2e
implementation_pr: 636
implementation_merge_sha: 16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3
acceptance_workflow_pr: 637
acceptance_workflow_merge_sha: ea796e7037f1ca92164b069b6b55ceb20e94190a
reporting_workflow_pr: 638
reporting_workflow_merge_sha: 3caf2d46d29f506b3b6d1fca5706892be098c19d
observable_workflow_pr: 639
observable_workflow_merge_sha: 5707af6c413cd9949f6c33b17744801cedef6eaf
physical_trigger_branch: test/OTC-20260820-surveyor-auth-session-physical-trigger
physical_trigger_sha: 579249c982fefeaeaa614c871eda34c8b8eb8331
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-21T13:30:00+02:00
next_action: validate and merge the exact-head trusted-base pull_request_target workflow, then open the pre-pinned trigger PR at SHA 579249c982fefeaeaa614c871eda34c8b8eb8331 and accept only a physical PASS
---

# Surveyor v2 next gap — auth/session typed reader

## Selected gap and baseline

Fresh pre-implementation repository-only and admitted physical Surveyor `--collect-all` both produced 169 canonical rows, 12 alias views, 10 missing typed readers and privacy PASS. `auth_session_typed_reader` ranked first at score 125. `world_minimap_typed_reader` tied at 125 but overlapped active #475/#593, so auth/session was selected.

Historical pre-implementation physical target evidence was one exact client in `otclient-track-a-kasmvnc`, display `:1`, PID `19590`, start ticks `76611792`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, one matching visible Tibia window, released lease generation `19`, matching canonical registration generation `2` / lease generation `19`, registration semantic state `UNKNOWN`. PID/start/control values are historical evidence only and are never reused as current admission.

## Implementation complete

PR #636 merged to `main` as `16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3`.

The merged reader exact-fences the official client and deployed Qt StateMachine library, resolves singleton `TGameClient`, validates `TGameClient + 0x8d0 -> TAuthenticationProcessController`, and exposes only the exact `QStateMachine::isRunning()`-equivalent lifecycle boolean. It emits `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, `credentials_retained=false`, `session_secrets_retained=false`, and `semantic_promotion_allowed=false`.

Exact implementation head `18bee436f57915bf61d59f0d068448a5b91e6ab1` passed 40/40 focused Surveyor tests, repository-only collect-all 169 / 12 / 9 with privacy PASS, CI `32452573404`, Track A agent runtime governance `32452573189`, Track A canonical live governance `32452573109`, and fresh exact-head validator audit with 0 material findings.

Durable static/current-build evidence: `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/current-build-auth-lifecycle.md`.

## Acceptance transport repair history

PR #637 merged as `ea796e7037f1ca92164b069b6b55ceb20e94190a`; its exact head passed CI `32453287954`, Track A governance `32453287783`, actionlint/yamllint and fresh validator audit. The audit repaired wrong implementation-SHA labeling and insufficiently strict `pgrep`/active-lease handling before merge.

PR #638 merged as `3caf2d46d29f506b3b6d1fca5706892be098c19d`; exact head passed CI `32453919718`, Track A governance `32453919720`, actionlint/yamllint and fresh audit with 0 material findings.

PR #639 merged as `5707af6c413cd9949f6c33b17744801cedef6eaf`; exact head passed CI `32454886034` and Track A governance `32454885984`, actionlint/yamllint and fresh audit. Its push-trigger design still produced no retrievable authority/final verdict comment. No physical result is inferred from silence.

Because the repository connector reliably creates `pull_request` events but the prior connector-driven main merges did not yield an observable push-run, the current transport repair replaces only the trigger mechanism. It does not weaken runtime admission or semantic assertions.

## Trusted-base `pull_request_target` physical acceptance

The workflow is installed on `main` before the trigger PR is opened. It accepts only the single pre-created same-repository trigger branch `test/OTC-20260820-surveyor-auth-session-physical-trigger` at immutable SHA `579249c982fefeaeaa614c871eda34c8b8eb8331`, base `main`, actor `blakinio`.

Security boundary:

- event is `pull_request_target`, so workflow source is trusted default-branch `main`;
- the self-hosted physical job checks out exact `${{ github.sha }}` from trusted base, never PR head code;
- PR code is never executed;
- self-hosted physical job has only `contents: read` and receives no issue-write token;
- GitHub-hosted authority/report jobs alone may post the run ID and sanitized final verdict;
- any changed trigger SHA, branch, repo, base or actor fails the authority job before physical scheduling.

Before `/proc/PID/mem` is opened, the physical job must freshly prove no fresh active canonical lease, exactly one exact-fenced client, current process start ticks/executable path, display `:1`, exactly one matching visible window, registration identity consistency when registration exists, and implementation ancestry.

Only then may merged passive Surveyor `--collect-all` run. PASS requires 169 canonical rows, 12 aliases, auth reader `AVAILABLE`, `process_memory_access=read_only`, `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, no credential/session-secret retention, 9 missing readers and privacy PASS.

The causal discriminator is implementation availability: auth reader `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`, missing readers `10 -> 9`, privacy `PASS -> PASS`. The lifecycle boolean need not change and is not an `IN_GAME` discriminator.

## Hard safety boundary

No login/logout/relogin, credential access, GUI/gameplay input, process control, attach/debug/injection, process-memory write, client/container restart, target-network mutation, item/economic action or local-model execution is authorized. `BRIDGE_3_OF_3` remains structural presence only and is never `IN_GAME` proof.

## Remaining closeout

1. exact-head CI/governance/actionlint/fresh audit for this transport repair;
2. merge transport repair;
3. open only the pinned trigger PR at SHA `579249c982fefeaeaa614c871eda34c8b8eb8331`;
4. inspect exact run ID, physical job and sanitized PASS/FAIL;
5. on PASS, record durable post-merge evidence;
6. close the trigger PR unmerged, remove the temporary workflow, archive this task with runtime access reset to none, and merge final closeout;
7. verify current `main` and remaining Surveyor gap count.
