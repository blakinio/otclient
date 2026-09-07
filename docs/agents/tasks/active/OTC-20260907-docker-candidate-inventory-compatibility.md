---
task_id: OTC-20260907-docker-candidate-inventory-compatibility
status: implementing
agent: ChatGPT
session_id: docker-candidate-inventory-compatibility-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_recovery_repair
phase: implementation
branch: fix/OTC-20260907-docker-candidate-inventory-compatibility
base_branch: main
base_main: 9736b38e9c8aa54833716ac63a75e93e5415cc92
execution_mode: chatgpt
execution_class: repository_only
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
physical_action_budget: 0
implementation_authorized: true
owned_paths:
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  - .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/tasks/active/OTC-20260907-docker-candidate-inventory-compatibility.md
modules_touched:
  - track_a_kasm_bootstrap_worker
  - track_a_kasm_existing_runtime_probe
reuses:
  - current exact-client fence
  - existing deep size/SHA/start candidate proof
  - Docker daemon process census
  - canonical bootstrap and adoption contracts
depends_on:
  - OTC-20260907-zero-client-stage-diagnostics
blocks:
  - OTC-20260907-same-boot-zero-client-invalidation-live
---

# Docker candidate inventory compatibility repair

## Live evidence

Trusted-main stage diagnostic `34110414865 / 101705085690` on `main@9736b38e9c8aa54833716ac63a75e93e5415cc92` completed under canonical lease generation `58` with `NO_CREDENTIAL_ACCESS=true` and `RUNTIME_MUTATION=false`.

It proved `RUNNING_CONTAINER_COUNT=37`, `NON_TARGET_CONTAINER_COUNT=36`, `EXACT_CANDIDATE_COUNT=0`, `MAIN_WINDOW_COUNT=0`, and no canonical target display/package/boot/candidate/window stage error. Seventeen unrelated non-target candidate-inventory stages failed only because their in-container deep inspector could not be executed: `command_failed:docker:126`.

The blocker is therefore the all-container inventory mechanism, not evidence of an existing canonical client.

## Repair objective

Preserve the contract requirement to cover every running Docker container while removing the false assumption that every unrelated container must provide Python or shell execution support.

Use daemon-side `docker top` as the read-only first-stage process census for every running container. A container with no current official-client process hint is excluded without executing anything inside it. A container whose process list has an official-client hint (`comm=client`, `comm=Tibia*`, or Tibia package/client path in argv) must still pass the existing in-container deep identity scan; failure of that deep scan remains fail-closed. Exact/mismatched/unverifiable candidates remain blockers.

Apply the same two-stage census to both Kasm create-new bootstrap and existing-runtime adoption probe so the repaired recovery does not merely move the same incompatibility to the next transition.

## Non-goals

No runtime execution, recovery retry, registration mutation, client launch/kill, credential access, auth, login, GUI input or Track B change is authorized by this repository-only task.

## Acceptance

- deterministic tests model unrelated non-target containers whose deep exec would return 126 and prove they no longer block after complete daemon-side process census;
- a hinted non-target container whose deep proof is unavailable still fails closed;
- exact, conflicting and unreadable official candidates still block as before;
- bootstrap/adoption retain `all_running_docker_containers` inventory semantics;
- exact-head Track A contracts/governance/self-hosted boundary/CI pass before merge.
