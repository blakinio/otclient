# Official Tibia Runtime Bridge

This tool is the durable read-only bridge/API boundary for `OTCLIENT-TIBIA-RE` P1. The original bounded implementation was accepted from PR #283 and is rebuilt here on current `main`; PR #359 adds deterministic health, reacquisition and recovery semantics without taking live-runtime authority.

## Execution and authority boundary

P1 runs as `github_hosted` with `runtime_access: none`. Repository tests and bridge compilation are allowed; real attach, launch, login/relogin, restart, kill, X11/VNC control, live `/proc` inspection and physical recovery belong to separately admitted RUNTIME work.

The bridge must never infer a canonical target from historical `:98`, RFB `6082`, a PID or a reachable socket. Current canonical identity is usable only when the authoritative runtime registration, current controller generation, fresh Gate B identity and bridge PING agree. Missing or contradictory evidence fails closed.

## Read-only bridge v1

1. `launcher.py` loads a versioned profile and verifies the exact official-client SHA-256 before launch.
2. The launcher injects `otclient-tibia-runtime-bridge.so` with `LD_PRELOAD`; it does not modify installed client files.
3. `bridge.cpp` discovers the executable PIE base at runtime, binds a mode-`0600` Unix-domain socket and accepts bounded local commands.
4. `PING` reports helper/base readiness.
5. `DISCOVER <target>` runs on the client's Qt event-loop thread, scans only readable/writable mappings of the current process for the profile's exact primary-vptr value, applies an object-layout plausibility gate and validates candidate QObject-compatible instances by Qt class name.
6. `session-status` combines three structural discoveries into a deliberately non-terminal `in_game_candidate` result.
7. `ipc_client.py` provides a bounded JSON client.

The committed profile is fenced to official native-Linux client `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`. Primary-vptr offsets came from exact-binary relocation/typeinfo evidence in historical run `31654434331`; they are evidence for this hash only. A client update requires a new verified profile.

| Target | Primary vptr offset | Expected Qt class |
|---|---:|---|
| `player_protocol_handler` | `0x308a008` | `tibia::game::TPlayerProtocolMessageHandler` |
| `worldmap_handler` | `0x30871d8` | `tibia::worldmap::TWorldmapProtocolMessageHandler` |
| `gameserver_game_session` | `0x3078ba0` | `tibia::game::TGameserverGameSession` |
| `player_data` | `0x308ca70` | `tibia::game::TPlayerData` |
| `container_storage` | `0x308a1a0` | `tibia::container::TContainerStorage` |
| `creature_storage` | `0x308d078` | `tibia::creatures::TCreatureStorage` |
| `game_client` | `0x3076908` | `tibia::client::TGameClient` |

## Health API v1

`health.py` is a pure evaluator. It performs no filesystem, process, socket, X11, VNC or network discovery. A separately authorized runtime producer supplies three non-secret evidence objects:

- the authoritative `runtime-registration.json` record from the canonical namespace;
- a fresh Gate B observation whose boot identity, PID, process start ticks, exact client fence, display/window evidence, registration generation and lease generation exactly match that record;
- a current bridge `PING` response proving `main_base_resolved=true`.

The caller must also provide the current expected controller lease generation. A positive `READY` result requires all of the following:

- registration schema v1 and `runtime_id=track-a-canonical-live`;
- exact client `15.32.df7b29 / 51965216 / e6c244...ff7fe`;
- current expected lease generation equals both registration and fresh observation;
- canonical namespace `canonical-live-runtime`;
- fresh `gate_b=PASS` and `target_uniqueness=PROVEN` observation inside the configured age/skew window;
- exact equality of registration generation, boot hash, PID, process start ticks, version/size/SHA, display and window identity;
- healthy `PING` with a resolved main PIE base.

Failure tokens are explicit: `NOT_REGISTERED`, `REGISTRATION_INVALID`, `EXPECTED_AUTHORITY_UNAVAILABLE`, `LEASE_GENERATION_MISMATCH`, `GATE_B_NOT_PROVEN`, `NAMESPACE_MISMATCH`, `OBSERVATION_STALE`, `OBSERVATION_FROM_FUTURE`, `IDENTITY_MISMATCH` and `BRIDGE_UNHEALTHY`.

