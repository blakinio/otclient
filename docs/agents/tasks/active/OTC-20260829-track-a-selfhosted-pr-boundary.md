---
task_id: OTC-20260829-track-a-selfhosted-pr-boundary
status: ready
agent: ChatGPT
session_id: chatgpt-20260829-selfhosted-boundary-v2
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: infrastructure_security
phase: validate
branch: fix/OTC-20260829-track-a-selfhosted-pr-boundary-v2
base_branch: main
base_main: b5c7d0fbb0e9667abe6fea7bbaea8834c1c654b5
created: 2026-08-29T07:35:00+02:00
updated: 2026-08-29T17:12:04+02:00
risk: high
execution_class: github_hosted
execution_mode: static_security_validation
execution_reason: close review-discovered PR/workflow-ref bypasses and define an external clean one-job runner boundary before V4 secret access
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
related_pr: 795
owned_paths:
  - .github/scripts/test_track_a_selfhosted_pr_boundary.py
  - .github/scripts/audit_track_a_selfhosted_pr_boundary.py
  - .github/scripts/test_track_a_selfhosted_pr_review_regressions.py
  - .github/workflows/track-a-selfhosted-pr-boundary.yml
  - .github/workflows/tibia-official-client-re-canonical-live-lease.yml
  - docs/agents/contracts/TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md
  - docs/agents/tasks/active/OTC-20260829-track-a-selfhosted-pr-boundary.md
  - docs/agents/reports/OTC-20260829-selfhosted-pr-boundary-v2.md
  - docs/superpowers/plans/2026-08-29-selfhosted-pr-boundary.md
blocks:
  - OTC-20260828-current-login-field6-runtime
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Supersede stale PR #788 on fresh protected main and close its two P1 plus one P2 review findings before any V4 credential-bearing execution. Repository checking is defense in depth; the primary secret boundary is an offline-by-default, fresh one-job runner defined by `TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md`.

# Fresh continuation facts

- Fresh base at resume: `main@b5c7d0fbb0e9667abe6fea7bbaea8834c1c654b5`.
- PR #788 head `1674cfd8...` is stale/unmergeable and retains three unresolved material review threads.
- GitHub runner API freshly reported `synology-otclient-01` offline, not busy, labels `otclient,synology`. No V4 login has occurred.
- Current field6 task remains `runtime_access:none`, `physical_action_count:0`, `FIELD6_VALUE=UNKNOWN`.

# TDD

The carried-forward #788 checker was first proven locally GREEN against its old incomplete implementation. New review regressions then failed exactly because both mixed event predicates were accepted and the canonical self-hosted dispatch lacked a main-ref requirement. The v2 implementation parses boolean event structure so nested non-event ORs remain legal while any branch that can admit `pull_request` is rejected, and the canonical dispatch now requires owner + workflow_dispatch + `refs/heads/main`.

Focused local GREEN after repair:

```text
TRACK_A_SELFHOSTED_PR_REVIEW_REGRESSION=PASS
TRACK_A_SELFHOSTED_PR_BOUNDARY=PASS
python -m py_compile ... = PASS
git diff --check = PASS
```

No Synology job, official client, credential, login, GUI action, process mutation, or network payload capture was used.
Two optional local-model audit attempts were not accepted as completion evidence: `qwen2.5-coder:14b` produced findings contradicted by the exact source, and `gpt-oss:20b` did not return a usable terminal report before being stopped. Both were treated fail-closed; a deterministic fresh CI validator role is the required independent audit.
The canonical lease/guard unit modules require Linux `fcntl`; local Windows execution stops at import and is not claimed. Their required proof is the exact-head GitHub-hosted workflow.

# Remaining gates

1. Final restacked exact-head hosted boundary/audit, canonical lease, governance and required CI must remain GREEN.
2. Mark PR #795 Ready, inspect central Spark output if any appears before merge, verify zero material review threads, then squash-merge on stable fresh main.
3. Before V4, harden the one-shot workflow with `GITHUB_RUN_ATTEMPT == 1`, merge its admission on trusted main, and provision a clean one-job runner under the new contract.
4. Only then create one new V4 owner trigger.

# Next action

Clean-restack PR #795 to one commit on fresh main, run final exact-head validation, then squash-merge if all gates stay GREEN.
