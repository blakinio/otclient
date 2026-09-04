# Coordinator promotion — be4f48 post-#874/#875 receiver/writer boundaries

Decision: **SOURCE_BLOCKER / BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA**.

This clean coordinator promotion is reconstructed from fresh trusted `main@446eb643d6ef24dc996a410df812393e19800973` and the terminal exact-current source Draft PRs #874 and #875. Neither source analyzer/workflow is promoted. Track B PR #284 remains untouched.

## Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Source #874 — queue drain consumption

Final source head and exact-head qualification:

```text
source PR                 #874
source head               369acfb075e8a9d2716dcd73280ca092e0600332
focused workflow          33784324169 = SUCCESS
focused job               100745591266 = SUCCESS
CI                         33784324506 = SUCCESS
governance                 33784324157 = SUCCESS
self-hosted boundary       33784324096 = SUCCESS
artifact                   9904873672
artifact sha256            acb7f2747b0c83c57bf03dba3690b90e4df4b8854b74e94d498e6a885b096e01
result.json sha256         47ac0c9f8dc79d024a8eaa484474bd8e33bf9cf2407458c2a2bc8256211ddb70
terminal result            QUEUE_DRAIN_CONSUMPTION_PROVEN
```

Accepted exact-current facts:

- the serialized queue object is the exact 16-byte `{object=allocation+0x10, owner=allocation}` pair copied unchanged into `TProtocolMessageQueue` storage through target `0xbd24a0`;
- owned drain callback `0xbd2190..0xbd2495` copies that exact dequeued pair, retains the owner lifetime, advances queue begin by one 16-byte element, and dispatches the copied pair;
- direct dispatch `0xbd22c2 -> 0x4d7dc0` resolves to `QMetaObject::activate(QObject*, QMetaObject const*, int, void**)`;
- sender is `TProtocolMessageQueue`, static metaobject is `0x30b73e0`, signal index is decimal `191` / hex `0xbf`;
- `argv[1]` points to the exact copied 16-byte `GameclientMessage` shared pair.

This **proves causal consumption by the queue drain**. It does not prove the receiver/slot/writer connected to signal `0xbf`, so `NEXT_UNIQUE_WRITER_EDGE=UNKNOWN`, `FINAL_QUEUE_WRITER_IDENTIFIED=false`, `FINAL_TCP_WRITER_IDENTIFIED=false` and `FINAL_WRITER_CONTRACT=UNKNOWN` remain mandatory.

## Source #875 — sendLogin peer metaowner

Final PR head and exact-head qualification:

```text
source PR                 #875
final PR head             9653268fc57e94adcfb41c1f6b1a3e7914f2aa0f
source analysis head      6174d44df2017bc5a435de0e843ee824520a12a5
exact source run          33838135600 = SUCCESS
exact source job          100914746055 = SUCCESS
source artifact           9923975240
source artifact sha256    e96c91c2b8bf408c06ff829ac25d48d39595f719a275e7361886cea93cb7d8ff
final focused workflow    33838475637 = SUCCESS
final CI                   33838475915 = SUCCESS
final governance           33838475665 = SUCCESS
final self-hosted boundary 33838475643 = SUCCESS
final artifact             9924087376
final artifact sha256      47a0a890d903a3d400ac0aa0d0530517249934f496276c3b0a2f4dce57d5b6de
terminal result            SOURCE_BLOCKER
```

Accepted exact-current facts:

- peer `0xd052a0` belongs to `tibia::authentication::TLoginProtocolMessageHandler`;
- peer signal index `0` is `sendLoginMessage`;
- the actual bounded Qt connection primitive is `QObject::connectImpl(...)` at callsite `0x7c6b9f`;
- the selected connection block is bounded by the previous `connectImpl` at `0x7c6b07` and contains the unique adapter reference `0x7c6b34`, peer reference `0x7c6b40` and allocator call `0x7c6b5e`;
- the hidden-sret ABI is independently proven by the same `rbp` return storage flowing to `QMetaObject::Connection::~Connection()`;
- sender endpoint is `TLoginProtocolMessageHandler` and the sender metaobject/signal are bound to this connection;
- adapter `0xbd3050` is copied into the allocated Qt slot object at field `+0x10` before the selected `connectImpl` call;
- receiver object provenance is exact: `[entry-rdi-derived-rbx+0x88]`.

The receiver's **class identity remains UNKNOWN**. Therefore the complete sender/receiver pair and causal signal-to-`sendLogin` binding remain `NOT_PROVEN`.

## Combined boundary

The two source lanes now prove substantially more of the native path:

```text
TLoginProtocolMessageHandler::sendLoginMessage
  -> QObject::connectImpl @ 0x7c6b9f
  -> QSlot object carrying adapter 0xbd3050
  -> receiver object from [rbx+0x88], class UNKNOWN

sendLogin-created exact GameclientMessage pair
  -> TProtocolMessageQueue insertion 0xbd24a0
  -> owned drain 0xbd2190
  -> exact causal consumption PROVEN
  -> QMetaObject::activate signal 0xbf
  -> connected receiver/writer UNKNOWN
```

This is not yet an implementable Track B wire delta. Field6 value is still UNKNOWN, complete pre-login ordering is still UNKNOWN, the final writer contract is still UNKNOWN, and no protocol mutation or official-service E2E is authorized.

## Next admitted source boundaries

Exactly two independent source-only follow-ups are justified:

```text
OTC-BE4F48-SENDLOGIN-RECEIVER-IDENTITY
  [entry-rdi-derived-rbx+0x88] -> exact receiver class identity
  -> complete the sender/receiver pair for connectImpl @ 0x7c6b9f
  -> prove or reject causal sendLogin adapter binding

OTC-BE4F48-QUEUE-SIGNAL-BF-RECEIVER
  TProtocolMessageQueue signal 0xbf carrying the exact GameclientMessage pair
  -> unique connected receiver/slot/writer identity
  -> at most the next uniquely identity-preserving writer edge
```

These tasks may run in parallel. They must not reuse historical addresses as authority without exact-current derivation, broaden into global Qt/socket/writer census, execute the official client, use OCR/Vision, login, access credentials/process memory, capture packets, run official-service E2E, or modify Track B PR #284.

## Terminal coordinator state

```text
QUEUE_DRAIN_CAUSAL_CONSUMPTION=true
SENDLOGIN_SENDER_IDENTITY=tibia::authentication::TLoginProtocolMessageHandler
SENDLOGIN_SIGNAL=sendLoginMessage
SENDLOGIN_CONNECTION_PRIMITIVE=QObject::connectImpl@0x7c6b9f
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
QUEUE_SIGNAL_BF_RECEIVER_WRITER=UNKNOWN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
terminal_result=SOURCE_BLOCKER
```
