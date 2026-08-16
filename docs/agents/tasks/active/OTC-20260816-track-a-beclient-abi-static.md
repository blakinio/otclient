---
task_id: OTC-20260816-track-a-beclient-abi-static
status: completed
agent: ChatGPT
session_id: chatgpt-beclient-abi-static-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: static-research
phase: client-beclient-loader-abi
branch: research/OTC-20260816-track-a-beclient-abi-static
base_branch: main
base_main: 139ef452214bd212a130f916e87d55c7f8712b93
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-beclient-abi-static
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 330
updated: 2026-08-16T09:40:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-beclient-abi-static.md
modules_touched: []
reuses:
  - closed diagnostic PR #327 static BEClient evidence
  - retained PR #303 exact-client package artifact
  - synology-otclient-01 as static file-analysis executor only
depends_on:
  - current main Track A runtime admission governance
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
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
beclient_size: 3620287
beclient_sha256: 5d1c90ab244155d393296b2e575425aee3252d4d09110007a6d6c3a0bfe05a98
runtime_platform: official_native_linux_only
validation_runs:
  - 31933690981/95132257220
  - 31934000853/95133025014
  - 31934067682/95133184321
  - 31934120792/95133309389
  - 31934210106/95133530199
  - 31934287388/95133715398
  - 31934370065/95133912441
  - 31934410062/95134006400
validation_conclusion: success
e2e: NOT_APPLICABLE_STATIC_FILE_ANALYSIS
mutation_performed: false
next_action: none
---

# Objective

Recover the bounded static integration contract between exact official Linux Tibia client `15.32.df7b29` and its retained `BEClient.so`, without executing either binary or deriving anti-cheat bypass/evasion behavior.

# Final result

## Exact artifacts — FACT

- exact Tibia client fence revalidated throughout: size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`;
- `BEClient.so`: size `3620287`, SHA-256 `5d1c90ab244155d393296b2e575425aee3252d4d09110007a6d6c3a0bfe05a98`;
- `BEClient.cfg`: size `29`, SHA-256 `4b36d4ab990a3bd9f9b5379f58b65ec6402eb3b3109dc83a02b6827778d29281`;
- `BEClient.cfg` contains only `GameID tibia` and `MasterPort 7171`.

## False lead removed — FACT

The client's raw `dlopen/dlsym/dlclose` wrapper cluster is **not** the BattlEye loader. Run `31934000853` / job `95133025014` proved those wrappers belong to miniaudio dynamic backend loading:

- ALSA: `libasound.so.2`, `libasound.so`, `snd_*`;
- PulseAudio: `libpulse.so`, `libpulse.so.0`, `pa_*`;
- JACK: `libjack.so`, `libjack.so.0`, `jack_*`.

No BattlEye conclusion may be based on those raw loader wrappers.

## QLibrary `Init` loader lifecycle — FACT

The exact client imports Qt `QLibrary` operations including `setFileName`, `load`, `resolve`, `isLoaded`, `unload`, constructor/destructor.

One compact code cluster contains:

- `QLibrary::unload` call `0x6fc541`;
- `QLibrary::isLoaded` call `0x6fc57a`;
- exact printable `Init` at `0x1c96c8f`, referenced by `lea rsi, [Init]` at `0x6fc587`;
- `QLibrary::resolve` call `0x6fc591` with `RDI=<embedded QLibrary at state+0x10>` and `RSI="Init"`;
- resolved function pointer stored in `r12` at `0x6fc596` and required non-null;
- when the library is not loaded, `QLibrary::setFileName` call `0x6fcaba` receives a dynamically built `QString`, followed by `QLibrary::load` at `0x6fcac2`; successful load branches back to `0x6fc587` and resolves `Init`.

The file name is not a direct `BEClient.so` literal in this cluster. The `QString` passed to `setFileName` is built earlier from client object/context state and remains `DIRECT_FILENAME_VALUE=UNKNOWN` under static-only analysis.

## Resolved `Init` is actually invoked — FACT

The pointer returned by `resolve("Init")` remains in `r12` and is directly called at `0x6fc6c0` before `r12` is overwritten by the return value.

Immediately before that call the exact client explicitly establishes at least:

```text
RDI = 2
RSI = r15
RDX = state + 0x28
CALL r12
```

After the call, `EAX` is copied to `r12d` and the low byte is tested as a success/failure status. This proves a minimum observed three-argument-plus-return ABI boundary but does **not** assign semantic C/C++ types to those values.

Before `Init`, the state region beginning at `state+0x28` is cleared. After successful `Init`, the pointer at `state+0x30` is checked and invoked when non-null. This is strong structural evidence that the third argument references an output/interface/callback state block populated or activated by initialization. Exact field semantics remain `UNKNOWN`.

## Package uniqueness — FACT

Run `31934410062` / job `95134006400` parsed every retained ELF file in the exact package without executing libraries.

Exactly one ELF exported the exact symbol `Init` among the BE export family searched:

```text
bin/BattlEye/BEClient.so
SHA-256 5d1c90ab244155d393296b2e575425aee3252d4d09110007a6d6c3a0bfe05a98
exports GetVer, Init, _0, _1, _2, _3, _4, _5, _6, _7
```

`BE_INIT_EXPORTER_COUNT=1`.

## Integration conclusion — HIGH-CONFIDENCE INFERENCE

The exact client has one observed `QLibrary::resolve("Init")` loader lifecycle, and `BEClient.so` is the **only retained package ELF exporting `Init`**. Together with the installed `bin/BattlEye/BEClient.so`/`BEClient.cfg` pair, this is high-confidence static evidence that this QLibrary lifecycle is the official client's BattlEye integration path.

It is not promoted to `DIRECT_FILENAME_PROOF` because the concrete `QString` supplied to `QLibrary::setFileName` is dynamically derived and was not reduced to a literal `BEClient.so` path without runtime execution.

## BEClient export-body boundary — FACT / UNKNOWN

`BEClient.so` exports `Init`, `GetVer`, `_0.._7`, but the file uses the previously proven custom `.be0/.be1` self-loading/packed layout. Bounded bytes at the low apparent export values do not decode as trustworthy normal entrypoint code in the on-disk representation. Therefore exact runtime implementations/signatures of `GetVer` and `_0.._7`, and the internal body of `Init`, remain `UNKNOWN` under static-only analysis rather than being inferred from transformed bytes.

The exact client-side evidence directly resolves only `Init`; this analysis found no equally authoritative client-side name-resolution proof for `GetVer` or `_0.._7`.

# Preserved unknowns

- concrete `QString` file name/path passed to `QLibrary::setFileName`;
- semantic type/name of the argument in `RSI` at the `Init` call;
- exact structure and meanings of fields at `state+0x28..`;
- internal unpack/decryption/self-mapping algorithm of `BEClient.so`;
- exact runtime implementation/signatures of `GetVer` and `_0.._7`;
- network protocol/endpoints beyond the static `MasterPort 7171` configuration value;
- any anti-debug/anti-tamper runtime path.

These unknowns were intentionally not converted into bypass/evasion research.

# Safety / validation

All listed semantic runs succeeded on `synology-otclient-01`. Every analysis workflow operated on files only and emitted `mutation_performed=false` equivalents. No Tibia or BattlEye binary was executed/dlopened/preloaded; no process was attached/debugged/injected; no credentials, process memory, login/session state, runtime traffic, canonical runtime, or PR #303 mutable runtime surface was touched.

The two temporary workflows used for this diagnostic task were removed from the branch after evidence collection. PR #330 is diagnostic-only and must be closed unmerged; no temporary analysis infrastructure belongs on `main`.
