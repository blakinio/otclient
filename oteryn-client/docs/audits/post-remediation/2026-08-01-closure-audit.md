# Post-remediation closure audit

Task: `OTC2-20260801-post-remediation-closure-audit`  
Evidence cut: `main@67a6c9d726f7e70977803b028270475570210db0`  
Scope: independent verification of `OTC2-AUD-001` through `OTC2-AUD-004`  
Implementation changes: **none authorized or performed**  
Status: **VALIDATED_WITH_ONE_RESIDUAL**

## Executive summary

The accepted post-W7 remediation programme materially corrected all four original medium-severity defects. Direct current-source review and fresh full-workspace CI independently confirm that:

- the event-loop shutdown path is nonblocking and retains worker ownership;
- asset source acceptance, metadata and reads are bound to one opened file object;
- architecture dependency enforcement is a complete closed allow policy across normal, build and dev edges;
- ordinary OAuth callback/query, serde secret and bearer-header intermediates in the active Identity/Platform flow now use bounded redacted owners and the documentation no longer claims complete process-memory erasure.

Three original findings are fully closed. `OTC2-AUD-001` is **partially closed** because two public project-owned input surfaces remain outside its literal accepted invariant: the mutable public `CallbackAttempt.target: String` can be cleared, taken or replaced before the owner's `Drop`, and an oversized direct `GameEntryCredential::new(Vec<u8>, ...)` input is rejected without explicitly clearing that input allocation. Neither path is exercised by the current internal technical-login flow, so the remaining issue is assessed as a focused **LOW** residual rather than the original broad **MEDIUM** conflict.

No `CRITICAL`, `HIGH` or new `MEDIUM` defect was found. Closing these findings does not change the existing production-readiness verdict: deployed Identity/Gateway compatibility, real Canary admission, interactive Windows behavior, real GPU/hardware, production assets, legal approval, performance and gameplay remain outside the evidence.

## Method

The audit compared the original post-W7 report and accepted remediation plan with current source, tests, accepted architecture decisions, manifests, lockfile, supply-chain policy, live pull-request state and fresh CI. Archived task records were treated as supporting evidence only.

For each finding the review asked:

1. whether the original vulnerable or incomplete mechanism still exists;
2. whether the accepted replacement invariant is enforced by current source rather than documentation alone;
3. whether focused regression tests exercise the security/lifecycle property;
4. whether later merges changed the remediated production paths;
5. whether fresh current-main validation still passes.

## Closure matrix

| Finding | Current verdict | Independent basis |
|---|---|---|
| `OTC2-AUD-001` secret lifecycle | **PARTIALLY_CLOSED** | active Identity/Platform flow and claims corrected; one mutable public callback target and rejected direct credential input remain outside the literal project-owned overwrite invariant |
| `OTC2-AUD-002` nonblocking shutdown | **CLOSED** | event-loop uses `begin_shutdown`/`poll_shutdown`; unfinished handles are retained and joined only after `is_finished`; bounded I/O configuration is enforced |
| `OTC2-AUD-003` opened-object integrity | **CLOSED** | capability-relative no-follow traversal; type, size and bytes use the same opened final handle; deterministic pathname-substitution test passes |
| `OTC2-AUD-004` complete architecture policy | **CLOSED** | closed 29-category allow policy retains dependency kind and is exhaustively checked for `29 x 29 x 3 = 2523` combinations |

## `OTC2-AUD-001` — secret lifecycle and claim correction

### Corrected behavior

Current Identity and Platform code removes the original ordinary formatted bearer `String`, moves callback state/code and serde-produced token/ticket/credential values into non-cloneable redacted owners, clears bounded project-owned buffers on terminal drop and keeps errors secret-free. The browser/URL, HTTP/TLS, allocator and operating-system boundaries are explicitly described as residual copies rather than claimed as erased.

`GameEntryCredential` and `AdmissionCredential` remain non-cloneable and redacted, and their accepted `SecretBytes` owner clears its current boxed byte slice on drop. The current Gateway producer first enforces the same 4 KiB secret bound and then moves the credential into this owner.

### Remaining acceptance gap — `OTC2-POST-001`

ID: `OTC2-POST-001`  
TITLE: Public callback mutation and rejected direct credential input can bypass complete project-owned overwrite coverage  
SEVERITY: **LOW**  
CONFIDENCE: **HIGH**  
AFFECTED_PATHS: `crates/identity/src/lib.rs`; `crates/game-session/src/lib.rs`

