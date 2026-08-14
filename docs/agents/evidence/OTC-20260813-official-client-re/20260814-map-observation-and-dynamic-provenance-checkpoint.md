# Track A map observation and dynamic provenance checkpoint — 2026-08-14

## Scope and authority

Repository: `blakinio/otclient`
Track: Track A / `official-client-re` (official native Linux Tibia client reverse engineering)
Runner: `synology-otclient-01`
Branch: `ci/OTC-20260813-official-client-re-continuation`
Checkpoint parent head: `41f9ad55618230fadd40d33bbf429cd18146f4a5`
Canonical predecessor: `docs/agents/evidence/OTC-20260813-official-client-re/20260813-canonical-artifact-correction.md`

This document is a durable continuation checkpoint for the runtime experiments performed after the 2026-08-13 canonical world-entry recovery. It records direct runtime observations separately from derived conclusions and open hypotheses. It contains no credentials, account identifiers, session tokens, cookies, or proprietary client bytes.

## PROVEN — runtime identity and login recipe remains valid

The runtime used throughout these experiments was the official Linux child client:

```text
path: /work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
Track marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
display: :98
WARP SOCKS endpoint: 127.0.0.1:25354
```

The successful login path is still the existing workflow:

```text
.github/workflows/tibia-official-client-re-software-world-login.yml
workflow id: 333784548
```

After the 2026-08-14 server save, a full restart/login was performed again instead of assuming a surviving process implied an in-world session:

```text
run: 31730884814
attempt: 12
job: 94711492400
conclusion: success
artifact: track-a-software-world-login
artifact_id: 9212294068
artifact_zip_sha256: dcfbb4e4a17a6199593c7b52fddb04733c4f86ef82d29e9e7d0cd55b8eb2d075
```

The workflow explicitly killed the previous owned client before starting a new one, cleared only the Track A-owned crashdump, launched the exact expected child client, submitted credentials from GitHub Actions secrets, selected the first character and captured the world frame. The final markers were:

```text
TRACK_A_WARP_VERIFIED=true
TRACK_A_OWNED_CRASHDUMP_CLEARED=true
TRACK_A_SOFTWARE_BACKEND_CLIENT_RUNNING=true
TRACK_A_KNOWN_GOOD_LOGIN_CLICK_SENT=true
TRACK_A_POST_LOGIN_CHANGED_PIXELS=319462
TRACK_A_FIRST_CHARACTER_ACTIVATION_SENT=true
TRACK_A_WORLD_CHANGED_PIXELS=660145
TRACK_A_LOCAL_SOCKS_ESTABLISHED=7
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

The canonical artifact-correction document remains authoritative for why changed-pixel markers alone are insufficient. World-entry claims must continue to be grounded by the known-good recovered path and captured in-world evidence.

## PROVEN — visible viewport and structural aware range are different

The visible game viewport was measured independently from structural map-description behavior.

Render movement evidence established an 11-row vertical game view with 32 px tiles:

```text
visible vertical map change span: 352 px
352 / 32 = 11 visible tile rows
```

Together with the known horizontal rendered grid measured during the same Track A experiments, the visible viewport is:

```text
15 x 11 = 165 visible tiles
```

The structural aware range for the player's current floor was then measured using controlled one-tile moves and decoded map records. The decisive run was:

```text
run: 31778752897
job: 94699702072
commit: 824b1ad1e1026255f9f976c49aea8c1c98a1aa8e
message: test(runtime): verify aware strip dimensions per floor
conclusion: success
```

For `z=7` the newly delivered strip for each single-tile move was:

```text
RIGHT: X_SPAN=1,  Y_SPAN=14, UNIQUE_XY=14
LEFT:  X_SPAN=1,  Y_SPAN=14, UNIQUE_XY=14
UP:    X_SPAN=18, Y_SPAN=1,  UNIQUE_XY=18
DOWN:  X_SPAN=18, Y_SPAN=1,  UNIQUE_XY=18
```

Therefore the directly measured current-floor aware rectangle is:

```text
18 x 14 = 252 tile positions
```

This is not an OTClient assumption; it was measured from records produced by the official Linux client.

The same run also observed partial records on `z=6` while the player was on `z=7`, for example:

```text
RIGHT z=6:  1 x 7 unique XY
LEFT  z=6:  1 x 13 unique XY
UP    z=6:  8 x 1 unique XY
DOWN  z=6: 10 x 1 unique XY
```

The partial adjacent-floor shapes must not be promoted to a full-floor aware rectangle without additional evidence.

## PROVEN — structural records can be decoded without OCR

A stable post-login runtime breakpoint used in these experiments was PIE-relative:

```text
+0x19a8ea3
```

At that point the following fields were decoded from the official process during map-description activity:

```text
x
y
z
stack/order
object pointer candidate (RBX)
type_id candidate from object + 0x30
```

The practical record format used by the later probes was:

```text
timestamp_ns x y z stack_order type_id
```

The baseline provenance run directly demonstrates that this produced structured IDs rather than OCR output:

```text
run: 31780838255
job: 94706054275
commit: b8c92674162072bd8995cc7c9a62e8f59b06267e
conclusion: success
movement: Right -> Down -> Left -> Up
TRACK_A_BASELINE_RECORDS=168
TRACK_A_BASELINE_CANONICAL_ROWS=168
TRACK_A_BASELINE_Z_VALUES=6,7
TRACK_A_BASELINE_DISTINCT_TYPE_IDS=59
TRACK_A_BASELINE_ITEM_SCAN_PROVEN=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

