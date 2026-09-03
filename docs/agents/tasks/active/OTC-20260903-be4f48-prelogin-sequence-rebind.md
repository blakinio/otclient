---
task_id: OTC-20260903-be4f48-prelogin-sequence-rebind
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: implement
branch: research/OTC-20260903-be4f48-prelogin-sequence-rebind
base_branch: main
base_main: 05a0befa9670b164e5d88046584899ae3aaebb29
created: 2026-09-03T10:00:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-current-game-login-pre-success-outbound.yml
  - tools/tibia_re_current_game_login_pre_success_outbound/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-prelogin-sequence-rebind.md
reuses:
  - closed source PR #743 analyzer at 1342423c6fe4ef675f4b0b0cdc39ae012089f20e
  - trusted current client fence 15.32.be4f48 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
blocks:
  - Track B PR #284 next material outbound hypothesis
---

# Objective

Rebind the already-proven source-only pre-success outbound analyzer from closed PR #743 to exact current public Linux Tibia `15.32.be4f48` (`52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`) without changing analyzer architecture. Recover the bounded native outbound ordering from the game-server connection root through `GameclientMessageLogin` up to the first login-success receive edge.

# Safety

Static-only GitHub-hosted research. Do not execute the official client, log in, use credentials/session values, read process memory, capture packets, or upload the raw proprietary client. Do not modify Track B PR #284 and do not run an official-service E2E.

# Anti-loop

Only rebind the exact-client fence and repair the smallest build-drift assumptions proven by failing static gates. No new architecture, subsystem, or broad refactor.

# TDD evidence

1. Fence RED: commit `96ee55ae5b0757870359050ad6932cace4220c7e`, run `33742788471`, job `100608313904` failed at contract validation before package acquisition.
2. Fence GREEN: commit `17b1f32769570241174b74a48192a5274b00097f`, run `33742917386`, job `100608729800` succeeded on exact `be4f48`; sanitized result retained only.
3. Exact-current result remained `PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN`: direct-call BFS from current `TGameClient` roots did not reach any queue `send*`. This proves the next discriminator must target the indirect binding, not increase BFS depth.
4. Adapter RED: commit `9bc619170d5e8bd74d13181effc5f86458286e8e`, run `33744487648`, job `100613732741` failed at contract validation with `sendLogin indirect binding discriminator not implemented`; all client materialization steps were skipped.
5. First adapter implementation: commit `91095813cce1ce192b8dfb27939bf33a8ab4ef9c`, run `33748565022`, job `100626619546`, artifact `9890726629` on exact `be4f48`. The sanitized result falsified the initial bounded-method assumption: the scan crossed the first unconditional tail jump and consumed adjacent QMeta methods, yielding `UNKNOWN_MULTIPLE_EXTERNAL_DIRECT_TRANSFERS` with four candidates.
6. Adapter method-boundary GREEN: commit `473be1ad313e181d27b4db76f83135165471bf8a`, run `33749268039`, job `100628816886`, artifact `9891026284`, digest `sha256:73064e958b3f856fbaa764ef1620b7f4dad59ad1087537560e6cdd2dfb81383c`. Exact-current sanitized result proves `sendLogin` QMeta target has one external tail transfer to adapter `0xbd3050`; independent exact-current writer artifact `9886703883` had already derived the same edge. The adapter has no direct-call xrefs and one unique RIP-owner FDE `0x7c6700-0x7cc933` (duplicate byte-aligned RIP detections at the same instruction are normalized as one owner).
7. The unique adapter reference occurs inside a repeated static connection-construction block. The same bounded block contains a second executable callable and the endpoint object loads, but these values are not promoted by inspection alone. The next RED requires deriving the connection peer, endpoint displacements, and connection call target from exact-current bytes without hardcoding the observed addresses.

# Current exact boundary

Exact-current `TProtocolMessageQueue::sendLogin` QMeta -> adapter binding is complete and independently falsified. Causal ordering is not yet complete. The first missing edge is the unique static connection block containing the `sendLogin` adapter: identify its peer callable and map that peer against exact-current QMeta methods, fail-closed. Inherited #743 literals such as the old QObject-connect target / owner field are historical guidance only until independently re-derived from this current connection block.

# Terminal outputs

- `PRE_LOGIN_SEQUENCE_COMPLETE=true|false`
- `PRE_LOGIN_MESSAGE_ORDER=<sanitized identities or UNKNOWN>`
- `PRE_LOGIN_REQUIRED_MESSAGE_MISSING_IN_OTCLIENT=<type or NONE/UNKNOWN>`
- `terminal_result=IMPLEMENTABLE_DELTA_PROVEN|STATIC_BOUNDARY_COMPLETE|INCONCLUSIVE`

next_action: TDD RED for an exact-current sendLogin connection-peer discriminator; then derive the peer callable and map it against current TGameClient QMeta without hardcoded observed addresses.
