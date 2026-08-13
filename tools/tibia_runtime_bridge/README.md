# Official Tibia Runtime Bridge

This tool is the durable Phase 9 integration boundary for `OTCLIENT-TIBIA-RE`. It is intentionally separate from the maintained OTClient product runtime.

## Current scope

Version 1 is read-only and fail-closed:

1. `launcher.py` loads a versioned profile and verifies the exact official-client SHA-256 before launch.
2. The launcher injects `otclient-tibia-runtime-bridge.so` with `LD_PRELOAD`; it does not modify the installed client files.
3. `bridge.cpp` discovers the executable PIE base at runtime, binds a mode-`0600` Unix-domain socket, and accepts only bounded local commands.
4. `PING` reports bridge health.
5. `DISCOVER <target>` executes on the client's Qt event-loop thread, scans only readable/writable mappings of the current process for the profile's exact primary-vptr value, and validates candidate QObject-compatible instances by Qt class name.
6. `ipc_client.py` provides a bounded JSON client for the socket.

The first committed profile is fenced to official Linux client `15.32.df7b29` with SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`. Its `player_protocol_handler` vptr offset is evidence for that hash only. A client update requires a new verified profile; do not copy the offset forward.

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

## Launch

The launcher performs the binary identity check before setting `LD_PRELOAD`:

```sh
python3 tools/tibia_runtime_bridge/launcher.py \
  --profile tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json \
  --helper /tmp/tibia-runtime-bridge-build/otclient-tibia-runtime-bridge.so \
  --socket /tmp/otclient-tibia-re.sock \
  /exact/path/to/Tibia/bin/client
```

Networking/tunnelling remains owned by the caller/runtime task. The bridge does not create credentials, WARP state or a network bypass.

## Read API

```sh
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock ping
python3 tools/tibia_runtime_bridge/ipc_client.py --socket /tmp/otclient-tibia-re.sock discover player_protocol_handler
```

`DISCOVER` returns counts and validated class names, not durable runtime addresses. A target may legitimately have zero hits while logged out or before its subsystem exists.

## Evidence boundary

Already proven by the programme's exact-client integration evidence:

- a temporary preload helper can load into this exact client;
- a helper worker can queue work onto the real Qt application thread;
- the client remains alive during repeated queued scans;
- QCoreApplication child traversal is insufficient for game-handler discovery.

This durable implementation adds exact-hash fencing, owner-only local IPC and profile-vptr discovery. It does **not** yet claim:

- current `IN_GAME` status;
- authoritative player position;
- successful discovery of the player protocol handler in a live world session;
- any gameplay write/action through the bridge;
- compatibility with any client hash other than an explicitly validated profile.

Write/action commands must not be added to the stable API until a current OTClient-owned live session proves the corresponding before/after structural state transition.
