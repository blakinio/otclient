---
task_id: OTC-20260816-track-a-beclient-callback-map
status: completed
agent: ChatGPT
session_id: chatgpt-beclient-callback-map-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: complete
branch: docs/OTC-20260816-track-a-beclient-callback-map
base_branch: main
base_main: a27b9f3383b0555142b31216672e9f0143d2cd3d
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260816-track-a-beclient-callback-map
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 332
updated: 2026-08-16T10:02:27+02:00
invocation_started_at: 2026-08-16T09:49:00+02:00
last_progress_at: 2026-08-16T10:02:27+02:00
modules_touched: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
validation_level: focused
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
validation_runs:
  - run: 31935025020
    job: 95135467968
    purpose: initial exact state-local/access windows
    conclusion: success
  - run: 31935171570
    job: 95135821982
    purpose: state-origin and PLT/lifecycle correlation
    conclusion: success
  - run: 31935234113
    job: 95135972836
    purpose: exact BattlEye-state ownership interval and failure paths
    conclusion: success
  - run: 31935315153
    job: 95136163740
    purpose: client-wide owner+0x748 consumer census
    conclusion: success
  - run: 31935419481
    job: 95136403149
    purpose: fresh deterministic exact-byte validator
    conclusion: success
e2e: NOT_APPLICABLE_STATIC_EVIDENCE_RECONSTRUCTION
audit: PASS_DETERMINISTIC_FRESH_VALIDATOR
mutation_performed: false
live_runtime_observed: false
target_executed: false
next_action: none
---

# Objective

Recover the bounded client-side interface shape around the exact official Linux Tibia state block passed as the third observed argument to the unique `QLibrary::resolve("Init")` result associated with `BEClient.so`, without executing or modifying Tibia/BattlEye.

# Final evidence summary

All evidence was collected from the retained exact package file only on `synology-otclient-01`. No target execution, `dlopen`/preload, live `/proc`, process attach/debug/injection, live memory/maps, input, network traffic, credentials, session state, binary patching, unpacking, anti-debug work or anti-cheat bypass/evasion occurred.

The exact client fence passed on every semantic run:

- version `15.32.df7b29`
- size `51965216`
- SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

Prior PR #330 remains the trusted predecessor for these facts: the actual integration uses Qt `QLibrary`; the exact client uniquely resolves `"Init"`; the resolved pointer is directly called at `0x6fc6c0`; the observed call arguments include `RDI=2`, `RSI=r15`, `RDX=state+0x28`; and the exact retained package has only one ELF exporting exact `Init`, `bin/BattlEye/BEClient.so`.

# Correct state ownership boundary

A key correction was established during this task. The giant client function reuses stack local `[rbp-0x148]` for multiple unrelated objects. Therefore later accesses after the local is overwritten must not be attributed to BattlEye.

For the BattlEye path specifically:

- `0x6fc4d7`: `mov r14,[rbx+0x748]`
- `0x6fc4eb`: `mov [rbp-0x148],r14`
- `0x6fc82d`: the same local is overwritten with a different object

Thus the exact client-side ownership interval for this BattlEye state in that function is `0x6fc4eb..0x6fc82c`. Earlier interpretations that associated later `0x6fc92a` state-local accesses with the same BattlEye object are **DISPROVEN**.

# Compact client-side state map

| State offset | Classification | Proven client behavior |
|---|---|---|
| `+0x10` | PROVEN | Embedded `QLibrary` subobject. Used for `isLoaded`, `resolve("Init")`, `setFileName`, `load`, `unload`. |
| `+0x28` | PROVEN | Function-pointer slot populated through the 32-byte `Init` output block. Conditionally called during existing-state reset/teardown before the block is cleared and `QLibrary` is unloaded. |
| `+0x30` | PROVEN | Function-pointer slot populated through the same output block. Conditionally called immediately after successful `Init`. |
| `+0x38` | UNKNOWN | Zeroed before `Init`; no exact client-side semantic consumer proved in this task. |
| `+0x40` | UNKNOWN | Zeroed before `Init`; no exact client-side semantic consumer proved in this task. |
| `+0x48` | PROVEN structure / UNKNOWN meaning | Word/byte control field. Initialized before loader/Init; low byte is forced to zero after `Init` and on resolve-null cleanup. Also gates whether reset executes the `+0x28` callback/unload path. Exact semantic name is unknown. |
| `+0x49` | PROVEN structure / UNKNOWN meaning | Byte read after successful `Init` and XORed with `1`; reset helper clears it to zero; one alternate branch sets it to `1`. Exact semantic name is unknown. |
| `+0x4a` | PROVEN structure / UNKNOWN meaning | Byte copied before `Init` from another client object at `[rbp-0x140]+0x1d8`. |
| `+0x4b` | PROVEN structure / UNKNOWN meaning | Byte tested before the loader path; nonzero follows an alternate branch which sets `+0x49=1` and `+0x4b=1`. Exact semantic name is unknown. |

