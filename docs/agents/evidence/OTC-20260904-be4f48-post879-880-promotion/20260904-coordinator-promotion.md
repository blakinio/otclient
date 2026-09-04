# Coordinator promotion — exact-current be4f48 post #879/#880

Decision: **SOURCE_BLOCKER / BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA**.

This promotion is rebuilt from trusted `main@f7a471c2cc7ab7fd53afacc8a7458eeefb96ad97` and consumes only sanitized exact-current facts from source Draft PRs #879 and #880. Neither source analyzer/workflow is promoted. Track B PR #284 remains untouched.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Promoted sendLogin-side facts (#879)

The selected `QObject::connectImpl@0x7c6b9f` receiver argument is now stack-aware proven to originate from `OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]`. Inside the selected connection-owner FDE `0x7c6700..0x7cc933`, that field has 165 reads and **zero writes**. Therefore the receiver class/ownership definition is outside this FDE and remains UNKNOWN.

```text
sender=tibia::authentication::TLoginProtocolMessageHandler
signal=sendLoginMessage
adapter=0xbd3050
receiver_provenance=[entry-rdi-derived-rbx+0x88]
receiver_identity=UNKNOWN
sendlogin_causal_binding_proven=false
FIRST_MISSING_BOUNDARY=RECEIVER_FIELD_DEFINITION_OUTSIDE_SELECTED_CONNECTION_OWNER_FDE
```

Source #879 final head `7bbbc1f1e5c02f31a71999333ba5423649e3d94a`; exact analysis `33854810739` / job `100965538997`; artifact `9929762469`, digest `sha256:eb9212da7acc41e0d67fc7c6a85740c846ac961faddf2ea0e79c49cdd684fd72`. Final exact-head focused/CI/governance/self-hosted runs: `33856163340`, `33856163561`, `33856163288`, `33856163258`, all SUCCESS.

## Promoted queue/writer-side facts (#880)

The queue signal is now bound source-only without broad whole-executable Capstone disassembly. Exact facts:

```text
sender=tibia::protocol::TProtocolMessageQueue
signal_index=0xbf
signal_name=clientMessageReadyToProcess
signal_body=0xbd2190
static_metaobject=0x30b73e0
static_metaobject_argument_chain=0xbd221d:rbp -> 0xbd22ae:rsi -> 0xbd22c2
connectImpl_candidate_count=1
connectImpl_callsite=0xbe2eee
connectImpl_fde=0xbe2a50..0xbe3086
receiver_provenance=ENTRY_ARG:rdi
qslot_function=UNKNOWN
writer_identity=UNKNOWN
FIRST_MISSING_BOUNDARY=QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN
```

The exact queued `GameclientMessage` shared pair remains causally consumed and delivered as `argv[1]`. The selected QSlot object is passed as `r9 <- rax` after a call-return boundary at `0xbe2eb1`, but the QSlot function target is not uniquely proven. No writer identity is promoted from generic Qt/socket candidates.

Source #880 final head `2b640340864c599851c07f9e31564a5644b8628d`; exact analysis `33856767530` / job `100971771959`; artifact `9930504401`, digest `sha256:0eae231ded57a47aa7ea2dfa37339b2a2e465a0e1b031e618e95dccd04da8f6f`. Final exact-head focused/CI/governance/self-hosted runs: `33857039832`, `33857040196`, `33857039745`, `33857039810`, all SUCCESS.

## Withheld / integration decision

```text
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
SENDLOGIN_RECEIVER_CLASS=UNKNOWN
QUEUE_SIGNAL_QSLOT_FUNCTION=UNKNOWN
FINAL_QUEUE_WRITER=UNKNOWN
FINAL_TCP_WRITER=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
```

Therefore no Track B mutation, runtime Field6 experiment, OCR/Vision run, login, or official-service E2E is authorized.

## Next bounded source tasks

Exactly two independent follow-ups are justified and may run in parallel:

```text
OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-OWNER
  Start from [entry-rdi-derived-rbx+0x88]. Resolve only the field initializer/ownership chain that can type the receiver object. Stop at the first non-unique constructor/owner edge.

OTC-BE4F48-QUEUE-SIGNAL-BF-QSLOT-IDENTITY
  Start from the unique connectImpl@0xbe2eee / FDE 0xbe2a50..0xbe3086 and call-return boundary 0xbe2eb1. Resolve only the QSlot object/function identity and at most one unique identity-preserving writer edge.
```

No global constructor/Qt/socket/writer census. #284 remains blocked and unchanged.
