# V22 guarded native on-connect continuation authority

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`
PR: `#475`
Owner continuation: `dokoncz zadanie`

If either `map-world-entry-v20.png` or `map-world-entry-v21.png` already exists on the task head, v22 physical execution is forbidden and must be skipped.

Otherwise v22 is authorized for exactly one further sequential baseline login attempt under the same one-session runtime ownership. The conservative durable budget is:

```text
BASELINE_LOGIN_MAX=12
BASELINE_LOGIN_CONSUMED_BEFORE_V22=11
TWELFTH_BASELINE_LOGIN_ATTEMPT_AUTHORIZED=true
SIMULTANEOUS_LOGGED_IN_SESSIONS_MAX=1
```

V22 must reproduce the already-proven chain and may add only this conditional control:

- require native character confirmation success;
- require real start-game-login implementation;
- require real `connectClientToGameserverWithExistingCredentials` implementation (natural or the guarded v21 zero-argument native fallback);
- only if `ConnectExistingImpl >= 1` and real `OnConnectGameserverImpl == 0`, invoke the original zero-argument `TGameClient::onConnectClientToGameserver` QMeta method on the unique live exact-vptr GameClient object after runtime instruction-byte and Qt-thread-affinity proof.

V22 may NOT directly invoke or fabricate:

- `onGameSessionConnected`;
- `onGameSessionLoginSuccessful`;
- any game-login success/error packet or callback;
- any auth/session/character payload.

After `onConnectClientToGameserver`, network and server acceptance must proceed through original client logic. Success remains `FullMap + >=10 strips + post-structural exact-window screenshot`.
