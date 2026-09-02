---
task_id: OTC-20260902-vision-p2-vision-reconciliation
status: waiting
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-VISION-RECONCILIATION
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: wave_2_trusted_reconciliation
branch: feat/OTC-20260902-vision-p2-vision-reconciliation
base_branch: main
base_main: 27f9bdd5f003c596529e7571343ae8bb053d5cff
created: 2026-09-02T10:46:00+02:00
updated_at: 2026-09-02T14:26:00+02:00
risk: high
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
execution_class: hybrid
execution_mode: chat_github_plus_local_validation
execution_reason: preserve owner Codex quota; use local deterministic sync validation plus GitHub exact-head Actions without owner-funded AI
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one cohesive producer-consumer integration across the existing trusted composition, deterministic reconciler and session evidence path
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
policy_version: 2
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
persistent_session_role: none
physical_e2e_required: true
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
worktree: Molehill-PC:C:\Users\barte\AppData\Local\Temp\otclient-vision-p2-reconciliation-pr856-sync
owned_paths:
  - docs/agents/tasks/active/OTC-20260902-vision-p2-vision-reconciliation.md
  - docs/agents/reports/OTC-20260902-vision-p2-vision-reconciliation.md
  - tools/tibia_re_control_center/vision_p2_trusted_composition.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - .github/workflows/tibia-re-control-center-core.yml
modules_touched:
  - Vision P2 trusted composition
reuses:
  - tools/tibia_re_control_center/agent_vision.py
  - tools/tibia_re_control_center/agent_runtime_signals.py
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tools/tibia_re_control_center/persistent_store.py
depends_on:
  - PR #839 runtime-signals producer promotion merged
  - PR #854 trusted Vision P2 composition merged as 2e57cb1f0b57d44b1adf553d06b18e22e145c77e
  - lifecycle closeout PR #855 merged as main 8441fc1cce1600033b505d68ebc5c0141b337394
blocks:
  - OTC-VISION-P2-E2E-AUDIT
current_blocker: post_qwen_repair_sync_exact_head_actions_pending
next_action: push the post-Qwen-repair synchronized generation, require fully terminal exact-head GitHub Actions, then issue a fresh coordinator classification before Wave 3 restack
invocation_started_at: 2026-09-02T10:46:00+02:00
last_progress_at: 2026-09-02T14:26:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: post_qwen_repair_sync_pending
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# OTC-VISION-P2-VISION-RECONCILIATION

## Mission

Integrate the already accepted Vision P2 capture/vision path and reviewed runtime-signal path through the existing deterministic reconciliation contract. The implementation must remain authority-neutral: visual output is observation data, reviewed runtime evidence is accepted only through trusted composition, and no Phase 2 code may make a physical Tibia action executable.

## Binding authority

