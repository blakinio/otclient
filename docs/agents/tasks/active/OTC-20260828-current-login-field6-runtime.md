---
task_id: OTC-20260828-current-login-field6-runtime
status: implementing
agent: ChatGPT
session_id: chatgpt-20260829-field6-v4-independent-runner
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: live_admission
branch: fix/OTC-20260829-field6-v4-independent-runner
base_branch: main
base_main: 8c207b38ecad5154a83ec3588e172f096cf2ff29
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-29T19:00:00+02:00
risk: high
execution_class: independent_ephemeral_physical_runtime
execution_mode: github_actions_independent_ephemeral_physical
execution_reason: one fresh exact-current scalar-only V4 login observation on a physically separate one-job clean Linux guest after terminal Synology secret-boundary disqualification
persistent_session_role: none
physical_e2e_required: true
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260828-current-login-field6-runtime
runtime_namespace: field6-runtime-ephemeral-OTC-20260828-v4-display131-port25441
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
live_runtime_authorization_source: PR_758_COMMENT_5457904227
related_pr: 805
independent_guest_name: OTClientV4Clean
independent_runner_name: molehill-otclient-v4-01
independent_rootfs_url: https://cloud-images.ubuntu.com/releases/noble/release-20260801/ubuntu-24.04-server-cloudimg-amd64-root.tar.xz
independent_rootfs_sha256: 915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d
independent_runner_provenance: /etc/otclient-field6-runner-provenance
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: field6 proof remains one sequential evidence chain; Track B is a separate consumer phase after scalar promotion
validation_level: exact_head
last_completed_step: independent-runner consumer RED proven on PR #805; task routing updated and implementation in progress
session_rotation_count: 2
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-28T22:50:00+02:00
last_progress_at: 2026-08-29T19:00:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: v4_independent_runner_implementation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 2
stall_warnings: 0
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
  - docs/superpowers/plans/2026-08-28-field6-materializer-repair.md
  - docs/superpowers/plans/2026-08-28-field6-v4-observation.md
modules_touched:
  - track-a-ephemeral-runtime-research
depends_on:
  - merged PR #752 exact-current field6 scalar-owner promotion
  - merged PR #754 exact-current client fence
  - merged PR #758 runtime observation implementation
  - merged PR #775 bounded exact-current package materialization repair
  - merged PR #783 static V4 generation and historical-rerun guard
  - merged PR #795 self-hosted secret-runner boundary
  - merged PR #798 reusable self-hosted boundary audit
  - merged PR #802 terminal Synology host-probe evidence
  - merged PR #804 independent ephemeral physical runtime contract/routing
  - PR #758 owner V4 admission comment 5457904227
  - host-probe run 33261106292 / job 99123092884 proving Synology Docker-socket RW
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar carried in `edx` when the official Linux Tibia client enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that scalar as the only admissible Track B field6 input.

# Terminal prior-generation evidence

V1, V2 and V3 are consumed historical generations and must never be rerun or replayed. Terminal V3 run `33202129157` / job `98953921602` stopped before authorization consumption, credential exposure, official-client execution or login:

```text
TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=1
TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS
physical_action_count=0
login_submit_count=0
FIELD6_VALUE=UNKNOWN
```

The exact consumed V3 trigger literal is intentionally absent from this active task. Immutable V3 evidence remains under `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/`.

# Trusted V4 implementation and authority

Materializer repair PR #775 is trusted as `5e9293f78e1757eafb88ca0b21cec8bf3d1d246a`. Static generation PR #783 is trusted as `0720ddc77affefc4206afc7e09da03b77dc8c26f`; it rotates the only executable generation to V4 and blocks historical V3 reruns.

