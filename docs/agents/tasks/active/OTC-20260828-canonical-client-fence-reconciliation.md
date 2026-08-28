---
task_id: OTC-20260828-canonical-client-fence-reconciliation
status: review_pending_merge
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: review
branch: fix/OTC-20260828-canonical-fence-unknown-remote-mapping
base_branch: main
base_main: 316842a95838b175135b7f48e0cb2bd745aecad8
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
  - PR #763 merged client-fence reconciliation implementation
  - PR #766 merged recovery admission
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Repair the exact fail-closed defect exposed by the first trusted-main client-fence reconciliation attempt, then re-admit and rerun that metadata-only reconciliation before returning to the gameWindowState readiness preflight.

This repair PR remains strictly `runtime_access: none`. It performs no live client or registration action and does not retain the prior temporary `canonical_recovery` authority while production code is being modified.

# Live failure

Trusted-main run `33200286357`, job `98947751420`, passed pending admission, deterministic pre-runtime verification, bounded `RECONCILE`, canonical lease acquisition/validation at live generation `40`, and Gate A. It then failed closed before any registration commit with:

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_ERROR=source_registration_remote_mapping_invalid
```

No process-memory observation, client mutation, GUI/input, login, credential or gameplay action occurred.

# Diagnosed defect

The canonical transition schema accepts `remote_view_mapping` in `{PROVEN, UNKNOWN}`. The historical predecessor Kasm adoption probe and the current exact Kasm adoption probe both emit:

```yaml
remote_view_endpoint: https://synology:6902/
remote_view_mapping: UNKNOWN
```

The v1 reconciliation contract requires the source and target to retain the same endpoint/mapping. The reconciliation helper alone incorrectly required the source mapping to be `PROVEN`.

# TDD repair

Exact RED head `9c0505ce184ebca402e94d0e6caef2bb7036974a`:

- run `33200847818`, job `98949632562` — expected FAILURE;
- 14 focused tests ran, 13 passed and exactly `test_reconciles_when_stable_remote_view_mapping_is_unknown` failed with the live error code;
- invalid source mapping remained rejected;
- live PR-event reconciliation was skipped.

Minimal implementation head `a88aff2fe4f8ebd773d1682328911abe42b81230` changes only the source mapping membership check from `PROVEN`-only to the canonical allowed set `{PROVEN, UNKNOWN}`. The existing exact fresh mapping equality check remains unchanged, so mapping drift still fails closed.

GREEN evidence before final restack:

- reconciliation run `33200969801`, job `98950035983` — SUCCESS, live job `98950037574` SKIPPED;
- Track A governance run `33200969705`, jobs `98950034608` and `98950034993` — SUCCESS;
- final checkpoint head `7c58c5ae109da0a5ba26be02fafc71886779e493`: reconciliation `33201111934 / 98950508557` SUCCESS, both governance jobs `98950507829` and `98950508207` SUCCESS, CI `33201112072` with syntax/actionlint and `CI / Required` `98950743450` SUCCESS.

Protected `main` then advanced independently through docs-only field6 admission #768 to `316842a95838b175135b7f48e0cb2bd745aecad8`; #768 changes only `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md` and does not overlap this repair. This branch must be clean-restacked on that exact main and freshly reverified before merge.

Durable detail: `docs/agents/evidence/OTC-20260828-canonical-client-fence-reconciliation/20260828-unknown-remote-mapping-repair.md`.

# Safety invariants retained

- exact predecessor fence only: `15.32 / 52109920 / ed5469b9...`;
- exact current fence only: `15.32.75d4a0 / 52105824 / d1a16819...`;
- source and target remain fail-closed `existing_runtime_adoption_v1`, `state: UNKNOWN`;
- same canonical Docker namespace, display, remote endpoint and remote mapping are required;
- all-running-Docker singleton inventory, fingerprint and X11 PID binding are required;
- active lease generation must be newer than the source registration binding;
- three stable current probes, atomic mode-0600 commit, exact-own-record rollback and `registration_generation + 1` remain required;
- no process memory, client process control/mutation, GUI/input, login, credentials, gameplay or payload capture.

# Post-merge rule

A successful repository repair does not itself authorize live recovery. After merge, a separate repository-only PR must restore the exact pending `client_fence_reconciliation_v1` admission with both generations and target uniqueness `UNKNOWN` before Gate A. Only then may one fresh owner-authored `RECONCILE_CANONICAL_CLIENT_FENCE` trigger be posted on #760.

After successful reconciliation, recovery authority must be released and `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION` rerun. No owner UI action is requested until that preflight explicitly reports READY.

next_action: clean-restack this repair onto protected `main@316842a95838b175135b7f48e0cb2bd745aecad8`, obtain fresh exact-head reconciliation/governance/CI GREEN, then safe-squash-merge PR #767. After merge create and merge a separate recovery re-admission checkpoint before one fresh live reconciliation trigger.