The 59 observed `type_id` values were:

```text
231,486,618,738,870,1168,1169,1170,1171,1173,1174,1281,1635,2317,2319,2323,
2445,2535,3615,3681,3687,3892,3907,4515,4516,4518,4521,4523,4525,4527,4528,
4529,4530,4532,4533,4536,4540,4598,4599,4600,4601,4602,4622,4633,4635,4639,
4643,5416,6216,6218,6370,6374,6378,6379,19394,20661,34336,34376,34395
```

The object field at `RBX+0x30` is therefore a strong runtime candidate for a stable type identifier in this exact client build. It remains an ABI-specific observation and must be revalidated if the official child binary SHA changes.

## PROVEN — the `+0x19a8ea3` hook is a map-description/strip hook, not a general dynamic-tile event hook

A controlled provenance experiment was performed with help from a second player character. The purpose was to test whether an item placed on an already-visible tile would appear in the records captured by the existing structural breakpoint.

Baseline:

```text
run: 31780838255
records: 168
z values: 6,7
distinct type IDs: 59
movement: Right -> Down -> Left -> Up
```

The external player then placed an item near the observed character. The post-drop workflow was:

```text
run: 31780927846
commit: bf6b7665114a100c4f2b5d1f96f07a592b429101
message: test(runtime): capture post-drop provenance scan
conclusion: success
```

The repeated scan produced no added/removed record relative to the baseline for the captured rows. This falsified the working assumption that simply moving around while attached to `+0x19a8ea3` would expose a dynamic item mutation on an already-aware tile.

A second strategy forced a larger aware-range reload (`12 x Right`, then `12 x Left`) and preserved a WITH_ITEM dataset:

```text
WITH_ITEM records: 209
WITH_ITEM dataset sha256: 172fbd1d7277ee8decb5606d58bd79fa89cdca2688b85743a7e3dc6554b1e677
TRACK_A_WITH_ITEM_DATASET_PRESERVED=true
```

After the external item was moved, an equivalent reload was compared. On the 123 common tile coordinates the stack content was unchanged (`removed=0`, `added=0`). The larger reload did expose additional world strips, but still did not isolate the user-controlled dynamic item.

Conclusion supported by these experiments:

