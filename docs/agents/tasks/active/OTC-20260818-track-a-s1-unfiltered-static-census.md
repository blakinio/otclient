---
task_id: OTC-20260818-track-a-s1-unfiltered-static-census
status: validating
agent: ChatGPT
session_id: chatgpt-s1-static-census-20260818
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-head-validation
execution_mode: github_only
execution_reason: exhaustive deterministic exact-client protocol/QMeta census without touching the serialized physical runtime
branch: research/OTC-20260818-track-a-s1-unfiltered-static-census
base_branch: main
base_main: ed09418b431c28087775b419f85bed404fa85d70
related_pr: 509
created: 2026-08-18T09:29:00+02:00
updated: 2026-08-18T09:54:00+02:00
risk: medium
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
  - docs/agents/tasks/active/OTC-20260818-track-a-s1-unfiltered-static-census.md
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-complete-message-census.md
  - tools/tibia_runtime_bridge/resolver.py
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json
  - historical exact-client static producer pattern from PR #473 / commit 553e447c0662892b0c1b9cab994c4545d09f22c8
  - historical exact QMeta parser pattern from PR #505 / commit d0c1360b649fd8c4a92587b7713644c49162694c
depends_on: []
blocks: []
non_overlap:
  - PR #475 runtime branch, task record, workflow surfaces, Synology state, lease, display, login budget and physical session were not touched or observed.
  - PR #498/#499 predecessor auth/session branches were not modified.
  - Track B PR #284 and OTC2 protocol work are outside scope.
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one exact-build static S1 census with one bounded producer and one durable evidence package
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
validation_level: focused
invocation_started_at: 2026-08-18T09:29:00+02:00
last_progress_at: 2026-08-18T09:54:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Execute the archived capability-sweep programme's next safe static step without consuming or observing the active physical Track A runtime:

```text
exact official Linux client 15.32.df7b29
  -> exhaustive unfiltered generated-message census
  -> exhaustive inbound-oriented QMeta/handler string census
  -> bounded static xref candidate extraction
  -> durable S1 registries and ranked S2 follow-up edges
```

