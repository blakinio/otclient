# Track A — queue QSlot consumer and adjacent QIODevice write cluster

Timestamp: 2026-08-14T19:01:00+02:00

Track: Track A / `official-client-re` / `OTCLIENT-TIBIA-RE` only.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Evidence sources

The concrete queue connection is re-audited in `20260814-chatgpt-network-handoff-correction.md` from successful exact-build runs `31805205225/94782356408` and `31805264031/94782546544`.

The local consumer/write disassembly below is recovered from exact-build write-xref run:

```yaml
workflow: .github/workflows/tibia-official-client-re-qiodevice-write-xrefs.yml
run: 31821085647
job: 94834146391
result: SUCCESS
runner: synology-otclient-01
```

That run independently recovered exactly five direct calls to `QIODevice::write(QByteArray const&)@plt (0x4de370)`:

```text
0x7dd563
0xb4066b
0xb46c75
0xc4a848
0xd08642
```

## Correct `clientMessageReadyToProcess` consumer root

At `QObject::connectImpl` site `0x19716a3`, the slot object stores:

```text
+0x08 = 0x7dd630  # QSlotObject operation/invoker
+0x10 = containing owner pointer
```

On Qt `Call` operation (`edi == 1`), exact disassembly of `0x7dd630` is:

```text
0x7dd630  push r12
0x7dd632  push rbp
0x7dd633  push rbx
0x7dd634  mov rbx,rsi
0x7dd637  sub rsp,0x40
0x7dd63b  test edi,edi
0x7dd63d  je 0x7dd6e0
0x7dd643  cmp edi,0x1
0x7dd646  jne 0x7dd6d1
0x7dd64c  mov rax,[rsi+0x10]
0x7dd650  mov r12,[rcx+0x8]
0x7dd654  mov rdi,[rax+0xc18]
0x7dd65b  mov rax,[rdi]
0x7dd65e  call [rax+0x90]
0x7dd664  test eax,eax
0x7dd666  je 0x7dd6d1
0x7dd668  mov rax,[rbx+0x10]
0x7dd66c  mov rbp,rsp
0x7dd66f  mov rdx,r12
0x7dd672  mov rdi,rbp
0x7dd675  mov rsi,[rax+0xa00]
0x7dd67c  mov rax,[rsi]
0x7dd67f  call [rax+0x10]
0x7dd682  mov rax,[rbx+0x10]
0x7dd686  mov rsi,rbp
0x7dd689  mov rdi,[rax+0xa10]
0x7dd690  mov rax,[rdi]
0x7dd693  call [rax+0x10]
0x7dd696  mov rax,[rbx+0x10]
0x7dd69a  mov rsi,rbp
0x7dd69d  mov rdi,[rax+0xc18]
0x7dd6a4  mov rax,[rdi]
0x7dd6a7  call [rax+0x80]
0x7dd6ad  mov rax,[rbx+0x10]
0x7dd6b1  mov rsi,rbp
0x7dd6b4  mov rdi,[rax+0xc18]
0x7dd6bb  mov rax,[rdi]
0x7dd6be  call [rax+0x78]
```

### FACT

- `0x7dd630` is the concrete QSlotObject operation function used by the `clientMessageReadyToProcess` connection.
- Its stored payload `slot+0x10` is the containing owner.
- Signal argument data is read from `args+0x08` into `r12`.
- The consumer first gates through the object at `owner+0xc18`, virtual slot `+0x90`.
- The signal argument is then passed into an operation on `owner+0xa00` via virtual slot `+0x10`, with a stack-local object as output/working storage.
- That stack-local object is then passed to `owner+0xa10` via virtual slot `+0x10`.
- The same working object is finally passed to `owner+0xc18` via virtual slots `+0x80` and `+0x78`.

### UNKNOWN

- exact class identities of objects stored at `owner+0xa00`, `owner+0xa10`, and `owner+0xc18`;
- whether the `+0xa00` stage is serialization, framing, encryption/compression, or another transform;
- whether the `+0xa10` stage is a transport buffer/queue stage;
- precise semantics of the `+0xc18` gate/finalization operations;
- whether this path performs synchronous write or schedules a later write.

