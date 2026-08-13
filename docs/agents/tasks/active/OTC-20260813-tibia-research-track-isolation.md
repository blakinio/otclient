---
task_id: OTC-20260813-tibia-research-track-isolation
status: implementing
agent: ChatGPT
project_lane: otclient
lane: otclient
track: coordination
task_kind: documentation_infrastructure
phase: coordination
branch: docs/OTC-20260813-tibia-research-track-isolation
base_branch: main
created: 2026-08-13T13:56:00+02:00
updated: 2026-08-13T13:56:00+02:00
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

Make the two live Tibia research tracks explicit, non-overlapping and OTClient-repository-only:

1. official-client reverse engineering: official Linux Tibia client runtime, structural reads/actions/protocol/map analysis;
2. OTClient-to-Global compatibility: this repository's OTClient authenticating to and entering official Tibia Global.

# Verified basis

- `blakinio/otclient` main is `83934aa1b6a3f03c2c3934c0eed47165667c3dd2` at task creation.
- Canonical consolidation PR #286 is merged and records `blakinio/otclient` as the canonical programme/coordination repository.
- `docs/agents/reports/OTCLIENT-20260813-tibia-re-external-evidence-manifest.md` records the material Oteryn Tibia-analysis knowledge as imported/superseded/indexed for normal continuation.
- PR #284 currently conflates the OTClient-to-Global lane with `OTCLIENT-TIBIA-RE`; this is a coordination defect because the owner requires it to remain a separate track.

# Acceptance inventory

- [ ] `docs/agents/TIBIA_RESEARCH_TRACKS.md` defines two distinct track IDs, scopes, owned runtime namespaces and forbidden cross-track actions.
- [ ] Normal future workers are forbidden from searching, reading or referencing `blakinio/Oteryn-Platform` / historical Oteryn runtime for these tracks; repository-owned imported evidence is the only normal authority.
- [ ] `OTCLIENT-TIBIA-RE` resolves only to the official-client reverse-engineering track.
- [ ] A separate `OTCLIENT-GLOBAL-LOGIN` alias resolves only to the OTClient-to-Tibia-Global compatibility track.
- [ ] Shared runner use is allowed only with isolated container/state/display/port namespaces and non-overlapping owned paths.
- [ ] One track may consume a promoted, repository-owned artifact/evidence contract from the other but may not take over its task, branch, PR, container, state directory or mutable files.
- [ ] PR #284 metadata is corrected so it no longer claims to be the single active `OTCLIENT-TIBIA-RE` lane.
- [ ] No writes occur outside `blakinio/otclient`.

# Evidence boundary

The external migration manifest intentionally retained provenance pointers and allowed forensic re-open for missing details. The owner now requires a stricter operational rule: because material continuation knowledge has been imported, future track workers must not search or refer back to Oteryn. If a required detail is absent from `blakinio/otclient`, classify it as `UNKNOWN` and persist an OTClient-owned recovery/research task instead of consulting Oteryn.

# Next action

Implement the coordination contract, update the short-command registry and nested agent instructions, correct PR #284 metadata, then run exact-head repository validation and merge if all gates pass.