A JSON envelope can be evaluated offline:

```sh
python3 tools/tibia_runtime_bridge/health.py evidence.json
```

Example shape (synthetic values only):

```json
{
  "expected_lease_generation": 9,
  "now_ms": 10500,
  "registration": {
    "schema_version": 1,
    "runtime_id": "track-a-canonical-live",
    "registration_generation": 7,
    "lease_generation": 9,
    "boot_id_sha256": "<64 lowercase hex>",
    "pid": 1234,
    "process_start_ticks": 5678,
    "client_version": "15.32.df7b29",
    "client_size": 51965216,
    "client_sha256": "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe",
    "display": ":synthetic",
    "window_identity": {"synthetic": true}
  },
  "observation": {
    "schema": "otclient.tibia-runtime-bridge.runtime-observation.v1",
    "runtime_namespace": "canonical-live-runtime",
    "checked_at_unix_ms": 10000,
    "gate_b": "PASS",
    "target_uniqueness": "PROVEN",
    "registration_generation": 7,
    "lease_generation": 9,
    "boot_id_sha256": "<same 64 lowercase hex>",
    "pid": 1234,
    "process_start_ticks": 5678,
    "client_version": "15.32.df7b29",
    "client_size": 51965216,
    "client_sha256": "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe",
    "display": ":synthetic",
    "window_identity": {"synthetic": true}
  },
  "bridge_ping": {"ok": true, "command": "PING", "main_base_resolved": true}
}
```

`registered_at` is intentionally not used as a liveness timeout. A persistent registration may be old; freshness comes from the separate current Gate B observation.

## Reacquisition and recovery

Reacquisition never falls back to the previous PID/session/generation when the newest authoritative evidence is absent, stale, mismatched or unhealthy:

- same fully ready identity -> `KEEP_CURRENT`;
- different fully ready identity/generation -> `ACCEPT_REACQUIRED`;
- invalid newest evidence with an old accepted identity -> `DROP_CURRENT_AND_WAIT`;
- no accepted identity and no valid newest evidence -> `WAIT_FOR_VALID_REGISTRATION`.

Recovery is a pure state transition only. `READY` degrades to `DEGRADED` on health loss, then moves to `REACQUIRING` while waiting for valid evidence, and returns to `READY` only after the complete health contract passes. It never launches, logs in, restarts, rebinds or mutates the physical client.

## Build and deterministic validation

```sh
cmake -S tools/tibia_runtime_bridge -B /tmp/tibia-runtime-bridge-build
cmake --build /tmp/tibia-runtime-bridge-build --parallel
python3 -m unittest discover -s tests/tools/tibia_runtime_bridge -p 'test_*.py' -v
```

The expected helper library is `/tmp/tibia-runtime-bridge-build/otclient-tibia-runtime-bridge.so`.

## Read API

```sh
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock ping
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock discover player_protocol_handler
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock session-status
```

`DISCOVER` returns counts and validated class names, not durable runtime addresses. A target may legitimately have zero hits while logged out or before its subsystem exists.

`session-status` requires validated `player_protocol_handler`, `gameserver_game_session` and `worldmap_handler` instances. Even when all are present, it returns evidence level `DERIVED_UNTIL_LIVE_CORRELATION`. Neither `health.py` nor recovery semantics promote that structural candidate to authoritative `IN_GAME`; their JSON output explicitly reports game state as unknown/not evaluated.

## Evidence boundary

Historical programme evidence proves the accepted exact-version bridge design and exact profile for the named hash. This P1 package can deterministically prove source reconstruction, unit behavior, standalone compilation and fail-closed lifecycle logic on GitHub-hosted runners.

It does **not** claim current canonical runtime existence, current `:98`/`6082` mapping, current PID/session, current `IN_GAME`, authoritative player position, physical restart/relogin recovery, successful live bridge reacquisition, gameplay writes/actions or compatibility with another official-client hash. Those require separately admitted fresh runtime evidence.
