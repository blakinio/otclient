---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: active
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-2105
session_role: researcher
session_rotation_count: 6
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime-research
phase: restart-relogin-reacquisition
branch: research/OTC-20260815-track-a-runtime-reacquisition
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-reacquisition
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 303
updated: 2026-08-15T21:36:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-classification.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-window.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-window-replay.yml
  - .github/workflows/tibia-official-client-re-runtime-xdotool-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
  - .github/scripts/tibia-official-client-re-parent-gdb-patch.py
depends_on:
  - coordinator-retained exact-build structural world evidence
  - PR #290 historical login procedure as revalidation-required input only
  - PR #307 bounded read-only loader/Qt/support-state diagnostics
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
runtime_code_bearing_head: 1147062b1f91298055f8623043457298c5797600
workflow_quality_head: 8177ec91311c1b6d526f5ecf1d02a2dc5c90aef3
invocation_started_at: 2026-08-15T21:05:00+02:00
last_progress_at: 2026-08-15T21:36:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: yama_parent_tracer_reacquisition
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
stop_reason: null
active_operation:
  type: replace_attach_observer_with_task_owned_parent_gdb
  prior_run: 31904207608
  prior_job: 95059419997
next_action: patch only the materialized effective helper so task-owned GDB launches the exact official client as its child with ASLR left enabled, preserves the same exact-SHA/proxy/software-render/login/structural breakpoint contract and repaired xdotool loader, and stops child-before-observer; do not change kernel.yama.ptrace_scope or any host security setting
---

# Objective

Prove restart/relogin/reacquisition stability for official native Linux Tibia and hand promotable evidence to coordinator PR #300. Final completion additionally requires the original structural position/record-format/privacy/network/live-session gates.

# Exact fence

`15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, runner `synology-otclient-01`, task display `:115`, task SOCKS `25415` -> Track-A WARP SOCKS `25354`.

# Accepted controls

- world/login run `31730884814`, successful attempt-13 `94716022704` and attempt-14 `94785048338`: world transition, local SOCKS only, direct TCP `0`, UDP `0`, session left running;
- structural run `31806312967` / `94785974126`: real `(x,y,z,order)` records, strip counts `0,33,88`, reversible `Up` then `Down`; `(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)` is DERIVED only;
- direct authoritative P0 XYZ remains UNKNOWN.

# Corrected visible-window root cause — FACT

Runs #26-#30 reported `client_gen_1_window_missing`, but the helper's `resolve_window()` and login path invoke private toolroot `xdotool` without toolroot `LD_LIBRARY_PATH`, while errors are redirected and converted to empty search results. Run `31903986899` / job `95058901925` is the required no-cache control: after only repairing the xdotool loader it proved 4 process windows / 2 visible windows and Tibia window `2097162` at `1020x650`. Canonical shader/GPU cache is therefore not required and must not be seeded into the full path.

# Yama transition — FACT

The first full xdotool-repaired reacquisition run `31904207608` / job `95059419997` reached the exact client/Xvfb/WARP/window setup but stopped before protected login with `TRACK_A_RUNTIME_ERROR=ptrace_scope_not_zero`. Cleanup succeeded and no login secret was used. The current host security posture is therefore incompatible with the old `launch client -> gdb attach` observer model.

The task will **not** write `/proc/sys/kernel/yama/ptrace_scope`, invoke `sysctl`, request privileged host mutation, or weaken Yama. The bounded replacement uses normal Yama parent-child semantics: a task-owned GDB process launches `/bin/bash <task-local-launcher>`, the launcher exports the exact existing client runtime/proxy/software-render environment and `exec`s the exact SHA-fenced client, and GDB catches that exec, computes the PIE from `/proc/<child>/maps`, installs the same exact-build Worldmap breakpoint at `PIE + 0x19a8ea3`, and continues. `set disable-randomization off` preserves ASLR so restart-stability still requires a fresh PIE. The client process receives the `client-gen-N` task role while GDB retains `observer-gen-N`; both remain credential-variable-free.

Stop ordering changes only as required by parent tracing: terminate the exact task-owned client first while GDB passes `SIGTERM` through, then allow batch GDB to exit naturally; terminate the exact task-owned observer only if it remains after a bounded child-exit wait. No broad process kill is permitted.

# Acceptance

- [ ] two successful reacquired live generations with exact SHA/size;
- [ ] fresh PID/PIE after clean restart;
- [ ] WARP/SOCKS confinement, direct TCP `0`, UDP `0`;
- [ ] structural `IN_GAME` on both generations and structural reacquisition after restart;
- [ ] accepted final position proof and original literal `REC x=... y=... z=... order=... raw28=... raw30=...` boundary;
- [ ] privacy-safe screenshot;
- [ ] final accepted session intentionally left logged in after observer detach;
- [x] no-cache visible-window gate proven;
- [x] host Yama security posture preserved; no global ptrace weakening authorized;
- [ ] final exact-head CI green.
