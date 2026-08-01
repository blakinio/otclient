---
task_id: OTC2-20260801-asset-open-integrity-remediation
status: completed
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: asset-security
phase: archived
branch: fix/OTC2-20260801-asset-open-integrity-remediation
base_branch: main
created: 2026-08-01T14:00:00+02:00
updated: 2026-08-01T14:40:00+02:00
last_verified_commit: "32557716b4455fa7d13094834f20b72ca8470e07"
required_base_commit: "a16c7e7da32bdc96404845341fd72fbdf4db9bc3"
implementation_merge: "beb0bc938c1ac0b5ff901db71ab0ad0592bad7ce"
related_pr: 131
risk: high
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: codex
---

# Result

`OTC2-AUD-003` is remediated and merged through PR #131.

The asset compiler now opens the manifest parent once as a directory capability, traverses every validated source component relative to that capability without following links, validates regular-file type and bounded size from the opened final file handle, and reads all payload bytes from that same handle. No accepted pathname is reopened.

The public `compile_manifest(&Path, &Path)` contract and pack format are unchanged. The implementation contains no project-owned unsafe code or Win32/FFI.

# Durable artifacts

- `oteryn-client/tools/asset-compiler/src/lib.rs`
- `oteryn-client/tools/asset-compiler/tests/source_integrity.rs`
- `oteryn-client/tools/asset-compiler/Cargo.toml`
- `oteryn-client/Cargo.lock`
- `oteryn-client/deny.toml`
- `oteryn-client/docs/architecture/decisions/2026-08-01-capability-safe-asset-source-open.md`
- implementation PR #131
- implementation merge `beb0bc938c1ac0b5ff901db71ab0ad0592bad7ce`

# Security evidence

- A deterministic post-open substitution test proves a later pathname replacement cannot redirect the current read.
- A regular nested-source test proves component-wise capability traversal works.
- An intermediate directory symlink is rejected on Windows CI.
- Existing final-symlink, traversal, special-file, oversize and deterministic-output tests remain active.
- `cap-std` and `cap-fs-ext` are pinned to `=4.0.2`.
- Cargo 1.94.0 generated the lockfile.
- `cargo-deny` remains fail-closed with only exact reviewed license and duplicate-version entries for the capability graph.

# Validation

Exact head `32557716b4455fa7d13094834f20b72ca8470e07`:

- Rust Client run `30699743934` — PASS;
- Windows job `91368541996` — PASS: locked metadata, rustfmt, strict Clippy, complete workspace tests and architecture validation;
- Supply Chain job `91368542008` — PASS;
- CI run `30699744005` — PASS;
- required job `91368653094` — PASS;
- ready-for-review CI run `30699950073` — PASS;
- ready required job `91369208801` — PASS;
- exact changed-file review — seven declared paths only;
- comments, reviews and unresolved threads — none.

# Boundaries

No workflow, shared PR #23 documentation, external repository or unrelated runtime path remains in the implementation diff.

# Remediation programme closure

The accepted post-W7 remediation sequence is complete:

1. `R1-SECRET` — merged and archived;
2. `R2-SHUTDOWN` — merged and archived;
3. `R4-ARCH-POLICY` — merged and archived;
4. `R3-ASSET-OPEN` — merged by PR #131 and archived by this lifecycle change.

# Next action

Run one independent post-remediation audit against current `main` to verify closure of `OTC2-AUD-001` through `OTC2-AUD-004` and detect regressions outside the package-local test suites.
