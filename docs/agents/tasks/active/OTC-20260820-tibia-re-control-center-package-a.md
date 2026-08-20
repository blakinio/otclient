---
task_id: OTC-20260820-tibia-re-control-center-package-a
status: waiting
agent: ChatGPT
project_lane: otclient
lane: P1-CONTROL-CORE
track_id: official-client-re
task_kind: implementation
phase: validate
risk: medium
branch: feat/OTC-20260820-tibia-re-control-center-package-a
base_branch: main
created: 2026-08-20T14:18:00+02:00
updated: 2026-08-20T21:37:00+02:00
initial_base_sha: 8620310a91c53e63abc0bf51fe40bdb8a3ee6cef
related_pr: 628
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
gameplay_allowed: false
transaction_authorized: false
network_listener_allowed: false
official_client_access: false
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
execution_mode: remote_desktop_plus_github
execution_reason: GitHub connector plus isolated GitHub-hosted validation preserves the in-progress branch after local terminal access became unavailable
execution_budget_minutes: 120
execution_budget_reason: cohesive Package A implementation, exact-head validation, independent validator role, merge and mandatory archive closeout
invocation_started_at: 2026-08-20T14:18:00+02:00
last_progress_at: 2026-08-20T21:37:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final_exact_head_green_audit_blocked
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 2
stall_warnings: 0
heavy_validation_runs: 2
decomposition_decision: phased
decomposition_reason: one cohesive Package A control-core with shared safety state; split would duplicate contracts and ledgers
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: medium
validation_level: full
complete_user_facing_feature: false
delegated_repair_task: OTC-20260820-tibia-re-control-center-package-a-p1-isolation
owned_paths:
  - .github/workflows/tibia-re-control-center-core.yml
  - docs/agents/tasks/active/OTC-20260820-tibia-re-control-center-package-a.md
  - docs/agents/tasks/archive/OTC-20260820-tibia-re-control-center-package-a.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - tibia_re_control_center
reuses:
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_POLICY_BOUNDARY_V1.md
  - repository Python unittest/tooling conventions
depends_on:
  - merged PR #613 Control Center hardened contracts
  - merged PR #627 terminal hardening lifecycle closeout
blocks:
  - Package B Control API/browser/CLI
cross_repository_tasks: []
---

# TIBIA RE Control Center Package A — control-core

## Delivery classification

```yaml
feature_scope:
  type: backend_only
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
implementation_status: package_a_implemented_validating
user_facing_feature_complete: false
missing_consumers:
  - Package B local Control API/browser/CLI
  - Package C accepted Surveyor read-only integration
  - Package D separately admitted official Track A mutation adapter
  - Package E separately governed Oteryn-v2 adapter
```

## Objective

Implement Package A from the accepted current-main Control Center contracts without inventing new authority or touching a live official Tibia runtime. The package is a reusable deterministic Python control core plus fake adapter/durability harness and mandatory falsification tests.

## Scope boundary

This task is permanently `runtime_access:none`. It does not connect to KasmVNC, inspect or mutate an official-client process, use credentials, login, send GUI/gameplay input, create a network listener, or claim Official Tibia capability evidence. Fake adapter success is test evidence only.

No Control API/browser/CLI listener is implemented here. No policy/Ollama loop is implemented. No Surveyor integration is implemented. No Official Tibia or Oteryn mutation adapter is implemented.

## Acceptance criteria

