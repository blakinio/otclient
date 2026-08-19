# Track A native auth/session static proof — phase 1

Task: `OTC-20260817-track-a-auth-session-flow-static`  
PR: `#498`  
Exact workflow head: `053a5717a6d9306f70c80e61164e144e4143d075`  
Workflow run: `32047266485`  
Source job: `95437930193` (`synology-otclient-01`)  
Hosted decode job: `95437962909` (`ubuntu-24.04`)  

## Scope

Phase 1 answers one structural question first: whether the already-promoted primary `TGameClient` vptr candidate can explain the proven `TLoginProtocolMessageHandler::sendLoginMessage -> 0xbd36a0 -> receiver virtual slot +0x68` route, while also opening bounded static windows around the known character-selection and game-login transition leads.

No runtime/login observation is part of this evidence.

## Source-side safety proof

The source job completed successfully after exact-fencing the retained official client:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The job emitted:

```text
AUTHSESSION_EXACT_FILE_FENCE=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_SOURCE_PROCESS_OBSERVATION=false
AUTHSESSION_SOURCE_X11_OBSERVATION=false
AUTHSESSION_SOURCE_LOGIN=false
AUTHSESSION_SOURCE_SECRET_ACCESS=false
AUTHSESSION_SOURCE_DISASSEMBLY=false
AUTHSESSION_SOURCE_SEMANTIC_CLASSIFICATION=false
AUTHSESSION_RAW_CLIENT_UPLOADED=false
AUTHSESSION_BOUNDED_FILE_WINDOWS_STAGED=true
```

Exact staged-window SHA-256 values:

```text
TGameClient vtable       bdd31539ac62e274db7b1e8c4f9cf8947e85812ebffc865c0dc8bd8d62cc844f
0xbd36a0 adapter window  fe80e2f80221dd129f30d29e2fa4bd0549bafeb9b6f9dbb8c279f43164020d1e
auth-controller window   c29849e71f2a2591a9bcc5985d90a89a4399eca5a3933070a21b1a9c3ad49d69
character-select window  2ef01d5190388f539c2348aad9a5b6fbacffda683d31b2185256edb17dd2d653
game-client window       aa3ef361862bb418c7c75f04fcaf68c5d64344a4ddf4a619b5cfc3409c929121
game-login-controller    0b2750b8c8e9c103c4b4b4358678d1d1f6b2883d82e7a9c11b40a95fd19c0eae
vslot target window      1b15b6626729d2ec9d65e0c39dc188febf67f371e7986be5e7679c5c83dc11ac
```

## FACT — hosted decode boundary

The GitHub-hosted job completed successfully and emitted:

```text
AUTHSESSION_HOSTED_DECODE=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_TGAMECLIENT_VPTR=0x3076908
AUTHSESSION_TGAMECLIENT_TYPEINFO=0x3070398
AUTHSESSION_TGAMECLIENT_VSLOT_PLUS_0X68_TARGET=0x6cc7b0
```

Therefore the exact-SHA primary `TGameClient` address point `0x3076908`, if used as the receiver vptr, resolves virtual slot `+0x68` to `0x6cc7b0`.

## FACT — `0xbd36a0` remains a delegating adapter

The new decode independently reproduces the already-promoted structural boundary:

```asm
bd37f3  mov rax,QWORD PTR [r12]
bd37f7  mov rax,QWORD PTR [rax+0x68]
...
bd381e  mov rdi,r12
bd3821  call rax
```

The adapter constructs/interprets an intermediate object before the call. This phase does not assign wire-field meanings to that intermediate.

## FACT — primary `TGameClient` `+0x68` target is construction-heavy

The exact target `0x6cc7b0` begins with a large routine that allocates and installs numerous owned objects/callback structures. Selected structural instructions include:

```asm
6cc7b0  push rbp
6cc7c7  call 0x6cc1c0
6cc7cc  mov edi,0x18
6cc7d1  call 0x4df670
6cc7dd  mov rdi,QWORD PTR [rbx+0x6d0]
...
6cc934  mov edi,0x78
6cc939  call 0x4df670
...
6cca0c  mov edi,0x60
6cca11  call 0x4df670
...
6ccb1a  mov edi,0x20
6ccb23  call 0x4df670
...
6ccbb4  mov edi,0x28
6ccbb9  call 0x4df670
...
6ccc44  mov edi,0x20
6ccc5d  call 0x4df670
```

