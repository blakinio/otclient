# Official Linux Tibia BEClient `QLibrary::setFileName` static data-flow report

Date: 2026-08-16  
Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Task: `OTC-20260816-track-a-beclient-path-static`  
Scope: exact-build static retained-file evidence only

## Objective

Determine whether the exact official native Linux Tibia client statically reveals the concrete filename/path passed to the previously proven BattlEye-associated `QLibrary::setFileName` call at client VA `0x6fcaba`.

This extends `docs/agents/reports/OTCLIENT-20260816-beclient-static-integration.md` without changing its prior boundaries: the exact package still has only one ELF exporting exact `Init`, `bin/BattlEye/BEClient.so`, while the direct concrete filename flow into `QLibrary` had remained `UNKNOWN`.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Every semantic runner probe revalidated this fence before reading the file.

## Result

```yaml
concrete_qlibrary_filename: UNKNOWN
construction_mode: dynamic_client_generated_QString
client_dataflow_to_setFileName: PROVEN
exact_package_unique_Init_exporter: bin/BattlEye/BEClient.so
client_to_BEClient_linkage: DERIVED_HIGH_CONFIDENCE
```

The concrete runtime `QString` value itself was **not** reduced to a literal path. This task therefore does not promote `bin/BattlEye/BEClient.so` as the directly observed `setFileName` argument.

## PROVEN loader-specific data flow

The final deterministic validator, run `31938495208`, job `95144070320`, completed successfully and re-derived these exact instruction-boundary facts from the fenced client.

### 1. Shared service getter

At `0x6fc4f2` the client makes a direct relative call to internal helper:

```text
0x6ba0b0
```

Earlier bounded helper disassembly showed this helper copies a shared-pointer-like pair from the owner object at offsets `+0x20/+0x28` into the caller-provided local result and performs the corresponding reference-count handling.

This service is not BattlEye-specific: a separate exact-client callsite census found 27 direct callers of helper `0x6ba0b0`, with unrelated semantic contexts including minimap, chat/UI, map window and `sessiondumps` code. The exact service class name remains `UNKNOWN`.

### 2. Service object to local string-like return object

Immediately after the helper call the loader-specific path performs:

```text
0x6fc4f7  load service object pointer from local [rbp-0xd0]
0x6fc4fe  take address of local [rbp-0xc0]
0x6fc505  save that local result address at [rbp-0x138]
0x6fc50c  prepare the local result pointer, load the service vptr,
          and call virtual slot +0xd8
```

The final validator checked the exact opcode sequence at each of those instruction boundaries.

The register arrangement is consistent with an ABI pattern where a non-trivial return object is written through a hidden return buffer while the service object is passed as the instance argument. In the surrounding Qt data flow the produced object is consumed as the value passed to `QLibrary::setFileName`; describing the source-level method name or service class is still `UNKNOWN`.

### 3. Same local object reaches `QLibrary::setFileName`

The pointer saved at `[rbp-0x138]` is later loaded into the argument register at `0x6fcab0`; the embedded QLibrary object is selected as the receiver, followed by:

```text
0x6fcaba  QLibrary::setFileName(...)
0x6fcac2  QLibrary::load()
```

The deterministic validator resolved the two relative calls back to the already established PLT targets:

```text
QLibrary::setFileName -> 0x4db830
QLibrary::load        -> 0x4dc340
```

Therefore the loader-specific client data flow is directly established as:

```text
owner shared service (+0x20/+0x28)
  -> helper 0x6ba0b0
  -> service object
  -> virtual method slot +0xd8
  -> local non-trivial string/result object at [rbp-0xc0]
  -> saved pointer [rbp-0x138]
  -> QLibrary::setFileName
  -> QLibrary::load
  -> QLibrary::resolve("Init")
```

The last `resolve("Init")` stage and the unique exact-package `BEClient.so` exporter were already established by the predecessor report.

## PROVEN absence of tested direct filename literals

The final validator searched the exact client bytes for these complete filename/path literals and found zero occurrences:

```text
ASCII:    BEClient.so
ASCII:    BattlEye/BEClient.so
ASCII:    /BattlEye/BEClient.so
UTF-16LE: BEClient.so
UTF-16LE: BattlEye/BEClient.so
```

