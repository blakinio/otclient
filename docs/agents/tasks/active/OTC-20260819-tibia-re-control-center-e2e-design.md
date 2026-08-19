---
task_id: OTC-20260819-tibia-re-control-center-e2e-design
status: in_progress
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN
track_id: official-client-re
task_kind: research_infrastructure_design
feature_scope:
  type: architecture
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
branch: docs/OTC-20260819-tibia-re-control-center-e2e-design
base_branch: main
base_sha: 951888b338382bc2511ec846fad46518298baa72
risk: low
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-e2e-design.md
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
modules_touched: []
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
  - tools/tibia_runtime_bridge/**
  - PR #592 tools/tibia_re_surveyor/**
depends_on:
  - PR #592 for Surveyor implementation/integration surface; design may merge independently
blocks: []
cross_repository_task_ids:
  - future separate Oteryn-v2 adapter task in blakinio/Oteryn-v2
track_a_runtime_agent_admission_version: 1
execution_class: github_repository_docs
runtime_access: none
persistent_session_role: none
runtime_owner_task: null
runtime_namespace: null
canonical_registration: NOT_ACCESSED
canonical_lease_generation: NOT_ACCESSED
registration_lease_generation: NOT_ACCESSED
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owner_funded_ai_api_authorized: false
owner_current_instruction: prepare the project described by the current TIBIA RE Control Center UI concept for browser or direct-machine use and future Oteryn Rust E2E reuse
invocation_started_at: 2026-08-19T15:16:00+02:00
last_progress_at: 2026-08-19T15:16:00+02:00
current_blocker: null
next_action: author the normative project architecture, adapter contract and bounded MVP implementation prompt, then self-review the exact diff
---

# TIBIA RE Control Center / E2E Lab design

## Objective

Turn the current Control Center UI concept into a durable implementation project for the official-client Track A programme, with two operator surfaces:

1. browser-based control UI;
2. direct-machine CLI/local UI on the machine that hosts the client runtime.

The design must preserve Track A authority and fail-closed boundaries, reuse Surveyor/runtime-bridge work instead of duplicating it, and define an adapter boundary that can later be implemented independently in `blakinio/Oteryn-v2` for semantic differential E2E testing.

## Scope for this task

Documentation and contracts only. No runtime observation, no GUI input, no login, no credential access, no process instrumentation, no gameplay and no Oteryn-v2 repository mutation.

## Acceptance criteria

- define the component architecture and deployment modes;
- define the operator UI information architecture based on the approved dense desktop-style mockup;
- define the scenario/action/event/artifact model;
- define fail-closed Track A authority flow and emergency-stop semantics;
- define a stable adapter contract that does not couple scenario semantics to official-client implementation details;
- define the future `blakinio/Oteryn-v2` adapter boundary without changing that repository;
- define MVP phases and explicit non-goals;
- provide a bounded implementation prompt that a later agent can execute without reconstructing this chat;
- keep all implementation paths unclaimed so #592 and other active runtime tasks are not overlapped.

## Context checkpoint

```yaml
phase: design_authoring
base_main: 951888b338382bc2511ec846fad46518298baa72
survey_pr: 592
survey_pr_status: open_draft
survey_owned_paths_overlap: none
runtime_access: none
credentials_accessed: false
client_executed: false
next_action: author the project programme and adapter contract
```
