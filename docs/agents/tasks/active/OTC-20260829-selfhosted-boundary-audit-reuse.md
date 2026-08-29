---
task_id: OTC-20260829-selfhosted-boundary-audit-reuse
status: ready
agent: ChatGPT
session_id: chatgpt-20260829-boundary-audit-reuse
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: infrastructure_security
phase: validate
branch: fix/OTC-20260829-selfhosted-audit-reusable
base_branch: main
base_main: ed0b048f72b93613ea87a177ce6c5a3ea9bfa92b
created: 2026-08-29T17:24:00+02:00
updated: 2026-08-29T17:28:00+02:00
risk: high
execution_class: github_hosted
execution_mode: static_security_validation
execution_reason: repair merged #795 independent audit so it validates reusable current-tree self-hosted invariants instead of hardcoding the historical #795 changed-file set
persistent_session_role: not_applicable
physical_e2e_required: false
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
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: NOT_APPLICABLE
related_pr: 798
validation_level: exact_head
owned_paths:
  - .github/scripts/audit_track_a_selfhosted_pr_boundary.py
  - .github/scripts/test_track_a_selfhosted_pr_boundary_audit_reuse.py
  - .github/workflows/track-a-selfhosted-pr-boundary.yml
  - docs/agents/tasks/active/OTC-20260829-selfhosted-boundary-audit-reuse.md
  - docs/agents/reports/OTC-20260829-selfhosted-boundary-audit-reuse.md
blocks:
  - OTC-20260828-current-login-field6-runtime
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Repair the reusable independent audit merged in #795 after PR #796 proved that its historical changed-path allowlist rejects every legitimate future workflow PR. Keep the actual self-hosted event scanner and canonical main-ref/owner gate unchanged.

# Causal RED

PR #796 exact-head boundary run `33260012616`, independent audit job `99120220924`, failed:

```text
AUDIT-F003: unexpected changed paths: .github/scripts/audit_track_a_current_login_field6_admission.py, ...
```

The sibling `boundary` job passed, proving the self-hosted event predicate itself was safe; only the non-reusable historical diff allowlist failed.

# Repair

`verify_changed_paths` now proves the exact PR diff is readable and non-empty but does not constrain unrelated future paths. The independent audit still separately validates the current scanner with adversarial predicate fixtures, the canonical physical owner/workflow_dispatch/main-ref gate, no-runtime boundary task metadata, and the secret-runner contract. A new regression injects the exact class of future field6 paths that triggered the bug and requires acceptance, while an empty diff remains fail-closed.

# Safety

GitHub-hosted static validation only. No Synology runner, secrets, official client, login or physical action.

# Pre-restack hosted validation

Exact head `8068e30c3c916d64bc0260dc9232b1453a96127a` passed self-hosted boundary run `33260190370` (boundary `99120682887`, fresh independent audit `99120682896`), governance run `33260190375`, and CI run `33260190479` with `CI / Required` job `99120784888`. Protected main remained `ed0b048f72b93613ea87a177ce6c5a3ea9bfa92b`. Final one-commit restack and exact-head rerun remain required before merge.