This proves only the absence of those exact complete literals in those encodings. It does **not** prove that the runtime `QString` cannot evaluate to one of those paths; the value may be composed, provided by the service, encoded differently, or depend on installation/runtime state.

The client still contains shorter/general strings such as `BattlEye` and `BEClient`, but their previously identified xrefs are not the proven loader value source.

## DERIVED interpretation

The strongest bounded interpretation is:

1. the official client does **not** feed `QLibrary::setFileName` from an obvious direct `BEClient.so` literal in the tested encodings;
2. instead it obtains the loader value through a broadly shared client service and a virtual string-producing method;
3. the exact package contains exactly one ELF exporting the exact `Init` that this QLibrary path resolves: `bin/BattlEye/BEClient.so`;
4. therefore the client-to-`BEClient.so` linkage remains **high-confidence DERIVED**, while the concrete dynamic `QString` value/path remains **UNKNOWN**.

## Corrected / rejected instrumentation

### GDB availability

Initial run `31938041809` / job `95142953265` proved GDB was unavailable on `synology-otclient-01`. No target execution was attempted; analysis continued using bounded exact-client byte windows and offline decoding.

### Raw global `vtable+0xd8` census — DISPROVEN as evidence

An exploratory raw-byte sweep attempted to count client-wide `CALL r/m64` patterns with displacement `0xd8`. A later deterministic validator exposed that this sweep was **not instruction-boundary-safe** and therefore produced false positives by interpreting byte sequences inside other instructions.

Consequently:

```yaml
previous_global_d8_count: REJECTED
semantic_conclusion_from_global_d8_count: NONE
```

No client-wide numerical claim for `vtable+0xd8` callsites is retained from that scanner.

This correction does not affect the loader-specific `0x6fc50c..0x6fc512` call, which is validated at a known exact instruction boundary and inside two immutable bounded windows.

## Bounded evidence provenance

Successful/material runs:

```text
31938041809 / 95142953265  GDB availability + relevant literal/string inventory
31938092847 / 95143078419  bounded loader/helper byte extraction
31938126533 / 95143159436  narrow filename data-flow windows
31938202217 / 95143350273  helper 0x6ba0b0 caller census / service-context evidence
31938263883 / 95143505149  loader getter/virtual-slot/setFileName anchor correlation
31938348199 / 95143716438  exploratory raw +0xd8 sweep; numerical census later rejected
31938451474 / 95143965655  validator attempt; load-bearing data-flow assertions passed, but run failed on rejected raw census assertion
31938495208 / 95144070320  final deterministic loader-specific validator: SUCCESS
```

Final validator immutable bounded-window checks:

```yaml
owner_producer_window:
  va: 0x6fc450..0x6fc53f
  sha256: f5a9738658cefa902916c6e563507a78e948c8d56b2540b3f0055cacc1023e66
setfilename_window:
  va: 0x6fca70..0x6fcadf
  sha256: c93526b7b9f5d341f9a860a5639a24f8bf8f545a52c228e11fa399bce4eafc6e
```

Final safety outputs:

```text
VALIDATOR_CONCRETE_FILENAME=UNKNOWN_DYNAMIC_QSTRING
VALIDATOR_EXECUTED_TARGET=false
VALIDATOR_LIVE_RUNTIME_OBSERVED=false
VALIDATOR_MUTATION_PERFORMED=false
```

## Remaining UNKNOWN

- exact source-level class of the shared owner `+0x20/+0x28` service;
- exact source-level name/signature of its loader-path virtual method at slot `+0xd8`;
- concrete runtime `QString` returned by that method;
- whether the returned string is absolute, relative, extensionless, platform-resolved, or transformed by Qt before the final library mapping;
- the exact filesystem path ultimately opened at runtime;
- any version-dependent difference on future official client builds.

No BattlEye internal checks, packed implementation, anti-debug/anti-tamper behavior, network protocol, patch point, disabling, spoofing, stealth or evasion mechanism was inspected or derived.

## Safe next research boundary

A future static task may identify the **client service type and virtual method name** by tracing the construction/type information of the shared owner `+0x20/+0x28` service, provided it remains limited to legitimate client-side path/resource architecture.

A runtime observation of the resolved QLibrary filename would be a different task and would require fresh Track A runtime admission/ownership evidence; this report does not authorize or perform it.
