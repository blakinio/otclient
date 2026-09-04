# Exact-current coordinator promotion — post #894 / #895

Date: 2026-09-04
Trusted base: `main@7e67c67783b19575ec7f378c7be49cb69d87f1ce`
Exact client: `15.32.be4f48` / `52105824` / `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`

## Decision

```text
terminal_result=SOURCE_BLOCKER
integration_status=BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
```

The two source PRs are terminal and exact-head qualified, but neither proves an implementable Track B wire change.

## Promoted #894 boundary

PR #894 final head `2e8f797ad0230b9a4338bd44ff98fc562010e422` preserves the exact owner-bound call `0x7c67b8 -> 0x7e8f30`. The callee FDE is `0x7e8f30..0x7f06d6`.

Promoted facts:

```text
OWNER_OBJECT_PROVENANCE=ENTRY_ARG:rdi carried by promoted 0x7c67b8->0x7e8f30 edge
OWNER_OBJECT_IDENTITY=UNKNOWN
OWNER_OBJECT_IDENTITY_PROVEN=false
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
FIRST_MISSING_BOUNDARY=CALLEE_INTERNAL_IDENTITY_EDGE_NOT_FOUND
```

Coordinator falsification rejects any inference from the absence of a typed vptr or internal edge to a guessed class identity. The source analyzer found no same-object external constructor/metaobject call and zero admissible same-object internal identity-edge candidates in the admitted callee FDE.

Final checks:

```text
focused=33881287522 success
ci=33881287951 success
governance=33881287474 success
self_hosted_boundary=33881287646 success
```

## Promoted #895 boundary

PR #895 final head `6e853a400831431ad3c3489828b34441dab86636` consumes the already-promoted queue receiver/self-relay facts and exhausts only the admitted queue-constructor connection context.

Promoted facts:

```text
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
SELF_RELAY_CONNECTIMPL_CALLSITE=0xbe2eee
QSLOT_FUNCTION_TARGET=0xbd2190
QUEUE_CONSTRUCTOR_FDE=0xbe2a50..0xbe3086
DIRECT_CONNECTIMPL_CALLS=0xbe2e54,0xbe2eee
AFTER_SELF_RELAY_CONNECT_COUNT=0
ADDITIONAL_EXACT_SIGNAL_IDENTITY_PRESERVING_CANDIDATE_COUNT=0
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
QUEUE_SIGNAL_WRITER_IDENTITY=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIRST_MISSING_BOUNDARY=NO_NEXT_CLIENTMESSAGEREADYTOPROCESS_SOURCE_CONNECTION_IN_BOUNDED_QUEUE_CONSTRUCTOR_FDE
```

Coordinator falsification rejects treating `0xbe2e54` as the next queue-signal connection: the exact signal body/static-metaobject evidence required by the bounded discriminator is absent there. It also rejects interpreting the lack of a constructor-local next connection as proof that no downstream connection exists elsewhere.

Final checks:

```text
focused=33881260048 success
ci=33881260365 success
governance=33881260072 success
self_hosted_boundary=33881260116 success
```

## Withheld claims

The promotion explicitly does **not** prove:

```text
SENDLOGIN_OWNER_CLASS=UNKNOWN
SENDLOGIN_RECEIVER_CLASS=UNKNOWN
COMPLETE_SENDLOGIN_SENDER_RECEIVER_PAIR=NOT_PROVEN
SENDLOGIN_CAUSAL_BINDING=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
NEXT_QUEUE_SIGNAL_ENDPOINT=UNKNOWN
FINAL_QUEUE_WRITER=UNKNOWN
FINAL_TCP_WRITER=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
```

Track B PR #284 remains untouched and blocked from protocol mutation/E2E based on these results.

## Coordinator-selected proof-mode changes

The consumed paths have reached their bounded terminal states. The next research must not repeat them.

### `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS`

Start from the already-promoted `+0x88` receiver-field provenance at the sendLogin connection context and reason about the loaded field object's immediate use/ABI semantics. Permit at most one object-tied vptr/QMeta/type edge. Do not search for the owner class again and do not perform a global `+0x88` field census.

### `OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE`

Start from the exact queue signal identity/body and admit only exact-signal reference sites that can be causally tied to a `QObject::connectImpl` setup. This is an exact-signal discriminator, not a generic connect/QObject/socket census. Classify at most one unique downstream endpoint and stop on non-uniqueness.

Both successors remain source-only and exact-fenced. They may run in parallel after separate alias registration.

## Safety

```text
runtime_access=none
official_client_executed=false
login_performed=false
credentials_used=false
process_memory_access=false
packet_capture=false
ocr_vision_used=false
official_service_e2e_count=0
track_b_pr_284_modified=false
```