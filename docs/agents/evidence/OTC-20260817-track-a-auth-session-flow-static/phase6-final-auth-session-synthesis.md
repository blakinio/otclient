# Phase 6 — final native auth/session static synthesis

Task: `OTC-20260817-track-a-auth-session-flow-static`  
PR: `#498`  
Track: `official-client-re`  
Execution boundary: `runtime_access: none`

## Exact-client fence

All promoted native-client claims in this file apply only to the exact official Linux executable:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed client.lzma sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

The final hosted probes fail closed on both the packed and unpacked hashes. They did not start the client, attach to a process, observe X11, perform login, access credentials/tokens/cookies, or upload the raw executable.

## Final validation runs

### Full static synthesis

```text
commit: b465d3fcaa888b4d871f5070cfaf9dc9999c8523
workflow run: 32057651024
job: 95471381728
result: SUCCESS
```

Observed safety/result markers:

```text
AUTHSESSION_FINAL_EXACT_PACKED_SHA=PASS
AUTHSESSION_FINAL_EXACT_CLIENT_SHA=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_LOGIN_PERFORMED=false
AUTHSESSION_SECRET_ACCESS=false
AUTHSESSION_PROCESS_X11_OBSERVATION=false
AUTHSESSION_RAW_CLIENT_UPLOADED=false
AUTHSESSION_FINAL_STATIC_SYNTHESIS=PASS
```

### Native game-login schema discriminator

```text
commit: b62002215e900df653418c48255f08c8c02b4e10
workflow run: 32058203684
job: 95473127456
result: SUCCESS
```

Observed markers:

```text
AUTHSESSION_SCHEMA_EXACT_CLIENT_SHA=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_LOGIN_PERFORMED=false
AUTHSESSION_SECRET_ACCESS=false
AUTHSESSION_SCHEMA_STATIC_PROBE=PASS
```

This discriminator was intentionally negative-capable: it was run to determine whether the exact binary supplied field-level proof that password or session key is the game-login credential. It did not provide such proof, so the password question remains `UNKNOWN` rather than being inferred from proximity.

## FACT — native authentication/session control surface

Historical Track A QMeta inventories were generated from the same exact client SHA and are consistent with the final synthesis.

### Authentication controller

`TAuthenticationProcessController` exposes, among others:

```text
advanceStateMachine                                      0xcfad70 argc=0
onLoginStateMachineStartedShortcutToCharacterSelection  0xcfad8b argc=0
advanceStateMachineDirectlyToCharacterSelection         0xcfadcb argc=0
onLoginStateMachineStarted                              0xcfadd4 argc=0
advanceStateMachineToLoginUpload                        0xcfae14 argc=0
onLoginFinishedSuccessfullyEntered                      0xcfaeb4
onStartGameServerLoginStateEntered                      0xcfb122
requestCharacterGameserverLogin                         0xcfb2e7 argc=0
onShowCharacterSelectionStateEntered                    0xcfb374
```

The exact client therefore contains an explicit native state-machine path that can proceed directly to character selection without traversing the login form when the controller already has the required internal state. The zero-argument signature proves that this entry does not receive email/password as direct invocation arguments. It does not, by itself, prove persistence lifetime or storage location of that internal state.

### Login uploader result

The exact QMeta signature for `TLoginRequestUploader::loginSuccessful` is:

```text
loginSuccessful(
  tibia::characterlist::TCharacterList,
  tibia::worldlist::TWorldList,
  tibia::login::TPlaySessionData
)
```

This is the strongest native structural boundary for the initial account-auth result: successful auth produces character/world data plus `TPlaySessionData` for downstream state.

### Native static login schema vocabulary

The exact binary contains the native login service endpoint and schema vocabulary including:

```text
loginWebService=https://www.tibia.com/clientservices/loginservice.php
stayLoggedInByDefault
login
deviceverificationcode
emailcode
stayloggedin
devicecookie
trusteddevicetoken
loginconfirmationmethod
loginconfirmationtoken
loginconfirmationcode
playdata
characters
worldid
sessionkey
SessionKey
loginemail
```

This proves those concepts are native-client schema/state concepts. It does not establish the exact storage location, refresh rules, or lifetime of every field.

## FACT — UI-to-protocol boundary corrections

The corrected exact-client login-signal chain is:

```text
TLoginProtocolMessageHandler::sendLoginMessage PMF 0xcf2950
 -> QObject connect 0x7d564f
 -> QSlotObject trampoline 0x7d4220
 -> adapter/delegator 0xbd36a0
 -> receiver [enclosing + 0x88]
 -> tibia::protocol::TProtocolMessageQueue
 -> receiver virtual dispatch *(vptr + 0x68)
```

Corrections retained from prior phases:

- `0xcf2ca0` is a Qt static-metacall case, not the implementation PMF.
- `0xbd36a0` is an adapter/delegator, not a proven final serializer.
- `0x858a50` is character/premium/status UI formatting, not credential transport.
- the investigated `0x88c2d0` branch is connecting-description/caption UI/localization, not credential serialization.

The receiver identity is proven by exact connection setup plus QMeta identity:

```text
receiver member: [enclosing + 0x88]
receiver QMetaObject: 0x3085b60
class: tibia::protocol::TProtocolMessageQueue
QMeta stringdata: 0x1cc9800
QMeta metadata: 0x1cc65e0
QMeta static metacall: 0xdf5fe0
```

The queue QMeta inventory contains `sendEnterWorld` and hundreds of protocol operations, establishing that it is the native protocol-message broker rather than a UI-only object.

