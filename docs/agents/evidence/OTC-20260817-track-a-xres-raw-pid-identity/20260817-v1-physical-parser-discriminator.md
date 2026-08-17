# Track A raw XRes PID identity — v1 physical parser discriminator

```yaml
task: OTC-20260817-track-a-xres-raw-pid-identity
pr: 455
physical_run: 32013868595
hosted_preflight_job: 95339063640
physical_job: 95339104951
runner: synology-otclient-01
runtime_access: ephemeral_isolated
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
V1_PHYSICAL_LAUNCH_EXECUTED: true
V1_CLIENT_LAUNCH_COUNT: 1
XRES_QUERY_VERSION_PROVEN: true
XRES_SERVER_VERSION: '1.2'
XRES_QUERY_CLIENT_IDS_PID_IDENTITY: NOT_PROVEN
FAILURE_CLASS: PROMOTED_HELPER_PROTOCOL_PARSER_DEFECT
CLEANUP: COMPLETE
CANONICAL_STATE_ACCESS: NONE
LOGIN: false
GAMEPLAY: false
PROCESS_MEMORY_ACCESS: false
CLIENT_BYTES_MUTATED: false
```

## Admission and isolation evidence

The valid physical generation ran only after the task checkpoint declared a task-owned `ephemeral_isolated` namespace and Track A runtime governance passed on the exact PR generation.

The generated harness rebound the inherited historical task marker to:

```text
OTC-20260817-track-a-xres-raw-pid-identity
```

and created this run-scoped namespace:

```text
/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260817-track-a-xres-raw-pid-identity/ephemeral-32013868595-1
```

The run reported:

```text
XRES_RAW_TASK_OWNER=OTC-20260817-track-a-xres-raw-pid-identity
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
POST_RHI_SUPPORT_FENCE=PASS
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
WINDOW_DIAG_WARP=PASS
WINDOW_DIAG_CLIENT_START=PASS
```

No canonical lease, canonical registration, canonical state directory, credentials, login, gameplay or process-memory access was used by this discriminator.

## Physical observation

The exact client was launched once in the task-owned isolated sandbox. The raw transport discovered the `X-Resource` extension on the same fresh XCB connection and the promoted codec successfully performed QueryVersion:

```text
XRES_RAW_VERSION=t05:1.2:major_opcode=148:sequence=2
```

Therefore the physical environment directly proves that the isolated X server implements XRes 1.2 and accepts the promoted QueryVersion wire shape.

The next one-spec QueryClientIds(LocalClientPid) reply reached the promoted parser, which raised:

```text
XResWireError: QueryClientIds client-id value payload is truncated
```

The generated script returned nonzero and the workflow did **not** promote XID-to-PID identity.

## Root-cause discriminator

Primary XRes 1.2 protocol/server behavior defines `CLIENTIDVALUE.length` as the byte length of the value payload. For LocalClientPid the server emits:

```text
length = 4
value  = one CARD32 PID
```

The promoted #448 helper instead treated `length` as a count of CARD32 values and calculated `value_bytes = length * 4`. For a correct LocalClientPid `length=4`, it therefore expected sixteen payload bytes instead of four and failed closed as truncated.

This is a deterministic helper-parser defect. It is not evidence that XRes lacks LocalClientPid, not evidence that the queried XID is foreign, and not a reason to relax the parser or runtime identity gate.

## Repair boundary

PR #455 corrects the helper so that:

```text
value_length_bytes = CLIENTIDVALUE.length
require value_length_bytes % 4 == 0
value_count = value_length_bytes / 4
payload_end = fixed_record_end + value_length_bytes
```

The fixture builder now encodes LocalClientPid with `length=4`, and the test suite adds an explicit four-byte-length regression plus a non-CARD32-aligned-length rejection case.

The one-shot v1 physical workflow and transform patchers were removed from the terminal #455 tree. A second client launch on this v1 branch is not authorized. After the helper fix reaches trusted `main`, the same task must create a fresh physical-authorized-v2 branch/admission for any retry.

## Cleanup proof

The physical run ended with:

```text
WINDOW_DIAG_CLEANUP=COMPLETE
```

The task-owned client/display/WARP/VNC sandbox was therefore cleaned by the bounded task-marker/role cleanup path even though QueryClientIds parsing failed.

## Current classification

```yaml
xres_query_version: PROVEN
xres_query_client_ids_transport_reached_parser: PROVEN
xres_local_client_pid_semantics_in_physical_reply: CONSISTENT_WITH_PRIMARY_PROTOCOL_EVIDENCE
xid_to_exact_client_pid_identity: NOT_PROVEN
promoted_helper_parser_correct_before_fix: DISPROVEN
v1_physical_retry_authorized: false
next_phase: HOSTED_HELPER_FIX_VALIDATION_THEN_FRESH_V2_PHYSICAL_ADMISSION
```
