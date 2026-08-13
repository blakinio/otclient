# Track A official Linux Tibia — live-session login and research handover (2026-08-13)

## Scope

This report persists the material findings from the 2026-08-13 owner session for **Track A / `official-client-re`**, whose subject is the official native Linux Tibia client.

Canonical track mapping is defined by `docs/agents/TIBIA_RESEARCH_TRACKS.md`:

```text
Track A = official native Linux Tibia client reverse engineering
Track B = native Linux blakinio/otclient -> Tibia Global compatibility
```

This report is a durable handover, not authority to access secrets or mutate another track. Current canonical runtime work must use `blakinio/otclient`, `synology-otclient-01`, and a Track A-owned isolated namespace. Historical external runner/container state is not a continuation dependency.

## Claim vocabulary

- `PROVEN`: already backed by repository-owned canonical evidence or a directly verified deterministic result.
- `DERIVED`: mechanically inferred from proven facts but not directly observed as the target semantic fact.
- `OWNER_OBSERVED`: supplied by the owner during the live session; useful but not yet repository-runtime proof.
- `REVALIDATION_REQUIRED`: historically successful procedure/fact that must be reproduced on the canonical OTClient runner before reuse as current-runtime evidence.
- `UNKNOWN`: not established.

## Session recovery / login procedure that succeeded

Status: `REVALIDATION_REQUIRED` on `synology-otclient-01`.

The successful historical sequence was:

1. Use the **official native Linux Tibia client only**. Do not substitute Wine/Proton or another platform.
2. Start inside a task-owned Linux GUI namespace with a dedicated X display. The successful setup used Xvfb and selected the largest visible window titled `Tibia`.
3. Before login, verify that the task-owned SOCKS/WARP path is healthy. The historical procedure checked WARP through the SOCKS endpoint and required `warp=on`.
4. Launch the official client through `proxychains4` using the task-owned SOCKS configuration. Do **not** start the client under GDB for normal login/session recovery; previous evidence rejected that as the preferred path.
5. Supply account credentials only from protected runtime secrets/environment injection. Never persist or print the email, password, session tokens, cookies, or secret values.
6. Use GUI automation only for the login UI itself:
   - focus the email field;
   - select-all and type the injected email;
   - focus the password field;
   - select-all and type the injected password;
   - activate the login button;
   - immediately unset the credential variables inside the shell used for the login step.
7. Wait for the character-selection screen.
8. The successful historical workflow used OCR **only to locate safe character-selection anchors/row geometry**, not to read in-game world state. It detected the first full character row from labels such as `Character` and `Status`, clicked that row, then sent `Return`.
9. After `Return`, verify session progression at several bounded intervals rather than assuming success from the keypress.
10. Verify network confinement for the official client PID:
    - at least one active TCP connection to the task-owned local SOCKS endpoint;
    - zero direct TCP connections from the client;
    - zero client UDP connections.
11. Reject the result if the final screen is still `Select Character`, has returned to `Account Login`, or shows a login/connection error.
12. Confirm in-world state with an observable game-world transition. Historical proof used a bounded movement action and a changed central viewport, while preserving SOCKS-only transport.
13. Leave the client running only if the task explicitly owns the runtime and a durable checkpoint records the process/session ownership.

### Important correction about OCR

The 2026-08-13 discussion initially described the login flow too broadly as "without OCR". That is not exact. The successful historical workflow did use Tesseract on the **character-selection screen to locate row geometry**. Structural world-state and Worldmap research did not rely on OCR. Future documentation must preserve this distinction.

### Minimal success criteria for a canonical re-run

A future `synology-otclient-01` re-run should not claim successful physical world entry until all of the following are directly verified in the Track A namespace:

```text
official native Linux client process alive
WARP/SOCKS path verified
no direct client TCP
no client UDP
character activation leaves the selection/login UI
structural or independently observable in-world state exists
client/session survives the proof action
```

A socket existing by itself is insufficient evidence of `IN_GAME`.

## Decoded Worldmap status

`PROVEN` for the exact historical researched Linux binary/version boundary already indexed in `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md`:

- decoded map records include real `(x,y,z)` coordinates;
- one coordinate may contain multiple ordered contents;
- at least floors `z=6` and `z=7` were observed;
- an observed capture produced 83 decoded records;
- a normalized model such as `WorldTile{x,y,z,ordered_contents[]}` is supported by the observed structure.

`UNKNOWN`:

- semantic identity of `raw28`;
- semantic identity of `raw30`;
- complete static/dynamic classification;
- complete ground/item/creature classification from those fields alone;
- full appearance -> OTB mapping;
- complete global OTBM coverage.

Do not promote `raw30` to an appearance/type ID without direct proof.

## Native action status

`PROVEN` for the exact researched Linux binary/version boundary already indexed in the canonical state report:

```text
GoNorth      0xee2cd0
GoEast       0xee2d50
GoSouth      0xee2dd0
GoWest       0xee2e50
GoNorthEast  0xee2ed0
GoSouthEast  0xee2f50
GoSouthWest  0xee2fd0
GoNorthWest  0xee3050
Stop         0xee30d0
Cancel       0xee3150
RotateNorth  0xee31d0
RotateEast   0xee3250
RotateSouth  0xee32d0
RotateWest   0xee3350
```

