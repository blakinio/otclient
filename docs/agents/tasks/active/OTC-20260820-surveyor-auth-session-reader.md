---
task_id: OTC-20260820-surveyor-auth-session-reader
status: investigating
phase: investigate
agent: ChatGPT
project_lane: otclient
lane: P0-AUTH
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
execution_mode: chat_remote_shell
execution_reason: current-main repository inspection plus bounded read-only physical Surveyor validation
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one typed reader with one exact-build structural resolver and one bounded read-only causal acceptance path
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: synology:otclient-track-a-kasmvnc:display-1:client-19590
canonical_registration: PRESENT
canonical_lease_generation: 19
registration_lease_generation: 19
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
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-20T23:12:00+02:00
next_action: run one fresh current-main passive collect-all against the exact admitted target, then perform bounded static discovery for the selected auth/session typed reader
---

# Surveyor v2 next gap — auth/session typed reader

## Current-main selection evidence

Trusted base at task start: `73487b0746b898365c759dbfc193e914e619acfb`.

A fresh repository-only current-main Surveyor `--collect-all` run produced:

- canonical rows: 169;
- alias views: 12;
- missing typed readers: 10;
- privacy scan: PASS;
- implemented typed reader: `player_state_typed_reader`;
- rank 1: `auth_session_typed_reader`, canonical priority score 125, 14 unresolved affected rows;
- rank 2: `world_minimap_typed_reader`, canonical priority score 125.

`world_minimap_typed_reader` is not selected because current open PR #475 owns the physical world-map server-delivery frontier and open PR #593 owns current world-minimap static G1 evidence. Selecting it would create material overlap. `auth_session_typed_reader` therefore has the highest current blocker/dependency priority without that known overlap.

## Fresh physical read-only admission

The current KasmVNC/Surveyor preflight was re-run from scratch after this task was admitted for read-only preflight:

- target container `otclient-track-a-kasmvnc`: running;
- control container `otclient-synology-runner`: running;
- display `:1`: connect PASS;
- exact `client` PID: `19590`;
- process start ticks: `76611792`;
- executable: `/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client`;
- executable size: `52109920`;
- SHA-256: `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`;
- exact target processes in declared namespace: `1`;
- visible Tibia windows on display: `1`;
- matching window owner count: `1`;
- target uniqueness: `PROVEN`;
- canonical lease: present, `released`, generation `19`, no active controller task;
- canonical registration: present, generation `2`, lease generation `19`, identity matches PID/start/size/SHA/display, state `UNKNOWN`;
- process environment read: false;
- raw window title retained: false.

Because the lease is released and no active controller owns the runtime, `runtime_owner_task=NOT_APPLICABLE` is proven for this read-only observation. Registration identity agrees with the freshly observed target. No Gate A/Gate B/rebind/bootstrap gate is required for non-invasive read-only observation; mutation remains forbidden.

## Scope

Implement the smallest exact-current-build, fail-closed, secret-free typed auth/session reader that materially improves the ranked Surveyor gap. It may expose only bounded non-secret lifecycle/session facts whose semantics can be proven structurally and, where required, causally without login/relogin or agent-generated gameplay input.

Expected owned paths are limited to:

- `tools/tibia_re_surveyor/**` for the reader and collect-all integration;
- `tests/tools/tibia_re_surveyor/**` for deterministic focused tests;
- `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/**`;
- this task record and required closeout/catalog/changelog metadata.

Do not modify or take ownership of PR #475/#593 world-map surfaces, Control Center, Ollama, credentials, login, network mutation, client bytes, or process memory writes.

## Runtime boundary

Only bounded semantic observation of the exact admitted target is permitted. Any lease/registration/PID/start/fence/display/window identity change triggers fresh re-admission before further observation.

Read-only observation never authorizes login, input, process control, attach/debug/injection, memory writes, item/economic actions, network mutation, or secret-bearing memory access. `mutation_authorized=false` throughout this slice.

`BRIDGE_3_OF_3` remains structural presence only and must not be treated as `IN_GAME` proof.

## Acceptance

- exact-current-build static discovery/resolver is deterministic and fail-closed;
- reader returns bounded typed non-secret state and distinguishes unavailable/read failure from healthy values;
- exact SHA/size/profile mismatch disables the reader;
- collect-all integrates the reader without semantic promotion authority;
- privacy scan remains PASS;
- focused tests and compile/static checks PASS;
- required current Track A governance/CI PASS on exact final head;
- fresh independent audit has no open material finding;
- post-merge physical read-only causal E2E PASS with owner action only if the selected field requires one;
- durable evidence is recorded, task archived, and ownership released.
