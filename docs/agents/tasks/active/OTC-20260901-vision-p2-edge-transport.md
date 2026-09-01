---
task_id: OTC-20260901-vision-p2-edge-transport
status: validating
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-EDGE-TRANSPORT
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: mcp_auth_claim_repair_validated
branch: feat/OTC-20260901-vision-p2-edge-transport
base_branch: main
base_main: 6c21ef021875aab15663505629b6e72655b1fcf1
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-02T00:01:00+02:00
risk: high
execution_class: github_hosted
execution_mode: direct_mcp_owner_authorized
preferred_execution: mcp
run_scope: wave_1_worker
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
prompting_standard_version: 2.1
policy_version: 2
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
worktree: C:/Users/barte/otclient-vision-p2-edge-transport
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
depends_on:
  - PR #820 merged foundation
  - PR #824 merged Wave 0 coordinator cleanup
  - current main d1cb8722c3116a0e0aeb72b9b360712f43151f17 after the subsequent main advance
related_prs:
  - PR #829 Wave 1 worker Draft
current_blocker: fresh exact-head hosted CI and coordinator classification are required for the owner-authorized MCP repair.
next_action: force-with-lease publish the current-main-restacked MCP repair, obtain exact-head CI/Package A/Package B/Track A, then return to coordinator classification; do not self-promote or merge.
invocation_started_at: 2026-09-01T17:03:28+02:00
last_progress_at: 2026-09-02T00:01:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: ca565c49-exact-head
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
---

# OTC-VISION-P2-EDGE-TRANSPORT

## Mission

Implement a narrow authenticated bounded Synology-to-Molehill edge transport with versioned metadata and content-addressed artifacts, without generic shell, raw GUI control or authority expansion.

## Independent-review repair checkpoint — 2026-09-01T23:14:54+02:00

The coordinator's exact-head independent review comment `5500413800` is the current repair authority. RED probes mechanically reproduced all four findings on `fe258ecdb65cbc6802b54d2adff57ecb4357865a`: arbitrary signed observation fields; A→B→A replay reopening; direct authenticated-object construction; and JCS-compatible `1`→`1.0` payload substitution.

The local RED→GREEN repair replaces open-ended metadata admission with per-kind exact schemas, signs explicit session/run/connection-generation identity, requires a caller-persisted bounded replay ledger (including a snapshot/restore boundary), removes public constructor self-certification, and requires exact observation application types before MAC verification. New focused probes cover all four review findings plus verifier reconstruction and cross-session/run substitution. The normal no-runtime/no-authority restrictions remain unchanged; physical action budget/count remains `0/0`.

Local validation at `2026-09-01T23:15:47+02:00`: focused edge transport `38/38`, protocol plus edge transport `55/55`, Ruff, `py_compile`, checkpoint validation, exact changed-task Track A governance validation, and `git diff --check` all passed. The attempted obsolete governance command path was corrected to `.github/scripts/test_track_a_agent_runtime_governance.py`; no source or authority change resulted.

The prior publication generated Package B `33560269278`, Package A `33560269282`, CI `33560269528` and Track A governance `33560269190` on the pre-restack head. Package A deterministic core passed; its fresh falsification path audit failed only because the stale topology made four current-main Phase 2 prompt files appear unexpected. The clean rebase at `61010d8f6d5797829a00ec5dd1e05b1f9e57fe4a` makes `origin/main..HEAD` exactly the four declared worker-owned paths, so a final force-with-lease publication and fresh exact-head aggregate are required.

The current-main-restacked implementation generation passed: Package A `33560626122`, Package B `33560626062`, CI `33560626315` and Track A governance `33560626049`, all `success`. Package A's deterministic core and fresh falsification audit both passed. This final evidence checkpoint is intentionally a new final head, so it awaits exactly one further aggregate before the worker returns to the coordinator.

After that aggregate, `main` advanced through `103fa3071ee4d82d7dff934034e2442c32bd3a81`. The worker rebased cleanly to `4db10aebabb45244aa1232d4f6267dcf09b96f14`; the current `origin/main...HEAD` diff is exactly the four declared worker-owned paths. Local focused `38/38`, protocol-plus-transport `55/55`, Ruff, `py_compile`, checkpoint validation, Track A governance validation and whitespace checks again passed. This final-main restack requires a fresh hosted aggregate.

## Dispatch boundary

This task is bootstrapped by `OTC-VISION-P2-COORDINATOR`. The worker may mutate repository files only after its own isolated session validates the exact task, branch, worktree and Draft PR and confirms the ownership set below remains non-overlapping. Real Official Tibia runtime observation is **not authorized** by this record. Any later transition from `runtime_access: none` to `read_only` requires a coordinator-assigned single observation window, fresh exact-target proof, and a persisted valid read-only admission record before observation.

