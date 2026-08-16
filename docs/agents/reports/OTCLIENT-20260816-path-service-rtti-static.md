# Official Linux Tibia QLibrary path-service RTTI report

Date: 2026-08-16  
Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Task: `OTC-20260816-track-a-path-service-rtti-static`  
Scope: exact-build static retained-file evidence only

## Purpose

Identify the concrete client-side class and virtual-method chain associated with the value producer that the predecessor report proved feeds `QLibrary::setFileName` before the exact client's `resolve("Init")` path.

This report extends and partially supersedes the uncertainty boundaries in:

- `docs/agents/reports/OTCLIENT-20260816-beclient-static-integration.md`;
- `docs/agents/reports/OTCLIENT-20260816-beclient-path-static.md`.

Specifically, the earlier statements that the service class was unknown and that the `BEClient` xref at `0xc95cb2` was not yet a proven loader-value source are superseded at the evidence levels described below.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

All semantic runner probes revalidated this exact file before static inspection.

## Final result

```yaml
filesystem_helper_rtti_type: tibia::shared::TTibiaFileSystemHelper
filesystem_helper_typeinfo: 0x3070940
filesystem_helper_vtable_address_point: 0x2f62080
filesystem_helper_slot_0x30: 0xc9b890
filesystem_helper_slot_0xd8: 0xc95cb0
slot_0xd8_exact_key: BEClient
slot_0xd8_client_role: DERIVED_BECLIENT_KEY_PATH_RESOLUTION_WRAPPER
loader_owner_plus_0x20_dynamic_type: NOT_DIRECTLY_PROVEN
source_level_method_name: UNKNOWN
concrete_runtime_qlibrary_filename: UNKNOWN
```

## PROVEN — exact RTTI and vtable identity

The exact binary contains the Itanium ABI type-name string:

```text
N5tibia6shared22TTibiaFileSystemHelperE
```

which demangles structurally to:

```text
tibia::shared::TTibiaFileSystemHelper
```

Exact locations:

```text
type-name string: 0x1c95880
typeinfo object:   0x3070940
vtable RTTI slot:  0x2f62078
offset-to-top:     0
vtable address point: 0x2f62080
```

The final deterministic validator re-derived that every relocation-backed virtual entry from `+0x00` through `+0xf8` at address point `0x2f62080` resolves into `.text`, with no intervening RTTI/vtable boundary. Relevant entries are:

```text
+0x28 -> 0xc9b620
+0x30 -> 0xc9b890
+0xd8 -> 0xc95cb0
```

This continuity matters because an earlier exploratory scan of similarly named helper candidates crossed adjacent vtable/typeinfo groups. Those other candidate `+0xd8` values are not retained as evidence. The `TTibiaFileSystemHelper` group is independently validated as continuous through `+0xd8`.

## PROVEN — concrete class construction exists in the exact client

The exact `TTibiaFileSystemHelper` vptr `0x2f62080` is written into embedded objects at at least two independent exact instruction-boundary sites:

```text
0x5ef510  RIP-relative LEA resolves to 0x2f62080
0x5ef517  stores that vptr into the constructed embedded object

0x19a6a9e RIP-relative LEA resolves to 0x2f62080
0x19a6aa8 stores that vptr into another constructed embedded object
```

This proves that the exact class is instantiated by the client; it is not merely dead RTTI/vtable metadata.

The task did **not** directly reduce either construction flow all the way to the loader owner's shared field at `owner+0x20/+0x28`. Therefore the exact dynamic type of that specific stored object remains `NOT_DIRECTLY_PROVEN` rather than being silently upgraded from correlation.

## PROVEN — `TTibiaFileSystemHelper` slot `+0xd8` is the `BEClient` wrapper

The continuous vtable maps:

```text
TTibiaFileSystemHelper vtable +0xd8 -> 0xc95cb0
```

The exact function at `0xc95cb0` begins by referencing:

