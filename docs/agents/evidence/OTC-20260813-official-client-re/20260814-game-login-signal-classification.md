# Official game-login Qt signal classification

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Recover the exact Qt signal-to-consumer path for the official 15.32 game-login message before Track B uses the official client as a protocol oracle.

## Exact-client QMeta evidence — PROVEN

Exact-client workflow run `31652067802`, job `94298391194`, recovered this QMeta surface:

```text
class: tibia::authentication::TLoginProtocolMessageHandler
QMetaObject: 0x3084fa0
static metacall: 0xcf2aa0

sendLoginMessage:          InvokeMetaMethod case entry 0xcf2ca0   argc=1 flags=0x6
sendSecondaryLoginMessage: InvokeMetaMethod case entry 0xcf2c50   argc=1 flags=0x6
```

Qt QMeta flags `0x06` are `AccessPublic (0x02) | MethodSignal (0x04)`, so both are public Qt signals. The `0xcf2cxx` addresses above are case entries inside the generated static metacall path; they are not packet serializers.

## Exact signal PMF identity — PROVEN

Exact-SHA workflow run `31820653663`, job `94832832975`, on `synology-otclient-01` disassembled `qt_static_metacall` and the signal functions themselves.

The `IndexOfMethod` path compares the supplied pointer-to-member against the exact signal functions and writes the corresponding QMeta method index:

```text
PMF 0xcf2950 -> method/signal index 0
PMF 0xcf2980 -> index 1
PMF 0xcf29b0 -> 2
PMF 0xcf29d0 -> 3
PMF 0xcf2a10 -> 4
PMF 0xcf2a50 -> 5
PMF 0xcf2a80 -> 6
```

The functions also directly confirm their signal indices through `QMetaObject::activate`:

```text
0xcf2950 -> QMetaObject::activate(..., signal_index=0, ...)
0xcf2980 -> QMetaObject::activate(..., signal_index=1, ...)
```

Combining that result with the recovered QMeta method order proves:

```text
sendLoginMessage          -> signal PMF 0xcf2950
sendSecondaryLoginMessage -> signal PMF 0xcf2980
```

## QObject::connect ABI correction — PROVEN

The earlier register labels around `QObject::connectImpl` omitted the hidden structure-return argument for `QMetaObject::Connection`. With the SysV hidden `sret` accounted for, the exact call-site mapping is:

```text
rdi   hidden QMetaObject::Connection return storage
rsi   sender
rdx   signal PMF storage
rcx   receiver
r8    slot PMF storage
r9    QSlotObjectBase*
stack connection type / types / sender QMetaObject
```

This corrected interpretation supersedes older provisional register labels from the first consumer scan.

## Primary and secondary consumer paths — PROVEN

The focused connect provenance plus the PMF map prove:

```text
sendLoginMessage
  QMeta index:      0
  signal PMF:       0xcf2950
  connectImpl call: 0x7d564f
  QSlotObject invoke trampoline: 0x7d4220
  slot PMF target:  0xbd36a0

sendSecondaryLoginMessage
  QMeta index:      1
  signal PMF:       0xcf2980
  connectImpl call: 0x7d56e7
  QSlotObject invoke trampoline: 0x7d4190
  slot PMF target:  0xbf3990
```

At the primary connect setup the receiver is loaded from the enclosing object's `[rbx+0x88]`; the sender is loaded from `[rbx+0x9c0]`.

## Primary slot-target analysis — PROVEN

Exact-SHA workflow run `31821003485`, job `94833872467`, on `synology-otclient-01` completed successfully and disassembled the primary target `0xbd36a0` plus a secondary control target `0xbf3990`.

The primary function is an adapter/delegator, not a proven final wire serializer. It allocates and initializes a `0x50`-byte intermediate object, transforms/copies selected fields from the signal argument, then dispatches the resulting object through a virtual method on the receiver:

```asm
0xbd37f3: mov rax,QWORD PTR [r12]
0xbd37f7: mov rax,QWORD PTR [rax+0x68]
...
0xbd381e: mov rdi,r12
0xbd3821: call rax
```

At function entry the receiver is preserved in `r12`, so the next exact semantic target is:

```text
receiver = primary connect receiver loaded from [enclosing_object+0x88]
receiver_vptr = *(receiver)
next_target = *(receiver_vptr + 0x68)
```

Other directly observed adapter structure includes:

```text
intermediate allocation size: 0x50
signal argument flags tested at +0x10: bits 0x1, 0x2, 0x4
signal argument fields structurally accessed: +0x18, +0x20, +0x28, +0x30
intermediate +0x38 OR=0x2
intermediate +0x48 = 0x0a
```

These offsets/flags are structural observations only; their protocol meanings are UNKNOWN and must not be named from guesswork.

The secondary target `0xbf3990` is also adapter-like, which supports treating the `0xbd36a0` virtual dispatch as the next boundary rather than treating the Qt slot itself as the serializer.

## Corrected claim boundary

### FACT

- `sendLoginMessage` is QMeta signal index 0 with actual signal PMF `0xcf2950`.
- it is connected through `connectImpl @ 0x7d564f` to captured slot PMF `0xbd36a0`.
- `0xcf2ca0` is an InvokeMetaMethod case entry, not the packet builder.
- `0xbd36a0` constructs an intermediate object and invokes `receiver->vtable[+0x68]`.
- primary receiver source at connect setup is `[enclosing_object+0x88]`.

### DISPROVEN

- `0xcf2ca0` is the official game-login packet builder.
- `0x7d4220` QSlotObject trampoline is the semantic serializer.
- `0xbd36a0` has been proven to be the final wire serializer.

### UNKNOWN

- exact primary receiver class/vptr;
- exact function address stored at receiver vtable slot `+0x68`;
- whether that virtual target directly serializes or delegates further;
- ordered public/pre-secret wire fields and widths;
- exact game-socket version representation;
- asset identifier placement;
- RSA boundary and checksum/sequence/framing state.

## Cross-track promotion contract

Track B may consume:

```yaml
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
send_login_message_qmeta_index: 0
send_login_message_signal_pmf: 0xcf2950
send_login_message_static_metacall_case: 0xcf2ca0
send_login_message_connect_call: 0x7d564f
send_login_message_slot_invoker: 0x7d4220
send_login_message_slot_target: 0xbd36a0
send_login_message_receiver_source: enclosing_object_plus_0x88
slot_target_role: adapter_delegator
adapter_intermediate_size: 0x50
adapter_virtual_dispatch_offset: 0x68
adapter_virtual_dispatch_target: UNKNOWN
serializer_or_builder_address: UNKNOWN
```

## Next action

Resolve the exact receiver vptr and `*(vptr+0x68)` target, preferably through an exact-SHA no-credential structural runtime probe or a statically proven receiver-vtable mapping. Then disassemble that target and continue until the actual outbound writer/serializer boundary is proven. Promote only non-secret, version-fenced structural facts to Track B.