# OTC-BE4F48-QUEUE-SIGNAL-BF-RECEIVER

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-RECEIVER autonomicznie.
```

Recommended effort: **Extra High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. Live GitHub state is the only current authority.

Starting promotion:

```text
PR #876
merge 44a35365e38b9483b9c43aff4c36c2379fdbfb3e
archive PR #877
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post874-875-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post874-875-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If a newer promotion supersedes this fence or boundary, follow the newer authority.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

Do not transfer addresses, offsets, QMeta, RTTI, vtables or writer identities from another build without fresh exact-current evidence.

## Proven starting facts

Promoted exact-current facts:

```text
serialized_queue_object_identity_proven=true
serialized_queue_object_identity=16-byte {object=allocation+0x10, owner=allocation} pair
queue_insert_target=0xbd24a0
owned_drain_callback=0xbd2190
owned_drain_fde=0xbd2190..0xbd2495
queued_gameclientmessage_causal_consumption=true
queue_signal_dispatch_callsite=0xbd22c2
queue_signal_dispatch_target=QMetaObject::activate(...)
queue_signal_sender=TProtocolMessageQueue
queue_signal_static_metaobject=0x30b73e0
queue_signal_index=191
queue_signal_index_hex=0xbf
queue_signal_argv1=exact copied GameclientMessage {object,owner} pair
queue_signal_bf_receiver_identity=UNKNOWN
queue_signal_bf_writer_identity=UNKNOWN
next_unique_writer_edge=UNKNOWN
final_writer_contract=UNKNOWN
```

Do not spend a new discriminator re-proving the queue-drain consumption itself unless new evidence falsifies the promotion.

## Single objective

Resolve only:

```text
TProtocolMessageQueue signal 0xbf
  carrying the exact queued GameclientMessage shared pair
  -> unique connected receiver/slot identity
  -> writer ownership/type identity
  -> at most one next uniquely identity-preserving writer edge
```

The proof must remain causally tied to signal `0xbf` and the exact `GameclientMessage` object identity. A generic socket/TCP/QMeta writer candidate is insufficient.

Admissible bounded approaches may include:

- exact-current QMeta signal metadata plus bounded `QObject::connectImpl` construction sites for this sender/signal;
- slot-object function pointer identity tied to a unique receiver object;
- receiver QMeta/RTTI/vtable/constructor ownership;
- exact shared-pair/dataflow continuity into one downstream writer object;
- an independent ownership/caller/vtable cross-check for any promoted writer edge.

## Strict anti-loop / scope

Do not:

- reopen or rerun #874 queue-drain consumption;
- globally enumerate all Qt connections, sockets, TCP symbols or writer-like functions;
- broaden into the separate sendLogin receiver `[rbx+0x88]` task;
- infer writer identity from name proximity, generic vslots or unbound call targets;
- modify Track B PR #284;
- guess Field6 value or complete pre-login ordering;
- execute the official client;
- perform login, credential/session access, process-memory reads, packet capture, OCR/Vision or official-service E2E.

If the signal receiver cannot be uniquely bound with bounded exact-current evidence, stop at the first precise missing connection/ownership edge.

## TDD / implementation contract

For any new analyzer/contract:

1. create a dedicated non-overlapping Track A task/branch/Draft PR from fresh trusted `main`;
2. persist ownership before material implementation;
3. prove repository-only RED before any client package/materialization;
4. implement the smallest GREEN discriminator;
5. enforce exact fence before static analysis;
6. emit deterministic sanitized JSON only;
7. remove transient raw client bytes before artifact upload;
8. run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable;
9. perform fresh whole-diff falsification before terminal claim.

Analyzer GREEN is not enough; scientific claims require unique causal evidence.

## Terminal outcomes

Use exactly one materially accurate result:

```text
QUEUE_SIGNAL_BF_RECEIVER_PROVEN
FINAL_WRITER_EDGE_PROVEN
SOURCE_BLOCKER
```

`QUEUE_SIGNAL_BF_RECEIVER_PROVEN` requires a unique connected receiver/slot identity but may still leave the next writer edge UNKNOWN.

`FINAL_WRITER_EDGE_PROVEN` additionally requires one uniquely identity-preserving downstream writer edge with an independent ownership/type cross-check. Do not call the complete final TCP writer contract proven unless this bounded task actually proves it.

If blocked:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact unresolved signal->receiver/slot/writer edge>
```

## Track B gate

This task does not directly authorize Track B mutation or E2E. Any positive receiver/writer result must be consumed by a clean coordinator promotion together with current sendLogin receiver, Field6 and pre-login-order evidence.

Until then:

```text
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
TRACK_B_PR_284_MODIFIED=false
OFFICIAL_SERVICE_E2E_COUNT=0
```

## Required final report

Persist and report at minimum:

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
QUEUE_DRAIN_CAUSAL_CONSUMPTION=true
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage pair
QUEUE_SIGNAL_RECEIVER_IDENTITY=<value|UNKNOWN>
QUEUE_SIGNAL_SLOT_IDENTITY=<value|UNKNOWN>
QUEUE_SIGNAL_WRITER_IDENTITY=<value|UNKNOWN>
NEXT_UNIQUE_WRITER_EDGE=<value|UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<QUEUE_SIGNAL_BF_RECEIVER_PROVEN|FINAL_WRITER_EDGE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<one bounded repository-owned step or coordinator promotion>
```

Evidence before claims. Stop when this bounded signal-`0xbf` receiver/writer question is terminal.
