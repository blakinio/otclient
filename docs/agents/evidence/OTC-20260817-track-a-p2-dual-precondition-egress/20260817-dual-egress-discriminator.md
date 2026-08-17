# Track A P2 DualConnection egress discriminator — Draft evidence

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-dual-precondition-egress`  
Draft PR: #458  
Research status: **DRAFT / NOT PROMOTED**  
Promotion authority: coordinator only

## Exact-client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Evidence generation

One bounded generation ran on exact experiment head `37c455f2ab3170457a0d084a7745eaa42e28aff1`:

- workflow run `32016842999` = `SUCCESS`;
- source job `95348018877` = `SUCCESS`;
- hosted decode job `95348295109` = `SUCCESS`;
- source artifact `9283851546`, digest `sha256:7e03ed66bff463e288b5f2414bad8190a27bf421161ba1218c2a74d7342baeab`;
- final artifact `9283858910`, digest `sha256:2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c`;
- experiment-head Track A governance run `32016848906` = `SUCCESS`.

The source stage verified the retained regular file by exact size/SHA and copied exactly three enumerated executable-file windows totalling `0xe20` / 3616 bytes. It performed no disassembly or semantic classification, accessed no client process/process memory/canonical runtime, executed no client and uploaded no raw ELF/package. Disassembly occurred on GitHub-hosted Ubuntu.

The accepted non-quarantined #310 artifact `9252025461` was independently re-hashed as `sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991` and is used only to cross-check PLT symbol identities for the same exact client SHA. Quarantined run `31944051248` is not used as proof.

## Primary correction: the historical window name overreached the function boundary

The historical artifact described the broad byte range as `dual_precondition_0xb40370`. Fresh exact bytes show that this label must **not** be interpreted as one function extending through `0xb4066b`.

`0xb40370` has its own entry/prologue and all observable control paths return by `0xb40421`:

```text
b40370: push r12
...
b403dc: movzx eax,bpl
b403e0: pop rbx
b403e1: pop rbp
b403e2: pop r12
b403e4: ret
...
b4040c: pop rbx
b4040d: xor eax,eax
b4040f: pop rbp
b40410: pop r12
b40412: ret
...
b40418: pop rbx
b40419: mov eax,0x3
b4041e: pop rbp
b4041f: pop r12
b40421: ret
```

A different function begins at `0xb40430`, and the candidate write belongs to another distinct entry beginning at `0xb40630`:

```text
b40630: push r13
b40632: push r12
b40634: mov  r12,rsi
b40637: push rbp
b40638: push rbx
b40639: mov  rbx,rdi
```

Therefore:

```yaml
claim: b4066b_is_inside_TGameserverDualConnection_plus_0x90_function_b40370
classification: DISPROVEN
```

The earlier broad-window naming is provenance only, not a function-boundary proof.

## Exact `0xb40630` dataflow

Fresh hosted disassembly gives:

```text
b40634: mov  r12,rsi                    # preserve original second argument
b40639: mov  rbx,rdi                    # preserve this
b40640: mov  rax,[rdi]
b40643: call [rax+0x78]
b40649: mov  rbp,rax                    # save +0x78 result
b4064c: mov  rax,[rbx]
b4064f: mov  r13,[rax+0x88]             # save virtual +0x88
b40656: call 0x4dac00
b4065b: mov  rdi,rbx
b4065e: mov  rsi,[rax+0x10]
b40662: call r13
b40665: mov  rsi,r12                    # restore original second argument
b40668: mov  rdi,rbx                    # same this as receiver
b4066b: call 0x4de370
b40670: mov  rax,[rbx]
b40673: mov  rsi,rbp
b40676: mov  rdi,rbx
b40679: mov  rax,[rax+0x88]
...
b4068a: jmp  rax
```

Accepted exact-SHA artifact `9252025461` resolves the two load-bearing imported targets as:

```text
0x4dac00 = QBuffer::buffer()
0x4de370 = QIODevice::write(QByteArray const&)
```

The fresh staged bytes independently reproduce those exact call targets.

### Receiver classification

At `0xb4066b`, SysV arguments are directly established:

```text
rdi = rbx = original function this
rsi = r12 = original function second argument
```

The same `rbx`/`this` is also passed to `QBuffer::buffer()` immediately before the write. Therefore:

```yaml
qiodevice_write_receiver:
  classification: FACT
  value: b40630_this_rbx
  structural_base: QBuffer/QIODevice-compatible object at this address
  exact_concrete_dynamic_type: UNKNOWN
