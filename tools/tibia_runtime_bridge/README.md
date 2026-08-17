# Official Tibia Runtime Bridge

This tool is the durable Phase 9 integration boundary for `OTCLIENT-TIBIA-RE`. It is intentionally separate from the maintained OTClient product runtime.

## Current scope and authority

The **IPC/discovery API is read-only and fail-closed**. Activation is a separate authority boundary: `launcher.py` uses `LD_PRELOAD`, which is invasive process instrumentation even though it does not modify installed client files. P1 health/recovery never invokes the launcher. Launch/injection/attach/login/restart/relogin and all physical-session control remain exclusively RUNTIME-owned under the current admission, Gate A, generation-rebind, Gate B and bootstrap contracts.

Current behavior:

1. `launcher.py` loads a versioned profile and verifies the exact official-client SHA-256 before launch. It is an implementation primitive for the RUNTIME lane, not P1 runtime authority.
2. When RUNTIME is authorized to activate it, the launcher injects `otclient-tibia-runtime-bridge.so` with `LD_PRELOAD`; installed client files are not modified.
3. `bridge.cpp` discovers the executable PIE base at runtime, binds a mode-`0600` Unix-domain socket, and accepts only bounded local read commands.
4. `PING` reports bridge readiness plus the process identity envelope: boot hash, PID, process start ticks and exact client version/size/SHA fields.
5. `DISCOVER <target>` executes on the client's Qt event-loop thread, scans only readable/writable mappings of the current process for the profile's exact primary-vptr value, applies an object-layout plausibility gate, and validates candidate QObject-compatible instances by Qt class name.
6. Discovery explicitly distinguishes a successful scan with zero hits from an unavailable/failed scan. `/proc/self/maps` or `/proc/self/mem` open/read failures return `ok:false`; they never collapse into a healthy zero-hit observation.
7. `session-status` combines three successful structural discoveries into a deliberately non-terminal `in_game_candidate` result. Any bridge-side discovery failure remains non-healthy.
8. `ipc_client.py` provides a bounded JSON client and separates transport, protocol and peer-identity failures. When an expected identity is supplied, every Unix connection verifies `SO_PEERCRED`, current boot identity, process start ticks and the exact executable size/SHA before accepting a response.
9. `health.py` provides a fail-closed lifecycle API over an explicitly supplied exact-runtime identity and socket binding. It rejects stale generations/process identities, verifies the `PING` identity envelope, drops stale cached bindings and performs bounded reacquisition/recovery without starting or mutating a client.

The first committed profile is fenced to official Linux client `15.32.df7b29`, size `51965216`, with SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`. Its primary-vptr offsets were resolved from exact-binary ELF relocation/typeinfo evidence in `OTCLIENT-TIBIA-RE` run `31654434331`; they are evidence for that hash only. A client update requires a new verified profile. Never copy an offset forward without rediscovery.

Current profiled targets are:

| Target | Primary vptr offset | Expected Qt class |
|---|---:|---|
| `player_protocol_handler` | `0x308a008` | `tibia::game::TPlayerProtocolMessageHandler` |
| `worldmap_handler` | `0x30871d8` | `tibia::worldmap::TWorldmapProtocolMessageHandler` |
| `gameserver_game_session` | `0x3078ba0` | `tibia::game::TGameserverGameSession` |
| `player_data` | `0x308ca70` | `tibia::game::TPlayerData` |
| `container_storage` | `0x308a1a0` | `tibia::container::TContainerStorage` |
| `creature_storage` | `0x308d078` | `tibia::creatures::TCreatureStorage` |
| `game_client` | `0x3076908` | `tibia::client::TGameClient` |

## Build

The helper is standalone and requires Qt 6 Core development files:

```sh
cmake -S tools/tibia_runtime_bridge -B /tmp/tibia-runtime-bridge-build
cmake --build /tmp/tibia-runtime-bridge-build --parallel
```

The expected library is:

```text
/tmp/tibia-runtime-bridge-build/otclient-tibia-runtime-bridge.so
```

## Launch — RUNTIME authority only

The launcher performs the binary identity check before setting `LD_PRELOAD`:

```sh
python3 tools/tibia_runtime_bridge/launcher.py \
  --profile tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json \
  --helper /tmp/tibia-runtime-bridge-build/otclient-tibia-runtime-bridge.so \
  --socket /tmp/otclient-tibia-re.sock \
  /exact/path/to/Tibia/bin/client
