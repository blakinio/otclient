---
task_id: OTC-20260818-track-a-s6-chat-inbound-static
status: ready_for_coordinator
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: final_exact_head
execution_mode: github_only
branch: research/OTC-20260818-track-a-s6-chat-inbound-static
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
related_pr: 526
created: 2026-08-18T12:30:00+02:00
updated: 2026-08-18T12:39:00+02:00
risk: low
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
owned_paths:
  - .github/workflows/track-a-s6-chat-inbound-log-reuse.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s6-chat-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s6-chat-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s6-chat-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - S1 exact type/name artifact run 32112814216 / artifact 9315562574
depends_on:
  - OTC-20260818-track-a-s5-container-inbound-static
blocks: []
non_overlap:
  - PR #475 runtime/native-login surfaces are not observed or mutated.
  - PR #302 direct-player-position Draft is not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: low
decomposition_decision: single
validation_level: focused
---

# Objective

Resolve the full handler-aligned chat inbound family using only already-sanitized exact-build/repository evidence.

# Result

Producer:

```text
run      32127503296
artifact 9320905712
digest   sha256:8016ce5b88f030335a9104e12c73ab320518b66505ed820833dc8e1bacf3c478
```

Exact QMeta source:

```text
run/job 31790507112 / 94736106350
head    9afdc76ca6fe238742f270e22d8ecf4abe5ba9a2
log sha sha256:481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70
```

Promoted researcher FACT candidates:

```text
TProtocolMessageQueue
  21 receivedTalkMessage
  23 receivedMessageMessage
  54 receivedOpenChannelMessage
  85 receivedChannelsMessage
  86 receivedPrivateChannelMessage
  89 receivedOpenOwnChannelMessage
  90 receivedCloseChannelMessage
  115 receivedChannelEventMessage
  188 receivedNpcTalkPartersMessage

TChatProtocolMessageHandler
  QMeta 0x30877c0
  qt_static_metacall 0xd05f20
  13 methods / 2 signals
  handle*Message methods = indices 2..10, exactly nine

TChatChannelStorage
  QMeta 0x3087900
  qt_static_metacall 0xd05c50
  6 methods / 5 signals
```

S1 retained exact `registerServerMessage<T>` template type contracts for all nine corresponding protobuf message types.

Boundaries retained deliberately:

```yaml
REGISTERED_MEMBER_POINTER_EQUALS_SUFFIX_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
QUEUE_SIGNAL_TO_CHAT_HANDLER_CONNECTION: UNKNOWN
CHAT_HANDLER_TO_CHANNEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CHAT_DELIVERY: NOT_OBSERVED
```

# Acceptance

- [x] no new official-client download/execution;
- [x] exact queue owner and indices for all nine handler-aligned chat receive surfaces;
- [x] complete TChatProtocolMessageHandler QMeta method/signal table;
- [x] complete TChatChannelStorage QMeta method/signal table;
- [x] exact registerServerMessage<T> type surfaces identified for all nine types;
- [x] explicit FACT / INFERENCE / UNKNOWN classifications;
- [x] no runtime/Synology/X11/process-memory/credentials/login/gameplay;
- [x] no PR #475 observation/mutation;
- [ ] temporary log-reuse workflow removed before promotion;
- [ ] exact-head CI/governance and coordinator closeout.

# Checkpoint

```yaml
checkpoint_version: 3
status: ready_for_coordinator
last_completed_step: normalized complete nine-message queue/handler/storage QMeta boundaries and S1 registration type contracts into durable evidence/report
blockers: []
next_action: remove temporary discriminator workflow, reconcile with live main if necessary, run exact-head CI/governance, then coordinator-promote and archive S6.
```
