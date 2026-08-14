# Track A callback live discrimination — corrected 2026-08-14

## Scope

Repository: `blakinio/otclient`
Track: `official-client-re` / Track A
Runner: `synology-otclient-01`
Subject: official native Linux Tibia client only

This checkpoint supersedes the initial hypothesis that child-client offsets `+0xcecc70` / `+0xcecf40` were map/item callbacks. Later live object-graph evidence disproved that interpretation.

The experiments used post-login GDB hardware breakpoints against the Track A-owned official client. They did not patch client code, modify or bypass BattlEye, inject gameplay packets, or persist credentials.

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

## Fresh observer and baseline

```text
observer run: 31783518111
observer job: 94716375182
result: success
live client pid: 19092
persistent gdb pid: 19394
client PIE base: 0x560e600db000
breakpoint candidates:
  - base + 0xcecc70
  - base + 0xcecf40
```

Collector job `94716527251` verified that the client and detached GDB persisted after Actions cleanup and initially reported zero hits.

## Controlled player movement negative control

```text
workflow: .github/workflows/tibia-official-client-re-controlled-step.yml
run: 31784304719
job: 94716687631
artifact_id: 9212883577
TRACK_A_CONTROLLED_STEP_CHANGED_PIXELS=151920
TRACK_A_DYNAMIC_MAP_EVENTS_BEFORE=0
TRACK_A_DYNAMIC_MAP_EVENTS_AFTER=0
```

The downloaded XWD artifact was directly inspected and shows a real one-tile movement while remaining in the normal game world. Thus post-login GDB attach did not itself force logout in this trial, and ordinary player movement did not hit the two candidate callbacks.

## Controlled drag no-op

```text
workflow: .github/workflows/tibia-official-client-re-controlled-item-drag.yml
run: 31784509337
job: 94717325713
artifact_id: 9212961464
TRACK_A_CONTROLLED_ITEM_DRAG_CHANGED_PIXELS=30760
TRACK_A_DYNAMIC_MAP_EVENTS_BEFORE=0
TRACK_A_DYNAMIC_MAP_EVENTS_AFTER=0
```

Direct inspection of the downloaded before/after XWD frames proved that no ground item moved; only the tile hover/selection highlight changed. This is a UI no-op control, not item-movement evidence.

## Exact later callback records

The corrected schema-2 collector finally exposed the exact records that were previously hidden by unrelated shared-library warning output.

```text
collector run: 31784814270
collector job: 94718266716
TRACK_A_DYNAMIC_MAP_EVENT_COUNT=2
TRACK_A_DYNAMIC_MAP_ARG_COUNT=2

EVENT handler=cecf40 ... rsi=0x560e7c6d0c20 ...
ARG cecf40 event_ptr=0x560e7c6d0c20 pos_ref=0x560e7c7cd7a0 thing_ptr=0x560e7d103560 stack_raw=0x2 flags=0x7

EVENT handler=cecf40 ... rsi=0x560e7ab5fa80 ...
ARG cecf40 event_ptr=0x560e7ab5fa80 pos_ref=0x560e7d275d80 thing_ptr=0x560e7e0391f0 stack_raw=0x2 flags=0x7
```

Both hits were `cecf40`; no `cecc70` hit was recorded.

The two hits occurred after the controlled step/no-op-drag windows had already independently ended with zero hits, so they cannot be attributed to either controlled action. They also cannot be attributed to the earlier user item placement, because the observer had been freshly re-armed and its log truncated after that earlier session.

## Live object-graph classification

Static disassembly from job `94710283300` shows `cecf40` consuming `rsi+0x10`, `rsi+0x18`, `rsi+0x20` and `rsi+0x28` through an object/model-style callback path.

The first attempt to interpret the object referenced by `event+0x18` as a simple position tuple was disproved by live memory run `31784874756`, job `94718452402`: the 12 bytes at `ref+0x18` were pointer-like values, not plausible Tibia coordinates.

A deeper live object-graph probe then ran as:

```text
run: 31784940411
job: 94718659436
result: success
TRACK_A_CECF40_RECORD_COUNT=2
```

The live event objects contained directly readable UTF-16 text payloads. Record 1 includes the sequence:

```text
0x00200077006f004c
0x002000670061006c
0x0037003400310028
0x00290073006d0020
```

Interpreted as little-endian UTF-16 code units this is:

```text
Low lag (147 ms)
```

The other record contains an FPS-style text payload ending in `fps`.

This directly falsifies the map/item-callback hypothesis for the observed `cecf40` hits. They belong to a UI/status/performance text update path, or a closely related model path, not authoritative world-map mutation evidence.

## Corrected conclusions

### PROVEN

- Fresh in-world Track A sessions can survive the current bounded post-login observer during controlled experiments.
- One real one-tile player movement did not hit `+0xcecc70` or `+0xcecf40`.
- The observed two later hits were both `+0xcecf40`.
- The live `cecf40` event payload includes `Low lag (147 ms)` and an FPS-style text payload.
- Therefore these observed `cecf40` hits are not evidence of item placement, map mutation, player position, or OTBM state.

### REJECTED HYPOTHESES

- `+0xcecf40` is established as a map/item callback because two hits appeared after an earlier manual item placement: **rejected**. Temporal correlation was coincidental; fresh-session object contents identify status/performance text updates.
- `event+0x18` is a simple `x,y,z` structure: **rejected** by direct live memory values.
- the controlled adjacent drag moved an item: **rejected** by direct frame inspection.

### UNKNOWN

- The actual current official-client world-map mutation callback(s).
- Authoritative structural player coordinates.
- Structural add/remove/move item records.
- Whether the historical Worldmap decoder target remains valid in this exact current client build.

## Exactly one next action

Return to the historical Worldmap decode/call-chain evidence and derive a new exact-build candidate set from functions that consume or emit real tile-position records. Do not use `+0xcecc70` / `+0xcecf40` as map evidence again unless new independent evidence changes their classification.
