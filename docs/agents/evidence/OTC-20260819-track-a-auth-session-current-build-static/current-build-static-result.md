# TIBIA-RE-AUTH-SESSION — current-build static result

Task: `OTC-20260819-track-a-auth-session-current-build-static`  
Draft PR: `#556`  
Research head before evidence checkpoint: `3ddc1d2889f6a4c84f15ccec3af20f32ea965699`  
Workflow run/job: `32228900775 / 95994337407`  
Execution: GitHub-hosted Ubuntu 24.04, `runtime_access: none`

## Exact current public build fence

The workflow independently fetched the public Linux package through the disposable WARP path and verified:

```yaml
packed_size: 10214529
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_size: 52109920
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Safety markers from the successful job:

```text
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_CLIENT_EXECUTED=false
AUTHSESSION_LOGIN_PERFORMED=false
AUTHSESSION_SECRET_ACCESS=false
AUTHSESSION_RAW_CLIENT_UPLOADED=false
AUTHSESSION_RAW_CLIENT_RETAINED=false
```

No proprietary raw client was committed or uploaded as an artifact.

## FACT — current `TGameClient` QMeta identity

The exact current build contains one recovered QMetaObject for `tibia::client::TGameClient`:

```text
static_metaobject = 0x2f82be0
stringdata        = 0x1cb4cf4
metadata          = 0x1cb4740
static_metacall   = 0xd19100
method_count      = 44
signal_count      = 6
```

The cold-auth method remains uniquely present:

```text
name              = onRequestLoginWithCredentials
meta_index        = 17
argc              = 2
method_flags      = 0x8
raw_param_type_ids= 0x2b,0xa,0xa
semantic signature= void(QString, QString)
```

## FACT — current cold-auth dispatch target

A unique full-44-method dispatch table was recovered from the current `TGameClient::qt_static_metacall`:

```text
dispatch_lea    = 0xd1910a
dispatch_table  = 0x1d903c4
method_17_target= 0xd196f0
instruction_fence_32 = 488b5110488b71084883c4485b5de93d609cff0f1f440000488bbfa009000048
```

Therefore the historical old-build target `0xd06850` is not reusable on the current SHA. The semantic QMeta contract survived, while the executable addresses changed.

## FACT — other current-build QMeta auth/session entries

The same exact-build scan recovered:

```text
tibia::authentication::TLoginRequestUploader
  static_metacall = 0xd0ffe0
  loginSuccessful index 0
  target = 0xd10200
  fence16 = 488b5310488b4b08488d35916c270248

tibia::client::TGameClient
  connectClientToGameserverWithExistingCredentials index 11
  target = 0xd19500
  fence16 = 4883c4485b5de9658c9cff0f1f440000

tibia::gamewindow::TCharacterSelectionController
  static_metacall = 0xd51c70
  requestCharacterLogin index 0
  target = 0xd52050
  fence16 = 498b442408f30f6f08488b100f298c24
```

These are static exact-build entry points only. This task does not claim runtime object provenance, thread affinity, live call safety, authentication success, character entry, or `IN_GAME`.

## FACT — structural family survives on the current build

All 19 bounded target names were present in the current binary, including:

- `TAuthenticationProcessController`;
- `advanceStateMachineDirectlyToCharacterSelection`;
- `onLoginStateMachineStartedShortcutToCharacterSelection`;
- `TLoginRequestUploader` / `loginSuccessful`;
- `TCharacterList`, `TWorldList`, `TPlaySessionData`;
- `TCharacterSelectionController` / `requestCharacterLogin`;
- `requestCharacterGameserverLogin`;
- `onStartGameServerLoginStateEntered`;
- `connectClientToGameserverWithExistingCredentials`;
- `TGameSessionDisconnectReactionController`;
- `sendLoginMessage`;
- `GameclientMessageLogin` / `LoginRSAEncryptedBlock`;
- `GameclientMessageSecondaryLogin` / `SecondaryLoginRSAEncryptedBlock`.

Result marker:

```text
AUTHSESSION_CURRENT_STRUCTURAL_STRING_TARGETS_PRESENT=19/19
AUTHSESSION_CURRENT_STATIC_DISCRIMINATOR=PASS
```

Presence proves structural continuity of names/types only. It does not assign executable addresses or semantic provenance to entries not separately recovered through QMeta/dispatch evidence.

## SUPERSEDED — historical old-build addresses

The following addresses remain evidence only for the prior `51965216 / e6c244bd...` build and are `SUPERSEDED_FOR_CURRENT_BUILD` unless separately rediscovered:

```text
TGameClient static metacall                     0xd06260
cold-auth target                                0xd06850
advance directly to character selection        0xcfadcb
shortcut to character selection                0xcfad8b
connect-existing-credentials wrapper            0xd06660
connect-existing-credentials historical impl    0x6ef1d0
requestCharacterLogin                           0xd47300
requestCharacterGameserverLogin                 0xcfb2e7
onStartGameServerLoginStateEntered              0xcfb122
```

## UNKNOWN / not claimed by this bounded slice

- exact executable targets for non-QMeta state-machine methods such as `advanceStateMachineDirectlyToCharacterSelection`, `requestCharacterGameserverLogin`, and `onStartGameServerLoginStateEntered`;
- current-build producer/field provenance inside `TPlaySessionData` and `TAuthenticationAndEncryptionInfo`;
- whether password material is required in the game-server-login message on the current build;
- live object addresses, vptr instances, Qt thread affinity and runtime instruction-byte proof;
- login success, character selection, game-server connection or causal `IN_GAME`;
- restart/relogin/update stability.

## Researcher disposition

```yaml
STATUS: DRAFT_NOT_PROMOTED
ALIAS: TIBIA-RE-AUTH-SESSION
RUNTIME_ACCESS: none
CURRENT_BUILD_STATIC_REVALIDATION: PASS
COLD_AUTH_QMETA_CURRENT_BUILD: PROVEN_STATIC_EXACT_BUILD
CHARACTER_AND_SESSION_FAMILY_CURRENT_BUILD: PARTIAL_STATIC_REVALIDATION
LIVE_AUTH_SESSION_SEMANTICS: NOT_TESTED
RAW_CLIENT_RETAINED: false
```

This result is suitable for coordinator review and for future current-build helper/profile work only after the applicable current trusted-base fence, runtime admission, exact-object provenance and live authorization gates are satisfied.
