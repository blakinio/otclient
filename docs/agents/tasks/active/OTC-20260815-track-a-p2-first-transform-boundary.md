---
task_id: OTC-20260815-track-a-p2-first-transform-boundary
status: active
agent: ChatGPT
session_id: chatgpt-p2-transform-researcher-20260815-1724
session_role: researcher
session_rotation_count: 1
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: runtime-research
phase: p2-first-transform-boundary
branch: research/OTC-20260815-track-a-p2-first-transform-boundary
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-first-transform-boundary
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 306
updated: 2026-08-15T17:24:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-first-transform-boundary.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/**
  - .github/workflows/tibia-official-client-re-p2-first-transform-boundary.yml
  - .github/scripts/tibia-official-client-re-p2-first-transform-boundary.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - coordinator PR #300 accepted #301/#305 evidence as pinned unmerged dependency only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
implementation_authorized: true
invocation_started_at: 2026-08-15T17:24:00+02:00
last_progress_at: 2026-08-15T17:24:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: p2-first-transform
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: task was ready/unassigned, PR #306 remained open Draft/mergeable at d87a646500832989c57e89f7e1bbf33e5b495bab, current main remained 8fca1c3, and RUNTIME #303 lease was released before this claim
next_action: inspect and complete the existing exact-SHA static reproducer/workflow, execute it on synology-otclient-01, classify the first retained-writer transform edge conservatively, persist machine-readable evidence, require exact-head CI, and release Draft-only result to coordinator #300
---

# Objective

Identify the first concrete serialization/data-transform boundary on the coordinator-accepted `TProtocolClientMessageProcessor -> retained intermediate -> retained shared TProtocolWriter` branch for the exact official native Linux Tibia client.

Research output remains Draft-only. Promotion authority is coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Pinned accepted starting boundary

```text
TProtocolClientMessageProcessor
 -> retained intermediate object (vptr 0x2f69e30, typeinfo 0x3080748)
 -> retained shared TProtocolWriter (vtable AP 0x2f69dd0, RTTI 0x3080728)
```

The intermediate is a separate allocated retained object; the simple secondary/base TProtocolWriter interpretation is disproven. Direct DualConnection writer ownership remains NOT_PROVEN. Exact-binary reproduction overrides pinned coordinator evidence if they conflict.

# Explicit non-duplication boundary

Do not use any of the following as the discriminator:
- final-socket run `31825417040`;
- generic QIODevice::write enumeration;
- generic Qt/QMeta census;
- vtable adjacency alone;
- superseded `0xb5b880`, `0xb46bd0`, `0xc33259` sink models;
- stale writer RTTI `0x3080700`.

# Hypothesis / outcomes

The first concrete call/reference path reachable from the retained writer/intermediate branch either proves a representation-changing serialization/transform edge or boundedly leaves it UNKNOWN.

Allowed semantic outcomes:
1. `TRANSFORM_EDGE_PROVEN`;
2. `SERIALIZATION_ONLY_PROVEN`;
3. `LIFECYCLE_ONLY`;
4. `BYPASS_OR_SPLIT`;
5. `INCONCLUSIVE`.

Any transform/serialization claim requires exact object and call/data provenance. Sequence/framing/compression/encryption ordering remains UNKNOWN unless directly discriminated.

# Planned discriminator

The exact-SHA static reproducer must:
1. revalidate current-main processor/writer/intermediate identities from exact binary structure/relocations;
2. enumerate bounded concrete call/xref sites using the retained intermediate/writer from processor construction/processing paths;
3. recover disassembly around those sites, argument sources, result destinations and resolvable virtual targets;
4. classify representations only when exact evidence supports `generated semantic object`, `typed message object`, `QByteArray/byte buffer`, `device write`, or `UNKNOWN`;
5. update framing/sequence/compression/encryption ordering only where directly supported;
6. prove negative controls against generic QIODevice enumeration, adjacent vtables and superseded sink addresses;
7. emit machine-readable result plus compact evidence with exact binary/tool provenance;
8. separate workflow execution success from semantic result.

# Acceptance gate

- [ ] exact client SHA/size verified by the executing job;
- [ ] current-main #299 and pinned #301/#305 facts independently revalidated;
- [ ] at least one retained-writer call/reference path concretely tied to `TProtocolClientMessageProcessor`, or bounded negative result;
- [ ] claimed transform role has exact call/data provenance;
- [ ] input/output representation is conservative and UNKNOWN preserved where necessary;
- [ ] framing/sequence/compression/encryption ordering changed only with direct evidence;
- [ ] negative controls reject generic QIODevice/vtable/superseded sink models;
- [ ] execution success and semantic result recorded separately;
- [ ] no proprietary client bytes, credentials, account state or secret payloads committed/uploaded;
- [ ] exact-head repository CI terminal before Draft handoff.

# Side-effect budget

Static exact-build analysis only. No login, process attach, gameplay action, movement, packet replay, credential access, account state or runtime mutation is authorized.
