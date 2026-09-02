---
task_id: OTC-20260902-canonical-current-client-fence-be4f48
status: waiting
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: verification
branch: fix/OTC-20260902-canonical-current-client-fence-be4f48
base_branch: main
base_main: 8441fc1cce1600033b505d68ebc5c0141b337394
created: 2026-09-02T12:35:00+02:00
updated_at: 2026-09-02T13:10:51+02:00
pr: 858
red_head: 33e64fc42fba640f3b4aaa8f4734d647b16f697b
implementation_head: 22977b3ab264bbfce986a5ff5b2ae7e9e1c457ba
current_blocker: exact_head_ci_repair_cycle_1
risk: high
execution_class: hybrid
execution_mode: chat_github_plus_remote_provenance
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
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
implementation_authorized: true
owner_funded_ai_api_authorized: false
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - .github/workflows/track-a-canonical-current-client-fence.yml
  - .github/workflows/track-a-canonical-live-governance.yml
  - .github/workflows/track-a-kasm-canonical-bootstrap.yml
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/CHANGELOG.md
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - .github/workflows/tibia-re-control-center-core.yml
  - docs/agents/tasks/active/OTC-20260902-canonical-current-client-fence-be4f48.md
  - docs/agents/evidence/OTC-20260902-canonical-current-client-fence-be4f48/**
---

# Objective

Advance only the trusted **current exact-client identity fence** from `15.32.75d4a0 / 52105824 / d1a16819...` to the owner-observed official-launcher build `15.32.be4f48 / 52105824 / 552dcf79...` and synchronize all current canonical/read-only admission consumers.

Historical build-specific reverse-engineering evidence, offsets, login writers, QMeta addresses, serializers and prior client-fence-reconciliation source/target contracts remain historical and must not be promoted to the new binary.

# Provenance boundary

Authority for the new tuple is limited to agreement between the official launcher's installed package manifest and a fresh hash/size of the exact singleton live ELF. Raw CDN refetch attempts were blocked by Cloudflare challenge/HTTP 403 and are not counted as proof.

# Acceptance

1. TDD RED proves the old trusted-current fence is still authoritative before implementation.
2. Normative Track A governance, canonical runtime components, Kasm bootstrap identity and Phase 2 read-only admission use one exact new tuple.
3. Historical build-specific research surfaces remain pinned to their source builds.
4. Existing canonical component tests, runtime-admission tests, deterministic governance and diff checks pass.
5. No login, credentials, gameplay, GUI input, process control, memory access or packet capture from this repository-only task.
6. Direct Codex usage remains zero unless a later independent audit is explicitly justified.

next_action: repair the first exact-head CI failures, rerun affected and broad validation, then require a fully terminal exact-head CI before fresh scope audit


## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T11:10:51Z
head: 22977b3ab264bbfce986a5ff5b2ae7e9e1c457ba
branch: fix/OTC-20260902-canonical-current-client-fence-be4f48
pr: 858
status: waiting
context_routes:
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - tools/tibia_re_control_center/agent_runtime_admission.py
owned_paths:
  - docs/agents/tasks/active/OTC-20260902-canonical-current-client-fence-be4f48.md
  - docs/agents/evidence/OTC-20260902-canonical-current-client-fence-be4f48/**
  - current exact-client governance/runtime-admission files listed in task frontmatter
proven:
  - trusted main at task creation and PR base is 8441fc1cce1600033b505d68ebc5c0141b337394
  - owner-authorized official launcher installed package version 15.32.be4f48
  - launcher-managed package manifest binds bin/client to size 52105824 and sha256 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
  - fresh singleton live ELF hash and size agree exactly with the launcher-managed manifest
  - TDD RED head 33e64fc42fba640f3b4aaa8f4734d647b16f697b failed at runtime admission contract current build version missing
  - GREEN implementation head 22977b3ab264bbfce986a5ff5b2ae7e9e1c457ba synchronizes only current identity surfaces and leaves build-specific historical RE evidence unchanged
  - GREEN focused fence, Phase 2 runtime-admission 14 of 14, deterministic Track A governance, changed Python compile and git diff check all pass
  - fresh Linux exact-head clone at 22977b3ab264bbfce986a5ff5b2ae7e9e1c457ba passed bash syntax, focused fence, canonical live-session, canonical transition, existing-runtime probe, Kasm bootstrap worker, and Phase 2 runtime-admission suites
  - direct Codex worker or reviewer invocations remain zero
  - repository task runtime_access remains none with physical action budget/count zero
  - first exact-head CI at 4c308ce11ba30f509894d87dffe9a1a4f9af936a exposed Package A path-boundary rejection plus 18 Package B errors, all traced to stale current-build fixtures rather than production admission
  - repair cycle 1 updates only those fixtures plus an exact-task and exact-branch gated Package A exception; affected suites 28 of 28 and boundary simulation over 23 paths pass with zero unexpected paths
derived:
  - direct raw CDN refetch was blocked by Cloudflare challenge or HTTP 403 on direct Synology, Molehill-PC and runner/WARP attempts and is not counted as proof
  - Linux governance rerun in the first exact-head clone failed only because the single-branch clone lacked origin/main; deterministic governance passed on Molehill-PC, and later runner clone attempts were blocked by GitHub credential/auth transport before tests started
unknown:
  - final exact-head GitHub Actions result after repair cycle 1 is pushed
  - fresh independent scope-audit classification
conflicts:
  - none
first_failure:
  marker: trusted current exact-client fence remained on 15.32.75d4a0
  evidence: TDD RED at 33e64fc42fba640f3b4aaa8f4734d647b16f697b
rejected_hypotheses:
  - current client identity can be advanced by global search-replace: rejected; historical build-specific RE evidence remains source-build-fenced
  - Windows component-suite errors are fence regressions: rejected; failures are platform-only fcntl AF_UNIX fchmod and bash/X11 incompatibilities while exact-head Linux suites pass
  - Package B 18 errors indicate production admission regression: rejected; every failure is a stale current-build test fixture rejected by the intentionally updated exact fence
changed_paths:
  - current exact-client governance/runtime-admission surfaces only
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - .github/workflows/tibia-re-control-center-core.yml
  - docs/agents/tasks/active/OTC-20260902-canonical-current-client-fence-be4f48.md
  - docs/agents/evidence/OTC-20260902-canonical-current-client-fence-be4f48/**
validation:
  - command: python .github/scripts/test_track_a_canonical_current_client_fence.py
    result: PASS
    evidence: focused current-client fence printed TRACK_A_CANONICAL_CURRENT_CLIENT_FENCE=PASS
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_runtime_admission
    result: PASS
    evidence: 14 tests ran and all passed
  - command: python .github/scripts/test_track_a_agent_runtime_governance.py --changed-from origin/main --expected-branch fix/OTC-20260902-canonical-current-client-fence-be4f48
    result: PASS
    evidence: deterministic governance printed TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
  - command: changed Python modules py_compile plus git diff --check
    result: PASS
    evidence: py_compile returned zero and git diff --check returned zero
  - command: Linux exact-head canonical session transition probe bootstrap admission and focused-fence matrix
    result: PASS
    evidence: fresh Linux clone fenced to 22977b3ab264bbfce986a5ff5b2ae7e9e1c457ba printed PASS for BASH_N FENCE SESSION TRANSITION PROBE BOOTSTRAP and ADMISSION
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_edge_bridge tests.tools.tibia_re_control_center.test_vision_p2_trusted_composition
    result: PASS
    evidence: repair-cycle affected suites ran 28 tests and all passed
  - command: Package A boundary simulation over committed PR diff plus repair worktree diff
    result: PASS
    evidence: 23 changed paths classified and UNEXPECTED_COUNT=0 with the exact task plus exact branch exception
blockers:
  - repair cycle 1 must be committed and exact-head GitHub CI must become fully terminal before fresh independent scope audit
next_action: commit and push repair cycle 1, require all exact-head GitHub CI workflows to become terminal, then perform fresh scope audit before classification
```
