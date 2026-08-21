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
execution_mode: trusted_main_issue_comment_self_hosted_read_only
execution_reason: implementation #636 is merged; prior push and pull_request_target transports produced no physical verdict, so use one owner-only exact-comment event on fixed PR #641 with workflow and checkout sourced only from trusted main
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
base_main: e3c5b5583985c38005530bf20eb0094a77f01267
branch: fix/OTC-20260820-surveyor-auth-session-comment-trigger
implementation_pr: 636
implementation_merge_sha: 16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3
acceptance_workflow_pr: 637
acceptance_workflow_merge_sha: ea796e7037f1ca92164b069b6b55ceb20e94190a
reporting_workflow_pr: 638
reporting_workflow_merge_sha: 3caf2d46d29f506b3b6d1fca5706892be098c19d
observable_workflow_pr: 639
observable_workflow_merge_sha: 5707af6c413cd9949f6c33b17744801cedef6eaf
pr_target_workflow_pr: 640
pr_target_workflow_merge_sha: e3c5b5583985c38005530bf20eb0094a77f01267
physical_trigger_pr: 641
physical_trigger_sha: 579249c982fefeaeaa614c871eda34c8b8eb8331
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-21T13:43:00+02:00
next_action: validate and merge the owner-only issue_comment transport, post exact marker ONE_SHOT_SURVEYOR_AUTH_READ_ONLY to PR #641, inspect exact run and accept only explicit physical PASS
---

# Surveyor v2 next gap — auth/session typed reader

## Selected gap and implementation

Fresh pre-implementation repository-only and admitted physical Surveyor `--collect-all` both produced 169 canonical rows, 12 alias views, 10 missing typed readers and privacy PASS. `auth_session_typed_reader` ranked first at score 125; `world_minimap_typed_reader` tied but overlapped active #475/#593.

PR #636 merged the exact-current-build fail-closed reader as `16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3`. It exact-fences the official client and Qt StateMachine library, validates `TGameClient + 0x8d0 -> TAuthenticationProcessController`, and exposes only the `QStateMachine::isRunning()`-equivalent lifecycle boolean. It emits `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, `credentials_retained=false`, `session_secrets_retained=false`, `semantic_promotion_allowed=false`, and uses read-only process-memory access.

Exact implementation head `18bee436f57915bf61d59f0d068448a5b91e6ab1` passed 40/40 focused Surveyor tests, repository-only collect-all 169 / 12 / 9 with privacy PASS, CI `32452573404`, Track A agent governance `32452573189`, Track A canonical-live governance `32452573109`, and fresh audit with 0 material findings. Static/current-build evidence: `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/current-build-auth-lifecycle.md`.

## Physical acceptance transport history

PRs #637, #638 and #639 successively installed and hardened a trusted-main push one-shot; all exact heads passed CI/governance/audit, but connector-driven main merges produced no retrievable authority or final verdict. No physical result was inferred from silence.

PR #640 (`e3c5b5583985c38005530bf20eb0094a77f01267`) replaced push transport with a narrowly pinned `pull_request_target` design. Exact head `79c2d80d609894ff78f42bfe162770ffed135c14` passed CI `32478067020`, Track A governance `32478066838`, yamllint/actionlint and fresh audit with 0 material findings. Trigger PR #641 was opened at exact SHA `579249c982fefeaeaa614c871eda34c8b8eb8331`, but no workflow job or fail-report was produced; therefore `physical_e2e_result` remains `NOT_RUN`.

The current transport repair changes only the event source to `issue_comment`. After merge to `main`, exactly one comment body `ONE_SHOT_SURVEYOR_AUTH_READ_ONLY` on PR #641 by actor `blakinio` is admitted. Workflow source and `${{ github.sha }}` checkout both remain trusted default-branch `main`; PR head code is never executed. The self-hosted physical job has only `contents: read`; only GitHub-hosted authority/report jobs have issue-write permission.

## Physical acceptance contract

Before `/proc/PID/mem` is opened, the physical job must freshly prove no active canonical lease, exactly one client in `otclient-track-a-kasmvnc`, exact size/SHA fence, process start ticks and executable path, display `:1`, exactly one visible Tibia window owned by that PID, canonical registration identity consistency when present, and implementation ancestry.

Only then may merged passive Surveyor `--collect-all` run. PASS requires 169 canonical rows, 12 aliases, auth reader `AVAILABLE`, `process_memory_access=read_only`, semantic state `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, no credential/session-secret retention, 9 missing readers and privacy PASS.

The causal discriminator is implementation availability: `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`, missing readers `10 -> 9`, privacy `PASS -> PASS`. The lifecycle boolean need not change and is not an `IN_GAME` discriminator.

## Hard boundary and closeout

No login/logout/relogin, credential access, GUI/gameplay input, process control, attach/debug/injection, process-memory write, client/container restart, target-network mutation, item/economic action or local-model execution is authorized. `BRIDGE_3_OF_3` remains structural presence only.

After explicit physical PASS: record durable evidence, close PR #641 unmerged, remove the temporary workflow, archive this task with runtime access reset to none, merge final closeout, and verify current `main` plus the remaining Surveyor gap count.
