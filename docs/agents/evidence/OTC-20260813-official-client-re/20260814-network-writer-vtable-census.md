# Track A — relocated network-writer vtable census

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Classify the strongest remaining direct `QIODevice::write(QByteArray const&)` candidate (`0xb40630`) against the canonical Track A network-owner structures using relocated, exact-SHA data rather than raw on-disk qwords.

Canonical outbound anchors entering this experiment:

```yaml
primary_network_owner_vtable: 0x308c408
primary_network_owner_slot_0x90: 0x8409d0
contained_network_subobject_vtable: 0x2f66288
contained_network_subobject_slot_0xb8: 0xb5b880
source_run: 31812572191
source_job: 94806473825
source_result: SUCCESS
```

Direct-writer candidate entering this experiment:

```yaml
candidate_writer_entry: 0xb40630
qiodevice_write_call: 0xb4066b
source_run: 31826270686
source_job: 94851048204
```

## Exact experiment — PROVEN

Workflow:

```text
.github/workflows/tibia-official-client-re-network-writer-vtable-census.yml
```

Relocation-aware run/job:

```yaml
run_id: 31827157926
job_id: 94853870296
head: 22b48d5d1d93543e9dceda6477be975ed79d3b11
result: SUCCESS
runner: synology-otclient-01
r_x86_64_relative_count: 168838
```

Artifact:

```yaml
name: track-a-network-writer-vtable-census-31827157926
artifact_id: 9229251044
zip_sha256: 4b914f65d4a4eb3c91a39ce9918e8e4f865fadcf4853ab4af25ffa5d5f519520
```

This run supersedes run `31827016253` for vtable/qword interpretation because the earlier version did not apply `R_X86_64_RELATIVE` relocations.

## Canonical primary owner comparison — PROVEN

For canonical primary owner address point `0x308c408` the relocated census recovered:

```text
offset_to_top = 0
RTTI = 0x30775a0
type_name = N5tibia4game23TSessiondumpGameSessionE
+0x90 = 0x8409d0
+0xd0 = 0x7eca30
```

Therefore:

```text
0x308c408 + 0xd0 != 0xb40630
```

`0xb40630` is not the `+0xd0` virtual function of the canonical primary network owner.

## Canonical contained-subobject comparison — bounded result

The scanner also read the persisted address `0x2f66288`; however its would-be Itanium preamble was not plausible in this particular static address-point interpretation:

```text
offset_to_top = 51652064
RTTI = 0x2f5ec40
type_name = UNKNOWN
```

The observed `+0xd0` value was `0x31399e0`, not `0xb40630`.

Because the preamble itself is not a valid normal Itanium address-point shape, this run must **not** be used to redefine the semantics of the previously promoted contained-subobject anchor. It is sufficient only to say that the relocation-aware scan did not produce a direct `0x2f66288 + 0xd0 -> 0xb40630` bridge. Existing run `31812572191` remains authoritative for the promoted `0x2f66288` / `+0xb8 -> 0xb5b880` relationship.

## Exact relocation to `0xb40630` — PROVEN

Across all `R_X86_64_RELATIVE` relocations there is exactly one whose addend is `0xb40630`:

```text
WRITER_B_RELATIVE_RELOCATION_COUNT=1
WRITER_B_RELATIVE_RELOCATION_DESTS=0x3084d40
```

Therefore the relocated runtime pointer stored at static destination `0x3084d40` resolves to executable target `0xb40630`.

## Candidate address point `0x3084c70` — PROVEN STRUCTURE, ROLE UNKNOWN

The unique plausible non-executable address point satisfying:

```text
address_point + 0xd0 = 0x3084d40
relocated *(address_point + 0xd0) = 0xb40630
```

is `0x3084c70`.

The run recovered:

```text
address_point = 0x3084c70
offset_to_top = 0
RTTI = 0x0
type_name = UNKNOWN
first = 0x7dcbd0
first_exec = 1
+0x08 = 0x7dcbe0
+0xd0 = 0xb40630
+0xd8 = 0xb40690
+0xe0 = 0xb40710
+0xe8 = 0x0
+0xf0 = 0x3080678
+0xf8 = 0xdc7260
+0x100 = 0xdd5b00
+0x108 = 0xdd8fe0
+0x110 = 0x7e1340
+0x118 = 0x7e1440
```

A second arithmetic match at `0x280e18` lies in the relocation-table region and has `first_exec=0`; it is a scanner artifact/relocation-record interpretation, not promoted as a vtable/address point.

The static RIP-relative LEA scanner found zero direct LEA references to `0x3084c70`. This does not prove the table is unused; provenance can flow through relocations, data tables, constructors using a neighboring address point, or indirect references.

## Writer function `0xb40630` — PROVEN STRUCTURE

Exact disassembly shows a staged Qt I/O adapter:

```asm
0xb40640  mov rax,[rdi]
0xb40643  call [rax+0x78]
...
0xb4064f  mov r13,[rax+0x88]
0xb40656  call QBuffer::buffer@plt
...
0xb40662  call r13
...
0xb4066b  call QIODevice::write(QByteArray const&)@plt
...
0xb40679  mov rax,[rax+0x88]
0xb4068a  jmp rax
```

This proves that `0xb40630` is not merely a string/log helper; it performs virtual pre/post processing around a concrete `QIODevice::write` call. Its exact class and whether the concrete QIODevice is the official game socket remain UNKNOWN.

## Classification

### FACT

- relocation-aware exact-SHA run `31827157926` succeeded;
- canonical primary network owner `0x308c408` has `+0xd0 = 0x7eca30`, not `0xb40630`;
- exactly one `R_X86_64_RELATIVE` relocation resolves a stored pointer to `0xb40630`, at destination `0x3084d40`;
- plausible table/address point `0x3084c70` has `+0xd0 -> 0xb40630` and executable first entries `0x7dcbd0`, `0x7dcbe0`;
- `0xb40630` directly invokes `QIODevice::write(QByteArray const&)` and virtual pre/post hooks.

### DISPROVEN

- `0xb40630` is the `+0xd0` slot of canonical primary network-owner vtable `0x308c408`.
- the raw non-relocated qword dump from run `31827016253` is sufficient to classify these vtables.

### UNKNOWN

- exact semantic/class identity of table `0x3084c70`;
- constructor/object provenance that installs or references `0x3084c70`;
- whether the QIODevice reached by `0xb40630` is a `QTcpSocket` used by the game connection, another network device, or a different Qt I/O path;
- exact bridge from `0xb5b880` / canonical network owner to one of the five direct QIODevice writers;
- exact game-login wire field contract.

## Next action

Recover provenance for `0x3084c70` structurally. Enumerate all relative relocations/data entries whose addend points to `0x3084c70`, its neighboring address points, `0x7dcbd0`, `0x7dcbe0`, `0xb40630`, `0xb40690`, and `0xb40710`; inspect constructor-shaped executable references to the surrounding `0x3084cxx` data block; classify `0x7dcbd0/0x7dcbe0` and the `0xb406xx` sibling functions from exact FDE boundaries. Promote a network bridge only if the recovered object provenance intersects the canonical game-session/network-owner path; otherwise keep this Qt writer family separate and continue with the next remaining writer candidate.