`CallbackAttempt` is non-cloneable and has a redacted `Debug`, but its security-sensitive target remains a public ordinary `String`. The drop implementation takes and clears only the target's state at terminal drop. A caller with mutable access can call `clear`, `take`, `replace` or directly assign the public field first; the original query allocation or bytes beyond the new logical length are then no longer guaranteed to be covered by the owner's explicit fill.

`SecretBytes::new(secret: Vec<u8>)` in game-session returns `TooLarge` without explicitly clearing the rejected vector. The normal Gateway path cannot produce this oversized value because its upstream secret owner enforces the same maximum, but the public constructor itself remains outside the plan's literal requirement that every project-controlled secret allocation receive explicit ownership and terminal best-effort overwrite.

Recommended disposition:

- make the callback target private behind a read-only bounded accessor or store it in a dedicated private zeroing owner;
- preserve fake/receiver construction through `CallbackAttempt::new`;
- explicitly clear rejected non-empty credential vectors before returning validation errors;
- add regression tests for the public API shape and rejected-input cleanup seam;
- do not expand the claim beyond best-effort project-owned bytes.

### Verdict

The original broad MEDIUM issue is materially mitigated and the active technical-login path no longer contains the reported ordinary bearer/query copies. Full R1 acceptance is not yet proven because `OTC2-POST-001` remains. Verdict: **PARTIALLY_CLOSED**.

## `OTC2-AUD-002` — nonblocking shutdown

The Windows shell starts shutdown without joining. It polls typed `Pending`, `Overdue` and `Complete` progress from worker-completion events and a 16 ms fallback. Renderer/window release and `event_loop.exit()` occur only after `Complete` on the normal shell-controlled exit path.

The runtime retains each `JoinHandle`, requests cancellation and checks `is_finished()` before joining during shutdown polling. `Overdue` after 31 seconds is diagnostic only and does not detach, abandon or force-terminate a worker. New work is rejected after shutdown starts. Public TCP connect/read/write configuration rejects values above 30 seconds; the HTTP maximum remains 30 seconds and callback cancellation remains observable through bounded read slices.

A gate-controlled test proves `Pending -> Overdue -> Complete`, retention while overdue, rejection of new work and eventual joined/logged-out completion. No app-runtime, client shell, technical-login or transport source changed after the R2 implementation merge.

Residual boundary: runtime `Drop` remains a potentially blocking ownership fallback for misuse outside the normal event-loop lifecycle. The accepted ADR names this boundary; the shell-controlled path reaches drop only after no worker remains.

Verdict: **CLOSED**.

## `OTC2-AUD-003` — asset opened-object integrity

The compiler opens the manifest parent once as a `cap_std::fs::Dir`, opens the manifest relative to that capability without following the final link, validates source paths as non-empty normal relative components, opens every intermediate directory separately with `open_dir_nofollow`, and opens the final component with `FollowSymlinks::No`.

Regular-file type, initial size and all payload bytes use the same opened `CapabilityFile`. A bounded `take(limit + 1)` read also detects growth beyond the accepted maximum. Path metadata is consulted only after an open failure to preserve stable error classification; it does not establish acceptance.

A deterministic unit test opens the accepted object, renames its pathname and writes different bytes under the original name before the read. The compiler still returns the original opened object's bytes. Integration tests cover normal nested directories and reject an intermediate directory symlink when the host permits symlink creation. `cap-std` and `cap-fs-ext` are pinned to `=4.0.2`, and fresh cargo-deny validation passes. No source or dependency-policy file changed after the R3 implementation merge; the only later change was lifecycle archiving.

Residual boundary: the invariant prevents pathname redirection, not concurrent in-place mutation by another writer already holding access to the same underlying object. The accepted ADR states this accurately.

Verdict: **CLOSED**.

## `OTC2-AUD-004` — complete architecture policy

The checker retains a closed catalogue of 29 categories and a typed `DependencyKind` for `normal`, `build` and `dev`. Unknown categories fail closed. Normal edges use source-category allowlists, product-to-tool normal edges are denied, dev edges may target tool explicitly, and build edges are denied except the exact listed pairs `tool -> foundation` and `tool -> asset-types`.

