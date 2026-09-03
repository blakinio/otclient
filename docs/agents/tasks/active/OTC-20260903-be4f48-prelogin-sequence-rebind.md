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

Only rebind the exact-client fence and repair the smallest build-drift assumptions proven by failing static gates. No new architecture, subsystem, broad BFS expansion, runtime experiment, feature toggle, or Track B E2E.

# TDD evidence

1. Fence RED: commit `96ee55ae5b0757870359050ad6932cace4220c7e`, run `33742788471`, job `100608313904` failed at contract validation before package acquisition.
2. Fence GREEN: commit `17b1f32769570241174b74a48192a5274b00097f`, run `33742917386`, job `100608729800` succeeded on exact `be4f48`; sanitized result retained only.
3. Exact-current result remained `PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN`: direct-call BFS from current `TGameClient` roots did not reach any queue `send*`. This proves the next discriminator must target the indirect binding, not increase BFS depth.
4. Adapter RED: commit `9bc619170d5e8bd74d13181effc5f86458286e8e`, run `33744487648`, job `100613732741` failed at contract validation with `sendLogin indirect binding discriminator not implemented`; all client materialization steps were skipped.
5. First adapter implementation: commit `91095813cce1ce192b8dfb27939bf33a8ab4ef9c`, run `33748565022`, job `100626619546`, artifact `9890726629` on exact `be4f48`. The sanitized result falsified the initial bounded-method assumption because adjacent QMeta methods shared one FDE.
6. Adapter method-boundary GREEN: commit `473be1ad313e181d27b4db76f83135165471bf8a`, run `33749268039`, job `100628816886`, artifact `9891026284`, digest `sha256:73064e958b3f856fbaa764ef1620b7f4dad59ad1087537560e6cdd2dfb81383c`. Exact-current sanitized result proves `sendLogin` QMeta target has one external tail transfer to adapter `0xbd3050`; independent exact-current writer artifact `9886703883` independently derived the same edge.
7. Connection-peer RED: commit `434941b4972467b890ed25162649e377d8ab3ad2`, run `33750080047`, job `100631379090` failed exactly because `sendlogin_connection.py` did not exist; package acquisition and client materialization were skipped.
8. Connection-peer GREEN: source head `d08bbeec7d7b0abf3ca565a96d089e8e44c3a6f7`, run `33755030910`, job `100647297444`, artifact `9893295350`, artifact digest `sha256:c6f45e4ccf4a9b1267293bfe00f79ac6565cecfda7fd25413b041f76a5a7db73`, sanitized `result.json` SHA-256 `c44a1cdd3f20a84da4ca3c8ec6970a0dc86ef46c89ee8cd348db7d46729a2d37`. Exact-head governance `33755030811`, self-hosted boundary `33755030936`, and CI `33755031063` all succeeded.

# Exact-current findings

- `tibia::protobuf::protocol::GameclientMessageLogin` remains the current typed login message.
- Outer field 6 is present and is produced from login-producer input `edx` through `r14d` into the current field-6 storage slot. Its exact runtime scalar value remains `UNKNOWN`; no historical 0/1 value is promoted.
- `TProtocolMessageQueue::sendLogin` QMeta resolves to one current adapter; that structural adapter edge was independently falsified by the separate current writer analysis.
- The adapter's unique aligned reference owner contains a current static connection-construction block. The block independently re-derives the two object-field displacements used around the callable construction, but the analyzer also identifies a stack-temporary false positive; therefore endpoint semantic ownership is not promoted.
- The second executable callable in that block does not match any exact-current `tibia::client::TGameClient` QMeta method or signal. The hypothesis `peer callable == TGameClient QMeta event` is disproven for this build.
- The inherited historical QObject/connect-target and owner-field literals are not used as current authority. Coincidental current structural values are not given semantic names without an independent current identity proof.
- The bounded first-game-server-connect graph still proves no complete ordered queue send sequence. `sendLogin`, `sendEnterWorld`, and `sendSecondaryLogin` remain causally unbound in the required pre-success sequence.
- Separate exact-current writer evidence still leaves the downstream queue/TCP writer contract unresolved.

# Terminal source decision

`terminal_result=SOURCE_BLOCKER`

This is not `IMPLEMENTABLE_DELTA_PROVEN`: the structural Field6 omission in Track B is real, but its material value is unknown and the native pre-login message ordering is still incomplete. It is also not `RUNTIME_FIELD6_REQUIRED` because Field6 is not the only remaining unknown; static sequence and downstream writer boundaries remain unresolved.

```text
PRE_LOGIN_SEQUENCE_COMPLETE=false
PRE_LOGIN_MESSAGE_ORDER=UNKNOWN
PRE_LOGIN_REQUIRED_MESSAGE_MISSING_IN_OTCLIENT=UNKNOWN
CURRENT_GAME_LOGIN_FIELD6_PRESENT=true
CURRENT_GAME_LOGIN_FIELD6_SOURCE=producer input edx
CURRENT_GAME_LOGIN_FIELD6_STATIC_VALUE=UNKNOWN
FIELD6_STRUCTURAL_MISMATCH_PROVEN=true
FINAL_LOGIN_SERIALIZER_IDENTIFIED=true
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
TRACK_B_CURRENT_WIRE_DELTA=UNKNOWN
RUNTIME_FIELD6_OBSERVATION_REQUIRED=false
OFFICIAL_SERVICE_E2E_COUNT=0
CREDENTIALS_USED=false
RUNTIME_ACCESS=none
```

`FIRST_MISSING_BOUNDARY=exact-current be4f48 static signal/callable identity and direction in the connection block that binds the TProtocolMessageQueue::sendLogin adapter; specifically identify the sender-side native message event before claiming pre-login ordering`

Secondary unresolved boundary: `sendLogin serialized queue object -> final queue/TCP writer`.

# Disposition

Stop source investigation here under strict anti-loop. Do not modify or E2E-test PR #284 from this result. A clean coordinator promotion may consume only the exact-current sanitized facts and the blocker above; source analyzers, historical addresses/Field6 values, payload bytes, secrets, and proprietary client material must not be promoted.
