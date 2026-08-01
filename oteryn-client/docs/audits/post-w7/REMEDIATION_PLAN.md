# Post-W7 Rust Client Remediation Plan

Status: accepted execution plan; no remediation implementation is authorized by this document alone  
Source audit: `OTC2-20260731-rust-client-post-w7-audit`  
Authoritative audit result: `VALIDATED_WITH_CORRECTIONS`  
Evidence cut: `main` `d23edd0a8395deb586e2b93dd1954bb175243dc4`

## 1. Live-state preflight

The planning preflight established:

- audit PR #120 merged as `97c4f7a1ec581072940ae87697b80a4ec9c53921`;
- audit lifecycle archive PR #121 merged as current `main` `d23edd0a8395deb586e2b93dd1954bb175243dc4`;
- the audit task is archived at `docs/agents/tasks/archive/OTC2-20260731-rust-client-post-w7-audit.md`;
- the canonical evidence is `main-audit-report.md` plus `VALIDATOR_PACKET.md` in this directory;
- the workspace has 19 members and the current required Rust gates are `Rust Client / Windows` and `Rust Client / Supply Chain`;
- every PR must also pass repository `CI / Required`;
- open PR #23 owns legacy login-shell files plus shared `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md`;
- open PRs #48 and #97 own isolated legacy/infrastructure workflow and task paths only;
- no active task or open PR owns the affected Rust production paths, architecture-check source, asset-compiler source or their public Rust contracts.

Open PR #23 does not block isolated Rust source work. It does block any concurrent edit to its declared shared documentation paths. A remediation worker must leave those paths untouched until the lease is released or explicitly transferred.

## 2. Accepted decomposition

The four findings map to four packages:

| Package | Finding | Task shape | Execution mode | Discovery before code | Contract role |
|---|---|---|---|---|---|
| `R1-SECRET` | `OTC2-AUD-001` | phased implementation | Codex | bounded allocation/API inventory first | producer amendment for secret-bearing Platform/Identity surfaces |
| `R2-SHUTDOWN` | `OTC2-AUD-002` | phased implementation | Codex | bounded lifecycle/API design first | producer amendment for app-runtime shutdown lifecycle |
| `R3-ASSET-OPEN` | `OTC2-AUD-003` | phased, discovery-first implementation | Codex | mandatory platform primitive proof | asset-compiler trust-boundary owner |
| `R4-ARCH-POLICY` | `OTC2-AUD-004` | single bounded implementation after policy checkpoint | Codex | policy-table checkpoint only | architecture-policy producer |

This is the smallest safe task count.

`R1-SECRET` and `R2-SHUTDOWN` must not be combined. They share Identity, Platform, technical-login evidence and integration tests, but they have different security invariants, public API decisions, acceptance tests and rollback boundaries. Combining them would make a secret-lifetime rollback depend on an event-loop lifecycle rollback.

`R1-SECRET` must merge before `R2-SHUTDOWN`. The shutdown package may need to amend cancellation-aware Platform/Identity boundaries and must consume the final secret-wrapper/request ownership surface rather than editing the same API concurrently.

`R3-ASSET-OPEN` and `R4-ARCH-POLICY` have independent production paths and public contracts. They may perform isolated discovery/source work in parallel only after a fresh coordinator preflight proves:

1. neither worker edits `oteryn-client/Cargo.toml`, `Cargo.lock`, `deny.toml`, architecture-check paths or shared agent documents concurrently;
2. `R4-ARCH-POLICY` remains dependency-free and does not require Cargo/lockfile integration;
3. the open PR #23 shared-document lease has been released or neither worker edits those paths;
4. exact-head heavy CI runs can be serialized.

Those conditions are not all proven now because `R3-ASSET-OPEN` has an unresolved dependency/platform-primitive decision and PR #23 still owns shared documentation. Concurrent final integration is therefore not authorized by this plan.

## 3. Dependency and merge graph

```text
planning PR
  -> planning archive PR
      -> R1-SECRET
          -> R2-SHUTDOWN
      -> R4-ARCH-POLICY
      -> R3-ASSET-OPEN discovery checkpoint
          -> R3-ASSET-OPEN implementation

shared integration lease:
  PR #23 release
      -> any remediation edit to MODULE_CATALOG / CHANGELOG

merge train:
  1. R1-SECRET
  2. R2-SHUTDOWN
  3. R4-ARCH-POLICY
  4. R3-ASSET-OPEN
```

