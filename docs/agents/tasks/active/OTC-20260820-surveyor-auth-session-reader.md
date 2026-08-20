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
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-20T23:00:00+02:00
next_action: reclassify to read_only only after the reviewed Track A physical preflight can prove current ownership, namespace and exact target uniqueness
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

## Scope

Implement the smallest exact-current-build, fail-closed, secret-free typed auth/session reader that materially improves the ranked Surveyor gap. It may expose only bounded non-secret lifecycle/session facts whose semantics can be proven structurally and, where required, causally without login/relogin or agent-generated gameplay input.

Expected owned paths are limited to:

- `tools/tibia_re_surveyor/**` for the reader and collect-all integration;
- `tests/tools/tibia_re_surveyor/**` for deterministic focused tests;
- `docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/**`;
- this task record and required closeout/catalog/changelog metadata.

Do not modify or take ownership of PR #475/#593 world-map surfaces, Control Center, Ollama, credentials, login, network mutation, client bytes, or process memory writes.

## Runtime boundary

Initial admission is `runtime_access: none`. No live official-client observation is authorized by this checkpoint. Before any runtime-related operation, update this task with a fresh `read_only` admission that proves current runtime ownership/non-conflict, namespace, exact target uniqueness, exact client fence and every current operator precondition. Read-only observation never authorizes login, input, process control, attach/debug/injection, memory writes, item/economic actions, or secret-bearing memory access.

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
