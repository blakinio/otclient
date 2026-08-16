# Official Linux Tibia filesystem-helper resolver report

Date: 2026-08-16  
Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Task: `OTC-20260816-track-a-filesystem-helper-resolver-static`  
Scope: exact-build static retained-file evidence only

## Purpose

Recover the client-side filesystem/path transformation beneath the already-proven `tibia::shared::TTibiaFileSystemHelper` `"BEClient"` wrapper and determine the exact symbolic/dynamic `QString` formula whose result is passed to the previously proven `QLibrary::setFileName` call.

This report extends and partially supersedes the earlier uncertainty boundary in:

- `docs/agents/reports/OTCLIENT-20260816-beclient-path-static.md`;
- `docs/agents/reports/OTCLIENT-20260816-path-service-rtti-static.md`;
- `docs/agents/reports/OTCLIENT-20260816-filesystem-helper-owner-provenance.md`.

The earlier statement that the concrete QLibrary filename/path was wholly `UNKNOWN` is superseded as follows: the exact client now has a **PROVEN symbolic/dynamic path-construction formula** and a **PROVEN relative suffix `BattlEye/BEClient`**. The runtime value of the application-directory prefix and the exact filesystem object ultimately mapped by QLibrary remain distinct questions.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Every material static probe revalidated this exact file before inspection.

## Final result

Define the directly recovered helper operation `J(components)` as:

```text
accumulator = empty QString
for each 24-byte QString component C in order:
    accumulator.append("/")
    accumulator.append(C)
return QDir::toNativeSeparators(accumulator)
```

For the exact `BEClient` loader key, the exact symbolic construction is:

```text
J([
  J([
    QCoreApplication::applicationDirPath(),
    "BattlEye"
  ]),
  "BEClient"
])
```

Evidence classification:

```yaml
shared_TFileSystemHelper_slot_0x78: PROVEN_0xcfa5e0
join_algorithm_J: PROVEN
category_9_root_component: PROVEN_QCoreApplication_applicationDirPath
category_9_subdirectory_component: PROVEN_BattlEye
terminal_key: PROVEN_BEClient
client_generated_extension: NONE
qlibrary_input_symbolic_formula: PROVEN
path_equivalent_relative_suffix: PROVEN_BattlEye/BEClient
runtime_application_directory_value: DYNAMIC
exact_character_for_character_runtime_QString: DYNAMIC
exact_filesystem_object_finally_mapped_by_QLibrary: UNKNOWN
```

A human-readable path-equivalent description is:

```text
<QCoreApplication::applicationDirPath()>/BattlEye/BEClient
```

The symbolic `J(...)` expression above is the authoritative exact client-construction description. The path-equivalent shorthand must not be used to claim an exact character-for-character runtime string because `J` explicitly inserts separators and `applicationDirPath()` is runtime-derived.

## PROVEN — base helper identity and resolver slot

The exact client contains:

```text
shared::TFileSystemHelper
mangled: N6shared17TFileSystemHelperE
typeinfo: 0x3070918
primary vtable address point: 0x2f61f90
vtable +0x78 -> 0xcfa5e0
```

The final deterministic validator re-derived the Itanium RTTI/vtable relation before accepting the slot mapping.

The predecessor provenance report independently proved that `TTibiaFileSystemHelper+0x18/+0x20` owns a shared pointer to the underlying `shared::TFileSystemHelper` object. The `TTibiaFileSystemHelper+0x30` method reads that exact member, loads the member vtable slot `+0x78`, and delegates through it.

## PROVEN — exact `J(components)` implementation at `0xcfa5e0`

Function `0xcfa5e0`, `shared::TFileSystemHelper::vtable+0x78`, consumes a begin/end pair for a sequence of 24-byte QString objects:

```text
0xcfa5f5  RBX = [RDX]       # begin
0xcfa5f8  R12 = [RDX+0x8]  # end
...
0xcfa685  RBX += 0x18
0xcfa689  compare against end
```

For every element it copies one 24-byte QString, then performs:

```text
0xcfa615  exact literal "/"
0xcfa646  setup accumulator.append("/")
0xcfa651  QString::append(QBasicUtf8StringView<false>)
0xcfa656  setup accumulator.append(component)
0xcfa65c  QString::append(QString const&)
```

After all components:

```text
0xcfa708  setup output + accumulated QString
0xcfa70e  QDir::toNativeSeparators(QString const&)
```

The relevant exact PLT identities are:

```text
0x4ddaf0  QString::append(QBasicUtf8StringView<false>)
0x4de970  QString::append(QString const&)
0x4db340  QDir::toNativeSeparators(QString const&)
```

Immutable window:

```yaml
va: 0xcfa5e0..0xcfa75f
sha256: 53a7479bca7733730fe513f76638d31eaa16cf58abad3ad65bafa8396685b16a
```

## PROVEN — the outer resolver receives exactly `[slot28(category), key]`

