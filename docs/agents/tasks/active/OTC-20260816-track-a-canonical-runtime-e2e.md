---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-canonical-runtime-p0-xres-window-20260817
session_role: canonical_runtime_integration
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: canonical-xres-window-integration
branch: runtime/OTC-20260816-track-a-canonical-runtime-p0-xres-window
base_branch: main
base_main: 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
risk: high
updated: 2026-08-17T11:57:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/scripts/tibia-official-client-re-xres-window-owner.py
  - .github/scripts/test_tibia_official_client_re_xres_window_owner.py
  - .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py
  - .github/scripts/test_tibia_official_client_re_canonical_xres_worker_adapter.py
  - .github/workflows/tibia-official-client-re-canonical-xres-window-identity.yml
modules_touched:
  - track-a-canonical-live-runtime
  - track-a-xres-window-identity
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: retained physical XRes identity #457 and persistent helper fix #461 are trusted on main; the remaining known canonical blocker is the legacy xdotool PID/name window selector, so this hosted-only phase integrates raw XRes ownership into the existing canonical worker contract before any fresh physical admission
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
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
client_byte_mutation_authorized: false
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
identity_chain:
  raw_xres_helper_promotion_pr: 448
  raw_xres_helper_promotion_merge: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
  client_id_length_fix_pr: 455
  client_id_length_fix_merge: 60ab740872d52f3f7c4802d49fd5275a9968d085
  physical_identity_pr: 457
  physical_identity_merge: 16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc
  physical_identity_run: 32015479835
  physical_identity_job: 95344000918
  physical_identity: PROVEN
  physical_identity_classification: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  physical_identity_cleanup: COMPLETE
  identity_archive_pr: 459
  identity_archive_merge: c55e3523e6e9d50df511e65dce9145a8f951a5f5
  identity_ownership_released: true
  xres_client_base_fix_pr: 461
  xres_client_base_fix_merge: 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
retained_v2_fixture:
  queried_resource_xid: '0x00c00011'
  returned_client_base: '0x00c00000'
  returned_mask: LocalClientPid
  returned_pid: 13648
  exact_launched_pid: 13648
  raw_reply_hex: 01000300040000000100000000000000000000000000000000000000000000000000c000020000000400000050350000
persistent_helper:
  finding: XRES-V2-AUD-001
  status: RESOLVED_ON_MAIN_BY_PR_461
  retained_physical_fixture_regression: PASS
  deterministic_tests: 37
  physical_retry_required: false
canonical_window_integration:
  trusted_worker: .github/scripts/tibia-official-client-re-canonical-live-session.sh
  legacy_selector: "xdotool search --onlyvisible --pid <pid> --name '^Tibia$'"
  legacy_selector_physical_disposition: DISPROVEN_FOR_EXACT_CLIENT_WINDOW_IDENTITY
  new_owner_resolver: .github/scripts/tibia-official-client-re-xres-window-owner.py
  worker_adapter: .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py
  behavior:
    - enumerate bounded VIEWABLE 1920x1080 X11 resources
    - QueryVersion XRes >= 1.2
    - QueryClientIds LocalClientPid using promoted wire helper semantics
    - select exactly one resource whose LocalClientPid equals the expected fenced client PID
    - fail closed on ambiguity, malformed reply, transport failure, no match or process exit
  physical_runtime_used_in_this_phase: false
safety:
  canonical_state_access: forbidden_during_hosted_integration
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  process_memory_access: false
  client_byte_mutation: false
  physical_identity_retry_authorized: false
  canonical_bootstrap_for_p0_only: forbidden
  track_b_access: false
acceptance:
  - current main helper semantics from #461 remain covered
  - retained #457 resource/client-base/PID fixture is accepted
  - exactly one expected-PID viewable candidate is selected; ambiguity fails closed
  - adapter replaces exactly one legacy canonical window selector and refuses source drift
  - generated canonical worker passes bash syntax and no legacy xdotool PID/name selector remains
  - existing canonical transition regression suite remains green
  - hosted-only workflow passes on the exact implementation head
  - independent exact-diff audit has zero material findings
  - no Synology, official-client, X11 runtime or canonical-state access occurs before merge
  - after merge, perform fresh P0 RUNTIME admission and stop fail-closed if no legal current IN_GAME lifecycle exists; do not bootstrap a session solely for P0
last_completed_step: rebased the remaining canonical XRes window-integration work onto main after #461 and removed the duplicate-task path from the integration plan
next_action: validate hosted XRes window integration on the exact PR head, audit and merge it, then create the fresh P0 physical RUNTIME admission required by the current trusted-base checkpoint
---

# Track A canonical runtime E2E — canonical XRes window integration

The physical XID-to-PID proof and persistent client-base helper correction are already promoted. This phase removes the last known property/name-based identity assumption from the worker used by canonical bootstrap/probe, without touching a live runtime. Physical P0 work remains separately gated by fresh admission after this integration reaches trusted main.
