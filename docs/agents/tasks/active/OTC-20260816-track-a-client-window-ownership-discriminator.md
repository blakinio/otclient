---
task_id: OTC-20260816-track-a-client-window-ownership-discriminator
status: implementing
agent: ChatGPT
session_id: chatgpt-window-discriminator-20260816
session_role: runtime_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: repaired-discriminator-v3-in-flight
branch: ci/OTC-20260816-track-a-client-window-ownership-discriminator
base_branch: main
base_main: 05d4a7136e234b874f7f112ad8c92f01b0aabd51
risk: high
updated: 2026-08-16T18:17:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-client-window-ownership-discriminator.md
  - docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/**
  - .github/workflows/tibia-official-client-re-window-ownership-discriminator-v2.yml
modules_touched: []
reuses:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v6-client-window-missing.md
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical discriminator must reproduce the exact native-Linux client startup on the dedicated runner; all mutation stays inside one task-owned ephemeral namespace and never writes canonical lease/registration state
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-client-window-ownership-discriminator
runtime_namespace: track-a-client-window-discriminator-v1
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
live_runtime_authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks; this authorization is limited to one isolated no-login startup discriminator and its evidence-based harness repair, excluding canonical registration/session mutation
namespace_proof:
  repository_overlap_search: ZERO_MATCHES_BEFORE_CLAIM
  state_root: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260816-track-a-client-window-ownership-discriminator/ephemeral
  state_root_rule: every run uses a run-id-specific child and refuses an existing child namespace
  display_pool: 231-250
  display_rule: select only lock/socket-free display and clean only recorded task-owned process/socket state
  network_rule: task-owned pinned wgcf/wireproxy binaries, profile and loopback SOCKS port only
canonical_boundary:
  read_or_write_canonical_lease: false
  read_or_write_canonical_registration: false
  canonical_display_or_vnc_reuse: false
  publish_registration: false
  login_allowed: false
  credentials_allowed: false
  gameplay_allowed: false
  track_b_access: false
exact_client_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
source_discriminator:
  canonical_pr: 397
  run: 31957502867
  job: 95190252936
  result: CLIENT_ALIVE_NO_MATCHING_PID_OWNED_VISIBLE_TIBIA_WINDOW
  evidence: docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v6-client-window-missing.md
first_diagnostic_run:
  run: 31957940075
  job: 95191373266
  result: DIAGNOSTIC_HARNESS_DEFECT_BEFORE_OBSERVATION
  exact_source_fence: PASS
  warp: PASS
  xvfb: PASS
  vnc: PASS
  failed_assertion: CLIENT_NOT_ISOLATED_GROUP
  observed_pid: 17676
  observed_pgid: 64
  window_snapshots_collected: false
  client_log_discriminator_collected: false
  cleanup: COMPLETE
  canonical_state_touched: false
  evidence: docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-first-run-harness-pgid-failure.md
repair_cycle:
  repair_cycles_for_current_gate: 1
  justification: remove unnecessary wrapper PID/PGID assumption before observation and add exact trusted-worker launchermetadata fidelity; first run never reached semantic discriminator
  launcher_model: direct Python subprocess with start_new_session true returning the exact client PID
  process_cleanup_model: launched PID plus marker-verified descendants from known ancestry only; no process-group kill and no broad process scan
  launchermetadata_fidelity: REQUIRED_AND_IMPLEMENTED
  corrected_workflow: .github/workflows/tibia-official-client-re-window-ownership-discriminator-v2.yml
  corrected_workflow_generation: v3
  additional_physical_runs_authorized: 1
acceptance:
  - reproduce the trusted client startup environment in a task-owned ephemeral home/display/WARP namespace without canonical state
  - verify exact client source size/SHA before launch and copy it into task-owned home
  - mirror the trusted worker conditional launchermetadata.json copy
  - verify contained toolroot and exact /usr/bin/xkbcomp before Xvfb
  - verify the launched observation PID resolves to the copied exact client and carries the task marker
  - collect bounded snapshots at startup and within 35 seconds only
  - enumerate only visible X11 windows on the task-owned display, recording window id/title/class/geometry and reported PID where available
  - distinguish exact launched PID, direct/descendant task-owned process window ownership, other title, or no visible window
  - capture bounded sanitized task-owned client stdout/stderr without credentials/tokens/cookies
  - do not inspect BattlEye internals or bypass/evasion behavior
  - do not login or send gameplay input
  - terminate only the launched marker-owned client PID plus marker-verified descendants from its known ancestry, then task-owned Xvfb/VNC/WARP; remove sandbox before exit
  - remove one-shot workflow after terminal evidence
last_completed_step: first physical run stopped before semantic observation because PGID==PID was an unnecessary harness assumption; v3 now launches the exact client via start_new_session, mirrors trusted launchermetadata handling and uses ancestry-only cleanup
next_action: consume exactly one repaired v3 physical discriminator; persist its bounded sanitized evidence and do not perform any further physical retry from this task
---

# Track A client-window ownership/startup discriminator

The first isolated run proved the namespace/support path but stopped before window observation because of a harness process-group assumption. The repaired v3 generation is the sole remaining physical discriminator and cannot modify canonical state or use login credentials.
