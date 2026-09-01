---
task_id: OTC-20260901-vision-p2-coordinator
status: validating
agent: ChatGPT
session_role: programme_coordinator
worker_alias: OTC-VISION-P2-COORDINATOR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: coordination
phase: wave_1_ci_repair
branch: ci/OTC-20260901-vision-p2-package-a-path-boundary
base_branch: main
base_main: 2df0aa64c4578832f41acbf66339310c07724fb4
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T18:15:30+02:00
risk: high
execution_mode: chat_github
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
prompting_standard_version: 2.1
policy_version: 2
runtime_access: none
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
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
worktree: NOT_APPLICABLE_GITHUB_ONLY
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - .github/workflows/tibia-re-control-center-core.yml
modules_touched:
  - github_actions_package_a_governance
reuses:
  - existing Package A falsification audit
  - existing Phase 2 programme ownership contract
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #825 merged Wave 1 dispatch checkpoint
  - PR #831 merged Codex routing policy
  - PR #834 merged Codex routing policy closeout
blocks:
  - PR #826 exact-head Package A revalidation
  - PR #828 exact-head Package A revalidation
  - PR #830 exact-head Package A revalidation
related_prs:
  - PR #824 merged Wave 0 coordinator cleanup
  - PR #825 merged Wave 1 coordinator dispatch
  - PR #826 runtime-admission worker Draft
  - PR #827 capture-edge worker Draft
  - PR #828 runtime-signals worker Draft
  - PR #829 edge-transport worker Draft
  - PR #830 control-bridge worker Draft
  - PR #832 closed superseded coordinator repair Draft
  - PR #833 active coordinator Package A repair
current_blocker: PR_833_FINAL_EXACT_HEAD_VALIDATION
next_action: validate PR #833 exact head on current main; if Package A, CI / Required, Track A governance, self-hosted boundary and PR hygiene are green and main is unchanged, squash-merge #833 and refresh affected worker lanes
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T18:15:30+02:00
ci_checks_for_current_head: 0
ci_check_generation: current-main-final
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# OTC Vision Phase 2 read-only programme coordinator

## Objective

Coordinate Phase 2 read-only runtime-edge integration, independently classify workers, repair shared governance blockers, serialize any later real read-only observation, and drive the programme through exact-head integration/E2E closeout without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- current Git/GitHub/runtime state and stricter trusted-base governance override stale historical prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:15:30+02:00
head: d37c33df3453853aec49ed91afd38379e266dc69
head_semantics: current-main repair commit before this checkpoint-only docs commit
branch: ci/OTC-20260901-vision-p2-package-a-path-boundary
pr: 833
status: validating
context_routes: [phase-2-read-only-coordination, track-a-governance, ci-repair]
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - .github/workflows/tibia-re-control-center-core.yml
proven:
  - PR 826 static runtime-admission implementation is complete at 0dbd823f6c89895e919f9bc07f7e99ecac9f31a6 with focused 14/14 PASS, Ruff PASS and compileall PASS; its Package A failure is the shared durable-doc path defect and later serialized read-only observation remains required.
  - PR 828 at 426a9aaf15c440531fb9d0bc315f382bf5465ea0 has CI, Track A governance and Package B SUCCESS plus Package A deterministic core SUCCESS; its Fresh Package A failure is the same shared durable-doc defect.
  - PR 827 at 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38 passed CI/governance, but coordinator independent review found its public empty secret policy can self-certify secret_safe and persist an unmasked frame without machine-checkable proof that the surface is secret-free; PR 827 was returned for repair in comment 5496909848.
  - PR 830 advanced to fc684f62ab9b4e79e23fab58c6fda942b8b969be; its UTF-8 BOM is removed (task bytes now begin directly with ---) and exact-head Track A governance is SUCCESS. Its Package A failure remains the shared old-workflow defect.
  - coordinator independent review also found PR 830 currently treats caller-declared runtime_access read_only and opaque runtime refs as sufficient rather than consuming validated #826 runtime admission and #828 runtime-signal contracts; PR 830 was returned for integration repair in comment 5496928156.
  - PR 829 remains dispatch-only at 2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b with no implementation handoff.
  - Package A root cause is the changed-path allowlist omitting mandatory OTC-20260901-vision-p2 task/archive/report namespaces; coordinator repair adds only those three programme-scoped prefixes.
  - Draft #832 was closed only because the connected Draft-to-Ready mutation fails on Repository.fullDatabaseId; non-draft replacement #833 uses the same bounded repair.
  - repair content has repeatedly passed Package A, CI, Track A governance and self-hosted boundary on exact heads c9c8fe0430d0a0ba2297a53db84d3f4840031d58 and 4f57c1cb4a406c226682325aeb761c12be14aadc.
  - repository ruleset 18840974 requires strict up-to-date status context CI / Required, linear history, squash merge and resolved review threads.
  - first merge attempt on 4f57c1cb4a406c226682325aeb761c12be14aadc was rejected despite CI / Required 99930254269 SUCCESS because GitHub classified the merge-commit restack as behind under the strict rule.
  - branch was rewritten as single-parent on main 11bb95eb, then main independently advanced through non-overlapping lifecycle PR #834 to 2df0aa64c4578832f41acbf66339310c07724fb4.
  - PR #834 changes only the Codex routing-policy task active-to-archive lifecycle and does not overlap either repair path.
  - branch has now been rewritten again as single-parent repair commit d37c33df3453853aec49ed91afd38379e266dc69 directly on current main 2df0aa64c4578832f41acbf66339310c07724fb4 with the same verified two-file repair content.
  - no Phase 2 live runtime observation, credentials, GUI input, process control, process-memory access, payload capture or physical action occurred.
