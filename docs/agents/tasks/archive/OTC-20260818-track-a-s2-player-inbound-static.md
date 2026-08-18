---
task_id: OTC-20260818-track-a-s2-player-inbound-static
status: completed
agent: ChatGPT
session_role: researcher_then_coordinator_review
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
execution_mode: github_only
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
mutation_authorized: false
source_pr: 512
source_branch: research/OTC-20260818-track-a-s2-player-inbound-static
source_final_head: d0c78772294cd6355221cce96f499b85fb7738cf
base_main: a9e7ab21ed0962482e4381aadd50be92714785a6
completed: 2026-08-18T10:28:00+02:00
risk: medium
owned_paths_released: true
---

# Terminal result

```yaml
RESEARCH_RESULT: COMPLETE_BOUNDED
PROMOTION_DECISION: ACCEPT_WITH_EDITS
EXACT_CLIENT: 15.32.df7b29
EXACT_CLIENT_SIZE: 51965216
EXACT_CLIENT_SHA256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
RUNTIME_ACCESS: none
PR475_RUNTIME_TOUCHED: false
```

## Promoted exact contracts

`TPlayerProtocolMessageHandler`:

```text
primary vptr       0x308a008
staticMetaObject   0x30852a0
qt_static_metacall 0xd1a920
methods/signals    22 / 22
dispatch table     0x1d713d0
```

Its QMeta surface is outbound/control (`sendGo*`, `sendStop`, `sendRotate*`, `sendSetTactics`, `worldEntered`, etc.). Direct QMeta ownership of `receivedPlayer*Message` is **DISPROVEN**.

`TProtocolMessageQueue` owns all five selected exact player receive signals:

```text
class              tibia::protocol::TProtocolMessageQueue
staticMetaObject   0x3085b60
qt_static_metacall 0xdf5fe0
methods/signals    355 / 192
dispatch table     0x1d8bd6c

index 34  receivedPlayerDataCurrentMessage(GameserverMessagePlayerDataCurrent) @ 0xdf8bc1
index 43  receivedPlayerDataBasicMessage(GameserverMessagePlayerDataBasic) @ 0xdf8d3b
index 48  receivedPlayerStateMessage(GameserverMessagePlayerState) @ 0xdf8e0d
index 49  receivedPlayerSkillsMessage(GameserverMessagePlayerSkills) @ 0xdf8e37
index 117 receivedPlayerInventoryMessage(GameserverMessagePlayerInventory) @ 0xdf899f
```

Every listed stub invokes `QMetaObject::activate@0x4dedc0` using the corresponding signal index.

`TPlayerData`:

```text
primary vptr       0x308ca70
staticMetaObject   0x307ea60
qt_static_metacall 0xd19f40
methods/signals    5 / 5
dispatch table     0x1d7139c
```

Its five QMeta signals are `playerDataChanged`, `publishGameAction`, `playerLevelUp`, `vocationSpecificPlayerDataChanged`, `vocationChanged`.

## Retained UNKNOWNs

```yaml
network_decoder_to_queue_signal_emission: UNKNOWN
queue_signal_to_TPlayerProtocolMessageHandler_connection: UNKNOWN
exact_connected_receiver_member: UNKNOWN
handler_to_TPlayerData_mutation: UNKNOWN
TPlayerData_XYZ_candidate_as_inbound_target: UNKNOWN
runtime_delivery_and_causal_state_change: UNKNOWN
```

The existing PR #302 `TPlayerData +0x78/+0x7c/+0x80` XYZ-shaped candidate remains only a static candidate and was not promoted as inbound storage or authoritative player position.

## Producer evidence

Phase 1 — handler/data QMeta:

```text
run      32115252111
job      95643199117
artifact 9316455906
digest   sha256:434340656a520110ac417fbd1fbd844664e7b2d49da418e7de5bc21b8f830fa5
```

Phase 2 — global receive-owner census:

```text
run      32115662884
job      95644479664
artifact 9316573491
digest   sha256:ec97899357f6db77d45cf915d9133c778d48469f03628ea8914d6402ca3aca8f
global valid QMetaObjects 708
target matches 5/5
unique target owner tibia::protocol::TProtocolMessageQueue
```

## Repair / review history

1. First producer attempt `32114891658 / 95642067206` failed after exact hashes passed because Capstone skipdata pseudo-instructions were queried for operands. The bounded repair separated normal function decoding from whole-section skipdata scanning. No failed-run semantic result was promoted.
2. Final source governance run `32116125158` exposed missing universal admission metadata on a static `runtime_access:none` task. The task added all required runtime-admission fields explicitly as `NOT_APPLICABLE`; research semantics did not change.

## Source exact-head validation

Source final head `d0c78772294cd6355221cce96f499b85fb7738cf`:

```text
Track A governance 32116406977 = SUCCESS
  Deterministic admission-policy audit 95646794390 = SUCCESS
  Fresh admission behavior audit      95646794402 = SUCCESS
CI 32116407136 = SUCCESS
  CI / Required                       95646841777 = SUCCESS
reviews = 0
unresolved review threads = 0
main freshness = PASS at a9e7ab21ed0962482e4381aadd50be92714785a6
```

Physical E2E is `NOT_APPLICABLE`: static exact-file discovery only.

## Safety / non-overlap

```yaml
synology_used: false
x11_or_vnc_used: false
process_memory_used: false
credentials_used: false
login_performed: false
gameplay_performed: false
raw_client_committed_or_uploaded: false
pr475_runtime_observed: false
pr475_runtime_mutated: false
```

## Next independent frontier

```text
TProtocolMessageQueue receivedPlayer* signal
  -> exact QObject typed-connect construction
  -> exact receiver object/type
  -> exact receiver member / QSlotObject trampoline
```

Only after that static edge should a later task trace the receiver into `TPlayerData`.
