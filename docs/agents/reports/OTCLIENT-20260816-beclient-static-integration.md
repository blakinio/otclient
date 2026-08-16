# Official Linux Tibia `BEClient.so` static integration report

Date: 2026-08-16  
Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Scope: static exact-build evidence only  
Repository: `blakinio/otclient`

## Purpose

This report is the canonical repository summary of the bounded static research performed on the BattlEye client module bundled with the exact official native Linux Tibia client and on the client-side loader/ABI used to initialize a module exposing the observed `Init` contract.

It consolidates material evidence previously retained only in closed diagnostic PRs #326, #327, #330 and #332. Those PRs were intentionally closed unmerged after temporary validation workflows were removed.

The report is descriptive research evidence. It is **not** a guide to disable, bypass, patch, evade or interfere with BattlEye.

## Evidence classification

- **PROVEN** — directly established from the exact fenced files or deterministic exact-byte validation.
- **DERIVED** — high-confidence conclusion supported by multiple PROVEN structural facts, but not directly established at the same semantic level.
- **UNKNOWN** — not established and must not be guessed.
- **DISPROVEN** — a prior bounded hypothesis was directly falsified.

## Exact subject identities

### Official Linux Tibia client

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

### Bundled BattlEye client module

```yaml
path_in_retained_package: bin/BattlEye/BEClient.so
size: 3620287
sha256: 5d1c90ab244155d393296b2e575425aee3252d4d09110007a6d6c3a0bfe05a98
md5: 236976e08df0cc30e112c717dced235c
```

### Bundled BattlEye configuration

```yaml
path_in_retained_package: bin/BattlEye/BEClient.cfg
size: 29
sha256: 4b36d4ab990a3bd9f9b5379f58b65ec6402eb3b3109dc83a02b6827778d29281
content:
  - GameID tibia
  - MasterPort 7171
```

`MasterPort 7171` is only a configuration fact. Exact protocol/endpoint semantics were not established.

## What is established about the role of `BEClient.so`

### PROVEN

The retained exact Tibia package contains `bin/BattlEye/BEClient.so`, `BEClient.cfg`, and BattlEye licensing material. The exact Tibia executable contains BattlEye/BEClient-related strings and contains a Qt `QLibrary` lifecycle that resolves and directly calls an exported function named `Init`.

A static inventory of every ELF in the retained exact package found **exactly one ELF exporting the exact symbol `Init`**: `bin/BattlEye/BEClient.so`. That same module exports `GetVer` and `_0.._7`.

The concrete dynamically derived `QString` passed to `QLibrary::setFileName` was not reduced to a literal filename, so the filename flow itself remains UNKNOWN.

### DERIVED

Taken together, the unique exact-package `Init` exporter and the client's unique observed `QLibrary::resolve("Init")` path identify `BEClient.so` with high confidence as the Linux-side BattlEye component intended to satisfy this official-client initialization boundary.

Its client-observable responsibilities are therefore best described as:

1. exposing the initialization contract consumed by the Tibia client;
2. providing or enabling population of a small client-facing interface/callback region used around initialization and teardown;
3. participating in a reset/unload lifecycle controlled by the Tibia client;
4. having access, through its imports, to memory-management, dynamic-loading, filesystem/system and networking primitives needed by its protected implementation.

This does **not** establish the exact anti-cheat checks, detection logic, collected data, server messages or callback implementations.

## Static ELF identity and layout

PR #327 established these direct facts from `BEClient.so` without executing it.

### PROVEN ELF facts

- ELF64, little-endian;
- type `ET_DYN`;
- machine `AMD x86-64`;
- ELF entrypoint `0xc6bbec`;
- 9 program headers;
- 31 section headers;
- `.symtab` absent;
- no `.debug_*` sections;
- no GNU build ID;
- embedded compiler strings include GCC 4.8.x Ubuntu toolchain identifiers.

Compiler strings are not proof of the module build date.

### PROVEN direct dependencies

```text
libc.so.6
libdl.so.2
libstdc++.so.6
libgcc_s.so.1
```

No direct OpenSSL/curl dependency was observed in the dynamic NEEDED list.

### PROVEN relevant imported capabilities

Observed dynamic imports include, among others:

