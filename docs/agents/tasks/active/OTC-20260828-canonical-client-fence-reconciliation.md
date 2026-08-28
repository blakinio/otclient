---
task_id: OTC-20260828-canonical-client-fence-reconciliation
status: review_pending_final_restack
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: review
branch: fix/OTC-20260828-canonical-client-fence-reconciliation
base_branch: main
base_main: 009c148a8ba7406acf07c5ce7f95a8f95f69b992
created: 2026-08-28T22:00:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
physical_e2e_required: false
implementation_authorized: true
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md
  - docs/agents/decisions/ADR-0002-track-a-canonical-client-fence-reconciliation.md
  - docs/agents/evidence/OTC-20260828-canonical-client-fence-reconciliation/**
  - docs/agents/tasks/active/OTC-20260828-canonical-client-fence-reconciliation.md
modules_touched:
  - track-a-canonical-live-runtime
  - track-a-runtime-agent-admission
reuses:
  - merged canonical lease guard-run supervisor
  - merged current Kasm existing-runtime adoption probe
  - PR #754 trusted exact-current client fence
  - PR #760 gameWindowState preflight blocker evidence
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Implement a narrow, reviewed, metadata-only canonical registration recovery for the exact predecessor fence left behind after the repository current-client authority advanced in PR #754.

The repository implementation phase is strictly `runtime_access: none`. It must not inspect or mutate the live official client or canonical registration. The implementation becomes eligible for live use only after squash merge to trusted protected `main` and a separate trusted-main recovery-admission checkpoint.

# Root cause

The gameWindowState memory-free preflight run `33193448068`, job `98924502254`, stopped at canonical registration resolution with `REGISTRATION_CLIENT_VERSION_MISMATCH`. No process-memory observation occurred.

Current transition `_read()` correctly rejects any registration outside the current exact fence. Existing rebind, stale-registration recovery and boot-epoch recovery all begin from that strict read and intentionally do not authorize exact-client fence replacement. Adoption/bootstrap cannot be substituted because the authoritative registration is present.

# Design boundary

The implementation must follow `TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md` and ADR-0002:

- exact source fence only: `15.32 / 52109920 / ed5469b9...`;
- exact target fence only: `15.32.75d4a0 / 52105824 / d1a16819...`;
- source must be fail-closed `existing_runtime_adoption_v1`;
- target must be proven by three stable current Kasm adoption probes;
- same canonical Docker container name/display/remote-view endpoint/mapping;
- current controller generation newer than source registration generation binding;
- atomic `registration_generation + 1` replacement and exact-own-record rollback;
- result forced to `state: UNKNOWN`;
- execution only as a finite child under reviewed canonical lease `guard-run`;
- no client launch/stop/signal/restart/attach/injection/input/login/credentials/gameplay/process-memory observation.

# TDD

Primary implementation RED is captured at exact test/design-only head `95a49119f8f8866c9761bcb587ca62719f416dc1`, workflow run `33195284267`, job `98930734507`. The focused step failed because every test reached the intentional pre-implementation assertion `canonical client-fence reconciliation implementation missing`; the trusted-main live job was skipped.

Primary implementation GREEN was established at `fe998516ecfd816fb053e0b56158d6aa7f9466e1`, run `33195900581`, job `98932830802`, with the focused contract, existing canonical transition, Kasm adoption probe and Track A governance green. Same-head Track A governance run `33195900573` passed jobs `98932830815` and `98932831016`.

Independent merge review then found that a future live workflow must not rely on an implementation task that still says `runtime_access: none`. A second test-first admission RED was captured at `e45da7114663d9276ce9225889ae1aa4ae746dea`, run `33196302067`, job `98934193806`: the new explicitly named pre-Gate-A client-fence recovery fixture was rejected solely because the global validator required `registration_lease_generation` to be a positive integer instead of allowing fresh under-lock discovery. The companion legacy recovery test still rejected the same UNKNOWN generation checkpoint, proving that a narrow mode-specific rule can be added without weakening old recovery.

The governance fix now reserves UNKNOWN generation discovery only for:

```yaml
runtime_access: canonical_recovery
recovery_mode: client_fence_reconciliation_v1
client_fence_reconciliation_contract: TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
```

That checkpoint grants no registration write. The helper must acquire current authority, prove a strictly newer controller generation, prove the exact approved predecessor and stable exact-current singleton target under the canonical guard, and emit concrete under-lock Gate-A/target-uniqueness evidence before atomic commit.

# Concurrent-main reconciliation

Protected `main` advanced during implementation through independent current-login-field6 work (#758 and #762). Those changes are task-owned `ephemeral_isolated` work and do not overlap canonical registration/lease authority.

Fresh exact-head verification after the first restack exposed a stale branch-name assumption in the pre-existing `Track A canonical current-client fence` workflow: run `33199411721`, job `98944789902` passed its focused fence/runtime component tests but rejected this PR because the governance invocation was still hard-coded to the historical #754 branch. The one-line repository-only repair was independently verified and squash-merged as #765, advancing protected `main` to `009c148a8ba7406acf07c5ce7f95a8f95f69b992`. The reconciliation branch must be restacked on that exact main and all exact-head checks rerun before merge.

# Live-use rule

The workflow exposes a post-merge owner-authored exact issue-comment trigger for the one metadata reconciliation, but it refuses to proceed unless trusted `main` contains the explicit pending `client_fence_reconciliation_v1` admission above and the global admission validator accepts that task state.

This implementation PR itself stays `runtime_access: none` and must never invoke the live trigger. After this PR merges, a **separate repository-only admission PR** must switch this task to the exact pending recovery admission; that PR must itself merge green before the live trigger is used. Dynamic generation values remain UNKNOWN until the guarded live worker freshly proves them.

# Acceptance

1. Correct implementation RED is captured before production helper exists.
2. Explicit recovery-admission RED is captured before global governance is changed.
3. Focused reconciliation tests pass on the final exact implementation head, including the legacy no-weakening check and exact contract binding.
4. Existing canonical transition, Kasm adoption and Track A agent runtime governance tests remain green.
5. The helper contains no process-control, memory-observation, input, login or credential primitive.
6. Exact changed scope is reviewed and protected-main freshness is checked immediately before squash merge.
7. Live reconciliation runs only after merge plus a separately merged trusted-main recovery-admission checkpoint and produces a precise PASS or fail-closed blocker.
8. The gameWindowState memory-free preflight is rerun after successful reconciliation; owner UI interaction remains forbidden until that preflight reports READY.

next_action: clean-restack this implementation onto protected `main@009c148a8ba7406acf07c5ce7f95a8f95f69b992`, obtain fresh exact-head GREEN for reconciliation/current-fence/governance/CI, then safe-squash-merge PR #763. After merge create and merge the separate pending live-admission checkpoint before any reconciliation trigger.