```text
0xc95cb2 -> exact string VA 0x1d69bb2 -> "BEClient"
```

and uses exact length `8` while calling the already identified Qt function target at `0x4df210` (`QString::fromUtf8` in the predecessor PLT map).

Bounded instruction flow:

```text
0xc95cb0  function entry
0xc95cb2  load exact "BEClient" key address
0xc95cca  length = 8
0xc95cd9  call Qt string construction target 0x4df210
0xc95cd2  load this object's virtual slot +0x30 into a call register
0xc95ce1  place value 9 in EDX
0xc95cec  invoke slot +0x30
```

The function uses the caller-provided non-trivial return buffer as its output and delegates to another virtual method of the same `TTibiaFileSystemHelper` object after constructing the `BEClient` key.

The incoming/forwarded value `9` is a direct register fact. Its source-level enum/name/meaning is UNKNOWN and is not inferred.

The immutable exact-byte window:

```yaml
va: 0xc95cb0..0xc95d3f
sha256: 8b5dd5d81bd76f0c68e155a3598717eca8d4eeb121378da922fb044de11bfc81
```

was revalidated by the final semantic validator.

## PROVEN — slot `+0x30` is a generic delegation/resolution path

The same continuous vtable maps:

```text
TTibiaFileSystemHelper vtable +0x30 -> 0xc9b890
```

Exact bounded instruction anchors establish that this method:

1. calls the same object's virtual slot `+0x28` and captures a non-trivial result/context;
2. reads an object pointer from `this+0x18`;
3. loads that member object's vtable slot `+0x78`;
4. prepares a temporary collection/sequence-like block containing copied non-trivial values, including the caller-supplied `BEClient` key/context;
5. delegates through the member object's slot `+0x78` with the original output buffer.

Exact anchors include:

```text
0xc9b8a7..0xc9b8b2  call own slot +0x28
0xc9b8b3             load this+0x18 member
0xc9b8c1             load member vptr
0xc9b8ce             load member slot +0x78
0xc9b96f..0xc9b97a  prepare args and call that slot
```

The source type of the temporary sequence and the member at `this+0x18` are not named without direct type evidence. The exact semantic method name at `+0x30` remains UNKNOWN.

Immutable bounded window:

```yaml
va: 0xc9b820..0xc9bd1f
sha256: cf1d1280d15b447c45e8ae0cdacc8de9306838f60006d5b25b8261a5ef33e957
```

## DERIVED — client-side role of slot `+0xd8`

Combining only the proven client-side facts:

```text
predecessor loader data flow:
owner shared service
  -> virtual +0xd8
  -> local non-trivial result
  -> QLibrary::setFileName

this task:
TTibiaFileSystemHelper vtable +0xd8
  -> 0xc95cb0
  -> construct exact key "BEClient"
  -> same object's generic +0x30 resolution/delegation path
```

supports the high-confidence client-side role:

```text
TTibiaFileSystemHelper slot +0xd8
≈ BEClient-key path/resource resolution wrapper
```

This is a **DERIVED role description**, not a recovered source-level method name.

It also upgrades the earlier isolated `BEClient` xref interpretation: `0xc95cb2` is now causally connected to the exact class/vtable method shape matching the loader filename-producing virtual slot. The earlier observation that the string alone did not prove a loader remains historically correct; the new vtable + predecessor data-flow evidence supplies the missing causal link.

## What remains UNKNOWN

The following are deliberately not promoted beyond the evidence:

- direct assignment proving that the exact loader owner field `+0x20/+0x28` always contains a `TTibiaFileSystemHelper` instance;
- exact source-level name/signature of virtual slots `+0xd8`, `+0x30`, `+0x28` or the member object's `+0x78`;
- source-level meaning of forwarded value `9`;
- exact type of the member at `TTibiaFileSystemHelper+0x18`;
- exact type of the temporary collection/sequence in `0xc9b890`;
- concrete runtime `QString` returned to `QLibrary::setFileName`;
- whether Qt receives an extensionless key, relative name, platform-resolved library name, or already-complete filesystem path at the final call boundary;
- exact filesystem path ultimately opened at runtime.

