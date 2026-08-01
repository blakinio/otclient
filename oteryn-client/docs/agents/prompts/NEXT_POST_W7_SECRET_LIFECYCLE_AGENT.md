# Next Post-W7 Secret-Lifecycle Worker Prompt

Copy the prompt below into a fresh Codex session only after the post-W7 remediation planning PR and its separate planning-task archive PR have merged.

---

ROLE

You are the sole secret-lifecycle remediation implementer for the validated post-W7 Rust-client audit, phase: `implementation`.

REPOSITORY AND REQUIRED LIVE STATE

Repository: `blakinio/otclient`

Task to create:

`OTC2-20260801-secret-lifecycle-remediation`

Source audit:

`OTC2-20260731-rust-client-post-w7-audit`

Accepted plan:

`oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md`

Before changing state, verify from durable repository state:

- current exact `main`;
- merged audit PR #120 and audit archive PR #121;
- merged remediation-plan PR and its separate archived planning task;
- canonical `main-audit-report.md` and `VALIDATOR_PACKET.md`;
- live open PRs and active tasks;
- current path and public-contract ownership;
- current required CI;
- whether PR #23 or another task still owns `docs/agents/MODULE_CATALOG.md` or `docs/agents/CHANGELOG.md`.

Do not rely on chat history for revisions, ownership, merge order or CI.

OBJECTIVE

Remediate `OTC2-AUD-001` without overstating guarantees.

Make this invariant true:

Every secret-bearing allocation controlled by project code has one explicit owner, a bounded lifetime, redacted formatting and deterministic best-effort overwrite on terminal drop. Documentation must state that scope precisely and must not claim erasure of allocator remnants, operating-system process arguments, browser state, TLS/library buffers or copies made inside third-party libraries or the operating system.

This is actual security remediation plus truthful claim correction. A documentation-only result is not accepted.

AUTHORIZATION

```yaml
implementation_authorized: true
policy_version: 2
task_kind: implementation
context_pressure: medium
decomposition_decision: phased
execution_mode: codex
```

Create one task, one branch/worktree and one draft PR before broad implementation. Do not create a second remediation task.

OWNED PRODUCTION PATHS

- `oteryn-client/crates/identity/src/lib.rs`
- `oteryn-client/crates/platform/src/lib.rs`
- `oteryn-client/crates/game-session/src/lib.rs` only if the common secret ownership contract must be aligned

OWNED TEST AND EVIDENCE PATHS

- tests embedded in the owned crates;
- `oteryn-client/tests/security/auth/**`;
- `oteryn-client/tests/integration/technical-login/**` only for secret-boundary regression coverage;
- `oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md`;
- `oteryn-client/docs/architecture/TECHNICAL_LOGIN.md`;
- your own task record.

CONDITIONAL SHARED-PATH LEASE

These paths are not owned until a unique lease is available and recorded in the task:

- `docs/agents/MODULE_CATALOG.md`;
- `docs/agents/CHANGELOG.md`;
- `docs/agents/BUILD_TEST_MATRIX.md` only if test routing changes materially;
- `oteryn-client/Cargo.toml`;
- affected crate manifests;
- `oteryn-client/Cargo.lock`;
- `oteryn-client/deny.toml`.

If PR #23 or another active task owns a shared documentation path, continue only in isolated owned Rust/evidence paths and do not edit, stage or claim the shared path. Final integration waits for a released or explicitly transferred lease.

A new dependency is not pre-approved. Prefer the existing standard-library-owned-byte pattern. If a new zeroization dependency is materially required, stop implementation at a durable checkpoint that identifies the exact API gap, proposed exact version/features, dependency graph, license/advisory/source result and required Cargo/lockfile lease.

REQUIRED READS

- `AGENTS.md`
- `docs/agents/AGENTS.md`
- `docs/agents/PROMPTING_HANDOVER.md`
- `docs/agents/EXECUTION_PROTOCOL.md`
- `docs/agents/CONTEXT_HANDOFF.md`
- `oteryn-client/AGENTS.md`
- `oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md`
- `oteryn-client/docs/audits/post-w7/main-audit-report.md`
- `oteryn-client/docs/audits/post-w7/VALIDATOR_PACKET.md`
- `oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md`
- archived source-audit and remediation-plan task records
- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- `oteryn-client/docs/architecture/TECHNICAL_LOGIN.md`
- `oteryn-client/docs/architecture/SECURITY_MODEL.md`
- `oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md`
- current manifests for Identity, Platform, Game Session and their consumers
- all live open PRs, active tasks and current shared-path leases

FIRST PHASE — BOUNDED DISCOVERY

Before editing implementation, persist an exact allocation and ownership inventory in the task checkpoint. At minimum trace:

- PKCE state and verifier generation, encoding, challenge derivation and browser URL construction;
- callback request bytes, target parsing, query ownership, code/state/error values and rejection paths;
- token-exchange form serialization;
- OAuth and ticket DTO deserialization;
- bearer-header construction and adapter/library ownership;
- Gateway request body and returned credential ownership;
- all debug/display/error/diagnostic boundaries;
- every project-owned copy created by `String`, `Url`, `Vec<u8>`, formatting, parsing, serialization or conversion.

