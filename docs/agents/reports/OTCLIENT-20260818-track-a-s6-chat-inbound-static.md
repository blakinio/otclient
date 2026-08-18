# OTCLIENT Track A — S6 chat inbound static report

## Decision

`ACCEPT_BOUNDED_PARTIAL` as a static exact-evidence result.

S6 proves the exact QMeta receive/handler/storage boundaries for the complete nine-message surface aligned with `TChatProtocolMessageHandler::handle*Message`, while deliberately retaining the dispatch/mutation edges as unknown.

## Promoted FACT candidates

```text
TProtocolMessageQueue
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
   2 handleTalkMessage
   3 handleMessageMessage
   4 handleOpenChannelMessage
   5 handleOpenOwnChannelMessage
   6 handleCloseChannelMessage
   7 handleChannelsMessage
   8 handlePrivateChannelMessage
   9 handleChannelEventMessage
  10 handleNpcTalkPartersMessage

TChatChannelStorage
  staticMetaObject 0x3087900
  qt_static_metacall 0xd05c50
  6 methods / 5 signals
  0 newChatChannelOpened
  1 chatChannelReopend
  2 chatChannelRemoved
  3 entryAddedToChatChannel
  4 publishGameAction
```

S1 additionally proves `TProtocolMessageQueue::registerServerMessage<T>` member-pointer type contracts for all nine corresponding exact protobuf message types.

## Not promoted

```text
specific registerServerMessage<T> member pointer == suffix-matching received* signal
  -> INFERENCE_HIGH_NOT_DIRECTLY_PROVEN

TProtocolMessageQueue received* -> TChatProtocolMessageHandler handle*
  -> UNKNOWN

TChatProtocolMessageHandler -> TChatChannelStorage mutation
  -> UNKNOWN

runtime chat delivery
  -> NOT_OBSERVED
```

## Provenance

```text
S6 run      32127503296
artifact    9320905712
digest      sha256:8016ce5b88f030335a9104e12c73ab320518b66505ed820833dc8e1bacf3c478

QMeta source run/job
31790507112 / 94736106350
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70

S1 type artifact
9315562574
sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

## Isolation

No new official-client bytes, no client execution, no Synology/X11/VNC, no process-memory access, no credentials, no login and no gameplay. PR #475 runtime/native-login surfaces were not observed or mutated.
