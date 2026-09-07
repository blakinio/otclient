# Session release handoff — worldmap causal runtime

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: `#475`  
Release time: `2026-08-18T09:40:00+02:00`  
Release reason: owner requested that the current agent persist its work and release task/runtime ownership so another agent can continue without inheriting a live session or ownership block.

## Disposition

```text
TASK_COMPLETED=false
STRUCTURAL_IN_GAME=NOT_PROVEN
MAP_SCREENSHOT=NOT_PROVEN
CURRENT_AGENT_OWNERSHIP=RELEASED
CURRENT_RUNTIME_AUTHORITY=RELEASED
CURRENT_CREDENTIAL_AUTHORITY=RELEASED
PR_STATE=KEEP_DRAFT
```

This handoff is a checkpoint, not a success claim. No `FullMap + >=10 strips` proof and no accepted post-structural map screenshot exist on the task branch at release.

## Exact client fence

```text
version=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform=official native Linux
```

## Physically proven upstream chain

The following were proven in real exact-client runs and should not be rediscovered from UI coordinates:

```text
LEGITIMATE_ACCOUNT_LOGIN=PASS
POST_LOGIN_TRANSPORT_ACTIVITY=PASS
POST_LOGIN_UI_TRANSITION=PASS
POSTAUTH_CHARACTER_CONTROLLER_PROVENANCE=PASS
NATIVE_CHARACTER_LIST_COUNT=1
NATIVE_SELECTION_INDEX=0
QT_THREAD_AFFINITY_FOR_CHARACTER_CONFIRMATION=PASS
NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS
TCHARACTERLOGINDATA_VECTOR_BEFORE=0
TCHARACTERLOGINDATA_VECTOR_AFTER=1
REQUEST_CHARACTER_LOGIN_SIGNAL=OBSERVED/PROVEN
REQUEST_CHARACTER_GAMESERVER_LOGIN=OBSERVED
```

V18 physical run `32076063134 / 95529595652` is the cleanest character-selection discriminator. It discovered exactly one runtime character model, selected index `0` deterministically from current-session data, invoked `TCharacterSelectionController` QMeta method 11 (`onCharacterSelectionConfirmed`) on the Qt-affine live object, and caused the client itself to build one `TCharacterLoginData` entry (`0 -> 1`).

V19 later established the downstream signal boundary:

```text
RequestCharacterLoginSignal=1
RequestCharacterGameserverLogin=2
StartGameServerLogin=0   # as observed by that generation's state/thunk probes
FullMap=0
```

The account-login and character-selection stages are therefore not the primary blocker anymore.

## Important corrections discovered during the session

1. `Invalid Monk` was imported from user memory and was **not** discovered from this runtime. That assumption was removed. Future character choice must come from the current runtime model/list only.
2. Coordinate/pixel/Tab character selection is closed. V14 bounded candidates did not provide a reliable native transition and should not be revived as the control plane.
3. Historical `0xd47300` was misclassified as a standalone `requestCharacterLogin` entry. It is a QMeta/property-table case, not a safe direct method entry. The successful path is through the controller's real QMeta/static-metacall boundary with a valid live object and argument model.
4. GDB `scheduler-locking on` must be restored to `off` before continuing normal network/session execution. V19 incorporated this correction.
5. Several historical addresses such as `0xcfb122`/`0xd06660` are QMeta cases or thin thunks; real implementation addresses must be used for observation when distinguishing state-entry from dispatch. During this session the following implementation mappings were recovered and used as working discriminators:
   - start-game-login implementation around `0x767440`;
   - connect-existing-credentials implementation `0x6ef1d0`;
   - on-connect-gameserver implementation around `0x6fe480`;
   - session-connected implementation around `0x6ee130`.
   Revalidate exact instruction bytes on any fresh run before invoking anything.

## Later v20-v22 state

Durable authority records exist for v21 and v22:

- `20260818-v21-runtime-authority.md` records `BASELINE_LOGIN_CONSUMED_BEFORE_V21=10` and max 11;
- `20260818-v22-runtime-authority.md` records the conservative `BASELINE_LOGIN_CONSUMED_BEFORE_V22=11` and max 12.

