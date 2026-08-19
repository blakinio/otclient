---
task_id: OTC-20260819-track-a-adoption-probe-executable
status: validating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_hardening
phase: exact_head_validation
branch: fix/OTC-20260819-track-a-adoption-probe-executable
base_branch: main
base_sha: 1a0a3824fd0d1e9e5a9ee8b6fd03889c30349f53
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
  - docs/agents/tasks/active/OTC-20260819-track-a-adoption-probe-executable.md
modules_touched:
  - canonical-live-kasm-adoption-probe
reuses:
  - PR #596
  - PR #606
  - PR #608
depends_on: []
blocks:
  - OTC-20260819-track-a-adopt-existing-live
focused_kasm_probe_tests: 10_OF_10_PASS
focused_transition_tests: 17_OF_17_PASS
direct_probe_exec: PASS
current_blocker: NONE
next_action: make the reviewed Kasm adoption probe executable in Git metadata, run exact-head governance/CI, and merge before retrying physical adoption
---

# Make Kasm adopt-existing probe executable

Physical adoption under PR #610 failed before its first probe because the reviewed Python probe was committed as mode `100644` while the canonical transition executes its worker path directly. The client was untouched and `runtime-registration.json` remained absent.

The minimal repair changes only the Git file mode of `.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py` from `100644` to `100755`; source bytes are unchanged. Local validation with that exact mode passed 10/10 Kasm-probe tests, 17/17 canonical-transition tests, and direct transition `_probe` execution against the current exact runtime (`PID 19590`, `IN_GAME`, `BRIDGE_3_OF_3`, candidate_count=1).
