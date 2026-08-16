# Official Linux Tibia filesystem-helper resolver report

Date: 2026-08-16  
Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Task: `OTC-20260816-track-a-filesystem-helper-resolver-static`  
Scope: exact-build static retained-file evidence only

## Purpose

Recover the client-side filesystem/path transformation beneath the already-proven `tibia::shared::TTibiaFileSystemHelper` `"BEClient"` wrapper and determine the exact symbolic/dynamic `QString` formula whose result is passed to the previously proven `QLibrary::setFileName` call.

This report partially supersedes the earlier boundary that treated the concrete QLibrary filename/path as wholly `UNKNOWN`: the exact client now has a **PROVEN symbolic/dynamic path formula** and a **PROVEN stable relative suffix `BattlEye/BEClient`**. The runtime application-directory prefix and the exact filesystem object ultimately mapped by QLibrary remain separate downstream questions.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Every material probe revalidated this exact file.

## Final result

Define the recovered helper operation `J(components)`:

```text
accumulator = empty QString
for each 24-byte QString component C in order:
    accumulator.append("/")
    accumulator.append(C)
return QDir::toNativeSeparators(accumulator)
```

For the exact loader key:

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

Path-equivalent shorthand:

```text
<QCoreApplication::applicationDirPath()>/BattlEye/BEClient
```

The nested `J(...)` expression is the authoritative exact construction description; the shorthand must not be treated as an exact character-for-character runtime string.

## PROVEN — base helper and `J(components)`

Exact RTTI/vtable:

```text
shared::TFileSystemHelper
mangled: N6shared17TFileSystemHelperE
typeinfo: 0x3070918
primary vptr: 0x2f61f90
vtable +0x78 -> 0xcfa5e0
```

The predecessor ownership report proves `TTibiaFileSystemHelper+0x18/+0x20` owns this base helper. `TTibiaFileSystemHelper+0x30` reads that member and dispatches its `+0x78`.

`0xcfa5e0` consumes a begin/end pair of 24-byte QString elements. For each element it copies one QString, appends exact literal `"/"`, appends the QString, advances by `0x18`, then after all elements invokes `QDir::toNativeSeparators`.

Exact relevant calls:

```text
0xcfa651 -> QString::append(QBasicUtf8StringView<false>)
0xcfa65c -> QString::append(QString const&)
0xcfa70e -> QDir::toNativeSeparators(QString const&)
```

Immutable window:

```yaml
va: 0xcfa5e0..0xcfa75f
sha256: 53a7479bca7733730fe513f76638d31eaa16cf58abad3ad65bafa8396685b16a
```

## PROVEN — outer resolver receives `[slot28(category), key]`

`TTibiaFileSystemHelper::vtable+0x30 -> 0xc9b890`:

```text
0xc9b8a7  call own slot +0x28
0xc9b8b7  copy slot+0x28 result
0xc9b8df  copy caller key QString
0xc9b905  allocate 0x30 bytes = 2 * 0x18-byte QString elements
0xc9b8ce  load base helper +0x78
0xc9b96f  invoke base helper +0x78
```

Immutable window:

```yaml
va: 0xc9b890..0xc9ba1f
sha256: 5d3257ac75e63766f25c671efd49fd6c64920c7e158bd5e112b9eb99fc91fec2
```

## PROVEN — terminal key `BEClient`, category `9`

`TTibiaFileSystemHelper::vtable+0xd8 -> 0xc95cb0`:

```text
0xc95cb2  exact literal "BEClient"
0xc95cca  length = 8
0xc95cd9  QString::fromUtf8(...)
0xc95ce1  EDX = 9
0xc95cec  call same object's slot +0x30
```

Thus the exact logical invocation is:

```text
slot30(category=9, key="BEClient")
```

## PROVEN — category `9` is resolved through slots `+0x18` and `+0x10`

`TTibiaFileSystemHelper::vtable+0x28 -> 0xc9b620` saves the incoming category, calls own `+0x18(category)`, calls own `+0x10(category)`, and when the `+0x10` result is present combines the two QStrings via the same `J` operation.

Anchors:

```text
0xc9b624  save EDX category
0xc9b64a  call own +0x18
0xc9b651  pass saved category to own +0x10
```

Immutable window:

```yaml
va: 0xc9b620..0xc9b88f
sha256: e1ad52aa1fa5a1a83930e1e37e97150269044a2520cddf8675cb61c675193e36
```

Category-9 jump-table entries:

```text
+0x18 table 0x1d68a4c, index 9 -> 0xc91230
+0x10 table 0x1d689f8, index 9 -> 0xc8f8e0
```

