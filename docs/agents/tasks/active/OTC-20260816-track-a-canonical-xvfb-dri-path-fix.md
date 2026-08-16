---
task_id: OTC-20260816-track-a-canonical-xvfb-dri-path-fix
status: implementing
agent: ChatGPT
session_id: chatgpt-canonical-xvfb-dri-path-fix-20260816
session_role: implementation_engineer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: implementation
phase: hosted-worker-repair
branch: fix/OTC-20260816-track-a-canonical-xvfb-dri-path
base_branch: main
base_main: d3f186414256151c9d5e03f34c5a9026b1fba500
risk: high
updated: 2026-08-16T20:58:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-xvfb-dri-path-fix.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-xvfb-dri-path-fix/**
modules_touched:
  - canonical Track A runtime session worker
reuses:
  - PR #420 causal LIBGL_DRIVERS_PATH proof as unpromoted research input only
  - PR #421 minimality proof as unpromoted research input only
  - current trusted main canonical session worker and tests
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical research isolated the missing canonical Xvfb GLX prerequisite to the contained DRI provider search path; implementation and validation are hosted-only and must reach trusted main before any fresh physical runtime redispatch
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
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
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
scope:
  worker_change:
    - validate `$TOOL/usr/lib/x86_64-linux-gnu/dri` as a real directory contained below the selected toolroot
    - validate `swrast_dri.so` exists and resolves to a regular file below that contained DRI directory/toolroot
    - derive the DRI path from the selected trusted toolroot only
    - export `LIBGL_DRIVERS_PATH` into the Xvfb launch environment
    - preserve the Xvfb argument list exactly; do not add `+extension GLX`
  tests:
    - complete toolroot fixtures include a contained DRI/swrast provider
    - resolver rejects missing DRI provider
    - resolver rejects swrast symlink escape
    - source contract proves Xvfb receives the derived LIBGL_DRIVERS_PATH
    - source contract proves no explicit GLX flag or unrelated renderer override is introduced
forbidden:
  - Synology/self-hosted execution
  - official client/X11/VNC/network/login/gameplay execution
  - canonical lease/registration/session mutation or observation
  - client graphics/backend environment changes
  - `+extension GLX`
  - LIBGL_ALWAYS_SOFTWARE
  - GALLIUM_DRIVER
  - MESA_LOADER_DRIVER_OVERRIDE
  - changes to lease, transition, Gate B, WARP, credentials or Track B
acceptance:
  - worker syntax passes
  - canonical session unit/contract tests pass
  - full relevant canonical transition/guard/lease test suite passes
  - deterministic source tests prove DRI containment and minimal Xvfb-only env change
  - repository governance and CI pass on exact final head
  - no physical runtime job executes
last_completed_step: PR #421 run 31965779546/job 95210624747 proved LIBGL_DRIVERS_PATH alone enables GLX with the exact current canonical worker Xvfb arguments, so no server flag change is needed
next_action: implement the minimal worker/test changes on current main, run hosted validation, remove any temporary validation workflow if used, and hand the Draft to coordinator for promotion
---

# Track A canonical Xvfb DRI-path fix

Hosted-only implementation. It converts the physical causal proof into a fail-closed trusted-worker contract without exercising the physical runtime.