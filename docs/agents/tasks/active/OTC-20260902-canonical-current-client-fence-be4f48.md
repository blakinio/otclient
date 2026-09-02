---
task_id: OTC-20260902-canonical-current-client-fence-be4f48
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: verification
branch: fix/OTC-20260902-canonical-current-client-fence-be4f48
base_branch: main
base_main: 8441fc1cce1600033b505d68ebc5c0141b337394
created: 2026-09-02T12:35:00+02:00
risk: high
execution_class: hybrid
execution_mode: chat_github_plus_remote_provenance
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
credentials_allowed: false
login_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
implementation_authorized: true
owner_funded_ai_api_authorized: false
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - .github/workflows/track-a-canonical-current-client-fence.yml
  - .github/workflows/track-a-canonical-live-governance.yml
  - .github/workflows/track-a-kasm-canonical-bootstrap.yml
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/CHANGELOG.md
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
  - docs/agents/tasks/active/OTC-20260902-canonical-current-client-fence-be4f48.md
  - docs/agents/evidence/OTC-20260902-canonical-current-client-fence-be4f48/**
---

# Objective

Advance only the trusted **current exact-client identity fence** from `15.32.75d4a0 / 52105824 / d1a16819...` to the owner-observed official-launcher build `15.32.be4f48 / 52105824 / 552dcf79...` and synchronize all current canonical/read-only admission consumers.

Historical build-specific reverse-engineering evidence, offsets, login writers, QMeta addresses, serializers and prior client-fence-reconciliation source/target contracts remain historical and must not be promoted to the new binary.

# Provenance boundary

Authority for the new tuple is limited to agreement between the official launcher's installed package manifest and a fresh hash/size of the exact singleton live ELF. Raw CDN refetch attempts were blocked by Cloudflare challenge/HTTP 403 and are not counted as proof.

# Acceptance

1. TDD RED proves the old trusted-current fence is still authoritative before implementation.
2. Normative Track A governance, canonical runtime components, Kasm bootstrap identity and Phase 2 read-only admission use one exact new tuple.
3. Historical build-specific research surfaces remain pinned to their source builds.
4. Existing canonical component tests, runtime-admission tests, deterministic governance and diff checks pass.
5. No login, credentials, gameplay, GUI input, process control, memory access or packet capture from this repository-only task.
6. Direct Codex usage remains zero unless a later independent audit is explicitly justified.

next_action: write and observe the focused TDD RED before changing any current-authority production/governance constants