For each allocation classify:

```text
project-owned and zeroed
project-owned but not zeroed
third-party/library-owned
operating-system/process boundary
non-secret
```

Do not claim feasibility until this inventory is complete.

IMPLEMENTATION REQUIREMENTS

Use the smallest coherent design that satisfies all of the following:

1. every project-owned secret intermediate is held by a non-cloneable redacted owner that overwrites its owned bytes on drop;
2. callback code/state parsing does not leave ordinary project-owned sensitive target/query strings after parsing;
3. serde-produced secret strings move immediately into zeroing ownership without an additional project-owned copy;
4. token/ticket/Gateway request serialization uses zeroing project-owned buffers;
5. the ordinary `format!("Bearer {bearer}")` ownership pattern is removed;
6. any unavoidable header, browser argument, URL-library, TLS or operating-system copy is named as a residual external boundary and its project-owned precursor is dropped promptly;
7. errors remain closed, stable and non-secret;
8. OAuth/Gateway request bytes, one-shot semantics and public non-secret outcomes remain compatible;
9. documentation narrows cleanup claims to project-owned best-effort overwrite and separates that from external copies;
10. no password fallback, persistence, logging, diagnostics, retry, async runtime or shutdown-state change is introduced.

Do not implement `OTC2-AUD-002`, `003` or `004` in this task.

PUBLIC CONTRACT CONTROL

`oteryn-platform` is the producer of `SecretString`, sensitive request ownership and `HttpTransport` request boundaries. `oteryn-identity` consumes and composes those contracts. `oteryn-game-session` remains the producer of `GameEntryCredential` if alignment is necessary.

If the remediation requires a material public signature change, record:

- exact producer API;
- every in-repository consumer;
- migration sequence;
- rollback boundary;
- whether a new ADR is required under `oteryn-client/AGENTS.md`.

Do not create substitute adjacent secret types in consumers.

ACCEPTANCE

- no project-owned callback code, state, verifier, token, ticket, credential, sensitive request body or bearer header intermediate remains in an ordinary unzeroed owned string/vector after last use;
- no ordinary formatted bearer string remains;
- secret-facing `Debug`, `Display`, errors and diagnostics remain redacted;
- authorization/browser and third-party copy boundaries are documented accurately;
- existing strict parsing, cache, redirect, size, timeout, generation and one-shot behavior remains fail closed;
- no complete-memory-erasure claim remains;
- exact changed paths match declared ownership and leases;
- no other remediation finding enters the diff.

FOCUSED TESTS

Add the cheapest deterministic evidence for:

- secret wrappers lacking revealing formatting, cloning and serialization;
- project-owned buffer overwrite at terminal drop where a safe test seam can prove it;
- callback parsing and rejection without retained ordinary secret strings;
- bearer construction without an ordinary formatted string;
- synthetic marker secrets absent from errors, debug output and diagnostics;
- unchanged fake Platform/Gateway success and negative behavior.

Never use real credentials, endpoints, private captures, personal paths or proprietary material.

VALIDATION LADDER

Focused:

```text
cargo test --locked -p oteryn-platform -p oteryn-identity -p oteryn-game-session
cargo test --locked --manifest-path tests/security/auth/Cargo.toml
cargo test --locked --manifest-path tests/integration/technical-login/Cargo.toml
```

Component and heavy:

```text
cargo metadata --locked --format-version 1
cargo fmt --all --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --all-targets --locked
cargo run --locked -p oteryn-architecture-check -- workspace .
```

If dependency policy changes, also run the current cargo-deny command and require `Rust Client / Supply Chain` without weakening policy.

Final exact-head requirements:

- `Rust Client / Windows` passed;
- `Rust Client / Supply Chain` passed;
- repository `CI / Required` passed;
- complete changed-file and full-diff review passed;
- no unresolved review threads or requested changes;
- branch current with required `main` and all declared consumers compile/test against the final producer API.

DURABLE CHECKPOINT

Maintain one checkpoint in the task with:

- exact base/head/branch/PR;
- allocation/ownership inventory;
- public API decision;
- shared lease state;
- proven tests and CI run IDs;
- residual external-copy boundaries;
- conflicts/blockers;
- exactly one `next_action`.

STOP CONDITIONS

Stop and checkpoint when:

- a live task/PR owns an affected source, contract or required shared path;
- a material public contract change lacks identified consumers/migration;
- a new dependency is required but not fully reviewed or leased;
- the only proposed result is documentation narrowing without actual project-owned cleanup improvement;
- implementation would claim complete memory erasure;
- implementation would weaken parsing, redaction, architecture, dependency or CI gates;
- another audit finding enters the diff;
- tests require real secrets, private captures or proprietary material.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <implemented secret-lifecycle remediation and truthful claim scope>
VALIDATION: <focused, component and exact-head evidence>
DURABLE_STATE: <task path, branch, head and PR>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <exactly one action>
```