- memory: `mmap`, `mprotect`, `munmap`;
- dynamic loading/introspection: `dlopen`, `dladdr`;
- networking: `socket`, `connect`, `send`, `sendto`, `recv`, `recvfrom`, `select`, `poll`, `gethostbyname`, `gethostname`, `getsockopt`;
- filesystem/system: `open`, `fopen`, `opendir`, `readdir`, `readlink`, `ioctl`, `__fxstatat`, `system`, `uname`, `lseek`, `fread`, `fwrite`;
- scheduling/time/threading: `sched_getaffinity`, `sched_setaffinity`, pthread mutex functions, `clock_gettime`, `gettimeofday`, `usleep`, `time`;
- stack protector: `__stack_chk_fail`.

A direct dynamic import of `ptrace` was **not** found. A printable `ptrace` token exists in the binary, but that does not prove how or whether a ptrace operation is invoked.

## Protected/self-loading structure

### PROVEN

The module contains custom executable sections `.be0` and `.be1`.

`.be1`:

```yaml
flags: ALLOC+EXEC
address: 0xa00270
file_offset: 0x270
size: 0x367de6
entropy: 7.790/8
contains_elf_entrypoint: true
mapped_load_segment:
  flags: RWE
  offset: 0x270
  vaddr: 0xa00270
  filesz: 0x367de6
  memsz: 0x367de6
```

`.be0` has unconventional/internally inconsistent file/section mapping metadata: its declared executable section range extends beyond EOF, while the corresponding lower executable LOAD destination has `filesz=0` and a large `memsz`.

Other lower code/data LOAD regions similarly have zero or tiny file-backed sizes while reserving much larger runtime memory regions.

The GNU stack flags are RW, so the stack is non-executable. GNU RELRO and BIND_NOW were not present. An RWE load segment is present.

### DERIVED

The combination of:

- entrypoint inside high-entropy `.be1`;
- almost-whole-file RWE mapping at a high virtual address;
- lower executable/data regions reserved with `memsz` but little/no `filesz`;
- imports such as `mmap`, `mprotect`, `munmap`;
- non-conventional section metadata;

is high-confidence evidence of a custom **self-loading/self-mapping packed or obfuscated protection architecture**.

Conceptually, the initial `.be1` layer likely prepares/materializes protected lower code/data regions before control reaches the effective runtime implementation.

The exact unpacking/decryption/materialization algorithm is UNKNOWN and intentionally not researched here.

The apparent on-disk low-address bodies associated with exported `Init`, `GetVer`, `_0.._7` must therefore **not** be treated as trustworthy ordinary runtime function bodies without separate proof.

## Export surface

### PROVEN relevant dynamic names

```text
GetVer
Init
_0
_1
_2
_3
_4
_5
_6
_7
```

The dynamic symbol/version metadata also exposes `BECLIENT_1.0`; it is not assumed to be a callable function.

The semantics of `_0.._7` are UNKNOWN.

## How the official Tibia client reaches the `Init` contract

### DISPROVEN: raw `dlopen/dlsym/dlclose` hypothesis

The official Tibia executable imports `dlopen`, `dlsym` and `dlclose`, but the directly identified call cluster belongs to the audio subsystem and dynamically loads ALSA/PulseAudio/JACK libraries.

That path is **not** the BattlEye integration path.

Future work must not cite the miniaudio `dlopen/dlsym` wrappers as BattlEye evidence.

### PROVEN: Qt `QLibrary` `Init` lifecycle

The exact client has the following Qt `QLibrary` call sequence around the unique observed `Init` string:

```text
0x6fc541  QLibrary::unload
0x6fc57a  QLibrary::isLoaded
0x6fc587  reference to exact C string "Init"
0x6fc591  QLibrary::resolve("Init")
0x6fc596  resolved function pointer retained in r12
0x6fcaba  QLibrary::setFileName(...)
0x6fcac2  QLibrary::load()
0x6fc6c0  direct call through resolved Init pointer
```

When the `QLibrary` instance is not loaded, the client supplies a dynamically derived `QString` to `setFileName`, calls `load`, then returns to the resolve path.

The concrete filename value remains UNKNOWN. Separately, the retained exact package contains only one ELF exporting exact `Init`: `bin/BattlEye/BEClient.so`.

### DERIVED

The combination of those two facts is high-confidence static identification of the official Tibia client → `BEClient.so` initialization boundary.

## `Init` ABI observed from the Tibia client

### PROVEN call preparation

Before the resolved `Init` call, the client prepares at least:

```text
RDI = 2
RSI = r15
RDX = state + 0x28
```

and calls the resolved pointer at `0x6fc6c0`.

The low byte of the return value is tested as success/failure.

Do not assign source-level C/C++ types to these arguments without further evidence.

