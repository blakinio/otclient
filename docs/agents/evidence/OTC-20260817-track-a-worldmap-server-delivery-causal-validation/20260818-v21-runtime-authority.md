# V21 guarded native GameClient continuation authority

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`
PR: `#475`
Owner continuation: `dokoncz zadanie`

This authority is conditional and fail-closed.

If `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/map-world-entry-v20.png` already exists on the task head, v21 physical execution is forbidden and must be skipped because the owner's success condition has already been met.

Otherwise v20 is treated as the tenth sequential baseline login attempt and v21 is authorized for exactly one additional sequential baseline login attempt:

```text
BASELINE_LOGIN_MAX=11
BASELINE_LOGIN_CONSUMED_BEFORE_V21=10
ELEVENTH_BASELINE_LOGIN_ATTEMPT_AUTHORIZED=true
SIMULTANEOUS_LOGGED_IN_SESSIONS_MAX=1
```

V21 must reuse unchanged:

- exact official client SHA `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`;
- XID/XRes/GDB/pre-Storage/pre-secret/secret-ingress gates;
- legitimate account login;
- native current-session character discovery (`characterList count == 1`);
- native index `0` selection;
- native `onCharacterSelectionConfirmed` method 11;
- scheduler-locking restoration;
- real implementation observation and v20 AUTH state-entry fallback semantics.

Only if the real start-game-login implementation has executed but the real `connectClientToGameserverWithExistingCredentials` implementation remains absent may v21 invoke the original `TGameClient` QMeta method `connectClientToGameserverWithExistingCredentials()` on a unique live exact-vptr GameClient object after runtime instruction-byte and Qt-thread-affinity proof.

Forbidden:

- fabricated auth/session/character state;
- packet/login-message synthesis;
- OCR or coordinate character selection;
- parallel logged-in session;
- screenshot before structural IN_GAME.

Success remains only:

```text
FullMap observed
AND map-description strips >= 10
AND exact-window post-structural screenshot persisted
```
