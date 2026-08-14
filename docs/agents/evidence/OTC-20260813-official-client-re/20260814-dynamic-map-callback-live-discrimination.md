# Track A dynamic world-map callback discrimination — corrected 2026-08-14

## Scope

Repository: `blakinio/otclient`
Track: `official-client-re` / Track A
Runner: `synology-otclient-01`
Subject: official native Linux Tibia client only
Official child-client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

This checkpoint supersedes both the initial unverified map-callback hypothesis and the later overcorrection that classified `+0xcecc70` / `+0xcecf40` as unrelated UI handlers. Exact Qt metaobject data embedded in the same official binary now identifies the owning class and method names directly.

The experiments used static binary inspection and bounded post-login GDB observation. They did not patch client code, modify or bypass BattlEye, inject gameplay packets, or persist credentials.

## Fresh verified world recovery

```text
workflow run: 31730884814
run attempt: 13
job: 94716022704
job conclusion: success
artifact: track-a-software-world-login
artifact_id: 9212815415
artifact_zip_digest: sha256:26b92d1e38c9fad9ef6f113ca1b2e4c675f25c477501722dbbaf761864ddb2e0
TRACK_A_POST_LOGIN_CHANGED_PIXELS=320319
TRACK_A_WORLD_CHANGED_PIXELS=660118
TRACK_A_LOCAL_SOCKS_ESTABLISHED=7
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
TRACK_A_SESSION_LEFT_RUNNING=true
```

## Existing post-login runtime controls

A post-login observer was previously armed against `+0xcecc70` and `+0xcecf40` with a clean zero-hit baseline. A real one-tile player movement (`run 31784304719`, job `94716687631`, artifact `9212883577`) changed the rendered world by 151920 pixels but produced zero hits. A separate bounded drag (`run 31784509337`, job `94717325713`, artifact `9212961464`) was proven by frame inspection to be only a hover/no-op and also produced zero hits.

Later, the observer recorded two `+0xcecf40` hits. Their event-associated memory included UTF-16 strings `Low lag (147 ms)` and an FPS-style string. Those records are still valid observations, but their earlier interpretation as proof that `cecf40` itself was a non-map UI handler was too strong. The function identity must be taken from the binary's own Qt metadata, while the status-text observation only proves that the particular object pointers/register assumptions used by that early runtime logger were not authoritative map payload decoding.

## Static recovery of the real Worldmap Qt dispatcher

A complete direct-call xref scan and focused disassembly established a Qt static-meta-call dispatcher at `+0xdf2a60`:

```text
test esi,esi
cmp edx,0xd
ja ...
lea rsi,[jump_table]
movsxd rax,DWORD PTR [rsi+rdx*4]
add rax,rsi
jmp rax
```

The exact 14-entry jump table at `0x1d8bd10` was decoded in:

```text
run: 31786047410
job: 94722066149
commit: 476236613b9a48e60a9a45e77689c2c7ab6a8c76
result: success
```

Decoded case targets:

```text
case  0 -> +0xdf2b58
case  1 -> +0xdf2b88
case  2 -> +0xdf2ba0
case  3 -> +0xdf2c00
case  4 -> +0xdf2c38
case  5 -> +0xdf2c70
case  6 -> +0xdf2ca8
case  7 -> +0xdf2cc0
case  8 -> +0xdf2cd8
case  9 -> +0xdf2cf0
case 10 -> +0xdf2d08
case 11 -> +0xdf2d20
case 12 -> +0xdf2d38
case 13 -> +0xdf2ac8
```

The case tails were independently disassembled. Relevant tail targets include:

```text
case 1  -> +0xcec8d0
case 2  -> left/right/top/bottom movement/map-description path
case 3  -> movement/map-description path
case 4  -> movement/map-description path
case 5  -> movement/map-description path
case 6  -> +0xcdbc90
case 7  -> +0xcdbe30
case 8  -> +0xcd3190
case 9  -> +0xcecc70
case 10 -> +0xcecf40
case 11 -> +0xcd4e20
case 12 -> +0xcd32c0
```

## Direct method names from the official binary

The `QMetaObject` corresponding to the `+0xdf2a60` dispatcher is at `0x3087800`. Its fields directly reference:

```text
stringdata/data regions: 0x1cd8a54 / 0x1cd8820
static_metacall:         0xdf2a60
related metadata:        0x2f6ab00
```

The method decode run was:

```text
run: 31786106136
job: 94722253536
commit: eb8090c2b633fd1824b17711072433704b3fb1e9
result: success
```

The embedded class name is:

```text
tibia::worldmap::TWorldmapProtocolMessageHandler
```

The ordered method strings in the same metaobject region are:

```text
publishGameAction
handleFullMapMessage
handleLeftColumnMessage
handleRightColumnMessage
handleTopRowMessage
handleBottomRowMessage
handleTopFloorMessage
handleBottomFloorMessage
handleFieldDataMessage
handleCreateOnMapMessage
handleChangeOnMapMessage
handleDeleteOnMapMessage
handleAmbientLightMessage
handleTibiaTimeMessage
```

