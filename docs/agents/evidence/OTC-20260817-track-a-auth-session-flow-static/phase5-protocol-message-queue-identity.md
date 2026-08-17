# Track A native auth/session static proof — phase 5

Task: `OTC-20260817-track-a-auth-session-flow-static`  
PR: `#498`

## Exact executions

### QMeta structure

```text
head:        f9cd6d98912f7189d98a7ee8ad0764bc6811fecf
run:         32048964991
source job:  95443426363 SUCCESS
hosted job:  95443473893 SUCCESS
```

### QMeta string table and connection setup

```text
head:        1b9ee48146827c792288790f0db1c88ee108a03f
run:         32049109119
source job:  95443912956 SUCCESS
hosted job:  95443958584 SUCCESS
```

### Exact receiver class name

```text
head:        afcbfaf283a3dab679aeed2dd58bb2d2fd693a47
run:         32049187487
source job:  95444172660 SUCCESS
hosted job:  95444212338 SUCCESS
```

All three executions retained `runtime_access=none`, exact-fenced the official `15.32.df7b29` / `51965216` / `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` file, performed no source-side disassembly/semantic classification, did not access secrets, and did not upload the full executable.

## FACT — `0x3085b60` is a Qt QMetaObject

Exact static data at `0x3085b60` has the same Qt QMetaObject layout as the already-proven `TLoginProtocolMessageHandler` QMetaObject `0x3084fa0`.

For `0x3085b60`:

```text
superdata/static first field: 0
stringdata:                   0x1cc9800
metadata:                     0x1cc65e0
static_metacall:              0xdf5fe0
related/meta auxiliary:       0
metatypes-like table:         0x2f66c80
```

For the known comparison object `0x3084fa0`:

```text
stringdata:      0x1cae518
metadata:        0x1cae3e0
static_metacall: 0xcf2aa0
metatypes table: 0x3080c80
```

The known comparison table decodes to `tibia::authentication::TLoginProtocolMessageHandler` and its signal names, confirming the decoding model.

## FACT — `0x3085b60` belongs to the object at enclosing `+0x88`

The exact setup function begins at `0x7d51b0` and retains its first argument as `this` in `rbx`:

```asm
7d51bb  lea r14,[rip+...]     # 0x3085b60
7d51c8  mov rbx,rdi
7d51cf  mov rcx,[rdi+0xc58]
7d51d6  mov r15,[rdi+0x88]
...
7d522d  mov rsi,r15
...
7d5249  push r14
...
7d5254  call 0x4dd800         # QObject::connectImpl
```

Using the already-proven SysV mapping of `QObject::connectImpl`, this call proves:

```text
sender = [this+0x88]
sender QMetaObject = 0x3085b60
```

The same setup function later repeatedly connects `[this+0x88]` with `[this+0x9c0]`. The previously proven `sendLoginMessage` connection has:

```text
sender   = [this+0x9c0]  (TLoginProtocolMessageHandler)
receiver = [this+0x88]
slot adapter = 0xbd36a0
adapter dispatch = *(receiver_vptr+0x68)
```

Therefore the object whose QMetaObject is `0x3085b60` is the exact receiver of `sendLoginMessage`.

## FACT — exact receiver class

The QMeta string-table descriptor for class-name index `0` is:

```text
base:   0x1cc9800
offset: 0x1fd8
length: 0x26
address: 0x1ccb7d8
```

A separately exact-fenced 38-byte read, decoded only on GitHub-hosted Linux, produced:

```text
tibia::protocol::TProtocolMessageQueue
```

Hence:

```text
SENDLOGIN_RECEIVER_CLASS=tibia::protocol::TProtocolMessageQueue PROVEN
SENDLOGIN_RECEIVER_MEMBER=enclosing+0x88 PROVEN
```

This rejects the earlier shortcut that treated a primary `TGameClient` vptr as the signal receiver.

## FACT — corrected structural chain

The exact proven chain is now:

```text
TLoginProtocolMessageHandler::sendLoginMessage
  signal PMF 0xcf2950
  sender = [enclosing+0x9c0]
  -> QObject::connectImpl @ 0x7d564f
  -> QSlotObject trampoline 0x7d4220
  -> adapter 0xbd36a0
  -> receiver = [enclosing+0x88]
  -> receiver class = tibia::protocol::TProtocolMessageQueue
  -> virtual dispatch *(TProtocolMessageQueue_vptr + 0x68)
```

## UNKNOWN

Still not proven:

```text
TProtocolMessageQueue primary vptr
TProtocolMessageQueue vptr+0x68 exact target
final login-message queue/wire serializer
ordered login protobuf fields and their provenance
session credential family/lifetime
plaintext-password participation after initial authentication
reconnect/logout/change-character credential behavior
```

## Next discriminator

Recover the exact C++ vtable/address point for `tibia::protocol::TProtocolMessageQueue` from a bounded static data neighborhood anchored by its proven QMeta/static-metacall data, then decode only the `+0x68` target and its immediate proven call chain. Static work remains productive, so no runtime escalation is justified.
