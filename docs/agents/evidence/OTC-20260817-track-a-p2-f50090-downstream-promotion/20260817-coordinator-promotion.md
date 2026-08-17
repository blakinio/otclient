# Track A P2 `0xf50090` downstream — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-f50090-downstream`  
Source Draft: PR #488  
Final reviewed source head: `76460840d583218dde1b268f4e46e17a074f0abf`  
Decision: **ACCEPT_WITH_EDITS**

## Exact client

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Independent coordinator verification

The coordinator inspected primary source/hosted job logs and final durable diff rather than relying on the researcher summary.

Successful evidence generations:

```text
Generation 2
  producer head  ea8113028a07ef84518f4a8b705bcecd97604376
  run            32037248323 = SUCCESS
  source job     95410048084 = SUCCESS
  hosted job     95410072413 = SUCCESS
  main window    0xf50040..0xf50480
  main sha256    1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea

Generation 3
  producer head  8642b419ca8ef3034ba747f689a14e24cf9a0152
  run            32037533068 = SUCCESS
  source job     95410828633 = SUCCESS
  hosted job     95410901806 = SUCCESS
  main sha256    1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
  ctor sha256    bc03c482e3ae04c0f9a91288d5f79612b2f0f08680ef10ffecdf9a927ec0371f
  vcall sha256   dc04038b7740f39095ed6ab599bc10048c368fab9eff126c3d0853930c62af14
```

Source jobs re-fenced exact size/SHA and performed only bounded file-backed byte staging. They did not disassemble/classify on the source runner, access a client process/process memory/canonical runtime, execute or mutate the client, or upload the raw executable.

## Accepted exact dataflow

The already-canonical predecessor reaches `0xf50090` with the same message in SysV `rsi`. Exact entry dataflow saves it in `rbp` and snapshots message fields.

The strongest accepted direct path is:

```text
canonical same message
 -> 0xf50090
 -> field decomposition
 -> writer vslot +0x58 guard == 0xcb2960
 -> payload pointer from canonical message+0x10
 -> payload length from canonical message+0x18
 -> underlying receiver at writer+0x18
 -> exact target 0x4dd250
```

Exact wrapper `0xcb2960` independently cross-checks that structural contract:

```text
cb2960: rdx = [arg+0x10]
cb2964: rsi = [arg+0x08]
cb2968: rdi = [wrapper+0x18]
...
cb2971/cb2987 -> 0x4dd250
```

The original whole message pointer is **not** forwarded as a whole by `0xf50090`; downstream continuity is through the extracted payload pointer/length fields.

## Supporting constructor evidence

Exact constructor-like function `0x1960340` proves only these bounded structural facts:

```yaml
installed_vptr: FACT:0x2f69d48
nested_object_member: FACT:this+0x18
owner_control_member: FACT:this+0x20
```

This is consistent supporting ownership evidence. It is **not** promoted as proof of the current writer dynamic type without a separate vtable/RTTI provenance proof.

## Promoted classifications

```yaml
f50090_second_argument: FACT:canonical_same_message
f50090_decomposes_message_into_fields: FACT
f50090_forwards_original_message_pointer_as_whole: DISPROVEN
writer_guard_slot: FACT:+0x58
writer_guard_exact_target: FACT:0xcb2960
raw_payload_pointer: FACT:canonical message+0x10 value
raw_payload_length: FACT:canonical message+0x18 value
underlying_receiver_on_direct_path: FACT:writer+0x18
raw_payload_target: FACT:0x4dd250
cb2960_payload_pointer: FACT:argument+0x08
cb2960_payload_length: FACT:argument+0x10
cb2960_underlying_receiver: FACT:wrapper+0x18
cb2960_target: FACT:0x4dd250
```

## Still UNKNOWN

```yaml
writer_exact_dynamic_type: UNKNOWN
underlying_receiver_exact_dynamic_type: UNKNOWN
semantic_role_of_0x4dd250: UNKNOWN
0x4dd250_is_final_binary_socket_write: UNKNOWN
final_binary_egress: UNKNOWN
final_socket_ownership: UNKNOWN
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
```

No socket/framing/compression/encryption semantic is inferred from calling convention, address adjacency or Qt-like object layout.

## Source final validation

Final researcher head `76460840d583218dde1b268f4e46e17a074f0abf`:

```text
Track A governance  32037873578 = SUCCESS
CI                  32037873878 = SUCCESS
CI / Required       95411808828 = SUCCESS
changed files       exactly 3 durable P2 files
reviews/threads     0/0
one-shot surfaces   removed
```

Fresh coordinator audit: `PASS_BOUNDED`; material findings open: `0`.

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.

## Programme handoff

This promotion does **not** start another research task in the current invocation. A later invocation may continue at exact target `0x4dd250` and resolve its receiver/dynamic identity and downstream semantics. Until then final socket/framing/sequence/compression/encryption claims remain UNKNOWN.
