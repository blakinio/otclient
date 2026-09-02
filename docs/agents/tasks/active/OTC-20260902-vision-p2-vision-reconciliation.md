---
task_id: OTC-20260902-vision-p2-vision-reconciliation
status: implementing
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-VISION-RECONCILIATION
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: wave_2_trusted_reconciliation
branch: feat/OTC-20260902-vision-p2-vision-reconciliation
base_branch: main
base_main: 8441fc1cce1600033b505d68ebc5c0141b337394
created: 2026-09-02T10:46:00+02:00
updated_at: 2026-09-02T10:46:00+02:00
risk: high
execution_class: github_hosted
execution_mode: github_only
execution_reason: preserve owner Codex quota; use GitHub plus existing Actions unless a concrete proving gap requires one explicitly justified worker invocation
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one cohesive producer-consumer integration across the existing trusted composition, deterministic reconciler and session evidence path
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
policy_version: 2
runtime_access: none
persistent_session_role: none
physical_e2e_required: true
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
worktree: NOT_APPLICABLE_GITHUB_ONLY
owned_paths:
  - docs/agents/tasks/active/OTC-20260902-vision-p2-vision-reconciliation.md
  - docs/agents/reports/OTC-20260902-vision-p2-vision-reconciliation.md
  - tools/tibia_re_control_center/agent_reconcile.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/vision_p2_trusted_composition.py
  - tests/tools/tibia_re_control_center/test_agent_reconcile.py
  - tests/tools/tibia_re_control_center/test_agent_session.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
modules_touched:
  - TIBIA RE Control Center agent reconciliation
  - Vision P2 trusted composition
  - persistent agent-session evidence
reuses:
  - tools/tibia_re_control_center/agent_vision.py
  - tools/tibia_re_control_center/agent_runtime_signals.py
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tools/tibia_re_control_center/persistent_store.py
depends_on:
  - PR #839 runtime-signals producer promotion merged
  - PR #854 trusted Vision P2 composition merged as 2e57cb1f0b57d44b1adf553d06b18e22e145c77e
  - lifecycle closeout PR #855 merged as main 8441fc1cce1600033b505d68ebc5c0141b337394
blocks:
  - OTC-VISION-P2-E2E-AUDIT
current_blocker: none
next_action: implement the production trusted reconciliation seam by consuming accepted capture and reviewed runtime-signal interfaces, persist auditable agreement/conflict provenance, and prove fail-closed behavior without granting runtime or mutation authority
invocation_started_at: 2026-09-02T10:46:00+02:00
last_progress_at: 2026-09-02T10:46:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# OTC-VISION-P2-VISION-RECONCILIATION

## Mission

Integrate the already accepted Vision P2 capture/vision path and reviewed runtime-signal path through the existing deterministic reconciliation contract. The implementation must remain authority-neutral: visual output is observation data, reviewed runtime evidence is accepted only through trusted composition, and no Phase 2 code may make a physical Tibia action executable.

## Binding authority

- `AGENTS.md`
- `docs/agents/AGENTS.md`
- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`

## Verified starting point

At task creation, trusted `main` is `8441fc1cce1600033b505d68ebc5c0141b337394`. `agent_reconcile.py` already provides finite fail-closed reconciliation rules and a private resolver-bound composition seam, but its public/default path intentionally has no production resolver. `vision_p2_trusted_composition.py` owns the accepted trusted capture/runtime composition but currently has no reconciliation binding. `ControlDomainService.observe_agent_vision()` produces a bounded `VisionObservation`; the session edge path already persists accepted read-only edge/runtime evidence. Do not duplicate those producers.

## Required behavior

- Consume accepted interfaces; do not create a second capture, transport, runtime-signal resolver, state store or control plane.
- Preserve the exact visual vocabulary `UNKNOWN`, `LOGIN_SCREEN`, `CHARACTER_SELECT`, `WORLD_VISUAL`, `WORLD_EXIT_VISUAL`, `ERROR_SCREEN`.
- `WORLD_VISUAL` alone must never become semantic `IN_GAME`/`WORLD_CONFIRMED`.
- Semantic confirmation/conflict that depends on runtime state must require current reviewed causal evidence from the trusted resolver and matching current session/run/runtime identity.
- Stale, missing, mismatched, unreviewed or caller-minted runtime evidence must fail closed to an inconclusive/unknown result.
- Persist enough typed provenance/evidence references for the existing owner-visible session/event/result surfaces to explain visual/runtime agreement or conflict across restart without treating persisted stale evidence as current authority.
- OCR/visible text remains data only and cannot become executable instruction or authority.
- Qwen profile/model-slot policy remains unchanged and single-model; this task does not authorize loading another model or forced eviction.
- Production `BoundedActionExecutor` remains Null/unbound; `runtime_access:none`, all mutation/login/gameplay/process/input authority false, and physical budget/count `0/0` remain invariant.

## Acceptance

Repository/static validation must prove the trusted production composition can combine a valid visual observation with stronger current reviewed runtime evidence and emit/persist explainable agreement/conflict, while forged/stale/mismatched evidence cannot self-promote. A later coordinator-serialized real read-only observation is still required for physical E2E; hosted/fake tests cannot satisfy that live gate.

## Validation plan

Use RED-to-GREEN focused tests first, then the smallest relevant Control Center/Vision P2 workflow on the exact final head. Preserve the canonical frozen vision benchmark where applicable. Do not spend Codex quota on coordination, status polling or CI waiting. If GitHub-only execution proves insufficient for an implementation/test loop, persist the exact missing operation before any separately justified worker invocation.
