# Surveyor live differential testing handoff

Date: 2026-08-20

Repository baseline when this handoff was created:

```text
blakinio/otclient
main = ec825e26ed33d28f40bff58e35caec59c01fa0ee
```

## Context

The prior Track A Surveyor false-positive repair is terminally complete. `BRIDGE_3_OF_3` is structural object-presence evidence only and must never be reused as standalone `IN_GAME` authority. The owner was already logged into the game world during the differential tests below. No login, logout, relog, character selection, restart, process control, credential access or local-model execution was performed by the agent.

The owner manually performed only the requested gameplay/UI actions. The agent performed read-only snapshots and comparisons.

## Physical runtime observed for this session

The following values are observational evidence for this session only and must be revalidated before reuse:

```text
runner/control path: synology-otclient-01 / otclient-synology-runner
runtime container: otclient-track-a-kasmvnc
display: :1
client PID observed: 19590
client count: 1
client size: 52109920
client SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
visible Tibia window id observed: 27262999
bridge player_protocol_handler: validated_hits=1, scan_status=OK
bridge gameserver_game_session: validated_hits=1, scan_status=OK
bridge worldmap_handler: validated_hits=1, scan_status=OK
```

Bridge 1/1/1 remains diagnostic only.

## Snapshot A — idle baseline

Owner state: already in the game world and idle for approximately 10 seconds.

Observed at:

```text
2026-08-20T13:24:31Z
```

Snapshot directory inside the control container:

```text
/tmp/tibia-re-baseline-1787232278
```

Results:

```text
COLLECT_ALL=PASS
COVERAGE_ROWS=169
ALIASES=12
MISSING_READERS=11
PRIVACY=PASS
```

## Snapshot B — after player movement

Owner action: moved the character approximately 3-5 tiles and stopped. No other requested action.

Observed at:

```text
2026-08-20T13:27:26Z
```

Snapshot directory:

```text
/tmp/tibia-re-move-1787232435
```

Results remained:

```text
ALIASES=12
MISSING_READERS=11
PRIVACY=PASS
```

All common JSON files from baseline vs movement were compared after removing timestamp-only fields (`generated_at`, `observed_at`, `observed_at_epoch`, `timestamp`, `captured_at`, `created_at`). Result:

```text
BASE_VS_MOVE_SEMANTIC_DIFF_FILES=0
```

Interpretation: current Surveyor output does not expose a semantic field that changed after this simple player-position change. This is evidence of a typed-reader/semantic-coverage gap, not evidence that movement did not occur.

## Snapshot C — main backpack opened

Owner action: opened the main backpack and left it open. No item was moved or used.

Observed at:

```text
2026-08-20T13:29:55Z
```

Snapshot directory:

```text
/tmp/tibia-re-backpack-1787232581
```

Results:

```text
ALIASES=12
MISSING_READERS=11
PRIVACY=PASS
```

Semantic comparisons after removing timestamp-only fields:

```text
BASE_VS_BACKPACK_SEMANTIC_DIFF_FILES=0
MOVE_VS_BACKPACK_SEMANTIC_DIFF_FILES=0
```

Interpretation: current Surveyor output does not expose a semantic field that changed when the main backpack became visibly open. This is a second concrete typed-reader/semantic-coverage gap.

## Current evidence-backed conclusion

Two owner-controlled state changes that are clearly visible in the real client currently produce no semantic JSON delta in Surveyor v2:

1. player position changed by several tiles;
2. main backpack changed from closed to open.

Therefore the next Track A research should use these controlled differentials to prioritize missing typed readers rather than treating 12/12 alias presence as equivalent to useful live-state coverage.

## Recommended next differential sequence

Continue one owner action at a time, taking a fresh read-only snapshot after each action and comparing it against the immediately preceding snapshot plus the idle baseline:

1. open/close a distinct UI panel that is expected to map to `UI-SETTINGS` or `FEATURES`;
2. open/minimize a minimap-related panel without moving the character;
3. change battle-list selection without attacking;
4. open a chat channel or change active chat tab without sending a message;
5. if still zero deltas, stop collecting redundant UI actions and move directly into P0 typed-reader implementation using `missing-readers.json` and the two proven differential gaps above.

Do not ask the owner to relog or restart merely to continue this differential programme. Preserve the current logged-in session whenever possible.

## Safety / authority boundary

For continuation of this handoff:

- agent-side runtime access should remain read-only unless a separately admitted task explicitly requires more;
- owner may perform the requested manual client actions;
- agent must not type credentials, log in/out, select characters, send gameplay input, restart/kill/signal/attach/inject into the client, or mutate canonical state without new authority;
- do not use local Ollama or other local AI models for this continuation unless the owner explicitly changes that instruction;
- revalidate current `main`, active tasks, PRs, lease/registration state, runtime identity and target uniqueness before relying on any historical PID/path/SHA.

## Durable continuation alias

```text
OTCLIENT-TIBIA-RE-SURVEYOR-LIVE-DIFFERENTIAL-CONTINUE
```