`R4-ARCH-POLICY` may merge before `R2-SHUTDOWN` only if `R2-SHUTDOWN` is blocked, all shared leases are clear, and `R2-SHUTDOWN` rebases and reruns the complete workspace gate afterward. `R3-ASSET-OPEN` remains last because its implementation approach is not yet proven and may add a reviewed dependency.

## 4. Package R1-SECRET — secret lifecycle and claim correction

Proposed task: `OTC2-20260801-secret-lifecycle-remediation`.

### Required invariant

Every secret-bearing allocation controlled by project code has an explicit owner, a bounded lifetime, redacted formatting and deterministic best-effort overwrite on terminal drop. Documentation states only that project-owned buffers are overwritten; it does not claim erasure of allocator remnants, operating-system process arguments, browser state, TLS/library buffers or copies made inside `url`, `ureq`, native TLS or the operating system.

A documentation-only narrowing is necessary but is not sufficient security remediation.

### Required disposition

Use a combination:

1. narrow overbroad claims in architecture/evidence/catalogue text;
2. extend non-cloneable zeroing wrappers to every project-owned secret intermediate;
3. eliminate ordinary formatted bearer `String` ownership;
4. avoid parsing callback code/state through ordinary owned `String`/sensitive `Url` values where a bounded byte parser or secret wrapper can retain ownership;
5. move serde-produced secret fields immediately into zeroing ownership without additional project-owned copies;
6. keep errors closed and non-secret;
7. document unavoidable external/library copies as explicit residual boundaries.

The package must not claim complete process-memory erasure.

### Production paths owned

- `oteryn-client/crates/identity/src/lib.rs`
- `oteryn-client/crates/platform/src/lib.rs`
- `oteryn-client/crates/game-session/src/lib.rs` only when the common secret ownership contract must be aligned

### Test and evidence paths owned

- tests embedded in the three crates above
- `oteryn-client/tests/security/auth/**`
- `oteryn-client/tests/integration/technical-login/**` only for secret-boundary regression coverage
- `oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md`
- `oteryn-client/docs/architecture/TECHNICAL_LOGIN.md`
- its own active task record

### Shared-path lease, conditional paths

- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/CHANGELOG.md`
- `docs/agents/BUILD_TEST_MATRIX.md` only if the test surface changes materially
- `oteryn-client/Cargo.toml`, affected crate manifests, `Cargo.lock` and `deny.toml` only if the discovery checkpoint proves a new dependency is necessary

No shared path may be edited while PR #23 owns it. The default design is standard-library-first and should reuse or generalize the existing owned-byte wrappers. A new `zeroize`-class dependency is not pre-approved; it requires an exact API benefit, license/advisory review, unique Cargo/lockfile lease and generated lockfile.

### Public producers and consumers

- producer: `oteryn-platform::SecretString`, `HttpRequest`, `HttpTransport` request ownership;
- producer/consumer: `oteryn-identity` callback, PKCE and Platform composition;
- producer: `oteryn-game-session::GameEntryCredential` if alignment is required;
- consumers: `apps/client/src/technical_login.rs`, technical-login integration tests, auth security tests and synthetic transports.

### Cheapest reproducible tests

- compile/runtime tests proving secret wrappers have no revealing `Debug`, `Display`, `Clone` or serialization surface;
- deterministic drop probes around project-owned buffers using a test-only observing allocator/container seam where feasible without unsafe production code;
- callback tests proving code/state do not remain in ordinary project-owned target/query strings after parsing;
- a source-level regression test or lint fixture rejecting the ordinary `format!("Bearer {bearer}")` pattern;
- request/error tests proving synthetic marker secrets do not appear in formatted errors, diagnostics or debug output.

Tests may prove project-owned overwrite and API surface only. They may not claim inspection of library or operating-system memory.

### Component validation

```text
cargo test --locked -p oteryn-platform -p oteryn-identity -p oteryn-game-session
cargo test --locked --manifest-path tests/security/auth/Cargo.toml
cargo test --locked --manifest-path tests/integration/technical-login/Cargo.toml
```

### Heavy final gate

Run the complete current Rust workspace ladder on the final rebased head:

```text
cargo metadata --locked --format-version 1
cargo fmt --all --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --all-targets --locked
cargo run --locked -p oteryn-architecture-check -- workspace .
cargo deny check --all-features
```

Then require `Rust Client / Windows`, `Rust Client / Supply Chain`, repository `CI / Required`, complete changed-file/diff review and no unresolved review threads.

### Acceptance criteria

- no project-owned callback code, state, verifier, token, ticket, credential, sensitive request body or bearer header intermediate remains in an ordinary unzeroed owned string/vector after its last use;
- no ordinary formatted bearer string remains;
- authorization/browser and third-party library copy boundaries are named accurately;
- all secret-facing formatting and error tests remain fail closed;
- existing OAuth/Gateway wire behavior and one-shot semantics are unchanged;
- no password fallback, persistence, logging or diagnostics surface is added;
- documentation distinguishes best-effort project-owned overwrite from complete memory erasure.

### Rollback boundary

One revert restores only secret ownership/parsing/request handling and its truthful documentation. It must not include event-loop shutdown, timeout policy, architecture-edge or asset-open changes.

### Feasibility

Implementation is feasible from current evidence, but the worker must complete a bounded allocation/API inventory before choosing wrappers. A material new dependency or a required public transport signature change is a stop-and-checkpoint condition.

## 5. Package R2-SHUTDOWN — nonblocking cancellation and joined completion

Proposed task: `OTC2-20260801-nonblocking-shutdown-remediation`.

### Exact blocking path

The Windows event-loop close/destroy path calls `ShellApplication::request_exit`, which calls `TechnicalLoginController::shutdown`, which calls `TechnicalLoginRuntime::shutdown`, then `disconnect_to_logged_out`, then unconditional `join_and_recover_workers`. The same unconditional join is reachable from `cancel_active`, `disconnect_to_logged_out` and `Drop`.

The following synchronous operations do not observe cancellation while one operating-system/library call is in progress:

- `ureq` request send/receive inside `UreqTransport::post`;
- `TcpStream::connect_timeout`;
- each blocking `TcpStream::read` and `TcpStream::write` call.

The loopback listener itself checks cancellation every 10 ms while accepting and uses read slices of at most 250 ms.

### Required invariant

No method invoked on the Windows event-loop thread blocks waiting for an unfinished worker. Closing initiates cancellation, keeps the event loop alive, surfaces worker completion through the existing proxy/poll mechanism, joins only a finished worker, closes session state, releases renderer/window and exits in deterministic order. No worker is detached, forgotten, killed silently or allowed to own resources after process teardown.

### Required public contract amendment

`oteryn-app-runtime` must expose an explicit nonblocking shutdown lifecycle with initiation and polling/completion states. Existing blocking `cancel_active`, `disconnect_to_logged_out` and `shutdown` behavior must be replaced or narrowed so an event-loop caller cannot invoke an unconditional join. A stable public progress result must distinguish at least waiting from complete and preserve typed worker panic/failure reporting.

`TECHNICAL_LOGIN.md` and a new architecture decision under `oteryn-client/docs/architecture/decisions/` must define renderer/window release and event-loop exit only after joined completion.

### Required timeout bounds

- retain the existing Platform HTTP global maximum of 30 seconds;
- add a hard maximum of 30 seconds to each configured transport connect, read and write timeout;
- reject technical-login environment values above the owning component maximum before work starts;
- retain the callback user-wait maximum of 300 seconds because callback accept is nonblocking and cancellation-observable; retain the 250 ms maximum callback stream read slice;
- after cancellation, expose an application `ShutdownOverdue`/equivalent typed state once 31 seconds elapse, but continue polling and joining; the overdue state must not detach or abandon the worker.

The 31-second overdue threshold is one second above the largest permitted single blocking operation and is diagnostic/escalation state, not permission to exit with a live worker.

### Production paths owned

- `oteryn-client/crates/app-runtime/src/lib.rs`
- `oteryn-client/crates/app-runtime/src/runtime.rs`
- `oteryn-client/crates/app-runtime/src/worker.rs`
- `oteryn-client/apps/client/src/main.rs`
- `oteryn-client/apps/client/src/technical_login.rs`
- `oteryn-client/crates/transport/src/lib.rs`
- `oteryn-client/crates/platform/src/lib.rs` only for cancellation/bound documentation or API propagation
- `oteryn-client/crates/identity/src/lib.rs` only for cancellation/bound propagation

### Test and documentation paths owned

- tests embedded in the affected crates/app
- `oteryn-client/tests/integration/technical-login/**`
- `oteryn-client/tests/security/auth/**` only where cancellation behavior changes
- `oteryn-client/docs/architecture/TECHNICAL_LOGIN.md`
- one new shutdown lifecycle ADR under `oteryn-client/docs/architecture/decisions/`
- its own active task record

### Shared-path lease

- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/CHANGELOG.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- Cargo/lockfile paths only if an unexpected new dependency is proposed; no new dependency is expected or pre-approved.

### Cheapest reproducible tests

- a gate-controlled fake worker proving shutdown initiation returns while the worker is unfinished;
- a deterministic poll test proving no `join` occurs before `JoinHandle::is_finished`;
- a completion test proving the worker is joined exactly once and lifecycle state is cleared before final exit;
- a Windows shell state test proving renderer/window release and `event_loop.exit()` are deferred until shutdown completion;
- timeout constructor tests rejecting zero and values above 30 seconds;
- cancellation tests for callback, HTTP stage boundaries and TCP loops;
- a drop-path test proving the normal application path reaches drop with no live worker.

### Component validation

```text
cargo test --locked -p oteryn-app-runtime -p oteryn-transport -p oteryn-platform -p oteryn-identity -p oteryn-client
cargo test --locked --manifest-path tests/integration/technical-login/Cargo.toml
cargo test --locked --manifest-path tests/security/auth/Cargo.toml
```

### Heavy final gate

The complete Rust workspace ladder and all current required CI/review gates from `R1-SECRET` are mandatory on the final head.

### Acceptance criteria

- close/destroy/exiting callbacks do not wait on unfinished workers;
- every worker remains owned until joined exactly once;
- no detached worker or silent resource abandonment path is introduced;
- `cancel_active`, disconnect and shutdown public behavior is nonblocking for event-loop use;
- configured HTTP/TCP blocking calls have the exact caps above;
- overdue shutdown is visible and typed but does not weaken ownership;
- renderer/window/session teardown order is deterministic and documented;
- all existing success, cancellation, failure and redaction behavior remains covered.

### Rollback boundary

One revert restores only app-runtime worker lifecycle, shell close coordination, timeout caps and their architecture/tests. It must not revert secret-wrapper changes already merged from `R1-SECRET`.

### Feasibility

Implementation is feasible with current standard-library threads, `JoinHandle::is_finished`, existing event-loop proxy events and bounded polling. No worker-kill primitive or async runtime is required.

## 6. Package R3-ASSET-OPEN — opened-object integrity

Proposed task: `OTC2-20260801-asset-open-integrity-remediation`.

### Required invariant

The bytes read for each manifest source come from the exact regular file object accepted by containment and link/reparse policy. No attacker-controlled rename, symlink, mount or reparse substitution between validation and open may change the opened object. Another pre-open metadata check is not acceptance.

### Required platform decision

The task begins with a proof checkpoint comparing, on pinned Rust and the supported Windows target:

1. safe handle-relative open from a trusted directory handle;
2. no-follow/reparse-point protection for every traversed component and final object;
3. final opened-handle regular-file and stable identity verification;
4. a capability-safe dependency such as a reviewed directory-capability API;
5. only if none is implementable, an explicitly enforced trusted-exclusive-source contract whose precondition is represented by an unforgeable API/handle and tested, not a documentation assertion.

Direct unsafe Win32/FFI is prohibited by workspace policy. A dependency may be selected only after exact Windows behavior, license, advisories, source and feature graph are proven. If no safe-Rust primitive or enforceable trusted-source contract is demonstrated, implementation stops blocked; the existing audit finding must not be marked fixed.

### Production paths owned

- `oteryn-client/tools/asset-compiler/src/lib.rs`
- `oteryn-client/tools/asset-compiler/src/main.rs` only if the trusted-root/handle CLI contract changes
- `oteryn-client/tools/asset-compiler/Cargo.toml` only after the dependency checkpoint

### Test and documentation paths owned

- `oteryn-client/tools/asset-compiler/tests/compiler.rs`
- additional platform-specific tests under `oteryn-client/tools/asset-compiler/tests/**`
- relevant asset-input evidence/architecture document only when the selected trust contract changes
- one new asset-open ADR when the public trust boundary changes
- its own active task record

### Shared-path lease

Potentially required and therefore reserved only after the design checkpoint:

- `oteryn-client/Cargo.toml`
- `oteryn-client/Cargo.lock`
- `oteryn-client/deny.toml`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CHANGELOG.md`
- `oteryn-client/docs/operations/RUST_WORKSPACE.md`

### Public contract impact

An internal handle-relative implementation may preserve `compile_manifest(&Path, &Path)`. An enforced trusted-exclusive-source precondition changes the compiler/CLI public contract and requires an ADR, migration note and caller tests. The worker may not silently weaken the current arbitrary-root API into a documented assumption.

### Cheapest reproducible tests

- a deterministic test seam that substitutes a source after name validation but before final acquisition and proves the implementation rejects it or continues reading the already accepted handle;
- final-handle regular-file and size checks performed after open;
- Unix symlink/special-file replacement tests;
- Windows symbolic-link, junction/reparse and rename replacement tests when the hosted runner permits creation;
- a stable identity test comparing the validated object identity with the opened handle identity;
- existing path traversal, outside-root, oversize and deterministic output tests unchanged.

### Component validation

```text
cargo test --locked -p oteryn-asset-compiler --all-targets
cargo run --locked -p oteryn-asset-compiler -- --help
```

The exact selected primitive must also be exercised on `Rust Client / Windows`. Any Unix-specific claim requires named Unix execution evidence; Windows CI alone does not prove Unix behavior.

### Heavy final gate

Complete Rust workspace, architecture, supply-chain, repository required CI and full review gates. If a dependency is added, regenerate `Cargo.lock` with Cargo 1.94.0 and pass cargo-deny without policy weakening.

### Acceptance criteria

- validation and read operate on one accepted opened object or an equivalent proven capability;
- symlink/reparse/rename substitution cannot redirect the read outside the trusted root;
- final opened object is a regular file and size is checked from the opened handle;
- no claim relies only on another pathname metadata check;
- current deterministic output and hostile-input bounds remain intact;
- any trusted-source precondition is mechanically enforced and migration-documented.

### Rollback boundary

One revert restores only asset source acquisition, its dependency/manifest integration, tests and trust-boundary documentation.

### Feasibility

A complete remediation is not yet proven from repository evidence. The task is authorized only as one phased package with a mandatory design checkpoint. It must stop before implementation if safe Windows semantics cannot be demonstrated.

## 7. Package R4-ARCH-POLICY — complete allowed-edge policy

Proposed task: `OTC2-20260801-architecture-edge-policy-remediation`.

### Required invariant

Every local workspace dependency edge is classified by dependency kind and an explicit fail-closed policy. An edge not explicitly allowed is rejected. The current valid 19-member graph remains valid without editing package manifests merely to satisfy the new checker.

### Complete category catalogue

The existing 29 categories remain the closed catalogue:

```text
tool, app, foundation, platform, runtime, identity,
account-session, world-directory, game-session, transport,
protocol-core, protocol-canary, protocol-oteryn,
game-domain, game-simulation, world-storage,
render-types, renderer, ui-core, ui-runtime, input, audio,
asset-types, asset-runtime, settings, diagnostics,
extension-api, extension-host, feature
```

The implementation must define an explicit allowed-target set for every source category. Empty sets are explicit. The policy must not use a partial forbidden-edge predicate or a default-allow branch.

### Dependency kinds

- normal dependencies use the explicit production allowed-edge table;
- build dependencies use a separate explicit table and default deny; no local build edge is accepted merely because a normal edge would be accepted;
- dev dependencies use a separate explicit table. It may include the production edge plus reviewed test-only edges such as `app -> tool` and the existing protocol test dependency, but it must not ignore dev dependencies;
- target-specific dependencies retain their Cargo kind and are checked by the same tables;
- unknown or missing dependency kind in synthetic fixtures fails schema validation.

The fixture schema must be versioned when dependency kind is added.

### Production and test paths owned

- `oteryn-client/tools/architecture-check/src/lib.rs`
- `oteryn-client/tools/architecture-check/src/main.rs` only if output/CLI contract changes
- `oteryn-client/tools/architecture-check/tests/policy_fixtures.rs`
- `oteryn-client/tests/architecture-fixtures/**`

### Architecture/documentation paths owned

- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- one new allowed-edge policy ADR under `oteryn-client/docs/architecture/decisions/`
- its own active task record

### Shared-path lease

- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/CHANGELOG.md`
- `docs/agents/BUILD_TEST_MATRIX.md` only if fixture/check commands change

No dependency, root Cargo manifest, lockfile, deny policy or workflow change is expected or authorized. If one becomes necessary, the worker stops and returns to planning.

### Migration behavior

- capture the exact current 19-member graph as a positive fixture/evidence snapshot;
- update all schema-v1 fixtures to the new dependency-kind schema;
- run the checker against the real workspace before changing any manifest;
- if the current graph exposes an unmodelled valid edge, amend the explicit policy with a documented architectural rationale;
- do not edit existing member dependencies/categories to make the checker green unless a separate architecture migration task is approved;
- retain stable violation ordering and preserve `E005_FORBIDDEN_EDGE` or provide an explicit compatibility migration for consumers.

### Cheapest reproducible tests

- an exhaustive table-driven test over every category pair for normal, build and dev kinds proving every pair is classified exactly once;
- positive fixtures for every allowed edge class and every dependency kind;
- negative fixtures for representative and exhaustive denied pairs, including the audit example `transport -> renderer`;
- unknown category, unknown dependency kind, unresolved path, cycle and source-policy tests preserved;
- the exact real 19-member workspace passes unchanged.

Exhaustiveness may be implemented by compact generated/table-driven fixtures; it does not require hundreds of handwritten files.

### Component validation

```text
cargo test --locked -p oteryn-architecture-check --all-targets
cargo run --locked -p oteryn-architecture-check -- workspace .
```

### Heavy final gate

Complete Rust workspace checks, both Rust CI jobs, repository `CI / Required`, complete changed-file/diff review and no unresolved review threads.

### Acceptance criteria

- no dependency edge is accepted by default;
- all 29 source categories have explicit normal/build/dev policy entries;
- Cargo dependency kind is parsed and enforced;
- exhaustive positive and negative tests exist;
- the unchanged 19-member graph passes;
- the policy preserves the normative direction in `ARCHITECTURE.md` and does not weaken cycle, source or containment checks;
- policy changes require ADR review rather than opportunistic allowlist expansion.

### Rollback boundary

One revert restores only architecture-check policy/schema/fixtures and the owning ADR/docs. It does not touch member manifests or other remediation packages.

### Feasibility

Implementation is feasible from current evidence without a new dependency. The exact allow tables require a short policy checkpoint before code, but no external owner decision is currently required.

## 8. Shared lease and CI rules

The following integration paths are serialized across all packages:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
```

Rules:

1. one active task holds each shared-path lease;
2. PR #23 must release `MODULE_CATALOG.md` and `CHANGELOG.md` before a remediation task edits them;
3. no manual `Cargo.lock` conflict resolution;
4. source work may proceed without a shared lease, but the PR may not enter final validation until integration paths are leased and current;
5. every merge invalidates later workspace evidence; downstream branches restack and rerun the complete gate;
6. exact-head heavy Rust CI runs are serialized even when focused tests ran concurrently.

## 9. Deferred and blocked decisions

- Complete process-memory erasure is not an attainable acceptance claim; only project-owned buffer cleanup is in scope.
- A new secret-zeroization dependency is deferred unless `R1-SECRET` proves a concrete API gap.
- Forced worker termination, detached threads and exit with live workers are rejected for `R2-SHUTDOWN`.
- The exact safe Windows opened-object primitive for `R3-ASSET-OPEN` remains a mandatory design decision. Failure to prove one blocks implementation rather than weakening the finding.
- No workflow change or new CI platform is pre-authorized. Platform claims require named evidence from the platform tested.
- No existing crate manifest/category migration is authorized for `R4-ARCH-POLICY`.
- No remediation worker launches until this planning PR and its separate lifecycle archive PR merge.

## 10. Planning acceptance

This plan is complete when:

- every MEDIUM finding has exactly one planned disposition;
- all production, test, documentation and conditional integration paths are named;
- public producers/consumers and contract amendments are identified;
- `R1-SECRET -> R2-SHUTDOWN` serialization is enforced;
- asset-open feasibility remains fail closed;
- architecture policy preserves the current 19-member graph;
- no concurrent shared path is assigned;
- exactly one first worker prompt exists;
- the planning task contains one checkpoint and one next action.

## 11. Next action

After this plan PR and its separate task-archive PR merge, launch only `R1-SECRET` from `NEXT_POST_W7_SECRET_LIFECYCLE_AGENT.md` after a fresh main/open-PR/task/shared-lease preflight.