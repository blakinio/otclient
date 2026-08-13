# OTCLIENT-TIBIA-RE canonical state and imported evidence

## Purpose

This report consolidates the material official Linux Tibia reverse-engineering evidence needed by `OTCLIENT-TIBIA-RE` into `blakinio/otclient` so future workers do not depend on an active Oteryn-Platform runtime or on chat history.

External source repositories remain read-only provenance. This report copies facts/claim boundaries, not proprietary client bytes, credentials or secret-bearing traces.

## Canonical programme location

```yaml
repository: blakinio/otclient
alias_registry: docs/agents/SHORT_COMMANDS.md
canonical_prompt: docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
base_programme_prompt: docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
canonical_runner_name: synology-otclient-01
migration_runner_selector: [self-hosted, otclient, synology]
canonical_state_dir: /home/runner/_work/_otclient_tibia_re_state
```

New live execution must not depend on `oteryn-staging`, `oteryn-synology-staging`, `oteryn-tibia-client-analysis` or `/var/lib/oteryn-staging-state/**`.

## Current OTClient work inventory

Revalidate exact heads/status before use.

### PR #48 — official-client runtime/live evidence

Purpose:
- login/recovery and structural `IN_GAME` work;
- exact client/runtime reconstruction;
- WARP confinement;
- static protocol/action/state catalogues;
- live experimentation and migration to the dedicated OTClient runner.

Durable task:

```text
docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md
```

Important researched client identity:

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

This identity is historical/current-at-proof only. A later current-client identity probe failed before producing a hash, so current upstream identity remains `UNKNOWN` until reverified.

### PR #279 — worldmap/OTBM reconstruction

Purpose:
- deterministic observation/schema pipeline;
- static/dynamic separation;
- explicit appearance and client->OTB mapping evidence;
- fail-closed comparison and OTBM-ready plan generation.

Fresh audit found and repaired a forged-snapshot fail-open path. Focused repaired suite passed 19/19 tests and synthetic `reconstruct -> compare -> plan-otbm` E2E. Final workflow-free repository CI run `31653805958`, including `CI / Required` job `94315480522`, completed successfully.

### PR #280 — dedicated Synology runners

Purpose:
- repository-level `synology-otclient-01` and `synology-ots-01` runners;
- isolated runner state/work volumes;
- no Docker socket/privileged mode;
- OTClient-specific `otclient-tibia-re` image target with official-client RE runtime/debug dependencies;
- canonical OTClient programme execution without Oteryn runner dependencies.

After redeploy the OTClient runner labels include `tibia-re`; during migration `[self-hosted, otclient, synology]` remains the bootstrap selector.

### PR #283 — stable runtime bridge

Purpose:
- exact-SHA-fenced launcher;
- `LD_PRELOAD` Qt helper;
- dynamic PIE-base resolution;
- mode-0600 Unix-domain IPC;
- read-only `PING`, `DISCOVER`, and derived session-status operations;
- relocation-aware primary-vptr resolver.

Exact-client no-credential E2E on bridge head `39ff79ac44a0a1010b4bcc8b8e3617525353df7e` passed run `31654701845`, job `94306484551`:

```text
11 focused tests PASS
BRIDGE_STANDALONE_BUILD_PASS=true
COMPLETE_OFFICIAL_RUNTIME_LAYOUT_VERIFIED=true
EXACT_BRIDGE_VALIDATION_RUNTIME_READY=true
BRIDGE_SOCKET_MODE=600
EXACT_CLIENT_BRIDGE_E2E_PASS=true
```

Logged-out state returned zero session-marker hits and `in_game_candidate=false`, which is correct fail-closed behavior. Live marker correlation remains unproven.

## Imported historical evidence — decoded Worldmap

Source provenance (read-only):

```yaml
repository: blakinio/Oteryn-Platform
branch: ops/oteryn-tibia-client-analysis-20260811
report: docs/agents/reports/OTERYN-20260812-live-worldmap-capture.md
capture_run: 31632627071
capture_job: 94234965002
capture_commit: 76098dc280fce2c38eeb1ce017247bdf77a8cb1e
historical_runner: oteryn-synology-staging
historical_container: oteryn-tibia-client-analysis
```

PROVEN in that exact historical runtime:

```text
DECODED_CAPTURE_RECORD_COUNT=83
ACTIVE_LOCAL_SOCKS_COUNT=2
ACTIVE_DIRECT_TCP_COUNT=0
LIVE_SESSION_RETAINED=true
LIVE_DECODED_WORLDMAP_CAPTURE_PROVEN=true
```

Static/runtime boundary for that exact researched binary/process:

```text
static common-map capture point: 0x19a8ea3
historical PIE base: 0x564bf7949000
historical runtime breakpoint: 0x564bf92f1ea3
```

The transient PID/PIE/runtime address must never be reused. The static offset is only a lead after exact current SHA revalidation.

Representative structural facts:
- real `(x,y,z)` coordinates were decoded;
- multiple ordered contents existed on one coordinate;
- records covered at least floors `z=6` and `z=7`;
- a normalized `WorldTile{x,y,z,ordered_contents[]}` model is supported by observed structure.

