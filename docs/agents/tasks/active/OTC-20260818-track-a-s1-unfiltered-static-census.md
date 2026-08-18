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
updated: 2026-08-18T10:03:00+02:00
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
last_progress_at: 2026-08-18T10:03:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-docs
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
  -> exhaustive generated-message census
  -> complete inbound receive-method name surface
  -> protocol-handler type/code xrefs
  -> current exact-build anchor revalidation
  -> ranked non-runtime S2 follow-up
```

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
platform: official_native_linux_only
```

# Acceptance inventory

- [x] exact compressed/unpacked hashes revalidated on GitHub-hosted runner;
- [x] protocol denominator revalidated: 349 total / 160 client->server / 189 server->client;
- [x] complete 160/189 registries persisted;
- [x] fresh registries byte-identical to independent #473 sanitized control;
- [x] complete 189 `received*Message` string surface persisted;
- [x] broad candidate method census split correctly: 149 `handle*` + 189 `received*` + 204 `on*` = 542;
- [x] exact string comparison: 188 receive-method stems match generated server-message stems exactly; one `TrackQuestFlags` / `TrackedQuestFlags` variant;
- [x] no receive-method string is promoted to a concrete dispatch edge;
- [x] 47 distinct `*ProtocolMessageHandler` class strings with direct executable xrefs persisted;
- [x] xref evidence stops at `DIRECT_CODE_TO_STRING_XREF`; dispatcher role remains unproven;
- [x] current-main exact-build vptr anchors revalidated 7/7 unique;
- [x] common upstream inbound dispatcher remains `UNKNOWN`;
- [x] naive substring family buckets independently rejected as semantic evidence;
- [x] no #475/runtime/Synology/X11/process-memory/login/credential/gameplay access;
- [x] no raw proprietary client bytes committed or uploaded;
- [x] temporary producer workflow removed from final branch diff;
- [x] E2E = `NOT_APPLICABLE`: static exact-file discovery only;
- [ ] final current-head diff/path audit after audit corrections;
- [ ] current-main freshness/reconciliation;
- [ ] exact-head required CI/governance;
- [ ] zero unresolved material review findings;
- [ ] coordinator/promotion disposition if required by current Track A governance.

# Fresh producer evidence

```yaml
producer_head: cb575cec2077c8002bb6712ffac4d4dc77420499
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

Independent #473 denominator control:

```yaml
run: 32022209943
artifact: 9285763750
artifact_digest: sha256:0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
protocol_all_sha256: 55f7cf2d6d4a63df6e24b8b156e38f1a2a64a9d6394357aa914661ab48fd983b
client_to_server_sha256: 621ecb7aa1a62aae559e8d793d1aebe9289d84811bc43c4339a7153458b553f0
server_to_client_sha256: e642f661546c2e6e89ddcd77ac5e8aa9cd517408a309f95a3a367af943550d96
fresh_lists_byte_identical: true
```

# Durable evidence

```text
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/summary.json
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/result.md
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/received-message-methods.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/inbound-method-strings.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-handler-code-xrefs.tsv
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/known-anchor-vptr-resolution.json
docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md
```

# Material result

```yaml
FACT:
  generated_protocol_total: 349
  client_to_server: 160
  server_to_client: 189
  broad_candidate_method_strings: 542
  handle_prefixed: 149
  received_message_strings: 189
  on_prefixed: 204
  received_exact_stem_matches: 188
  received_naming_variants: 1
  protocol_message_handler_class_xrefs: 47
  exact_profile_vptr_targets_unique: 7

INFERENCE:
  generated_message_to_received_method_name_alignment: static_lexical_only
  native_protocol_handler_type_surface: domain_partitioned

UNKNOWN:
  generated_message_to_concrete_handler_dispatch
  received_method_to_handler_owner
  handler_to_storage_controller_mutation_edge
  common_upstream_inbound_dispatcher
  runtime_delivery_or_state_mutation
```

# Repair and audit history

## R1 — resolver checkout/scratch path

Initial producer changed cwd to runner scratch but referred to the repository resolver/profile relatively. Self-review repaired this before accepting evidence by using exact `$GITHUB_WORKSPACE` paths and asserting both files exist. RTTI demangling was also corrected to `c++filt -t`. No pre-repair result was promoted.

## A1 — diagnostic family buckets rejected

Substring-only grouping could misclassify names (`Mark` inside `Market`, `row` inside `Browse`). These buckets were excluded from all durable semantic conclusions.

## A2 — broad 542-method set narrowed

Final diff review found the broad `handle/received/on` set was being described too strongly as an inbound-handler denominator. It was corrected to the actual prefix distribution `149/189/204`; the durable inbound receive-surface denominator is the exact 189 `received*Message` strings. The report/result/summary now preserve this distinction.

## A3 — shared-upstream-dispatcher non-claim

Many domain-specific `*ProtocolMessageHandler` types prove a broad partitioned handler type surface, but do not disprove a common upstream router/queue. Wording was corrected so `COMMON_UPSTREAM_INBOUND_DISPATCHER=UNKNOWN` remains explicit.

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

```text
1. TPlayerProtocolMessageHandler
   -> PlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
   -> exact QMeta/dispatch targets
   -> static TPlayerData owner/mutation edge where provable

2. TCreatureProtocolMessageHandler -> TCreatureStorage
3. TContainerProtocolMessageHandler -> TContainerStorage
4. TChatProtocolMessageHandler -> chat storage/controller
```

All are exact-file static work and remain independent of PR #475 physical runtime.

# Checkpoint

```yaml
checkpoint_version: 4
status: validating
phase: exact-head-validation
base_main_at_claim: ed09418b431c28087775b419f85bed404fa85d70
pr: 509
research_result: COMPLETE
producer_workflow_removed: true
last_completed_step: corrected final evidence semantics after A2/A3, including the exact 189 received-method denominator and shared-upstream-dispatcher non-claim
blockers: []
next_action: perform current-head full diff/path audit, refresh current main and promotion authority, reconcile only if required, then require exact-head CI/governance and review hygiene before terminal disposition.
```
