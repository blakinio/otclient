# Track A — bundled Qt 6.9 bridge recovery prepared

## Status

`PREPARED / UNARMED`

Recovery workflow:

```text
.github/workflows/tibia-official-client-re-atspi-session-bridge-recovery.yml
```

Prepared in commit:

```text
4ed64f1e80711deb191bc39c13f1194c57954d3b
```

The workflow does not run when its own file changes. Its push trigger requires the explicit arm path:

```text
docs/agents/evidence/OTC-20260813-official-client-re/experiments/ARM-20260814-atspi-bridge-recovery
```

That arm file has not been created.

## Historical failure corrected

Historical bridge run `31809994339` built the bridge successfully, then launched the official client with:

```bash
LD_LIBRARY_PATH="$runtime/lib:$lib"
```

where `$lib` contains the extracted Ubuntu toolroot Qt 6.4. The official client requires Qt 6.9 and failed with:

```text
libQt6Core.so.6: version 'Qt_6.9' not found
```

The recovery workflow separates the environments:

- `tool_lib`: build tools, D-Bus, AT-SPI registry and Python GI only;
- `client_lib="$runtime/lib"`: official client and preload bridge runtime only.

The client launch now uses:

```bash
LD_LIBRARY_PATH="$client_lib"
```

and never appends toolroot Qt.

## Loader preflight

Before any existing Track A client is stopped or any semantic login is attempted, the recovery workflow evaluates the official client and bridge preload with `LD_LIBRARY_PATH="$client_lib"` and requires:

1. `libQt6Core.so.6` resolves from the official Tibia runtime library directory;
2. no client Qt resolution points into the toolroot;
3. the bridge preload also resolves `libQt6Core.so.6` from the official runtime;
4. the bridge preload has no unresolved dependency.

Only after those gates may the workflow proceed to private D-Bus/AT-SPI setup, official-client launch, semantic login/character entry and read-only bridge `session-status`.

## Runtime ownership gate

This workflow remains unarmed while another task owns or may own the shared Track A runtime. Before creating the arm file, revalidate:

- no overlapping Track A live-runtime workflow is active;
- any `client.pid` belongs to this Track A namespace and is stale/recoverable under the session-recovery contract;
- Track B runtime/process/display/state is not inspected, stopped or mutated;
- exact client SHA remains `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## Expected acceptance effect

A successful armed run can close only the bridge portion of P1:

```text
bundled Qt 6.9 official-client launch
-> private semantic login
-> semantic character entry
-> bridge IPC socket
-> session-status ok=true
-> in_game_candidate=true
-> required markers have validated_hits > 0
```

It does not by itself prove direct player position, HP/mana, inventory, target, containers, chat/world events, or outbound serializer/framing semantics.
