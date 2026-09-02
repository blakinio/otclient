---
task_id: OTC-20260828-canonical-client-fence-reconciliation
status: live_admission_pending_central_fence_reconciliation
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: live_admission
branch: fix/OTC-20260902-canonical-reconcile-auth
base_branch: main
base_main: 1744b804745ab6ff0f805df908c855a97c23ca84
created: 2026-08-28T22:00:00+02:00
risk: high
execution_class: self_hosted
execution_mode: github_actions_metadata_reconciliation
runtime_access: canonical_recovery
runtime_owner_task: OTC-20260828-canonical-client-fence-reconciliation
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
recovery_mode: client_fence_reconciliation_v1
client_fence_reconciliation_contract: TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1
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
  - .github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md
  - docs/agents/decisions/ADR-0002-track-a-canonical-client-fence-reconciliation.md
  - docs/agents/evidence/OTC-20260828-canonical-client-fence-reconciliation/**
  - docs/agents/tasks/active/OTC-20260828-canonical-client-fence-reconciliation.md
modules_touched:
  - track-a-canonical-live-runtime
  - track-a-runtime-agent-admission
reuses:
  - merged canonical lease guard-run supervisor
  - merged current Kasm existing-runtime adoption probe
  - PR #754 trusted exact-current client fence
  - PR #760 gameWindowState preflight blocker evidence
  - PR #763 merged client-fence reconciliation implementation
  - PR #776 exact-current identity reconciliation support
  - PR #777 prior exact-current reconciliation admission
  - PR #778 prior reconciliation PASS closeout
  - PR #779 retry reconciliation admission
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

# 2026-09-02 central-fence re-admission

Trusted `main@1744b804745ab6ff0f805df908c855a97c23ca84` now carries the canonical current-client fence promoted by PR #862. Owner-triggered reconciliation run `33681608695` failed closed in deterministic pre-runtime verification before lease acquisition or runtime mutation because the live job checked out with `persist-credentials: false` and then attempted `git ls-remote origin` after checkout removed its auth header.

This checkpoint reopens exactly the existing `canonical_recovery` metadata-only admission and changes only the live reconciliation checkout credential lifetime needed by the already-existing live-main movement guards. It does not authorize client mutation, login, GUI input, process memory, payload capture or semantic promotion.

Keep the canonical exact-current official-client registration synchronized with the unique live exact-fenced client through a bounded metadata-only reconciliation, without granting gameWindowState process-memory or owner-UI authority.

# Retry trigger and result

Fresh owner trigger comment `5457630365` on merged PR #760 created trusted-main workflow run `33210019599`, job `98980682859`, on `synology-otclient-01` at exact `main@fd7a47308581dceda6fd6aa3613f0614a816d150`.

The run passed deterministic pre-runtime verification and selected `RECONCILE_CURRENT_IDENTITY`. It acquired canonical lease generation `43` against registration generation `42`, passed three independent guarded exact-current runtime probes, proved target uniqueness, committed only refreshed runtime identity metadata under the canonical guard, verified the exact current fence with `state: UNKNOWN`, and explicitly released the lease.

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PENDING_ADMISSION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PRERUNTIME=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_DECISION=RECONCILE_CURRENT_IDENTITY
TRACK_A_CANONICAL_LEASE_GENERATION=43
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_GATE_A=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS  # three guarded probes
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CANONICAL_LEASE_GENERATION=43
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_LEASE_GENERATION=42
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_TARGET_UNIQUENESS=PROVEN
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_MUTATION_AUTHORIZED=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_STATE=UNKNOWN
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CLIENT_PROCESS_MUTATION=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PROCESS_MEMORY_OBSERVATION=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_SEMANTIC_PROMOTION=false
TRACK_A_CANONICAL_LEASE_GUARD_COMMAND_RC=0
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_RELEASE=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_CURRENT=PASS
```

The final registration remained exact-fenced to version `15.32.75d4a0`, size `52105824`, SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, with semantic state `UNKNOWN`.

No client process mutation, process-memory observation, GUI/input, login, credentials, character selection, gameplay, packet/payload capture or semantic promotion occurred.

Durable evidence: `docs/agents/evidence/OTC-20260828-canonical-client-fence-reconciliation/20260828-current-identity-reconciliation-retry-pass.md`.

The current frontmatter above intentionally reopens only `canonical_recovery` for one fresh metadata-only reconciliation of the newly promoted canonical client fence.

next_action: after exact-head GREEN and merge, issue one new `RECONCILE_CANONICAL_CLIENT_FENCE` owner trigger, verify the metadata-only transaction and explicit lease release, then close runtime authority back to `none` before the fresh Surveyor admission.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T20:58:00Z
head: a86aa01212ab127bbf1faea8c280cacdc42a5ab6
branch: fix/OTC-20260902-canonical-reconcile-auth
pr: 863
status: validating
context_routes:
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - docs/agents/tasks/active/OTC-20260828-canonical-client-fence-reconciliation.md
owned_paths:
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - docs/agents/tasks/active/OTC-20260828-canonical-client-fence-reconciliation.md
proven:
  - owner-triggered run 33681608695 failed in deterministic pre-runtime verification before decision, lease acquisition or runtime mutation
  - job 100419250234 failed because checkout removed auth and git ls-remote origin could not read GitHub credentials
  - prior successful admission at fd7a47308581dceda6fd6aa3613f0614a816d150 used this task with canonical_recovery fields now restored
  - new workflow-auth regression failed before the one-line checkout fix and passes after it
  - canonical reconciliation unit contract passes 18 of 18 on Linux
  - runtime mutation, process memory observation and semantic promotion remain unauthorized
  - scoped Ruff I/F and git diff check pass`r`n  - native-LF exact implementation head 8ea990c74b41256eeeeaa028062cd6fcd873672e passed reconciliation 18/18, transition 58/58, adoption 10/10, current-fence 11/11, runtime governance, canonical fence guard, checkpoint validation and YAML parse
derived:
  - retaining checkout credentials only for the live reconciliation job is the minimal repair for the existing live-main movement guards
unknown:
  - native-LF exact-commit transition and adoption regression has not yet been rerun for this repair
  - exact-head GitHub Actions and PR classification are pending on the post-checkpoint final head
conflicts:
  - none
first_failure:
  marker: live-main guard could not authenticate git ls-remote after persist-credentials false checkout
  evidence: GitHub Actions run 33681608695 job 100419250234
rejected_hypotheses:
  - runtime registration or client-fence mismatch caused run 33681608695: rejected because failure occurred before registration decision step
  - widen reconciliation architecture: rejected because the failing gate is checkout authentication only
changed_paths:
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - docs/agents/tasks/active/OTC-20260828-canonical-client-fence-reconciliation.md
validation:
  - command: Linux targeted workflow-auth regression RED then GREEN
    result: PASS
    evidence: assertion first failed on persist-credentials false then passed after the one-line live checkout change
  - command: Linux canonical client-fence reconciliation contract
    result: PASS
    evidence: 18 tests passed
  - command: scoped Ruff I/F and git diff --check
    result: PASS
    evidence: both returned zero
  - command: Windows-worktree WSL transition suite
    result: BLOCKED
    evidence: known CRLF shebang artifact env bash CR prevented real transition execution; native-LF rerun is next
blockers:
  - none
next_action: push this PR-bound checkpoint commit, require terminal exact-head GitHub Actions for PR 863, then Ready and merge only if review hygiene and scope remain clean
```
# Historical release boundary

The prior successful retry closeout returned recovery authority to repository-only mode:

```text
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
recovery_mode: NOT_APPLICABLE
```