No `map-world-entry-v20.png`, `map-world-entry-v21.png`, or `map-world-entry-v22.png` was present when this release handoff was written. Treat v20-v22 as exploratory continuation generations, not successful completion evidence. A successor must re-read their terminal logs before asserting the final consumed-login count; this release does **not** carry any old login authority forward.

The intended guarded progression in those generations was:

```text
native character confirmation
 -> normal AUTH requestCharacterGameserverLogin propagation
 -> real StartGameServerLogin implementation
 -> real connectClientToGameserverWithExistingCredentials implementation
 -> real onConnectClientToGameserver implementation
 -> server/session logic unchanged
 -> FullMap + >=10 strips
```

They explicitly did not authorize fabricated `SessionConnected`, fabricated login success, synthesized packets, or fabricated auth/session/character payloads.

## VNC / observer result

The browser-observer work proved the task-owned x11vnc/Xvfb path itself can work:

```text
TRACK_A_VNC_LIVE_LOCAL_RFB=PASS
TRACK_A_VNC_LIVE_READY=true
TRACK_A_VNC_LIVE_PORT=6082
TRACK_A_VNC_LIVE_SECRET_USED=false
```

A v23 observer later went black because the helper waited only 180 seconds for the credential FIFO and then cleanup terminated the exact client/Xvfb/x11vnc. v24 (`fix(track-a): keep browser VNC observer alive`) removes that credential timeout only for the no-secret observer mode and holds before login. This VNC work is diagnostic only and is not game-entry evidence.

At release, do not assume any observer session is live. Runtime cleanup is required and the successor must establish a fresh display/session under fresh admission.

## Current-main drift that successor must consume first

The branch is now materially behind newer canonical native-login work on `main`.

Current `main` includes, among others:

- `17cc0dc1bf29c440cc08e443bdce98e4dde7be5d` — PR #505, native cold-auth QMeta entry research;
- `ed6202216886ec31d432e4e7dec56b47626f10c4` — PR #506, archive/release of that task;
- `2e6992da330e8a52d03b94b8d6a9de6fa79a6800` — PR #507, experimental form-less native auth bridge;
- `ed09418b431c28087775b419f85bed404fa85d70` — PR #508, archive/release of the bridge task.

The successor should rebase/re-read current `main` and evaluate the merged form-less native auth bridge before reusing the old UI credential-entry machinery in #475. Do not duplicate already-promoted native-auth work.

## Wider worldmap causal result remains unresolved

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
PATCH_CAUSES_ADDITIONAL_AUTHORITATIVE_MAP_DATA=UNKNOWN
BASELINE_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
PATCHED_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
OUTBOUND_EXTENT_NEGOTIATION_CHANGE=UNKNOWN
STORAGE_EXTENT_CHANGE=UNKNOWN
RENDER_PICKER_EXTENT_CHANGE=UNKNOWN
```

The patched `[19,14]` comparison must not run until a fresh baseline reaches structural `IN_GAME` and produces the authoritative inbound baseline measurements.

## Successor start procedure

1. read current `main` and merged #505-#508 native-auth work;
2. read this handoff, the active/released task record, and v18-v22 runtime evidence/logs;
3. perform a fresh no-client namespace/process inventory on `synology-otclient-01`;
4. acquire fresh task/runtime ownership rather than inheriting this session's authority;
5. use runtime-discovered character data only; do not import a character name from memory;
6. prefer the newly merged native auth bridge where its exact fences apply;
7. retain one-session maximum, WARP/SOCKS confinement, exact-client hash fence, Qt-thread/ABI/object-provenance checks;
8. completion remains exactly `FullMap + >=10 strips + post-structural exact-window screenshot`;
9. only after baseline success perform the single task-owned `[19,14]` patched comparison.

## Release checkpoint

```yaml
checkpoint_version: 40
status: waiting
agent: null
session_id: null
session_role: released
runtime_access: none
runtime_owner_task: null
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
owned_paths: []
pr: 475
pr_state: draft
structural_in_game: false
map_screenshot: false
next_action: successor re-reads current main, consumes merged native-auth bridge work, obtains fresh admission/ownership, and resumes from the post-character-confirmation game-server state-machine boundary
```
