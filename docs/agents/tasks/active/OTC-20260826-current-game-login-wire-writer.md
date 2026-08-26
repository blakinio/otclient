---
task_id: OTC-20260826-current-game-login-wire-writer
status: investigating
agent: ChatGPT
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260826-current-game-login-wire-writer
base_branch: main
base_main: 8085b40698d409bbacba3460001e8ddca4f6c84f
created: 2026-08-26T17:12:00+02:00
updated: 2026-08-26T18:05:00+02:00
risk: high
execution_mode: github_actions_hosted
execution_reason: current-build static protocol reconstruction is deterministic/disposable P2 work
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
policy_version: 2
session_id: chatgpt-20260826-current-login-wire-writer
session_role: implementer
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one sequential current-build queue-to-TCP writer proof with one evidence output
validation_level: focused
invocation_started_at: 2026-08-26T17:11:00+02:00
last_progress_at: 2026-08-26T17:12:00+02:00
heavy_validation_runs: 0
repair_cycles_for_current_gate: 0
identical_failure_retries: 0
context_reconstruction_attempts: 0
stall_warnings: 0
ci_checks_for_current_head: 0
unchanged_state_checks: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml
  - tools/tibia_re_current_game_login_wire_writer/**
  - docs/agents/evidence/OTC-20260826-current-game-login-wire-writer/**
  - docs/agents/tasks/active/OTC-20260826-current-game-login-wire-writer.md
modules_touched:
  - official-client-re
  - protocol-research
reuses:
  - docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/**
  - docs/agents/evidence/OTC-20260813-tibia-global-login-lab/20260826-current-build-encrypted-handoff-game-0x14.md
depends_on:
  - PR #589 historical native game-login structural promotion on trusted main
  - PR #284 Track B current-build structured 0x14 checkpoint as consumer requirement only
blocks:
  - PR #284 next game-login protocol mutation/retry
cross_repo_tasks: []
implementation_authorized: true
---

# Current-build game-login queue/TCP writer proof

Alias family: `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-WIRE-WRITER`.
## Runtime admission

```yaml
track_id: official-client-re
runtime_access: none
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
```

No official-client process/runtime observation, login, credentials, session secret, process-memory access, GUI input, gameplay, network-session capture or client mutation is authorized. Static analysis must run on a disposable GitHub-hosted Linux runner and delete proprietary client bytes before job completion.

## Objective

Revalidate the current official native-Linux Tibia package and recover, for that exact build, the complete outbound game-login path from typed `GameclientMessageLogin` through `TProtocolMessageQueue::sendLogin`, queue/adapter/framing/encryption/checksum/sequencing and the final TCP writer. The result must be precise enough for Track B to compare its `ProtocolGame::sendLoginPacket()` without protocol guessing.
## Acceptance criteria

- [ ] Revalidate current public Linux package version, packed/unpacked SHA-256 and unpacked size through a disposable secret-free producer.
- [ ] Recover current-build `TProtocolMessageQueue` QMeta `sendLogin(GameclientMessageLogin)` case and its first concrete consumer target.
- [ ] Follow that target to the final outbound byte/framing owner and identify the final TCP/socket writer or stop with the exact first unproven boundary.
- [ ] Distinguish protobuf serialization from RSA/encryption, length framing, checksum/sequence and transport write ordering; mark every unproven semantic `UNKNOWN`.
- [ ] Compare the promoted current-build contract against Track B `ProtocolGame::sendLoginPacket()` only structurally; do not modify Track B or execute a game login in this task.
- [ ] Publish only sanitized addresses/control-flow/schema evidence; never upload the proprietary client binary or raw packet/session material.
- [ ] Focused static validators, governance, diff check and exact-head CI pass before promotion.
- [ ] Fresh independent evidence audit has zero material findings before merge.

## Seed evidence, not current proof

Track B observed candidate public build `15.32.75d4a0`, unpacked SHA `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, size `52105824`. These values are discovery input only until independently revalidated by this task's secret-free producer.

Historical trusted-main PR #589 proves the same conceptual queue boundary only for `15.32.df7b29 / e6c244...`, ending at queue adapter `0xbd36a0`; historical addresses must not be reused as current addresses.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-26T17:15:00+02:00
head: 8085b40698d409bbacba3460001e8ddca4f6c84f
branch: research/OTC-20260826-current-game-login-wire-writer
pr: null
status: investigating
context_routes:
  - official-client-re
  - P2-NETWORK
  - current-build-game-login-wire
owned_paths:
  - .github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml
  - tools/tibia_re_current_game_login_wire_writer/**
  - docs/agents/evidence/OTC-20260826-current-game-login-wire-writer/**
  - docs/agents/tasks/active/OTC-20260826-current-game-login-wire-writer.md
proven:
  - Exact protected main at claim is 8085b40698d409bbacba3460001e8ddca4f6c84f.
  - Fresh branch/open-PR search found no owner for the exact current-build final game-login queue/TCP writer scope.
  - Historical trusted-main evidence ends at the older-build queue adapter and is not current-build writer proof.
derived:
  - The smallest compliant next package is a GitHub-hosted secret-free current-build static producer.
unknown:
  - Current package fence until this task independently revalidates it.
  - Current-build sendLogin QMeta case, consumer target and final TCP writer path.
  - Exact ordering of protobuf serialization, RSA/encryption, framing, checksum/sequencing and transport write.
conflicts:
  - none
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Reuse historical df7b29/bf29ac addresses as current: rejected by exact-build fencing.
  - Retry Track B login before writer proof: rejected by the current structured 0x14 stop rule.
changed_paths:
  - docs/agents/tasks/active/OTC-20260826-current-game-login-wire-writer.md
validation:
  - command: live branch/open-PR ownership search
    result: PASS
    evidence: no exact current-build final game-login wire-writer owner found.
blockers:
  - none
next_action: Commit and publish the task claim as an early Draft PR, then add the hosted current-build static producer.
```
