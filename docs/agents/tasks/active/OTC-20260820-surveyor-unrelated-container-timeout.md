---
task_id: OTC-20260820-surveyor-unrelated-container-timeout
status: implementing
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
task_kind: bugfix
phase: implement
branch: fix/OTC-20260820-surveyor-unrelated-container-timeout
base_branch: main
base_sha: 29f466b32192641f53ef691759e6589a6a185bd5
risk: low
owned_paths:
  - tools/tibia_re_surveyor/runtime.py
  - tests/tools/tibia_re_surveyor/test_runtime.py
  - docs/agents/tasks/active/OTC-20260820-surveyor-unrelated-container-timeout.md
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owner_funded_ai_api_authorized: false
related_physical_run: 32348184547
current_blocker: none
next_action: make unrelated-container pgrep timeout skippable while preserving target-container timeout as a hard failure, add regression tests, validate and merge before rerunning the same one-shot snapshot
---

# Surveyor unrelated-container timeout repair

Physical read-only run `32348184547` proved the exact target and `BRIDGE_3_OF_3`, then failed because `_candidate_containers()` treated a five-second `pgrep` timeout in unrelated `freqtrade-portal-staging` as fatal. This repository-only repair must skip probe failures for unrelated containers only. Failure to inventory the designated Tibia target remains fatal/fail-closed.
