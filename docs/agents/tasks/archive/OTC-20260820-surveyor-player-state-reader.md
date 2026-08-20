---
task_id: OTC-20260820-surveyor-player-state-reader
status: completed
phase: archived
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
runtime_access: read_only
runtime_owner_task: OTC-20260820-surveyor-player-state-reader
runtime_namespace: otclient-track-a-kasmvnc/display-1
target_uniqueness: PROVEN
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
implementation_pr: 634
closeout_pr: 635
physical_e2e_required: true
physical_e2e_result: PASS
---

# Surveyor v2 P0 player-state typed reader — completed

The original PR #634 reader correctly identified a live `TPlayerData` object but incorrectly interpreted `+0x78/+0x7c/+0x80` as player XYZ. The required post-merge causal test rejected that interpretation because it remained `(0,0,2520)` across owner movement.

PR #635 repaired the reader using the exact-current-build `tibia::cyclopedia::TCyclopediaMapStorage` position-update path. Static analysis resolves vptr `0x30c2738`, typeinfo `0x30c0aa0`, qt-metacast `0xd1eef0`, and `onPlayerPositionWasUpdated` handler `0xd19ef0`. Runtime reads require agreement between primary `+0x2f0/+0x2f4/+0x2f8` and mirror `+0x408/+0x40c/+0x410` copies and fail closed on mismatch or implausible coordinates.

Final physical read-only causal E2E on the same exact client fence changed from `(32547,32501,7)` to `(32547,32496,7)` after one owner-performed five-tile movement: delta `(0,-5,0)`. PID `19590`, start ticks `76611792`, executable size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, target uniqueness, and mirror consistency remained stable.

Validation: 32 focused tests PASS; compile validation PASS; `git diff --check` PASS; exact-current ELF static resolver PASS; CI run `32414943288` PASS; Track A governance run `32414942936` PASS.

Canonical evidence: `docs/agents/evidence/OTC-20260820-surveyor-player-state-reader/20260820-live-causal-e2e.md`.
