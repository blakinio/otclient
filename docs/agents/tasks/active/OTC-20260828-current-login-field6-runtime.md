---
task_id: OTC-20260828-current-login-field6-runtime
status: validating
agent: ChatGPT
session_id: chatgpt-20260830-field6-v5-independent-runner
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: live_admission
branch: fix/OTC-20260830-field6-v5-independent-runner
base_branch: main
base_main: 0b5e473aed4e61f05fc28005f1c0ec9cd99cbf61
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-30T15:05:00+02:00
risk: high
execution_class: independent_ephemeral_physical_runtime
execution_mode: github_actions_independent_ephemeral_physical
execution_reason: one fresh exact-current scalar-only V5 login observation on a brand-new one-job isolated WSL2 guest using a root-owned exact official-launcher package seed after terminal V4 pre-action acquisition failure
persistent_session_role: none
physical_e2e_required: true
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260828-current-login-field6-runtime
runtime_namespace: field6-runtime-ephemeral-OTC-20260828-v5-display131-seed
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
credentials_allowed: true
login_allowed: true
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: true
process_control_authorized: true
network_payload_capture_allowed: false
physical_action_budget: 1
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: PR_758_COMMENT_5468621219
related_pr: 813
independent_guest_name: OTClientV5Clean
independent_runner_name: molehill-otclient-v5-01
independent_rootfs_url: https://cloud-images.ubuntu.com/releases/noble/release-20260801/ubuntu-24.04-server-cloudimg-amd64-root.tar.xz
independent_rootfs_sha256: 915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d
independent_runner_provenance: /etc/otclient-field6-runner-provenance
independent_runner_provenance_schema: otclient.track-a.independent-field6-runner.v2
independent_seed_path: /opt/otclient-v5-seed/seed.tar.gz
independent_seed_size: 412272538
independent_seed_sha256: 64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: V5 routing/admission and one-shot field6 proof are sequential; scalar promotion and Track B remain separate only after sanitized proof
validation_level: exact_head
last_completed_step: Draft PR #813 RED run 33311073185 failed on missing V5 physical boundary while live job 99256101894 was skipped; seed importer PR #814 then merged to main as 0b5e473aed4e61f05fc28005f1c0ec9cd99cbf61 and real seed integration passed 8732/8732
session_rotation_count: 5
heavy_validation_runs: 1
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-30T11:05:00+02:00
last_progress_at: 2026-08-30T15:05:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: field6_v5_independent_seed_green
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
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
  - docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V2.md
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**
  - docs/superpowers/plans/2026-08-30-field6-v5-independent-runner.md
modules_touched:
  - track-a-ephemeral-runtime-research
depends_on:
  - merged PR #752 exact-current field6 scalar-owner promotion
  - merged PR #754 exact-current client fence
  - merged PR #758 runtime observation implementation
  - merged PR #804 independent ephemeral physical runtime contract/routing
  - merged PR #811 serialized acquisition repair
  - merged PR #812 static V5 generation
  - merged PR #814 exact official-launcher seed importer at 0b5e473aed4e61f05fc28005f1c0ec9cd99cbf61
  - PR #758 V5 owner admission comment 5468621219
  - terminal V4 run 33300352335 / job 99227195253 with physical_action_count=0
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar carried in `edx` when the exact official native Linux Tibia client enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote only that scalar as the Track B field6 input.

Exact client fence remains `15.32.75d4a0`, size `52105824`, SHA256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`. `FIELD6_VALUE=UNKNOWN` until the admitted physical observation proves a uint32 value.

# Prior-generation terminal fact

V4 run `33300352335`, attempt 1, job `99227195253` passed clean-runner/trusted-main/WARP gates and failed before owner authorization, secret exposure, client execution or login. Therefore `physical_action_count=0`, `login_submit_count=0`, and `FIELD6_VALUE=UNKNOWN`. Historical V3/V4 executable trigger literals must remain revoked.

# V5 owner admission

PR #758 comment `5468621219` is the separate owner admission for this generation. It grants at most one login scalar observation, no relogin, no restart, no character selection, no world entry, no gameplay and no network payload capture.

The exact V5 trigger remains unposted. The executable trigger is `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true`, but it becomes usable only after this routing/admission change is merged to trusted main.

The exact queued trigger comment ID becomes the one-time runner label. The scheduling form is the one-time label `field6-v5-<comment_id>`. That comment ID becomes the one-time runner label. Before registration, exactly one attempt-1 queued job must request it and no other job may request it.

If the one allowed login submit occurs without scalar proof, an identical V5 retry is forbidden.

# Fresh independent host proof

The only admitted guest is `OTClientV5Clean` on owner-controlled Molehill-PC and runner `molehill-otclient-v5-01`. It was imported fresh from the pinned Canonical rootfs after the tainted V4 guest was removed by exact WSL ownership/BasePath proof.

Direct pre-registration readback proved automount and Windows interop disabled, no `/mnt/c`, no host drive mounts, no Docker or Podman sockets, no prior repository checkout, no runner credentials, no runner `_work`, required system toolroot installed, and GitHub Actions runner `2.337.0` archive SHA256 `70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613`.

# Exact official-launcher seed

Merged PR #814 provides the fail-closed official-launcher seed importer. Proprietary seed bytes remain local. The root-owned guest path is `/opt/otclient-v5-seed/seed.tar.gz`, size `412272538`, SHA256 `64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016`.

A pre-registration production-importer probe on the real archive verified `8732/8732` regular files, exact package/assets manifests and the exact `bin/client` fence, then its extracted probe output was deleted. Only the immutable root-owned mode-0400 seed remains. V5 package acquisition must use this official-launcher seed and must not use the known-unreliable custom direct payload curl path.

# Live boundary after merge

The provenance record is `/etc/otclient-field6-runner-provenance` with schema `otclient.track-a.independent-field6-runner.v2`. It must bind the exact guest, rootfs, runner, trigger-derived label, generation nonce and exact seed path/size/SHA, plus all isolation booleans true. The workflow independently re-hashes the seed before checkout, authorization consumption or secret exposure.

Runner registration is allowed only after queue uniqueness proof and uses `--ephemeral --disableupdate --no-default-labels --labels field6-v5-<comment_id>`. The runner accepts at most one job. After every terminal outcome the entire V5 guest, runner state and local seed are destroyed.

# Next action

Make #813 exact-head hosted runtime/security/admission/materializer/governance/self-hosted-boundary/CI checks GREEN with the physical live job SKIPPED, merge with expected-head guard, then post exactly one V5 trigger, prove queue uniqueness, create root-owned schema-v2 provenance, register/start the one-job runner and evaluate the sanitized scalar-only result. Track B remains blocked until a proven scalar is separately promoted to trusted main.
