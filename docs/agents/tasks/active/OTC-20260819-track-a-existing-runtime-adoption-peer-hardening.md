---
task_id: OTC-20260819-track-a-existing-runtime-adoption-peer-hardening
status: validating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_hardening
phase: exact_head_ci
branch: fix/OTC-20260819-track-a-existing-runtime-adoption-peer-hardening
base_branch: main
base_sha: a5cbdf1125887f8e5455dfbed5ee5a8e901f105c
risk: high
owned_paths:
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py
  - docs/agents/tasks/active/OTC-20260819-track-a-existing-runtime-adoption-peer-hardening.md
  - docs/agents/evidence/OTC-20260819-track-a-existing-runtime-adoption-peer-hardening/**
modules_touched:
  - canonical-live-kasm-adoption-probe
reuses:
  - PR #596 / merge a71dda46742d8db1bdddfa5d225e9b32703b2080
depends_on: []
blocks:
  - first physical adopt-existing invocation
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
gameplay_allowed: false
invocation_started_at: 2026-08-19T15:54:00+02:00
last_progress_at: 2026-08-19T16:13:00+02:00
focused_transition_tests: 17_OF_17_PASS
focused_kasm_probe_tests: 9_OF_9_PASS
focused_track_a_governance: PASS
focused_py_compile: PASS
focused_git_diff_check: PASS
independent_audit_validator: existing-runtime-adoption-peer-hardening-validator-v1
independent_audit_result: PASS
independent_audit_review: 4973072757
independent_audit_open_material_findings: 0
prior_exact_head: edb454e8f07a5cd326cee288bbe4feaaa3946456
prior_action_required_runs:
  - 32262029910
  - 32262030083
  - 32262029867
current_blocker: NONE
next_action: verify normal exact-head CI emitted by this connector-authored audit checkpoint; if green, squash-merge PR #606 and archive/release this hardening task; physical adoption remains a separate fresh runtime invocation from trusted main
---

# Existing-runtime adoption peer hardening

Post-merge falsification of #596 found two additional fail-closed hardening gaps before the first physical adoption:

1. bridge JSON identity was checked but the Unix socket peer PID was not bound with `SO_PEERCRED`;
2. a plausible `client` / `Tibia*` process whose `/proc/<pid>/exe` could not be resolved could be skipped rather than classified unverifiable.

The remediation requires exact bridge peer PID equality on every structural connection and fails closed on plausible unreadable candidates. It preserves title redaction, `BRIDGE_3_OF_3`, all-container inventory, and metadata-only/no-runtime authority.

## Fresh independent audit

Validator `existing-runtime-adoption-peer-hardening-validator-v1` reviewed exact base `a5cbdf1125887f8e5455dfbed5ee5a8e901f105c` and exact implementation head `edb454e8f07a5cd326cee288bbe4feaaa3946456` from a clean detached worktree. It independently reran 9/9 Kasm adoption-probe tests, 17/17 canonical transition regressions, Track A governance, Python compilation, `git diff --check`, path-scope checks and targeted semantic falsification assertions. Result: `PASS`, open material findings `0`; review `4973072757`.

The prior exact-head workflow generation ended `action_required` before jobs were emitted because that implementation head was synchronized by Actions. This connector-authored audit checkpoint intentionally creates a new exact head so normal pull-request CI can run under the regular repository actor path. No runtime authority changes with this checkpoint.
