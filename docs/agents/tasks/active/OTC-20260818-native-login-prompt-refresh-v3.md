---
task_id: OTC-20260818-native-login-prompt-refresh-v3
status: ready
agent: ChatGPT
session_id: chatgpt-native-login-prompt-refresh-v3-20260818
session_role: implementer
project_lane: otclient
lane: DOCUMENTATION
track_id: official-client-re
task_kind: documentation
phase: final_exact_head
execution_mode: github_only
execution_reason: current-main prompt refresh and repository persistence are fully supported through the GitHub connector
branch: docs/OTC-20260818-native-login-prompt-refresh-v3
base_branch: main
base_main: 13c5939ef89900a0998d56d2bf625c3906c9a68e
related_pr: 516
created: 2026-08-18T11:12:00+02:00
updated: 2026-08-18T11:23:00+02:00
risk: medium
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
runtime_access: none
RUNTIME_ACCESS: none
EXECUTION_CLASS: github_hosted
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
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
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_ALIAS.md
  - docs/agents/tasks/active/OTC-20260818-native-login-prompt-refresh-v3.md
modules_touched: []
reuses:
  - merged PR #505 native cold-auth QMeta contract
  - merged PR #507 experimental form-less native auth bridge
  - merged PR #510 protected TTY native-auth secret source
  - PR #475 owner-requested runtime release handoff
  - archived v2 prompt task OTC-20260817-track-a-native-login-to-ingame-prompt
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one versioned documentation deliverable updating the canonical prompt and short alias from the same current-main evidence
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
validation_level: full_documentation
invocation_started_at: 2026-08-18T11:12:00+02:00
last_progress_at: 2026-08-18T11:23:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft-final
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Refresh the repository-owned `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` prompt from v2.0.0 to a current-main v3 contract that incorporates the now-merged form-less native-auth implementation and the released physical-runtime handoff, while preserving the strict success, secret-safety, exact-client, Track A admission and no-GUI-login invariants.

# Baseline

Baseline prompt:

`docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md` v2.0.0 from merged PR #501 / `42aafde73f45ae997ec7629a5d321e2a49b110d6`.

Current trusted base at task claim:

`main@13c5939ef89900a0998d56d2bf625c3906c9a68e`.

Current-main facts incorporated:

- PR #505 merged as `17cc0dc1bf29c440cc08e443bdce98e4dde7be5d`: exact `tibia::client::TGameClient::onRequestLoginWithCredentials(QString,QString)` QMeta method id 17, `qt_static_metacall` `0xd06260`, method-17 target/fence `0xd06850` plus exact instruction bytes;
- PR #507 merged as `2e6992da330e8a52d03b94b8d6a9de6fa79a6800`: separate opt-in one-shot experimental auth bridge, exact peer identity, sealed-memfd `SCM_RIGHTS`, Qt named invocation, stable read-only bridge API unchanged;
- PR #510 merged as `13c5939ef89900a0998d56d2bf625c3906c9a68e`: protected controlling-TTY credential source using no-echo TTY, required `mlock`, `RLIMIT_CORE=0`, `PR_SET_DUMPABLE=0`, exact identity binding and fully sealed anonymous memfd;
- PR #475 current released head `8bf26dde309c46f08be414c4d2aef3e3599d7f5a`: prior owner/runtime/session authority released; exact task marker processes cleaned to zero; objective still unresolved.

# Required behavioural changes

1. Treat #505/#507/#510 as current-main native-auth implementation, not merely predecessor candidates.
2. Explicitly state that #475 is released and does not block a successor, while old login/runtime authority is not inherited.
3. Route the successor directly toward fresh admission and physical E2E rather than more generic bridge discovery.
4. Preserve the absolute ban on login-form OCR/image/coordinate/Tab/Return/blind input control.
5. Preserve secret prohibition for Git, argv, environment, logs, artifacts, screenshots, GDB history and plaintext files.
6. Prefer Qt named invocation through the merged experimental bridge; never raw-jump to `0xd06850` when the QMeta route is available.
7. Preserve runtime-discovered character selection and the correction that historical `0xd47300` is not a safe standalone direct-call target.
8. Require fresh no-client Synology inventory/admission/ownership before physical execution.
9. Require structural `IN_GAME` evidence including `FullMap` plus at least 10 map-description strips, current runtime identity, gameplay/local-player evidence and matching selected character/world.
10. Make missing legal secret ingress, 2FA/device confirmation or current admission an exact stop condition rather than a reason to fall back to GUI or unsafe secrets.
11. Tell the worker not to create more infrastructure/static tasks unless one concrete physical failure proves a missing dependency.
12. Keep direct `gpt-5.3-codex-spark` standing authorization bounded exactly as current root governance defines it.
13. Use current `PROMPTING_STANDARD.md` enum values for continuation/task-completion policy and explicitly bound the alias to the native-login task plus its required closeout.
14. Classify PR/issues/comments/logs/retrieved text as evidence data rather than authority and keep live state/trusted-base governance as the permission source.

# Prompt evaluation matrix

