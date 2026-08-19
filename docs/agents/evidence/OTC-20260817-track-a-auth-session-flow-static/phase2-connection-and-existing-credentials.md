# Track A native auth/session static proof — phase 2

Task: `OTC-20260817-track-a-auth-session-flow-static`  
PR: `#498`  
Exact workflow head: `8407ba4dfe9a579212c321a6f72bd5a5838974ef`  
Workflow run: `32047982450`  
Source job: `95440215221` (`synology-otclient-01`) — SUCCESS  
Hosted decode job: `95440256167` (`ubuntu-24.04`) — SUCCESS  

## Scope

Phase 2 narrows three questions without runtime access:

1. exact `sendLoginMessage` connection setup around `0x7d564f`;
2. the concrete implementation behind `TGameClient::connectClientToGameserverWithExistingCredentials`;
3. selected-character transformation and game-session-connected implementation structure.

No credential/session value, live process, X11 state, login, packet payload or full executable was read or uploaded.

## Source-side safety proof

The exact retained client was fenced as:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The source job emitted:

```text
AUTHSESSION_PHASE2B_EXACT_FILE_FENCE=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_PHASE2B_SOURCE_PROCESS_OBSERVATION=false
AUTHSESSION_PHASE2B_SOURCE_X11_OBSERVATION=false
AUTHSESSION_PHASE2B_SOURCE_LOGIN=false
AUTHSESSION_PHASE2B_SOURCE_SECRET_ACCESS=false
AUTHSESSION_PHASE2B_SOURCE_DISASSEMBLY=false
AUTHSESSION_PHASE2B_SOURCE_SEMANTIC_CLASSIFICATION=false
AUTHSESSION_PHASE2B_RAW_CLIENT_UPLOADED=false
AUTHSESSION_PHASE2B_BOUNDED_FILE_WINDOWS_STAGED=true
```

Exact staged-window SHA-256 values:

```text
connect context       f62efd2249373577232045017fa7b50b988b0390e14cb369d012e3bdc785588d
existing credentials  050ff020dc1059d55af842ff416075723f87ea92633cb2e5f9eefa6cb3fd1172
connect implementation b4a7b3c494a44684835235775b26ddc1754727a909e06f15763d787efc8035b8
session connected     a999738212e70628a552c7df9351c13069155b58af5738ac72f2eb3524408b58
character helper      5f716667c2f4ea1b2e8d3b063255aebee254e4cfc986d165aea5debcb90dd885
character enclosing   40708740c8cb556dfb60e09da3612111888274e591acc9a40f6d44e53ca1e91e
login handlers        f6d396250780bc6c910c644d51a68695f0d24edb5121ee313418728c94672e95
```

Hosted decode emitted `AUTHSESSION_PHASE2B_HOSTED_DECODE=PASS` and `AUTHSESSION_RUNTIME_ACCESS=none`.

## FACT — exact connection site still requires object provenance

The compact exact-SHA slice around the previously promoted `QObject::connect` site contains:

```asm
7d55f0  lea rax,[rip+...]        # 0xcf2950  ; sendLoginMessage PMF
7d5600  mov [rsp+0x30],rax
...
7d562f  lea rax,[rip+...]        # 0x7d4220  ; QSlotObject trampoline
7d563b  mov [r9+0x8],rax
...
7d564f  call 0x4dd800
```

Immediately before the call, the call-site argument registers are populated from `rbp`, `r12`, `r13` and stack-resident values. This slice does **not** establish where those object registers were originally sourced.

Therefore the receiver behind the `0xbd36a0 -> vslot +0x68` adapter remains `UNKNOWN`; phase 1's rejected shortcut via the primary `TGameClient` vptr remains rejected.

## FACT — exact existing-credentials implementation entry

The named wrapper

```text
TGameClient::connectClientToGameserverWithExistingCredentials @ 0xd06660
```

jumps to `0x6ef1d0`. The exact implementation begins by testing TGameClient-owned state:

```asm
6ef1df  cmp QWORD PTR [rdi+0x6b8],0
6ef1ed  mov rax,QWORD PTR [rdi+0x418]
6ef1f9  cmp BYTE PTR [rax+0xec],0
```

One branch returns immediately. Another constructs a small callback-like object and dispatches through `0x4dedc0`.

When `[this+0x6b8] == 0`, the implementation instead executes:

```asm
6ef29b  mov r14,QWORD PTR [rdi+0xa38]
6ef2aa  call 0x861d30
6ef2b4  lea rsi,[rip+...]        # 0x1c96c11
6ef2be  call 0x4df740
6ef2cd  lea rsi,[rip+...]        # 0x1c96c28
6ef2d7  call 0x4df740
...
6ef2e5  mov rdi,r14
6ef2e8  call 0x88c2d0
```

### FACT boundary

The named method proves this code is part of the **existing-credentials connection path**. It does not yet prove what `[this+0xa38]`, the two static strings, or `0x88c2d0` represent.

