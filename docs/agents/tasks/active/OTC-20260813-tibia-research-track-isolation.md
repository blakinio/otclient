---
task_id: OTC-20260813-tibia-research-track-isolation
status: validating
agent: ChatGPT
project_lane: otclient
lane: otclient
track: coordination
task_kind: documentation_infrastructure
phase: exact-head-validation
branch: docs/OTC-20260813-tibia-research-track-isolation
base_branch: main
created: 2026-08-13T13:56:00+02:00
updated: 2026-08-13T14:13:00+02:00
risk: medium
owned_paths:
  - docs/agents/AGENTS.md
  - docs/agents/SHORT_COMMANDS.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/tasks/active/OTC-20260813-tibia-research-track-isolation.md
modules_touched:
  - agent-coordination
reuses:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-external-evidence-manifest.md
cross_repo_tasks: []
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
---

# Objective

Make the two live Tibia research tracks explicit, non-overlapping, OTClient-repository-only and native-Linux-client-only:

1. Track A `official-client-re`: official native Linux Tibia client runtime, structural reads/actions/protocol/map analysis;
2. Track B `otclient-global-login`: native Linux build/runtime of this repository's OTClient authenticating to and entering official Tibia Global.

# Verified basis

- `blakinio/otclient` main was `83934aa1b6a3f03c2c3934c0eed47165667c3dd2` at task creation.
- Canonical consolidation PR #286 is merged and records `blakinio/otclient` as the canonical programme/coordination repository.
- `docs/agents/reports/OTCLIENT-20260813-tibia-re-external-evidence-manifest.md` records material Oteryn Tibia-analysis knowledge as imported/superseded/indexed for normal continuation.
- PR #284 previously conflated the OTClient-to-Global lane with `OTCLIENT-TIBIA-RE`; its PR body has been corrected to Track B scope only.
- Track B's task currently lives on the active PR #284 branch, not `main`; the short-command registry now resolves it explicitly through that live PR-local branch/path.

# Acceptance inventory

- [x] `docs/agents/TIBIA_RESEARCH_TRACKS.md` defines two distinct track IDs, scopes, owned runtime namespaces and forbidden cross-track actions.
- [x] Normal future workers are forbidden from searching, reading or referencing `blakinio/Oteryn-Platform` / historical Oteryn runtime for these tracks; repository-owned imported evidence is the normal authority.
- [x] `OTCLIENT-TIBIA-RE` resolves only to the official-client reverse-engineering track.
- [x] `OTCLIENT-GLOBAL-LOGIN` resolves only to the OTClient-to-Tibia-Global compatibility track through a revalidated live PR-local branch/task while PR #284 is active.
- [x] Shared runner use is allowed only with isolated container/state/display/port namespaces and non-overlapping owned paths.
- [x] One track may consume a promoted repository-owned evidence contract from the other but may not take over its task, branch, PR, container, state directory or mutable files.
- [x] Both tracks are native-Linux-client-only: Track A may use only the official native Linux Tibia client; Track B may use only the native Linux `blakinio/otclient` runtime.
- [x] Windows, macOS, Android, iOS, browser/web, Wine/Proton-wrapped Windows and other non-native-Linux clients/runtimes are forbidden as runtime evidence, fallback or substitute for these tracks.
- [x] PR #284 metadata no longer claims to be the single active `OTCLIENT-TIBIA-RE` lane.
- [x] No writes occur outside `blakinio/otclient`.

# Review finding

P2 review finding on PR #287: Track B was not resolvable because the alias was missing from `SHORT_COMMANDS.md` and its task was not on `main`.

Resolution: added `OTCLIENT-GLOBAL-LOGIN` to the registry and explicitly bound the active entry point to PR #284 branch `feat/OTC-20260813-tibia-global-login-lab` plus `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md`, with live-head revalidation and post-terminal fallback to resulting main/replacement state. Review thread resolved after the repair.

# Evidence boundary

Material continuation knowledge has been imported into `blakinio/otclient`. If a required detail is absent, future workers classify it as `UNKNOWN` and recover it inside the owning OTClient track instead of consulting Oteryn. For runtime evidence, only native Linux client/runtime observations are admissible.

# Validation

- Initial exact-head CI on `f703ef9455ab42f3409fac42f9fe0731e2a8f465`: PASS, run `31698110606`.
- Review finding repaired after that run; final exact-head CI is required on the current head before merge.
- Runtime E2E: NOT_APPLICABLE; this task changes governance/coordination documentation only.

# Next action

Observe final exact-head CI and review state for PR #287; merge only when exact-head CI is green and no unresolved material review finding remains.
