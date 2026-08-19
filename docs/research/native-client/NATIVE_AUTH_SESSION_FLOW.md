# Native authentication and session flow — official Linux client 15.32.df7b29

Task: `OTC-20260817-track-a-auth-session-flow-static`  
PR: `#498`  
Target: official native Linux client `15.32.df7b29`  
Exact SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

This document answers the `OTS_NATIVE_AUTH_SESSION_RESEARCH_AGENT` charter only as far as the exact-client evidence permits. It is not an authentication bypass design. All recommended integration paths preserve the native client's legitimate account authentication, 2FA/device confirmation, server validation, session ownership, game-server login, reconnect, and logout behavior.

## 1. Executive Summary

```text
STATUS: PARTIAL
CAN_SKIP_LOGIN_FORM: PARTIAL
CAN_SKIP_PASSWORD_ENTRY: PARTIAL
CAN_REUSE_SESSION: YES
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES
BEST_BYPASS_ENTRY_POINT: TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection @ 0xcfadcb, only when valid retained auth/play-session state exists
SESSION_CREDENTIAL: tibia::login::TPlaySessionData is the proven native post-auth state object; native schema contains SessionKey/sessionkey, but exact field mapping/persistence/expiry is UNKNOWN
RECONNECT_BEHAVIOR: native disconnect-reaction state machine reuses existing session/game state when possible and has explicit fallback routes to character selection or the login dialog; exact expiry/refresh thresholds are UNKNOWN
```

### FACT

The exact client has an explicit zero-argument authentication-controller transition named `advanceStateMachineDirectlyToCharacterSelection @ 0xcfadcb` plus `onLoginStateMachineStartedShortcutToCharacterSelection @ 0xcfad8b`. This is a native below-UI path, not mouse/keyboard automation.

Successful initial account authentication is represented by:

```text
TLoginRequestUploader::loginSuccessful(
  tibia::characterlist::TCharacterList,
  tibia::worldlist::TWorldList,
  tibia::login::TPlaySessionData
)
```

The exact client also has a separate zero-argument game connection method:

```text
TGameClient::connectClientToGameserverWithExistingCredentials()
```

and a distinct initial credential boundary:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

These boundaries prove a native separation between initial credential submission and later reuse of client-owned authenticated state.

### INFERENCE

The safest implementation architecture is therefore to reuse the client's native retained auth/play-session state and invoke the native shortcut to character selection when that state is valid. If no valid retained state exists, automation should enter the legitimate native auth subsystem below the login UI rather than attempting to synthesize a session or game-login packet.

### UNKNOWN

Static evidence does not prove the exact fields inside `GameclientMessageLogin` / `LoginRSAEncryptedBlock`, so it does not justify either `YES` or `NO` for plaintext-password participation in game-server login. Static evidence also does not prove the exact persistent store, expiry, or refresh policy for `TPlaySessionData` / session keys.

## 2. Full Flow

The exact-client architecture is best represented as two legitimate entry modes converging on the same authenticated character-selection state.

```mermaid
flowchart TD
    A[Client startup] --> B{Valid retained native auth/play-session state?}
    B -->|YES| C[advanceStateMachineDirectlyToCharacterSelection\nTAuthenticationProcessController @ 0xcfadcb]
    B -->|NO| D[onRequestLoginWithCredentials\nTGameClient QString QString]
    D --> E[Native account-auth flow\nHTTPS/login uploader + confirmation states]
    E --> F[loginSuccessful\nTCharacterList + TWorldList + TPlaySessionData]
    F --> C
    C --> G[Character selection state]
    G --> H[requestCharacterLogin TCharacter\nTCharacterSelectionController @ 0xd47300]
    H --> I[requestCharacterGameserverLogin\nTAuthenticationProcessController @ 0xcfb2e7]
    I --> J[onStartGameServerLoginStateEntered\n@ 0xcfb122]
    J --> K[connectClientToGameserverWithExistingCredentials\nTGameClient @ 0xd06660]
    K --> L[Native login protocol message path\nTLoginProtocolMessageHandler]
    L --> M[TProtocolMessageQueue]
    M --> N[Game login / challenge / secondary-login handling]
    N --> O[Authenticated game session / world entered]
    O --> P{Disconnect / error / character change?}
    P --> Q[TGameSessionDisconnectReactionController]
    Q -->|state/session reusable| G
    Q -->|reauth required| D
```

The diagram joins verified native boundaries. The detailed wiring between `connectClientToGameserverWithExistingCredentials` and every protobuf field written by the login protocol remains partly unresolved; no field-level credential claim is inferred from the diagram.

### Startup → authentication decision

