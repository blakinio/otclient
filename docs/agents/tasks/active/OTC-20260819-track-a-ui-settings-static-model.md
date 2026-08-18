---
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: investigating
phase: investigate
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_id: chatgpt-20260819-ui-settings-001
session_role: researcher
execution_mode: chat_github
execution_reason: bounded repository/static evidence discovery with GitHub connector; no live runtime required for this phase
decomposition_decision: phased
decomposition_reason: static phase recovered current-build settings/controller/persistence candidates; later reversible write/reload proof requires fresh live runtime admission
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
invocation_started_at: 2026-08-19T00:33:00+02:00
updated_at: 2026-08-19T00:56:00+02:00
last_progress_at: 2026-08-19T00:56:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final_checkpoint_pending_exact_head_validation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
session_rotation_count: 0
heavy_validation_runs: 3
stale_takeover_count: 0
human_interruptions: 0
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
---

# OTC-20260819 Track A UI/settings static model

## Invocation and authority

Owner invocation: `TIBIA-RE-UI-SETTINGS` autonomously.

Alias source used for this invocation: PR #543 head `981febf4bf8f60896c5c09f8f30ad2859f6ca67c`, `docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md`. PR #543 is Draft and is not represented as merged governance. The owner named the alias directly; trusted-base repository safety/admission rules remain authoritative and stricter rules win.

This researcher owns discovery/evidence only and stops repository delivery at Draft PR #544. It does not update the canonical coverage matrix and does not promote or merge its own claims.

## Objective and coverage

Primary alias ownership is `H01-H19`, with priority `H07-H14`.

This phase recovered a current-build, falsifiable static model for:

```text
UI/controller -> backing-model candidates -> persistence-capable code -> static read/write callsites
```

The acceptance chain segment requiring a **live safe read -> reversible write -> reload/restart persistence -> rollback** remains intentionally unexecuted because this phase has `runtime_access: none` and `mutation_authorized: false`.

## Runtime admission

```yaml
track_id: official-client-re
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
```

No live official-client observation, GUI input, anti-idle input, login, credential use, process control, instrumentation, memory mutation, client-byte mutation, network mutation, purchase or transfer occurred.

