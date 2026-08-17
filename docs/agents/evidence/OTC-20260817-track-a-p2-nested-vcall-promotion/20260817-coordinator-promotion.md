# Track A P2 nested DualConnection virtual calls — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-dual-nested-vcall-resolution`  
Source Draft: PR #483, head `a1b8a2c6e760a8727b3f08e3777c05e81760704d`  
Disposition: **ACCEPT_WITH_EDITS**

## Verification basis

The coordinator independently re-downloaded exact-fenced artifact `9283858910` from predecessor run `32016842999` / hosted job `95348295109`, re-hashed the ZIP as:

```text
sha256 2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c
```

and independently inspected its exact `disassembly.txt` dataflow. No researcher summary was used as proof.

Exact client fence remains:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Source Draft exact-head validation:

```text
Track A governance  32033390538 = SUCCESS
repository CI        32033390624 = SUCCESS
CI / Required job    95398262482 = SUCCESS
changed files        exactly 3 P2 files
reviews / threads    0 / 0
```

Runtime admission remained `runtime_access:none`; no client process, login, gameplay, process memory, canonical runtime or world-map evidence was used.

## Promoted result — `0xb56c93`

In the canonical DualConnection `+0x78` entry, the second argument is preserved:

```text
b5697b: mov r14,rsi
```

and restored immediately before the nested virtual call:

```text
b56c50: mov rbx,[r12]
b56c54: lea rsi,[rip+...]      # 0xb3eda0
b56c5b: mov rax,[rbx]
b56c5e: mov rax,[rax+0x98]
b56c65: cmp rax,rsi
...
b56c6e: mov rdi,[rbx+0x20]
b56c72: lea rdx,[rip+...]      # 0xf45cf0
b56c79: mov rax,[rdi]
b56c7c: mov rax,[rax+0x60]
b56c80: cmp rax,rdx
...
b56c89: mov rdi,[rdi+0x20]
b56c8d: mov rsi,r14
b56c90: mov rax,[rdi]
b56c93: call [rax+0x10]
```

Because canonical PR #450 already proves that the `b56970` `+0x78` second argument is the same post-`TGameserverNetworkPacketRawDataProcessor` message, the following are promoted:

```yaml
b56c93_receiver_provenance: FACT:nested_pointer_chain_current_entry_plus_0x20_plus_0x20
b56c93_outer_guard_vslot_plus_0x98_target: FACT:0xb3eda0
b56c93_intermediate_guard_vslot_plus_0x60_target: FACT:0xf45cf0
b56c93_virtual_slot: FACT:+0x10
b56c93_second_argument: FACT:original_b56970_second_argument_rsi
b56c93_same_message_preserved: FACT
b56c93_receiver_exact_dynamic_type: UNKNOWN
b56c93_concrete_target: UNKNOWN
b56c93_target_equals_b40630: UNKNOWN
```

No target is inferred from vtable adjacency, range proximity, RTTI naming or guard names.

## Promoted negative result — `0xb57042`

In the canonical `+0x80` path, the direct branch reaching `0xb57042` establishes:

```text
b56ecd: mov rdx,[rbx+0x8]
b56ed4: movabs rsi,0x100000001
b56ee1: cmp rdx,rsi
b56ee4: je 0xb57030
...
b57030: mov rdx,[rbx]
b57037: mov rdi,rbx
b5703a: mov QWORD PTR [rbx+0x8],0x0
b57042: call [rdx+0x10]
```

No original-message restore occurs on that taken edge. Promoted classifications:

```yaml
b57042_receiver_provenance: FACT:internal_rbx_object_selected_from_plus_0x80_path
b57042_virtual_slot: FACT:+0x10
b57042_rsi_on_taken_branch: FACT:0x100000001
b57042_same_message_preserved: DISPROVEN
b57042_is_same_message_edge_to_b40630: DISPROVEN
b57042_receiver_exact_dynamic_type: UNKNOWN
b57042_concrete_target: UNKNOWN
```

No destructor/refcount/ownership semantic is attached to this call.

## Canonical P2 frontier after this promotion

The P2 chain remains:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

PR #481 additionally established that `0xb4066b` is a direct `QIODevice::write(QByteArray const&)` callsite in distinct function `0xb40630`, but not a proven direct QTcpSocket sink and not yet proven reachable from the canonical same-message chain.

This promotion reduces the missing reachability edge to exactly one live candidate:

```text
same message -> b56c93 nested receiver vslot +0x10 -> UNKNOWN target
```

`0xb57042` is no longer a same-message candidate.

## Still UNKNOWN

- exact dynamic type/vtable of the `0xb56c93` receiver;
- concrete `+0x10` target at `0xb56c93`;
- whether that target equals `0xb40630`;
- framing;
- sequence;
- compression;
- encryption;
- final binary egress;
- final socket ownership;
- complete transport stage order beyond the promoted chain.

## Exact next step

Do one bounded static discriminator only: recover the exact object-construction/vtable provenance for the receiver used at `0xb56c93`, anchored to the proven pointer chain and guards `+0x98 -> 0xb3eda0` / `+0x60 -> 0xf45cf0`, then resolve vslot `+0x10` and test exact equality with `0xb40630`.

If the slot resolves to another function, the `b40630` same-message reachability hypothesis is falsified for this path. If the slot cannot be resolved from bounded exact evidence, keep it `UNKNOWN` and record the narrow missing construction/relocation bytes. Do not broaden into generic network reverse engineering.

## Audit / E2E

Independent coordinator audit: `PASS_BOUNDED`; material findings open: `0`.

E2E: `NOT_APPLICABLE` — static exact-artifact dataflow only.
