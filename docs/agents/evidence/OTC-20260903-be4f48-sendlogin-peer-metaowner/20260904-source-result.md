# OTC-20260903-be4f48-sendlogin-peer-metaowner — terminal source result

## Decision

`SOURCE_BLOCKER`

The exact-current source-only discriminator materially advanced the sendLogin connection boundary but did not satisfy the positive acceptance gate. The peer owner, signal identity, exact local `QObject::connectImpl` call, sender direction and sendLogin slot-object binding are now proven. The receiver object's **class identity** remains unproven, so the complete sender/receiver pair and causal `sendLogin` binding remain withheld.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
trusted_main=446eb643d6ef24dc996a410df812393e19800973
source_analysis_head=6174d44df2017bc5a435de0e843ee824520a12a5
source_pr=#875
```

No runtime observation was used. The official client was never executed; the exact ELF existed only transiently inside the GitHub-hosted static workflow and was deleted before sanitized JSON upload.

## TDD evidence

Repository-only REDs occurred before any exact-client materialization:

```text
initial RED: run=33783290711 job=100741903966 head=df2d291073ab6c6b3a716d40639d94fad3550226
v3 ABI RED: run=33837464949 job=100912796002 head=c86500f8d110bac43c582738213e5ea1458c3d30
sret audit RED: run=33837902877 job=100914066665 head=64472af5ebca95c116198010dc343387a6f2cb15
```

Each failed in the repository-only contract and skipped package preparation/client materialization.

Final exact-current static run:

```text
run=33838135600
job=100914746055
head=6174d44df2017bc5a435de0e843ee824520a12a5
conclusion=success
artifact=9923975240
digest=sha256:e96c91c2b8bf408c06ff829ac25d48d39595f719a275e7361886cea93cb7d8ff
```

## Peer metaobject — proven

The static metaobject `0x30b68a0` decodes as:

```text
owner=tibia::authentication::TLoginProtocolMessageHandler
signal_index=0
signal_name=sendLoginMessage
method_count=7
signal_count=7
```

This independently resolves the owner of peer signal body `0xd052a0`.

## Exact Qt connection — proven

Inside the already bounded owner FDE `0x7c6700..0x7cc933`, the exact construction block is bounded by the previous `QObject::connectImpl` at `0x7c6b07` and the selected call at `0x7c6b9f`.

The block contains exactly one adapter reference and one peer reference:

```text
0x7c6b34 -> 0xbd3050  sendLogin adapter
0x7c6b40 -> 0xd052a0  sendLoginMessage peer signal
0x7c6b5e -> operator new(unsigned long)
0x7c6b9f -> QObject::connectImpl(...)
```

The selected primitive is exactly:

```text
QObject::connectImpl(QObject const*, void**, QObject const*, void**,
                     QtPrivate::QSlotObjectBase*, Qt::ConnectionType,
                     int const*, QMetaObject const*)
```

## Hidden-sret ABI — proven from the exact ELF

The analyzer does not assume the C++ return ABI. It requires exact binary evidence:

```text
0x7c6b69  mov rdi, rbp   # connectImpl return storage
0x7c6b9f  call QObject::connectImpl
0x7c6ba8  mov rdi, rbp   # same storage passed to destructor
0x7c6bab  call QMetaObject::Connection::~Connection()
```

Therefore the formal arguments are mapped after the hidden return-storage pointer:

```text
rsi     sender
rdx     signal
rcx     receiver
r8      slotPtr
r9      QSlotObjectBase
stack0  connection type
stack8  types
stack16 senderMetaObject
```

The three stack arguments resolve to `0`, `0`, and metaobject `0x30b68a0` respectively.

## Signal / adapter dataflow — proven

The signal argument resolves through a stack address to the exact peer function:

```text
0x7c6b40 -> peer 0xd052a0
0x7c6b50 -> store peer pointer
rdx/r12 -> address of that stored pointer
```

The sendLogin adapter is embedded into the allocated Qt slot object before `connectImpl`:

```text
0x7c6b34 -> adapter 0xbd3050
0x7c6b3b -> stack scratch
0x7c6b5e -> operator new
0x7c6b6c -> load adapter-bearing 16-byte payload
0x7c6b7c -> r9 = allocated slot object
0x7c6b86 -> store payload at [r9+0x10]
0x7c6b9f -> QObject::connectImpl
```

Together with `senderMetaObject=0x30b68a0`, this proves:

```text
sender_endpoint_identity=tibia::authentication::TLoginProtocolMessageHandler
peer_signal_name=sendLoginMessage
sendlogin_adapter_bound_to_connection=true
```

## Remaining fail-closed boundary

The receiver formal argument has exact local provenance from an entry-object field:

```text
receiver <- rcx <- saved [rbx+0x88]
rbx <- owner-FDE entry rdi
```

No bounded exact-current evidence in this task identifies the class of that receiver object. The analyzer therefore deliberately keeps:

```text
receiver_endpoint_identity=UNKNOWN
sendlogin_causal_binding_proven=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=SENDER_RECEIVER_ENDPOINT_IDENTITY_NOT_PROVEN
```

No receiver type was inferred from adjacency, the slot adapter, or the sender class.

## Audit / safety

Fresh whole-diff falsification found one material issue: the first v3 draft modeled the hidden-sret shift without independently proving it from the exact ELF. Finding `SRET-001` was remediated by the exact storage/destructor proof above and revalidated by run `33838135600`. No material audit findings remain in the static source result.

```text
runtime_access=none
official_client_executed=false
login_performed=false
credentials_used=false
secret_access=false
process_memory_access=false
packet_capture=false
official_service_e2e_count=0
raw_client_uploaded=false
track_b_pr_284_modified=false
```

E2E is `NOT_APPLICABLE`: this source-only discriminator explicitly forbids official-client execution/login/runtime observation.

## Coordinator handoff

Promote only the sanitized facts above from a clean current `main`. Keep Track B PR #284 unchanged. Source PR #875 should be consumed and closed unmerged after promotion, following the same lifecycle used for the preceding source blockers. If receiver class identity is still valuable, admit it as a new bounded source task rather than widening this lane.
