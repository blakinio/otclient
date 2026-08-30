---
task_id: OTC-20260828-current-login-field6-runtime
status: implementing
agent: ChatGPT
session_id: chatgpt-20260830-field6-v6-generation
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: validate
branch: fix/OTC-20260830-field6-v6-generation
base_branch: main
base_main: d1ce0ad811cf6a4a5a3466f7e5af045f39acab31
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-30T16:08:11+02:00
risk: high
execution_class: github_hosted
execution_mode: github_actions_static
execution_reason: repository-only V6 generation rotation after terminal pre-action V5 provenance-readability failure; no runner registration, credential access, client execution, login or physical mutation is authorized in this phase
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
decomposition_reason: revoke terminal V5 statically first; a fresh V6 guest and physical routing/admission require a separate trusted-main phase
validation_level: focused
last_completed_step: PR #815 candidate b28599af6f73d024d4d56fcb6486199ca1cb8a07 passed exact-head runtime/static audit/package/governance/self-hosted boundary/CI; physical job 99269338963 skipped
session_rotation_count: 6
heavy_validation_runs: 1
stale_takeover_count: 0
human_interruptions: 1
invocation_started_at: 2026-08-30T11:05:00+02:00
last_progress_at: 2026-08-30T16:08:11+02:00
ci_checks_for_current_head: 5
ci_check_generation: field6_v6_static_green
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 5
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
related_pr: 815
owned_paths:
  - .github/scripts/test_track_a_current_login_field6_runtime.py
  - .github/scripts/test_track_a_current_login_field6_security_contract.py
  - .github/scripts/audit_track_a_current_login_field6_admission.py
  - .github/scripts/track_a_current_client_package_materialize.py
  - .github/scripts/track_a_current_client_package_seed.py
  - .github/scripts/track_a_current_client_package_acquire.sh
  - .github/scripts/track_a_current_login_field6_runtime.sh
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
  - .github/workflows/track-a-current-login-field6-runtime.yml
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**
  - docs/superpowers/plans/2026-08-30-field6-v6-generation.md
modules_touched:
  - track-a-ephemeral-runtime-research
depends_on:
  - merged PR #752 exact-current field6 scalar-owner promotion
  - merged PR #754 exact-current client fence
  - merged PR #758 runtime observation implementation
  - merged PR #811 serialized acquisition repair
  - merged PR #812 static V5 generation
  - merged PR #814 exact official-launcher seed importer
  - merged PR #813 V5 independent seed runner admission at d1ce0ad811cf6a4a5a3466f7e5af045f39acab31
  - terminal V5 run 33314713078 / job 99265883209 with physical_action_count=0
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar carried in `edx` when official native Linux Tibia client `15.32.75d4a0` enters the proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote only that scalar as the admissible Track B field6 input.

This phase is repository-only generation rotation. It revokes terminal V5 and creates no live V6 authority.

# Exact client fence

```yaml
version: 15.32.75d4a0
size: 52105824
sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
packed_bin_client_sha256: 075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
producer_entry: 0xe25620
FIELD6_VALUE: UNKNOWN
```

# Terminal V5 fact

V5 trigger comment `5469017445` created run `33314713078`, attempt 1, job `99265883209`. Queue uniqueness and runner identity were proven. The first live step then failed before checkout because root-owned provenance mode `0600` was not readable by the unprivileged runner account.

Trusted-main checkout, package preflight, owner-authorization consumption, secret-bearing capture, scalar validation and upload were all skipped. Authoritative terminal state remains `physical_action_count: 0`, `login_submit_count: 0`, `FIELD6_VALUE: UNKNOWN`, authorization unconsumed, credentials not exposed to capture, official client not started.

The ephemeral runner removed its runner credentials/config and deregistered. Exact WSL ownership readback then proved and destroyed only `OTClientV5Clean`. Durable sanitized evidence is `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/20260830-v5-terminal-pre-action-provenance-readability.md`.

The exact consumed V5 trigger body is deliberately omitted from this active task so historical UI reruns cannot satisfy current trusted-main admission.

# Static V6 generation

The current future generation identifier is exactly:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V6 once=true
```

This is only a repository generation identifier. It has not been posted as an owner trigger and this task grants it no live authority.

Current task must remain static-safe:

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

The workflow current-generation condition and trusted-main task check rotate to V6. Existing `field6-v5-*`, `molehill-otclient-v5-01`, `OTClientV5Clean` and seed/provenance executable boundaries remain unchanged but inert while this task is `runtime_access: none`; they are not reusable and will be rotated only in a separate V6 physical routing/admission PR after a brand-new guest is proven.

# TDD evidence

RED head `12ed31a58ddc9e33dc546f577aba41ef3117ba24` produced hosted run `33315765050`. Runtime contract job `99268806498` failed exactly because workflow lacked the current V6 generation literal. Physical job `99268807332` was SKIPPED. No runner, secret, client or physical action was used by the RED generation.

# V6 static exact-head GREEN checkpoint

Candidate head `b28599af6f73d024d4d56fcb6486199ca1cb8a07` passed:

- field6 run `33315959590`: runtime job `99269338212` SUCCESS, fresh static audit `99269338409` SUCCESS, physical job `99269338963` SKIPPED;
- package run `33315959597`, job `99269338316` SUCCESS;
- governance run `33315959585`: jobs `99269338228` and `99269338281` SUCCESS;
- self-hosted boundary run `33315959570`: jobs `99269338200` and `99269338225` SUCCESS;
- CI run `33315959686`: syntax/actionlint job `99269366267` SUCCESS and `CI / Required` job `99269435334` SUCCESS.

No V6 trigger, runner registration, credential exposure, client execution, login or physical action occurred.

# Successor host rule

After static V6 merge, create a brand-new `OTClientV6Clean` from the same pinned Canonical rootfs. The V6 provenance record must be root-owned, not writable by runner, **and readable by runner**: mode `0644`. The official-launcher seed is copied fresh and independently reverified. No V6 trigger may be posted until a separate V6 routing/admission change is merged to trusted main and exact queue uniqueness is proven.

# Next action

Require exact-head static runtime/security/audit/package/governance/self-hosted-boundary/CI GREEN with physical job SKIPPED, record evidence, merge with expected-head guard, then proceed to fresh V6 guest preparation and separate V6 routing/admission.
