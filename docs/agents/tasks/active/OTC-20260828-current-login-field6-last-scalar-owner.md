---
task_id: OTC-20260828-current-login-field6-last-scalar-owner
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: specify
branch: research/OTC-20260828-current-login-field6-last-scalar-owner
base_branch: main
base_main: 9b3c9fbd4bcac241082591508002ec766d42a1fa
created: 2026-08-28T19:22:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-current-login-field6-last-scalar-owner.yml
  - tools/tibia_re_current_login_field6_last_scalar_owner/**
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-last-scalar-owner.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-last-scalar-owner/**
modules_touched: []
reuses:
  - trusted-main promotion #747 current field6 producer boundary
  - trusted-main exact-current fence #754
  - closed source PR #751 scalar census as hypothesis input only
  - closed source PR #759 embedded login-handler layout
blocks:
  - Track B PR #284 CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN
---

# Objective

Independently re-derive and classify the only remaining non-rejected scalar `slot+0x60` site on exact public Linux Tibia `15.32.75d4a0`: FDE `0x16da340..0x16da7fc`, callsite `0x16da716`, reaching `edx=0`.

Recover the exact QMeta/RTTI owner of that FDE and the parent/member chain for `parent=[rbx+0x20]`, `receiver=[parent+0x10]`. Accept value `0` for the native login producer only if the owner/member construction proves that this exact child is `TLoginProtocolMessageHandler` and the virtual call resolves to its slot `+0x60 -> 0xe25620`. Otherwise reject the candidate and stop.

# Safety

Static GitHub-hosted analysis only. No official-client execution, login, credentials/session access, process memory, packet capture, gameplay, or proprietary binary upload.

# Acceptance

1. Re-assert exact current SHA/size and exact scalar instructions at `0x16da705`, `0x16da70e`, `0x16da713`, `0x16da716`.
2. Recover QMeta/RTTI owner of FDE `0x16da340..0x16da7fc` without global ranking.
3. Recover owner constructor/member `+0x20` identity and prove or disprove nested child `+0x10 == TLoginProtocolMessageHandler`.
4. Emit `FIELD6_VALUE_PROVEN=0` only on exactly one deterministic owner/member proof; otherwise `FIELD6_VALUE_UNKNOWN` with reason.
5. Sanitized structural JSON only; no Track B mutation/E2E from source task.

next_action: prove hosted contract RED before package/client acquisition, then implement focused owner/member discriminator.