- [x] Typed Scenario/Execution/Adapter/Artifact/Comparison/Policy-boundary-compatible models and version negotiation fail closed.
- [x] Bounded JSON/YAML Scenario v1 parsing, duplicate/tag/alias rejection, semantic validation, deterministic JCS/SHA-256 hashes and stable step IDs.
- [x] Typed SideEffectBudget, AbortCondition, SemanticFieldPath, closed semantic references and every v1 action-family parameter schema.
- [x] Deterministic EffectBound model and refusal when hard effect cannot be bounded.
- [x] Manual clock, backend epoch/control generation, active-backend marker, durable STOP/reset/recovery and no fresh runtime window after restart.
- [x] MutationCoordinator serializes mutation, enforces action idempotency, one-shot dispatch commit and external-effect budget transitions.
- [x] Dispatch durability failure/timeout prevents effect; post-commit crash/effect uncertainty becomes conservative AMBIGUOUS/no auto-retry.
- [x] STOP-vs-commit and STOP-while-authority-waiting interleavings are deterministic and fail closed.
- [x] Recorder preserves source/ingest clocks, causal metadata and late-event immutability without claiming causality from ingestion order.
- [x] Construction-time privacy excludes secret, arbitrary exception/debug, environment values and unsafe screenshots from normal artifacts.
- [x] Artifact staging/finalization, hashes, safety-state precedence, incomplete crash behavior and append-only supplements satisfy Artifact v1 Package A scope.
- [x] Pure Comparison v1 profile/result types and coverage-gap semantics are implemented for Package A.
- [x] Deterministic fake adapter supports passive/invasive capture boundary and emergency-stop no-mutation invariant.
- [x] All 65 mandatory Package A tests in `TIBIA_RE_CONTROL_CENTER_MVP.md` are represented by focused automated tests.
- [x] Exact Package A fake one-step journey is covered as non-UI E2E.
- [x] No concrete official-client runtime or operator-facing adapter-bypass interface exists.
- [x] Full exact-head validation and changed-file self-review are clean; module catalogue/changelog/task are current.
- [ ] Fresh independent exact-head validator role has no open material findings.
- [ ] Required exact-head GitHub checks pass, review threads are resolved and implementation PR reaches an intentional terminal state.
- [ ] Post-merge archive closeout records terminal evidence and releases ownership.

## Validation evidence so far

- Interim head `a4a9a02168a3bfc39a498be01a117f5f4564ff69`, workflow run `32381505315`: compile PASS; 76/76 focused tests PASS; explicit mandatory inventory 65/65 PASS; `runtime_access:none` AST boundary PASS.
- Track A governance run `32381504968`: fresh admission behavior audit PASS; deterministic task policy failed only because the original task file carried a UTF-8 BOM before YAML front matter. The subsequent checkpoint removed the BOM and preserved the full `runtime_access:none` admission record.
- Candidate head `9a959438ad6eaea49cb1e21bcd081bd094c27c29`, Package A workflow run `32395883708`: both `Package A deterministic core` and `Fresh Package A falsification audit` PASS; 76/76 focused tests PASS; explicit mandatory inventory 65/65 PASS; Ruff 0.16.1 PASS; `git diff --check` PASS; `PACKAGE_A_CHANGED_PATHS=17_DECLARED_ONLY`; `PACKAGE_A_FRESH_AUDIT=PASS`; `MATERIAL_FINDINGS_OPEN=0`; `RUNTIME_ACCESS_NONE=PASS`; `FAKE_ONE_STEP_E2E=PASS`.
- The same candidate exact head also has Track A runtime governance run `32395883691` PASS, Track A canonical-live governance run `32395883700` PASS and repository CI run `32395883738` PASS.
- Full 17-file PR diff was re-read after reconciliation. No material self-review finding remains. One unrelated pre-existing changelog line is normalized from mojibake (`Âµ`/`Ã—`) to the intended UTF-8 glyphs (`µ`/`×`); this is documentation-only and has no runtime behavior impact.
- Current `main@2a2b607bf11818cdd6bfc4377c932a170e4be2a9` was reconciled as the second parent of merge commit `9e188ff1d5d377d81c80ceb45791868a9f31e067`; current-main Surveyor/Track A semantics were preserved, PR #628 became mergeable, and the Package A catalogue/changelog union was restored in `f3b5783984684b47a23fb2ab9a259c4541535e00`.
- Codex review at `eddc54d13d76b983d6bf82192dda90d2444ffe09` found four P1 defects (failed-STOP reset reopening, missing final abort revalidation, callback identity/session fencing, and clean-shutdown/in-flight fencing). Successor `eb12586a9f0e8cb0c5ccefd64158bd53a23bca59` repairs all four and removes the one-shot repair workflow/script.
- After reconciling current `main@9376ad6ff13924628749a186f2586d438f2c60bd`, local predecessor `6f37fde3ef60a4c364f2c5b7ad084e47a870d6f1` passes 80/80 focused tests, `audit_package_a.py`, `audit_package_a_p1.py`, Ruff and `git diff --check`; all four P1 falsification checks report PASS. Fresh exact-head independent review and GitHub CI remain required after this checkpoint commit.

