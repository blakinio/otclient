---
task_id: OTC-20260901-vision-p2-trusted-composition-repair
status: ready
agent: OTC-VISION-P2-COORDINATOR
session_role: coordinator_assigned_integration_repair
worker_alias: OTC-VISION-P2-TRUSTED-COMPOSITION-REPAIR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: integration_repair
phase: final_validation
branch: feat/OTC-20260901-vision-p2-trusted-composition-repair
base_branch: main
base_main: c63412d9b34d2859912709a3ed6e35b82c989437
created: 2026-09-01T23:28:41+02:00
updated_at: 2026-09-02T08:31:16+02:00
risk: high
execution_class: github_hosted
execution_mode: github_mcp_owner_override
execution_reason: owner explicitly authorized completion without Codex; implementation, validation and repository writes are performed through GitHub MCP and deterministic GitHub Actions
preferred_execution: github_mcp
run_scope: bounded_coordinator_repair
continuation_policy: continue_until_real_stop
task_completion_policy: exact_head_validation_review_hygiene_then_squash_merge
prompting_standard_version: 2.1
policy_version: 2
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
worktree: unavailable_remote_host_offline_github_mcp_fallback
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-trusted-composition-repair.md
  - docs/agents/reports/OTC-20260901-vision-p2-trusted-composition-repair.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/persistent_store.py
  - tools/tibia_re_control_center/vision_p2_trusted_composition.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_session.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_replay_atomicity.py
depends_on:
  - PR #838 merged runtime-admission producer
  - PR #839 merged runtime-signals producer
  - PR #827 frozen capture-edge source semantics
  - PR #830 frozen control-bridge source semantics
  - PR #829 frozen edge-transport source semantics consumed and independently revalidated in this integration PR
related_prs:
  - PR #827 capture-edge source closed unmerged
  - PR #829 edge-transport source closed unmerged
  - PR #830 control-bridge source closed unmerged
  - PR #846 trusted-composition integration and promotion vehicle
current_blocker: NONE
next_action: run final exact-head CI and governance after closeout metadata, review full diff and changed-file list, resolve review hygiene, mark PR ready, and squash-merge
invocation_started_at: 2026-09-02T06:20:00+02:00
last_progress_at: 2026-09-02T08:31:16+02:00
ci_checks_for_current_head: 0
ci_check_generation: final_closeout_metadata_pending
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
---

# OTC Vision P2 trusted composition repair

## Mission

Integrate the accepted Phase 2 capture-edge, control-bridge and edge-transport semantics behind one application-owned trusted composition root while preserving `runtime_access:none` and zero physical authority.

## Completed integration

- `VisionP2TrustedComposition` is application-composition data only; task/API/MCP/transport payloads cannot choose reviewed runtime contracts, capture policy or evidence root.
- capture artifacts are content-addressed, confined to the existing Control Center data root, and secret-mask safety is recomputed from PNG bytes plus the pinned reviewed mask policy rather than trusting a caller Boolean;
- raw edge observations cannot self-assert `capture.secret_safe=true`; trusted capture enters the session only after validation and current runtime-admission identity matching;
- capture/runtime provenance is fenced by namespace/container/display/PID/start ticks/XID/client version/size/SHA and task/run identity;
- accepted edge transport is authority-neutral and carries no caller-mintable authentication or mutation claims;
- replay ledger state is persisted in the existing SQLite `meta` table and survives verifier/store reconstruction;
- replay `load -> verify -> persist` now executes inside one existing `BEGIN IMMEDIATE` transaction domain, preventing concurrent verifier reconstruction from reopening the same replay window;
- production default remains fail-closed when reviewed capture/runtime configuration is absent.

## RED -> GREEN evidence

The coordinator added `test_vision_p2_trusted_replay_atomicity.py`. On head `a09c054301770fab2588722970d3c183b6626dce` the new test failed exactly as intended with observed depths `load=0`, `save=0`. The minimal repair on `062a5c173b3410ec8fc2e5efaaefa1c4e34d15d6` wraps replay load/verification/persistence in the existing SQLite transaction domain.

Exact code-generation validation for `062a5c173b3410ec8fc2e5efaaefa1c4e34d15d6`:

- Track A agent runtime governance run `33598991421`: SUCCESS;
- Package A run `33598991422`: SUCCESS;
- Package B run `33598991441`: SUCCESS, including full regression, Ruff/whitespace, fresh falsification and browser/CLI E2E;
- CI run `33598991677`: SUCCESS.

The Package B full regression includes the new atomicity test and all prior Control Center tests. No Official Tibia, Synology or Kasm live observation was used to satisfy repository/static gates.

## Safety invariants

```yaml
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
```

## Final completion gate

This task is `ready` for its final closeout generation. After MODULE_CATALOG/CHANGELOG/report/PR metadata are current, run exact-head Package A, Package B, Track A and CI, review the complete changed-file list/diff, verify zero unresolved review threads/requested changes, mark #846 ready and squash-merge without bypassing protection or weakening any test.
