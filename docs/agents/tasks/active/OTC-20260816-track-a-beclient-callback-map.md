---
task_id: OTC-20260816-track-a-beclient-callback-map
status: investigating
agent: ChatGPT
session_id: chatgpt-beclient-callback-map-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260816-track-a-beclient-callback-map
base_branch: main
base_main: a27b9f3383b0555142b31216672e9f0143d2cd3d
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260816-track-a-beclient-callback-map
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: pending
updated: 2026-08-16T09:49:00+02:00
invocation_started_at: 2026-08-16T09:49:00+02:00
last_progress_at: 2026-08-16T09:49:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-beclient-callback-map.md
  - .github/workflows/tibia-official-client-re-beclient-callback-map-static.yml
modules_touched: []
reuses:
  - closed diagnostic PR #330 client-to-BEClient QLibrary/Init static evidence
  - retained PR #303 exact-client package artifact as static file input only
depends_on:
  - current main Track A runtime-admission governance
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: GitHub Actions is the permitted remote static-file analysis environment; no Codex or local terminal is required
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one cohesive static client-side interface reconstruction with one exact package and no live runtime
validation_level: focused
heavy_validation_runs: 0
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
track_a_runtime_agent_admission_version: 1
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
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
next_action: statically map the exact client-side state block passed to resolved BEClient Init, enumerate only proven pointer-slot reads/calls and their control-flow contexts, and preserve UNKNOWN semantics without executing or modifying Tibia/BattlEye
---

# Objective

Recover the bounded client-side interface shape around the state block passed as the third observed argument to the exact official Linux client's `QLibrary::resolve("Init")` result, with special focus on the block beginning at the previously observed `state + 0x28` and the function-pointer use at `state + 0x30`.

# Trusted starting facts

From closed diagnostic PR #330 and its successful static runs on exact client `15.32.df7b29`:

- the raw `dlopen/dlsym/dlclose` clusters in the client were disproven as BattlEye and identified as miniaudio ALSA/Pulse/JACK loaders;
- the exact client has a Qt `QLibrary` lifecycle that performs `isLoaded`, `setFileName`, `load`, and exactly one `resolve("Init")` path;
- `resolve("Init")` result is stored in `r12`, required non-null, and directly called at client VA `0x6fc6c0`;
- immediately before that call the observed argument registers include `RDI=2`, `RSI=r15`, `RDX=state+0x28`;
- the low byte of the return value is used as a success/failure status;
- the block beginning at `state+0x28` is cleared before Init and a pointer at `state+0x30` is conditionally called after successful Init;
- a full static inventory of the retained exact package found exactly one ELF exporting exact symbol `Init`: `bin/BattlEye/BEClient.so`, which also exports `GetVer` and `_0.._7`;
- the concrete dynamically derived `QString` passed to `QLibrary::setFileName` was not reduced to a literal filename and remains unproven;
- on-disk apparent bodies for low-address `Init/GetVer/_0.._7` exports are not trustworthy as normal runtime code because the library has a packed/self-loading `.be0/.be1` layout.

# Acceptance inventory

1. Revalidate the exact Tibia client fence before analysis.
2. Operate on retained package files only; no process/runtime observation or target execution.
3. Identify the exact base register/object used for the third `Init` argument and prove which offsets within that object are zeroed, read, written, compared, or indirectly called in the same client-side lifecycle.
4. For every indirect function call attributable to a proven slot, record exact client VA, slot offset, argument-register preparation that can be statically established, and post-call branching/use.
5. Distinguish direct slot calls from unrelated virtual calls or reused registers; do not assign names such as heartbeat, packet, kick, scan, or network unless exact client-side evidence proves them.
6. Determine whether the client treats the block as one flat callback table, a header plus nested interface pointer, or another structure, only to the level proven by client-side accesses.
7. Preserve exact `PROVEN`, `DERIVED`, `UNKNOWN`, `DISPROVEN` classifications.
8. Do not analyze unpacking, anti-debug, anti-tamper, detection, signatures, scan logic, stealth, bypass/evasion, or methods to disable BattlEye.
9. Remove the temporary validation workflow before terminal closeout; do not merge it to `main`.
10. Persist exact run/job identifiers and the compact interface map in this task record/PR body.

# Safety boundary

Static file inspection only. Do not execute or load `client`/`BEClient.so`, do not preload, inject, attach, debug, trace live processes, read live memory/maps, send input/network traffic, alter credentials/session state, patch binaries, or redistribute proprietary files. Do not derive anti-cheat bypass/evasion, detection avoidance, disabling, spoofing, anti-debug defeat or signature neutralization instructions. PR #303 runtime-owned surfaces remain untouched.

# E2E profile

`NOT_APPLICABLE`: this is a static evidence-reconstruction task with no executable/product behavior change and no live runtime access. Outcome verification is exact-build static consistency plus bounded control/data-flow evidence from the client file.
