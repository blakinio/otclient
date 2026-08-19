# Phase 5 — final native game-login auth-state provenance

Task: `OTC-20260817-track-a-native-game-login-credential-proof`

## Scope and safety fence

This phase is the terminal synthesis of the authorized static-only Track A scope. No live Tibia login, process-memory inspection, X11 observation, packet capture, credential value, token value, cookie value, or PR #475 runtime/session was used.

```text
client_version=15.32.df7b29
client_size=51965216
client_sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_access=none
login_performed=false
secret_access=false
process_x11_observation=false
```

The final narrow run also revalidated the packed download SHA and the decompressed exact-client SHA before promoting any address or type claim.

## Evidence progression

The final producer/provenance sequence was intentionally narrowed after the wire-format phases:

| Run | Result | Purpose |
|---|---|---|
| `32061277638` | SUCCESS | locate exact producer/call boundaries |
| `32062679049` | FAIL-CLOSED | attempt descriptor recovery; no promotable embedded `FileDescriptorProto` material |
| `32062920499` / job `95488112835` | SUCCESS | bounded producer value flow and RTTI/vtable identity |
| `32063272999` | SUCCESS | bounded `TAuthenticationAndEncryptionInfo` provenance/structure |
| `32063542030` | FAIL-CLOSED | direct retained-field writer xrefs; method was not suitable for virtual access |
| `32063751865` | SUCCESS | recover post-auth QMeta dispatch |
| `32064075257` | SUCCESS | isolate authentication-controller receiver cases |
| `32066254378` / job `95498969337` | SUCCESS | final narrow receiver/provenance discriminator |

Failed runs are negative methodological evidence only; they are not semantic evidence that a field or credential is absent.

## FACT — native producer and retained source type

Run `32062920499` recovered the exact source-object vtable candidate used by the producer:

```text
VTABLE_BASE=0x2f63240
TYPEINFO=0x3077840
TYPE=tibia::authentication::TAuthenticationAndEncryptionInfo
```

The same run recovered `0xe1abe0` as a virtual function owned by:

```text
TYPE=tibia::authentication::TLoginProtocolMessageHandler
VTABLE_BASE=0x3084e00
SLOT=0x60
FUNCTION=0xe1abe0
```

The bounded disassembly at `0xe1abe0` proves that this one native producer contains both branches:

```text
primary:
  GameclientMessageLogin vptr       0x30c84a0
  LoginRSAEncryptedBlock vptr       0x30c8428

secondary:
  GameclientMessageSecondaryLogin   vptr 0x30c6628
  SecondaryLoginRSAEncryptedBlock   vptr 0x30c65b0
```

The producer reads multiple retained string-like/value regions from the `TAuthenticationAndEncryptionInfo` source object, including fast-path offsets in the `+0xd0 .. +0x170` range, and writes them into the primary/secondary protobuf structures. Exact semantic field names for those retained values are not present in promotable descriptor material.

## FACT — complete native transport chain proved by this task

Combining Phases 1–4 with the producer proof:

```text
TAuthenticationAndEncryptionInfo retained values
    -> TLoginProtocolMessageHandler producer @ 0xe1abe0
    -> GameclientMessageLogin
       -> field 7: LoginRSAEncryptedBlock
    -> TProtocolMessageQueue::sendLogin(GameclientMessageLogin)
    -> QMeta target 0xdf6be2
    -> queue consumer 0xbd36a0
```

The secondary branch is separately represented as:

```text
TAuthenticationAndEncryptionInfo retained values
    -> TLoginProtocolMessageHandler producer @ 0xe1abe0
    -> GameclientMessageSecondaryLogin
       + SecondaryLoginRSAEncryptedBlock
    -> TProtocolMessageQueue::sendSecondaryLogin(...)
    -> QMeta target 0xdf7da5
    -> queue consumer 0xbf3990
```