#### FACT

The native binary contains login/session concepts including:

```text
loginWebService=https://www.tibia.com/clientservices/loginservice.php
stayLoggedInByDefault
stayloggedin
devicecookie
trusteddevicetoken
loginconfirmationtoken
deviceverificationcode
emailcode
playdata
sessionkey
SessionKey
loginemail
```

The authentication controller exposes both the normal login-state path and a direct-to-character-selection path.

#### INFERENCE

At startup the deciding condition for the direct path must be some form of already acceptable native auth/play-session state. The exact predicate and persistent-storage implementation are not yet proven.

### Initial authentication

#### FACT

The initial credential-facing controller boundary is `TGameClient::onRequestLoginWithCredentials(QString, QString)`. The authentication controller has explicit 2FA/device/email/login-confirmation states, so a below-UI integration can preserve those states without driving widgets.

The account-auth result is delivered as character list, world list, and `TPlaySessionData`.

#### UNKNOWN

The exact semantic assignment of the two `QString` parameters is not promoted beyond the credential-boundary role without runtime or stronger static provenance. The charter's email/password naming is consistent with surrounding UI/schema evidence, but the final integration should bind them from the native caller contract rather than from positional guesswork.

### Character list → selected character

#### FACT

`TCharacterSelectionController::requestCharacterLogin` takes a `tibia::characterlist::TCharacter` and is located at `0xd47300` in the exact client. The authentication controller then exposes `requestCharacterGameserverLogin @ 0xcfb2e7` and `onStartGameServerLoginStateEntered @ 0xcfb122`.

This proves the selected-character handoff is a native programmatic control path below the visual character-list interaction.

### Game-server login

#### FACT

`TGameClient::connectClientToGameserverWithExistingCredentials` has no arguments and resolves through wrapper `0xd06660` to implementation `0x6ef1d0`.

The native game-login protocol surface includes:

```text
TLoginProtocolMessageHandler::sendLoginMessage
GameclientMessageLogin
LoginRSAEncryptedBlock
sendSecondaryLoginMessage
GameclientMessageSecondaryLogin
SecondaryLoginRSAEncryptedBlock
gameLoginChallengeMessage
```

#### UNKNOWN

The exact fields serialized into `GameclientMessageLogin` / `LoginRSAEncryptedBlock` have not been proven. Therefore `PASSWORD_REQUIRED_FOR_GAME_LOGIN` remains `UNKNOWN`.

## 3. Call Graph

### Authentication / character-selection graph

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
  -> native authentication process
  -> TLoginRequestUploader
  -> loginSuccessful(TCharacterList, TWorldList, TPlaySessionData)
  -> TAuthenticationProcessController authenticated state
  -> character selection

Retained-state shortcut:
TAuthenticationProcessController::onLoginStateMachineStartedShortcutToCharacterSelection @ 0xcfad8b
  -> TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection @ 0xcfadcb
  -> character selection state

Selected character:
TCharacterSelectionController::requestCharacterLogin(TCharacter) @ 0xd47300
  -> TAuthenticationProcessController::requestCharacterGameserverLogin() @ 0xcfb2e7
  -> TAuthenticationProcessController::onStartGameServerLoginStateEntered @ 0xcfb122
  -> TGameClient::connectClientToGameserverWithExistingCredentials() @ 0xd06660
  -> implementation 0x6ef1d0
```

### Corrected login-protocol message graph

```text
TLoginProtocolMessageHandler::sendLoginMessage PMF 0xcf2950
  -> QObject connection @ 0x7d564f
  -> QSlotObject trampoline @ 0x7d4220
  -> adapter/delegator @ 0xbd36a0
  -> receiver [enclosing + 0x88]
  -> tibia::protocol::TProtocolMessageQueue
  -> virtual dispatch *(receiver_vptr + 0x68)
