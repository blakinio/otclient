# Track A hosted raw-XRes wire helper validation

## Scope

Canonical task: `OTC-20260816-track-a-canonical-runtime-e2e`  
Research Draft: `#447`  
Trusted base: `main@55803133a5abe8b1e75e4660da1d2b84b154ab9a`

This phase is intentionally transport-free. It implements only pure byte encoding/parsing for the promoted XRes 1.2 identity path and performs no socket, X11 server, official-client, Synology or canonical-state access.

## Promoted protocol basis

The helper consumes the already-promoted support facts:

- XRes target protocol version `1.2`;
- QueryVersion minor opcode `0`;
- QueryClientIds minor opcode `4`;
- LocalClientPid mask `0x02`;
- QueryClientIds fixed request header size `8` bytes;
- QueryClientIds fixed reply header size `32` bytes.

The extension major opcode remains a caller-provided value that a future physical transport must obtain separately from core X11 `QueryExtension`. This hosted phase performs no QueryExtension or transport operation.

## Implementation

Helper:

`.github/scripts/tibia-official-client-re-xres-wire.py`

Current helper blob:

`ce5992bc1171eef9f24a71dfc97da728f18627a9`

The module is fail-closed and pure. It provides:

- QueryVersion(1.2) request encoding for little/big endian;
- exact fixed-size QueryVersion reply parsing with reply-type, declared-length and optional sequence checks;
- minimum server-version enforcement (`>= 1.2`);
- one-resource QueryClientIds request encoding for LocalClientPid;
- bounded QueryClientIds reply parsing with configured byte/id/value caps;
- strict declared-size, record-size and trailing-payload checks;
- unambiguous LocalClientPid extraction only when a one-spec query yields exactly one record matching the requested resource, exact LocalClientPid mask and exactly one positive CARD32 PID.

## Coordinator review hardening

An initial green 32-test generation still allowed one fail-closed ambiguity: a one-resource request could accept one matching target record plus an unrelated extra record because extraction filtered the target and ignored the extra result.

The review finding was repaired before source closeout:

- any non-empty one-spec result must contain exactly one record total;
- an extra unrelated record now causes rejection;
- a dedicated negative fixture proves this boundary.

## Validation

First dedicated workflow generation failed only because the workflow invoked the test file with a hyphen/underscore path typo after both files had compiled successfully. That workflow path was corrected once; no runtime or parser failure was involved.

A later 32-test generation passed, then coordinator review added the stricter one-record boundary above.

Final dedicated validation on semantic helper head `06c6f18fc4a8920428ca353173b0596758a0190a`:

- workflow run `32001448940`;
- job `95302425720`;
- result `SUCCESS`;
- Python compile: `PASS`;
- deterministic unit tests: `33/33 PASS`;
- AST purity contract: `XRES_WIRE_PURE_TRANSPORT_FREE=PASS`.

The 33 fixtures cover:

- exact little/big-endian QueryVersion request bytes;
- exact little/big-endian QueryClientIds request bytes;
- valid QueryVersion and LocalClientPid replies;
- server version below 1.2;
- wrong reply type;
- sequence mismatch;
- truncation;
- declared length mismatch;
- unexpected trailing payload;
- byte/id/value caps;
- zero resource XID;
- wrong target mask;
- wrong PID value shape;
- zero PID;
- missing requested resource;
- duplicate requested-resource records;
- target plus unrelated extra record;
- zero-ID reply as unresolved (`None`) rather than fabricated identity.

Track A governance on the same semantic head: run `32001448948`, both admission jobs `SUCCESS`.

## Purity boundary

The dedicated workflow parses the helper AST and permits imports only from:

- `__future__`;
- `dataclasses`;
- `struct`.

It rejects transport/process/filesystem/network primitives including socket, subprocess, os, pathlib, urllib, requests, http, asyncio, open, exec and eval. Final result is `XRES_WIRE_PURE_TRANSPORT_FREE=PASS`.

## Classification

`PROVEN_HOSTED_RAW_XRES_WIRE_CODEC_FAIL_CLOSED_AND_TRANSPORT_FREE_WITH_33_DETERMINISTIC_FIXTURES`

## Non-claims

This validation does not prove:

- XRes is present on a future physical X server;
- the server reports XRes >= 1.2;
- the viewable XID belongs to the exact official-client PID;
- any current canonical display/session/PID exists;
- canonical bootstrap or window-identity relaxation is safe.

## Next action

Coordinator must independently review and promote the persistent helper/test/workflow code. Only after that promotion may the canonical task freshly admit one task-owned isolated physical identity discriminator that obtains the XRes extension opcode, verifies QueryVersion >= 1.2, queries LocalClientPid for the raw viewable XID and compares it directly to the exact fenced client PID. No canonical bootstrap/login/gameplay is authorized by this evidence.
