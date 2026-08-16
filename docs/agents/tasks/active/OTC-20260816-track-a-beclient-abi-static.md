---
task_id: OTC-20260816-track-a-beclient-abi-static
status: investigating
agent: ChatGPT
session_id: chatgpt-beclient-abi-static-20260816
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: static-research
phase: client-beclient-loader-abi
branch: research/OTC-20260816-track-a-beclient-abi-static
base_branch: main
base_main: 139ef452214bd212a130f916e87d55c7f8712b93
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-beclient-abi-static
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: null
updated: 2026-08-16T09:20:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-beclient-abi-static.md
  - .github/workflows/tibia-official-client-re-beclient-abi-static.yml
modules_touched: []
reuses:
  - closed diagnostic PR #327 static BEClient evidence
  - retained PR #303 exact-client package artifact
  - synology-otclient-01 as static file-analysis executor only
depends_on:
  - current main Track A runtime admission governance
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
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
next_action: statically map the official client's BattlEye loader strings, dynamic-loader imports, BEClient.cfg, and bounded disassembly around BEClient exported entrypoints and client-side loader callsites without executing either binary
---

# Objective

Recover the bounded static integration contract between exact official Linux Tibia client `15.32.df7b29` and its retained `BEClient.so`: library-name discovery, dynamic loading/symbol-resolution path, exported entrypoint shapes (`Init`, `GetVer`, `_0.._7`), and non-secret configuration semantics visible in `BEClient.cfg`.

# Safety boundary

Static file inspection only. Do not execute, dlopen, preload, inject, attach, debug a live process, patch, modify, or redistribute BattlEye or Tibia binaries. Do not derive bypass/evasion, signature neutralization, anti-debug defeat, spoofing, or detection-avoidance instructions. Do not inspect credentials, live process memory, session state, or runtime traffic. PR #303 mutable/runtime namespace remains untouched.

# Acceptance

- revalidate exact Tibia client fence and `BEClient.so` hash from prior evidence;
- hash and inspect `BEClient.cfg` as text only;
- enumerate client-side BattlEye/library/symbol literals and dynamic-loader imports;
- locate available static disassembly tooling without installing or executing target code;
- recover bounded function prologues/call structure for `Init`, `GetVer`, `_0.._7` when statically disassemblable;
- identify client-side loader/symbol-resolution callsites only to the level needed to describe the legitimate ABI/lifecycle;
- classify every behavioral statement as FACT or INFERENCE and preserve unknowns;
- remove temporary workflow and close temporary PR unmerged after evidence collection.
