---
task_id: OTC-20260816-track-a-xres-support-inventory
status: implementing
agent: ChatGPT
session_id: chatgpt-xres-support-inventory-20260816
session_role: runtime_support_observer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_infrastructure_inventory
phase: fixed-path-xres-client-support-readonly
branch: diag/OTC-20260816-track-a-xres-support-inventory
base_branch: main
base_main: 845adabba5f6d2bfecb6d54bc13834c47cc61c94
risk: low
updated: 2026-08-16T23:32:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-xres-support-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-xres-support-inventory/**
  - .github/workflows/tibia-official-client-re-xres-support-inventory.yml
modules_touched: []
reuses:
  - PR #442 XRes helper-unavailable result as unpromoted research input only
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260816-track-a-xres-window-identity
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the one physical XRes identity attempt reproduced the viewable raw X11 window but could not resolve libxcb-res.so.0 from its bounded fixed allowlist. Before any new client launch, this task performs one fixed-path read-only support inventory on the same Synology runner to determine whether libxcb-res, libXRes, XRes/XCB-RES headers/pkgconfig metadata, or the necessary QueryClientIds symbols exist elsewhere in the contained toolroot or standard system library/include roots; it also records enough protocol-layout evidence to decide whether a future helper can use an existing library or must implement the request over the local X socket.
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: read_only
runtime_owner_task: OTC-20260816-track-a-xres-support-inventory
runtime_namespace: runner-support-xres-client-capability
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
observation_allowlist:
  - /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu fixed named libxcb-res.so*, libXRes.so*, libxcb.so*, libX11.so* candidates
  - /work/_otclient_tibia_re_state/toolroot/lib/x86_64-linux-gnu same fixed named candidates
  - /usr/lib/x86_64-linux-gnu same fixed named candidates
  - /lib/x86_64-linux-gnu same fixed named candidates
  - /work/_otclient_tibia_re_state/toolroot/usr/include/xcb/res.h
  - /work/_otclient_tibia_re_state/toolroot/usr/include/X11/extensions/XRes.h and XResproto.h
  - /usr/include/xcb/res.h
  - /usr/include/X11/extensions/XRes.h and XResproto.h
  - fixed xcb-res/XRes pkgconfig files beneath contained/system pkgconfig roots
  - file metadata, symlink target containment, SHA-256, bounded symbol/string matches for QueryClientIds/LocalClientPid/XResQueryClientIds/XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID
forbidden_observation:
  - official client package/files/processes
  - any X server/display/window state
  - /proc process inventory
  - canonical lease/registration/session state
  - credentials, network/game/login state
  - Track B and historical PR #303 runtime surfaces
acceptance:
  - same-job deterministic Track A admission passes before support read
  - exact PR base fence passes
  - no process/X11/client/canonical state access
  - all fixed candidate paths are reported present/absent without ambient filesystem search
  - present libraries receive resolved path/hash/size and bounded XRes symbol/string evidence
  - present headers/pkgconfig metadata receive bounded relevant lines without unrelated content
  - result classifies existing libxcb-res helper, existing libXRes helper, headers-only/raw-protocol basis, or no support evidence
  - exactly one read-only inventory run; one-shot workflow removed after capture
last_completed_step: XRes source result from PR #442 run 31973388722 / job 95229260820 proved the bounded runtime helper saw libxcb=true, libxcb_res=false, libX11=true and therefore left exact window PID ownership unresolved; no second client launch is authorized
next_action: execute exactly one fixed-path read-only XRes client-support inventory on synology-otclient-01, persist the result, remove the workflow, return mutation_authorized=false and hand the Draft to coordinator
---

# Track A XRes client-support inventory

Support-filesystem observation only. This task must not start Xvfb or the official client and must not inspect canonical runtime state.