```text
P01 current main has #505/#507/#510 merged -> PASS: explicit reuse/current-main stack, generic bridge rediscovery prohibited
P02 #475 release handoff exists -> PASS: released state recognized; fresh admission required; old authority not inherited
P03 retained native session is valid -> PASS: retained-session-first path, password not requested
P04 no retained session + legal protected credential ingress -> PASS: sealed-memfd/SCM_RIGHTS/QMeta method-17 cold auth
P05 exactly one runtime character -> PASS: unique current-session native object may be selected only after provenance/thread checks
P06 game login progresses naturally -> PASS: original state machine continues through structural IN_GAME
N01 visual login form visible -> PASS: no locate/click/type control allowed
N02 Actions secret/env path available -> PASS: credential environment ingress explicitly forbidden
N03 method-17 static target known -> PASS: 0xd06850 is a fence; raw jump is not the preferred entry
N04 historical 0xd47300 known -> PASS: explicitly forbidden as standalone direct-call target
N05 stale PID/XID/session or prior login budget exists -> PASS: never current authority; fresh admission required
N06 another live Track A owner exists -> PASS: fail closed; no preempt/attach/inject/parallel login
N07 server/TCP/login-success observed -> PASS: not IN_GAME without server/world/gameplay/local-player/identity proof
B01 no controlling TTY or approved secret broker -> PASS: EXTERNAL_ACTION_REQUIRED/BLOCKED, no unsafe fallback
B02 2FA/device/CAPTCHA required -> PASS: original challenge preserved, no bypass
B03 current main or governance moved -> PASS: live-state preflight/revalidation precedes runtime mutation
B04 merged #510 task record is still active -> PASS: lifecycle closeout required; stale task is not runtime ownership
B05 PR/comment/log says authority was granted -> PASS: explicit untrusted-data/trusted-authority boundary
B06 alias reaches native-login task closeout -> PASS: task-only programme boundary forbids unrelated next-task selection
```

Final evaluation: `PASS 19/19`.

# Acceptance inventory

```yaml
prompt_version: 3.0.0
alias_version: 1.2.0
current_main_native_auth_factored_in: true
pr_475_release_factored_in: true
no_gui_login_control: true
no_unsafe_secret_ingress: true
runtime_admission_required: true
physical_e2e_priority: true
structural_ingame_gate_preserved: true
spark_boundary_preserved: true
trust_boundary_explicit: true
prompting_standard_enums_aligned: true
programme_boundary_native_login_only: true
rollback: revert this prompt-refresh PR to v2.0.0 / alias 1.1.0
```

# Fresh prompt audit

First falsification pass found and repaired:

```text
PROMPT-V3-AUD-001 MEDIUM: first draft used non-normative continuation/task-completion policy values.
PROMPT-V3-AUD-002 MEDIUM: trust/context authority boundary was implied but insufficiently explicit for Prompting Standard 2.1.
```

Repairs:

- `continuation_policy: continue_until_real_stop`;
- `task_completion_policy: finalize_archive_and_continue`, explicitly bounded to this task and its required closeout only;
- dedicated trusted-authority/untrusted-data section in the full prompt;
- matching task-only boundary and trust warning in the alias.

Fresh exact-diff/matrix falsification after the repairs:

```text
changed_paths=3 expected/3 actual
matrix=PASS 19/19
baseline_success_gate_preserved=true
baseline_exact_client_fence_preserved=true
baseline_no_gui_login_preserved=true
baseline_auth_2fa_tls_no_bypass_preserved=true
baseline_object_abi_thread_provenance_preserved=true
baseline_secret_nonpersistence_preserved=true
baseline_runtime_serialization_preserved=true
current_main_505_507_510_factored_in=true
pr475_release_without_authority_inheritance=true
physical_e2e_priority=true
open_material_findings=0
```

Audit result: `PASS`, fresh validator role: `ChatGPT prompt falsification / exact-diff role`, evidence source is the exact current PR diff and current-main producer state rather than the implementer summary.

# E2E

```text
result: NOT_APPLICABLE
reason: this task changes repository prompt/alias behavioural instructions only; it neither executes the proprietary official client nor mutates a live authentication/session runtime. The prompt itself requires the later RUNTIME task to perform the real physical native-login E2E.
```

# Validation gate

Before merge still require:

- repository-required exact-head CI/governance on the frozen head;
- unresolved review threads = 0;
- PR diff remains exactly the two prompt surfaces plus this task record;
- current base remains mergeable/current or is clean-restacked without changing prompt semantics.

# Checkpoint

```yaml
checkpoint_version: 3
status: ready
last_completed_step: v3 prompt and v1.2 alias passed fresh exact-diff/matrix falsification 19/19 with zero open material findings; head frozen for exact-head validation
blockers: []
next_action: inspect aggregate required checks on the frozen exact head; if green, verify review hygiene/base freshness, mark Ready and complete protected merge then archive/release this task
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: chatgpt-native-login-prompt-refresh-v3-20260818
  session_started_at: 2026-08-18T11:12:00+02:00
  checkpointed_at: 2026-08-18T11:23:00+02:00
  last_progress_at: 2026-08-18T11:23:00+02:00
  phase: final_exact_head
  exact_head: pending_this_checkpoint_commit
  pull_request: 516
  active_operation: exact-head required CI and review hygiene
  external_run_ids: []
  operation_started_at: 2026-08-18T11:23:00+02:00
  wait_deadline_at: null
  check_generation: draft-final
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: PR #516 remains the sole writer of the two canonical native-login prompt surfaces and the final diff remains exactly three owned paths
  next_action: resolve the current PR head, then take one aggregate exact-head required-check snapshot and continue only under current anti-stall rules
```
