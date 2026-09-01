---
task_id: OTC-20260901-vision-p2-trusted-composition-repair
status: blocked
agent: unclaimed
session_role: coordinator_assigned_integration_repair
worker_alias: OTC-VISION-P2-TRUSTED-COMPOSITION-REPAIR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: integration_repair
phase: prepared_waiting_for_codex
branch: feat/OTC-20260901-vision-p2-trusted-composition-repair
base_branch: main
base_main: 103fa3071ee4d82d7dff934034e2442c32bd3a81
created: 2026-09-01T23:28:41+02:00
updated_at: 2026-09-01T23:32:09+02:00
risk: high
execution_class: github_hosted
execution_mode: isolated_worker_branch
preferred_execution: codex
run_scope: bounded_coordinator_repair
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
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
worktree: C:/Users/barte/otclient-vision-p2-trusted-composition
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-trusted-composition-repair.md
  - docs/agents/reports/OTC-20260901-vision-p2-trusted-composition-repair.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/persistent_store.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_session.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
depends_on:
  - PR #838 merged runtime-admission producer
  - PR #839 merged runtime-signals producer
  - PR #827 source head 6991b98f3f970c6ffc9d1bec9bf032aed89f0f2d coordinator ACCEPT_WITH_EDITS
  - PR #830 source head 971787f380d52d0e141c50b9201498b0c99e752d coordinator ACCEPT_WITH_EDITS
  - PR #829 must reach coordinator ACCEPT before transport replay persistence is enabled
related_prs:
  - PR #827 capture-edge source Draft
  - PR #829 edge-transport source Draft
  - PR #830 control-bridge source Draft
  - PR #843 coordinator reconciliation Draft
  - PR #846 trusted-composition repair Draft
current_blocker: CODEX_SPARK_QUOTA_EXHAUSTED_UNTIL_2026-09-02T04:15+02:00_AND_PR_829_RETURN_FOR_REPAIR
next_action: after Spark quota reset, integrate exact accepted source slices into this isolated branch, keep runtime access none, and implement the trusted composition root without reintroducing caller-mintable authority
invocation_started_at: null
last_progress_at: 2026-09-01T23:28:41+02:00
ci_checks_for_current_head: 0
ci_check_generation: scaffold-only
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
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

Create the one trusted application composition root required by accepted-with-edits capture-edge and Control Bridge slices. Keep all repository work at `runtime_access:none`; this task grants no observation authority.

This is a coordinator-assigned bounded repair task, not a new conceptual programme worker. Source Drafts #827 and #830 become frozen source evidence once this task is bound; their exact accepted-with-edits heads are inputs, not independent implementation lanes.

## Binding reads

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T23:32:09+02:00
head: 123115eb81728a473cff85f7c2614913d31a95ea
head_semantics: pr_binding_commit_before_metadata_repair_checkpoint
branch: feat/OTC-20260901-vision-p2-trusted-composition-repair
pr: 846
status: blocked
context_routes:
  - phase-2-read-only-coordination
  - trusted-composition-repair
  - capture-secret-safety
  - control-bridge-authority
  - edge-replay-persistence
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-trusted-composition-repair.md
  - docs/agents/reports/OTC-20260901-vision-p2-trusted-composition-repair.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/persistent_store.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_session.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
proven:
  - PR 827 head 6991b98f3f970c6ffc9d1bec9bf032aed89f0f2d safely fails closed until a trusted reviewed capture-policy/evidence-root consumer exists.
  - PR 830 head 971787f380d52d0e141c50b9201498b0c99e752d has green hosted gates and safely fails closed because production ControlDomain supplies no reviewed runtime authority configuration.
  - production ControlDomainService constructs AgentSessionCoordinator without ReviewedRuntimeAuthorityConfiguration.
  - EdgeReplayLedger currently has no production persistence/reuse callsite; a fresh ledger is created by EdgeOutboundClient.connect.
  - no Official Tibia/Synology/Kasm live observation or mutation occurred; runtime_access remains none and physical budget/count are 0/0.
derived:
  - capture policy/root, bridge runtime configuration and replay persistence belong to one application composition root rather than caller/task/transport payloads.
  - merging PR 827 or PR 830 standalone would weaken the Phase-2 completeness gate, so both are source inputs only until this integration repair is accepted.
  - PR 829 must be independently accepted before its replay contract is consumed here.
unknown:
  - final reviewed capture mask policy representation and exact trusted configuration source.
  - final persistence schema/keying for replay ledger within the existing store.
  - final accepted PR 829 transport head.
conflicts: []
first_failure:
  marker: TRUSTED_COMPOSITION_CONSUMER_MISSING
  evidence: safe worker slices intentionally fail closed because production composition does not yet pin the reviewed authority/policy/root/replay state.
rejected_hypotheses:
  - Python-private tokens or object identity can establish trusted same-process authority: rejected by mechanical bypasses in capture/transport review.
  - worker green CI alone makes the Phase-2 integration complete: rejected by programme acceptance rules and missing production composition.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-trusted-composition-repair.md
  - docs/agents/reports/OTC-20260901-vision-p2-trusted-composition-repair.md
validation:
  - command: coordinator live source/head/production-callsite reconciliation
    result: PASS
    evidence: exact source heads and missing production configuration/replay callsites recorded above.
blockers:
  - Codex Spark quota is exhausted until 2026-09-02T04:15+02:00.
  - PR 829 remains RETURN_FOR_REPAIR and cannot yet be consumed.
next_action: after Spark quota reset, integrate the exact accepted-with-edits source semantics, keep runtime access none, and implement one fail-closed trusted composition root; consume PR 829 only after coordinator ACCEPT.
```

## Required integration repairs

1. Construct the approved runtime-signal/admission authority configuration only at trusted application composition. Request/task/API/MCP/transport data must not choose or replace reviewed contracts, clock domain, freshness policy, admission source or resolver.
2. Restore capture only through an externally pinned reviewed secret-mask policy. The capture request/evidence must not nominate its own policy, `secret_safe` value or evidence root. Secret safety must be recomputable from canonical artifact metadata plus the expected policy.
3. Derive a canonical evidence root from trusted application configuration/data root, with path and symlink confinement. Do not expose generic caller-selected filesystem writes.
4. Preserve conservative acquisition timing: capture start/end/final currentness and immutable binding snapshots must fail closed before persistence/handoff.
5. Reuse the existing persistent store/control plane for any restart-durable edge replay ledger. Do not create a second store or reset replay state simply because a verifier/process was reconstructed.
6. After PR #829 reaches coordinator ACCEPT, consume its exact transport contract without treating peer authentication as runtime/Track A authority.
7. Production default remains fail-closed if any reviewed configuration, canonical root or persistent replay state is absent/invalid.

## Required negative tests

- task/API/MCP cannot select reviewed runtime contracts or capture policy/root;
- caller-created policy/evidence cannot become secret-safe by type, token, object identity or Boolean;
- stale/foreign admission and runtime signal evidence cannot bind;
- expired task cannot acquire or retain runtime authority;
- evidence-root traversal/symlink escape fails closed;
- restart/reconstruction cannot reopen a retired transport replay epoch;
- missing composition configuration leaves Official-client access `NONE` and capture unavailable.

## Completion gate

Do not promote source PR #827 or #830 independently. This task must integrate the exact accepted source semantics, run focused/component/integration validation on one exact head, and return to the programme coordinator for independent review. Live read-only observation remains a later serialized gate and cannot be used to compensate for repository/static findings.