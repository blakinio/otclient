# Coordinator promotion — exact-current be4f48 post #884/#885

Decision: **SOURCE_BLOCKER / BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA**.

This promotion is rebuilt from trusted `main@e24462d72942d8381e1a468de84f16b60f1aa8c9` and consumes only sanitized exact-current facts from source Draft PRs #884 and #885. Neither source analyzer/workflow is promoted. Track B PR #284 remains untouched.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Independent coordinator falsification

The coordinator independently reconstructed both live source PRs from their exact current heads, inspected their complete changed-path sets, re-read the sanitized result/source evidence, inspected the bounded proof logic for the claimed boundary, and verified current exact-head GitHub check state.

Result:

```text
INDEPENDENT_COORDINATOR_FALSIFICATION=PASS
MATERIAL_FINDINGS_OPEN=0
IMPLEMENTABLE_DELTA_COUNT=0
SOURCE_WORKER_SELF_PROMOTION_USED=false
```

The independent audit specifically rejects three invalid upgrades:

1. zero direct callers in #884 are not converted into a guessed owner/receiver identity;
2. QSlot dispatcher `0xbe4df0` in #885 is not mislabeled as the callable target; exact payload/dispatcher proof binds callable target `0xbd2190`;
3. callable identity `0xbd2190` is not converted into queue/TCP writer identity because the bounded downstream edges are non-unique.

## Promoted sendLogin-side facts (#884)

```text
sender=tibia::authentication::TLoginProtocolMessageHandler
signal=sendLoginMessage
connectImpl_callsite=0x7c6b9f
adapter=0xbd3050
receiver_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
receiver_field_definition=UNKNOWN
receiver_owner_chain=UNKNOWN
receiver_identity=UNKNOWN
complete_sender_receiver_pair_proven=false
sendlogin_causal_binding_proven=false
FIRST_MISSING_BOUNDARY=CONNECTION_OWNER_FDE_DIRECT_CALLER_NOT_UNIQUE
```

The exact target-specific direct-caller search for connection-owner FDE `0x7c6700..0x7cc933` yields zero accepted direct caller candidates. That is a fail-closed stop, not evidence of absence of an owner or constructor.

Source #884 current PR head `18a0567c61d3f606e4a8d72e4ab832583ca6b429`; scientific source head `29d30b7de6a59bfa0a40c619abfbf3f3061692e1`; exact source analysis `33866338005` / job `101001945445`; artifact `9934120718`, digest `sha256:2a8313249628076f1daef8766ac07ae6adf4fdc72e5f232f6b955ceaa4b62614`.

Current exact-head focused/CI/governance/self-hosted runs on `18a0567...`: `33867156653`, `33867157221`, `33867156626`, `33867156624`, all SUCCESS.

## Promoted queue/QSlot-side facts (#885)

The exact queue connection remains:

```text
sender=tibia::protocol::TProtocolMessageQueue
signal_index=0xbf
signal_name=clientMessageReadyToProcess
signal_body=0xbd2190
connectImpl_callsite=0xbe2eee
connectImpl_fde=0xbe2a50..0xbe3086
receiver_provenance=ENTRY_ARG:rdi
```

The QSlot object/function is now exact-current proven:

```text
allocation=operator new@0xbe2eb1
allocation_size=0x20
handoff=0xbe2ec3: r9 <- rax
dispatch_impl=0xbe4df0
callable_payload=(0xbd2190, 0)
callable_target=0xbd2190
qslot_identity_proven=true
```

The object stores place the dispatcher at `QSlot+0x08` and the callable pair at `QSlot+0x10..+0x20`. The dispatcher branch `0xbe4e38..0xbe4e52` uses the zero-lowbit/zero-adjustment direct path to `0xbd2190`. This proves QSlot callable identity, but the target FDE `0xbd2190..0xbd2495` still contains multiple downstream direct/indirect edges, so no unique queue/TCP writer edge is promoted.

```text
queue_signal_writer_identity=UNKNOWN
next_unique_writer_edge=UNKNOWN
final_queue_writer_identified=false
final_tcp_writer_identified=false
final_writer_contract=UNKNOWN
FIRST_MISSING_BOUNDARY=NEXT_WRITER_EDGE_SEMANTICS_NOT_UNIQUELY_PROVEN
```

Source #885 current PR head `5fb8be7458fb8ecc12818baab5729681df67ee21`; scientific source head `2431ef51a9e3d95365fbae0d1b5d23846b9b1a99`; exact analysis `33867321414` / job `101005030098`; artifact `9934486697`, digest `sha256:a78f3c40161738d0d58c34e98d0e873f9d37920e586944963ec6e332e848a41f`.

Current exact-head focused/CI/governance/self-hosted runs on `5fb8be7...`: `33867557971`, `33867558234`, `33867558010`, `33867557979`, all SUCCESS.

## Withheld / integration decision

```text
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
SENDLOGIN_RECEIVER_CLASS=UNKNOWN
COMPLETE_SENDLOGIN_CAUSAL_BINDING=NOT_PROVEN
QUEUE_SIGNAL_RELAY_RECEIVER_CLASS=UNKNOWN
NEXT_UNIQUE_WRITER_EDGE=UNKNOWN
FINAL_QUEUE_WRITER=UNKNOWN
FINAL_TCP_WRITER=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
```

Therefore no Track B mutation, runtime Field6 experiment, official-client execution, login, OCR/Vision, or official-service E2E is authorized. PR #284 remains blocked and unchanged.

## Next bounded source tasks

Two independent follow-ups are justified. Each changes proof mode and must not replay a consumed discriminator.

```text
OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE
  Start only from connection-owner FDE 0x7c6700..0x7cc933, its entry-rdi owner object, and the proved receiver field [entry-rdi-derived-rbx+0x88]. Resolve only bounded in-FDE or one unique identity-preserving vtable/RTTI/QMeta owner edge. Do not repeat the zero-result direct-caller search and do not open a global constructor/RTTI/QMeta/QObject census. Only if exact owner identity is proven may +0x88 receiver typing be attempted.

OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE
  Start only from connectImpl@0xbe2eee, receiver provenance ENTRY_ARG:rdi, exact QSlot callable 0xbd2190, and the causally carried GameclientMessage shared pair. Resolve the receiver object/class identity and determine whether this exact connection is a signal relay. Only if unique may one next identity-preserving clientMessageReadyToProcess edge be followed. No global Qt/socket/writer census.
```

These follow-ups may run in parallel only after a separate fresh-main alias-registration lifecycle. No runtime or Track B authority is implied by this promotion.