## FACT — character selection and existing-credentials game connection

Exact QMeta/static boundaries establish:

```text
TCharacterSelectionController::requestCharacterLogin(
  tibia::characterlist::TCharacter
) @ 0xd47300

TAuthenticationProcessController::requestCharacterGameserverLogin()
  @ 0xcfb2e7

TAuthenticationProcessController::onStartGameServerLoginStateEntered
  @ 0xcfb122

TGameClient::connectClientToGameserverWithExistingCredentials()
  wrapper 0xd06660 -> implementation 0x6ef1d0
```

`connectClientToGameserverWithExistingCredentials` is a zero-argument method. This proves the game-server connection path consumes credentials/state already owned by the client rather than taking email/password as parameters at that boundary.

`TGameClient::onRequestLoginWithCredentials(QString, QString)` is a separate two-argument credential-entry boundary, consistent with initial account authentication rather than later game-server connection.

## FACT — reconnect / error / character-selection routing

`TGameSessionDisconnectReactionController` exists in the exact client and exposes explicit reactions including:

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

This proves reconnect/error handling is an explicit stateful native subsystem and that it has distinct routes back to character selection and back to the login dialog. It does not prove exact expiry/refresh thresholds for `TPlaySessionData`.

The exact client also contains `TGameActionChangeCharacter` / change-character handling adjacent to the native protocol/session surface, corroborating a separate character-switch path rather than a mandatory fresh password UI traversal.

## Comparative corroboration — NOT native proof

PR `#284` at `69f9f0fa6dd390e57a11d828508753f7e45988ce` is read-only corroboration only. Its exact-version server/login oracle shows successful account auth returning `session`, `playdata`, and `devicecookie`, with world/character handoff using session/world/character data rather than email/password.

This is consistent with the native `TPlaySessionData` / existing-credentials architecture above, but it is not used as proof of the exact native `GameclientMessageLogin` field contract.

## Rejected overclaim — password requirement in native game login

The final exact-SHA schema probe found native type families:

```text
GameclientMessageLogin
LoginRSAEncryptedBlock
GameclientMessageSecondaryLogin
SecondaryLoginRSAEncryptedBlock
```

It also found `Password` and `SessionKey` strings elsewhere in the executable. Static proximity does not establish field membership or runtime provenance. Therefore:

```text
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
```

A claim of `NO` would exceed the available native evidence. A claim of `YES` would also exceed it.

## Decision matrix

| Question | Result | Evidence boundary |
|---|---|---|
| `CAN_SKIP_LOGIN_FORM` | `PARTIAL` | Native zero-arg direct-to-character-selection state exists for already valid internal auth/session state. Cold auth still requires legitimate authentication. |
| `CAN_SKIP_PASSWORD_ENTRY` | `PARTIAL` | Manual password UI is avoidable when valid retained state is reusable; the cold-auth credential boundary remains `onRequestLoginWithCredentials(QString,QString)` and must preserve server auth/2FA. |
| `CAN_REUSE_SESSION` | `YES` | `loginSuccessful(..., TPlaySessionData)`, native `sessionkey`/`stayLoggedInByDefault`, zero-arg direct-to-character-selection and zero-arg `connect...WithExistingCredentials` form a consistent native reuse architecture. Persistence location/lifetime remain unknown. |
| `PASSWORD_REQUIRED_FOR_GAME_LOGIN` | `UNKNOWN` | Exact field-level native proof is still missing. |
| `DIRECT_CHARACTER_LOGIN_POSSIBLE` | `YES` | With valid play-session state and a selected `TCharacter`, native request-character-login → request-character-gameserver-login → start-game-login boundaries exist. Cold-start persisted preselection is not proven. |

## Lowest safe bypass points

### Valid retained auth/play-session state

```text
TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection
@ 0xcfadcb
```

This is the lowest proven native state-machine entry whose semantic purpose is explicitly to bypass the login-state traversal and proceed to character selection. It must only be used when the native client has valid retained auth/play-session state.

### No valid retained state

Do not jump to character selection. The safe below-UI credential boundary is:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

Credentials must come from an external secure runtime secret source and then remain inside the client's legitimate auth/2FA/device-confirmation state machine. No UI automation is required and no server authentication is bypassed.

## Remaining UNKNOWN

1. Exact in-memory field layout of `tibia::login::TPlaySessionData`.
2. Exact persistent storage implementation for reusable session/device state (file, keyring, launcher handoff, or combination).
3. Exact session expiry and refresh thresholds and whether refresh can happen without a fresh password in every case.
4. Exact native `GameclientMessageLogin` / `LoginRSAEncryptedBlock` credential fields and therefore whether plaintext password participates in game-server login.
5. Exact cold-start storage/selection mechanism for automatically choosing one specific `TCharacter` before character-list presentation.
6. A complete proof of the final queue C++ vtable identity is not required for the bypass decision and was not promoted; only the QMeta receiver identity and virtual-dispatch boundary are proven.

## Terminal static-scope conclusion

The authorized `runtime_access: none` discovery scope is exhausted far enough to identify the safe architecture and implementation entry points without guessing. The wider charter remains `PARTIAL` because the native field-level game-login credential and persistence/expiry details cannot be promoted from the available static evidence.

Any further proof that observes real credential/session provenance must be a new, separately admitted minimal Track A runtime task. It must not inherit PR #475's worldmap runtime/login budget, must redact secrets at source, and must never persist credentials, cookies, tokens, session keys, or plaintext passwords in repository artifacts.
