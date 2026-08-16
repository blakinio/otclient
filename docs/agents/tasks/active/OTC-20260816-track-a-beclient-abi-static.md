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
related_pr: 330
updated: 2026-08-16T09:23:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-beclient-abi-static.md
  - .github/workflows/tibia-official-client-re-beclient-abi-static.yml
  - .github/workflows/tibia-official-client-re-beclient-abi-bounded-bytes.yml
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
prior_analysis_run: 31933690981
prior_analysis_job: 95132257220
next_action: isolate the concrete client BEClient string at 0x1d69bb2 and xref at 0xc95cb2, then extract only bounded static byte windows for offline disassembly of that legitimate loader path plus Init/GetVer/_0.._7 prologues; do not expand into bypass/evasion analysis
---

# Objective

Recover the bounded static integration contract between exact official Linux Tibia client `15.32.df7b29` and its retained `BEClient.so`: library-name discovery, dynamic loading/symbol-resolution path, exported entrypoint shapes (`Init`, `GetVer`, `_0.._7`), and non-secret configuration semantics visible in `BEClient.cfg`.

# Current direct facts

Run `31933690981`, job `95132257220`, succeeded without executing either target.

- exact Tibia client and prior `BEClient.so` SHA fences passed;
- `BEClient.cfg` is 29 bytes, SHA-256 `4b36d4ab990a3bd9f9b5379f58b65ec6402eb3b3109dc83a02b6827778d29281`, with only `GameID tibia` and `MasterPort 7171`;
- exact client imports `dlopen`, `dlsym`, `dlclose`;
- one concrete `BEClient` literal occurs at client VA/file offset `0x1d69bb2`, with a common RIP-relative reference at `0xc95cb2`;
- numerous broad `BattlEye` and substring `Init` occurrences exist, so they are not yet individually loader-authoritative;
- remote runner currently lacks `objdump`, `gdb`, and Python capstone;
- prior BE dynamic symbols remain `Init`, `GetVer`, `_0.._7`; their section-index metadata is structurally inconsistent with the low-address values and will not be trusted as semantic section ownership without independent bounds.

# Safety boundary

Static file inspection only. Do not execute, dlopen, preload, inject, attach, debug a live process, patch, modify, or redistribute BattlEye or Tibia binaries. Do not derive bypass/evasion, signature neutralization, anti-debug defeat, spoofing, or detection-avoidance instructions. Do not inspect credentials, live process memory, session state, or runtime traffic. PR #303 mutable/runtime namespace remains untouched.

# Acceptance

- revalidate exact Tibia client fence and `BEClient.so` hash from prior evidence;
- hash and inspect `BEClient.cfg` as text only;
- enumerate client-side BattlEye/library/symbol literals and dynamic-loader imports;
- recover bounded function prologues/call structure for `Init`, `GetVer`, `_0.._7` through offline disassembly of minimal byte windows when direct remote disassembly is unavailable;
- identify the client-side loader/symbol-resolution callsite only to the level needed to describe legitimate ABI/lifecycle;
- classify every behavioral statement as FACT or INFERENCE and preserve unknowns;
- remove temporary workflows and close temporary PR unmerged after evidence collection.
