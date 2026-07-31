# Post-W7 audit evidence index

Task: `OTC2-20260731-rust-client-post-w7-audit`

## Repository state

- exact `main`: `227958e3fb33a3cf1a18b0b6da011290c2877cd2`;
- W7 feature merge: `946063cd9c19ae1ae17726649bb4a0b9f21e6e32` / PR #118;
- W7 archive merge: `227958e3fb33a3cf1a18b0b6da011290c2877cd2` / PR #119;
- tested PR merge ref: `38b656add027f8aa21bdc5bde51424347137256c`;
- open PRs at the cut: #97, #48 and #23; none changes `oteryn-client/**`;
- no unresolved review threads or overlapping Rust-client task/lease were identified.

PR #119 changed only `docs/agents/MODULE_CATALOG.md` and moved the W7 task record from active to archive. The implementation, manifests, lockfile and workflow remained unchanged.

Identical blobs between the tested PR merge ref and current `main`:

- `oteryn-client/Cargo.toml`: `3014a23b30766d4b5e63809f7339486315590913`;
- `oteryn-client/Cargo.lock`: `0f2e91094260c9ea5990d2d8713be1a680de062f`;
- `oteryn-client/apps/client/src/technical_login.rs`: `42bc41c6939876bc204a78d3a31875974914dce7`.

## Exact CI evidence

Rust Client run `30647931191`:

- Windows job `91213890051`: locked metadata, formatting, strict Clippy, workspace tests and architecture check passed;
- Supply Chain job `91213890169`: cargo-deny advisories, bans, licenses and sources passed;
- checkout: `38b656add027f8aa21bdc5bde51424347137256c`;
- 139 ordinary tests passed;
- no documentation-test phase was present.

Final heads for PRs #50, #54, #61, #73, #79, #86, #92, #104, #110, #113 and #118 have successful Rust Client workflow runs.

## Key source evidence

- Identity secrets/callback: `oteryn-client/crates/identity/src/lib.rs:1-220,320-545,680-705`;
- Platform secret/HTTP boundary: `oteryn-client/crates/platform/src/lib.rs:90-205,300-390`;
- runtime cancellation/join: `oteryn-client/crates/app-runtime/src/runtime.rs:180-270,390-465`;
- event-loop close path: `oteryn-client/apps/client/src/main.rs:105-175,185-235`;
- configuration timeouts: `oteryn-client/apps/client/src/technical_login.rs:170-245`;
- transport bounds: `oteryn-client/crates/transport/src/lib.rs:1-240`;
- asset source open: `oteryn-client/tools/asset-compiler/src/lib.rs:285-330`;
- architecture edge policy: `oteryn-client/tools/architecture-check/src/lib.rs:385-455`.

## Governance evidence

- `docs/agents/ACTIVE_WORK.md:1-20`;
- `docs/agents/MODULE_CATALOG.md`;
- `oteryn-client/docs/research/technical-login/W7_ENTRY_CONTRACT_EVIDENCE.md`;
- `oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md`;
- `oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md`;
- `oteryn-client/docs/research/technical-login/W7_LOGIN_E2E_EVIDENCE.md`.

## Local execution limitation

`git ls-remote https://github.com/blakinio/otclient.git refs/heads/main` failed with exit code `128` because the sandbox could not resolve `github.com`. `cargo` and `cargo-deny` were unavailable locally. Local Cargo commands are therefore `NOT RUN`; exact repository CI is the execution evidence.
