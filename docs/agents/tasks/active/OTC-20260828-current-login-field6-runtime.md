---
task_id: OTC-20260828-current-login-field6-runtime
status: ready
agent: ChatGPT
session_id: chatgpt-20260830-field6-official-launcher-seed
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: implement
branch: fix/OTC-20260830-field6-official-launcher-seed
base_branch: main
base_main: 18ff83053f5c5d85c9bce6debab0f7fef6b79ecd
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-30T10:49:00+02:00
risk: high
execution_class: independent_ephemeral_physical_runtime
execution_mode: repository_only_seed_repair
execution_reason: V4 terminated before authorization because direct curl package acquisition is Cloudflare-challenged; repair now consumes a hash-pinned package produced by the existing official Linux launcher
persistent_session_role: none
physical_e2e_required: true
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
physical_action_budget: 1
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: NOT_APPLICABLE_V4_TERMINAL_PRE_AUTH
related_pr: 806
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
last_completed_step: V4 run 33300352335/job 99227195253 terminated pre-authorization on Cloudflare-challenged custom package fetch; official launcher exact package seed frozen and causal RED test recorded
session_rotation_count: 3
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-30T09:38:00+02:00
last_progress_at: 2026-08-30T10:49:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: official_launcher_seed_repair_red
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 2
stall_warnings: 0
owned_paths:
  - .github/scripts/test_track_a_current_client_package_parallel.py
  - .github/scripts/test_track_a_current_client_package_seed.py
  - docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md
  - docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE_ALIAS.md
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

This is not the live trigger. The V4 trigger was posted once as comment `5467500633`; run `33300352335` / job `99227195253` terminated before authorization consumption and the V4 generation is terminal. It must never be reposted or rerun.

# Synology disqualification and independent fallback

Trusted-main host probe run `33261106292`, job `99123092884`, proved the historical `synology-otclient-01` runner was itself inside a container with read/write access to the Synology host Docker socket. PR #802 persisted the sanitized terminal evidence and removed the probe workflow. Therefore neither that historical runner nor a new container on the same unverified Synology host is admissible for Tibia credentials.

Merged PR #804 (`8c207b38ecad5154a83ec3588e172f096cf2ff29`) now defines the trusted `independent_ephemeral_physical_runtime` fallback. This V4 task satisfies its static routing shape: it is task-owned `ephemeral_isolated`, retains `physical_e2e_required: true`, has `persistent_session_role: none`, and does not use canonical registration/Gate A/rebind/Gate B/bootstrap/Kasm retained state.

The only admitted executor is a freshly imported WSL2 Ubuntu 24.04 guest `OTClientV4Clean` on physically separate `Molehill-PC`, built from the immutable Canonical release-20260801 amd64 rootfs and exact SHA256 recorded in task metadata. It must have host automount/interop disabled, no Docker/Podman socket, no prior repository/runner/task state, and root-owned `/etc/otclient-field6-runner-provenance` before GitHub runner registration.

The GitHub runner name is exactly `molehill-otclient-v4-01`. It is configured only after the V4 job queues, with `--ephemeral --disableupdate --no-default-labels` and the one-time label `field6-v4-<comment_id>`. Before registration/start, the coordinator must prove exactly one attempt-1 queued V4 job requires that exact comment-derived label and no other queued job requests it. A generic self-hosted job must never be eligible.

# Consumer TDD and GREEN

PR #805 exact RED head `ed5321fd8e4bdeb253da10a88c9eda58e816dc3a` changed only the security contract. Hosted run `33264367089`, contract job `99131694221`, failed exactly with:

```text
FIELD6_SECURITY_CONTRACT_RED: task missing 'execution_class: independent_ephemeral_physical_runtime'
```

Fresh independent admission audit also failed as expected on the old Synology admission shape; physical live job `99131694774` was skipped. No runtime/credential/client action occurred.

During GREEN implementation, an additional existing causal gate was discovered: `.github/scripts/track_a_current_client_package_acquire.sh` also hard-coded `RUNNER_NAME=synology-otclient-01`. The independent consumer updates that gate under the same provenance flag; overriding/spoofing `RUNNER_NAME` is forbidden. The runtime helper accepts system toolroot `/` only when the exact independent runner name plus both provenance/system-toolroot flags are present; old Synology retained-toolroot resolution is unchanged.

Pre-restack candidate `2aa4049e31b765f5f2c437fb4ea47b9547a193d3` passed:

