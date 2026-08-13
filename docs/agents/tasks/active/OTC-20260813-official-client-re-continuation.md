---
task_id: OTC-20260813-official-client-re-continuation
status: investigating
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
branch: ci/OTC-20260813-official-client-re-continuation
base_branch: main
pr: 289
task_kind: runtime-research
phase: live-state-revalidation
risk: medium
runtime_platform: native_linux_only
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - tests/tools/test_tibia_official_client_re_*.py
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
modules_touched:
  - official-client-re workflow and evidence only
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md
  - closed PR 48 repository-owned official-client scripts as versioned leads only
  - PR 283 runtime bridge after exact-SHA validation
depends_on:
  - synology-otclient-01 availability
blocks: []
cross_repository_tasks: []
---

# OTC-20260813 — Official Linux client RE continuation

## Objective

Continue Track A from current `blakinio/otclient` durable state: establish an
isolated native-Linux official-client runtime on `synology-otclient-01`, recover
structural `IN_GAME`, correlate the stable bridge, and proceed through player,
map, creature, inventory/container, protocol/action and OTBM evidence gates.

## Runtime ownership

```yaml
runner: synology-otclient-01
subject: official native Linux Tibia client only
state_directory: /home/runner/_work/_otclient_tibia_re_state
compatibility_state_directory_while_legacy_runner_image_is_live: /work/_otclient_tibia_re_state
display: :98
warp_socks_port: 25354
bridge_socket: <state_directory>/runtime/otclient-tibia-re.sock
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
container_names: none
```

Track B owns its own branch, PR, workflow, runtime, display, ports and state.
This task never reads or mutates them and never uses broad process or Docker
cleanup.

## Acceptance inventory

- [ ] Live Track A namespace is proven isolated on the dedicated runner.
- [ ] Exact current official Linux client version, size and SHA are verified.
- [ ] Official client is reconstructed and launched normally through verified WARP.
- [ ] Login recovery consumes secrets only in the approved Actions step and does not persist them.
- [ ] `IN_GAME` is proven from decoded structural state, not OCR/pixels/sockets.
- [ ] Bridge session status is correlated with decoded world state.
- [ ] Authoritative player position and one reversible movement transition are proven.
- [ ] Subsequent capability evidence is persisted with exact run/job/head/SHA references.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T14:47:00+02:00
head: 801d2c35c
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
status: investigating
context_routes:
  - official-client-re
  - native-linux-runtime
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - tests/tools/test_tibia_official_client_re_*.py
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
proven:
  - current main defines Track A as official native Linux client only and isolates Track B mutable runtime
  - PR 48 is closed without merge and is no longer the active ownership source
  - synology-otclient-01 is online with live labels otclient and synology
  - run 31700834510 job 94449297810 proved isolated native-Linux Track A state at /work/_otclient_tibia_re_state with display :98 and WARP port 25354
  - the live Track A namespace has no owned client, Xvfb, or wireproxy PID marker
  - the current runner image has bash curl and python3 but lacks file gdb proxychains4 socat xdotool and Xvfb
  - run 31700967902 job 94449744345 proved WARP ownership and current official client SHA e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
derived:
  - a fresh main-based Track A task and PR are required for discoverable continuation
unknown:
  - current structural session state
  - whether six missing runner tools can run from an isolated unprivileged Track A toolroot without changing the shared runner image
conflicts:
  - canonical preferred runner labels differ from the currently reported legacy label set
first_failure:
  marker: direct runner image lacks six dependencies required for client launch and instrumentation
  evidence: run 31700834510 job 94449297810 emitted TRACK_A_MISSING_TOOL_COUNT=6
rejected_hypotheses:
  - continue mutating closed PR 48 as active ownership: rejected by live PR state and current main governance
changed_paths:
  - .github/scripts/tibia-official-client-re-reconstruct.py
  - .github/workflows/tibia-official-client-re-identity.yml
  - .github/workflows/tibia-official-client-re-live-state.yml
  - .github/workflows/tibia-official-client-re-toolroot.yml
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - tests/tools/test_tibia_official_client_re_reconstruct.py
validation:
  - command: live main governance and PR/runner preflight
    result: PASS
    evidence: main dc18f795, PR 48 closed, runner 21 online
  - command: Track A official-client RE live state run 31700834510 job 94449297810
    result: PASS
    evidence: isolated namespace proven; no owned runtime processes; six required tools absent
  - command: Track A official Linux client identity run 31700967902 job 94449744345
    result: PASS
    evidence: isolated WARP ready; current client size 51965216 and SHA e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  - command: python -m unittest tests.tools.test_tibia_official_client_re_reconstruct
    result: PASS
    evidence: four path/hash-policy tests pass
blockers:
  - runner image lacks file gdb proxychains4 socat xdotool and Xvfb for launch/instrumentation phases
next_action: prepare and validate an unprivileged Track A toolroot for the six missing binaries without altering the shared runner image or Track B runtime
```
