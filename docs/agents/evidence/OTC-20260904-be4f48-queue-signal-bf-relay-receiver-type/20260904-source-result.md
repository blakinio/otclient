# OTC-20260904-be4f48-queue-signal-bf-relay-receiver-type — source result

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
exact_client_fence_proven=true
```

The successful source run was GitHub Actions run `33873246506`, job `101024010911`, source head `7dab5a0cb60f9f971ff0623aa0d5b9922bbbcd65`. The sanitized artifact is `9936796961`, digest `sha256:9dd2bb0d11af5240b5f0275df89f8b4bccabb3af8d19461642619883ebcc3879`.

## TDD and repair evidence

- Initial RED: run `33872253528`, job `101020741944`. The repository-only contract failed before WARP/client materialization because the analyzer was intentionally absent.
- First implementation run: `33872716592`, job `101022270664`, completed successfully as a workflow but returned the source blocker `ENTRY_RDI_RECEIVER_PROVENANCE_NOT_REPROVEN`. Its bounded trace nevertheless exposed the constructor-tied root-vptr store at `0xbe2a85`.
- Repair RED: run `33872908681` failed at the repository-only contract after the test was changed to require explicit consumption of the already-promoted receiver provenance; all later client-materialization steps were skipped.
- Repair GREEN: run `33873246506`, job `101024010911`, completed all exact-fence, transient-materialization, source-analysis, sanitized-validation, and sanitized-artifact steps successfully.

The repair does not widen the research scope. `ENTRY_ARG:rdi` at `QObject::connectImpl@0xbe2eee` is a promoted exact-current input from the prior receiver-provenance task and coordinator promotion, so this task consumes it rather than attempting to re-prove it across unrelated caller-saved-register clobbers inside the enclosing constructor FDE.

## Bounded receiver identity proof

Within only the admitted FDE `0xbe2a50..0xbe3086`:

```text
QObject::QObject(QObject*) call = 0xbe2a6d
entry-object root vptr store   = 0xbe2a85
object alias/base register     = rbx
object offset                  = 0x0
vptr                           = 0x30ed588
typeinfo                       = 0x30ed548
typeinfo name pointer          = 0x1d77cc0
typeinfo raw name              = N5tibia8protocol21TProtocolMessageQueueE
demangled exact type           = tibia::protocol::TProtocolMessageQueue
connectImpl callsite           = 0xbe2eee
connectImpl target             = 0x4d6800 / QObject::connectImpl(...)
```

The primary-vptr ABI header has `offset_to_top=0`. The object-tied RTTI name is unique and demangles to `tibia::protocol::TProtocolMessageQueue`, therefore:

```text
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_RECEIVER_IDENTITY_PROVEN=true
```

## Exact connection role

Promoted inputs already establish:

```text
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QSLOT_FUNCTION_TARGET=0xbd2190
```

The exact receiver is the same `tibia::protocol::TProtocolMessageQueue` owner whose promoted QSlot target is the `clientMessageReadyToProcess` signal body. The exact connection is therefore classified:

```text
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
```

No next identity-preserving relay edge was uniquely established within the admitted receiver-type proof, so the analysis stops rather than widening into a global connect/QObject/QSlot/socket/writer search.

## Terminal boundary

```text
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
FIRST_MISSING_BOUNDARY=NEXT_RELAY_EDGE_NOT_UNIQUELY_PROVEN_WITHIN_BOUNDED_RECEIVER_TYPE_PROOF
terminal_result=QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_PROVEN
NEXT_ACTION=clean coordinator promotion before any Track B decision
```

## Safety

```text
RUNTIME_ACCESS=none
OFFICIAL_CLIENT_EXECUTED=false
LOGIN_PERFORMED=false
CREDENTIALS_USED=false
PROCESS_MEMORY_ACCESS=false
PACKET_CAPTURE=false
OCR_VISION_USED=false
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
```

Only transient exact public client bytes were materialized in the GitHub-hosted source-analysis job and removed before artifact publication. The retained artifact is sanitized `result.json` only.
