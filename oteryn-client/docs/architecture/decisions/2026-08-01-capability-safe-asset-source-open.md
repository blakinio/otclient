# Capability-safe asset source opening

- Status: Accepted
- Date: 2026-08-01
- Finding: `OTC2-AUD-003`
- Scope: offline `oteryn-asset-compiler` source acquisition

## Context

The previous compiler validated a source pathname with link metadata, canonicalization and regular-file metadata, then later called ambient `File::open` on that pathname. A rename, symbolic-link or reparse substitution between validation and open could therefore redirect the bytes read by the compiler. Repeating pathname metadata checks would only move the race.

The workspace prohibits project-owned unsafe Win32/FFI. Rust 1.94 exposes safe Windows file flags and opened-handle metadata, but it does not expose a safe standard-library API for traversing a relative path from an already opened directory handle while refusing links for every component.

## Decision

The asset compiler pins `cap-std = 4.0.2` and `cap-fs-ext = 4.0.2` and uses their capability filesystem APIs.

1. The manifest parent is opened once as a `cap_std::fs::Dir` capability.
2. The manifest file is opened relative to that capability with `FollowSymlinks::No`.
3. Manifest source paths retain the existing portable validation: only non-empty normal relative components are accepted.
4. Each intermediate component is opened separately with `DirExt::open_dir_nofollow`.
5. The final component is opened with capability `OpenOptions` and `FollowSymlinks::No`.
6. Regular-file type and byte-size limits are checked using metadata from that opened final file handle.
7. Payload bytes are read from the same handle. No accepted pathname is reopened.
8. Path metadata after an open failure is used only to preserve stable error classification; it never establishes acceptance.

The public `compile_manifest(&Path, &Path)` contract and output format remain unchanged.

## Security invariant

For every manifest source, containment and link policy select one opened file object. Type, size and payload checks then operate on that same object. Replacing the pathname after acquisition either fails because of platform sharing rules or changes only future name resolution; it cannot redirect the current read.

This decision protects against pathname substitution through rename, symbolic-link and reparse traversal. It does not claim immutable file contents against a separate writer that already holds write access to the same underlying object; trusted input production must still avoid concurrent in-place mutation.

## Evidence

- A deterministic hook replaces the source pathname after final open and before read. The compiler still returns the originally opened object's bytes.
- A cross-platform integration test proves ordinary nested directories work.
- A cross-platform integration test proves an intermediate directory symlink is rejected when the host permits symlink creation.
- Existing final-symlink, special-file, traversal, outside-root, oversize and deterministic-output tests remain active.
- Windows CI validates the pinned implementation on `x86_64-pc-windows-msvc`.

## Dependency and supply-chain review

The selected Bytecode Alliance crates are pinned to `4.0.2` from crates.io. The generated lockfile is produced with Cargo 1.94.0. `cargo-deny` remains fail-closed; the reviewed dependency graph requires:

- the SPDX expression `Apache-2.0 WITH LLVM-exception` through `winx`;
- `io-lifetimes 2.0.4` beside 3.0.1;
- Windows binding versions 0.59, 0.60 and 0.61 beside the existing 0.52 graph;
- `windows-targets` and `windows_x86_64_msvc` 0.53 beside 0.52.

Only those exact transitive versions are listed in `deny.toml`; wildcard, advisory and source policy are unchanged.

## Consequences

The compiler gains a reviewed capability dependency graph and lockfile delta. Source acquisition no longer depends on ambient re-resolution after validation. Rollback is one revert covering the asset compiler source path, its pinned dependencies, lockfile and this decision record.
