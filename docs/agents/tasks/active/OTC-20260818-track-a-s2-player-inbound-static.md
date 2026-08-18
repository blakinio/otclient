---
task_id: OTC-20260818-track-a-s2-player-inbound-static
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-head-validation
execution_mode: github_only
branch: research/OTC-20260818-track-a-s2-player-inbound-static
base_branch: main
base_main: a9e7ab21ed0962482e4381aadd50be92714785a6
related_pr: 512
created: 2026-08-18T10:06:00+02:00
updated: 2026-08-18T10:25:00+02:00
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
  - docs/agents/tasks/active/OTC-20260818-track-a-s2-player-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s2-player-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - tools/tibia_runtime_bridge/resolver.py
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json
  - exact QMeta reconstruction pattern from merged PR #505
  - PR #302 exact static TPlayerData evidence as read-only negative/control material
depends_on:
  - OTC-20260818-track-a-s1-unfiltered-static-census
blocks: []
non_overlap:
  - PR #475 physical runtime/worldmap/native-login surfaces were not observed or mutated.
  - PR #302 direct-player-position Draft was not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: medium
decomposition_decision: single
validation_level: focused
repair_cycles_for_current_gate: 1
---

# Objective

Resolve the exact static player inbound message boundary without consuming the active physical runtime:

```text
GameserverMessagePlayer*
  -> exact typed TProtocolMessageQueue receivedPlayer* QMeta signals
  -> bound the receiver/handler/data edges that remain unknown
```

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Acceptance inventory

- [x] exact client fence revalidated on both accepted hosted producers;
- [x] `TPlayerProtocolMessageHandler` metaobject identity/method table recovered;
- [x] unique full-range `TPlayerProtocolMessageHandler` QMeta dispatch table recovered;
- [x] direct QMeta ownership of `receivedPlayer*Message` by `TPlayerProtocolMessageHandler` disproven;
- [x] exact owner of all five selected received methods proven as `tibia::protocol::TProtocolMessageQueue`;
- [x] queue staticMetaObject/static_metacall/method/signal counts recovered;
- [x] exact QMeta indices, signatures, protobuf parameter types and signal stubs for all five selected player messages persisted;
- [x] exact `QMetaObject::activate@0x4dedc0` signal-stub behavior persisted;
- [x] `TPlayerData` exact QMeta surface recovered and kept separate from unproven inbound storage semantics;
- [x] handler -> `TPlayerData` relation explicitly classified `UNKNOWN` because no direct edge was found in this bounded task;
- [x] existing `TPlayerData +0x78/+0x7c/+0x80` P0 candidate not overpromoted as inbound target;
- [x] no runtime/login/Synology/X11/process-memory/credential access;
- [x] no raw proprietary client committed/uploaded;
- [x] temporary producer workflow removed from final diff;
- [x] E2E = `NOT_APPLICABLE`: static exact-file discovery only;
- [x] final full diff/path audit completed before admission-metadata-only repair;
- [x] current main matched task base at final pre-repair audit;
- [ ] exact-head required CI/governance after admission-metadata repair;
- [ ] zero unresolved material review findings;
- [ ] coordinator/promotion disposition.

# Accepted producer evidence

Phase 1 — handler/data QMeta reconstruction:

```yaml
run: 32115252111
job: 95643199117
head: 74433287fa9549361eed3733c513b3f46fd2601c
artifact: 9316455906
artifact_digest: sha256:434340656a520110ac417fbd1fbd844664e7b2d49da418e7de5bc21b8f830fa5
result: SUCCESS
```

Phase 2 — global QMeta ownership census:

```yaml
run: 32115662884
job: 95644479664
head: ea22c8db751f82fff17ae22c2be4f4fc3cd0420d
artifact: 9316573491
artifact_digest: sha256:ec97899357f6db77d45cf915d9133c778d48469f03628ea8914d6402ca3aca8f
result: SUCCESS
global_valid_metaobjects: 708
target_matches: 5
target_owner_classes:
  - tibia::protocol::TProtocolMessageQueue
```

# Promotable exact contracts

```yaml
TProtocolMessageQueue:
  static_metaobject: 0x3085b60
  static_metacall: 0xdf5fe0
  method_count: 355
  signal_count: 192
  dispatch_table: 0x1d8bd6c

receivedPlayerDataCurrentMessage:
  qmeta_index: 34
  protobuf_type: GameserverMessagePlayerDataCurrent
  signal_stub: 0xdf8bc1

receivedPlayerDataBasicMessage:
  qmeta_index: 43
  protobuf_type: GameserverMessagePlayerDataBasic
  signal_stub: 0xdf8d3b

receivedPlayerStateMessage:
  qmeta_index: 48
  protobuf_type: GameserverMessagePlayerState
  signal_stub: 0xdf8e0d

receivedPlayerSkillsMessage:
  qmeta_index: 49
  protobuf_type: GameserverMessagePlayerSkills
  signal_stub: 0xdf8e37

receivedPlayerInventoryMessage:
  qmeta_index: 117
  protobuf_type: GameserverMessagePlayerInventory
  signal_stub: 0xdf899f
```

Every listed stub invokes `QMetaObject::activate@0x4dedc0` with the corresponding signal index.

# Negative/control results

```yaml
DISPROVEN:
  receivedPlayer_methods_direct_TPlayerProtocolMessageHandler_QMeta_ownership: true

UNKNOWN:
  network_decoder_to_queue_signal_emission: true
  queue_signal_to_TPlayerProtocolMessageHandler_connection: true
  exact_connected_receiver_member: true
  handler_to_TPlayerData_mutation: true
  TPlayerData_XYZ_candidate_as_inbound_target: true
```

# Repair history

First phase-1 run `32114891658 / 95642067206` passed both exact-client hashes but failed in producer tooling with Capstone `CS_ERR_SKIPDATA`. The bounded repair separated function decoding from whole-section skipdata scanning and guarded pseudo-instruction operand access. No semantic result from the failed run was promoted.

Final governance run `32116125158` failed only because this static task record omitted the universal Track A admission keys even though `runtime_access:none` was already declared. The exact failure listed `runtime_owner_task`, `runtime_namespace`, `canonical_registration`, both lease-generation fields, `gate_a`, `generation_rebind`, `gate_b`, `bootstrap` and `target_uniqueness`. This checkpoint adds every required key explicitly as `NOT_APPLICABLE`; no research or runtime semantics changed.

# Durable evidence

```text
docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/qmeta-contract.json
docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/received-player-owner.json
docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/received-player-signal-stubs.txt
docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/anchor-code-xrefs.json
docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/result.md
docs/agents/reports/OTCLIENT-20260818-track-a-s2-player-inbound-static.md
```

# Next frontier

```text
TProtocolMessageQueue receivedPlayer* signal
  -> exact QObject typed-connect construction
  -> exact receiver object/type
  -> exact receiver member / QSlotObject trampoline
```

Only after that edge should a later static task trace the receiver into `TPlayerData`.

# Checkpoint

```yaml
checkpoint_version: 5
status: validating
phase: exact-head-validation
pr: 512
research_result: COMPLETE_BOUNDED
producer_workflow_removed: true
last_completed_step: repaired final governance admission metadata exactly as required; no evidence or scope change
blockers: []
next_action: require exact-head Track A governance and CI on the admission-fixed head, then inspect review hygiene and perform coordinator promotion before creating the queue-to-receiver follow-up.
```
