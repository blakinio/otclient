# Post-W7 audit evidence index

Task: `OTC2-20260731-rust-client-post-w7-audit`  
Independent result: `VALIDATED_WITH_CORRECTIONS`

## Repository state

- exact `main`: `227958e3fb33a3cf1a18b0b6da011290c2877cd2`;
- W7 feature merge: `946063cd9c19ae1ae17726649bb4a0b9f21e6e32` / PR #118;
- W7 archive merge: `227958e3fb33a3cf1a18b0b6da011290c2877cd2` / PR #119;
- tested PR merge ref: `38b656add027f8aa21bdc5bde51424347137256c`;
- validator input branch head: `7c74c8b1801296a4f4788f0d69cb27c353476fe4`;
- open PRs during validation: #120, #97, #48 and #23;
- #120 changes only authorized audit/checkpoint paths;
- #97, #48 and #23 do not change `oteryn-client/**`;
- all four open PRs had zero unresolved review threads;
- no overlapping Rust-client task/lease was identified.

PR #119 changed only:

- `docs/agents/MODULE_CATALOG.md`;
- `docs/agents/tasks/active/OTC2-20260731-w7-login-e2e.md`;
- `docs/agents/tasks/archive/OTC2-20260731-w7-login-e2e.md`.

The implementation, manifests, lockfile and workflow remained unchanged.

Identical blobs between the tested PR merge ref and current `main`:

- `oteryn-client/Cargo.toml`: `3014a23b30766d4b5e63809f7339486315590913`;
- `oteryn-client/Cargo.lock`: `0f2e91094260c9ea5990d2d8713be1a680de062f`;
- `oteryn-client/apps/client/src/technical_login.rs`: `42bc41c6939876bc204a78d3a31875974914dce7`.

## Exact CI evidence

Rust Client run `30647931191`:

- Windows job `91213890051`: locked metadata, formatting, strict Clippy, workspace tests and architecture check passed;
- Supply Chain job `91213890169`: cargo-deny advisories, bans, licenses and sources passed;
- checkout: `38b656add027f8aa21bdc5bde51424347137256c`;
- Rust/Cargo `1.94.0`;
- 139 ordinary tests passed, independently re-summed from test-target results;
- no documentation-test phase or `Doc-tests` output was present;
- cargo-deny action built/used version `0.20.2` and reported advisories/bans/licenses/sources `ok`.

## Workspace inventory evidence

Root `oteryn-client/Cargo.toml` lists exactly 19 members. Every member manifest was independently read at exact `main`; the direct graph is recorded in `main-audit-report.md`. No manifest points to legacy `src/**`, `modules/**` or `mods/**`.

## Key source evidence

- Identity secret copies/callback: `oteryn-client/crates/identity/src/lib.rs`;
- Platform secret/HTTP boundary: `oteryn-client/crates/platform/src/lib.rs`;
- runtime cancellation/join: `oteryn-client/crates/app-runtime/src/runtime.rs`;
- event-loop close path: `oteryn-client/apps/client/src/main.rs`;
- configuration timeouts: `oteryn-client/apps/client/src/technical_login.rs`;
- transport bounds: `oteryn-client/crates/transport/src/lib.rs`;
- asset source open: `oteryn-client/tools/asset-compiler/src/lib.rs:285-330`;
- architecture edge policy: `oteryn-client/tools/architecture-check/src/lib.rs`;
- normative separation: `oteryn-client/docs/architecture/ARCHITECTURE.md`;
- production Canary fail-closed: `oteryn-client/crates/protocol-canary/src/lib.rs`;
- synthetic/production boundary tests: `oteryn-client/tests/integration/technical-login/src/lib.rs`.

## Governance evidence

- `docs/agents/ACTIVE_WORK.md`;
- `docs/agents/MODULE_CATALOG.md`;
- `oteryn-client/docs/research/technical-login/W7_ENTRY_CONTRACT_EVIDENCE.md`;
- `oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md`;
- `oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md`;
- `oteryn-client/docs/research/technical-login/W7_LOGIN_E2E_EVIDENCE.md`.

## Unauthorized-change evidence

At validator input head, compare against exact `main` contained only:

- `docs/agents/tasks/active/OTC2-20260731-rust-client-post-w7-audit.md`;
- `oteryn-client/docs/audits/post-w7/**`.

Independent-validator corrections stayed within the same authorized paths.

## Local execution limitation

The primary audit sandbox could not resolve `github.com`, and local `cargo`/`cargo-deny` were unavailable. Local Cargo commands remain `NOT RUN`; exact repository CI is the execution evidence.
