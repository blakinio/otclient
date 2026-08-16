---
task_id: OTC-20260816-track-a-runner-system-xkbcomp-repair
status: ready
agent: ChatGPT
session_id: chatgpt-system-xkbcomp-repair-20260816-1722
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runner_infrastructure_repair
phase: coordinator-promotion-ready
branch: ci/OTC-20260816-track-a-runner-system-xkbcomp-repair
base_branch: main
base_main: 22089c5ca65228379c409dd33561a096eea00b16
risk: medium
updated: 2026-08-16T17:27:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-runner-system-xkbcomp-repair.md
  - docs/agents/evidence/OTC-20260816-track-a-runner-system-xkbcomp-repair/**
modules_touched: []
reuses:
  - docs/agents/evidence/OTC-20260816-track-a-isolated-xvfb-startup-discriminator/20260816-xvfb-startup.md
  - xkbcomp support inventory run 31955054478/job 95184310959 from PR #388
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: repair targeted only the dedicated runner container support filesystem required by the packaged Xvfb absolute helper path; no official-client or canonical runtime surface was accessed
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
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
target_uniqueness: PROVEN
mutation_authorized: false
runner_filesystem_mutation_authorized: true
owner_funded_ai_api_authorized: false
authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks; bounded dedicated-runner support repair only, no client/canonical runtime mutation
repair_source:
  path: /work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
  required_realpath: /work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
  required_uid: 0
  required_mode: 755
  required_sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
  required_ldd_missing_count: 0
repair_target:
  path: /usr/bin/xkbcomp
  publication_result: ATOMIC_CREATED
  retained_after_success: true
  sha256: 0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
  durability: immediate_container_repair_not_declarative_image_provisioning
post_repair_validation:
  process: contained Xvfb only
  display: ':199'
  socket_created: true
  result: PASS
  canonical_runtime_touched: false
validation:
  repair_head: ebd428390e13cec5b064602d37e8a2b2b76181ed
  repair_run: 31955642775
  repair_job: 95185761723
  repair_result: SUCCESS
  source_fence: PASS
  target_publication: ATOMIC_CREATED
  target_sha_match: PASS
  xvfb_socket_validation: PASS
  one_shot_workflow_removed: true
  final_exact_head_governance: PENDING
  final_exact_head_repository_ci: PENDING
  review_threads_open: 0
evidence_path: docs/agents/evidence/OTC-20260816-track-a-runner-system-xkbcomp-repair/20260816-system-xkbcomp-repair.md
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - stale queued runs 31955423015 and 31955459528 plus queued selector-mismatch run 31955535321 were cancelled before execution by task-local concurrency
    - successful run used proven dedicated-runner labels [otclient, synology]
    - no official client, VNC, WARP, canonical lease/registration/session, game login, credentials or Track B surface was touched
acceptance:
  - source exact path/realpath/uid/mode/SHA were re-proven and ldd under contained libs had zero missing dependencies
  - job authority was root and /usr/bin was safely writable
  - exact helper was atomically published to /usr/bin/xkbcomp and source/target SHA equality was proven
  - one isolated Xvfb invocation created its X11 socket and was cleaned up
  - one-shot workflow was removed immediately after terminal result
  - successful system helper publication remains classified as immediate container repair, not durable declarative runner-image provisioning
last_completed_step: run 31955642775/job 95185761723 atomically published exact /usr/bin/xkbcomp and proved isolated contained Xvfb socket creation on :199; one-shot workflow removed and sanitized evidence persisted
next_action: obtain final exact-head Track A governance/repository CI, then coordinator-promote this PR and archive the task; fresh RUNTIME bootstrap may then resume from current trusted main with a new admission record
---

# Dedicated runner system xkbcomp repair

The dedicated runner now has the exact contained xkbcomp helper exposed at the compile-time absolute path required by Xvfb. An isolated Xvfb startup created its socket successfully. This task did not launch or claim the canonical official-client runtime.