## Correct BattlEye state ownership boundary

PR #332 corrected an important earlier over-attribution.

The large client function reuses stack local `[rbp-0x148]` for multiple unrelated objects. For the BattlEye-associated path specifically:

```text
0x6fc4d7  load [owner+0x748] into r14
0x6fc4eb  store r14 into [rbp-0x148]
0x6fc82d  overwrite [rbp-0x148] with a different object
```

Therefore the proven ownership interval for that local is:

```text
0x6fc4eb .. 0x6fc82c
```

### DISPROVEN correction

Earlier attribution of later accesses around `0x6fc92a` to the same BattlEye-associated state is false: by then `[rbp-0x148]` has already been overwritten with another object.

Future analysis must preserve this boundary.

## Client-observed state/interface layout

Within the proven owner object, the following client-side behavior was established.

| Offset | Classification | Client-observed behavior |
|---|---|---|
| `+0x10` | PROVEN | Used as the `QLibrary` object/subobject for load/resolve/unload calls. |
| `+0x28` | PROVEN | Function-pointer slot in the 32-byte region passed to `Init`; later conditionally called during reset/teardown before the region is cleared and the library is unloaded. |
| `+0x30` | PROVEN | Function-pointer slot in the same region; later conditionally called immediately after successful `Init`. |
| `+0x38` | UNKNOWN | Zeroed before `Init`; no exact client-side semantic consumer proved. |
| `+0x40` | UNKNOWN | Zeroed before `Init`; no exact client-side semantic consumer proved. |
| `+0x48` | PROVEN structure / UNKNOWN meaning | Control field/byte participating in reset/init branches. Low byte is cleared after `Init` and on resolve-null cleanup; it also gates a reset path. |
| `+0x49` | PROVEN structure / UNKNOWN meaning | Byte read after successful `Init` and XORed with `1`; reset clears it; an alternate branch can set it. |
| `+0x4a` | PROVEN structure / UNKNOWN meaning | Byte copied before `Init` from another client object. |
| `+0x4b` | PROVEN structure / UNKNOWN meaning | Byte tested before the loader path and used in alternate control flow. |

### PROVEN 32-byte region passed to `Init`

The third observed argument points at:

```text
state + 0x28
```

The client zeroes exactly 32 bytes from:

```text
state + 0x28 .. state + 0x47
```

before initialization. This is four qword-sized slots.

### DERIVED

Because the region is zeroed, passed directly to `Init`, and later contains conditionally invoked function pointers, the client treats it as an output/interface/callback region associated with the `Init` contract.

This does not prove how `BEClient.so` internally constructs or owns those values.

## Lifecycle of the proven function-pointer slots

### `state+0x28`

#### PROVEN

Before re-initialization, when the reset gate allows it, the client:

1. loads `state+0x28`;
2. if non-null, calls the function pointer;
3. clears the full 32-byte `state+0x28..+0x47` region;
4. unloads the `QLibrary` object at `state+0x10`.

The shared reset helper at `0x7319e0` independently repeats the same pattern, and a separate owner cleanup path at `0x7019c7..0x701aab` re-proves it from `[owner+0x748]`.

#### DERIVED

From the Tibia client's perspective, `+0x28` has the lifecycle role of a **reset/teardown callback**.

This does not establish what BattlEye internally performs inside that callback.

### `state+0x30`

#### PROVEN

After `Init` reports success, the client:

1. clears the low byte at `state+0x48`;
2. loads `state+0x30`;
3. if non-null, calls that function pointer;
4. later reads `state+0x49` and XORs it with `1` for client control flow.

No semantic callback name is assigned. The exact internal responsibility of `+0x30` is UNKNOWN.

No explicit fresh argument-marshalling sequence was observed between the successful `Init` return and the `+0x30` call. That does **not** prove a zero-argument source-level ABI because caller-saved registers may still contain values established by `Init`.

### `state+0x38` and `state+0x40`

These slots are zeroed before `Init`, but no exact client-side semantic consumer was established in the bounded research. They remain UNKNOWN, not assumed unused globally.

## Failure/reset paths

### PROVEN

- If `Init` reports false, the client enters reset helper `0x7319e0`.
- If `resolve("Init")` returns null, the client clears `state+0x48` and enters the same reset helper.
- When permitted by its gate, reset helper `0x7319e0` calls `+0x28`, clears `+0x28..+0x47`, unloads `state+0x10`, and clears `+0x49`.

## Client-wide owner-member census

