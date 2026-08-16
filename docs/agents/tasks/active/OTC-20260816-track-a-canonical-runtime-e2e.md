---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-post-rhi-window-state-20260816
session_role: runtime_discriminator_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: post-glx-post-rhi-x11-window-state-discriminator
branch: diag/OTC-20260816-track-a-post-rhi-window-state
base_branch: main
base_main: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
risk: high
updated: 2026-08-16T22:50:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-post-rhi-window-state.yml
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-dri-repair-isolated-client-revalidation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - immutable isolated harness blob 1616edcc982be50ef2c95b8077160ec8fe9291fe
  - immutable DRI-revalidation transformer blob d2951fc592b3e1b7d28a953730bcee39ba18cfe5
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: governance reconciliation is now trusted on main via #436, while promoted physical evidence #431/#432/#434 proves the contained DRI path restores GLX and removes the prior configured QXcb no-GLX/EGL failure signature but the exact client remains alive with zero visible windows through 35 seconds. A canonical bootstrap retry would therefore be blind. This phase performs one separately admitted task-owned isolated startup whose new observations distinguish no X11 window creation from an existing but unmapped/unviewable/pid-shifted window, while also capturing bounded task-owned thread wait-channel state and a broader redacted post-RHI Qt/QML/window log.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260816-track-a-canonical-runtime-e2e
runtime_namespace: track-a-post-rhi-window-state-v1
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
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
latest_promoted_evidence:
  source_pr: 431
  promotion_pr: 432
  archive_pr: 434
  semantic_run: 31970703417
  semantic_job: 95222630271
  exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  glx_present: true
  qrhi_vulkan_initialized: true
  qtquick_window_plugin_loaded: true
  client_alive_t05_t15_t35: true
  visible_windows_t05_t15_t35: 0
  complete_client_log_lines: 415
  configured_allowlist_matches: 35
  remaining_no_window_root_cause: UNKNOWN_POST_GLX_PREREQUISITE
new_discriminator:
  exactly_one_semantic_physical_run: true
  canonical_state_access: NONE
  official_client_launch: task-owned isolated exact-fenced copy only
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  client_backend_forcing: false
  xvfb_new_input: contained LIBGL_DRIVERS_PATH only, matching the promoted repair
  observations:
    - complete non-root X11 window tree at t05/t15/t35 including XGetWindowAttributes map_state and geometry
    - correlate any X11 window with task-owned client/descendant PID, title and class when properties are available
    - distinguish viewable, unviewable and unmapped windows; retain bounded counts even when PID properties are absent
    - bounded task-owned client thread state/wchan snapshots; no global process scan
    - complete client log scanned locally with a broader redacted allowlist for QQml/QML/QtQuick/QQuick/QWindow/QPlatformWindow/window/scenegraph/QSG/QRhi/Vulkan/xcb/GLX/EGL/surface/swapchain/present/render/warning/error/failed/fatal/cannot/screen
    - preserve exact line count and emitted match count
  classifications_of_interest:
    - NO_NONROOT_X11_WINDOWS_CREATED
    - NONROOT_X11_WINDOWS_PRESENT_NONE_VIEWABLE
    - TASK_OWNED_X11_WINDOW_PRESENT_BUT_UNVIEWABLE
    - TASK_OWNED_X11_WINDOW_VIEWABLE
    - CLIENT_EXITED_BEFORE_DISCRIMINATOR
forbidden:
  - canonical lease/registration/session access
  - canonical-live-runtime namespace
  - Track B and historical PR #303 runtime surfaces
  - global /proc process inventory
  - credentials, login or gameplay
  - QT_XCB_GL_INTEGRATION=none
  - QSG_RHI_BACKEND or another forced graphics backend
  - +extension GLX
  - client-side LIBGL_DRIVERS_PATH leakage
  - second semantic run after a valid discriminator
  - blind canonical bootstrap retry
acceptance:
  - exact base and immutable source blobs fenced before physical execution
  - standard Track A admission passes on the semantic head
  - exact contained Xvfb and swrast support fences pass
  - GLX remains present on the task-owned display
  - X11 all-window tree and task-owned thread state captured at bounded snapshots
  - broader redacted complete-log filter emits exact match count
  - no canonical state, credentials/login/gameplay or forced client backend
  - cleanup complete
  - exactly one valid semantic physical run
  - one-shot workflow removed immediately after capture
  - resulting evidence determines a narrower next causal action; identical launch is not retried
safety:
  blind_canonical_bootstrap_retry_forbidden: true
  canonical_bootstrap_admission_validator_reconciled_on_main: true
  canonical_bootstrap_currently_authorized_for_this_phase: false
last_completed_step: #436 merged the trusted bootstrap-admission reconciliation as b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4; review of #431 job 95222630271 proved the prior window harness counted all visible windows on the isolated display and still saw zero, while QRhi Vulkan and QtQuick/Window loaded
next_action: execute exactly one task-owned isolated post-RHI X11-window-state discriminator, persist the result, remove its workflow, then continue from the new causal classification without a blind canonical retry
---

# Track A canonical runtime E2E — post-RHI window-state phase

The canonical bootstrap path is now governable but deliberately not used here. The current blocker is a proven visible-window failure that persists after GLX restoration. This one-run isolated discriminator asks whether an X11 window exists but is not viewable, or whether the exact client never creates a non-root X11 window at all.
