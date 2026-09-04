# Coordinator promotion — exact-current be4f48 post #889/#890

Decision: **SOURCE_BLOCKER / BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA**.

This promotion is rebuilt from trusted `main@e94e6c5764851f9cb62691d90c55f42e9c6253a1` and consumes only sanitized exact-current facts from source Draft PRs #889 and #890. Neither source analyzer/workflow is promoted. Track B PR #284 remains untouched.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Independent coordinator falsification

The coordinator re-read both terminal source results, the bounded analyzer logic that produced the decisive boundaries, all changed-path sets, current exact-head workflow status, and review hygiene.

No source worker self-promotion is accepted. The only promoted claims below are exact-current sanitized facts that survive this independent check.

```text
INDEPENDENT_COORDINATOR_FALSIFICATION=PASS
MATERIAL_FINDINGS_OPEN=0
IMPLEMENTABLE_DELTA_COUNT=0
SOURCE_WORKER_SELF_PROMOTION_USED=false
```

### Source #889 — sendLogin connection owner type

The bounded owner-type lane correctly remained fail-closed. Inside connection-owner FDE `0x7c6700..0x7cc933`, no typed vptr/RTTI event was tied to `ENTRY_ARG:rdi`. Exactly one entry-object-bound direct edge was admitted:

```text
0x7c67b8 -> 0x7e8f30
```

That callee did not yield one exact type under the task's proof rule. The analyzer therefore did not type the owner, did not type the `+0x88` receiver, and did not claim sendLogin causal binding.

```text
CONNECTION_OWNER_ENTRY_OBJECT=ENTRY_ARG:rdi
CONNECTION_OWNER_IDENTITY=UNKNOWN
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=false
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
FIRST_MISSING_BOUNDARY=UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN
```

Scientific source head `903b7e6c5f9452d9be545d698355bcb151c62aec`; run `33872240794`, job `101020701224`; artifact `9936389943`, digest `sha256:f4fcfd66b409c31ddaf7b06c471eccd33a638d7ff6cdaeeae9c4f47bef147636`.

Final PR head `66bd46b42cbc5d18e0f338d4a37b2ee13390adb4` passed focused source `33872718283`, CI `33872718522`, Track A governance `33872718247`, and self-hosted boundary `33872718325`.

### Source #890 — queue signal relay receiver type

The queue-side lane produced one new exact-current positive identity without widening into a global connect/socket/writer census.

Within only FDE `0xbe2a50..0xbe3086`, the promoted receiver provenance `ENTRY_ARG:rdi` is tied to the constructor/root-object path. The active primary vptr store is:

```text
QObject::QObject(QObject*) call=0xbe2a6d
entry-object root vptr store=0xbe2a85
base_register=rbx
object_offset=0x0
vptr=0x30ed588
typeinfo=0x30ed548
typeinfo_raw_name=N5tibia8protocol21TProtocolMessageQueueE
receiver_identity=tibia::protocol::TProtocolMessageQueue
```

The exact receiver therefore matches the already-promoted signal owner `tibia::protocol::TProtocolMessageQueue`. Together with promoted QSlot callable `0xbd2190`, which is the `clientMessageReadyToProcess` signal body, this exact connection is classified as a signal relay:

```text
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_RECEIVER_IDENTITY_PROVEN=true
QSLOT_FUNCTION_TARGET=0xbd2190
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
```

This does **not** identify the next relay endpoint or writer. The lane correctly stops at:

```text
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIRST_MISSING_BOUNDARY=NEXT_RELAY_EDGE_NOT_UNIQUELY_PROVEN_WITHIN_BOUNDED_RECEIVER_TYPE_PROOF
```

Scientific source head `7dab5a0cb60f9f971ff0623aa0d5b9922bbbcd65`; run `33873246506`, job `101024010911`; artifact `9936796961`, digest `sha256:9dd2bb0d11af5240b5f0275df89f8b4bccabb3af8d19461642619883ebcc3879`.

Final PR head `a9bdeb4a39d27cbaff8f77cf67212b06c6630510` passed focused source `33873511549`, CI `33873512071`, Track A governance `33873511534`, and self-hosted boundary `33873511577`.

## Withheld / integration decision

```text
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
SENDLOGIN_CONNECTION_OWNER_CLASS=UNKNOWN
SENDLOGIN_RECEIVER_CLASS=UNKNOWN
COMPLETE_SENDLOGIN_SENDER_RECEIVER_PAIR=NOT_PROVEN
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
FINAL_QUEUE_WRITER=UNKNOWN
FINAL_TCP_WRITER=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
```

The new `TProtocolMessageQueue` receiver/relay fact is materially useful, but it is not itself an implementable wire delta. Therefore no Track B mutation, runtime Field6 experiment, OCR/Vision run, login, or official-service E2E is authorized.

## Next bounded source tasks

Exactly two independent follow-ups are justified and may run in parallel after a separate alias-registration lifecycle:

```text
OTC-BE4F48-SENDLOGIN-OWNER-EDGE-7E8F30-IDENTITY
  Start only from the already-proven unique owner-bound edge 0x7c67b8 -> 0x7e8f30. Resolve the callee's treatment of the same entry owner object using bounded in-callee prologue/vptr/RTTI/QMeta/constructor semantics and at most one unique internal identity-preserving edge. Do not repeat #884 caller discovery or #889 owner-FDE scanning; no global constructor/RTTI/QMeta/QObject census.

OTC-BE4F48-QUEUE-SIGNAL-BF-NEXT-RELAY-EDGE
  Start only from the promoted TProtocolMessageQueue receiver, SIGNAL_RELAY classification, QSlot callable 0xbd2190, and exact GameclientMessage shared pair. Identify at most one next identity-preserving clientMessageReadyToProcess relay edge/endpoint inside a bounded queue constructor/metaobject/connect context. Do not redo receiver typing or QSlot construction; no global connect/socket/writer census.
```

No global writer census. No #284 mutation. No runtime or E2E.