```text
+0x19a8ea3 is useful for map description / newly entering aware strips.
It is not sufficient as the sole observer for CreateOnMap/ChangeOnMap/DeleteOnMap-style
mutations occurring on tiles already inside the aware range.
```

## PROVEN — provenance cannot be inferred from one static `(x,y,z,stack,type_id)` snapshot

The experiments establish a hard design requirement for OTBM reconstruction:

```text
"client currently contains this type_id at this tile" != "this is canonical map content"
```

A single structural snapshot cannot by itself distinguish all of:

- fixed map decoration,
- movable item present since before observation,
- item dropped by a player,
- corpse,
- creature/player/NPC representation,
- temporary effect,
- transformed map object.

Canonical reconstruction therefore requires an event/history layer in addition to snapshot data.

Recommended data model for future probes:

```text
(x, y, z, stack_order, type_id, object_class, event_type, provenance, first_seen, last_seen)
```

Recommended provenance classes:

```text
STATIC_CONFIRMED
STATIC_PROBABLE
DYNAMIC_ITEM
PLAYER_DROPPED
CREATURE
PLAYER
NPC
CORPSE
TEMP_EFFECT
PROJECTILE
TRANSIENT_UNKNOWN
```

No dynamic/transient class should be written automatically into canonical OTBM.

## PROVEN — early GDB attach is unsafe for this research lane

An attempt to attach GDB before the character entered the world caused the official client to abort after BattlEye initialization (`SIGABRT`). No attempt was made to bypass or disable BattlEye.

Policy resulting from the observation:

```text
Do not use early/pre-world GDB attach.
Do not bypass, patch or disable BattlEye.
Use post-login/read-only observation only where the client remains stable.
```

This also means the complete initial map-description floor set was not directly captured by early GDB.

## DERIVED — floor model from protocol/source behavior

Runtime movement directly observed `z=6` and `z=7` in the current surface session.

The compatible protocol implementation in this repository uses the following map-description model:

```text
seaFloor = 7
maxZ = 15
awareUndergroundFloorRange = 2
surface map description: floors 7 down to 0
underground map description: z-2 through z+2, clipped to valid Z range
```

This protocol/source model is useful for experiment design, but the statement that the official client simultaneously materializes every one of those floors in an equivalent in-memory representation remains DERIVED rather than directly proven by the aborted early-GDB experiment.

## PROVEN — reverse-engineering narrowed the map movement and dynamic mutation paths

Analysis of the working strip breakpoint showed that its callers belong to the map movement/map-description path. Four nearby movement handlers were identified around:

```text
+cdbad0
+cdbb40
+cdbbb0
+cdbc20
```

They call the same map-description routine around:

```text
+0x19a8a80
```

This explains why the old observer is effective for newly revealed strips but not for arbitrary dynamic tile mutations.

Subsequent static disassembly and Qt meta-dispatch analysis was persisted through a sequence of `tibia-official-client-re-session-sockets.yml` experiments. The latest completed classification before this checkpoint was:

```text
run: 31782222154
job: 94710283300
commit: 41f9ad55618230fadd40d33bbf429cd18146f4a5
message: test(runtime): classify adjacent dynamic map callback targets
conclusion: success
```

The current strongest dynamic-mutation candidates are:

```text
+0xcecc70
+0xcecf40
```

Why they are candidates:

- they operate on object/thing-like structures rather than only rectangle strip coordinates;
- they read stack/index-like fields;
- they construct/copy position/object state and invoke mutation-like virtual callbacks;
- they are adjacent to the map-related meta-dispatch region found during the analysis.

This is still a HYPOTHESIS regarding their exact semantic names. They have not yet been directly correlated with a controlled external add/change/remove event.

Other adjacent targets were disassembled and rejected or deprioritized when their behavior matched unrelated UI/color/object handling rather than a clear dynamic map mutation path.

## UNKNOWN — exact mapping of dynamic callbacks

The following are not yet proven for the official client:

