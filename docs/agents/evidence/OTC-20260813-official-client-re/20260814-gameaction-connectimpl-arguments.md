# GameAction `QObject::connectImpl` argument reconstruction

## Scope

- Official native Linux client `15.32.df7b29`.
- SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Read-only workflow run `31800999307`, job `94768688628`, on `synology-otclient-01`.
- Input: 31 direct `connectImpl@plt` calls with a selected GameAction static-metaobject reference in the preceding 64 bytes.

## ABI correction

`QMetaObject::Connection` is returned through a hidden structure-return pointer. The effective SysV AMD64 layout is:

| Location | Value |
| --- | --- |
| `rdi` | hidden `QMetaObject::Connection` result storage |
| `rsi` | sender object |
| `rdx` | signal pointer-to-member storage |
| `rcx` | receiver object |
| `r8` | slot pointer-to-member storage |
| `r9` | allocated `QtPrivate::QSlotObjectBase` |
| stack argument 7 | `Qt::ConnectionType` |
| stack argument 8 | queued argument types |
| stack argument 9 | sender static metaobject |

This corrects the naive register-only interpretation that omitted the hidden return pointer. Every recovered site pushes, in order, a sender-metaobject pointer, zero, and zero before the call. Thus all 31 use `Qt::AutoConnection`, pass no queued-type array, supply a sender static metaobject, and allocate a 32-byte slot object placed in `r9`.

## Static-metaobject role classification

The nearby reference is the actual stack argument 9 at 29 sites. It is not the sender metaobject at `0x7d7b42` (nearby Chat `0x30851a0`, pushed `0x3085b60`). At `0x7d7307`, pushed `r14` is not defined inside the bounded neighborhood; nearby Container `0x30850a0` is loaded into `r15`, which had already been copied into the receiver register.

| Family | Calls | Sender-metaobject classification |
| --- | --- | --- |
| Creatures | `0x7d6876`, `0x7ff2c3` | both exact `0x3085060` |
| Chat | `0x7d7b42`, `0x7ff58e` | first mismatch `0x3085b60`; second exact `0x30851a0` |
| Container | `0x7d7307`, `0x7ffb24` | first unresolved in window; second exact `0x30850a0` |
| PlayerTrade | `0x7d8b66`, `0x7ff3e1` | both exact `0x3085360` |
| WorldMap | `0x7d7857` | exact `0x30850e0` |
| Player | `0x7d858e`, `0x7f8f84`, `0x7f9016`, `0x7f90a8`, `0x7f913a`, `0x7f91cc`, `0x7f925e`, `0x7f92f0`, `0x7f9382`, `0x7f9414`, `0x7f94a6`, `0x7f9538`, `0x7f95ca`, `0x7f965c`, `0x7f96ee`, `0x7f9780`, `0x7ff470`, `0x804f25`, `0x8baa7a`, `0x8e6a10`, `0x927efc`, `0x9ea484` | all exact `0x30852a0` |

## Recovered source patterns

The six early sites (`0x7d6876` through `0x7d8b66`) use result storage in `rbp`, signal storage in `r12`, a receiver copied to `r15`, slot storage in `r13`, and the new slot object in `rax -> r9`; sender sources are preserved stack values or callee-saved registers. The compact sites `0x7ff2c3` through `0x7ffb24` use result storage in `rbx`, reload sender and signal-storage pointers from the pre-push stack, use receiver `r15`, slot storage `r12`, and slot object `rax -> r9`.

The Player sequence `0x7f8f84` through `0x7f9780` repeats one form: result storage `rbp`, sender `r13`, signal storage `r15`, receiver `r14`, slot storage reloaded from the pre-push stack, and slot object `rax -> r9`. Isolated Player sites expose register or frame-relative sources but not stable object identities inside the bounded window.

The slot-object invoke-function address is stored at offset `+0x8` of the allocation. Naming those lambdas or receiver classes requires separate function-boundary/RTTI correlation and is not claimed here.

## Result and limits

- `31/31`: connection type, queued-types pointer, slot-object allocation and sender-metaobject argument position identified.
- `29/31`: nearby GameAction metaobject proven to be the sender metaobject.
- `0x7d7b42`: explicitly nearby but not the sender metaobject.
- `0x7d7307`: sender metaobject `UNRESOLVED` within this window.
- Source expressions do not alone establish receiver class identities, pointer-to-member signal indices, or lambda semantics.

