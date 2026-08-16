---
task_id: OTC-20260816-track-a-xres-window-identity
status: implementing
agent: ChatGPT
session_id: chatgpt-xres-window-identity-20260816
session_role: runtime_identity_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: hosted-preflight-before-xres-identity-current-main
branch: diag/OTC-20260816-track-a-xres-window-identity
base_branch: main
base_main: c4fd10384d988d3eedeb64535239dc24c184e299
risk: high
updated: 2026-08-16T23:17:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xres-window-identity.md
  - docs/agents/evidence/OTC-20260816-track-a-xres-window-identity/**
  - .github/scripts/tibia-official-client-re-xres-window-identity-patch.py
  - .github/workflows/tibia-official-client-re-xres-window-identity.yml
modules_touched: []
reuses:
  - PR #438 post-RHI raw-X11 evidence as unpromoted research input only
  - semantic source head 8e9cc81011383922cf6bad75ca7207deb749fffb
  - immutable harness blob 1616edcc982be50ef2c95b8077160ec8fe9291fe
  - immutable post-RHI transformer blobs d663a40c446983c7359265bf834113ba49e6a5d1 and b9d15f8d1131339b06bfa9cb1e81940c2163a283
  - X-Resource protocol v1.2 / XCB RES QueryClientIds primary specification
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: PR #438 directly proved a raw VIEWABLE 1920x1080 XID exists from t15 while available WM PID/name/class queries cannot bind it to the exact client PID. X-Resource v1.2 QueryClientIds is specifically designed to identify the local-client PID from any resource XID. One separately admitted isolated launch can therefore resolve the exact ownership question without changing graphics behavior, credentials, login or canonical state. Main advanced after branch creation only through unrelated documentation PR #439 defining the World Observation/Atlas boundary; the PR base is now c4fd10384d988d3eedeb64535239dc24c184e299 and this task/workflow are re-fenced to that exact trusted main before any physical enablement.
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-xres-window-identity
runtime_namespace: track-a-xres-window-identity-v1
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
source_evidence:
  pr: 438
  run: 31972261899
  job: 95226396914
  source_final_head: 171fbfa679c8c75dc9722fe39c19141962282f01
  source_final_governance: 31972667061_SUCCESS
  source_final_ci: 31972667199_SUCCESS
  source_final_required_ci: 95227425189_SUCCESS
  classification: PROVEN_RAW_X11_TREE_HAS_VIEWABLE_1920X1080_NAMELESS_PIDLESS_WINDOW_FROM_T15_WHILE_XDOTOOL_NAMED_VISIBLE_SEARCH_RETURNS_ZERO_AND_EXACT_CLIENT_REMAINS_ALIVE_POST_GLX
main_reconciliation:
  original_branch_parent: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
  current_pr_base: c4fd10384d988d3eedeb64535239dc24c184e299
  intervening_pr: 439
  overlap_with_owned_paths: false
  physical_execution_during_reconciliation: false
primary_protocol_basis:
  extension: X-Resource
  required_version: 1.2
  request: QueryClientIds
  selector: observed resource XID
  requested_id_mask: LocalClientPid
  semantics: any resource XID owned by a client may select that client; local PID is returned for local requesters when supported
experiment:
  initial_physical_gate: disabled_by_pr_body_marker
  exactly_one_semantic_run_after_green_preflight: true
  launch_surface: same exact isolated client/DRI-repaired Xvfb surface as PR #438
  new_observation_only:
    - persist raw non-root XID and map_state list per t05/t15/t35
    - query X-Resource version on the same local task-owned X display
    - for each raw XID request LocalClientPid via QueryClientIds
    - compare returned PID with the exact fenced client PID
    - classify viewable XID as exact-client-owned, foreign, or unresolved
  helper_policy:
    - use libxcb and libxcb-res only for local read-only XRes protocol calls
    - select libraries from a bounded fixed allowlist of contained or standard runner library paths
    - resolve to regular files and emit SHA-256 before use
    - refuse before identity query if XRes version is below 1.2 or helper ABI cannot be loaded
forbidden:
  - canonical lease/registration/session access
  - canonical-live-runtime namespace
  - credentials, login or gameplay
  - Track B or historical PR #303 runtime surfaces
  - any change to client graphics/backend environment relative to PR #438
  - +extension GLX
  - QT_XCB_GL_INTEGRATION=none
  - QSG_RHI_BACKEND
  - client-side LIBGL_DRIVERS_PATH
  - global process inventory
  - relaxing canonical worker identity before positive XRes proof
  - second semantic run after a valid XRes classification
acceptance:
  - hosted preflight regenerates immutable PR #438 semantic script and applies only the XRes observer patch
  - generated script passes bash syntax and source-contract checks before physical enablement
  - Track A governance and repository CI pass with physical job skipped
  - one explicit semantic authorization marker enables exactly one physical generation
  - same-generation admission passes immediately before runtime boundary
  - XRes v1.2 availability/version recorded
  - viewable raw XID receives a LocalClientPid result or an explicit unsupported/unresolved result
  - returned PID is compared to exact client PID without inference
  - cleanup complete
  - one-shot workflow/patcher removed after valid result
last_completed_step: main advanced from b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4 to c4fd10384d988d3eedeb64535239dc24c184e299 only through unrelated documentation PR #439; physical gate remained disabled and task authority is now refreshed to the exact current PR base
next_action: run hosted XRes transformer preflight, Track A governance and repository CI against current main c4fd10384d988d3eedeb64535239dc24c184e299; keep physical job gated until all are green and main is re-read stable
---

# Track A XRes window identity discriminator

This task does not assume that the viewable X11 window belongs to Tibia. It exists to obtain direct X-Resource local PID identity before any canonical worker change.
