# Track A raw XRes PID identity — v2 final audit

Task: `OTC-20260817-track-a-xres-raw-pid-identity`  
PR: #457  
Audited physical run: `32015479835`  
Audited physical job: `95344000918`

## Audit question

Does the retained v2 physical evidence directly bind the unique VIEWABLE `1920x1080` X11 resource to the exact fenced official-client process, without relying on the failed wrapper classification?

## Independent decode

Raw t35 facts from the job log:

```text
WINDOW_DIAG_CLIENT_PID=13648
XRES_RAW_V2_CANDIDATE_COUNT=t35:1
XRES_RAW_V2_WINDOW=t35:xid=0x00c00011:map=2:geom=1920x1080
XRES_RAW_V2_VERSION=t35:1.2:major_opcode=148:sequence=2
XRES_RAW_V2_REPLY_HEX=t35:xid=0x00c00011:sequence=3:hex=01000300040000000100000000000000000000000000000000000000000000000000c000020000000400000050350000
WINDOW_DIAG_CLEANUP=COMPLETE
```

The QueryClientIds reply is 48 bytes. The 32-byte fixed reply declares four CARD32 words of trailing payload and one returned ID. The 16-byte payload decodes little-endian as:

```text
client = 0x00c00000
mask = 0x00000002
length = 4 bytes
value = 0x00003550 = 13648
```

Therefore LocalClientPid equals the exact launched process PID.

## Protocol-semantic cross-check

The wrapper expected the returned `CLIENTIDVALUE.spec.client` to equal the queried resource `0x00c00011`. That expectation is not valid for the observed X server implementation.

Primary X server semantics:

1. `ConstructClientIds` accepts the requested resource ID and computes the owning X client via the resource's client-id portion (`CLIENT_ID(spec.client)`).
2. `ConstructClientIdValue` emits `rep.spec.client = client->clientAsMask` for the selected client.
3. For LocalClientPid it emits mask `0x02`, byte length `4`, and one CARD32 PID.

Thus the observed response `0x00c00000 / LocalClientPid / 13648` is the expected response for a resource such as `0x00c00011` owned by that X client.

The XRes protocol specification likewise permits a client to be selected by a resource allocated by that client and documents resource-base as a client identifier.

Primary references checked independently outside the implementer summary:

- X.Org xorgproto `resproto.txt`, XRes client-id specification and QueryClientIds semantics;
- X.Org X server `Xext/xres.c`, `ConstructClientIds` and `ConstructClientIdValue`.

## Audit matrix

| Check | Result |
|---|---|
| exact official-client source fence before launch | PASS |
| task-owned isolated namespace | PASS |
| Track A runtime admission | PASS |
| exactly one v2 client launch | PASS |
| client live PID independently captured | PASS (`13648`) |
| one final VIEWABLE 1920x1080 candidate | PASS (`0x00c00011`) |
| XRes >= 1.2 | PASS (`1.2`) |
| raw QueryClientIds reply retained before helper interpretation | PASS |
| reply LocalClientPid equals exact client PID | PASS (`13648 == 13648`) |
| returned client-base semantics supported by server implementation | PASS |
| wrapper exact-XID equality requirement | DISPROVEN / false-negative source |
| canonical state touched | NO |
| credentials/login/gameplay | NO |
| process memory | NO |
| client bytes mutated | NO |
| cleanup | PASS |
| one-shot v2 workflow/patcher retained in terminal PR tree | NO |

## Findings

No finding invalidates the physical ownership result.

`XRES-V2-AUD-001` — **LOW / helper follow-up**: persistent helper `extract_local_client_pid(records, resource_xid)` still assumes returned `record.client` must equal the exact queried resource. The real X server returns the owning client resource-base. This should be corrected by the persistent helper owner using the retained v2 reply as a deterministic regression fixture. It does not require another physical client launch and does not reduce the confidence of the raw physical identity proof.

## Audit disposition

```yaml
physical_identity: PROVEN
classification: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
material_findings_open_for_this_task: 0
nonblocking_helper_findings: 1
additional_physical_retry_required: false
additional_physical_retry_authorized: false
cleanup: COMPLETE
one_shot_runtime_surfaces_retained: false
```

The physical identity discriminator is complete. The consumed v2 one-shot workflow and patcher are absent from the terminal PR tree. Later runtime work must obtain its own admission; this result alone does not authorize canonical bootstrap/login, process-memory access, gameplay, or client-byte mutation.