# TIBIA RE Control Center Control API Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-CONTROL-API-V1
version: 1.1
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: none
remote_exposure: forbidden_in_v1
```

## 1. Purpose

Define one bounded, local-only operator transport for the Control Center so browser and CLI invoke exactly the same domain operations without creating a second execution implementation.

This contract covers transport authentication, same-origin/Host policy, clickjacking resistance, request idempotency, replay behavior, bounds, event delivery and shutdown. It does not grant Track A authority and does not authorize remote/LAN control.

Normative execution semantics remain in `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`. Durable global RequestLedger and control-state semantics are normative in `TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md`.

## 2. Threat model

Loopback binding reduces network exposure but is not sufficient by itself.

The local API must defend against at least:

- unrelated local web pages attempting cross-origin requests;
- DNS rebinding to a loopback-bound service;
- hostile framing/clickjacking of the real same-origin operator UI;
- browser retries/reloads;
- CLI retries;
- connection loss after the backend accepted a request;
- crash after request acceptance but before response/resource scheduling;
- duplicate tabs/operators;
- oversized/malformed requests;
- slow event consumers;
- backend restart;
- accidental wildcard/non-loopback bind.

This contract is not a hostile-local-user privilege boundary. Another process running as the same trusted OS user may be able to read the local control credential or access the same files. Hardening against a malicious same-user process requires a separate OS security design.

## 3. Bind policy

Control API v1 binds exactly to IPv4 loopback by default:

```text
127.0.0.1:<ephemeral-or-configured-port>
```

Rules:

- wildcard addresses (`0.0.0.0`, `::`) are forbidden;
- non-loopback addresses are forbidden;
- IPv6 `::1` may be enabled only explicitly and must preserve all v1 Host/origin/token rules;
- bind failure is terminal for the API listener; do not silently fall back to another interface;
- the chosen authority (`host:port`) is recorded as non-secret runtime status, not as mutation authority.

Remote/LAN exposure requires a new separately reviewed security profile/major contract. There is no v1 convenience flag that weakens this rule.

## 4. Backend control credential

Each backend process creates a fresh random `control_nonce` bound to its `backend_epoch`.

Requirements:

```yaml
entropy_bits_minimum: 256
reuse_across_restart: false
persist_to_run_artifacts: false
loggable: false
```

The nonce is Control Center local-control secret material, not Tibia account/auth material.

Storage/handling:

- store only in memory and/or a mode-0600 backend runtime file owned by the current OS user;
- never place it in scenario files, Event payloads, reports, agent bundles, URLs, query strings, fragments or browser history;
- never print it in logs/errors;
- rotate on every backend epoch;
- delete/overwrite the runtime file on clean shutdown where practical; stale nonce is invalid because backend epoch changes.

## 5. Browser bootstrap and mandatory anti-framing

The browser UI is served by the same backend origin as the Control API.

The initial HTML/bootstrap response may provision the current nonce to same-origin JavaScript through a non-URL mechanism such as an inline boot object or a same-origin protected bootstrap response.

Requirements:

- nonce must never appear in a URL/query/fragment;
- every HTML/bootstrap response containing the nonce uses `Cache-Control: no-store`;
- no third-party scripts/resources are required for the initial implementation;
- the initial implementation **MUST** emit a Content Security Policy that is self-contained/same-origin and includes `frame-ancestors 'none'`;
- the UI **MUST NOT** be frameable by another origin or by arbitrary same-site pages; an implementation may also emit `X-Frame-Options: DENY` as defense in depth;
- weakening/removing `frame-ancestors 'none'` requires a separately reviewed integration/security profile; it is not a v1 runtime flag;
- browser code sends the control nonce only in the required custom request header;
- no script loaded by the UI may send the nonce to another origin.

Origin+nonce protect direct hostile requests; mandatory anti-framing protects the real authenticated same-origin UI from being driven through clickjacking.

## 6. CLI credential access

CLI obtains the current nonce from the backend's mode-0600 runtime metadata/control file or an equivalent local IPC bootstrap approved by the implementation.

CLI must not accept the control nonce via ordinary command-line argument because process argument listings can expose it.

Environment-variable transport is discouraged and must not be the default because environment dumps/debugging can leak it.

## 7. Required request authentication

Every `/v1/*` request, including reads, requires:

```text
X-Tibia-RE-Control-Nonce: <current nonce>
```

Missing, malformed or stale nonce -> `401 CONTROL_AUTH_REQUIRED` without revealing expected values.

The backend compares nonce values using a constant-time comparison where practical.

A successful local control nonce proves only access to the Control API. It grants no Track A mutation authority.

## 8. Host and DNS-rebinding defense

The backend records its configured/actual loopback authorities at listener creation.

Every HTTP request must have a `Host` header matching exactly one allowed authority for that listener, including the actual port.

Examples:

```text
127.0.0.1:49152
localhost:49152      only if explicitly enabled and resolved/served intentionally
[::1]:49152          only if IPv6 loopback was explicitly enabled
```

Unknown Host -> `421 CONTROL_HOST_REJECTED`.

Do not accept arbitrary DNS names merely because they resolve to `127.0.0.1`.

Do not infer trust from client source IP alone.

## 9. Origin/CORS policy

Browser requests must be same-origin.

Rules:

- do not emit permissive CORS (`*` or reflected arbitrary origins);
- requests with an `Origin` header must match the backend's exact allowed origin (`scheme://host:port`);
- mismatched/null/untrusted browser Origin -> `403 CONTROL_ORIGIN_REJECTED`;
- preflight requests from untrusted origins are rejected;
- same-origin UI uses the custom nonce header;
- CLI/non-browser clients may omit `Origin` but still require valid Host and nonce;
- do not enable cookie-based ambient authentication for v1.

This prevents an unrelated website from turning the user's browser into an authenticated Control Center operator through a direct request.

## 10. HTTP method policy

Only explicitly declared methods/routes exist.

Unknown route -> `404 CONTROL_ROUTE_NOT_FOUND`.

Unsupported method on a known route -> `405 CONTROL_METHOD_NOT_ALLOWED`.

No generic RPC, eval, shell, raw-adapter, raw-input or debug mutation endpoint is permitted.

## 11. API routes

Minimum v1 routes:

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

Implementations may add additive bounded read-only routes inside major version 1. New mutation-capable operations require explicit domain semantics and idempotency and must not bypass Scenario Engine/MutationCoordinator.

## 12. Request IDs and POST idempotency

Every POST requires a caller-provided:

```text
X-Tibia-RE-Request-Id: <opaque non-secret ID>
```

`request_id` is distinct from `action_id`.

- `request_id` deduplicates transport/domain requests such as creating a run or issuing STOP;
- `action_id` deduplicates logical semantic action attempts inside runs.

The authoritative RequestLedger is global and uses Artifact v1 `RequestLedgerRecord`:

```yaml
request_id:
request_hash:
operation:
resource_id:
transition_id:
backend_epoch_created:
status: INTENT_DURABLE | ACCEPTED | COMPLETED | FAILED | RECOVERY_REQUIRED
response_code:
response_body_hash:
```

The request hash is:

```text
request_hash = lowercase_hex(SHA-256(UTF8(JCS({
  api_major: 1,
  method,
  canonical_path,
  normalized_body
}))))
```

Headers carrying nonce, request ID, timestamps or transport metadata do not participate in the request hash.

Duplicate rules:

- same `request_id` + same request hash -> return/recover the existing logical response/resource/transition; do not allocate a second identity or re-execute a completed domain side effect;
- same `request_id` + different request hash -> `409 CONTROL_IDEMPOTENCY_CONFLICT`;
- repeated `POST /v1/runs` with the same request ID returns the same `run_id`, never creates a second run;
- repeated one-step experiment request resolves to the same experiment/run/action identities;
- duplicate STOP request resolves the same logical `transition_id`; it must not create accidental additional semantic effects merely due to transport retry;
- duplicate reset request resolves the same logical `transition_id`; uncertain reset recovery never silently clears STOP.

## 13. Crash-safe request admission protocol

For every POST capable of creating durable identity, scheduling work or changing durable control state, use the following ordering:

```text
parse + normalize + validate
-> compute request_hash
-> serialize on request_id in local safety store
-> check existing request_id/hash
-> allocate stable logical resource_id/transition_id in memory
-> atomically durably write RequestLedger INTENT_DURABLE
   + minimum corresponding domain/control record
-> durability barrier succeeds
-> only then schedule/execute the domain operation
-> persist ACCEPTED/COMPLETED/FAILED transition
-> return response
```

The `INTENT_DURABLE + minimum corresponding record` atomicity is normative in Artifact v1.

Examples:

- `POST /v1/runs`: durable mapping plus `RunRecord(CREATED/NOT_SCHEDULED)` precedes scheduling;
- one-step experiment: durable experiment/run/action identities with action `NOT_DISPATCHED` precede scheduling;
- pause/resume/abort: durable request/transition identity precedes the idempotent run-state transition;
- STOP/reset: durable request/transition identity precedes the Execution-v1 control transition; `ControlStateRecord.last_transition_id` proves whether that transition committed.

Failure before the durable intent means the conforming backend was forbidden to create/schedule the protected resource, so a later same request may safely allocate it once.

Failure after durable intent means the identity already exists. Recovery must never allocate a replacement.

Mutation-capable work is never automatically resumed solely because an intent/resource survived restart.

### 13.1 STOP/reset recovery

For a STOP intent whose transition is not yet proven committed, recovery may complete the **same** STOP transition ID because doing so only strengthens the fail-closed state.

For a reset intent whose transition is not proven committed, recovery must leave STOP latched and return `RECOVERY_REQUIRED`; it must not auto-apply reset. A new explicit reset may be issued only after the recovered state is validated under Execution v1.

## 14. Request-ledger durability and retention

Package B persists the global RequestLedger in the selected Control Center safety store.

After backend restart:

- valid same request ID/hash retrieves the existing durable resource/result;
- an `INTENT_DURABLE` resource remains the same identity even when scheduling never started;
- missing/corrupt contradictory state after a protected intent may have existed fails closed and must not silently recreate mutation-capable work;
- request IDs are never reused for a different operation/body.

The ledger may retain completed non-mutating requests for a bounded retention window, but any entry needed to prevent duplicate side effects/resources must remain at least as long as the corresponding run/action/control recovery state.

## 15. Normalized request bodies

All JSON request bodies are validated into typed domain request structs before hashing or execution.

Rules:

- duplicate JSON keys are rejected by the parser/decoder path selected by the implementation;
- unknown required/unsafe fields are rejected;
- no polymorphic arbitrary object deserialization;
- strings/collections/numbers obey finite route-specific bounds;
- no secret values belong in ordinary API request types.

One-step experiment/scenario bodies must satisfy `TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md`.

## 16. Default bounds

Initial defaults, configurable only downward without a security review:

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

Tighter route/domain limits still apply.

A future need to increase these limits requires review for memory/CPU/artifact amplification.

## 17. Event delivery and backpressure

Initial implementation may use bounded polling or same-origin SSE. WebSocket is not required.

Every subscriber has a bounded queue.

If a subscriber cannot keep up:

- do not block Recorder/Scenario Engine indefinitely;
- close/drop the subscriber with a stable `CONTROL_EVENT_BACKPRESSURE` indication or require explicit cursor resynchronization;
- never drop execution-safety state solely to preserve a slow UI stream;
- canonical persisted event/run state remains the source for later retrieval.

Event cursors are non-authoritative observation positions only.

## 18. Error envelope

Errors use stable non-secret structure:

```yaml
ControlApiError:
  code: string
  safe_message: string
  request_id: string | null
  resource_id: string | null
  retryable: bool
```

No raw exception, stack trace, environment value, secret nonce, adapter stderr or arbitrary repr/debug text is returned to clients by default.

HTTP status alone is not the semantic error contract; `code` is stable within major version 1.

## 19. Browser reload and multiple tabs

The backend owns run/action lifecycle.

Browser state is only a view/controller.

On reload/new tab:

- discover active runs via GET;
- reuse known durable request/run/action IDs when retrying the same logical request;
- never infer that missing local JavaScript state means a new action should be created;
- concurrent tabs are serialized/deduplicated by the backend ledgers/coordinator.

## 20. Shutdown

Graceful backend shutdown:

1. stop accepting new scheduling/mutation-capable POSTs;
2. expose `SHUTTING_DOWN` status;
3. latch cancellation/STOP semantics for harness work according to the execution contract;
4. flush required RequestLedger, ControlState, action dispatch journal, budget ledger and event/artifact state;
5. boundedly stop harness-owned subscribers/captures/resources;
6. mark unresolved runs/actions truthfully incomplete/ambiguous as required;
7. invalidate/delete current control nonce;
8. exit.

Forced/crash shutdown is recovered according to Execution v1 and persistent ledgers. It never implies successful cleanup or PASS.

## 21. No remote/LAN mode in v1

Control API v1 does not define remote authentication, TLS termination, user identity, role-based authorization, proxy trust, CSRF across origins, network rate limiting or multi-user tenancy.

Therefore non-loopback exposure is unsupported and must fail closed.

A later remote-control feature requires a separate security-sensitive task and new accepted contract/profile before deployment.

## 22. Browser/CLI parity acceptance

For every domain operation exposed to both surfaces, tests must prove the same backend command path and result semantics.

The CLI is not permitted to import/call concrete adapters to bypass HTTP/domain safety merely because it runs locally.

If an in-process CLI transport is introduced later for performance, it must call the exact same domain service with the same request/idempotency/authority semantics and have no adapter escape hatch.

## 23. Package B mandatory security/replay tests

At minimum:

1. binds only `127.0.0.1` by default;
2. wildcard/non-loopback bind rejected;
3. missing nonce rejected;
4. stale nonce after backend restart rejected;
5. nonce absent from URLs/loggable error objects;
6. unrecognized Host rejected even from loopback client;
7. cross-origin browser request rejected;
8. permissive CORS absent;
9. browser UI cannot be framed because CSP contains `frame-ancestors 'none'`;
10. CLI without Origin works only with valid Host + nonce;
11. oversized body/header rejected before expensive parsing;
12. duplicate JSON keys rejected;
13. same request ID/body returns same run/resource;
14. same request ID/different body returns idempotency conflict;
15. repeated `POST /runs` across transport retry creates one run;
16. crash after durable run intent but before scheduling preserves the same run ID;
17. repeated request after backend restart resolves existing durable resource when ledger is valid;
18. corrupt/missing safety-critical RequestLedger does not silently re-execute mutation-capable work;
19. one-step intent persists stable experiment/run/action IDs before scheduling;
20. STOP replay resolves one logical transition ID;
21. uncertain reset replay remains latched/RECOVERY_REQUIRED rather than silently resetting;
22. slow event subscriber cannot block execution and receives deterministic backpressure behavior;
23. page/event bounds enforced;
24. unknown raw/debug/action endpoint absent;
25. browser reload/new tab cannot duplicate an active run/action solely due to lost client state;
26. graceful shutdown flushes required ledgers/control state and invalidates nonce;
27. crash recovery follows Execution v1 rather than auto-resuming mutation.

## 24. Compatibility

Control API major version 1 is local-only and additive-only.

Changing nonce authentication, Host/origin/anti-framing trust, request-intent durability/idempotency semantics, remote exposure policy or domain bypass guarantees requires a new major contract or an explicitly reviewed security profile.