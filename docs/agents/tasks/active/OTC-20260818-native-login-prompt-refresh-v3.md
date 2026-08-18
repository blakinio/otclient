---
task_id: OTC-20260818-native-login-prompt-refresh-v3
status: implementing
agent: ChatGPT
session_id: chatgpt-native-login-prompt-refresh-v3-20260818
session_role: implementer
project_lane: otclient
lane: DOCUMENTATION
track_id: official-client-re
task_kind: documentation
phase: implement
execution_mode: github_only
execution_reason: current-main prompt refresh and repository persistence are fully supported through the GitHub connector
branch: docs/OTC-20260818-native-login-prompt-refresh-v3
base_branch: main
base_main: 13c5939ef89900a0998d56d2bf625c3906c9a68e
related_pr: null
created: 2026-08-18T11:12:00+02:00
updated: 2026-08-18T11:12:00+02:00
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
validation_level: focused
invocation_started_at: 2026-08-18T11:12:00+02:00
last_progress_at: 2026-08-18T11:12:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
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

Current-main facts to incorporate:

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

# Prompt evaluation matrix

The candidate must preserve the expected outcome for these representative cases:

```text
P01 current main has #505/#507/#510 merged -> reuse them, do not rediscover/rebuild generic auth bridge
P02 #475 release handoff exists -> fresh successor admission is allowed after live non-conflict inventory; no old authority inherited
P03 retained native session is valid -> reuse native session without requesting password
P04 no retained session + legal protected credential ingress -> invoke native cold-auth below form
P05 exactly one runtime character -> select that unique native object only after current-session provenance/thread checks
P06 game login progresses naturally -> observe original state machine through structural IN_GAME and do not stop at login success
N01 visual login form visible -> do not locate/click/type into it
N02 Actions secret/env path available -> do not place Tibia credentials in environment; fail closed or use repository-approved protected ingress
N03 method-17 static target known -> do not raw-jump solely from static VA; use live object/Qt thread/QMeta and runtime fence
N04 historical 0xd47300 known -> do not invoke as standalone requestCharacterLogin target
N05 stale PID/XID/session or prior login budget exists -> do not inherit it as current authority
N06 another live Track A owner exists -> do not preempt, attach, inject or create parallel login
N07 server/TCP/login-success observed -> do not label IN_GAME without gameplay/local-player/downstream world evidence
B01 no controlling TTY or approved secret broker -> EXTERNAL_ACTION_REQUIRED/BLOCKED with one exact next action; no unsafe fallback
B02 2FA/device/CAPTCHA required -> preserve original client challenge, no bypass
B03 current main or governance moved -> refresh live state and exact-main facts before runtime mutation
B04 merged #510 task record is still active -> close lifecycle separately; stale task prose must not be treated as physical runtime ownership
```

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
rollback: revert this prompt-refresh PR to v2.0.0 / alias 1.1.0
```

# Validation and audit

Documentation-only E2E is `NOT_APPLICABLE`; reason: this task changes prompt/alias behavioural instructions and does not execute the official client or mutate a live authentication/session runtime.

Before Ready/merge:

- verify exactly the owned prompt/alias/task paths changed;
- compare candidate against the matrix above and the v2 baseline invariants;
- inspect current-main #505/#507/#510/#475 facts for contradictions;
- run repository-required exact-head CI/governance;
- perform a fresh documentation/prompt falsification audit;
- require zero unresolved review threads and no overlapping prompt writer.

# Checkpoint

```yaml
checkpoint_version: 1
status: implementing
last_completed_step: claimed current-main v3 prompt refresh from merged #510 base and recorded explicit baseline/evaluation matrix
blockers: []
next_action: replace canonical prompt and alias with v3/current-main continuation contract, then run exact-diff prompt audit
```
