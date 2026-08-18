---
task_id: OTC-20260819-track-a-world-minimap-static-g0
status: implementing
agent: ChatGPT
session_id: chatgpt-world-minimap-static-g0-20260819
session_role: researcher
project_lane: otclient
lane: P0-STATE
task_kind: discovery
phase: current-package-static-minimap-census
branch: research/OTC-20260819-track-a-world-minimap-static-g0
base_branch: main
base_main: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
created: 2026-08-19T00:33:00+02:00
updated: 2026-08-19T00:33:00+02:00
risk: low
execution_mode: github_only
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
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
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
implementation_authorized: true
e2e_required: false
decomposition_decision: single
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-world-minimap-static-g0.md
  - docs/agents/reports/OTCLIENT-20260819-track-a-world-minimap-static-g0.md
  - docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g0/**
  - .github/workflows/track-a-world-minimap-static-g0.yml
reuses:
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
  - docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
related_prs:
  - 367
  - 439
  - 462
  - 473
  - 475
  - 528
  - 536
  - 543
---

# Track A world/minimap static G0

## Objective

Execute the owner alias `TIBIA-RE-WORLD-MINIMAP` as a bounded static Track A package, prioritizing the previously uncovered minimap rows while preserving the already-promoted worldmap dependency evidence.

Primary mission coverage is `F01-F15`; this task is the dedicated G0 producer for `F11`/`F12` and may strengthen `F13` only where direct current-package static evidence supports it. It does not claim that blocked physical worldmap rows `F08`/`F10` are solved.

## Authority and isolation

This task is GitHub-hosted/static only.

```yaml
runtime_access: none
mutation_authorized: false
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
```

It must not:

- observe, bootstrap, log in to, control or mutate the shared Synology/KasmVNC client;
- consume credential/Secrets state;
- run the historical `[19,14]` client mutation;
- modify branches owned by PR #475, #528, #536 or #543;
- upload or commit the official Tibia executable or proprietary asset payloads;
- treat historical offsets as current-build facts without a fresh exact package fence.

PR #475 is read-only dependency evidence for the still-unresolved server-delivery causal rows. PR #528's published current-package hash is only a candidate fence and must fail closed if the public package changed.

## Verified starting evidence

Historical exact build `15.32.df7b29` / SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` established:

- `TMinimapController` and `TMinimapRenderInfoStorage` static presence;
- QML world-map camera/viewport coordinate-transform helpers;
- worldmap Handler -> Storage dependency graph, Storage bounds/eviction, Viewport geometry, RenderProvider clipping/indexing, Picker transforms and bounded Camera ownership through merged #367;
- server-delivery control/capability remains `UNKNOWN` through merged #473;
- one `[19,14]` startup canary is safe only for the bounded no-login lifecycle and does not prove semantic propagation through merged #462.

A newer read-only package probe in PR #528 reported candidate unpacked SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8` and size `52109920`. This task must verify that fence before promoting any new current-package fact.

## Acceptance inventory

- [ ] Fresh current public Linux package is fetched only in a GitHub-hosted ephemeral job through the existing WARP pattern and exact packed/unpacked hashes are recorded.
- [ ] If the #528 candidate package fence still matches, enumerate all QMeta methods for every minimap-specific controller/storage/render-info metaobject rather than relying on the old capability regex subset.
- [ ] Enumerate current-package world-map camera/viewport conversion helpers relevant to `F13`.
- [ ] Recover direct static method targets when the Qt static-metacall jump table is unambiguous; otherwise retain `UNKNOWN`.
- [ ] Persist only compact text evidence; delete the executable/package before artifact upload and remove the temporary workflow before terminal review.
- [ ] Classify `F11`, `F12` and any strengthened `F13` row as `DONE|PARTIAL|NOT_STARTED|BLOCKED` with FACT/INFERENCE/UNKNOWN separation.
- [ ] Preserve `F08`/`F10` as blocked unless independent causal physical evidence exists; do not inherit mutation authority from #475.
- [ ] Connect minimap semantics to the promoted worldmap/storage/render/picker/camera graph without conflating minimap UI state, live worldmap Storage extent and server-delivered extent.
- [ ] Record an exact next discriminator for every remaining UNKNOWN.
- [ ] Run proportional exact-head repository checks.
- [ ] Obtain a fresh independent documentation/research audit before `completed`; author self-review is not sufficient.

## Delivery classification

```yaml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
implementation_status: research_in_progress
complete_user_facing_feature: false
physical_e2e: NOT_APPLICABLE_WITH_REASON
physical_e2e_reason: static reverse-engineering evidence package with runtime_access none
```

## Non-overlap

- #367/#439/#462/#473 are merged evidence inputs only.
- #475 retains its physical worldmap causal scope and branch.
- #528 retains current package/native-login runtime scope.
- #536 owns the broad 169-row coverage matrix; this task will not edit that branch.
- #543 owns the unmerged alias/prompt package; this task consumes its mission wording as scope data only and does not rely on it to expand authority.

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: chatgpt-world-minimap-static-g0-20260819
  session_started_at: 2026-08-19T00:33:00+02:00
  checkpointed_at: 2026-08-19T00:33:00+02:00
  last_progress_at: 2026-08-19T00:33:00+02:00
  phase: current-package-static-minimap-census
  exact_head: pending-first-task-commit
  pull_request: none
  active_operation: none
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: null
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: branch and task remain exclusively owned with no overlapping minimap PR
  next_action: Add the branch-only hosted static minimap census workflow, then verify the candidate current-package fence and collect the minimap/QMeta text evidence.
```

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T00:33:00+02:00
last_progress_at: 2026-08-19T00:33:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
```