## Binding reads

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`

## Owned paths

- `docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md`
- `docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md`
- `tools/tibia_re_control_center/agent_edge_transport.py`
- `tests/tools/tibia_re_control_center/test_agent_edge_transport.py`

Shared indexes/governance files, including `docs/agents/MODULE_CATALOG.md`, are not owned. Any required path outside this set is a coordinator ownership-extension request, not an implicit permission.

## Implementation discipline

Use RED-to-GREEN TDD for each behavior. Preserve the approved architecture and reuse the existing Control Center/session plane rather than creating a second control plane/store. Fake/hosted evidence can validate repository behavior but can never be reported as real-runtime success. The worker must open no additional implementation PR and must not merge/promote its own result; the coordinator classifies the Draft PR.

## Dispatch contract

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-EDGE-TRANSPORT
TASK_ID: OTC-20260901-vision-p2-edge-transport
TASK_RECORD: docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
PROJECT_LANE: otclient
BASE_MAIN: e883543403d5430d7b1d287f59043b23c98f37d6
BRANCH: feat/OTC-20260901-vision-p2-edge-transport
WORKTREE: C:/Users/barte/otclient-vision-p2-edge-transport
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
DEPENDENCIES:
  - PR #820 merged
  - PR #824 merged
runtime_access: none
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T00:01:00+02:00
head: eb8ecbe9b315800575f0abbae9e2d520c54d363d
head_semantics: owner_authorized_mcp_repair_rebased_to_current_main_before_final_metadata_commit
branch: feat/OTC-20260901-vision-p2-edge-transport
pr: 829
status: validating
phase: direct_mcp_auth_claim_repair
context_routes:
  - phase-2-read-only-coordination
  - edge-transport
  - authentication-boundary
  - owner-authorized-mcp-execution
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
proven:
  - trusted main is 6c21ef021875aab15663505629b6e72655b1fcf1; it contains owner-authorized direct-MCP coordinator override PR #848 and the later Codex cost-control governance #849, which changes no worker-owned transport path.
  - coordinator mechanically reproduced that module-global proof objects could mint peer_authenticated transport objects on the prior exact head even with all hosted gates green.
  - RED required the real proof globals and authority-looking local attributes to be absent and failed on the prior implementation.
  - the repair removes _VERIFIED_FRAME_PROOF and _OUTBOUND_CHANNEL_PROOF entirely; VerifiedEdgeFrame and EdgeOutboundChannel carry no peer_authenticated, mutation_authorized, physical_action_budget, evidence_fresh or action_resume_allowed attributes.
  - VerifiedEdgeFrame uses frozen slots and EdgeOutboundChannel uses explicit slots, so callers cannot attach those authority-looking attributes after construction.
  - wire frames still carry authority_scope=PEER_IDENTITY_ONLY plus mutation_authorized=false, physical_action_budget=0, evidence_fresh=false and action_resume_allowed=false, and verifier-side schema/HMAC checks reject expansion before returning neutral data.
  - focused edge transport passes 38/38 and protocol-plus-transport passes 55/55; Ruff and git diff whitespace checks pass.
  - runtime_access remains none; no Official Tibia/Synology/Kasm observation, credentials, login, GUI input, process control, process memory, payload capture or physical action occurred.
derived:
  - Python object provenance is no longer treated as an authentication boundary; authentication is a property of the successful cryptographic verify/handshake call path only.
  - direct construction can create only authority-neutral data/channel objects and cannot manufacture a local authentication or Track A authority claim.
  - replay-ledger durable persistence remains an integration concern assigned to PR #846 and is not widened into this worker's four-path scope.
unknown:
  - exact-head hosted CI/Package A/Package B/Track A result for the MCP repair commit.
  - independent coordinator classification of the exact published repair head.
conflicts: []
first_failure:
  marker: RED-CALLER-MINTABLE-AUTH-CLAIM
  evidence: focused negative test failed because _VERIFIED_FRAME_PROOF existed and direct objects exposed authentication/authority-looking fields.
rejected_hypotheses:
  - module-private proof objects are a sufficient Python security boundary: rejected by direct use of the real module globals.
  - keeping authority fields hard-coded false on a constructible object is sufficient: rejected because callers could supply or attach alternate values outside verifier provenance.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
validation:
  - command: focused caller-mintable authentication-claim RED then GREEN
    result: PASS
    evidence: RED reproduced the reachable proof global; GREEN proves proof globals and authority-looking object attributes are absent and cannot be attached through normal or object.__setattr__ paths.
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_edge_transport
    result: PASS
    evidence: 38/38.
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_protocol tests.tools.tibia_re_control_center.test_agent_edge_transport
    result: PASS
    evidence: 55/55.
  - command: python -m ruff check plus git diff --check
    result: PASS
    evidence: all checks passed.
blockers:
  - exact-head hosted aggregate and coordinator classification remain required before promotion.
next_action: publish the current-main-restacked MCP repair with safe lease, obtain one exact-head hosted aggregate, and return to coordinator classification without self-promoting.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: 2026-09-01T22:49:31+02:00
  session_started_at: 2026-09-01T22:43:34+02:00
  checkpointed_at: 2026-09-01T22:52:27+02:00
  last_progress_at: 2026-09-02T00:01:00+02:00
  phase: exact-head-ci-passed-return-to-coordinator
  exact_head: ca565c49fd2ab222f247ad11bf2742ca5bf4d780
  pull_request: 829
  active_operation: none
  external_run_ids: [33557712369, 33557712221, 33557712165, 33557712147]
  operation_started_at: 2026-09-01T22:51:00+02:00
  wait_deadline_at: null
  check_generation: ca565c49-exact-head
  checks_used: 1
  status: waiting_for_coordinator_classification
  safe_to_resume: true
  resume_condition: coordinator classification of the green Draft PR.
  next_action: leave PR #829 Draft and return this exact-head evidence to the coordinator.
```
