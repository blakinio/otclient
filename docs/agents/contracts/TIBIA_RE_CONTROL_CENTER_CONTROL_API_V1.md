# TIBIA RE Control Center Control API Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-CONTROL-API-V1
version: 1.2
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: none
remote_exposure: forbidden_in_v1
artifact_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
```

## 1. Purpose

Define one bounded local-only operator transport so browser and CLI invoke exactly the same Control Center domain operations without creating a second execution implementation.

This contract covers transport authentication, Host/Origin/anti-framing trust, request/resource idempotency, crash replay, bounds, event delivery and shutdown. It does not grant Track A authority and does not authorize remote/LAN control.

Normative execution semantics remain in Execution v1. Global RequestLedger, ResourceIdentityLedger and ControlState persistence are normative in Artifact v1.

## 2. Threat model

Loopback binding is insufficient by itself. Defend against at least:

- unrelated local web pages attempting cross-origin requests;
- DNS rebinding to loopback;
- hostile framing/clickjacking of the real operator UI;
- browser/CLI retries and lost responses;
- crash after request identity allocation but before scheduling/response;
- duplicate tabs/operators;
- oversized/malformed requests;
- slow event consumers;
- backend restart;
- accidental wildcard/non-loopback bind.

This is not a hostile same-OS-user privilege boundary. A malicious process under the same trusted user may access local credential/files; that requires a separate OS security design.

## 3. Bind policy

Default:

```text
127.0.0.1:<ephemeral-or-configured-port>
```

Rules:

- `0.0.0.0`, `::` and all non-loopback addresses are forbidden;
- `::1` may be enabled only explicitly and must preserve all v1 trust rules;
- bind failure is terminal; no silent fallback to another interface;
- chosen `host:port` is non-secret runtime status, not mutation authority;
- remote/LAN exposure requires a separately reviewed new security profile/major contract.

## 4. Backend control credential

Each backend process creates a fresh random `control_nonce` bound to its fresh `backend_epoch`.

```yaml
entropy_bits_minimum: 256
reuse_across_restart: false
persist_to_run_artifacts: false
loggable: false
```

Requirements:

- memory and/or mode-0600 backend runtime file owned by current OS user only;
- never scenario/Event/report/agent bundle/URL/query/fragment/browser history/log/error;
- rotate every backend epoch;
- clean shutdown deletes/overwrites runtime file where practical;
- stale nonce is invalid after backend epoch changes.

## 5. Browser bootstrap and mandatory anti-framing

The browser UI is served by the same backend origin as Control API.

Current nonce may be provisioned to same-origin JavaScript only through a non-URL mechanism such as an inline boot object protected by CSP or a protected same-origin bootstrap response.

Requirements:

- nonce never in URL/query/fragment;
- any response containing nonce uses `Cache-Control: no-store`;
- no required third-party script/resource in initial implementation;
- CSP **MUST** be same-origin/self-contained and include `frame-ancestors 'none'`;
- ordinary config cannot weaken/remove `frame-ancestors 'none'`;
- `X-Frame-Options: DENY` may be emitted as defense in depth;
- browser sends nonce only in required custom header and never to another origin.

Origin+nonce protect direct hostile requests; anti-framing protects the authenticated real UI from clickjacking.

## 6. CLI credential access

CLI reads current nonce from mode-0600 runtime metadata/control file or equivalent approved local IPC bootstrap.

Nonce must not be accepted as ordinary command-line argument. Environment transport is discouraged and not default.

## 7. Request authentication

Every `/v1/*` request, including reads, requires:

```text
X-Tibia-RE-Control-Nonce: <current nonce>
```

Missing/malformed/stale -> `401 CONTROL_AUTH_REQUIRED` without disclosing expected value.

Constant-time compare where practical.

Nonce proves only local API access, never Track A mutation authority.

## 8. Host and DNS-rebinding defense

Every request must carry exact allowed `Host`, including actual port, for the listener.

Examples:

```text
127.0.0.1:49152
localhost:49152     only if explicitly enabled
[::1]:49152         only if explicitly enabled
```

Unknown Host -> `421 CONTROL_HOST_REJECTED`.

Never trust arbitrary DNS name merely because it resolves to loopback. Never infer trust from source IP alone.

## 9. Origin/CORS policy

Browser requests are exact same-origin.

- no `Access-Control-Allow-Origin: *`;
- no reflected arbitrary origin;
- present `Origin` must exactly equal allowed `scheme://host:port`;
- mismatched/null/untrusted browser Origin -> `403 CONTROL_ORIGIN_REJECTED`;
- reject preflight from untrusted origin;
- CLI/non-browser may omit Origin but still needs exact Host+nonce;
- no cookie ambient authentication.

## 10. HTTP method policy

Only declared methods/routes exist.

Unknown route -> `404 CONTROL_ROUTE_NOT_FOUND`.

Unsupported method on known route -> `405 CONTROL_METHOD_NOT_ALLOWED`.

No generic RPC, eval, shell, raw-adapter, raw-input or debug mutation endpoint.

## 11. API routes

Minimum:

```text
GET  /v1/status
GET  /v1/capabilities
GET  /v1/scenarios
GET  /v1/runs
GET  /v1/runs/<run_id>
GET  /v1/actions/<action_id>
GET  /v1/events

POST /v1/runs
POST /v1/runs/<run_id>/pause
POST /v1/runs/<run_id>/resume
POST /v1/runs/<run_id>/abort
POST /v1/experiments/one-step
POST /v1/stop-all
POST /v1/reset-stop
```

Additive bounded read-only routes are allowed in major v1. New mutation-capable operation requires explicit domain semantics/idempotency and cannot bypass Scenario Engine/MutationCoordinator.

## 12. Request IDs and request hash

Every POST requires caller-provided non-secret:

```text
X-Tibia-RE-Request-Id: <request_id>
```

`request_id` is distinct from semantic `action_id`.

Request hash:

```text
request_hash = lowercase_hex(SHA-256(UTF8(JCS({
  api_major: 1,
  method,
  canonical_path,
  normalized_body
}))))
```

Nonce/request-id/timestamp/transport headers are excluded from hash.

All bodies are parsed into typed bounded domain structs before hashing; duplicate JSON keys, unsafe/unknown required fields, polymorphic arbitrary objects, non-finite/out-of-domain values and secrets are rejected.

One-step/scenario bodies additionally satisfy Scenario v1.

## 13. Global RequestLedger and ResourceIdentityLedger

Artifact v1 global safety state is authoritative.

`RequestLedgerRecord` fixes:

```text
request_id
request_hash
operation
resource_id or transition_id
status
```

Resource-creating operations additionally use Artifact-v1 `ResourceIdentityRecord` to fix stable logical IDs before scheduling.

Duplicate rules:

- same request ID/hash -> return/recover same resource/transition/result; never allocate replacement;
- same request ID/different hash/operation -> `409 CONTROL_IDEMPOTENCY_CONFLICT`;
- repeated `POST /v1/runs` -> same `run_id`;
- repeated one-step POST -> same `experiment_id`, `run_id`, initial `action_ids`;
- duplicate STOP/reset -> same logical transition ID;
- duplicate transport delivery never creates extra semantic effect by itself.

## 14. Crash-safe resource-creating POST protocol

For `POST /v1/runs` and `POST /v1/experiments/one-step`:

```text
parse + normalize + validate
-> compute request_hash
-> serialize on request_id in local safety store
-> check existing request_id/hash
-> allocate stable run/experiment/action identities in memory
-> atomically durably write:
     RequestLedger(status=INTENT_DURABLE, resource_id=<stable resource>)
   + ResourceIdentityRecord(state=CREATED_NOT_SCHEDULED, all stable child IDs)
-> durability barrier succeeds
-> only now mark resource SCHEDULED and schedule domain work
-> persist ACCEPTED/COMPLETED/FAILED request transition
-> return response
```

For `/v1/runs`:

```text
resource_kind = RUN
resource_id = run_id
```

For one-step:

```text
resource_kind = ONE_STEP_EXPERIMENT
resource_id = experiment_id
ResourceIdentityRecord fixes experiment_id + run_id + initial action_ids
```

Failure semantics:

- before durable pair -> protected resource was not scheduled; later same request may allocate once;
- after durable pair but before scheduling -> same request recovers same IDs; no replacement and no mutation auto-resume;
- uncertain/corrupt pair -> `RECOVERY_REQUIRED`, fail closed, no replacement/re-execution.

## 15. Crash-safe run-control POST protocol

Pause/resume/abort do not allocate a new run. They use stable `transition_id` in RequestLedger before applying the idempotent run-state transition.

A duplicate request resolves the same transition. If recovery cannot prove whether a transition completed, domain recovery must use the existing run state and fail closed rather than create a new run/action.

Pause/resume never cache or manufacture external authority; later mutation final commit is freshly checked.

## 16. STOP/reset request recovery

STOP/reset use RequestLedger `transition_id` plus Execution/Artifact `ControlStateRecord.last_transition_id`.

Ordering:

```text
RequestLedger INTENT_DURABLE(request_id, request_hash, transition_id)
-> Execution-v1 STOP_TRANSITION or RESET_TRANSITION under dispatch_gate
-> persist request terminal status
```

Recovery:

- uncommitted/uncertain STOP intent may complete the **same** STOP transition ID because this strengthens fail-closed state;
- uncommitted/uncertain reset intent must **not** auto-apply reset; remain latched and return `RECOVERY_REQUIRED` until a new explicit reset is validly admitted;
- committed transition is recognized by matching durable ControlState transition ID and replay returns that logical result.

## 17. Retention

RequestLedger/ResourceIdentity records required to prevent duplicate resources/effects remain at least as long as corresponding run/action/control recovery state.

Eviction cannot turn missing history into permission to allocate/retry.

## 18. Default bounds

Initial defaults, configurable only downward without security review:

```yaml
max_request_body_bytes: 262144
max_header_bytes: 32768
max_page_size: 1000
default_page_size: 100
max_event_batch: 1000
max_active_event_subscribers: 32
max_queued_events_per_subscriber: 2048
max_open_runs_returned_per_page: 1000
```

Tighter route/domain limits still apply. Increasing limits requires amplification review.

## 19. Event delivery/backpressure

Initial implementation may use bounded polling or same-origin SSE. WebSocket not required.

Each subscriber has bounded queue.

Slow consumer:

- never blocks Recorder/Scenario Engine indefinitely;
- disconnect/drop with stable `CONTROL_EVENT_BACKPRESSURE` or require cursor resync;
- never drop execution-safety state to preserve UI stream;
- persisted run/event state is source for later retrieval.

Event cursors are non-authoritative observation positions.

## 20. Error envelope

```yaml
ControlApiError:
  code: string
  safe_message: string
  request_id: string | null
  resource_id: string | null
  retryable: bool
```

No raw exception, stack trace, environment value, nonce, adapter stderr or arbitrary repr/debug text is returned by default.

## 21. Browser reload and multiple tabs

Backend owns run/action lifecycle. Browser is view/controller only.

On reload/new tab:

- discover active runs via GET;
- reuse durable request/run/action identities for same logical retry;
- missing JavaScript state never implies new action/resource;
- concurrent tabs are serialized/deduplicated by safety store/coordinator.

## 22. Shutdown

Graceful shutdown:

1. stop accepting new scheduling/mutation-capable POSTs;
2. expose `SHUTTING_DOWN`;
3. latch cancellation/STOP semantics according to Execution v1;
4. flush RequestLedger, ResourceIdentityLedger, ControlState, Action/Budget journal and required evidence;
5. boundedly stop harness-owned subscribers/captures/resources;
6. mark unresolved runs/actions truthfully incomplete/ambiguous;
7. invalidate/delete current nonce;
8. exit.

Crash shutdown recovers through durable safety state and never implies successful cleanup/PASS.

## 23. No remote/LAN mode in v1

V1 defines no remote auth/TLS/user identity/RBAC/proxy trust/network rate limiting/multi-user tenancy. Non-loopback exposure is unsupported and must fail closed.

## 24. Browser/CLI parity

Both surfaces call the same backend/domain operations.

CLI cannot import/call concrete adapters to bypass HTTP/domain safety.

A future in-process CLI transport must invoke the exact same domain service with identical request/idempotency/authority semantics and no adapter escape hatch.

## 25. Mandatory Package B security/replay tests

At minimum:

1. default bind only `127.0.0.1`;
2. wildcard/non-loopback rejected;
3. missing nonce rejected;
4. stale nonce after restart rejected;
5. nonce absent URLs/loggable errors;
6. unrecognized Host rejected even from loopback;
7. hostile cross-origin request rejected;
8. permissive/reflected CORS absent;
9. UI cannot be framed because CSP includes `frame-ancestors 'none'`;
10. CLI without Origin requires valid Host+nonce;
11. oversized body/header rejected before expensive parsing;
12. duplicate JSON keys rejected;
13. same request ID/body -> same run/resource;
14. same request ID/different body -> idempotency conflict;
15. `POST /runs` durable Request+Resource pair fixes run ID before scheduling;
16. one-step durable pair fixes experiment/run/action IDs before scheduling;
17. crash after durable pair before scheduling -> same IDs, no auto-resume;
18. corrupt/uncertain pair -> recovery required, no replacement;
19. repeated request after restart resolves existing durable resource;
20. STOP replay resolves same transition ID;
21. uncertain reset replay remains latched/RECOVERY_REQUIRED;
22. slow subscriber cannot block execution;
23. page/event bounds enforced;
24. unknown raw/debug/action endpoint absent;
25. browser reload/new tab cannot duplicate active resource/action;
26. graceful shutdown flushes required ledgers/control state and invalidates nonce;
27. crash recovery never auto-resumes mutation.

## 26. Compatibility

Control API major version 1 is local-only and additive-only.

Changing nonce authentication, Host/origin/anti-framing trust, request/resource durability/idempotency, remote exposure policy or domain bypass guarantees requires a new major contract or explicitly reviewed security profile.