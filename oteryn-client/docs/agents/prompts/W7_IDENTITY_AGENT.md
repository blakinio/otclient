# W7-IDENTITY Worker Prompt

```text
Work autonomously in repository blakinio/otclient as lane W7-IDENTITY for wave OTERYN-W7-TECHNICAL-LOGIN.

Do not start until W7-ENTRY-CONTRACT is merged/archived and the coordinator confirms exact current main, producer commit, no overlap and lease state.

Read all required agent/architecture/lifecycle/security documents, current tasks/PRs/reviews/CI, the merged ENTRY APIs, and exact Oteryn Platform/Gateway source at the coordinator-approved revision. External repositories are read-only.

Create one unique task, branch, worktree and early draft PR. Record exact producer/base commits, source evidence and external/deployment blockers.

Contract role: consumer. Do not redefine AccountSessionId, CharacterId, WorldId, GameplayChannelId, DirectoryRevision, GameEntryRequest, GameEntryCredential, EntryFailure, SessionEntered or entry lifecycle states.

Exclusive paths:
- oteryn-client/crates/platform/**
- oteryn-client/crates/identity/**
- oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md

Required bounded scope:
- Authorization Code + PKCE S256 transaction generation;
- system-browser launch adapter without embedded credentials or shell interpolation;
- bind IPv4 loopback to 127.0.0.1:0 before browser launch and use the actual OS-assigned port;
- exact state, callback path, loopback peer, active-generation, stale, duplicate and mismatch validation;
- one bounded authorization-code exchange;
- strict bounded HTTP/JSON boundaries for Game Login Ticket issue and Gateway POST /v1/login;
- exact Gateway protocol_version 1 request and response DTOs only;
- validate one selected world and one character whose world_id matches it;
- convert raw DTOs only into merged ENTRY domain types;
- clear verifier, callback code, access/refresh token and Game Login Ticket at exact terminal boundaries;
- preserve typed redacted errors, bounded timeouts/response sizes and no retry that can duplicate one-shot issuance;
- no Oteryn password collection and no Canary password fallback.

Exact current Gateway response surface:
- protocol_version
- session { credential, expires_at }
- worlds[] { id, slug, name, region, host, port }
- characters[] { id, name, level, vocation, world_id }

Do not invent directory revisions, gameplay-channel IDs, issuer directories, multi-world routing or extra response fields.

Exact loopback producer evidence to preserve:
- Platform registers the public native client redirect base as http://127.0.0.1/callback with no fixed port;
- current Platform test NativeOAuthPkceTest::test_dynamic_loopback_port_authorization_and_pkce_s256_token_exchange_succeed_without_client_secret proves authorization and token exchange with an OS-assigned-style redirect such as http://127.0.0.1:49152/callback;
- wrong callback path and non-loopback redirect are rejected;
- therefore do not bind fixed port 80 and do not treat the no-port registration record as a blocker;
- revalidate this behavior at the exact producer revision before claiming real compatibility.

Current Platform revokes the native access token and associated refresh token after one Game Login Ticket. Claim only one bounded bootstrap account-session attempt, not reusable relog/channel switching.

HTTP/security requirements:
- non-loopback Platform/Gateway endpoints require HTTPS with normal certificate and hostname validation;
- loopback fake services may use HTTP;
- reject uncontracted redirects on sensitive API calls;
- reject unknown/trailing/oversized response data and invalid identifiers/ports/relationships;
- OAuth, ticket and session values never enter Debug, Display, logs, diagnostics, panic text, fixtures or persistence.

Dependency selection:
- no dependency/version is pre-approved;
- any HTTPS/JSON/browser/randomness dependency requires current primary-source evidence, Rust 1.94 compatibility, minimal features, license/advisory review and the serialized shared-path lease;
- prefer a bounded synchronous core that final composition can run on an explicitly owned worker thread; do not introduce an async runtime without an accepted architecture change;
- never weaken deny/lint/unsafe policy.

Shared-path lease set is exactly the one in CURRENT_PARALLEL_WAVE.md. If unavailable, keep shared paths read-only, finish exclusive work, mark integration_ready and wait. Manual Cargo.lock conflict resolution is prohibited.

Automated evidence must include:
- PKCE S256 known vector and state/verifier uniqueness using a CSPRNG port;
- fake browser/listener/HTTP success on an OS-assigned loopback port;
- state/path/peer/generation validation, stale and duplicate callbacks, timeout and cancellation;
- malformed/oversized/trailing JSON, unknown fields and invalid protocol version;
- no-store/cache headers where observable;
- selection mismatch and invalid/duplicate identifiers;
- one-shot ticket/session handoff, fresh-second-attempt requirement, cleanup and secret redaction.

Interactive evidence must name exact Platform/Gateway revisions and observe real system-browser launch/return on Windows. If deployed TLS, client configuration or reachable producer evidence is unavailable, mark only that real/deployment claim blocked; deterministic and fake integration may still merge without claiming production compatibility.

Run exact-head locked metadata, fmt, strict Clippy, all tests, architecture check, cargo-deny and repository CI. Inspect full diff and all review threads. Merge through gates and archive separately.
```
