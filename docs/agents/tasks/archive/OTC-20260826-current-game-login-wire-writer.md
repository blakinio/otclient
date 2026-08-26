---
task_id: OTC-20260826-current-game-login-wire-writer
status: completed
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
branch: research/OTC-20260826-current-game-login-wire-writer
related_pr: 699
base_branch: main
created: 2026-08-26T17:12:00+02:00
completed: 2026-08-26T21:01:00+02:00
risk: high
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
promotion_authority: coordinator_only
owned_paths: []
modules_touched: []
implementation_authorized: false
---

# Archived source research — current game-login wire writer

Terminal source disposition: **ACCEPT_WITH_EDITS / CLOSED UNMERGED AS SUPERSEDED**.

```text
source PR            #699
research head        3d87d729b73f868aefe1662c72af666a4921b1d8
freeze head          7de745105ce06271ff45bcdf5e5eaf91268008e5
producer run         32998976901 = SUCCESS
artifact             9617908322
artifact digest      sha256:a43ed724d00e18575d969859ad3345d69f2650ee5790d3dbcf13767de1b9ebf4
source CI            32998977749 = SUCCESS
source governance    32998976855 = SUCCESS
freeze CI            33001390982 = SUCCESS
freeze governance    33001390364 = SUCCESS
promotion PR         #706
promotion merge      87730e7116aa1e8be211be4b2443bc9ee6f50d9c
```

The source workflow/analyzer was intentionally not merged. Coordinator PR #706 independently re-downloaded and re-hashed the exact source artifact and promoted only accepted sanitized current-build facts to trusted `main`.

Accepted canonical result now lives under:

- `docs/agents/evidence/OTC-20260826-current-game-login-wire-writer-promotion/20260826-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260826-current-game-login-wire-writer-promotion/result.json`

Current exact public Linux client fence at promotion:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Promoted current facts include `sendLogin` QMeta/adapter/queue vslot, padding, current XTEA mode-2 transform, sequence, final block framing and Qt/QTcpSocket-bound binary writer. The coordinator explicitly withheld queue asynchronous-drain causality, exact current generated login-message field schema, final OS syscall and a causal explanation of Track B's structured `0x14`.

No official-client runtime, login, credentials, session values, process memory, packet capture, proprietary binary upload or Track B mutation occurred in this source task.

```yaml
closeout:
  source_pr_terminal: CLOSED_UNMERGED_SUPERSEDED
  coordinator_decision: ACCEPT_WITH_EDITS
  promoted_to_trusted_main: true
  promotion_pr: 706
  promotion_merge: 87730e7116aa1e8be211be4b2443bc9ee6f50d9c
  audit_result: PASS_BOUNDED
  material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: static exact-file protocol reconstruction only
  ownership_released: true
  blocker: none
  next_action: none
```
