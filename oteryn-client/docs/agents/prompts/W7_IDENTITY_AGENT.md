# W7-IDENTITY Worker Prompt

```text
Work autonomously in repository blakinio/otclient as lane W7-IDENTITY for wave OTERYN-W7-TECHNICAL-LOGIN.

Do not start until W7-ENTRY-CONTRACT is merged/archived and the coordinator confirms exact current main, producer commit, no overlap and lease state.

Read all required agent/architecture/lifecycle/security documents, current tasks/PRs/reviews/CI, the merged ENTRY APIs, and exact Oteryn Platform/Gateway source at the coordinator-approved revision. External repositories are read-only.

Create one unique task, branch, worktree and early draft PR. Record exact producer/base commits and blockers.

Contract role: consumer. Do not redefine AccountSessionId, CharacterId, WorldId, GameplayChannelId, DirectoryRevision, GameEntryRequest, GameEntryCredential, EntryFailure, SessionEntered or entry lifecycle states.

Exclusive paths:
- oteryn-client/crates/platform/**
- oteryn-client/crates/identity/**
- oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md

Required bounded scope:
- Authorization Code + PKCE S256 transaction generation;
- system-browser launch request abstraction without embedded credentials;
- exact state, callback path, origin, active-generation, stale, duplicate and mismatch validation;
- one authorization-code exchange boundary;
- strict bounded HTTP/JSON boundaries for Game Login Ticket issue and Gateway POST /v1/login;
- exact Gateway protocol_version 1 request and response DTOs only;
- validate one selected world and one character whose world_id matches it;
- convert raw DTOs only into merged ENTRY domain types;
- clear code verifier, callback code, access/refresh token and Game Login Ticket at exact terminal boundaries;
- preserve typed redacted errors, bounded timeouts/response sizes and no retry that can duplicate one-shot issuance;
- no Oteryn password collection and no Canary password fallback.

Exact current Gateway response surface:
- protocol_version
- session { credential, expires_at }
- worlds[] { id, slug, name, region, host, port }
- characters[] { id, name, level, vocation, world_id }

Do not invent directory revisions, gameplay-channel IDs, issuer directories, multi-world routing or extra response fields.

Mandatory blocker W7-BLOCK-IDENTITY-REDIRECT:
- current Platform source requires redirect URI exactly http://127.0.0.1/callback and rejects a port;
- normative Rust SECURITY_MODEL requires an OS-assigned loopback port;
- do not bind fixed port 80, weaken the invariant, silently substitute localhost, or invent dynamic registration;
- implement only deterministic transaction/state-machine and fake browser/listener/HTTP adapters while this remains unresolved;
- the real browser/listener adapter and real Identity compatibility claim remain blocked and must be explicit in code docs/task/PR.

Current Platform revokes access and associated refresh tokens after one Game Login Ticket. Claim only one bounded bootstrap account-session attempt, not reusable relog/channel switching.

Dependency selection:
- no dependency/version is pre-approved;
- any HTTPS/JSON/browser dependency requires current primary-source evidence, Rust 1.94 compatibility, minimal features, license/advisory review and the serialized shared-path lease;
- never weaken deny/lint/unsafe policy.

Shared-path lease set is exactly the one in CURRENT_PARALLEL_WAVE.md. If unavailable, keep shared paths read-only, finish exclusive work, mark integration_ready and wait. Manual Cargo.lock conflict resolution is prohibited.

Automated evidence must include fake-service tests for PKCE S256, state/path/origin/generation, stale and duplicate callbacks, malformed/oversized/trailing JSON, unknown fields, timeout/cancel, no-store headers where observable, selection mismatch, one-shot ticket/session handoff, cleanup and secret redaction.

Run exact-head locked metadata, fmt, strict Clippy, all tests, architecture check, cargo-deny and repository CI. Inspect full diff and all review threads. Do not claim real or production compatibility while the blocker/deployment evidence is absent. Merge through gates and archive separately.
```
