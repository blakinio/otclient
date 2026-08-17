# Track A P2 — `0xf50090` downstream dataflow

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-f50090-downstream`  
Research status: **DRAFT / NOT PROMOTED — READY FOR COORDINATOR REVIEW AFTER FINAL CI**

## Exact-client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

No live client process, process memory, login/gameplay, canonical runtime state or world-map evidence was used. Synology source stages only verified the retained regular exact file and copied bounded file-backed bytes; disassembly and interpretation ran on GitHub-hosted Ubuntu.

## Evidence generations

The first marketplace-action producer failed before source access because GitHub could not download `actions/checkout` from `codeload.github.com` (HTTP 503/429). The replacement producer removed all marketplace actions instead of retrying indefinitely.

### Generation 2 — `0xf50090` function

```text
producer head    ea8113028a07ef84518f4a8b705bcecd97604376
run              32037248323 = SUCCESS
source job       95410048084 = SUCCESS
hosted job       95410072413 = SUCCESS
main window      0xf50040..0xf50480
main sha256      1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
source candidate 1
```

### Generation 3 — writer wrapper / ownership discriminator

```text
producer head    8642b419ca8ef3034ba747f689a14e24cf9a0152
run              32037533068 = SUCCESS
source job       95410828633 = SUCCESS
hosted job       95410901806 = SUCCESS
main window      0xf50040..0xf50480
main sha256      1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
ctor window      0x1960300..0x1960600
ctor sha256      bc03c482e3ae04c0f9a91288d5f79612b2f0f08680ef10ffecdf9a927ec0371f
vcall window     0xcb2900..0xcb29c0
vcall sha256     dc04038b7740f39095ed6ab599bc10048c368fab9eff126c3d0853930c62af14
source candidate 1
```

Both successful source stages revalidated exact file size/SHA, ELF64 little-endian structure and file-backed executable ranges. Source-side disassembly/semantic classification, process/runtime access, client execution/mutation and raw-client upload were absent.

## `0xf50090`: canonical argument and message decomposition

Hosted decode establishes function entry `0xf50090`; the next aligned function is `0xf501e0`.

```text
f50090: push r12
f50092: push rbp
f50093: mov  rbp,rsi
f50096: push rbx
f50097: mov  rbx,rdi
```

The coordinator-promoted predecessor proves that `0xb56c93` invokes exact target `0xf50090` with the canonical same message in SysV second argument `rsi`.

```yaml
f50090_second_argument: FACT:canonical_same_message
f50090_saved_message_pointer: FACT:rbp
```

`0xf50090` snapshots fields rather than forwarding the original object pointer:

```text
f5009e: movdqu xmm0,[rsi+0x8]
f500a3: mov    rax,[rsi+0x18]
f500ab: mov    [rsp+0x10],rax
f500b0: movaps [rsp],xmm0
```

Thus:

```text
message+0x08 -> stack+0x00
message+0x10 -> stack+0x08
message+0x18 -> stack+0x10
```

The original pointer remains saved in `rbp` for field reads.

## Concrete downstream calls

The earlier helpers carry only derived/scalar message fields:

```text
f500f7: call 0x4dc3d0   # scalar derived from message+0x18
f50107: mov esi,[rbp]
f50121: call 0x4daaf0   # scalar from message+0x00
```

The strongest raw-payload edge is:

```text
f5012a: lea rdx,0xcb2960
f50131: mov rax,[rdi]
f50134: mov rax,[rax+0x58]
f50138: cmp rax,rdx
f5013b: jne fallback
f5013d: mov rsi,[rsp+0x8]   # canonical message+0x10 value
f50142: mov rdi,[rdi+0x18]  # underlying receiver
f50146: mov rdx,[rsp+0x10]  # canonical message+0x18 value
f50153: call 0x4dd250
```

Therefore, on the exact direct guarded branch:

```yaml
writer_guard_slot: FACT:+0x58
writer_guard_exact_target: FACT:0xcb2960
raw_payload_pointer: FACT:value copied from canonical message+0x10
raw_payload_length: FACT:value copied from canonical message+0x18
underlying_receiver: FACT:writer object +0x18
raw_payload_target: FACT:0x4dd250
```

## Independent wrapper cross-check at `0xcb2960`

Generation 3 independently decodes the exact guard target:

```text
cb2960: mov rdx,[rsi+0x10]
cb2964: mov rsi,[rsi+0x08]
cb2968: mov rdi,[rdi+0x18]
cb296c: test rsi,rsi
cb296f: je 0xcb2980
cb2971: jmp 0x4dd250
...
cb2980: mov rsi,[0x312fe68]
cb2987: jmp 0x4dd250
```

This independently confirms the same structural contract: a QByteArray-like/subobject value contributes data pointer at `+0x08` and length at `+0x10`; the wrapper's underlying receiver is at `this+0x18`; the concrete downstream target is `0x4dd250`. The null-data branch substitutes the global empty-data pointer before the same target.

## Constructor ownership evidence

Generation 3 also decodes constructor-like function `0x1960340`:

```text
1960342: lea rax,0x2f69d48
1960354: mov [rdi],rax
...
1960387: mov edi,0x30
1960390: call 0x4df670
19603a2: lea r12,[rbp+0x10]
19603b1: mov rdi,r12
19603b8: call 0x4db6d0
19603c1: mov [rbx+0x18],r12
19603c5: mov [rbx+0x20],rbp
```

Exact structural facts from this function:

```yaml
constructor_installed_vptr: FACT:0x2f69d48
constructor_nested_object_member: FACT:this+0x18
constructor_owner_control_member: FACT:this+0x20
```

This is supporting ownership evidence consistent with the `+0x18` forwarding wrapper. This bounded task does **not** overpromote `0x2f69d48` into the exact current dynamic type of the `0xf50090` writer without a separate vtable/RTTI provenance proof.

## Negative control — whole-message forwarding

No downstream call in decoded `0xf50090` receives the original saved message pointer `rbp` as a whole. The fallback at `f501a3` explicitly replaces `rsi` with a stack-local snapshot address before `call rax`.

```yaml
f50090_forwards_original_message_pointer_as_whole: DISPROVEN
f50090_decomposes_message_into_fields: FACT
```

Payload continuity is nevertheless directly proven through the `message+0x10` pointer and `message+0x18` length to `0x4dd250`.

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

No socket/framing/compression/encryption semantic is inferred from calling convention, Qt-like layout, address adjacency or constructor shape.

## Result

The task stop condition is satisfied with a stronger exact path:

```text
canonical same message
 -> 0xf50090
 -> field decomposition
 -> writer guard +0x58 == 0xcb2960
 -> payload pointer (message+0x10) + length (message+0x18)
 -> underlying receiver at writer+0x18
 -> exact target 0x4dd250
```

A later invocation may investigate the exact dynamic identity of the writer/underlying receiver and the semantics/downstream dataflow of `0x4dd250`. This task does not start that new frontier.

E2E: `NOT_APPLICABLE` — exact static file/disassembly evidence only.