Cargo metadata dependency kinds and fixture schema-v2 kinds are parsed into the same graph. Schema v1 remains readable with missing kind interpreted as normal. All dependency kinds remain subject to source/path validation and cycle detection. The stable violation code remains `E005_FORBIDDEN_EDGE`.

The exhaustive test constructs and parses every `29 x 29 x 3 = 2523` category/kind combination, compares the public decision with actual fixture enforcement and proves each kind has both allowed and denied edges. Dedicated tests cover dev-only tool access, explicit build pairs and required schema-v2 kinds. The unchanged real workspace passes the current architecture command. No architecture-check source changed after the R4 implementation merge.

Residual boundary: the gate proves declared category/kind edge policy, not semantic correctness of code inside an allowed edge or production readiness.

Verdict: **CLOSED**.

## Fresh current-main validation

Audit source-validation head `7db8b868b815296a2e97fc6edf7518ac69da2f5e` was based directly on `main@67a6c9d726f7e70977803b028270475570210db0` and changed only the audit task/report scaffold.

Rust Client run `30701844955`:

- Windows job `91374101355` — PASS;
- pinned Rust/Cargo 1.94.0 installation — PASS;
- `cargo metadata --locked --format-version 1` — PASS;
- `cargo fmt --all --check` — PASS;
- `cargo clippy --workspace --all-targets --locked -- -D warnings` — PASS;
- `cargo test --workspace --all-targets --locked` — PASS;
- `cargo run --locked -p oteryn-architecture-check -- workspace .` — PASS;
- Supply Chain job `91374101337` — PASS for advisories, licenses, bans and sources with cargo-deny `--all-features`;
- auxiliary `luacheck` and `cppcheck` jobs — PASS.

Repository CI run `30701845062`:

- scope detection — PASS;
- Lua syntax — PASS;
- YAML/workflow/XML validation — PASS;
- informational static analysis — PASS;
- `CI / Required` job `91374318993` — PASS.

Final documentation-evidence head `48b6bc1beab9ecca9a348c654e1201daedabeebb` also passed:

- Rust Client run `30702367732`;
- Windows job `91375505764` — PASS for locked metadata, rustfmt, strict Clippy, full workspace tests and real-workspace architecture validation;
- Supply Chain job `91375505751` — PASS;
- repository CI run `30702367776` — PASS;
- `CI / Required` job `91375624461` — PASS;
- exact changed-file review — the audit task and report only;
- comments, review submissions and unresolved review threads — none.

The Rust workflow does not pass `--all-features` to Clippy or workspace tests; this report therefore claims the exact current required ladder only. Cargo-deny does run with `--all-features`.

The evidence-append commit changes this report only and must retain green status gates before merge.

## Live PR and ownership review

Open PRs during this audit:

- #23 — draft and currently not mergeable; UI/Lua scope plus shared governance files. It does not touch the two audit paths or Rust remediation sources, but it must rebase and preserve the current truthful R1 catalogue/changelog wording before any future merge.
- #48 — Linux runner analysis workflow/task; no audit or remediated Rust-source overlap.
- #97 — client-assets release rehearsal; no audit or remediated Rust-source overlap.
- #133 — this isolated audit.

No active task or open PR owns either audit path. The implementation diff remains documentation-only.

## Unrelated and deferred observations

- Original LOW governance/evidence findings `OTC2-AUD-005` and `OTC2-AUD-006` were not reopened or reassessed by this four-finding closure package.
- No deployed endpoint, private credential, proprietary capture, interactive desktop, real GPU/driver, real asset-signing, legal, fuzz, soak, performance or gameplay evidence was introduced.
- The current synthetic technical-login and production Canary fail-closed boundaries remain unchanged.

## Final verdict

**VALIDATED_WITH_ONE_RESIDUAL**

`OTC2-AUD-002`, `OTC2-AUD-003` and `OTC2-AUD-004` are independently closed on current `main`. `OTC2-AUD-001` is materially corrected but remains partially closed until `OTC2-POST-001` makes the callback target non-mutable from outside its secret owner and clears rejected direct credential input.

No new implementation defect above LOW severity was found. The next remediation should be one isolated, standard-library-only R1 follow-up; it must not modify shutdown, architecture-policy, asset-open, workflow, lockfile or unrelated UI paths.