`TTibiaFileSystemHelper::vtable+0x30 -> 0xc9b890` first invokes the same object's slot `+0x28`, then builds a two-element sequence:

```text
element 0 = result of TTibiaFileSystemHelper +0x28(category)
element 1 = caller key QString
```

Exact anchors include:

```text
0xc9b8a7  call own slot +0x28
0xc9b8b7  copy slot+0x28 result
0xc9b8df  copy caller key argument
0xc9b905  allocate 0x30 bytes = 2 * 0x18-byte QString elements
0xc9b8ce  load base-helper slot +0x78
0xc9b96f  call base-helper +0x78 with the two-element sequence
```

Immutable window:

```yaml
va: 0xc9b890..0xc9ba1f
sha256: 5d3257ac75e63766f25c671efd49fd6c64920c7e158bd5e112b9eb99fc91fec2
```

For the BattlEye-associated wrapper, the caller key is independently PROVEN to be `"BEClient"`.

## PROVEN — `TTibiaFileSystemHelper +0xd8` supplies key `BEClient` and category `9`

The continuous primary vtable maps:

```text
TTibiaFileSystemHelper +0xd8 -> 0xc95cb0
```

At this wrapper:

```text
0xc95cb2  exact literal "BEClient"
0xc95cca  length = 8
0xc95cd9  QString::fromUtf8(...)
0xc95ce1  EDX = 9
0xc95cec  call same object's slot +0x30
```

Thus the relevant invocation is directly:

```text
slot30(category=9, key="BEClient")
```

No source-level enum/name is assigned to category `9`; its path behavior is established below by the exact switch cases.

## PROVEN — slot `+0x28` resolves category into two path components

`TTibiaFileSystemHelper::vtable+0x28 -> 0xc9b620` saves the incoming category and invokes:

```text
own +0x18(category)
own +0x10(category)
```

When the `+0x10` result is present, it builds another two-QString sequence from those results and invokes the same base helper `J` operation.

Exact anchors:

```text
0xc9b624  save EDX category
0xc9b64a  call own slot +0x18
0xc9b651  pass saved category to own slot +0x10
```

Immutable window:

```yaml
va: 0xc9b620..0xc9b88f
sha256: e1ad52aa1fa5a1a83930e1e37e97150269044a2520cddf8675cb61c675193e36
```

## PROVEN — category `9` root is `QCoreApplication::applicationDirPath()`

Relevant vtable mappings:

```text
TTibiaFileSystemHelper +0x18 -> 0xc91200
TTibiaFileSystemHelper +0x10 -> 0xc8f6e0
```

Both methods dispatch categories `0..15` through static jump tables.

For index `9`:

```text
+0x18 jump table 0x1d68a4c -> 0xc91230
+0x10 jump table 0x1d689f8 -> 0xc8f8e0
```

The `+0x18(9)` case is:

```text
0xc91230  direct call -> 0x4e0050
```

and exact dynamic symbol resolution identifies:

```text
0x4e0050  QCoreApplication::applicationDirPath()
```

Therefore the first category-9 component is directly the application-directory QString.

## PROVEN — category `9` subdirectory is exact QString `"BattlEye"`

The `+0x10(9)` case at `0xc8f8e0` copies the 24-byte global QString object at:

```text
0x31964a0
```

That object is runtime-initialized storage, so its raw on-disk bytes alone are not meaningful. The static initializer was traced instead.

Exact instruction-boundary initializer chain:

```text
0x613463  load exact global object address 0x31964a0
0x61346a  load exact literal "BattlEye" at 0x1d7b160
0x613471  pass global object as destination
0x613474  call helper 0x6b2350
```

Tiny immutable initializer window:

```yaml
va: 0x613450..0x6134bf
sha256: 0facd17d377cc00b14d728a2a5fda15fdb323098cbf99d6c1c9887be8e403f08
```

Helper `0x6b2350` preserves the output and source C-string arguments and invokes:

```text
0x6b236c -> strlen
0x6b237b -> QString::fromUtf8(QByteArrayView)
```

Immutable helper window:

```yaml
va: 0x6b2350..0x6b24bf
sha256: 2b69a06ad9f6726536251b137d461be7bf170abe68c46d620c3ed2ea4f308390
```

The adjacent initializer sequence also registers destruction through `__cxa_atexit`, consistent with runtime construction of a global non-trivial QString object.

Therefore:

```text
TTibiaFileSystemHelper +0x10(category 9) = QString("BattlEye")
```

is directly established from the static initializer, not inferred from a raw string xref.

## PROVEN symbolic path formula

Combining the exact client-side call graph:

```text
category9_root = QCoreApplication::applicationDirPath()
category9_subdir = "BattlEye"
category9_path = J([category9_root, category9_subdir])
terminal_key = "BEClient"
qlibrary_name = J([category9_path, terminal_key])
```

Therefore the authoritative symbolic formula is:

```text
J([J([QCoreApplication::applicationDirPath(), "BattlEye"]), "BEClient"])
```

and the stable path-equivalent suffix is:

