# OTC-BE4F48 sendLogin receiver field owner — terminal source result

Exact-current source-only analysis for Tibia Linux client `15.32.be4f48` reached the bounded terminal result `SOURCE_BLOCKER`.

## Proven

- exact client fence: size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`;
- promoted receiver provenance remains `OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]`;
- repository-only TDD RED was observed before any client materialization: run `33865752388`, job `101000116304`, failed because `receiver_field_owner.py` was intentionally absent and all WARP/client steps were skipped;
- after the analyzer was added, exact-current run `33866338005`, job `101001945445`, completed successfully and emitted a sanitized result;
- the bounded target-specific direct-caller search for connection-owner FDE `0x7c6700..0x7cc933` produced zero direct caller candidates.

## Terminal boundary

Because the allowed owner/caller chain cannot advance uniquely from the selected connection-owner FDE, the field initializer/type cannot be claimed without widening into a disallowed global constructor/owner search.

```text
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_FIELD_DEFINITION=UNKNOWN
SENDLOGIN_RECEIVER_OWNER_CHAIN=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=false
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CONNECTION_OWNER_FDE_DIRECT_CALLER_NOT_UNIQUE
```

This is fail-closed: zero candidates is not treated as a guessed owner or constructor identity. The bounded-search rule stops here rather than starting a global `+0x88`, RTTI, QMeta, QObject, or constructor census.

## Exact-head evidence

Source head `29d30b7de6a59bfa0a40c619abfbf3f3061692e1`:

```text
SOURCE_RUN=33866338005 success
SOURCE_JOB=101001945445 success
ARTIFACT_ID=9934120718
ARTIFACT_DIGEST=sha256:2a8313249628076f1daef8766ac07ae6adf4fdc72e5f232f6b955ceaa4b62614
CI_RUN=33866338387 success
GOVERNANCE_RUN=33866337998 success
SELF_HOSTED_BOUNDARY_RUN=33866338017 success
RAW_CLIENT_RETAINED=false
```

The exact workflow log also reports `BE4F48_SENDLOGIN_RECEIVER_FIELD_OWNER_REPOSITORY_CONTRACT=PASS`, `BE4F48_SENDLOGIN_RECEIVER_FIELD_OWNER_EXACT_FENCE=PASS`, and `BE4F48_SENDLOGIN_RECEIVER_FIELD_OWNER_SANITIZED_RESULT=PASS`.

## Safety and disposition

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
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
```

No runtime or official-service E2E applies to this source-only discriminator. The next lifecycle action is a clean coordinator promotion after the parallel queue-signal QSlot source lane has its own terminal durable result. This source PR must not broaden into that lane or mutate Track B.
