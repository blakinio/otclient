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
execution_mode: chat_github_and_hosted_ci
execution_reason: exact-current static resolver and deterministic implementation validation followed by separately re-admitted post-merge physical read-only acceptance
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one typed reader with one exact-build lifecycle resolver and one bounded read-only implementation-causal acceptance path
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
base_main: 73487b0746b898365c759dbfc193e914e619acfb
branch: feat/OTC-20260820-surveyor-auth-session-reader
implementation_pr: 636
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-21T07:36:00+02:00
next_action: finish exact-head focused validation and repository-required independent audit for PR #636, merge only if green, then freshly re-admit the unchanged or newly proven runtime for post-merge passive collect-all acceptance
---

# Surveyor v2 next gap — auth/session typed reader

## Current-main selection evidence

Trusted base at task start: `73487b0746b898365c759dbfc193e914e619acfb`.

Fresh repository-only and admitted physical current-main Surveyor `--collect-all` runs produced:

- canonical rows: 169;
- alias views: 12;
- missing typed readers: 10;
- privacy scan: PASS;
- implemented typed reader: `player_state_typed_reader`;
- rank 1: `auth_session_typed_reader`, canonical priority score 125, 14 unresolved affected rows;
- rank 2: `world_minimap_typed_reader`, canonical priority score 125.

`world_minimap_typed_reader` was not selected because open #475 owns the physical world-map server-delivery frontier and open #593 owns current world-minimap static G1 evidence. `auth_session_typed_reader` is therefore the highest-value current non-overlapping reader gap.

## Pre-implementation physical baseline

The last explicitly admitted pre-implementation observation proved:

- target container `otclient-track-a-kasmvnc`: running;
- control container `otclient-synology-runner`: running;
- display `:1`: connect PASS;
- exact `client` PID: `19590`;
- process start ticks: `76611792`;
- exact client size/SHA: `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`;
- exactly one target process and one matching visible Tibia window;
- canonical lease generation `19`, released, with no active controller;
- canonical registration generation `2`, lease generation `19`, identity matching PID/start/size/SHA/display, semantic state `UNKNOWN`;
- process environment read: false;
- raw window title retained: false.

That admission is retained as historical before-evidence only. Current frontmatter is reset to `runtime_access:none`; any post-merge physical observation requires a fresh admission rather than reuse of stale runtime authority.

## Exact-current implementation evidence

The exact current binary resolves:

- `TGameClient` typeinfo/vptr: `0x30a7778 / 0x30adce8`;
- `TAuthenticationProcessController` typeinfo/vptr: `0x30b4410 / 0x30b5290`;
- current `TGameClient::onGameSessionConnected` implementation reads the controller from `TGameClient + 0x8d0`;
- bounded live type correlation confirmed that member points to the exact auth controller without inspecting credential or play-session payload fields.

The exact deployed `libQt6StateMachine.so.6` is fenced at size `394824`, SHA-256 `26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8`. Its `QStateMachine::isRunning()` reads private pointer offset `0x8`, compares private state offset `0xf0` with value `2`, and returns that boolean. The pre-implementation live controller state was `0`, hence `authentication_state_machine_running=false` under this exact predicate.

Durable detail: `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/current-build-auth-lifecycle.md`.

## Implemented slice

PR #636 now contains:

- `tools/tibia_re_surveyor/auth_session.py` with deterministic exact-build layout resolver and bounded read-only runtime probe;
- exact client and Qt StateMachine fences;
- singleton heap resolution of the exact `TGameClient` primary vptr;
- exact `TGameClient + 0x8d0` auth-controller vptr validation;
- exact Qt `isRunning()`-equivalent lifecycle boolean;
- explicit `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, `semantic_promotion_allowed=false` output;
- collect-all integration registering both auth/session and player-state readers as implemented;
- focused auth/session tests plus updated Surveyor gap expectations: repository-only collect-all is expected to report 9 missing readers after this slice.

## Scope

Owned implementation paths remain limited to:

- `tools/tibia_re_surveyor/**`;
- `tests/tools/tibia_re_surveyor/**`;
- `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/**`;
- this task record and required closeout/catalog/changelog metadata.

Do not modify or take ownership of #475/#593 world-map surfaces, Control Center, Ollama/local models, credentials, login, network mutation, client bytes or process-memory writes.

## Runtime boundary

Any future lease/registration/PID/start/fence/display/window identity change requires fresh read-only admission before observation.

Read-only observation never authorizes login, logout/relogin, input, process control, attach/debug/injection, memory writes, item/economic actions, network mutation or secret-bearing memory access. `mutation_authorized=false` throughout this slice.

`BRIDGE_3_OF_3` remains structural presence only and is never treated as `IN_GAME` proof.

## Acceptance

- exact-current-build static discovery/resolver deterministic and fail-closed;
- reader returns bounded typed non-secret lifecycle state and distinguishes unavailable/read failure from healthy values;
- exact client or Qt-library mismatch disables the reader;
- collect-all integrates the reader without semantic-promotion authority;
- repository-only collect-all moves missing-reader count from 10 to 9 while privacy remains PASS;
- focused tests and compile/static checks PASS;
- required current Track A governance/CI PASS on exact final head;
- fresh independent audit has no open material finding;
- implementation PR merges to `main`;
- post-merge physical read-only causal E2E freshly re-admits the target and proves the implementation delta `auth missing -> AVAILABLE`, `10 -> 9`, privacy PASS without requiring a login-state transition;
- durable final evidence is recorded, task archived and ownership released.
