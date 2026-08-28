---
task_id: OTC-20260828-canonical-current-client-fence
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: verification
branch: fix/OTC-20260828-canonical-current-client-fence
base_branch: main
base_main: 785d888e8392e32c8ba852d6db7c8de03db9d8be
created: 2026-08-28T15:40:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
physical_e2e_required: false
implementation_authorized: true
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - .github/workflows/track-a-canonical-current-client-fence.yml
  - .github/workflows/track-a-canonical-live-governance.yml
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260828-canonical-current-client-fence.md
modules_touched:
  - track-a-canonical-live-runtime
reuses:
  - trusted-main promotion #752 exact current client and field6 runtime-observation boundary
  - merged canonical lease/transition/session worker
  - merged existing-runtime adoption probe
  - merged exact-current observer evidence from #744/#745/#746
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Repair the trusted canonical-live and runtime-admission exact-client contract so it admits the already independently promoted current official Linux client `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a` instead of the superseded `ed5469... / 52109920` cut.

This task is repository-only. It must not bootstrap, execute, authenticate, observe, mutate or control any official client. A later runtime successor must use the merged result under fresh admission and the requirements of its chosen `runtime_access` class.

# Root-cause boundary

The stale fence was not isolated to one launcher. Trusted `main` bound the superseded cut in the canonical session worker, canonical transition/Gate-B controller, Kasm existing-runtime adoption probe, mandatory Track A runtime-admission contract, normative Track A/ADR/bootstrap governance, canonical-live governance audit, and deterministic Track A agent governance audit. Updating only a subset would create a split-brain canonical identity contract and is forbidden.

# TDD / verification evidence

- Mandatory runtime-admission RED: head `fc1b944ea6ce92da7f8fbe9164047458592f5ecb`, run `33182303064`, job `98886326388`, failure `runtime admission contract: current build version missing`.
- Component repair proof: run `33182582810`, job `98887274050`, focused fence/session/transition/adoption validation and `git diff --check` PASS before its non-workflow repair commit was pushed.
- Stale exact-version provenance RED: head `93eb752ebebd143156b50adc78f3fc4a6f47475f`, run `33183051046`, job `98888001935`, failure `runtime admission contract: stale version-family provenance remains`.
- Independent deterministic Track A governance RED: run `33183051039`, job `98888893067`, proving its own old `ed5469...` current-fence constants also had to be updated.
- Exact-current governance constants are now synchronized to `15.32.75d4a0 / 52105824 / d1a168...` and all temporary write-capable workflow jobs have been removed.
- Read-only verification head `e04043e306c933697757a47d6208b84f2757ebaf`: focused canonical current-client fence run `33183712961` SUCCESS; Track A agent runtime governance run `33183712944` SUCCESS; canonical live governance run `33183712982` SUCCESS. CI was still running when this task checkpoint was written, so no terminal merge claim is made here.

# Acceptance

1. Hosted RED proves trusted main bound stale current authority and independently falsifies all discovered split-brain consumers.
2. Worker, transition controller, adoption probe, runtime-admission contract, deterministic Track A governance test, canonical-live governance fence and normative current-client references use one exact current identity.
3. Historical evidence may retain historical hashes only when explicitly historical.
4. Existing canonical session/transition/adoption tests remain GREEN.
5. Fresh exact-current promotion evidence on trusted main is provenance; no client download/execution is required for this repository repair.
6. Exact-head CI, Track A agent governance, canonical-live governance and focused fence workflow must pass.
7. Fresh post-implementation exact-scope audit must find zero material issues before merge.
8. No runtime, credentials, login, process memory, packet access, GUI input or process control from this PR.

next_action: obtain a fresh all-green exact-head run after this verification checkpoint, review exact changed scope and unresolved threads, re-check protected main immediately before merge, then squash-merge only if every gate remains PASS.
