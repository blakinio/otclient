# Exact-current source result — sendLogin owner edge `0x7c67b8 -> 0x7e8f30`

Date: 2026-09-04
Task: `OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity`
PR: #894
Scientific source head: `9c68d92657100b054c6d5006ab46ddc5303112ee`
Workflow run: `33880393758`
Job: `101047349555`
Artifact: `9939610461`
Artifact digest: `sha256:ae15b1091e72ca4a4ae5eb970fe91695189f2248582a6519286660a03d646877`

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
EXACT_CLIENT_FENCE_PROVEN=true
```

The workflow verified the live package manifest against the exact version, unpacked size and SHA-256 before static analysis. The official client was materialized only as transient bytes for static inspection, was never executed, and was deleted before artifact upload (`RAW_CLIENT_RETAINED=false`).

## TDD boundary

Repository-only RED was observed first at head `684e301ada1feef6590fc59b3375a19c547f16a8`, run `33879930241`, job `101045813815`:

```text
AssertionError: edge_identity.py is missing: expected RED before client materialization
```

All WARP/client-materialization/result steps were skipped in that RED run.

## Bounded scientific result

```text
OWNER_EDGE_CALLSITE=0x7c67b8
OWNER_EDGE_CALLEE=0x7e8f30
OWNER_EDGE_CALLEE_FDE=0x7e8f30..0x7f06d6
OWNER_OBJECT_IDENTITY=UNKNOWN
OWNER_OBJECT_IDENTITY_PROVEN=false
OWNER_IDENTITY_PROOF_CLASSES=[]
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=false
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=false
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CALLEE_INTERNAL_IDENTITY_EDGE_NOT_FOUND
NEXT_ACTION=one newly admitted bounded step only if coordinator authorizes it
```

Within only the callee FDE `0x7e8f30..0x7f06d6`, no primary vptr store tied to the carried `ENTRY_ARG:rdi` object resolved to one exact Itanium RTTI type. The analyzer also found no same-object external constructor/metaobject call and no direct internal call whose `rdi` backward-sliced uniquely to that same entry object. Because the permitted one-edge continuation set is empty, no internal edge was followed and the task stops fail-closed.

This result does not repeat #884 caller discovery or #889 owner-FDE scanning and does not open a global constructor, RTTI, QMeta, QObject, vtable, `+0x88`, queue, QSlot or writer census.

## Safety and withheld claims

```text
OFFICIAL_CLIENT_EXECUTED=false
LOGIN_PERFORMED=false
CREDENTIALS_USED=false
PROCESS_MEMORY_ACCESS=false
PACKET_CAPTURE=false
OCR_VISION_USED=false
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
```

No owner class, receiver class, complete sender/receiver pair, sendLogin causal binding, Field6 value, pre-success send order or Track B wire delta is claimed.
