# Track A P2 — nested DualConnection virtual-call dataflow

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-dual-nested-vcall-resolution`  
Research status: **DRAFT / NOT PROMOTED**

## Exact-client / evidence fence

This discriminator reuses the already exact-fenced, non-quarantined final artifact from the accepted predecessor generation:

```text
client version  15.32.df7b29
client size     51965216
client sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
run             32016842999
hosted job      95348295109
artifact        9283858910
artifact sha256 2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c
```

The coordinator/researcher downloaded artifact `9283858910` again and independently re-hashed the ZIP to the recorded digest before inspecting `disassembly.txt`. No new client bytes, runtime access, process memory, login, gameplay or Synology semantic execution were required.

Admission remains:

```yaml
track_id: official-client-re
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
```

## `0xb56c93`: same-message argument is preserved to one unresolved nested vslot

The canonical `+0x78` entry begins at `0xb56970`. Exact disassembly preserves the function's original second SysV argument in `r14`:

```text
b5697b: mov r14,rsi
```

The callsite path later performs two guarded nested dereferences:

```text
b56c50: mov rbx,[r12]
b56c54: lea rsi,[rip+...]           # 0xb3eda0
b56c5b: mov rax,[rbx]
b56c5e: mov rax,[rax+0x98]
b56c65: cmp rax,rsi
...
b56c6e: mov rdi,[rbx+0x20]
b56c72: lea rdx,[rip+...]           # 0xf45cf0
b56c79: mov rax,[rdi]
b56c7c: mov rax,[rax+0x60]
b56c80: cmp rax,rdx
...
b56c89: mov rdi,[rdi+0x20]
b56c8d: mov rsi,r14
b56c90: mov rax,[rdi]
b56c93: call [rax+0x10]
```

Therefore the bounded exact classifications are:

```yaml
b56c93_receiver_provenance:
  classification: FACT
  value: nested_pointer_chain_from_current_plus_0x78_iteration
  chain: current_entry=[r12] -> current_entry+0x20 -> intermediate+0x20 -> receiver
  outer_guard_vslot_plus_0x98_target: 0xb3eda0
  intermediate_guard_vslot_plus_0x60_target: 0xf45cf0
  receiver_exact_dynamic_type: UNKNOWN
b56c93_virtual_slot: FACT:+0x10
b56c93_concrete_target: UNKNOWN
b56c93_second_argument:
  classification: FACT
  value: original_b56970_second_argument_rsi
b56c93_same_message_preserved:
  classification: FACT
  basis: canonical #450 identifies the b56970 +0x78 input second argument as the same post-RawDataProcessor message
b56c93_target_equals_b40630: UNKNOWN
```

This reduces the missing reachability question to one exact unresolved receiver vtable slot. If the nested receiver's `+0x10` target is proven to be `0xb40630`, then the `b40630` second argument is already proven to be the same message. If the target resolves elsewhere, the `b40630` edge is falsified for this branch.

No target is inferred from vtable adjacency or address proximity.

## `0xb57042`: not a same-message continuation

The canonical `+0x80` entry begins at `0xb56d60`. Its original second argument is stored on the stack:

```text
b56d71: cmp DWORD PTR [rsi+0x28],0x1
b56d75: mov [rsp+0x10],rsi
```

The branch that reaches `0xb57042` instead sets `rsi` to a fixed value and jumps directly to the call path when the compared field matches it:

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
b57045: mov rdx,[rbx]
b57048: mov rdi,rbx
b5704b: call [rdx+0x18]
```

There is no instruction between `b56ed4` and `b57042` on this direct taken branch that restores the entry second argument to `rsi`.

Bounded classifications:

```yaml
b57042_receiver_provenance:
  classification: FACT
  value: internal_rbx_object_selected_from_plus_0x80_path
  receiver_exact_dynamic_type: UNKNOWN
b57042_virtual_slot: FACT:+0x10
b57042_concrete_target: UNKNOWN
b57042_rsi_on_taken_branch:
  classification: FACT
  value: 0x100000001
b57042_same_message_preserved:
  classification: DISPROVEN
b57042_is_same_message_edge_to_b40630:
  classification: DISPROVEN
```

This does **not** prove what semantic operation the vslot performs and does not require guessing that the internal object is a refcount/control block. It only proves that this particular call is not the continuation carrying the promoted same message as `b40630`'s second argument.

## Frontier reduction

Before this task, two nested calls were candidates for the unresolved DualConnection reachability edge. After exact dataflow review:

```yaml
candidate_b56c93_same_message_edge: STILL_LIVE_TARGET_UNKNOWN
candidate_b57042_same_message_edge: DISPROVEN
```

The next smallest discriminator is now only:

> Resolve the exact dynamic receiver/vtable used at `0xb56c93`, specifically the `+0x10` target after the `0xb3eda0` / `0xf45cf0` guarded pointer chain, and test `target == 0xb40630`.

No framing, sequence, compression, encryption, final socket ownership or final binary egress semantic claim changes from `UNKNOWN`.

## Negative controls

- no world-map/map evidence used;
- no class-name/vtable-adjacency inference used as target proof;
- `0xb57042` is not relabeled with an unproven destructor/refcount semantic;
- no new raw official client artifact was uploaded;
- no live runtime was observed or mutated.

E2E: `NOT_APPLICABLE` — exact static artifact/dataflow analysis only.
