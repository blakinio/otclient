---
task_id: OTC-20260818-track-a-s3-player-queue-receiver-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
execution_mode: github_only
branch: research/OTC-20260818-track-a-s3-player-queue-receiver-static
base_branch: main
base_main: 592e193a5ada1c40d23193038f350e23c539898b
related_pr: pending
created: 2026-08-18T10:32:00+02:00
updated: 2026-08-18T10:32:00+02:00
risk: medium
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
  - .github/workflows/track-a-s3-player-queue-receiver-static.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s3-player-queue-receiver-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s3-player-queue-receiver-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s3-player-queue-receiver-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static-promotion/**
  - exact Qt/QSlotObject connection patterns from prior promoted Track A research
depends_on:
  - OTC-20260818-track-a-s2-player-inbound-static
blocks: []
non_overlap:
  - PR #475 physical runtime/worldmap/native-login surfaces will not be observed or mutated.
  - PR #302 direct-player-position Draft will not be modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: medium
decomposition_decision: single
validation_level: focused
---

# Objective

Resolve one exact static connection edge for the promoted player receive signals:

```text
TProtocolMessageQueue receivedPlayer* typed signal
  -> QObject::connect / QSlotObject construction
  -> exact receiver object/type
  -> exact receiver member/trampoline where statically provable
```

The task must follow evidence rather than assume the receiver is `TPlayerProtocolMessageHandler`.

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
platform: official_native_linux_only
```

# Canonical inputs from #513

```text
TProtocolMessageQueue:
  staticMetaObject   0x3085b60
  qt_static_metacall 0xdf5fe0
  methods/signals    355 / 192

player signals:
  index 34  receivedPlayerDataCurrentMessage @ 0xdf8bc1
  index 43  receivedPlayerDataBasicMessage @ 0xdf8d3b
  index 48  receivedPlayerStateMessage @ 0xdf8e0d
  index 49  receivedPlayerSkillsMessage @ 0xdf8e37
  index 117 receivedPlayerInventoryMessage @ 0xdf899f

TPlayerProtocolMessageHandler:
  primary vptr 0x308a008
  direct QMeta ownership of receivedPlayer* = DISPROVEN
```

# Questions

1. Recover exact static references to the five queue signal stubs / signal PMF identities and nearby connection-construction code.
2. Identify `QObject::connect`/typed-connect or QSlotObject construction boundaries from direct code/dataflow rather than address proximity.
3. Prove receiver object/type with vtable/RTTI/QMeta provenance where possible.
4. Prove exact receiver member/trampoline only where PMF/QSlotObject/control flow supports it.
5. If multiple player signals share one receiver construction family, record the common pattern; do not extrapolate beyond proven entries.
6. Keep `handler -> TPlayerData` outside this task unless the connection discriminator directly and unambiguously reaches that edge.

# Acceptance

- [ ] exact client fence revalidated;
- [ ] at least one of the five player queue signals has a bounded exact static connection-construction result or a terminal `UNKNOWN` after exhaustive bounded discrimination;
- [ ] receiver type classified `FACT | INFERENCE | UNKNOWN`;
- [ ] receiver member/trampoline classified `FACT | INFERENCE | UNKNOWN`;
- [ ] no assumption that `TPlayerProtocolMessageHandler` is receiver without direct proof;
- [ ] no runtime/login/Synology/X11/process-memory/credential access;
- [ ] no raw client committed/uploaded;
- [ ] temporary producer removed before promotion;
- [ ] exact-head CI/governance and review hygiene before terminal disposition.

# Checkpoint

```yaml
checkpoint_version: 1
status: investigating
last_completed_step: claimed the post-#513 queue-to-receiver static frontier with complete runtime admission metadata and explicit non-overlap
blockers: []
next_action: open Draft PR and run one bounded exact-client discriminator around the five signal identities and QObject/QSlotObject connection construction.
```
