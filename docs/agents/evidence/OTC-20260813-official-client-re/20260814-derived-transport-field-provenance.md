# Track A — derived transport field provenance

Date: 2026-08-14
Track: A / official native Linux Tibia client RE
Branch: `ci/OTC-20260814-track-a-chatgpt-framing-recovery`
Exact client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
Workflow run: `31822915413`
Job: `94840190364`
Result: `SUCCESS`
Runner: `synology-otclient-01`
Artifact: `track-a-derived-transport-fields-31822915413`, id `9227981704`, zip SHA256 `3cccdd502d4f229eff5056e0171661a82a213d648c6605508e8b6b2adc62e39e`

## FACT

1. The exact-build scan for an address point whose `+0xe8` qword equals concrete method `0xb40630` produced two raw candidates:
   - `0x280e00`, reported header `offset_to_top=8`, `rtti=0xb3ec50`, no direct LEA refs;
   - `0x3084c58`, header `offset_to_top=0`, `rtti=0x3080660`, direct LEA refs at `0x7dcbd0`, `0x7dcbe0`, `0x19707fd`, `0x1970cb2`.
2. The current scanner's header predicate was intentionally broad: it required the RTTI candidate only to be mapped, not specifically resident in non-executable data. Therefore the two raw candidates are not yet equivalent-strength vtable proofs.
3. `0x3084c58` has executable slots including:
   - `+0x18 = 0x7dcbd0`
   - `+0x20 = 0x7dcbe0`
   - `+0xe8 = 0xb40630`
   - `+0xf0 = 0xb40690`
   and RTTI candidate `0x3080660`.
4. The derived constructor caller around `0x6fcc63` zero-initializes the owner field family:
   - `+0x9d0..+0x9df`
   - `+0x9e0..+0x9ef`
   - `+0x9f0..+0x9ff`
   - `+0xa00..+0xa0f`
   - `+0xa10..+0xa1f`
   - `+0xa20..+0xa2f`
   and `+0xa30`.
5. The bounded constructor window contains no raw `disp32=0xc18` match. It does initialize a broader tail including `+0xc10..+0xc1f` as one zeroed XMM block at `0x6fd2cf`, so `+0xc18` begins zero-initialized as part of that block.
6. At `0x6fccbc`, immediately after those initial zero stores, the constructor allocates `0x190` bytes. The allocated object receives several vptr-like values (`0x2f632f8`, `0x2f63240`, `0x2f631c8`) and nested state; this allocation is later stored at owner `+0xa38` (`0x6fd165`). It is therefore not, on this evidence alone, the object later loaded directly from owner `+0x9f0`.
7. A second allocation of `0x218` bytes begins at `0x6fcd39` and is wired into the first allocation (`[r14+0xd8]=r13` at `0x6fd0b6`) before the first allocation is stored at owner `+0xa38`.
8. The same derived constructor initializes owner `+0xc68` and `+0xc88` as `QTimer` objects and later establishes multiple `QObject::connectImpl` connections.
9. Concrete method `0xb40630` is independently disassembled and contains:
   - virtual call `self+vtable[0x78]`;
   - `QBuffer::buffer(self)`;
   - virtual call through `self+vtable[0x88]` using data from that buffer;
   - direct `QIODevice::write(QByteArray const&)` at `0xb4066b`;
   - tail virtual call through `self+vtable[0x88]`.
10. Neighbor method `0xb40690` also uses `QBuffer::buffer(self)`, removes bytes from the buffer, rearranges state, and tail-calls virtual `+0x88`.
11. The constructor includes host-resolution/network-adjacent code (`QHostInfo::fromName`, `QHostInfo::addresses`, `QHostAddress`) in the same most-derived construction/setup function, reinforcing that this is the relevant network-owner family but not by itself identifying the gameplay socket field.

## DERIVED

- `0x3084c58` is the high-confidence vtable/address-point candidate for the concrete `0xb40630/+0xe8` object because it has a conventional zero offset-to-top, data-region-looking RTTI, executable method slots, and four direct code references. A stricter RTTI/data-segment validation is still required before calling it uniquely proven.
- `0x280e00` is likely a false positive/table interior rather than a true Itanium address point: its reported RTTI value `0xb3ec50` is in the executable-looking function-address range and it has no direct LEA references. This must be verified rather than assumed.
- The objects consumed from owner `+0x9f0/+0xa00/+0xa10/+0xc18` are not simply assigned by the visible constructor prologue; they are zero-initialized there and must be populated later by setup/state transitions or helper calls.

## UNKNOWN

- RTTI type name corresponding to `0x3080660`.
- Exact semantic class represented by `0x3084c58`.
- Which of xrefs `0x7dcbd0`, `0x7dcbe0`, `0x19707fd`, `0x1970cb2` are constructor/destructor/vptr stores versus method-local references.
- Later assignment sites for owner `+0x9f0`, `+0xa00`, `+0xa10`, `+0xc18`.
- Concrete QTcpSocket / final gameplay network-write object and framing order.

## NEXT ACTION

Tighten the Itanium vtable predicate to require non-executable RTTI storage (or null RTTI where structurally justified), decode the RTTI/name at `0x3080660`, disassemble the four direct references to `0x3084c58`, and use those constructor/destructor paths to identify the concrete QIODevice/QBuffer-derived class. Then trace stores of instances of that class back into the owner field family and intersect with the proven `0x7dd630 -> 0x7dd3f0 -> QIODevice::write` path.
