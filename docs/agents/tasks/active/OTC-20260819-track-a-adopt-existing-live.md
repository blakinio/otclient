---
task_id: OTC-20260819-track-a-adopt-existing-live
status: in_progress
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: bounded_runtime_reconciliation
phase: post_adoption_pre_gate_b
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
gate_b: REQUIRED_NOT_PROVEN
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
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
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
depends_on: []
blocks:
  - surveyor canonical keepalive authorization
adopt_existing_result: PASS
adopt_existing_lease_generation: 17
registered_pid: 19590
registered_state: IN_GAME
registered_state_evidence: BRIDGE_3_OF_3
registered_candidate_count: 1
registered_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
registered_runtime_locator: docker:otclient-track-a-kasmvnc:1af4af4d67f5
current_blocker: GATE_B_REQUIRED
next_action: execute fresh adoption-aware Gate B under the current generation-17 lease and canonical flock, then persist the mutation admission result before any GUI input
---

# Physical adopt-existing of current Track A runtime

The reviewed metadata-only `adopt-existing` transition completed from trusted main. The authoritative registration is now present and binds generation 17 to the exact current client: PID `19590`, client 15.32 exact size/SHA, `DISPLAY=:1`, Docker runtime locator, one candidate, and structural `IN_GAME / BRIDGE_3_OF_3` evidence.

This checkpoint is a fresh ordinary canonical reuse admission. Mutation remains refused until adoption-aware Gate B passes under the same current lease and canonical flock. No credentials, login, restart, signal, injection, kill, or GUI/gameplay input has occurred in this task.