The 32-byte block supplied as the third observed `Init` argument is exactly `state+0x28..state+0x47`, i.e. four qword-sized slots. It is zeroed with two 16-byte stores immediately before loader/Init use.

# Exact lifecycle

## Existing-state reset before re-initialization

At `0x6fc518` the client checks `state+0x48`. On the reset path where it is zero:

1. loads `state+0x28`;
2. if non-null, directly calls that function pointer;
3. zeroes all 32 bytes `state+0x28..+0x47`;
4. passes `state+0x10` to `QLibrary::unload`.

This same lifecycle is independently repeated in the shared reset helper at `0x7319e0` and in an owner cleanup path at `0x7019c7..0x701aab`.

Because `+0x28` is invoked immediately before block clearing and library unload in multiple independent cleanup contexts, its **client-observed lifecycle role is teardown/reset callback**. This describes only when the client invokes it; its BattlEye-internal implementation remains unresearched.

## Init

The client resolves exact string `"Init"` through `QLibrary` and calls the resulting pointer at `0x6fc6c0`. Immediately before the call the statically observed register preparation includes:

- `RDI = 2`
- `RSI = r15`
- `RDX = state + 0x28`

The third argument therefore points to the zeroed four-qword output/interface block described above.

## Successful Init

Immediately after `Init` returns:

1. the low byte of the return value is tested as success/failure;
2. `state+0x48` low byte is cleared;
3. on success, `state+0x30` is loaded and conditionally called;
4. `state+0x49` is read and XORed with `1` for later client control flow.

No fresh argument-marshalling instructions occur between the successful `Init` return and the `call` through `state+0x30`. This does **not** prove a `void()` ABI because caller-saved registers may contain values established by `Init`; only the absence of explicit fresh client-side argument setup is proven.

## Init/resolve failure

- If `Init` reports false, the client enters reset helper `0x7319e0`.
- If `resolve("Init")` returns null, the client first clears `state+0x48` and then enters the same reset helper.
- `0x7319e0`, when the gate permits, invokes `+0x28`, zeroes `+0x28..+0x47`, unloads the embedded `QLibrary`, and clears `+0x49`.

# Client-wide owner census

A bounded client-wide scan for common non-SIB `mov r64,[base+0x748]` forms found exactly eight direct owner-member loads:

- `0x6fc4d7`
- `0x7019c7`
- `0x7da4e9`
- `0x7fce89`
- `0xb713da`
- `0xd41f1c`
- `0xd602d8`
- `0xd9430c`

The independent owner cleanup at `0x7019c7` re-proved the `+0x28` callback / 32-byte clear / `QLibrary::unload` lifecycle. The bounded consumer scan did not establish an analogous direct semantic use for `+0x38` or `+0x40`; they remain **UNKNOWN**, not assumed unused globally.

# Fresh deterministic validation

Run `31935419481`, job `95136403149`, completed `success`. It re-derived exact byte invariants from the fenced client independently of the earlier decoded summaries and passed all of the following anchors:

- owner `+0x748` -> state pointer at `0x6fc4d7`;
- state-local assignment at `0x6fc4eb`;
- next local overwrite at `0x6fc82d`;
- pre-init `+0x28` callback at `0x6fc518`;
- 32-byte clear + unload at `0x6fc531`;
- exact `resolve("Init")` sequence at `0x6fc587`;
- observed `Init` argument/call sequence at `0x6fc69c`;
- success-path `+0x30` callback at `0x6fc6c6`;
- success-path `+0x49` read/invert at `0x6fc6e5`;
- shared reset lifecycle at `0x7319e0`;
- independent owner cleanup at `0x7019c7` / `0x701a90`;
- resolve-null reset at `0x6fd8be`;
- exact bounded owner `+0x748` load census count `8`.

Validator safety outputs:

- `VALIDATOR_EXECUTED_TARGET=false`
- `VALIDATOR_LIVE_RUNTIME_OBSERVED=false`
- `VALIDATOR_MUTATION_PERFORMED=false`

# Preserved unknowns and safety boundary

The following remain intentionally unknown/unresearched:

- semantic purpose of `+0x38` and `+0x40`;
- semantic names for control bytes `+0x48..+0x4b`;
- internal behavior of the callbacks supplied by BattlEye;
- packed/self-loading implementation details of `BEClient.so`;
- anti-debug/anti-tamper/detection/signature logic;
- network protocol internals beyond already visible non-secret configuration;
- any bypass, disabling, spoofing, stealth or evasion technique.

This task produced no product/runtime mutation and requires no E2E execution. Temporary proving workflow must be removed before PR closeout and must not enter `main`.
