---
task_id: OTC-20260730-w7-workspace-membership-repair
status: in_progress
agent: "W7 coordinator repair"
track: greenfield-rust
workstream: workspace-governance
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: coordinator-repair
parallel_lane_state: validating
branch: fix/OTC-20260730-w7-workspace-membership-repair
base_branch: main
created: 2026-07-30T21:29:00+02:00
updated: 2026-07-30T21:35:00+02:00
last_verified_commit: "db7476c5e69eeef60824f7458552c1ce8398e153"
required_base_commit: "c85b8427deb66cacc204d01684b6c393edb9c25c"
risk: medium
related_pr: "#108"
owned_paths:
  - docs/agents/tasks/active/OTC-20260730-w7-workspace-membership-repair.md
  - oteryn-client/Cargo.toml
shared_path_lease:
  - oteryn-client/Cargo.toml
contract_role: coordinator-owned repair
contracts_produced: []
contracts_consumed:
  - W7-ENTRY-CONTRACT merge 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - W7-ENTRY-CONTRACT archive merge 8dcd353d5a9f19fabccf49508c27074f7749e3cf
blockers: []
---

# Goal

Repair the Rust workspace membership regression discovered after W7-ENTRY-CONTRACT merged and archived.

# First failure

Current `main` omits the direct workspace members:

- `crates/account-session`;
- `crates/world-directory`;
- `tools/asset-compiler`.

`crates/game-session` remains present and reaches the first two crates only through path dependencies. This means workspace-wide gates do not directly enumerate every produced W7 crate and no longer enumerate the merged W6 asset compiler.

# Scope

- restore `tools/asset-compiler`;
- register `crates/account-session` and `crates/world-directory` as direct workspace members;
- preserve `crates/game-session` and every existing member;
- make no Rust source, dependency, lockfile, workflow, protocol or compatibility change.

# Acceptance criteria

- [ ] `cargo metadata --locked` includes all three W7 contract crates and the W6 asset compiler as workspace members;
- [ ] locked formatting, strict Clippy, all workspace tests/doctests, architecture policy and cargo-deny pass;
- [ ] full two-path diff review passes;
- [ ] merge before launching W7-IDENTITY or W7-CANARY-ENTRY.