A bounded scan for common direct `mov r64,[base+0x748]` forms found eight exact client locations:

```text
0x6fc4d7
0x7019c7
0x7da4e9
0x7fce89
0xb713da
0xd41f1c
0xd602d8
0xd9430c
```

The separate cleanup site beginning at `0x7019c7` independently confirmed the `+0x28` callback → clear 32-byte region → `QLibrary::unload` lifecycle.

The bounded scan did not prove semantic consumers for `+0x38` or `+0x40`.

## What remains UNKNOWN

The following are intentionally not promoted beyond available evidence:

- exact semantic type/signature of `Init`;
- exact meaning of argument value `RDI=2`;
- semantic name/purpose of the `RSI=r15` context;
- semantic purpose of callbacks `+0x30`, `+0x38`, `+0x40`;
- semantic names of control fields `+0x48..+0x4b`;
- semantics of exports `_0.._7`;
- exact dynamically derived filename passed to `QLibrary::setFileName`;
- exact internal checks performed by BattlEye;
- data collected or inspected by BattlEye;
- exact network endpoints/messages/protocol;
- exact `ptrace` usage, if any;
- packed/self-loader unpack/decryption/materialization algorithm;
- anti-debug, anti-tamper, detection/signature logic;
- any bypass, disabling, spoofing, stealth or evasion mechanism.

## Operational/non-claims boundary

None of the evidence in this report proves that a particular **current live** Tibia process presently has `BEClient.so` loaded.

The package relationship and exact-build client integration are established statically at the evidence levels described above. Current canonical runtime identity remains governed separately by Track A runtime admission; historical process/display/port observations are not current authority.

This research performed no target execution, no `dlopen`/preload of `BEClient.so`, no live process-memory/maps inspection, no attach/debug/injection, no binary patching, no input/session mutation and no live BattlEye traffic analysis.

## Primary evidence provenance

### PR #326 — package presence

Successful read-only run:

```text
run 31932798483
job 95130062729
```

Established retained-package BattlEye files and exact-client presence without runtime mutation.

### PR #327 — `BEClient.so` static ELF/layout analysis

Successful runs:

```text
run 31933354934 / job 95131426738
run 31933401869 / job 95131548768
```

Established module identity, imports/exports, custom `.be0/.be1` layout, RWE/self-loading structural evidence and high entropy.

### PR #330 — exact client loader/`Init` ABI

Material successful runs/jobs:

```text
31933690981 / 95132257220
31934000853 / 95133025014
31934067682 / 95133184321
31934120792 / 95133309389
31934210106 / 95133530199
31934287388 / 95133715398
31934370065 / 95133912441
31934410062 / 95134006400
```

Established the QLibrary `Init` lifecycle, falsified the unrelated raw `dlopen/dlsym` audio path, proved the direct resolved `Init` call, and established that `BEClient.so` is the only exact-package ELF exporting exact `Init`.

### PR #332 — client-side output/callback lifecycle

Successful runs/jobs:

```text
31935025020 / 95135467968
31935171570 / 95135821982
31935234113 / 95135972836
31935315153 / 95136163740
31935419481 / 95136403149
```

The final deterministic validator `31935419481 / 95136403149` re-derived load-bearing byte anchors from the exact fenced client and reported:

```text
VALIDATOR_EXECUTED_TARGET=false
VALIDATOR_LIVE_RUNTIME_OBSERVED=false
VALIDATOR_MUTATION_PERFORMED=false
```

It validated:

- `[owner+0x748]` state load at `0x6fc4d7`;
- state-local assignment at `0x6fc4eb`;
- local overwrite boundary at `0x6fc82d`;
- pre-init `+0x28` function-pointer call sequence;
- 32-byte clear and QLibrary unload;
- exact `resolve("Init")` anchor;
- observed `Init` argument/call sequence;
- post-success `+0x30` function-pointer call sequence;
- `+0x49` control-byte use;
- shared reset lifecycle `0x7319e0`;
- independent owner cleanup `0x7019c7..0x701aab`;
- resolve-null reset;
- bounded count of eight common direct owner `+0x748` loads.

## Safe continuation guidance

Safe future work may continue to study the **legitimate client-facing ABI/lifecycle** through static official-client evidence, version-to-version compatibility, and governance-compliant module-presence observations when needed.

Do not use this report as a basis for disabling or evading BattlEye. Internal protection mechanisms, patch points, stealth/evasion, anti-debug defeat, signature neutralization and equivalent anti-cheat bypass work are outside this report's scope.
