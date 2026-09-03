---
task_id: OTC-20260903-be4f48-prelogin-sequence-promotion
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: close
branch: docs/archive-OTC-20260903-be4f48-prelogin-sequence-promotion
base_branch: main
base_main: 4bf27c0ffb376d789df78a6c78930b3d5f1dfb93
created: 2026-09-03T17:28:00+02:00
completed: 2026-09-03T17:37:30+02:00
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
  - docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/**
  - docs/agents/tasks/archive/OTC-20260903-be4f48-prelogin-sequence-promotion.md
modules_touched: []
reuses:
  - source Draft PR #865 exact-current static evidence at 8d6c752cd3d009a78b5deddb650c752c95156298
  - exact-current writer run 32998976901 at 3d87d729b73f868aefe1662c72af666a4921b1d8
blocks:
  - Track B PR #284 next material outbound hypothesis
---

# Objective

Promote only independently verified exact-current source facts for Linux Tibia `15.32.be4f48` (`52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`) from source Draft PR #865 and the already-existing exact-current writer evidence, preserve the fail-closed `SOURCE_BLOCKER`, merge the clean promotion, close the source PR unmerged as consumed, and archive the lifecycle without modifying Track B PR #284.

# Completion

Coordinator promotion PR #866 was rebuilt cleanly from trusted `main@05a0befa9670b164e5d88046584899ae3aaebb29`, validated, and squash-merged:

```text
promotion PR          #866
promotion final head  025ddbf29aff4d235339a38a488f243556e5230b
promotion CI          33773519831 = SUCCESS
promotion governance  33773519545 = SUCCESS
promotion merge       4bf27c0ffb376d789df78a6c78930b3d5f1dfb93
changed files         3 docs-only
review submissions    0
review threads        0
material comments     0
```

The initial promotion head `5e2878502292b0344d4a84959b53b903acc83e50` had CI `33773362539=SUCCESS` but deterministic governance job `100708897807` correctly failed because the static coordinator task omitted mandatory Track A admission metadata. Commit `025ddbf29aff4d235339a38a488f243556e5230b` added only the required `NOT_APPLICABLE` admission fields under `runtime_access: none`; exact-head governance then passed. No promoted scientific evidence changed.

Source Draft PR #865 was closed **unmerged as consumed** after promotion merge:

```text
source PR             #865 = CLOSED_UNMERGED
source head           8d6c752cd3d009a78b5deddb650c752c95156298
source workflow       33756449924 = SUCCESS
source job            100651924970 = SUCCESS
source CI             33756450210 = SUCCESS
source governance     33756449991 = SUCCESS
source boundary       33756449971 = SUCCESS
source artifact       9893838828
artifact sha256       20043e76288cf7377c480015a1c2726fb76f39fd1366e43faae445c3bfd87cee
result.json sha256    c44a1cdd3f20a84da4ca3c8ec6970a0dc86ef46c89ee8cd348db7d46729a2d37
```

Independent exact-current writer evidence retained by the promotion:

```text
writer run             32998976901 = SUCCESS
writer head            3d87d729b73f868aefe1662c72af666a4921b1d8
writer artifact        9886703883
writer artifact sha256 84e88080ea862d2faf82fc169dde5f908fc5fd7a856585e434523795481fc4fa
writer result sha256   296f5a915d15f9383fc3f1c7809eb5c6934a3deb24a9e2b9cd1808b660c40f14
```

# Final decision

`terminal_result=SOURCE_BLOCKER`.

Promoted exact-current facts:

- `tibia::protobuf::protocol::GameclientMessageLogin.field6` is structurally PRESENT and sourced from producer input `edx`; the exact value and semantic name remain UNKNOWN.
- exact-current `TProtocolMessageQueue::sendLogin` QMeta target `0xde82a2` uniquely tail-transfers at `0xde82ae` to adapter `0xbd3050`, FDE `0xbd3050..0xbd34dd`.
- the current connection-block peer target `0xd052a0` has no `TGameClient` QMeta candidate; sender-side causal ordering remains unproven.
- bounded `PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN` with no proved queue send methods.
- independent writer evidence proves current sendLogin QMeta/first direct edge/adapter FDE/adapter indirect calls but retains `final_writer_contract=UNKNOWN`.

```text
PRE_LOGIN_SEQUENCE_COMPLETE=false
PRE_LOGIN_MESSAGE_ORDER=UNKNOWN
PRE_LOGIN_REQUIRED_MESSAGE_MISSING_IN_OTCLIENT=UNKNOWN
FIELD6_PRESENT=true
FIELD6_SOURCE=producer input edx
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=exact-current sender-side native event/peer identity and direction for the connection that binds TProtocolMessageQueue::sendLogin
SECONDARY_MISSING_BOUNDARY=sendLogin serialized queue object -> final queue/TCP writer contract
```

# Safety / Track B

No official client execution, login, credentials/session material, process-memory read, packet capture, raw-client upload or official-service E2E occurred in this source task. PR #284 was not modified by this task or its promotion. This result does not authorize a guessed Field6 value, a Track B payload mutation, or another official-service E2E.

next_action: keep Track B PR #284 blocked on the promoted exact-current source boundary. Do not relaunch the #865 analyzer, broaden BFS, reuse historical literals, or introduce new architecture unless a new concrete discriminator can prove one of the two missing boundaries above.
