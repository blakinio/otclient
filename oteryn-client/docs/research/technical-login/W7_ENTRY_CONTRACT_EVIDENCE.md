# W7 Entry Contract Evidence

Status: implementation and exact-head validation in progress  
Wave: `OTERYN-W7-TECHNICAL-LOGIN`  
Lane: `W7-ENTRY-CONTRACT`  
Contract role: sole producer

## Scope

This lane produces the shared deterministic account/session/directory/game-entry contract used by W7 Identity, Canary admission and application composition. It contains no OAuth/HTTP DTO, browser launch, socket, transport trait, Canary packet/opcode, native UI, async runtime, global singleton or production compatibility claim.

Implemented packages:

- `oteryn-account-session`;
- `oteryn-world-directory`;
- `oteryn-game-session`.

All packages use the pinned workspace toolchain and existing standard-library/foundation contracts. No new third-party dependency or `deny.toml` exception is introduced.

## Public contract and invariants

### Account session

`AccountSessionId` is a non-zero client-local generation/correlation identity. It is not an Oteryn account ID, bearer value or persisted credential.

### Directory

- `CharacterId` and `WorldId` preserve positive signed 64-bit Gateway protocol-v1 identifiers.
- `GameplayChannelId` is a reserved positive opaque identifier. Gateway protocol v1 does not populate or serialize it in W7.
- `DirectoryRevision` is a non-zero client-local validated-response generation because Gateway protocol v1 exposes no server revision.
- `WorldRoute` accepts bounded ASCII host text and a non-zero TCP port.
- directory strings and collection counts are bounded before ownership;
- worlds, characters and channels are sorted by typed identifier;
- duplicate identifiers and unknown world references fail closed;
- selection proves that character and optional channel belong to the selected world and remain available/compatible in the exact snapshot;
- display names are never routing keys.

Closed directory control enums are `Availability` and `Compatibility`; arbitrary producer text never controls selection.

### Entry transaction

- `GameEntryAttemptId` is a non-zero client-local attempt generation.
- `GameEntryRequest` binds one attempt to one validated `SelectedEntry`, exact `EntryProfile` and deterministic `Moment`.
- `GameEntryCredential` owns non-empty bounded opaque bytes and a monotonic `Deadline`.
- credential and admission types are non-`Clone`, have no serialization surface and redact `Debug`/`Display`.
- secret storage is overwritten with zero bytes on terminal drop as a best-effort safe-Rust cleanup barrier; this is not a claim that compiler/runtime memory copies cannot ever exist.
- `AdmissionCredential` is created only by the lifecycle's one successful move into admission.
- no automatic replay or reconnect surface exists.

### Entry lifecycle

Public phases are:

`LoggedOut -> Authenticating -> AccountReady -> DirectoryReady -> EntryRequested -> CredentialReady -> Connecting -> SessionEntered`.

Typed terminal/control phases are `Failed` and `Closing`.

Rejected transitions do not replace lifecycle state. Stale attempts, duplicate callbacks, account mismatch, stale directory revisions, invalid selection, expired credentials and second credential handoff return typed failures.

Required failure categories and application actions are closed `EntryFailureKind` and `RecoveryAction` enums. No raw HTTP, server, parser, transport-backend or OS text is retained.

`SessionEntered` contains only non-secret typed evidence: attempt, account session, directory revision, character, world, optional channel, profile and monotonic entry moment.

## Consumer API: W7-IDENTITY

The first expected calls are:

1. `EntryLifecycle::begin_authentication(attempt_id)`;
2. after validated OAuth completion, `EntryLifecycle::account_ready(attempt_id, account_session_id)`;
3. validate strict Gateway DTOs, then construct `WorldRoute`, `WorldSummary`, `CharacterSummary` and optionally `GameplayChannelSummary`;
4. construct `AccountDirectorySnapshot::new(...)`;
5. install it with `EntryLifecycle::directory_ready(attempt_id, snapshot)`;
6. call `AccountDirectorySnapshot::select(revision, character_id, world_id, channel_id)` for explicit user/config selection;
7. construct `GameEntryRequest::new(...)` and call `EntryLifecycle::request_entry(request)`;
8. construct `GameEntryCredential::new(secret_bytes, deadline)` and move it through `EntryLifecycle::credential_ready(attempt_id, credential, clock)`.

