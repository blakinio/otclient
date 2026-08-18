---
task_id: OTC-20260818-track-a-s6-chat-inbound-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-evidence-reuse
execution_mode: github_only
branch: research/OTC-20260818-track-a-s6-chat-inbound-static
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
related_pr: pending
created: 2026-08-18T12:30:00+02:00
updated: 2026-08-18T12:30:00+02:00
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

Resolve, using only already-sanitized exact-build/repository evidence:

```text
GameserverMessageTalk / Channels / ChannelEvent / OpenChannel /
CloseChannel / OpenOwnChannel / PrivateChannel
  -> exact received* owner and QMeta signal indices
  -> exact TChatProtocolMessageHandler handle* QMeta boundaries
  -> exact TChatChannelStorage QMeta boundaries
```

Do not infer queue->handler or handler->storage edges from naming alone.

# Acceptance

- [ ] no new official-client download/execution;
- [ ] recover exact queue owner and indices for all seven chat receive surfaces;
- [ ] recover exact handler QMeta methods/signals;
- [ ] recover exact chat-channel storage QMeta methods/signals;
- [ ] prove exact registerServerMessage<T> type surfaces where retained evidence permits;
- [ ] explicit FACT / INFERENCE / UNKNOWN classifications;
- [ ] no runtime/Synology/X11/process-memory/credentials/login/gameplay;
- [ ] no PR #475 observation/mutation;
- [ ] temporary log-reuse workflow removed before promotion;
- [ ] exact-head CI/governance and coordinator closeout.

# Checkpoint

```yaml
checkpoint_version: 1
status: investigating
last_completed_step: admitted chat-only static proof on current main after S5 promotion
blockers: []
next_action: reuse historical exact-SHA exhaustive QMeta log and S1 type/name surfaces for queue, TChatProtocolMessageHandler and TChatChannelStorage.
```