It initializes many `rbx` members such as `+0x6c8/+0x6d0`, `+0x6e8/+0x6f0`, `+0x2c8/+0x2d0`, `+0xa28/+0xa30`, and installs multiple type/vtable-like pointers.

### INFERENCE — receiver identity is not established by the `TGameClient` vptr lead

Confidence: high.

The `0x6cc7b0` body is structurally inconsistent with treating the primary `TGameClient +0x68` target as an already-proven small game-login serializer. This does **not** by itself prove that the signal receiver can never be a `TGameClient` subobject; it proves that the promoted primary vptr lead is insufficient to identify the receiver used by `0xbd36a0`.

The actual receiver must therefore be recovered from the exact connection setup / object provenance around the promoted `QObject::connect` site rather than guessed from the class-name vptr profile.

Rejected hypothesis:

```text
H1-old: 0xbd36a0 receiver == object using primary TGameClient vptr 0x3076908,
        and primary-vptr +0x68 directly names the final game-login send path.
DISPOSITION: REJECTED AS UNSUPPORTED BY EXACT STATIC DECODE.
```

## FACT — known game-client wrappers expose concrete implementation targets

The bounded `TGameClient` window resolves three named wrapper leads to real code targets:

```asm
# TGameClient::connectClientToGameserverWithExistingCredentials @ 0xd06660
d06660  add rsp,0x48
...
d06666  jmp 0x6ef1d0

# TGameClient::onGameSessionConnected @ 0xd066e0
d066e0  add rsp,0x48
...
d066e6  jmp 0x6ee130

# TGameClient::onConnectClientToGameserver @ 0xd06810
d06810  add rsp,0x48
...
d06816  jmp 0x6fe480
```

These three exact targets are stronger next probes than guessing the serializer from the primary vtable.

## FACT — character-selection lead carries bounded selected-character state

At `TCharacterSelectionController::requestCharacterLogin @ 0xd47300`, the exact window shows:

```asm
d4731a  mov eax,DWORD PTR [rdi+0x58]
d47325  cmp eax,0x1
d4732e  cmp eax,0x2
d47337  movzx edx,WORD PTR [rdi+0x50]
d4733b  mov esi,DWORD PTR [rdi+0x54]
d4733e  mov rdi,rbp
d47341  call 0x858a50
...
d4734e  mov rax,QWORD PTR [r12]
...
d47355  mov QWORD PTR [r12],rdx
...
d47369  mov rax,QWORD PTR [r12+0x8]
...
d4736e  mov QWORD PTR [r12+0x8],rdx
...
d47383  mov rax,QWORD PTR [r12+0x10]
...
d47388  mov QWORD PTR [r12+0x10],rdx
```

### INFERENCE

Confidence: medium.

`requestCharacterLogin` transforms state containing a word at `+0x50`, dword at `+0x54`, and mode/state dword at `+0x58` through `0x858a50`, then moves a three-qword result into storage referenced by `r12`. Exact field meanings and the identity of `r12` remain unproven because the enclosing function prologue is outside the first bounded window.

## FACT — authentication state controller exposes request/state transitions

The exact authentication-controller window contains:

```asm
# onStartGameServerLoginStateEntered lead
cfb122  ...
cfb12a  jmp 0x767440

# requestCharacterGameserverLogin lead
cfb2e7  xor ecx,ecx
cfb2e9  mov edx,0x5
cfb2ee  jmp 0xcfad74
```

No credential semantics are assigned to state id `5` from this alone.

## Unknown after phase 1

- exact receiver object/vptr behind `0xbd36a0`;
- exact semantics of `0x6ef1d0`, `0x6fe480`, `0x6ee130`;
- exact semantics of `0x858a50` and the `r12` destination in `requestCharacterLogin`;
- final game-login serializer and ordered fields;
- initial account-auth request/response parser;
- session credential family and lifetime;
- whether plaintext password participates after initial auth;
- reconnect / logout / change-character credential behavior.

## Next bounded static discriminator

Phase 2 should exact-fence and stage only:

1. the `QObject::connect`/receiver-provenance window around `0x7d564f`;
2. `0x6ef1d0` (`connectClientToGameserverWithExistingCredentials` implementation);
3. `0x6fe480` (`onConnectClientToGameserver` implementation);
4. `0x6ee130` (`onGameSessionConnected` implementation);
5. `0x858a50` plus enough of the enclosing `TCharacterSelectionController` body to identify `r12`;
6. a small `0xcf2e80..` handler window if required to resolve the gameserver login controller transition.

No runtime escalation is justified yet because the static route is still producing discriminating evidence.