```text
BattlEye/BEClient
```

The predecessor filename-data-flow report proved that the result of this loader-path `+0xd8` call is the exact non-trivial value later passed to:

```text
QLibrary::setFileName @ 0x6fcaba
```

Thus the **client-generated QLibrary input formula is now PROVEN**, while its application-directory prefix remains runtime-derived.

## Extension boundary

The client-side formula recovered here contains:

```text
BEClient
```

not:

```text
BEClient.so
```

No `.so` suffix is appended anywhere in this proven client-side resolver chain. This is a direct client-code fact.

It does **not** by itself prove which final filesystem object QLibrary maps. Platform-specific QLibrary suffix/prefix resolution is a separate layer and remains outside the direct client resolver proof in this report.

## Corrections / rejected exploratory evidence

### Raw global xref census

One exploratory probe performed a broad raw scan for references to the category global and `"BattlEye"` literal. As with the earlier rejected global `+0xd8` census, such a raw byte sweep is not accepted as instruction-boundary-safe semantic evidence.

Only the exact adjacent initializer instructions at `0x613463`, `0x61346a`, `0x613471`, and `0x613474` are retained after exact-boundary validation.

### Runtime global raw bytes

An earlier probe tried to read the raw bytes of global QString object `0x31964a0` directly from the file. That approach is invalid for this runtime-initialized storage and the probe failed. The value was instead recovered from its exact static initializer as described above.

### `objdump` availability

A diagnostic attempt to use `objdump` on the Synology runner failed because the command is not installed. No semantic conclusion is retained from that failed run; final proof uses exact-byte, relocation, RTTI and PLT anchors only.

## Deterministic validator

Final semantic validator:

```text
run: 31942437204
job: 95153445603
result: SUCCESS
```

It re-derived in one run:

```text
TTibiaFileSystemHelper RTTI/vtable
shared::TFileSystemHelper RTTI/vtable +0x78 -> 0xcfa5e0
all relevant Qt/strlen/__cxa_atexit PLT identities
BEClient key + category 9 wrapper
slot+0x30 two-element [slot28,key] construction
slot+0x28 category forwarding
category-9 jump-table targets
category-9 applicationDirPath root
category-9 global QString source
exact BattlEye global initializer
base J slash/component loop
QDir::toNativeSeparators final conversion
immutable evidence-window hashes
```

Final validator outputs include:

```text
VALIDATOR_PATH_JOIN_OPERATOR=J(components):append("/");append(component);QDir::toNativeSeparators
VALIDATOR_PATH_FORMULA=J([J([QCoreApplication::applicationDirPath(),"BattlEye"]),"BEClient"])
VALIDATOR_PATH_EQUIVALENT_SUFFIX=BattlEye/BEClient
VALIDATOR_SET_FILENAME_EXTENSION_IN_CLIENT_FORMULA=NONE
VALIDATOR_RUNTIME_ABSOLUTE_PREFIX=DYNAMIC_APPLICATION_DIR_PATH
VALIDATOR_EXECUTED_TARGET=false
VALIDATOR_LIVE_RUNTIME_OBSERVED=false
VALIDATOR_MUTATION_PERFORMED=false
```

## Material evidence provenance

```text
31941609207 / 95151515942  base-helper RTTI/+0x78 and caller correlation
31941660701 / 95151640998  exact base-resolver/slash/caller windows
31941716491 / 95151777224  Qt append/toNativeSeparators symbol mapping
31941768535 / 95151899494  TTibia +0x28 and outer two-QString construction
31941829706 / 95152041120  +0x10/+0x18 category switch and category forwarding
31941909566 / 95152225148  exact category-9 jump-table cases
31942173414 / 95152833368  exact BattlEye global/literal initializer boundary
31942213755 / 95152924982  initializer helper -> strlen + QString::fromUtf8
31942437204 / 95153445603  deterministic final path-formula validator: SUCCESS
```

Non-load-bearing diagnostic failures/corrections are recorded above and are not used as positive evidence.

## Remaining UNKNOWN / next layer

The client-generated resolver is now sufficiently reduced. Remaining questions are downstream of `QLibrary::setFileName`:

- exact runtime value of `QCoreApplication::applicationDirPath()` for a particular live invocation;
- exact character-for-character normalization performed by Qt around leading/native separators at runtime;
- exact platform-specific QLibrary candidate-name expansion for extensionless `BEClient`;
- exact filesystem path ultimately opened/mapped by QLibrary;
- whether the mapped object can be promoted from the existing high-confidence package/`Init` correlation to direct static platform-resolution proof.

Those belong to a separate QLibrary/platform-resolution task and must not be conflated with the now-PROVEN client-side formula.

## Safety boundary

All work was static exact-file client analysis. No Tibia/BattlEye execution/loading, live `/proc`, process memory/maps, attach/debug/injection, input/network/session/credential mutation, binary patching, unpacking, anti-debug/detection research, packet/protocol inspection, disabling, spoofing, stealth or bypass/evasion work occurred.
