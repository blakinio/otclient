# Next Diagnostics Agent Prompt

Copy the block below into one fresh worker session only after `CURRENT_PARALLEL_WAVE.md` is merged and live state confirms that the lane is still unclaimed.

```text
Work autonomously in repository:

blakinio/otclient

Task: implement the next bounded Gate 1 package for the greenfield Rust Oteryn client: exactly one small `oteryn-diagnostics` crate defining structured diagnostic-event and secret-redaction contracts.

Do not rely on previous chat history. Current Git/main, root and nested AGENTS.md, live tasks/PRs, accepted architecture/security documents, merged foundation source/tests, current Cargo policy and exact CI are the only source of truth.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate Canary, Oteryn Platform, upstream or another repository;
- never push directly to main;
- use one dedicated task, branch and worktree;
- open a draft PR early;
- do not weaken branch protection, tests, lints, dependency policy or security checks;
- do not commit secrets, private captures, proprietary assets, raw server payloads or personal data.

Mandatory preflight:

1. Read AGENTS.md and docs/agents/README.md.
2. Read oteryn-client/AGENTS.md.
3. Read:
   - oteryn-client/docs/architecture/ARCHITECTURE.md;
   - oteryn-client/docs/architecture/SECURITY_MODEL.md;
   - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md;
   - oteryn-client/docs/agents/PROGRAM.md;
   - oteryn-client/docs/agents/WORKSTREAMS.md;
   - oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md;
   - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md;
   - oteryn-client/docs/operations/RUST_WORKSPACE.md.
4. Inspect every active Rust-client task, open PR, review thread and required check.
5. Inspect merged foundation PR #54, archive PR #58, `oteryn-client/crates/foundation/**`, current workspace manifests, architecture checker, fixtures and existing validation matrix.
6. Verify current main contains the foundation producer commit and that no task/PR owns:
   - oteryn-client/crates/diagnostics/**;
   - the diagnostics public contract;
   - Cargo.toml/Cargo.lock or the required shared integration paths.
7. Perform a fresh dependency/security/license/source preflight. Default to the standard library and the merged `oteryn-foundation` crate. Do not add an external crate merely because it is commonly used.
8. Create a bounded parallel task record using the required metadata, claim lane W2-DIAG, and declare the unique shared-path lease before editing shared files.

Required base evidence at plan creation:

- foundation implementation merge: 7a68f6e7d92eb6b05078bb001e4881d78544a82b;
- foundation archive/main checkpoint: acbc78c618e6998fe29d16833f5c907d8ae8d1e8.

Revalidate live main. Record a newer exact base when the repository has advanced.

Goal:

Add exactly one package named `oteryn-diagnostics` under `oteryn-client/crates/diagnostics/`. It owns narrow, reusable contracts for structured diagnostic events and redaction-at-creation. It may depend downward on `oteryn-foundation` when a generic technical primitive is actually reused.

Required functional envelope:

- stable structured severity/category/code concepts suitable for future sinks without selecting or installing a sink now;
- typed diagnostic fields whose safe versus sensitive handling is explicit;
- redaction performed when values enter the diagnostic representation, not only before upload;
- deterministic `Debug`/`Display` behavior that cannot reveal sensitive values;
- safe correlation/technical context without account, character, world, protocol or product identifiers;
- bounded data structures and deterministic behavior;
- focused regression tests using obviously synthetic marker values shaped like access tokens, authorization codes, PKCE verifiers, game tickets, cookies, private chat and personal paths, proving those marker values do not appear in formatted diagnostics;
- compile-time or constructor-level barriers preventing arbitrary untrusted strings from silently becoming safe fields;
- documentation of what downstream callers must classify before creating an event.

Required boundaries:

- no global logger, subscriber or process-wide mutable registry;
- no `tracing` subscriber installation and no product tracing integration;
- no filesystem/network sink, telemetry upload, crash-report upload or support-bundle generation;
- no replay recorder/runner;
- no async runtime, executor, hidden thread or background worker;
- no application service composition;
- no protocol, authentication, directory, gameplay-channel, asset, renderer, UI or legacy-client implementation;
- no arbitrary raw external text in errors or safe diagnostic fields;
- no real secret, real endpoint, real token, private capture or personal path in any fixture or example;
- diagnostics must not be required for correctness and must own no authoritative state;
- no unsafe or FFI.

Default owned path:

- oteryn-client/crates/diagnostics/**

Default shared-path lease:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md
- docs/agents/CHANGELOG.md

Do not edit architecture-check policy/fixtures by default. The `diagnostics` category already exists. Touch those paths only when fresh evidence proves a missing dependency rule, and record the enlarged lease before editing.

Implementation quality:

- prefer closed enums, typed wrappers and reviewed static templates over arbitrary strings;
- keep public APIs minimal and difficult to misuse;
- avoid generic `Any`, unbounded maps and broad trait-object frameworks;
- do not create a facade for future sinks that do not exist;
- document redaction and drop/ownership behavior;
- keep error types narrow and secret-free;
- add focused unit/doc/compile-fail tests where they provide real API evidence;
- preserve zero or minimal external dependencies.

Validation required on the exact final head:

- cargo metadata --locked --format-version 1;
- cargo fmt --all --check;
- cargo clippy --workspace --all-targets --locked -- -D warnings;
- cargo test --workspace --all-targets --locked;
- real workspace architecture validation;
- cargo-deny advisories/licenses/bans/sources;
- Rust Client / Windows;
- Rust Client / Supply Chain;
- repository CI / Required;
- complete changed-file list and full diff review;
- all comments, reviews and unresolved threads inspected.

Do not claim product logging, upload, crash-reporting, replay, server compatibility, runtime performance or non-Windows compatibility from this contract-only package.

Finish end to end through the autonomous merge gate, then archive the task in a separate lifecycle PR. Leave exactly one next bounded recommendation, expected to be deterministic test support/fake-time helpers unless live evidence changes the order.
```
