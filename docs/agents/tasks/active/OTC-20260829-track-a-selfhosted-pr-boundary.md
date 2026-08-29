---
task_id: OTC-20260829-track-a-selfhosted-pr-boundary
status: validating
agent: ChatGPT
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: infrastructure_security
phase: validate
branch: fix/OTC-20260829-track-a-selfhosted-pr-boundary
base_branch: main
base_main: 4c751870b5dcd51d5b984b78a4f06625306be961
created: 2026-08-29T07:35:00+02:00
updated: 2026-08-29T07:47:00+02:00
risk: high
execution_class: github_hosted
execution_mode: static_security_validation
execution_reason: eliminate PR-controlled execution on the credential-bearing Synology runner before any V4 secret access
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
related_pr: 788
owned_paths:
  - .github/scripts/test_track_a_selfhosted_pr_boundary.py
  - .github/workflows/track-a-selfhosted-pr-boundary.yml
  - .github/workflows/tibia-official-client-re-canonical-live-lease.yml
  - docs/agents/tasks/active/OTC-20260829-track-a-selfhosted-pr-boundary.md
  - docs/agents/reports/OTC-20260829-selfhosted-pr-boundary-red.md
  - docs/superpowers/plans/2026-08-29-selfhosted-pr-boundary.md
blocks:
  - OTC-20260828-current-login-field6-runtime
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Remove every trusted-main workflow path that allows `pull_request`-controlled code to execute on the shared Synology self-hosted runner before any credential-bearing V4 field6 run.

# TDD evidence

The initial hosted scan exposed a parser false-positive because payload references such as `github.event.issue.pull_request` were confused with a PR event. After correcting that distinction, the causal RED was exact:

```text
run=33236883246
job=99059301992
TRACK_A_SELFHOSTED_PR_BOUNDARY_RED: PR-controlled self-hosted jobs: .github/workflows/tibia-official-client-re-canonical-live-lease.yml::isolated-selfhosted
```

No Synology job was run by the RED. The only real unsafe trusted-main path was the canonical lease self-hosted test.

GREEN gates that job to:

```yaml
if: github.event_name == 'workflow_dispatch' && github.actor == github.repository_owner
runs-on: [otclient, synology]
```

and changes its checkout to the exact trusted `main` with credentials persistence disabled. Pull-request validation remains GitHub-hosted.

Exact GREEN evidence on implementation head `4a6a792f1bc2682819db08d64c24665039774b90`:

```text
Track A self-hosted PR boundary       run 33236911255  success
Track A canonical live controller     run 33236911337  success
  isolated-selfhosted                                     skipped
Track A agent runtime governance      run 33236911266  success
CI / Required                         run 33236911425  success
```

No official client, credentials, login, GUI action, process control, or network payload capture occurred.

# Completion boundary

This PR prevents **future** PR-controlled code from entering the shared Synology runner through trusted main. It does not by itself prove the runner is free of residue from historical PR jobs. After independent review and merge, the field6 task still requires a separate no-secret clean-runner attestation/remediation step before any V4 credential exposure.
