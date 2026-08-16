---
task_id: OTC-20260816-track-a-beclient-static-analysis
status: completed
agent: ChatGPT
session_id: chatgpt-beclient-static-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: static-research
phase: elf-static-analysis
branch: research/OTC-20260816-track-a-beclient-static-analysis
base_branch: main
base_main: 3a5568f36ebc326afd246d0d2da45b5d8eecabfa
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-beclient-static-analysis
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 327
updated: 2026-08-16T09:16:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-beclient-static-analysis.md
modules_touched: []
reuses:
  - synology-otclient-01
  - retained PR #303 exact-client package artifact
  - GitHub-only temporary workflow pattern
depends_on:
  - current main Track A governance
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
runtime_platform: official_native_linux_only
static_run: 31933354934
static_job: 95131426738
layout_run: 31933401869
layout_job: 95131548768
validation_conclusion: success
e2e: NOT_APPLICABLE_STATIC_FILE_ANALYSIS
mutation_performed: false
next_action: none
---

# Objective

Statically characterize the retained official native Linux `BEClient.so` associated with exact Tibia client `15.32.df7b29`, focusing on ELF identity, size/hash, sections, hardening indicators, dynamic dependencies, imports/exports, selected capabilities suggested by symbol/string evidence, and obvious configuration/network markers.

# Direct evidence

Successful static-parser run `31933354934`, job `95131426738`; successful layout run `31933401869`, job `95131548768`, both on `synology-otclient-01`. The first attempt `31933291739` / `95131261442` failed only because the runner lacked `file`/`readelf`; the analysis was repaired to a Python-stdlib ELF parser and rerun successfully.

The exact neighboring Tibia client fence passed before analysis: version `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## BEClient.so identity

- size: `3620287` bytes (`0x373dbf`);
- SHA-256: `5d1c90ab244155d393296b2e575425aee3252d4d09110007a6d6c3a0bfe05a98`;
- MD5: `236976e08df0cc30e112c717dced235c`;
- ELF64, little-endian, `ET_DYN`, AMD x86-64;
- entry point: `0xc6bbec`;
- 9 program headers, 31 section headers;
- `.symtab`: absent; `.debug*`: absent; GNU build-id: absent;
- compiler comments: `GCC: (Ubuntu 4.8.4-2ubuntu1~14.04) 4.8.4` and `GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2`.

## Conventional hardening metadata

- GNU stack: `RW`, therefore NX stack is enabled;
- GNU RELRO: absent;
- `BIND_NOW`: absent;
- `TEXTREL`: absent;
- one executable load segment is explicitly `RWE`.

## Dynamic dependencies

Only four direct `DT_NEEDED` libraries were present:

- `libc.so.6`;
- `libdl.so.2`;
- `libstdc++.so.6`;
- `libgcc_s.so.1`.

No direct OpenSSL/cURL dependency was present.

## Dynamic API surface

119 imported dynamic symbols were observed. Important families include:

- memory/protection: `mmap`, `mprotect`, `munmap`;
- dynamic loader/introspection: `dlopen`, `dladdr`;
- networking: `socket`, `connect`, `send`, `sendto`, `recv`, `recvfrom`, `poll`, `select`, `gethostbyname`, `gethostname`, `getsockopt`;
- filesystem/process-environment inspection primitives: `open`, `fopen`, `opendir`, `readdir`, `readlink`, `ioctl`, `uname`;
- CPU/scheduling: `sched_getaffinity`, `sched_setaffinity`;
- process command execution primitive: `system`;
- timing: `clock_gettime`, `gettimeofday`, `time`, `usleep`;
- pthread mutex functions and standard C/C++ runtime support.

No direct dynamic import named `ptrace`, `process_vm_*`, `prctl`, `syscall`, `kill` or `tgkill` was present. However, the printable ASCII token `ptrace` is present in the file. Static evidence therefore proves awareness/reference to the token, not a specific ptrace call path.

The dynamic export surface contained the API-looking names `Init`, `GetVer`, `_0` through `_7`, plus the `BECLIENT_1.0` version namespace/symbol metadata. The binary is otherwise stripped.

## Printable-string surface

13,936 ASCII strings of length >=5 were found, but only seven matched the bounded BattlEye/debug/network/library filter:

- `BECLIENT_1.0`;
- `BEClient_x64.so`;
- `libc.so.6`;
- `libdl.so.2`;
- `libgcc_s.so.1`;
- `libstdc++.so.6`;
- `ptrace`.

No obvious plaintext URL/domain, `/proc/`, `/sys/` or `/dev/` path was surfaced by that filter. This is an absence-of-plaintext observation only, not proof that such resources are unused.

# Custom ELF layout — strongest finding

The ELF layout is highly non-standard and strongly protected/packed.

Key program headers:

- `LOAD RE` at `vaddr 0x0`, `filesz 0x270`, `memsz 0x3e0dc`;
- `LOAD RW` at `vaddr 0x200270`, `filesz 0`, `memsz 0x58338`;
- `LOAD RE` at `vaddr 0x400270`, `filesz 0`, `memsz 0x45fbd0`;
- `LOAD RWE` at `vaddr 0xa00270`, `offset 0x270`, `filesz=memsz=0x367de6`;
- final `LOAD RW` around `vaddr 0xf68060` containing dynamic tables.

The normal `.text` section exists in the file at offset/address `0x47c0`, size `0x2b879`, but the kernel-facing low-address executable `LOAD` segment has only `0x270` bytes of file data and a much larger zero-filled memory size. Therefore the normal `.text` bytes are not initially mapped to their declared low virtual addresses by the ELF loader.

Two custom executable sections exist:

- `.be0`: `addr 0x440300`, `offset 0x40300`, declared size `0x41fb40`; the declaration extends beyond end-of-file and lies in the large executable segment whose `filesz` is zero;
- `.be1`: `addr 0xa00270`, `offset 0x270`, size `0x367de6`; it is fully file-backed, mapped through the `RWE` load segment, and has measured entropy `7.790/8`.

The ELF entry point `0xc6bbec` lies inside `.be1`, not inside ordinary `.text`.

# Interpretation

**HIGH-CONFIDENCE INFERENCE:** `BEClient.so` uses a custom self-loading / self-mapping protection layer. The kernel initially maps the high-address `.be1` payload as read/write/execute, while several lower code/data ranges are largely zero-fill destinations. The entry point starts inside `.be1`; the imports `mmap`/`mprotect`/`munmap` and the unusual zero-file-size executable destinations are consistent with a bootstrap that reconstructs or materializes protected code/data into their runtime locations.

**HIGH-CONFIDENCE INFERENCE:** `.be1` is a packed/obfuscated loader/payload region rather than ordinary application code. Evidence: custom section name, entrypoint inside it, RWE mapping, very high entropy, stripped symbols/debug metadata, and unconventional overlapping/load layout.

**MEDIUM-CONFIDENCE INFERENCE:** `.be0` is likely a protected runtime destination or second-stage code area. Its declared executable range extends beyond EOF and sits in a `filesz=0` executable load region, which makes conventional static section interpretation unreliable and is consistent with anti-analysis/self-unpack techniques.

**UNKNOWN:** exact unpack/decryption algorithm, exact purpose of `_0.._7`, exact network endpoints/protocol, exact `ptrace` usage, and exact anti-debug/anti-tamper checks remain unproven by this bounded static pass.

# Safety / closeout

No library execution, `dlopen`, preload, attach, injection, debug, patch, process-memory inspection, credential access, Tibia launch/stop, runtime mutation, or anti-cheat bypass work occurred. The analysis remained static and read-only. Temporary workflows are removed before closing PR #327 unmerged.
