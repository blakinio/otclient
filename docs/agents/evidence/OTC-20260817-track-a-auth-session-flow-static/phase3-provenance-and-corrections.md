# Track A native auth/session static proof — phase 3

Task: `OTC-20260817-track-a-auth-session-flow-static`  
PR: `#498`  
Exact workflow head: `a73354e60dee7f9a7a3e4ca956ba0404bd3c9ba0`  
Workflow run: `32048212912`  
Source job: `95440966391` (`synology-otclient-01`) — SUCCESS  
Hosted decode job: `95441008577` (`ubuntu-24.04`) — SUCCESS

## Scope

Phase 3 resolves exact connection-object provenance far enough to identify the sender and receiver member locations for `TLoginProtocolMessageHandler::sendLoginMessage`, classifies several previously ambiguous helper branches, and corrects one misleading character-selection lead. It remains a static exact-file proof with `runtime_access: none`.

## Source-side safety proof

Exact retained executable fence:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The source job emitted:

```text
AUTHSESSION_PHASE3_EXACT_FILE_FENCE=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_PHASE3_SOURCE_PROCESS_OBSERVATION=false
AUTHSESSION_PHASE3_SOURCE_X11_OBSERVATION=false
AUTHSESSION_PHASE3_SOURCE_LOGIN=false
AUTHSESSION_PHASE3_SOURCE_SECRET_ACCESS=false
AUTHSESSION_PHASE3_SOURCE_DISASSEMBLY=false
AUTHSESSION_PHASE3_SOURCE_SEMANTIC_CLASSIFICATION=false
AUTHSESSION_PHASE3_RAW_CLIENT_UPLOADED=false
AUTHSESSION_PHASE3_BOUNDED_FILE_WINDOWS_STAGED=true
```

Staged-window SHA-256 values:

```text
connect_prelude   ff9b5adfc2fa8fa286cfd2eec8d3d41a26c1d05ef7e4e931e6748b280781efa3
helper_88c2d0     57d0a644fdaa1685531d073aaff9622409a7a833dd80999d2287666665597020
helper_861d30     12ccb8b53bc310021ca5a6d9db2c7c55fd0cf1127231257f7f69fab0aa25cd7f
helper_197ce10    4a9f7fb1b27ae80980bfd4eab0f7e782da9b03cb4f518d2ff5cd7b32bc2b09b7
existing_tail     31c7335879405134ce12f69190910779c034bb5606c1abd8d9ddf8243332a5d5
connect_tail      a7d084838e47622244e831c64586cbd5b29f667d8616d90b1e809512834b2dea
strings_a         3f57a3cce1d7b6c53393b4942be00f8f698f7835843ad64644bd4a2a0c532990
strings_b         60394678fcc459b54135051e26a50c637fa873edea74b3d17a29f551be0a6f79
strings_c         4651340f88e0e607bf7d508345663112adf002ed5b2689d0a5bcda6ad5108dde
```

Hosted decode emitted `AUTHSESSION_PHASE3_HOSTED_DECODE=PASS` and `AUTHSESSION_RUNTIME_ACCESS=none`.

## FACT — exact sender and receiver member provenance

The previously promoted corrected SysV mapping for `QObject::connectImpl` includes the hidden structure-return argument:

```text
rdi hidden return storage
rsi sender
rdx signal PMF storage
rcx receiver
r8 slot PMF storage
r9 QSlotObjectBase*
stack connection type / types / sender QMetaObject
```

The exact phase-3 prelude immediately before the `sendLoginMessage` connection contains:

```asm
7d559c  lea r15,[rip+...]        # 0x3084fa0
...
7d55c8  mov rcx,QWORD PTR [rbx+0x88]
7d55d4  mov rsi,QWORD PTR [rbx+0x9c0]
7d55e4  lea rax,[rip+...]        # 0xbd36a0
7d55eb  mov QWORD PTR [rsp+0x20],rax
```

The already-proven continuation loads `0xcf2950` (`TLoginProtocolMessageHandler::sendLoginMessage` signal PMF), installs trampoline `0x7d4220`, and calls `QObject::connectImpl` at `0x7d564f`.

Therefore, for this exact connection:

```text
sender   = *(enclosing_object + 0x9c0)
receiver = *(enclosing_object + 0x88)
sender QMetaObject = 0x3084fa0 = TLoginProtocolMessageHandler
captured slot adapter = 0xbd36a0
adapter next dispatch = *(receiver_vptr + 0x68)
```

The exact class of `enclosing_object` and the exact receiver class/vptr remain `UNKNOWN`. They must be recovered from the enclosing function/constructor provenance; guessing `TGameClient` from object size/layout is not sufficient proof.

## FACT — primary `TGameClient` vptr shortcut remains rejected

Phase 1 proved that primary `TGameClient` vptr `0x3076908` has `+0x68 -> 0x6cc7b0`, a large construction-heavy routine. Phase 3 now proves the actual receiver is specifically the object stored at `[enclosing+0x88]`.