Identity must not expose raw Gateway DTOs or add adapter-specific fields to these contracts. A fresh Gateway credential is required after expiry, rejection, uncertain handoff or consumption.

## Consumer API: W7-CANARY-ENTRY

The first expected calls are:

1. inspect the non-secret request via `EntryLifecycle::request()`;
2. call `EntryLifecycle::begin_connecting(attempt_id, clock)` immediately before admission handoff;
3. perform a final `AdmissionCredential::is_expired(clock)` check;
4. use `AdmissionCredential::expose_secret()` only while encoding the exact authenticated Current-profile login;
5. after ordered admission through the exact enter-world marker, call `EntryLifecycle::session_entered(attempt_id, entered_at)`;
6. map bounded adapter outcomes to `EntryFailure::for_kind(...)` and call `EntryLifecycle::record_failure(...)` when admission fails;
7. drop the moved admission credential and all protocol key material on every terminal path.

Canary admission must not clone, format, persist or replay the credential and must not define replacement request/result/failure types.

## Consumer API: W7-LOGIN-E2E

Application composition observes `EntryLifecycle::phase()` and emits progress corresponding to:

- `LoggedOut`;
- `Authenticating`;
- `AccountReady`;
- `DirectoryReady`;
- `EntryRequested`;
- `CredentialReady`;
- `Connecting`;
- `SessionEntered`;
- `Failed` with `EntryFailure` and its `RecoveryAction`;
- `Closing`.

The final success payload is `SessionEntered`. Application close calls `EntryLifecycle::close()`, joins/cancels owning workers in the application layer, then calls `finish_closing()` only after resources are released. The shared contract itself starts no worker or runtime.

## Migration and compatibility notes

- Legacy Lua tables, character lists and `GameSessionKey` state were not copied one-to-one.
- Gateway world/character names remain bounded presentation data, not identifiers.
- `DirectoryRevision` is explicitly local; consumers must not present it as a producer revision.
- `GameplayChannelId` remains absent for the one exact issuer milestone.
- The contract does not establish Platform, Gateway or Canary wire compatibility. Those claims require exact consumer evidence on the final producer merge.
- No temporary adapter-specific field, arbitrary error text, route override or speculative multi-world issuer API was added.

## Test coverage

Crate-local tests cover:

- zero/negative identifier rejection and signed-64 preservation;
- string and collection bounds;
- duplicate identifier and unknown relation rejection;
- deterministic ordering;
- stale directory revision and invalid world/character relationship handling;
- legal and illegal lifecycle transitions;
- stale and duplicate completion rejection;
- one-shot credential handoff and second-use rejection;
- expiry through `ManualClock`;
- cancellation and close ordering;
- no mutation after rejected transitions;
- compile-fail proof that `GameEntryCredential` is not cloneable;
- redacted credential/admission/lifecycle formatting;
- explicit secret-buffer overwrite behavior.

## Validation record

Local Cargo execution is unavailable in the current worker sandbox: DNS cannot resolve GitHub and no Rust toolchain is installed. Exact-head GitHub CI is therefore the authoritative execution environment.

Pending exact-head evidence:

- `cargo metadata --locked --format-version 1`;
- `cargo fmt --all --check`;
- `cargo clippy --workspace --all-targets --locked -- -D warnings`;
- `cargo test --workspace --all-targets --locked`;
- `cargo run --locked -p oteryn-architecture-check -- workspace .`;
- `cargo deny check`;
- repository required CI;
- complete changed-file/full-diff review and unresolved-thread check.

## Claims

- `PASS` may be recorded only after exact-head CI completes successfully.
- `OBSERVED`: source-level ownership, closed APIs, bounds and redaction surfaces described above.
- `BLOCKED`: real Platform/Gateway/Canary compatibility, deployed configuration, transport/admission behavior and production readiness are outside this producer lane.