qiodevice_write_payload:
  classification: FACT
  value: original_b40630_second_argument_rsi
```

This is enough to reject `0xb4066b` as a **direct `TGameserverTCPConnection::QTcpSocket*` write site**. The direct receiver is the same QBuffer-compatible `this`, not the separately proven `TGameserverTCPConnection +0x10 -> QTcpSocket*` member.

This does **not** prove that an unknown subclass could never forward data elsewhere, and it does not identify the global final socket sink. The bounded correct classification is:

```yaml
direct_qtcpsocket_sink_at_b4066b: DISPROVEN
final_binary_egress: UNKNOWN
final_socket_ownership: UNKNOWN
```

## Relationship to the promoted same-message chain

Coordinator PR #450 promoted the exact chain:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

Fresh windows for `0xb56970..0xb56d60` and `0xb56d60..0xb57280` contain no direct call to `0xb40630`. They do contain indirect virtual `+0x10` calls on nested objects (`0xb56c93`, `0xb57042`), but the staged evidence does not resolve those nested vtables to `0xb40630`.

Therefore no exact edge currently binds the original argument of `0xb40630` to the promoted same post-RawDataProcessor message:

```yaml
payload_relationship_to_promoted_same_message: UNKNOWN
b40630_reachable_from_promoted_dualconnection_plus_0x78_or_plus_0x80: UNKNOWN
```

No vtable adjacency or source-range proximity is used as a reachability claim.

## Hypothesis disposition

Initial H1 stated that the `0xb4066b` write is the concrete binary gameplay egress candidate reachable after the promoted same-message handoff into `TGameserverDualConnection`.

Result:

```yaml
H1: DISPROVEN_IN_STATED_FORM
reason:
  - b4066b is not inside the b40370 +0x90 function
  - its direct QIODevice receiver is the b40630 QBuffer-compatible this object, not a proven QTcpSocket member
  - no exact edge from the promoted +0x78/+0x80 same-message path to b40630 was recovered
```

This is useful negative evidence. It removes another false final-socket shortcut without inventing a replacement sink.

## Remaining P2 classifications

```yaml
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
final_socket_ownership: UNKNOWN
complete_transport_stage_order_beyond_promoted_chain: UNKNOWN
```

No semantic label is inferred from `QBuffer`, `RawDataProcessor`, `DualConnection`, method naming, vtable adjacency or workflow success.

## Negative controls preserved

- `0xb46bd0`: FACT writes QString/local-8-bit plus newline through the proven `TGameserverTCPConnection::QTcpSocket*`; DISPROVEN as binary gameplay-frame proof.
- `0xc33259`: DISPROVEN, QMatrix4x4/non-network candidate.
- `0xb5b880`: SUPERSEDED endpoint model; must not be promoted again.
- run `31944051248`: quarantined routing provenance; not current proof.

## Researcher disposition

`DRAFT_NOT_PROMOTED / READY_FOR_COORDINATOR_REVIEW`.

The coordinator should independently inspect source artifact `9283851546`, final artifact `9283858910`, the exact instruction/dataflow above and the accepted symbol-identity cross-check from artifact `9252025461`. The coordinator may accept the bounded negative result, return for a narrower receiver-vtable/reachability discriminator, or supersede it with stronger evidence.

Physical/runtime E2E: `NOT_APPLICABLE` — static file-byte/disassembly evidence only; no client/runtime/network state was changed or observed.