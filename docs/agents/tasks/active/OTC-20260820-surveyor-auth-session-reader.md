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
execution_reason: implementation PR #636 is merged; run one separately reviewed trusted-main passive post-merge collect-all and archive only after exact causal implementation acceptance
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: post-merge closeout is one bounded read-only acceptance followed by evidence/archive cleanup
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
base_main: 16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3
branch: fix/OTC-20260820-surveyor-auth-session-postmerge-e2e
implementation_pr: 636
implementation_merge_sha: 16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3
physical_e2e_required: true
physical_e2e_result: NOT_RUN
updated_at: 2026-08-21T08:08:00+02:00
next_action: validate and merge the one-shot trusted-main read-only acceptance workflow with exact phrase ONE_SHOT_SURVEYOR_AUTH_READ_ONLY; allow the workflow to freshly re-prove runtime identity before any semantic read
---

# Surveyor v2 next gap — auth/session typed reader

## Selected gap

Fresh pre-implementation repository-only and admitted physical Surveyor `--collect-all` both produced 169 canonical rows, 12 alias views, 10 missing typed readers and privacy PASS. `auth_session_typed_reader` ranked first at score 125. `world_minimap_typed_reader` tied at 125 but overlapped active #475/#593, so auth/session was selected.

## Implementation result

Implementation PR #636 merged to `main` as:

`16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3`

The merged reader is exact-current-build, fail-closed and read-only. It validates the exact official client and deployed Qt StateMachine library, resolves the singleton `TGameClient`, verifies `TGameClient + 0x8d0 -> TAuthenticationProcessController`, and exposes only the exact `QStateMachine::isRunning()`-equivalent lifecycle boolean.

It explicitly emits `TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, `credentials_retained=false`, `session_secrets_retained=false`, and `semantic_promotion_allowed=false`.

## Implementation validation

Exact implementation head `18bee436f57915bf61d59f0d068448a5b91e6ab1` passed:

- Track A Surveyor tests run `32452573096`: PASS;
- Python compile: PASS;
- 40/40 focused Surveyor tests: PASS;
- repository-only collect-all: 169 rows / 12 aliases / 9 missing readers / privacy PASS;
- CI run `32452573404`: PASS;
- Track A agent runtime governance `32452573189`: PASS;
- Track A canonical live governance `32452573109`: PASS;
- fresh exact-head validator audit: PASS, material findings 0;
- open review threads: 0.

## Historical physical before-evidence

The last explicitly admitted pre-implementation observation proved one exact current client in `otclient-track-a-kasmvnc`, display `:1`, PID `19590`, start ticks `76611792`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, one matching visible Tibia window, released lease generation `19`, and matching canonical registration generation `2` / lease generation `19`. Semantic registration state remained `UNKNOWN`.

That exact PID/start/control metadata is historical before-evidence only. The post-merge workflow must re-prove the current target from scratch and fails closed before `/proc/PID/mem` if PID/start/fence/window/registration ownership conditions no longer hold.

The target namespace itself was proven unique for the bounded read-only programme and remains the declared observation namespace. Frontmatter does not promote the historical PID/start values into current authority.

## Exact static/live lifecycle evidence

Durable implementation evidence:

`docs/agents/evidence/OTC-20260820-surveyor-auth-session-reader/current-build-auth-lifecycle.md`

Exact current identities:

- `TGameClient` typeinfo/vptr: `0x30a7778 / 0x30adce8`;
- `TAuthenticationProcessController` typeinfo/vptr: `0x30b4410 / 0x30b5290`;
- auth-controller member: `TGameClient + 0x8d0`;
- Qt StateMachine library size/SHA: `394824 / 26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8`;
- Qt `isRunning()` layout: private pointer `+0x8`, private state `+0xf0`, running value `2`.

Pre-implementation bounded read-only correlation observed lifecycle state `0`, equivalent to `authentication_state_machine_running=false`. This is not an `IN_GAME` discriminator.

## One-shot post-merge acceptance

Owned temporary workflow:

`.github/workflows/track-a-surveyor-auth-session-postmerge.yml`

It is push-to-main only, owner-actor gated and additionally requires the merge commit message marker `ONE_SHOT_SURVEYOR_AUTH_READ_ONLY`. It has `contents: read`, no secrets and no mutation path. Before semantic collection it must freshly prove:

- no conflicting fresh canonical lease owner;
- exactly one `client` in the declared target container;
- exact current size/SHA;
- process start ticks;
- display connectivity;
- exactly one matching visible Tibia window;
- canonical registration identity consistency when registration is present.

It then runs only the merged passive Surveyor collect-all and requires:

- runtime admission `AVAILABLE`;
- auth typed reader `AVAILABLE`;
- `process_memory_access=read_only`;
- `TYPED_AUTH_LIFECYCLE_ONLY`;
- `in_game_claimed=false`;
- credentials/session secrets retained false;
- aliases `12`;
- missing readers `9`;
- privacy PASS.

The causal acceptance is an implementation differential, not a login-state transition: pre-implementation auth reader `NO_TYPED_READER_IMPLEMENTED` / gap count `10` becomes post-merge `AVAILABLE` / gap count `9` on a freshly admitted physical snapshot.

## Hard safety boundary

No login/logout/relogin, user credential access, GUI/gameplay input, process control, attach/debug/injection, memory write, client/container restart, network mutation, item/economic action or local-model execution is authorized. The workflow reads only declared safe control metadata and the exact reader opens process memory with `O_RDONLY|O_CLOEXEC`.

`BRIDGE_3_OF_3` remains structural presence only and is never `IN_GAME` proof.

## Acceptance remaining

- one-shot workflow PR exact-head CI/governance/audit PASS;
- one-shot workflow merged to trusted `main` with the exact authorization marker;
- physical read-only acceptance PASS and sanitized artifact/log evidence captured;
- temporary one-shot workflow removed;
- durable post-merge evidence recorded;
- this task archived and runtime access reset to none.
