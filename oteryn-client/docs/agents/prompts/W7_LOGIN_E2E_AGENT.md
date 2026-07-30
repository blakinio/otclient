# W7-LOGIN-E2E Worker Prompt

```text
Work autonomously in repository blakinio/otclient as lane W7-LOGIN-E2E for wave OTERYN-W7-TECHNICAL-LOGIN.

Do not start final integration until W7-ENTRY-CONTRACT, W7-IDENTITY and W7-CANARY-ENTRY required producer commits are merged/archived and the coordinator grants the final integration lease. After ENTRY merges, private fake-service harness work may begin only in exclusive paths.

Read all required agent/architecture/lifecycle/security documents, current tasks/PRs/reviews/CI, merged producer APIs and exact evidence/blockers. Create one unique task, branch, worktree and early draft PR. Record exact base/producer commits and phase (`private_fake` or `final_integration`).

Contract role: final consumer/composition owner. Do not redefine public entry, identity, directory, transport or protocol types.

Exclusive paths before final integration:
- oteryn-client/crates/app-runtime/**
- oteryn-client/tests/integration/technical-login/**
- oteryn-client/docs/research/technical-login/W7_LOGIN_E2E_EVIDENCE.md

Final integration lease additionally owns:
- oteryn-client/apps/client/**

Required composition:
- preserve the existing Windows winit window, renderer and close lifecycle;
- keep browser, listener, HTTP and TCP work off the event-loop thread in explicitly owned cancellable/joined workers;
- use typed runtime events for progress/result/cancellation and reject stale generations;
- expose one explicit technical configuration surface for authorization/token endpoints, public OAuth client ID, Gateway base URL, expected world identity/host/port and selected character; no hidden production defaults or committed credentials;
- bind OAuth callback to 127.0.0.1:0 and use the actual OS-assigned port proven by the Platform producer contract;
- validate the selected character belongs to the selected world;
- request/move one fresh credential into Canary admission;
- report SessionEntered or typed recoverable EntryFailure;
- stop before map-description decoding;
- disconnect safely and clear callback state, verifier, code, access/refresh token, Game Login Ticket, Game Session credential, transport keys and session buffers.

Private fake-service E2E must prove:
- valid PKCE success path on an OS-assigned loopback port;
- stale callback rejection;
- duplicate callback rejection;
- state/path/peer/generation mismatch rejection;
- malformed/oversized/trailing Gateway responses;
- world-character mismatch rejection;
- exactly one credential handoff and duplicate/late use rejection;
- a second attempt requires a fresh ticket/session credential;
- SessionEntered only after the ordered Canary admission prefix reaches 0x0F;
- cancellation/window close/disconnect cleanup;
- no credential in Debug, Display, logs, panic text, snapshots or diagnostics.

Real-path evidence rules:
- revalidate current Platform dynamic-loopback tests and use the exact same redirect URI in authorization and token exchange;
- observe a real system-browser launch and return on supported Windows only when the exact Platform/Gateway configuration is available;
- if deployed Identity/Gateway/Canary revisions, TLS, client ID, issuer mapping or credentials are unavailable, do not run or claim the real path;
- legacy OTClient physical E2E is reference only;
- the final PR may merge a fully passing fake technical flow with exact real/deployment path explicitly blocked, as allowed by CURRENT_PARALLEL_WAVE.md.

Shared-path lease:
- final integration may edit apps/client and the common Cargo/lockfile/deny/catalog/matrix/changelog/repository-layout/Rust-workspace paths only while explicitly granted;
- non-holder phases keep them read-only and mark integration_ready;
- manual Cargo.lock conflict resolution is prohibited; restack/regenerate.

Acceptance evidence:
- pinned Rust 1.94 Windows executable builds;
- existing window opens and remains responsive during fake login;
- exact-head locked metadata, fmt, strict Clippy, all unit/integration/E2E tests, architecture check, cargo-deny and repository required CI pass;
- full changed-file/diff review and no unresolved threads;
- interactive real flow names exact producer revisions or is recorded blocked without compatibility claim.

Do not add map rendering/decoding, inventory, chat, combat, general-purpose native UI, channel switching, production assets, updater/deployment code or password fallback. Internal protocol work is for project-owned Oteryn/Canary compatibility only and must not be published as abuse or anti-cheat tooling. Merge through gates and archive separately.
```
