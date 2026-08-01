---
task_id: OTC2-20260801-playability-p0-coordination
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0
phase: validation
branch: docs/OTC2-20260801-playability-p0-coordination
base_branch: main
created: 2026-08-01T18:55:00+02:00
updated: 2026-08-01T19:04:00+02:00
last_verified_commit: "5e9460844eb5de8663c3cb6f8851ec091c4567b9"
required_base_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
risk: medium
related_pr: 139
depends_on:
  - full-playability programme PR #135 merge 72a45210aafd682d6d9e95c54c1fee55dca46abb
  - programme archive PR #138 merge 17f2a4bf86563609e6f9edb4c71ca40fbbda59b2
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-coordination.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: chat
context_pressure: medium
decomposition_decision: split
validation_level: focused
---

# Goal

Launch the accepted P0 full-playability discovery wave without product implementation by creating five isolated worker tasks, branches and draft PRs with exclusive evidence paths and no shared source-path lease.

# Authorization and scope

This launch task owns only its coordinator checkpoint. It may inspect live Git, tasks, PRs, checks and accepted programme documents. It must not modify Rust, C++, Lua, OTUI, manifests, lockfiles, workflows, producer repositories or P0 worker report paths.

# Dispatch

- Canary capability/fixtures — PR #140, head `5ac490e04d072f16a48d6c5f18b54a094fcabd36`;
- legacy workflows/parity — PR #141, head `d143e031e115e731df9660b578d3ede9587b54c1`;
- asset source/runtime — PR #142, head `0e529d0707f13484956d9a738d8011cace4463a8`;
- Windows UX/input/audio — PR #143, head `e09a52605baadf230ad6c7e181096926c49a8991`;
- staging/E2E/release — PR #144, head `952c3539758e3ef002512ffb84eee79321f04107`.

All five PRs are draft, documentation/evidence-only, start from `main@17f2a4bf86563609e6f9edb4c71ca40fbbda59b2`, own one task plus two exclusive report paths, and hold no shared source-path lease.

# Acceptance

- [x] exact current `main`, plan/archive merges and open PR ownership are verified;
- [x] five unique worker tasks, branches and draft PRs exist;
- [x] every worker owns only its task plus two named report paths;
- [x] no worker receives a shared source-path lease or implementation authorization;
- [x] dispatch state records exact PR numbers and heads;
- [ ] coordinator PR contains only this task path and required CI passes.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T19:04:00+02:00
head: 5e9460844eb5de8663c3cb6f8851ec091c4567b9
branch: docs/OTC2-20260801-playability-p0-coordination
pr: 139
status: validating
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P0_DISCOVERY.md
  - oteryn-client/docs/agents/prompts/PLAYABILITY_COORDINATOR_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-coordination.md
proven:
  - Current main is 17f2a4bf86563609e6f9edb4c71ca40fbbda59b2.
  - Programme PR #135 and lifecycle archive PR #138 are merged.
  - Open PRs #23, #48 and #97 do not overlap any P0 task or report path.
  - Canary PR #140 owns its task plus capability and fixture reports.
  - Legacy PR #141 owns its task plus workflow and scenario reports.
  - Assets PR #142 owns its task plus rights and runtime-roadmap reports.
  - UX PR #143 owns its task plus Windows inventory and UI decomposition reports.
  - Release PR #144 owns its task plus staging/release and performance reports.
derived:
  - The five P0 lanes may investigate independently and merge in any validated order.
  - No shared source-path lease is required for P0.
unknown: []
conflicts: []
first_failure:
  marker: none
  evidence: launch preflight and dispatch are complete.
rejected_hypotheses:
  - Launch gameplay implementation now: rejected because P0 authorizes discovery only.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-coordination.md
validation:
  - command: live main/open PR/path ownership preflight
    result: PASS
    evidence: main 17f2a4bf; PR #23/#48/#97 changed paths are disjoint from all P0 outputs.
  - command: five worker task/branch/draft PR dispatch review
    result: PASS
    evidence: PRs #140-#144 have unique task/report ownership and no shared lease.
blockers: []
next_action: Validate, merge and archive coordinator PR #139, then execute the five independent P0 discovery lanes.
```
