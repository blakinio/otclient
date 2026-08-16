---
task_id: OTC-20260816-track-a-dri-repair-isolated-client-revalidation
status: implementing
agent: ChatGPT
session_id: chatgpt-dri-repair-isolated-client-revalidation-20260816-2219
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: runtime-admitted-before-dispatch
branch: diag/OTC-20260816-track-a-dri-repair-isolated-client-revalidation
base_branch: main
base_main: fa5b66b697d42c60515c5de48ea5e30135eadd0e
current_main: fa5b66b697d42c60515c5de48ea5e30135eadd0e
created: 2026-08-16T22:19:00+02:00
updated: 2026-08-16T22:19:00+02:00
risk: high
researcher_delivery: draft_only
implementation_authorized: true
owned_paths:
  - .github/workflows/tibia-official-client-re-dri-repair-isolated-client-revalidation.yml
  - docs/agents/tasks/active/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - docs/agents/evidence/OTC-20260816-track-a-dri-repair-isolated-client-revalidation/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-xcbgl-runtime-trace.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xvfb-dri-path-default-glx.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - immutable isolated startup harness blob 1616edcc982be50ef2c95b8077160ec8fe9291fe
  - accepted XCB/GL transformer surface from semantic run 31964397523/job 95207211173
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: trusted-main DRI repair is merged and archived; one bounded non-canonical physical discriminator is required to test whether the exact official client can produce a visible task-owned window when the already-proven contained DRI path is supplied only to task-owned Xvfb
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-dri-repair-isolated-client-revalidation
runtime_namespace: track-a-dri-repair-client-revalidation-v1
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
canonical_boundary:
  read_or_write_canonical_lease: false
  read_or_write_canonical_registration: false
  publish_registration: false
  canonical_namespace_access: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
  second_logged_in_global_session_allowed: false
exact_client_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
experiment:
  immutable_source_commit: cb557da12ebb41c597340909b2db717ee59cdfe1
  immutable_source_blob: 1616edcc982be50ef2c95b8077160ec8fe9291fe
  accepted_prior_trace_run: 31964397523
  accepted_prior_trace_job: 95207211173
  changed_runtime_dimension: task-owned Xvfb receives contained LIBGL_DRIVERS_PATH
  contained_dri_path: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
  explicit_glx_flag: false
  client_receives_libgl_drivers_path: false
  client_graphics_env:
    QT_QUICK_BACKEND: software
    QSG_INFO: '1'
    QT_DEBUG_PLUGINS: '1'
  client_backend_forcing: false
  snapshots_seconds: [5, 15, 35]
  max_semantic_physical_runs: 1
acceptance:
  - task-owned ephemeral namespace and dynamically free display/ports are proven before mutation
  - exact source/client/support fences pass
  - contained DRI directory and swrast provider resolve inside trusted toolroot before Xvfb start
  - task-owned Xvfb preserves accepted argument list and receives only LIBGL_DRIVERS_PATH as the new graphics/provider input
  - same-display GLX/RENDER state is captured read-only
  - exact official client starts without credentials/login/gameplay and without client backend forcing
  - client liveness and task-owned visible windows are captured at 5/15/35 seconds
  - complete client log is scanned locally and only sanitized allowlisted XCB/GLX/EGL/QRhi/Vulkan/load lines are emitted
  - task-owned processes and namespace are fully cleaned
  - no canonical state is read or written
  - exactly one semantic physical run is allowed; any valid discriminator stops execution without retry
audit:
  result: PENDING_PHYSICAL_DISCRIMINATOR
  material_findings_open: 0
last_completed_step: current-main DRI repair was promoted and archived; anti-duplication found no open equivalent physical revalidation task; admission is persisted before the one-shot workflow is added
next_action: add one immutable-source-derived one-shot ephemeral_isolated workflow, obtain Track A governance admission, execute exactly one semantic physical run, then remove the workflow and persist sanitized terminal evidence
---

# Track A isolated DRI-repair client revalidation

This task is intentionally non-canonical. It may mutate only its task-owned ephemeral namespace. It does not acquire the canonical lease, publish registration, use credentials, log in, perform gameplay, or authorize a canonical bootstrap retry.