No serializer/framing label is promoted yet.

## Adjacent QSlot transport/write operation at `0x7dd3f0`

A separate QSlotObject-style operation function immediately before `0x7dd630` uses the same owner-layout region and contains the direct `QIODevice::write` call at `0x7dd563`.

On its call-operation path, the recovered structure includes:

```text
owner = [slot+0x10]
call virtual +0x18 on [owner+0xa10]
transport_state = [owner+0x9f0]
if [transport_state+0x20] == 0:
    device = [transport_state]
    target = device->vtable[+0xe8]
    compare target with 0xb40630
    if target == 0xb40630:
        call device->vtable[+0x78]
        call QBuffer::buffer()
        call device->vtable[+0x88]
        call QIODevice::write(QByteArray const&) at 0x7dd563 with rdi=device
        call device->vtable[+0x88]
    else:
        call target dynamically
```

### FACT

- `0x7dd563` is a direct call to `QIODevice::write(QByteArray const&)@plt`.
- Its `this` argument is the object loaded from `[ [owner+0x9f0] ]` on this path.
- The operation checks virtual target `device->vtable[+0xe8]` against concrete executable `0xb40630` before selecting an optimized local send/write sequence.
- This establishes a real QIODevice-backed transport/write cluster in the same exact code neighborhood as the queue-message QSlot consumer.

### IMPORTANT BOUNDARY

`0x7dd3f0` and `0x7dd630` are adjacent **separate** QSlot operation functions. Proximity does not prove that `0x7dd630` directly calls `0x7dd3f0` or `0x7dd563`. The shared owner-layout offsets make them structurally related candidates, but the edge between the queue consumer and this write operation remains `UNKNOWN` until object/connection provenance closes it.

## Concrete helper `0xb40630`

The exact disassembly shape of `0xb40630` is a QIODevice/QBuffer-oriented method:

```text
this = rdi
QByteArray-like argument = rsi
call this->vtable[+0x78]
load this->vtable[+0x88]
call QBuffer::buffer()
call vtable +0x88
call QIODevice::write(QByteArray const&)@plt at 0xb4066b
then continue/tail through vtable +0x88
```

### DERIVED

`0xb40630` behaves like a concrete virtual byte-output method for a QIODevice-derived or QIODevice-owning transport object. Exact class identity is not yet proven.

## Other direct QIODevice-write candidates

Current disassembly classifies the remaining direct callsites conservatively:

- `0xb46c75`: text/newline write pattern — likely logging/text output; not promoted as game transport.
- `0xc4a848`: QNetworkReply data into QFileDevice/flush path — file output, not game socket send.
- `0xd08642`: QFile open/write/close path — file output, not game socket send.

Therefore the strongest current transport candidates are `0x7dd563` and `0xb4066b`.

## Updated structural model

```text
TProtocolMessageQueue
  -> clientMessageReadyToProcess wrapper 0xde91b0
  -> Qt connection 0x19716a3
  -> QSlotObject invoker 0x7dd630
  -> owner+0xc18 gate (+0x90)
  -> owner+0xa00 transform (+0x10)
  -> owner+0xa10 transform/queue (+0x10)
  -> owner+0xc18 finalization (+0x80, +0x78)
  -> [write scheduling/path still UNKNOWN]

adjacent related transport cluster:
owner+0xa10 / owner+0x9f0
  -> QIODevice-like device
  -> 0xb40630 or equivalent virtual target
  -> QIODevice::write(QByteArray const&)
```

## Next action

Recover construction/assignment/vtable provenance for owner fields `+0x9f0`, `+0xa00`, `+0xa10`, and `+0xc18`. Then identify the exact QIODevice class behind `[ [owner+0x9f0] ]`, including the vtable containing target `0xb40630` at byte offset `+0xe8`. Use that evidence to close or reject the structural edge between queue consumer `0x7dd630` and direct write cluster `0x7dd3f0/0x7dd563`.
