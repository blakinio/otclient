---
task_id: OTC-20260907-docker-candidate-inventory-compatibility
status: implementing
agent: ChatGPT
session_id: docker-candidate-inventory-compatibility-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_scope_correction
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
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe-compatible.py
  - .github/scripts/tibia-official-client-re-same-boot-zero-client-invalidate-compatible.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition-scoped.py
  - .github/workflows/track-a-same-boot-zero-client-recovery-v2.yml
  - docs/agents/contracts/TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1.md
  - docs/agents/tasks/active/OTC-20260907-docker-candidate-inventory-compatibility.md
  - docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-recovery-v2-live.md
  - docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-bootstrap-v2-live.md
  - tests/tools/tibia_runtime_bridge/test_docker_candidate_inventory_compatibility.py
  - tests/tools/tibia_runtime_bridge/test_same_boot_zero_client_recovery_v2_contract.py
modules_touched:
  - track_a_kasm_bootstrap_worker_scope
  - track_a_kasm_existing_runtime_probe_scope
  - track_a_canonical_transition_scope
reuses:
  - current exact-client fence
  - existing deep size/SHA/start candidate proof
  - canonical Kasm container identity
  - canonical bootstrap and adoption state machine
depends_on:
  - OTC-20260907-zero-client-stage-diagnostics
blocks:
  - OTC-20260907-same-boot-zero-client-invalidation-live
---

# Canonical Kasm runtime scope correction

## Evidence that exposed the mistake

Trusted-main stage diagnostic `34110414865 / 101705085690` on `main@9736b38e9c8aa54833716ac63a75e93e5415cc92` completed under canonical lease generation `58` with `NO_CREDENTIAL_ACCESS=true` and `RUNTIME_MUTATION=false`.

It showed the canonical Kasm target itself was healthy and empty: `EXACT_CANDIDATE_COUNT=0` and `MAIN_WINDOW_COUNT=0`. Failures came only from attempting candidate inspection in unrelated Synology containers.

The runtime scope was then explicitly corrected by the owner: official-client uniqueness for this Track A path is within the canonical Kasm container `otclient-track-a-kasmvnc`, not across every Docker container on the Synology host.

## Repair objective

Restore the intended boundary:

- exactly one canonical Kasm container must exist;
- zero-client recovery/create-new checks only official-client processes and Tibia windows inside that container;
- adoption/post-launch uniqueness is also evaluated inside that container;
- unrelated Synology containers are outside the Track A runtime namespace and are never executed into or scanned for Tibia candidates;
- exact size/SHA/start, package, boot, display/window, registration and lease proofs remain fail-closed inside the canonical container.

The corrected registration provenance is `inventory_scope: canonical_kasm_container`. Historical registrations using `all_running_docker_containers` remain readable only for backward-compatible recovery; newly created canonical Kasm registrations must use the corrected scope.

## Non-goals

No runtime execution, recovery retry, registration mutation, client launch/kill, credential access, auth, login, GUI input or Track B change is authorized by this repository-only task.

## Acceptance

- deterministic tests prove foreign containers are never deep-scanned;
- missing or duplicate canonical Kasm container fails closed;
- exact/conflicting/unreadable candidates inside canonical Kasm still fail closed as before;
- PRECHECK proves zero client/window only inside canonical Kasm;
- EXECUTE remains separately one-shot authorized and unavailable before PRECHECK PASS;
- new registration records truthful `inventory_scope: canonical_kasm_container`;
- exact-head Track A contracts/governance/self-hosted boundary/CI pass before merge.
