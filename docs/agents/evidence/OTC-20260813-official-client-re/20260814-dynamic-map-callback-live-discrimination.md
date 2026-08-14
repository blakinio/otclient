# Track A dynamic map callback live discrimination — 2026-08-14

## Scope

Repository: `blakinio/otclient`
Track: `official-client-re` / Track A
Runner: `synology-otclient-01`
Subject: official native Linux Tibia client only

This checkpoint records post-login runtime observations around candidate callbacks at child-client offsets `+0xcecc70` and `+0xcecf40`. The experiments used GDB hardware breakpoints against the already running Track A-owned official client. They did not patch client code, modify BattlEye, bypass BattlEye, inject gameplay packets, or persist account credentials.

## Fresh verified world recovery

The historically credential-capable world-login workflow was re-run after the user reported that the previous session had returned to a logged-out state.

```text
workflow run: 31730884814
run attempt: 13
job: 94716022704
job conclusion: success
artifact: track-a-software-world-login
artifact_id: 9212815415
artifact_zip_digest: sha256:26b92d1e38c9fad9ef6f113ca1b2e4c675f25c477501722dbbaf761864ddb2e0
```

The run reported:

```text
TRACK_A_WARP_VERIFIED=true
TRACK_A_SOFTWARE_BACKEND_CLIENT_RUNNING=true
TRACK_A_KNOWN_GOOD_LOGIN_CLICK_SENT=true
TRACK_A_POST_LOGIN_CHANGED_PIXELS=320319
TRACK_A_FIRST_CHARACTER_ACTIVATION_SENT=true
TRACK_A_WORLD_CHANGED_PIXELS=660118
TRACK_A_LOCAL_SOCKS_ESTABLISHED=7
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

This fresh execution re-established a live Track A world session through the previously verified login recipe.

## Fresh post-login observer

A post-login observer was armed against the fresh client session.

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

A subsequent collector verified that both the client and detached GDB process survived Actions job cleanup and that the initial callback baseline was zero:

```text
collector run: 31783560390
collector job: 94716527251
TRACK_A_DYNAMIC_MAP_OBSERVER_PERSISTENT=true
TRACK_A_DYNAMIC_MAP_EVENT_COUNT=0
```

Therefore the fresh post-login attach itself did not produce hits at either candidate.

## Manual single-item placement observation

Before the fresh-session recovery above, the same observer design had a clean baseline of zero events. The user then performed one externally observed action: placing one item on an adjacent tile. A collector immediately afterwards reported:

```text
collector run: 31783560390
run attempt: 2
collector job: 94714738661
TRACK_A_DYNAMIC_MAP_OBSERVER_PERSISTENT=true
TRACK_A_DYNAMIC_MAP_EVENT_COUNT=2
```

The before-action baseline had been `0`.

This is direct evidence that two candidate breakpoint hits occurred after that real single-item placement window. It is **not** yet sufficient to assign exact semantics to either handler: the collector version used for that attempt tailed a bounded suffix of the GDB log, and BattlEye ELF warning output displaced the exact `EVENT`/`ARG` records from the visible suffix. The later fresh observer re-arm reset the event log, so those two argument records are no longer recoverable from the persistent runtime file.

Do not invent the lost register or argument values.

## Controlled real player movement negative control

A dedicated workflow sent exactly one `Up` key to the verified in-world client while the fresh observer was armed.

```text
workflow: .github/workflows/tibia-official-client-re-controlled-step.yml
run: 31784304719
job: 94716687631
artifact: track-a-controlled-step
artifact_id: 9212883577
artifact_zip_digest: sha256:8099f1685159a4a54a63f05a557940b148645b2a9b55f6b82f11bb319811f736
```

Results:

```text
TRACK_A_CONTROLLED_STEP_SENT=true
TRACK_A_CONTROLLED_STEP_CHANGED_PIXELS=151920
TRACK_A_DYNAMIC_MAP_EVENTS_BEFORE=0
TRACK_A_DYNAMIC_MAP_EVENTS_AFTER=0
TRACK_A_DYNAMIC_MAP_ARGS_BEFORE=0
TRACK_A_DYNAMIC_MAP_ARGS_AFTER=0
```

The before/after XWD frames from artifact `9212883577` were downloaded and directly inspected. They show the normal in-game world before and after a real one-tile player movement; they do not show a logout screen. Thus the fresh post-login GDB attach did not by itself force logout in this trial, and ordinary player movement did not hit either `+0xcecc70` or `+0xcecf40`.

## Controlled drag negative/no-op control

A second workflow attempted exactly one bounded adjacent-tile drag while preserving the same observer.

```text
workflow: .github/workflows/tibia-official-client-re-controlled-item-drag.yml
run: 31784509337
job: 94717325713
artifact: track-a-controlled-item-drag
artifact_id: 9212961464
artifact_zip_digest: sha256:2c278b0fbefe2371916af4b2384d0525e83b87c1e6157a750d3c59c08d0bc81c
```

Results:

```text
TRACK_A_CONTROLLED_ITEM_DRAG_SENT=true
TRACK_A_CONTROLLED_ITEM_DRAG_CHANGED_PIXELS=30760
TRACK_A_DYNAMIC_MAP_EVENTS_BEFORE=0
TRACK_A_DYNAMIC_MAP_EVENTS_AFTER=0
TRACK_A_DYNAMIC_MAP_ARGS_BEFORE=0
TRACK_A_DYNAMIC_MAP_ARGS_AFTER=0
```

The before/after XWD frames from artifact `9212961464` were downloaded and directly inspected. The attempted drag did **not** move a ground item. It only changed the tile hover/selection highlight while ordinary animated world pixels continued changing. This run is therefore a safe UI/no-op negative control, not evidence about successful item movement.

## Current interpretation

### PROVEN

- A fresh recovered in-world official-client session can tolerate the current post-login GDB observer long enough for controlled runtime experiments.
- Fresh observer baseline at `+0xcecc70` / `+0xcecf40` is `0` hits.
- One real one-tile player movement produces a large visual world transition but `0` hits at these two candidates.
- One bounded no-op tile drag also produces `0` hits.
- The earlier real single-item placement window changed the same observer from `0` to `2` hits.

### INFERENCE

The observed discrimination is consistent with `+0xcecc70` / `+0xcecf40` belonging to a map/thing update path that is exercised by a real item placement but not by ordinary player movement or hover-only UI activity. This is an inference, not yet a semantic identification of the functions.

### UNKNOWN

- Which of the two candidate handlers fired for each of the two manual-placement hits.
- Exact register/argument values for those two lost hits.
- Whether the two hits represent source/destination map updates, add/remove callbacks, or another paired operation.
- Authoritative tile coordinates or item identity for the manual placement.
- Structural player position remains unproven by these callback experiments.

## Exactly one next action

Repeat one real, single ground-item placement or movement while the fresh observer is armed, then immediately collect the now-filtered `EVENT`/`ARG` evidence before re-arming or truncating the log. Do not perform additional random UI drags as a substitute for a verified real item mutation.
