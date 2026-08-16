---
task_id: OTC-20260816-track-a-runner-support-x11vnc-repair
status: ready
agent: ChatGPT
session_id: chatgpt-runner-x11vnc-repair-20260816-1657
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runner_infrastructure_repair
phase: coordinator-promotion-ready
branch: ci/OTC-20260816-track-a-runner-support-x11vnc-repair
base_branch: main
base_main: c2e1466b4c0ac11deb96b104830f90aae9c35a97
current_main: c2e1466b4c0ac11deb96b104830f90aae9c35a97
risk: medium
updated: 2026-08-16T17:01:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-runner-support-x11vnc-repair.md
  - docs/agents/evidence/OTC-20260816-track-a-runner-support-x11vnc-repair/**
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-runner-support-layout-inventory.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-toolroot-layout-fix.md
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded mutation targets only the dedicated runner support-tool filesystem needed by the trusted canonical worker; no official-client runtime surface is observed or mutated
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
runner_filesystem_mutation_authorized: true
owner_funded_ai_api_authorized: false
authorization_source: owner instruction 2026-08-16 to finish existing Track A tasks; bounded runner-support repair only, no canonical runtime/client mutation
repair_source:
  path: /usr/bin/x11vnc
  realpath: /usr/bin/x11vnc
  package: x11vnc
  package_version: 0.9.16-10
  sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
repair_target:
  root: /work/_otclient_tibia_re_state/toolroot
  path: /work/_otclient_tibia_re_state/toolroot/usr/bin/x11vnc
  pre_state: ABSENT
  post_state: PRESENT_IDENTICAL_CONTAINED
  sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
  trusted_worker_resolved_root: /work/_otclient_tibia_re_state/toolroot
forbidden_surface:
  - official client files/processes
  - canonical registration/lease/session directories
  - /proc process inventory
  - X11 displays/windows or VNC listeners/endpoints
  - network/game/login state
  - credentials/environment secrets
  - Track B PR #284
physical_attempts:
  - run: 31954234775
    job: 95182280438
    result: FAIL_CLOSED_BEFORE_COPY
    target_created: false
    finding: dpkg -V reported only four missing documentation/manpage files in the slim image; no /usr/bin/x11vnc mismatch
  - run: 31954295453
    job: 95182427755
    result: SUCCESS
    dpkg_verification: ONLY_KNOWN_DOCS_MISSING
    target_prestate: TARGET_ABSENT_CREATED
    source_sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
    target_sha256: 4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
    trusted_worker_toolroot: /work/_otclient_tibia_re_state/toolroot
    classification: PASS_CONTAINED_TOOLROOT_COMPLETE
known_docs_only_dpkg_omissions:
  - /usr/share/doc/x11vnc/NEWS.gz
  - /usr/share/doc/x11vnc/README.gz
  - /usr/share/man/man1/x11vnc.1.gz
  - /usr/share/man/man8/Xdummy.8.gz
evidence_path: docs/agents/evidence/OTC-20260816-track-a-runner-support-x11vnc-repair/20260816-contained-x11vnc-repair.md
validation:
  successful_physical_repair_run: 31954295453
  successful_physical_repair_job: 95182427755
  successful_physical_repair_result: SUCCESS
  workflow_removed_after_capture: true
  exact_head_governance: PENDING_AFTER_WORKFLOW_REMOVAL
  exact_head_repository_ci: PENDING_AFTER_WORKFLOW_REMOVAL
  review_threads_open: 0
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: runner support-tool filesystem completion only; no official-client runtime behavior exercised
audit:
  result: PASS
  material_findings_open: 0
  notes:
    - the first attempt made no persistent change and exposed an over-broad package validator in a slim image
    - the repaired validator still fails for any package verification difference outside the four exact documentation/manpage omissions
    - source/target executable identity is proven by exact SHA-256 and the trusted worker's existing contained-root resolver now passes
    - the one-root/realpath-containment worker remains unchanged; no ambient system fallback was introduced
acceptance:
  - source x11vnc is package-owned, exact-version, root-owned, non-group/world-writable, regular executable
  - target publication is atomic and content-identical inside the already trusted contained root
  - any unexpected target or binary/package payload mismatch fails closed
  - trusted worker contract-test resolves the completed contained root
  - one-shot repair workflow is removed before task checkpoint updates
last_completed_step: package-verified /usr/bin/x11vnc was atomically staged into the persistent contained toolroot, source/target hashes matched exactly, the trusted worker resolved the completed /work root, and the one-shot workflow was removed
next_action: obtain exact-head governance/CI, coordinator review and merge; archive this repair, then fresh-current-main redispatch canonical runtime and retry bootstrap exactly once
---

# Track A runner support x11vnc repair

The persistent hardened toolroot is now complete without weakening the trusted worker. The exact system x11vnc executable from package version 0.9.16-10 was verified and copied bit-identically into the contained `/work/.../toolroot`; the trusted worker resolver accepts that root. No official-client or canonical runtime surface was touched.
