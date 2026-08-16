---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: investigating
agent: ChatGPT
session_id: chatgpt-runtime-20260816-1311
session_role: runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: reconcile-runtime
branch: ci/OTC-20260816-track-a-canonical-runtime-e2e
base_branch: main
base_main: 0d7b2607912552599ae501891491aab439cfde7b
risk: high
updated: 2026-08-16T13:11:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-canonical-runtime-e2e.yml
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
depends_on:
  - trusted main Gate A manager/supervisor implementation
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical Synology evidence is routed through repository-controlled GitHub Actions; no ad-hoc SSH or owner-funded AI is used
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one serialized physical runtime objective; reconcile authority/identity first, then execute only the gate-selected canonical transition
validation_level: focused
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: canonical-live-runtime
canonical_registration: UNKNOWN
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
owner_funded_ai_api_authorized: false
live_runtime_authorization_source: owner invocation 2026-08-16 for physical Synology X11/VNC/login/relogin/E2E, subject to all current Track A gates
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
excluded_runtime_surfaces:
  - PR #303 task-owned display/process/state/proxy surfaces
admission_basis:
  - initial operation is read-only inspection of the fixed canonical authority/registration namespace only
  - no client process, X11 display, VNC endpoint, credential, login state, input or PR #303 surface is observed or mutated before reclassification
  - fixed canonical authority state path is unique by accepted ADR and wrapper; mutation remains false
current_trusted_base_limitations:
  generation_rebind: REQUIRED_UNAVAILABLE if a current registration exists with an older lease generation
  bootstrap: REQUIRED_UNIMPLEMENTED if the authoritative registration is absent
  consequence: no live client mutation may use a newly authored unmerged primitive to bypass the trusted-base gate
acceptance:
  - fresh Synology reconciliation classifies authoritative lease and canonical registration without historical display/PID assumptions
  - before any mutation, task is reclassified to exactly one permitted canonical transition with a complete admission record
  - Gate A passes under the final cancellation-safe whole-lifetime supervisor for every state-changing operation
  - any required generation rebind is a reviewed trusted-base implementation and passes before Gate B
  - Gate B freshly proves exact official Linux client identity, display/window/state and target uniqueness before reuse
  - if registration is absent, canonical bootstrap is performed only through a reviewed trusted-base implementation; otherwise the task fails closed
  - canonical X11/VNC session is persistent and current mapping is directly proven rather than inherited from historical :98/6082 claims
  - bounded login/relogin and physical E2E pass without exposing credentials or creating a second logged-in Track A Global session
  - final session is intentionally left alive idle when healthy and controller authority is released safely
  - PR #303-owned runtime surfaces are never stopped, signalled, attached, reconfigured, reused or cleaned
last_completed_step: claimed fresh current-main RUNTIME task with mutation disabled
next_action: execute one read-only Synology reconciliation job that reports only public canonical lease status plus existence/schema/generation fields of the fixed runtime registration, without process/display/client observation
---

# Track A canonical physical runtime E2E

This task is the serialized `OTCLIENT-TIBIA-RE-RUNTIME` owner for the current invocation. It does not inherit historical `:98`, `6082`, PID/session or PR #303 runtime authority.

The first physical operation is intentionally read-only and limited to canonical authority metadata. Its result decides whether the trusted-base path is ordinary reuse, generation rebind, or initial bootstrap. Any required transition that is unavailable/unimplemented on the trusted base remains a hard fail-closed blocker until a separately reviewed implementation is promoted; this task will not convert its own unmerged code into live authority.