```text
Track A current login field6 runtime observation  run 33264987994  success
  Fresh independent V4 admission audit           job 99133361642  success
  Current login field6 runtime contract           job 99133370772  success
  One-shot isolated field6 observation            job 99133363963  skipped
Track A current client package materializer       run 33264987970  success
  Bounded package materializer contract           job 99133367013  success
Track A self-hosted PR boundary                    run 33264987952  success
Track A agent runtime governance                   run 33264987987  success
CI                                                run 33264988038  success
  Fast Checks / Syntax and workflow validation    job 99133387246  success
  CI / Required                                   job 99133465023  success
```

The same six-file GREEN tree was clean-restacked as one commit `009b864a949083f043d02bb6b7140f79f1a36e96` directly on unchanged `main@8c207b38ecad5154a83ec3588e172f096cf2ff29`. Exact-head validation passed again:

```text
Track A current login field6 runtime observation  run 33265176263  success
Track A current client package materializer       run 33265176266  success
Track A self-hosted PR boundary                    run 33265176267  success
Track A agent runtime governance                   run 33265176274  success
CI                                                run 33265176375  success
  CI / Required                                   job 99133970798  success
review_threads                                     0
```

The connected Ready mutation has the known `Repository.fullDatabaseId` response-schema bug. Draft #805 was therefore closed unmerged as superseded rather than merged in Draft state; ready replacement #806 was opened from the same branch/tree. This pointer update will be folded back into one final replacement commit before merge.

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

# V4 terminal trigger state

The V4 trigger was posted exactly once as owner comment `5467500633`. Its run `33300352335` / job `99227195253` is terminal and must never be rerun or recreated. The job failed before authorization consumption, secret exposure, client execution or login. The one-time runner deregistered and the V4 guest was destroyed.

Consumed archival trigger literal (non-executable): `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true`.

# 2026-08-30 terminal V4 checkpoint and seed repair

V4 trigger comment `5467500633` created run `33300352335` / job `99227195253` on the exact one-time label `field6-v4-5467500633`. Independent provenance and trusted-main gates passed. Package acquisition then failed with `FETCH_FAILED:curl_22` after `TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=1`; authorization, credentials and login capture steps were skipped. Therefore `physical_action_count=0`, `login_submit_count=0` and `FIELD6_VALUE=UNKNOWN` remain authoritative. The ephemeral runner deregistered and `OTClientV4Clean` was destroyed.

Direct requests for manifest-listed client binaries now receive Cloudflare managed challenge HTTP 403 while the manifest itself remains exact-current. An existing official Linux launcher archive on Molehill-PC was therefore tested in a throwaway isolated guest without credentials/login. The launcher successfully installed `15.32.75d4a0`; its `bin/client` is exactly `52105824` bytes with SHA256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

The complete launcher-installed package is frozen locally as `C:\OTClientV4\tibia-15.32.75d4a0-official-launcher-seed.tar.gz`, size `412272538`, SHA256 `64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016`. Proprietary bytes are not committed. Durable sanitized evidence is `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/20260830-v4-preauth-failure-official-launcher-seed.md`.

Repository repair branch `fix/OTC-20260830-field6-official-launcher-seed` starts from trusted `main@18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`. RED test `.github/scripts/test_track_a_current_client_package_seed.py` currently fails causally with `FIELD6_SEED_RED: materialize_seed missing`. This checkpoint grants no V5 runtime, credentials or login authority.

# Completion

This task remains incomplete. Current authoritative state is `FIELD6_VALUE=UNKNOWN`, `physical_action_count=0`, `runtime_access:none`, credentials/login/mutation disarmed. Completion requires: trusted-main seed acquisition repair; a separately admitted fresh V5 one-shot observation; sanitized scalar promotion to trusted `main`; then Track B consumption. The V4 generation is archival evidence only.

# Next action

Continue the repository-only seed repair on `fix/OTC-20260830-field6-official-launcher-seed`: finish the RED fixture, implement `materialize_seed` so a hash-pinned official-launcher seed is extracted without executing package content and every package/asset row is revalidated against the embedded manifests plus the exact client fence, then update acquisition/workflow/security contracts for a fresh V5 generation. Require focused GREEN, independent audit and exact-head CI before merge. Only after that repair reaches trusted `main` may a separately admitted fresh V5 one-time trigger/runner be created. Never rerun V4 or reuse comment `5467500633`.
