---
task_id: OTC-20260907-kasm-bin-launch-root-v2
status: implementing
agent: ChatGPT
session_id: kasm-bin-launch-root-v2-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap_repair
phase: implementation
branch: fix/OTC-20260907-kasm-bin-launch-root-v2
base_branch: main
base_main: 5edbb7585e1877dea45b91f8c0dc005fc3598bfa
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
  - .github/workflows/track-a-canonical-kasm-bootstrap-retry.yml
  - tests/tools/tibia_runtime_bridge/test_kasm_bootstrap_launch_readiness.py
  - tests/tools/tibia_runtime_bridge/test_canonical_kasm_bootstrap_retry_contract.py
  - docs/agents/tasks/active/OTC-20260907-kasm-bin-launch-root-v2.md
  - docs/agents/tasks/active/OTC-20260907-canonical-kasm-bootstrap-retry-v2-live.md
modules_touched:
  - track_a_kasm_bootstrap_worker_scoped
reuses:
  - historical physically successful canonical Kasm launcher evidence
  - canonical Kasm scope contract
  - canonical live lease and scoped transition
  - identity-bound bootstrap rollback
depends_on:
  - OTC-20260907-canonical-kasm-bootstrap-retry-live
blocks:
  - OTC-20260906-native-login-physical-executor
---

# Canonical Kasm bin launch-root repair

## Fresh evidence

Trusted-main bootstrap retry EXECUTE run `34121830411`, job `101741397166`, on `main@5edbb7585e1877dea45b91f8c0dc005fc3598bfa` failed before registration with `TRACK_A_KASM_BOOTSTRAP_ERROR=WorkerError`; transition rollback could not classify the early-exit record and reported `kasm_bootstrap_rollback_failed`.

Immediate read-only Surveyor run `34122156989`, job `101742448722`, proved the post-failure state was nevertheless clean: `CANONICAL_REGISTRATION=ABSENT` and `TARGET_NAMESPACE_CLIENTS=0`, with no credential access and no runtime mutation by Surveyor.

Historical physically successful helper relaunch run `32233929770`, job `96009597899`, used the binary directory as both working directory and loader root:

- `client_dir=${CLIENT%/client}` = `.../Tibia/.../bin`;
- `LD_LIBRARY_PATH=$client_dir:$client_dir/lib`;
- `cd '$client_dir' && exec ./client`.

The current scoped bootstrap wrapper instead launches from package root `.../packages/Tibia` and sets `LD_LIBRARY_PATH` to package-root paths, while the exact executable is `.../packages/Tibia/bin/client`. That is a concrete launcher regression.

## Repair

Use `CLIENT_DIR = dirname(CLIENT_PATH)` for:

- Docker working directory;
- `LD_LIBRARY_PATH=CLIENT_DIR:CLIENT_DIR/lib`;
- `cd CLIENT_DIR && exec ./client`.

Keep package identity/fence paths unchanged. Preserve canonical-container-only candidate scope, credential/helper env stripping, exact identity persistence, bounded GUI readiness and identity-bound rollback.

If launch exits before a launch-identity record exists, rollback may return success only after a fresh canonical-Kasm preflight proves the original preflight record is still true: same container/boot/fence with zero exact candidates and zero Tibia windows. This makes early-exit cleanup classification fail-closed without pretending a process was killed.

## Non-goals

No physical retry, process creation/termination, registration write, credential access, auth, login, character selection, GUI input, gameplay or Track B mutation is authorized by this repository-only task.
