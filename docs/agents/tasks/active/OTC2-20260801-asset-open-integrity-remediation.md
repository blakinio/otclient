---
task_id: OTC2-20260801-asset-open-integrity-remediation
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: asset-security
phase: implementation
branch: fix/OTC2-20260801-asset-open-integrity-remediation
base_branch: main
created: 2026-08-01T14:00:00+02:00
updated: 2026-08-01T14:00:00+02:00
last_verified_commit: "a16c7e7da32bdc96404845341fd72fbdf4db9bc3"
required_base_commit: "a16c7e7da32bdc96404845341fd72fbdf4db9bc3"
risk: high
related_pr: null
depends_on:
  - OTC2-20260801-complete-architecture-policy
  - R4 implementation merge abe0c8c6a96026ba874f3fc58fa84eae3444b699
  - R4 archive merge a16c7e7da32bdc96404845341fd72fbdf4db9bc3
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-asset-open-integrity-remediation.md
  - oteryn-client/tools/asset-compiler/src/lib.rs
  - oteryn-client/tools/asset-compiler/tests/compiler.rs
  - oteryn-client/tools/asset-compiler/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/docs/architecture/decisions/2026-08-01-capability-safe-asset-source-open.md
shared_path_lease:
  - oteryn-client/Cargo.lock
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

# Discovery checkpoint

The pinned standard library exposes safe Windows open flags and handle metadata but no safe handle-relative directory traversal API. Direct Win32/FFI is prohibited.

Reviewed capability solution:

- `cap_std::fs::Dir` is an unforgeable opened-directory capability and resolves relative paths without escaping its directory tree;
- `cap_fs_ext::DirExt::open_dir_nofollow` fails when its single path component names a symlink;
- `cap_fs_ext::OpenOptionsFollowExt` with `FollowSymlinks::No` prevents following the final source component;
- traversing one validated normal component at a time applies no-follow to every intermediate directory;
- final type, size and bytes are obtained from the same opened `cap_std::fs::File` handle;
- the reviewed crates are Bytecode Alliance releases `=4.0.2`, support Windows, use crates.io sources and offer an allowed MIT/Apache licensing alternative;
- no unsafe project code or public CLI contract change is required.

This proves an implementable safe-Rust platform primitive and authorizes implementation. Open PRs #23, #48 and #97 do not touch the owned Rust paths or `Cargo.lock`.

# Acceptance

- manifest directory is acquired once as a directory capability;
- manifest file and every source are opened relative to that capability;
- every intermediate source directory is opened one component at a time with no-follow;
- the final source is opened with no-follow;
- regular-file and size validation use metadata from the opened final handle;
- the same handle supplies all payload bytes;
- deterministic substitution tests prove a post-validation rename cannot redirect the read;
- existing traversal, symlink, special-file, oversize and deterministic-output behavior remains covered;
- no unsafe code, raw Win32/FFI or shared PR #23 documentation path changes.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T14:00:00+02:00
head: a16c7e7da32bdc96404845341fd72fbdf4db9bc3
branch: fix/OTC2-20260801-asset-open-integrity-remediation
pr: null
status: active
proven:
  - Current read_source performs symlink/canonical/metadata validation before File::open and is TOCTOU-vulnerable.
  - Rust std has no safe handle-relative directory traversal API for the required Windows invariant.
  - cap-std/cap-fs-ext 4.0.2 provide capability-relative and no-follow primitives on Windows and Unix.
  - Open PRs have no asset-compiler or Cargo.lock overlap.
derived:
  - One bounded dependency-backed implementation can preserve compile_manifest path API while eliminating the race.
unknown:
  - Exact generated Cargo.lock delta and cargo-deny duplicate-version impact.
conflicts: []
first_failure:
  marker: not-run
  evidence: Implementation has not started.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-asset-open-integrity-remediation.md
validation:
  - command: ownership, overlap and primitive-discovery preflight
    result: PASS
    evidence: main a16c7e7da32bdc96404845341fd72fbdf4db9bc3; reviewed capability APIs; no open PR overlap.
blockers: []
next_action: Open the draft PR, add the pinned capability dependencies and implement exact-handle acquisition tests.
```