This task is deliberately independent of the currently active PR #475 runtime/world-entry/worldmap mutation work.

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
platform: official_native_linux_only
```

# Acceptance inventory

- [x] exact client compressed and unpacked hashes revalidated on hosted runner;
- [x] generated-message denominator revalidated: 349 total / 160 client->server / 189 server->client;
- [x] complete 160/189 registries persisted in Git;
- [x] fresh registries independently compared byte-for-byte with #473 sanitized control and all three hashes match exactly;
- [x] all 189 inbound names preserved;
- [x] unfiltered inbound-oriented method census persisted: 542 exact strings;
- [x] 47 distinct `*ProtocolMessageHandler` class names with direct code-to-class-string xrefs persisted;
- [x] bounded xref evidence strength explicitly stops at `DIRECT_CODE_TO_STRING_XREF` and does not claim a dispatcher edge;
- [x] current-main exact-build vptr anchors revalidated: 7/7 unique;
- [x] generated-message-to-similar-method correlations classified only as static lexical inference;
- [x] sole automatic lexical miss identified as `GameserverMessageTrackQuestFlags`; nearby `TrackedQuestFlags` methods recorded without overclaim;
- [x] no common inbound dispatcher was invented; status remains `UNKNOWN`;
- [x] producer substring-family grouping was independently falsified as semantic evidence (`Mark`/`Market`, `row`/`Browse`) and excluded from promoted conclusions;
- [x] no live/runtime/worldmap mutation or #475-owned surface touched;
- [x] no raw client bytes committed or uploaded;
- [x] temporary producer workflow removed from final branch diff;
- [x] result/report distinguish FACT / INFERENCE / UNKNOWN;
- [x] E2E = NOT_APPLICABLE: static exact-file discovery only; no product/runtime behavior changed;
- [ ] fresh final diff audit on current final head;
- [ ] exact-head required repository CI/governance green;
- [ ] zero unresolved material review findings and coordinator/promotion disposition where required;

# Fresh producer evidence

```yaml
producer_pre_checkpoint_head: cb575cec2077c8002bb6712ffac4d4dc77420499
workflow_run: 32112814216
job: 95635760592
conclusion: SUCCESS
artifact: 9315562574
artifact_digest: sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
client_executed: false
runtime_access: none
secret_access: false
pr475_runtime_touched: false
raw_client_uploaded: false
```

Primary durable evidence:

```text
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/summary.json
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/result.md
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/inbound-method-strings.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-handler-code-xrefs.tsv
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/known-anchor-vptr-resolution.json
docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md
```

# Independent denominator control

The sanitized exact-build #473 artifact was independently re-opened during this task:

```yaml
run: 32022209943
artifact: 9285763750
artifact_digest: sha256:0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
protocol_all_sha256: 55f7cf2d6d4a63df6e24b8b156e38f1a2a64a9d6394357aa914661ab48fd983b
client_to_server_sha256: 621ecb7aa1a62aae559e8d793d1aebe9289d84811bc43c4339a7153458b553f0
server_to_client_sha256: e642f661546c2e6e89ddcd77ac5e8aa9cd517408a309f95a3a367af943550d96
fresh_lists_byte_identical: true
```

# Material findings

## FACT — protocol denominator

```text
349 generated protocol message names
160 GameclientMessage*
189 GameserverMessage*
```

The historical 98-message capability-regex list was only a filtered subset and is not the denominator.

## FACT — inbound-oriented native surface

```text
542 inbound-oriented method strings
148 relevant demangled protocol/storage/session/data types in the producer artifact
51 interesting strings with direct executable code xrefs
52 retained direct xrefs
47 distinct *ProtocolMessageHandler class names with direct executable xrefs
```

Representative exact handler classes include player, creature, container, chat, game, login, market, quickloot, quest, sound, store, trade and worldmap domains.

## FACT — current exact-build anchors

```text
TGameClient                     0x3076908
TGameserverGameSession          0x3078ba0
TPlayerProtocolMessageHandler   0x308a008
TPlayerData                     0x308ca70
TContainerStorage               0x308a1a0
TCreatureStorage                0x308d078
TWorldmapProtocolMessageHandler 0x30871d8
```

All seven were re-resolved uniquely by the current-main relocation-aware resolver on the fresh exact binary.

## INFERENCE — lexical message/method alignment

188/189 generated inbound names have at least one exact/broader `handle*` / `received*` / related method surface under the bounded static matcher. This is not a call edge.

The one automatic miss is `GameserverMessageTrackQuestFlags`; `handleTrackedQuestFlagsMessage`, `receivedTrackedQuestFlagsMessage` and `onTrackedQuestFlagsChanged` exist separately and are retained as a naming-variant hypothesis only.

## UNKNOWN — semantic wiring

```text
GameserverMessageX -> exact handler dispatch
handler -> storage/controller mutation
single/global inbound dispatcher
runtime delivery/state mutation
```

# Repair history

## Repair 1 — checkout/scratch resolver path

Self-review found that the first producer implementation changed cwd to runner scratch but called the repository resolver through a relative `tools/...` path. The producer was repaired to use exact `$GITHUB_WORKSPACE` paths and assert resolver/profile existence before evidence was accepted. `c++filt -t` was also used for RTTI type encodings. No pre-repair result was promoted.

## Audit finding A1 — diagnostic family grouping rejected

Post-artifact review found that substring-only convenience grouping could misclassify names (`Mark` inside `Market`, `row` inside `Browse`). Those buckets are not durable semantic evidence and no report conclusion depends on them. Exact names/types/xrefs are used instead.

# Non-overlap / E2E

```yaml
pr475_runtime_observed: false
pr475_runtime_mutated: false
synology_used: false
x11_or_vnc_used: false
process_memory_used: false
credentials_used: false
login_performed: false
gameplay_performed: false
physical_e2e:
  result: NOT_APPLICABLE
  reason: static exact-file discovery only; no runtime/product behavior changed
```

# Ranked next static frontier

While #475 owns live native-login/worldmap runtime, next independent S2 priority is:

```text
TPlayerProtocolMessageHandler
  -> PlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
  -> exact QMeta/dispatch targets
  -> exact static owner/mutation edge into TPlayerData where provable
```

Then, independently:

```text
TCreatureProtocolMessageHandler -> TCreatureStorage
TContainerProtocolMessageHandler -> TContainerStorage
TChatProtocolMessageHandler -> chat storage/controller
```

# Checkpoint

```yaml
checkpoint_version: 3
status: validating
phase: exact-head-validation
base_main_at_claim: ed09418b431c28087775b419f85bed404fa85d70
pr: 509
pre_checkpoint_head: b25ea25b732154e273ef4182cbe9c14429acbbf6
producer_workflow_removed: true
research_result: COMPLETE
promotion_status: PENDING_FINAL_AUDIT_AND_EXACT_HEAD_CHECKS
last_completed_step: persisted complete protocol registries, 542-method census, 47 handler xrefs, exact vptr anchors, result and report; removed the temporary producer
blockers: []
next_action: perform full final PR diff/changed-path audit against current main, reconcile only real base drift if necessary, then require exact-head CI/governance and review hygiene before promotion/merge.
```
