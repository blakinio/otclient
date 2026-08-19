---
task_id: OTC-20260819-track-a-adopt-existing-live
status: in_progress
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: bounded_runtime_reconciliation
phase: gate_b_pass_keepalive_admission
branch: runtime/OTC-20260819-track-a-adopt-existing-live
base_branch: main
base_sha: 97593631cfdaae8c38fcb497adf156760068f19a
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260819-track-a-adopt-existing-live
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: 17
registration_lease_generation: 17
gate_a: PASS
generation_rebind: NOT_APPLICABLE
gate_b: PASS
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: true
gui_input_authorized: true
mutation_scope: surveyor_keepalive_turn_in_place_only
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-adopt-existing-live.md
modules_touched:
  - canonical-live-transition
  - canonical-live-kasm-adoption-probe
reuses:
  - PR #596
  - PR #606
  - PR #608
  - PR #611
  - PR #592
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
depends_on: []
blocks: []
adopt_existing_result: PASS
adopt_existing_lease_generation: 17
gate_b_result: PASS
registered_pid: 19590
registered_state: IN_GAME
registered_state_evidence: BRIDGE_3_OF_3
registered_candidate_count: 1
registered_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
registered_runtime_locator: docker:otclient-track-a-kasmvnc:1af4af4d67f5
current_blocker: NONE
next_action: validate this exact mutation admission and run only the Surveyor keepalive turn-in-place path inside the final canonical guard and shared GUI lock
---

# Physical adopt-existing of current Track A runtime

The reviewed metadata-only `adopt-existing` transition completed from trusted main. The authoritative registration binds generation 17 to the exact current client: PID `19590`, client 15.32 exact size/SHA, `DISPLAY=:1`, Docker runtime locator, one candidate, and structural `IN_GAME / BRIDGE_3_OF_3` evidence.

A fresh adoption-aware Gate B then passed under the same current generation-17 lease and canonical flock. Mutation authority is now narrowly admitted only for the owner-requested Surveyor keepalive turn-in-place path. No credential access, login, restart, signal, injection or kill is authorized; all GUI input must remain inside the final canonical guard and the repository's shared GUI lock/heartbeat contract.
