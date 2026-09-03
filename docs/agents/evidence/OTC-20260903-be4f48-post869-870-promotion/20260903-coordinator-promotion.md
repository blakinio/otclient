# Coordinator promotion — be4f48 post-#869/#870 source blockers

Decision: **SOURCE_BLOCKER / BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA**.

This clean coordinator promotion is reconstructed from trusted `main@a35bbacd475a31ce52736ccbc3b5e837626def66` and the two independent exact-current source Draft PRs #869 and #870. Neither source analyzer/workflow is promoted, and Track B PR #284 remains untouched.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Source A — sendLogin sender peer (#869)

Final source head `cce4f0dc4f34eecb069f326681958e58a8e6585c` passed:

```text
focused workflow 33778468114 = SUCCESS
CI               33778468410 = SUCCESS
governance       33778468111 = SUCCESS
self-hosted gate 33778468084 = SUCCESS
artifact         9902622204
artifact sha256  b820e4e9423183a8277e36d8635bd31bf0feca0edbfbd0f6ecab51e133438ae2
```

Exact-current static evidence proves:

```text
peer_target=0xd052a0
peer_fde=0xd052a0..0xd052c7
peer_direct_callee=0x4d7dc0
peer_direct_callee=QMetaObject::activate(QObject*, QMetaObject const*, int, void**)
peer_role=QT_SIGNAL_BODY_CALLING_QMETAOBJECT_ACTIVATE
peer_static_metaobject_argument=0x30b68a0
peer_signal_index_argument=0
```

The previous helper interpretation is corrected:

```text
0x4d8670 -> _Znwm -> operator new(unsigned long)
role=ALLOCATOR_OPERATOR_NEW
is_qt_connection_primitive=false
```

Therefore `0x4d8670` must not be reused as sender/receiver direction evidence. The peer class owner, actual Qt connection primitive, sender/receiver endpoint identities, causal signal-to-`sendLogin` binding and complete pre-login ordering remain unproven.

## Source B — final login writer (#870)

Final source head `a87904047032fcc8c20b7ac7c1aac6c43d805207` passed:

```text
focused workflow 33779461583 = SUCCESS
CI               33779461865 = SUCCESS
governance       33779461528 = SUCCESS
self-hosted gate 33779461550 = SUCCESS
artifact         9902982410
artifact sha256  bc7529dab9a3ccf1c6c5356bbd14e7600dc8beae7205806416620e7c970bea3a
result.json sha  509ebc4086edbd5dba5b82638079568080ca56fa480baebb33e3f354c670ad9a
```

Exact-current static evidence independently proves the adapter-built serialized queue object as a 16-byte pair `{object=allocation+0x10, owner=allocation}` copied unchanged into `TProtocolMessageQueue` storage. The queue owner follow-up finds exactly one owned drain candidate:

```text
queue_vslot_0x68=0xbd24a0
owned_drain_candidate_count=1
owned_drain_candidate=0xbd2190
owned_drain_fde=0xbd2190..0xbd2495
```

However the bounded follow-up still has no unique causal consumer of the same queued `tibia::protobuf::protocol::GameclientMessage` object and does not causally reach the known downstream packet/frame seeds. Therefore:

```text
final_queue_writer_identified=false
final_tcp_writer_identified=false
final_writer_contract=UNKNOWN
FIRST_MISSING_BOUNDARY=owned queue callback 0xbd2190 -> causal consumption of queued GameclientMessage object
```

## Coordinator decision

These two sources materially narrow the problem but do **not** prove an implementable Track B wire delta. Field6 value remains `UNKNOWN`; sender-side causal ordering remains incomplete; final writer identity remains `UNKNOWN`.

No Track B payload mutation and no official-service E2E is authorized from this evidence cut. PR #284 remains unchanged.

## Next bounded source tasks

Exactly two new independent source-only discriminators are justified:

1. `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER`
   - start from exact static-metaobject anchor `0x30b68a0` and signal index `0`;
   - identify the peer class/metaobject owner and the actual bounded Qt connection primitive/direction that binds this signal to the proved `sendLogin` adapter;
   - do not reuse `0x4d8670` and do not broaden into global Qt/BFS discovery.

2. `OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION`
   - start from unique owned callback `0xbd2190` and the already-proven 16-byte queued `GameclientMessage` identity;
   - prove or falsify causal consumption of that exact object by the callback;
   - follow only the next uniquely bound writer edge if causal identity remains intact; stop immediately at ambiguity.

These tasks may run in parallel because they own independent static boundaries. Neither authorizes runtime, OCR/Vision, credentials, packet capture, official-client execution, official-service E2E or Track B #284 mutation.
