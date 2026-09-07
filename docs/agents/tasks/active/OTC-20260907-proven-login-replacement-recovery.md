---
task_id: OTC-20260907-proven-login-replacement-recovery
status: ready
agent: ChatGPT
session_id: proven-login-replacement-recovery-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_replacement_repair
phase: merge_readiness
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
  - .github/scripts/tibia-official-client-re-same-boot-zero-client-invalidate.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/scripts/track_a_agent_runtime_governance_base.py
  - .github/workflows/track-a-native-login-be4f48-proven.yml
  - .github/workflows/track-a-same-boot-zero-client-recovery.yml
  - docs/agents/contracts/TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1.md
  - docs/agents/tasks/active/OTC-20260907-proven-login-replacement-recovery.md
  - docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-invalidation-live.md
  - docs/agents/tasks/active/OTC-20260907-same-boot-zero-client-bootstrap-live.md
  - tests/tools/tibia_runtime_bridge/test_native_login_proven_secret_ingress_contract.py
  - tests/tools/tibia_runtime_bridge/test_same_boot_zero_client_recovery_contract.py
modules_touched:
  - Track A proven native-login exact-PID replacement
  - Track A canonical runtime recovery
repair_cycles_for_current_gate: 1
identical_failure_retries: 0
ci_checks_for_current_head: 2
ci_check_generation: draft
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# OTC-20260907 — proven-login replacement startup recovery

## Evidence

Trusted-main EXECUTE `34094162584 / 101654124268` on `c2e191de82b805eb1ec950e20d83b04edb358429` passed PRECHECK, acquired canonical lease generation 55, completed generation rebind and Gate B, printed `NO_SECRET_ACCESS_BEFORE_AUTH=true`, then failed inside guarded replacement with `TRACK_A_BE4F48_PHYSICAL_ERROR=replacement_exact_current_runtime_not_ready`. The run never reached `auth-one-shot`, so credential-bearing auth attempt count remains 0.

Read-only Surveyor `34095184707 / 101657174020` immediately afterward proved `CANONICAL_REGISTRATION=PRESENT` and `TARGET_NAMESPACE_CLIENTS=0`; credential access and runtime mutation were false. Because Gate B had passed immediately before the old registered exact PID was terminated, this is a same-boot failed-replacement state, not a prior-boot registration. The registration remained bound to the generation-55 identity accepted by that Gate B.

A physically successful helper relaunch in historical trusted run `32233929770 / 96009597899` used the exact Kasm GUI environment `HOME=/home/kasm-user`, `DISPLAY=:1`, `XAUTHORITY=/home/kasm-user/.Xauthority`, `LD_LIBRARY_PATH=<package_dir>:<package_dir>/lib`, the three helper `LD_PRELOAD` entries, and `sh -lc 'cd <package_dir> && exec ./client'`; all three helper sockets became ready. The inherited base `replace()` omitted `XAUTHORITY` and `LD_LIBRARY_PATH` and directly execed the absolute client path.

## Implemented repair

The corrected proven-login wrapper now owns the replacement seam instead of inheriting the incomplete base launch shape. It uses the physically proven Kasm environment and shell/working-directory launch form while preserving the existing exact-current fence, helper sockets, one-shot secret boundary and explicit credential-environment scrubbing.

Replacement is transactional before auth. If the instrumented process cannot become exact-current with all helpers ready, the worker performs only bounded exact-current cleanup, starts one plain credential-free exact-current client with helper variables explicitly unset, verifies its exact identity/UID and writes sanitized rollback evidence. The operation then still returns failure before `auth-one-shot`; a later canonical stale-registration recovery must reconcile the rollback PID before any login attempt.

For the already-created `registration=PRESENT / clients=0` state, this task adds `TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1`. The invalidator is metadata-only and requires a newer recovery lease plus external canonical `guard-run`. It independently proves the coordination flock is already held, exact-fences the approved Kasm bootstrap worker, repeatedly proves same boot + zero official-client candidates + zero Tibia windows + dead registered process + unchanged lease/registration, then atomically moves only the stale registration to a byte-identical private tombstone. It repeats zero-client and lease proof after commit and never restores stale metadata on post-commit uncertainty.

The future trusted-main live sequence is split into two durable admissions:

1. `OTC-20260907-same-boot-zero-client-invalidation-live` — zero process actions, no credentials, metadata invalidation only;
2. `OTC-20260907-same-boot-zero-client-bootstrap-live` — exactly one existing reviewed `kasm-bootstrap` create-new action, stopping at plain exact-current `state: UNKNOWN` with no credentials/login/input.

The owner-only comment command `/track-a-same-boot-zero-client-recovery EXECUTE` executes those two transitions from exact trusted `main`; PR-head remains repository-only.

## Exact-head validation

Final implementation head before this documentation checkpoint was `e8034a5ffc086793dd47f9de71eeff528e0b40bb`. Current protected `main` remained `c2e191de82b805eb1ec950e20d83b04edb358429`; the PR was mergeable and had exactly 11 intended changed paths, zero review submissions and zero review threads.

All exact-head pull-request workflows on `e8034a5f...` completed successfully:

- `34104669992` — Track A same-boot zero-client recovery: SUCCESS;
- `34104669889` — Track A be4f48 proven native login: SUCCESS;
- `34104669994` — Track A proven secret-ingress contract: SUCCESS;
- `34104669925` — Track A agent runtime governance, including fresh admission behavior audit: SUCCESS;
- `34104669937` — Track A canonical current-client fence: SUCCESS;
- `34104670000` — Track A Kasm canonical bootstrap: SUCCESS;
- `34104669876` — Track A canonical client-fence reconciliation: SUCCESS;
- `34104669965` — Track A self-hosted PR boundary: SUCCESS;
- `34104670147` — CI: SUCCESS.

The first exact-head generation exposed two compatibility defects in the governance shim rather than recovery semantics: missing `task_matches_expected_branch` export and missing direct current-fence loader marker. Both were repaired without changing the base governance validator; the promoted base validator is retained byte-for-byte in `track_a_agent_runtime_governance_base.py`, and all non-new-mode validation still delegates to it. The second exact-head generation passed all checks above.

Independent deterministic audit evidence is supplied by the separate fresh-admission audit, canonical current-fence validator, self-hosted PR boundary validator and the new same-boot recovery contract. Open material findings after repair: `0`.

## Acceptance

- PR-head remains repository-only; no self-hosted PR-head execution.
- proven replacement launch includes `XAUTHORITY` and package-local `LD_LIBRARY_PATH` and preserves secret-environment scrubbing;
- startup failure does not leave zero clients when a bounded credential-free rollback can restore the exact client;
- concrete sanitized replacement/rollback failure codes replace the opaque readiness-only outcome where possible;
- current same-boot zero-client recovery is explicit, bounded, owner-triggered from trusted `main`, credential-free, exact-fenced and fail-closed;
- recovery cannot acquire the canonical flock itself and pass; it must prove an external `guard-run` already owns the flock;
- recovery and bootstrap have separate durable admissions and action budgets;
- focused deterministic tests, workflow contract, Track A governance and exact-head required CI pass;
- after merge, recover canonical runtime first, then fresh PRECHECK, then exactly one EXECUTE; no credential attempt before helper readiness is proven.

## Next action

Promote PR #975 after this documentation-only checkpoint receives its exact-head required checks. After merge, execute exactly one trusted-main `/track-a-same-boot-zero-client-recovery EXECUTE`; only after that restores one plain exact-current canonical client run fresh proven-login PRECHECK and then the single authorized proven-login EXECUTE.
