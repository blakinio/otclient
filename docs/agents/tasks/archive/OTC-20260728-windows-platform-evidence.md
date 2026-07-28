---
task_id: OTC-20260728-windows-platform-evidence
status: completed
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R02
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-PR
parallel_lane_state: archived
branch: docs/OTC-20260728-windows-platform-evidence
base_branch: main
created: 2026-07-28T23:58:00+02:00
updated: 2026-07-29T00:12:00+02:00
last_verified_commit: "eecab3c52cfb0ee5b868d3ffc7f3e500bc59bc78"
required_base_commit: "048414f9457f6adaf6c3f94f8a8e6b92d624389d"
risk: low
related_pr: "#67"
depends_on:
  - merged foundation audit PR #47
  - merged diagnostics PR #61
blocks: []
owned_paths:
  - oteryn-client/docs/research/windows-platform/**
  - docs/agents/tasks/archive/OTC-20260728-windows-platform-evidence.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - accepted Windows-first architecture
  - merged foundation and diagnostics contracts
crates_touched: []
features_touched: []
contracts_touched:
  - evidence only; no accepted platform API
modules_touched: []
reuses:
  - foundation platform/hardware audit
  - official winit/raw-window-handle documentation
  - Microsoft Win32 DPI/input/IME/lifecycle documentation
public_interfaces:
  - documentation evidence only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no native code, unsafe, FFI, secrets or private captures
---

# Goal

Evaluate current primary Windows window/event/DPI/IME/raw-input/shutdown evidence and Rust dependency candidates, then recommend one bounded Windows application-shell spike without adding code, dependencies, workflows or architecture changes.

# Result

Merged PR #67 delivered five evidence files under `oteryn-client/docs/research/windows-platform/`:

- `README.md` with findings, boundaries and primary references;
- `WINDOW_AND_EVENT_REQUIREMENTS.md` for lifecycle, DPI, IME and input;
- `DEPENDENCY_EVALUATION.md` for winit/raw-window-handle/direct-Win32 roles;
- `THREAD_AND_SHUTDOWN_MODEL.md` for main-thread ownership and orderly exit;
- `SPIKE_RECOMMENDATION.md` for one bounded winit-only blank-window shell.

# Material findings

- main thread owns the event loop, window creation, DPI/IME policy and shutdown coordination;
- `winit 0.30.13` is the recommended spike candidate, not an accepted production dependency;
- `raw-window-handle 0.6.2` remains interop-only unless a renderer boundary needs it;
- direct Win32 bindings require a separately proven gap and focused unsafe/FFI review;
- Raw Input registration must be application-owned;
- exact minimum Windows version and DPI/IME/device compatibility remain blocked on named runtime evidence.

# Validation and merge

| Evidence | Result |
|---|---|
| exact six-file/full-content review on `eecab3c52cfb0ee5b868d3ffc7f3e500bc59bc78` | PASS |
| Rust Client run `30402995977` | PASS: Windows and Supply Chain |
| repository CI run `30402995998` | PASS: all required jobs and `CI / Required` |
| ready-for-review CI run `30403099742` | PASS: all emitted required jobs; legacy Windows build skipped correctly |
| comments/reviews/unresolved threads | none |
| base before merge | unchanged at `048414f9457f6adaf6c3f94f8a8e6b92d624389d` |
| squash merge | `e7d9b5d5feb53debd79c4bdc82da16ca672217c5` |

# Boundaries preserved

- no Cargo, lockfile, platform/app crate, workflow or architecture change;
- no native code, unsafe, FFI, renderer, protocol, assets, UI or async runtime;
- no Windows release, hardware, DPI, IME, device or performance compatibility claim.

# Next action

A future WS-R02 task should implement only the recommended blank-window application shell after a fresh shared-path/dependency preflight and must retain unavailable runtime matrix cases as blockers.

# Completion

- Final status: completed
- PR: #67
- Merge commit: `e7d9b5d5feb53debd79c4bdc82da16ca672217c5`
- Archived at: `docs/agents/tasks/archive/OTC-20260728-windows-platform-evidence.md`
