---
task_id: OTC-20260829-field6-independent-clean-runner
status: validating
agent: ChatGPT
session_id: chatgpt-20260829-independent-clean-runner
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: infrastructure_security
phase: validate
branch: fix/OTC-20260829-field6-independent-clean-runner
base_branch: main
base_main: d05744b746b33c979b85ba25442ffab7298ba786
created: 2026-08-29T18:20:00+02:00
updated: 2026-08-29T18:45:00+02:00
risk: high
execution_class: github_hosted
execution_mode: github_actions_static
execution_reason: merge a security-fallback physical execution class and contract before any field6 consumer can rely on it
persistent_session_role: none
physical_e2e_required: false
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
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: NOT_APPLICABLE
related_pr: 803
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: governance must merge before a separate field6 consumer PR may use the new execution class; host provisioning is post-merge execution, not governance
validation_level: exact_head
last_completed_step: pre-restack exact-head contract/audit/self-hosted/governance/CI GREEN; governance clean-restacked to one commit on fresh main; final exact-head validation pending
repair_cycles_for_current_gate: 1
owned_paths:
  - docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - .github/scripts/test_track_a_independent_ephemeral_physical_runtime_contract.py
  - .github/scripts/audit_track_a_independent_ephemeral_physical_runtime_contract.py
  - .github/workflows/track-a-independent-ephemeral-physical-runtime-contract.yml
  - docs/agents/tasks/active/OTC-20260829-field6-independent-clean-runner.md
  - docs/superpowers/specs/2026-08-29-track-a-independent-clean-physical-runtime-design.md
  - docs/superpowers/plans/2026-08-29-track-a-independent-clean-physical-runtime.md
modules_touched:
  - track-a-execution-routing
depends_on:
  - merged PR #795 self-hosted secret-runner boundary
  - merged PR #798 reusable self-hosted boundary audit
  - merged PR #802 terminal sanitized Synology host-probe evidence
  - host-probe run 33261106292 / job 99123092884 proving Docker socket RW
blocks:
  - OTC-20260828-current-login-field6-runtime
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Define and merge the only permitted independent physical fallback for the already-admitted field6 V4 after the Synology secret boundary was disproven. This task is governance/static-only and cannot execute, register or provision a runner, access Tibia credentials, or post the V4 trigger.

# Frozen decision

`independent_ephemeral_physical_runtime` is legal only for task-owned ephemeral physical Linux work on a physically separate clean owner host after durable Synology disqualification evidence. It never applies to canonical bootstrap/reuse/rebind/recovery, Kasm retained state, or ordinary persistent physical gameplay.

The initial consumer is field6 V4 only. Its later consumer PR must preserve `runtime_access: ephemeral_isolated`, `physical_e2e_required: true`, use a comment-ID-derived one-time runner label with no default labels, and prove clean guest provenance before secrets.

# Causal RED

Exact RED head `a9191c8d4ef593fcb8640e64a49c15a164e6d411` ran only on GitHub-hosted Ubuntu. Run `33263340958`, job `99128922527`, failed exactly with:

```text
INDEPENDENT_PHYSICAL_CONTRACT_RED: routing missing independent_ephemeral_physical_runtime
```

No physical runner, official client, secret, login or mutation was reachable.

# GREEN implementation and independent audit

The minimal implementation adds routing version `1.1.0`, the dedicated `TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md` contract, hosted deterministic contract validation and a separate full-diff falsification audit. Canonical access classes remain bound to `synology_physical_runtime`; the fallback is only for separately contracted `ephemeral_isolated` physical work after durable Synology disqualification.

Pre-final head `b9056733a10a89129e5be113a51969d21c9286ef` proved:

```text
Track A independent ephemeral physical runtime contract  run 33263483362  success
  contract job                                           99129292315    success
  Fresh independent physical routing audit               99129292393    success
Track A self-hosted PR boundary                           run 33263483366  success
Track A agent runtime governance                          run 33263483345  success
```

CI run `33263483454` failed only on yamllint because the new workflow lacked a final newline:

```text
.github/workflows/track-a-independent-ephemeral-physical-runtime-contract.yml
62:46 [new-line-at-end-of-file] no new line character at the end of file
```

The EOF defect was repaired without changing runtime semantics. Exact head `8ca15df56301b23d304817aef0425dac012a4d9e` then proved the complete pre-restack gate:

```text
Track A independent ephemeral physical runtime contract  run 33263615236  success
Track A self-hosted PR boundary                           run 33263615253  success
Track A agent runtime governance                          run 33263615238  success
CI                                                       run 33263615402  success
  CI / Required job                                      99129744367    success
```

No physical/self-hosted job ran from this governance branch. The exact eight-file tree was then rebuilt as one commit directly on unchanged protected `main@d05744b746b33c979b85ba25442ffab7298ba786`; this checkpoint is included in that same one-commit restack and triggers the final exact-head validation generation.

# Next action

Require final one-commit exact-head contract + fresh-audit + self-hosted-boundary + runtime-governance + `CI / Required` GREEN, verify zero material review threads and fresh stable main, then mark PR #803 Ready and squash-merge. Only a later invocation based on that merged governance may restack the field6 consumer to the new execution class. No V4 trigger or physical job is legal from this task.