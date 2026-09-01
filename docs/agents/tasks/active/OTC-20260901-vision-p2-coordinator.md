---
task_id: OTC-20260901-vision-p2-coordinator
status: implementing
agent: ChatGPT
session_role: programme_coordinator
worker_alias: OTC-VISION-P2-COORDINATOR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: coordination
phase: wave_1_mcp_direct_repair_and_integration
branch: docs/OTC-20260901-vision-p2-coordinator-mcp-override
base_branch: main
base_main: 03f0671232d1e6e6557d6c1fbb5547660a814415
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T23:45:00+02:00
risk: high
execution_mode: chat_mcp_github
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
prompting_standard_version: 2.1
policy_version: 2
runtime_access: none
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
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
worktree: C:/Users/barte/otclient-vision-p2-coordinator
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #825 merged Wave 1 dispatch checkpoint
  - PR #833 merged Package A path-boundary repair
blocks:
  - Wave 2 reconciliation
related_prs:
  - PR #826 runtime-admission worker Draft
  - PR #827 capture-edge worker Draft
  - PR #828 runtime-signals worker Draft
  - PR #829 edge-transport worker Draft
  - PR #830 control-bridge worker Draft
  - PR #833 merged shared CI repair
  - PR #836 coordinator post-repair checkpoint
  - PR #843 coordinator benchmark reconciliation checkpoint
  - PR #846 trusted-composition integration Draft
  - PR #847 coordinator Spark real-stop checkpoint
current_blocker: EDGE_TRANSPORT_AUTH_PROOF_RFR_AND_TRUSTED_COMPOSITION_IMPLEMENTATION
next_action: execute #829 proof-boundary repair directly through owner-authorized MCP, independently re-review it, then implement #846 trusted composition through MCP and run exact-head gates before Wave 2
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T23:45:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-mcp-override
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# OTC Vision Phase 2 read-only programme coordinator

## Objective

Coordinate independently reviewed Wave 1 slices through current-main validation, then serialize any required read-only runtime observation and continue to Wave 2 reconciliation and final independent E2E/audit without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- live Git/GitHub/runtime state and stricter trusted-base governance override stale historical prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T23:45:00+02:00
head: 03f0671232d1e6e6557d6c1fbb5547660a814415
head_semantics: trusted_main_before_owner_authorized_mcp_execution
branch: docs/OTC-20260901-vision-p2-coordinator-mcp-override
pr: pending
status: implementing
context_routes:
  - phase-2-read-only-coordination
  - worker-classification
  - trusted-composition-integration
  - edge-transport-security-repair
  - owner-authorized-mcp-execution
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - trusted main is 03f0671232d1e6e6557d6c1fbb5547660a814415; it includes merged runtime-admission #838, runtime-signals #839, benchmark #841/#842 and coordinator Codex-dispatch prompt updates #844/#845.
  - PR #827 exact source head 6991b98f3f970c6ffc9d1bec9bf032aed89f0f2d is coordinator ACCEPT_WITH_EDITS for a safe fail-closed capture boundary; source PR is closed without merge and frozen for integration in #846.
  - PR #830 exact source head 971787f380d52d0e141c50b9201498b0c99e752d is coordinator ACCEPT_WITH_EDITS with Package A/B, Track A and CI Required green; source PR is closed without merge and frozen for integration in #846.
  - production ControlDomainService still constructs AgentSessionCoordinator without ReviewedRuntimeAuthorityConfiguration, so #830 remains safely disabled until trusted composition is wired.
  - PR #829 exact current head 6031cf5862f7dd019aafa9314aaee408c67b20fe is CLEAN and all hosted gates are green, with exact schema/type/replay-epoch repairs retained.
  - PR #829 nevertheless remains RETURN_FOR_REPAIR: direct use of reachable module globals _VERIFIED_FRAME_PROOF and _OUTBOUND_CHANNEL_PROOF still creates peer_authenticated objects without cryptographic verifier/handshake issuance.
  - EdgeReplayLedger has no production persistence/reuse callsite; a fresh ledger is constructed by EdgeOutboundClient.connect, so durable restart replay state is assigned to integration PR #846 after #829 reaches ACCEPT.
  - PR #846 exact scaffold head 04050655d9eb0d18bf55dc2d1324b0a1bc613eeb is Draft/CLEAN with CI Required and Track A governance SUCCESS; it is the single integration owner for capture policy/root, runtime authority composition and later replay persistence.
  - on 2026-09-01 the owner explicitly authorized the coordinator to finish #829 and #846 directly through MCP/GitHub without invoking Codex; this is the active execution-mode override for these bounded repository repairs.
  - no Official Tibia/Synology/Kasm live observation, credentials, login, GUI input, process control, process memory, payload capture or physical action occurred; runtime_access remains none and physical action count/budget remain 0/0.