```

This command is **not** permission for P1 to launch or inject the physical client. Networking/tunnelling remains owned by the caller/runtime task. The bridge does not create credentials, WARP state or a network bypass. Current Track A runtime governance still requires separate admission/bootstrap/rebind/Gate A/Gate B authority and evidence.

## Read API

```sh
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock ping
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock discover player_protocol_handler
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock session-status
```

The CLI commands above are raw read operations and do not on their own establish canonical runtime identity. The P1 lifecycle API uses the same transport with an explicit admitted identity and enables peer verification for every connection.

A successful `DISCOVER` response includes `scan_status="OK"`, counts and validated class names, not durable runtime addresses. A target may legitimately have zero hits while logged out or before its subsystem exists. Scanner failures return `ok:false` with a stable error code such as `PROC_MEM_OPEN_FAILED` or `PROC_MEM_READ_FAILED` and therefore cannot be interpreted as a normal zero-hit state.

`session-status` currently requires validated instances of all three:

- `player_protocol_handler`;
- `gameserver_game_session`;
- `worldmap_handler`.

If all are present it returns `in_game_candidate=true` with evidence level `DERIVED_UNTIL_LIVE_CORRELATION`. This is intentionally **not** the final `session.is_in_game()` contract. It may be promoted only after a current OTClient-owned live world session correlates these three markers with independently decoded Worldmap/protocol state and also proves their disappearance or replacement across logout/restart.

## Health, reacquisition and recovery API

`health.py` deliberately has no candidate-process scanner and no process-control function. A separately admitted runtime producer must supply a `BridgeBinding` containing both:

- the explicit schema-v1 runtime identity (`runtime_id`, registration/lease generations, boot hash, PID, process start ticks and the exact client version/size/SHA fence);
- an explicit absolute Unix-socket path for that exact runtime.

Typical integration shape:

```python
from pathlib import Path
from tools.tibia_runtime_bridge.health import BridgeBinding, BridgeSession, RecoveryPolicy


def current_binding():
    registration = get_current_gate_b_approved_registration_from_runtime_lane()
    if registration is None:
        return None
    return BridgeBinding.from_registration(
        registration,
        socket_path=Path(get_current_admitted_bridge_socket()),
    )


session = BridgeSession(current_binding)
result = session.recover(RecoveryPolicy(max_attempts=3))
```

The producer functions above are intentionally placeholders for a higher-level admitted integration. P1 does not implement canonical host discovery and must not substitute historical `:98`, `6082`, PID/session data, scan the host for a likely client, or infer a socket path. `BridgeBinding.from_registration(...)` validates schema/fence shape; the producer is still responsible for supplying only a current Gate-B-approved registration/lease generation.

For the default transport, a stable socket pathname is **not** treated as identity. Every accepted connection verifies the actual Unix peer PID with `SO_PEERCRED`, rechecks current boot ID and process start ticks under `/proc`, and verifies the peer executable's exact size/SHA. `PING` must then return the same boot/PID/start/version/size/SHA envelope. A same-path socket replacement, PID reuse, process `exec`, stale registration, or profile mismatch therefore fails closed and discards the cached binding.

Health semantics are deliberately narrower than gameplay/session semantics:

| State | Meaning |
|---|---|
| `HEALTHY` | The explicit binding stayed current; every IPC connection was bound to the exact peer process/executable identity; `PING` identity matched; all discovery scans succeeded; and the bounded read API returned structurally valid responses. `in_game_candidate` remains derived only. |
| `DEGRADED` | The exact endpoint answered but bridge/read-discovery readiness failed, including explicit scanner failure. |
| `UNREACHABLE` | Local Unix-socket transport failed. |
| `MALFORMED` | Response framing/schema or derived-session contract was invalid. |
| `NO_IDENTITY` | No explicit runtime binding is available; P1 does not guess one. |
| `INVALID_IDENTITY` | Supplied identity is outside the exact runtime/profile fence. |
| `STALE_IDENTITY` | Registration/lease generation regressed, identity changed without a registration-generation advance, the binding changed during a probe, the actual Unix peer did not match boot/PID/start/executable identity, or the `PING` identity envelope mismatched. The cached binding is discarded. |

`BridgeSession.recover()` is bounded by `RecoveryPolicy.max_attempts`. Each attempt reacquires only whatever explicit binding the producer currently supplies and probes it. It has no launch, login, logout, restart, signal, attach, input, display, VNC, lease, registration-write or bootstrap side effect. Real persistent-session reacquisition/restart/relogin evidence remains the RUNTIME lane's responsibility.

## Evidence boundary

Already proven by the programme's exact-client integration evidence:

- a temporary preload helper can load into this exact client;
- a helper worker can queue work onto the real Qt application thread;
- the client remains alive during repeated queued scans;
- QCoreApplication child traversal is insufficient for game-handler discovery;
- exact-binary relocation/typeinfo analysis resolves the profiled primary vptrs listed above.

This durable implementation adds exact-hash fencing, owner-only local IPC, exact-peer channel binding, explicit scanner failure semantics, profile-vptr discovery and deterministic fail-closed lifecycle semantics. It does **not** yet claim:

- current canonical runtime existence or identity;
- current `IN_GAME` status;
- real persistent-session attach/reacquisition success;
- restart/relogin stability on the physical client;
- authoritative player position;
- successful discovery of the player protocol handler in a current OTClient-owned live world session;
- any gameplay write/action through the bridge;
- compatibility with any client hash other than an explicitly validated profile.

Write/action commands must not be added to the stable API until a current OTClient-owned live session proves the corresponding before/after structural state transition.
