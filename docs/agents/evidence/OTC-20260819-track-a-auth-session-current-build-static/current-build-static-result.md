# TIBIA-RE-AUTH-SESSION — promoted current-build static result

```yaml
task: OTC-20260819-track-a-auth-session-current-build-static
source_pr: 556
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
source_run: 32228900775
source_job: 95994337407
coordinator_review: 4970802493
coordinator_decision: ACCEPT_WITH_EDITS
independent_strict_run: 32239540646
runtime_access: none
client_executed: false
login_performed: false
credentials_accessed: false
raw_client_retained: false
```

This is the coordinator-promoted form of source #556 evidence. It preserves the source's exact-build static findings, applies the independently verified QMeta `METHOD` versus `SIGNAL` distinction, and removes stale lifecycle wording about the current-client fence.

## Exact current public build fence

The source workflow independently fetched the public Linux package and verified:

```yaml
packed_size: 10214529
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_size: 52109920
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Current trusted fence authority is PR #555 squash merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` plus lifecycle closeout #561. The SHA/size pair is exact executable identity; `15.32` remains only the bounded version-family token recorded by current governance.

Source producer job `32228900775 / 95994337407` uploaded no artifact. The retained raw producer evidence is the GitHub Actions job log plus the sanitized source document. The raw packed/unpacked client was deleted before job completion and was not uploaded.

Safety markers reproduced from the source job:

```text
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_CLIENT_EXECUTED=false
AUTHSESSION_LOGIN_PERFORMED=false
AUTHSESSION_SECRET_ACCESS=false
AUTHSESSION_RAW_CLIENT_UPLOADED=false
AUTHSESSION_RAW_CLIENT_RETAINED=false
```

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

The cold-auth entry is uniquely present:

```text
name               = onRequestLoginWithCredentials
meta_index         = 17
role               = METHOD
argc               = 2
method_flags       = 0x8
raw_param_type_ids = 0x2b,0xa,0xa
semantic signature = void(QString, QString)
```

## FACT — independently proven `TGameClient` method dispatch targets

Coordinator strict run `32239540646` independently re-fetched the same exact build and required one complete Qt invoke switch chain:

```text
0xd19104: cmp edx, 0x2b
0xd1910a: lea rsi, [rip + 0x10772b3]
0xd1911b: movsxd rax, dword ptr [rsi + rdx*4]
0xd1911f: add rax, rsi
0xd19122: jmp rax
jump table = 0x1d903c4
```

The complete 44-entry table resolved to executable targets and proved:

```text
TGameClient::onRequestLoginWithCredentials
  QMeta index = 17
  role = METHOD
  target = 0xd196f0
  instruction fence32 = 488b5110488b71084883c4485b5de93d609cff0f1f440000488bbfa009000048

TGameClient::connectClientToGameserverWithExistingCredentials
  QMeta index = 11
  role = METHOD
  argc = 0
  target = 0xd19500
  instruction fence16 = 4883c4485b5de9658c9cff0f1f440000
```

These are exact-build QMeta method dispatch targets. This static package does **not** establish live object provenance, Qt thread affinity, helper call safety, authentication success, or game-world entry.

## FACT — exact-build QMeta signal activation dispatch targets

Independent strict audit also proved the QMeta role of two source entries that must not be described as ordinary business-method implementations.

### `TLoginRequestUploader::loginSuccessful`

```text
static_metacall = 0xd0ffe0
method_count = 9
signal_count = 8
QMeta index = 0
role = SIGNAL
argc = 3
target = 0xd10200
instruction fence16 = 488b5310488b4b08488d35916c270248
```

Strict switch proof:

```text
0xd0ffef: cmp edx, 8
0xd0fff4: lea rcx, [rip + 0x107fff1]
0xd10000: movsxd rax, dword ptr [rcx + rdx*4]
0xd10004: add rax, rcx
0xd10007: jmp rax
```

`0xd10200` is promoted only as the exact-build QMeta **signal activation dispatch target** for `loginSuccessful`, not as a call-safe login-success business implementation.

### `TCharacterSelectionController::requestCharacterLogin`

```text
static_metacall = 0xd51c70
method_count = 26
signal_count = 10
QMeta index = 0
role = SIGNAL
argc = 1
target = 0xd52050
instruction fence16 = 498b442408f30f6f08488b100f298c24
```

Strict switch proof:

```text
0xd51c8b: cmp edx, 0x19
0xd51c90: lea rcx, [rip + 0x104734d]
0xd51c99: movsxd rax, dword ptr [rcx + rdx*4]
0xd51c9d: add rax, rcx
0xd51ca0: jmp rax
```

`0xd52050` is promoted only as the exact-build QMeta **signal activation dispatch target** for `requestCharacterLogin`, not as a call-safe character-login business implementation.

## FACT — bounded structural family survives on the current build

Source producer string inventory found all 19 declared target names in the exact current binary:

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

Result marker from the producer:

```text
AUTHSESSION_CURRENT_STRUCTURAL_STRING_TARGETS_PRESENT=19/19
AUTHSESSION_CURRENT_STATIC_DISCRIMINATOR=PASS
```

For names not independently QMeta/dispatch-bound above, this proves **structural name/type presence only**. It does not assign an executable target or establish semantic provenance.

## SUPERSEDED — historical old-build addresses

The following addresses remain valid evidence only for the prior `51965216 / e6c244bd...` executable and are `SUPERSEDED_FOR_CURRENT_BUILD` unless separately rediscovered on the current SHA:

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

## UNKNOWN / not promoted by this bounded slice

- exact current executable targets for non-QMeta methods such as `advanceStateMachineDirectlyToCharacterSelection`, `requestCharacterGameserverLogin`, and `onStartGameServerLoginStateEntered`;
- current `TPlaySessionData` / `TAuthenticationAndEncryptionInfo` field provenance;
- whether password material is required in the game-server-login message on the current build;
- live object addresses, vptr instances, Qt thread affinity and helper call safety;
- login success, character selection, game-server connection or causal `IN_GAME`;
- restart/relogin/update/session-retention stability.

## Coordinator disposition

```yaml
STATUS: PROMOTED_STATIC_EVIDENCE_PENDING_PR_MERGE
ALIAS: TIBIA-RE-AUTH-SESSION
RUNTIME_ACCESS: none
CURRENT_BUILD_STATIC_REVALIDATION: PASS
COLD_AUTH_QMETA_CURRENT_BUILD: PROVEN_STATIC_EXACT_BUILD
CHARACTER_AND_SESSION_FAMILY_CURRENT_BUILD: PARTIAL_STATIC_REVALIDATION
LIVE_AUTH_SESSION_SEMANTICS: NOT_TESTED
COORDINATOR_DECISION: ACCEPT_WITH_EDITS
OPEN_MATERIAL_FINDINGS_AFTER_REPAIR: 0
RAW_CLIENT_RETAINED: false
```

Detailed independent audit provenance is retained in the sibling `OTC-20260819-track-a-auth-session-current-build-static-promotion` evidence directory.