derived:
  - PRs 826, 828 and the Package A portion of 830 share one coordinator-owned deterministic governance blocker.
  - PR 827 and PR 830 have separate worker-owned/integration findings that remain real after the shared workflow repair.
  - old worker check failures must be rerun against repaired trusted main; #833 success cannot retroactively change an old exact-head result.
unknown:
  - exact final PR #833 head created by this checkpoint commit and its fresh final GitHub Actions results.
  - future worker repair outcomes for #827/#830 and implementation outcome for #829.
  - current Synology/Kasm target identity/availability for any later serialized read-only observation.
conflicts: []
first_failure:
  marker: PACKAGE_A_CHANGED_PATHS_REJECT_PHASE2_DURABLE_DOCS
  evidence: PR 826/828/830 Fresh Package A logs reject mandatory Phase 2 durable paths while deterministic implementation jobs succeed.
rejected_hypotheses:
  - unchanged worker Package A reruns can fix the blocker: rejected because path classification is deterministic.
  - workers may edit shared workflow outside owned paths: rejected by ownership contract.
  - PR 830 governance and Package A failures were one cause: rejected by independent BOM byte proof and separate Package A log.
  - green CI workflow alone proves strict mergeability: rejected by ruleset readback and first merge rejection.
changed_paths:
  - .github/workflows/tibia-re-control-center-core.yml
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: exact worker Package A log inspection
    result: PASS
    evidence: PR 826/828/830 failures are path-boundary-only; Package A deterministic core succeeds.
  - command: PR 830 BOM revalidation
    result: PASS
    evidence: current task base64 begins LS0t (---), not 77u/; Track A governance run 33530326530 SUCCESS.
  - command: independent PR 827 requirements/diff review
    result: FAIL_MATERIAL_FINDING
    evidence: empty secret policy can persist unmasked bytes and set secret_safe=True without a proof object; returned in comment 5496909848.
  - command: independent PR 830 integration review
    result: FAIL_MATERIAL_FINDING
    evidence: read_only bridge admission is caller-string driven and runtime states accept opaque refs rather than validating #826/#828 producer contracts; returned in comment 5496928156.
  - command: inspect ruleset 18840974 and exact required check
    result: PASS
    evidence: strict CI / Required plus linear/squash/review-thread rules are active; prior exact check CI / Required 99930254269 was SUCCESS but branch was behind.
  - command: compare PR #834 to repair scope
    result: PASS
    evidence: #834 changes only docs/agents/tasks/{active,archive}/OTC-20260901-codex-model-effort-routing-policy.md.
  - command: current-main single-parent restack
    result: PASS_PENDING_FINAL_CI
    evidence: d37c33df3453853aec49ed91afd38379e266dc69 has sole parent 2df0aa64c4578832f41acbf66339310c07724fb4 and preserves exact repair blobs.
blockers:
  - final exact-head PR #833 checks and hygiene are pending on current main.
next_action: validate PR #833 exact head on current main; if Package A, CI / Required, Track A governance, self-hosted boundary and PR hygiene are green and main is unchanged, squash-merge #833 and refresh affected worker lanes.
```

## Wave 1 live ledger

| Alias | Draft PR | Current durable state | Coordinator classification |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | static implementation complete; shared Package A blocker; later serialized read-only observation required | `RETURN_FOR_EVIDENCE` after shared repair |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | static implementation published; independent secret-safety finding open | `RETURN_FOR_REPAIR` |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #828 | static implementation published; shared Package A blocker | `RETURN_FOR_REVALIDATION` after shared repair |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 | dispatch-ready only; no implementation handoff | pending worker execution |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 | BOM fixed; shared Package A blocker plus missing validated #826/#828 producer binding | `RETURN_FOR_REPAIR` |

Actual Official Tibia runtime observation remains serialized to one worker and requires a fresh persisted `read_only` admission before observation. Mutation, credentials, login/relogin, gameplay, GUI/anti-idle input, process control, process memory, network payload capture and physical actions remain forbidden with budget/count `0/0`.
