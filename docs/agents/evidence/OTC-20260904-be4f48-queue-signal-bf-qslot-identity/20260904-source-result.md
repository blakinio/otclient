# OTC-20260904 be4f48 queue signal 0xbf QSlot identity

## Terminal source result

```text
EXACT_CLIENT_FENCE_PROVEN=true
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QSLOT_OBJECT_PRODUCER=operator new@0xbe2eb1 size=0x20 -> r9<-rax@0xbe2ec3
QSLOT_DISPATCH_IMPL_TARGET=0xbe4df0
QSLOT_FUNCTION_TARGET=0xbd2190
QSLOT_IDENTITY_PROVEN=true
QUEUE_SIGNAL_WRITER_IDENTITY=UNKNOWN
NEXT_UNIQUE_WRITER_EDGE=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN
FIRST_MISSING_BOUNDARY=NEXT_WRITER_EDGE_SEMANTICS_NOT_UNIQUELY_PROVEN
```

## Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Bounded construction proof

The exact `QObject::connectImpl` call remains `0xbe2eee` in FDE `0xbe2a50..0xbe3086`. The QSlot object is a fresh `0x20`-byte allocation from `operator new` at `0xbe2eb1` and is passed as `r9 <- rax` at `0xbe2ec3`.

The exact object stores are:

```text
0xbe2ebf: [rax+0x08] <- r13
0xbe2ec6: [rax+0x00] <- 1
0xbe2ed6: [rax+0x10] <- xmm5
```

The dispatcher implementation is independently traced from `r13`:

```text
0xbe2e27: lea r13,[rip+0x1fc2] -> 0xbe4df0
0xbe2ebf: [QSlot+0x08] <- r13
FDE=0xbe4df0..0xbe4e69
```

The callable payload is independently reconstructed inside the same selected connect FDE:

```text
0xbe2e86: lea rax,[rip-0x10cfd] -> 0xbd2190
0xbe2e8d: [rbp-0x58] <- 0
0xbe2e9a: [rbp-0x60] <- rax
0xbe2eb6: xmm5 <- [rbp-0x60..-0x50]
0xbe2ed6: [QSlot+0x10..+0x20] <- xmm5
payload=(0xbd2190, 0)
```

The exact dispatcher branch then cross-checks the Qt member-callable representation rather than treating the dispatcher itself as the slot target:

```text
0xbe4e38: rcx <- [rsi+0x10]
0xbe4e3c: rdx += [rsi+0x18]
0xbe4e43: test cl,1
0xbe4e46: je 0xbe4e50
0xbe4e50: jmp rcx
```

For payload `(0xbd2190,0)`, the low bit is zero and the adjustment is zero, so the direct callable target is uniquely `0xbd2190`. The earlier intermediate interpretation of `0xbe4df0` as the slot callable was falsified; `0xbe4df0` is the QSlot dispatcher implementation stored at `+0x08`, while `0xbd2190` is the callable payload target stored at `+0x10`.

## Writer stop boundary

A bounded summary of FDE `0xbd2190..0xbd2495` contains multiple direct/indirect downstream edges, including Qt timer/metaobject calls and indirect virtual calls. None provides a unique identity-preserving queue/TCP writer edge under this task's bounded rule. The task therefore stops without a global Qt/socket/writer census.

```text
queue_signal_writer_identity=UNKNOWN
next_unique_writer_edge=UNKNOWN
FIRST_MISSING_BOUNDARY=NEXT_WRITER_EDGE_SEMANTICS_NOT_UNIQUELY_PROVEN
```

## TDD and exact-head evidence

Repository-only REDs stopped before WARP/client materialization:

```text
33865975313  analyzer intentionally absent
33866328798  inline construction contract missing
33866657246  r13 dispatcher provenance contract missing
33867024373  callable-payload/dispatcher distinction missing
```

Scientific GREEN:

```text
SOURCE_ANALYSIS_HEAD=2431ef51a9e3d95365fbae0d1b5d23846b9b1a99
SOURCE_RUN=33867321414 success
SOURCE_JOB=101005030098 success
ARTIFACT_ID=9934486697
ARTIFACT_DIGEST=sha256:a78f3c40161738d0d58c34e98d0e873f9d37920e586944963ec6e332e848a41f
```

The workflow verified repository contract/compile/diff checks, exact public package fence, transient client materialization, sanitized result validation and raw-client deletion before artifact upload.

## Safety and next action

```text
runtime_access=none
official_client_execution=false
login=false
credentials=false
process_memory=false
packet_capture=false
ocr_vision=false
official_service_e2e=false
track_b_pr_284_modified=false
```

This source task is terminal. Do not widen PR #885 into another writer census and do not mutate Track B #284. The next admissible step is a clean coordinator promotion that consumes this terminal source evidence together with the current parallel sendLogin receiver-field-owner result.
