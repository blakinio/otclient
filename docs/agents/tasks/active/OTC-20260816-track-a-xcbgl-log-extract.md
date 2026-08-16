---
task_id: OTC-20260816-track-a-xcbgl-log-extract
status: implementing
agent: ChatGPT
session_id: chatgpt-xcbgl-log-extract-20260816
session_role: runtime_evidence_researcher
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: evidence_extraction
phase: hosted-log-filter
branch: diag/OTC-20260816-track-a-xcbgl-log-extract
base_branch: main
base_main: cf3dce624efe58d2cc75192831030470ef9a338b
risk: low
updated: 2026-08-16T19:58:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xcbgl-log-extract.md
  - docs/agents/evidence/OTC-20260816-track-a-xcbgl-log-extract/**
  - .github/workflows/track-a-xcbgl-log-extract.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-qt-debug-plugins-discriminator.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xcbgl-plugin-inventory.md
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: completed physical job 95202662909 already contains QT_DEBUG_PLUGINS evidence, but connector rendering elided its middle section; GitHub-hosted Actions log extraction can recover the load-bearing xcbglintegrations/GLX/EGL lines without another physical client run
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
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
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
source_job:
  run: 31962559445
  job: 95202662909
  source_task: OTC-20260816-track-a-qt-debug-plugins-discriminator
  source_governance: SUCCESS
  source_cleanup: COMPLETE
filter_scope:
  - xcbglintegrations
  - libqxcb-glx-integration
  - libqxcb-egl-integration
  - xcb_glx
  - xcb_egl
  - Xcb GLX gl-integration
  - Failed to initialize GLX
  - QXcbIntegration
  - Cannot load library
  - loaded library
  - QRhi
acceptance:
  - fetch only completed job 95202662909 logs via GitHub Actions API
  - emit only allowlisted load-bearing plugin/GLX/EGL/RHI lines
  - no physical runner or client execution
  - no canonical runtime state access
  - no credentials/secrets printed or persisted
  - classify xcbglintegration discovery/load/init from the same already-completed physical run where evidence permits
last_completed_step: #410/#411 proved bundled platforms/libqxcb discovery but connector rendering omitted xcbglintegrations-specific middle lines
next_action: execute one GitHub-hosted filtered extraction of completed job 95202662909 and persist exact evidence; no physical retry
---

# Track A XCB GL log extraction

Hosted-only evidence recovery from one already-completed, governance-compliant physical job. No runtime execution occurs in this task.