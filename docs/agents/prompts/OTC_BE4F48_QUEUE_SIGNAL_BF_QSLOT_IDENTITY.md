# OTC-BE4F48-QUEUE-SIGNAL-BF-QSLOT-IDENTITY

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-QSLOT-IDENTITY autonomicznie.
```

Recommended effort: **Extra High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. Live GitHub state is the only current authority.

Starting promotion/lifecycle:

```text
promotion PR #881
promotion merge 2023254a4c6f0bac3a5ac4e8b06426d9dfed0862
archive PR #882
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post879-880-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post879-880-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If a newer promotion supersedes this exact fence or boundary, follow the newer authority instead of this prompt.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No address, offset, QMeta, RTTI, vtable, QSlot or writer identity from another build is authoritative without fresh exact-current proof.

## Promoted starting facts

```text
queue_sender_identity=tibia::protocol::TProtocolMessageQueue
queue_signal_name=clientMessageReadyToProcess
queue_signal_index=0xbf
queue_signal_body=0xbd2190
queue_signal_static_metaobject=0x30b73e0
queue_signal_static_metaobject_argument_chain=0xbd221d:rbp -> 0xbd22ae:rsi -> 0xbd22c2
queue_drain_causal_consumption=true
queue_signal_argv1_identity=exact GameclientMessage shared pair
queue_signal_connectimpl_candidate_count=1
queue_signal_connectimpl_callsite=0xbe2eee
queue_signal_connectimpl_fde=0xbe2a50..0xbe3086
queue_signal_receiver_provenance=ENTRY_ARG:rdi
qslot_object_argument=r9 <- rax after call-return boundary 0xbe2eb1
queue_signal_qslot_function=UNKNOWN
queue_signal_writer_identity=UNKNOWN
final_writer_contract=UNKNOWN
FIRST_MISSING_BOUNDARY=QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN
```

The signal body, exact static-metaobject register chain, exact signal index, unique bounded `connectImpl` and receiver pointer provenance are already promoted exact-current facts. Do not spend a new discriminator re-proving them unless fresh evidence falsifies the promotion.

## Single objective

Resolve only the QSlot object/function construction used by the unique connection:

```text
TProtocolMessageQueue::clientMessageReadyToProcess (signal 0xbf)
  -> exact QObject::connectImpl @ 0xbe2eee
  -> QSlot object passed through r9
  -> call-return boundary 0xbe2eb1 producing rax
  -> exact QSlot function target / slot identity
  -> at most one uniquely identity-preserving downstream writer edge
```

The task must remain causally tied to this one `connectImpl` and the exact signal carrying the causally consumed `GameclientMessage` pair.

A positive QSlot identity claim requires exact-current construction/dataflow evidence. Useful bounded proof classes include:

- the exact helper/call at `0xbe2eb1` and its return-object construction semantics;
- a unique function pointer stored into the returned QSlot object;
- RTTI/vtable/typeinfo or template/thunk identity tied to that exact object;
- receiver ownership/type identity if it can be proven without leaving the selected FDE/constructor chain;
- one independent caller/vtable/ownership cross-check for any promoted writer edge.

Generic Qt slot shapes, socket-like names, adjacent executable addresses, broad writer candidates or historical QSlot layouts are not proof.

## Bounded search rule

Start from:

```text
connectImpl FDE=0xbe2a50..0xbe3086
QSlot object producer boundary=0xbe2eb1
QSlot object handoff=r9 <- rax before connectImpl@0xbe2eee
```

Follow only the smallest identity-preserving producer chain required to identify the QSlot function target. If one unique slot target is proven, follow at most one additional uniquely identity-preserving writer edge.

Stop at the first non-unique producer/type/writer boundary.

Do **not** perform:

- a global Qt connection/QSlot census;
- a global socket/TCP/writer census;
- whole-executable Capstone disassembly to find generic references;
- the parallel sendLogin `[rbx+0x88]` owner/initializer task;
- a protocol rewrite or Track B mutation.

## Strict safety / anti-loop

Forbidden:

- official-client execution;
- login or credential/session/cookie/character/world access;
- process-memory access;
- packet capture;
- OCR/Vision;
- official-service E2E;
- runtime Field6 observation;
- modifying Track B PR #284;
- guessing Field6 value or complete pre-login message order.

If static source evidence cannot uniquely identify the QSlot function through this bounded construction chain, terminate at the first precise unresolved edge rather than opening another analyzer family.

## TDD / implementation contract

For any new analyzer or contract:

1. start from fresh trusted `main` on a dedicated non-overlapping source branch/Draft PR;
2. persist task ownership before material implementation;
3. first produce repository-only **RED** before any WARP package/client materialization;
4. implement the smallest GREEN discriminator;
5. enforce exact version/size/SHA fence before analysis;
6. emit deterministic sanitized JSON only;
7. delete transient raw client bytes before artifact upload;
8. run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable;
9. perform fresh whole-diff falsification before a terminal claim.

Green analyzer tests are not scientific PASS by themselves.

## Terminal outcomes

Use one materially accurate result:

```text
QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN
FINAL_WRITER_EDGE_PROVEN
SOURCE_BLOCKER
```

`QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN` requires at minimum:

```text
queue_signal_connectimpl_callsite=0xbe2eee
qslot_object_producer=<exact bounded producer>
qslot_function_target=<exact target>
qslot_identity_proven=true
queue_signal_writer_identity=<value|UNKNOWN>
```

`FINAL_WRITER_EDGE_PROVEN` additionally requires one uniquely identity-preserving downstream writer edge with an independent ownership/type cross-check. Do not call the complete final TCP writer contract proven unless this bounded task actually proves it.

If blocked:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique QSlot producer/function/writer edge>
```

## Track B gate

This source task never directly authorizes Track B #284 mutation or E2E. Any positive QSlot/writer result must first pass a clean coordinator promotion together with current sendLogin receiver-owner, Field6 and pre-login-order evidence.

Until then:

```text
TRACK_B_PR_284_MODIFIED=false
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
OFFICIAL_SERVICE_E2E_COUNT=0
RUNTIME_ACCESS=none
```

## Required final report

Persist and report at minimum:

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QSLOT_OBJECT_PRODUCER=<value|UNKNOWN>
QSLOT_FUNCTION_TARGET=<value|UNKNOWN>
QSLOT_IDENTITY_PROVEN=true|false
QUEUE_SIGNAL_WRITER_IDENTITY=<value|UNKNOWN>
NEXT_UNIQUE_WRITER_EDGE=<value|UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN|FINAL_WRITER_EDGE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when this QSlot identity question is terminal. Do not consume the parallel sendLogin receiver-field-owner task's scope.
