# OTC-20260903-be4f48-sendlogin-sender-peer — terminal source result

## Decision

`SOURCE_BLOCKER`

The exact-current source lane advanced one fact but did not satisfy the positive acceptance gate. The peer target `0xd052a0` is now statically proven to be a Qt signal body, but the promoted helper target `0x4d8670` is statically proven to be `operator new(unsigned long)`, not a Qt connection primitive. Therefore sender/receiver direction and the causal signal-to-`sendLogin` binding remain unproven.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
trusted_main=a35bbacd475a31ce52736ccbc3b5e837626def66
source_head=df9febe6f2817a606093898318595982222f056c
source_pr=#869
```

No runtime observation was used. The official client was never executed; the exact ELF existed only transiently in the GitHub-hosted static workflow and was deleted before sanitized JSON upload.

## TDD evidence

Initial RED:

```text
run=33776945999
job=100720910769
head=6295381433c38949ae8af0ab51468243bf827274
repository-only contract=FAIL
Prepare exact public client package through WARP=SKIPPED
Materialize transient exact client=SKIPPED
```

The one permitted evidence-derived PLT follow-up also had an independent repository-only RED before any client materialization:

```text
run=33777802812
job=100723755748
head=56d4684105118ff7e50a1503ffcc3e514754691e
repository-only contract=FAIL
Prepare exact public client package through WARP=SKIPPED
Materialize transient exact client=SKIPPED
```

## Exact source evidence

Stage 1 exact run:

```text
run=33777474194
job=100722673198
head=12af7ca291bc88ea4868a6abfcb32efb9b6a4248
conclusion=success
artifact=9902213010
digest=sha256:6a0d3d3fdec009c009c8ed359a45bca85119d16fc1e2a2155e672ce698ac66b3
```

It established:

```text
peer_target=0xd052a0
peer_fde=0xd052a0..0xd052c7
peer_instruction_count=9
peer_direct_call_target=0x4d7dc0
peer_vtable_memberships=[]
peer_constructor_vtable_xrefs=[]
peer_owner_identity=UNKNOWN
adapter_reference_site=0x7c6b34
promoted_helper_target=0x4d8670
sender_endpoint_identity=UNKNOWN
receiver_endpoint_identity=UNKNOWN
sendlogin_causal_binding_proven=false
```

The one permitted bounded follow-up resolved only the two PLT targets already exposed by Stage 1:

```text
run=33778038445
job=100724556224
head=df9febe6f2817a606093898318595982222f056c
conclusion=success
artifact=9902452300
digest=sha256:cbe454857fd778f0d989918553f8c999d80ab3dd0c866bcbcd638f3b78ffef89
```

### Peer role — proven

Exact peer FDE:

```text
0xd052a0  sub rsp,0x18
0xd052a4  xor edx,edx
0xd052a6  mov [rsp+8],rsi
0xd052ab  mov rcx,rsp
0xd052ae  lea rsi,[rip+...] -> 0x30b68a0
0xd052b5  mov [rsp],0
0xd052bd  call 0x4d7dc0
0xd052c2  add rsp,0x18
0xd052c6  ret
```

PLT target `0x4d7dc0` resolves through GOT slot `0x31756c8` to:

```text
mangled=_ZN11QMetaObject8activateEP7QObjectPKS_iPPv
demangled=QMetaObject::activate(QObject*, QMetaObject const*, int, void**)
```

The peer body passes signal index `0` (`edx=0`) and static-metaobject pointer `0x30b68a0` before invoking `QMetaObject::activate`. This proves the callable role:

```text
peer_role=QT_SIGNAL_BODY_CALLING_QMETAOBJECT_ACTIVATE
```

It does **not** by itself prove the class owner or which connection endpoint consumes this signal.

### Promoted helper role — disproven as connection primitive

PLT target `0x4d8670` resolves through GOT slot `0x3175b20` to:

```text
mangled=_Znwm
demangled=operator new(unsigned long)
helper_role=ALLOCATOR_OPERATOR_NEW
```

Therefore the previously promoted label `connection_helper_target=0x4d8670` cannot be used as sender/receiver direction authority. The target is an allocator call occurring in the bounded construction region, not a Qt connection primitive.

## Withheld conclusions

The following remain deliberately `UNKNOWN` / not proven:

```text
peer_class_owner=UNKNOWN
sender_endpoint_identity=UNKNOWN
receiver_endpoint_identity=UNKNOWN
actual_qt_connection_primitive=UNKNOWN
causal_signal_to_sendlogin_binding=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
safe Track B delta=NOT_PROVEN
```

No attempt was made to broaden into a new call graph, final-writer work, runtime observation, OCR/Vision, credentials, official-service E2E, or a third discriminator.

## Safety / Track B

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

## Terminal boundary

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=PROMOTED_HELPER_TARGET_IS_ALLOCATOR_NOT_A_CONNECTION_PRIMITIVE
```

## Coordinator handoff

A clean coordinator promotion should preserve the newly proven peer role and correct the helper interpretation. If a later source task is authorized, it may start from the newly exposed exact peer static-metaobject anchor `0x30b68a0` and/or recover the actual bounded Qt connection primitive. It must not reuse `0x4d8670` as direction authority, and this lane does not authorize any mutation of Track B PR #284.
