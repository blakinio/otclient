---
task_id: OTC-20260907-proven-login-replacement-recovery
status: implementing
agent: ChatGPT
session_id: proven-login-replacement-recovery-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_replacement_repair
phase: implementation
branch: fix/OTC-20260907-proven-login-replacement-recovery
base_branch: main
base_main: c2e191de82b805eb1ec950e20d83b04edb358429
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
physical_e2e_required: true
credentials_allowed: none
parent_task: OTC-20260906-native-login-physical-executor
depends_on:
  - OTC-20260907-proven-login-explicit-root-reset
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_proven.py
  - .github/workflows/track-a-native-login-be4f48-proven.yml
  - tests/tools/tibia_runtime_bridge/test_native_login_proven_secret_ingress_contract.py
  - docs/agents/tasks/active/OTC-20260907-proven-login-replacement-recovery.md
modules_touched:
  - Track A proven native-login exact-PID replacement
  - Track A canonical runtime recovery
---

# OTC-20260907 — proven-login replacement startup recovery

## Evidence

Trusted-main EXECUTE `34094162584 / 101654124268` on `c2e191de82b805eb1ec950e20d83b04edb358429` passed PRECHECK, acquired canonical lease generation 55, completed generation rebind and Gate B, printed `NO_SECRET_ACCESS_BEFORE_AUTH=true`, then failed inside guarded replacement with `TRACK_A_BE4F48_PHYSICAL_ERROR=replacement_exact_current_runtime_not_ready`. The run never reached `auth-one-shot`, so credential-bearing auth attempt count remains 0.

Read-only Surveyor `34095184707 / 101657174020` immediately afterward proved `CANONICAL_REGISTRATION=PRESENT` and `TARGET_NAMESPACE_CLIENTS=0`; credential access and runtime mutation were false. Because Gate B had passed immediately before the old registered exact PID was terminated, this is a same-boot failed-replacement state, not a prior-boot registration.

A physically successful helper relaunch in historical trusted run `32233929770 / 96009597899` used the exact Kasm GUI environment `HOME=/home/kasm-user`, `DISPLAY=:1`, `XAUTHORITY=/home/kasm-user/.Xauthority`, `LD_LIBRARY_PATH=<package_dir>:<package_dir>/lib`, the three helper `LD_PRELOAD` entries, and `sh -lc 'cd <package_dir> && exec ./client'`; all three helper sockets became ready. The current inherited base `replace()` omits `XAUTHORITY` and `LD_LIBRARY_PATH` and directly execs the absolute client path.

## Repair objective

Restore the physically proven Kasm launch shape for the corrected proven-login worker and make replacement failure transactional: if the instrumented replacement cannot become exact-current/helper-ready, restore one credential-free exact-current client before returning failure so canonical stale-registration recovery can reconcile identity instead of leaving `registration=PRESENT / clients=0`.

The already-existing zero-client state also needs a one-shot fail-closed recovery path before the next PRECHECK/EXECUTE. That recovery must remain credential-free, prove the same exact current fence and zero-client condition under canonical coordination authority, create exactly one ordinary exact-current Kasm client, and then reconcile it through canonical registration semantics. It must not reinterpret prior-boot recovery, bypass Gate A, edit registration by hand, use broad process cleanup, or perform login/GUI input.

## Acceptance

- PR-head remains repository-only; no self-hosted PR-head execution.
- proven replacement launch includes `XAUTHORITY` and package-local `LD_LIBRARY_PATH` and preserves secret-environment scrubbing;
- startup failure does not leave zero clients when a bounded credential-free rollback can restore the exact client;
- concrete sanitized replacement/rollback failure codes replace the opaque readiness-only outcome where possible;
- current same-boot zero-client recovery is explicit, bounded, owner-triggered from trusted `main`, credential-free, exact-fenced and fail-closed;
- focused deterministic tests, workflow contract, Track A governance and exact-head required CI pass;
- after merge, recover canonical runtime first, then fresh PRECHECK, then exactly one EXECUTE; no credential attempt before helper readiness is proven.