Claim boundary:
- `raw30` carried stable decoded numeric values, but its semantic identity as appearance/type/other generated field was not proven;
- `raw28=1` was observed but semantic name remained unknown;
- static/dynamic, ground/item, pathability and full OTBM attributes remained unknown;
- 83 live records do not prove complete global-map coverage.

## Imported historical evidence — native action path

Source provenance (read-only):

```yaml
repository: blakinio/Oteryn-Platform
branch: ops/oteryn-tibia-client-analysis-20260811
report: docs/agents/reports/OTERYN-20260812-native-client-action-proof.md
pr: 1006
historical_runner: oteryn-synology-staging
historical_container: oteryn-tibia-client-analysis
```

### Live player protocol handler

Run `31638654454`, job `94255291393`, commit `e20325b3b82a0421fa50e3fcc5414990938a01df` proved exactly one live `TPlayerProtocolMessageHandler` object for the researched binary using primary-vptr basis:

```text
static primary vptr offset: 0x308a008
historical runtime vptr: 0x564279c73008
historical live object: 0x56427ebeebe0
candidate count: 1
```

Only the static exact-binary vptr offset is reusable as a version-fenced lead; heap/runtime addresses are transient.

### Movement/rotation method mapping

Exact researched-binary wrappers:

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

Run `31638928121`, job `94256223308`, commit `0274c4ff570285c28b2690779141f24531afc595` validated metadata mapping to the corresponding `GameclientMessage*` types.

### Direct native calls

Run `31639062297`, job `94256667804`, commit `48fd4b73a8f2caf260333681d27d89876a8367e2` proved direct `RotateEast` invocation returned successfully and the client/session survived with two local SOCKS connections and zero direct TCP.

Run `31639224501`, job `94257213013`, commit `04ce5fc9e934d4ea6bb54bf8141d54eeb900318a` proved direct `GoEast` and `GoWest` invocations returned successfully, client survived, WARP confinement remained intact, and the active game SOCKS connection showed traffic deltas during the bounded action interval.

Claim boundary:
- those calls prove GUI-independent internal movement/rotation invocation;
- socket deltas support progression into the active session but do not by themselves prove exact server-accepted coordinate movement;
- authoritative before/after player position was not captured in those action runs;
- GDB was the historical execution mechanism and is not the intended stable API.

### Other action families exposed

The exact researched binary exposed structured outbound families for:

```text
Attack
Follow
UseObject
UseTwoObjects
UseOnCreature
MoveObject
Talk
container close/up/seek/action
```

Argument ABI and live-object ownership were not fully proven for those families. Do not guess arguments.

## OTClient-owned relocation proof

Run `31654434331`, job `94305639119`, reproduced primary-vptr recovery inside `blakinio/otclient` for the exact researched SHA and recovered:

```text
TPlayerProtocolMessageHandler    0x308a008
TWorldmapProtocolMessageHandler  0x30871d8
TGameserverGameSession           0x3078ba0
TGameSessionBase                 0x3084648
IGameSession                     0x30841c0
TPlayerData                      0x308ca70
TContainerStorage                0x308a1a0
TCreatureStorage                 0x308d078
TGameClient                      0x3076908
```

The durable resolver is implemented in PR #283. This supersedes blind raw-qword scanning as the preferred exact-binary recovery method.

## Rejected hypotheses that must not be repeated unchanged

```text
- critical QMetaObjects are missing
- FIRST_CHARACTER_ACTIVATED proves character activation
- absence of a QMeta wrapper breakpoint proves the semantic state did not occur
- starting the client under GDB is the preferred login/world-entry recovery path
- QCoreApplication QObject descendants contain the target Tibia game handlers
- blind raw-qword vptr scanning is a reliable resolver
- socket existence/byte deltas alone prove IN_GAME or successful movement
```

## Current unknowns

```text
- current upstream official-client SHA/version
- current OTClient-owned structural IN_GAME session
- live bridge session-marker correlation
- authoritative player position through the stable bridge/runtime
- authoritative before/after movement transition
- raw28/raw30 semantics
- exact live ABI/action paths for attack/follow/use/move-object/chat/container operations
- complete appearance -> OTB mapping and global OTBM coverage
```

## Canonical continuation order

1. Finish runner migration: validate PR #280 image/Compose, deploy `synology-otclient-01`, and prove a PR #48 job runs there with writable `/home/runner/_work/_otclient_tibia_re_state` and no Oteryn runtime dependency.
2. Reverify current official-client identity through the dedicated OTClient runner.
3. If SHA changed, run the durable PR #283 relocation resolver and create a new exact-version profile before reusing any static offsets.
4. Recover a structural `IN_GAME` session on the OTClient runner.
5. Correlate bridge `session-status` with decoded world state.
6. Read authoritative player position.
7. Prove one reversible movement transition with structural before/after state.
8. Continue capability gates through creatures, inventory/containers, actions, protocol catalogue and OTBM extraction.

External Oteryn runtime is no longer part of this continuation path.