Direct internal calls to rotation and east/west movement were previously shown to return successfully without keyboard/mouse control of the action itself, while the client/session survived and remained SOCKS-confined.

`UNKNOWN`:

- authoritative exact server-accepted coordinate delta for every direct call;
- complete live ABI for attack/follow/use/move-object/talk/container families;
- stable non-GDB production-quality bridge for all action families.

## Additional downstream message-path findings from 2026-08-13

Status: `REVALIDATION_REQUIRED` against the exact current official-client SHA.

Static analysis during the session narrowed the rotation path further:

```text
sendRotateEast wrapper: 0xee3250
movement/action metacall lead: 0xd1a920
string "prepareAndEnqueueGameclientMessage": 0x1cd0b47
"GameclientMessageRotateEast" string/type-name occurrences included:
  0x1cb53b2
  0x1cd1218
  0x1cc2d00
```

Claim boundary:

- `0x1cd0b47` is a **string location**, not a proven function entry point;
- these offsets are exact-binary/version-fenced leads only;
- do not reuse them until the current official-client SHA is reverified and relocation/profile resolution is performed.

The intended next proof remains:

```text
native RotateEast
  -> concrete GameclientMessageRotateEast instance
  -> prepare/enqueue path
  -> protocol writer/framing
  -> outbound session
  -> decoded state confirmation
```

Use a short bounded attach/hook only after static xrefs identify the exact function, because long invasive attaches previously endangered session continuity.

## Position and pathing findings from the live session

`OWNER_OBSERVED`:

The owner corrected the post-movement position to:

```json
{"x": 32554, "y": 32512, "z": 7}
```

The attempted route had advanced until the character encountered a blocking object near a barrel/lantern area. Repeated `Right` commands then no longer implied successful coordinate changes.

The owner later requested return to:

```json
{"x": 32554, "y": 32517, "z": 7}
```

A five-step south command sequence was prepared for that geometric delta, but exact canonical Track A position must be re-read structurally on the OTClient-owned runtime before using either coordinate as current state.

### Pathing rule derived from the collision

`DERIVED`:

A reliable controller must not treat "command sent" as "movement succeeded". Movement should be closed-loop:

```text
read authoritative XYZ
-> select one adjacent traversable tile
-> issue exactly one movement action
-> re-read authoritative XYZ
-> if unchanged, classify collision/rejection
-> replan
-> repeat
```

Do not queue long blind directional sequences when the map contains unverified collision geometry.

## Passive nearby-action logging experiment

The session attempted to prepare a passive observer for actions performed by another nearby character. The intended observer design was:

```text
no observer-generated movement
timestamped decoded Worldmap records
session/SOCKS activity counters
later correlation against decoded GameState/protocol event families
```

`UNKNOWN / NOT PROVEN`:

- no complete canonical nearby-action event capture was obtained;
- Worldmap alone is insufficient for actions that do not modify map contents, including some speech/spell/effect/state events;
- a complete observer must cover decoded GameState/protocol events in addition to Worldmap.

Do not claim that arbitrary nearby-character actions are currently decoded.

## Runner and runtime boundary

Current canonical Track A runner from repository governance:

```text
synology-otclient-01
```

Every future live task must own a unique namespace for its containers/processes/state/X display/ports and must not interfere with Track B.

Historical external runner names, containers, displays, ports, PIDs, heap addresses and task state are intentionally not made active continuation dependencies by this report.

## Security and secret-handling rules

- Never commit Tibia credentials, session tokens, cookies or protected account data.
- Secret names/references may be documented; secret values may not.
- Never log credential-bearing screenshots or OCR output.
- Mask or crop proof screenshots before publishing artifacts.
- WARP/SOCKS confinement must be verified before and after invasive runtime work.
- Do not use the owner's Codex/OpenAI/API quota or credentials without explicit per-use authorization.

## Rejected assumptions / do not repeat

```text
- Track A is the OTClient-to-Global lane. (False; that is Track B.)
- A successful keypress proves successful world movement. (False.)
- Socket existence alone proves IN_GAME. (False.)
- Socket byte deltas alone prove an exact coordinate move. (False.)
- raw30 is already a proven appearance/type ID. (False.)
- 0x1cd0b47 is the entry point of prepareAndEnqueueGameclientMessage. (False; it is a string location.)
- the historical login flow used no OCR at all. (False; OCR was used to locate the character row.)
- long GDB attach is the preferred login/runtime-observation mechanism. (False.)
```

## Exact next action

On `synology-otclient-01`, under a fresh Track A-owned isolated namespace:

1. verify the current official Linux Tibia client version and SHA;
2. resolve the exact-version relocation/profile through the repository-owned bridge tooling;
3. reproduce the login/session-recovery procedure above without persisting secrets;
4. prove structural `IN_GAME` and read authoritative player position;
5. prove one reversible single-tile movement with structural before/after XYZ;
6. then correlate one native rotation with its exact `GameclientMessageRotateEast` enqueue/writer path.

Only after these gates should the session expand to attack/follow/use/chat/container ABI or OTBM semantic extraction.
