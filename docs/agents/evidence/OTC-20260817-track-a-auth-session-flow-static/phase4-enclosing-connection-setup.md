# Track A native auth/session static proof — phase 4

Task: `OTC-20260817-track-a-auth-session-flow-static`  
PR: `#498`  
Exact workflow head: `ec4991331d8b74abdc5b296a58e370a0036f3f7e`  
Workflow run: `32048719394`  
Source job: `95442611445` (`synology-otclient-01`) — SUCCESS  
Hosted decode job: `95442653919` (`ubuntu-24.04`) — SUCCESS

## Scope

Phase 4 tests whether the connection-setup function itself directly proves the enclosing class via the promoted `TGameClient` primary vptr/typeinfo and extends exact member provenance around `[this+0x88]` / `[this+0x9c0]`. It also classifies several static strings reached by earlier ambiguous branches.

## Safety proof

Exact retained executable fence:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Source markers:

```text
AUTHSESSION_PHASE4_EXACT_FILE_FENCE=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_PHASE4_SOURCE_PROCESS_OBSERVATION=false
AUTHSESSION_PHASE4_SOURCE_X11_OBSERVATION=false
AUTHSESSION_PHASE4_SOURCE_LOGIN=false
AUTHSESSION_PHASE4_SOURCE_SECRET_ACCESS=false
AUTHSESSION_PHASE4_SOURCE_DISASSEMBLY=false
AUTHSESSION_PHASE4_SOURCE_SEMANTIC_CLASSIFICATION=false
AUTHSESSION_PHASE4_RAW_CLIENT_UPLOADED=false
AUTHSESSION_PHASE4_BOUNDED_FILE_WINDOWS_STAGED=true
```

Staged-window hashes:

```text
setup_a   287108428dcf9bb6158fb50a7f7081258ac71c22f72d6bc989d2080846b66ddd
setup_b   6df9024904b8dd8bae8cdbe9dcfa6c6330027d672b8830ea04a1fa5a0fb1eed8
strings_d 93dc782c9717bf48c82b9a37cd91839df2f8d46b49c5c16a386131023add0468
strings_e f94b315b200c687164967d592e4a56881b9de7c0e8d24329ad421c46c131d521
strings_f a127134e03e1c071613238e14378307df8bedc6256501158190d903b3377fc84
strings_g de2c8aa38192cb13e640d78193af69c30f6efec9204778f60e73d16c53e97873
```

Hosted marker: `AUTHSESSION_PHASE4_HOSTED_DECODE=PASS` with `AUTHSESSION_RUNTIME_ACCESS=none`.

## FACT — connection setup is one `this`-based function

The exact bounded setup contains a function beginning at `0x7d51bb`:

```asm
7d51bb  lea r14,[rip+...]        # 0x3085b60
7d51c2  push r13
7d51c4  push r12
7d51c6  push rbp
7d51c7  push rbx
7d51c8  mov rbx,rdi
7d51cb  sub rsp,0x48
7d51cf  mov rcx,QWORD PTR [rdi+0xc58]
7d51d6  mov r15,QWORD PTR [rdi+0x88]
```

Later in the same function:

```asm
7d5265  mov rdi,rbx
7d5268  call 0x7f6bc0
7d526d  mov rsi,QWORD PTR [rbx+0x88]
...
7d5285  mov r15,QWORD PTR [rbx+0x9c0]
...
7d52ea  call 0x4dd800
...
7d52fb  mov rsi,QWORD PTR [rbx+0x88]
...
7d530e  mov r15,QWORD PTR [rbx+0x9c0]
...
7d5378  call 0x4dd800
...
7d5389  mov rsi,QWORD PTR [rbx+0x88]
...
7d539c  mov r15,QWORD PTR [rbx+0x9c0]
```

Phase 3 already proves the later `sendLoginMessage` connection in this same member pattern has:

```text
sender   = [this+0x9c0]
receiver = [this+0x88]
```

Therefore the connection graph is not an isolated one-off expression; it is constructed inside one method whose first argument is retained as `this` in `rbx`, with repeated connections between the same two object members.

## FACT — no direct promoted TGameClient primary-vptr/typeinfo hit in the tested setup windows

The hosted exact-address discriminator searched `0x7d3400..0x7d5400` for RIP references to:

```text
TGameClient primary vptr 0x3076908
TGameClient typeinfo     0x3070398
TLoginProtocolMessageHandler QMetaObject 0x3084fa0
```

and emitted no known-ref hit in either bounded setup chunk.

### Disposition

```text
ENCLOSING_CLASS=TGameClient  NOT_PROVEN
```

Absence of those direct references is not negative proof that the object cannot be `TGameClient`; this function may be a non-constructor setup method. It means only that this exact discriminator cannot establish the class.

## FACT — new static QMeta-like lead at `0x3085b60`

The setup method begins by loading static address `0x3085b60` into `r14`. The current phase does not assign its type or class name. It is the strongest bounded data-provenance lead for Phase 5.

## FACT — previously ambiguous strings are non-credential UI/state labels

Exact hosted string decoding produced:

```text
0x1c96d0b = cancel
0x1c96e88 = launcher_start_pointless_due_to_files_uptodate
0x1ce7262 = textCentered
0x28a7c92 = caption
0x1d91113 = message
```

This further rejects credential semantics for the observed UI/helper branches that reference these literals.

## Current disposition

```text
SENDLOGIN_SENDER_MEMBER=this+0x9c0                  PROVEN
SENDLOGIN_RECEIVER_MEMBER=this+0x88                 PROVEN
CONNECTION_SETUP_FUNCTION_START=0x7d51bb             PROVEN_IN_BOUNDED_WINDOW
ENCLOSING_CLASS=UNKNOWN
RECEIVER_CLASS=UNKNOWN
RECEIVER_VPTR=UNKNOWN
RECEIVER_VSLOT_PLUS_0X68_TARGET=UNKNOWN
STATIC_LEAD_0x3085b60=PROVEN_REFERENCE_TYPE_UNKNOWN
FINAL_GAME_LOGIN_SERIALIZER=UNKNOWN
SESSION_CREDENTIAL_TYPE=UNKNOWN
PASSWORD_USED_AFTER_INITIAL_AUTH=UNKNOWN
```

## Next bounded static discriminator

Phase 5 should remain static and exact-fenced:

1. stage the small static-data neighborhood around `0x3085b60` and decode its qword/relative metadata structure on GitHub-hosted Linux;
2. use only the exact references recovered from that structure to stage the minimal class-name/QMeta data required for identity;
3. recover caller/construction provenance for `0x7d51bb` only if the metadata does not identify the enclosing class;
4. once the enclosing class is proven, trace creation/storage of member `+0x88` and recover that object's exact vptr and `+0x68` target.

No runtime escalation is justified yet.
