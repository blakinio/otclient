# Official Linux Tibia filesystem-helper ownership provenance report

Date: 2026-08-16  
Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Task: `OTC-20260816-track-a-filesystem-helper-owner-provenance`  
Scope: exact-build static retained-file evidence only

## Purpose

Close as much as statically possible of the ownership-provenance gap left by `OTCLIENT-20260816-path-service-rtti-static.md`: trace the already proven `tibia::shared::TTibiaFileSystemHelper` object through application bootstrap and game-client construction into the `+0x20/+0x28` shared-pointer pair used by client code, while keeping the exact dynamic type of the separate loader callback receiver at `0x6fc034` distinct unless it can be proved directly.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

All semantic probes revalidated this exact file before static inspection.

## Final result

```yaml
ttibia_filesystem_helper_type: tibia::shared::TTibiaFileSystemHelper
ttibia_filesystem_helper_vptr: 0x2f62080
tgameapplication_plus_0x18_0x20: PROVEN_shared_ptr_to_TTibiaFileSystemHelper
tgameclient_plus_0x20_0x28: PROVEN_shared_ptr_to_TTibiaFileSystemHelper
tgameclient_plus_0x748: PROVEN_member_of_same_constructed_TGameClient_layout
loader_receiver_plus_0x20_0x28_plus_0x748_shape: PROVEN
loader_receiver_exact_dynamic_type: NOT_DIRECTLY_PROVEN
loader_receiver_TGameClient_layout_correlation: DERIVED_HIGH_CONFIDENCE
```

The material advance is direct: the `TTibiaFileSystemHelper` shared-pointer object/control-block pair is now followed instruction-by-instruction into `tibia::client::TGameApplication+0x18/+0x20`, and from that same application object into a freshly constructed `tibia::client::TGameClient+0x20/+0x28`.

## PROVEN — `TTibiaFileSystemHelper` construction and its internal base helper

The predecessor task established the class identity. This task revalidated it and recovered its bootstrap ownership flow.

Exact class facts:

```text
tibia::shared::TTibiaFileSystemHelper
mangled: N5tibia6shared22TTibiaFileSystemHelperE
typeinfo: 0x3070940
primary vtable address point: 0x2f62080
```

At bootstrap:

```text
0x5ef4ee  allocate 0x38-byte shared allocation
0x5ef4f7  RBp = allocation/control-block base
0x5ef4fa  R15 = allocation + 0x10 = embedded TTibiaFileSystemHelper object
0x5ef510  materialize exact vptr 0x2f62080
0x5ef517  store concrete TTibiaFileSystemHelper vptr
```

A first allocation creates the underlying `shared::TFileSystemHelper` object. The concrete TTibia helper then stores a shared-pointer-like pair to that base helper:

```text
0x5ef540  [control+0x30] = R14   -> TTibia object +0x20 = base-helper control block
0x5ef544  [control+0x28] = RAX   -> TTibia object +0x18 = base-helper object pointer
```

Therefore the previously unnamed `TTibiaFileSystemHelper+0x18/+0x20` member is directly established as the object/control-block pair for its underlying shared filesystem helper.

## PROVEN — bootstrap stores the TTibia shared pointer in `TGameApplication+0x18/+0x20`

The bootstrap function uses:

```text
0x5ef458  R12 = RSP + 0x70
```

as the base of the stack-resident application object.

After the `TTibiaFileSystemHelper` shared allocation is constructed:

```text
0x5ef570  [RSP+0x90] = RBP  -> application +0x20 = TTibia control block
0x5ef578  [RSP+0x88] = R15  -> application +0x18 = TTibia object pointer
```

because `R12 = RSP+0x70`.

The same stack object is subsequently assigned the exact derived application vptr:

```text
0x5ef6ba  materialize 0x3076bd0
0x5ef6cd  [RSP+0x70] = 0x3076bd0
```

RTTI/relocation validation proves:

```text
tibia::client::TGameApplication
mangled: N5tibia6client16TGameApplicationE
typeinfo: 0x3073958
vptr: 0x3076bd0
vtable +0x78 -> 0x6c9760
```

Thus the object/control-block pair at `TGameApplication+0x18/+0x20` is directly the freshly constructed `shared_ptr`-like ownership pair for `TTibiaFileSystemHelper`.

