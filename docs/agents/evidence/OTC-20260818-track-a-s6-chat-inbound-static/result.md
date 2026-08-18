# Track A S6 — chat inbound static dispatch

Task: `OTC-20260818-track-a-s6-chat-inbound-static`  
Researcher PR: `#526`  
Execution: GitHub-hosted exact-evidence reuse only, `runtime_access: none`

## Producer provenance

```text
S6 discriminator run 32127503296
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

Exact client represented by the retained evidence:

```text
version 15.32.df7b29
size    51965216
sha256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

No new client bytes were obtained and the client was not executed by S6.

## FACT — queue receive surfaces

The exhaustive QMeta record for `tibia::protocol::TProtocolMessageQueue` is:

```text
staticMetaObject    0x3085b60
qt_static_metacall  0xdf5fe0
methods             355
signals             192
```

All nine chat-handler-aligned receive names are QMeta signals because their indices are inside the exact signal prefix:

```text
 21  receivedTalkMessage
 23  receivedMessageMessage
 54  receivedOpenChannelMessage
 85  receivedChannelsMessage
 86  receivedPrivateChannelMessage
 89  receivedOpenOwnChannelMessage
 90  receivedCloseChannelMessage
115  receivedChannelEventMessage
188  receivedNpcTalkPartersMessage
```

Classification: **FACT**.

## FACT — `TChatProtocolMessageHandler`

```text
tibia::chat::TChatProtocolMessageHandler
staticMetaObject    0x30877c0
qt_static_metacall  0xd05f20
methods             13
signals             2
```

Signals:

```text
0  currentlyAvailableChannels
1  publishGameAction
```

All nine QMeta `handle*Message` methods:

```text
 2  handleTalkMessage
 3  handleMessageMessage
 4  handleOpenChannelMessage
 5  handleOpenOwnChannelMessage
 6  handleCloseChannelMessage
 7  handleChannelsMessage
 8  handlePrivateChannelMessage
 9  handleChannelEventMessage
10  handleNpcTalkPartersMessage
```

Other QMeta slots:

```text
11  onChatProtocolMessageHandlerOptionsChanged
12  onPlayerCreatureAddedToCreatureStorage
```

Classification: **FACT** for ownership, indices, names and signal/method partition.

## FACT — `TChatChannelStorage`

```text
tibia::chat::TChatChannelStorage
staticMetaObject    0x3087900
qt_static_metacall  0xd05c50
methods             6
signals             5
```

Signals:

```text
0  newChatChannelOpened
1  chatChannelReopend
2  chatChannelRemoved
3  entryAddedToChatChannel
4  publishGameAction
```

Slot:

```text
5  onPlayerCreatureAddedToCreatureStorage
```

`chatChannelReopend` is preserved with the exact spelling present in the retained QMeta metadata.

Classification: **FACT** for the QMeta surface only.

## FACT — typed queue registration contracts

The retained S1 artifact contains exact `TProtocolMessageQueue::registerServerMessage<T>` template symbols for each of these protobuf message types:

```text
GameserverMessageTalk
GameserverMessageMessage
GameserverMessageOpenChannel
GameserverMessageOpenOwnChannel
GameserverMessageCloseChannel
GameserverMessageChannels
GameserverMessagePrivateChannel
GameserverMessageChannelEvent
GameserverMessageNpcTalkParters
```

The encoded template signature contains a `TProtocolMessageQueue` member-function pointer accepting the corresponding `const T&`. This proves the **registration type contract** for all nine types.

It does **not** identify the concrete member-pointer value passed to each registration invocation. Therefore the tempting suffix match:

```text
GameserverMessageTalk -> receivedTalkMessage
...
GameserverMessageNpcTalkParters -> receivedNpcTalkPartersMessage
```

is classified as `INFERENCE_HIGH_NOT_DIRECTLY_PROVEN`, not FACT.

## Retained UNKNOWNs

```yaml
QUEUE_SIGNAL_TO_CHAT_HANDLER_CONNECTION: UNKNOWN
CHAT_HANDLER_TO_CHANNEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CHAT_DELIVERY: NOT_OBSERVED
```

Matching `receivedX` and `handleX` names are insufficient to prove a QObject connection, direct call, queued connection or other dispatch edge. Likewise, storage QMeta signals do not prove which handler method mutates or causes storage state.

## Safety / isolation

```text
new official-client bytes obtained = false
official client executed           = false
runtime access                     = none
Synology/X11/VNC                   = false
process memory                     = false
credentials/login/gameplay         = false
PR #475 runtime touched            = false
```

S6 is a static evidence-reuse result only; physical E2E is not applicable to this task.