- Fresh Codex review of `0fa92442675619305f4a8487e9403fb8bb5c920f` found four additional P1 defects (mutation-run admission race, failed-STOP cleanup early return, callback/reconciliation race, scenario artifact secret persistence) and one P2 abort-reason loss. Repair heads `6224791faf4635cf9f69aba4980845e595b6186b` / `00d0acaa6d95158080f8d191562eeff874605122` address all five. Local exact-code validation passes 84/84 focused tests, compileall, `audit_package_a.py`, expanded `audit_package_a_p1.py`, Ruff and `git diff --check`; the expanded audit reports PASS for mutation-run admission serialization, failed-STOP cleanup, callback/reconciliation serialization, scenario-artifact privacy, and final-gate abort-reason preservation. Exact-head Package A and both Track A governance workflows also PASS; repository CI run `32406952139` was still in progress at the last observation. A fresh independent review of the final metadata successor remains required.


- Exact-head `e2fb467bfd57120041ec7528e0cdc6ca067f48b2` passed Package A run `32407757611`, Track A runtime governance `32407757604`, Track A canonical-live governance `32407757556` and repository CI `32407757969`.
- Fresh Codex review anchored to repaired code head `00d0acaa6d95158080f8d191562eeff874605122` opened four additional P1 findings that remain applicable to the metadata-only successor: STOP cleanup/reset overlap, missing post-final-hook dispatch-fence revalidation, caller-trusted ActionRequest hash before deduplication, and unscanned adapter/runtime/session artifact metadata. These are review threads `PRRT_kwDOTVmdjs6a7eTJ`, `PRRT_kwDOTVmdjs6a7eTO`, `PRRT_kwDOTVmdjs6a7eTS`, and `PRRT_kwDOTVmdjs6a7eTW`.
- The prior five repaired findings are resolved and 84/84 focused tests plus both Package A audits remain PASS, but the four new P1 findings block Ready/merge. The task has reached `repair_cycles_for_current_gate: 3`; repository anti-stall policy forbids a fourth repair cycle in this task without an explicitly authorized fresh isolation task.

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 7
  session_id: package-a-audit-blocked-20260820-2123
  session_started_at: 2026-08-20T21:19:00+02:00
  checkpointed_at: 2026-08-20T21:23:56+02:00
  last_progress_at: 2026-08-20T21:23:56+02:00
  phase: audit
  validated_predecessor_head: e2fb467bfd57120041ec7528e0cdc6ca067f48b2
  pull_request: 628
  active_operation: blocked after third independent-audit repair cycle; preserve Draft PR and exact findings
  external_run_ids:
    - 32407757611
    - 32407757604
    - 32407757556
    - 32407757969
  operation_started_at: 2026-08-20T21:23:56+02:00
  wait_deadline_at: null
  check_generation: final_exact_head_green_audit_blocked
  checks_used: 2
  status: waiting
  safe_to_resume: false
  resume_condition: delegated repair task OTC-20260820-tibia-re-control-center-package-a-p1-isolation reaches terminal PASS
  next_action: reconcile the delegated isolation result into PR #628 closeout after the child task is terminal
```
