# Track A P2 DualConnection egress discriminator — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-dual-precondition-egress`  
Source Draft: PR #458, final head `c3a3d8339a9fb769847011ffb76662688d91f06c`  
Coordinator disposition: **ACCEPT_WITH_EDITS**

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Independent verification

The coordinator did not use the researcher summary as proof. The following live evidence was independently checked:

- source generation `32016842999` / job `95348018877` re-fenced the retained exact regular ELF by size and SHA and staged exactly three bounded executable-file windows; source-side operation was file-byte mapping only, with no client execution, process-memory access, canonical runtime access, disassembly or semantic classification;
- source artifact `9283851546` uploaded with digest `sha256:7e03ed66bff463e288b5f2414bad8190a27bf421161ba1218c2a74d7342baeab`;
- hosted decode job `95348295109` independently checked the exact ranges/digests and instruction anchors and uploaded final artifact `9283858910` with digest `sha256:2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c`;
- final source head Track A governance `32018496831 = SUCCESS` and repository CI `32018496866 = SUCCESS`;
- final PR #458 changed-file inventory is exactly the two durable evidence files plus the source task record; reviews and review threads are empty.

The accepted non-quarantined #310 artifact remains the exact-SHA symbol-identity cross-check for `0x4dac00 = QBuffer::buffer()` and `0x4de370 = QIODevice::write(QByteArray const&)`. Quarantined run `31944051248` is not proof.

## Accepted bounded facts

Fresh exact bytes establish that the old broad `0xb40370` window label crossed a function boundary:

- `0xb40370` returns on observed paths by `0xb40421`;
- `0xb40630` is a distinct function entry;
- therefore `0xb4066b` is not inside the `0xb40370` / DualConnection `+0x90` function.

At `0xb40630`, exact SysV dataflow establishes:

```text
b40634: mov r12,rsi
b40639: mov rbx,rdi
...
b40656: call 0x4dac00
...
b40665: mov rsi,r12
b40668: mov rdi,rbx
b4066b: call 0x4de370
```

Promoted classifications:

```yaml
b4066b_inside_b40370_plus_0x90_function: DISPROVEN
b40630_distinct_function_entry: FACT
b4066b_qiodevice_write_callsite: FACT
b4066b_receiver: FACT:b40630_this_rbx_QBuffer_QIODevice_compatible
b4066b_receiver_exact_concrete_dynamic_type: UNKNOWN
b4066b_payload: FACT:original_b40630_second_argument_rsi
b4066b_direct_qtcpsocket_sink: DISPROVEN
payload_relationship_to_promoted_same_message: UNKNOWN
b40630_reachability_from_promoted_dualconnection_plus_0x78_or_plus_0x80: UNKNOWN
```

The direct receiver at `0xb4066b` is the same `this` passed to `QBuffer::buffer()`. It is not proven to be the separately established `TGameserverTCPConnection +0x10 -> QTcpSocket*` member. This disproves the direct-QTcpSocket interpretation only; it does not prove the concrete dynamic subtype or rule out internal forwarding by an unknown subclass.

Fresh `TGameserverDualConnection +0x78/+0x80` windows contain no direct call to `0xb40630`. They do contain nested indirect `+0x10` virtual calls at `0xb56c93` and `0xb57042`; their receiver object/vtable targets are not resolved by the accepted package.

## Hypothesis disposition

The prior hypothesis that `0xb4066b` is the concrete gameplay binary/socket egress reachable from the promoted same-message DualConnection handoff is **DISPROVEN_IN_STATED_FORM**.

No replacement final sink is promoted.

## Canonical P2 state after this promotion

The prior #450 chain remains canonical:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

Additionally, the `0xb4066b` direct write and negative reachability result above are canonical only within their bounded classification.

Still `UNKNOWN`:

- reachability from the promoted DualConnection path to `0xb40630`;
- relationship of the `0xb40630` second argument to the promoted same message;
- concrete dynamic type of the `0xb40630` receiver;
- framing;
- sequence;
- compression;
- encryption;
- final binary egress;
- final socket ownership;
- complete transport stage order beyond the promoted #450 chain.

## Next falsifiable frontier

Resolve the receiver provenance and concrete virtual target(s) for the two nested `+0x10` calls at `0xb56c93` and `0xb57042`, using exact-client object construction/vtable evidence. The task must answer only whether either call reaches `0xb40630` or another exact function target and whether the same-message argument is preserved across that edge. Absence of a resolvable edge remains `UNKNOWN`; vtable adjacency or address proximity is not proof.

This is the smallest current static discriminator that can either establish or falsify the missing DualConnection reachability edge without guessing framing, crypto, compression or final socket ownership.

## Audit / E2E

Fresh coordinator review: `PASS_BOUNDED`; material findings open: `0`.

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence promotion only; no live client/runtime/network state changed or observed.
