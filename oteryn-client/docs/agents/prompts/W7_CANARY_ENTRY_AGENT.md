# W7-CANARY-ENTRY Worker Prompt

```text
Work autonomously in repository blakinio/otclient as lane W7-CANARY-ENTRY for wave OTERYN-W7-TECHNICAL-LOGIN.

Do not start until W7-ENTRY-CONTRACT is merged/archived and the coordinator confirms exact current main, producer commit, no overlap and lease state.

Read all required agent/architecture/lifecycle/security/protocol documents, Canary-current research, merged ENTRY APIs, current tasks/PRs/reviews/CI and exact coordinator-approved Canary source. Canary is read-only evidence.

Create one unique task, branch, worktree and early draft PR. Record exact Canary revision, release/build identifiers, source paths and fixture provenance.

Contract role: consumer plus sole producer of W7's initial transport/Current-profile admission interface.

Exclusive paths:
- oteryn-client/crates/transport/**
- oteryn-client/crates/protocol-core/**
- oteryn-client/crates/protocol-canary/**
- oteryn-client/contracts/canary/current-entry/**
- oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md

Consume merged ENTRY types without substitutes. Input is one explicitly selected world/host/port, selected character name and one moved GameEntryCredential. Output is SessionEntered or typed EntryFailure.

Exact initial evidence cut to revalidate:
- Canary 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f;
- release 3.6.1, protocol/client 1525;
- Current profile, OpenTibia RSA, server challenge before login;
- modern block-count framing and modern padding;
- sequence checksum after login and official compression high-bit signaling;
- Current login layout: OS u16, protocol u16, client version u32, client-version string, asset-hash string, preview byte, RSA block containing XTEA key/GM/session key/character/challenge and optional OTCv8 probe;
- one-shot session key consumed against character and Current profile;
- successful placement emits login 0x17, bounded pre-world packets including 0x1A and 0xEF, pending-state 0x0A and enter-world 0x0F before map description.

Admission rule:
- parse and validate the ordered bounded prefix through 0x0F;
- emit SessionEntered only after 0x0F in the correct generation/connection;
- stop before map-description decoding and disconnect cleanly;
- do not implement general world/gameplay decoding, map, inventory, chat, combat or protocol-domain APIs.

Only this lane may publish the initial connection/admission trait and exact Current-profile framing/login types. Do not publish ENTRY shared types or general gameplay packet enums.

Security/parser requirements:
- bounded reads/writes/frames/strings/decompression and checked arithmetic;
- explicit timeouts and partial I/O handling;
- challenge/profile/version/character validation;
- checksum/sequence/padding/compression validation;
- no secret Debug/Display/logging/persistence;
- consume credential once and clear credential, XTEA key and buffers on every terminal path;
- no automatic replay/retry with the same credential;
- no unsafe code or policy weakening.

Synthetic fixtures only unless exact public provenance permits otherwise. Do not commit private captures, credentials or proprietary bytes. Source-derived vectors must name revision/file/function and contain only the minimum original test bytes necessary.

Dependency selection:
- no crypto/compression dependency or version is pre-approved;
- use current primary documentation/source, Rust 1.94 compatibility, minimal features, license/advisory review and cargo-deny;
- acquire the serialized shared-path lease before Cargo/lockfile/deny/shared-doc edits;
- otherwise finish exclusive work and mark integration_ready;
- manual Cargo.lock conflict resolution is prohibited.

Required automated tests:
- exact challenge/login/admission happy transcript;
- malformed/truncated/oversized length and string fields;
- challenge, version, profile, checksum, sequence, padding and opcode-order mismatch;
- bounded decompression bomb/output;
- partial read/write, timeout, disconnect and cancellation;
- wrong character, expired/replayed credential and duplicate SessionEntered prevention;
- cleanup and secret-redaction assertions.

Interactive evidence:
- after exact-head automated gates, one named exact configured Canary revision/issuer may be tested with a fresh credential;
- record one 0x0F admission and safe disconnect without storing secrets/captures;
- if environment/credential/deployed-revision evidence is unavailable, mark real Rust admission blocked and do not claim compatibility.

Legacy OTClient E2E evidence is reference only, never Rust proof. Run exact-head locked metadata, fmt, strict Clippy, all tests, architecture check, cargo-deny and repository CI; inspect full diff/threads; merge through gates and archive separately.
```