This prevents the secondary/challenge credential path from being mistaken for the initial account-auth form credential.

## FACT — final controller receiver discriminator

Final run `32066254378`, job `95498969337`, completed successfully with:

```text
FINAL_PROVENANCE_EXACT_CLIENT_SHA=PASS
FINAL_PROVENANCE_RUNTIME_ACCESS=none
FINAL_PROVENANCE_LOGIN_PERFORMED=false
FINAL_PROVENANCE_SECRET_ACCESS=false
FINAL_CONTROLLER_METADATA=S:0x1cae3e0,M:0x1cae1e0,METHODS:10,SIGNALS:2
FINAL_RECEIVER_METHOD index=6 name=onLoginFinishedSuccessfullyEntered argc=0
FINAL_RECEIVER_METHOD index=9 name=onConfirmationCodeLoginSuccessful argc=0
FINAL_AUTHINFO_VTABLE=0x2f63240
FINAL_CASE name=onLoginFinishedSuccessfullyEntered va=0xcfa63d
FINAL_CASE name=onConfirmationCodeLoginSuccessful va=0xcfa69d
FINAL_PLAYSESSION_RECEIVER_PROBE=PASS
```

No promoted controller receiver method in that QMeta table carried `TPlaySessionData` in its decoded signature, and the bounded receiver bodies did not produce an `AUTHINFO_VTABLE_TARGET` marker establishing a direct `TPlaySessionData -> TAuthenticationAndEncryptionInfo` write.

That is a limitation of the recovered static provenance path, not proof that such a transfer does not exist.

## Terminal decision

```text
GAME_LOGIN_MESSAGE_TYPE: GameclientMessageLogin                    FACT
PROTECTED_LOGIN_BLOCK: LoginRSAEncryptedBlock in field 7           FACT
NATIVE_PRODUCER: TLoginProtocolMessageHandler @ 0xe1abe0            FACT
RETAINED_SOURCE_TYPE: TAuthenticationAndEncryptionInfo              FACT
RETAINED_SOURCE_VTABLE: 0x2f63240                                   FACT
SECONDARY_LOGIN_RELATION: separate message + separate RSA block     FACT
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
PASSWORD_ABSENT_FROM_GAME_LOGIN: NOT PROVEN
PASSWORD_PRESENT_IN_GAME_LOGIN: NOT PROVEN
```

### Why `PASSWORD_REQUIRED_FOR_GAME_LOGIN` remains `UNKNOWN`

Static exact-client evidence proves that the game-login message is populated from retained `TAuthenticationAndEncryptionInfo` state. It does **not** prove the semantic origin of every retained string-like field, specifically whether any such field is the account password, is derived from it, or instead consists entirely of post-auth/session/challenge material.

The known initial-auth boundary `TLoginRequestUploader::loginSuccessful(TCharacterList, TWorldList, TPlaySessionData)` and the native existing-credentials/session path are strong architectural context, but this task did not recover a direct static `TPlaySessionData -> TAuthenticationAndEncryptionInfo -> specific RSA field` assignment. Therefore promoting `PASSWORD_REQUIRED_FOR_GAME_LOGIN=NO` would exceed the evidence.

## INFERENCE

**High-confidence inference:** the native architecture is designed around retained authentication/encryption state for game-server login, rather than reading credentials directly from login-form widgets at the send boundary.

Falsifier: an exact-client producer/writer proof showing that one of the retained values used by `0xe1abe0` is populated from the account-password value and remains required for game-server login.

This inference does not alter the terminal `UNKNOWN` above.

## Remaining discriminator outside this task

The authorized `runtime_access:none` static lane is exhausted. A future task may resolve the remaining semantic question only with a new, explicit admission and a provenance-only method that records categories/edges rather than secret values. It must not inherit or reuse PR #475 runtime/session authority implicitly.

No further static probe is planned under `OTC-20260817-track-a-native-game-login-credential-proof`.