The concrete QLibrary filename/path therefore remains `UNKNOWN` despite the newly proven `BEClient` key and class-level wrapper.

## Corrections and rejected evidence

### Other FileSystemHelper candidate `+0xd8` mappings

The first RTTI scan computed `+0xd8` mechanically after every typeinfo reference. Follow-up vtable-boundary validation showed that other similarly named helper regions encounter new RTTI/vtable groups before that offset. Their calculated `+0xd8` entries were therefore from adjacent objects/groups and are **REJECTED** as method mappings for those candidate classes.

`TTibiaFileSystemHelper` is different: its exact primary group remains relocation-backed `.text` continuously from `+0x00` through `+0xf8`.

### Direct owner-field dynamic-type claim

Class existence, exact vtable, concrete construction, and the `BEClient` wrapper are proven. The specific loader-owner shared field has not yet been traced from construction/assignment to consumption with a single causal chain. It remains `NOT_DIRECTLY_PROVEN` rather than being inferred from matching virtual behavior alone.

## Evidence provenance

Material successful runs/jobs:

```text
31938853042 / 95144958602  initial RTTI/relocation candidate discovery
31938968180 / 95145240491  candidate vtable-boundary validation and c95cb0 discovery
31939144527 / 95145667546  bounded concrete vtable, construction-site and generic-resolver windows
31939306766 / 95146060860  final deterministic validator: SUCCESS
```

Final deterministic validator passed all of:

```text
VALIDATOR_PASS=type_name:tibia::shared::TTibiaFileSystemHelper
VALIDATOR_PASS=itanium_offset_to_top_and_typeinfo
VALIDATOR_PASS=vtable_slots_0_to_f8_contiguous_text
VALIDATOR_PASS=slot30_0xc9b890
VALIDATOR_PASS=slotd8_0xc95cb0
VALIDATOR_PASS=two_concrete_vptr_construction_sites
VALIDATOR_PASS=slotd8_BEClient_wrapper_chain
VALIDATOR_PASS=slot30_generic_delegate_shape
VALIDATOR_PASS=slotd8_window_sha256:8b5dd5d81bd76f0c68e155a3598717eca8d4eeb121378da922fb044de11bfc81
VALIDATOR_PASS=slot30_window_sha256:cf1d1280d15b447c45e8ae0cdacc8de9306838f60006d5b25b8261a5ef33e957
VALIDATOR_OWNER_PLUS20_DYNAMIC_TYPE=NOT_DIRECTLY_PROVEN
VALIDATOR_SOURCE_METHOD_NAME=UNKNOWN_STRIPPED_BINARY
VALIDATOR_SLOT_D8_CLIENT_ROLE=BECLIENT_KEY_PATH_RESOLUTION_WRAPPER_DERIVED
VALIDATOR_EXECUTED_TARGET=false
VALIDATOR_LIVE_RUNTIME_OBSERVED=false
VALIDATOR_MUTATION_PERFORMED=false
```

## Safety boundary

All work was exact-file static analysis. No Tibia/BattlEye execution or loading, no live `/proc`, process memory/maps, attach/debug/injection, input, network/session/credentials, binary patching, unpacking, anti-debug/anti-tamper/detection analysis, network-protocol inspection, disabling, spoofing, stealth or bypass/evasion work occurred.

## Safe future boundary

A future static task could trace one of the two concrete `TTibiaFileSystemHelper` construction sites into the owner object's shared-field assignment to decide whether `owner+0x20/+0x28` can be upgraded from high-confidence class correlation to direct type provenance.

A separate path-architecture task could identify the type behind `TTibiaFileSystemHelper+0x18` and its slot `+0x78` if needed for legitimate client compatibility. Neither is required to retain the current class/vtable/`BEClient` wrapper proof.
