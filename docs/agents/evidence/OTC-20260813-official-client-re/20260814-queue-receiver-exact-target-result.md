# Track A — exact queue receiver reconstruction result

## Exact-target experiment

```yaml
workflow: Track A queue receiver exact target
head: 7be0c193d2b20cbb2c82b53884ecd2f5c439f344
run: 31817347325
job: 94822092882
runner: synology-otclient-01
result: SUCCESS
artifact: 9225834832
artifact_digest: sha256:dc39d2edce36d3eb6d163e93a559ef1608092c1038dd0ce453552c29386b752e
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The artifact completed with `TRACK_A_QUEUE_RECEIVER_EXACT_TARGET_COMPLETE=true`.

## Direct vtable-qword validation

The exact binary directly contains:

```text
0x308c408 + 0x90 -> 0x8409d0  executable=true
0x2f66288 + 0xb8 -> 0x313cce0  executable=false
```

Therefore:

- **FACT:** address point `0x308c408` has executable slot `+0x90 = 0x8409d0`.
- **DISPROVEN:** `0x2f66288:+0xb8 -> 0xb5b880`. The exact qword is `0x313cce0`, not `0xb5b880`, and it is not executable.

A reverse address-point census found two vtable-like address points whose `+0x90` qword equals `0x8409d0`:

```text
0x28db78  first20 executable score=7
0x308c408 first20 executable score=13
```

Consequently the slot value alone does not uniquely establish the containing owner's primary vptr.

## Correct queue connect site recovered from original provenance runs

The earlier summary label `0x7e7470` is not the queue `QObject::connectImpl` callsite. Reinspection of the exact successful source runs establishes the real connection.

### Slot provenance

Run `31805205225`, job `94782356408`, `SUCCESS` reports:

```text
PROVEN_SITE call=0x19716a3
sender_metaobject=0x3085b60
invoker=0x7dd630@0x1971670
signal_payload_word0=0xde91b0@0x197163c
signal_payload_word1=0x0@0x197164c
sender_source=0x1971695:mov rsi,rbx
receiver_source=0x1971691:mov rcx,rax
slot_payload_word0=0x91@0x1971595
slot_payload_word1=0x0@0x19715a4
```

### Same-object owner/queue relationship

Run `31805264031`, job `94782546544`, `SUCCESS` contains the exact aligned sequence:

```text
0x1971635  mov rax,QWORD PTR [rbp-0x1b0]
0x197163c  lea rcx,[rip+...] # 0xde91b0
...
0x1971654  mov rbx,QWORD PTR [rax+0x88]
...
0x1971682  mov rax,QWORD PTR [rbp-0x1b0]
...
0x1971691  mov rcx,rax
0x1971695  mov rsi,rbx
...
0x19716a3  call QObject::connectImpl@plt
```

This proves the receiver and queue relation without relying on a guessed class/vtable:

```text
owner = [rbp-0x1b0]
sender_queue = [owner+0x88]
receiver = owner
signal wrapper = 0xde91b0 = TProtocolMessageQueue::clientMessageReadyToProcess
slot pointer-to-member payload = 0x91
connectImpl call = 0x19716a3
```

**FACT:** the outbound queue signal is connected from the queue at `owner+0x88` to the containing owner object.

**FACT:** encoded member pointer `0x91` denotes a virtual receiver entry at offset `+0x90` under the already established ABI interpretation.

## Current boundary

The chain is now:

```text
semantic action
-> TInternalGameActionRouter
-> TProtocolMessageQueue builder
-> clientMessageReadyToProcess / 0xde91b0
-> sender queue = [owner+0x88]
-> QObject::connectImpl @ 0x19716a3
-> receiver = owner
-> virtual member-pointer payload 0x91
-> receiver slot offset +0x90
```

What is **not yet proven** is which of the candidate address points is the primary vptr of this exact receiver object. Therefore `0x8409d0` is not yet promoted as the concrete queue receiver function solely from the table census.

## Historical live-owner probe

Workflow `Track A live network owner slot` was designed to break on `0xde91b0` and read:

```text
queue = rdi
owner = queue - 0x88
vptr = *(owner)
slot = *(vptr+0x90)
```

Its latest run `31807425717`, job `94789596246`, failed before producing a `LIVE_VPTR/LIVE_SLOT_90` marker, so it supplies no dynamic value and is not used as evidence.

## Next proof obligation

Use exact function-boundary/FDE-aligned disassembly around `0x19716a3` to trace the provenance of `[rbp-0x1b0]`, and independently validate constructor/vptr stores to `0x28db78` versus `0x308c408`. Only after the receiver's actual vptr is structurally or dynamically established may `+0x90` be mapped to a concrete routine.