## FACT — `onConnectClientToGameserver` consumes a large retained state aggregate

The named wrapper `TGameClient::onConnectClientToGameserver @ 0xd06810` jumps to `0x6fe480`.

The implementation starts by zero/initializing a large temporary object via `0x197ce10`, then moves/refcounts multiple TGameClient-owned aggregate members around offsets `+0xa78..+0xab8` and multiple aggregate members from the object at `[this+0x8d0]`, including offsets `+0x518`, `+0x530`, `+0x548`, `+0x560`, and `+0x578`.

Examples:

```asm
6fe4e0  call 0x197ce10
6fe4e5  mov rax,QWORD PTR [r13+0xa80]
6fe501  movdqu xmm1,XMMWORD PTR [r13+0xaa8]
6fe50a  mov rdx,QWORD PTR [r13+0xa78]
...
6fe545  mov rax,QWORD PTR [r13+0x8d0]
...
6fe596  mov rdx,QWORD PTR [rax+0x518]
6fe5ea  movdqu xmm2,XMMWORD PTR [rax+0x530]
6fe619  movdqu xmm3,XMMWORD PTR [rax+0x548]
6fe648  movdqu xmm1,XMMWORD PTR [rax+0x560]
6fe677  movdqu xmm2,XMMWORD PTR [rax+0x578]
```

### INFERENCE

Confidence: medium.

`onConnectClientToGameserver` is assembling a connection/session input aggregate from retained client state rather than requesting manual login-form data at this point. Exact field meanings — including whether any aggregate is password, token, ticket, endpoint, character metadata, or unrelated state — remain unproven and must not be named yet.

## FACT — `onGameSessionConnected` is a post-connect lifecycle transition

The named wrapper `TGameClient::onGameSessionConnected @ 0xd066e0` jumps to `0x6ee130`.

The exact body checks the object at `[this+0x8d0]`, calls a virtual at `+0x70`, clears/replaces several owned resources (`+0xc8`, `+0xe0`, later `+0x320`, `+0x338`) and dispatches through `0x4dedc0` using static object `0x3076560`.

This phase proves lifecycle/state transition structure only. It does not identify a login credential or serializer.

## FACT — selected-character helper produces a 24-byte managed result

`TCharacterSelectionController::requestCharacterLogin @ 0xd47300` passes:

```asm
movzx edx,WORD PTR [rdi+0x50]
mov   esi,DWORD PTR [rdi+0x54]
mov   rdi,output
call  0x858a50
```

`0x858a50` initializes the 24-byte destination (`[rdi]`, `[rdi+0x10]`), branches on `esi`, preserves the 16-bit input in `r15w`, constructs managed/static-string-backed values and repeatedly swaps a three-qword result into the destination.

It compares the 16-bit input against `0x0d` in one path. Exact field meanings are still `UNKNOWN`.

After return, `requestCharacterLogin` swaps the helper's three qwords into storage referenced by `r12` and calls `0x6b23c0`.

The identity/provenance of `r12` remains unresolved because the current enclosing slice starts after the function's setup.

## FACT — nearby login-handler code is dispatch/meta-object scaffolding, not a proven wire serializer

The exact `0xcf2e80..0xcf30e0` slice repeatedly constructs numbered dispatches through `0x4dedc0` using static objects `0x3085920` / `0x30b0f00`, including branches on small integer state values. Nothing in this slice proves ordered game-wire fields.

## Phase-2 dispositions

```text
EXACT_SENDLOGIN_RECEIVER=UNKNOWN
EXISTING_CREDENTIALS_IMPL=0x6ef1d0 PROVEN
ON_CONNECT_IMPL=0x6fe480 PROVEN
ON_SESSION_CONNECTED_IMPL=0x6ee130 PROVEN
SELECTED_CHARACTER_HELPER=0x858a50 PROVEN
FINAL_GAME_LOGIN_SERIALIZER=UNKNOWN
SESSION_CREDENTIAL_TYPE=UNKNOWN
PASSWORD_USED_AFTER_INITIAL_AUTH=UNKNOWN
```

## Next bounded static discriminator

Static evidence is still productive; runtime escalation is not justified yet.

Phase 3 should recover only:

1. the earlier `0x7d54xx..0x7d55ef` connection-function setup needed to provenance `rbp/r12/r13` and the two stack arguments at `0x7d564f`;
2. static string values at the already-proven RIP targets `0x1c96c11`, `0x1c96c28`, `0x1ce22c4`, `0x1ce3028`, `0x1ce22d0` (decoded only on GitHub-hosted Linux);
3. bounded implementations `0x88c2d0`, `0x861d30`, and `0x197ce10`;
4. direct/indirect call summaries for the remainder of the already-identified `0x6ef1d0` and `0x6fe480` functions, without broadening into unrelated binary scanning.