```

### FACT — important corrections

`0xcf2ca0` is a Qt static-metacall case, not the implementation PMF for `sendLoginMessage`.

`0xbd36a0` is an adapter/delegator, not a proven final serializer.

The receiver `[enclosing+0x88]` is proven by exact QMeta identity to be `tibia::protocol::TProtocolMessageQueue`:

```text
QMetaObject: 0x3085b60
stringdata:  0x1cc9800
metadata:    0x1cc65e0
static call: 0xdf5fe0
```

## 4. Credential Lifecycle

| Credential/state | Source | Native representation / boundary | Lifetime/storage | Consumers | Status |
|---|---|---|---|---|---|
| Initial account credentials | Secure runtime source / existing UI caller | `onRequestLoginWithCredentials(QString,QString)` | Not proven | Native account-auth state machine | FACT boundary; exact parameter semantics partly UNKNOWN |
| 2FA / verification material | Native confirmation states | `deviceverificationcode`, `emailcode`, `loginconfirmationtoken`, related controller states | Not proven | Account-auth flow | FACT concepts, UNKNOWN storage/lifetime |
| Device remembered state | Account-auth response/state | `devicecookie`, `trusteddevicetoken`, `stayloggedin` schema concepts | UNKNOWN | Startup/auth reuse | FACT concepts, UNKNOWN implementation |
| Play-session state | `TLoginRequestUploader::loginSuccessful` | `tibia::login::TPlaySessionData` | UNKNOWN | Authentication controller / character selection / later game connection | FACT |
| Session key concept | Native auth schema | `sessionkey` / `SessionKey` | UNKNOWN | Exact consumer mapping not proven | FACT concept, UNKNOWN field mapping |
| Selected character | Character list | `tibia::characterlist::TCharacter` | Current selection/session | `requestCharacterLogin` | FACT |
| Game-login credential payload | Existing authenticated client state | `GameclientMessageLogin` / `LoginRSAEncryptedBlock` | UNKNOWN | game-server login | UNKNOWN field contract |

### Password lifetime

#### FACT

There is a distinct initial `onRequestLoginWithCredentials(QString,QString)` boundary and a later zero-argument `connectClientToGameserverWithExistingCredentials` boundary.

#### INFERENCE

This architecture is designed so that later game connection consumes internal authenticated state, not the login form's values as direct function parameters.

#### UNKNOWN

The exact static protobuf field contract does not prove that plaintext password is absent from all internal game-login payload construction. No password-wipe timing or memory-lifetime claim is made.

## 5. Session Lifecycle

### FACT

A successful account-auth result includes `TPlaySessionData`. The binary also contains `stayLoggedInByDefault`, `stayloggedin`, `devicecookie`, and `SessionKey/sessionkey` concepts. The authentication controller has a direct-to-character-selection path, and the game client has `connectClientToGameserverWithExistingCredentials()`.

Taken together, these exact-client boundaries prove that session/authenticated state is intentionally reusable inside the client.

Therefore:

```text
CAN_REUSE_SESSION: YES
```

This answer means **native session reuse exists as an architecture and control path**. It does not mean that every expired session can be reused or that the exact persistence/refresh behavior has been proven.

### UNKNOWN

- exact `TPlaySessionData` field layout;
- exact disk/keyring/launcher storage path;
- exact expiry timestamp or TTL;
- exact refresh mechanism;
- whether a refresh always avoids re-entering the account password;
- cleanup/destruction timing of sensitive fields.

## 6. Reconnect Flow

### FACT

The exact client contains `TGameSessionDisconnectReactionController` with explicit methods for:

```text
loginAgainAfterLoginWaitElapsed
onGameSessionConnected
onGameSessionLoginSuccessful
onWorldEntered
onSessionEndInformation
onGameSessionDisconnected
onConnectionError
onGameLoginErrorMessage
onGameLoginWaitMessage
onGameLoginChallengeMessage
onDialogResponseShowCharacterSelection
onDialogResponseShowLoginDialog
onWaitAbortedShowCharacterSelection
onGameSessionPingTimeout
onPingTimeoutWaitTimeElapsed
```

The existence of separate `ShowCharacterSelection` and `ShowLoginDialog` reactions proves reconnect/error handling can choose between continuing with existing authenticated state and forcing a return to account login.

### INFERENCE

When reconnect state remains usable, the native path should reuse the same client-owned existing-credentials/session machinery rather than require UI account-password entry on every transient disconnect.

### UNKNOWN

The exact condition that marks `TPlaySessionData` invalid/expired and the exact refresh/re-auth threshold are not statically proven.

## 7. Character Switch Flow

### FACT

The exact binary contains `TGameActionChangeCharacter` handling near the protocol/session surface, and the disconnect-reaction controller has an explicit route to character selection. Character entry itself is programmatic through `requestCharacterLogin(TCharacter)`.

This supports the following native high-level flow:

```text
in-game session
 -> change-character / session transition
 -> character selection
 -> requestCharacterLogin(TCharacter)
 -> requestCharacterGameserverLogin()
 -> game-server login using existing client-owned authenticated state
