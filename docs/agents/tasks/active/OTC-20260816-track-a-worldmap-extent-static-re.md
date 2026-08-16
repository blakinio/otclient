---
task_id: OTC-20260816-track-a-worldmap-extent-static-re
status: investigating
agent: ChatGPT
session_id: chatgpt-viewport-static-20260816-1426
session_role: static_re_researcher
project_lane: otclient
lane: STATIC-RE
track_id: official-client-re
task_kind: discovery
phase: investigate
implementation_authorized: false
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
base_branch: main
base_main: ddf7dd9408116fbeaca05bfeb69663f30f7cd34f
pr: 367
risk: medium
updated: 2026-08-16T14:33:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-extent-static-re.md
  - .github/scripts/tibia-official-client-re-worldmap-extent-static.py
  - .github/workflows/tibia-official-client-re-worldmap-extent-static.yml
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/**
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md
  - docs/agents/evidence/OTC-20260816-official-client-map-viewport-feasibility/20260816-evidence.md
  - PR #365 merged feasibility checkpoint
  - PR #366 merged feasibility-task archive/ownership release
  - PR #310 GitHub-hosted exact-client staging failure evidence
  - run 31892019505 artifact 9248797952 static exact-binary evidence
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: exact-client ELF/RTTI/xref/disassembly work is deterministic/disposable and Track A hybrid routing requires GitHub-hosted execution rather than Synology
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: rising
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive patch/dependency graph spans extent ownership, storage/protocol consumers and render/camera/picker consumers; rotate the same task before any split
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
invocation_started_at: 2026-08-16T14:20:00+02:00
last_progress_at: 2026-08-16T14:33:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: hosted-static-dispatch-1
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
heavy_validation_runs: 0
hosted_staging_attempts_this_task: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
static_classification: MORE_STATIC_RE_NEEDED
new_gui_session_created: false
runtime_used: false
next_action: run exactly one materially different GitHub-hosted exact-fence materialization attempt and, only if the fence passes, extract the bounded worldmap type/xref/call/field graph; otherwise persist INPUT_BLOCKED without Synology fallback
---

# Track A worldmap extent static RE

## Objective

Recover a durable static patch/dependency graph for the exact official native-Linux client covering:

- `TWorldMapExtent`;
- `TWorldMapSubfieldExtent`;
- `TWorldMapViewport`;
- `TWorldMapStorage`;
- `TWorldmapProtocolMessageHandler`;
- `TWorldMapRenderProvider`;
- `TWorldMapCamera`;
- `TWorldMapPicker`.

No client bytes are modified in this task. No live official-client runtime is observed or mutated.

## Trusted starting point and ownership

PR #365 merged the accepted PR #325 feasibility report/evidence onto `main`; PR #366 then archived that completed feasibility task and released its ownership. The retained report/evidence remain on `main` and are read-only dependencies for this continuation.

The prior evidence proves exact-client semantic/type-name surfaces and preserves historical `18 x 14` only as `DERIVED_FROM_OBSERVED_JOB_LOG`. It does not prove object layouts, dimension fields, allocations, parser limits, maximum dimensions or patch points.

PR #363 owns only the continuation prompt/task paths and remains read-only to this task. PR #310 owns its P2 script/workflow/task and remains read-only. This task owns only the new paths declared above.

## Execution boundary

```yaml
static_execution: github_hosted_first
runtime_access: none
synology_static_fallback: forbidden
gui_runtime_initial_phase: forbidden
new_x11_display: forbidden
new_vnc_or_novnc_desktop: forbidden
new_logged_in_tibia_session: forbidden
client_byte_mutation: forbidden
owner_codex_openai_api_paid_ai: forbidden
```

If static evidence later proves a runtime discriminator is necessary, this task records the smallest discriminator and stops/rotates. It does not silently reclassify into live observation.

## Static acceptance inventory

- [ ] revalidate exact client size/SHA and source provenance for every new exact-binary claim;
- [ ] recover or explicitly bound typeinfo/vtable/xref/constructor/destructor evidence for extent/subfield/viewport;
- [ ] identify or explicitly bound candidate dimension/edge fields and default/material writers;
- [ ] enumerate material readers through storage/protocol;
- [ ] enumerate material readers through render provider/camera/picker;
- [ ] correlate literal/derived dimension constants with call/data flow, never blind numeric search alone;
- [ ] audit fixed arrays, allocation/capacity, loops/masks, row/column/floor parser assumptions, clipping/culling, coordinate packing, cache and picking limits;
- [ ] persist a patch/dependency graph with exact locations, evidence, writers/readers, allocation/protocol/render dependencies, isolated-change consequence and confidence;
- [ ] classify exactly one of `STATIC_PATCH_GRAPH_READY`, `MORE_STATIC_RE_NEEDED`, `RUNTIME_DISCRIMINATOR_REQUIRED`, `BLOCKED`;
- [ ] no client byte mutation or live runtime action occurred;
- [ ] focused validation, fresh static/docs audit, exact-head required CI and lifecycle gates pass before completion.

## Input staging evidence and bounded experiment

PR #310 already exhausted two hosted source attempts: `download.tibia.com` failed DNS resolution and a plain automated request to `static.tibia.com` returned HTTP 403. Those requests are not repeated blindly.

PR #97's public GitHub-release source was also inspected as a potential compliant source, but the published original-Linux inventory inspected for this task does not expose the required `15.32.df7b29` build and is therefore not accepted as an exact-client source.

The single new hosted staging experiment uses the same official static archive URL but a materially different request behavior: compressed transfer plus a same-URL `Referer`, matching a historical package-manager workaround for automated downloads from this endpoint. Exact size/SHA fencing remains decisive. A download that succeeds but does not match the exact fence is still `INPUT_BLOCKED`.

The workflow never executes the client. The archive/client remain only in `$RUNNER_TEMP`, are removed in an `always()` cleanup step, and are excluded from uploaded artifacts. Only sanitized structural JSON/text evidence may be uploaded.