- `AGENTS.md`
- `docs/agents/AGENTS.md`
- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`

## Verified starting point

At task creation, trusted `main` is `8441fc1cce1600033b505d68ebc5c0141b337394`. `agent_reconcile.py` already provides finite fail-closed reconciliation rules and a private resolver-bound composition seam, but its public/default path intentionally has no production resolver. `vision_p2_trusted_composition.py` owns the accepted trusted capture/runtime composition but currently has no reconciliation binding. `ControlDomainService.observe_agent_vision()` produces a bounded `VisionObservation`; the session edge path already persists accepted read-only edge/runtime evidence. Do not duplicate those producers.

## Required behavior

- Consume accepted interfaces; do not create a second capture, transport, runtime-signal resolver, state store or control plane.
- Preserve the exact visual vocabulary `UNKNOWN`, `LOGIN_SCREEN`, `CHARACTER_SELECT`, `WORLD_VISUAL`, `WORLD_EXIT_VISUAL`, `ERROR_SCREEN`.
- `WORLD_VISUAL` alone must never become semantic `IN_GAME`/`WORLD_CONFIRMED`.
- Semantic confirmation/conflict that depends on runtime state must require current reviewed causal evidence from the trusted resolver and matching current session/run/runtime identity.
- Stale, missing, mismatched, unreviewed or caller-minted runtime evidence must fail closed to an inconclusive/unknown result.
- Persist enough typed provenance/evidence references for the existing owner-visible session/event/result surfaces to explain visual/runtime agreement or conflict across restart without treating persisted stale evidence as current authority.
- OCR/visible text remains data only and cannot become executable instruction or authority.
- Qwen profile/model-slot policy remains unchanged and single-model; this task does not authorize loading another model or forced eviction.
- Production `BoundedActionExecutor` remains Null/unbound; `runtime_access:none`, all mutation/login/gameplay/process/input authority false, and physical budget/count `0/0` remain invariant.

## Acceptance

Repository/static validation must prove the trusted production composition can combine a valid visual observation with stronger current reviewed runtime evidence and emit/persist explainable agreement/conflict, while forged/stale/mismatched evidence cannot self-promote. A later coordinator-serialized real read-only observation is still required for physical E2E; hosted/fake tests cannot satisfy that live gate.

## Validation plan

Use RED-to-GREEN focused tests first, then the smallest relevant Control Center/Vision P2 workflow on the exact final head. Preserve the canonical frozen vision benchmark where applicable. Do not spend Codex quota on coordination, status polling or CI waiting. If GitHub-only execution proves insufficient for an implementation/test loop, persist the exact missing operation before any separately justified worker invocation.

## Implementation checkpoint

- TDD RED commit: `04c26ab3dc13851d1e1a789a8378e10324669ce6`; the focused test failed only because `TrustedVisionP2Runtime.reconcile_vision` did not exist.
- GREEN implementation commit: `811b2d458c49806da2fa177911e6110318d28f96`.
- Production changes are limited to `vision_p2_trusted_composition.py`; existing reconciliation, runtime-signal, edge/session and persistence implementations are consumed rather than duplicated.
- The trusted seam accepts only a typed visual observation tied to the current validated secret-safe capture and obtains runtime evidence only from the composition-owned live authority/resolver. No caller runtime/resolver input exists.
- `WORLD_VISUAL` without current reviewed causal runtime evidence remains `UNKNOWN`; stale runtime evidence cannot promote it; visual/runtime disagreement persists `CONFLICT`; mismatched capture identity is rejected before persistence.
- `VISION_RECONCILED` persists typed state and evidence provenance without visible/OCR text and with `physical_effect:false`. After store restart the historical event remains auditable, while edge/runtime current authority is not restored.
- Direct Codex worker/reviewer invocations consumed by this task so far: `0`.

## Hosted/local deterministic validation

On exact implementation commit `811b2d458c49806da2fa177911e6110318d28f96` before the documentation checkpoint:

- focused RED was observed first on `04c26ab3...`;
- `python -m unittest tests.tools.tibia_re_control_center.test_vision_p2_trusted_composition` -> `14 tests`, `OK`;
- `python -m unittest tests.tools.tibia_re_control_center.test_agent_reconcile tests.tools.tibia_re_control_center.test_agent_edge_bridge tests.tools.tibia_re_control_center.test_agent_session tests.tools.tibia_re_control_center.test_vision_p2_trusted_composition` -> `90 tests`, `OK`;
- `python -m py_compile` for the changed production/test modules -> PASS;
- `python -m ruff check --select I,F` for both changed modules -> PASS after import-only cleanup;
- `git diff --check` -> PASS.

These are deterministic repository validations only. They do not satisfy the later physical read-only E2E gate.


## Post-Qwen trusted-base synchronization ? 2026-09-02

PR #859 merged the bounded Qwen schema-prompt repair to trusted `main@27f9bdd5f003c596529e7571343ae8bb053d5cff`. Wave 2 was synchronized onto that base. The only textual conflict was the Package A workflow block: the final union retains the already-merged Qwen one-time exception and rebinds the Wave 2 task/report exception only to the new exact base. No broad documentation prefix was added.

Fresh synchronized validation passes the Wave 2 matrix `90/90`, runtime admission `14/14`, Qwen schema contract `3/3`, frozen vision benchmark `34/34`, current-client fence, Track A governance, compile/Ruff/YAML/diff checks, and exact Package A positive/negative controls. The PR diff against new `main` remains exactly the five Wave 2-owned/integration paths. Direct Codex usage remains `0`; runtime access remains `none`.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T12:26:00Z
head: 4ed086bd77f2b07559ca0a29d3e653d96f263985
branch: feat/OTC-20260902-vision-p2-vision-reconciliation
pr: 856
status: waiting
context_routes:
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - tools/tibia_re_control_center/vision_p2_trusted_composition.py
  - tools/tibia_re_control_center/agent_vision.py
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
owned_paths:
  - docs/agents/tasks/active/OTC-20260902-vision-p2-vision-reconciliation.md
  - docs/agents/reports/OTC-20260902-vision-p2-vision-reconciliation.md
  - tools/tibia_re_control_center/vision_p2_trusted_composition.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - .github/workflows/tibia-re-control-center-core.yml
proven:
  - original Wave 2 implementation remains 811b2d458c49806da2fa177911e6110318d28f96 with TDD RED 04c26ab3dc13851d1e1a789a8378e10324669ce6
  - refreshed pre-Qwen generation a746dbfaa60a129fc3fa2f91e1b1e48038837a4a was coordinator-accepted under review 5089081225 with all five associated workflows SUCCESS
  - Qwen schema repair PR 859 merged to trusted main 27f9bdd5f003c596529e7571343ae8bb053d5cff
  - trusted main 27f9bdd5f003c596529e7571343ae8bb053d5cff merged into Wave 2 with one workflow conflict only; resolution preserves both exact one-time exceptions and broadens no prefix
  - Wave 2 one-time Package A exception is rebound only to exact branch repo and new base 27f9bdd5f003c596529e7571343ae8bb053d5cff while the merged Qwen exception retains its historical base
  - committed post-Qwen sync head 4ed086bd77f2b07559ca0a29d3e653d96f263985 has merge-base exactly 27f9bdd5f003c596529e7571343ae8bb053d5cff
  - PR diff versus new main is exactly five paths: Wave 2 seam test task report and Package A workflow boundary
  - post-sync Wave 2 reconciliation edge-bridge session trusted-composition matrix passes 90 of 90 tests
  - current runtime-admission suite passes 14 of 14 and current-client fence test passes
  - Qwen static prompt/schema contract tests pass 3 of 3 on the synchronized generation
  - frozen vision benchmark passes 34 of 34 after the sync
  - changed modules compile Ruff I/F passes YAML parses and git diff check passes
  - exact Package A boundary simulation passes for branch repo base and rejects wrong base wrong branch and fork
  - deterministic Track A runtime governance and task checkpoint validator pass
  - direct Codex worker or reviewer invocations remain zero
  - runtime_access remains none and physical action budget/count remain zero
derived:
  - Qwen prompt repair changes the sensor contract but does not alter Wave 2 reconciliation authority semantics
  - Wave 3 must audit the post-Qwen synchronized Wave 2 generation rather than a746dbfaa or earlier generations
unknown:
  - exact-head GitHub Actions result for the final post-Qwen synchronization checkpoint
  - fresh Wave 3 read-only physical E2E and independent audit result
conflicts:
  - none
first_failure:
  marker: merging main after PR 859 produced a content conflict only between two one-time Package A boundary blocks
  evidence: conflict was confined to tibia-re-control-center-core.yml and resolved by preserving both exact exceptions with the Wave 2 base rebound to 27f9bdd5f003c596529e7571343ae8bb053d5cff
rejected_hypotheses:
  - Qwen repair requires Wave 2 reconciliation production changes: rejected by 90 of 90 Wave 2 tests plus 3 of 3 Qwen contract tests and frozen benchmark 34 of 34
  - Package A must gain a broad 20260902 prefix: rejected because exact task/report branch repo base fencing passes positive and negative controls
  - old a746dbfaa generation remains sufficient for Wave 3: rejected because trusted main changed the production Qwen sensor contract that Wave 3 must retest
changed_paths:
  - docs/agents/tasks/active/OTC-20260902-vision-p2-vision-reconciliation.md
  - docs/agents/reports/OTC-20260902-vision-p2-vision-reconciliation.md
  - tools/tibia_re_control_center/vision_p2_trusted_composition.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - .github/workflows/tibia-re-control-center-core.yml
validation:
  - command: Wave 2 reconciliation edge bridge session trusted composition matrix
    result: PASS
    evidence: 90 tests OK on post-Qwen sync tree
  - command: runtime admission plus current-client fence
    result: PASS
    evidence: 14 tests OK and TRACK_A_CANONICAL_CURRENT_CLIENT_FENCE=PASS
  - command: Qwen focused schema contract plus frozen vision benchmark
    result: PASS
    evidence: 3 focused tests and 34 benchmark tests OK
  - command: py_compile Ruff I/F YAML parse and git diff check
    result: PASS
    evidence: all returned zero
  - command: exact Package A boundary positive and negative controls
    result: PASS
    evidence: exact branch repo new base returns RC 0; wrong base wrong branch and fork each return RC 1
  - command: Track A runtime governance plus checkpoint validator
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true and checkpoint validated
blockers:
  - final exact-head GitHub Actions for the post-Qwen synchronized generation are pending
next_action: push the post-Qwen synchronization checkpoint and require terminal exact-head GitHub Actions before fresh coordinator ACCEPT and Wave 3 restack
```