derived:
  - source PRs #827 and #830 must not receive further writes while #846 owns their integration paths.
  - green CI cannot override #829's mechanically reproduced authentication-boundary flaw.
  - Wave 2 and all live read-only observation remain blocked until #829 is independently ACCEPTED and #846 implements/reviews the trusted composition root on one exact head.
  - direct MCP execution consumes no separate Codex/model worker and remains bounded by the same owned paths, TDD, CI, independent-review and no-live-runtime gates.
unknown:
  - final repaired #829 exact head and independent coordinator disposition.
  - final #846 integrated exact head and trusted reviewed capture-policy representation.
  - final existing-store replay-ledger persistence schema/keying.
conflicts: []
first_failure:
  marker: EDGE_TRANSPORT_CALLER_MINTABLE_AUTH_PROOF
  evidence: on exact current #829 source, VerifiedEdgeFrame(_proof=module._VERIFIED_FRAME_PROOF) and EdgeOutboundChannel(...,_proof=module._OUTBOUND_CHANNEL_PROOF) both report peer_authenticated=True without verifier/handshake issuance.
rejected_hypotheses:
  - module-private proof objects are a sufficient same-process authentication boundary: rejected by direct exact-head construction using the real exported module globals.
  - full hosted GREEN is sufficient to promote #829: rejected because the adversarial proof bypass is outside existing negative coverage.
  - accepted-with-edits source PRs #827/#830 should be merged standalone: rejected by Phase-2 completeness rules; they are frozen source inputs for #846.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: live git/gh reconciliation of main and PRs #827/#829/#830/#846
    result: PASS
    evidence: main 03f067123; #827/#830 closed unmerged at exact frozen heads; #829 open Draft 6031cf586 with all hosted gates green/CLEAN; #846 open Draft 04050655d with CI Required/Track A green and CLEAN.
  - command: direct current-head #829 authentication-object probe
    result: PASS
    evidence: real module proof globals mint peer_authenticated VerifiedEdgeFrame and EdgeOutboundChannel objects, preserving RETURN_FOR_REPAIR.
  - command: production composition/replay callsite search
    result: PASS
    evidence: ControlDomain lacks ReviewedRuntimeAuthorityConfiguration and transport replay ledger has no production persistence consumer; both are explicitly assigned to #846.
  - command: PR #846 scaffold checkpoint / Track A governance / CI Required
    result: PASS
    evidence: checkpoint PASS, local Track A governance PASS after current-main restack, GitHub Track A and CI Required SUCCESS on 04050655d.
blockers:
  - PR #829 requires removal of caller-mintable authentication proof objects and fresh exact-head re-review.
  - PR #846 requires implementation/integration after accepted #829 is available for replay persistence consumption.
next_action: repair #829 directly through MCP, independently re-review exact head, then implement #846 through MCP and rerun exact-head gates before Wave 2 or any live observation.
```

## Wave 1 live ledger

| Alias / repair | PR | Current exact state | Coordinator disposition |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #838 | merged `fb0c489f2ed166e872c4f197c6a78375a8576685` | repository/static `ACCEPT`; later serialized live evidence still required |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 source | closed unmerged at `6991b98f3f970c6ffc9d1bec9bf032aed89f0f2d` | `ACCEPT_WITH_EDITS`; safe fail-closed source frozen into #846 |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #839 | merged `e883543403d5430d7b1d287f59043b23c98f37d6` | repository/static `ACCEPT` |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 Draft | `6031cf5862f7dd019aafa9314aaee408c67b20fe`, hosted GREEN/CLEAN | `RETURN_FOR_REPAIR`; caller-mintable module proof objects remain |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 source | closed unmerged at `971787f380d52d0e141c50b9201498b0c99e752d` | `ACCEPT_WITH_EDITS`; safe source frozen into #846 |
| trusted composition repair | #846 Draft | scaffold `04050655d9eb0d18bf55dc2d1324b0a1bc613eeb`, CI/Track A GREEN | MCP implementation authorized; waits only for accepted #829 before replay persistence; sole integration owner |

Official runtime observation remains unauthorized at this checkpoint. All Phase 2 mutation/effect authorities remain false and physical action budget/count remain `0/0`.
