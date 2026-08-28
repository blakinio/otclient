# V3 exact-current field6 observation — terminal pre-action timeout

Date: 2026-08-28

## Identity

- exact owner trigger comment: `5456592899`;
- trigger body: `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true`;
- trigger author association: `OWNER`;
- trigger created at: `2026-08-28T19:03:21Z`;
- workflow: `Track A current login field6 runtime observation`;
- run: `33202129157`;
- job: `98953921602`;
- exact tested trusted main: `32146659213cba71910cbe8d46aa4c2f6ded607c`;
- terminal status: `completed`;
- terminal conclusion: `cancelled`.

GitHub live state does not contain comment `5456601015`; the REST endpoint returns `404 Not Found`. That earlier locator is rejected. The existing owner comment `5456592899` precedes the issue-comment workflow run by two seconds and is the authoritative V3 trigger identity.

The trigger and run are consumed historical evidence and must not be rerun or replayed.

## Proven timeline and boundary

The job began at `2026-08-28T19:03:31Z`. The package preflight began at approximately `19:04:00Z`; WARP/SOCKS passed at `19:04:09Z`. GitHub cancelled the operation at `19:21:40Z`, matching the job-level `timeout-minutes: 18` boundary. The task-owned package cleanup marker was emitted at `19:21:44Z`, and runner cleanup ended at approximately `19:21:48Z`.

Before materialization, the task-owned WARP/SOCKS path passed:

```text
TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=1
```

The materializer then emitted no terminal package markers before:

```text
##[error]The operation was canceled.
```

Cleanup remained ownership-safe and completed:

```text
TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS
```

## Root cause

The exact V3 materializer at `32146659213cba71910cbe8d46aa4c2f6ded607c` iterates every manifest row serially. Every row performs a separate task-owned SOCKS `curl`, packed size/hash verification, unpacking, and unpacked size/hash verification before the next row begins. A single invocation is bounded, but the aggregate full-package duration is not bounded below the 18-minute job deadline.

The V3 log suppresses per-file names, sizes, and timings. Therefore the identity of any individual slow download is **UNKNOWN**. There is no evidence that WARP failed, and there is no evidence sufficient to claim one specific `curl` hung. The directly proven defect is cumulative serial full-package acquisition exceeding the job deadline.

## No-action result

V3 never consumed the owner authorization and never entered the credential-bearing capture step:

```text
physical_action_count=0
login_submit_count=0
FIELD6_VALUE=UNKNOWN
```

No official client runtime capture, character selection, world entry, gameplay, network-payload capture, credentials retention, packet retention, process-environment retention, or raw-memory retention occurred.

## Repair boundary

The next implementation must remain `runtime_access: none`, preserve full package and exact-client verification, and replace serial file acquisition with bounded deterministic concurrency. No repair PR may execute downloaded Tibia content or perform a live login. A later observation requires a separately reviewed docs-only V4 admission and a new distinct owner trigger.
