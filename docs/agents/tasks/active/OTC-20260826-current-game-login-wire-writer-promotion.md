---
task_id: OTC-20260826-current-game-login-wire-writer-promotion
status: investigating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: audit
branch: docs/OTC-20260826-current-game-login-wire-writer-promotion
base_branch: main
base_main: c9525b8c9fb98b61f8fcd57ccd32f4bd873a800c
created: 2026-08-26T20:48:00+02:00
updated: 2026-08-26T20:48:00+02:00
risk: medium
execution_mode: github_only
execution_reason: coordinator audit and docs-only promotion of sanitized exact-current static evidence
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
owner_funded_ai_api_authorized: false
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
policy_version: 2
session_role_detail: independent_coordinator_validator
validation_level: focused
owned_paths:
  - docs/agents/evidence/OTC-20260826-current-game-login-wire-writer-promotion/**
  - docs/agents/tasks/active/OTC-20260826-current-game-login-wire-writer-promotion.md
  - docs/agents/tasks/archive/OTC-20260826-current-game-login-wire-writer.md
modules_touched: []
reuses:
  - PR #699 exact-current source research
  - PR #284 structured current-build 0x14 consumer checkpoint
depends_on:
  - source PR #699 frozen researcher evidence
blocks:
  - PR #284 next bounded login-payload repair
cross_repo_tasks: []
implementation_authorized: true
---

# Coordinator promotion — current game-login wire writer

## Objective

Independently falsify source PR #699 from its exact primary artifact and exact source diff, then promote only current-build facts that survive review. Do not merge the researcher workflow/analyzer and do not execute or mutate any official/Track-B runtime.

## Audit inputs

```text
source PR          #699
source code head   3d87d729b73f868aefe1662c72af666a4921b1d8
source freeze head 7de745105ce06271ff45bcdf5e5eaf91268008e5
producer run       32998976901
artifact           9617908322
digest             sha256:a43ed724d00e18575d969859ad3345d69f2650ee5790d3dbcf13767de1b9ebf4
source CI          32998977749 = SUCCESS
source governance  32998976855 = SUCCESS
freeze CI          33001390982 = SUCCESS
freeze governance  33001390364 = SUCCESS
```

The coordinator re-downloaded artifact `9617908322`; ZIP SHA-256 independently equals the GitHub artifact digest above. The contained sanitized `result.json` SHA-256 is `022a58f738b6586e9143f9e558cb19e89e4fdeb83cd4624a5c7a5cb9dbceddd7`.

## Required review

- [ ] Independently verify exact client fence and safety markers from primary artifact.
- [ ] Falsify `sendLogin` QMeta case -> adapter -> queue vslot `+0x68` current-build chain.
- [ ] Falsify current padding/XTEA and sequence dataflow.
- [ ] Falsify unique final framing serializer and `QDataStream::writeRawData` boundary.
- [ ] Falsify current Qt/QTcpSocket construction graph without claiming the OS syscall.
- [ ] Compare current native outer transport structurally with Track B code and reject unsupported framing guesses.
- [ ] Preserve queue asynchronous-drain and exact current generated login-message field schema as `UNKNOWN`.
- [ ] Review complete source PR diff and ensure no proprietary client, secrets or Track B mutation is promoted.
- [ ] Exact promotion-head CI/governance pass and review threads are zero before merge.

## E2E

`NOT_APPLICABLE` — coordinator promotion is static docs/evidence integration only; no client or network behavior is changed.

## Context checkpoint

```yaml
checkpoint_version: 1
status: investigating
phase: audit
source_pr: 699
source_artifact: 9617908322
source_artifact_digest_match: PASS
material_findings_open: UNKNOWN
next_action: independently validate source artifact claims and publish a bounded promotion report or reject the source with exact finding IDs.
```
