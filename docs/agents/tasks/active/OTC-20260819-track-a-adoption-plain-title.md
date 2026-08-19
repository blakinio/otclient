---
task_id: OTC-20260819-track-a-adoption-plain-title
status: validating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_hardening
phase: exact-head-validation
branch: fix/OTC-20260819-track-a-adoption-plain-title
base_branch: main
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
gameplay_allowed: false
owned_paths:
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py
  - docs/agents/tasks/active/OTC-20260819-track-a-adoption-plain-title.md
modules_touched: [canonical-live-kasm-adoption-probe]
reuses: [PR #596, PR #606]
depends_on: []
blocks: [first physical adopt-existing invocation]
focused_kasm_probe_tests: 10_OF_10_PASS
physical_readonly_probe: PASS
physical_readonly_pid: 19590
physical_readonly_state: IN_GAME
physical_readonly_state_evidence: BRIDGE_3_OF_3
physical_readonly_candidate_count: 1
current_blocker: EXACT_HEAD_CI
---

# Adoption plain-title compatibility

Accept `Tibia` / `Tibia - ...` title candidates only as discovery input, then require exactly one candidate with exact X11 `WM_CLASS=client/Tibia` ownership and the freshly inventoried client PID. Auxiliary `Tibia` utility windows are ignored because they lack the required ownership. The title remains hashed identity context only; `IN_GAME` still requires exact-peer `BRIDGE_3_OF_3` and is never inferred from title text.

Fresh live read-only validation after the ownership-aware fix: exact client PID `19590`, exact size/SHA fence PASS, one exact owned client window selected despite an auxiliary 1x1 `Tibia` window, `candidate_count=1`, and structural `IN_GAME / BRIDGE_3_OF_3`. Focused probe tests are 10/10 PASS.
