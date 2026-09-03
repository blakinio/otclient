# OTC-20260903-be4f48-queue-drain-consumption source result

## Terminal classification

```text
TERMINAL_RESULT=QUEUE_DRAIN_CONSUMPTION_PROVEN
EXACT_CLIENT_FENCE_PROVEN=true
SERIALIZED_QUEUE_OBJECT_IDENTITY_PROVEN=true
OWNED_DRAIN_CALLBACK=0xbd2190
QUEUED_GAMECLIENTMESSAGE_CAUSAL_CONSUMPTION=true
NEXT_UNIQUE_WRITER_EDGE=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
FIRST_MISSING_BOUNDARY=TProtocolMessageQueue signal 0xbf carrying the exact queued GameclientMessage shared_ptr -> unique connected receiver/writer edge
```

## Exact source run

```text
source_pr=874
source_head=4471ccf1e396794ae0d2ce3de97d0474284e6fee
workflow_run=33783945122
workflow_job=100744062650
artifact_id=9904688934
artifact_digest=sha256:7d707d2820a891c6d91f974b305d657227587c65aeac2d7ba8557dd04cab4778
result_json_sha256=47ac0c9f8dc79d024a8eaa484474bd8e33bf9cf2407458c2a2bc8256211ddb70
```

The job re-read public current launcher metadata through the repository's secret-free WARP pattern and proved the exact current tuple remained:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
PUBLIC_CURRENT_EXACT_FENCE=PASS
CURRENT_CLIENT_EXACT_FENCE=PASS
RAW_CLIENT_RETAINED=false
```

Only the sanitized `result.json` artifact persisted. The official client was never executed.

## Re-proved producer identity

The new analyzer independently re-proved the local producer chain instead of trusting PR #870's analyzer implementation:

```text
0xbd3070 call 0x4d8670                  allocation
0xbd3087 mov rbx,rax                    owner/control allocation
0xbd3099 lea r15,[rbx+0x10]             object pointer
0xbd31bc mov [rsp],r15                   pair qword 0 = object
0xbd31c0 mov [rsp+8],rbx                 pair qword 1 = owner
queue RTTI=tibia::protocol::TProtocolMessageQueue
queue vtable address point=0x30ed588
queue vslot +0x68=0xbd24a0
queued object RTTI=tibia::protobuf::protocol::GameclientMessage
```

It then re-proved `0xbd24a0` copies all 16 bytes from the incoming pair into queue storage and advances the queue end by exactly `0x10`.

## Causal drain proof

Inside only the owned FDE `0xbd2190..0xbd2495`, the analyzer proved these linked relations:

1. `0xbd2306` loads queue begin from `this+0x70`; `0xbd230a` compares it to queue end `this+0x90`.
2. `0xbd2317` copies one exact 16-byte queue element to `xmm1`; `0xbd231b` separately loads the element's owner qword; `0xbd231f` writes the same 16-byte pair to `rsp+0x10`.
3. `0xbd233d` increments the copied owner's refcount, preserving shared ownership for the copied pair.
4. The original queue entry is retired and `0xbd229a..0xbd22a2` advances queue begin by exactly one 16-byte element.
5. `r13` is the address of `rsp+0x10`; immediately before `0xbd22c2`, the callback constructs Qt argv such that `argv[1] = r13`.
6. `0xbd22c2` directly calls exact target `0x4d7dc0`, the promoted `QMetaObject::activate(QObject*, QMetaObject const*, int, void**)`, with sender `TProtocolMessageQueue this`, static metaobject `0x30b73e0`, signal index `0xbf`, and `argv[1]` pointing to the exact copied `{object,owner}` pair.
7. `0xbd22c7` reloads the copied owner qword after that dispatch, independently confirming the copied owner lifetime spans the semantic consumer call.

These relations prove causal consumption of the queued `GameclientMessage` shared-pointer identity by the owned queue callback.

## Why the writer is still withheld

The exact identity reaches `QMetaObject::activate`, but the bounded callback contains no uniquely bound connected receiver/writer target. Proving one would require a separate, specifically authorized Qt connection/receiver discriminator. This task therefore does not infer a writer from address proximity, names, generic networking calls, or a broad socket/QMeta/TCP scan.

Consequently:

```text
NEXT_UNIQUE_WRITER_EDGE=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
```

## Falsification notes

The positive causal claim survives the following checks:

- changing the exact client version/size/SHA causes fail-closed termination;
- changing the adapter pair, queue RTTI/vslot or insertion pattern causes fail-closed termination before drain classification;
- changing any local queue-begin pair-copy, owner-refcount, one-element advance, Qt argv propagation, signal index or exact direct dispatch target causes the drain proof to fail;
- no positive writer claim is emitted without a unique next edge plus an independent ownership/vtable/caller cross-check.

The implementation required no evidence-derived semantic correction after its first exact-current run. One unrelated governance repair restored seven mandatory `NOT_APPLICABLE` source-only admission keys in the active task record; it did not change analyzer semantics.

## Safety and cross-track isolation

```text
runtime_access=none
official_client_execution=false
login_performed=false
credential_access=false
process_memory_access=false
packet_capture=false
ocr_vision_used=false
official_service_e2e_count=0
raw_client_uploaded=false
track_b_pr_284_modified=false
field6_value=UNKNOWN
```

## Next action

Consume only these sanitized facts in a clean coordinator promotion from fresh trusted `main`, then close Draft source PR #874 unmerged as consumed. Do not extend #874 into global Qt/writer discovery and do not mutate Track B PR #284 from this source task.
