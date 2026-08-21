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
execution_reason: implementation #636 is merged; complete a separately reviewed trusted-main passive acceptance and publish only a sanitized verdict for durable agent retrieval
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
base_main: ea796e7037f1ca92164b069b6b55ceb20e94190a
branch: fix/OTC-20260820-surveyor-auth-session-report-e2e
implementation_pr: 636
implementation_merge_sha: 16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3
acceptance_workflow_pr: 637
acceptance_workflow_merge_sha: ea796e7037f1ca92164b069b6b55ceb20e94190a
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-21T08:18:00+02:00
next_action: validate and merge the reporting revision with ONE_SHOT_SURVEYOR_AUTH_READ_ONLY; accept physical E2E only from its sanitized PASS report on PR #637, then remove the temporary workflow and archive this task
---

# Surveyor v2 next gap — auth/session typed reader

## Selected gap and baseline

Fresh pre-implementation repository-only and admitted physical Surveyor `--collect-all` both produced 169 canonical rows, 12 alias views, 10 missing typed readers and privacy PASS. `auth_session_typed_reader` ranked first at score 125. `world_minimap_typed_reader` tied at 125 but overlapped active #475/#593, so auth/session was selected.

Historical pre-implementation physical target evidence: one exact current client in `otclient-track-a-kasmvnc`, display `:1`, PID `19590`, start ticks `76611792`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, one matching visible Tibia window, released lease generation `19`, matching canonical registration generation `2` / lease generation `19`, registration semantic state `UNKNOWN`. PID/start/control values are historical before-evidence only and are never reused as current admission.

## Implementation complete

PR #636 merged to `main` as `16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3`.

The reader exact-fences the official client and deployed Qt StateMachine library, resolves the singleton `TGameClient`, validates `TGameClient + 0x8d0 -> TAuthenticationProcessController`, and exposes only the exact `QStateMachine::isRunning()`-equivalent lifecycle boolean. It emits `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, `credentials_retained=false`, `session_secrets_retained=false`, and `semantic_promotion_allowed=false`.

Exact implementation head `18bee436f57915bf61d59f0d068448a5b91e6ab1` passed 40/40 focused Surveyor tests, repository-only collect-all 169 / 12 / 9 with privacy PASS, CI `32452573404`, Track A agent runtime governance `32452573189`, Track A canonical live governance `32452573109`, and fresh exact-head validator audit with 0 material findings.

Durable static/current-build evidence: `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/current-build-auth-lifecycle.md`.

## Trusted-main acceptance workflow

PR #637 merged to trusted `main` as `ea796e7037f1ca92164b069b6b55ceb20e94190a` with marker `ONE_SHOT_SURVEYOR_AUTH_READ_ONLY`. Its exact head passed CI `32453287954`, Track A agent runtime governance `32453287783`, actionlint/yamllint, and a fresh validator audit. The audit found and repaired two pre-merge defects: wrong implementation-SHA labeling and insufficiently strict `pgrep`/active-lease handling.

The connector available to the agent cannot enumerate `push`-event workflow runs, so a physical verdict from that first trusted-main trigger is not assumed or guessed. It is not used as acceptance evidence unless independently retrieved.

The current reporting revision keeps the same runtime operation and adds only:

- exact assertion of 169 coverage rows;
- canonical lease/registration generation/state fields in the sanitized acceptance object;
- repository-side reporting to merged PR #637 using the built-in GitHub token with `issues: write` after and only after all physical assertions and artifact upload succeed.

The reported comment contains only sanitized non-secret facts and the GitHub `run_id`; no raw window title, process environment, credential, session secret or packet payload is included.

## Physical acceptance contract

Before `/proc/PID/mem` is opened, trusted-main workflow must freshly prove:

- no fresh active canonical lease (therefore `runtime_owner_task=NOT_APPLICABLE`);
- exactly one `client` in `otclient-track-a-kasmvnc`;
- exact current size/SHA;
- fresh process start ticks;
- display `:1` connectivity;
- exactly one visible Tibia window owned by that PID;
- canonical registration identity consistency when registration exists;
- implementation merge ancestry.

Only then may it run merged passive Surveyor `--collect-all`. PASS requires:

- canonical rows `169`;
- aliases `12`;
- `auth_session_typed_reader=AVAILABLE`;
- `process_memory_access=read_only`;
- `semantic_state=TYPED_AUTH_LIFECYCLE_ONLY`;
- `in_game_claimed=false`;
- credentials/session secrets retained false;
- missing readers `9`;
- privacy PASS.

The causal delta is implementation-only: `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`, missing readers `10 -> 9`, privacy `PASS -> PASS`. The lifecycle boolean itself is not required to change and is not an `IN_GAME` discriminator.

## Hard safety boundary

No login/logout/relogin, user credential access, GUI/gameplay input, process control, attach/debug/injection, process-memory write, client/container restart, network mutation, item/economic action or local-model execution is authorized. The runtime reader opens process memory only with `O_RDONLY|O_CLOEXEC`.

`BRIDGE_3_OF_3` remains structural presence only and is never `IN_GAME` proof.

## Remaining closeout

1. exact-head CI/governance/audit for reporting revision PASS;
2. merge reporting revision with the exact one-shot marker;
3. retrieve and verify sanitized physical PASS report from PR #637;
4. record durable post-merge evidence;
5. delete temporary one-shot workflow;
6. archive this task with runtime access reset to none and merge final closeout.
