# W7 Technical Login Application Integration Evidence

Status: private fake-runtime implementation in progress  
Lane: `W7-LOGIN-E2E`  
Branch: `feat/OTC2-20260731-w7-login-e2e`  
PR: #114

## Exact merged producers

- W7 entry contract: `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`;
- entry lifecycle archive: `8dcd353d5a9f19fabccf49508c27074f7749e3cf`;
- W7 Identity: `d66da47a33d6639876f3edda2b2c08709d1b7a5e`;
- Identity lifecycle archive: `5ffda0f64821d2cf9de388faa6675c05fd99e9d1`.

The final Canary producer commit is not recorded here until PR #113 and its separate lifecycle archive merge. No compatibility claim is derived from its draft head.

## Composition boundary

`oteryn-app-runtime` owns application orchestration only:

1. allocate one non-zero `GameEntryAttemptId`;
2. call merged `EntryLifecycle::begin_authentication`;
3. run one injected Identity operation in an owned cancellable thread;
4. accept only merged `AccountSessionId`, `AccountDirectorySnapshot` and `GameEntryCredential` values;
5. validate the explicit typed development selection against the authoritative snapshot;
6. move the credential exactly once through `EntryLifecycle::begin_connecting`;
7. run one injected admission operation in an owned cancellable thread;
8. call `EntryLifecycle::session_entered` only after the operation reports the exact admission marker;
9. cancel and join all workers before dropping session-scoped state;
10. return through `Closing -> LoggedOut` on disconnect or shutdown.

No public Identity, directory, credential, transport or protocol type is created by this lane.

## Private fake matrix

| Scenario | Expected producer-owned outcome |
|---|---|
| complete success | `LoggedOut -> Authenticating -> AccountReady -> DirectoryReady -> EntryRequested -> CredentialReady -> Connecting -> SessionEntered` |
| second authentication while active | `RuntimeError::AuthenticationAlreadyActive` |
| second connection while active | `RuntimeError::ConnectionAlreadyActive` |
| stale completion | `EntryFailureKind::StaleAuthenticationTransaction` |
| duplicate callback | `EntryFailureKind::DuplicateCallback` |
| account session expiry | `EntryFailureKind::AccountSessionExpired` |
| stale directory revision | `EntryFailureKind::DirectoryRevisionStale` |
| selected character unavailable | `EntryFailureKind::SelectedEntryUnavailable` with `ChooseAnotherCharacter` |
| expired credential | `EntryFailureKind::CredentialExpired` before admission |
| consumed credential | second handoff rejected by merged lifecycle |
| second attempt | a new attempt and fresh credential are required |
| route/protocol mismatch | typed producer failure, no arbitrary server text |
| Canary denial | `EntryFailureKind::ServerAdmissionDenied` |
| transport timeout | `EntryFailureKind::TransportFailure` |
| cancellation during authentication | cancellation source set, worker joined, `SafeCancellation` |
| cancellation during connection | cancellation source set, worker joined, credential dropped |
| shutdown during active phase | both worker slots cancelled/joined before lifecycle close |
| redaction | no credential bytes in runtime `Debug`, typed failures or snapshots |

Identity-specific wrong-state, stale/duplicate/path/peer/generation callback and strict Gateway malformed/oversized/trailing response cases are already owned and tested by merged W7 Identity. The final E2E test will invoke that exact service rather than duplicate its parser or public types.

Canary framing, denial, ordered admission prefix and transport timeout cases remain owned by PR #113. Final E2E will consume its exact merged interface and fixtures rather than create substitutes.

## Evidence classification

### PASS

- exact ENTRY and Identity producer commits are merged and archived;
- LOGIN-E2E task, branch and draft PR are unique and own disjoint paths;
- the private runtime uses merged entry lifecycle and credential types;
- worker ownership has explicit cancellation and `JoinHandle` joins;
- runtime snapshots contain only typed non-secret state;
- no shared Cargo/lockfile/document path or `apps/client` path was edited while PR #113 holds the lease.

These PASS items are source/diff evidence only until the crate enters the workspace and exact CI executes.

### OBSERVED

- existing Windows shell owns the `winit` window, renderer close ordering and one joined wake worker on merged main;
- merged Identity owns system-browser launch and dynamic IPv4 loopback callback binding;
- named interactive Windows application login has not yet been exercised by this lane.

### BLOCKED

- final workspace registration, lockfile generation and full validation while PR #113 owns the serialized shared-path lease;
- final `apps/client` integration until exact Canary feature and archive merges;
- named real configured Identity -> Gateway -> Canary result without deployed endpoint/client/issuer evidence;
- production deployment readiness;
- arbitrary world/channel directory;
- gameplay, map rendering/decoding, reconnect/resume and production assets.

## Final validation gate

After exact Canary merge/archive and restack onto current main:

- `cargo metadata --locked`;
- `cargo fmt --all --check`;
- complete workspace Clippy with warnings denied;
- all workspace tests and doctests;
- architecture check;
- `cargo deny check`;
- Windows MSVC build on pinned Rust `1.94.0`;
- repository required CI;
- changed-file and full-diff review;
- review-thread check;
- named Windows launch/browser/callback smoke evidence when supported;
- exact-head repetition after final restack.

## Real-path boundary

No production endpoint, credential, client secret, private capture or deployed revision is stored in the repository. Real technical mode must remain explicitly opt-in and non-secret. If exact deployed evidence is unavailable, the final record must preserve `W7-BLOCK-REAL-RUST-E2E` and make no real compatibility or production claim.
