---
task_id: OTC-20260828-current-login-field6-runtime
status: implementing
agent: ChatGPT
session_id: chatgpt-20260830-field6-v5-generation
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: validate
branch: fix/OTC-20260830-field6-v5-generation
base_branch: main
base_main: dad71238d3da48ad9cf0bdcb45f9d0a445131f8c
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-30T12:05:00+02:00
risk: high
execution_class: github_hosted
execution_mode: github_actions_static
execution_reason: repository-only V5 generation rotation after terminal pre-action V4 and merged package repair; no live client, credentials, runner registration, login, or physical mutation are authorized in this phase
persistent_session_role: none
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
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: rotate the current generation statically first; independent V5 guest/runner routing and one-login admission require a separate trusted-main phase after a brand-new guest is physically proven
validation_level: focused
last_completed_step: V5 TDD RED run 33305488409 contract job 99241188716 failed exactly on missing current V5 generation while physical live job 99241189199 was skipped
session_rotation_count: 4
heavy_validation_runs: 1
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-30T11:05:00+02:00
last_progress_at: 2026-08-30T12:05:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: field6_v5_static_green
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
related_pr: 812
owned_paths:
  - .github/scripts/test_track_a_current_client_package_parallel.py
  - .github/scripts/test_track_a_current_login_field6_runtime.py
  - .github/scripts/test_track_a_current_login_field6_security_contract.py
  - .github/scripts/audit_track_a_current_login_field6_admission.py
  - .github/scripts/track_a_current_client_package_materialize.py
  - .github/scripts/track_a_current_client_package_acquire.sh
  - .github/scripts/track_a_current_login_field6_runtime.sh
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
  - .github/workflows/track-a-current-client-package-materializer.yml
  - .github/workflows/track-a-current-login-field6-runtime.yml
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/reports/OTC-20260829-field6-v4-admission-v2.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**
  - docs/superpowers/plans/2026-08-30-field6-v5-generation.md
modules_touched:
  - track-a-ephemeral-runtime-research
depends_on:
  - merged PR #752 exact-current field6 scalar-owner promotion
  - merged PR #754 exact-current client fence
  - merged PR #758 runtime observation implementation
  - merged PR #775 bounded exact-current package materialization repair
  - merged PR #783 V4 generation and historical-rerun guard
  - merged PR #795 self-hosted secret-runner boundary
  - merged PR #798 reusable self-hosted boundary audit
  - merged PR #802 terminal Synology host-probe evidence
  - merged PR #804 independent ephemeral physical runtime contract/routing
  - merged PR #806 independent V4 consumer
  - merged PR #807 independent host wait gate
  - merged PR #811 serial field6 package acquisition repair at dad71238d3da48ad9cf0bdcb45f9d0a445131f8c
  - PR #758 V4 owner admission comment 5457904227
  - PR #758 consumed V4 generation comment 5467500633
  - terminal V4 run 33300352335 / job 99227195253
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar carried in `edx` when the official native Linux Tibia client enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that scalar as the only admissible Track B field6 input.

This phase only rotates the repository's current generation from consumed terminal V4 to static V5. It does not create a V5 guest, runner, owner trigger, live admission, credential path, client execution, or login authority.

# Exact client fence

```yaml
version: 15.32.75d4a0
size: 52105824
sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
packed_bin_client_sha256: 075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
producer_entry: 0xe25620
FIELD6_VALUE: UNKNOWN
```

No scalar may be guessed or promoted without a later separately admitted physical observation.

# Terminal V4 facts

PR #758 owner admission comment `5457904227` authorized the historical V4 generation. The distinct generation comment was `5467500633`; its exact consumed body is deliberately omitted from this active task so a historical workflow rerun cannot satisfy current trusted-main admission.

That generation created run `33300352335`, attempt 1, job `99227195253` on `molehill-otclient-v4-01`. Independent provenance and trusted-main gates passed, task-owned WARP passed, then exact-current package materialization failed pre-action with `FETCH_FAILED:curl_22`.

The later authorization, secret injection, official-client execution, login submit, scalar validation and evidence upload steps were skipped. Cleanup passed. Authoritative terminal state remains:

```yaml
physical_action_count: 0
login_submit_count: 0
FIELD6_VALUE: UNKNOWN
owner_authorization_consumed: false
credentials_injected: false
official_client_started: false
```

Historical V3 and V4 generation triggers are consumed and must not be executable or reproduced as current task literals. Workflow reruns other than attempt 1 remain forbidden.

