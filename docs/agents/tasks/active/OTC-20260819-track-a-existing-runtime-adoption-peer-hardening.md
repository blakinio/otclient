---
task_id: OTC-20260819-track-a-existing-runtime-adoption-peer-hardening
status: validating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure_hardening
phase: independent_audit_and_exact_head_ci
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
last_progress_at: 2026-08-19T16:05:00+02:00
focused_transition_tests: 17_OF_17_PASS
focused_kasm_probe_tests: 9_OF_9_PASS
focused_track_a_governance: PASS
current_blocker: NONE
next_action: publish PR #606 exact hardened head, obtain fresh independent audit and exact-head CI, merge/archive, then leave physical adoption to a fresh runtime invocation from trusted main
---

# Existing-runtime adoption peer hardening

Post-merge falsification of #596 found two additional fail-closed hardening gaps before the first physical adoption:

1. bridge JSON identity was checked but the Unix socket peer PID was not bound with `SO_PEERCRED`;
2. a plausible `client` / `Tibia*` process whose `/proc/<pid>/exe` could not be resolved could be skipped rather than classified unverifiable.

The remediation requires exact bridge peer PID equality on every structural connection and fails closed on plausible unreadable candidates. It preserves title redaction, `BRIDGE_3_OF_3`, all-container inventory, and metadata-only/no-runtime authority.
