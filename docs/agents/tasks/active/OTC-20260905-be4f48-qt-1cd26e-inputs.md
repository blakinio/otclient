---
task_id: OTC-20260905-be4f48-qt-1cd26e-inputs
status: validating
agent: Codex
session_id: login-closure-20260905-084311-ae070f034ee4
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: validate
branch: ai/OTC-20260905-be4f48-qt-1cd26e-inputs
base_branch: main
base_main: 981a64151d219341f175597027e676be0f52068a
created: 2026-09-05T09:24:28Z
updated_at: 2026-09-05T09:34:46Z
invocation_started_at: 2026-09-05T08:43:11Z
last_progress_at: 2026-09-05T09:34:46Z
policy_version: 2
prompting_standard_version: 2.1
execution_mode: codex
execution_reason: isolated checkout and deterministic local tests; exact client qualification on GitHub-hosted runner
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: true
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one selected call input projection in the exact qualified caller
max_additional_tasks_after_terminal_entry_task: 4
additional_task_budget_reason: explicit ordered multi-task owner login-closure programme, fresh invocation prospective 240-minute declaration under owner ordered programme request
additional_source_task_ordinal: 2
foreground_runtime_budget_minutes: 240
foreground_budget_reason: explicit sequential source qualification and clean promotion/archive programme
ci_checks_for_current_head: 0
ci_check_generation: source_claim
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - tools/tibia_re_be4f48_qt_1cd26e/**
  - .github/workflows/tibia-re-be4f48-qt-1cd26e.yml
  - docs/agents/tasks/active/OTC-20260905-be4f48-qt-1cd26e-inputs.md
  - docs/agents/evidence/OTC-20260905-be4f48-qt-1cd26e-inputs/**
modules_touched: []
reuses:
  - docs/agents/prompts/OTC_BE4F48_QT_1CD26E_CALL_INPUTS.md
  - docs/agents/evidence/OTC-20260904-be4f48-post911-promotion/result.json
  - source911 finite must-identity design and source919 exact package and ELF guards
depends_on: []
blocks:
  - clean coordinator consumption of this exact source result
cross_repository_task_ids: []
ownership_released: false
next_action: exact qualification and independent whole-diff review
---

# Source claim

Execute merged registration #926 (981a64151d219341f175597027e676be0f52068a) and exact prompt docs/agents/prompts/OTC_BE4F48_QT_1CD26E_CALL_INPUTS.md from fresh main981a64151d219341f175597027e676be0f52068a. Source923 consumed by924 and archived925; no overlapping active source ownership. Source919's blocked warning graph remains separate. Only135-byte caller[1cd220,1cd2a7), selectedcall1cd26e→142e30; sixregisters+threeoutgoing8-byte stackslots. TargetFDE/dynsym metadata only, no callee body or storage-output rescan.

Fresh governance/track/admission/currentfence and active/openPR roster unchanged after registration-onlymerge. Primary15.32.be4f48/52105824/552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1; packagedQtCore7354472/03ac3e4e7356399897ec58d42c81ae5c257072d45d539de1def528a8a04911fa. TrackB284 unchanged62383aded3acbeb5f405a12fe1f93849cd8e35f9; wire deltaNOT_PROVEN.

Reuse source923 repaired finite must-value core, replacing store enumeration with selected-call incoming values. TDDRED/GREEN, conservative aliases/implicit memory/prefixed control, exact qualification, independent whole-diff, final exact focused/CI/governance/boundary. Unknown inputs are not actual absence; call-return tokens are provenance only. RuntimeE2E NOT_APPLICABLE because static-only producer. SourceDraft/unmerged; cleanpromotion and separatearchive before a nextproofclass.

Invocation08:43:11Z/240minutes/4additional, this is additional2. No terminal-entry CI exception; max2ordinary observations/head and1identicaltransient retry,3repaircycles,15minute no-progress. Runtimeadmissionnone complete above; no client execution/login/credentials/memory/capture/OCR/serviceE2E/TrackB change. Rawclient/core and acquisition state transient, deleted before sanitized JSON artifacts.

## Repository-only RED/GREEN

RED 4b357ec1574ea177e9df68485f5de23dc0ab50ff:18behavior tests fail on explicit unimplemented selected-call scaffold, no official bytes involved. GREEN38testsPASS includes inherited package/identity tests and precise register/stack-slot projection. The first minimal implementation conservatively lost stack arguments after known register-only XOR; TDD exposed this, then explicit known ordinary instruction effects preserve memory when no memory-write operand exists. Unknown instructions still stop, privilege/BND/implicit-stack/segment/address-size regression families pass; exact setcc/cmov condition whitelist prevents admission by broad mnemonic prefix. Source923 storage enumeration is removed entirely from the new analyzer; only one selected call is projected. Python compileall and git diff --check PASS. No callee body inspected, no cap widened. Independent review and hosted exact qualification remain required.

## Independent finding-family repair

Scientific head d89190a7b90ef4380d25e2749f40bc345be86c0c is disqualified from promotion. Root found S927-01 selected target parameter shadowing by branch successor traversal. Independent reviewer found S927-02 Capstone5.0.6 write metadata omits MOVQ/CMPXCHG memory writes and CMPXCHG implicit RAX write. Regression RED7907f7ca656e5f8cc79cb951364d95060181a55e demonstrated three failures; sibling RED5ad1acceda3647ff3283b85af871e378d502b9f1 adds the independently reproduced implicit RAX failure. GREEN renames the traversal variable, invalidates memory on any generic MEM operand, and explicitly invalidates RAX for CMPXCHG. Register-only ordinary operations preserve stack values; unknown instructions still stop.42testsPASS and git diff --check PASS. This is repair cycle1, no cap/scope expansion. Source923 promoted only model/no-positive-store and CFG facts, not a positive affected scalar carrier. Fresh independent repair review and exact-head qualification are required before consumption.
