---
task_id: OTC-20260818-track-a-s1-unfiltered-static-census
status: investigating
agent: ChatGPT
session_id: chatgpt-s1-static-census-20260818
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
execution_mode: github_only
execution_reason: exhaustive deterministic exact-client protocol/QMeta census without touching the serialized physical runtime
branch: research/OTC-20260818-track-a-s1-unfiltered-static-census
base_branch: main
base_main: ed09418b431c28087775b419f85bed404fa85d70
related_pr: 509
created: 2026-08-18T09:29:00+02:00
updated: 2026-08-18T09:43:00+02:00
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
  - .github/workflows/track-a-s1-unfiltered-static-census.yml
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
  - PR #475 runtime branch, task record, workflow surfaces, Synology state, lease, display, login budget and physical session are read-only/non-targeted and will not be touched.
  - PR #498/#499 predecessor auth/session branches are not modified.
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
last_progress_at: 2026-08-18T09:43:00+02:00
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
  -> bounded static xref/dispatch candidate extraction where directly provable
  -> machine-readable S1 registries and ranked S2 follow-up edges
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

A mismatched size/hash/build fails closed.

# Scope

The bounded S1 producer may:

- fetch the exact public Linux client on a disposable GitHub-hosted runner using the already-reviewed exact-hash/WARP producer pattern;
- decompress only in runner scratch space;
- inspect ELF sections, printable strings, RTTI/type names, QMeta-oriented string surfaces and bounded disassembly/xrefs;
- reuse the current-main relocation-aware exact-build resolver for known static anchors;
- write only sanitized text/JSON registries and summaries;
- delete compressed/unpacked proprietary client bytes before artifact upload.

It may not:

- launch the official client;
- access process memory, X11, VNC, Synology, PR #475 runtime state, credentials, account/session values or packet captures;
- upload/commit the raw proprietary executable or secret-bearing material;
- infer live behavior from static names alone.

# Questions

1. Revalidate the complete generated protocol denominator (`349 = 160 client -> server + 189 server -> client`) on the exact client.
2. Persist the complete **189-name server -> client** registry, grouped by stable lexical families without dropping unmatched names.
3. Enumerate exact-binary inbound-oriented handler/QMeta strings without the historical narrow capability regex, including `handle*Message`, `received*Message`, protocol-handler/message-queue types and relevant RTTI types.
4. Where bounded static evidence directly supports it, associate a generated server message family with lexical/QMeta surfaces and concrete code-to-string xref candidates.
5. Keep all unsupported message->handler or handler->storage edges explicitly `UNKNOWN`; do not force a single common inbound dispatcher hypothesis.
6. Produce ranked S2 candidates for later dependency-graph proof, prioritizing session/world entry, player state, creatures, inventory/containers, chat/world events and non-worldmap protocol surfaces.

# Acceptance inventory

- [ ] exact client compressed and unpacked hashes revalidated on hosted runner;
- [ ] generated-message denominator revalidated and complete 160/189 registries persisted;
- [ ] all 189 inbound names preserved in machine-readable evidence;
- [ ] unfiltered inbound-oriented handler/QMeta census persisted with counts and exact string evidence;
- [ ] bounded static code-to-string xref candidates persisted with evidence strength labels;
- [ ] known current-main exact-build vptr anchors revalidated using the repository resolver;
- [ ] no absence claim is made from a filtered subset;
- [ ] no live/runtime/worldmap mutation or #475-owned surface is touched;
- [ ] no raw client bytes are committed or uploaded;
- [ ] temporary producer workflow removed before final merge;
- [ ] result report distinguishes FACT / INFERENCE / UNKNOWN / DISPROVEN;
- [ ] E2E = NOT_APPLICABLE with reason: static exact-file discovery only;
- [ ] fresh audit, exact-head required CI and zero unresolved material review findings before completion.

# Admission

```yaml
track_id: official-client-re
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
mutation_authorized: false
```

# Existing independent denominator control

The sanitized exact-build artifact from #473 remains available and was independently re-opened during this task:

```yaml
run: 32022209943
artifact: 9285763750
artifact_digest: sha256:0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
artifact_expired: false
observed_files:
  - protocol-all.txt
  - protocol-client-to-server.txt
  - protocol-server-to-client.txt
  - summary.json
control_counts:
  protocol_total: 349
  client_to_server: 160
  server_to_client: 189
```

That artifact is a comparison control, not a substitute for the fresh S1 producer.

# Repair history

## Repair 1 — checkout/scratch path fence

The first producer implementation changed the shell working directory to runner scratch before invoking the repository resolver through a relative `tools/...` path. Self-review identified that this would make known-anchor validation depend on the wrong current directory.

Repair:

```text
profile/resolver relative path
 -> explicit $GITHUB_WORKSPACE absolute paths
 -> assert both files exist before invoking resolver
```

The same repair also uses `c++filt -t` for RTTI type encodings and enables Capstone skipdata for the bounded executable-section xref scan. No runtime or evidence claim was promoted from the pre-repair run.

# Checkpoint

```yaml
checkpoint_version: 2
status: investigating
phase: investigate
base_main: ed09418b431c28087775b419f85bed404fa85d70
pr: 509
producer_workflow: .github/workflows/track-a-s1-unfiltered-static-census.yml
pre_repair_head: 86bb32ffc0c06940cd76169a9f7123de1ff3c275
repaired_producer_head: d4666383ae4bae6524d2b47a70ed0a9e0efc4c51
first_producer_run: 32112477071
last_completed_step: implemented the bounded hosted producer, independently re-opened the #473 sanitized denominator artifact, and repaired a checkout/scratch resolver-path defect before accepting any result
proven:
  - PR #475 owns the current physical runtime/worldmap login lane and is outside this task's mutation/observation scope.
  - The archived capability experiment task explicitly names exhaustive unfiltered S1 protocol/QMeta/runtime census as the next programme action.
  - Current routing sends deterministic static Track A work to GitHub-hosted runners with runtime_access none.
  - The independent #473 sanitized artifact still contains 349 generated names split 160 client-to-server / 189 server-to-client.
  - The current-main resolver/profile provide exact-build static anchors including TPlayerProtocolMessageHandler, TPlayerData, TCreatureStorage and TContainerStorage.
unknown:
  - fresh repaired-producer result and artifact identity
  - complete unfiltered inbound handler/method denominator on the exact client
  - number and strength of direct code-to-string xrefs recoverable in one bounded producer
  - whether inbound handling is one dispatcher or several independent handler families
rejected_hypotheses:
  - reuse PR #475 physical runtime for this census: rejected because static hosted evidence is sufficient and runtime is separately owned.
  - treat the old 98 capability-filtered protocol list as exhaustive: rejected by the accepted 349-name denominator.
  - invoke the repository resolver relative to scratch cwd: rejected by self-review; checkout location is now explicit.
blockers: []
next_action: inspect the next exact-head S1 workflow result/artifact; if it is green, persist sanitized evidence and remove the temporary producer, otherwise repair only the first concrete failure within the bounded repair budget.
```