A separate repository-owner admission exists on merged PR #758 as comment `5457904227`:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 admission=true previous_generation=V3 previous_run=33202129157 previous_physical_action_count=0 scope=one_login_scalar_only physical_action_budget=1 relogin=false restart=false character_selection=false world_entry=false gameplay=false network_payload_capture=false
```

This is not the live trigger. The exact V4 trigger remains unposted.

# Synology disqualification and independent fallback

Trusted-main host probe run `33261106292`, job `99123092884`, proved the historical `synology-otclient-01` runner was itself inside a container with read/write access to the Synology host Docker socket. PR #802 persisted the sanitized terminal evidence and removed the probe workflow. Therefore neither that historical runner nor a new container on the same unverified Synology host is admissible for Tibia credentials.

Merged PR #804 (`8c207b38ecad5154a83ec3588e172f096cf2ff29`) now defines the trusted `independent_ephemeral_physical_runtime` fallback. This V4 task satisfies its static routing shape: it is task-owned `ephemeral_isolated`, retains `physical_e2e_required: true`, has `persistent_session_role: none`, and does not use canonical registration/Gate A/rebind/Gate B/bootstrap/Kasm retained state.

The only admitted executor is a freshly imported WSL2 Ubuntu 24.04 guest `OTClientV4Clean` on physically separate `Molehill-PC`, built from the immutable Canonical release-20260801 amd64 rootfs and exact SHA256 recorded in task metadata. It must have host automount/interop disabled, no Docker/Podman socket, no prior repository/runner/task state, and root-owned `/etc/otclient-field6-runner-provenance` before GitHub runner registration.

The GitHub runner name is exactly `molehill-otclient-v4-01`. It is configured only after the V4 job queues, with `--ephemeral --disableupdate --no-default-labels` and the one-time label `field6-v4-<comment_id>`. Before registration/start, the coordinator must prove exactly one attempt-1 queued V4 job requires that exact comment-derived label and no other queued job requests it. A generic self-hosted job must never be eligible.

# Consumer TDD

PR #805 exact RED head `ed5321fd8e4bdeb253da10a88c9eda58e816dc3a` changed only the security contract. Hosted run `33264367089`, contract job `99131694221`, failed exactly with:

```text
FIELD6_SECURITY_CONTRACT_RED: task missing 'execution_class: independent_ephemeral_physical_runtime'
```

Fresh independent admission audit also failed as expected on the old Synology admission shape; the physical `One-shot isolated field6 observation` job `99131694774` was skipped. No runtime/credential/client action occurred.

During GREEN implementation, an additional existing causal gate was discovered: `.github/scripts/track_a_current_client_package_acquire.sh` also hard-coded `RUNNER_NAME=synology-otclient-01`. The independent consumer must update that gate under the same provenance flag; overriding/spoofing `RUNNER_NAME` is forbidden.

# Exact client and observer boundary

Before login the trusted workflow must freshly verify:

- version `15.32.75d4a0`;
- unpacked size `52105824`;
- unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- producer entry `0xe25620`;
- authoritative pre-observation scalar `FIELD6_VALUE=UNKNOWN`.

Any current-client fence movement fails closed before authorization consumption, credentials or login. No scalar may be guessed.

GDB remains the client parent, never attach. ASLR remains enabled; the child PIE is resolved after `exec`; the only retained process value is `uint32(edx)` at `PIE + 0xe25620`. Stack bytes, packet payloads, credentials, process environment, unrelated registers and arbitrary/raw process memory may not be retained.

# Credential and mutation boundary

The credential wrapper remains the only path receiving `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`; it removes their export attribute and the helper sends both strings to `xdotool type --file -` through stdin, never argv.

V4 grants exactly one logical account-login form submission after independent guest provenance, trusted-main, exact package and run-attempt gates pass. It grants no relog, restart, character selection/activation, world entry or gameplay. Network payload capture is forbidden.

Successful sanitized evidence must prove:

```text
TRACK_A_FIELD6_RUNTIME_CAPTURED=true
FIELD6_VALUE=<uint32>
FIELD6_VALUE_PROVEN=true
login_submit_count=1
character_selection_performed=false
world_entry_performed=false
gameplay_performed=false
network_payload_capture_performed=false
credentials_retained=false
packet_payloads_retained=false
process_environment_retained=false
raw_memory_retained=false
```

# V4 trigger and cleanup

Only after PR #805 is independently audited, exact-head GREEN, clean-restacked and merged, and the fresh guest passes pre-registration provenance may one new top-level owner comment be created on merged PR #758 with body exactly:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```

That comment ID becomes the one-time runner label. `GITHUB_RUN_ATTEMPT != 1` fails before authorization/secret/client/physical action. After the one job terminates, the ephemeral runner must deregister/exit and `OTClientV4Clean` must be destroyed. If the login submit occurred but scalar proof failed, an identical V4 retry is forbidden.

# Completion

`FIELD6_VALUE=UNKNOWN` and `physical_action_count=0` remain authoritative. After one terminal V4 run, a separate repository-only evidence PR must return this task to `runtime_access: none`, disarm credential/login/mutation authority, record the actual action count, archive the trigger as consumed, and promote only sanitized scalar/provenance evidence. Track B may consume field6 only after that promotion reaches trusted `main`.

# Next action

Finish the #805 GREEN implementation for dynamic one-time runner routing, root-owned provenance, independent package-acquisition runner gate and V4-only system toolroot. Require field6 security/runtime/fresh audit, materializer, Track A governance, reusable self-hosted boundary and `CI / Required` GREEN; clean-restack and merge before any V4 trigger or runner registration.