No evidence yet proves that member uses the primary `TGameClient` vptr. The final serializer path must therefore continue from the actual member object identity, not from `TGameClient` primary vptr.

## FACT — `0x88c2d0` observed branch is connecting-UI/localization work

Phase 2 showed `connectClientToGameserverWithExistingCredentials @ 0x6ef1d0` reaches `0x88c2d0` in one branch after constructing two static strings. Phase 3 decoded those exact strings:

```text
0x1c96c11 = connecting_description
0x1c96c28 = connecting_caption
```

`0x88c2d0` itself accesses object-owned translation/observer containers and repeatedly routes formatted values through helper calls. In this proven caller context it is a connecting-dialog/localization path, not evidence of a password/session credential serializer.

### Correction

Any prior interpretation of the two arguments passed to `0x88c2d0` as possible credential/session strings is rejected.

## FACT — `0x858a50` is character-selection status presentation, not a proven network handoff

The exact strings used by `0x858a50` were decoded as:

```text
0x1ce22c4 = %1 (%2%4%3)
0x1ce22d0 = <font color=%1>
0x1ce22e0 = </font>
0x1ce3028 = characterselection_status_premium
```

The routine builds/swaps a managed 24-byte result and performs formatting/color/status operations around these literals.

### Correction — material

The earlier inference that `0x858a50` was a selected-character transport/credential transformation helper is rejected.

The historical locator labelled `TCharacterSelectionController::requestCharacterLogin @ 0xd47300` must be revalidated before it is used as a native game-login handoff proof. At the exact observed body, the path through `0x858a50` is character-selection UI/status presentation.

## FACT — `0x197ce10` is a generic aggregate/container initializer

The routine initializes an object with capacity-like value `8`, allocates `0x40` and `0x200` regions, then stores pointer ranges/metadata. This supports only a generic container/aggregate-construction classification. It does not establish credential semantics for `0x6fe480`.

## FACT — `0x6ef1d0` remains an existing-credentials connection state-machine implementation

The exact named wrapper `TGameClient::connectClientToGameserverWithExistingCredentials @ 0xd06660` still jumps to `0x6ef1d0`.

The expanded tail shows multiple local virtual/Qt dispatches and state constants, including calls through `vtable+0x68`, but none is yet tied to a proven credential field or final wire writer. One later path reaches `0xcae030` and a still-unresolved static string at `0x1c96e88`.

Therefore:

```text
EXISTING_CREDENTIALS_CONTROL_PATH=PROVEN
EXISTING_CREDENTIAL_TYPE=UNKNOWN
PLAINTEXT_PASSWORD_PARTICIPATION=UNKNOWN
FINAL_WIRE_SERIALIZER=UNKNOWN
```

## FACT — `0x6fe480` assembles retained state but its final protocol role remains unproven

The expanded body continues copying/refcounting many retained aggregates and later calls `0x6fc020` and `0x6e9d90`, among cleanup/container operations. Nothing in the current bounded evidence proves an ordered login packet field contract.

## Dispositions after phase 3

```text
SENDLOGIN_SENDER_MEMBER=enclosing+0x9c0 PROVEN
SENDLOGIN_RECEIVER_MEMBER=enclosing+0x88 PROVEN
SENDLOGIN_RECEIVER_CLASS=UNKNOWN
SENDLOGIN_RECEIVER_VPTR=UNKNOWN
SENDLOGIN_VSLOT_PLUS_0X68_TARGET=UNKNOWN
PRIMARY_TGAMECLIENT_VPTR_AS_RECEIVER=NOT_PROVEN_AND_SHORTCUT_REJECTED
0x88c2d0_CONNECTING_UI_ROLE=PROVEN_IN_OBSERVED_CALLER_CONTEXT
0x858a50_CHARACTER_STATUS_UI_ROLE=PROVEN
0xd47300_AS_NETWORK_REQUEST_CHARACTER_LOGIN=REQUIRES_REVALIDATION
FINAL_GAME_LOGIN_SERIALIZER=UNKNOWN
SESSION_CREDENTIAL_TYPE=UNKNOWN
PASSWORD_USED_AFTER_INITIAL_AUTH=UNKNOWN
```

## Next bounded static discriminator

Static work is still producing causal evidence; runtime escalation is not justified.

Phase 4 should:

1. recover the enclosing object/function provenance before `0x7d5400` and test whether the enclosing object is structurally proven `TGameClient` or another class;
2. identify the object created/stored at `enclosing+0x88`, then recover its exact vptr and `vptr+0x68` target;
3. decode already-referenced static strings `0x1c96d0b`, `0x1c96e88`, `0x1ce7262`, `0x28a7c92`, `0x1d91113` only on GitHub-hosted Linux;
4. revalidate the authentication-process/character-login method map from exact QMeta metadata rather than trusting the old `0xd47300` label;
5. follow only proven call edges from the existing-credentials control path toward a final outbound writer.
