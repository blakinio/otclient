---
task_id: OTC-20260819-track-a-world-minimap-static-g0
status: blocked
agent: null
session_id: null
session_role: researcher
project_lane: otclient
lane: P0-STATE
task_kind: discovery
phase: independent-audit-gate
branch: research/OTC-20260819-track-a-world-minimap-static-g0
base_branch: main
base_main: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
created: 2026-08-19T00:33:00+02:00
updated: 2026-08-19T00:52:08+02:00
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
  - 545
---

# Track A world/minimap static G0

## Objective

Execute the owner alias `TIBIA-RE-WORLD-MINIMAP` as a bounded static Track A package, prioritizing the previously uncovered minimap rows while preserving the already-promoted worldmap dependency evidence.

Primary mission coverage is `F01-F15`; this task is the dedicated G0 producer for `F11`/`F12` and strengthens `F13` only where direct current-package static evidence supports it. It does not claim that blocked physical worldmap rows `F08`/`F10` are solved.

## Authority and isolation

```yaml
runtime_access: none
mutation_authorized: false
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
```

No Synology/KasmVNC runtime was observed or controlled. No credentials were consumed. The official client was never executed, logged into or mutated. PR #475, #528, #536 and #543 branches were not modified.

## Producer result

GitHub-hosted producer:

```text
run/job: 32194443653 / 95895463554
producer_head: 715b4c63271e16ff97ff3bd18498f74a652bae7c
result: SUCCESS
artifact: 9345368809
artifact_digest: sha256:c3c32ad9ce527e5ff7d469ae41914f3802fb55d465a993c8dbb32be2840e9755
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked_size: 52109920
current_package_fence: PASS
raw_client_retained: false
```

Current exact-build evidence recovered:

- `TMinimapController` — 24 QMeta methods including layer, visible-area, position, zoom/scroll/click/marker surfaces;
- `TMinimapVisibleArea`, tile storage/manager and render-info storage;
- marker edit dialog, game-action handler, controller/storage/overlay/render-info, protobuf/disk persistence names;
- current world-map camera/viewport conversion and layer-translation helper surfaces.

Coverage delta against PR #536:

```text
F11 NOT_STARTED -> PARTIAL
F12 NOT_STARTED -> PARTIAL
F13 PARTIAL -> PARTIAL (strengthened current exact-build evidence)
F08 BLOCKED unchanged
F10 BLOCKED unchanged
```

Retained report/evidence:

- `docs/agents/reports/OTCLIENT-20260819-track-a-world-minimap-static-g0.md`
- `docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g0/20260819-current-package-minimap-qmeta.md`

The temporary producer workflow was removed after the compact text evidence was persisted.

## Acceptance inventory

- [x] Fresh current public Linux package fetched only in a GitHub-hosted ephemeral job through the existing WARP pattern and exact packed/unpacked hashes recorded.
- [x] #528 candidate package fence revalidated before current-build facts were promoted.
- [x] All QMeta methods enumerated for discovered minimap-specific controller/storage/render-info metaobjects.
- [x] Current-package world-map camera/viewport conversion helpers relevant to `F13` enumerated.
- [x] Direct static method targets retained only where the Qt static-metacall jump table was unambiguous; unresolved targets remain without invented addresses.
- [x] Only compact text evidence persisted; packed/unpacked client deleted before artifact upload; temporary workflow retired before terminal review.
- [x] `F11`, `F12`, and strengthened `F13` classified with FACT/INFERENCE/UNKNOWN boundaries.
- [x] `F08`/`F10` preserved as blocked; no mutation authority inherited from #475.
- [x] Minimap UI/controller state, worldmap Storage state, render/picker/camera projection state, server-delivered extent and World Observation/OTBM reconstruction kept distinct.
- [x] Exact next static discriminators recorded for remaining minimap/transform UNKNOWNs.
- [ ] Proportional exact-head repository checks — execute on the checkpoint commit produced by this task update; record terminal run IDs in PR #545 without further branch mutation.
- [ ] Fresh independent documentation/research audit — required and unavailable in this session; author self-review does not count.

## Delivery classification

```yaml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
implementation_status: research_complete_pending_independent_audit
complete_user_facing_feature: false
physical_e2e: NOT_APPLICABLE_WITH_REASON
physical_e2e_reason: static reverse-engineering evidence package with runtime_access none
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: null
  session_started_at: 2026-08-19T00:33:00+02:00
  checkpointed_at: 2026-08-19T00:52:08+02:00
  last_progress_at: 2026-08-19T00:52:08+02:00
  phase: independent-audit-gate
  exact_head: checkpoint-commit-created-by-this-update
  pull_request: 545
  active_operation: exact-head-ci-observation
  external_run_ids:
    - 32194443653
  operation_started_at: 2026-08-19T00:52:08+02:00
  wait_deadline_at: null
  check_generation: 2
  checks_used: 0
  status: blocked
  safe_to_resume: true
  resume_condition: fresh independent documentation/research auditor is available for exact PR #545 head
  next_action: Verify exact-head governance/CI once, then obtain a fresh independent documentation/research audit. If zero material findings, revalidate main freshness, mark Ready, merge under repository policy, and archive the task.
```

## Blocker

```text
BLOCKER=REQUIRED_FRESH_INDEPENDENT_RESEARCH_DOCUMENTATION_AUDIT_UNAVAILABLE_IN_CURRENT_SESSION
```

This is the only intended terminal blocker after exact-head repository checks. It is not satisfied by author self-review or by an advisory standing pre-review.

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T00:33:00+02:00
last_progress_at: 2026-08-19T00:52:08+02:00
ci_checks_for_current_head: 0
ci_check_generation: 2
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
```