## Owned paths

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/**`

Existing #528 native-login, #539 action-protocol, #475 worldmap, #302 player-position, #536 coverage-matrix and #543 prompt-package owned paths were not edited.

## Durable evidence

- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`

## Researcher final checkpoint

```yaml
STATUS: DRAFT_NOT_PROMOTED
ALIAS: TIBIA-RE-UI-SETTINGS
TASK_ID: OTC-20260819-track-a-ui-settings-static-model
TASK_RECORD: docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md
LANE: official-client-re
BRANCH: docs/OTC-20260819-track-a-ui-settings-static-model
HEAD: PR_544_CURRENT_HEAD_SELF_REFERENTIAL_CHECKPOINT_COMMIT_VERIFY_VIA_GITHUB
BASE_MAIN: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
DRAFT_PR: 544
OWNED_PATHS:
  - .github/workflows/track-a-ui-settings-static-model.yml
  - docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md
  - docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/**
RUNTIME_IDENTITY: NOT_APPLICABLE_RUNTIME_ACCESS_NONE
CLIENT_BUILD_FENCE:
  official_source: static.tibia.com/launcher/tibiaclient-linux-current/bin/client.lzma
  packed_size: 10214529
  packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
  client_size: 52109920
  client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
  elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
OBJECTIVE: recover official-client UI/options/settings models and persistence evidence, prioritizing H07-H14, without exceeding static-only admission
EXPERIMENTS_COMPLETED:
  - current-build bounded lexical/model scan
  - current-build clientoptions.json and QSettings code-xref scan
  - current-build unfiltered nearest-string key-adjacency negative-control scan
  - lower-priority current-build H01-H06/H15-H19 non-overlap refresh
FACTS:
  - H07-H13 have exact-current-build dedicated action-bar, hotkey, multi-action/cooldown, graphics, sound, interface and gameplay/control model/controller identifiers
  - H14 has exact-current-build TClientOptions/EClientOption/config wrapper identifiers, QSettings APIs and a clientoptions.json literal
  - clientoptions.json has one literal at VA 0x20d2406 and 38 decoded RIP-relative code references in the bounded linear scan
  - four QSettings read/write/group PLT targets are used by 51 decoded direct callsites
  - a QSettings beginGroup/value/endGroup region is adjacent to Qt graphics/Vulkan bootstrap calls
  - repeated QSettings beginGroup/setValue/endGroup regions are adjacent to renderer probing/backend setup code
  - third-stage key-adjacency run reproduced all counts and completed PASS without executing or retaining the client binary
INFERENCES:
  - current client has real QSettings-backed configuration activity, including renderer/bootstrap-adjacent state
  - H07-H14 now have substantially stronger exact-current-build static evidence than broad capability-name census alone
UNKNOWN:
  - authoritative QSettings group/key argument names
  - whether user-visible H10 graphics options share the renderer/bootstrap QSettings store
  - exact TClientOptions to clientoptions.json relationship
  - exact persistence stores for H11-H13
  - profile/migration schema and scope
  - runtime safe read/write/readback/reload/restart persistence and rollback semantics
  - H01/H03/H16/H17 semantic runtime state and H19 TSessiondumpPlayer under this task
DISPROVEN_OR_SUPERSEDED:
  - string/API coexistence alone is not accepted as TClientOptions-to-clientoptions.json linkage
  - QSettings import presence alone is superseded by direct decoded callsite evidence
NEGATIVE_CONTROLS:
  - unfiltered nearest-string scan did not recover an unambiguous QSettings group/key
  - QT_OPENGL_BUGLIST adjacency is not promoted to a QSettings key claim
  - clientoptions.json xref neighborhoods did not establish JSON file-I/O or TClientOptions call linkage
REPEATABILITY:
  - all three static probes reproduced the same packed/client hashes and ELF Build ID
  - second and third xref/key scans reproduced one clientoptions.json literal, 38 code refs, four QSettings targets and 51 QSettings callsites
ANTI_IDLE_INPUTS: none
MISSION_INPUTS:
  - owner alias invocation TIBIA-RE-UI-SETTINGS
  - PR #543 head 981febf4bf8f60896c5c09f8f30ad2859f6ca67c alias/common-worker prompt
  - trusted main governance at a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
  - PR #536 coverage checklist/matrix as a non-owned evidence boundary
RESTORE_RESULT: NOT_APPLICABLE_NO_RUNTIME_OR_CLIENT_MUTATION
FILES_CHANGED:
  - .github/workflows/track-a-ui-settings-static-model.yml
  - docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md
  - docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md
  - docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md
  - docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md
  - docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md
VALIDATION:
  static_probe_1: run 32194079533 job 95894394865 success
  governance_after_frontmatter_repair: run 32194426224 both admission jobs success
  static_xref_probe_2: run 32194426242 job 95895411896 success
  static_key_adjacency_probe_3: run 32194829992 job 95896584056 success
  final_exact_head: pending_after_this_self_referential_checkpoint_commit_and_to_be_recorded_on_PR_544
E2E: NOT_APPLICABLE_WITH_REASON static-only slice has runtime_access none; live UI mutation/reload acceptance requires a fresh Track A runtime admission and shared input lock
SIDE_EFFECTS:
  - GitHub branch, Draft PR, documentation/evidence and bounded GitHub Actions static probes only
  - no official-client launch, login, credentials, GUI input, process attach, client/network/renderer mutation, or proprietary binary retention
BLOCKERS: []
NEXT_ACTION: coordinator reviews Draft PR #544 and decides whether to promote partial static evidence; if live persistence proof is authorized later, acquire fresh Track A runtime admission and shared input lock, use one non-display-critical non-network-critical reversible setting, capture exact before/read/write/readback/reload/restart/rollback evidence, then restore exact before state
```

The static phase is intentionally stopped here: the third discriminator produced a bounded negative key-recovery result, so further broad linear scans would add noise without a new falsifiable question.
