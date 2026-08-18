---
task_id: OTC-20260818-track-a-s6-chat-inbound-static
status: completed_bounded_partial
session_role: researcher_then_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
execution_mode: github_only
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PHYSICAL_E2E_REQUIRED: false
source_pr: 526
source_final_head: 7cec8d37907448e7bd025864628de9f8858781a4
promotion_decision: ACCEPT_BOUNDED_PARTIAL
ownership_release_state: released
---

# Result

S6 reused only already-sanitized exact-build/repository evidence. It recovered the complete nine-message QMeta surface aligned with `tibia::chat::TChatProtocolMessageHandler::handle*Message`, plus the complete `TChatChannelStorage` QMeta surface.

## Promoted exact boundaries

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
  QMeta 0x30877c0
  qt_static_metacall 0xd05f20
  13 methods / 2 signals
  message handlers = indices 2..10

TChatChannelStorage
  QMeta 0x3087900
  qt_static_metacall 0xd05c50
  6 methods / 5 signals
```

S1 also proves `TProtocolMessageQueue::registerServerMessage<T>` member-pointer type contracts for all nine corresponding protobuf message types.

## Retained boundaries

```yaml
REGISTERED_MEMBER_POINTER_EQUALS_SUFFIX_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
QUEUE_SIGNAL_TO_CHAT_HANDLER_CONNECTION: UNKNOWN
CHAT_HANDLER_TO_CHANNEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CHAT_DELIVERY: NOT_OBSERVED
```

## Provenance / validation

```text
S6 producer run 32127503296
artifact 9320905712
artifact digest sha256:8016ce5b88f030335a9104e12c73ab320518b66505ed820833dc8e1bacf3c478

source final head 7cec8d37907448e7bd025864628de9f8858781a4
CI 32127738468 = SUCCESS
Track A governance 32127738121 = SUCCESS
reviews = 0
unresolved review threads = 0
```

No new official-client bytes, client execution, Synology/X11/VNC, process memory, credentials, login or gameplay were used. PR #475 runtime/native-login surfaces were not observed or mutated.
