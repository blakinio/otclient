# OTC-BE4F48 sendLogin receiver identity — terminal source result

Exact-current source-only analysis for Tibia Linux client `15.32.be4f48` completed at source head `12070c649dd2e5e1f237fd524a3c48e7ca8375a0`.

## Proven

- exact client fence: size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`;
- promoted sender remains `tibia::authentication::TLoginProtocolMessageHandler::sendLoginMessage`;
- selected `QObject::connectImpl` callsite remains `0x7c6b9f` and QSlot adapter remains `0xbd3050`;
- stack-aware slicing proves the selected receiver argument at `connectImpl` comes from the exact object field `[entry-rdi-derived-rbx+0x88]` through stack scratch;
- inside the selected owner FDE `0x7c6700..0x7cc933`, `[rbx+0x88]` is read 165 times and written 0 times.

## Withheld / terminal boundary

The receiver class/ownership identity is not defined inside the selected FDE. Therefore:

```text
receiver_endpoint_identity=UNKNOWN
complete_sender_receiver_pair_proven=false
sendlogin_causal_binding_proven=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=RECEIVER_FIELD_DEFINITION_OUTSIDE_SELECTED_CONNECTION_OWNER_FDE
```

Do not extend this source PR into a global constructor/owner sweep. A later receiver-field owner discriminator, if admitted by coordinator promotion, must be a new bounded source task.

## Exact-head evidence

```text
SOURCE_RUN=33854810739 success
SOURCE_JOB=100965538997 success
ARTIFACT_ID=9929762469
ARTIFACT_DIGEST=sha256:eb9212da7acc41e0d67fc7c6a85740c846ac961faddf2ea0e79c49cdd684fd72
CI_RUN=33854811068 success
GOVERNANCE_RUN=33854810851 success
SELF_HOSTED_BOUNDARY_RUN=33854810677 success
```

Safety remained source-only: no official-client execution, login, credentials, process memory, packet capture, OCR/Vision, official-service E2E, or Track B PR #284 mutation.
