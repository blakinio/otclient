# Oteryn Client Security Model

Status: normative baseline. Detailed threat models for implementation slices extend this document.

## 1. Trust assumptions

The client runs on a user-controlled device and is not trusted by the server. Rust memory safety protects the product from classes of client bugs; it does not make the client authoritative or prevent modification by a determined user.

External inputs are untrusted:

- Identity and Platform responses;
- loopback callback requests;
- game-server bytes;
- directory and gameplay-channel data;
- manifests, updates and asset packs;
- local settings and caches;
- extension modules;
- command-line arguments and launcher IPC;
- replay and diagnostic files.

## 2. Security boundaries

```text
System browser / Identity
        |
        v
identity transaction boundary
        |
        v
account-session boundary
        |
        v
one-shot game-entry transaction
        |
        v
transport/protocol parser boundary
        |
        v
game domain
```

Separate boundaries also exist for launcher/updater, asset runtime, settings/credential storage, diagnostics and extension hosting.

## 3. Identity invariants

- Use Authorization Code + PKCE with `S256` through the system browser.
- Do not embed a client secret in the desktop application.
- Validate `state`, callback path, redirect origin and transaction generation.
- Bind the callback to an OS-assigned loopback port and a single active transaction.
- Reject stale, duplicate or mismatched callbacks.
- Do not collect the main Oteryn password in the client UI.
- Do not send the main password to Canary or native game nodes.
- Do not silently fall back to legacy password authentication for an Oteryn profile.
- Keep long-lived eligible credentials only in the operating-system credential store.
- Do not expose bearer credentials to first-party feature crates or extensions.

## 4. Game-ticket invariants

A game-entry credential is short-lived and scoped according to the authoritative contract, including the selected account/character/world/gameplay channel where applicable.

- Consume a one-shot ticket once.
- Clear in-memory ticket material after handoff.
- Do not persist tickets in settings, logs or crash reports.
- Do not replay the original ticket during automatic reconnect.
- Obtain a fresh ticket for relog to another gameplay channel.
- Reject routing that is not authenticated by the Platform/Gateway contract.
- Distinguish account-session credentials, game-entry tickets and game-session/resume credentials by type.

## 5. Network and parser security

- Use authenticated encrypted transport where the exact protocol supports/requires it.
- Validate certificate/endpoint policy according to environment and contract.
- Bound reads, writes, frames, collections, strings and decompressed output.
- Treat count/length fields as hostile before allocation.
- Use checked arithmetic and conversions.
- Reject malformed state transitions.
- Avoid parser panics and uncontrolled recursion.
- Apply timeouts and queue limits.
- Redact endpoints or identifiers classified as sensitive from telemetry.

## 6. Server authority

The server validates all meaningful actions, including movement legality, range, line of sight, cooldowns, item ownership, quantities, container access, target validity and economic operations.

The client may predict visual movement and immediate UI feedback, but reconciles with authoritative state. Extension APIs do not grant authority.

## 7. Updater security

The launcher/updater must:

- consume an authenticated update manifest;
- verify cryptographic signatures and content hashes before activation;
- enforce expected product/channel/version metadata;
- prevent path traversal and unsafe archive links;
- stage outside the active installation;
- activate atomically;
- retain a tested rollback path;
- never execute unverified downloaded content;
- avoid logging signed URLs, credentials or private paths unnecessarily.

TLS alone is not sufficient to authorize an update artifact.

## 8. Asset security

Runtime asset packs are immutable, versioned and verified before mounting.

- Every distributable source has provenance and license records.
- Pack indexes, offsets and lengths are bounds-checked.
- Decompression has output and ratio limits.
- Shader/material inputs are validated and compiled through controlled paths.
- Asset IDs cannot silently change meaning within a compatibility version.
- Development loose-file mode is not enabled in production without a separate policy.
- Proprietary assets are not committed without confirmed redistribution rights.

## 9. Settings and local storage

- Settings are typed, schema-versioned and size-limited.
- Import/export excludes secrets.
- Untrusted imported layouts cannot create arbitrary file/network/process actions.
- Cache corruption fails safely and can be rebuilt.
- Sensitive local files use restrictive platform permissions when applicable.
- The user-data directory cannot redirect trusted writes to arbitrary unsafe locations without explicit validation and product policy.

## 10. Extension sandbox

Optional extensions use WebAssembly and capability-based host APIs.

Forbidden by default:

- raw filesystem access;
- raw sockets;
- process creation;
- native dynamic libraries;
- credential store;
- authentication/session secrets;
- raw protocol frames;
- unrestricted memory sharing;
- direct GPU command access.

The host enforces module provenance policy, memory limit, fuel/time budget, host-call rate limits, storage quota and revocation. A crashed or malicious extension can be terminated without corrupting core state.

## 11. Diagnostics, crash reports and replay

Diagnostics use structured redaction at creation time, not only before upload.

Never record:

- access/refresh tokens;
- PKCE verifier or authorization codes;
- game tickets/session secrets;
- cookies;
- private chat by default;
- personal filesystem paths when avoidable;
- extension private storage;
- full raw server payloads without explicit sanitized developer mode.

Telemetry is documented, user-visible and configurable according to product/legal policy.

## 12. Unsafe Rust and native dependencies

- `unsafe` is denied by default at workspace level.
- An exception requires a narrow module, documented safety invariants, tests and review.
- Native dependencies are minimized and isolated.
- FFI inputs and callbacks are treated as untrusted boundaries.
- Supply-chain policy includes locked dependencies, license checks, advisory scanning and controlled update review.

## 13. Threat-driven tests

Required negative tests include:

- forged/stale OAuth callback;
- incorrect `state` or callback path;
- duplicate authorization completion;
- game-ticket replay;
- ticket scoped to the wrong gameplay channel;
- automatic reconnect attempting initial-ticket reuse;
- malformed/truncated/oversized protocol frames;
- decompression bomb;
- malicious asset offsets and archive paths;
- unsigned or rollback update attack;
- corrupted settings/layout import;
- extension CPU/memory/host-call exhaustion;
- diagnostics redaction regressions.

## 14. Incident containment

The client supports safe failure actions:

- terminate only the affected extension;
- unmount/reject a bad asset pack;
- rollback a failed update;
- close a protocol session on fatal violation;
- preserve account session only when safe;
- require reauthentication after credential uncertainty;
- produce a redacted correlation identifier for support.

No component weakens validation merely to continue connecting.
