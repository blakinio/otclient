---
task_id: OTC-20260907-same-boot-recovery-diagnostics
status: implementing
agent: ChatGPT
session_id: same-boot-recovery-diagnostics-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: recovery_observability
phase: implementation
branch: fix/OTC-20260907-same-boot-recovery-diagnostics
base_branch: main
base_main: 5e72f5a44a52a43b47dae83dccca656682d118a3
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
physical_e2e_required: false
credentials_allowed: none
parent_task: OTC-20260907-proven-login-replacement-recovery
depends_on:
  - OTC-20260907-same-boot-zero-client-invalidation-live
owned_paths:
  - .github/scripts/track_a_kasm_zero_client_diagnose.py
  - .github/workflows/track-a-kasm-zero-client-diagnose.yml
  - tests/tools/tibia_runtime_bridge/test_kasm_zero_client_diagnostic_contract.py
  - docs/agents/tasks/active/OTC-20260907-same-boot-recovery-diagnostics.md
  - docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-diagnostic-live.md
modules_touched:
  - Track A Kasm zero-client recovery observability
---

# OTC-20260907 — same-boot recovery diagnostics

## Evidence

Merged PR #975 restored a reviewed same-boot zero-client recovery path. Trusted-main recovery run `34105630197 / 101689863472` on `5e72f5a44a52a43b47dae83dccca656682d118a3` passed durable admission, consumed its one-shot recovery marker and acquired canonical lease generation `56`, then failed inside guarded invalidation with `TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_ERROR=zero_client_preflight_failed`. Bootstrap and final registration verification were skipped; no credential or login action ran.

Fresh read-only Surveyor `34106503302 / 101692630870` on the same trusted main then proved `CANONICAL_REGISTRATION=PRESENT` and `TARGET_NAMESPACE_CLIENTS=0`. Therefore the zero-client preflight failure is not explained by a current client in the canonical Kasm namespace. Surveyor does not scan external Docker containers, while the approved Kasm bootstrap worker deliberately performs all-running-container candidate inventory.

The current bootstrap worker and invalidator collapse the precise `WorkerError` cause into generic public errors. That observability gap prevents evidence-based recovery selection.

## Objective

Add one narrow diagnostic surface that imports the existing approved Kasm bootstrap worker and runs only its current `collect_preflight()` under canonical recovery serialization. Surface only a validated hardcoded/sanitized worker error code. Do not alter the production worker semantics, registration, recovery marker, client processes, credentials, login state or bootstrap budget.

## Acceptance

- PR-head execution is hosted/repository-only;
- live diagnostic is owner-triggered only from merged trusted `main`;
- live diagnostic requires a fresh canonical recovery lease and executes under `guard-run`;
- diagnostic verifies the external coordination flock is held;
- exact approved bootstrap worker and central current-client fence are required;
- only a strict sanitized worker error code may be emitted;
- no registration write/invalidation, process launch/stop, bootstrap transition, credential access, auth, GUI input or one-shot recovery marker occurs;
- focused tests, Track A governance, self-hosted boundary audit and exact-head CI are green;
- after merge, execute the diagnostic once and use its exact code to decide the next recovery repair instead of retrying `34105630197`.
