# Track A — correction of queue-to-network-owner slot interpretation

Timestamp: 2026-08-14T18:55:00+02:00

Track: Track A / `official-client-re` / `OTCLIENT-TIBIA-RE` only.

## Purpose

Correct a material false inference in the previous outbound handoff model. The queue-to-containing-owner connection remains real, but the prior conclusion that `clientMessageReadyToProcess` dispatches through receiver virtual slot `+0x90` is disproven by direct reconstruction of the exact connection site.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Historic exact runs re-audited

```yaml
slot_provenance:
  run: 31805205225
  job: 94782356408
  result: SUCCESS
concrete_ownership:
  run: 31805264031
  job: 94782546544
  result: SUCCESS
runner: synology-otclient-01
```

The original runs themselves succeeded. The defect was in the later interpretation of a generic backward payload reconstruction across adjacent Qt connections.

## Relevant connection at `0x19716a3`

The exact disassembly around the connection is:

```text
0x1971635  mov rax,[rbp-0x1b0]
0x197163c  lea rcx,[rip+...]       # 0xde91b0
0x1971648  mov [rbp-0x70],rcx
0x197164c  mov [rbp-0x68],0
0x1971654  mov rbx,[rax+0x88]
0x197165b  call operator new(0x18)
0x1971660  mov dword ptr [rax],1
0x1971666  mov r9,rax
0x197166d  xor r8d,r8d
0x1971670  lea rcx,[rip+...]       # 0x7dd630
0x1971677  lea rsi,[rip+...]       # 0x3085b60
0x197167e  mov [rax+0x8],rcx
0x1971682  mov rax,[rbp-0x1b0]
0x1971689  lea rdx,[rbp-0x70]
0x197168d  mov [r9+0x10],rax
0x1971691  mov rcx,rax
0x1971695  mov rsi,rbx
0x197169c  mov rdi,[rbp-0x1a0]
0x19716a3  call QObject::connectImpl
```

Therefore for this exact connection:

- sender object = `[owner+0x88]`;
- sender metaobject = `0x3085b60` (`TProtocolMessageQueue` from prior QMeta evidence);
- signal storage = `{0xde91b0, 0}` (`clientMessageReadyToProcess` wrapper from prior QMeta evidence);
- receiver object = the containing `owner` itself;
- explicit receiver slot storage argument `r8` = `NULL`;
- allocated slot object size = `0x18` bytes;
- slot-object operation/invoker pointer at `+0x08` = `0x7dd630`;
- slot-object payload at `+0x10` = containing owner pointer.

This is a functor/QSlotObject-style connection, not a receiver pointer-to-member virtual slot connection.

## Origin of the false `0x91` interpretation

Immediately before the relevant connection, the same setup function builds another connection. That preceding edge writes:

```text
0x1971595  mov qword ptr [rbp-0x40],0x91
0x19715a4  mov qword ptr [rbp-0x38],0
...
0x1971624  call QObject::connectImpl
```

Only after that connection finishes does the code build the `clientMessageReadyToProcess` edge beginning at `0x1971635`.

The earlier generic provenance parser searched backward across adjacent connection setup code and incorrectly associated the stale `{0x91,0}` payload from the preceding connection with the later call at `0x19716a3`.

## Consequences

### FACT

- `TProtocolMessageQueue` sender ownership at `[owner+0x88]` remains proven.
- `clientMessageReadyToProcess` signal wrapper `0xde91b0` remains proven for this connection.
- the containing owner remains the receiver object.
- concrete consumer recovery must start at QSlotObject invoker `0x7dd630`, not at owner vtable byte offset `+0x90`.

### DISPROVEN

- `clientMessageReadyToProcess -> owner virtual slot +0x90`.
- treating `{0x91,0}` as the slot payload for connection `0x19716a3`.
- treating primary owner vtable `0x308c408 + 0x90 = 0x8409d0` as the proven queue-consumer function solely from that Qt connection.
- treating `0x8409d0 -> subobject +0xb8 -> 0xb5b880` as the proven outbound serialization chain.
- treating `0x2f66288 +0xb8 = 0xb5b880`; exact relocation-aware validation instead gives `0x2f66288 +0xb8 = 0x313cce0`, non-executable.
- treating `0xb5b880` as a normal ABI function entry; linear disassembly shows that address lies inside the instruction beginning at `0xb5b87c`.

### UNKNOWN

- exact executable consumer reached by QSlotObject invoker `0x7dd630`;
- whether the consumer is a direct owner method, lambda body, or another forwarding helper;
- exact serializer/framing/encryption/compression path;
- final network write site.

## Independently confirmed direct `QIODevice::write(QByteArray const&)` callsites

Recovery run `31821085647` / job `94834146391` confirms exactly five direct callsites to PLT `0x4de370` in the exact binary:

```text
0x7dd563
0xb4066b
0xb46c75
0xc4a848
0xd08642
```

The QFile-associated candidates are not promoted as network writes. The structural relationship of `0x7dd563` and `0xb4066b` to the queue consumer remains to be proven.

## Next action

Disassemble and classify `0x7dd630` with exact boundaries and resolve the concrete operation path it invokes using its stored owner pointer. Then build forward/reverse structural provenance between that consumer and the confirmed `QIODevice::write` candidates. Do not use the superseded `+0x90 -> 0x8409d0 -> 0xb5b880` route.
