---
task_id: OTC-20260816-track-a-worldmap-extent-static-re
status: blocked
agent: ChatGPT
session_id: chatgpt-viewport-static-20260816-1426
session_role: static_re_researcher
project_lane: otclient
lane: STATIC-RE
track_id: official-client-re
task_kind: discovery
phase: investigate
implementation_authorized: false
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
pr: 367
risk: medium
updated: 2026-08-16T14:40:30+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-extent-static-re.md
  - .github/scripts/tibia-official-client-re-worldmap-extent-static.py
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/**
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md
  - docs/agents/evidence/OTC-20260816-official-client-map-viewport-feasibility/20260816-evidence.md
  - PR #365 merged feasibility checkpoint
  - PR #366 merged feasibility-task archive/ownership release
  - PR #310 GitHub-hosted exact-client staging failure evidence
  - run 31892019505 artifact 9248797952 historical exact-binary static evidence
  - run 31947502633 artifact 9263704543 independent hosted input-blocker corroboration
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: exact-client ELF/RTTI/xref/disassembly work is deterministic/disposable and Track A hybrid routing requires GitHub-hosted execution rather than Synology
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: rising
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive patch/dependency graph spans extent ownership, storage/protocol consumers and render/camera/picker consumers; the task is blocked on exact hosted input before a useful split exists
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
invocation_started_at: 2026-08-16T14:20:00+02:00
last_progress_at: 2026-08-16T14:40:30+02:00
ci_checks_for_current_head: 0
ci_check_generation: blocked-static-frontier-checkpoint-pending
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
heavy_validation_runs: 1
hosted_staging_attempts_this_task: 1
hosted_staging_run: 31947523640
hosted_staging_job: 95165795953
hosted_staging_artifact: 9263709952
hosted_staging_artifact_digest: sha256:87315733a626bd0d2f8540bc05b0aa5bcd1fcd33d78764be6dc0243a30ae837f
hosted_staging_result: INPUT_BLOCKED
independent_hosted_corroboration_run: 31947502633
independent_hosted_corroboration_job: 95165743019
independent_hosted_corroboration_artifact: 9263704543
historical_exact_binary_run: 31892019505
historical_exact_binary_job: 95029600292
historical_exact_binary_artifact: 9248797952
historical_exact_binary_runner: synology-otclient-01
historical_exact_binary_evidence_reused: true
current_exact_binary_reexecution: NOT_PERFORMED
current_exact_binary_provenance_upgraded: false
blocker_class: INPUT_BLOCKED
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
static_classification: BLOCKED
new_gui_session_created: false
runtime_used: false
client_bytes_modified: false
synology_static_re_this_task: false
temporary_hosted_workflow_retained: false
analyzer_validation:
  python_syntax_on_hosted_boundary: PASS
  exact_binary_execution: NOT_RUN_INPUT_BLOCKED
next_action: provide a compliant GitHub-hosted-readable exact 15.32.df7b29 native-Linux client source, verify size/SHA, then resume static typeinfo/vtable/xref/field/allocation/parser/render dependency recovery; do not use Synology static fallback and do not escalate to GUI/runtime for this input blocker
---

# Track A worldmap extent static RE

## Objective

Recover a durable static patch/dependency graph for the exact official native-Linux client covering:

- `TWorldMapExtent`;
- `TWorldMapSubfieldExtent`;
- `TWorldMapViewport`;
- `TWorldMapStorage`;
- `TWorldmapProtocolMessageHandler`;
- `TWorldMapRenderProvider`;
- `TWorldMapCamera`;
- `TWorldMapPicker`.

No client bytes were modified. No live official-client runtime was observed or mutated.

## Final classification for this invocation

```yaml
static_classification: BLOCKED
blocker_class: INPUT_BLOCKED
runtime_discriminator_required: false
```

The unresolved questions remain static questions, but the exact `15.32.df7b29` binary cannot currently be staged on the required GitHub-hosted analysis surface. Synology is explicitly not used as a static fallback.

## Durable outputs

- `docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-static-frontier.md`
- `docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md`
- `.github/scripts/tibia-official-client-re-worldmap-extent-static.py` — retained as an unvalidated-on-exact-input analyzer scaffold; syntax passed the hosted boundary step but exact analysis never ran because input staging failed.

The one-shot staging workflow is removed at this checkpoint so subsequent task/report pushes cannot silently repeat the failed source request.

## Trusted starting point and ownership

PR #365 merged the accepted PR #325 feasibility report/evidence; PR #366 archived that completed task and released its ownership. PR #363's continuation-prompt paths and PR #310's P2 staging paths remain read-only.

Current coordinator state also classifies P2 hosted staging as blocked on a compliant exact-client source with no Synology fallback.

## Static acceptance inventory

- [x] exact historical client size/SHA fence revalidated from retained artifact `9248797952`; current exact-binary reexecution is explicitly `NOT_PERFORMED`;
- [x] all eight requested semantic/type surfaces inventoried with exact retained addresses;
- [x] retained `.data.rel.ro` relocation leads for `TWorldMapRenderProvider` and `TWorldMapViewport` recorded without overclaiming them as vtables;
- [ ] typeinfo/vtable/constructor/destructor evidence recovered for extent/subfield/viewport — BLOCKED on exact hosted binary;
- [ ] candidate dimension/edge fields and default writers identified — BLOCKED on exact hosted binary;
- [ ] material readers/writers through storage/protocol recovered — BLOCKED on exact hosted binary;
- [ ] material readers/writers through render/camera/picker recovered — BLOCKED on exact hosted binary;
- [x] literal `18`/`14` are not treated as patch constants; historical `18 x 14` remains `DERIVED_FROM_OBSERVED_JOB_LOG` only;
- [ ] fixed arrays, allocation/capacity, loops/masks, parser row/column/floor assumptions, clipping/culling, coordinate packing, cache and picking limits audited — BLOCKED on exact hosted binary;
- [ ] complete patch/dependency graph with isolated-change consequences produced — BLOCKED;
- [x] final classification chosen from the required set: `BLOCKED`;
- [x] no client byte mutation or live runtime action occurred;
- [x] one materially different GitHub-hosted staging experiment executed; failure persisted as sanitized evidence;
- [x] independent same-repo P0 GitHub-hosted attempt corroborates the same input blocker;
- [x] one-shot workflow removed to prevent blind retries;
- [ ] exact-head normal repository CI for the final blocked checkpoint — pending after this commit.

## Input-staging result

This task's run `31947523640` / job `95165795953` failed at the materialization step. Analyzer installation and static graph extraction were skipped; cleanup and sanitized artifact upload succeeded. Artifact `9263709952` records `INPUT_BLOCKED` for the same-URL Referer/compressed strategy.

Independent P0 run `31947502633` / job `95165743019` on `ubuntu-latest` records the same class of failure in artifact `9263704543`.

No additional HTTP variant, no Synology fallback and no runtime escalation are authorized by this result.

## Resume condition

Resume only when the exact fenced client is available to GitHub-hosted Actions through a compliant source. The first resumed action is exact size/SHA validation followed by static recovery of typeinfo/vtables, field writers/readers, allocation limits, protocol parser assumptions and render/camera/picker dependencies.
