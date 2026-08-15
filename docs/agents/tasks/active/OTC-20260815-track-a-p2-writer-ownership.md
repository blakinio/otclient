---
task_id: OTC-20260815-track-a-p2-writer-ownership
status: ready
agent: unassigned_draft_only_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: runtime-research
phase: p2-writer-ownership
branch: research/OTC-20260815-track-a-p2-writer-ownership
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-writer-ownership
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-ownership.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-writer-ownership/**
  - .github/workflows/tibia-official-client-re-p2-writer-ownership.yml
  - .github/scripts/tibia-official-client-re-p2-writer-ownership.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 / merged PR #299
  - coordinator PR #300 for promotion authority
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
---

# Objective

Resolve the next concrete P2 edge for the exact official native Linux Tibia client without repeating a queued or disproven experiment: recover the concrete ownership/construction/virtual-dispatch path from the already-proven `TGameserverDualConnection` into the actual `TProtocolWriter` / `TIODeviceWriter` writer object.

# Dispatch contract

```yaml
TASK_ID: OTC-20260815-track-a-p2-writer-ownership
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-ownership.md
PROJECT_LANE: otclient
LANE: P2-NETWORK
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: research/OTC-20260815-track-a-p2-writer-ownership
WORKTREE: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-writer-ownership
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-ownership.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-writer-ownership/**
  - .github/workflows/tibia-official-client-re-p2-writer-ownership.yml
  - .github/scripts/tibia-official-client-re-p2-writer-ownership.py
DEPENDENCIES:
  - merged PR #299 canonical P2 reconciliation
  - coordinator PR #300 promotion authority
```

Research output is DRAFT-ONLY. This task cannot promote canonical Track A claims or merge itself.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Every build-specific result must fail closed unless this exact identity is verified first.

# Canonical starting facts

- `TGameserverDualConnection` is on the corrected outbound ownership chain promoted by PR #299.
- `TProtocolWriter : TIODeviceWriter` is exact-build RTTI evidence.
- `TGameserverTCPConnection` and its concrete `QTcpSocket*` member at receiver `+0x10` are proven.
- `0xb46bd0` is not the binary gameplay sink.

# Do not repeat

```text
DISPROVEN/SUPERSEDED:
- owner +0x88 -> 0xb5b880 as the gameplay endpoint
- generic QIODevice::write callsite enumeration as semantic proof
- 0xc33259 as a network/gameplay binary sink

ACTIVE NONCANONICAL QUEUE:
- run 31825417040 final-socket-write resolution remains queued on last coordinator observation
- do not dispatch its conceptual duplicate merely to bypass the queue
```

# Hypothesis

A concrete retained field, constructor path, factory, or virtual dispatch reachable from the proven `TGameserverDualConnection` ownership graph identifies an actual `TProtocolWriter`/`TIODeviceWriter` instance or subobject and discriminates the next outbound transformation edge.

Competing outcomes must be retained:

1. direct writer ownership/reference is proven;
2. writer is indirectly owned by another contained/retained object;
3. the current graph lead does not reach the RTTI-proven writer and is disproven;
4. evidence is insufficient and remains UNKNOWN.

# Acceptance gate

- [ ] exact client identity hard-fenced before ELF/runtime-specific inference;
- [ ] current-main #299 facts are used, not the superseded #289 model;
- [ ] concrete constructor/member/reference/virtual-dispatch evidence ties `TGameserverDualConnection` to the writer type, or a bounded negative result disproves the hypothesis;
- [ ] relocation/RTTI/vtable candidates are validated as Itanium structures, not loose address coincidences;
- [ ] at least one negative control prevents generic symbol/callsite matches from becoming semantic proof;
- [ ] execution success is reported separately from semantic result;
- [ ] no claim is made for framing/encryption/final socket egress unless directly discriminated;
- [ ] artifact/report contains no credentials, proprietary binary bytes, secret-bearing payloads or account state;
- [ ] exact-head repository CI is terminal before Draft handoff.

# Side-effect budget

Static exact-build analysis is preferred. Live execution, if materially needed, must be read-only, task-owned and WARP/SOCKS confined. No gameplay action, currency, market, trade, forge or irreversible effect is authorized by this task.

# Deliverable

Open/update only a Draft PR from this branch with a bounded evidence report and reproducer. Hand it to coordinator PR #300 with one proposed disposition and explicit `FACT | INFERENCE | ASSUMPTION | UNKNOWN | DISPROVEN/SUPERSEDED` classifications.
