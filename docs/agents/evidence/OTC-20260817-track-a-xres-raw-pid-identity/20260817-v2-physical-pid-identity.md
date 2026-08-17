# Track A raw XRes PID identity — conclusive v2 physical evidence

Task: `OTC-20260817-track-a-xres-raw-pid-identity`  
PR: #457  
Physical run: `32015479835`  
Hosted preflight job: `95343925201 = SUCCESS`  
Physical job: `95344000918`  
Runner: `synology-otclient-01`

## Final classification

```yaml
physical_discriminator: PASS_EVIDENCE_CAPTURED
xres_server_version: '1.2'
viewable_candidate_xid: '0x00c00011'
viewable_candidate_geometry: '1920x1080'
reply_client_base: '0x00c00000'
reply_mask: LocalClientPid
reply_value_length_bytes: 4
reply_pid: 13648
exact_launched_client_pid: 13648
XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT: true
wrapper_classification: FALSE_NEGATIVE_DUE_TO_OVERSTRICT_CLIENT_BASE_CHECK
cleanup: COMPLETE
canonical_state_access: NONE
login: false
gameplay: false
process_memory_access: false
client_bytes_mutated: false
```

## Admission and isolation

Same-job Track A runtime governance passed before the physical boundary:

```text
TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1
TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS=1
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
XRES_RAW_V2_RUNTIME_ADMISSION=PASS
```

The generated sandbox was task-owned and run-attempt scoped:

```text
WINDOW_DIAG_NAMESPACE=/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260817-track-a-xres-raw-pid-identity/ephemeral-32015479835-1
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
```

Exact source/support fences passed and exactly one v2 exact-client process was launched:

```text
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
WINDOW_DIAG_CLIENT_PID=13648
WINDOW_DIAG_CLIENT_START=PASS
```

## Final t35 X11 candidate

At t35 the task-owned client was alive. The raw X11 tree contained exactly one VIEWABLE 1920x1080 candidate:

```text
XRES_RAW_V2_CANDIDATE_COUNT=t35:1
XRES_RAW_V2_WINDOW=t35:xid=0x00c00011:map=2:geom=1920x1080
```

The fresh local X11/XRes connection reported XRes 1.2:

```text
XRES_RAW_V2_VERSION=t35:1.2:major_opcode=148:sequence=2
```

The exact QueryClientIds(LocalClientPid) reply for queried resource `0x00c00011` was preserved before helper interpretation:

```text
0100030004000000010000000000000000000000000000000000000000000000
0000c000020000000400000050350000
```

Little-endian bounded decode:

- reply sequence = `3`;
- reply payload length = `4` words / `16` bytes;
- `numIds = 1`;
- returned client identifier = `0x00c00000`;
- mask = `0x02` (`LocalClientPid`);
- value byte length = `4`;
- value = `0x00003550` = decimal `13648`.

The returned LocalClientPid therefore equals the exact process PID launched and fenced by the same task: `13648 == 13648`.

## Why returned client is a base and not the queried resource XID

Primary XRes protocol semantics allow a client to be selected by any resource XID owned by it. The X server implementation resolves the owner using the client portion of the requested resource XID, then `ConstructClientIdValue` writes `rep.spec.client = client->clientAsMask` into the reply. In other words, the response identifies the owning client by its resource base; it is not required to echo the exact queried resource ID.

This exactly matches the observed pair:

```text
queried resource: 0x00c00011
returned client base: 0x00c00000
returned LocalClientPid: 13648
```

Primary references used for the semantic cross-check:

- XRes protocol specification (`xorgproto/resproto.txt`), `CLIENTXID` / `CLIENTIDSPEC` / `XResQueryClientIds` semantics;
- X server `Xext/xres.c`, `ConstructClientIds` and `ConstructClientIdValue`, where request resources are mapped to a client and reply `spec.client` is set to `client->clientAsMask`.

## Wrapper false negative

The trusted-main helper correctly parsed the v2 byte-length after #455, but `extract_local_client_pid()` still required `record.client == resource_xid`. The physical server returned the owning client's resource base instead, so the helper raised:

```text
XResWireError: QueryClientIds reply did not identify the requested resource
```

That check is disproven as a valid requirement for this server implementation. The wrapper consequently emitted `XRES_RAW_V2_IDENTITY_UNRESOLVED`, but the raw reply retained enough information to independently and unambiguously prove ownership.

No further physical launch is needed or authorized for this identity question. Any helper API correction belongs to the persistent helper owner and can be validated host-side from this retained real reply fixture.

## Cleanup

The generated script completed normally (`RC=0`) and the task-owned cleanup path emitted:

```text
WINDOW_DIAG_CLEANUP=COMPLETE
```

The GitHub job is red only because its final assertion expected the overstrict wrapper classification. It does not represent a client/runtime failure.

## Terminal result

`XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT`

The exact official-client X11 resource-to-PID identity gate is physically satisfied for the bounded isolated discriminator. This evidence may be consumed by later separately admitted RUNTIME work; it does not itself authorize canonical bootstrap/login, process-memory access, gameplay, or client-byte mutation.