## PROVEN — root component is `QCoreApplication::applicationDirPath()`

At category `9`, `+0x18` case `0xc91230` directly calls `0x4e0050`, whose exact dynamic symbol is:

```text
QCoreApplication::applicationDirPath()
```

Therefore category-9 root component is the runtime application-directory QString.

## PROVEN — subdirectory component is exact QString `"BattlEye"`

The category-9 `+0x10` case `0xc8f8e0` copies the runtime-initialized global QString object at `0x31964a0`.

Its exact static initializer is:

```text
0x613463  load global object address 0x31964a0
0x61346a  load exact literal "BattlEye" at 0x1d7b160
0x613471  pass global as destination
0x613474  call helper 0x6b2350
```

Initializer window:

```yaml
va: 0x613450..0x6134bf
sha256: 0facd17d377cc00b14d728a2a5fda15fdb323098cbf99d6c1c9887be8e403f08
```

Helper `0x6b2350` preserves destination/source and calls:

```text
0x6b236c -> strlen
0x6b237b -> QString::fromUtf8(QByteArrayView)
```

Helper window:

```yaml
va: 0x6b2350..0x6b24bf
sha256: 2b69a06ad9f6726536251b137d461be7bf170abe68c46d620c3ed2ea4f308390
```

Thus:

```text
TTibiaFileSystemHelper +0x10(category 9) = QString("BattlEye")
```

is directly established from its static initializer.

## PROVEN symbolic formula passed toward QLibrary

Combining the exact call graph:

```text
category9_root = QCoreApplication::applicationDirPath()
category9_subdir = "BattlEye"
category9_path = J([category9_root, category9_subdir])
terminal_key = "BEClient"
qlibrary_name = J([category9_path, terminal_key])
```

Therefore:

```text
J([J([QCoreApplication::applicationDirPath(), "BattlEye"]), "BEClient"])
```

with stable path-equivalent suffix:

```text
BattlEye/BEClient
```

The predecessor loader-data-flow report proves the result of this `+0xd8` path is the value passed to `QLibrary::setFileName @ 0x6fcaba`.

## Extension boundary

The recovered client-side formula contains `BEClient`, not `BEClient.so`. No `.so` suffix is appended anywhere in this proven resolver chain.

This does **not** by itself prove which final filesystem object QLibrary maps. Platform-specific QLibrary candidate-name expansion is a separate downstream layer.

## Corrections / rejected evidence

- A broad raw global xref scan for `"BattlEye"`/global storage was exploratory and is rejected as semantic evidence. Only the exact adjacent initializer instructions are retained.
- Raw file bytes of runtime-initialized global QString `0x31964a0` are not used; its value is proved via its static initializer.
- One diagnostic `objdump` run failed because `objdump` is unavailable on the Synology runner; no semantic conclusion depends on it.

## Deterministic validator

Final validator:

```text
run: 31942437204
job: 95153445603
result: SUCCESS
```

It re-derived RTTI/vtables, Qt/strlen PLT identities, `BEClient` key/category 9, both TTibia resolver layers, category-9 jump-table entries, `applicationDirPath`, `BattlEye` initializer, `J` loop, `QDir::toNativeSeparators`, and all immutable evidence-window hashes.

Key outputs:

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

## Material provenance

```text
31941609207 / 95151515942  base-helper RTTI/+0x78 and caller correlation
31941660701 / 95151640998  exact base resolver and slash handling
31941716491 / 95151777224  Qt append/toNativeSeparators mapping
31941768535 / 95151899494  TTibia +0x28 / outer two-QString construction
31941829706 / 95152041120  category switching/forwarding
31941909566 / 95152225148  category-9 jump-table cases
31942173414 / 95152833368  exact BattlEye initializer boundary
31942213755 / 95152924982  initializer helper -> strlen/fromUtf8
31942437204 / 95153445603  deterministic final validator: SUCCESS
```

## Remaining downstream boundary

- exact runtime value of `QCoreApplication::applicationDirPath()` for a particular invocation;
- exact character-for-character runtime separator shape;
- native-Linux QLibrary candidate expansion for extensionless `BEClient`;
- exact filesystem path/object ultimately opened and mapped by QLibrary.

These are downstream of the now-PROVEN client-generated formula and belong to a separate QLibrary/platform-resolution task.

## Safety

All work was static exact-client analysis. No Tibia/BattlEye execution/loading, live process observation, process memory/maps, attach/debug/injection, input/network/session/credential mutation, binary patching, unpacking, anti-debug/detection research, packet/protocol inspection, disabling, spoofing, stealth or bypass/evasion work occurred.