```

### UNKNOWN

The exact cleanup order for the old game connection and the precise retained credential object across every character-switch variant were not promoted from this static task.

## 8. UI Bypass Point

### Existing valid retained auth/play-session state

The preferred native entry is:

```text
TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection
0xcfadcb
argc=0
```

**THIS is the lowest safe entry point below the login UI.**

The statement is conditional: this entry point is safe only when the client already owns valid retained auth/play-session state. It must not be used to fabricate authenticated state or skip required server authentication, 2FA, device verification, or login confirmation.

### No valid retained state

Do **not** invoke the direct-to-character-selection shortcut.

The lowest currently identified legitimate below-UI credential boundary is:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

A future integration may supply its required values from a secure runtime secret provider and then allow the client's existing authentication state machine to handle HTTPS account authentication and all required confirmation steps. This removes the visual form without bypassing authentication.

### Forbidden approaches

Do not use:

- `xdotool` or screen coordinates;
- OCR/pixel matching;
- AutoHotkey or synthetic mouse/keyboard traversal;
- plaintext-password files committed to or generated inside the repository;
- token/cookie/session-key fixtures;
- disabled TLS verification;
- hand-built server-auth bypasses;
- direct game-login packet synthesis while its native credential fields remain `UNKNOWN`.

## 9. Recommended Oteryn Integration

The smallest evidence-compatible implementation should be a thin integration layer around existing native state-machine entry points rather than a replacement login stack.

### Recommended startup algorithm

1. Ask the native client/session subsystem whether retained authenticated/play-session state is valid. The exact predicate still needs implementation-level discovery; do not invent one.
2. If valid, invoke `TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection @ 0xcfadcb`.
3. If invalid/unavailable, obtain account credentials only from an approved secure runtime secret source and call the native below-UI credential/auth boundary. Preserve all native 2FA/device/login-confirmation states.
4. After `loginSuccessful(TCharacterList,TWorldList,TPlaySessionData)`, allow the native controller to own the resulting state.
5. Select a desired `TCharacter` programmatically through the existing character-selection controller.
6. Invoke the native character game-server-login transition, ending in `connectClientToGameserverWithExistingCredentials()`.
7. Do not synthesize `GameclientMessageLogin` independently until the exact native game-login credential field contract is proven.
8. Reuse the native disconnect/reconnect reaction controller rather than adding retry timers, credential replay loops, or UI automation.

### Direct selected-character startup

```text
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES
```

This is proven for the state **after a valid play session exists and a `TCharacter` object is available**: the native `requestCharacterLogin(TCharacter)` and game-server-login transitions can be invoked programmatically.

What is not yet proven is the cold-start persistence mechanism for selecting a named character before the character list has been reconstructed. The implementation should therefore treat persisted character preference as a separate integration concern, not as an authentication credential.

### Secret handling requirements

- Never log plaintext password, OTP, confirmation token, device cookie, session key, or raw `TPlaySessionData`.
- Never commit those values to Git, CI output, fixtures, screenshots, or evidence files.
- Do not copy secrets into Oteryn-owned durable state unless governance explicitly defines an approved credential store.
- Prefer native retained-session reuse over password persistence.

## 10. Remaining Unknowns

The authorized static scope cannot resolve these without either stronger exact descriptor/static proof or a separately admitted, minimal runtime observation:

1. Exact `TPlaySessionData` field layout.
2. Exact persistent store and startup load path for reusable session/device state.
3. Exact session expiry, refresh, invalidation, and destruction policy.
4. Exact native fields inside `GameclientMessageLogin` / `LoginRSAEncryptedBlock`.
5. Whether plaintext password participates in game-server login at any internal stage.
6. Exact secure lifecycle/wipe timing of the initial account password.
7. Exact cold-start persisted-character preference path.
8. Complete field-level mapping of reconnect credential reuse after every error variant.

### Required next proof if the wider charter must become DONE

Create a **new Track A runtime task with explicit runtime admission**, separate from PR #475's worldmap runtime budget. Its scope should be only the remaining provenance questions, with source-side redaction so no secret value is ever persisted. A successful runtime task would need to prove field provenance/consumer identity, not reveal credential contents.

## Evidence index

Durable evidence for this task:

```text
docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase1-existing-credentials-chain.md
docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase2-connection-and-existing-credentials.md
docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase3-provenance-and-corrections.md
docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase4-enclosing-connection-setup.md
docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase5-protocol-message-queue-identity.md
docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase6-final-auth-session-synthesis.md
```

Final exact-client validation:

```text
full static synthesis:
  commit: b465d3fcaa888b4d871f5070cfaf9dc9999c8523
  run: 32057651024
  job: 95471381728
  result: SUCCESS

game-login schema discriminator:
  commit: b62002215e900df653418c48255f08c8c02b4e10
  run: 32058203684
  job: 95473127456
  result: SUCCESS
```

No live login, credential access, token/cookie capture, process/X11 observation, or secret artifact was used to produce this report.
