# Track A read-only runtime bridge — accepted bounded evidence

Source PR: `#283`
Source branch: `feat/OTC-20260813-tibia-runtime-bridge`
Source final head at coordinator review: `d93ccb34f66af7d3198a50a46e706b4f902ae637`
Validated implementation head: `89e13819e6f53026b831b7e8e4c8fab228d1626c`
Coordinator disposition: `ACCEPT` for the bounded read-only bridge implementation only
Programme classification: `P1 PARTIAL / NOT COMPLETE`
Track: `official-client-re`
Subject: official native Linux Tibia client only

## Exact client fence

```text
version mapping: 15.32.df7b29
size: 51965216
SHA-256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Accepted implementation surface

The source implements a reusable non-GDB, fail-closed, read-only integration boundary:

- launcher exact-SHA/profile fencing before injection;
- `LD_PRELOAD` helper without permanent CipSoft file modification;
- dynamic executable PIE-base discovery;
- owner-only Unix-domain IPC socket (`0600`);
- bounded JSON IPC client;
- read-only `PING`;
- read-only `DISCOVER <target>`;
- derived `session-status` candidate;
- current-process readable/writable-map vptr discovery;
- expected Qt-class validation for QObject-compatible candidates;
- Qt-sensitive discovery marshalled to the real Qt application thread;
- relocation-aware ELF resolver for primary-vptr rediscovery on the exact binary.

No gameplay write/action command is accepted or implemented by this slice.

## Exact profile evidence

Recorded relocation-aware run:

```yaml
run: 31654434331
job: 94305639119
result: PASS
```

Recovered exact-binary primary vptrs include:

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

The committed bridge profile exposes seven discovery targets: player protocol handler, worldmap handler, gameserver game session, player data, container storage, creature storage and game client. Every target is fenced to the exact client digest.

## Exact implementation validation

Recorded exact implementation validation:

```yaml
run: 31654823776
job: 94306874981
validated_head: 89e13819e6f53026b831b7e8e4c8fab228d1626c
focused_tests: 12 PASS
python_compile: PASS
standalone_qt_bridge_build: PASS
complete_official_runtime_layout: VERIFIED
profile_rediscovery_match: true
bridge_socket_mode: 0600
exact_client_no_credential_e2e: PASS
```

The exact client remained alive through the no-credential bridge E2E.

Logged-out `session-status` failed closed:

```yaml
in_game_candidate: false
evidence_level: DERIVED_UNTIL_LIVE_CORRELATION
player_protocol_handler.validated_hits: 0
gameserver_game_session.validated_hits: 0
worldmap_handler.validated_hits: 0
```

This is positive fail-closed evidence. It is **not** proof that those markers are authoritative while logged into a world.

## Current source-head relationship

Coordinator compare of `89e13819... -> d93ccb34...` proves:

```yaml
status: ahead
commits_after_validated_code: 2
changed_files:
  - docs/agents/tasks/active/OTC-20260813-tibia-runtime-bridge.md
product_tool_test_delta: none
```

Therefore the product/tool/test blobs on source head `d93ccb34...` are exactly the implementation exercised at `89e13819...`.

Final source repository CI:

```yaml
head: d93ccb34f66af7d3198a50a46e706b4f902ae637
run: 31680615776
conclusion: success
unresolved_review_threads: 0
```

## Accepted evidence classes

### FACT

- exact-SHA launcher/profile fencing exists;
- dynamic PIE-base discovery exists;
- owner-only `0600` local IPC exists;
- bridge operations in this slice are read-only;
- Qt-sensitive discovery is marshalled to the client Qt event thread;
- relocation-aware primary-vptr rediscovery is implemented and validated against the exact researched binary;
- logged-out marker discovery returns zero validated hits and fails closed;
- exact implementation head passed its recorded focused/build/runtime E2E evidence;
- current source head contains no product/tool/test delta from that validated implementation.

### DERIVED

- `session-status` is only a structural candidate until correlated with independently decoded structural world state in a live exact-build session.

### UNKNOWN

- authoritative live `IN_GAME` semantics of `session-status`;
- authoritative standalone player position through the bridge;
- marker lifecycle across logout/relogin/restart;
- complete health/recovery semantics;
- every gameplay write/action ABI and action parity;
- A3/A4 action gates.

## Current consumers

- P0 Draft PR `#302` may use the exact profile/type leads without owning bridge paths.
- RUNTIME Draft PR `#303` may validate fresh restart/relogin/reacquisition without treating this file as live-session proof.
- Coordinator PR `#300` integrates the accepted immutable bridge implementation on current main after releasing source-branch ownership.

Any later write API requires new separately gated evidence. A successful function call, socket write or keypress is not action parity.