# Merged package repair

PR #811 merged to trusted `main` as `dad71238d3da48ad9cf0bdcb45f9d0a445131f8c`.

Verified trusted-main invariants:

- production `FILE_WORKERS='1'`;
- materializer `DEFAULT_FILE_WORKERS=1` and `MAX_FILE_WORKERS=16`;
- exact packed/unpacked size and SHA checks remain intact;
- downloaded package content is not executed during preflight;
- task-owned WARP/SOCKS and cleanup boundaries remain intact;
- live-observation timeout is bounded at 45 minutes.

The exact CDN policy behind current HTTP 403 behavior remains UNKNOWN. The repository evidence supports only the medium-high-confidence inference that eight-way payload concurrency materially worsened edge throttling compared with V3 serial transfer.

# Static V5 generation

The current future generation identifier is:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true
```

This text is a repository generation identifier only. It has not been posted as an owner trigger and this task grants it no live authority.

Current phase must stay exactly static-safe:

```yaml
execution_class: github_hosted
execution_mode: github_actions_static
physical_e2e_required: false
runtime_access: none
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
physical_action_budget: 0
physical_action_count: 0
```

The workflow generation condition and trusted-main task check rotate to V5, but the existing `field6-v4-*`, `molehill-otclient-v4-01`, `OTClientV4Clean`, provenance schema, helper and acquisition allowlists remain intentionally unchanged and inert in this generation-only PR. They cannot become usable while this task is `runtime_access: none`; rotating those physical boundaries is a separate future V5 routing/admission change.

# TDD evidence

## FACT — RED

Draft PR #812 RED head `8c262e0d509af1927380cf36b9179ee9950c507d` created field6 workflow run `33305488409`.

- contract job `99241188716`: FAILURE exactly because the workflow lacked current V5 generation text;
- fresh static audit job `99241188630`: FAILURE through the same current-generation contract;
- physical `One-shot isolated field6 observation` job `99241189199`: SKIPPED.

Exact causal failure:

```text
FIELD6_RUNTIME_CONTRACT_RED: .github/workflows/track-a-current-login-field6-runtime.yml missing ['AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true']
```

No self-hosted runner, secret, official client, login or physical action was used by the RED generation.

## GREEN candidate

The minimal GREEN candidate changes only the two executable current-generation checks in `.github/workflows/track-a-current-login-field6-runtime.yml`, updates this static task to V5, and retains the RED contract. No physical routing or runtime helper is changed.

Exact-head GREEN run/job IDs must be recorded only after GitHub reports them terminally.

# Independent host boundary

`Molehill-PC` is currently offline from the authorized Remote Desktop channel; last observed `last_seen` was `2026-08-30T09:28:21.845+00:00`. No live action is legal while it is unavailable and Synology remains disqualified for this secret-bearing task.

The existing `OTClientV4Clean` guest was used for public diagnostics after terminal V4 and is therefore tainted for any future secret-bearing generation. When Molehill returns, only that exact owned guest may be terminated/unregistered, and the successor must be a brand-new guest imported from the pinned Canonical rootfs and must re-prove automount, interop, Docker/Podman socket, prior-repo and prior-runner isolation before any separate live admission can be considered.

# Successor routing/admission gate

Static V5 merge does not authorize a physical V5 observation. After this generation is on trusted `main`:

1. if Molehill remains offline, stop at the external host gate;
2. if Molehill returns, remove the tainted exact V4 guest only after ownership proof and create a fresh independent successor guest;
3. create a separate TDD-reviewed V5 routing/admission change that rotates the one-time label, runner/guest identifiers, helper/acquisition allowlists and admission/security expectations;
4. merge that change to trusted `main` and prove exact queued-job uniqueness before posting any V5 owner trigger;
5. allow at most one login scalar observation; identical physical replay remains forbidden if it submits login without proving the scalar.

Track B PR #284 remains blocked until a later sanitized evidence-promotion PR proves and merges one exact `FIELD6_VALUE=<uint32>` from the exact current official client.

# Next action

Require PR #812 exact-head runtime/static-audit/package/governance/self-hosted-boundary/CI checks to become GREEN with the physical live job SKIPPED. Then update the V5 plan with exact RED/GREEN evidence, perform fresh diff/review/main readback, obtain a non-draft mergeable PR without changing verified code, and squash-merge with an exact-head guard. After trusted-main readback, stop at the independent-host gate unless a brand-new successor guest can be directly proven.
