# Coordinator promotion — post #899 / #900 exact-current boundaries

Date: 2026-09-04
Trusted main at start: `73bf55043e1a46732b30fd0be537742b0ac6fed9`
Exact client: `15.32.be4f48` / `52105824` / `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`

## Coordinator decision

```text
terminal_result=SOURCE_BLOCKER
integration_status=BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
```

No Track B implementation or official-service E2E is unlocked.

## Source PR #899 — sendLogin receiver field +0x88 use semantics

Final PR head: `eb73af287f6a77289404661ff0816524aa16164b`.

Fresh coordinator readback independently confirmed that the analyzer starts at the already-promoted receiver field provenance, resolves the exact field load at `0x7c6b18` through a stack-aware slice, proves the hidden-sret ABI shift for `QObject::connectImpl`, and binds the same value to the formal receiver argument `rcx` at `connectImpl@0x7c6b9f`.

Promoted:

```text
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_RECEIVER_FIELD_LOAD_SITE=0x7c6b18
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
RECEIVER_FIELD_VALUE_USE=QOBJECT_CONNECTIMPL_RECEIVER_ARGUMENT
RECEIVER_FIELD_VALUE_USE_PROVEN=true
CONNECTIMPL_FORMAL_RECEIVER_REGISTER=rcx
SENDLOGIN_ADAPTER_TARGET=0xbd3050
```

Not promoted beyond evidence:

```text
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=false
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=false
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
FIRST_MISSING_BOUNDARY=NO_UNIQUE_OBJECT_TIED_TYPE_EDGE_IN_EXACT_FIELD_VALUE_LIFETIME
```

The source worker's first implementation was scientifically rejected after it treated stale `rcx` state at an unrelated allocation as object-tied evidence. Its repair correctly restricts object-tied calls to the exact receiver carried as `this` in `rdi`; the final exact field-value lifetime contains zero admissible type edges. Coordinator readback finds no basis to re-upgrade receiver identity.

Exact-head qualification:

```text
FOCUSED_RUN=33888349678 success
CI_RUN=33888350117 success
GOVERNANCE_RUN=33888349676 success
SELF_HOSTED_BOUNDARY_RUN=33888349867 success
```

## Source PR #900 — exact queue signal xref/connect discriminator

Final PR head: `28cb4b8d7fccf197129c10e0abfdf6d7f737aa0e`; scientific source head `1970ea47d785387c43c2ff02372d1c038ff17702`.

Coordinator readback independently confirmed that the analyzer first derives the exact queue signal identity from `QMetaObject::activate@0xbd22c2`, including:

```text
QUEUE_STATIC_METAOBJECT=0x30b73e0
QUEUE_METAOBJECT_OWNER=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_METHOD_ROW=0x1ce47c0
QUEUE_SIGNAL_NAME_ADDRESS=0x1ceda8e
QUEUE_SIGNAL_NAME=clientMessageReadyToProcess
```

It then admits only exact signal-specific body/method/name references and exact pointer wrappers. The only signal-specific reference that survives is:

```text
lea@0xbe2e86 -> 0xbd2190
```

inside the already-consumed constructor FDE `0xbe2a50..0xbe3086`. The analyzer correctly classifies that reference as the promoted self-relay QSlot callable, not a downstream source-signal descriptor. No downstream `QObject::connectImpl` site is causally tied to exact signal-specific evidence.

Promoted blocker:

```text
EXACT_SIGNAL_REFERENCE_COUNT=1
EXACT_SIGNAL_CONNECT_CANDIDATE_COUNT=0
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
FIRST_MISSING_BOUNDARY=NO_DOWNSTREAM_CONNECTIMPL_CAUSALLY_TIED_TO_EXACT_SIGNAL_REFERENCES
```

Exact-head qualification:

```text
FOCUSED_RUN=33887506277 success
CI_RUN=33887506379 success
GOVERNANCE_RUN=33887506138 success
SELF_HOSTED_BOUNDARY_RUN=33887506151 success
```

## Independent falsification

Coordinator rejects the following invalid upgrades:

1. `+0x88` being a proven `connectImpl` receiver does **not** prove its class identity.
2. The adapter address `0xbd3050` is not automatically the receiver class or final writer.
3. Absence of downstream exact body/name xrefs does **not** prove absence of a Qt connection registered by method-index/metaobject semantics.
4. The known `0xbe2e86 -> 0xbd2190` reference is consumed self-relay evidence and cannot be relabeled as a new endpoint.
5. Neither source result proves final queue/TCP writer, Field6 value, or pre-success message order.

Material coordinator findings open: `0`.

## Next proof-mode-changing bounded tasks

After this promotion is merged and archived, register exactly two independent source-only successors.

### `OTC-BE4F48-SENDLOGIN-ADAPTER-BD3050-RECEIVER-SEMANTICS`

Change proof mode from receiver-object lifetime/type search to the already-promoted exact adapter callable.

Start only from:

```text
SENDLOGIN_CONNECTIMPL=0x7c6b9f
SENDLOGIN_ADAPTER_TARGET=0xbd3050
RECEIVER_FIELD_LOAD=0x7c6b18
RECEIVER_FIELD_USE=QOBJECT_CONNECTIMPL_RECEIVER_ARGUMENT
```

Inspect the exact QSlot/adapter construction and `0xbd3050` callable semantics to determine whether the adapter uniquely carries, dereferences, or dispatches the same receiver object and whether one exact receiver/member/slot identity can be proven. Follow at most one unique adapter-internal member/call edge.

Do not repeat #884/#889/#894 owner discovery or #899 field-lifetime scans. Do not open a global QSlot/QObject/vtable/caller census.

### `OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION`

Change proof mode from exhausted exact body/name xrefs to exact QMeta method-index connection semantics.

Start only from:

```text
QUEUE_STATIC_METAOBJECT=0x30b73e0
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_METHOD_ROW=0x1ce47c0
QUEUE_SIGNAL_NAME=clientMessageReadyToProcess
QUEUE_SIGNAL_BODY=0xbd2190
```

Search only connection-registration semantics that explicitly combine the exact queue metaobject/method index with a Qt connection primitive or static-metacall/index path. Admit at most one uniquely causal connection site and one endpoint identity edge.

Do not repeat #885/#890/#895 constructor/QSlot work or #900 body/method/name xref enumeration. No generic/global QObject/connect/socket/writer census.

The two successors are independent and may run in parallel. They remain source-only, exact-fenced, fail-closed, and do not authorize Track B #284 mutation or official-service E2E.
