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
updated_at: 2026-08-13T13:55:00+02:00
head: dc18f795bf13cee37a115164da56a452aaa14f02
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
status: investigating
context_routes:
  - official-client-re
  - native-linux-runtime
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
proven:
  - current main defines Track A as official native Linux client only and isolates Track B mutable runtime
  - PR 48 is closed without merge and is no longer the active ownership source
  - synology-otclient-01 is online with live labels otclient and synology
derived:
  - a fresh main-based Track A task and PR are required for discoverable continuation
unknown:
  - live Track A state directory and process state on the runner
  - exact current official-client binary identity on the runner
  - current structural session state
conflicts:
  - canonical preferred runner labels differ from the currently reported legacy label set
first_failure:
  marker: none
  evidence: live revalidation has not yet run in the new isolated namespace
rejected_hypotheses:
  - continue mutating closed PR 48 as active ownership: rejected by live PR state and current main governance
changed_paths:
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
validation:
  - command: live main governance and PR/runner preflight
    result: PASS
    evidence: main dc18f795, PR 48 closed, runner 21 online
blockers:
  - none
next_action: publish the isolated Track A task and run a non-invasive live namespace and dependency probe on synology-otclient-01
```
