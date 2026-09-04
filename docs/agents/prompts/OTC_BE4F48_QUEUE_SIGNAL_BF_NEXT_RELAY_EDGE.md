# OTC-BE4F48-QUEUE-SIGNAL-BF-NEXT-RELAY-EDGE

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-NEXT-RELAY-EDGE autonomicznie.
```

Recommended effort: **Extra High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. GitHub LIVE STATE is the only current authority.

Starting promotion/lifecycle:

```text
promotion PR #891
promotion merge b4582b1e72d689b5d26fbd16c0ba2bbd20dca970
archive PR #892
archive merge 58cc12558babcfcadaa89bbdc49ca19ee1e58e5e
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post889-890-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post889-890-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If a newer promotion supersedes this exact fence or boundary, follow the newer authority instead of this prompt.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No address, offset, RTTI, QMeta, vtable, QSlot, connection or writer identity from another build is authoritative without fresh exact-current proof.

## Promoted starting facts

```text
queue_sender_identity=tibia::protocol::TProtocolMessageQueue
queue_signal_name=clientMessageReadyToProcess
queue_signal_index=0xbf
queue_signal_body=0xbd2190
queue_signal_argv1_identity=exact GameclientMessage shared pair
queue_signal_connectimpl_callsite=0xbe2eee
queue_signal_connectimpl_fde=0xbe2a50..0xbe3086
queue_signal_receiver_provenance=ENTRY_ARG:rdi
queue_signal_receiver_identity=tibia::protocol::TProtocolMessageQueue
queue_signal_receiver_identity_proven=true
queue_signal_receiver_vptr=0x30ed588
queue_signal_receiver_typeinfo=0x30ed548
qslot_function_target=0xbd2190
queue_signal_connection_role=SIGNAL_RELAY
next_unique_relay_edge=UNKNOWN
next_endpoint_identity=UNKNOWN
final_queue_writer=UNKNOWN
final_tcp_writer=UNKNOWN
final_writer_contract=UNKNOWN
FIRST_MISSING_BOUNDARY=NEXT_RELAY_EDGE_NOT_UNIQUELY_PROVEN_WITHIN_BOUNDED_RECEIVER_TYPE_PROOF
```

The receiver type and `SIGNAL_RELAY` role are already promoted exact-current evidence. Do not spend a new discriminator re-proving receiver RTTI, QSlot construction, or the existing `connectImpl@0xbe2eee` identity unless fresh evidence falsifies the promotion.

## Single objective

Resolve only one next identity-preserving relay edge carrying the same exact `GameclientMessage` shared pair after the proven self-relay:

```text
TProtocolMessageQueue::clientMessageReadyToProcess
  -> proven self relay at connectImpl@0xbe2eee / QSlot 0xbd2190
  -> same GameclientMessage shared pair
  -> one next exact connection/endpoint
```

The target is the next unique relay endpoint, not a global final-writer search.

A positive next-edge claim requires exact-current causal and identity-preserving evidence, for example:

- one unique `QObject::connectImpl`/QMeta connection tied to the same queue signal and shared pair;
- exact receiver provenance plus object-tied RTTI/QMeta/type identity for that connection;
- an exact QSlot/callable target tied to that one connection if needed;
- a bounded argument/dataflow cross-check that the same `GameclientMessage` pair is carried through the edge.

A socket-like function name, generic Qt connection, historical writer address or broad xref count is not proof.

## Bounded search rule

Start only from the promoted self-relay facts and remain in a bounded queue constructor/metaobject/connect context. You may enumerate only connection candidates that are causally tied to `clientMessageReadyToProcess(0xbf)` and the same `GameclientMessage` pair.

Follow at most **one** next unique identity-preserving relay edge. If more than one candidate remains, stop at that ambiguity. If one endpoint is proven and happens to be writer-like, report that exact endpoint but do not automatically continue to a second socket/TCP edge.

Do **not** perform:

- a global QObject/connect/QSlot census;
- a global socket/TCP/writer census;
- broad whole-executable generic xref discovery;
- #885 QSlot reconstruction again;
- #890 receiver RTTI/type reconstruction again;
- parallel sendLogin owner/receiver work;
- protocol mutation or Track B work.

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
- guessing Field6 value or complete pre-success message order;
- widening into a global writer search if the next relay edge is non-unique.

If one next identity-preserving edge cannot be uniquely proven, terminate at the first precise connection/endpoint ambiguity.

## TDD / implementation contract

For any new analyzer/contract:

1. start from fresh trusted `main` on a dedicated non-overlapping source branch/Draft PR;
2. persist task ownership before material implementation;
3. first produce repository-only **RED** before WARP/client materialization;
4. implement the smallest GREEN discriminator for one next relay edge only;
5. enforce exact version/size/SHA fence before analysis;
6. emit deterministic sanitized JSON only;
7. delete transient raw client bytes before artifact upload;
8. run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable;
9. perform fresh whole-diff falsification before a terminal claim.

Green analyzer tests are not scientific PASS by themselves.

## Terminal outcomes

Use one materially accurate result:

```text
QUEUE_SIGNAL_BF_NEXT_RELAY_EDGE_PROVEN
SOURCE_BLOCKER
```

A positive result requires at minimum:

```text
queue_signal_receiver_identity=tibia::protocol::TProtocolMessageQueue
queue_signal_connection_role=SIGNAL_RELAY
next_unique_relay_edge=<exact callsite/connection>
next_endpoint_identity=<exact class/type or callable endpoint>
next_relay_identity_preserved=true
next_relay_gameclientmessage_pair=exact GameclientMessage shared pair
```

If the endpoint is writer-like, additionally report only what is actually proven:

```text
queue_signal_writer_identity=<value|UNKNOWN>
final_queue_writer_identified=true|false
final_tcp_writer_identified=true|false
final_writer_contract=<value|UNKNOWN>
```

Do not upgrade to a complete final TCP writer contract unless this single bounded edge genuinely proves it.

If blocked:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique relay connection/endpoint edge>
```

## Track B gate

This source task never directly authorizes Track B #284 mutation or E2E. Any positive relay/writer result must first pass a clean coordinator promotion together with current sendLogin owner/receiver, Field6 and pre-login-order evidence.

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
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
QSLOT_FUNCTION_TARGET=0xbd2190
NEXT_UNIQUE_RELAY_EDGE=<value|UNKNOWN>
NEXT_ENDPOINT_IDENTITY=<value|UNKNOWN>
NEXT_RELAY_IDENTITY_PRESERVED=true|false
QUEUE_SIGNAL_WRITER_IDENTITY=<value|UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<QUEUE_SIGNAL_BF_NEXT_RELAY_EDGE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when one next relay edge is terminal. Do not consume the parallel sendLogin owner-edge task's scope.