The associated protobuf type names are also embedded next to the handlers, including:

```text
tibia::protobuf::protocol::GameserverMessageFullMap
tibia::protobuf::protocol::GameserverMessageLeftColumn
tibia::protobuf::protocol::GameserverMessageRightColumn
tibia::protobuf::protocol::GameserverMessageTopRow
tibia::protobuf::protocol::GameserverMessageBottomRow
tibia::protobuf::protocol::GameserverMessageTopFloor
tibia::protobuf::protocol::GameserverMessageBottomFloor
tibia::protobuf::protocol::GameserverMessageFieldData
tibia::protobuf::protocol::GameserverMessageCreateOnMap
tibia::protobuf::protocol::GameserverMessageChangeOnMap
tibia::protobuf::protocol::GameserverMessageDeleteOnMap
```

Because the metaobject has exactly 14 dispatch cases and exactly the ordered method set above, and the already-known full-map/directional/floor handlers align with cases 1 through 7, the dynamic mutation identities are established for this binary:

```text
+0xcd3190 = handleFieldDataMessage
+0xcecc70 = handleCreateOnMapMessage
+0xcecf40 = handleChangeOnMapMessage
+0xcd4e20 = handleDeleteOnMapMessage
+0xcd32c0 = handleAmbientLightMessage
case 13    = handleTibiaTimeMessage
```

This mapping is direct binary evidence, not an OTClient naming assumption.

## Structural behavior of the three mutation handlers

Static disassembly is consistent with the recovered names:

### `+0xcecc70` — `handleCreateOnMapMessage`

The handler consumes a position-like record, resolves a world-map/tile object through a virtual method, obtains a thing/object payload and stack/index-like field, invokes helper `+0xceca50`, and dispatches a virtual mutation operation on the resolved map object.

### `+0xcecf40` — `handleChangeOnMapMessage`

The handler consumes a position-like record, thing/object payload and stack/index-like field, resolves the target world-map/tile object, invokes helper `+0xceca50`, and dispatches a different virtual mutation operation. It also contains an alternate branch for another object-position encoding.

### `+0xcd4e20` — `handleDeleteOnMapMessage`

The handler consumes an object-position representation with multiple variants, resolves a world-map target, and follows deletion/object-class-specific paths. The surrounding code includes object type/vtable checks and dynamic-cast-style handling.

These structural observations explain why the functions looked map-related before their names were recovered.

## Reinterpretation of the earlier status-text hits

### PROVEN

- `+0xcecf40` is the official binary's `handleChangeOnMapMessage` for `TWorldmapProtocolMessageHandler`.
- The two old GDB records at this address nevertheless exposed pointers whose memory contained `Low lag (147 ms)` and FPS-style text.
- Therefore those old register/object-field assumptions did **not** correctly decode the authoritative `GameserverMessageChangeOnMap` payload.

### INFERENCE

The status strings may have been reached through stale/transient/shared pointer state, an incorrect interpretation of the handler's C++ argument wrapper, or an indirect object referenced during processing. They must not be used to classify the handler itself.

### REJECTED

- `+0xcecf40` is purely a status/performance UI handler: **rejected by direct QMetaObject method-name evidence**.
- the old `event+0x18` pointer is a plain `x,y,z` tuple: **still rejected by direct live memory values**.
- two unclassified hits alone prove a user item placement: **still rejected**; exact payload decoding is required.

## Current proven architecture

```text
FULL / STRIP SNAPSHOT PATH
  handleFullMapMessage / directional / floor handlers
  -> map description routine around +0x19a8a80
  -> proven structural record hook +0x19a8ea3

DYNAMIC WORLD-MAP PATH
  +0xcecc70 = CreateOnMap
  +0xcecf40 = ChangeOnMap
  +0xcd4e20 = DeleteOnMap

FIELD DATA PATH
  +0xcd3190 = FieldData

PROVENANCE LAYER
  required to distinguish map-loaded/static state from later dynamic mutations
```

This directly supports the user's earlier hypothesis that initial/map-loaded state and later player/environment modifications travel through different processing paths, while not implying that the client itself labels an object as 'map-editor-created'.

## Remaining unknowns

- Exact in-memory protobuf/wrapper field layout at entry to CreateOnMap, ChangeOnMap and DeleteOnMap.
- Correct authoritative extraction of world `x,y,z`, stack position and stable appearance/type identifier for each dynamic event.
- Whether creature movement is represented through these modern protobuf messages or a separate handler/class in this client version.
- Proven dynamic classification of corpses, effects, missiles, doors/transforms and player-dropped items.

## Exactly one next action

Arm a new post-login observer on the now-identified `CreateOnMap`, `ChangeOnMap` and `DeleteOnMap` handlers, but log raw argument-wrapper bytes/pointers first rather than reusing the disproven `event+0x18 = position` assumption. Correlate exactly one controlled world mutation with one handler and decode its protobuf/wrapper layout from that evidence before generalizing.
