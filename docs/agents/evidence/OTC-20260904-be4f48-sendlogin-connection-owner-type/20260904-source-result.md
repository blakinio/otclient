# Exact-current source result — sendLogin connection owner type

Date: 2026-09-04
Task: `OTC-20260904-be4f48-sendlogin-connection-owner-type`
Source head: `903b7e6c5f9452d9be545d698355bcb151c62aec`
PR: #889

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
EXACT_CLIENT_FENCE_PROVEN=true
```

The package manifest, unpacked size and SHA-256 were exact-guarded before static analysis. The client binary was materialized transiently only for source inspection and removed before artifact upload. It was never executed.

## Bounded result

```text
CONNECTION_OWNER_FDE=0x7c6700..0x7cc933
CONNECTION_OWNER_ENTRY_OBJECT=ENTRY_ARG:rdi
CONNECTION_OWNER_IDENTITY=UNKNOWN
CONNECTION_OWNER_IDENTITY_PROVEN=false
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
FIRST_MISSING_BOUNDARY=UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN
NEXT_ACTION=one newly admitted bounded step only if coordinator authorizes it
```

Within the selected owner FDE, no typed vptr/RTTI event was bound to `ENTRY_ARG:rdi`. The only entry-object-bound direct identity edge admitted by the bounded rule is:

```text
0x7c67b8 -> 0x7e8f30
```

That single adjacent edge did not yield one proven exact type. The search therefore stops there. The consumed #884 direct-caller scan was not repeated, and no global constructor/caller, RTTI/QMeta/QObject/vtable or `+0x88` census was opened.

## Verification evidence

```text
TDD_RED_HEAD=396849b2ce1ae818c3db42ced133f4e1ffca2674
TDD_RED_RUN=33871893625
TDD_RED_JOB=101019573417
TDD_RED_RESULT=expected failure in repository-only contract step

SOURCE_HEAD=903b7e6c5f9452d9be545d698355bcb151c62aec
SOURCE_MERGE_REF_SHA=51a4410e24ee75ed6218e30b5b0e613b00e33792
SOURCE_RUN=33872240794 success
SOURCE_JOB=101020701224 success
ARTIFACT_ID=9936389943
ARTIFACT_DIGEST=sha256:f4fcfd66b409c31ddaf7b06c471eccd33a638d7ff6cdaeeae9c4f47bef147636
CI_RUN=33872241316 success
GOVERNANCE_RUN=33872241004 success
SELF_HOSTED_BOUNDARY_RUN=33872240809 success
RAW_CLIENT_RETAINED=false
```

The uploaded artifact contains only deterministic sanitized `result.json`; artifact size is 1097 bytes. No proprietary client bytes were uploaded.

## Safety

Source-only static analysis. No official-client execution, login, credential/session/cookie/character/world access, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, queue/QSlot/writer work, Track B mutation, or guessed protocol value/order.
