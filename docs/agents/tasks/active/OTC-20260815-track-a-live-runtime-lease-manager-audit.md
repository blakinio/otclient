---
task_id: OTC-20260815-track-a-live-runtime-lease-manager-audit
status: validating
agent: ChatGPT
session_id: null
session_role: fresh-validator
session_rotation_count: 0
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: audit
phase: independent-post-remediation-audit
branch: test/OTC-20260815-track-a-live-runtime-lease-manager-audit
base_branch: main
base_main: f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
risk: medium
related_prs:
  - 312
  - 313
  - 314
created: 2026-08-15T23:31:00+02:00
updated: 2026-08-15T23:31:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-live-runtime-lease-manager-audit.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-live-runtime-lease-manager-audit.md
  - docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager-audit/**
  - .github/workflows/tibia-official-client-re-canonical-live-lease-audit.yml
implementation_authorized: false
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
next_action: attempt to falsify the corrected lease manager on exact main f6fa2264904c6ffb3734d4a63e1edbb29260fcc1 using a separate non-mutating audit harness and source review, then record PASS or material findings without editing manager implementation
---

# Objective

Independently audit the corrected Track A canonical-live lease manager after PR #313, specifically attempting to falsify the concurrency, expiry, fencing, redaction and production-state-isolation guarantees required for closeout.

# Validator boundary

This task is not authorized to modify the manager implementation. If a material defect is found, record it and return the owning implementation task to remediation instead of patching the code from this audit branch.

The audit must not touch a Tibia client process, production canonical state, PR #303/#309 runtime-owned paths/processes or Track B.

# Audit inventory

- [ ] exact audited main commit is `f6fa2264904c6ffb3734d4a63e1edbb29260fcc1`;
- [ ] corrected source contains post-lock time validation for every time-sensitive operation;
- [ ] guard child retains serialization if guard parent terminates;
- [ ] concurrent acquisition cannot create two controllers;
- [ ] stale takeover requires explicit reason and generation fencing;
- [ ] stale/expired credentials cannot renew/validate/release;
- [ ] status output does not expose capability token/digest;
- [ ] state/token modes remain restrictive;
- [ ] corruption fails closed;
- [ ] audit uses only temporary isolated state and does not create/mutate production canonical state;
- [ ] material findings are zero before PASS.
