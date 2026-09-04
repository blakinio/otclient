# Source qualification evidence

Task: `OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics`
Draft PR: #899

## TDD RED

Initial repository-only RED:

```text
HEAD=f0d94c0e6a16dff41e8135bbd4a2700c70172cd6
RUN=33886750137
JOB=101068292328
RESULT=expected failure
FIRST_ERROR=AssertionError: receiver_field_use_semantics.py is missing: expected RED before client materialization
CLIENT_MATERIALIZATION=skipped
```

The missing-analyzer assertion failed before WARP/package/client steps, as required.

## First source run and falsification

The first implemented source head was deliberately not accepted as scientific qualification after fresh falsification exposed an admission bug:

```text
HEAD=4c309fd088257d9f94fc6a0ecdaa316be0445030
RUN=33887133223
JOB=101069574567
WORKFLOW_RESULT=success
SCIENTIFIC_RESULT=rejected
```

The analyzer admitted a stale exact receiver value still present in `rcx` at `operator new(unsigned long)@0x7c6b5e` as an object-tied call candidate. Root cause: candidate admission scanned every ABI argument register while the only admitted statically followable object call edge was receiver-as-`this` in `rdi`.

Regression RED:

```text
HEAD=0573a784ce3554345ea1c9730f664f95b17d5cd2
RUN=33887477954
JOB=101070712173
RESULT=expected failure
FIRST_ERROR=AssertionError: missing receiver-field-use contract token: OBJECT_TIED_THIS_REGISTER = "rdi"
CLIENT_MATERIALIZATION=skipped
```

Minimal repair: restrict direct object-tied call admission to the exact receiver value in `rdi`; forbid the previous generic `for reg in ARG_REGS` proof mode.

## Accepted exact-current source run

```text
SOURCE_HEAD=9397bb9eb44c7566a789f6a310e20c0da7845923
SOURCE_RUN=33887723682
SOURCE_JOB=101071529772
SOURCE_RESULT=success
ARTIFACT_ID=9942554299
ARTIFACT_DIGEST=sha256:b9da2ed976d0fb93dcd84f337c71e8e2a5a963124abd61ae62e18cb4215e19ef
CI_RUN=33887724009 success
GOVERNANCE_RUN=33887723710 success
SELF_HOSTED_BOUNDARY_RUN=33887723792 success
RAW_CLIENT_RETAINED=false
```

Exact public client fence:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

Accepted scientific result:

```text
EXACT_CLIENT_FENCE_PROVEN=true
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
RECEIVER_FIELD_VALUE_USE=QOBJECT_CONNECTIMPL_RECEIVER_ARGUMENT
RECEIVER_FIELD_VALUE_USE_PROVEN=true
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
FIRST_MISSING_BOUNDARY=NO_UNIQUE_OBJECT_TIED_TYPE_EDGE_IN_EXACT_FIELD_VALUE_LIFETIME
```

The exact receiver field load is `0x7c6b18`. The value is preserved through the bounded stack slice and reaches the formal receiver register `rcx` at `QObject::connectImpl@0x7c6b9f`. Hidden sret handling is independently bounded by the matching `QMetaObject::Connection` destructor path. After the regression repair, the exact field-value lifetime contains zero admitted object-tied `this`/primary-vptr type edges before the selected connect call, so identity remains fail-closed as `UNKNOWN`.

## Safety

`runtime_access=none`. The official client was never executed. No login, credentials, session/cookie/character/world access, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, or Track B PR #284 mutation occurred. Exact client bytes existed only transiently for static ELF analysis and were deleted before sanitized artifact upload.
