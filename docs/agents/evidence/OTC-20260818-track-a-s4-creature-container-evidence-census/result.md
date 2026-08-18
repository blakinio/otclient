# Track A S4 — creature/container evidence census

Task: `OTC-20260818-track-a-s4-creature-container-evidence-census`  
PR: `#517`  
Execution: GitHub-hosted repository evidence only, `runtime_access: none`

## Producer

```text
run      32120910903
job      95660747269
artifact 9318473016
digest   sha256:2759b4ec6e010485205f974bb726c2be350ffeed20a2417707cb207efd0b491d
result   SUCCESS
```

The producer scanned only the checked-out repository and Git history. It did not download or execute an official client, access Synology/X11/process memory, use credentials, log in, perform gameplay, or observe/mutate PR #475 runtime.

## Repository evidence inventory

The deterministic census found comparable broad evidence density for both families:

```yaml
container:
  paths_with_hits: 20
  total_line_hits: 82
  exact_address_paths: 13
  qmeta_paths: 2
  bounded_disassembly_paths: 0
  runtime_proven_paths_from_lexical_heuristic: 3
  history_commit_token_hits: 161
creature:
  paths_with_hits: 20
  total_line_hits: 77
  exact_address_paths: 13
  qmeta_paths: 3
  bounded_disassembly_paths: 0
  runtime_proven_paths_from_lexical_heuristic: 2
  history_commit_token_hits: 153
```

The `runtime_proven_paths_from_lexical_heuristic` field is diagnostic only. It is based on words such as `runtime/live/observed` appearing in evidence text and is **not** promoted as proof that either family has live runtime semantics.

## Exact retained QMeta discriminator

The decisive evidence is the already-committed exact-client QMeta census from run `31790507112`, job `94736106350`.

### Container

```text
tibia::container::TContainerProtocolMessageHandler
  QMeta record       0x3084fe0
  qt_static_metacall 0xd1e000
  method_count       35
  signal_count       11

tibia::container::TContainerStorage
  QMeta record       0x308e720
  qt_static_metacall 0xd15af0
  method_count       3
  signal_count       3
```

The capability census independently records container handler surfaces including close/up/paging/update, object-info requests, sorting, and moving contents to managed containers, plus `TContainerStorage::containerUpdated/containerRemoved`.

### Creature

```text
tibia::creatures::TCreatureProtocolMessageHandler
  QMeta record       0x30cec80
  qt_static_metacall 0xd12510
  method_count       0
  signal_count       0

tibia::creatures::TCreatureStorage
  QMeta record       0x3085ba0
  qt_static_metacall 0xd25b70
  method_count       3
  signal_count       3
```

The creature family remains valuable, but its protocol handler exposes no direct QMeta method/signal surface in this retained census, so exact handler routing would require a different static discriminator or an unavailable exact-client code window.

## Existing exact-build storage anchors

Promoted S1 also retains primary-vptr anchors:

```text
TContainerStorage 0x308a1a0
TCreatureStorage  0x308d078
```

These are identity/structural anchors only; they do not by themselves prove inbound mutation.

## Existing inbound name surfaces

Promoted S1 retains lexical correspondence for both families:

```text
GameserverMessageContainer         -> receivedContainerMessage
GameserverMessageCreateInContainer -> receivedCreateInContainerMessage
GameserverMessageChangeInContainer -> receivedChangeInContainerMessage
GameserverMessageDeleteInContainer -> receivedDeleteInContainerMessage

GameserverMessageCreatureData   -> receivedCreatureDataMessage
GameserverMessageCreatureHealth -> receivedCreatureHealthMessage
GameserverMessageCreatureUpdate -> receivedCreatureUpdateMessage
GameserverMessageMoveCreature   -> receivedMoveCreatureMessage
```

These remain name-surface correlations until exact queue/owner/receiver dataflow is proven.

## Selection

```yaml
NEXT_STATIC_FRONTIER: CONTAINER
REASON:
  - TContainerProtocolMessageHandler has a substantial exact retained QMeta surface: 35 methods / 11 signals.
  - TContainerStorage has an exact retained 3-signal QMeta surface.
  - exact generated-message and received-method name surfaces already exist for Container/Create/Change/DeleteInContainer.
  - this gives more independent exact anchors for a repo-only follow-up than the creature handler's 0-method/0-signal QMeta surface.
CREATURE_FRONTIER: DEFERRED_NOT_DISPROVEN
```

This is a prioritization result, not a claim that the container message-to-storage edge is already proven.

## Retained UNKNOWNs

```text
receivedContainer* exact owner/typed QMeta signal contract beyond name surface
queue -> container handler receiver connection
container handler -> TContainerStorage mutation
container storage data layout
runtime delivery / causal mutation

receivedCreature* exact owner/typed QMeta signal contract beyond name surface
creature handler/storage connection and mutation
runtime creature delivery
```

## Terminal S4 result

```yaml
S4_CENSUS: COMPLETED
NEXT_FRONTIER: CONTAINER
RUNTIME_ACCESS: none
CLIENT_DOWNLOAD: false
CLIENT_EXECUTION: false
PR475_RUNTIME_TOUCHED: false
```