## PROVEN — the same application object is passed into the TGameClient factory

Bootstrap passes the same `R12` application object into its exact virtual slot `+0x78`:

```text
0x5ef82b  RDI = R12
0x5ef82e  call 0x6c9760
```

Function `0x6c9760` belongs to `TGameApplication::vtable+0x78`. Its entry preserves the receiver:

```text
0x6c977b  RBX = RDI
```

Later in the same function:

```text
0x6ca12e  RDI = RBX
0x6ca131  call 0x6c8020
```

Therefore `0x6c8020` receives the identical `TGameApplication*` as its first observed argument.

## PROVEN — TGameClient factory copies the TTibia pair directly into `TGameClient+0x20/+0x28`

The factory at `0x6c8020` starts with:

```text
0x6c8028  R14 = RDI
```

so `R14` is the application source object.

It then reads the exact application pair:

```text
0x6c80c6  RSI = [R14+0x18]   # TTibia object pointer
0x6c80ca  R13 = [R14+0x20]   # TTibia control block
```

and transfers it into the freshly allocated client object held in `R12`:

```text
0x6c814f  [R12+0x28] = R13
0x6c8172  reload TTibia object pointer
0x6c8182  [R12+0x20] = object pointer
```

The same newly allocated `R12` object is then assigned the exact derived vptr:

```text
0x6c844c  materialize 0x3076908
0x6c8463  [R12] = 0x3076908
```

RTTI proves:

```text
tibia::client::TGameClient
mangled: N5tibia6client11TGameClientE
typeinfo: 0x3070398
primary vptr: 0x3076908
```

Therefore this is a direct provenance result, not a class-layout guess:

```text
TGameClient+0x20  = TTibiaFileSystemHelper object pointer
TGameClient+0x28  = the same TTibiaFileSystemHelper shared control block
```

at this exact construction path.

## PROVEN — `+0x748` belongs to the same constructed TGameClient layout

Within the same `R12` TGameClient construction:

```text
0x6c8507  LEA RDI,[R12+0x748]
```

Later the same factory/constructor flow reads:

```text
0x6c8a96  RBX = [R12+0x748]
```

This establishes `+0x748` as a member of the exact constructed `TGameClient` layout. It is the same offset used by the previously bounded BattlEye-associated state path.

## PROVEN — loader receiver shape

The separate loader-side function beginning at `0x6fc034` has:

```text
0x6fc041  RBX = RDI          # receiver retained as RBX
0x6fc4d7  R14 = [RBX+0x748]
0x6fc4de  RSI = RBX
0x6fc4f2  call 0x6ba0b0
```

Helper `0x6ba0b0` directly reads:

```text
0x6ba0b0  [RSI+0x20]
0x6ba0bd  [RSI+0x28]
```

and returns/copies that shared-pointer-like pair.

Thus the loader receiver is directly proven to expose the same three relevant offsets:

```text
+0x20/+0x28  shared pointer getter source
+0x748        BattlEye-associated state member
```

that were independently established in the exact `TGameClient` construction layout.

## DERIVED — loader receiver is a TGameClient-layout object

The exact correspondence is strong:

1. a concrete `TGameClient` is built with direct `TTibiaFileSystemHelper` ownership at `+0x20/+0x28`;
2. the same concrete construction owns and consumes member `+0x748`;
3. the loader receiver reads exactly `+0x748` and passes itself into the exact `+0x20/+0x28` getter;
4. surrounding predecessor work already established the returned service's `+0xd8` path into `QLibrary::setFileName`.

This supports **high-confidence DERIVED** identification of the loader receiver as a `TGameClient`-layout object.

However the task did not find an instruction-boundary-safe direct call, direct code-address materialization, relocation, or raw qword registration for exact entry `0x6fc034`. Therefore the exact dynamic type/source-level method ownership of that callback/function entry is deliberately **not promoted to PROVEN**.

## Important evidence boundary

The following two claims must remain distinct:

```yaml
TGameClient_plus_0x20_plus_0x28_contains_TTibiaFileSystemHelper_shared_ptr: PROVEN
loader_receiver_exact_dynamic_type_is_TGameClient: NOT_DIRECTLY_PROVEN
```

This avoids laundering a very strong structural correlation into a direct class-provenance claim.

## Deterministic validator

Final semantic validator:

