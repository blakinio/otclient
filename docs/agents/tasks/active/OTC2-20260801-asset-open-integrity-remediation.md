---
task_id: OTC2-20260801-asset-open-integrity-remediation
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: asset-security
phase: validation
branch: fix/OTC2-20260801-asset-open-integrity-remediation
base_branch: main
created: 2026-08-01T14:00:00+02:00
updated: 2026-08-01T14:25:00+02:00
last_verified_commit: "1ec63633921da994ae6e99a9dc88e88cba92961b"
required_base_commit: "a16c7e7da32bdc96404845341fd72fbdf4db9bc3"
risk: high
related_pr: 131
depends_on:
  - OTC2-20260801-complete-architecture-policy
  - R4 implementation merge abe0c8c6a96026ba874f3fc58fa84eae3444b699
  - R4 archive merge a16c7e7da32bdc96404845341fd72fbdf4db9bc3
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-asset-open-integrity-remediation.md
  - oteryn-client/tools/asset-compiler/src/lib.rs
  - oteryn-client/tools/asset-compiler/tests/compiler.rs
  - oteryn-client/tools/asset-compiler/tests/source_integrity.rs
  - oteryn-client/tools/asset-compiler/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - oteryn-client/docs/architecture/decisions/2026-08-01-capability-safe-asset-source-open.md
shared_path_lease:
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
modules_touched:
  - Rust asset compiler source acquisition
crates_touched:
  - oteryn-asset-compiler
features_touched:
  - capability-relative source opening
  - no-follow component traversal
reuses:
  - current portable source-path validation
  - current stable CompilerError surface
  - cap-std 4.0.2 directory capabilities
  - cap-fs-ext 4.0.2 no-follow extensions
contracts_produced:
  - exact opened-object source-read invariant
contracts_consumed:
  - manifest-relative source paths
contracts_touched:
  - asset compiler source trust boundary
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: codex
---

# Goal

Remediate `OTC2-AUD-003` so every source payload is validated and read from the same opened regular-file object, with no pathname validation/open race.

# Implemented contract

- The manifest parent is opened once as a `cap_std::fs::Dir` capability.
- The manifest file is opened relative to that capability without following the final link.
- Every validated normal source component is traversed relative to the capability.
- Every intermediate directory uses `open_dir_nofollow` one component at a time.
- The final file uses `FollowSymlinks::No`.
- Type, size and bytes use the same opened final file object.
- Path metadata after an open failure is used only for stable error classification.
- The public `compile_manifest(&Path, &Path)` and pack format are unchanged.
- No project unsafe code, Win32/FFI, workflow or shared PR #23 documentation path remains in the diff.

# Dependency review

`cap-std` and `cap-fs-ext` are pinned to `=4.0.2`. Cargo 1.94.0 generated the lockfile. `cargo-deny` remains fail-closed and records only the exact reviewed capability-graph license and duplicate-version exceptions in `deny.toml`.

# Evidence

- Deterministic post-open substitution test: replacing the pathname after acquisition cannot redirect the current read.
- Regular nested source integration test.
- Intermediate directory symlink rejection integration test when the host permits symlink creation.
- Existing traversal, final-symlink, special-file, oversize and deterministic-output tests remain active.
- Decision record: `oteryn-client/docs/architecture/decisions/2026-08-01-capability-safe-asset-source-open.md`.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T14:25:00+02:00
head: aebfde2fcf9fd4ec3a563a135b4cc986c98af3c9
branch: fix/OTC2-20260801-asset-open-integrity-remediation
pr: 131
status: active
proven:
  - Previous read_source used metadata and canonicalization before a later ambient File::open.
  - Rust std has no safe handle-relative Windows traversal API for this invariant.
  - cap-std/cap-fs-ext 4.0.2 provide the required safe capability and no-follow primitives.
  - Every accepted source is now validated and read from one opened final file object.
  - Source head 1ec63633921da994ae6e99a9dc88e88cba92961b passed locked metadata, rustfmt, strict Clippy, full workspace tests, architecture validation and Supply Chain.
  - Rust Client run 30699475876 passed; Windows job 91367798935 passed; Supply Chain job 91367798976 passed.
  - Open PRs have no asset-compiler, Cargo.lock or deny.toml overlap.
derived:
  - The pathname substitution window reported by OTC2-AUD-003 is closed for manifest source acquisition.
unknown:
  - Final exact-head CI result after adding the intermediate-component test and ADR.
conflicts: []
first_failure:
  marker: resolved
  evidence: Initial rustfmt and cargo-deny failures were corrected with exact formatting and reviewed policy entries.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-asset-open-integrity-remediation.md
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - oteryn-client/docs/architecture/decisions/2026-08-01-capability-safe-asset-source-open.md
  - oteryn-client/tools/asset-compiler/Cargo.toml
  - oteryn-client/tools/asset-compiler/src/lib.rs
  - oteryn-client/tools/asset-compiler/tests/source_integrity.rs
validation:
  - command: cargo metadata --locked --format-version 1
    result: PASS
    evidence: Windows job 91367798935.
  - command: cargo fmt --all --check
    result: PASS
    evidence: Windows job 91367798935.
  - command: cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
    result: PASS
    evidence: Windows job 91367798935.
  - command: cargo test --workspace --all-targets --all-features --locked
    result: PASS
    evidence: Windows job 91367798935.
  - command: cargo deny check --all-features
    result: PASS
    evidence: Supply Chain job 91367798976.
blockers: []
next_action: Run exact-head validation, review and merge PR #131.
```
