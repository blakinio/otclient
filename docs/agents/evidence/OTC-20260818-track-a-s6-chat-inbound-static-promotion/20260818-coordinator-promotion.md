# Track A S6 chat inbound static — coordinator promotion

Date: 2026-08-18  
Source Draft: PR #526  
Source final head: `7cec8d37907448e7bd025864628de9f8858781a4`  
Trusted promotion base: `main@a518ceaef9135c05e36ffd7066b3acb2d81f8c4c`  
Decision: **ACCEPT_BOUNDED_PARTIAL**

## Promoted exact-build boundaries

```text
TProtocolMessageQueue
  staticMetaObject 0x3085b60
  qt_static_metacall 0xdf5fe0
  355 methods / 192 signals
  21  receivedTalkMessage
  23  receivedMessageMessage
  54  receivedOpenChannelMessage
  85  receivedChannelsMessage
  86  receivedPrivateChannelMessage
  89  receivedOpenOwnChannelMessage
  90  receivedCloseChannelMessage
  115 receivedChannelEventMessage
  188 receivedNpcTalkPartersMessage

TChatProtocolMessageHandler
  staticMetaObject 0x30877c0
  qt_static_metacall 0xd05f20
  13 methods / 2 signals
  0 currentlyAvailableChannels [signal]
  1 publishGameAction [signal]
  2 handleTalkMessage
  3 handleMessageMessage
  4 handleOpenChannelMessage
  5 handleOpenOwnChannelMessage
  6 handleCloseChannelMessage
  7 handleChannelsMessage
  8 handlePrivateChannelMessage
  9 handleChannelEventMessage
  10 handleNpcTalkPartersMessage
  11 onChatProtocolMessageHandlerOptionsChanged
  12 onPlayerCreatureAddedToCreatureStorage

TChatChannelStorage
  staticMetaObject 0x3087900
  qt_static_metacall 0xd05c50
  6 methods / 5 signals
  0 newChatChannelOpened [signal]
  1 chatChannelReopend [signal]
  2 chatChannelRemoved [signal]
  3 entryAddedToChatChannel [signal]
  4 publishGameAction [signal]
  5 onPlayerCreatureAddedToCreatureStorage
```

`chatChannelReopend` is preserved with the exact spelling encoded in the retained build metadata.

## Typed registration surface

S1 artifact `9315562574` retains exact `TProtocolMessageQueue::registerServerMessage<T>` template type strings for the nine corresponding protobuf messages. The signatures prove that each instantiation accepts a `TProtocolMessageQueue` member-function pointer taking `const T&`.

The concrete member pointer passed to a registration call is not retained. Therefore:

```yaml
REGISTERED_MEMBER_POINTER_EQUALS_SUFFIX_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
```

## Retained UNKNOWNs

```yaml
QUEUE_SIGNAL_TO_CHAT_HANDLER_CONNECTION: UNKNOWN
CHAT_HANDLER_TO_CHANNEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CHAT_DELIVERY: NOT_OBSERVED
```

The coordinator explicitly rejects promotion of suffix-matched `receivedX`/`handleX` names into an actual QObject/direct-call dispatch edge without a connection/call-dataflow discriminator.

## Provenance

```text
S6 discriminator
run 32127503296
artifact 9320905712
digest sha256:8016ce5b88f030335a9104e12c73ab320518b66505ed820833dc8e1bacf3c478

historical exhaustive QMeta source
run 31790507112
job 94736106350
source head 9afdc76ca6fe238742f270e22d8ecf4abe5ba9a2
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70

S1 type-info artifact
run 32112814216
artifact 9315562574
digest sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

## Source exact-head validation

```text
CI 32127738468 = SUCCESS
Track A governance 32127738121 = SUCCESS
reviews = 0
unresolved review threads = 0
main freshness at source finalization = 0 behind
```

No new official-client download/execution, physical runtime, Synology/X11/VNC, process-memory access, credentials, login or gameplay was used. PR #475 runtime/native-login surfaces remained untouched. Physical E2E is `NOT_APPLICABLE` for this static exact-evidence task.
