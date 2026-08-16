---
task_id: OTC-20260816-track-a-beclient-static-analysis
status: investigating
agent: ChatGPT
session_id: chatgpt-beclient-static-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: static-research
phase: elf-static-analysis
branch: research/OTC-20260816-track-a-beclient-static-analysis
base_branch: main
base_main: 3a5568f36ebc326afd246d0d2da45b5d8eecabfa
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-beclient-static-analysis
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: null
updated: 2026-08-16T09:10:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-beclient-static-analysis.md
  - .github/workflows/tibia-official-client-re-beclient-static-analysis.yml
modules_touched: []
reuses:
  - synology-otclient-01
  - retained PR #303 exact-client package artifact
  - GitHub-only temporary workflow pattern
depends_on:
  - current main Track A governance
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
track_a_runtime_agent_admission_version: 1
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
runtime_platform: official_native_linux_only
next_action: run bounded static ELF analysis against the retained exact-client BEClient.so without executing or loading it
---

# Objective

Statically characterize the retained official native Linux `BEClient.so` associated with exact Tibia client `15.32.df7b29`, focusing on ELF identity, size/hash, sections, hardening indicators, dynamic dependencies, imports/exports, selected capabilities suggested by symbol/string evidence, and obvious configuration/network markers.

# Safety boundary

Static file inspection only. Do not execute, dlopen, preload, inject, attach, debug, patch, modify, or redistribute `BEClient.so`; do not launch or stop Tibia; do not inspect credentials, process memory, session state, or anti-cheat runtime traffic. Do not derive or publish bypass/evasion instructions.

# Acceptance

- locate `BEClient.so` only under the already identified retained PR #303 run package;
- record exact file size and SHA-256;
- record ELF class/type/machine/build-id/strip state and hardening-relevant program headers;
- enumerate dynamic `NEEDED` libraries and exported dynamic symbols;
- summarize imported symbol families and selected non-secret strings/paths/domains without dumping proprietary binary content;
- distinguish direct facts from inferences about likely behavior;
- remove the temporary workflow and close the temporary PR unmerged after evidence collection.
