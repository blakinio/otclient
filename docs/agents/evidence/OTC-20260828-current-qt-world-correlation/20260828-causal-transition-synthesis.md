# Current Qt world correlation — causal transition synthesis

Task: `OTC-20260828-current-qt-world-correlation`

Exact client: `15.32.75d4a0`, size `52105824`, SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

All three retained deep-lifecycle runs used the same official-client process identity: PID `13947`, start ticks `51652120`. The logger retained no credentials, session secrets, packet payloads, socket endpoints, raw window titles, process environment or heap bytes. Process-memory access was read-only.

## Retained runs

- `33159662745` / job `98810780559`: owner-marked login-to-world transition; artifact `9681511026`.
- `33161071475` / job `98815400955`: mixed entry plus owner-marked world-exit control; artifact `9682068904`.
- `33162761241` / job `98820910859`: continuous owner-manual login → character selection → world; artifact `9682715983`.

The exact secret-free JSONL and summary files from each artifact are retained under the corresponding `run-*` directory. `result.json` records their SHA-256 digests.

## Repeated entry ordering

Across three observed entry segments the same ordering recurred:

1. authentication QState transiently entered raw value `2`;
2. authentication QState returned to `0`;
3. `TGameserverLoginProcessController` QState candidate changed from `0` to unresolved/null;
4. PID-owned TCP established count increased;
5. boolean character/world window context became `true`;
6. in the two owner-marked entry runs, the owner subsequently reported a visible game map.
For the owner-marked entry runs, the observed `auth 2→0` to gameserver-login-null interval was `2.319 s` and `2.055 s`; the gameserver-login-null to window-context-true interval was `1.171 s` and `1.920 s`. The observer-only entry segment in run `33161071475` fell in the same ordering (`3.354 s`, then `1.417 s`).

This establishes a repeatable causal corridor around world entry, but not a standalone semantic state.

## Reverse control

Run `33161071475` also captured the owner-marked world exit:

- `12:05:54.486+02:00`: PID-owned TCP established count reached `0`;
- `12:05:55.520+02:00`: authentication QState entered `2`;
- `12:05:56.041+02:00`: TCP count rose again;
- `12:05:56.775+02:00`: boolean world/character window context became `false`;
- `12:06:10+02:00`: owner reported visible character selection.

Therefore `auth QState=2`, TCP counts and gameserver-login-null are transition observations, not durable `IN_GAME` state.

## Rejected standalone authorities

The following must not be used individually to claim `IN_GAME`: `BRIDGE_3_OF_3`, heap vptr-hit counts for the long-lived player/session/world/disconnect objects, authentication state-machine running/raw state, gameserver-login QState null, PID-owned TCP count, or boolean window context.

Historical and current runtime evidence also proves that the long-lived object-presence markers survive login, character selection and world exit. Their presence is architectural lifetime evidence only.

## Next semantic frontier

The correct next anchor is the exact-current native `tibia::game::TPlayerProtocolMessageHandler::worldEntered` signal, or a durable state mutation directly caused by that signal and cleared on world exit.
Historical QMeta evidence identifies `worldEntered` as a signal on `TPlayerProtocolMessageHandler`, but historical addresses are not reusable. The current-build resolver must recover the signal from the exact `15.32.75d4a0` ELF by current strings/RELA/QMeta structure and must fence all output to the exact size/SHA above.

Until that exact semantic anchor is recovered, causally observed and independently reviewed:

```text
IN_GAME_CLAIMED=false
SEMANTIC_PROMOTION_PERFORMED=false
CAUSAL_CORRIDOR=REPEATABLE
CANONICAL_IN_GAME_AUTHORITY=NOT_YET_ESTABLISHED
```

The current runtime container was later found absent on the Docker host. That is not treated as evidence about the client state; any future live confirmation requires fresh canonical runtime admission and exact process identity.