```text
CreateOnMap -> exact binary handler
ChangeOnMap -> exact binary handler
DeleteOnMap -> exact binary handler
MoveCreature -> exact binary handler
corpse creation/decay callback path
effect/projectile callback path
```

The next experiment must correlate runtime breakpoint hits with one controlled world mutation, rather than assigning names from static disassembly alone.

## Next controlled experiment

Precondition:

1. verify the current owned client is actually in-world; a live PID alone is insufficient;
2. after server save/logout/crash, perform the canonical full restart/login path;
3. attach only after world entry;
4. verify the observer is active and the client remains stable before asking the owner to modify the world.

Arm post-login runtime breakpoints on at least:

```text
+0xcecc70
+0xcecf40
```

and, if necessary, their immediate map-meta-dispatch neighbors.

For every hit record at minimum:

```text
timestamp_ns
handler PIE-relative offset
x/y/z candidates
stack/index candidate
thing/object pointer candidate
type_id candidate
relevant register snapshot
```

Only after the observer is proven armed, ask the owner to perform exactly one controlled action from a second character, preferably moving one known item from one adjacent tile to another. Correlate the event timestamp with handler hits.

The acceptance target for this phase is a directly observed event that provides:

```text
add/change/remove semantic class
x
y
z
stack position
type_id or equivalent stable object type
```

Once one event is proven, repeat for add, remove and move, then extend to creature movement, death/corpse, corpse decay and temporary effects.

## OTBM reconstruction consequence

The current research already supports a safer map-reconstruction architecture:

```text
STRUCTURAL STRIP OBSERVER
  -> discovers coordinates and object stacks for newly entering aware tiles

DYNAMIC EVENT OBSERVER (still under investigation)
  -> records add/change/remove/move events inside the already-aware region

PROVENANCE ENGINE
  -> maintains history/confidence/classification

CANONICAL OTBM WRITER
  -> consumes only canonical/static-qualified state
```

The canonical writer must never directly consume every object observed in the official client's world state.

## Current claim state

```yaml
OFFICIAL_CLIENT_SHA256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
RUNNER: synology-otclient-01
WORLD_LOGIN_AFTER_20260814_SERVER_SAVE: PROVEN_BY_RUN_31730884814_ATTEMPT_12
WORLD_SCREEN_ARTIFACT_AFTER_SERVER_SAVE: 9212294068
VISIBLE_VIEWPORT: PROVEN_15x11
CURRENT_FLOOR_AWARE_RANGE: PROVEN_18x14
STRUCTURAL_MAP_RECORDS: PROVEN
STRUCTURAL_RECORD_FIELDS: PROVEN_X_Y_Z_STACK_AND_TYPE_ID_CANDIDATE
TYPE_ID_FIELD_FOR_THIS_BINARY: STRONG_CANDIDATE_RBX_PLUS_0x30
OBSERVED_RUNTIME_Z_VALUES: PROVEN_6_7
FULL_SIMULTANEOUS_Z_SET: UNKNOWN
OLD_BREAKPOINT_0x19a8ea3_ROLE: PROVEN_MAP_DESCRIPTION_OR_STRIP_PATH
DYNAMIC_CREATE_CHANGE_DELETE_HANDLERS: UNKNOWN
DYNAMIC_HANDLER_CANDIDATES: 0xcecc70,0xcecf40
STATIC_VS_DYNAMIC_FROM_SINGLE_SNAPSHOT: NOT_PROVEN_AND_NOT_SUFFICIENT
OTBM_PROVENANCE_LAYER_REQUIRED: DERIVED_FROM_CONTROLLED_EXPERIMENTS
```

## Exactly one next action

Arm a stable post-login runtime observer on `+0xcecc70`, `+0xcecf40` and the minimum adjacent candidate set, prove it is active, then correlate exactly one owner-controlled item move with the resulting handler hits before assigning Create/Change/Delete semantics.
