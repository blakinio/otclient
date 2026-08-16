---
task_id: OTC-20260816-track-a-hosted-client-staging-discovery
status: investigating
agent: ChatGPT
session_id: chatgpt-hosted-staging-discovery-20260816-1554
session_role: coordinator_support
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: infrastructure_discovery
phase: official-download-discovery
branch: ci/OTC-20260816-track-a-hosted-client-staging-discovery
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
risk: low
updated: 2026-08-16T15:54:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-hosted-client-staging-discovery.md
  - .github/workflows/tibia-official-client-hosted-staging-discovery.yml
modules_touched: []
reuses:
  - official Tibia Linux Client FAQ entry 121
  - current official Tibia play/download page
  - exact-client fence from OTCLIENT-TIBIA-RE canonical state
depends_on: []
blocks: []
consumers:
  - PR #310 P2-NETWORK exact-binary continuation
  - PR #367 worldmap extent static RE
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_and_continue
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
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
owner_funded_ai_api_authorized: false
exact_target:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
prior_blockers:
  p2_pr_310:
    dns_failure_run: 31944074222
    http_403_run: 31944119641
  worldmap_pr_367:
    same_url_referer_failure_run: 31947523640
strategy:
  - fetch the current official Tibia download/play page with browser-compatible public HTTP headers; no account/session credentials
  - derive the Linux tarball URL from the official page rather than guessing historical static/download endpoints
  - require the resolved download host to remain inside the official tibia.com domain family
  - download the public Linux tarball only to ephemeral GitHub-hosted runner storage
  - inspect/extract only enough to locate client candidates and compare size/SHA against the exact target fence
  - never upload the tarball, client, BattlEye files or other proprietary package bytes as artifacts
  - always remove downloaded/extracted bytes before job exit
  - persist only public URL provenance, HTTP status, archive metadata and hashes/sizes of candidate client executables in logs/task evidence
  - no client execution, no BattlEye analysis, no login, no Synology fallback
acceptance:
  - discovery is materially different from the exhausted direct static/download URL retries
  - exact URL is derived from a current official page or the task records INPUT_BLOCKED without guessing
  - exact target match is claimed only after size 51965216 and SHA-256 e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe both match
  - proprietary bytes remain ephemeral and are not committed/uploaded
  - if the current official tarball no longer contains the exact target build, record CURRENT_OFFICIAL_BUILD_DIFFERS and do not relabel it as exact staging
  - temporary discovery workflow is removed before any terminal merge
last_completed_step: official Tibia Linux FAQ confirms the supported tarball filename tibia.x64.tar.gz; repository direct-URL retries are intentionally not repeated
next_action: run one GitHub-hosted official-page-derived discovery attempt and classify EXACT_STAGING_AVAILABLE, CURRENT_OFFICIAL_BUILD_DIFFERS or INPUT_BLOCKED
---

# Hosted exact-client staging discovery

This task exists only to remove the shared GitHub-hosted exact-input blocker without violating post-PR-331 routing. It must not use Synology merely because retained package bytes exist there.

The workflow obtains any Linux download URL from the current official public Tibia page, keeps package bytes ephemeral, validates the exact target fence, and leaves no proprietary artifact. A failure to derive or fetch the official URL is a durable input blocker, not permission to fall back to Synology static analysis.