```text
run: 31941120670
job: 95150360284
result: SUCCESS
```

It independently re-derived:

```text
VALIDATOR_PASS=ttibia_rtti_vtable
VALIDATOR_PASS=ttibia_plus18_plus20_shared_base_filesystem_pair
VALIDATOR_PASS=ttibia_shared_ptr_to_tgameapplication_plus18_plus20
VALIDATOR_PASS=tgameapplication_this_to_tgameclient_factory
VALIDATOR_PASS=tgameclient_rtti_vtable
VALIDATOR_PASS=ttibia_shared_ptr_to_tgameclient_plus20_plus28_DIRECT
VALIDATOR_PASS=tgameclient_plus748_layout_member
VALIDATOR_PASS=loader_receiver_plus20_plus28_plus748_shape
```

and retained the explicit boundary:

```text
VALIDATOR_PROVENANCE=TGameApplication_plus18_plus20_and_TGameClient_plus20_plus28_DIRECT_TTibiaFileSystemHelper_SHARED_PTR
VALIDATOR_LOADER_RECEIVER_EXACT_DYNAMIC_TYPE=NOT_DIRECTLY_PROVEN
VALIDATOR_LOADER_RECEIVER_TGAMECLIENT_LAYOUT_CORRELATION=HIGH_CONFIDENCE_DERIVED
```

Immutable windows revalidated by the final run:

```yaml
bootstrap_ttibia:
  va: 0x5ef480..0x5ef58f
  sha256: a611ddea5178c1cb286340e51e635d544c27438962aacf32ba9c8b8b24110ae1
factory_pair:
  va: 0x6c80b0..0x6c818f
  sha256: 4865cefae5a364922a3d4dc0de7100865ac6df9ff79134e64291978beb5e1a8f
tgameclient_derived:
  va: 0x6c83c0..0x6c84bf
  sha256: cbb42f1e5b9aa36cd60a20d88ea9a6b03cf9eca39758aa82090b3828d94a1b19
plus748_init:
  va: 0x6c84d0..0x6c855f
  sha256: ebf87700d3ae62ec8bf69625f3742849eac93bbe02d61bb547329d7e9441733e
plus748_read:
  va: 0x6c8a70..0x6c8adf
  sha256: 2b17d8b56ac504acb9dd79a98474f45918eec10a40073225722fcc4555ae4b86
loader_pair:
  va: 0x6fc4c0..0x6fc52f
  sha256: 8ebe482d09736fb934f3bda7526eb34e270a838c50a62720348d99f6a0ce993f
```

## Corrections made during the task

A temporary heuristic initially treated `0x6c976e` as a function start. Further bounded control-flow analysis corrected this: the real function entry is `0x6c9760`; `0x6c976e` is simply inside its normal prologue. The final validator uses only the corrected boundary.

Exploratory searches for a direct reference to `0x6fc034` found no common direct-call, RIP-relative address materialization, `.rela.dyn` addend, or raw qword reference. These absence scans are **not** used as proof of global non-reference because they are not complete instruction/control-flow decoders; they only explain why the receiver's exact source-level ownership was not upgraded.

## Remaining UNKNOWN / NOT DIRECTLY PROVEN

- exact dynamic/source-level type of the first argument accepted at `0x6fc034`;
- source-level name/signature of the `0x6fc034` entry;
- exact mechanism that dispatches to that entry in the stripped binary;
- concrete runtime QString / final filesystem path ultimately handed to Qt after `BEClient` resolution.

## Safety boundary

All work was static exact-file analysis. No Tibia/BattlEye execution/loading, live `/proc`, process memory/maps, attach/debug/injection, input/network/session/credential mutation, binary patching, unpacking, anti-debug/detection research, protocol inspection, disabling, spoofing, stealth or bypass/evasion work occurred.

## Safe next research boundary

The strongest next client-side static direction is no longer ownership provenance; that is now direct through `TGameClient+0x20/+0x28`. A useful next step is to continue down the legitimate filesystem path architecture: identify the exact `shared::TFileSystemHelper` resolver path invoked beneath `TTibiaFileSystemHelper` and determine, if statically possible, how the key `"BEClient"` is transformed into the final QString supplied to `QLibrary::setFileName`, without inspecting BattlEye internals or anti-cheat behavior.
