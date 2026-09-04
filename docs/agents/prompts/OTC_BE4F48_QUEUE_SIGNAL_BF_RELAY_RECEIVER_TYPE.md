# OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE autonomicznie.
```

Recommended effort: **Extra High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. Live GitHub state is the only current authority.

Starting lifecycle:

```text
promotion PR #886
promotion merge 4ca7f33386a3e9d602a942105626150b2359960b
archive PR #887
archive merge 6ab922152d288e56112b162518512859552f06e6
source PR #885 CLOSED UNMERGED AS CONSUMED
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post884-885-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post884-885-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If newer promotion supersedes this fence or boundary, follow the newer authority instead of this prompt.

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
queue_drain_causal_consumption=true
queue_signal_argv1_identity=exact GameclientMessage shared pair
queue_signal_connectimpl_callsite=0xbe2eee
queue_signal_connectimpl_fde=0xbe2a50..0xbe3086
queue_signal_receiver_provenance=ENTRY_ARG:rdi
qslot_object_producer=operator new@0xbe2eb1 size=0x20
qslot_handoff=0xbe2ec3:r9<-rax
qslot_dispatch_impl_target=0xbe4df0
qslot_callable_payload=(0xbd2190,0)
qslot_function_target=0xbd2190
qslot_identity_proven=true
queue_signal_writer_identity=UNKNOWN
next_unique_writer_edge=UNKNOWN
final_queue_writer_identified=false
final_tcp_writer_identified=false
final_writer_contract=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

Source PR #885 has already proven the QSlot construction and callable target. **Do not re-run QSlot identity discovery and do not reinterpret dispatcher `0xbe4df0` as the callable target.**

## Single objective

Resolve only the exact object/class identity of the receiver passed to the unique `QObject::connectImpl@0xbe2eee`, starting from `ENTRY_ARG:rdi`, and determine whether this exact connection is a signal-relay hop rather than the final writer.

Required primary questions:

```text
QUEUE_SIGNAL_RECEIVER_IDENTITY=<exact type|UNKNOWN>
QUEUE_SIGNAL_RECEIVER_IDENTITY_PROVEN=true|false
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY|WRITER_EDGE|OTHER|UNKNOWN
```

A positive receiver identity requires exact-current object/type evidence tied specifically to the `entry-rdi` object at this connection. Useful proof classes include:

- exact vptr/vtable/typeinfo identity tied to the receiver object;
- exact QMeta/static-metaobject identity tied to the same object;
- bounded constructor/member provenance reachable through one unique identity-preserving edge;
- independent type/ownership cross-check.

Only if receiver identity and relay role are uniquely proven may this task follow **one** next identity-preserving `clientMessageReadyToProcess` edge and report its endpoint. That endpoint is not automatically a TCP writer; writer semantics require independent proof.

## Bounded search rule

Allowed route:

```text
connectImpl@0xbe2eee
  -> receiver ENTRY_ARG:rdi
  -> exact receiver type/identity
  -> classify this exact connection role
  -> optionally one next unique identity-preserving relay edge
```

The causally carried object remains the exact queued `GameclientMessage` shared pair. Preserve that identity throughout any permitted relay step.

Stop immediately if receiver typing or the next relay edge becomes non-unique.

Do **not** perform:

- the consumed QSlot construction analysis from #885 again;
- a global QObject/connect/QSlot census;
- a global socket/TCP/writer census;
- broad whole-executable generic xref discovery;
- the parallel sendLogin owner/`+0x88` task;
- Track B protocol implementation or mutation.

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
- guessing Field6 value or complete pre-login order.

If exact receiver identity or relay role cannot be proven statically within this boundary, terminate `SOURCE_BLOCKER` with the first precise missing edge. Do not create a broad writer architecture.

## TDD / validation

For any new analyzer/contract:

1. create a fresh independent source-only Track A task/branch/Draft PR from current trusted `main`;
2. persist non-overlapping ownership before implementation;
3. produce repository-only **RED** before any client package materialization;
4. implement the smallest GREEN discriminator;
5. exact-guard version/size/SHA before analysis;
6. emit deterministic sanitized output only;
7. retain zero proprietary client bytes in repository/artifacts;
8. run `git diff --check`, scoped syntax/Ruff where applicable, Track A governance, self-hosted PR boundary where applicable and exact-head CI;
9. perform fresh whole-diff falsification before a terminal claim.

Analyzer GREEN is not scientific PASS by itself.

## Terminal outcomes

Use one materially accurate result:

```text
QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_PROVEN
NEXT_RELAY_EDGE_PROVEN
SOURCE_BLOCKER
```

Required terminal fields:

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QUEUE_SIGNAL_RECEIVER_IDENTITY=<value|UNKNOWN>
QUEUE_SIGNAL_RECEIVER_IDENTITY_PROVEN=true|false
QSLOT_FUNCTION_TARGET=0xbd2190
QUEUE_SIGNAL_CONNECTION_ROLE=<SIGNAL_RELAY|WRITER_EDGE|OTHER|UNKNOWN>
NEXT_UNIQUE_RELAY_EDGE=<value|UNKNOWN>
NEXT_ENDPOINT_IDENTITY=<value|UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_PROVEN|NEXT_RELAY_EDGE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when this receiver/relay question is terminal. Do not consume the parallel sendLogin connection-owner task's scope.
